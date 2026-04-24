# KPIs on Different Layers

A structured framework for product managers to define what their product area is responsible for, identify the right metrics at each organizational level, and connect daily work to business outcomes.

---

## Why PMs Struggle with Data

Most PMs are not effectively data-driven despite having more data available than ever before.

| # | Failure Mode | Description |
|---|---|---|
| 1 | **Too many metrics** | Dashboards with 30+ metrics produce no clear signal |
| 2 | **Vanity metrics** | Numbers that go up easily but don't reflect real impact |
| 3 | **Solution-level metrics** | Measuring individual features rather than product area outcomes |
| 4 | **No business connection** | Work isn't tied to what the supervisor or company cares about |

Being data-driven does not mean analyzing results after the fact. It means using data to make better decisions upfront and evaluating outcomes over time.

---

## The Three Layers

Each PM operates at three simultaneous altitudes — their own, their supervisor's above, and the solution space below.

```
┌─────────────────────────────────────────────────────────────┐
│  SUPERVISOR'S ALTITUDE                                       │
│  The outcome metrics your supervisor owns                    │
├─────────────────────────────────────────────────────────────┤
│  PM'S ALTITUDE                                               │
│  Your product area — where you own outcomes                  │
├─────────────────────────────────────────────────────────────┤
│  SOLUTION ALTITUDE                                           │
│  Individual features and bundles of features                 │
└─────────────────────────────────────────────────────────────┘
```

| Layer | What It Is | Tool |
|---|---|---|
| **Supervisor's Altitude** | The outcome metrics your supervisor owns | Supervisor's Metric Scorecard |
| **PM's Altitude** | Your product area — qualitative + quantitative definition | Qualitative Description + Altitude Scorecard |
| **Solution Altitude** | Individual features and feature bundles | Solution Scorecard |

---

## 7-Step Build Process

Steps 1–4 define the PM's altitude. Steps 5–7 define the solution altitude.

| Step | Name | Output |
|---|---|---|
| 1 | Identify the Altitudes | Org chart breakdown: product lines → product areas |
| 2 | Build Supervisor's Metric Scorecard | ≤3 metrics across Acquisition, Retention, Monetization |
| 3 | Qualitative Altitude Description | Product area name, target audience, user value, business value |
| 4 | Build Altitude Scorecard | 3–5 metrics: Adoption, Retention, User Value, Monetization, Business Impact |
| 5 | Map Solution Space | Index of features and feature bundles in the product area |
| 6 | Qualitative Solution Description | Per-solution: audience, user value, business value |
| 7 | Build Solution Scorecards | Per-solution quantitative assessment against altitude metrics |

---

## Step 1 & 2: Identify Altitudes and Supervisor Scorecard

### Identifying the Altitudes

Break the product into product lines, then product areas. Each PM owns exactly one altitude — the product area they are responsible for.

- **Product Line** — a group of related product areas owned by a VP or senior leader (e.g., "Jira Service Management")
- **Product Area** — a specific area owned by a single PM (e.g., "Jira Service Management Reports")

**Example — Jira:**
- Atlassian → Jira → Jira Service Management → Jira Service Management Reports ← Name X's altitude

**Example — abc:**
- abc → Abcunity ← Name X's altitude (community & communication tools)

### Supervisor's Metric Scorecard

Captures the outcome metrics the supervisor owns — the layer above the PM. Maximum 3 metrics. These are not the PM's metrics; they belong to the supervisor's altitude.

| Category | Question It Answers |
|---|---|
| **Acquisition** | How many new users or accounts are we bringing in? |
| **Retention** | How many users are staying and returning? |
| **Monetization** | How much revenue is the product generating? |

**Why it matters:** The PM will later identify which of these metrics their product area drives most directly — this becomes the Business Impact metric on their own scorecard.

**Example — Name X's supervisor's scorecard (Jira Service Management):**

| Category | Metric |
|---|---|
| Acquisition | # of new Jira Service Management accounts |
| Retention | # of monthly Jira Service Management retained users |
| Monetization | Jira Service Management revenue |

**Example — Name X's supervisor's scorecard (abc):**

