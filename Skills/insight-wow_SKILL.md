---
name: insight-wow
description: Generate a multi-cadence (daily, week-over-week, month-over-month) usage report for any PostHog insight by mirroring the insight's saved filter (including filterTestAccounts) and running rolling SQL with per-customer breakdown and optional feature-flag overlay. Always asks the user for a target (e.g. "80% WoW usage", "≥ 6 companies/week", "70% retention MoM") before running and reports the gap. Always renders a self-contained HTML dashboard to the Desktop and opens it in the browser. Use when the user asks for "WoW usage", "week-over-week", "DoD", "MoM", "monthly usage", "how is X being used", "are we hitting our target", or names a PostHog insight/dashboard and wants a usage comparison. Triggers on "/insight-wow", "WoW for <insight>", "monthly usage of X", "show me adoption of <insight>", "is <insight> on track for <target>".
---

# Insight WoW

Produce a usage report for one or more PostHog insights at three cadences:

1. **Daily** — last 14 days, one row per day.
2. **Week-over-week** — rolling 7-day this week vs prior 7-day.
3. **Month-over-month** — rolling 30-day this month vs prior 30-day.

The report mirrors the insight's own filter **including `filterTestAccounts`**, adds a per-customer breakdown the saved insight doesn't show, and (if a feature flag gates the feature) overlays flag-value to distinguish real feature use from URL pokes. Always reports **unique sessions, unique users, unique companies, and events**. Never invent numbers — if data is missing or zero, say so.

> **Critical lesson:** never skip or loosen `filterTestAccounts`. If your team's filter strips internal staff who routinely work inside customer accounts (support, PMs, BDs), bypassing it can inflate numbers **10–30×**. Always mirror the saved insight's full filter and spot-check against the UI before reporting.

## When to use

- User names a PostHog insight (short_id like `B6uU7VE2`, numeric id, or full name) and asks for usage.
- User asks how a recently launched feature is being used over time.
- User asks "is anyone using X?" about a feature with a known insight.
- User asks for daily, weekly, or monthly usage trends.

If the user specifies a cadence ("just WoW", "only daily", "MoM only"), produce only that section. Otherwise produce **all three** by default.

## Targets (required — always ask first)

**Before running any queries, always ask the user for a target.** A usage report without a target is just numbers — the gap analysis is what makes it actionable. Do not skip this step, even if the user only asked for "WoW for <insight>".

Phrase the question concretely, offering the three target types so the user can pick:

> "Before I run this, what's the target?
> - **Reach %** — e.g. *80% of launch customers active this week* (needs a feature flag)
> - **Retention %** — e.g. *keep 70% of last week's active users*
> - **Absolute threshold** — e.g. *≥ 6 active companies this week*, *≥ 50 sessions*"

Parse the response into one of three target types:

| Target type | Example phrasing | What it means | Required input |
|---|---|---|---|
| **Reach %** | "80% WoW", "80% of customers" | % of launch customers active in the period | feature flag (to know N) |
| **Retention %** | "70% retention MoM", "keep 70% of users" | % of *last period's* active entities that are active again *this period* | none |
| **Absolute** | "≥ 6 companies/week", "10 users MoM", "target 50 sessions" | minimum count of the metric in the period | none |

**Default if ambiguous:** If the user says "80% WoW usage" and there's a related feature flag, treat it as **Reach %** of launch customers. If there's no flag, treat as **Retention %** of last week's active companies. Always state your interpretation explicitly in the report.

If multiple targets are given (e.g. "80% WoW reach AND ≥ 50 sessions"), evaluate all of them.

If the user explicitly declines to set a target ("just show me the numbers", "no target"), proceed without one and skip the gap-analysis section — but only after asking.

## How to run

### 1. Resolve the insight(s)

If the user gives a short_id, numeric id, or exact name, resolve via:

```
call insight-get {"id": <numeric_id>}
```

If only a partial name is given, search first:

```sql
SELECT id, short_id, name, description
FROM system.insights
WHERE NOT deleted
  AND (name ILIKE '%<term>%' OR description ILIKE '%<term>%')
ORDER BY id DESC
LIMIT 20
```

Then call `insight-get` on the best match to get the authoritative query. **Always confirm the match with the user if there's more than one plausible candidate.**

### 2. Extract the filter from `query.source.series`

For each EventsNode in the series, capture:

- **Event name** — read the `event` field. **If it's missing/null, the insight counts ALL events** matching the other filters (not just `$pageview`). Mirror that — do not add a `$pageview` filter the saved insight doesn't have.
- **URL filter** — most commonly `$current_url icontains '<value>'`. Capture the value verbatim (e.g. `/checkout`, `dashboard`).
- **Group type index** — usually `0` (company) on the `unique_group` series.
- **`filterTestAccounts`** — read this from `query.source`. If `true`, you **must** mirror it via SQL (step 3). Do not skip it.

Label the count column **"Events"** (not "Pageviews") if the insight has no event filter. Label it as the event name otherwise.

