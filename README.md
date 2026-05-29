<div align="center">

# 🧠 Dual-Brain

### Remember it. Grill it. Verify it. Document it.

A portable dual-agent workflow that splits hard problems across **two debating sub-agents** and gives them durable project context. The **Right Brain** ruthlessly *interrogates* your request against prior decisions. The **Left Brain** *verifies* every claim against real code, docs, and memory. The orchestrator synthesizes the result, ships the work, auto-saves durable memory, and asks what you want removed or adjusted.

[![Codex Compatible](https://img.shields.io/badge/Codex-Compatible-111111?style=flat-square&logo=openai&logoColor=white)](https://openai.com/codex/)
[![Claude Code Compatible](https://img.shields.io/badge/Claude_Code-Compatible-D97757?style=flat-square&logo=anthropic&logoColor=white)](https://claude.com/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](#-contributing)

</div>

---

## ✨ Why Dual-Brain?

A single AI agent tends to fail in one of three ways. It either:

- 🌫️ **Takes the request at face value** — runs with your ambiguous wording, builds the wrong thing confidently, and hallucinates APIs that don't exist,
- 🔬 **Drowns in detail** — gets lost in syntax and corner cases while missing the simpler, smarter path and shipping nothing you can actually use, or
- 🕳️ **Forgets the project** — re-litigates decisions you already settled last week because the session ended and the context disappeared.

The fix isn't a better single prompt — it's **structured tension plus persistent project memory**. Dual-Brain bakes that in. It runs a strict debate between two specialists with opposite instincts, feeds them project memory when it exists, verifies that memory against reality, then synthesizes a single production-ready result *with documentation*.

> **The orchestrator remembers it. Right Brain grills it. Left Brain verifies it. The final answer ships it — documented.**

---

## 🎭 Meet the two brains

| | 🔍 **Right Brain** — *Context, Pattern & Grill* | 🔬 **Left Brain** — *Logic, Verification & Code* |
|---|---|---|
| **Sees** | The forest 🌲 | The trees 🌿 |
| **Job** | Interrogate, clarify, map context | Cross-check, verify, refine, document |
| **Superpower** | Exposing hidden assumptions & stale project lore | Catching hallucinations against real code/docs/memory |
| **Always asks** | *"What are the blind spots? What did we already decide?"* | *"Does this actually match the docs, code, and memory?"* |
| **Speaks** | First (the grilling) | Second (the verification) |

---

## 🔄 How it works

The main agent acts as an **orchestrator** — it never answers directly. It runs a fixed cycle:

```
                        ┌─────────────────────────────┐
        your task  ──▶  │  STEP 0A · MEMORY INTAKE    │
                        │  load .dual-brain/MEMORY.md │
                        └──────────────┬──────────────┘
                                       ▼
                        ┌─────────────────────────────┐
                        │  STEP 0B · ORCHESTRATOR     │
                        │  frames the problem         │
                        └──────────────┬──────────────┘
                                       │  (same context to both)
                                       ▼
                        ┌───────────────────────────────┐
                        │  STEP 1 · 🔍 RIGHT BRAIN      │
                        │  DECONSTRUCT & GRILL          │
                        │  · interrogate assumptions    │
                        │  · define the lexicon         │
                        │  · flag memory suspicions     │
                        └──────────────┬────────────────┘
                                       │  passes full output ▼
                        ┌───────────────────────────────┐
                        │  STEP 2 · 🔬 LEFT BRAIN       │
                        │  CROSS-REFERENCE & REFINE     │
                        │  · verify vs code/docs/memory │
                        │  · catch stale assumptions    │
                        │  · enforce structural rigor   │
                        └──────────────┬────────────────┘
                                       │  refutes a core premise?
                          ┌────────────┴─────────────┐
                          ▼ (≤ 1 round)              │
                ┌────────────────────────┐           │
                │ STEP 3 · mediation     │ ──────────┘
                │ realign direction      │
                └───────────┬────────────┘
                            ▼
                ┌───────────────────────────────────┐
                │  STEP 4 · 🤝 DUAL SYNTHESIS       │
                │  clarified + verified →           │
                │  production-ready code + docs     │
                └───────────┬───────────────────────┘
                            ▼
                ┌───────────────────────────────────┐
                │ STEP 4A · MEMORY AUTO-SAVE        │
                │ save/compact, then ask for review │
                └───────────────────────────────────┘
```

1. **Remember** — the orchestrator checks `.dual-brain/MEMORY.md` in the active project root and extracts relevant context.
2. **Frame** — it distills your request into one shared paragraph, including the useful memory context.
3. **Right Brain grills** — it refuses to take the request or memory at face value: it interrogates assumptions, defines every ambiguous term, maps the macro-context, and flags stale or contradictory memory.
4. **Left Brain verifies** — it physically cross-checks the idea against your codebase, official docs, and project memory, then rebuilds it as a rigorous, deployable blueprint.
5. **Mediate (if needed)** — if verification refutes a *core premise* (e.g. the API doesn't behave as assumed, or memory contradicts current code), the orchestrator sends it back to the Right Brain **once** to realign. No infinite loops.
6. **Synthesize** — the orchestrator fuses both into a single production-ready deliverable **with documentation**, and carries it through to actual file changes for coding tasks.
7. **Auto-save memory** — if the session created durable non-sensitive knowledge, the orchestrator updates `.dual-brain/MEMORY.md`, compacts stale/noisy memory, and asks what you want removed or adjusted.

---

## 🗂️ Project Memory

Dual-Brain's memory is intentionally boring: one Markdown file in your project.

```text
.dual-brain/MEMORY.md
```

That file is the shared long-term context for the project: active constraints, architecture decisions, vocabulary, rejected alternatives, open questions, recent changes, and archived decisions.

If the file does not exist yet, Dual-Brain creates it automatically after synthesis when the session produces durable non-sensitive project knowledge.

```md
# Project Memory

## Active Constraints

- Keep the public API backward-compatible until v2.

## Architecture Decisions

- 2026-05-29: Use a unified notification dispatcher for email and Slack.

## Vocabulary

- "Notification" means a real-time user-facing event, not a batched digest.

## Rejected Alternatives

- Raw fire-and-forget webhooks were rejected because dropped alerts are unacceptable.

## Open Questions

- Should admin alerts use the same dispatcher or a separate operational channel?

## Recent Changes

- Added a retry queue that makes Slack delivery viable.

## Archived Decisions

- The old "no webhook retries" constraint is obsolete now that the queue exists.
```

Memory is **advisory, not authoritative**. Current code and official docs beat stale memory. The user can override memory. The Left Brain verifies memory before relying on it.

Dual-Brain never treats `.dual-brain/MEMORY.md` as a secret store. Do not put credentials, tokens, private keys, API keys, or sensitive personal data in it. Sensitive content is not stored or summarized; if found, it is removed or redacted and reported only by category.

---

## 🧹 Memory Compaction

Long-term memory needs a trash day.

When `.dual-brain/MEMORY.md` gets noisy, repetitive, stale, or contradictory, Dual-Brain compacts it automatically instead of blindly appending more text. The rule is simple:

> **Keep decision-value, compress noise.**

That means:

- Keep constraints that still affect future work.
- Keep decisions and rejected alternatives that prevent re-litigation.
- Keep vocabulary that prevents ambiguity.
- Keep open questions that still need an answer.
- Compress obsolete detail into `Archived Decisions`.
- Remove sensitive content instead of summarizing it.

Compaction is part of the same auto-save step. After saving, the agent summarizes what changed and asks what memory you want removed or adjusted.

---

## 📦 Installation

Clone this repo straight into your Codex skills directory:

```bash
git clone https://github.com/sleeplesshan/dual-brain.git ~/.codex/skills/dual-brain
```

Or into your Claude Code skills directory:

```bash
git clone https://github.com/sleeplesshan/dual-brain.git ~/.claude/skills/dual-brain
```

Or add it as a per-project skill in either environment:

```bash
git clone https://github.com/sleeplesshan/dual-brain.git .codex/skills/dual-brain
git clone https://github.com/sleeplesshan/dual-brain.git .claude/skills/dual-brain
```

That's it — Codex and Claude Code can discover the workflow from `SKILL.md`. No build step, no dependencies.

> **Requirements:** An agentic coding environment that supports Markdown skills and sub-agents, such as Codex or [Claude Code](https://claude.com/claude-code). The protocol expects a general-purpose sub-agent capability; no runtime package is required.

---

## 🚀 Usage

Just describe your task and invoke the skill by name, or use any of its trigger phrases:

```
> use dual brain to refactor my notification system to support Slack alerts

> dual-brain: design a rate limiter for our public API

> left brain right brain — pick a caching strategy for the feed service
```

Dual-Brain shines when a task needs **both creative interrogation and rigorous, verified implementation** at once — architecture decisions, tricky refactors, integrating an unfamiliar API, or any "I'm not even sure I'm asking the right question" moment.

### 🎯 When to reach for it

| ✅ Great fit | ⏭️ Overkill |
|---|---|
| Vague or under-specified requests | A one-line fix |
| Integrating an unfamiliar API / SDK | Renaming a variable |
| Refactors with subtle correctness risks | Trivial, well-understood tasks |
| Architecture & design decisions | Anything you already know the answer to |
| Anything where hallucinated APIs would hurt | Pure boilerplate |
| Projects with recurring decisions and tradeoffs | One-off throwaway snippets |

---

## 📋 Example: "Add Slack alerts to my notification system"

```
## 🧠 Dual-Brain Result

### 🧭 Memory Intake
Loaded .dual-brain/MEMORY.md. Email alerts must remain backward-compatible.
Webhook retries were previously rejected because there was no queue. The queue
now exists.

### 🔍 Right Brain (Deconstruct & Grill)
Grilling this against project memory: are we combining Slack with email, or
replacing email? Does the new queue invalidate the old "no webhook retries"
decision? Lexicon — "notification" = a real-time user-facing event, not a
batched digest. Macro pattern: a unified dispatcher with pluggable channels.

### 🔬 Left Brain (Cross-reference & Verify)
Checked the current queue implementation and Slack's docs. The old rejected
alternative is stale now that retry infrastructure exists. The async webhook
approach is valid, but raw fire-and-forget would still drop messages under
rate limits. Email compatibility can stay intact behind the dispatcher.

### 🤝 Dual Synthesis
Unified notification service: email + Slack behind one dispatcher, with a
rate-limit-aware retry queue and comprehensive error handling.
- Clarified direction: combine channels via a pluggable dispatcher
- Verified against: Slack docs + existing email module + project memory
- Memory impact: old webhook retry objection should be archived
- Deliverable + documentation: [implementation written to notifier/, with setup docs]

### 📝 Memory Auto-Saved
Updated .dual-brain/MEMORY.md to record the Slack channel decision, archive the
old retry objection, and keep the email compatibility constraint. Nothing
sensitive was stored. Tell me if you want any memory removed or adjusted.
```

---

## 🧩 Why it works (the design philosophy)

Dual-Brain is a small bet on a big idea: **specialized, adversarial collaboration beats a single generalist pass.** By forcing the order — *remember first, grill second, verify third, synthesize last* — it neutralizes the failure modes that plague solo agents:

- The Right Brain can't let a vague request slide, because **nothing gets built until the assumptions are interrogated and the terms are defined.**
- The Left Brain can't ship a fantasy, because **every claim is cross-checked against real code, official docs, and project memory before it reaches you.**
- The orchestrator can't pretend the past never happened, because **durable decisions live in `.dual-brain/MEMORY.md` and get refreshed when they change.**

The orchestrator holds the tiebreaker: **verification conflicts lean Left, framing conflicts lean Right, stale memory gets challenged.** The result is reliably more thoughtful — and more *deployable* — than either brain, or one undivided agent, would produce alone.

---

## 🤝 Contributing

Ideas, persona tweaks, memory rules, and new debate patterns are very welcome:

1. Fork the repo
2. Tune `SKILL.md` (the persona prompts and memory contract are the heart of it)
3. Open a PR describing what changed and why

See [CONTRIBUTING.md](CONTRIBUTING.md) for details. If Dual-Brain helped you think better, a ⭐ goes a long way.

---

## 📄 License

[MIT](LICENSE) — use it, fork it, remix it.

<div align="center">
<sub>Packaged for Codex and <a href="https://claude.com/claude-code">Claude Code</a>, designed as a portable agent workflow. Remembered, grilled, verified, documented, and shipped.</sub>
</div>
