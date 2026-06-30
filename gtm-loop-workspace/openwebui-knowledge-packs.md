# Open WebUI Knowledge Packs

Attach the smallest pack that matches the agent. Add client files only when that agent is working on that client.

## Core Pack

Use for the global workstation agent.

- `gtm-loop-workspace/README.md`
- `gtm-loop-workspace/AGENTS.md`
- `gtm-loop-workspace/HOME.md`
- `gtm-loop-workspace/workbench.md`
- `gtm-loop-workspace/UPDATE-OWNERSHIP.md`
- `gtm-loop-workspace/orchestrator/`
- `gtm-loop-workspace/schemas/board-card.md`
- `gtm-loop-workspace/board.md`
- `gtm-loop-workspace/openwebui-knowledge-packs.md`
- `gtm-loop-workspace/llm-wiki/`
- `gtm-loop-workspace/governance/approval-gates.md`
- `gtm-loop-workspace/tools/tool-registry.md`
- `gtm-loop-workspace/runs/_template.md`
- `gtm-loop-workspace/evals/gtm-loop-evals.md`

## Client Pack

Use for client-specific investigation or build work.

- Core Pack
- `gtm-loop-workspace/clients/<client-slug>/context.md`
- `gtm-loop-workspace/clients/<client-slug>/systems.md`
- `gtm-loop-workspace/clients/<client-slug>/open-questions.md`
- `gtm-loop-workspace/clients/<client-slug>/workflow-inventory.md`
- `gtm-loop-workspace/clients/<client-slug>/field-mapping.md`
- `gtm-loop-workspace/clients/<client-slug>/endpoint-matrix.md`
- `gtm-loop-workspace/clients/<client-slug>/configuration-inventory.md`
- Tool-specific client files as needed: `hubspot.md`, `gong.md`, `airops.md`, `n8n.md`

## Tool Pack

Use for tool permission, runtime, and approval discussions.

- Core Pack
- `gtm-loop-workspace/tools/tool-registry.md`
- `gtm-loop-workspace/governance/approval-gates.md`
- `gtm-loop-workspace/payloads/README.md`
- relevant fake payload examples under `gtm-loop-workspace/payloads/`

## Workflow Pack

Use for automation design, debugging, and build handoff.

- Core Pack
- Client Pack
- `gtm-loop-workspace/workflows/daily-operating-loop.md`
- `gtm-loop-workspace/workflows/investigate.md`
- `gtm-loop-workspace/workflows/solve-issue.md`
- `gtm-loop-workspace/workflows/design.md`
- `gtm-loop-workspace/workflows/architecture-to-build.md`
- `gtm-loop-workspace/workflows/build.md`
- `gtm-loop-workspace/workflows/validate.md`
- `gtm-loop-workspace/workflows/registry.md`
- `gtm-loop-workspace/payloads/`
- `gtm-loop-workspace/evals/gtm-loop-evals.md`

## Research Pack

Use for source-grounded research.

- Core Pack
- `gtm-loop-workspace/research/index.md`
- `gtm-loop-workspace/research/_template/brief.md`
- `gtm-loop-workspace/research/_template/sources.md`
- `gtm-loop-workspace/research/_template/notes.md`
- `gtm-loop-workspace/research/_template/evidence-cards.md`

## Architecture / Design Pack

Use for system maps, integration flows, risks, and ADRs.

- Core Pack
- Client Pack
- `gtm-loop-workspace/architecture/_template/system-map.md`
- `gtm-loop-workspace/architecture/_template/integration-flow.md`
- `gtm-loop-workspace/architecture/_template/risks-and-threat-model.md`
- `gtm-loop-workspace/architecture/_template/architecture-review.md`
- `gtm-loop-workspace/architecture/_template/adr.md`

## Build Handoff Pack

Use when handing work to Codex, n8n, AirOps, or a human builder.

- Core Pack
- Client Pack
- `gtm-loop-workspace/clients/<client-slug>/build-handoff.md`
- `gtm-loop-workspace/clients/<client-slug>/validation-notes.md`
- `gtm-loop-workspace/evals/gtm-loop-evals.md`
- relevant fake/redacted payloads under `gtm-loop-workspace/payloads/`

## Rule

Do not attach raw customer exports, real transcripts, secrets, auth headers, endpoint hosts, tenant IDs, or copied logs as Knowledge.
