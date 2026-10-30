# Capacity and data — Planning Preparation reference

## Capacity model

The "points that fit" range has **historical velocity as its empirical basis**; time capacity only **adjusts** it when the next sprint is atypical.

Availability = product of three ratios (each 1.0 when not applicable):
- **absences**: `net_person_days / gross_person_days` (one-off absences in the sprint).
- **relative focus**: `focus_factor / baseline_focus`. If this sprint's focus equals the one assumed in the velocity (default 0.7), this ratio is 1 and does not move the range — avoids double counting.
- **headcount**: `people / people_in_prior_sprints`, if `people_in_prior_sprints` is provided. Captures permanent team losses/gains vs the velocity sprints; emits a note when it differs from 1.

`effective_person_days = net_person_days × focus` is a **diagnostic** (shown), not the origin of the range.

**Range:** derived from the **observed min–max** of the velocities of the last N sprints, each end × availability — reflects the real dispersion instead of a fixed band. The method is echoed in the output.

**Asymmetric ceiling.** Adjusting the range down is prudence; adjusting up is a bet. Therefore, when availability exceeds 100%, the upper bound is **capped at the best delivery already recorded** and a warning is emitted with the value extrapolation would give. To allow extrapolation, pass `allow_extrapolation: true` — and even then the **candidate scope** only fills up to the historical maximum, so the proposal does not materialise the bet. Without this asymmetry, an optimistic focus produced numerical validation for over-commitment, which is the classic failure mode of planning and exactly what this skill exists to avoid.

**Focus factor range.** 0.5–0.9 is the typical range; outside it a **warning** is emitted (the value is self-reported). Outside 0.1–1.0 it is an **input error**: focus is the fraction of time dedicated to the sprint and cannot exceed 1.0. Capacity not provided (`people` or `sprint_days` at zero) also raises a warning — the range is left without a capacity basis.

**Without velocity:** the script does **not** produce a points range. It returns the effective person-days and the instruction to ask the team about the delivery of the last sprints.

## JQL

Ready items (top of the backlog, outside any sprint) — only **downstream** types (team work that goes into a sprint): Story, Task, Spike, Bug, Improvement, Incident and Problem:
```
project = "<CHAVE>" AND issuetype IN (Story, Task, Spike, Bug, Improvement, Incident, Problem) AND sprint is EMPTY AND statusCategory != Done ORDER BY Rank ASC
```
Filter those that have an estimate and criteria (or use `backlog-ready-check`).

**Upstream** types that **never** enter the search — they are not sprint work: **Initiative, Epic, Dependency, Change Request, Milestone**, and the Xray test types (**Test, Test Set, Test Plan, Test Execution**). If you prefer an exclusion rule instead of a whitelist:
```
project = "<CHAVE>" AND issuetype NOT IN (Initiative, Epic, Dependency, "Change Request", Milestone, Test, "Test Set", "Test Plan", "Test Execution") AND sprint is EMPTY AND statusCategory != Done ORDER BY Rank ASC
```
The whitelist (first form) is recommended: new types in the scheme are left out by default, instead of getting in by mistake. The list is configurable — adjust it to the project's issue type scheme.

Velocity of a previous sprint:
```
project = "<CHAVE>" AND sprint = <ID_ANTERIOR> AND statusCategory = Done
```

## Script JSON schema

```json
{
  "team": "Squad Checkout",
  "sprint_name": "Sprint 43",
  "people": 5,
  "sprint_days": 10,
  "absences_person_days": 4,
  "focus_factor": 0.7,
  "baseline_focus": 0.7,
  "people_in_prior_sprints": 6,
  "prior_velocities": [21, 18, 25],
  "ready_stories": [
    {"key": "ABC-201", "title": "Apple Pay at checkout", "points": 5},
    {"key": "ABC-202", "title": "Payment retry", "points": 3}
  ]
}
```

Notes:
- `baseline_focus` optional (default 0.7). `focus_factor` optional (default 0.7).
- `people_in_prior_sprints` optional — without it, there is no headcount adjustment.
- `absences_person_days` optional (person-days lost in the sprint).
- `prior_velocities` optional — without it, the script does not propose a points range.
- The candidate scope is built in rank order, **stopping** at the first story that does not fit; the rest go to "next in queue". Unestimated stories do not enter the scope (listed separately).
