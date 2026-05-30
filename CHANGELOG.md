# Changelog

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
