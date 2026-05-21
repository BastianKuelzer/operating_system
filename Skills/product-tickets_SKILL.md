---
name: product-tickets
description: Create Linear tickets in the ecoplanet PROB team backlog for the user's product management work. Use whenever the user wants to create, draft, file, or log a ticket for their PM work — triggers include "/product-tickets", "create a ticket", "file this in PROB", "make a backlog item", "draft a ticket for X", "log this as a ticket", or any request to send product work to Linear. Each ticket gets a tight What + Acceptance Criteria + Questions to increase quality, lives in Backlog, and is matched to an existing PROB project (or left unassigned when no project clearly fits).
---

# Product Tickets

Create Linear tickets in the ecoplanet PROB team backlog. Tickets are descriptive but tight — no padding, no boilerplate, no ceremony. Every ticket includes Questions to increase quality to expose what still needs to be decided so engineering doesn't pick it up half-baked.

## Fixed parameters — never change

- **Team:** PROB (ecoplanet — `https://linear.app/ecoplanet/team/PROB`)
- **State:** Backlog (every ticket, every time)
- **No ticket type field.** Don't classify, prefix, or label by type.

## Step 1 — Take the input

The user will describe the work in any form: a sentence, a paragraph, a meeting note, a customer quote, a Slack snippet. If the request is ambiguous in scope or outcome, ask one or two sharp clarifying questions before drafting.

**Treat the user's input as the only source of truth.** You may use it verbatim, paraphrase it, or rearrange it — but you may not extend it. Anything not in the input (or in the user's clarifying answers) is unknown, and unknowns belong in *Questions to increase quality*, never in *What* or *Acceptance Criteria*.

If you find yourself thinking "they probably also want…" or "it would obviously need to…" — stop. That's hallucination. Either ask the user, or list it as a Question.

If the user dumps several requests in one message, plan to handle them as a batch (see "Multiple tickets" below).

### Ask for a source link

Before drafting, ask the user whether there's a source to link for context — a Slack thread, meeting notes, customer message, Notion or Google doc, Figma file, Fireflies recording, Linear comment, or any URL that gives a downstream agent or engineer the background needed to act on the ticket without re-asking the user. Accept "no source" as a valid answer; do not invent one. The user may provide multiple sources — capture each as a `{url, title}` pair, where the title is short and meaningful (e.g. "PM-eng sync notes 2026-05-08", not "Notion page").

If the request is part of a multi-ticket batch, ask once whether the same source applies to all of them, or per-ticket.

## Step 2 — Match a project

Call `mcp__linear__list_projects` filtered to the PROB team. Read each project's name and goal.

**Rule:** A PROB project always has a goal of shipping a product. Match a ticket to a project only when the ticket clearly contributes to that project's ship goal.

When in doubt, leave it unassigned:
- Ticket spans multiple projects → unassigned
- No project's ship-goal cleanly matches → unassigned
- Work is internal, process, ops, or otherwise not part of shipping a specific product → unassigned

**Do not create a new project to make a ticket fit.** Only create a new project when the user explicitly asks for one. If they do:
1. Confirm the proposed name and ship-goal with the user
2. Call `mcp__linear__save_project` with team PROB
3. Then assign the ticket to it

## Step 3 — Draft and create the ticket

**Title:** Imperative, specific, ≤ 80 chars. Names the outcome, not the activity.
- Good: "Add CSV export to invoice list"
- Bad: "Invoice list improvements" / "Look into invoice export"

**Description:** Use exactly this structure. No extra sections.

```markdown
## Source
- [Title 1](url1)
- [Title 2](url2)

## What
[1–3 sentences restating what the user said. Concrete nouns and verbs from the input. Do not extend it.]

## Acceptance Criteria
- [ ] [Testable outcome grounded in the input]
- [ ] [Testable outcome grounded in the input]

## Questions to increase quality
- [Real gap 1]
- [Real gap 2]
```

Omit the `## Source` section entirely if the user said there is no source. Do not include the heading with a "none" placeholder.