| Category | Metric |
|---|---|
| Acquisition | # of new abc accounts |
| Retention | M5 retention rates of all users |
| Monetization | abc revenue |

---

## Step 3: Qualitative Altitude Description

Before defining metrics, understand the altitude qualitatively. This prevents losing sight of the main user problem by going too granular into individual feature problems.

> When a PM dives into granular sub-problems, attention can easily stray from the main user problem — wasting time and attention on tangential issues.

### Template

| Component | Question |
|---|---|
| **Product Area Name** | A simple title and description for the product area |
| **Target Audience — Description** | Who does my work primarily serve? |
| **Target Audience — Size** | How big is the target audience? |
| **Target Audience — Relevant Segments** | What are the best ways to segment this target audience? |
| **User Value — Problem Description** | What user problem does the product area solve? |
| **User Value — Core Actions** | What 2–5 core actions does the user need to take to solve their problem? |
| **Business Value** | How does solving the customer problem create value for the business? |

### Target Audience

| Component | Description |
|---|---|
| **Description** | Who the target user is — their role and context |
| **Size** | Absolute or relative size of the audience; feeds directly into the adoption metric denominator |
| **Relevant Segments** | The most meaningful ways to split the audience (e.g., by company size, usage frequency, persona) |

### User Value

**Problem Description** — scoped to the product area, not the whole product and not individual features.

**Core Actions** — the 2–5 actions a user takes to solve the problem; should stem directly from the problem description.

| Type | Example |
|---|---|
| Collaborating with team members | Working together to complete a shared task |
| Consuming content | Reading, watching, or browsing information |
| Generating content | Creating, posting, or publishing |

### Business Value

Key question: *"How does solving the customer problem create value for the business?"*

It is essential to create value for both the user and the business — not one or the other.

### Worked Example: Name X (Jira Service Management Reports)

| Field | Value |
|---|---|
| Product Area Name | Jira Service Management Reports |
| Product Area Description | Reporting functionality for operational teams managing service work using Jira Service Management Reports |
| Target Audience — Description | Service teams (operational teams managing service desk work) in Jira |
| Target Audience — Size | 10% of Jira Service Management active user base |
| Target Audience — Relevant Segments | By company size; Number of service teams managing service work within Jira; Length of time using the product |
| User Value — Problem Description | Managers need to understand work being done and manage work within a service team — driving operational efficiency with high satisfaction |
| User Value — Core Actions | Creating reports, viewing reports, sharing reports |
| Business Value | Making Jira Service Management the best management tool for service teams; materializes as: 1. Teams retain longer due to reporting utility; 2. Teams become more efficient (reduced time to close tickets) |

### Worked Example: Name X (Abcunity @ abc)

| Field | Value |
|---|---|
| Product Area Name | Abcunity |
| Product Area Description | Communication and community-building tools for groups and individuals |
| Target Audience — Description | Community members: Active abc users looking for friends & communities (streamers, active watchers) |
| Target Audience — Size | Top 30% of abc's active user base |
| Target Audience — Relevant Segments | Lurkers (consumers) vs Engagers (paying, posting, commenting, streaming) |
| User Value — Problem Description | Users feel disconnected and want a sense of belonging/purpose through access to up-to-date information and a 24/7 support system they can trust and relate to |
| User Value — Core Actions | Viewing/liking/sharing content, watching live streams |
| Business Value | Unlocking participatory experiences; enables more asynchronous content on the platform, which drives deeper engagement and better retention |

---

## Step 4: Altitude Scorecard

### Why Wrong Metrics Stall Careers

| # | Trap | Description |
|---|---|---|
| 1 | **North Star over-optimization** | Optimizing so hard on a single metric that side effects are created and the full picture is missed |
| 2 | **Vanity metrics** | Metrics that go up easily but don't reflect real value (e.g., raw page views, total signups) |
| 3 | **Solution-level metrics** | Measuring individual features instead of product area outcomes; doesn't connect work to business impact |

### The Five Scorecard Categories

Total scorecard size: **3–5 metrics** — including 1–2 business impact metrics, plus a mix from the remaining categories.

Sense check: *"Looking forward to a year from now, if I only had three or four metrics on my scorecard, and all those metrics have gone up, could I hang my hat on that and say I've nailed it?"* — Name X

