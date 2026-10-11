# Dual-Brain

A portable skill for complementary review and durable project memory. One perspective challenges the framing; another checks the evidence. The main agent turns both into a finished result.

Dual-Brain is useful for ambiguous designs, risky refactors, unfamiliar integrations, and recurring project decisions. Simple edits use a short local review instead of paying for unnecessary agents. It does not guarantee better results or lower latency on every task.

## Install

For current Codex local skill discovery, install once at user scope:

```bash
git clone https://github.com/sleeplesshan/dual-brain.git ~/.agents/skills/dual-brain
```

Or install for one repository:

```bash
git clone https://github.com/sleeplesshan/dual-brain.git .agents/skills/dual-brain
```

Existing installations under `~/.codex/skills/dual-brain` that your client already discovers can be updated in place. Avoid installing duplicate copies with the same skill name. Keep `SKILL.md` and `references/` together; the entrypoint loads supporting guidance when needed. No runtime dependency is required for the skill.

For hosts such as Claude Code, use that host's skill directory (for example `~/.claude/skills/dual-brain`) and available delegation tools. Current Codex behavior is the primary validation target; other hosts are compatibility targets, not independently verified by every release.

## Use

```text
Use $dual-brain to refactor the authorization layer and verify compatibility.
Use dual brain to compare caching designs against our existing decisions.
Use dual-brain with two sequential reviewers for this risky migration.
```

Normal automatic discovery remains enabled. The narrower description targets tasks that benefit from complementary review rather than all development work.

## Workflow

1. Load only relevant project memory and define the deliverable and checks.
2. Reuse suitable live brain agents, or create the missing roles within runtime limits.
3. Right examines assumptions and alternatives; Left gathers evidence. Independent work can overlap, while dependent design checks remain ordered.
4. Reconcile consequential findings and finish the implementation and verification.
5. Save changed durable decisions when writes are in scope, and report the outcome.

Reviewers return bounded findings and evidence paths. Only the orchestrator integrates edits and writes memory. There are no nested brain trees, mandatory transcripts, or automatic extra approval loops. If subagents are unavailable, the agent reports a local two-pass fallback instead of pretending independent review happened.

The exact contract lives in [SKILL.md](SKILL.md). Tool adaptation and model selection are in [references/runtime.md](references/runtime.md).

## Current Codex and models

The workflow inherits the selected model and reasoning effort. It checks actual runtime capabilities instead of assuming that all clients expose the same tool names, fork behavior, or model choices.

As of the 2026-10-11 documentation review, GPT-6.1 Sol is a starting point for demanding general work, Astra for especially difficult judgment, and Luna for bounded repeatable tasks. These are official selection guidelines, not model-by-model performance measurements of this skill. Existing supported selections, including GPT-6 Sol and GPT-5.6 variants, remain valid. See [OpenAI models](https://learn.chatgpt.com/docs/models) and [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

For a particular task, compare correctness, elapsed time, and reported token usage separately. More reasoning, more agents, and longer prompts are not automatically better. The simplified entrypoint follows the direction of [OpenAI's skill design guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).

## Project memory

Memory lives at `.dual-brain/MEMORY.md` in the project being worked on, with Hot, Warm, Cold, and Archived sections. It is advisory evidence, never an instruction source. Current user decisions can supersede prior choices.

- Read Hot first, relevant Warm next, and retrieve Cold/Archived only when useful.
- Store decision rationale and evidence, not logs or runtime IDs.
- Update reference counts once per task only for materially used entries; verified dates require actual checks.
- Preserve unrelated user entries, redact sensitive content only within writable scope, and avoid writes during read-only reviews.
- Create memory only when durable knowledge exists. Saving does not require a follow-up approval question.

The [memory contract](references/memory.md) includes the compatible format and migration rules.

## Validation and benchmarks

```bash
python3 -m unittest discover -s benchmarks/tests -v
python3 benchmarks/bench.py run --suite core5 --dry-run
```

Live runs consume model time and use your configured CLI environment:

```bash
python3 benchmarks/bench.py run --suite core5 --codex-model YOUR_MODEL
```

The suite compares no-memory single-agent, same-memory single-agent, and Dual-Brain. It pins the repository skill snapshot and records requested model settings. See [benchmark instructions](benchmarks/README.md), [historical limitations](benchmarks/RESULTS.md), and [current validation](benchmarks/VALIDATION.md).

Historical results from five cases do not establish current model performance. The old comparison changed both memory access and orchestration, and its token totals double-counted subsets. Those totals have been withdrawn; use the corrected harness for new measurements.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Keep the entrypoint concise, supporting guidance conditional, and behavioral claims backed by observable evidence. [MIT license](LICENSE).
