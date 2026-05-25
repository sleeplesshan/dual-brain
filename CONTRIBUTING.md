# Contributing to Dual-Brain

Thanks for your interest in improving Dual-Brain! 🧠 This is a [Claude Code](https://claude.com/claude-code) skill — its "source" is the persona prompts and protocol in [`SKILL.md`](SKILL.md). Most contributions are prompt-engineering improvements, docs, or new debate patterns.

## Ways to contribute

- 🐛 **Report a bug** — the skill misbehaves, ignores the protocol, or the agents drift out of role.
- 💡 **Suggest an improvement** — a sharper persona, a better mediation rule, clearer output format.
- 📖 **Improve docs** — fix the README, add examples, clarify wording or translations.
- 🧩 **Add a debate pattern** — a variant workflow (e.g., a third reviewer brain, a domain-specific persona).

## Getting set up

1. Fork and clone the repo.
2. Install the skill locally so you can test it:
   ```bash
   git clone https://github.com/<your-fork>/dual-brain.git ~/.claude/skills/dual-brain
   ```
3. Open Claude Code and invoke the skill (e.g. `use dual brain to ...`) to see your changes in action.

## Making changes

- The **heart of the skill is `SKILL.md`** — especially the two persona blocks and the fixed Step 0–4 protocol. Tune these carefully and keep the fixed order (Right Brain grills → Left Brain verifies → dual synthesis).
- Keep the `description:` frontmatter in `SKILL.md` accurate — it's how Claude Code decides when to trigger the skill.
- If you change behavior, update the README so docs stay in sync.
- Test your change against at least one real task before opening a PR, and describe what you observed.

## Opening a pull request

1. Create a branch: `git checkout -b my-improvement`
2. Commit with a clear message describing **what** changed and **why**.
3. Open a PR using the template. Include:
   - A short description of the change.
   - The motivation / problem it solves.
   - A sample task you ran and the resulting behavior.

## Style

- Keep prose clear and concise. The personas should read as crisp instructions, not essays.
- Preserve the bilingual spirit if relevant, but the canonical files in this repo are English.

## Questions?

Open a [Discussion](https://github.com/sleeplesshan/dual-brain/discussions) or an issue. Friendly, constructive collaboration only — see the [Code of Conduct](CODE_OF_CONDUCT.md).

If Dual-Brain helps you, a ⭐ is always appreciated!
