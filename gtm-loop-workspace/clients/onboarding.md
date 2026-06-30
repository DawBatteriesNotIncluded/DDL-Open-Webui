# First Client Onboarding

Use this checklist to create the first real client workspace.

## 1. Create The Folder

- [ ] Choose a short client slug.
- [ ] Copy `clients/_template/` to `clients/<client-slug>/`.
- [ ] Keep the template folder unchanged.

## 2. Fill Minimum Context

- [ ] Fill `clients/<client-slug>/context.md`.
- [ ] Fill `clients/<client-slug>/systems.md`.
- [ ] Fill `clients/<client-slug>/open-questions.md`.
- [ ] Set current phase: Discovery / Investigation / Design / Build / Validate / Operate.

## 3. Fill Tool-Specific Notes

- [ ] Fill `hubspot.md` if HubSpot is in scope.
- [ ] Fill `gong.md` if Gong is in scope.
- [ ] Fill `airops.md` if AirOps is in scope.
- [ ] Fill `n8n.md` if n8n is in scope.
- [ ] Add source/repo/API notes to `systems.md` and `endpoint-matrix.md`.

## 4. Map Data And Workflows

- [ ] Fill `field-mapping.md` with source and target field names.
- [ ] Fill `workflow-inventory.md` with live, proposed, paused, and unknown workflows.
- [ ] Fill `endpoint-matrix.md` with routes/triggers and auth model, values omitted.
- [ ] Fill `configuration-inventory.md` with setting names only.

## 5. Update Global Control Files

- [ ] Update `llm-wiki/current-client.md`.
- [ ] Update `workbench.md`.
- [ ] Add or move one card in `board.md`.
- [ ] Add cross-client automation rows to `workflows/registry.md` only when useful.
- [ ] Log onboarding in `runs/index.md`.

## 6. Prepare First Build Candidate

- [ ] Pick one small workflow or issue.
- [ ] Create fake/redacted payloads under `payloads/`.
- [ ] Fill `build-handoff.md`.
- [ ] Fill `validation-notes.md`.
- [ ] Run `evals/gtm-loop-evals.md` manually.

## Done Means

- Future agents can identify the active client.
- The first workflow candidate has a clear owner, evidence, and next action.
- No secrets, raw transcripts, endpoint hosts, tenant IDs, auth headers, copied logs, or real customer records were stored.
