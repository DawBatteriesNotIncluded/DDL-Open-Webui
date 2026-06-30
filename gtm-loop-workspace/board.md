# GTM Loop Board

Manager-facing mirror of `tasks/*.md`. The task files are the source of truth; update the task first, then update this board summary.

Task schema: `schemas/task-card.md`
Transition rules: `orchestrator/transition-rules.md`

## Planned

- [GTM-001](tasks/GTM-001.md) - Onboard first real client
  - Client: TBD
  - Lane: Brody
  - Status: Planned
  - Blocked: yes
  - Next action: Manager provides client name and initial automation objective.

- [GTM-003](tasks/GTM-003.md) - Confirm tool permissions
  - Client: Global
  - Lane: Brody
  - Status: Planned
  - Blocked: yes
  - Next action: Confirm which integration surfaces are read-only, draft-only, approval-gated, deferred, or disabled.

- [GTM-004](tasks/GTM-004.md) - Identify first automation candidate
  - Client: TBD
  - Lane: Brody
  - Status: Planned
  - Blocked: yes
  - Next action: Capture current manual workflow and open questions.

- [GTM-005](tasks/GTM-005.md) - Draft first architecture-to-build pack
  - Client: TBD
  - Lane: Archy
  - Status: Planned
  - Blocked: yes
  - Next action: Map systems, boundaries, flow, risks, and build handoff.

- [GTM-006](tasks/GTM-006.md) - Prepare first build handoff
  - Client: TBD
  - Lane: Cody
  - Status: Planned
  - Blocked: yes
  - Next action: Add confirmed requirements and acceptance checks.

- [GTM-007](tasks/GTM-007.md) - Validate first workflow with fake payloads
  - Client: TBD
  - Lane: Verifier
  - Status: Planned
  - Blocked: yes
  - Next action: Pick one fake payload and record expected output.

## In Progress

_No active tasks._

## Smoke Test

_No active tasks._

## In Review

_No active tasks._

## Done

- [GTM-011](tasks/GTM-011.md) - Verify local Docker test runtime
  - Client: Global
  - Lane: Reporter
  - Status: Done
  - Blocked: no
  - Next action: Open `http://localhost:3000/gtm-loop` and complete manual Open WebUI agent/Knowledge setup if needed.

- [GTM-010](tasks/GTM-010.md) - Add report-only orchestrator spine
  - Client: Global
  - Lane: Reporter
  - Status: Done
  - Blocked: no
  - Next action: Use `GTM-001` to onboard the first real client.

- [GTM-009](tasks/GTM-009.md) - Add Open WebUI GTM Loop UI surface
  - Client: Global
  - Lane: Reporter
  - Status: Done
  - Blocked: no
  - Next action: Open `http://localhost:3000/gtm-loop` or use the sidebar `GTM Loop` link.

- [GTM-002](tasks/GTM-002.md) - Configure Open WebUI Workstation Agent and Core Pack
  - Client: Global
  - Lane: Reporter
  - Status: Done
  - Blocked: no
  - Next action: Verify in Open WebUI, then use `GTM-001` for first-client onboarding.

- [GTM-000](tasks/GTM-000.md) - Create lean GTM Loop Markdown workspace
  - Client: Global
  - Lane: Reporter
  - Status: Done
  - Blocked: no
  - Next action: None.

Board rules: `tasks/*.md` is canonical; `board.md` is a short manager-facing mirror. Columns stay limited to Planned, In Progress, Smoke Test, In Review, and Done. `blocked`, `approval_required`, and `rework_needed` are task flags, not columns.
