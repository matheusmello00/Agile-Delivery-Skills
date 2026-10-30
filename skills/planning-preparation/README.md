# planning-preparation

Crosses the ready stories at the top of the backlog with the team's real capacity and historical velocity, and proposes a candidate scope and a sprint-goal draft for the team to react to.

**When to use:** before planning — how much fits, which stories to propose, which sprint goal to draft.
**Not for:** assessing story readiness (`backlog-ready-check`) or analysing the past sprint in a separate skill; sprint context comes from the board/Jira. It does not create the sprint or move issues.

## Requirements
A tracker connector (MCP) with read access: Atlassian (Jira), Azure DevOps or ClickUp (mapping in `references/trackers.md`). Python 3.9+.

## Script
```bash
python scripts/capacity.py planning.json [--json]
python scripts/capacity.py --help
```
Input schema in `references/capacity.md`.

## Behavior notes
- The commitment range comes from **velocity adjusted by availability** (absences × focus relative to baseline × headcount). Effective person-days are a **diagnostic**, not the origin of the range.
- The range is the **observed min–max** of the velocities, not a fixed band — it reflects the real dispersion.
- **Without historical velocity no points range is proposed.** It returns the person-days and asks the team about recent delivery.
- **Asymmetric ceiling:** availability above 100% does not extrapolate above the best recorded delivery — the upper bound is capped and a warning is raised. With `allow_extrapolation: true` the range extends, but the candidate scope still only fills up to the historical maximum. `focus_factor` outside 0.5–0.9 raises a warning; outside 0.1–1.0 it is an input error.
- The candidate scope **respects rank**: it stops at the first story that does not fit; the following ones go to "next in queue".

## Language
Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Issue keys, names and field values stay verbatim.
