# GTM Loop Orchestrator

Report-only control layer for the GTM Loop workspace.

This folder is the brain of the workstation. It defines how a Markdown task moves from idea to investigated facts, design, build handoff, verification, and report. It does not execute external actions.

## Start Order

1. Read `state.md`.
2. Read `loop-constraints.md`.
3. Read `transition-rules.md`.
4. Read `agent-routing.md`.
5. Read the active task under `../tasks/`.
6. Read `../board.md` as the manager-facing mirror.
7. Create or resume a run from `../runs/_template.md`.

## Control Files

| File | Owns |
| --- | --- |
| `state.md` | Active task pointer, kill switch, attempt limits, and current orchestration level. |
| `loop-constraints.md` | Report-only boundaries, stop conditions, attempt caps, and human gates. |
| `transition-rules.md` | Allowed task status movement and done criteria. |
| `agent-routing.md` | Ricky, Brody, Archy, Cody/Codex, verifier, reporter roles and tool placement. |
| `../schemas/task-card.md` | Required task frontmatter and body fields. |
| `../schemas/board-card.md` | Required board mirror summary fields. |
| `../runs/_template.md` | Per-run evidence template. |

## Operating Rule

One active task, one active run, one next action. Tools are capabilities, not the control system.
