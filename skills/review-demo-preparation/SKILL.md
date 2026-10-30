---
name: review-demo-preparation
description: 'Prepares a sprint review or a product demo from completed Jira items, grouping them by perceived value, structuring a business-oriented narrative and proposing presenters based on the assignees and their real contribution. Suitable for Scrum and Kanban. Does not create actions, does not invent impact and does not replace the team decision on what to demo.'
when_to_use: 'When the team needs to turn completed deliveries into a credible briefing for a sprint review, product demo, stakeholder session or product review, focused on value, narrative and presentation ownership.'
maturity: ready
allowed-tools:
- Bash
- Read
- mcp__atlassian
- mcp__azure-devops
- mcp__clickup
compatibility: 'Requires a tracker connector (MCP) with read access: Atlassian (Jira), Azure DevOps or ClickUp. Confluence is only used if the user asks for publication, and it is never written automatically.'
argument-hint: '[board] [sprint | period] [audience | goal]'
metadata:
  author: Matheus Mello
  version: '0.1.0'
audience: 'Scrum Master, PM, Product Owner, Agile Coach, Team Lead'
tags:
- agile
- scrum
- kanban
- review
- demo
- jira
- azure-devops
- clickup
---

# Review Demo Preparation Pack

This pack prepares a review or demo from facts, focused on perceived value, a coherent narrative and a clear split of presentation responsibilities. The goal is not to replace the meeting or to invent impact; it is to give the team a factual, actionable working base to run a session with clarity and credibility.

## Goal

Turn delivered Jira items into:
- a short narrative that is relevant to the audience;
- a set of value blocks in order of impact;
- a practical presenter recommendation;
- a briefing structure that the Product Manager and the team can use before the session.

## Scope and limits

- Reads Jira only; does not create, change or publish items without an explicit request.
- Works only with evidence of items completed in the requested interval.
- Does not invent business outcome, financial impact, ROI, metrics or adoption when these are not provided.
- Rejects or narrows hypotheses when the material is insufficient and asks for clarification.
- The session can be Scrum (sprint) or Kanban (time window); the skill must tell the two apart before synthesizing.

## Minimum requirements

- A tracker connector (MCP) with read access — Atlassian (Jira), Azure DevOps or ClickUp — to the board/project, sprint or analysis window. See `references/trackers.md`.
- Name of the board, project or relevant area.
- Session type: sprint review, demo, product review, stakeholder review or list of deliveries.
- Target audience: team, stakeholders, business, internal customers, cross-functional.
- Analysis period: a specific sprint, week, month or date range.

## Context resolution rule

The skill must first identify the analysis mode before structuring the output.

- Scrum / Sprint mode:
  - applies when the user mentions sprint, sprint review, sprint goal, SNN, retro/preview, a board with sprint cadence, or when the context indicates a review per iteration.
  - uses the issues completed in that sprint.
- Kanban / continuous flow mode:
  - applies when the user mentions week, month, quarter, period, delivery backlog, product demo, delivered this week, flow channel or calendar.
  - uses a time window and filters the issues completed in the interval.
- If the context is ambiguous:
  - ask: "Do you want to analyze a specific sprint (Scrum) or a Kanban time interval?"
- If the board or the project is not clear:
  - ask for the board/project and the relevant date window.

## Inherited context contract

The factual block must be consistent and comparable between sessions. The skill always uses the same minimum set of context:
- issues completed in the analysis interval;
- assignees and main owners;
- value themes or epics;
- perceived impact for the business, user or operation;
- suggested presentation order;
- risks, dependencies and follow-up questions.

## Extraction and filtering rules

1. **Resolve the analysis interval** based on the delivery mode and the user's input.
2. **Filter deliverable items**. Only these enter the synthesis:
   - Story
   - Task
   - Improvement
   - Problem
   - Incident
   - Bug
   - other equivalent types, when finished and deliverable
3. **Exclude non-deliverable items**. They do not count toward the count, the narrative or the deliveries table:
   - Test
   - Test Plan
   - Test Execution
   - Test Set
   - Xray Test
   - any management, quality or support items that do not represent a business/functional/operational delivery