### 3. Read the project's `test_account_filters` and translate to SQL

If `filterTestAccounts: true`, fetch the project's filter definition:

```sql
SELECT test_account_filters FROM system.teams WHERE id = <team_id>
```

Find your team id at the bottom of the PostHog URL when logged in, or via `SELECT id, name FROM system.teams`. The result is a JSON array of filter clauses. Translate **every** clause into SQL — order doesn't matter; the filter is conjunctive. Typical clause types you'll encounter:

| Clause shape | SQL translation |
|---|---|
| `{key: $host, operator: not_icontains, value: 'X'}` (event) | `AND e.properties.$host NOT ILIKE '%X%'` |
| `{key: $host, operator: icontains, value: 'X'}` (event) | `AND e.properties.$host ILIKE '%X%'` |
| `{key: $current_url, operator: not_icontains, value: 'X'}` (event) | `AND e.properties.$current_url NOT ILIKE '%X%'` |
| `{key: $ip, operator: is_not, value: ['A.B.C.D']}` (event) | `AND coalesce(e.properties.$ip, '') != 'A.B.C.D'` |
| `{key: $user_id, operator: is_not, value: ['xxxx']}` (event) | `AND coalesce(e.properties.$user_id, '') != 'xxxx'` |
| `{key: email, operator: not_icontains, value: 'X'}` (event) | `AND coalesce(e.properties.email, '') NOT ILIKE '%X%'` |
| `{key: email, operator: not_icontains, value: 'X'}` (person) | `AND e.person.properties.email NOT ILIKE '%X%'` |
| `{key: email, operator: is_set}` (person) | `AND e.person.properties.email IS NOT NULL AND e.person.properties.email != ''` |
| `{key: email, operator: is_not, value: ['a@b.c']}` (person) | `AND e.person.properties.email != 'a@b.c'` |
| `{key: name, operator: not_icontains, value: 'X', group_type_index: 0}` | filter via excluded-groups CTE on `index = 0` (see template) |
| `{key: name, operator: not_icontains, value: 'X', group_type_index: 1}` | excluded-orgs CTE on `index = 1` |

Note: `NOT ILIKE` returns NULL for NULL values, which propagates as "not matched." Use `coalesce(..., '')` for event properties that might be missing to avoid silently dropping events. For person-property `not_icontains`, always pair with `is_set` (most projects have this paired explicitly already).

### 4. Spot-check against the UI before the full report

After building the full filter clause, run **just the daily query for the most recent day** and compare to PostHog's UI. If it doesn't match, your test_account_filters translation is wrong — fix it before producing the full report.

```sql
-- spot check for one day
WHERE e.timestamp >= toDate('<YYYY-MM-DD>')
  AND e.timestamp < toDate('<YYYY-MM-DD+1>')
  AND <full filter clause>
GROUP BY toDate(e.timestamp)
```

Only proceed once the spot-check matches.

### 5. Run the daily trend

Last 14 days, one row per day. Use this to spot single-day spikes/drops that get hidden in weekly aggregates.

```sql
WITH excluded_companies AS (
  SELECT DISTINCT key FROM groups
  WHERE index = 0 AND (
    properties.name ILIKE '%demo%'
    OR properties.name ILIKE '%Test%'
    OR properties.name ILIKE '%INNOVAT%'
    -- mirror any group_type_index=0 not_icontains filters here
  )
),
excluded_orgs AS (
  SELECT DISTINCT key FROM groups
  WHERE index = 1 AND properties.name ILIKE '%<org_exclude_substring>%'
  -- mirror any group_type_index=1 not_icontains filters here
)
SELECT
  toDate(e.timestamp) as day,
  count() as events,
  count(DISTINCT e.properties.$session_id) as unique_sessions,
  count(DISTINCT e.person_id) as unique_users,
  count(DISTINCT e.$group_0) as unique_companies
FROM events e
WHERE e.timestamp > now() - INTERVAL 14 DAY
  AND e.timestamp <= now()
  -- saved insight filters:
  AND e.properties.<url_property> ILIKE '%<url_value>%'
  -- AND e.event = '<event_from_insight>'  -- omit entirely if insight has no event filter
  -- test_account_filters (when filterTestAccounts: true) — derived from step 3:
  AND e.properties.$host ILIKE '%<your_prod_host>%'
  AND coalesce(e.properties.$ip, '') != '<excluded_ip>'
  AND coalesce(e.properties.$user_id, '') != '<excluded_user_id>'
  AND coalesce(e.properties.email, '') NOT ILIKE '%<internal_email_substring>%'
  AND e.person.properties.email IS NOT NULL AND e.person.properties.email != ''
  AND e.person.properties.email NOT ILIKE '%<internal_email_substring>%'
  AND e.person.properties.email NOT ILIKE '%test%'
  -- add one NOT ILIKE per email substring listed in test_account_filters
  AND e.$group_0 NOT IN (SELECT key FROM excluded_companies)
  AND e.$group_1 NOT IN (SELECT key FROM excluded_orgs)
GROUP BY day
ORDER BY day DESC
LIMIT 14
```

