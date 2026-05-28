# Contributing to Dual-Brain

Thanks for your interest in improving Dual-Brain! 🧠 This is a [Claude Code](https://claude.com/claude-code) skill — its "source" is the persona prompts, memory contract, and protocol in [`SKILL.md`](SKILL.md). Most contributions are prompt-engineering improvements, docs, memory behavior, or new debate patterns.

## Ways to contribute

- 🐛 **Report a bug** — the skill misbehaves, ignores the protocol, mishandles memory, or the agents drift out of role.
- 💡 **Suggest an improvement** — a sharper persona, a better mediation rule, clearer output format, or smarter memory rule.
- 📖 **Improve docs** — fix the README, add examples, clarify wording or translations.
- 🧩 **Add a debate pattern** — a variant workflow (e.g., a third reviewer brain, a domain-specific persona).
- 🗂️ **Improve project memory** — better intake, verification, patch proposals, or compaction behavior.

## Getting set up

1. Fork and clone the repo.
2. Install the skill locally so you can test it:
   ```bash
   git clone https://github.com/<your-fork>/dual-brain.git ~/.claude/skills/dual-brain
   ```
3. Open Claude Code and invoke the skill (e.g. `use dual brain to ...`) to see your changes in action.

## Making changes

- The **heart of the skill is `SKILL.md`** — especially the two persona blocks, the memory contract, and the fixed protocol. Tune these carefully and keep the order: memory intake → Right Brain grills → Left Brain verifies → dual synthesis → memory patch proposal.
- Keep the `description:` frontmatter in `SKILL.md` accurate — it's how Claude Code decides when to trigger the skill.
- If you change behavior, update the README so docs stay in sync.
- If you touch project memory behavior, document how `.dual-brain/MEMORY.md` is read, verified, patched, and compacted.
- Never introduce instructions that silently write memory. Dual-Brain proposes patches; the user approves them.
- Test your change against at least one real task before opening a PR, and describe what you observed.

## Testing memory behavior

For protocol changes that affect memory, test the important paths:

- **No memory file** — the skill should proceed normally and optionally propose creating `.dual-brain/MEMORY.md`.
- **Valid memory** — Right Brain should use prior decisions to ask sharper questions.
- **Stale or contradictory memory** — Left Brain should verify against code/docs and flag the mismatch.
- **Overgrown memory** — synthesis should propose compaction that keeps decision-value and archives noise.
- **Sensitive content** — the skill should not reuse secrets, tokens, keys, credentials, or sensitive personal data; it should propose removing them.
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
