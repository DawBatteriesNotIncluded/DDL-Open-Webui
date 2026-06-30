# GTM Loop Board

Plain Markdown Kanban board for client investigations, research, designs, builds, validations, and follow-ups.

Move cards between sections. Keep each card linked to the source file that owns the real detail.

## Backlog

- [ ] Review HOME dashboard at start of day
  - Type: daily control
  - Link: `HOME.md`
  - Next: set active client, active card, and next action

- [ ] Fill workbench manifest for first real client
  - Type: workbench setup
  - Link: `workbench.md`
  - Next: set active client, stage, and active board card

- [ ] Configure Loop Engineering Workstation Agent in Open WebUI
  - Type: agent setup
  - Link: `openwebui-setup.md`
  - Next: create custom model and attach workspace Knowledge

- [ ] Define initial tool registry and approval gates
  - Type: governance
  - Link: `tools/tool-registry.md`
  - Next: mark n8n, HubSpot, Gong, AirOps, and API access levels

- [ ] Create first real client folder from `clients/_template/`
  - Type: client setup
  - Link: `clients/_template/README.md`
  - Next: choose client slug and fill `context.md`

- [ ] Pick first automation candidate
  - Type: discovery
  - Link: `llm-wiki/current-client.md`
  - Next: capture objective, systems, and owner

## Investigating

- [ ] Confirm active client systems
  - Type: investigation
  - Link: `clients/_template/systems.md`
  - Evidence target: HubSpot, Gong, AirOps, n8n, custom APIs, repos

- [ ] Run first issue through Solve Issue workflow
  - Type: issue
  - Link: `workflows/solve-issue.md`
  - Next: capture symptom, impact, evidence, and likely owner

## Designing

- [ ] Draft first workflow inventory row
  - Type: design
  - Link: `clients/_template/workflow-inventory.md`
  - Next: define trigger, inputs, outputs, runtime, owner

- [ ] Add first automation to workflow registry
  - Type: registry
  - Link: `workflows/registry.md`
  - Next: record runtime, trigger, status, owner, approval gate

- [ ] Create first architecture-to-build pack
  - Type: architecture
  - Link: `workflows/architecture-to-build.md`
  - Next: map systems, boundaries, flow, risks, and handoff

## Building

- [ ] Prepare first build handoff
  - Type: build handoff
  - Link: `clients/_template/build-handoff.md`
  - Next: add confirmed requirements and acceptance checks

## Validating

- [ ] Create fake/redacted validation payload
  - Type: validation
  - Link: `payloads/README.md`
  - Next: record expected output and approval gate

- [ ] Run GTM loop evals on first workflow
  - Type: eval
  - Link: `evals/gtm-loop-evals.md`
  - Next: check grounding, safety, build readiness, validation

## Blocked

- [ ] Confirm which client is active
  - Type: owner question
  - Link: `llm-wiki/current-client.md`
  - Blocker: client name and initial objective needed

## Done

- [x] Create lean GTM Loop Markdown workspace
  - Type: workspace setup
  - Link: `README.md`

## Card Rules

- One card equals one outcome.
- Link to the owning file instead of duplicating detail.
- Use `Blocked` only when the next action needs access, owner input, or a decision.
- Move finished cards to `Done`; keep the proof in the linked file.
