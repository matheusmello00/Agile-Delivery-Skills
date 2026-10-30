<div align="center">

**🌐 English** · [Português](README.pt.md) · [Español](README.es.md)

<img src="assets/banner.svg" alt="Agile Delivery Skills — Matheus Mello" width="100%">

*Five agile delivery skills for Scrum and Kanban teams that turn your board data into a ready-to-use briefing: backlog readiness, blockers, planning, retros and reviews.*

<a href="https://www.linkedin.com/in/matheusmello00/"><img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="mailto:m.mello00@outlook.com"><img src="https://img.shields.io/badge/Email-Say%20hello-6D1A36?style=for-the-badge&logo=microsoftoutlook&logoColor=white" alt="Email"></a>
<a href="https://wa.me/351920102358"><img src="https://img.shields.io/badge/WhatsApp-Chat-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp"></a>

<img src="https://img.shields.io/github/stars/matheusmello00/Agile-Delivery-Skills?label=Stars&style=flat-square&color=6B7B3A" alt="Stars">

</div>

---

## 🧭 Start with the work in your hands

| Stage | Bring this | Use this | Ask for this |
|---|---|---|---|
| **Scrum:** refinement, in the days before planning, when the top must be ready to enter the sprint.<br>**Kanban:** queue replenishment, before pulling items into the flow. | The top of your backlog | `backlog-ready-check` | Check whether the top 20 items are ready for the next sprint against our Definition of Ready. |
| **Scrum:** sprint execution, at the daily and at checkpoints, whenever items are stalled.<br>**Kanban:** board review, to see the impact of blockers on WIP and the queue. | A board with blocked items | `blocker-aging` | Show what is blocked, for how many business days, and what to escalate. |
| **Scrum:** pre-planning, before Sprint Planning, to arrive with a proposed scope and goal.<br>**Kanban:** not applicable (no sprint, no scope commitment). | The next sprint and team capacity | `planning-preparation` | Cross capacity with velocity, propose the candidate scope and draft a sprint goal. |
| **Scrum:** pre-retrospective, when closing the sprint, before gathering the team.<br>**Kanban:** periodic retro over a flow window (lead time, throughput, WIP). | An upcoming retrospective | `retro-preparation` | Prepare a facts-based retro: metrics, two or three candidate themes and a suitable format. |
| **Scrum:** pre-review/demo, at the end of the sprint, before presenting to stakeholders.<br>**Kanban:** end of a time window (week, month), before the delivery demo. | A finished sprint | `review-demo-preparation` | Build the review/demo briefing grouped by value, with a narrative and presenters. |

> **Scrum or Kanban:** the skills work with both models and ask which one you use when the context is unclear. The exception is `planning-preparation`, which relies on sprints, capacity and velocity, so it is Scrum-only. In Kanban, estimates are optional by default.

The assistant reads what you provide, asks up to four questions for missing context, and works toward the deliverable. Give it your board or project, sprint, team, goal and constraints when you can. The skills are read-only by default: they report, they never change your tracker.

## 🧱 How each skill is built (Agent Skills standard)

All skills follow the open [Agent Skills specification](https://agentskills.io/specification), so they work in any compatible assistant.

```
skill-name/
├── SKILL.md          # Required: frontmatter + instructions (under 500 lines)
├── references/       # Optional: detail loaded only when needed, one level deep
├── scripts/          # Optional: self-contained code, with --help and clear errors
├── assets/           # Optional: templates and static resources
└── evals/            # Our extension: discovery queries and quality scenarios
```

## 🔌 Works with

Jira (Atlassian), Azure DevOps and ClickUp, through the tracker connector (MCP) your assistant already has. Each skill ships a `references/trackers.md` with the query and field mapping. Replies come in the language you write in. Bundled scripts use Python 3.9+ with the standard library only.

> **Azure DevOps and ClickUp:** to work well outside Jira, add your tool's own fields to the lookup (work item types and states, estimate field, blocked marker, sprint/iteration, acceptance criteria) or tell the skill their names. Without them the search can miss items.

## 📦 Install

### Claude Code plugin

Run these commands inside Claude Code:

```text
/plugin marketplace add matheusmello00/Agile-Delivery-Skills
/plugin install agile-delivery@agile-delivery
```

Then invoke a skill by its plugin name:

```text
/agile-delivery:blocker-aging
Show me what is blocked on the Checkout board and what should be escalated.
```

The plugin contains the 5 skills under `skills/`. It needs no API key or external service to read its instructions; your assistant supplies the model and the tracker connector.

### Codex or Cursor

Clone the repository, then copy one skill into your personal skills directory:

```bash
git clone https://github.com/matheusmello00/Agile-Delivery-Skills.git
mkdir -p ~/.agents/skills
cp -R Agile-Delivery-Skills/skills/blocker-aging ~/.agents/skills/
```

To install all 5, replace the final command with:

```bash
cp -R Agile-Delivery-Skills/skills/* ~/.agents/skills/
```

Check for existing folders with the same names before copying; copying can overwrite files. For team use, copy into `.agents/skills/` in your project instead. In Codex, invoke `$blocker-aging`; in Cursor, use `/blocker-aging` or describe the task so the assistant can select the skill.

### Claude Code without the plugin

After cloning, use `~/.claude/skills/` for personal skills or `.claude/skills/` for project skills:

```bash
mkdir -p ~/.claude/skills
cp -R Agile-Delivery-Skills/skills/blocker-aging ~/.claude/skills/
```

Invoke `/blocker-aging`. Choose either the plugin or the copy method to avoid duplicate installations.

### Other assistants, including ChatGPT

Open the relevant `SKILL.md` and provide it with your work. Include that skill's `references/` files (and `scripts/` if you can run Python) for the full supporting material. Automatic discovery depends on the assistant; cloning this repository does not install the skills into every product.

## 👤 Author

Built by [Matheus Mello](https://github.com/matheusmello00) — Senior Product Manager & Agile Coach.
