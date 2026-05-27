---
name: score-tickets
description: Score every open Linear ticket in your team on Strategic Fit + Urgency, print a sorted importance table, and (on confirmation) push the resulting priorities back to Linear. After the push, automatically chains to /score-tickets-eval so a second adversarial pass red-teams the result. Use whenever you want to prioritize, rank, or set priorities on your team's tickets. Triggers include "/score-tickets", "score my tickets", "score the backlog", "rank my tickets", "set priorities in Linear", "score by importance".
---

# Score Tickets

Score every open Linear ticket in your team on a simple two-axis rubric — **Strategic Fit** + **Urgency** — print a sorted table, then push the resulting Linear priority values back to the tickets after the user confirms. After the push, automatically chain to `/score-tickets-eval` to QA the result.

## Configuration — set these before first use

Replace the placeholders below with your team's values. Either edit them inline in this file, or keep them as variables you swap at run time.

- **`{TEAM_KEY}`** — the Linear team key/prefix (e.g. `ENG`, `GROWTH`). This is what `mcp__linear__list_issues` accepts as the `team` filter and what appears as the issue identifier prefix.
- **`{WORKSPACE}`** — your Linear workspace slug, used in issue URLs (`https://linear.app/{WORKSPACE}/issue/{TEAM_KEY}-XXX`).
- **`{STRATEGY_DOC}`** *(optional)* — pointer to wherever your team's current strategy lives (Notion page, README section, memory entry). The scorer reads this to know what "Strategic Fit 5" means for *your* team. If you don't have one, lean on the in-line anchors below.
- **`{KEY_CUSTOMERS}`** *(optional)* — list the named accounts that, when mentioned in a ticket, should bump Strategic Fit. Without these, customer-naming gives no SF bump.
- **`{ACTIVE_LAUNCHES}`** *(optional)* — current launches / bets that should bump Strategic Fit when a ticket sits inside one (project name match).

## Fixed parameters — never change

