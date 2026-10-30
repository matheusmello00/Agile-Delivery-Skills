---
name: planning-preparation
description: 'Prepares Sprint Planning to be a decision session rather than a discovery one: crosses the ready stories at the top of the backlog with real team capacity and historical velocity, and proposes a candidate scope and a sprint-goal draft for the team to react to and adjust. The commitment range comes from availability-adjusted velocity; with no history it never invents a number in points. Generic: any board, with configurable capacity and focus factor. Does not assess story readiness (use backlog-ready-check) and does not create the sprint or move issues.'
when_to_use: 'When preparing a planning and you need to know how much fits in the next sprint, which stories to propose, or what sprint goal to draft, including capacity-versus-velocity conversations and absences that shorten the sprint. Serves Scrum Master, PMO and Agile Coach.'
maturity: ready
allowed-tools:
- Bash
- Read
- mcp__atlassian
- mcp__azure-devops
- mcp__clickup
compatibility: 'Requires a tracker connector (MCP) with read access: Atlassian (Jira), Azure DevOps or ClickUp; Confluence only for the version to publish, optional. Python 3 standard-library scripts, no external dependencies.'
argument-hint: '[board] [sprint]'
metadata:
  author: Matheus Mello
  version: '0.1.0'
audience: 'Scrum Master, PMO, Agile Coach'
tags:
- agile
- scrum
- jira
- azure-devops
- clickup
- planning
---

# Planning Preparation Pack

Arrive at Sprint Planning with a proposal on the table instead of starting from scratch. The skill brings the ready stories, calculates how much fits (capacity + velocity) and suggests a scope and a sprint goal — for the team to **react and decide**, not to have the plan imposed on it.

The plan always belongs to the team. This skill provides the informed starting point; the final commitment comes out of the planning conversation.

## Requires

A tracker connector (MCP): Atlassian (Jira), Azure DevOps or ClickUp — see `references/trackers.md`.

## What you need before starting

- **Board / team** and the **next sprint** (or the period).
- **Capacity**: how many people, how many days in the sprint, and known absences/holidays. If they are not provided, ask.
- **Focus factor** (default 0.7) and **baseline focus** (default 0.7 — the focus assumed in the sprints that produced the velocity). The range is only adjusted for focus when it **differs** from the baseline.

## Flow

1. **Pull ready items.** Top of the backlog by rank, outside any sprint. Only **downstream** items are included (team work that goes into a sprint): **Story, Task, Spike, Bug, Improvement, Incident and Problem**. **Upstream** items never enter the search — they are not sprint work: **Initiative, Epic, Dependency, Change Request, Milestone** and the Xray test types (**Test, Test Set, Test Plan, Test Execution**). The list is configurable — see the JQL in [references/capacity.md](references/capacity.md). Use the `backlog-ready-check` skill if it exists; otherwise filter by what has an estimate and criteria.
2. **Get the historical velocity** — last 2–3 closed sprints (via JQL).
3. **Calculate capacity and scope** and run:
   ```bash
   python scripts/capacity.py planning.json
   ```
   **Velocity is the basis** of the range; availability (absences × relative focus × headcount) adjusts it. **Without velocity, the script does NOT propose a points range** (story points do not derive from days) — it returns the person-days as a diagnostic and a note to ask the team about recent delivery.
4. **Draft the sprint goal** from the dominant theme of the candidate stories. It is a draft for the team to refine.
5. **Assemble the pack** with the template below.
6. **Do not create the sprint or move issues.** If asked, approval applies.

## Template

```
# Planning preparation — [team]  ·  [next sprint]

## Capacity
- People: [n] · Days: [d] · Absences: [p-d] · Focus: [f] (base [bf])
- Effective person-days (diagnostic): [~]
- Availability vs normal sprint: [..%]  (absences / focus / headcount)
- Velocity: average [pts] · observed [min–max]
- Reasonable commitment range: [min–max pts]  ·  method: [observed min–max × availability]
  [or, without velocity: "Range not proposed — velocity missing; ask the team about recent delivery."]

## Candidate scope (for the team to react to)
- [KEY] [title] — [pts]
- Total candidate: [pts]

## Next in queue (by rank)
- [KEY] [title] — [pts]

## Sprint goal draft
"[one sentence]"

## Warnings
- [focus factor outside the typical range; capacity not provided; upper bound capped at the historical maximum]

## Notes
- [absences/headcount considered; unestimated stories; whether velocity was missing]
```

## Rules

- **The team decides the commitment.** The proposal is a starting point; the scope is a "candidate".
- **Person-days are a diagnostic, not the origin of the range** — the range comes from velocity adjusted by availability. Do not suggest a focus→points chain that does not exist.
- **The candidate scope respects rank**: it stops at the first story that does not fit; the following ones go to "next in queue". It does not skip a large story to fit a small one.
- **Without velocity, no points range is invented** — ask the team.
- **The ceiling is asymmetric.** Availability above 100% does not push the upper bound above what the team has already delivered: it stays capped at the historical maximum, with a warning. Adjusting down is prudence, adjusting up is a bet. Always read the **WARNINGS** block of the output before taking the range to planning — that is where focus factor outside the typical range, capacity not provided and capped ceilings show up.
- **Propagate the warnings and do not swallow errors.** Reproduce the `WARNINGS` block in the pack you deliver — the warning serves the team, not the script. If the script ends with **exit 2**, the input does not match the schema: fix the normalisation and run again, never propose scope from a rejected input.
- **Do not invent capacity** — if missing, ask or flag it in "Notes".
- **Only ready stories are included.** **Do not create the sprint or move issues** without a request.
- **Keep issue keys and names verbatim.**

## Language

Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Keep verbatim items (issue keys, names, field values) untouched.

## References

| Read this | Before… |
|---|---|
| `references/capacity.md` §Capacity model | explaining where the commitment range comes from |
| `references/capacity.md` §JQL | pulling ready stories or the historical velocity |
| `references/capacity.md` §JSON schema | normalising the input before running `capacity.py` |
| `references/trackers.md` | pulling data from Azure DevOps or ClickUp instead of Jira (query and field mapping) |
