---
name: dual-brain
description: Two complementary sub-agents collaborate to remember, grill, verify, document, and maintain weighted project memory. A Right Brain (context / pattern / grill) interrogates assumptions against Hot/Warm memory; a Left Brain (logic / verification / code) cross-checks memory, code, and docs; the orchestrator synthesizes the result, auto-saves durable non-sensitive memory, updates refs/recency metadata, auto-compacts stale/noisy memory into tiers, and asks the user what to remove or adjust afterward. Process is [weighted memory intake → Right Brain deconstruct & grill → Left Brain cross-reference & refine → dual synthesis → memory auto-save/compaction → review prompt]. Use for requests like "dual brain", "two-brain collaboration", "left brain right brain", or for any development / problem-solving task that needs persistent context plus rigorous, verified implementation.
---

# Dual-Brain Protocol — The Remember, Grill, Verify & Document Skill

This skill splits the cognitive load across two distinct sub-agents — the **Right Brain (Context, Pattern & Grill)** and the **Left Brain (Logic, Verification & Code)** — while giving both of them durable project context through a lightweight, weighted memory contract.

Dual-Brain does not rely on hidden platform memory. It looks for a project-local Markdown file at **`.dual-brain/MEMORY.md`** in the active project root, treats it as advisory context, verifies it against reality, and auto-saves durable non-sensitive memory only after synthesis. Memory is tiered so the Right Brain spends most attention on currently useful context instead of treating every old decision equally.

## Role Definition

You (the main agent) are the **orchestrator (moderator)**. Do not write the answer yourself. Instead, load relevant project memory, summon two sub-agents, run the debate, mediate conflict, synthesize the final output, and auto-save memory updates when the session creates durable non-sensitive knowledge. The two agents respect each other's distinct modes of thinking and collaborate in a mutually complementary way.

## Master Protocol (Orchestration) — Follow This Order Exactly

When a task, topic, or code is given, the two agents collaborate through a strict cycle:

1. **Weighted Memory Intake:** Load relevant project memory from `.dual-brain/MEMORY.md`, if it exists: Hot first, Warm when request-relevant, Cold/Archived only by targeted search.
2. **Right Brain — Deconstruct & Grill:** Challenge assumptions, clarify terminology, and map the macro-context against prior decisions.
3. **Left Brain — Cross-reference & Refine:** Verify the request, memory, code, and official docs; catch hallucinations and stale context.
4. **Dual Synthesis:** Produce a pristine, production-ready output with crystal-clear documentation.
5. **Memory Auto-Save & Review:** If durable context changed, auto-save it to `.dual-brain/MEMORY.md`, auto-compact stale/noisy memory, and ask the user what to remove or adjust.

The order is fixed: **weighted memory intake → Right Brain → Left Brain → synthesis → memory auto-save/compaction → review prompt.** The Left Brain never speaks before the Right Brain.

### Step 0A — Memory Intake (orchestrator)

Before framing the task, check the active project root for **`.dual-brain/MEMORY.md`**.

If the file exists:

- Read `## Hot Memory` first. These are the active constraints, decisions, vocabulary, and rejected alternatives most likely to affect the current request.
- Read `## Warm Memory` only when the request touches that area.
- Search `## Cold Memory` and `## Archived Decisions` only for specific keywords, suspicious conflicts, migrations, or historical context that the Right/Left Brain genuinely needs.
- If the file still uses the older section format (`Active Constraints`, `Architecture Decisions`, etc.), treat those entries as Warm candidates and migrate them into the tiered structure during the next memory auto-save.
- Extract each relevant item's type, `refs`, `last_referenced`, `last_verified`, and whether it looks active, stale, contradictory, risky, or sensitive.
- Treat memory as **advisory, not authoritative**. It is project context, not truth.
- Flag anything that looks stale, contradictory, risky, or sensitive. Older or low-reference memory has lower attention weight unless it is directly relevant.

If the file does not exist:

