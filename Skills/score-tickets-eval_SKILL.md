---
name: score-tickets-eval
description: Ruthlessly challenge the current Linear priorities on every open ticket in your team. Independently re-scores each ticket on Strategic Fit + Urgency from scratch, compares against the priority already set in Linear, reports statistics (agreement rate, drift distribution), and walks the user through every disagreement one-by-one — asking whether to accept the new score before pushing. Approved changes flow back into the score-tickets rubric; rejected challenges flow back into this eval's adversarial stance, so the loop sharpens itself over time. Use whenever you want to audit, challenge, sanity-check, or red-team the priorities produced by /score-tickets. Triggers include "/score-tickets-eval", "challenge the scores", "audit the priorities", "eval my scoring", "red-team the backlog priorities", "are my Linear priorities right".
---

# Score Tickets — Eval

Audit the Linear priorities currently set on every open ticket in your team. Treat the existing priorities as a hypothesis to attack, not defend. Re-score from scratch with an adversarial lens, surface every disagreement with a sharp reason, then have the user adjudicate ticket-by-ticket before any write.

This skill is the QA pass for [[score-tickets]]. It never invents scores out of thin air — it always re-derives them from the live ticket data and the same Strategic Fit + Urgency rubric.

## Configuration — set these before first use

Use the same placeholders as `/score-tickets`. If you've configured that skill, you're done.

- **`{TEAM_KEY}`** — Linear team key/prefix.
- **`{WORKSPACE}`** — Linear workspace slug for issue URLs.
- **`{STRATEGY_DOC}`** *(optional)* — strategy reference. The adversarial stance reads this to know what *not* to challenge as "off-strategy."
- **`{KEY_CUSTOMERS}`** *(optional)* — named accounts that warrant an SF bump when present in a ticket. Without this list, customer-naming gets no special treatment.
- **`{ACTIVE_LAUNCHES}`** *(optional)* — current launches/bets the eval will accept as legitimate SF anchors.

## Fixed parameters — never change

