# 🤖 My Operating System

A personal AI-powered operating system combining autonomous agents, curated knowledge, and active projects to get things done faster and smarter. From agents to my knowledge and even my value system, it is moving and evolving and this repo will change constantly.

---

## 👥 My AI Minions — Skills & Autonomous Agents

A squad of AI agents that get work done, learn from curated knowledge, and improve over time. + My human team can use this repo, add their own skills and knowledge, and run the same AI team alongside me.  


### 🛠️ Skills

**🧑‍💼 Product Manager**

| Skill | Description | Why | Performance Evaluation |
|-------|-------------|-----|----------------------------------|
| 🎫 [**Linear Ticket Writer**](./Skills/linear-tickets_SKILL.md) | Creates structured Linear tickets (New Feature · Bug · Testing · Feedback) using standardized templates matched to the team's style, with context from existing tickets. | Creates >100 well-defined tickets incl. edge cases in under 10 minutes | Follow-up questions from engineers ≤ 2 per 10 tickets · Requirements not implemented as intended ≤ 2 per 10 tickets |
| ⚔️ [**Ticket Challenger**](./Skills/ticket-challenger_SKILL.md) | Reviews any Linear ticket as a senior product strategist — challenges scope, defers non-essentials, and simplifies or confirms readiness. | Prevents inferior customer experience and days of wasted work | Logic added back after implementation ≤ 2 per 10 tickets · Simplifications found after skill was invoked ≤ 2 per 10 tickets |
| 📊 [**Ticket Visualizer**](./Skills/ticket-visualizer_SKILL.md) | Fetches a Linear ticket and generates an interactive HTML diagram of its logic flow, acceptance criteria, and edge cases. | Visualizes complex ticket logic in seconds vs. 20 minutes manually | 0 Logic flows missed in the diagram |
| 📋 [**Context Page**](./Skills/context-page_SKILL.md) | Creates a post-prototype decision log with executive summary, business logic, and MVP stages — a PRD-equivalent as handover to engineering. | Writes pages of condensed knowledge for engineering that would otherwise take days | 0 Critical information ignored · 0 Wrong information hallucinated · 0 Incorrect output structure |
| 📋 [**Backlog Sorting**](./Skills/backlog-sorting_SKILL.md) | Prioritizes the Linear backlog using the Notion priority table with deterministic ordering rules across critical bugs and in/out-of-scope tickets. | Engineering always knows current priorities — one skill call, any time, for todo tickets | ≤ 1 Manual backlog order adjustments needed |

**🎨 Designer**

| Skill | Description | Why | Performance Evaluation |
|-------|-------------|-----|----------------------------------|
| 🎨 [**Figma**](./Skills/figma_SKILL.md) | Translates Linear tickets into Figma design briefs or creates frames, components, and annotations directly via MCP for dev handoff. | Creates hundreds of designs per design principles and user stories within minutes | ≥ 2 Iterations needed afterwards |
| ⚡ [**AI Prototyping**](./Skills/ai-prototyping_SKILL.md) | Turns any input (Notion page, Figma design, competitor URL, or description) into 4 prototype arguments + 1 recommended version as copy-paste-ready prompts for v0, Google AI Studio, Bolt, or Lovable. | Builds prompts that create several fully functional front-end products within minutes | 0 Logic missed in the prompt |

**🔍 User Researcher**

| Skill | Description | Why | Performance Evaluation |
|-------|-------------|-----|------------------------|
| 🎙️ [**Customer Voice**](./Skills/customer-voice_SKILL.md) | Answers product questions from a Notion-indexed feedback database (Fireflies, Slack, Email). Optional: paste raw sources for inline extraction at query time. | Turns scattered customer feedback into structured evidence in seconds | 0 quotes were hallucinated, 0 customer feedback is wrongly clustered, 0 customer feedback is missing |

**📈 Business Development**

| Skill | Description | Why | Performance Evaluation |
|-------|-------------|-----|------------------------|
| 🔎 [**Competitor Research**](./Skills/competitor-research_SKILL.md) | Pulls competitor data from a linked Google Sheet across three arguments: Inspiration (features + screenshots), Pricing (models + tiers), and Customers (who uses them and why). | Surfaces structured competitor intelligence in seconds instead of days | 0 data points hallucinated, 0 fields inferred or enriched beyond the source |
| 🗣️ [**Sales Talk Track**](./Skills/sales-talk-track_SKILL.md) | Creates a Sales talk track when launching a new product or feature — covers the customer problem, the solution, and a step-by-step product walkthrough in plain spoken language. | Gives Sales a ready-to-use pitch the moment something ships, no prep needed | 0 jargon without explanation |

> Each skill lives in its own `.md` file and can be triggered directly in Claude Code or any other LLM.

---

## 🧠 My Knowledge

A curated collection of frameworks, mental models, and references that serve as a sparring partner for problems that arise or decisions on how to move forward.

| Topic | Description |
|-------|-------------|
| 👥 [**Team Performance & Leadership**](./Knowledge/team-performance.md) | Who I am as a leader, team archetypes, 5 levels of leadership, conflict patterns and solutions, and pressure calibration per person. |

---

## 🚀 Projects

Active and past projects built with or managed through this system.

| Project | Description | Status |
|---------|-------------|--------|
| 🌀 [**Project Fusion — Commercial Product Coaching**](./Project_Fusion/) | A coaching framework taught with principles not guidelines, built around the six core leverages that separate great PMs from good ones through a strong focus on building and sclaing commercial viable products: Leadership Buy-in, Team Empowerment, Needle-Moving Work, Focused Work, Product Intuition, and PM Leadership. | Active |

---

## 💻 Setup on a new machine

Clone the repo anywhere you like, then run the setup script once:

```bash
git clone <repo-url>
cd <repo-folder>
./setup.sh
```

This will:
- Register all skills as `/skill-name` slash commands in Claude Code
- Make all skills auto-trigger when Claude detects the right context
- Install a `post-merge` git hook so any new skill added to the repo is wired up automatically after a `git pull`

Several MCP servers for Notion, Fireflies, Slack, Linear, and Figma also need to be configured separately.

> Restart Claude Code after running the script to pick up the new slash commands.

**How it works:** `setup.sh` creates symlinks from `~/.claude/skills/` and `.claude/commands/` to the `Skills/` folder in this repo. Updates pushed to a skill file are instantly live — no re-setup needed.

