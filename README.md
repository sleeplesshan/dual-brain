<div align="center">

# 🧠 Dual-Brain

### Two minds are better than one — even when both are AI.

A [Claude Code](https://claude.com/claude-code) skill that splits hard problems across **two debating sub-agents**: a creative **Right Brain** that sketches the big picture, and a rigorous **Left Brain** that stress-tests every line. You get ideas that are bold *and* correct.

[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-D97757?style=flat-square&logo=anthropic&logoColor=white)](https://claude.com/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](#-contributing)

</div>

---

## ✨ Why Dual-Brain?

A single AI agent tends to collapse into one mode of thinking. It either:

- 🌫️ **Over-dreams** — proposes a slick architecture that falls apart on the first edge case, or
- 🔬 **Over-engineers** — gets lost in syntax and corner cases while missing the simpler, smarter path.

Real breakthroughs usually come from the **tension between vision and rigor**. Dual-Brain bakes that tension into the workflow. Instead of one agent doing everything, it orchestrates a structured debate between two specialists with opposite instincts — then synthesizes their best ideas into one answer.

> **Right Brain dreams it. Left Brain proves it. The orchestrator ships it.**

---

## 🎭 Meet the two brains

| | 🌳 **Right Brain** — *The Context Patterner* | 🔬 **Left Brain** — *The Logic Engine* |
|---|---|---|
| **Sees** | The forest 🌲 | The trees 🌿 |
| **Thinks in** | Patterns, analogies, paradigms | Causality, types, corner cases |
| **Superpower** | Creative detours around deadlocks | Catching the bug before it ships |
| **Ignores** | Syntax & nitpicks | Nothing |
| **Speaks** | First (the bold sketch) | Second (the cold verification) |

---

## 🔄 How it works

The main agent acts as an **orchestrator** — it never answers directly. It runs a fixed, four-step debate:

```
                        ┌─────────────────────────────┐
        your task  ──▶  │  STEP 0 · Orchestrator       │
                        │  frames the problem          │
                        └──────────────┬──────────────┘
                                       │  (same context to both)
                                       ▼
                        ┌─────────────────────────────┐
                        │  STEP 1 · 🌳 RIGHT BRAIN     │
                        │  macro sketch · paradigm     │
                        │  · clever detours            │
                        └──────────────┬──────────────┘
                                       │  passes full output ▼
                        ┌─────────────────────────────┐
                        │  STEP 2 · 🔬 LEFT BRAIN      │
                        │  logic check · corner cases  │
                        │  · production-ready refinement│
                        └──────────────┬──────────────┘
                                       │  conflict on a core premise?
                          ┌────────────┴────────────┐
                          ▼ (≤ 1 round)             │
                ┌───────────────────────┐           │
                │ STEP 3 · mediation     │ ──────────┘
                │ realign direction      │
                └───────────┬───────────┘
                            ▼
                ┌───────────────────────────────────┐
                │  STEP 4 · 🤝 FINAL CONSENSUS        │
                │  vision + rigor, combined →         │
                │  real code / spec changes           │
                └───────────────────────────────────┘
```

1. **Frame** — the orchestrator distills your request into one shared paragraph of context.
2. **Right Brain proposes** — a holistic sketch, the core paradigm, and 1–2 alternative detours.
3. **Left Brain verifies** — tears the sketch apart logically, hunts corner cases, and rebuilds it as an executable plan or production code.
4. **Mediate (if needed)** — if the Left Brain rejects a *core premise*, the orchestrator sends it back to the Right Brain **once** to realign. No infinite loops.
5. **Consensus** — the orchestrator fuses both perspectives into a single answer and carries it through to actual file changes when code is involved.

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
> use dual brain to design a rate limiter for our public API

> dual-brain: refactor this auth module so it's testable

> left brain right brain — pick a caching strategy for the feed service
```

Dual-Brain shines when a task needs **both creative design and rigorous verification** at once — architecture decisions, tricky refactors, algorithm design, debugging gnarly issues, or any "I'm not sure this approach is right" moment.

### 🎯 When to reach for it

| ✅ Great fit | ⏭️ Overkill |
|---|---|
| Designing a new system or API | Renaming a variable |
| Choosing between architectural approaches | A one-line fix |
| Refactors with subtle correctness risks | Trivial, well-understood tasks |
| Algorithm / data-structure design | Anything you already know the answer to |
| "Is this design actually sound?" | Pure boilerplate |

---

## 📋 Example output

```
## 🧠 Dual-Brain Result

### 🌳 Right Brain (macro proposal)
Treat the rate limiter as a token-bucket per API key, but lean on the
existing Redis layer instead of in-process state so it survives horizontal
scaling. Detour: if Redis latency hurts, fall back to a sliding-window log.

### 🔬 Left Brain (micro verification)
Token refill must be computed lazily on read to avoid a background sweep —
otherwise N keys = N timers. Watch the race on concurrent decrements; use
an atomic Lua script. Sliding-window log is O(requests) memory — cap it.

### 🤝 Final Consensus
Redis token-bucket with a lazy-refill Lua script (atomic, scale-safe).
- Adopted Right Brain direction: per-key bucket on shared Redis
- Detail reinforced by Left Brain: atomic Lua refill, no background timers
- Consensus deliverable: [implementation written to rate_limiter.py]
```

---

## 🧩 Why it works (the design philosophy)

Dual-Brain is a small bet on a big idea: **specialized, adversarial collaboration beats a single generalist pass.** By forcing the order — *vision first, verification second, synthesis last* — it prevents the two failure modes that plague solo agents:

- The Right Brain can't ship a fantasy, because the Left Brain audits it before anything is written.
- The Left Brain can't bikeshed into the weeds, because it's anchored to a clear macro direction.

The orchestrator holds the tiebreaker: **logic conflicts lean Left, direction conflicts lean Right.** The result is reliably more thoughtful than either brain — or one undivided agent — would produce alone.

---

## 🤝 Contributing

Ideas, persona tweaks, and new debate patterns are very welcome:

1. Fork the repo
2. Tune `SKILL.md` (the persona prompts are the heart of it)
3. Open a PR describing what changed and why

If Dual-Brain helped you think better, a ⭐ goes a long way.

---

## 📄 License

[MIT](LICENSE) — use it, fork it, remix it.

<div align="center">
<sub>Built as a skill for <a href="https://claude.com/claude-code">Claude Code</a>. Right Brain dreams it · Left Brain proves it.</sub>
</div>
