---
name: linear-tickets
description: Create Linear tickets using standardized templates for New Feature, Bug, Testing, or Feedback When Testing
argument-hint: "[New Feature | Bug | Testing | Feedback When Testing]"
---

The user wants to create a "$ARGUMENTS" ticket.

## Step 1 — Gather context
Ask the user:
1. Which Linear team or project should the ticket be created in?
2. Are there any existing tickets that should serve as context? If yes, search for them using the Linear MCP tools and fetch their details.

## Step 2 — Review context
Use the Linear MCP tools to:
- Fetch the tickets the user mentioned or recent tickets from the selected team
- Understand the patterns, terminology, and style used in existing tickets
- Check for duplicates or related tickets

## Step 3 — Create the ticket

Use the templates below. Only apply the template that matches the "$ARGUMENTS" ticket type.
Use the context from existing tickets to match the team's style and terminology.
Once the ticket content looks good, ask the user if they want to create it directly in Linear via the MCP tools.

Tickets are always created as **Backlog**, not todo or triage.

---

## Templates

There are 4 types: New Feature, Bug, Testing, Feedback When Testing.

### New Feature

```
## Overview
[Brief description of the feature and its purpose]

## Requirements

### Functional
- [Functional requirement 1]
- [Functional requirement 2]

Cluster the requirements in groups if there are more than 6 with a group headline so that it is easier to read

### Non-Functional
- [Non-functional requirement if applicable]

### Constraints
- [Technical, regulatory, or business constraints if applicable]


## Edge Cases
- [Edge case 1 and handling approach]
- [Edge case 2 and handling approach]
```

**What NOT to Do:**
- Do not add bug fixes or debugging information
- Do not include actual implementation code
- Do not use vague or unclear acceptance criteria
- Do not skip edge case consideration
- Do not add extra sections outside this format
- Do not mix multiple unrelated features in one ticket
- Do not omit technical approach or testing strategy
- Do not create tickets in triage or backlog, instead tickets should be created in todo

---

### Bug

```
## Problem
[Clear description of the bug and its impact]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Behavior
[What should happen]

## Actual Behavior
[What currently happens]

## Root Cause
[Technical explanation of why the bug occurs]

## Solution
- [Fix approach]
- [Files/components to modify]

## Verification
- [ ] [Verification step 1]
- [ ] [Verification step 2]
- [ ] [Regression testing completed]

## Edge Cases Considered
- [Related scenarios that could be affected]
```

**What NOT to Do:**
- Do not include feature requests or enhancements
- Do not omit reproduction steps
- Do not skip root cause analysis
- Do not leave out verification steps
- Do not add extra sections outside this format
- Do not provide solutions without understanding root cause
- Do not mix multiple unrelated bugs in one ticket
- Do not include actual code fixes in the description

---

### Testing

```
## Test Scope
[What is being tested and why]

## Test Cases
### Case 1: [Scenario name]
- **Setup**: [Preconditions]
- **Steps**: [Test actions]
- **Expected**: [Expected outcome]

### Case 2: [Scenario name]
- **Setup**: [Preconditions]
- **Steps**: [Test actions]
- **Expected**: [Expected outcome]

## Edge Cases
- [Edge case 1 with test approach]
- [Edge case 2 with test approach]

## Coverage
- [ ] Happy path scenarios
- [ ] Error handling
- [ ] Boundary conditions
- [ ] Integration points

## Test Data Requirements
[Data needed for testing]

## Dependencies
[External systems, APIs, or services involved]
```

**What NOT to Do:**
- Do not include actual test implementation code
- Do not omit test cases or edge cases
- Do not be vague about test scope
- Do not skip coverage requirements
- Do not add extra sections outside this format
- Do not mix testing tickets with bug reports or features
- Do not leave test data requirements undefined
- Do not forget to document dependencies

---

### Feedback When Testing

```
## Test Context
- **Ticket**: [Reference to original ticket]
- **Environment**: [Testing environment used]
- **Date**: [Testing date]

## Findings

### Working as Expected
- [Functionality 1]
- [Functionality 2]

### Issues Found
1. **[Issue title]**
   - **Severity**: [Critical/High/Medium/Low]
   - **Description**: [What went wrong]
   - **Steps to reproduce**: [How to trigger]
   - **Expected vs Actual**: [Comparison]

2. **[Issue title]**
   - **Severity**: [Critical/High/Medium/Low]
   - **Description**: [What went wrong]
   - **Steps to reproduce**: [How to trigger]
   - **Expected vs Actual**: [Comparison]

### Edge Cases Observed
- [Edge case 1 and outcome]
- [Edge case 2 and outcome]

### Suggestions
- [Improvement suggestion 1]
- [Improvement suggestion 2]

## Status Assessment
[Overall status: Ready/Needs fixes/Blocked]

## Next Steps
- [ ] [Action item 1]
- [ ] [Action item 2]
```

**What NOT to Do:**
- Do not provide feedback without test context
- Do not report issues without severity levels
- Do not omit steps to reproduce for bugs found
- Do not skip status assessment
- Do not add extra sections outside this format
- Do not mix subjective opinions without evidence
- Do not leave next steps undefined
- Do not forget to reference the original ticket
