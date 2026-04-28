---
name: prd
description: Generate a detailed, code-grounded PRD for any feature in the ecoplanet codebase by searching app-fe, app-backend, and procurement-service-kt. Creates a new Notion page at a location chosen by the user, or updates an existing one if found. Use when asked to "create a PRD", "document a feature", "write a PRD for X", or "generate a product requirements document".
---

# Feature PRD Generator

Generate a detailed PRD for any ecoplanet feature and publish it to Notion.

## Step 0 — Ask the user two questions upfront

Before doing anything else, ask both questions in a single message:

> 1. "Which feature should I document? (e.g. 'Portfolio Management Overview', 'Load Planning', 'Invoicing')"
> 2. "Where in Notion should I create or update the page? Please paste the URL of the parent page."

Wait for both answers before proceeding. Use the feature name for all searches, the PRD title, and the Notion page title. Use the Notion URL to resolve the parent page ID for create/update operations.

---

## Step 1 — Check Notion for an existing page

Search for an existing PRD page in Notion using the feature name:

1. Use `notion-fetch` on the parent page URL provided by the user to get its page ID and list of child pages
2. Use `notion-search` to search for `"Agent — PRD: {feature name}"` within the workspace
3. If a matching page is found:
   - Fetch its full content with `notion-fetch`
   - Note its page ID — you will **update** this page instead of creating a new one
   - Tell the user: "Found existing PRD page — will update it."
4. If no matching page is found:
   - Tell the user: "No existing PRD found — will create a new page under {parent page URL}."

---

## Step 2 — Parallel codebase exploration

Spawn three Explore agents simultaneously, one per repo. Search for all code related to the feature name provided by the user.

### Repos

| Repo | Path | Role |
|------|------|------|
| Frontend | `~/Desktop/app-fe` | UI components, routing, state, API calls |
| Backend EI | `~/Desktop/app-backend` | Domain code, endpoints, services |
| Backend MO | `~/Desktop/procurement-service-kt` | Kotlin endpoints, business logic, data models |

If any repo is missing from the Desktop, note it explicitly and continue with what is available.

### What to extract per repo

**app-fe** — read every component file individually. Do not stop at a high-level search. For every screen, modal, form, and panel file:

- **Form fields** — for each field record: component type (`FormDatePicker`, `FormNumericInput`, `FormSelect`, `FormWeekDaySelect`, `SelectTimeInput`, `FormTextarea`, `Checkbox`, `FormInput`), label, required/optional, and all props.
- **Date pickers** — record exactly: `minDate`, `maxDate`, picker type (day/month/range), `isRange`, any `excludeDates`, custom `filterDate`, presets, and any dynamic constraints (e.g. 7-day minimum enforcement).
- **Validation** — extract the full Yup schema: which fields are `.required()`, numeric `.min()`/`.max()`, `.optional()`, and any cross-field rules.
- **Button states** — record the exact boolean expression that disables each button (e.g. `!formik.isValid || !formik.dirty || !isCalculated`).
- **Conditional rendering** — what shows/hides under which conditions (e.g. a field only rendered when another field has a specific value, info boxes that appear after data loads).
- **Modal metadata** — size, `motionPreset`, `isCentered`, layout (flex ratios of columns).
- **Step sizes and option lists** — for time/numeric inputs record the step value and how it varies by energy type or other context.
- **Auto-triggered effects** — `useEffect` calls that fire on modal open or state change (e.g. auto-calculating on edit mode open).
- React screen/page components and routing entries
- API calls (endpoints, query hooks, staleTime, keepPreviousData)
- React Query keys
- TypeScript types and interfaces
- Empty states, loading states, and error states (including exact component used and container size)
- Any premium/upselling gate or feature flag

**app-backend** — search for the feature name:
- Confirm presence or absence of feature domain code
- Controllers, services, DTOs if present

**procurement-service-kt** — search for the feature name:
- Controllers and REST endpoint definitions
- DTOs (request/response shapes)
- Domain models and JPA entities
- Service methods and business logic
- Calculation functions — extract exact formulas where they exist

---

## Step 3 — Write the PRD

