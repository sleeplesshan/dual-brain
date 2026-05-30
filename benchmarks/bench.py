#!/usr/bin/env python3
"""Benchmark Dual-Brain against a single-agent baseline in Codex.

Scenario files are JSON-compatible YAML. Keeping the extension as `.yaml`
matches the public benchmark shape while avoiding a PyYAML dependency.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import selectors
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BENCH_ROOT = ROOT / "benchmarks"
SCENARIOS_DIR = BENCH_ROOT / "scenarios"
FIXTURES_DIR = BENCH_ROOT / "fixtures"
RUNS_DIR = BENCH_ROOT / "runs"

MATRIX = {
    "codex_single_no_memory": ("codex", "single"),
    "codex_dual_memory": ("codex", "dual"),
    "claude_single_no_memory": ("claude", "single"),
    "claude_dual_memory": ("claude", "dual"),
}

DEFAULT_MATRIX = ["codex_single_no_memory", "codex_dual_memory"]
COMPATIBILITY_MATRIX = ["claude_single_no_memory", "claude_dual_memory"]
FULL_MATRIX = DEFAULT_MATRIX + COMPATIBILITY_MATRIX

SUITES = {
    "core5": [
        ("notifications", "main"),
        ("notifications", "trap"),
        ("billing", "trap"),
        ("notifications", "memory"),
        ("access_control", "memory"),
    ]
}


@dataclass
class AgentRun:
    env: str
    strategy: str
    attempt: int
    prompt: str
    command: list[str]
    returncode: int
    started_at: str
    ended_at: str
    wall_time_ms: int
    ttft_ms: int | None
    input_tokens: int = 0
    cached_input_tokens: int = 0
    output_tokens: int = 0
    reasoning_output_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float | None = None
    session_id: str | None = None
    stdout_path: str | None = None
    stderr_path: str | None = None
    final_text: str = ""
    raw_usage: dict[str, Any] = field(default_factory=dict)


def now_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_scenario(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"{path} must be JSON-compatible YAML so the harness stays dependency-free: {exc}"
        ) from exc
    data["_path"] = str(path)
    return data


def load_scenarios(selection: str) -> list[dict[str, Any]]:
    all_paths = sorted(SCENARIOS_DIR.glob("*.yaml"))
    scenarios = [load_scenario(path) for path in all_paths]
    if selection == "all":
        return scenarios
    selected = [s for s in scenarios if s["id"] == selection]
    if not selected:
        known = ", ".join(s["id"] for s in scenarios)
        raise SystemExit(f"Unknown scenario {selection!r}. Known scenarios: {known}")
    return selected


def expand_matrix(selection: str, include_claude: bool = False) -> list[str]:
    if selection == "default":
        return DEFAULT_MATRIX + (COMPATIBILITY_MATRIX if include_claude else [])
    if selection == "all":
        return FULL_MATRIX
    if selection == "compatibility":
        return COMPATIBILITY_MATRIX
    names = [name.strip() for name in selection.split(",") if name.strip()]
    unknown = [name for name in names if name not in MATRIX]
    if unknown:
        raise SystemExit(f"Unknown matrix entries: {', '.join(unknown)}")
    return names


def expand_methods(selection: str) -> list[str]:
    if selection == "all":
        return ["main", "trap", "memory"]
    methods = [m.strip() for m in selection.split(",") if m.strip()]
    unknown = [m for m in methods if m not in {"main", "trap", "memory"}]
    if unknown:
        raise SystemExit(f"Unknown methods: {', '.join(unknown)}")
    return methods


def expand_suite(selection: str) -> list[tuple[str, str]]:
    if selection in SUITES:
        return SUITES[selection]
    raise SystemExit(f"Unknown suite {selection!r}. Known suites: {', '.join(SUITES)}")


def run_shell(command: str, cwd: Path, timeout: int) -> dict[str, Any]:
    start = time.monotonic()
    proc = subprocess.run(
        command,
        cwd=cwd,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "wall_time_ms": int((time.monotonic() - start) * 1000),
    }


def copy_fixture(scenario: dict[str, Any], dest: Path) -> None:
    fixture = FIXTURES_DIR / scenario["fixture"]
    if not fixture.exists():
        raise SystemExit(f"Missing fixture: {fixture}")
    shutil.copytree(fixture, dest)
    run_shell("git init -q", dest, timeout=30)
    run_shell('git config user.name "Benchmark Bot"', dest, timeout=30)
    run_shell('git config user.email "benchmark@example.invalid"', dest, timeout=30)
    run_shell("git add . && git commit -qm baseline", dest, timeout=30)


def prepare_workspace_for_strategy(repo: Path, strategy: str) -> bool:
    """Return whether project memory is available to the agent."""
    memory_dir = repo / ".dual-brain"
    if strategy == "single":
        if memory_dir.exists():
            shutil.rmtree(memory_dir)
            run_shell("git add -A && git commit -qm single-baseline-without-memory", repo, timeout=30)
        return False
    return (memory_dir / "MEMORY.md").exists()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_prompt(scenario: dict[str, Any], method: str, strategy: str, repair: str | None = None, session_index: int | None = None) -> str:
    prompts = scenario["prompts"]
    if method == "memory":
        base = prompts["memory_sessions"][session_index or 0]
    else:
        base = prompts[method]

    guard = (
        "You are running inside an automated benchmark sandbox. "
        "Modify the repository directly. Run or reason against the provided tests. "
        "Do not ask the human for clarification; make the smallest safe implementation that satisfies the task. "
        "Finish with a concise summary of changed files and verification."
    )
    if strategy == "dual":
        mode = (
            "Use dual-brain for this task. Follow Memory Intake, Right Brain Grill, "
            "Left Brain Verify, Dual Synthesis, and Memory Auto-Save. "
            "For benchmark automation, update .dual-brain/MEMORY.md directly when durable non-sensitive memory changes, "
            "preserve Hot/Warm/Cold/Archived tiers when present, and mention any refs/last_referenced/last_verified updates in the final response."
        )
    else:
        mode = (
            "Use a traditional single-agent approach. Do not invoke dual-brain, do not simulate a two-agent debate, "
            "and do not use the Right Brain / Left Brain protocol. The benchmark workspace intentionally does not "
            "include `.dual-brain/MEMORY.md`; do not assume hidden project memory. Respond and implement as one direct coding agent."
        )
    if repair:
        return f"{guard}\n\n{mode}\n\nRepair the previous attempt. Test/evaluator output:\n\n{repair}\n\nOriginal task:\n{base}"
    return f"{guard}\n\n{mode}\n\nTask:\n{base}"


class CodexAdapter:
    def __init__(self, model: str | None = None, dangerous: bool = False):
        self.model = model
        self.dangerous = dangerous

    def run(self, repo: Path, prompt: str, out_dir: Path, attempt: int, timeout: int, strategy: str) -> AgentRun:
        cmd = ["codex", "exec", "--json", "--ephemeral", "--sandbox", "workspace-write", "--cd", str(repo)]
        if self.model:
            cmd.extend(["--model", self.model])
        if self.dangerous:
            cmd.append("--dangerously-bypass-approvals-and-sandbox")
        cmd.append(prompt)
        return run_codex(cmd, out_dir, attempt, prompt, timeout, strategy)


class ClaudeAdapter:
    def __init__(self, model: str | None = None, dangerous: bool = False):
        self.model = model
        self.dangerous = dangerous

    def run(self, repo: Path, prompt: str, out_dir: Path, attempt: int, timeout: int, strategy: str) -> AgentRun:
        cmd = ["claude", "-p", "--output-format", "json", "--permission-mode", "acceptEdits"]
        if strategy == "single":
            cmd.append("--disable-slash-commands")
        if self.model:
            cmd.extend(["--model", self.model])
        if self.dangerous:
            cmd.append("--dangerously-skip-permissions")
        cmd.append(prompt)
        return run_claude(cmd, repo, out_dir, attempt, prompt, timeout, strategy)


def run_codex(cmd: list[str], out_dir: Path, attempt: int, prompt: str, timeout: int, strategy: str) -> AgentRun:
    stdout_path = out_dir / f"agent_attempt_{attempt}.jsonl"
    stderr_path = out_dir / f"agent_attempt_{attempt}.stderr.log"
    started_at = iso_now()
    start = time.monotonic()
    first_message_ms: int | None = None
    final_text_parts: list[str] = []
    final_usage: dict[str, Any] = {}
    thread_id = None

    proc = subprocess.Popen(
        cmd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
    )
    stdout_lines: list[str] = []
    stderr_lines: list[str] = []
    sel = selectors.DefaultSelector()
    assert proc.stdout is not None
    assert proc.stderr is not None
    sel.register(proc.stdout, selectors.EVENT_READ, "stdout")
    sel.register(proc.stderr, selectors.EVENT_READ, "stderr")
    deadline = start + timeout
    returncode = None
    while sel.get_map():
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            proc.kill()
            returncode = 124
            stderr_lines.append("Timed out\n")
            break
        for key, _ in sel.select(timeout=min(0.25, remaining)):
            line = key.fileobj.readline()
            if line == "":
                sel.unregister(key.fileobj)
                continue
            if key.data == "stderr":
                stderr_lines.append(line)
                continue
            stdout_lines.append(line)
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "thread.started":
                thread_id = event.get("thread_id")
            item = event.get("item") or {}
            if item.get("type") == "agent_message":
                if first_message_ms is None:
                    first_message_ms = int((time.monotonic() - start) * 1000)
                final_text_parts.append(item.get("text", ""))
            if event.get("type") == "turn.completed":
                final_usage = event.get("usage") or {}
        if proc.poll() is not None and not sel.get_map():
            break
    if returncode is None:
        returncode = proc.wait(timeout=1)
    ended_at = iso_now()
    wall_ms = int((time.monotonic() - start) * 1000)
    write_text(stdout_path, "".join(stdout_lines))
    write_text(stderr_path, "".join(stderr_lines))
    input_tokens = int(final_usage.get("input_tokens") or 0)
    cached = int(final_usage.get("cached_input_tokens") or 0)
    output_tokens = int(final_usage.get("output_tokens") or 0)
    reasoning = int(final_usage.get("reasoning_output_tokens") or 0)
    return AgentRun(
        env="codex",
        strategy=strategy,
        attempt=attempt,
        prompt=prompt,
        command=cmd,
        returncode=returncode,
        started_at=started_at,
        ended_at=ended_at,
        wall_time_ms=wall_ms,
        ttft_ms=first_message_ms,
        input_tokens=input_tokens,
        cached_input_tokens=cached,
        output_tokens=output_tokens,
        reasoning_output_tokens=reasoning,
        total_tokens=input_tokens + cached + output_tokens + reasoning,
        session_id=thread_id,
        stdout_path=str(stdout_path),
        stderr_path=str(stderr_path),
        final_text="\n".join(final_text_parts),
        raw_usage=final_usage,
    )


def run_claude(cmd: list[str], repo: Path, out_dir: Path, attempt: int, prompt: str, timeout: int, strategy: str) -> AgentRun:
    stdout_path = out_dir / f"agent_attempt_{attempt}.json"
    stderr_path = out_dir / f"agent_attempt_{attempt}.stderr.log"
    started_at = iso_now()
    start = time.monotonic()
    proc = subprocess.run(
        cmd,
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    ended_at = iso_now()
    wall_ms = int((time.monotonic() - start) * 1000)
    write_text(stdout_path, proc.stdout)
    write_text(stderr_path, proc.stderr)
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        data = {}
    usage = data.get("usage") or {}
    input_tokens = int(usage.get("input_tokens") or 0)
    cache_create = int(usage.get("cache_creation_input_tokens") or 0)
    cache_read = int(usage.get("cache_read_input_tokens") or 0)
    output_tokens = int(usage.get("output_tokens") or 0)
    return AgentRun(
        env="claude",
        strategy=strategy,
        attempt=attempt,
        prompt=prompt,
        command=cmd,
        returncode=proc.returncode,
        started_at=started_at,
        ended_at=ended_at,
        wall_time_ms=wall_ms,
        ttft_ms=data.get("ttft_ms"),
        input_tokens=input_tokens,
        cached_input_tokens=cache_create + cache_read,
        output_tokens=output_tokens,
        reasoning_output_tokens=0,
        total_tokens=input_tokens + cache_create + cache_read + output_tokens,
        cost_usd=data.get("total_cost_usd"),
        session_id=data.get("session_id"),
        stdout_path=str(stdout_path),
        stderr_path=str(stderr_path),
        final_text=data.get("result") or "",
        raw_usage={"usage": usage, "modelUsage": data.get("modelUsage")},
    )


def run_evaluator(repo: Path, scenario: dict[str, Any], mode: str, transcript: str, out_dir: Path) -> dict[str, Any]:
    transcript_path = out_dir / f"{mode}_transcript.txt"
    write_text(transcript_path, transcript)
    cmd = [
        sys.executable,
        str(BENCH_ROOT / "evaluators" / "evaluate.py"),
        "--scenario",
        scenario["id"],
        "--mode",
        mode,
        "--repo",
        str(repo),
        "--transcript",
        str(transcript_path),
    ]
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=ROOT)
    write_text(out_dir / f"{mode}_evaluator.stdout.json", proc.stdout)
    write_text(out_dir / f"{mode}_evaluator.stderr.log", proc.stderr)
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        data = {"passed": False, "error": "invalid evaluator output", "stdout": proc.stdout, "stderr": proc.stderr}
    data["returncode"] = proc.returncode
    return data


def git_diff(repo: Path) -> str:
    proc = subprocess.run(["git", "diff", "--", "."], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout


def run_one(
    scenario: dict[str, Any],
    matrix_name: str,
    method: str,
    repetition: int,
    run_root: Path,
    args: argparse.Namespace,
) -> dict[str, Any]:
    env, strategy = MATRIX[matrix_name]
    case_dir = run_root / scenario["id"] / method / matrix_name / f"rep_{repetition}"
    repo = case_dir / "repo"
    logs = case_dir / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    copy_fixture(scenario, repo)
    memory_available = prepare_workspace_for_strategy(repo, strategy)

    adapter = (
        CodexAdapter(args.codex_model, args.dangerous)
        if env == "codex"
        else ClaudeAdapter(args.claude_model, args.dangerous)
    )

    initial_test = run_shell(scenario["test_command"], repo, timeout=args.test_timeout)
    write_text(logs / "initial_test.stdout.log", initial_test["stdout"])
    write_text(logs / "initial_test.stderr.log", initial_test["stderr"])

    attempts: list[AgentRun] = []
    final_test = initial_test
    final_eval: dict[str, Any] = {"passed": False}
    transcript = ""
    passed = False

    if method == "memory":
        session_prompts = scenario["prompts"]["memory_sessions"]
        for idx, _ in enumerate(session_prompts):
            prompt = build_prompt(scenario, method, strategy, session_index=idx)
            agent = adapter.run(repo, prompt, logs, idx + 1, args.agent_timeout, strategy)
            attempts.append(agent)
            transcript += f"\n\n--- SESSION {idx + 1} ---\n{agent.final_text}\n"
            session_test = run_shell(scenario["test_command"], repo, timeout=args.test_timeout)
            write_text(logs / f"session_{idx + 1}_test.stdout.log", session_test["stdout"])
            write_text(logs / f"session_{idx + 1}_test.stderr.log", session_test["stderr"])
        final_test = run_shell(scenario["test_command"], repo, timeout=args.test_timeout)
        final_eval = run_evaluator(repo, scenario, "memory", transcript, logs)
        passed = final_test["returncode"] == 0 and bool(final_eval.get("passed"))
    else:
        repair_text = None
        for attempt in range(args.max_repair_loops + 1):
            prompt = build_prompt(scenario, method, strategy, repair=repair_text)
            agent = adapter.run(repo, prompt, logs, attempt + 1, args.agent_timeout, strategy)
            attempts.append(agent)
            transcript += f"\n\n--- ATTEMPT {attempt + 1} ---\n{agent.final_text}\n"
            final_test = run_shell(scenario["test_command"], repo, timeout=args.test_timeout)
            write_text(logs / f"test_attempt_{attempt + 1}.stdout.log", final_test["stdout"])
            write_text(logs / f"test_attempt_{attempt + 1}.stderr.log", final_test["stderr"])
            final_eval = run_evaluator(repo, scenario, method, transcript, logs)
            passed = final_test["returncode"] == 0 and bool(final_eval.get("passed"))
            if passed:
                break
            repair_text = (
                f"Test command: {scenario['test_command']}\n"
                f"Return code: {final_test['returncode']}\n"
                f"STDOUT:\n{final_test['stdout']}\n"
                f"STDERR:\n{final_test['stderr']}\n"
                f"Evaluator:\n{json.dumps(final_eval, indent=2)}"
            )

    diff = git_diff(repo)
    write_text(logs / "final.diff", diff)
    total_wall = sum(a.wall_time_ms for a in attempts) + int(final_test.get("wall_time_ms") or 0)
    tokens = {
        "input_tokens": sum(a.input_tokens for a in attempts),
        "cached_input_tokens": sum(a.cached_input_tokens for a in attempts),
        "output_tokens": sum(a.output_tokens for a in attempts),
        "reasoning_output_tokens": sum(a.reasoning_output_tokens for a in attempts),
        "total_tokens": sum(a.total_tokens for a in attempts),
    }
    result = {
        "scenario": scenario["id"],
        "method": method,
        "matrix": matrix_name,
        "environment": env,
        "strategy": strategy,
        "memory_available": memory_available,
        "repetition": repetition,
        "passed": passed,
        "first_pass": passed and len(attempts) == (3 if method == "memory" else 1),
        "repair_loops": max(0, len(attempts) - (3 if method == "memory" else 1)),
        "attempts": [a.__dict__ for a in attempts],
        "ttft_ms_first_attempt": attempts[0].ttft_ms if attempts else None,
        "agent_wall_time_ms": sum(a.wall_time_ms for a in attempts),
        "total_wall_time_ms": total_wall,
        "tokens": tokens,
        "cost_usd": sum(a.cost_usd or 0 for a in attempts) or None,
        "initial_test": scrub_process(initial_test),
        "final_test": scrub_process(final_test),
        "evaluator": final_eval,
        "raw_dir": str(case_dir.relative_to(run_root)),
    }
    write_text(case_dir / "result.json", json.dumps(result, indent=2))
    return result


def scrub_process(data: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in data.items() if k in {"command", "returncode", "wall_time_ms"}}


def summarize(results: list[dict[str, Any]], run_root: Path) -> None:
    write_text(run_root / "results.json", json.dumps(results, indent=2))
    lines = ["# Dual-Brain Benchmark Results", ""]
    lines.append(f"Run directory: `{run_root}`")
    lines.append("")
    lines.append("## Quality Summary")
    lines.append("")
    lines.append("| Scenario | Method | Strategy | Memory | Pass | First pass | Repair loops | Raw |")
    lines.append("|---|---|---|---:|---:|---:|---:|---|")
    for row in results:
        lines.append(
            "| {scenario} | {method} | {strategy} | {memory} | {passed} | {first_pass} | {loops} | `{raw}` |".format(
                scenario=row["scenario"],
                method=row["method"],
                strategy=row["matrix"],
                memory="✅" if row.get("memory_available") else "❌",
                passed="✅" if row["passed"] else "❌",
                first_pass="✅" if row.get("first_pass") else "❌",
                loops=row.get("repair_loops", ""),
                raw=row.get("raw_dir", ""),
            )
        )
    lines.append("")
    lines.append("## Human Iteration Avoidance")
    lines.append("")
    lines.append(
        "This is the primary readout: did Dual-Brain prevent the kind of agent mistakes "
        "that usually force a human to re-prompt, repair, or re-litigate architecture?"
    )
    lines.append("")
    lines.append("| Strategy | Pass rate | First-pass correctness | Human repair prompts | Trap failures | Memory regressions |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for matrix_name in sorted({row["matrix"] for row in results}):
        rows = [row for row in results if row["matrix"] == matrix_name]
        trap_rows = [row for row in rows if row["method"] == "trap"]
        memory_rows = [row for row in rows if row["method"] == "memory"]
        lines.append(
            "| {strategy} | {passes}/{total} | {first}/{total} | {repairs} | {trap_failures}/{trap_total} | {memory_failures}/{memory_total} |".format(
                strategy=matrix_name,
                passes=sum(1 for row in rows if row["passed"]),
                first=sum(1 for row in rows if row.get("first_pass")),
                total=len(rows),
                repairs=sum(row.get("repair_loops", 0) for row in rows),
                trap_failures=sum(1 for row in trap_rows if not row["passed"]),
                trap_total=len(trap_rows),
                memory_failures=sum(1 for row in memory_rows if not row["passed"]),
                memory_total=len(memory_rows),
            )
        )
    single_rows = [row for row in results if row["matrix"] == "codex_single_no_memory"]
    dual_rows = [row for row in results if row["matrix"] == "codex_dual_memory"]
    if single_rows and dual_rows:
        single_repairs = sum(row.get("repair_loops", 0) for row in single_rows)
        dual_repairs = sum(row.get("repair_loops", 0) for row in dual_rows)
        single_memory_regressions = sum(1 for row in single_rows if row["method"] == "memory" and not row["passed"])
        dual_memory_regressions = sum(1 for row in dual_rows if row["method"] == "memory" and not row["passed"])
        lines.append("")
        lines.append(
            "In this run, Dual-Brain reduced repair prompts from "
            f"{single_repairs} to {dual_repairs} and memory regressions from "
            f"{single_memory_regressions} to {dual_memory_regressions}. "
            "That is the practical claim: spend more reasoning up front to avoid extra human correction loops later."
        )
    lines.append("")
    lines.append("## Trap Defense")
    lines.append("")
    lines.append("| Scenario | Matrix | Defended | Evidence |")
    lines.append("|---|---|---:|---|")
    for row in [r for r in results if r["method"] == "trap"]:
        ev = row.get("evaluator", {})
        lines.append(
            f"| {row['scenario']} | {row['matrix']} | {'✅' if row['passed'] else '❌'} | {escape_md('; '.join(ev.get('messages', [])[:3]))} |"
        )
    lines.append("")
    lines.append("## Memory Persistence")
    lines.append("")
    lines.append("| Scenario | Matrix | Persisted | Evidence |")
    lines.append("|---|---|---:|---|")
    for row in [r for r in results if r["method"] == "memory"]:
        ev = row.get("evaluator", {})
        lines.append(
            f"| {row['scenario']} | {row['matrix']} | {'✅' if row['passed'] else '❌'} | {escape_md('; '.join(ev.get('messages', [])[:3]))} |"
        )
    lines.append("")
    lines.append("## Cost Summary")
    lines.append("")
    lines.append("Time and tokens are retained as overhead/cost indicators. They are not the primary success criteria.")
    lines.append("")
    lines.append("| Scenario | Method | Strategy | TTFT ms | Total ms | Tokens | Cost USD |")
    lines.append("|---|---|---|---:|---:|---:|---:|")
    for row in results:
        lines.append(
            "| {scenario} | {method} | {strategy} | {ttft} | {wall} | {tokens} | {cost} |".format(
                scenario=row["scenario"],
                method=row["method"],
                strategy=row["matrix"],
                ttft=row.get("ttft_ms_first_attempt") if row.get("ttft_ms_first_attempt") is not None else "",
                wall=row.get("total_wall_time_ms", ""),
                tokens=row.get("tokens", {}).get("total_tokens", ""),
                cost=f"{row['cost_usd']:.4f}" if row.get("cost_usd") else "",
            )
        )
    lines.append("")
    lines.append("## Benchmark Question")
    lines.append("")
    lines.append(
        "The benchmark is not trying to prove that Dual-Brain is faster per attempt. "
        "It is expected to spend more time and tokens. The question is whether that "
        "up-front reasoning cost prevents the mistakes that make a human run the agent again: "
        "repair prompts, hallucinated APIs, stale assumptions, and architecture regressions."
    )
    lines.append("")
    write_text(run_root / "benchmark_results.md", "\n".join(lines))


def escape_md(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def cmd_list(_: argparse.Namespace) -> None:
    for scenario in load_scenarios("all"):
        print(f"{scenario['id']}: {scenario.get('title', '')}")


def cmd_run(args: argparse.Namespace) -> None:
    run_root = RUNS_DIR / now_id()
    run_root.mkdir(parents=True, exist_ok=True)
    if args.suite:
        suite_cases = expand_suite(args.suite)
    else:
        suite_cases = [(scenario["id"], method) for scenario in load_scenarios(args.scenario) for method in expand_methods(args.method)]
    scenario_by_id = {scenario["id"]: scenario for scenario in load_scenarios("all")}
    matrix_entries = expand_matrix(args.matrix, include_claude=args.include_claude)
    results = []
    for scenario_id, method in suite_cases:
        scenario = scenario_by_id[scenario_id]
        for matrix_name in matrix_entries:
            for rep in range(1, args.repetitions + 1):
                print(f"Running {scenario['id']} / {method} / {matrix_name} / rep {rep}", flush=True)
                if args.dry_run:
                    continue
                results.append(run_one(scenario, matrix_name, method, rep, run_root, args))
                summarize(results, run_root)
    if args.dry_run:
        print(f"Dry run planned {len(suite_cases) * len(matrix_entries) * args.repetitions} cases")
    else:
        summarize(results, run_root)
        print(run_root)


def cmd_summarize(args: argparse.Namespace) -> None:
    run_root = Path(args.run_dir)
    result_paths = sorted(run_root.glob("**/result.json"))
    results = [json.loads(path.read_text(encoding="utf-8")) for path in result_paths]
    summarize(results, run_root)
    print(run_root / "benchmark_results.md")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Dual-Brain benchmarks")
    sub = parser.add_subparsers(required=True)
    list_p = sub.add_parser("list")
    list_p.set_defaults(func=cmd_list)

    run_p = sub.add_parser("run")
    run_p.add_argument("--suite", default="core5", help="core5 by default; omit with --suite '' to use scenario/method")
    run_p.add_argument("--scenario", default="all")
    run_p.add_argument("--method", default="all", help="all, main, trap, memory, or comma-separated")
    run_p.add_argument("--matrix", default="default", help="default, all, compatibility, or comma-separated matrix entries")
    run_p.add_argument("--include-claude", action="store_true", help="Add Claude compatibility entries to the default Codex matrix")
    run_p.add_argument("--repetitions", type=int, default=1)
    run_p.add_argument("--max-repair-loops", type=int, default=2)
    run_p.add_argument("--agent-timeout", type=int, default=900)
    run_p.add_argument("--test-timeout", type=int, default=120)
    run_p.add_argument("--codex-model")
    run_p.add_argument("--claude-model")
    run_p.add_argument("--dangerous", action="store_true", help="Use CLI permission bypass flags where available")
    run_p.add_argument("--dry-run", action="store_true")
    run_p.set_defaults(func=cmd_run)

    sum_p = sub.add_parser("summarize")
    sum_p.add_argument("run_dir")
    sum_p.set_defaults(func=cmd_summarize)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
