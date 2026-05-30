# Contributing to Dual-Brain

Thanks for your interest in improving Dual-Brain! 🧠 This is a portable Markdown skill for agentic coding environments such as Codex and Claude Code. Its "source" is the persona prompts, memory contract, and protocol in [`SKILL.md`](SKILL.md). Most contributions are prompt-engineering improvements, docs, memory behavior, or new debate patterns.

## Ways to contribute

- 🐛 **Report a bug** — the skill misbehaves, ignores the protocol, mishandles memory, or the agents drift out of role.
- 💡 **Suggest an improvement** — a sharper persona, a better mediation rule, clearer output format, or smarter memory rule.
- 📖 **Improve docs** — fix the README, add examples, clarify wording or translations.
- 🧩 **Add a debate pattern** — a variant workflow (e.g., a third reviewer brain, a domain-specific persona).
- 🗂️ **Improve project memory** — better weighted intake, verification, auto-save, review prompts, tiering, or compaction behavior.

## Getting set up

1. Fork and clone the repo.
2. Install the skill locally so you can test it:
   ```bash
   git clone https://github.com/<your-fork>/dual-brain.git ~/.codex/skills/dual-brain
   ```
3. Open Codex, Claude Code, or another compatible agentic coding environment and invoke the skill (e.g. `use dual brain to ...`) to see your changes in action.

## Making changes

- The **heart of the skill is `SKILL.md`** — especially the two persona blocks, the memory contract, and the fixed protocol. Tune these carefully and keep the order: memory intake → Right Brain grills → Left Brain verifies → dual synthesis → memory auto-save/compaction → review prompt.
- Keep the `description:` frontmatter in `SKILL.md` accurate — compatible agents use it to decide when to trigger the skill.
- If you change behavior, update the README so docs stay in sync.
- If you touch project memory behavior, document how `.dual-brain/MEMORY.md` is read, tiered, verified, auto-saved, reviewed, and compacted.
- Never introduce instructions that store or summarize sensitive content. Dual-Brain auto-saves only durable non-sensitive project memory, then asks the user what to remove or adjust.
- Test your change against at least one real task before opening a PR, and describe what you observed.

## Testing memory behavior

For protocol changes that affect memory, test the important paths:

- **No memory file** — the skill should proceed normally and create `.dual-brain/MEMORY.md` after synthesis only when durable non-sensitive project knowledge exists.
- **Valid memory** — Right Brain should use Hot memory first and relevant Warm memory to ask sharper questions.
- **Stale or contradictory memory** — Left Brain should verify against code/docs, flag the mismatch, and archive or rewrite the item.
- **Overgrown memory** — synthesis should auto-compact memory in a way that keeps decision-value, demotes stale low-reference context, and archives noise.
- **Metadata updates** — `refs` and `last_referenced` should change only for memory that materially influenced the task; `last_verified` should change only after real verification.
- **Sensitive content** — the skill should not reuse, store, or summarize secrets, tokens, keys, credentials, or sensitive personal data; it should remove or redact them and report only their category.
- **Trivial task** — the skill should not force a memory update when nothing durable changed.

## Opening a pull request

1. Create a branch: `git checkout -b my-improvement`
2. Commit with a clear message describing **what** changed and **why**.
3. Open a PR using the template. Include:
   - A short description of the change.
   - The motivation / problem it solves.
   - A sample task you ran and the resulting behavior.
   - Any memory scenarios you tested, if relevant.

## Style

- Keep prose clear and concise. The personas should read as crisp instructions, not essays.
- Match the repo's current voice: direct, developer-focused, and workflow-oriented.
- Preserve the bilingual spirit if relevant, but the canonical files in this repo are English.

## Questions?

Open a [Discussion](https://github.com/sleeplesshan/dual-brain/discussions) or an issue. Friendly, constructive collaboration only — see the [Code of Conduct](CODE_OF_CONDUCT.md).

If Dual-Brain helps you, a ⭐ is always appreciated!
