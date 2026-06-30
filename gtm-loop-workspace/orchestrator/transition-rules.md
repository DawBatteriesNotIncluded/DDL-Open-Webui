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