(The exact set of `e.person.properties.email NOT ILIKE` and excluded-name patterns comes from step 3 — keep the query in sync with the live filter, do not hard-code from memory.)

### 6. Run the WoW query

Rolling 7-day windows. Same WHERE clause as daily; wrap in a CTE that buckets each row by week.

```sql
WITH excluded_companies AS (...),
     excluded_orgs AS (...),
filtered_events AS (
  SELECT
    person_id,
    properties.$session_id as session_id,
    $group_0 as company_id,
    if(timestamp >= now() - INTERVAL 7 DAY, 'this_week', 'last_week') as week
  FROM events e
  WHERE timestamp > now() - INTERVAL 14 DAY AND timestamp <= now()
    AND <same filter clause as daily>
)
SELECT week, count() as events,
       count(DISTINCT session_id) as unique_sessions,
       count(DISTINCT person_id) as unique_users,
       count(DISTINCT company_id) as unique_companies
FROM filtered_events GROUP BY week ORDER BY week
```

### 7. Run the MoM query

Rolling 30-day windows. "This month" = last 30 days; "last month" = 31–60 days ago.

```sql
WITH ..., filtered_events AS (
  SELECT person_id, properties.$session_id as session_id, $group_0 as company_id,
         if(timestamp >= now() - INTERVAL 30 DAY, 'this_month', 'last_month') as month
  FROM events e
  WHERE timestamp > now() - INTERVAL 60 DAY AND timestamp <= now()
    AND <same filter clause as daily>
)
SELECT month, count() as events, ... FROM filtered_events GROUP BY month ORDER BY month
```

### 8. Run the per-customer breakdown

Cover all three cadences in a single query bucketed by recency. `bucket` distinguishes "this_week", "last_week", and "older_30d" (8–30 days back).

```sql
WITH excluded_companies AS (...), excluded_orgs AS (...)
SELECT
  g.properties.name as company,
  multiIf(
    e.timestamp >= now() - INTERVAL 7 DAY, 'this_week',
    e.timestamp >= now() - INTERVAL 14 DAY, 'last_week',
    'older_30d'
  ) as bucket,
  count() as events,
  count(DISTINCT e.properties.$session_id) as sessions,
  count(DISTINCT e.person_id) as users
FROM events e
LEFT JOIN groups g ON g.key = e.$group_0 AND g.index = 0
WHERE e.timestamp > now() - INTERVAL 30 DAY AND e.timestamp <= now()
  AND <same filter clause as daily>
  AND e.$group_0 != ''
GROUP BY company, bucket
ORDER BY bucket, events DESC
LIMIT 100
```

### 9. Optional — feature-flag overlay

If the insight is associated with a feature flag (by name match, user statement, or because the feature is gated), capture the flag key and add a per-flag-value cut:

```sql
SELECT e.properties['$feature/<flag-key>'] as flag_value, ...
FROM events e WHERE <same filter clause> GROUP BY flag_value
```

This distinguishes:

- **`flag=true` events** = users who actually had the feature enabled when they hit the URL.
- **`flag=false` events** = users who hit the URL but the gate rejected them (URL pokes, deep links, curiosity).
- **`flag=null/None` events** = flag wasn't evaluated (very rare).

Use bracket notation `properties['$feature/<key>']` because flag keys contain hyphens and slashes that break dot notation. Compare against the string `'true'`, not the boolean — type-checks fail otherwise.

**Flag history matters.** `$feature/<key>` is recorded at event capture time. If the flag definition was edited (companies added/removed), historical events keep their old value. Check the flag's `version` and `updated_at`:

```
call feature-flag-get-definition {"id": <flag_id>}
```

A company can show `flag=true` events from before a rollback and `flag=false` events after — that's the rollback signature. Flag this in the report if it's load-bearing.

### 10. Optional — adoption gap vs a feature flag

If a feature flag is in play, pull its definition and compare its `filters.groups[].properties[].value` (target company names) against the customers seen in the per-customer breakdown.

Report:

- Which launch customers used the feature this week / this month.
- Which launch customers used it last week / last month but not this week.
- Which launch customers have **not** used it at all in 30 days.
- Any non-launch customers seen in the data — but split them: were they `flag=true` (real access, possibly historical from before a rollback) or `flag=false` (URL pokes, no real access)?

### 11. Target gap analysis

Compute one row per (target × cadence) using the target you collected in step 0. Skip cadences the target doesn't apply to. (If the user explicitly declined to set a target, skip this section entirely.)

**Reach %** (requires feature flag):

```
N_target = count of companies in flag rollout (excluding demos)
N_actual = unique_companies in the period (from the WoW or MoM aggregate query, restricted to flag=true)
reach_pct = N_actual / N_target
gap = target_pct - reach_pct        (positive = behind, negative = ahead)
missing = launch_customers \ active_customers_in_period
```