| Category | Key Question | Notes |
|---|---|---|
| **Adoption (Acquisition)** | How well are we reaching the target audience? | Denominator = target audience size from qualitative description |
| **Retention** | How well are we solving the relevant user problem? | Formula: Frequency (X) × Core Action (a) × Who (Y) = XaY |
| **User Value** | How well does our product area deliver value to users? | Always a proxy metric — evolve over time |
| **Monetization** | How much revenue is our product area creating? | Most rare — only include if direct tie to revenue |
| **Business Impact** | How well are we creating value for the business? | Pull from supervisor's scorecard, do not invent new metrics |

---

### Adoption

How well are we reaching the target audience?

```
# of target users using the product area
─────────────────────────────────────────
Total target audience size
```

The denominator is the Target Audience Size defined in the qualitative altitude description.

| Example | Metric |
|---|---|
| Name X (Jira) | # of service teams using Jira Service Management reporting functionality |
| Name X (abc) | # of users using Groups, Group Chats, or Team features |

---

### Retention

How well are we solving the relevant user problem? Defined using the formula: **Frequency (X) × Core Action (a) × Who (Y)**

| Component | Description |
|---|---|
| **Frequency (X)** | How often a user experiences the problem — the natural cadence |
| **Core Action (a)** | An action that shows the product is solving the user's problem |
| **Who (Y)** | The type of user that experiences the problem |

**Three levels of "who" — from broadest to most meaningful:**

| Level | Definition |
|---|---|
| 1 | All current users |
| 2 | Target audience |
| 3 | Target audience who completed the core action at the designated frequency *(most meaningful)* |

This also enables retention as a percentage:

```
# of target audience completing core action at frequency
─────────────────────────────────────────────────────────
# of active adopted users
= % of retained users
```

| Example | Metric |
|---|---|
| Name X (Jira) | # of service teams using Jira Service Management reporting functionality weekly (WAU) |
| Name X (abc) | # of users using Community & Communication features weekly (WAU) |

---

### User Value

How well does our product area deliver value to users? User value can never be measured directly — it is always a proxy metric. Start from the qualitative altitude description: what does solving the user problem look like?

**Engagement metrics** are the most common proxy, with three types:

| Type | What It Measures |
|---|---|
| **Frequency** | How often users engage with the product area (core action completion rate) |
| **Intensity** | Intensity per use — time spent, money spent, number of activities performed |
| **Breadth** | % of relevant features users engage with in the product area |

**Important:** Engagement is not always the best proxy. For Confluence, weekly active users is a weak signal — a user reading passively is not the same as a user creating content. Better alternatives: content consumption, content creation, % of consumers who are also creators.

Any user value metric is a proxy. Evolve the altitude scorecard over time to find better measures.

