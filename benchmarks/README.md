# Dual-Brain Benchmark Harness

This directory contains a reproducible benchmark scaffold for comparing:

- Codex `single-agent` vs. Codex `dual-brain`
- quality gains vs. reasoning overhead
- hallucination defense under trap prompts
- multi-session memory persistence via `.dual-brain/MEMORY.md`

The benchmark question is not "is Dual-Brain faster?" Dual-Brain is expected to spend more time and tokens. The question is whether that extra reasoning cost buys fewer human correction loops, better trap defense, and less architecture/memory regression.

The harness is intentionally plain Python: no package install, no hidden telemetry, no external test runner beyond the local CLIs and each fixture's own tests.

## Quick Start

List available scenarios:

```bash
python3 benchmarks/bench.py list
```

Run the default five-case suite:

```bash
python3 benchmarks/bench.py run --suite core5
```

Preview the suite without spending model time:

```bash
python3 benchmarks/bench.py run --suite core5 --dry-run
```

Summarize an existing run:

```bash
python3 benchmarks/bench.py summarize benchmarks/runs/<run-id>
```

## Core Suite

`core5` runs five benchmark cases:

- `notifications/main`
- `notifications/trap`
- `billing/trap`
- `notifications/memory`
- `access_control/memory`

Each case runs two strategies:

- `codex_single_no_memory`
- `codex_dual_memory`

That keeps the default run short enough to repeat, while still covering ordinary refactoring, trap-prompt defense, and memory persistence.

## Matrix

The default matrix is Codex-only:

- `codex_single_no_memory`
- `codex_dual_memory`

Single-agent workspaces remove `.dual-brain/` before the agent runs, so the baseline cannot use Dual-Brain project memory. Dual-Brain workspaces keep `.dual-brain/MEMORY.md`.

Claude Code entries are available only as optional compatibility runs:

```bash
python3 benchmarks/bench.py run --suite core5 --include-claude
python3 benchmarks/bench.py run --suite core5 --matrix compatibility
```

## Outputs

Each run writes:

- `results.json`
- `benchmark_results.md`
- per-attempt raw CLI logs
- test output
- evaluator output
- git diffs

The Markdown file is the artifact to read first; the JSON file is for plotting or later analysis.

See [RESULTS.md](RESULTS.md) for a tracked early benchmark snapshot. Raw run directories are local-only and ignored by Git.

The Markdown report is quality-first:

- pass/fail
- first-pass correctness
- repair loops
- trap defense
- memory persistence
- separate cost summary for TTFT, wall-clock time, tokens, and cost when available

## Safety

The harness copies fixtures into isolated workspaces under `benchmarks/runs/`. It initializes a fresh Git repo per attempt so diffs are easy to inspect. It does not depend on hidden platform telemetry; token counts come from CLI JSON when exposed.

`benchmarks/runs/` is intentionally ignored. Treat it as local raw evidence: useful for inspection, too bulky and environment-specific for the repository.