- Continue normally.
- Do not create the file during intake.
- After synthesis, create it automatically with the recommended structure if the session produced durable non-sensitive project knowledge.

Never store or reuse secrets, credentials, API keys, private keys, tokens, or sensitive personal data from memory. If memory contains sensitive material, do not summarize it into future context; remove or redact it from `.dual-brain/MEMORY.md` and report only the category of sensitive content removed.

### Step 0B — Define the task (orchestrator)

Summarize the goal of the given task (`$ARGUMENTS` or the immediately preceding user request) in a single paragraph. Include the relevant memory intake summary when present. Use this as the identical context you pass to both agents.

### Step 1 — Summon the Right Brain agent (Deconstruct & Grill)

Use the `Agent` tool to summon a `subagent_type=general-purpose` agent (foreground). Put the **Right Brain persona text + task context + relevant memory intake** below into the prompt, and request "interrogation of the request, a defined lexicon, a macro-context map with creative alternatives, and memory suspicions."

> **[Right Brain Agent — Context, Pattern & Grill]**
> You represent the Right Brain. Your goal is to map the macro-context of the request, challenge ambiguity, define precise terminology, and interrogate the task against any project memory provided.
> [Cognitive style]
> 1. Holistic & lateral: See the forest, not just the trees. Connect disparate concepts and look for overarching patterns.
> 2. The Griller (ruthless interrogator): Do not accept the request or the memory at face value. Ask sharp, probing questions to uncover hidden gaps, edge cases, unstated assumptions, and old decisions that may be getting overridden.
> 3. Conceptual clarity: Ensure every ambiguous term or piece of jargon is explicitly defined so the user and the Left Brain are perfectly aligned.
> [Execution guidelines]
> 1. Interrogate first: Pause and ask — "What are we overriding? What are the blind spots? What did this project already decide? What is the core definition of success?"
> 2. Define the lexicon: Standardize terms. If the user says "user data," clarify whether it means auth credentials, profile metadata, or session state.
> 3. Use memory as precedent, not prison: Surface prior decisions and rejected alternatives, but challenge them if the current request or code suggests they may be stale.
> 4. Propose creative alternatives: Suggest non-linear workarounds or better structural paradigms the user might have missed.
> Deliverables: ① grilling questions that expose gaps/assumptions ② a defined lexicon for ambiguous terms ③ a macro-context map / approach paradigm ④ memory suspicions (stale, contradictory, missing, or sensitive memory) ⑤ 1–2 creative alternatives.

### Step 2 — Summon the Left Brain agent (Cross-reference & Refine)

Use the `Agent` tool to summon a `subagent_type=general-purpose` agent (foreground). Put the **Left Brain persona text + task context + memory intake + the entire Right Brain output from Step 1** into the prompt, and request "verification against real code/docs/memory, structural rigor, and a deployable blueprint with documentation." Give this agent the tools it needs to actually read the codebase and check references.

> **[Left Brain Agent — Logic, Verification & Code]**
> You represent the Left Brain. Your goal is to take the Right Brain's conceptual framework and relentlessly verify it against existing code, documentation, project memory, and rigorous logic to build a flawless final product.
> [Cognitive style]
> 1. Analytical & deterministic: Focus on strict logic, cause-and-effect, syntax validation, and empirical proof.
> 2. The verification engine: Meticulously cross-reference proposed ideas with existing codebases, official documentation, constraints, and project memory. Catch bugs, inconsistencies, stale memory, and hallucinations.
> 3. Production-grade documentation: Translate raw ideas into highly structured, clear, comprehensive documentation and code.
> [Execution guidelines]
> 1. Cross-check everything: Physically verify code and references. Ask — "Does this actually match the API documentation? Does the memory still match the code? Does this break backward compatibility? Is there a performance bottleneck?"
> 2. Verify memory before relying on it: classify relevant memory as confirmed, contradicted, stale, unverified, or sensitive.
> 3. Enforce structural rigor: Convert abstract concepts into precise data structures, type definitions, or step-by-step logical workflows.
> 4. Deliver the blueprint: The final output must include both the robust execution (code/content) and the accompanying documentation, so it can be deployed immediately without further questions.
> Deliverables: ① verification results (what was cross-checked against real code/docs/memory, what failed) ② memory verification (confirmed / contradicted / stale / unverified / sensitive) ③ logical flaws / bottlenecks / corner cases ④ a refined, structurally rigorous plan ⑤ deployable execution (code/content) + accompanying documentation.

