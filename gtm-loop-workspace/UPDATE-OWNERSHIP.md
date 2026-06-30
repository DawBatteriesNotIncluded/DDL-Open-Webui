# Update Ownership

Use this page when deciding where a fact, task, decision, or status update belongs.

## Ownership Matrix

| File | Owns | Does Not Own |
| --- | --- | --- |
| `HOME.md` | Daily dashboard, quick status, next 3 actions, blockers, quick links. | Durable facts, audit trail, detailed tasks, tool permissions. |
| `README.md` | Static workspace overview, folder map, how the workbench is intended to be used. | Daily status, active client, task details. |
| `workbench.md` | Agent-readable control manifest: active client, active task, lane, approval mode, enabled/disabled tools, safety posture, Knowledge pack version. | Detailed task notes, run history, client facts. |
| `orchestrator/state.md` | Active orchestration level, kill switch, active task pointer, active run pointer, gate, and attempt limits. | Full task detail, evidence notes, client facts. |
| `orchestrator/transition-rules.md` | Allowed board movement, done criteria, attempt rules, and report-only transition boundaries. | Task-specific status or run history. |
| `orchestrator/agent-routing.md` | Ricky, Brody, Archy, Cody/Codex, verifier, reporter, manager, and tool-placement responsibilities. | Agent prompts or tool credentials. |
| `orchestrator/loop-constraints.md` | Report-only boundaries, stop conditions, attempt caps, kill switch, and human gates. | Detailed approval history or tool inventory. |
| `schemas/task-card.md` | Required task frontmatter and body fields. | Current task state. |
| `schemas/board-card.md` | Required board mirror summary shape. | Current task state. |
| `tasks/` | Canonical task source of truth: status, lane, flags, gates, evidence links, artifacts, decisions, manager report. | Durable client facts, raw logs, secrets, or long transcripts. |
| `board.md` | Five-column manager-facing mirror over `tasks/*.md`. | Full investigation notes, validation evidence, historical audit trail, canonical state. |
| `llm-wiki/llm-index.md` | Durable agent memory entry point and routing. | Session scratch notes, daily task state. |
| `llm-wiki/current-client.md` | Durable current-client pointer and stable active-client summary. | Full client dossier. |
| `clients/<client-slug>/` | Client-specific source of truth: context, systems, fields, endpoints, workflows, questions, build handoff, validation. | Cross-client patterns and global tool policy. |
| `runs/index.md` | Audit trail index of meaningful runs: investigations, builds, validations, approval requests. | Live task queue or detailed client notes. |
| `runs/_template.md` | Template for per-run evidence files. | Current run evidence for a specific run. |
| `workflows/registry.md` | Cross-client automation inventory and lifecycle status. | Per-client workflow details. |
| `tools/tool-registry.md` | Available tools, access levels, safe reads, blocked actions, owners, evidence. | Active work status or approval history. |
| `governance/approval-gates.md` | Approval rules and do-not-automate-yet boundaries. | Tool inventory or run results. |
| `payloads/` | Fake/redacted payload examples for testing and design. | Real customer data, logs, secrets. |
| `evals/gtm-loop-evals.md` | Readiness checklists for investigation, build, validation, production activation. | Test evidence from a specific client run. |
| `openwebui-knowledge-packs.md` | Recommended Knowledge bundles by agent type. | Agent prompts or client facts. |

## Update Rules

- Put facts where they will be reused.
- Put task movement in `tasks/GTM-###.md`, then mirror it in `board.md`.
- Put audit history in `runs/index.md`.
- Put stable agent memory in `llm-wiki/`.
- Put client detail in the client folder.
- Put global policy in `governance/` or `tools/`.
- If the same update seems to belong in three places, update the owner file and link to it from the others.

## Closeout Rule

At the end of a meaningful session, update only:

1. the owning task file in `tasks/`;
2. the owning client/workbench file if the pointer or client facts changed;
3. `board.md`;
4. `runs/index.md` if the work changed state or produced evidence;
5. `llm-wiki/` only if future agents need the fact before work starts.
