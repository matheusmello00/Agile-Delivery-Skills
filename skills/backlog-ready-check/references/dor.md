# Definition of Ready / Flow Readiness — Backlog Ready Check reference

## Default DoR criteria

### Scrum

An item is "ready" when, typically:
- It has a **description** with value/context (not just the title).
- It has clear, testable **acceptance criteria**.
- It is **estimated** in story points (or the configured equivalent).
- It is **linked to an epic** when the context requires product context — a gap by default (`epic_required: true`) if the team uses context hierarchies.
- It is not **too large** to fit in the next delivery slice (split candidate above the `team_estimate_ceiling` ceiling).

### Kanban

In a continuous flow, readiness for **pull / flow entry** centres on the value and clarity of the work — **not on the estimate**. By default:

- It has a **description** with value/context (not just the title).
- It has clear, testable **acceptance criteria**.
- **Estimate / T-shirt size is optional** — story points, points or size do **not** count as a readiness gap (`require_estimate: false` by default in Kanban).
- It is **linked to an epic** only if the team requires it (`epic_required`; default `true` in Scrum, but in Kanban many teams use `false`).
- It is not **too large** to fit the flow pull — only if the team uses size and has `size_ceiling` configured.

If the Kanban team **opts in** to T-shirt size or story points as a refinement practice, enable `require_estimate: true` and choose `estimate_mode` (`tshirt_size` or `story_points`). Until then, the absence of an estimate is **informational** and does not block readiness.

**Optional** criteria (can be enabled in both modes; they tend to be the ones that blow up in refinement):
- **External dependencies identified** (`require_dependencies_identified: true`).
- **Testable item / clear validation path** (`require_testable: true`).

These are the defaults. If the team has its own Definition of Ready, use theirs and record in the shortlist which criteria you applied.

## JQL — top of the backlog

### Scrum
```
project = "<CHAVE>" AND issuetype in (Story) AND sprint is EMPTY AND statusCategory != Done ORDER BY Rank ASC
```
Adjust `issuetype` if the team also refines Bugs/Tasks. Limit to the requested N.

### Kanban
```
project = "<CHAVE>" AND issuetype in (Story) AND statusCategory != Done ORDER BY Rank ASC
```
In Kanban, read the entry queue / top of the board rather than the "outside a sprint" query. Adjust `status`/`column` if the team uses a specific flow window.

## Field mapping

- **Description / AC**: the `description` field and the criteria field/section. Whether they have **substance** is the model's judgment → translated into the booleans `has_description` / `has_acceptance_criteria`.
- **Estimate / size**: in Scrum, `points` (story points) — a gap by default if absent. In Kanban, `size` / `tshirt_size` — **optional by default**; only a gap if `require_estimate: true`. In both, `estimate_mode` and `delivery_model` guide the normalisation.
- **Epic/parent**: `parent` or Epic Link. With `epic_required: true` (default), absence is a **gap**, not just a note, if the team uses epics as context.
- **Dependencies / testability**: booleans `has_dependencies_identified` / `is_testable`, assessed by the model; they only count as a gap if the respective `require_*` is on.

## Script JSON schema

```json
{
  "board": "Example Board",
  "delivery_model": "scrum",
  "estimate_mode": "story_points",
  "require_estimate": true,
  "team_estimate_ceiling": 8,
  "epic_required": true,
  "require_dependencies_identified": false,
  "require_testable": false,
  "issues": [
    {
      "key": "ABC-201",
      "title": "Checkout with Apple Pay",
      "type": "Story",
      "has_description": true,
      "has_acceptance_criteria": false,
      "points": 5,
      "has_epic": true,
      "has_dependencies_identified": true,
      "is_testable": true
    }
  ]
}
```

### Kanban example (no required estimate — default)
```json
{
  "board": "Delivery Flow",
  "delivery_model": "kanban",
  "estimate_mode": "tshirt_size",
  "require_estimate": false,
  "size_ceiling": "L",
  "epic_required": false,
  "require_dependencies_identified": true,
  "require_testable": true,
  "issues": [
    {
      "key": "KAN-301",
      "title": "Landing page refresh",
      "type": "Story",
      "has_description": true,
      "has_acceptance_criteria": true,
      "has_epic": false,
      "has_dependencies_identified": true,
      "is_testable": true
    },
    {
      "key": "KAN-302",
      "title": "Notifications API",
      "type": "Story",
      "has_description": true,
      "has_acceptance_criteria": true,
      "tshirt_size": "M",
      "has_epic": false,
      "has_dependencies_identified": true,
      "is_testable": true
    }
  ]
}
```

### Kanban example (team that opts in to T-shirt size in the DoR)
```json
{
  "board": "Delivery Flow",
  "delivery_model": "kanban",
  "estimate_mode": "tshirt_size",
  "require_estimate": true,
  "size_ceiling": "L",
  "epic_required": false,
  "issues": [
    {
      "key": "KAN-401",
      "title": "Checkout express",
      "type": "Story",
      "has_description": true,
      "has_acceptance_criteria": true,
      "tshirt_size": "M",
      "has_epic": false
    }
  ]
}
```

Notes:
- `delivery_model` defaults to `scrum` (compatibility with the old behaviour).
- `require_estimate` defaults to `true` in Scrum and **`false` in Kanban**. It only flags an estimate/size gap when explicit or when the mode default requires it.
- `estimate_mode` defaults to `story_points` in Scrum and `tshirt_size` in Kanban, but may be explicit in the payload.
- `epic_required` defaults to `true` (aligned with the DoR criterion stated above) and only makes sense with contexts that use epics.
- `require_dependencies_identified` / `require_testable` default to `false` (opt-in).
- `team_estimate_ceiling` is optional: above this value, a story with no other gaps is a split candidate in Scrum. In Kanban, `size_ceiling` and `tshirt_size` / `size` are used to detect out-of-flow fit — only applicable when a size is filled in.
- `points` may be `null` (unestimated → gap in Scrum; informational in Kanban with `require_estimate: false`). In Kanban with `require_estimate: true`, a missing `tshirt_size`/`size` counts as a "size" gap.
- Substance booleans are determined by the model; the script aggregates and applies the counting rules.
