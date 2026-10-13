# Runtime and model guidance

Read this when adapting delegation or settings to a host. Inspect the tools exposed in the current session; names, schemas, concurrency limits, and availability can change independently of the installed client version.

## Orchestration

| Capability | How to use it |
|---|---|
| Native subagents | Use the host's actual spawn, follow-up, message, wait, and lifecycle tools. Codex may expose `collaboration.spawn_agent`; other hosts may expose `spawn_agent` or `Agent`. Never call a name merely because this document mentions it. |
| Existing agents | Check role, task scope, status, and usable context. A message may only queue input; use a follow-up/resume operation when an idle agent needs a new turn. Avoid repeating work already in flight. |
| Missing slots/tools | Run sequentially within limits, or complete the missing perspective locally. Do not invent handles or launch nested CLIs to bypass limits. |
| Waiting | Do useful independent work first, then use a bounded wait. Avoid rapid status polling and repeating unchanged progress. |
| User-owned chats | Creating a sidebar chat is not a substitute for a subagent. Do so only when the user requested a separate chat. |

Agent handles belong only to the live session. After compaction, use available session state to recover valid handles; if unavailable, rebuild a concise brief from files and evidence. Never save runtime IDs in project memory. Replace a reused agent if irrelevant or stale context would outweigh reuse savings.

When user steering changes the goal or implementation, send affected agents the updated brief and identify which earlier findings need rechecking. Interrupt superseded work when supported. Confirm an old writer has stopped, or agree on non-overlapping ownership, before a replacement edits its files. If stopping it cannot be confirmed, continue independent work without competing writes. Match returned findings to the brief and file state they actually checked.

## Models and context

Inherit the active model and reasoning effort unless the user or applicable configuration requests a different choice. Read live support before any override; a model available to the parent or in public docs may not be available to a particular spawn tool. Do not silently switch the parent, change global configuration, or install an upgrade.

For Codex tools exposing `fork_turns`, follow their schema: full-history forks may disallow model/effort overrides. A fresh-context fork needs a self-contained task brief and evidence paths. Use one when it removes substantial irrelevant history; inherit context when it contains essential constraints that are costly to reconstruct.

If the user asks for model selection, these are **dated starting points, not measured Dual-Brain rankings** (reviewed 2026-10-11):

| Available model | Suggested use |
|---|---|
| `gpt-6.1-sol` | General demanding coding and repeated agent workflows; start with the client's default effort. |
| `gpt-6-astra` | Especially difficult synthesis and judgment; preserve autonomy and concrete completion criteria rather than adding ceremony. |
| `gpt-6-luna` | Narrow, explicit checks and repeatable transformations; supply clear inputs and acceptance criteria. |
| `gpt-6-sol`, GPT-5.6 variants | Retain when selected and supported; the same capability-based protocol applies. |

Increase effort only for unresolved complexity that could change the outcome. Maximum effort and more agents are not automatic performance improvements. Check support for each effort; do not assume Ultra exists on every model. These suggestions do not authorize an override by themselves.

Official sources: [models](https://learn.chatgpt.com/docs/models), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), and [skill/prompt design](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra). Recheck current guidance when making model recommendations. Desktop, CLI, API, and other hosts can have different capabilities.