| Example | Metric | Note |
|---|---|---|
| Name X (Jira) | # of report views per team per week | Engagement (intensity); acknowledged as imperfect proxy |
| Name X (abc) | (# minutes streaming + # messages sent + # comments/posts/likes) / WAU | Composite engagement metric |

---

### Monetization

How much revenue is our product area creating for the company?

This is the most rare metric — only relevant when the product area has a direct tie to revenue generation.

| Form | Description |
|---|---|
| **Total revenue** | Absolute revenue generated |
| **Breadth** | Number of paid customers |
| **Depth** | Revenue per customer (e.g., ARPU — Average Revenue Per User) |

| Situation | Include Monetization? |
|---|---|
| PM working on discounting and pricing | Yes |
| PM working on user onboarding | No |

---

### Business Impact

How well are we creating value for the business?

This connects the PM's altitude to the supervisor's scorecard. There is no need to generate new metrics — identify which metric on the supervisor's scorecard the product area drives most directly. Use the Business Value section of the qualitative altitude description to reason through the choice.

Key question: *"Which metric on my supervisor's scorecard indicates how well our product area is creating business value?"*

| Example | Reasoning | Business Impact Metric |
|---|---|---|
| Name X (Jira) | Qualitative description noted business value materializes as teams retaining longer | # of monthly Jira Service Desk retained users (and retention rate) |
| Name X (abc) | Qualitative description noted Abcunity enables deeper engagement and better retention | M5 retention rates of all users |

---

### Complete Altitude Scorecards

**Name X — Jira Service Management Reports**

| Category | Metric |
|---|---|
| Adoption (Acquisition) | # of service teams using Jira Service Management reporting functionality |
| Retention | # of service teams using Jira Service Management reporting functionality weekly (WAU) |
| User Value | # of report views per team per week |
| Monetization | N/A |
| Business Impact | # of monthly Jira Service Desk retained users (and retention rate) |

**Name X — Abcunity @ abc**

| Category | Metric |
|---|---|
| Adoption (Acquisition) | # of users using Groups, Group Chats, or Team features |
| Retention | # of users using Community & Communication features weekly (WAU) |
| User Value | (# minutes streaming/watching + # messages sent + # comments/posts/likes) / WAU |
| Monetization | N/A |
| Business Impact | M5 retention rates of all users |

---

## Using the KPI Layer Map

### Complete Map Structure

```
┌──────────────────┬──────────────────────────────────────────────┐
│ Supervisor's     │ Supervisor's Metric Scorecard                 │
│ Altitude         │ Outcome metrics the supervisor owns           │
├──────────────────┼────────────────────┬─────────────────────────┤
│ PM's Altitude    │ Qualitative        │ Altitude Scorecard       │
│                  │ Description        │ 3–5 metrics; how we      │
│                  │ Audience, user     │ quantitatively evaluate  │
│                  │ value, biz value   │ impact over time         │
├──────────────────┼────────────────────┴─────────────────────────┤
│ Solution         │ Solution Scorecard                            │
│ Altitude         │ Major features + bundles assessed against     │
│                  │ altitude metrics                              │
└──────────────────┴──────────────────────────────────────────────┘
```

### Product Decisions as Bets

Framework from Annie Duke (*Thinking in Bets*): every product decision is a bet — not a certainty.

| Bet Type | Question |
|---|---|
| **User Value Bet** | Will this feature solve a user problem? |
| **Business Value Bet** | Will solving this user problem create business value? |

A good bet requires evidence and reasoning — not just intuition. The altitude scorecard and solution scorecard provide the quantitative foundation for making and evaluating bets.

### Pitfalls for Effective Bets

| # | Pitfall | Description |
|---|---|---|
| 1 | **Feature adoption ≠ outcome improvement** | A feature being used doesn't mean the underlying problem is being solved |
| 2 | **Insufficient baseline** | No baseline data makes it impossible to evaluate impact after shipping |
| 3 | **Granular sub-problems** | Bets placed on edge-case problems rather than the main user problem |
| 4 | **No scorecard connection** | Solutions not mapped back to altitude metrics — no way to assess if the bet paid off |

### Practical Uses of the Map

| Use Case | How the Map Helps |
|---|---|
| **Prioritization** | Evaluate which solutions most directly move the altitude scorecard metrics |
| **Leadership communication** | Show how work connects to the supervisor's scorecard |
| **Roadmap planning** | Ground new bets in the qualitative and quantitative altitude definition |
| **Performance evaluation** | Track progress against 3–5 outcome metrics over time |
| **Onboarding** | Quickly communicate what the product area is responsible for |

The altitude scorecard is not static — evolve it over time as better proxy metrics are found and the product area matures.

---

## Key Principles

| # | Principle | Description |
|---|---|---|
| 1 | **Data-driven means upfront** | Using data to make better decisions before acting — not just analyzing results after the fact |
| 2 | **Altitude ≠ features** | The scorecard measures outcomes, not feature adoption |
| 3 | **User value is always a proxy** | It cannot be measured directly — evolve the metric over time |
| 4 | **Business impact connects up** | Always pull from the supervisor's scorecard; do not invent new metrics |
| 5 | **Scorecard size: 3–5 metrics** | Enough to be comprehensive, few enough to be actionable |
| 6 | **Qualitative before quantitative** | Define the altitude qualitatively (Step 3) before building the scorecard (Step 4) |
| 7 | **Decisions are bets** | Every product decision is a bet on user + business value; the map is what you use to evaluate it |

---

