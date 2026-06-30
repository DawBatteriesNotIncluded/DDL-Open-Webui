---
name: gtm-loop-engineering
description: >
  Run the GTM Loop workspace as an agentic Forward Deployed AI Solutions
  Engineering cockpit: issue triage, client/system investigation, architecture
  notes, workflow design, build handoffs, validation, board updates, and
  llm-wiki maintenance.
---

# GTM Loop Engineering

Use this skill when work involves GTM/FDE loop engineering, client systems, HubSpot, Gong, AirOps, n8n, custom APIs, workflow debugging, architecture notes, or build handoffs inside `gtm-loop-workspace/`.

## Start

Read these first:

1. `gtm-loop-workspace/AGENTS.md`
2. `gtm-loop-workspace/README.md`
3. `gtm-loop-workspace/board.md`
4. `gtm-loop-workspace/llm-wiki/llm-index.md`
5. `gtm-loop-workspace/llm-wiki/current-client.md`

## Operating Loop

1. Create or update one card in `board.md`.
2. Identify the active client and owning client folder.
3. Classify the work:
   - issue/debugging;
   - investigation;
   - research;
   - architecture/design;
   - build handoff;
   - validation.
4. Use the matching workflow under `gtm-loop-workspace/workflows/`.
5. Record evidence as `Confirmed`, `Confirmed mismatch`, `Unknown`, `Inferred`, or `Recommendation`.
6. Update the narrowest owning file.
7. Promote only durable context into `llm-wiki/`.
8. Move the board card when the stage changes.

## Default Outputs

- Issue work: symptom, impact, evidence, likely root cause, fix/handoff, validation.
- Architecture work: system map, flow, boundaries, risks, ADR only if justified.
- Build work: objective, requirements, inputs, outputs, acceptance checks, evidence, unknowns.
- Validation work: fake/redacted payload, expected result, actual result, readiness, follow-up.

## Safety

- Do not write secrets, endpoint hosts, tenant IDs, auth headers, tokens, copied logs, or raw customer data.
- Record setting names only.
- Require explicit human approval before CRM writes, email sends, external messages, production workflow activation, credential changes, or data mutation.
- Use fake or redacted payloads for examples.

## Closeout

Before finishing:

- update `board.md`;
- update the client file that owns the facts;
- update `llm-wiki/current-client.md` if active state changed;
- update `llm-wiki/open-questions.md` for cross-client blockers;
- state validation run or skipped;
- state remaining unknowns.
