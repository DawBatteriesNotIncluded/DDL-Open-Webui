# Task Card Contract

Markdown files under `../tasks/` are the canonical task source of truth for the GTM Loop workstation.

`../board.md` is a manager-facing mirror only. Agents update the task file first, then update the board summary.

## Required Frontmatter

```yaml
---
gtm_task: true
id: GTM-001
title: ""
client: ""
board_status: planned
current_lane: brody
current_gate: ""
current_phase: intake
priority: medium
progress: 0

manager_request: ""
interpreted_objective: ""

research_agent: Ricky Research Agent
requirements_agent: Brody Investigation Agent
architecture_agent: Archy Architecture Agent
builder_agent: Cody Build Agent
verifier_agent: GTM Verifier Agent
reporter_agent: GTM Reporter Agent

executor: ""
verifier: GTM Verifier Agent

approval_required: false
approval_status: not_required
blocked: false
blocker: ""
rework_needed: false

proposal_required: false
architecture_required: false

current_attempt: 0
max_attempts: 3

dependencies: []
tags: []
artifact_links: []
evidence_links: []

next_action: ""
definition_of_done: ""
manager_summary: ""
last_updated: ""
---
```

## Allowed Values

| Field | Values |
| --- | --- |
| `board_status` | `planned`, `in-progress`, `smoke-test`, `in-review`, `done`, `cancelled` |
| `current_lane` | `ricky`, `brody`, `archy`, `cody`, `verifier`, `reporter`, `manager`, `none` |
| `approval_status` | `not_required`, `required`, `requested`, `approved`, `rejected`, `deferred` |
| `priority` | `low`, `medium`, `high`, `urgent` |
| `current_phase` | `intake`, `triage`, `context-read`, `research`, `requirements`, `proposal`, `architecture`, `execution-plan`, `build`, `verify`, `rework`, `smoke-test`, `report`, `board-update`, `done` |
| `progress` | Integer from `0` to `100` |

## Required Body Sections

```markdown
# <Task ID>: <Title>

## Manager request

## Interpreted objective

## Current status

## Lane history

## Gate checklist

## Evidence

## Artifacts

## Decisions

## Open questions

## Next action

## Manager report
```

## Board Mapping

| Detailed state | `board_status` | Board column |
| --- | --- | --- |
| Not started | `planned` | Planned |
| Ricky/Brody/Archy/Cody work | `in-progress` | In Progress |
| Verifier work | `smoke-test` | Smoke Test |
| Reporter or manager gate | `in-review` | In Review |
| Completed and accepted | `done` | Done |
| Cancelled or intentionally removed from board | `cancelled` | Not listed |

`blocked`, `approval_required`, and `rework_needed` are frontmatter flags. They must not become board columns.

## Update Rule

1. Update `tasks/GTM-###.md`.
2. Update `../board.md` with the short summary.
3. Run `node scripts\validate-gtm-tasks.js` from the repo root.
4. Update `../workbench.md` only when the active pointer changes.
5. Update `../runs/index.md` only for meaningful run history.

Future frontend board work must read from valid task files. Validation must pass before connecting any executor, MCP write path, or external automation surface.
