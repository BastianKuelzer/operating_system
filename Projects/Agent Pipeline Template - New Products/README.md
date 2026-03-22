# 🔗 Agent Pipeline Template — New Products

A 5-agent pipeline that turns a new product idea into everything needed to build and sell it — automatically. One trigger, five specialized agents, zero dropped tasks.

---

## Why a Pipeline Instead of One Agent?

A single agent doing everything — gathering insights, extracting tasks, finding skills, executing, logging — crashes regularly. Too much context, too many steps, too many failure points.

The solution: **one agent, one job.** Each agent is lean, reliable, and independently improvable. Status fields in your databases act as checkpoints between agents — you control how much automation vs. human review you want.

---

## The New Product Pipeline

```
Input (Meeting / Briefing / Feature Request)
        ↓
[1] Insights Agent        → Insights Database
    ├── Customer Voice         → Customer evidence doc
    └── Competitor Research    → Competitor landscape doc
        ↓
[2] Task Extractor        → Tasks Database
        ↓
[3] Skill Scout           → Skills assigned to each task
        ↓
[4] Skill Executor        → Runs all 4 skills in parallel
    ├── AI Prototyping         → Prototype prompts (v0 / Bolt / Lovable)
    ├── Linear Ticket Writer   → Engineering tickets
    ├── Context Page           → PRD-equivalent handover doc
    └── Sales Talk Track       → Spoken pitch for Sales
        ↓
[5] Feedback Logger       → Feedback Database
```

---

## Agent Definitions

### 1. Insights Agent

**Job:** Gather all external evidence needed before building — customer proof and competitive context. Runs two skills in parallel.

**Input:** Feature name or problem description (from meeting, briefing, or request)
**Output:** Two insight records in the Insights Database
**Trigger:** Manual (after a meeting or briefing) or automated (via calendar/email hook)

**Skills it runs:**

| Skill | Output |
|-------|--------|
| [Customer Voice](../../Skills/customer-voice_SKILL.md) | Structured evidence doc with quotes from customer feedback confirming the pain point |
| [Competitor Research](../../Skills/competitor-research_SKILL.md) | Competitor landscape: who has this, who doesn't, how they price it |

---

### 2. Task Extractor

**Job:** Read the insight records and extract the four standard execution tasks for a new product launch. Each task becomes its own record in the Tasks Database.

**Input:** Insight records with status `Processed`
**Output:** Four task records, one per execution skill
**Trigger:** Automatically after Insights Agent completes

**Standard tasks for a new product:**
- `Generate prototype prompt for [proposed solution]`
- `Write Linear tickets for [feature scope]`
- `Write context page for engineering handover`
- `Create sales talk track for [feature name]`

**Rules:**
- One task = one skill
- Tasks must include enough context (feature name, scope, customer evidence summary) for the skill to run without follow-up
- Ambiguous items are flagged for human review, not silently dropped

---

### 3. Skill Scout

**Job:** For every output task, find and assign the correct skill to execute it.

**Input:** Insight records with status `Processed`
**Output:** Skill name assigned to each task record
**Trigger:** Automatically after Insights Agent completes

**Skill assignments for this pipeline:**

| Task | Skill |
|------|-------|
| Generate prototype prompt | [AI Prototyping](../../Skills/ai-prototyping_SKILL.md) |
| Write Linear tickets | [Linear Ticket Writer](../../Skills/linear-tickets_SKILL.md) |
| Write context page | [Context Page](../../Skills/context-page_SKILL.md) |
| Create sales talk track | [Sales Talk Track](../../Skills/sales-talk-track_SKILL.md) |

If no matching skill exists, Skill Scout flags the task as `No Skill Found` and drafts a new skill using `new-skill_SKILL.md`.

---

### 4. Skill Executor

**Job:** Execute all four skills in parallel. Each skill produces one artifact.

**Input:** Task records with status `Ready to Execute`
**Output:** Four completed artifacts
**Trigger:** Automatically after Skill Scout completes — or manually after a human checkpoint

**What each skill produces:**