Structure the PRD using the sections below. Adapt section names and subsections to what was actually found in the code — do not invent sections for things that don't exist. Omit sections that are not applicable.

**Depth requirement**: Every built UI interaction must be documented. For each form, modal, and panel: list every individual field, every button with its disabled condition, every date picker constraint, every conditional display rule. A reader should be able to fully reconstruct the UI from the PRD alone without looking at the code.

### Title format

`Agent — PRD: {Feature Name}`

### Required sections

**1. Overview**
One paragraph: what the feature is, who uses it, what problem it solves.

**2. Problem Statement**
Bullet list of what users cannot do without this feature.

**3. Users & Personas**
Who uses this feature and why.

**4. User Stories**
Table: # | As a... | I want to... | So that...

**5. Functional Requirements**
Break into subsections per major screen area or flow. For each subsection cover:
- Route / entry point
- Layout (column structure, flex ratios)
- Every UI control and what it does (from code, not assumptions) — include field type, label, required/optional, all constraints
- For date pickers: minDate, maxDate, picker type, range mode, presets, excludeDates, filterDate, any minimum-range enforcement
- For inputs: step size, unit suffix, width, min/max, coercion behavior
- For selects: every option, how options are generated, disabled options and why, custom option label rendering
- For buttons: exact disabled condition as a boolean expression, what happens on click, any auto-trigger logic
- Conditional fields/sections: exact condition under which they appear
- Data displayed and where it comes from
- For KPI or calculation-heavy features: the exact formula from the backend, inputs, edge case handling (nulls, zero denominators), aggregation logic
- Empty states, loading states, error states — component used, container dimensions
- Any premium/upselling gate

**6. Technical Architecture**
ASCII diagram showing the data flow from frontend to backend service(s). Call out explicitly which backend owns the feature domain and which backends have no involvement.

Frontend stack table: Concern | Technology.
Backend stack table: Concern | Technology.

**7. API Specification**
For each endpoint: method + path, description, query params, request body, response shape with example JSON, auth notes.

**8. Data Models**
Field tables for key domain entities. Lifecycle diagrams where relevant (e.g. state machines).

**9. State Management**
React Query keys table (include staleTime and keepPreviousData where set). Client state (Zustand, URL params, component state that affects behavior).

**10. Unit & Conversion Handling**
(Include only if the feature involves unit conversions.)

**11. Non-Functional Requirements**
Table: Category | Requirement. Include performance SLAs, security, accessibility, reliability.

**12. Empty & Edge States**
Table: State | Trigger | UI Response.

**13. Dependencies**
Table: Dependency | Direction | Purpose.

**14. Open Questions**
Table: # | Question | Owner | Status.

---

## Step 4 — Publish to Notion

Fetch the Notion-flavored Markdown spec using `ReadMcpResourceTool` with server `"notion"` and uri `"notion://docs/enhanced-markdown-spec"`. Use `<table fit-page-width="true" header-row="true">` for all tables. Add a callout at the top:

```
<callout icon="🤖" color="blue_bg">
  Generated by Claude Code Agent on {today's date}. Source: app-fe, app-backend, procurement-service-kt.
</callout>
```

Include a `<table_of_contents/>` after the callout.

### If updating an existing page

Use `notion-update-page` with:
- `command`: `"replace_content"`
- `page_id`: the page ID found in Step 1
- `allow_deleting_content`: `true`
- `new_str`: the full PRD content

### If creating a new page

Use `notion-create-pages` with:
- `parent`: `{ "type": "page_id", "page_id": "{page ID resolved from the user's Notion URL}" }`
- `properties.title`: `"Agent — PRD: {Feature Name}"`

### If making a partial update later (e.g. removing or editing a section)

Use `notion-fetch` on the page ID first to get the exact current content, then use `notion-update-page` with `command: "update_content"` and match the exact string from the fetched content in `old_str`.

---

## Quality rules

- Every formula must come from actual code — do not invent or approximate
- If a repo has no code for the feature, state that explicitly in the architecture section
- Only list UI options that are actually rendered, not everything that exists in enums
- Do not include an "Out of Scope" section
- After publishing, output the Notion page URL so the user can open it directly
