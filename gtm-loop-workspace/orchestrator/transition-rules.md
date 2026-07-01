# Transition Rules

Allowed movement for `tasks/*.md` and the `board.md` mirror.

Task files are the source of truth. `board.md` only mirrors `board_status`, lane, blocked flag, and next action for managers.

## Board Columns

`Planned -> In Progress -> Smoke Test -> In Review -> Done`

Do not create board columns for Backlog, Investigating, Designing, Building, Validating, Blocked, Approval Required, or Rework Needed.

Use task frontmatter flags instead:

- `blocked: true`
- `approval_required: true`
- `rework_needed: true`

## Swimlane Mapping

| Work state | Task frontmatter | Board column |
| --- | --- | --- |
| Not started | `board_status: planned` | Planned |
| Ricky research | `current_lane: ricky`, `board_status: in-progress` | In Progress |
| Brody requirements/evidence | `current_lane: brody`, `board_status: in-progress` | In Progress |
| Archy architecture/risk | `current_lane: archy`, `board_status: in-progress` | In Progress |
| Cody/Codex build | `current_lane: cody`, `board_status: in-progress` | In Progress |
| Verifier checks | `current_lane: verifier`, `board_status: smoke-test` | Smoke Test |
| Reporter or manager gate | `current_lane: reporter`, `board_status: in-review` | In Review |
| Completed and accepted | `board_status: done` | Done |

## UI Transition Paths

`PATCH /api/gtm-loop/tasks/{task_id}/status` is for manager board movement. It may update only `board_status` and `last_updated`.

Drag/drop on `/gtm-loop/board` is a status move only. It must call the same status endpoint, must not change `current_lane`, `current_phase`, or `current_gate`, and must not create artifacts or call external systems.

Moving to `done` through the status endpoint is allowed only when the task is unblocked, does not need rework, has required approval approved, has no requested/deferred approval records, and is already in a reporter/manager review state: `board_status: in-review`, `current_lane: reporter`, `current_lane: manager`, `current_phase: report`, or `current_gate: manager-review`.

`PATCH /api/gtm-loop/tasks/{task_id}/transition` is for orchestrator swimlane/gate progression. It may update only the safe frontmatter fields needed for the selected transition plus `last_updated`.

Allowed orchestrator transitions:

| Transition | Lane | Phase | Gate | Board status |
| --- | --- | --- | --- | --- |
| `pick-up` | `brody` | `requirements` | `requirements-accepted` | `in-progress` |
| `move-to-ricky` | `ricky` | `research` | `research-accepted` | `in-progress` |
| `move-to-brody` | `brody` | `requirements` | `requirements-accepted` | `in-progress` |
| `move-to-archy` | `archy` | `architecture` | `architecture-accepted` | `in-progress` |
| `move-to-cody` | `cody` | `build` | `build-complete` | `in-progress` |
| `move-to-verifier` | `verifier` | `smoke-test` | `smoke-test-passed` | `smoke-test` |
| `move-to-reporter` | `reporter` | `report` | `manager-review` | `in-review` |
| `mark-done` | `manager` | `done` | `done` | `done` |
| `send-back-for-rework` | `cody` | `rework` | `build-complete` | `in-progress` |

Transition writes append local audit entries under `tasks/_audit/status-changes.jsonl`. They do not call external systems, activate workflows, or write credentials.

## Lane Artifact Creation

Transitions move the task through lanes. Artifact creation creates the lane's local working documents.

`POST /api/gtm-loop/tasks/{task_id}/artifacts/{lane}` may create deterministic Markdown starters only under `artifacts/<task_id>/` and may update only `artifact_links` plus `last_updated` in the task frontmatter.

Allowed artifact lanes:

| Lane | Creates |
| --- | --- |
| `research` | Ricky research brief, sources, notes, and evidence cards. |
| `requirements` | Brody requirements, endpoint matrix, field mapping, open questions, and build handoff. |
| `architecture` | Archy architecture, integration flow, ADR, and risks. |
| `build` | Cody build plan, tool plan, test plan, and rollback plan. |
| `verification` | Verifier report, failed checks, and rework instructions. |
| `report` | Reporter completion report, manager summary, and approval request. |