- **Team:** `{TEAM_KEY}`. Pass this as the team filter to `mcp__linear__list_issues`.
- **Assignee filter:** none, by default. If your team uses assignment rigorously, set `assignee: "me"`. Otherwise leave unfiltered — many teams keep tickets unassigned until pickup.
- **Statuses to include:** *Backlog*, *Todo*, *In Progress*, *Waiting for Feedback* (or your team's equivalents). Exclude *In Review*, *Done*, *Canceled*, *Duplicate*.
- **Rubric:** Strategic Fit (1–5) + Urgency (1–5) → Total (2–10). No RICE, no other frameworks unless the user explicitly asks.

## Step 1 — Fetch tickets

Call `mcp__linear__list_issues` once per included status, in **parallel**, filtered by:
- `team: {TEAM_KEY}`
- `state` = the status name
- assignee filter per your team's convention
- `limit: 250`

If a status doesn't exist in your team, skip it silently. If a status returns >250 tickets, paginate.

## Step 2 — Score each ticket

For each ticket, assign two integer scores in `[1, 5]`:

### Strategic Fit (SF)
How well the ticket aligns with `{STRATEGY_DOC}` and `{ACTIVE_LAUNCHES}`.

- **5** — Directly serves an active launch, the strategy doc's stated priorities, or a named key customer commitment (from `{KEY_CUSTOMERS}`).
- **4** — Strong fit: lives inside an active project, unblocks a key customer, or shapes product vision.
- **3** — Useful product work, no clear strategic lever.
- **2** — Internal tooling or speculative work with weak link to strategy.
- **1** — Stale / off-strategy. Candidate for archive.

### Urgency (U)
Time-sensitivity given today's date (always read from the harness context, do not hard-code).

- **5** — Hard deadline within 7 days, or in-flight launch work that's literally tomorrow.
- **4** — Deadline within 30 days, blocks active launch comms, or named customer waiting.
- **3** — Important but no concrete deadline; foundational strategy work.
- **2** — Useful, no time pressure.
- **1** — Could sit for months without harm.

Compute **Total = SF + U** (range 2–10).

When scoring, **read the ticket's `description`, `project`, `dueDate`, and `status` fields** — these are the inputs to both SF and U. If a description is truncated by the list call, do not blindly fetch the full body for every ticket; only fetch via `mcp__linear__get_issue` when the truncated snippet leaves the strategic intent genuinely ambiguous.

## Step 3 — Render the table

Print a single markdown table sorted by Total descending, then by Urgency descending as a tiebreaker. Use this exact column layout:

```markdown
| # | ID | Title | Status | Project | SF | U | Score | Why this score |
```

Rules:
- **ID** — link to `https://linear.app/{WORKSPACE}/issue/{TEAM_KEY}-XXX`.
- **Project** — name, or `—` if none.
- **Score** — bold the number (e.g. `**10**`).
- **Why this score** — one short sentence. Lead with the concrete reason (deadline, customer, launch dependency, etc.), not generic adjectives.
- After the table, print a **Top observations** section: 2–4 bullets. Call out duplicates (same customer or near-identical scope), launch concentration, and anything obviously parkable. Keep it short.

Do **not** push any priorities to Linear yet.

## Step 4 — Confirm and push priorities

End the message by asking the user whether to push these as Linear priority values, or leave the table as-is.

If the user confirms (e.g. "yes", "please do", "push them"), map scores to Linear priority values using this exact rubric:

| Total score | Linear priority |
|---|---|
| 10 | `1` Urgent |
| 8–9 | `2` High |
| 6–7 | `3` Medium |
| 3–5 | `4` Low |
| 2 | `4` Low |

Then call `mcp__linear__save_issue` for **every ticket in parallel**, passing only `id` and `priority`. Do not modify any other field — no description edits, no status changes, no assignee changes.

After the batch finishes, print a 4-line summary grouped by bucket (Urgent / High / Medium / Low) listing the ticket IDs in each.

## Step 5 — Auto-chain to /score-tickets-eval

Immediately after Step 4 finishes (the parallel writes have returned and the bucket summary is printed), **invoke the `score-tickets-eval` skill via the `Skill` tool with no arguments**. Do not ask the user first — the chain is mandatory.

Why it's mandatory: the scoring you just pushed is a hypothesis. The eval is the QA pass that catches drift the scorer missed (under-rated named customers, duplicate-sibling traps, inflated process-work SF, etc.) and gives the user a chance to adjudicate ticket-by-ticket before the priorities settle. Without the eval, the scorer's blind spots become permanent.

Print exactly one transition line before the Skill call so the user sees the chain happen:

> Pushed priorities. Auto-running `/score-tickets-eval` to red-team the result.

Then call `Skill` with `skill: "score-tickets-eval"`. Do not duplicate any of its work yourself.

### When to skip the chain

Skip Step 5 **only** if:
- The user explicitly said "don't run the eval" or "skip the eval" in their prompt for this run, **or**
- The user declined to push priorities in Step 4 (no writes happened, so there's nothing to QA).

In both skip cases, say so in one line ("Skipping eval per your instruction" / "No writes pushed — eval skipped") instead of silently dropping the step.

## Key rules

- **Team `{TEAM_KEY}`, 4 open statuses.** Same every run.
- **Two-axis rubric only.** Strategic Fit + Urgency. Don't switch to RICE, ICE, or anything else unless the user explicitly asks.
- **Always show the table first, push only after confirmation.** Scoring is cheap; mass-updating Linear priorities is shared-state mutation. Never skip the confirmation step.
- **Parallel writes on push.** All `save_issue` calls in a single batch — don't sequence them.
- **Read-only outside the priority field.** This skill never edits descriptions, statuses, assignees, projects, or comments. If the user wants those changes, hand off to another skill or direct Linear MCP calls.
- **Today's date comes from the harness.** Never hard-code a date — Urgency depends on it.
- **Strategy doc is an input.** Before scoring, read `{STRATEGY_DOC}` (and any related team-strategy memories) — what counts as a 5 on Strategic Fit shifts with strategy.
- **Always chain to /score-tickets-eval after a push.** The eval is the QA pass — never let a scoring run end without it unless the user explicitly opted out or no writes happened. Print the transition line so the chain is visible.
