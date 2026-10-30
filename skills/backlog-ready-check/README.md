# backlog-ready-check

Definition of Ready / flow entry scan of the top of the backlog or the entry queue: flags items with no useful description, no acceptance criteria, no estimate/size **when the mode requires it**, no epic when the team requires context, or too large for the delivery model, and returns the shortlist of what to refine first or fit into the flow.

**When to use:** before refinement, to measure backlog hygiene, to assess entry into the continuous flow in Kanban, or to confirm whether a set of items is ready to enter a sprint / be pulled.
**Not for:** proposing scope or capacity (`planning-preparation`). Read-only — it does not change the stories.

## Requirements
A tracker connector (MCP) with read access: Atlassian (Jira), Azure DevOps or ClickUp (mapping in `references/trackers.md`). Python 3.9+.

> **Azure DevOps and ClickUp:** to work well outside Jira, add your tool's own fields to the lookup — work item types and states, estimate field, blocked marker, sprint/iteration and acceptance criteria — or tell the skill their names. Without them the search can miss items or misread their status. Mapping in `references/trackers.md`.

## Script
```bash
python scripts/check_readiness.py backlog.json [--json]
python scripts/check_readiness.py --help
```
Input schema and criteria in `references/dor.md`.

## Behaviour notes
- **Mutually exclusive buckets** that sum to the total: items with gaps go to "To refine" (excess size goes down to a note); "To split" is only for large items without other gaps.
- `delivery_model` defaults to `scrum`, but the script supports `kanban`.
- **Estimate / size:** in Scrum it is a gap by default (`require_estimate: true`). In **Kanban it is optional by default** (`require_estimate: false`) — story points and T-shirt size do not block readiness unless the team opts in.
- `epic_required` defaults to `true`: a missing epic is a **gap**, not an informational note, when the flow requires context.
- Optional criteria: `require_dependencies_identified`, `require_testable`.
- The **substance assessment** (is the description useful? do the AC have content?) is done by the model; the script aggregates and applies the counting rules.

## Language
Defaults to English. It always replies in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish); only the output language changes, not the logic. Verbatim items (issue keys, names, field values) are kept untouched.
