# review-demo-preparation

Prepares a sprint review, a product demo or a product review from completed Jira items, grouping deliveries by perceived value, building a business-oriented narrative and suggesting presenters based on the assignees' real contribution.

**When to use:** before preparing a sprint review, a product demo or a meeting with stakeholders, when completed deliveries need to be turned into a credible, value-oriented briefing that is useful to the team, the Product Manager and the business audience.

**Not for:** creating automatic actions, writing release notes, publishing to Confluence without an explicit request or replacing the team's decision on what to demo. It also must not invent business impact, metrics or adoption when this data does not exist.

## Main goal
The skill must turn completed deliveries into:
- a short narrative that is relevant to the audience;
- value blocks in order of impact;
- a practical presenter recommendation;
- a briefing oriented to decision, alignment or understanding of the value delivered.

## Requirements
- A tracker connector (MCP) with read access: Atlassian (Jira), Azure DevOps or ClickUp (mapping in `references/trackers.md`).
- Access to the relevant board, project or sprint.
- Identification of the target audience and the session goal.
- Definition of the analysis type: Scrum/sprint or Kanban/time window.

> **Azure DevOps and ClickUp:** to work well outside Jira, add your tool's own fields to the lookup — work item types and states, estimate field, blocked marker, sprint/iteration and acceptance criteria — or tell the skill their names. Without them the search can miss items or misread their status. Mapping in `references/trackers.md`.

## Language
Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Verbatim items (issue keys, names, field values) are kept untouched.

## Operational flow

### 1) Resolve the context before the output
The skill must first distinguish between:
- Scrum / sprint: when the request indicates sprint, sprint review, sprint goal, iteration or review per cycle;
- Kanban / time window: when the request indicates week, month, quarter, period, delivered this week or a review over a time interval.

If the context is ambiguous, it must ask for confirmation instead of assuming.

### 2) Filter only deliverable items
These enter the main narrative:
- Story
- Task
- Improvement
- Problem
- Incident
- Bug
- other equivalent types, when completed and deliverable

These do not enter as a main delivery:
- management or support items with no clear business, operational or user value

### 3) Group by perceived value
Deliveries must be grouped by value theme and not just as a list of issues. Examples:
- user experience improvement;
- reduced process friction;
- operational automation;
- critical functional delivery;
- risk mitigation or stability improvement.

### 4) Choose the format by audience and goal
- internal review: value narrative with detail useful to the team;
- demo with stakeholders: focus on impact, decision and message clarity;
- several small deliveries: grouping by theme;
- complex dependencies: journey narrative;
- executive review: decision-oriented summary.

### 5) Define presenters
- Product Manager / PO: context, value and decision;
- developers: implementation, quality, risks and trade-offs;
- if there are several owners for a theme: one main presenter and one in support.

### 6) Produce a structured briefing
The expected output includes:
- factual context;
- main message;
- value blocks;
- deliveries to present;
- suggested script;
- presenters;
- risks and dependencies;
- opening questions.

## Expected scenarios
The skill must respond consistently to these scenarios:
- internal sprint review;
- demo for stakeholders;
- executive product review;
- product demo over a time window/Kanban;
- review with a technical audience and a decision-making audience;
- sessions with small deliveries, fragmented themes or complex dependencies.

## Quality guardrails
- **Only state what the data supports.**
- **Do not invent impact, ROI, adoption or metrics** when there is not enough evidence.
- **Do not turn technical tasks into business value** without adequate context.
- **Do not order by chronology** when the audience needs an impact narrative.
- **Do not publish to Confluence or other systems** without an explicit request.
- **Ask for clarification** when the context or the board is not sufficiently defined.

## Behavior notes
- **Value first**: the narrative must answer what changed, why it matters and who explains it best.
- **Scrum vs Kanban**: the skill must first resolve the analysis type before structuring the output.
- **Evidence before inference**: it does not invent business impact, adoption or metrics when there is not enough data.
- **Audience fit**: stakeholders get less technical detail; the team can get more depth, but still needs a clear value line.
- **No silent publishing**: it does not write to Confluence, Jira or other systems without an explicit request.
