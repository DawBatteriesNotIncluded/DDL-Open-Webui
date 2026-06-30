# Loop To n8n Build Pipeline

## Pipeline

1. Start with approved loop spec.
2. Identify runtime trigger: webhook, schedule, manual trigger, CRM event, Gong event, or error trigger.
3. Define input schema and fake payload.
4. Add validation and normalization step.
5. Add enrichment reads with least-privilege credentials.
6. Add AI/planner step only where reasoning is required.
7. Add deterministic decision branches where possible.
8. Add approval queue before external side effects.
9. Add write/action node only after approval.
10. Add logging and idempotency.
11. Add error branch with safe retry rules.
12. Test with fake payloads.
13. Document import and activation checklist.

## Placement Rules

- n8n: triggers, integrations, retries, scheduled runs, stateful runtime.
- Open WebUI: reasoning, debugging, supervision, review.
- AirOps: reusable content/prompt-chain production.
- Codex: versioned files, specs, scripts, payloads.
- MCP/OpenAPI: controlled reads/writes with approval.