4. **If there is quality/coverage evidence** and it is useful, it may be mentioned for transparency, but without mixing it with the main delivery narrative.
5. **Never use the "done" status without confirming the board logic**. If there is a risk of ambiguity, ask before interpreting.

## Work process

1. Resolve the session type and the interval.
2. Get the relevant completed issues and check the item type.
3. Group the deliveries by perceived value, not just by area or component.
4. Identify verifiable impact: flow improvement, reduced friction, capacity gain, feature delivery, customer problem resolved, operations support or risk mitigated.
5. Choose the format best suited to the audience:
   - internal review: narrative walkthrough
   - demo with stakeholders: value-first demo
   - several small deliveries: theme-based demo
   - dependencies/complexity: journey demo
   - executive review: executive synopsis
6. Define the script and the presentation split.
7. Produce the final briefing in the structured output format.

## Operational flow per scenario

The skill must apply a basic decision flow before the synthesis:

- If the request is Scrum / sprint: filter only items completed in the sprint and use the iteration narrative.
- If the request is Kanban / time window: filter by interval and use the value and business narrative.
- If the audience is the team: use more technical detail and focus on implementation and risk.
- If the audience is stakeholders: reduce technical detail and reinforce impact, decision and next steps.
- If the work is fragmented: group by theme and present in value blocks.
- If there are complex dependencies: use a journey narrative, not a list of issues.

This flow must be in line with the scenarios documented in `references/review-demo-formats.md` and with the skill's quality evals.

## Presentation criteria

- The presentation must answer: "what changed?", "why does it matter?", "who explains it best?"
- The PM/PO leads the context, the value and the decision.
- Developers explain implementation, quality and trade-offs.
- The presentation order must follow impact and relevance for the audience, not just Jira chronology.
- In sessions with stakeholders, reduce technical detail and reinforce the business message.

## Expected output

The output must follow this contract, with factual, clear language and no exaggeration (see the Language section for the output language):

```md
# Review / Demo — [sprint or board name]

## 1) Factual context
- Period: [start date → end date]
- Completed issues: [n]
- Main owners: [names / roles]
- Value themes: [short list]
- Dependencies / blockers: [summary]
- Target audience: [team / stakeholders / business / cross-functional]

## 2) Main message
- Value delivered: [short 1-line sentence]
- Session goal: [what the team wants to align on or decide]

## 3) Value blocks
1. [Theme 1] — [what was delivered] — [why it matters]
2. [Theme 2] — [what was delivered] — [why it matters]
3. [Theme 3] — [what was delivered] — [why it matters]

## 4) Deliveries to present
| Theme | Issues | Assignee(s) | Presentation script |
|---|---|---|---|
| [Theme] | [JIRA] | [name] | [1 line] |
| [Theme] | [JIRA] | [name] | [1 line] |

## 5) Suggested script
- Opening and goal — 3 min
- What changed — 8-10 min
- Impact for business / user — 6-8 min
- Next steps / decisions — 3-5 min

## 6) Who presents
- Product Manager / PO — context, value and decision
- Developer A — main implementation
- Developer B — quality, risks or relevant technical part

## 7) Transparency and risks
- Implementation / quality risks: [summary]
- External dependencies: [summary]
- Follow-up questions: [list]

## 8) Opening questions
- What changed since the last review?
- What is the impact for the business, user or operation?
- What needs attention, a decision or alignment today?
```

## Quality guardrails

- Only state what the data supports.
- Do not invent impact, business metrics or usage that do not appear in the context.
- Do not turn technical deliveries into "business value" without contextual evidence.
- If data is missing, say "I don't have enough evidence to state X" instead of inferring.
- Keep names and other verbatim items (issue keys, field values) untouched.
- Do not publish to Confluence or any system without an explicit request.
- If there are multiple boards, use the explicit board/project or ask for confirmation.

## Language

Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Keep verbatim items (issue keys, names, field values) untouched.

## References

| Read this | Before... |
|---|---|
|`references/review-demo-formats.md` | quick choice by context and audience |
|`references/review-demo-formats.md` | criteria for presenting by theme, PM/developers and facilitation |
| `references/trackers.md` | pulling data from Azure DevOps or ClickUp instead of Jira (query and field mapping) |
