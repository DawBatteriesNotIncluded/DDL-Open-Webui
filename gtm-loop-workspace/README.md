# GTM Loop Workspace

Lean Markdown workspace for GTM and Forward Deployed AI Solutions Engineering inside Open WebUI.

Use it to keep client context, system maps, field mappings, workflow inventories, research notes, architecture decisions, and Codex/n8n/AirOps handoffs in one agent-readable source of truth.

## Start Here

1. Open `HOME.md`.
2. Read `AGENTS.md` before asking an agent to work in this workspace.
3. Read `workbench.md` for active workbench state.
4. Read `llm-wiki/llm-index.md` for current context and routing.
5. Check `board.md` for active work.
6. Pick or create a client folder from `clients/_template/`.
7. Run the daily loop in `workflows/daily-operating-loop.md`.
8. Keep confirmed facts, mismatches, unknowns, and evidence separate.
9. Promote stable findings back into `llm-wiki/` so future agents start with the right context.

## Folder Map

| Path | Use |
| --- | --- |
| `HOME.md` | Daily dashboard for active client, board card, tools, readiness, quick links, and end-of-session checks. |
| `workbench.md` | Current workbench manifest: active client, tools, control files, and safety rule. |
| `board.md` | Markdown Kanban board for backlog, investigation, design, build, validation, blockers, and done work. |
| `agents/` | Open WebUI system prompts, including the Loop Engineering Workstation Agent. |
| `llm-wiki/` | Agent-readable source of truth: current client, system map, shared context, open questions, repo index, and reusable patterns. |
| `clients/_template/` | Client dossier template for HubSpot, Gong, AirOps, n8n, custom APIs, field mappings, endpoints, config, validation, and build handoff. |
| `tools/tool-registry.md` | Tool registry for access level, allowed actions, blocked actions, owner, and evidence. |
| `governance/approval-gates.md` | Hard approval rules for writes, sends, activation, retries, credentials, and destructive actions. |
| `runs/index.md` | Run ledger for investigations, builds, validations, debugging, and approval requests. |
| `payloads/` | Fake/redacted payload library for testing without real client data. |
| `research/_template/` | Ricky-style research session template with brief, sources, notes, and evidence cards. |
| `architecture/_template/` | Archy-style system map, integration flow, ADR, risk/threat model, and architecture review templates. |
| `prompts/` | Ready-to-paste prompts for Codex, client discovery, troubleshooting, and platform-specific design work. |
| `workflows/` | Repeatable operating loops for investigation, research, design, build, validation, and daily use. |
| `workflows/registry.md` | Cross-client registry of automations and runtime status. |
| `evals/gtm-loop-evals.md` | Grounding, safety, build-readiness, and validation checks. |
| `openwebui-setup.md` | Minimal setup guide for turning the workspace into Open WebUI Knowledge and agents. |

Existing folders such as `agents/`, `build-system/`, `evals/`, `knowledge/`, `loops/`, and `workflow-templates/` are supporting material from the broader cockpit setup. Use them when helpful; do not let them replace the lean client source of truth above.

## Evidence Labels

Use these labels everywhere:

| Label | Meaning |
| --- | --- |
| `Confirmed` | Direct source evidence supports the claim. |
| `Confirmed mismatch` | Source evidence contradicts a claim, assumption, doc, or stakeholder statement. |
| `Unknown` | Evidence is missing or insufficient. |
| `Inferred` | Evidence suggests the claim, but it is not production truth. |
| `Recommendation` | Proposed next action based on confirmed facts and stated assumptions. |

## Agentic Loop Mode

Use `agents/loop-engineering-workstation-agent.md` as the primary Open WebUI control agent. It should keep one `board.md` card active, route work through `workflows/`, update the owning client files, and promote durable context to `llm-wiki/`.

## Daily Use

1. Start in `workbench.md` and `llm-wiki/current-client.md`.
2. Check `board.md` and move or create one card for the session outcome.
3. Open the client folder and update `context.md`, `systems.md`, and `open-questions.md`.
4. Check `tools/tool-registry.md` and `governance/approval-gates.md` before using tools or planning writes.
5. Investigate systems using `workflows/investigate.md`.
6. Capture flows in `workflow-inventory.md`, `endpoint-matrix.md`, `field-mapping.md`, and `workflows/registry.md`.
7. Use `architecture/_template/` when the flow needs boundaries, risks, or an ADR.
8. Use `research/_template/` when external tool or repo research needs an audit trail.
9. Generate build handoffs in `build-handoff.md`.
10. Validate with fake/redacted payloads and `evals/gtm-loop-evals.md`.
11. Log meaningful work in `runs/index.md`.
12. Update the relevant `llm-wiki/` pages before ending the session.

## Safety Rules

- Do not store secrets, tokens, endpoint hosts, tenant IDs, auth headers, or copied logs.
- Record setting names and ownership only.
- Treat Gong transcripts, CRM records, sponsor data, sales strategy, and workflow payloads as sensitive.
- Use fake or redacted payloads for examples.
- Require human approval before CRM writes, external messages, email sends, production workflow activation, or commercial decisions.
- Keep Open WebUI as the cockpit, this folder as source of truth, and n8n/AirOps/custom code as execution surfaces.
