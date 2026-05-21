---
name: solve-in-progress
description: Read every In Progress ticket in the ecoplanet PROB team and print a proposed solution per ticket directly in the terminal. Use whenever the user wants to unblock or move forward their active work without opening Linear. Triggers include "/solve-in-progress", "solve my in progress tickets", "how do I solve my in progress work", "answer my in progress tickets", "walk me through my in progress tickets", "give me solutions for what's in progress".
---

# Solve In Progress

Pull every In Progress ticket in PROB, read it fully (description + comments + source links), and print a concrete proposed solution per ticket in the terminal. Read-only — no Linear writes.

The goal: the user can read the terminal output and immediately know the next concrete move for each active ticket, without opening Linear.

## Fixed parameters — never change

- **Team:** PROB (ecoplanet — `https://linear.app/ecoplanet/team/PROB`)
- **Status:** *In Progress* only
- **Scope:** all In Progress tickets, regardless of assignee (the user said "all", not "mine")

If the user says "just mine" or "the ones assigned to me", filter to assignee `bastian.kuelzer@ecoplanet.tech` for that run only.

## Step 1 — Resolve IDs

Run in parallel:

- `mcp__linear__list_issue_statuses` filtered to team PROB → capture the ID of the status matching *In Progress* (case-insensitive)
- `mcp__linear__list_users` only if the user asked for "just mine" — to resolve the user's ID

If no exact match for *In Progress* exists in PROB, pick the closest semantic match in the workflow and say so in one line at the top of the output.

## Step 2 — Fetch tickets

Call `mcp__linear__list_issues` once, filtered by:
- team PROB
- state = the In Progress status ID
- assignee = user ID (only if the user asked for "just mine")

Order by `updatedAt` desc.

## Step 3 — Fetch full context per ticket (parallel)

For each ticket returned, fan out in parallel:

- `mcp__linear__get_issue` for the full description (if `list_issues` didn't already include it)
- `mcp__linear__list_comments` for the full comment thread

Read every comment — not just the last one. Comments are where blockers, decisions, and updates live, and they're the most important input for proposing a solution.

If a ticket links to a source (Notion doc, Google doc, Slack thread, Figma, Fireflies recording, customer message), do **not** fetch it by default. Fetching arbitrary URLs is slow and noisy. Only fetch a source when the ticket body is too thin to propose a solution and the source is clearly the missing context — and even then, only one source per ticket. Mention in the output when you did this.

## Step 4 — Propose a solution per ticket

For every ticket, write a tight proposed solution. The goal is one paragraph + one short next-step list that the user can act on.

### What "a solution" means

A solution is the concrete next move that gets this ticket closer to done. It is **not** a restatement of the ticket. It is **not** a generic "schedule a meeting to align" non-answer. Examples of valid solutions:

- "Description is clear, AC is testable, just needs implementation — recommended next step: assign to engineering and add to the next sprint."
- "Blocked on the eligibility logic question in comment 3 — decide between option A (segment by ARR) and option B (segment by contract type). Recommend A because the existing pricing table is already keyed by ARR."
- "Last comment from {name} on 2026-05-08 asks for a Figma link. None exists yet — next step: produce a low-fi Figma frame for the empty state, ping {name} when done."
- "Two ACs depend on the procurement-service-kt schema change that hasn't landed yet (see [[project_X]] context). Park this ticket until that schema ships, or split the UI-only AC into a separate ticket that can move now."

### Drafting rules

- **Ground every recommendation in the ticket body or comments.** Don't invent constraints. If the input is too thin to recommend, say "Too thin to propose — needs: X, Y from the user" and list the specific missing inputs.
- **Be specific.** Name the next person to ping, the next file to touch, the next decision to lock. "Push it forward" is not a solution.
- **Surface real blockers.** If a ticket has been sitting in In Progress while waiting on someone else, call that out explicitly with who and since when.
- **Short over thorough.** Each ticket gets ~3–6 lines total. The whole output should be scannable in under two minutes even for 10+ tickets.
- **No hedging boilerplate.** Skip "you might want to consider…", "it could be helpful to…". Recommend directly.

## Step 5 — Render the output

Use this exact structure. Plain markdown, terminal-friendly. No tables.

```markdown
## In Progress — {count} tickets · proposed solutions

### [PROB-123 — Ticket title](https://linear.app/ecoplanet/issue/PROB-123)
_Project name or unassigned · assignee {first name or "unassigned"} · updated {relative date}_

**Status read:** {1–2 sentences on where this ticket actually stands — what's done, what's blocked, what the latest comment says. Grounded in the body + comments.}

**Proposed solution:** {1–2 sentences with the concrete next move.}

**Next steps:**
- {Action 1 — specific, named owner if relevant}
- {Action 2}

---

### [PROB-124 — …](https://linear.app/ecoplanet/issue/PROB-124)
...
```

### Rendering rules

- **Top line count** = number of In Progress tickets returned.
- **Relative date** computed from today's date in the harness context (not a placeholder).
- **Project line** in italics, with `unassigned` when there's no project and `unassigned` when there's no assignee.
- **No preamble**, no closing remarks, no "let me know if you want me to…". The list is the output.
- **Order:** most recently updated first (matches the fetch order).
- **Separator** (`---`) between tickets so it's easy to skim in the terminal.

### When there are zero In Progress tickets

Print one line and stop: `No In Progress tickets in PROB. Nothing to solve.`

## Key rules

- **Read-only.** Never create, update, comment on, transition, or assign Linear tickets from this skill. If the user wants to act on a recommendation, hand off to `/product-tickets` or normal Linear MCP calls.
- **Team PROB, status In Progress, all assignees** by default. Only filter to the user when they ask for "just mine".
- **Read every comment, not just the last one.** Comments are the highest-signal input for proposing a solution.
- **Don't auto-fetch source links.** Only fetch a source when the ticket body is too thin and that source is clearly the missing context — and note when you did.
- **Ground every solution in the ticket.** If there's not enough to recommend, say so and list what's missing. Never invent constraints or pad with generic advice.
- **One ticket = one proposed solution block.** Don't merge tickets, don't reorder by topic — keep it 1:1 with Linear so the user can map output back to tickets at a glance.