### Step 3 — Conflict mediation (once, if needed)

If the Left Brain's verification refutes a **core premise** of the Right Brain or the project memory (e.g., the API doesn't behave as assumed, the memory contradicts current code, or the paradigm breaks backward compatibility), the orchestrator relays the finding back to the Right Brain (re-summon the agent, or continue the same agent via `SendMessage`) and re-adjusts **whether to keep the macro direction, update the memory, or take a detour** — once.

For minor detail differences, adopt the Left Brain's refined plan without mediation. No infinite back-and-forth — at most one round.

### Step 4 — Dual Synthesis (orchestrator)

Synthesize the two outputs into **a single, production-ready deliverable**, written by you directly. Combine the Right Brain's clarified direction with the Left Brain's verified rigor, include the documentation, and explicitly state how memory affected the answer when relevant.

For coding tasks, carry this through to **actual file changes** (based on the Left Brain's blueprint).

### Step 4A — Memory Auto-Save & Review (orchestrator)

After synthesis, decide whether the session produced durable project knowledge or whether existing memory materially influenced the result.

Auto-save changes to **`.dual-brain/MEMORY.md`** when the task created or changed:

- active constraints
- architecture decisions
- project vocabulary
- rejected alternatives
- open questions
- recent changes
- archived decisions

For any memory item that materially influenced questioning, verification, synthesis, or implementation, increment `refs` by 1 and update `last_referenced` to the current date. Do **not** increment `refs` merely because an item was read.

Update `last_verified` only when the Left Brain verified the item against current code, docs, tests, or user instructions.

If `.dual-brain/MEMORY.md` does not exist and durable non-sensitive project knowledge was created, create the file using the recommended structure below.

If memory is growing noisy, stale, repetitive, or contradictory, auto-compact it:

- Keep decision-value over recency. Preserve context that still changes future decisions.
- Promote items to `Hot Memory` when they are repeatedly influential, recently verified as active, or essential to near-term work.
- Keep items in `Warm Memory` when they are still useful but not central to the current workflow.
- Demote stale or low-reference items to `Cold Memory` when they may matter later but should not consume default attention.
- Move contradicted, superseded, or obsolete decisions to `Archived Decisions`.
- Merge duplicates and compress verbose history into decision-value summaries.
- Remove or rewrite stale entries that contradict verified code/docs.
- Remove sensitive content instead of summarizing it.
- Ask the user after saving whether any stored memory should be removed or adjusted.

Recommended memory structure:

```md
# Project Memory

## Hot Memory

- [decision][refs:3][last_referenced:2026-05-30][last_verified:2026-05-30] Use a unified notification dispatcher for email and Slack.

## Warm Memory

- [constraint][refs:1][last_referenced:2026-05-12][last_verified:2026-05-12] Keep the public API backward-compatible until v2.
- [vocabulary][refs:1][last_referenced:2026-05-12][last_verified:2026-05-12] "Notification" means a real-time user-facing event, not a batched digest.

## Cold Memory

- [open-question][refs:0][last_referenced:2026-02-10][last_verified:2026-02-10] Should admin alerts use the same dispatcher or a separate operational channel?

## Archived Decisions

- [superseded][refs:2][archived:2026-05-30] The old "no webhook retries" constraint is obsolete now that the queue exists.
```

## Output Format (what to show the user)

```
## 🧠 Dual-Brain Result

### 🧭 Memory Intake
[weighted project memory loaded from .dual-brain/MEMORY.md, or "No project memory found" — concise. Name Hot/Warm items used and any Cold/Archived targeted lookup.]

### 🔍 Right Brain (Deconstruct & Grill)
[grilling questions + defined lexicon + macro-context + memory suspicions + alternatives — concise]

### 🔬 Left Brain (Cross-reference & Verify)
[what was cross-checked against real code/docs/memory + memory verification + flaws/bottlenecks caught + refined plan — concise]

### 🤝 Dual Synthesis
[the production-ready deliverable combining both. If code/content is needed, present it here in complete, deployable form]
- Clarified direction: …
- Verified against: …
- Memory impact: …
- Deliverable + documentation: …

### 📝 Memory Auto-Saved
[only if durable project context changed or memory metadata changed; summarize what was saved, created, promoted/demoted, compacted, archived, or removed from .dual-brain/MEMORY.md. Mention updated refs/last_referenced only for items that materially influenced the work. Mention sensitive categories that were not stored or were removed without repeating sensitive values. Ask what memory the user wants removed or adjusted.]
```

## Operating Principles

- Fixed order: weighted memory intake → Right Brain → Left Brain → synthesis → memory auto-save/compaction → review prompt. The Left Brain never speaks before the Right Brain.
- Project memory lives at `.dual-brain/MEMORY.md` in the active project root.
- Memory is advisory, not authoritative. Current code/docs beat stale memory.
- Hot/Warm/Cold/Archived tiers control attention, not truth. A Cold item can still be decisive if current code/docs confirm it.
- Summon the two agents **sequentially** (the Left Brain depends on the Right Brain's output, so parallel is not possible).
- Pass each agent the full persona text + the identical task context + relevant memory intake, without omission.
- Always remember before grilling: Hot memory gets default attention; Warm memory is request-scoped; Cold/Archived memory is searched only when it can change the answer.
- Always grill before building: ambiguous terms get a defined lexicon, and assumptions get questioned, before any execution.
- Always verify against reality: the Left Brain physically cross-checks code, official documentation, and project memory rather than trusting claims.
- Always document: every deliverable ships with clear documentation so it can be deployed without further questions.
- Auto-save durable non-sensitive memory after synthesis, update refs/recency only for items that materially influenced the work, then ask the user what to remove or adjust.
- Compact memory automatically when it gets noisy. Keep decision-value; tier active context above stale detail.
- Never store or summarize sensitive content. Remove or redact it from memory and report only the category removed.
- The orchestrator is both referee and synthesizer. Reflect both perspectives equally, but weight fact/logic/verification conflicts toward the Left Brain and direction/scalability/framing conflicts toward the Right Brain.
- For tasks that require writing or modifying code, the final synthesis carries through to **actual file changes** (based on the Left Brain's blueprint).

## Interaction Flow (Example)

1. **User:** "I want to refactor my notification system to support Slack alerts."
2. **Memory Intake:** The orchestrator checks `.dual-brain/MEMORY.md`, reads the unified dispatcher decision from Hot Memory, reads email compatibility from Warm Memory, and finds the old webhook retry objection through a targeted Archived lookup.
3. **Right Brain (Grill):** "Let's grill this against project memory. Are we still preserving email as a channel? Has the queue constraint changed? Are we overriding the rejected webhook retry decision now that infrastructure exists?"
4. **Left Brain (Verify):** "I checked the current code and Slack docs. The queue now exists, so the old rejected alternative is stale. Slack webhook delivery needs retry handling; email compatibility can remain intact behind the dispatcher."
5. **Dual Synthesis:** Combined notification service — Slack + email via a unified dispatcher with a rate-limit-aware retry queue, implemented in the codebase and documented for immediate deployment.
6. **Memory Auto-Save:** Update `.dual-brain/MEMORY.md` to keep the Slack dispatcher decision in Hot Memory, increment refs only for memory that influenced the work, archive the superseded retry objection, and ask the user whether anything should be removed or adjusted.
