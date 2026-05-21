---
name: to-dos
description: Summarize the user's open Linear work in the ecoplanet PROB team — every ticket currently In Progress, Todo, or Waiting for Feedback — with the last comment shown inline for any Waiting-for-Feedback ticket. Use whenever the user wants a quick read of what's on their plate or what's blocked. Triggers include "/to-dos", "what's on my plate", "what am I working on", "show my open tickets", "what's waiting on me", "what's waiting for feedback".
---

# To-Dos

Give the user a tight, scannable summary of their open Linear work in PROB, grouped by status. Optimize for a 10-second read: titles, links, and just enough context to act.

## Fixed parameters — never change

- **Team:** PROB (ecoplanet — `https://linear.app/ecoplanet/team/PROB`). Internal team name in the Linear API is `ProductBasti`; the issue identifier prefix is `PROB`. Always pass `PROB` as the team filter — it resolves correctly.
- **Assignee:** *do not filter by assignee.* PROB is Bastian's personal team and tickets are typically left unassigned, so filtering by assignee (UUID or `"me"`) returns zero results. Every open PROB ticket is effectively his work. Treat the whole team as the assignee.
- **Statuses to include:** *In Progress*, *Todo*, *Waiting for Feedback*

## Step 1 — Resolve status IDs

Call `mcp__linear__list_issue_statuses` for team PROB to capture the IDs (and exact names) of the statuses matching *In Progress*, *Todo*, and *Waiting for Feedback*.

For reference, current PROB status IDs (verify by listing — they can change):
- In Progress → `5a6fab68-cffa-4f27-acef-746126fd6ad3`
- Todo → `8ec76132-f3fe-4c9d-92ae-22d773a05892`
- Waiting for Feedback → `d1f1703b-d184-40d9-a7f2-18a6fd8a5ce5`

Match status names case-insensitively. If a status name doesn't match exactly (e.g. "Waiting on feedback", "Awaiting feedback"), pick the closest semantic match in the PROB workflow and note the actual name used in the final output. If a status genuinely doesn't exist in PROB, skip its section and say so in one line.

Skip `mcp__linear__list_users` — there's no assignee filter to populate.

## Step 2 — Fetch tickets

Call `mcp__linear__list_issues` once per status (parallel), filtered by:
- team PROB
- state = the status ID
- **no** assignee filter

Order by `updatedAt` desc within each status.

## Step 3 — Fetch last comments (Waiting for Feedback only)

For every Waiting-for-Feedback ticket, call `mcp__linear__list_comments` in parallel (one call per issue). Take the most recent comment by `createdAt`. If the issue has no comments, mark it as such.

Do **not** fetch comments for In Progress or Todo tickets — that's extra noise.

## Step 4 — Render the summary

Use this exact structure. Sections appear in this order. Omit a section only if its status has zero tickets, and replace it with a single line: `### In Progress — none` (etc.).

```markdown
## To-dos — {count} open

### In Progress ({n})
- [PROB-123 — Ticket title](https://linear.app/ecoplanet/issue/PROB-123) · _Project name or unassigned_ · updated {relative date}
- ...

### Todo ({n})
- [PROB-124 — Ticket title](https://linear.app/ecoplanet/issue/PROB-124) · _Project name or unassigned_ · updated {relative date}
- ...

### Waiting for Feedback ({n})
- [PROB-125 — Ticket title](https://linear.app/ecoplanet/issue/PROB-125) · _Project name or unassigned_ · updated {relative date}
  - **Last comment** ({author}, {relative date}): {comment body, trimmed to ~280 chars, single line — collapse newlines to spaces, end with `…` if truncated}
- [PROB-126 — Ticket title](https://linear.app/ecoplanet/issue/PROB-126) · _unassigned_ · updated {relative date}
  - **Last comment**: _none_
- ...
```

### Rendering rules

- **Title line:** `PROB-XXX — Title`, linked. Project name in italics; `unassigned` if no project. Updated date as relative (e.g. "2d ago", "3w ago") computed from today (2026-05-21).
- **Last comment line** (Waiting for Feedback only): author display name, relative date, body. Trim body to ~280 chars on a single line — collapse newlines to spaces, end with `…` if truncated. If there are no comments, write `_none_`.
- **Counts** in section headings reflect actual ticket counts in that section.
- **Top-line count** is the total across all three sections.
- **Order within each section:** most recently updated first.
- **No padding.** No "here's your summary" preamble, no closing remarks, no next-step suggestions. The list is the output.

## Key rules

- **Team PROB, no assignee filter, statuses In Progress / Todo / Waiting for Feedback** — every run. PROB tickets are typically unassigned; filtering by assignee returns nothing.
- **Last comment only for Waiting for Feedback.** Don't fetch or render comments for the other two sections.
- **One single ticket fetch per status, in parallel.** Don't loop or paginate unless a section returns a truncated result (>50 tickets in one section is the signal — then mention it in a one-line note under the heading).
- **Read-only.** This skill never creates, updates, or comments on tickets. If the user asks for follow-up actions on a ticket from the summary, hand off to `/product-tickets` or normal Linear MCP calls — don't fold writes into this skill.
- **Real relative dates.** Compute from today's date in the harness context, not a placeholder.