### Drafting rules

- **Short over thorough.** If a section feels padded, cut it. The whole ticket should be readable in under 30 seconds.
- **Highly descriptive ≠ long.** Specificity in nouns and verbs beats more words. "Show last 12 months of invoices, paginated 50 per page" beats "improve the invoice listing experience for users."
- **Acceptance Criteria must be grounded in the input.** Every AC has to trace back to something the user actually said or confirmed. If you can't point to the source phrase, it doesn't go in. One AC is fine. Zero ACs is fine — write `- [ ] To be defined — see Questions below`. Do not pad to hit 3.
- **Acceptance Criteria are testable.** Anyone should be able to verify done/not-done. Avoid "improve," "optimize," "ensure good UX," "make it nicer."
- **Questions to increase quality surface real gaps.** Use them for the things that, if left unanswered, would let someone build the wrong thing. Common categories: scope edges, success metric, target user/segment, rollout strategy, dependencies, edge cases, ownership. If genuinely nothing is open, write `- None — ready to scope`. Do not fill in ceremonial questions.
- **No effort estimates, T-shirt sizes, sprints, dependency-graph sections, or technical-notes sections.** They are not part of this ticket structure.

### What you must NOT invent

When the input doesn't specify something, it goes in *Questions*, not in *What* or *AC*. Specifically, never invent:

- **Behaviors or states** the user didn't mention (e.g. "shows as active when already purchased", empty states, error states, loading states)
- **Permissions / access control / gating** ("restricted to billing admins", "requires auth")
- **Copy, labels, CTA text, or specific UI elements** ("a primary CTA", "a comparison table") unless the user named them
- **Mechanics** the user didn't pick (sales-request vs. self-serve, modal vs. page, sync vs. async)
- **Eligibility, segmentation, or pricing logic**
- **Integrations, tracking events, analytics, localization, accessibility requirements**
- **Edge cases, fallbacks, validation rules**
- **Scope expansions** ("…and also for the mobile app")

Test before each AC: *Can I quote the user's words that justify this?* If no, move it to Questions or delete it.

### Create immediately

Once drafted, call `mcp__linear__save_issue` directly — no preview, no confirmation step:
- `team`: PROB
- `state`: Backlog
- `title`: as drafted
- `description`: as drafted, with **real newlines** (per Linear MCP guidance — never `\n` escape sequences)
- `project`: matched project ID, or omit the field entirely if unassigned
- `links`: pass each source as `{url, title}` so it shows up as a Linear attachment. Always pass sources via `links` *in addition to* the `## Source` section in the description — the body line is for downstream agents reading the description, the attachment is for humans skimming the Linear UI. Omit the field if there are no sources.

Reply with the Linear URL on one line, plus a one-line note of the project decision (e.g. `Project: Invoice Foundation` or `Project: unassigned — no clear single-project fit`).

## Multiple tickets in one go

If the user provides several distinct pieces of work in one message, draft them all and create them in a single batch (parallel `save_issue` calls). Reply with all URLs as a numbered list, each with its project decision.

Don't drip them out one at a time unless the user asks for that.

## Key rules

- **Team PROB, state Backlog, no type field — every ticket, every time.**
- **Never invent content.** Every clause in *What* and every *Acceptance Criterion* must trace to the user's words. Unknowns go in *Questions*. A short ticket with one AC and many questions beats a fuller one with invented details.
- **Never invent a project to fit a ticket.** Match or leave unassigned. New projects only on explicit user request, and only with a confirmed product-shipping goal.
- **Ask before drafting** when scope or outcome is ambiguous. Questions to increase quality is for residual gaps, not for things you should have asked.
- **Always ask for a source link** before drafting, so a downstream agent or engineer has the context to act without re-asking. "No source" is a valid answer — accept it and move on.
- **Real newlines** in the description body when calling Linear — not `\n`.
- **One ticket = one outcome.** If a single request would produce a ticket with three unrelated acceptance criteria sets, split it into multiple tickets and tell the user why.
