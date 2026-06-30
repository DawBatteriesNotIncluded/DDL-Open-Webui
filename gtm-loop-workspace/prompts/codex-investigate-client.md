# Codex Investigate Client Prompt

```text
You are investigating a client system for GTM/FDE automation.

Read:
- gtm-loop-workspace/AGENTS.md
- gtm-loop-workspace/llm-wiki/current-client.md
- clients/<client-slug>/context.md
- clients/<client-slug>/systems.md
- clients/<client-slug>/open-questions.md

Investigate:
<system, workflow, repo, API, or question>

Output/update:
- Confirmed facts with evidence.
- Confirmed mismatches with impact.
- Unknowns with next evidence needed.
- Endpoint, field, config, or workflow tables if relevant.
- Build handoff seed if implementation work is now clear.

Safety:
- No secrets, hosts, tenant IDs, tokens, auth headers, copied logs, or raw customer records.
```
