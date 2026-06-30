# Tool Registry

Registry of tools this workbench may reason about or use when connected. This file records scope and safety, not secrets.

This file owns tool access status, permission level, safe reads, blocked actions, and evidence. It does not own active work status.

## Registry

| Tool | Purpose | Access Level | Allowed Actions | Blocked Without Approval | Owner | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Open WebUI Knowledge | Agent context and retrieval | Read | Retrieve workspace docs | Upload sensitive client data | User | Ready | `openwebui-setup.md`, `imports/openwebui-workspace-manifest.json` |
| Open WebUI GTM Loop UI | Daily in-app cockpit surface | Read | View status, links, starter prompt, and safety gates | Execute external actions or mutate client systems | User | Ready | `src/routes/(app)/gtm-loop/+page.svelte` |
| Codex | Repo/file edits and validation | Read/write in repo | Edit workspace docs, inspect repo, run safe checks | External writes, destructive commands, secret handling | User | Available | Current session |
| codebase-memory-mcp | Repo code discovery and impact analysis | Read | Search graph, trace paths, inspect snippets, query indexed architecture | Mutate source, infer production truth from code alone | User | Available | `AGENTS.md` |
| Board MCP | Future structured board read/update adapter | None | None for v1; use `board.md` directly | Updating cards outside `board.md` contract | `TBD` | Deferred | `orchestrator/agent-routing.md` |
| n8n MCP/API | Workflow inspection and runtime control | Unknown | Inspect workflows, draft changes, validate exports | Activate workflows, retry production runs, edit credentials | `TBD` | Unknown | `TBD` |
| HubSpot API | CRM records and metadata | Unknown | Read schema/metadata when approved | Create/update/delete CRM records, tasks, notes, associations | `TBD` | Unknown | `TBD` |
| Gong API/export | Calls, transcripts, trackers | Unknown | Read metadata/summaries when approved | Store raw transcripts, expose participant/customer data | `TBD` | Unknown | `TBD` |
| AirOps | Prompt/content workflows | Unknown | Inspect workflow shape, draft prompt chains | Publish or run customer-facing content at scale | `TBD` | Unknown | `TBD` |
| Custom APIs | Client/internal actions | Unknown | Read docs, inspect schemas, dry-run with fake data | Mutate production data, use live secrets | `TBD` | Unknown | `TBD` |
| Docker/containers | Local services and test harnesses | Read | Inspect local status/logs, verify health, use existing compose runtime | Delete volumes, rebuild/recreate containers, expose secrets, connect production services | User | Ready | `docker-compose.yaml`, `gtm-loop-workspace/docs/docker-openwebui-setup.md`, `RUN-0004` |
| GitHub MCP | Future issue/PR/release coordination | None | None for v1 | Create PRs, merge, change repo settings, publish releases | `TBD` | Deferred | `orchestrator/agent-routing.md` |
| Hermes | Future external message/send surface | None | None for v1 | Send messages or customer-facing communications | `TBD` | Deferred | `orchestrator/agent-routing.md` |
| OpenHands | Future implementation executor | None | None for v1 | Execute builds without board handoff and verifier gate | `TBD` | Deferred | `orchestrator/agent-routing.md` |

## Access Levels

- `None`: not connected.
- `Read`: can inspect only.
- `Draft`: can generate changes but not apply externally.
- `Write-approved`: can write after explicit approval for exact action.
- `Admin`: avoid for agents unless the user explicitly scopes it.

## Safe Default

All unconfirmed tools are treated as `None` or read-only planning surfaces. Agents may draft requests and payloads, but must not execute writes, activation, credential changes, or destructive actions.

## Tool Card Template

| Field | Value |
| --- | --- |
| Tool | `TBD` |
| Purpose | `TBD` |
| Access level | None / Read / Draft / Write-approved / Admin |
| Credential name | `TBD`, value omitted |
| Safe reads | `TBD` |
| Safe writes | `TBD` |
| Approval required | `TBD` |
| Owner | `TBD` |
| Evidence | `TBD` |
