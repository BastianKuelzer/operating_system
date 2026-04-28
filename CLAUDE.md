# Claude Navigation Guide

This file is your map to everything in this operating system. Find the right skill, knowledge file, or project below — each entry is one sentence so you know exactly what lives where.

---

## Skills

Invoke skills with `/skill-name` in Claude Code. Each skill file contains full instructions, inputs, and output format.

### Product Manager
| File | What it does |
|------|-------------|
| [linear-tickets_SKILL.md](./Skills/linear-tickets_SKILL.md) | Creates structured Linear tickets (New Feature, Bug, Testing, Feedback) using standardized templates. |
| [ticket-challenger_SKILL.md](./Skills/ticket-challenger_SKILL.md) | Reviews a Linear ticket as a senior product strategist — challenges scope, defers non-essentials, confirms readiness. |
| [ticket-visualizer_SKILL.md](./Skills/ticket-visualizer_SKILL.md) | Fetches a Linear ticket and generates an interactive HTML diagram of its logic flow, acceptance criteria, and edge cases. |
| [context-page_SKILL.md](./Skills/context-page_SKILL.md) | Creates a post-prototype decision log (General, Details, Stages) as a PRD-equivalent handover to engineering. |
| [prd_SKILL.md](./Skills/prd_SKILL.md) | Generates a code-grounded PRD by reading the actual source files — creates a single source of truth for each feature that is never edited by humans and drives all stakeholder communications: roadmap entries, release notes, sales talk tracks, and more. Run after every software deployment to keep it current. |
| [backlog-sorting_SKILL.md](./Skills/backlog-sorting_SKILL.md) | Prioritizes the Linear backlog using the Notion priority table with deterministic ordering rules. |

### Designer
| File | What it does |
|------|-------------|
| [figma_SKILL.md](./Skills/figma_SKILL.md) | Translates tickets into Figma design briefs or creates frames and components directly via MCP for dev handoff. |
| [ai-prototyping_SKILL.md](./Skills/ai-prototyping_SKILL.md) | Turns any input into copy-paste-ready prototype prompts for v0, Google AI Studio, Bolt, or Lovable. |

### User Researcher
| File | What it does |
|------|-------------|
| [customer-voice_SKILL.md](./Skills/customer-voice_SKILL.md) | Answers product questions from a Notion-indexed feedback database (Fireflies, Slack, Email). |

### Business Development
| File | What it does |
|------|-------------|
| [competitor-research_SKILL.md](./Skills/competitor-research_SKILL.md) | Pulls competitor data from a linked Google Sheet across inspiration, pricing, and customer arguments. |
| [sales-talk-track_SKILL.md](./Skills/sales-talk-track_SKILL.md) | Creates a ready-to-use sales pitch covering the customer problem, solution, and product walkthrough. |
| [executive-review_SKILL.md](./Skills/executive-review_SKILL.md) | Pressure-tests any idea or plan through simplicity, speed, and strategic fit — ends with a clear thumbs up or down. |

### Utility
| File | What it does |
|------|-------------|
| [clear-desktop_SKILL.md](./Skills/clear-desktop_SKILL.md) | Moves all screenshots from the Desktop to the Trash. |

---

## Knowledge

Curated frameworks and mental models — use these as context when reasoning about leadership, decisions, and strategy.

| File | What it covers |
|------|---------------|
| [Knowledge/team-performance.md](./Knowledge/team-performance.md) | Leadership identity, team archetypes, 5 levels of leadership, conflict patterns, and pressure calibration per person. |
| [Knowledge/decision-making-under-pressure-and-uncertainty.md](./Knowledge/decision-making-under-pressure-and-uncertainty.md) | 15 principles, 8 biases to avoid, and emotional signals for making fast, high-quality decisions under uncertainty. |
| [Knowledge/kpis-on-different-layers.md](./Knowledge/kpis-on-different-layers.md) | 7-step framework for defining a product area's KPIs across supervisor, PM, and solution layers — includes qualitative description template, scorecard categories, and worked examples. |

---

## News Agents

Autonomous agents that fetch live news sources and generate structured briefings on a schedule.

| Folder | What it does |
|--------|-------------|
| [News_Agents/podcasts/](./News_Agents/podcasts/) | Monitors three energy podcasts (Energy Unplugged, Redefining Energy, The Energy Gang), transcribes audio with Whisper, and saves Overview/Key Topics/Key Insights summaries per episode into each podcast's own subfolder. |
| [News_Agents/energate/](./News_Agents/energate/) | Pulls the 15 latest energate messenger articles and generates an English morning briefing (headlines, themes, market watch) saved to ~/Documents/Energate News/. |

---

## Projects

Active and template projects — each folder contains its own README with full context.

| Folder | What it is |
|--------|-----------|
| [Projects/Project_Fusion/](./Projects/Project_Fusion/) | A commercial product coaching framework built around six core leverages that separate great PMs from good ones. |
| [Projects/Agent Pipeline Template - New Products/](./Projects/Agent%20Pipeline%20Template%20-%20New%20Products/) | A 6-skill pipeline that turns a new product idea into customer evidence, a prototype, tickets, a handover doc, and a sales pitch. |
