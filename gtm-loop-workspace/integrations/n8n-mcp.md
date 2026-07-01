# n8n MCP Integration

Purpose: make the GTM Loop workbench aware of the local n8n MCP surface for future Cody/build-lane work, while keeping this pass draft-only and inspect-only.

## Current Local Runtime Status

Observed on `2026-07-01` from local Docker:

| Component | Observed status | Local surface |
| --- | --- | --- |
| `n8n` | Running, healthy | `http://localhost:5678` |
| `n8n-mcp` | Running, healthy | `http://localhost:3001` |
| Docker MCP gateway | Configured for Open WebUI | `http://host.docker.internal:8811/mcp` |
| Direct n8n MCP config | Present in repo | `MCPS/N8N.json` -> `http://host.docker.internal:3001/mcp` |
| Alternate direct config | Present in repo, not runtime-verified here | `tool-server-n8n-direct.json` -> `http://host.docker.internal:8812/mcp` |

This status proves local availability only. It does not grant permission to create, update, activate, or run production workflows.

## Operating Mode

`n8n MCP` is `available-local / draft-only / approval-gated`.

Use it as a Cody/build executor surface for planning and local draft artifacts only. Until the user explicitly approves a specific action, agents may prepare draft workflow specs, draft workflow JSON, fake payload tests, and local approval requests.

## Allowed Actions

- Inspect local container availability.
- Inspect n8n MCP availability when read-only access is configured and the user asks for it.
- Inspect existing workflow shape only when read-only and approved for that session.
- Generate local Markdown workflow draft artifacts under `artifacts/<task_id>/`.
- Prepare draft n8n workflow JSON as a local artifact.
- Validate draft logic against fake/redacted payloads.
- Prepare an approval request for any future live workflow action.

## Blocked Without Explicit Approval

- Activate, enable, disable, or retry any production workflow.
- Create or update a live workflow in production.
- Call a production webhook.
- Write HubSpot, Gong, AirOps, or custom API data.
- Use real credentials, tokens, auth headers, cookies, or tenant identifiers.
- Expose an external webhook.
- Schedule recurring production automation.
- Store real client data or raw logs in this workspace.

## Approval Gates

Before any live n8n action, prepare a local approval record under `tasks/_approvals/APP-####.json` that states:

- workflow name or draft id;
- environment;
- trigger type;
- expected effect;
- systems and data touched;
- exact credentials or credential names, with values omitted;
- fake payload validation result;
- rollback or disable plan.

If any approval scope is ambiguous, do not act. Keep the work in draft artifacts.

An approved approval record does not execute n8n work by itself. Future n8n MCP executor code must require a matching approved approval before create/update, activation, credential use, webhook exposure, production retry, or scheduled automation.

## Fake Payload Requirement

All n8n design and validation in this workbench must use fake or redacted payloads from `payloads/` or task-specific fake samples under `artifacts/<task_id>/`.

Do not paste real webhook bodies, CRM records, Gong transcript text, auth headers, tenant ids, or customer logs into task files, artifacts, Knowledge, or audit logs.

## Safe First Test

1. Confirm local containers are running with `docker ps`.
2. Open the task in `/gtm-loop/board`.
3. Move the task to Cody/build lane if needed.
4. Create or use build artifacts under `artifacts/<task_id>/build/`.
5. Draft `n8n-workflow-draft.md` from the template.
6. Validate only against fake payloads in `payloads/n8n/`.
7. Prepare an approval request before any real n8n write, trigger, activation, or webhook call.

## Readiness Checklist

- [ ] Task has an accepted Brody requirements artifact.
- [ ] Task has an Archy integration-flow artifact.
- [ ] Cody build-plan and tool-plan exist.
- [ ] Fake input and output payloads are linked.
- [ ] External writes are explicitly blocked in the draft.
- [ ] Approval boundary is written in the draft.
- [ ] Rollback or disable plan exists.
- [ ] Human approval request is prepared before any live n8n action.