**Retention %** (no flag needed):

```
last_period_companies = set of companies active in the prior window
this_period_companies = set of companies active in the current window
retained = | last_period_companies ∩ this_period_companies |
retention_pct = retained / |last_period_companies|
gap = target_pct - retention_pct
churned = last_period_companies \ this_period_companies
```

For retention, use a query of this shape (swap `$group_0` for `person_id` for user retention, `properties.$session_id` for session retention):

```sql
WITH excluded_companies AS (...), excluded_orgs AS (...),
last_period AS (
  SELECT DISTINCT $group_0 as company_id
  FROM events e
  WHERE timestamp >= now() - INTERVAL 14 DAY AND timestamp < now() - INTERVAL 7 DAY
    AND <same filter clause as daily>
    AND $group_0 != ''
),
this_period AS (
  SELECT DISTINCT $group_0 as company_id
  FROM events e
  WHERE timestamp >= now() - INTERVAL 7 DAY AND timestamp <= now()
    AND <same filter clause as daily>
    AND $group_0 != ''
)
SELECT
  (SELECT count() FROM last_period) as last_period_count,
  (SELECT count() FROM this_period) as this_period_count,
  (SELECT count() FROM last_period l INNER JOIN this_period t ON l.company_id = t.company_id) as retained,
  (SELECT count() FROM last_period l LEFT JOIN this_period t ON l.company_id = t.company_id WHERE t.company_id IS NULL OR t.company_id = '') as churned
```

Adjust intervals to 30 / 60 days for MoM retention.

**Absolute**: compare the metric directly against the threshold.

### 12. Produce the report

Output **exactly** in this format. Use markdown tables, percent change rounded to integers, and `−` (en-dash) for negative deltas. Cap absolute dates to YYYY-MM-DD.

```
<Insight name> usage (<filter description>, filterTestAccounts <on/off>):

### Daily (last 14 days)

| Day        | Events | Sessions | Users | Companies |
|------------|---:|---:|---:|---:|
| <YYYY-MM-DD> | <n> | <n> | <n> | <n> |
| ...        | ... | ... | ... | ... |

### Week-over-week (rolling 7-day)

| Metric           | Last week (<date range>) | This week (<date range>) | WoW |
|------------------|---:|---:|---:|
| Unique sessions  | <n> | <n> | <±n%> |
| Unique users     | <n> | <n> | <±n%> |
| Unique companies | <n> | <n> | <±n%> |
| Events           | <n> | <n> | <±n%> |

### Month-over-month (rolling 30-day)

| Metric           | Last month (<date range>) | This month (<date range>) | MoM |
|------------------|---:|---:|---:|
| Unique sessions  | <n> | <n> | <±n%> |
| Unique users     | <n> | <n> | <±n%> |
| Unique companies | <n> | <n> | <±n%> |
| Events           | <n> | <n> | <±n%> |

### By customer (last 30 days)

**This week (<count>):** <Company A> (<n> ev / <users> user), <Company B> (<n>/<users>), ...

**Last week only (<count>):** <Company A> (<n>/<users>), ...

**Older 30d only (<count>):** <Company A> (<n>/<users>), ...

### Flag overlay (if applicable)

State the flag and its current rollout count. List any companies showing `flag=true` historical events that aren't in the current rollout — these are usually rollback signatures (see step 9).

### Target gap (only if target provided)

State the parsed target up top: e.g. *Target: 80% WoW reach (= 6 of 7 launch companies)*.

| Cadence | Target | Actual | Gap | Status |
|---|---:|---:|---:|:---:|
| WoW | 80% | 29% (2/7) | **−51pp** | ❌ |
| MoM | 80% | 71% (5/7) | −9pp | ⚠️ |

Use:
- ✅ **on track** — actual ≥ target
- ⚠️ **close** — actual within 10pp / 10% of target (for relative / absolute)
- ❌ **behind** — actual missing target by more than 10pp / 10%
- ⏳ **in progress** — current period is still active and shouldn't be judged yet

**Missing customers (Reach %):** list the launch customers who did not use the feature in the period. Always name them — don't just give a count.

**Churned customers (Retention %):** list the last-period customers who did not return this period.

Notes:
- <1–3 bullets on what stands out: daily spikes/drops, deep vs shallow engagement, new vs returning customers, adoption gaps vs the rollout list, anything unexpected.>
- <If filterTestAccounts: false on the saved insight but the user is interested in real customer use, suggest applying the project's test-account filter — internal-staff activity often dominates the signal otherwise.>
- <Flag today's date and note if the current week/month bucket is still active.>
- <If a flag rollback is visible in the data (companies with flag=true history then flag=false), call it out and link to the flag's `updated_at`.>
```

If running for **multiple insights** in one go, repeat the full block per insight, separated by a horizontal rule. Do not produce a combined summary unless asked.

### 13. Render the browser dashboard (always)

After the markdown report is delivered, **always** write the HTML dashboard and open it. This is not optional — every run ends with both a markdown report and a browser-rendered dashboard.

