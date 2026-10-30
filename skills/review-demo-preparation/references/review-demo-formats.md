# Review/demo formats and mechanisms

This reference is the operational guide for preparing a sprint review, a product demo or a product review based on Jira evidence. The goal is not just to "choose a format", but to decide how the team should communicate value, in what order and with whom speaking for each part.

## 1) Context decision rule

Before choosing the format, the skill must resolve the analysis type.

### Scrum / sprint
Use when the request indicates:
- sprint, sprint review, sprint goal, iteration, sprint cycle;
- a board with a defined cadence;
- a review of work completed in a specific sprint.

Expected result:
- filter only items completed in that sprint;
- group by value theme and perceived impact;
- place the narrative in the context of the iteration's delivery.

### Kanban / time window
Use when the request indicates:
- week, month, quarter, period, time window, delivered this week, product review;
- continuous flow, calendar, delivery backlog in a defined window;
- a review of deliveries completed on a specific date.

Expected result:
- filter by date range;
- group by themes and by value for the business or user;
- keep the focus on an executive message rather than an iteration review.

### If the context is ambiguous
Ask:
- "Do you want to analyze a specific sprint (Scrum) or a Kanban time interval?"

If there is no explicit board, project or window, ask for that data before continuing.

## 2) Preparation operational flow

### Step 1 — Filter valid deliveries
These enter the main narrative:
- Story
- Task
- Improvement
- Problem
- Incident
- Bug
- other equivalent types, when completed and deliverable

These do not enter as a main delivery:
- Test
- Test Plan
- Test Execution
- Test Set
- Xray Test
- management, support or quality items with no evidenced business/functional/operational value

### Step 2 — Group by perceived value
Group deliveries by theme, not by list of tickets. Examples of grouping:
- user experience improvement;
- operational flow automation;
- reduced process friction;
- internal efficiency improvement;
- quality or customer problem resolution;
- critical functional delivery for the business.

### Step 3 — Define the audience
The shape of the session and the level of detail must reflect the audience:
- team: more technical detail, more implementation context;
- Product Manager: focus on value, risk, decision and priority;
- stakeholders / business: focus on impact, decision and what changed;
- leadership / cross-functional: executive synthesis, risks and next steps.

### Step 4 — Define the presentation order
The order must follow impact and relevance, not Jira chronology.

Recommended priority:
1. business problem or opportunity with the greatest impact;
2. theme that changes the experience or operational capability;
3. incremental improvement or functional support;
4. items with low relevance for the session.

### Step 5 — Assign presenters
Recommended assignment:
- Product Manager: context, value, decision and business trade-offs;
- developers: main implementation, quality, risks and relevant technical details;
- if there are several owners for a theme: one main presenter and one in support.

### Step 6 — Produce the final output
Use the skill's standard structure:
- factual context;
- main message;
- value blocks;
- deliveries to present;
- suggested script;
- presenters;
- risks and dependencies;
- opening questions.

## 3) Format matrix by scenario

| Scenario | Recommended format | How to communicate |
|---|---|---|
| Internal sprint review | Narrative walkthrough | link deliveries to a value theme and explain the iteration's contribution |
| Demo for stakeholders | Value-first demo | reinforce impact, decision and relevance for the business |
| Multiple small deliveries | Theme-based demo | group by theme and reduce the feeling of a ticket list |
| Dependencies or complex flow | Journey demo | show the complete experience and the critical context |
| Executive product review | Executive synopsis | focus on decision, impact, risks and next steps |
| Session with technical audience | Deep-dive review | detail implementations, quality and relevant trade-offs |

## 4) Facilitation rules by audience

### For the internal team
- keep technical context when useful;
- highlight how the delivery supports the flow or the product;
- explain implementation risks, dependencies and decisions.

### For stakeholders
- reduce technical detail;
- prioritize impact and decision;
- use sentences that can be understood outside the Jira context.

### For leadership or PMO
- use executive language;
- reinforce risks, dependencies and pending decisions;
- avoid long lists and excess operational detail.

## 5) Recommended session structure

### Minimum structure
- session context;
- main message;
- value blocks;
- deliveries to present;
- risk, dependency and next steps;
- who presents.

### Narrated structure
- what changed;
- why it matters;
- who explains it best;
- what needs attention or a decision now.

## 6) Anti-patterns to avoid

- do not invent financial impact, ROI, adoption or metrics without evidence;
- do not present tests, management or support as a main delivery;
- do not order by Jira chronology when the audience needs a value narrative;
- do not mix technical work with business value without context;
- do not publish to Confluence or any system without an explicit request;
- do not assume the session is Scrum or Kanban without checking the context.

## 7) Pre-meeting checklist

- Is there a clear main message?
- Were the deliveries grouped by value and not as a list of issues?
- Was the audience identified and the level of detail adjusted?
- Is there a main presenter per block?
- Are there risks, dependencies or decisions to confirm?
- Does the presentation order follow impact and relevance?

## 8) Final best practice

A strong review or demo is not an enumeration of issues. It is a value narrative, structured in factual language, with a clear presentation order, defined responsibilities and a decision or alignment that the meeting should support.

## 9) Cross-reference

| Document | Use |
|---|---|
| `SKILL.md` | skill base and main operational flow |
| `evals/evals.json` | expected execution and output scenarios |
| `README.md` | summary view and usage examples |
