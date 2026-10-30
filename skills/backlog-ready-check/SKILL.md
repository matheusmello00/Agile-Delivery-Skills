---
name: backlog-ready-check
description: 'Readiness scan of the top of the backlog / flow: assesses whether a set of items is ready to enter a sprint or to be pulled into a continuous Kanban flow, against Definition of Ready / flow-entry criteria. Flags items with no useful description, no acceptance criteria, no estimate/size when the delivery mode requires it, no epic when the context requires it, or too large for the delivery mode. In Kanban, story points and T-shirt size are optional by default and never block readiness. The buckets are mutually exclusive; judging substance is left to the model, the script applies the counting rules. Criteria are configurable, on any Jira board. Does not propose scope or compute capacity (use planning-preparation) and is read-only: it never changes the stories.'
when_to_use: 'When preparing a refinement, measuring backlog hygiene, or asking whether a set of stories/items is ready to enter a sprint or the continuous Kanban flow, including Definition of Ready, unestimated/unsized items (Scrum, or Kanban with estimation enabled), and items with no acceptance criteria. Hierarchy: Initiative, Epic, Story/Task. Serves Scrum Master, Product Owner, Agile Coach and Kanban teams.'
maturity: ready
allowed-tools:
- Bash
- Read
- mcp__atlassian
- mcp__azure-devops
- mcp__clickup
compatibility: 'Requires a tracker connector (MCP) with read access: Atlassian (Jira), Azure DevOps or ClickUp; Confluence only for the publishable version, optional. Python 3 standard-library scripts, no external dependencies.'
argument-hint: '[board] [n-stories]'
metadata:
  author: Matheus Mello
  version: '0.1.0'
audience: 'Scrum Master, PMO, Agile Coach, Product Owners, Kanban Leads and continuous-flow teams'
tags:
- agile
- scrum
- kanban
- jira
- azure-devops
- clickup
- backlog
---

# Backlog Ready Check (DoR / Flow Readiness)

Prepares refinement and work intake by showing, from the top of the backlog or the entry queue, what is already ready and what needs work before it can be pulled or enter a sprint. Instead of discovering live that an item has no acceptance criteria, you arrive with the list of what is missing. In Kanban flows, readiness centres on clarity and value — **estimates (story points or T-shirt size) are fully optional by default** and do not determine whether the item is ready for development.

## Requires

A tracker connector (MCP): Atlassian (Jira), Azure DevOps or ClickUp — see `references/trackers.md`. Read-only by default — it only reads and reports.

## What you need before starting

- **Board / project**, **delivery mode** (Scrum or Kanban) and how many stories to analyse (by default, the next ~15-20 in the backlog, by rank).
- **DoR criteria.** See `references/dor.md`. If the team has its own Definition of Ready, ask for it and use it.
- **In Kanban:** confirm whether the team uses estimates/size as a practice — by default they are **not** part of the DoR (`require_estimate: false`). Only enable it if the team explicitly asks.

## Flow

1. **Resolve the mode** — Scrum (sprint, points required by default) or Kanban (continuous flow, estimate optional by default). If the user does not say, ask or infer from the board/context.
2. **Pull the top of the backlog / entry queue** — next N stories/items by rank: in Scrum, outside a sprint; in Kanban, at the top of the board/queue, without imposing a sprint. JQL / query in the reference.
3. **Collect the readiness fields** and **assess substance**: whether the description is useful and whether the acceptance criteria have content is **your** judgment (the model's), translated into booleans. Note the judgment criteria you used.
4. **Normalise** to the script's schema and run:
   ```bash
   python scripts/check_readiness.py backlog.json
   ```
   The script **aggregates and applies the counting rules consistently** (mutually exclusive buckets that sum to the total) — the substance assessment is yours, the script does not do it. In Kanban, use `delivery_model: kanban` and, unless asked otherwise, `require_estimate: false`.
5. **Build the shortlist** with the template below. Prioritise what is almost ready (1 gap).
6. **Do not change the stories.** Read-only. If the user asks to add AC/estimates, that is another conversation (with approval).

## Template

```
# Backlog / flow readiness — [board]  ·  top [N] items

## Summary
- Ready: [X]  ·  To refine: [Y]  ·  To split / prepare for flow: [Z]   (exclusive buckets — they sum to the total)
- (mode: [Scrum/Kanban])
- (epic required: [yes/no])
- (estimate/size required: [yes/no])

## Ready for the next step
- [KEY] [title]

## To refine (in suggested order — fewest gaps first)
- [KEY] [title] — missing: [AC / estimate/size / description / epic / dependencies]  [note: split candidate, if also large]

## Split candidates / size out of fit (large, no other gaps)
- [KEY] [title] — [points above the ceiling / T-shirt size above the limit]

## Notes
- [DoR criteria used; substance judgment criteria; in Kanban without estimates: record that points/size are optional]
```

## Rules

- **Diagnose only** — read-only; you do not write without a request and approval.
- **Mutually exclusive buckets**: an item with gaps goes to "To refine" (excess size goes down to a note); "To split" is only for large items **without** other gaps. The three sum to the total.
- **The substance assessment is the model's; the script only applies the counting rules.** Do not attribute to the script judgments that are yours.
- **Use the team's DoR** if one exists; otherwise the default set for the mode, and say so.
- **Do not invent AC or estimates/size.**
- **Scrum vs Kanban — estimate:**
  - **Scrum:** `require_estimate` defaults to `true` — absence of points is a gap.
  - **Kanban:** `require_estimate` defaults to **`false`** — story points and T-shirt size are optional; absence does **not** prevent readiness. Record it as informational if relevant. Only require an estimate if the Kanban team asks for it (`require_estimate: true`).
- **Supports two intake/delivery modes**: `scrum` (sprint, points) and `kanban` (flow, optional estimate). If `delivery_model` is not provided, the script assumes `scrum` for compatibility.
- **Propagate warnings and do not swallow errors.** If the script returns a `WARNINGS` block, reproduce those warnings in the report you deliver — the warning serves the reader, not the script. If the script ends with **exit 2**, the input does not match the schema: fix the normalisation and run again, never report a result from a rejected input.
- Issue keys and names verbatim.

## Language

Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Keep verbatim items (issue keys, names, field values) untouched.

## References

| Read this | Before… |
|---|---|
| `references/dor.md` §DoR criteria | deciding what counts as a gap and what is optional |
| `references/dor.md` §JQL / §Field mapping | pulling the top of the backlog from Jira |
| `references/dor.md` §JSON schema | normalising the input before running `check_readiness.py` |
| `references/trackers.md` | pulling data from Azure DevOps or ClickUp instead of Jira (query and field mapping) |