Output a single self-contained HTML file at `~/Desktop/insight-wow-dashboard.html` (overwrites any prior render — the user can rename to keep history). After writing, open it with `open <path>` on macOS.

**Required sections (in order):**

1. **Header** — Title, generation date, PostHog project + ID, filter description (saved-insight, filterTestAccounts on/off), and any related flag with rollout count.
2. **Reach matrix** — ONLY if 2+ insights share a feature flag. Rows = each launch customer; columns = each feature × {this week, last week, older 30d}. Cells show event count (green) or `—` (red, no events).
3. **Per-insight blocks** (one per insight) containing:
   - KPI cards: companies, users, sessions, events for *this week*, each with WoW delta and "from N last week" caption.
   - Daily trend chart (last 14 days, Chart.js line chart, dual y-axis: left for companies/users/sessions, right for events).
   - WoW table (rolling 7-day, same shape as the markdown report).
   - MoM table (rolling 30-day, same shape).
4. **Findings** — 3–5 bullet takeaways from the analysis. Same content as the markdown report's Notes section.
5. **Methodology footer** — Brief note on what filter was applied, mention any UI spot-check that was performed.

**Design language (Bridgewater-inspired):**

- Warm off-white background (`#f6f4ee`), white surface cards.
- Charcoal/ink text (`#1a1d23`), navy primary accent (`#1e2c4f`).
- Restrained color: green (`#2c6f44`) and red (`#a83232`) only for deltas and matrix hit/miss.
- Tabular numbers (`font-variant-numeric: tabular-nums`).
- Generous whitespace, thin borders (`#e3dfd4`).
- Georgia serif for headings, Inter / system-sans for body.
- Subtle tan accents (`#efe9d6`) for table headers and code spans.
- No shadows, no gradients, no emojis.

