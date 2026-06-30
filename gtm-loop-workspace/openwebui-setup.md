# Open WebUI Setup

Minimal setup for using this repo as an automation AI workbench.

## Knowledge To Attach

Attach these first:

- `gtm-loop-workspace/README.md`
- `gtm-loop-workspace/AGENTS.md`
- `gtm-loop-workspace/HOME.md`
- `gtm-loop-workspace/workbench.md`
- `gtm-loop-workspace/board.md`
- `gtm-loop-workspace/llm-wiki/`
- `gtm-loop-workspace/workflows/`
- `gtm-loop-workspace/clients/_template/`
- `gtm-loop-workspace/tools/tool-registry.md`
- `gtm-loop-workspace/governance/approval-gates.md`
- `gtm-loop-workspace/evals/gtm-loop-evals.md`

## Primary Agent

Create one custom Open WebUI model from:

- `gtm-loop-workspace/agents/loop-engineering-workstation-agent.md`

Use this as the default cockpit agent for daily loop engineering.

## Specialist Agents

Add these only when needed:

| Agent | Use |
| --- | --- |
| `agents/loop-architect-agent.md` | Turn vague work into loop specs. |
| `agents/build-controller-agent.md` | Coordinate design, build, QA, and approval. |
| `agents/workflow-debugger-agent.md` | Diagnose failed workflows and payloads. |
| `agents/n8n-builder-agent.md` | Draft n8n workflow plans. |
| `agents/hubspot-architect-agent.md` | HubSpot object/field/workflow design. |
| `agents/gong-intelligence-agent.md` | Gong signal extraction and deal intelligence. |

## Tool Rule

Start with Knowledge-only. Add n8n, HubSpot, Gong, AirOps, API, or repo tools only after `tools/tool-registry.md` and `governance/approval-gates.md` define the allowed actions.

## First Run

1. Open `workbench.md`.
2. Set active client.
3. Pick one board card.
4. Run the Loop Engineering Workstation Agent.
5. Log the result in `runs/index.md`.