| Skill | Output |
|-------|--------|
| [AI Prototyping](../../Skills/ai-prototyping_SKILL.md) | 4 prototype arguments + 1 recommended prompt, copy-paste ready for v0, Bolt, or Lovable |
| [Linear Ticket Writer](../../Skills/linear-tickets_SKILL.md) | Structured tickets with acceptance criteria, edge cases, and effort estimates |
| [Context Page](../../Skills/context-page_SKILL.md) | PRD-equivalent handover doc: executive summary, business logic, MVP stages |
| [Sales Talk Track](../../Skills/sales-talk-track_SKILL.md) | Spoken pitch covering the customer problem, the solution, and a product walkthrough |

**Parallel execution:** All four skills run simultaneously. A task with status `Waiting for Approval` is skipped until a human confirms it.

---

### 5. Feedback Logger

**Job:** After execution, review what happened and capture learnings for system improvement.

**Input:** Completed task records
**Output:** Feedback records in the Feedback Database
**Trigger:** Automatically after Skill Executor completes

**What it logs:**
- Did the skill execute without errors?
- Was the output accepted as-is, or did a human edit it?
- Were there missing inputs that caused failure or degraded quality?
- Suggestions for improving the skill or the pipeline step

---

## Checkpoints — Control How Much You Automate

Every status transition is a potential checkpoint. Add human review anywhere by inserting a `Waiting for Approval` status before the next agent triggers.

| Between | Optional Checkpoint | What you review |
|---------|---------------------|-----------------|
| Insights → Task Extractor | `Review Insights` | Is the customer evidence and competitor research sufficient? |
| Task Extractor → Skill Scout | `Review Tasks` | Are the four tasks correctly scoped? |
| Skill Scout → Executor | `Approve Skills` | Is each skill assignment correct? |
| Executor → Feedback | `Review Outputs` | Are the four artifacts good enough to use? |

Start with all checkpoints on. Remove them as you trust each stage.

---

## Worked Example: New Feature Launch from a Client Meeting

A client meeting surfaces a recurring pain point and a feature request. The pipeline runs:

1. **Insights Agent** runs two skills in parallel:
   - Customer Voice pulls 12 feedback quotes confirming the pain point
   - Competitor Research surfaces how three competitors handle this — two have it, one doesn't
2. **Task Extractor** pulls four tasks from the insight records:
   - `Generate prototype prompt for the proposed solution`
   - `Write Linear tickets for the feature scope`
   - `Write context page for engineering handover`
   - `Create sales talk track for the new feature`
3. **Skill Scout** assigns one skill per task:
   - `Generate prototype prompt` → AI Prototyping
   - `Write Linear tickets` → Linear Ticket Writer
   - `Write context page` → Context Page
   - `Create sales talk track` → Sales Talk Track
4. **Skill Executor** runs all four skills in parallel:
   - AI Prototyping generates 4 prototype arguments + 1 recommended prompt ready to paste into v0
   - Linear Ticket Writer creates structured tickets with acceptance criteria and edge cases
   - Context Page writes the full PRD-equivalent handover doc for engineering
   - Sales Talk Track produces a spoken pitch the sales team can use from day one
5. **Feedback Logger** notes: all skills ran cleanly, prototype prompt needed one manual tweak on the tech stack, tickets accepted without follow-up questions → logs the prototype skill for review

---

## Database Schema (Minimum)

**Insights Database**

| Field | Type | Notes |
|-------|------|-------|
| Title | Text | Short label for the insight |
| Source | Select | Customer Voice / Competitor Research |
| Raw Input | Long text | Evidence, quotes, or competitor data |
| Date | Date | When the source was created |
| Status | Select | `New` → `Processed` → `Archived` |

**Tasks Database**

| Field | Type | Notes |
|-------|------|-------|
| Task | Text | One concrete action |
| Source Insight | Relation | Links back to the insight it came from |
| Assigned Skill | Text | Skill name to execute |
| Output | Files / URL | Artifact produced by Skill Executor |
| Status | Select | `Pending Skill` → `Ready to Execute` → `Waiting for Approval` → `Done` → `Needs Review` |

**Feedback Database**

| Field | Type | Notes |
|-------|------|-------|
| Task | Relation | Links to the task that was executed |
| Skill Used | Text | Which skill ran |
| Outcome | Select | `Clean` / `Minor Edit` / `Major Edit` / `Failed` |
| Notes | Long text | What went wrong or what could improve |
| Date | Date | Execution date |
