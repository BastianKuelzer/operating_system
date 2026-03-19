---
name: ticket-visualizer
description: Visualize the logic and flow of a Linear ticket as an interactive HTML diagram. Use when a user wants to understand, review, or present business logic defined in a ticket from a Product Manager's perspective.
argument-hint: "[ticket-id]"
allowed-tools: Bash(python *), Bash(echo *), mcp__linear__*
---

# Ticket Logic Visualizer

Fetch a Linear ticket and generate an interactive HTML visualization of its logic, acceptance criteria, and open questions — from a Product Manager's perspective.

## Step 1 — Fetch the ticket

Use the Linear MCP tools to fetch the ticket specified in "$ARGUMENTS". If no ticket ID is provided, ask the user which ticket to visualize.

Retrieve:
- Title, description, status, priority
- Comments (for additional context on decisions made)
- Related/linked tickets if relevant

## Step 2 — Extract the logic structure

Analyze the ticket content carefully and extract the following into a JSON object. Think like a Product Manager mapping out the complete logic — including happy paths, edge cases, and open questions.

Choise the best visualization on logic flow and think hard to show it correctly, this is the most importamt part.

```json
{
  "id": "TICKET-123",
  "title": "Short ticket title",
  "status": "In Progress",
  "priority": "High",
  "user_story": {
    "as_a": "type of user",
    "i_want": "what they want to do",
    "so_that": "the benefit they get"
  },
  "acceptance_criteria": [
    {
      "id": "AC-1",
      "description": "Clear description of the criterion",
      "type": "happy_path",
      "sub_criteria": ["Additional detail if needed"]
    },
    {
      "id": "AC-2",
      "description": "What happens when input is invalid",
      "type": "validation"
    },
    {
      "id": "AC-3",
      "description": "Edge case handling",
      "type": "edge_case"
    },
    {
      "id": "AC-4",
      "description": "Error state behavior",
      "type": "error"
    }
  ],
  "logic_flow": [
    {
      "id": "start",
      "label": "User Action",
      "type": "start",
      "next": ["validate"]
    },
    {
      "id": "validate",
      "label": "Input Valid?",
      "type": "decision",
      "next": ["process", "show-error"]
    },
    {
      "id": "process",
      "label": "Process Request",
      "type": "action",
      "next": ["success"]
    },
    {
      "id": "show-error",
      "label": "Show Error",
      "type": "error",
      "next": []
    },
    {
      "id": "success",
      "label": "Show Success",
      "type": "end",
      "next": []
    }
  ],
  "states": [
    { "from": "Draft", "to": "Submitted", "trigger": "User clicks submit" }
  ],
  "edge_cases": [
    "What happens if the user is offline?",
    "What if the same action is triggered twice?"
  ],
  "open_questions": [
    "What should happen if X?",
    "Who is responsible for Y?"
  ],
  "dependencies": [
    "TICKET-456: Backend API must be ready",
    "Design: Modal spec from Figma"
  ]
}
```

**Rules for extraction:**
- `logic_flow` nodes represent the full logical flow — keep labels short (max 4 words).
- `type` for flow nodes: `start`, `action`, `decision`, `error`, `end`
- For `decision` nodes, `next` lists all branches (first = happy path)
- `edge_cases` captures anything not addressed by explicit acceptance criteria
- `open_questions` are things the ticket leaves undefined or ambiguous
- Omit any field that has no data (don't include empty arrays)

## Step 3 — Generate the visualization

Save the JSON to a temp file and run:

```bash
echo '<JSON_STRING>' > /tmp/ticket_data.json
python ~/.claude/skills/ticket-visualizer/scripts/visualize.py /tmp/ticket_data.json
```

This creates `ticket-logic.html` in the current directory and opens it in the browser.

## Step 4 — Share findings

After the visualization opens, briefly summarize:
- Are there open questions that must be resolved before development starts?
- Are edge cases and error states sufficiently covered?
- Is the logic flow complete and unambiguous?