Artifact creation is local-only, template-based, and audited in `tasks/_audit/artifact-events.jsonl`. It does not call LLMs, external systems, n8n MCP, or production APIs.

## Approval Queue

Approval records move risky future actions through request, approval, rejection, deferral, or cancellation. They do not execute the action.

Approval endpoints:

| Endpoint | Purpose | Writes |
| --- | --- | --- |
| `GET /api/gtm-loop/approvals` | List local approvals, with filters. | None |
| `GET /api/gtm-loop/tasks/{task_id}/approvals` | List approvals for one task. | None |
| `POST /api/gtm-loop/tasks/{task_id}/approvals` | Create one local approval request. | `tasks/_approvals/APP-####.json`, task approval summary, approval audit |
| `PATCH /api/gtm-loop/approvals/{approval_id}/decision` | Approve, reject, defer, or cancel. | Approval JSON status/notes, task approval summary, approval audit |

Task frontmatter fields `approval_required` and `approval_status` are summaries only. Approval JSON files under `tasks/_approvals/` are canonical for approval detail. Approval events are audited in `tasks/_audit/approval-events.jsonl`.

## Cody n8n Draft Executor

When a task moves to Cody/build, n8n MCP may be used only as a draft executor surface after required requirements and architecture artifacts exist.

Allowed Cody/n8n outputs:

- local workflow draft specs;
- local draft workflow JSON;
- fake payload validation notes;
- local approval requests for live n8n actions.

Blocked without explicit approval:

- live workflow creation or update;
- workflow activation, retry, scheduling, or production webhook calls;
- real credential use;
- HubSpot, Gong, AirOps, or custom API writes.

Use `executors/n8n-draft-executor.md`, `integrations/n8n-mcp.md`, and `artifacts/_templates/build/n8n-workflow-draft.md`.

Future n8n MCP calls must require a matching approved approval record for the exact requested action. Rejected, deferred, requested, or cancelled records do not unlock execution.

## Required Conditions

| From | To | Required Before Move |
| --- | --- | --- |
| Planned | In Progress | Client or global scope is known, one next action is clear, and any blocking flag is either resolved or intentionally carried. |
| In Progress | Smoke Test | Draft artifact, spec, payload, file change, or handoff exists, with acceptance checks and fake/redacted test input when relevant. |
| Smoke Test | In Review | Verifier result is recorded in the task file, including pass/fail, evidence, and any drift or rework notes. |
| In Review | Done | Reporter has updated the task, board mirror, run ledger when needed, and no blocking approval or rework flag remains. |
| Any | Planned | Work is intentionally deferred, waiting for dependency, or not ready to start. Set `blocked: true` when the next action needs input, access, evidence, or approval. |
| Any | In Review | Manager approval or reporter closeout is the next action. Set `approval_required: true` when an explicit human gate exists. |

## Done Rule

A builder cannot mark a task Done. The verifier records the result first; the reporter then moves `board_status` to `in-review` or `done`.

## Attempt Rule

- Default max attempts: `3`.
- Increment `current_attempt` when a build, design, or validation pass fails and needs rework.
- Set `rework_needed: true` when the next loop requires correction.
- Set `blocked: true` when max attempts is reached or the next step needs manager input.

## Report-Only Rule

For `L1-report-only`, transitions may produce plans, specs, Markdown, fake payloads, and approval requests. They must not execute external writes, production retries, workflow activation, sends, credential changes, or destructive actions.

## Update Order

1. Update `tasks/GTM-###.md`.
2. Update `board.md`.
3. Run `node scripts\validate-gtm-tasks.js`.
4. Update `workbench.md` only when the active pointer changes.
5. Update `runs/index.md` only for meaningful workbench history.
