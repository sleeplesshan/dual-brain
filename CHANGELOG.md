# Changelog

## v1.4.0 — Reusable Brain Agents

Dual-Brain now reuses active Right Brain and Left Brain sub-agents when the runtime exposes reusable agent handles, instead of blindly spawning fresh brains on every skill invocation.

- Adds **Step 0C — Sub-Agent Reuse Check** before the Right Brain pass.
- Reuses active Right/Left Brain agents inside the current conversation/runtime when available.
- Resumes closed-but-resumable brain agents when the platform supports it.
- Spawns fresh brain agents only when no usable handle exists or the platform does not expose reusable handles.
- Prevents unbounded nested Right/Left Brain sub-agent trees; only the orchestrator manages brain agents.
- Keeps runtime agent IDs, handles, and thread IDs out of `.dual-brain/MEMORY.md`; cross-session continuity still comes from project memory.

## v1.3.0 — Memory Tiering & Weighted Recall

Dual-Brain memory now uses weighted recall so old decisions do not consume the same attention as active project context.

- Adds Hot / Warm / Cold / Archived tiers for `.dual-brain/MEMORY.md`.
- Adds lightweight metadata: `refs`, `last_referenced`, and `last_verified`.
- Increments `refs` only when a memory item materially influences questioning, verification, synthesis, or implementation.
- Reads Hot memory first, Warm memory when request-relevant, and Cold/Archived memory only by targeted lookup.
- Auto-compacts memory by promoting active items, demoting stale low-reference items, archiving superseded decisions, and merging noisy duplicates.
- Migrates older untiered memory files into the tiered structure during the next memory auto-save.
- Updates benchmark fixtures and prompts to exercise the tiered memory contract.

## v1.2.0 — Persistent Project Memory

- Adds project-local memory intake from `.dual-brain/MEMORY.md`.
- Adds memory auto-save and auto-compaction for durable non-sensitive project context.
- Keeps sensitive content out of memory and reports only removed/redacted categories.
- Adds SkillsGate installation guidance for multi-agent and multi-project setups.
- Adds the benchmark harness and an early results snapshot.
