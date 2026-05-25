<div align="center">

# 🧠 Dual-Brain

### Grill it. Verify it. Document it.

A [Claude Code](https://claude.com/claude-code) skill that splits hard problems across **two debating sub-agents**: a **Right Brain** that ruthlessly *interrogates* your request and pins down what you actually mean, and a **Left Brain** that *verifies* every claim against real code & docs and ships it with production-grade documentation. You get answers that are bold, correct, **and** deployable.

[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-D97757?style=flat-square&logo=anthropic&logoColor=white)](https://claude.com/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](#-contributing)

</div>

---

## ✨ Why Dual-Brain?

A single AI agent tends to fail in one of two ways. It either:

- 🌫️ **Takes the request at face value** — runs with your ambiguous wording, builds the wrong thing confidently, and hallucinates APIs that don't exist, or
- 🔬 **Drowns in detail** — gets lost in syntax and corner cases while missing the simpler, smarter path and shipping nothing you can actually use.

The fix isn't a better single prompt — it's **structured tension** between interrogation and verification. Dual-Brain bakes that in. Instead of one agent doing everything, it runs a strict three-step debate between two specialists with opposite instincts, then synthesizes a single production-ready result *with documentation*.

> **Right Brain grills it. Left Brain verifies it. The orchestrator ships it — documented.**

---

## 🎭 Meet the two brains

| | 🔍 **Right Brain** — *Context, Pattern & Grill* | 🔬 **Left Brain** — *Logic, Verification & Code* |
|---|---|---|
| **Sees** | The forest 🌲 | The trees 🌿 |
| **Job** | Interrogate, clarify, map context | Cross-check, verify, refine, document |
| **Superpower** | Exposing hidden assumptions & defining terms | Catching hallucinations against real code/docs |
| **Always asks** | *"What are the blind spots? What does success mean?"* | *"Does this actually match the docs? Does it break anything?"* |
| **Speaks** | First (the grilling) | Second (the verification) |

---

## 🔄 How it works

The main agent acts as an **orchestrator** — it never answers directly. It runs a fixed, three-step cycle:

```
                        ┌─────────────────────────────┐
        your task  ──▶  │  STEP 0 · Orchestrator       │
                        │  frames the problem          │
                        └──────────────┬──────────────┘
                                       │  (same context to both)
                                       ▼
                        ┌─────────────────────────────┐
                        │  STEP 1 · 🔍 RIGHT BRAIN     │
                        │  DECONSTRUCT & GRILL          │
                        │  · interrogate assumptions    │
                        │  · define the lexicon         │
                        │  · map context + alternatives │
                        └──────────────┬──────────────┘
                                       │  passes full output ▼
                        ┌─────────────────────────────┐
                        │  STEP 2 · 🔬 LEFT BRAIN      │
                        │  CROSS-REFERENCE & REFINE     │
                        │  · verify vs real code/docs   │
                        │  · catch bugs & hallucinations│
                        │  · enforce structural rigor   │
                        └──────────────┬──────────────┘
                                       │  refutes a core premise?
                          ┌────────────┴────────────┐
                          ▼ (≤ 1 round)             │
                ┌───────────────────────┐           │
                │ STEP 3 · mediation     │ ──────────┘
                │ realign direction      │
                └───────────┬───────────┘
                            ▼
                ┌───────────────────────────────────┐
                │  STEP 4 · 🤝 DUAL SYNTHESIS         │
                │  clarified + verified →             │
                │  production-ready code + docs       │
                └───────────────────────────────────┘
```

1. **Frame** — the orchestrator distills your request into one shared paragraph of context.
2. **Right Brain grills** — it refuses to take the request at face value: it interrogates assumptions, defines every ambiguous term, maps the macro-context, and proposes creative alternatives.
3. **Left Brain verifies** — it physically cross-checks the idea against your codebase and official docs, catches bugs and hallucinations, and rebuilds it as a rigorous, deployable blueprint.
4. **Mediate (if needed)** — if verification refutes a *core premise* (e.g. the API doesn't behave as assumed), the orchestrator sends it back to the Right Brain **once** to realign. No infinite loops.
5. **Synthesize** — the orchestrator fuses both into a single production-ready deliverable **with documentation**, and carries it through to actual file changes for coding tasks.

---

## 📦 Installation

Clone this repo straight into your Claude Code skills directory:

```bash
git clone https://github.com/sleeplesshan/dual-brain.git ~/.claude/skills/dual-brain
```

Or add it as a per-project skill:

```bash
git clone https://github.com/sleeplesshan/dual-brain.git .claude/skills/dual-brain
```

That's it — Claude Code auto-discovers the skill from `SKILL.md`. No build step, no dependencies.

> **Requirements:** [Claude Code](https://claude.com/claude-code). The skill uses the built-in `general-purpose` sub-agent type, so nothing else to install.

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

---

## 📋 Example: "Add Slack alerts to my notification system"

```
## 🧠 Dual-Brain Result

### 🔍 Right Brain (Deconstruct & Grill)
Grilling this: are we replacing email alerts or combining them? What
happens when Slack rate-limits us? Lexicon — "notification" = a real-time
event push, not a batched digest. Macro pattern: a unified dispatcher with
pluggable channels so future channels (SMS, webhook) drop in cleanly.

### 🔬 Left Brain (Cross-reference & Verify)
Checked Slack's current Bolt SDK docs — the async webhook approach is valid,
but raw fire-and-forget will drop messages under the documented rate limits.
Verified fix: a retry queue with exponential backoff. No backward-compat
break since email stays on the same dispatcher interface.

### 🤝 Dual Synthesis
Unified notification service: email + Slack behind one dispatcher, with a
rate-limit-aware retry queue and comprehensive error handling.
- Clarified direction: combine channels via a pluggable dispatcher
- Verified against: Slack Bolt SDK docs + existing email module
- Deliverable + documentation: [implementation written to notifier/, with setup docs]
```

---

## 🧩 Why it works (the design philosophy)

Dual-Brain is a small bet on a big idea: **specialized, adversarial collaboration beats a single generalist pass.** By forcing the order — *grill first, verify second, synthesize last* — it neutralizes the two failure modes that plague solo agents:

- The Right Brain can't let a vague request slide, because **nothing gets built until the assumptions are interrogated and the terms are defined.**
- The Left Brain can't ship a fantasy, because **every claim is cross-checked against real code and official docs before it reaches you** — the strongest practical defense against hallucination.

The orchestrator holds the tiebreaker: **verification conflicts lean Left, framing conflicts lean Right.** The result is reliably more thoughtful — and more *deployable* — than either brain, or one undivided agent, would produce alone.

---

## 🤝 Contributing

Ideas, persona tweaks, and new debate patterns are very welcome:

1. Fork the repo
2. Tune `SKILL.md` (the persona prompts are the heart of it)
3. Open a PR describing what changed and why

See [CONTRIBUTING.md](CONTRIBUTING.md) for details. If Dual-Brain helped you think better, a ⭐ goes a long way.

---

## 📄 License

[MIT](LICENSE) — use it, fork it, remix it.

<div align="center">
<sub>Built as a skill for <a href="https://claude.com/claude-code">Claude Code</a>. Right Brain grills it · Left Brain verifies it · documented and shipped.</sub>
</div>