- **Team:** `{TEAM_KEY}`.
- **Assignee filter:** none, by default (match `/score-tickets`).
- **Statuses to include:** *Backlog*, *Todo*, *In Progress*, *Waiting for Feedback* (or your team's equivalents). Exclude *In Review*, *Done*, *Canceled*, *Duplicate*.
- **Rubric:** same as `/score-tickets` — Strategic Fit (1–5) + Urgency (1–5) → Total (2–10). Mapping to Linear priority:

  | Total | Linear priority |
  |---|---|
  | 10 | `1` Urgent |
  | 8–9 | `2` High |
  | 6–7 | `3` Medium |
  | 2–5 | `4` Low |

## Step 1 — Fetch tickets with current priority

Call `mcp__linear__list_issues` once per status in **parallel**, filtered by `team: {TEAM_KEY}`, the status name, assignee per your team's convention, `limit: 250`. Capture for each ticket: `id`, `title`, `priority.value`, `priority.name`, `status`, `project`, `dueDate`, `description`, `updatedAt`.

If a description is truncated and the strategic intent is genuinely ambiguous, fetch the full body via `mcp__linear__get_issue` — but only for those tickets, not all of them.

## Step 2 — Re-score independently and adversarially

For every ticket, derive **SF (1–5)** and **U (1–5)** from scratch using the rubric below. **Do not look at the current Linear priority while scoring** — score blind, then compare. Today's date comes from the harness context (never hard-code).

### Adversarial scoring stance

Challenge the obvious. For every ticket, ask:

- **Strategic Fit** — Does this *actually* serve `{ACTIVE_LAUNCHES}` or the priorities stated in `{STRATEGY_DOC}`? Or is it adjacent work that *feels* important because it's recent or top-of-mind?
- **Urgency** — Is there a real external deadline, or just internal momentum? Has the ticket been sitting at "High" for weeks with no movement (a sign the urgency was inflated)?
- **Customer specificity** — Tickets that name an account from `{KEY_CUSTOMERS}` get an SF bump; vague "improve X" tickets do not.
- **Duplicate or sibling tickets** — If two tickets cover the same outcome, the second one should typically score lower (consolidation candidate), not equal.
- **Internal tooling** — Skills, EVALs, roadmap setup, "vision" docs — be honest. They feel strategic but often have weak external pull. Don't score them above 4 SF unless there's a concrete consumer.
- **Stale tickets** — If a ticket hasn't been touched in 30+ days and has no deadline, U is almost certainly ≤ 2. Don't let "Backlog" inertia keep it at 3.

### Rubric (same as /score-tickets)

**Strategic Fit (SF):**
- 5 — Directly serves an active launch, the strategy doc's stated priorities, or a named key customer commitment.
- 4 — Strong fit: inside an active project, unblocks a key customer, or shapes product vision.
- 3 — Useful product work, no clear strategic lever.
- 2 — Internal tooling / speculative.
- 1 — Stale / off-strategy.

**Urgency (U):**
- 5 — Hard deadline within 7 days, or in-flight launch work tomorrow.
- 4 — Deadline within 30 days, blocks active launch comms, or named customer waiting.
- 3 — Important, no concrete deadline.
- 2 — Useful, no time pressure.
- 1 — Could sit for months.

Compute **Total = SF + U** and map to the proposed Linear priority via the table above.

## Step 3 — Diff against current Linear priority

For each ticket, classify the diff between **current** priority and **proposed** priority:

- **Match** — same priority.
- **Off by 1 bucket** — e.g. current High, proposed Medium (or vice versa).
- **Off by 2+ buckets** — e.g. current Urgent, proposed Medium. These are the loud ones.
- **Missing priority** — current is `0` No priority, proposed is anything. Always flag.

Treat *every* non-Match as "off" — even off-by-1 matters when the backlog is small.

## Step 4 — Print statistics first

Open the response with a tight stats block. No preamble.

```markdown
## Score audit — {N} open tickets

- **Agreement:** {match_count}/{N} ({pct}%)
- **Off by 1 bucket:** {n}
- **Off by 2+ buckets:** {n}
- **Missing priority (was None):** {n}
- **Net drift:** {n} tickets I'd raise · {n} I'd lower
- **Biggest single delta:** {TEAM_KEY}-XXX ({current} → {proposed}, Δ {n} buckets)
```

Follow with a one-line headline assessment: is the current prioritization roughly right with edge-case drift, or systematically off?

## Step 5 — Walk through every "off" ticket, one at a time

After the stats block, do **not** dump all disagreements in one table. Instead, walk through them **one ticket at a time**, in this order:

1. Off-by-2+ buckets (loudest first, biggest delta first within tie)
2. Missing priority (was None)
3. Off-by-1 buckets (highest proposed priority first)

For each ticket, print this block:

```markdown
---

### {k}/{total_off} — [{TEAM_KEY}-XXX](https://linear.app/{WORKSPACE}/issue/{TEAM_KEY}-XXX) — Title

- **Current:** {Current priority name} (was {SF_implied}+{U_implied} ≈ {total_implied}, if inferable)
- **Proposed:** {Proposed priority name} — SF {sf} + U {u} = **{total}**
- **Why current is off:** {1–2 sharp sentences. Lead with the concrete reason — deadline, customer, launch dependency, staleness, duplicate, weak strategic link. No hedging.}
- **What would change my mind:** {1 sentence — what evidence would justify keeping the current priority. This is the user's escape hatch.}
```

After printing the block, ask the user: **"Accept proposed priority {Proposed name} for {TEAM_KEY}-XXX? (yes / keep current / different priority)"** using `AskUserQuestion` with options:
- **Accept proposed** ({Proposed name})
- **Keep current** ({Current name})
- **Set to a different priority** — let the user pick Urgent / High / Medium / Low / None

Record the user's decision per ticket. Do not push to Linear yet. Move to the next off-ticket and repeat.

### Batching rule

If the off-list is longer than 8 tickets, ask the user up-front whether to walk through all of them, or just the top N (default: top 5 by delta + all missing-priority tickets). Don't drown them in 25 prompts unless they asked for it.

## Step 6 — Push the accepted changes

After the walk-through, summarize the user's decisions:

```markdown
## Decisions

- **Accepting proposed:** {n} tickets → list IDs
- **Keeping current:** {n} tickets → list IDs
- **Custom priority:** {n} tickets → list IDs with new priorities
```

Then call `mcp__linear__save_issue` in **parallel**, one call per ticket that needs a change (skip "keep current"). Pass only `id` and `priority`. Never modify other fields.

After the batch completes, print a 4-line bucket summary (Urgent / High / Medium / Low) of the **final state** across all team tickets — so the user sees the net result, not just deltas.

## Step 7 — Learn from the decisions

The user's verdicts are the ground truth. Every disagreement teaches one of the two skill files something. Don't skip this step — without it, the same mis-scoring happens next run.

### Classify each decision

For every ticket the user adjudicated, classify the outcome:

- **Eval was right** — user picked "Accept proposed." `score-tickets` produced a wrong priority; the eval correctly flagged it.
- **Eval was wrong** — user picked "Keep current." The current Linear priority was correct; the eval challenged it for a reason that didn't hold.
- **Both were wrong** — user picked a custom priority different from both. Calibration is off in both rubrics.

### Look for patterns, not one-offs

Don't propose an edit for every single decision. Group decisions by the underlying reason and only propose edits where a **pattern** emerges (typically 2+ tickets with the same root cause). Patterns to scan for:

- **Missed customer signal** — multiple tickets where naming an account from `{KEY_CUSTOMERS}` should have bumped SF but didn't, and the user agreed with the bump.
- **Inflated launch halo** — multiple tickets where being in an "active project" inflated SF beyond what the actual work warranted, and the user agreed with the cut.
- **Stale-ticket inertia** — tickets that sat at a high priority despite no movement, where the user agreed with the lowering.
- **Internal-tooling over-weighting** — tickets about internal scripts, EVALs, roadmap tooling that scored too high on SF, with user confirming the cut.
- **Deadline blindness** — tickets with a real-but-not-obvious external deadline (utility billing windows, regulatory dates, customer go-live) that didn't get the urgency bump, with user confirming the raise.
- **Eval over-aggression** — multiple tickets where the eval challenged a priority the user defended on the same kind of evidence ("named customer is real," "deadline is real," etc.).

### Propose edits, one per pattern

For each pattern, draft a **specific, surgical edit** to the right file. The edit should add an anchor, example, or rule — not rewrite the rubric.

**Where to write:**

- **Eval was right pattern** → edit your local `score-tickets/SKILL.md`. Add a concrete anchor under the relevant rubric axis (SF or U) or under "Key rules." Example: "If the description names a key customer by name, SF is at least 4."
- **Eval was wrong pattern** → edit your local `score-tickets-eval/SKILL.md`. Add a counter-anchor under "Adversarial scoring stance" so the eval stops over-challenging. Example: "Tickets that name a specific customer with an active engagement should *not* be challenged on Strategic Fit unless there's evidence the work is misaligned with the customer's actual ask."
- **Both wrong pattern** → edit both files with calibration notes. Rare — only do this when the user's chosen priority is consistently off from both rubrics in the same direction.

### Confirm before editing

Present each proposed edit as a diff-style block:

```markdown
### Proposed edit {k}/{total} — `score-tickets/SKILL.md`

**Pattern observed:** {2-line summary — which tickets, what they had in common, what the user decided}

**Edit:**
- **Section:** {section heading from the target file}
- **Add:**
  > {exact text to insert, ≤ 2 sentences}

Apply this edit? (yes / no / revise)
```

Use `AskUserQuestion` per edit. Options:
- **Apply as-is**
- **Skip this edit** — pattern wasn't real enough
- **Revise the wording** — user types replacement text

Only after the user accepts do you use the `Edit` tool to actually modify the file. Insert at the most relevant location — typically the end of the cited section, so existing anchors stay in their order. Never replace an existing rule; only append.

### When to do nothing

If the only disagreements were one-off ticket-specific calls (the user picked custom priorities for idiosyncratic reasons, no shared root cause), say so explicitly:

> No patterns strong enough to update the skill rubrics this run.

Don't force edits. Noise in the rubric is worse than no edit.

### After edits applied

Print a 2-line summary: `{n} edits applied to score-tickets/SKILL.md`, `{n} edits applied to score-tickets-eval/SKILL.md`. Done.

## Key rules

- **Score blind, compare second.** Never let the current Linear priority anchor the new score. Adversarial means independent.
- **Stats first, walk-through second.** The user should see the headline before being asked to adjudicate.
- **One ticket at a time, with an explicit ask.** Never batch-confirm. Use `AskUserQuestion` per ticket. The whole point of this skill is that the user is the judge.
- **Cite a reason, not an opinion.** "Why current is off" must point at a concrete fact (deadline, customer name, staleness, duplicate) — not "feels low" or "could be higher."
- **Offer the escape hatch.** Always print "What would change my mind" so the user can defend the current priority with one piece of evidence.
- **Read-only outside `priority`.** Same as `/score-tickets` — descriptions, statuses, assignees, projects, comments are never touched.
- **Strategy doc is an input.** Re-read `{STRATEGY_DOC}` before scoring. The strategy can shift; the rubric should bend with it.
- **Today's date from the harness.** Never hard-code — urgency depends on it.
- **Always run Step 7.** The learning loop is the whole point of the eval — never skip it, even on a clean run (in which case you say "no patterns strong enough" explicitly and move on). Edits are append-only and require explicit user approval per edit.
- **Patterns, not one-offs.** Never propose a rubric edit from a single ticket. Two or more tickets with the same root cause is the minimum bar.
