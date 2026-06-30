# GTM Loop Evals

Manual readiness checklists for orchestration, investigation, build, validation, and production activation. Use `scripts/validate-json-payloads.py` for local fake payload JSON checks.

## Orchestrator Readiness

| Check | Pass? | Notes |
| --- | --- | --- |
| `orchestrator/state.md` names the active card and run pointer | Unknown | `TBD` |
| Active card follows `schemas/board-card.md` | Unknown | `TBD` |
| Active card status matches its board section | Unknown | `TBD` |
| Attempt count is below max attempts | Unknown | `TBD` |
| Gate is explicit: None, Manager input required, Dependency blocked, Tool access required, Human approval required, or Verifier required | Unknown | `TBD` |
| Transition is allowed by `orchestrator/transition-rules.md` | Unknown | `TBD` |
| Report-only boundaries in `orchestrator/loop-constraints.md` were checked | Unknown | `TBD` |

## Investigation Readiness

| Check | Pass? | Notes |
| --- | --- | --- |
| Active client is set in `workbench.md` and `llm-wiki/current-client.md` | Unknown | `TBD` |
| One board card owns the current outcome | Unknown | `TBD` |
| Scope and non-goals are written | Unknown | `TBD` |
| Evidence sources are listed | Unknown | `TBD` |
| Findings use Confirmed / Confirmed mismatch / Unknown / Inferred / Recommendation | Unknown | `TBD` |
| Open questions have owners or evidence needed | Unknown | `TBD` |

## Build Readiness

| Check | Pass? | Notes |
| --- | --- | --- |
| Objective is clear | Unknown | `TBD` |
| Source and target systems are known | Unknown | `TBD` |
| Required fields are mapped | Unknown | `TBD` |
| Endpoint, trigger, or auth model is known or blocked | Unknown | `TBD` |
| Tool permissions are checked in `tools/tool-registry.md` | Unknown | `TBD` |
| Approval gates are checked in `governance/approval-gates.md` | Unknown | `TBD` |
| Failure behavior is defined | Unknown | `TBD` |
| Fake/redacted test payload exists | Unknown | `TBD` |
| Build handoff has acceptance checks | Unknown | `TBD` |

## Validation Readiness

| Check | Pass? | Notes |
| --- | --- | --- |
| Expected output is recorded | Unknown | `TBD` |
| Actual result is recorded | Unknown | `TBD` |
| Negative/error path is considered | Unknown | `TBD` |
| Field-level mapping result is checked | Unknown | `TBD` |
| No real customer data is used in test payloads | Unknown | `TBD` |
| Run is logged in `runs/index.md` when meaningful | Unknown | `TBD` |

## Verifier Readiness

| Check | Pass? | Notes |
| --- | --- | --- |
| Builder output is linked from the card or run file | Unknown | `TBD` |
| Acceptance checks are observable, not vague | Unknown | `TBD` |
| Expected and actual results are compared | Unknown | `TBD` |
| Safety gates and approval gates were checked | Unknown | `TBD` |
| Rework decision is recorded: pass, retry, or blocked | Unknown | `TBD` |
| Reporter moved the card only after verifier result | Unknown | `TBD` |

## Production Activation Readiness

| Check | Pass? | Notes |
| --- | --- | --- |
| Production activation is explicitly requested by the user | Unknown | `TBD` |
| Workflow owner is identified | Unknown | `TBD` |
| Rollback or disable path is known | Unknown | `TBD` |
| Monitoring or failure alert path is known | Unknown | `TBD` |
| Idempotency or duplicate handling is known | Unknown | `TBD` |
| Approval request names exact action, system, data affected, and risk | Unknown | `TBD` |

## Result

Ready / Not ready / Blocked

Reason:

`TBD`
