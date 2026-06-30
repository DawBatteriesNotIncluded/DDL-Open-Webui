# Daily Operating Loop

## Start

1. Open `HOME.md`.
2. Read `llm-wiki/current-client.md`.
3. Read `workbench.md`.
4. Review `board.md`.
5. Open the active client folder.
6. Review `open-questions.md`, `workflow-inventory.md`, and `validation-notes.md`.
7. Check `tools/tool-registry.md` and `governance/approval-gates.md` if tools or writes are involved.
8. Pick one outcome for the session.

## Work

| Situation | Use |
| --- | --- |
| Need to understand a system | `workflows/investigate.md` |
| Need to solve a broken workflow or issue | `workflows/solve-issue.md` |
| Need external/source-grounded research | `workflows/research.md` |
| Need to design a workflow | `workflows/design.md` |
| Need architecture before build | `workflows/architecture-to-build.md` |
| Need to implement from a handoff | `workflows/build.md` |
| Need to prove it works | `workflows/validate.md` |
| Need workbench readiness checks | `evals/gtm-loop-evals.md` |

## End

1. Update the client file that owns the facts.
2. Update `llm-wiki/` only for durable shared context.
3. Close or add open questions.
4. Record validation results.
5. Update `workflows/registry.md` if an automation changed stage.
6. Log meaningful work in `runs/index.md`.
7. Move or update the matching `board.md` card.
8. Write the next action in `llm-wiki/current-client.md`.

## Daily Rule

If a future agent cannot tell what is confirmed, what is unknown, and what to do next, the session is not closed.
