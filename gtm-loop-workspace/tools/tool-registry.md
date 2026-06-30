# Tool Registry

Registry of tools this workbench may reason about or use when connected. This file records scope and safety, not secrets.

## Registry

| Tool | Purpose | Access Level | Allowed Actions | Blocked Without Approval | Owner | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Open WebUI Knowledge | Agent context and retrieval | Read | Retrieve workspace docs | Upload sensitive client data | User | Planned | `openwebui-setup.md` |
| Codex | Repo/file edits and validation | Read/write in repo | Edit workspace docs, inspect repo, run safe checks | External writes, destructive commands, secret handling | User | Available | Current session |
| n8n MCP/API | Workflow inspection and runtime control | Unknown | Inspect workflows, draft changes, validate exports | Activate workflows, retry production runs, edit credentials | `TBD` | Unknown | `TBD` |
| HubSpot API | CRM records and metadata | Unknown | Read schema/metadata when approved | Create/update/delete CRM records, tasks, notes, associations | `TBD` | Unknown | `TBD` |
| Gong API/export | Calls, transcripts, trackers | Unknown | Read metadata/summaries when approved | Store raw transcripts, expose participant/customer data | `TBD` | Unknown | `TBD` |
| AirOps | Prompt/content workflows | Unknown | Inspect workflow shape, draft prompt chains | Publish or run customer-facing content at scale | `TBD` | Unknown | `TBD` |
| Custom APIs | Client/internal actions | Unknown | Read docs, inspect schemas, dry-run with fake data | Mutate production data, use live secrets | `TBD` | Unknown | `TBD` |
| Docker/containers | Local services and test harnesses | Unknown | Inspect local status/logs when safe | Delete volumes, rebuild production-like services, expose secrets | User | Unknown | `TBD` |

## Access Levels

- `None`: not connected.
- `Read`: can inspect only.
- `Draft`: can generate changes but not apply externally.
- `Write-approved`: can write after explicit approval for exact action.
- `Admin`: avoid for agents unless the user explicitly scopes it.

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
