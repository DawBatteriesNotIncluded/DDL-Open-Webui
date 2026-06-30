# Shared Context

Stable operating context for GTM Loop agents.

## Mission

Turn messy client system knowledge into buildable, testable GTM automation work without losing evidence, ownership, or risk.

## Default Flow

1. Start with client context.
2. Investigate systems and integrations.
3. Capture confirmed facts, mismatches, unknowns, and evidence.
4. Map fields, endpoints, workflows, configuration, and owners.
5. Research external tools or repos only when needed.
6. Produce architecture notes when boundaries or risks matter.
7. Create Codex, n8n, AirOps, or human build handoffs.
8. Validate with fake/redacted payloads.
9. Update `llm-wiki/`.

## Roles

| Role | Responsibility |
| --- | --- |
| Open WebUI | Daily cockpit, reasoning, review, prompts, and knowledge access. |
| Codex | Local file edits, code/repo inspection, build handoff execution when requested. |
| n8n | Workflow runtime, API orchestration, scheduled/background execution. |
| AirOps | Content/prompt-chain workflows and GTM generation pipelines. |
| Human owner | Scope, approval, production activation, customer decisions, and risk acceptance. |

## Evidence Preference

1. Production workflow definitions, source code, API docs, admin exports, and system configuration screens.
2. Current client documentation and owner statements.
3. Tests, sample payloads, and recorded runs.
4. Generated clients, local settings, and examples as supporting evidence only.
