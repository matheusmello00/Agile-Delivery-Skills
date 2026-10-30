---
name: retro-preparation
description: 'Prepares a facts-based retrospective: inherits a fixed set of sprint or flow metrics straight from Jira / the team board, highlights two or three candidate themes phrased as neutral questions, proposes a format and a collection mechanism suited to the moment the team is in, and delivers the facilitation pack with agenda, timeboxes and prompts. Generic: any board or team. Does not compute the sprint/flow metrics through an external skill, does not create the action tickets and does not publish to Confluence unless asked.'
when_to_use: 'When preparing or facilitating a retrospective and you need to decide what to discuss, which format to use, or how to open the session with data, including cases of low morale, a new team, a distributed team, and teams in continuous Kanban flow. Serves Scrum Master, PMO, Agile Coach and Kanban teams.'
maturity: ready
allowed-tools:
- Bash
- Read
- mcp__atlassian
- mcp__azure-devops
- mcp__clickup
compatibility: 'Requires a tracker connector (MCP) with read access: Atlassian (Jira), Azure DevOps or ClickUp; Confluence only for the optional publishable version. Scripts in standard-library Python 3, no external dependencies.'
argument-hint: '[board] [sprint] [period]'
metadata:
  author: Matheus Mello
  version: '0.1.0'
audience: 'Scrum Master, PMO, Agile Coach, Kanban Leads and continuous-flow teams'
tags:
- agile
- scrum
- kanban
- retrospective
- facilitation
---

# Retro Preparation Pack

Prepares a retrospective that starts from facts. The common mistake is to walk into the retro with feelings only; this skill brings the sprint/period data or the continuous-flow data and translates it into 2-3 concrete themes for the team to discuss, plus a format and an agenda to facilitate.

The goal is not for the skill to "run" the retro or draw conclusions for the team — it is to give the Scrum Master, Agile Coach or facilitator a good factual starting point and a structure, letting the insight emerge from the people.

## Requires

A tracker connector (MCP) — Atlassian (Jira), Azure DevOps or ClickUp — for the sprint/flow data (see `references/trackers.md`). Confluence (optional) only to publish the agenda/notes. Nothing is written without a request.

## Flow

1. **Get the period / flow result.** Pull the sprint or flow data directly from Jira / the team board, normalizing it into a single comparable contract. **Inherited metrics contract:** the "Factual context" block always uses the same minimum set, mapped to the keys of the normalized JSON output, so retros of the same team are comparable over time:
   - in Scrum: `commitment_reliability_pct_count`, `carryover`, `scope_change_pct`, `velocity` vs `prior_velocity_avg`, `flagged.issues`
   - in Kanban: `lead_time_avg`, `cycle_time_avg`, `throughput`, `wip_by_column`, `blocked_items`, `waiting_time` / `wait_age`
   If data is missing, do not invent it: record the warnings and report only what the board supports.
2. **Extract 2-3 candidate themes** from that data — objective signals, not judgments. Triggers: carryover concentrated in one epic (use `by_epic`); high scope change; insufficient delivery (flat burndown); many flagged; high lead time; WIP over the limit; queues in columns; many wait blockers. Phrase each theme as a **neutral question**, not a verdict.
3. **Choose the format.** See `references/retro-formats.md` — it includes the formats and the **orthogonal mechanisms** (anonymous/asynchronous collection) for the "low morale", "distributed team" and "continuous flow also requires reflection on the board" cases.
4. **Assemble the facilitation pack** with the template below.
5. **Actions → tickets** only on request and with approval.
6. **Publish (optional)** to Confluence: propose it and let the user publish — no overwrite.

## Pack template

```
# Retro — [sprint name / flow window]

## Factual context (to open) — comparable minimum set
- Model: [Scrum / Kanban]
- Reliability (count): [..%]
- Carryover: [X issues / Y pts]
- Scope change: [..%]
- Velocity: [Y] vs average [Z]
- Blocked: [n]
- Lead time / cycle time: [..]
- Throughput: [..]
- WIP per column: [..]
- Wait / blocked age: [..]

## Candidate themes
1. [theme as a neutral question] — why it matters: [1 line]

## Suggested format: [name]  ·  Mechanism: [in person / anonymous / asynchronous]
Why: [1-2 lines tied to the team's moment and operating context]

## Agenda (default 60 min; adjust to the team)
- Check-in / set the stage — 5 min
- Gather data — 15 min
- Generate insights — 20 min
- Decide actions — 15 min
- Close — 5 min
[groups > ~8 people: gather in breakouts and merge in plenary]

## Opening prompts / questions
- [3-5 questions aligned with the format and the themes]
```

## Rules

- **Facts, not judgments.** Themes are born from the data, as neutral questions. No blaming people.
- **Fixed minimum set of inherited metrics** — for comparability between the team's retros. In Kanban the specific set is the flow set, not the sprint set.
- **If the Jira / board feed returns warnings, bring them into the retro.** A `WARNINGS` block in the output (zero issues, insufficient estimate coverage, noisy lead time, zero throughput, incomplete flow data) changes what can be claimed in the session: do not open the retro with metrics that the board context itself flagged as unreliable.
- **Only state what the data supports.**
- **The team owns the insights and the actions.**
- **Verbatim names.**
- **Do not write without a request**; Confluence is propose-and-the-user-publishes; tickets only on request.

## Language

Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Keep verbatim items (issue keys, names, field values) untouched.

## References

| Read this | Before… |
|---|---|
| `references/retro-formats.md` §Quick choice | proposing the format for the team's moment |
| `references/retro-formats.md` §Collection mechanisms | a team with low morale, new or distributed |
| `references/trackers.md` | pulling data from Azure DevOps or ClickUp instead of Jira (query and field mapping) |