**Reusable template** — substitute `{{placeholders}}` with computed values; repeat the per-insight `<section>` block N times for N insights; omit the `Launch customer reach` section when only one insight is in play.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{{title}}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  :root {
    --bg: #f6f4ee; --surface: #ffffff;
    --border: #e3dfd4; --border-strong: #c9c2af;
    --ink: #1a1d23; --ink-soft: #5b5e66; --ink-mute: #98978d;
    --accent: #1e2c4f; --accent-soft: #4a5a82;
    --pos: #2c6f44; --neg: #a83232; --warn: #b87a1f;
    --tan: #d9cfb3; --tan-soft: #efe9d6;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: var(--bg); color: var(--ink); }
  body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif; font-size: 14px; line-height: 1.5; -webkit-font-smoothing: antialiased; }
  .wrap { max-width: 1240px; margin: 0 auto; padding: 48px 32px 80px; }
  header { border-bottom: 1px solid var(--border-strong); padding-bottom: 24px; margin-bottom: 40px; }
  header h1 { font-family: 'Georgia', 'Times New Roman', serif; font-weight: 500; font-size: 32px; letter-spacing: -0.01em; margin: 0 0 6px; }
  header .meta { font-size: 13px; color: var(--ink-soft); }
  header .meta span { margin-right: 18px; }
  header .meta b { color: var(--ink); font-weight: 500; }
  section { margin-bottom: 56px; }
  h2 { font-family: 'Georgia', serif; font-weight: 500; font-size: 22px; letter-spacing: -0.005em; margin: 0 0 4px; }
  h2 .subtle { color: var(--ink-soft); font-size: 14px; font-family: 'Inter', sans-serif; font-weight: 400; margin-left: 10px; }
  h3 { font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--ink-soft); font-weight: 600; margin: 32px 0 12px; }
  .reach-banner { background: var(--surface); border: 1px solid var(--border); padding: 24px 28px; margin-bottom: 24px; display: grid; grid-template-columns: repeat({{n_features}}, 1fr); gap: 32px; }
  .reach-banner .item .label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--ink-soft); margin-bottom: 6px; }
  .reach-banner .item .value { font-family: 'Georgia', serif; font-size: 28px; }
  .reach-banner .item .value .denom { color: var(--ink-soft); font-size: 18px; }
  .reach-banner .item .pct { color: var(--ink-soft); font-size: 13px; margin-left: 8px; }
  .kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }
  .kpi { background: var(--surface); border: 1px solid var(--border); padding: 18px 20px; }
  .kpi .label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--ink-soft); margin-bottom: 8px; }
  .kpi .value { font-family: 'Georgia', serif; font-size: 28px; line-height: 1; margin-bottom: 6px; }
  .kpi .delta { font-size: 12px; font-variant-numeric: tabular-nums; }
  .kpi .delta .from { color: var(--ink-soft); }
  .pos { color: var(--pos); } .neg { color: var(--neg); } .neu { color: var(--ink-soft); }
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }
  .panel { background: var(--surface); border: 1px solid var(--border); padding: 24px 24px 28px; }
  table { width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }
  th, td { text-align: left; padding: 8px 12px; border-bottom: 1px solid var(--border); }
  th { font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--ink-soft); font-weight: 600; background: var(--tan-soft); border-bottom: 1px solid var(--border-strong); }
  td.num, th.num { text-align: right; }
  tbody tr:hover { background: #fafaf2; }
  .chart-wrap { position: relative; height: 260px; margin: 16px 0 4px; }
  .matrix { width: 100%; border-collapse: collapse; font-size: 13px; font-variant-numeric: tabular-nums; }
  .matrix th, .matrix td { padding: 10px 12px; border-bottom: 1px solid var(--border); border-right: 1px solid var(--border); }
  .matrix th { background: var(--tan-soft); font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--ink-soft); font-weight: 600; }
  .matrix th.feature { background: var(--tan); color: var(--ink); border-bottom: 1px solid var(--border-strong); }
  .matrix th.bucket { font-weight: 500; text-transform: none; letter-spacing: 0; }
  .matrix td.company { font-weight: 500; }
  .matrix td.cell { text-align: center; }
  .matrix td.hit { background: #e8f0e6; color: var(--pos); font-weight: 500; }
  .matrix td.miss { background: #f7eded; color: var(--neg); }
  .matrix td.weak { background: #faf6e8; color: var(--warn); }
  .notes { background: var(--surface); border: 1px solid var(--border); padding: 24px 28px; }
  .notes ul { margin: 0; padding-left: 18px; }
  .notes li { margin-bottom: 8px; }
  .notes .small { font-size: 12px; color: var(--ink-soft); margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border); }
  footer { margin-top: 56px; padding-top: 24px; border-top: 1px solid var(--border); font-size: 12px; color: var(--ink-soft); }
  footer code, .notes code { background: var(--tan-soft); padding: 1px 6px; font-size: 11.5px; }
  @media (max-width: 900px) { .two-col, .kpis, .reach-banner { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<div class="wrap">

<header>
  <h1>{{title}}</h1>
  <div class="meta">
    <span>Generated <b>{{date}}</b> ({{tz}})</span>
    <span>PostHog project <b>{{project_name}}</b> ({{project_id}})</span>
    <span>Filter: <b>saved-insight, filterTestAccounts {{on_off}}</b></span>
    {{#if flag}}<span>Launch flag: <b>{{flag_key}}</b> · {{rollout_count}} customers</span>{{/if}}
  </div>
</header>

<!-- Reach matrix: include only if 2+ features share a flag -->
<section>
  <h2>Launch customer reach <span class="subtle">{{rollout_count}} customers · last 30 days</span></h2>
  <div class="reach-banner">
    {{#each features}}
    <div class="item">
      <div class="label">{{name}} · this week</div>
      <div class="value">{{active_this_week}} <span class="denom">/ {{rollout_count}}</span><span class="pct">{{reach_pct}}% reach</span></div>
    </div>
    {{/each}}
  </div>
  <table class="matrix">
    <thead>
      <tr>
        <th rowspan="2" style="vertical-align:bottom">Launch customer</th>
        {{#each features}}<th class="feature" colspan="3">{{name}}</th>{{/each}}
      </tr>
      <tr>
        {{#each features}}
        <th class="bucket">This week</th><th class="bucket">Last week</th><th class="bucket">Older 30d</th>
        {{/each}}
      </tr>
    </thead>
    <tbody>
      {{#each customers}}
      <tr>
        <td class="company">{{name}}</td>
        {{#each cells}}<td class="cell {{cls}}">{{value}}</td>{{/each}}
      </tr>
      {{/each}}
    </tbody>
  </table>
</section>

<!-- Per-insight block — repeat for each insight -->
<section>
  <h2>{{insight.name}} <span class="subtle">$current_url icontains <code>{{insight.url_filter}}</code></span></h2>
  <div class="kpis">
    {{#each insight.kpis}}
    <div class="kpi">
      <div class="label">{{label}}</div>
      <div class="value">{{value}}</div>
      <div class="delta"><span class="{{delta_class}}">{{delta}}</span> <span class="from">from {{prev}} last week</span></div>
    </div>
    {{/each}}
  </div>
  <div class="panel">
    <h3>Daily trend (last 14 days)</h3>
    <div class="chart-wrap"><canvas id="{{insight.chart_id}}"></canvas></div>
  </div>
  <div class="two-col" style="margin-top:28px;">
    <div class="panel">
      <h3>Week-over-week (rolling 7-day)</h3>
      <table>
        <thead><tr><th>Metric</th><th class="num">Last week</th><th class="num">This week</th><th class="num">WoW</th></tr></thead>
        <tbody>{{insight.wow_rows}}</tbody>
      </table>
    </div>
    <div class="panel">
      <h3>Month-over-month (rolling 30-day)</h3>
      <table>
        <thead><tr><th>Metric</th><th class="num">Last month</th><th class="num">This month</th><th class="num">MoM</th></tr></thead>
        <tbody>{{insight.mom_rows}}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="notes">
  <h2>Findings</h2>
  <ul>{{#each findings}}<li>{{text}}</li>{{/each}}</ul>
  <div class="small"><strong>Methodology.</strong> {{methodology}}</div>
</section>

<footer>{{footer}}</footer>

</div>

<script>
const COLORS = { ink: '#1a1d23', soft: '#5b5e66', navy: '#1e2c4f', navySoft: '#4a5a82', tan: '#b89b5e', pos: '#2c6f44', border: '#e3dfd4' };

// One entry per insight; values are arrays aligned to `labels` (14 days, oldest→newest)
const DATA = {{chart_data_json}};
// { "<chart_id>": { labels: [...], events: [...], sessions: [...], users: [...], companies: [...] }, ... }

function buildChart(canvasId, data) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.labels.map(d => d.slice(5)),
      datasets: [
        { label: 'Companies', data: data.companies, borderColor: COLORS.navy, borderWidth: 2, tension: 0.25, pointRadius: 3, yAxisID: 'yLeft' },
        { label: 'Users', data: data.users, borderColor: COLORS.navySoft, borderWidth: 1.5, borderDash: [4,3], tension: 0.25, pointRadius: 2, yAxisID: 'yLeft' },
        { label: 'Sessions', data: data.sessions, borderColor: COLORS.tan, borderWidth: 1.5, tension: 0.25, pointRadius: 2, yAxisID: 'yLeft' },
        { label: 'Events', data: data.events, borderColor: COLORS.pos, backgroundColor: 'rgba(44,111,68,0.05)', borderWidth: 1.5, tension: 0.25, pointRadius: 2, yAxisID: 'yRight', fill: true },
      ],
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { align: 'end', labels: { boxWidth: 10, boxHeight: 10, color: COLORS.soft, font: { size: 12 } } },
        tooltip: { backgroundColor: '#fff', titleColor: COLORS.ink, bodyColor: COLORS.ink, borderColor: COLORS.border, borderWidth: 1, padding: 10 },
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: COLORS.soft, font: { size: 11 } } },
        yLeft: { position: 'left', beginAtZero: true, grid: { color: COLORS.border }, ticks: { color: COLORS.soft, font: { size: 11 } }, title: { display: true, text: 'Companies / Users / Sessions', color: COLORS.soft, font: { size: 11 } } },
        yRight: { position: 'right', beginAtZero: true, grid: { display: false }, ticks: { color: COLORS.soft, font: { size: 11 } }, title: { display: true, text: 'Events', color: COLORS.soft, font: { size: 11 } } },
      },
    },
  });
}

Object.entries(DATA).forEach(([id, d]) => buildChart(id, d));
</script>
</body>
</html>
```

**Placeholder cheat-sheet:**

- `{{title}}` → e.g. *"Load Planning & Portfolio — Usage Report"*
- `{{date}}` → today as `YYYY-MM-DD`; `{{tz}}` → `CEST`/`UTC`
- `{{project_name}}` / `{{project_id}}` → the PostHog project name and numeric id
- `{{on_off}}` → `ON` or `OFF` depending on `filterTestAccounts`
- `{{flag_key}}` / `{{rollout_count}}` → if a flag is in play
- `{{features[]}}` → one entry per insight, with `name`, `active_this_week`, `reach_pct`
- `{{customers[]}}` → one row per launch customer; `cells[]` ordered matching the `features × buckets` header (3 cells per feature). Cell `cls` is `hit` (used), `miss` (no events, value `—`), or `weak` (very low, optional). Cell `value` is the event count or `—`.
- `{{insight.kpis[]}}` → 4 cards in order: Companies, Users, Sessions, Events. Each has `label`, `value`, `delta` (e.g. `−43%`), `delta_class` (`pos`/`neg`/`neu`), `prev`.
- `{{insight.chart_id}}` → CSS-safe id e.g. `lpChart`, `pfChart`. Must match a key in `DATA`.
- `{{insight.wow_rows}}` / `{{insight.mom_rows}}` → 4 `<tr>` strings per table (sessions, users, companies, events).
- `{{chart_data_json}}` → JSON object mapping each `chart_id` to `{ labels, events, sessions, users, companies }`. Arrays must be the same length (14 days), ordered oldest→newest, with `0` for missing days. `labels` is `YYYY-MM-DD` strings.
- `{{findings[]}}` → 3–5 short HTML strings (can include `<strong>`).
- `{{methodology}}` → one sentence summarising the filter and any UI verification done.
- `{{footer}}` → source citation: project + insight short_ids + flag id + version.

After writing the file:

```bash
open ~/Desktop/insight-wow-dashboard.html
```

**Verify the render.** Don't claim the dashboard renders correctly unless you actually opened it. If you have agent-browser or a screenshot tool, take a quick screenshot to confirm; otherwise just open it and trust the user will flag issues.

## Hard rules

- **Mirror `filterTestAccounts` when set on the saved insight.** Do not skip or loosen it — in projects where staff routinely act inside customer accounts, internal-staff usage can be 10–30× of real customer traffic, and stripping it is the whole point of the filter. Read `test_account_filters` from `system.teams` and translate every clause to SQL.
- **No event filter ≠ `$pageview` filter.** If the saved insight has no `event` field on its EventsNode, mirror that — count ALL events on the URL, not just pageviews. Label the count column "Events", not "Pageviews."
- **Spot-check one day against the UI before producing the full report.** If the spot-check doesn't match, your filter translation is wrong. Fix it before delivering numbers.
- **Always use rolling windows** (`now() - INTERVAL N DAY`). Never use `toStartOfWeek` or `toStartOfMonth` for the headline numbers — they split the current period mid-stream.
- **Don't compare like-for-like across uneven windows.** This-week-so-far vs full-last-week is misleading — call this out in Notes when relevant.
- **Never use `$pathname`** in `execute-sql` — it doesn't resolve. Use `properties.$pathname` or `properties.$current_url`.
- **Group table uses `index`, not `group_type_index`.** Filter with `WHERE index = 0` for company-level groups.
- **Feature-flag property keys need bracket notation:** `properties['$feature/<flag-key>']` — dot notation breaks on hyphens and slashes. Compare against the string `'true'`, not boolean.
- **`$feature/<key>` is a capture-time value.** A flag rollback (adding/removing customers) creates a "before/after" split in the data — old events keep their old value. Check the flag's `version` and `updated_at` to interpret this.
- **One flag can gate multiple features.** Don't assume 1:1 mapping by name — a single flag often gates several related URLs/features. Ask if uncertain.
- **PostHog captures `$pageview` regardless of how the flag evaluates.** Companies showing up on a URL filter aren't necessarily using the feature — they may have hit the URL and gotten an empty state / redirect. Use `properties['$feature/<flag>'] = 'true'` to count real flag-enabled use.
- **Don't claim "0 this week is a drop"** if today is early in the week — call out that the window is still active. The PostHog `execute-sql` response also adds a system reminder about this; respect it but still surface the comparison.
- **Verify launch customers against the live flag definition.** Don't rely on memory — flag rollouts change. Use `feature-flag-get-definition` to get the current rollout list.
- **Run the four SQL queries in parallel** (daily, WoW, MoM, per-customer) — they're independent and parallel cuts latency 4×. If a target is given, add the retention SQL to the parallel batch. If a flag is in play, also add the flag-overlay query.
- **Always ask for a target before running.** Don't skip this step — even a one-line "what's the target?" prompt before queries is mandatory. State the parsed interpretation explicitly so the user can correct you (e.g. "interpreting as 80% of launch customers active per week").
- **Reach % requires the flag.** If the user asks for "80% reach" but the insight has no associated feature flag, ask which population to measure against (all paying customers? a specific list?) instead of guessing.
- **Don't penalise an active period.** If today is mid-week / mid-month, flag the in-progress window in the status column ("⏳ in progress") rather than ❌ — partial-period numbers extrapolated to a full-period target are misleading.
- **Always render the browser dashboard.** Every run ends with both a markdown report and an HTML dashboard written to `~/Desktop/insight-wow-dashboard.html` and opened via `open`. Reuse the template in step 13 — don't invent new visual styles per request, the design language is fixed.

## Project-specific defaults (recommended)

The first time you run this skill on a new PostHog project, it pays to cache the inputs you'd otherwise re-derive every call. Add a section like the one below to your local copy of this skill so future runs can jump straight to step 3.

### Insight defaults

For each insight you query repeatedly, record:

| Insight name | short_id | id | Event filter | URL filter (icontains) | filterTestAccounts | Related flag |
|---|---|---|---|---|---|---|
| `<insight name>` | `<short_id>` | `<id>` | `<event or "none">` | `<url substring>` | `true` / `false` | `<flag key (id)>` |

**Re-verify with `insight-get` before relying on cached values** — saved insight queries get edited.

### `test_account_filters` snapshot

Cache the project's resolved test-account filter so SQL translation is mechanical. Refresh by querying `SELECT test_account_filters FROM system.teams WHERE id = <team_id>` — entries get added and removed over time.

Typical clauses to expect (the exact set is project-specific):

- Event: `$host` must contain your prod host (excludes staging, localhost, custom hosts)
- Event: `$host` / `$current_url` must NOT contain `localhost` or staging hosts
- Event: `$ip` is_not `<office_ip>`
- Event: `$user_id` is_not `<known_internal_id>`
- Event/Person: `email` not_icontains `<your-company-domain>`
- Person: `email` is_set
- Person: `email` not_icontains: `test`, plus any noisy free-email domains you've blocklisted
- Group (companies / orgs): `name` not_icontains `Test`, `Demo`, and any internal test-org substrings

The single most impactful clause in most projects is **`person.email not_icontains <your-company-domain>`** — it removes internal staff acting inside customer accounts, which would otherwise dominate the data.
