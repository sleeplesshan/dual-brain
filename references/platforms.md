# Platform setup and compatibility

Documentation checked 2026-11-07. Use the same `SKILL.md` and references across hosts; do not copy Codex tool names or model IDs into other products. **Documented installation, portable prompt use, and runtime verification are different claims.** This release's behavioral checks run in the available Codex harness, not all five products.

| Environment | Distribution route | Review execution |
|---|---|---|
| Codex | Native skill directory | Actual subagent tools when exposed; local passes otherwise |
| Claude Code | Native skill directory | Supported subagents with an explicit brief; local passes otherwise |
| Grok web/apps | Paste or attach `PORTABLE.md` and explicitly request its use | Review supplied material with available tools; no assumed native skill discovery |
| Grok Bot (xAI) | Send the [installer instruction](../prompts/install-grok-bot.md) to the main Bot | Bot retrieves the prompt, saves/updates a private skill, and verifies availability |
| Muse (Meta) | Send the [installer instruction](../prompts/install-muse.md) to Muse | Muse checks supported persistence and verifies it, or reports session-only use |

“Grokbot” here means xAI Grok Bot, and “Muse” means Meta's Muse personal agent. Muse Code is a separate coding product; its features do not establish an installation path for the personal agent.

## Codex

Choose **one** location for a new installation:

```bash
# User scope
git clone https://github.com/sleeplesshan/dual-brain.git ~/.agents/skills/dual-brain
# OR project scope, from the intended project root
git clone https://github.com/sleeplesshan/dual-brain.git .agents/skills/dual-brain
```

Invoke `$dual-brain` in Codex CLI/IDE, or select the skill using the client's skill picker. Update an existing discovered `~/.codex/skills/dual-brain` checkout in place rather than adding a duplicate. [Official skill documentation](https://learn.chatgpt.com/docs/build-skills).

## Claude Code

Choose one location:

```bash
# User scope
git clone https://github.com/sleeplesshan/dual-brain.git ~/.claude/skills/dual-brain
# OR project scope
git clone https://github.com/sleeplesshan/dual-brain.git .claude/skills/dual-brain
```

Invoke `/dual-brain` followed by the task. Keep `SKILL.md` and `references/` together. We do not set Claude-specific `context: fork` in shared frontmatter: the orchestrator needs the user's task and controls delegation. Give each reviewer a self-contained brief and relevant rules; do not assume a separate subagent has loaded the skill or inherited the conversation. [Official skills](https://code.claude.com/docs/en/skills), [subagents](https://code.claude.com/docs/en/sub-agents).

## Grok

Paste the complete contents of [PORTABLE.md](../PORTABLE.md), or attach the Markdown file, then say:

```text
Use these Dual-Brain instructions for this task: [task and acceptance criteria].
Use only available tools and supplied evidence. If no actionable issue is supported,
report that result without inventing changes. Distinguish suggestions from executed work.
```

The documented upload support includes Markdown/text. Attaching instructions does not install a native skill or establish persistent memory; explicitly request their use. This repository needs no API key or integration service for that route. [Grok overview](https://docs.x.ai/grok/overview), [uploads FAQ](https://docs.x.ai/grok/faq).

## Grok Bot

Send this message to your main **xAI Grok Bot**. The linked instruction asks the Bot to retrieve the full prompt, save or update its private skill, and verify availability:

```text
Read and follow these instructions to install or update dual-brain for this Bot:
https://raw.githubusercontent.com/sleeplesshan/dual-brain/main/prompts/install-grok-bot.md
Complete setup and verify the saved skill. Tell me any remaining step.
```

Then request “Use dual-brain to [task].” Grok Bot documents saving named private skills and enabling them per Bot. If the Bot cannot enable it itself, use Connect apps → connected count → Private skills. The installation request does not create a routine or publish a team skill. **Grok Build** is a different CLI; its directories are not the Bot's installation contract. [Official skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations).

## Meta Muse

Meta describes Muse as a personal agent that accepts tasks through conversation in its app or WhatsApp. Give Muse the setup task directly. A native skill import format is not verified, so the installer checks the current product's supported persistence instead of assuming a directory or API. [Official Muse introduction](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/).

Send this message to Muse:

```text
Read and follow these instructions to install or update dual-brain for me:
https://raw.githubusercontent.com/sleeplesshan/dual-brain/main/prompts/install-muse.md
Use your supported reusable-instruction mechanism and verify saving/loading.
If persistence is unavailable, apply it in this conversation and say so.
```

The installer distinguishes a reusable skill, a saved document that needs loading, and session-only instructions. It asks Muse to report the actual outcome and invocation. Saving a file does not by itself prove future loading. Meta's separate [Muse Code](https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2) product does not establish Muse's installation path.

If either Bot cannot open the installer link, paste the linked installer's text. If it cannot retrieve the skill source, also attach or paste the complete [PORTABLE.md](../PORTABLE.md). No shell command is required from the user for these bot-driven routes.

## Portable file and updates

`PORTABLE.md` is a generated, self-contained prompt containing the core workflow and runtime/memory rules. It needs no Python at use time. When maintaining this repository, regenerate and check it with:

```bash
python3 scripts/export_portable.py
python3 scripts/export_portable.py --check
```

Edit the source documents, not the generated file. Native installations keep progressive loading; chat-only hosts get the complete prompt so local references are not silently missing. Check the host's input limit; do not silently truncate the rules.

For a Git installation, run `git pull --ff-only` inside that existing checkout. For Grok Bot or Muse, send the same installer request again to update the existing copy. Other saved/pasted prompts need explicit replacement with the current portable file; updating this repository does not update another product's account automatically.
