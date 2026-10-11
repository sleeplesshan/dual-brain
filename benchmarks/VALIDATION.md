# v1.5.0 validation — 2026-10-11

This records observed checks, not a claim of optimal performance across models.

## Environment observed

- Codex desktop: 26.1007.21159, build 20052, prod channel.
- Codex CLI: 0.162.1; its `exec --help` confirmed the options used by the harness.
- Desktop update checker returned `busy`; no claim that the installed app is the latest eligible release.
- Model guidance was checked against official [models](https://learn.chatgpt.com/docs/models), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [skills](https://developers.openai.com/codex/skills), and [non-interactive CLI](https://developers.openai.com/codex/noninteractive) documentation. Availability remains runtime-dependent.

## Checks performed

- Bundled skill-creator `quick_validate.py`: passed.
- `python3 -m unittest discover -s benchmarks/tests -v`: 7 passed, including synthetic CLI JSON events, token accounting, snapshots, failure gating, effort forwarding, and honest report output.
- `python3 benchmarks/bench.py run --suite core5 --dry-run`: planned 15 cases; no live suite calls.
- `git diff --check`: passed.
- Independent source review identified and corrected ambiguous descendant-agent wording and the benchmark's overstatement of causal isolation.

## Behavioral forward test

A fresh-context evaluator received only the candidate skill/resources, an isolated copy of the access-control fixture, and a request to centralize authorization while preserving route behavior and allowing owner billing. Delegation was explicitly unavailable in this test.

Observed outcome: the agent disclosed a single-agent fallback, implemented `POLICIES` with thin route delegates, preserved owner denial on existing routes, and passed six local tests including added compatibility/default-denial checks. It updated four influential memory entries once each, added evidence, and preserved unrelated Cold/Archived entries.

A follow-up read-only review explicitly superseded owner-only billing with owner/admin billing. The agent proposed the precise code/test and memory changes, respected the user's override, distinguished the requested decision from current code, and made no file edits.

These checks exercise implementation, memory, explicit override, and read-only fallback behavior. They do not validate every native delegation path, lifecycle recovery, host, or model.

## Size and measurement limits

The entrypoint shrank from 20,030 bytes to approximately 5,500 bytes (about 73%). Conditional runtime and memory references are additional context when loaded. This is a static source-size reduction, not a measured token, latency, or quality improvement.

No full live model matrix was run. Existing historical results are not comparable to the corrected harness without rerunning them. Equal initial memory reduces one confound, but differences in detailed instructions and actual delegation still require inspection. Raw smoke artifacts were kept outside the repository; the outcome above is a validation record, not a reproducible performance dataset.
