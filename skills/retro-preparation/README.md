# retro-preparation

Facts-based retrospective facilitation pack: sprint/period or flow metrics, two or three candidate themes phrased as neutral questions, a format and collection mechanism suited to the team's moment, an agenda with timeboxes, and prompts.

**When to use:** before facilitating a retro — what to discuss, which format, how to open with data, whether in a sprint or in continuous Kanban flow.
**Not for:** computing sprint/flow metrics from an external report, creating the action tickets. It does not publish to Confluence without a request.

## Requirements
A tracker connector (MCP) with read access: Atlassian (Jira), Azure DevOps or ClickUp (mapping in `references/trackers.md`). No script of its own — it uses the board/sprint data feed and, in Kanban, the tracker's flow context. Python 3.9+ only for the local normalizer, if one exists.

> **Azure DevOps and ClickUp:** to work well outside Jira, add your tool's own fields to the lookup — work item types and states, estimate field, blocked marker, sprint/iteration and acceptance criteria — or tell the skill their names. Without them the search can miss items or misread their status. Mapping in `references/trackers.md`.

## Inherited metrics contract
The factual context block always uses the same minimum set, mapped to the keys of the chosen contract's JSON output, so retros of the same team are comparable. In Scrum the minimum set is `commitment_reliability_pct_count`, `carryover`, `scope_change_pct`, `velocity` vs `prior_velocity_avg`, `flagged.issues`. In Kanban the minimum set becomes `lead_time_avg`, `cycle_time_avg`, `throughput`, `wip_by_column`, `blocked_items` and `waiting_time` / `wait_age`.

## Behavior notes
- Themes as **neutral questions**, never verdicts, and never blaming people.
- **Mechanisms orthogonal to the format** (`references/retro-formats.md`): anonymous collection for low morale, asynchronous collection for distributed teams, silent writing for large groups, and wait/flow collection for Kanban boards at risk of a blocked column. This is the mechanism that makes those sprints/flows discussable.
- Default agenda 60 min (5/15/20/15/5); above ~8 people, gather in breakouts.
- Always reserve time to decide actions — a retro without actions changes nothing.

## Language
Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Verbatim items (issue keys, names, field values) are kept untouched.
