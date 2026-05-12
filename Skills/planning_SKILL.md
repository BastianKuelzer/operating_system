---
name: planning
description: Generate a tight, opinionated planning doc for a feature, experiment, or initiative using a 7-section template (Problem, Hypothesis, Customer Value, Reach, Success Metric, Rollout, Capacity). Use when the user wants to plan, scope, or pitch a piece of work before building it. Triggers on "/planning", "plan this", "draft a plan for X", "write a planning doc", or any request to structure an idea into a shippable plan.
---

# Planning

You help the user turn an idea, feature, or initiative into a tight planning document using a fixed 7-section template. The goal is a one-page plan that is data-backed, measurable, and decision-ready — not a brainstorm.

## How to run

1. If the user hasn't provided the topic to plan, ask: "What are we planning?" Then ask only the minimum follow-ups needed to fill the sections — do not pad with discovery questions.
2. Pull data where you can (codebase, Linear, Notion, memory). If a number is missing, write `TBD — <what to measure and where>` rather than inventing a value. Never fabricate metrics.
3. Keep every section short. The whole doc should fit on one screen. Cut anything that isn't load-bearing for a go/no-go decision.
4. Output the plan using the exact section structure below. Do not add extra sections, intros, or summaries.

## Section structure

Render the plan in this exact format:

```
# Plan: <title>

## 1. Problem
<2 sentences. State the problem and back it with a specific data point.>
Example: "Users are turning off notifications at a high rate. 8% of users muted notifications in the last 30 days, up from 3% in Q4."

## 2. Hypothesis
<What you believe will happen and how the problem will be solved. One short paragraph. Format: "If we <change>, then <expected outcome>, because <reasoning>.">

## 3. Customer Value
<What the customer gets when this is solved. Quantify in financials or time saved where possible (e.g. "saves €X/month per customer", "removes 2 hours/week of manual work"). If non-financial, state the concrete user benefit.>

## 4. Reach
**Affected:** <How many customers / users / accounts are affected. Absolute number AND % of base. e.g. "~1,200 users (18% of MAU)".>
**Install base:** <Total current customers as an absolute number. e.g. "6,500 customers".>
**Target market:** <Total addressable market as an absolute number. e.g. "85,000 accounts in TAM".>

## 5. Success Metric
**Primary:** <specific metric with threshold, e.g. "Mute rate drops to ≤ 15% within 4 weeks of rollout.">
**Guardrails:** <metrics that must NOT regress, with thresholds. e.g. "High-priority CTA click-through does not drop below 2%. DAU does not decrease by more than 1%.">

> Before writing this section, read `/Users/bastiankulzer/Desktop/Github_Operating_System/Knowledge/kpis-on-different-layers.md` and use it to pick the right KPI layer (input vs. output, leading vs. lagging, team vs. company) and to ground the chosen primary metric and guardrails in that framework.

## 6. Rollout
**Exposure:** <% of users or specific cohort>
**Duration:** <time window>
**Kill criteria:** <specific condition that triggers rollback>
Example: "10% of users, 2 weeks. Kill if mute rate does not improve by ≥ 5 percentage points vs. control by day 10."

## 7. Capacity
<Estimated effort in person-days, broken down by role.>
- Engineering: <X days>
- Design: <X days>
- Product: <X days>
- Other (QA, Data, etc.): <X days if applicable>
Total: <sum> person-days
```

## Rules

- **Be specific.** Replace vague words ("improve", "increase", "soon") with numbers and dates.
- **No filler.** If a section can be one sentence, make it one sentence.
- **Mark gaps explicitly.** Unknown numbers become `TBD — <how to find it>`, never guesses.
- **One decision per plan.** If the user describes multiple loosely-related ideas, ask which one to plan first rather than mashing them together.
- **No closing summary.** End at Section 7.
