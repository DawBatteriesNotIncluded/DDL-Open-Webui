# Automation Backlog Loop

Continuously identify which manual GTM work should be automated next.

## Loop Name

Automation Backlog Loop

## Business Goal

Prioritise repeatable manual work by impact, frequency, complexity, risk, and build readiness so automation effort targets the highest-value loops.

## Trigger

User describes a repeated manual task, weekly backlog review, failure pattern, or observed operational bottleneck.

## Inputs

- Manual task description.
- Frequency, time spent, business impact, systems involved.
- Risk and sensitivity notes.

## Context Sources

- Open WebUI Knowledge: build-system docs, loop spec template, evals.
- Existing backlog.
- Workflow debugging notes and prior failures.

## Tools Required

- Open WebUI for analysis.
- Codex for backlog file updates.
- Optional n8n inspection for existing workflows.

## Step-By-Step Loop Design

1. Capture manual task.
2. Clarify outcome, frequency, owner, systems, and pain.
3. Classify automation type: signal, CRM, content, debug, prep, proposal, reporting, or integration.
4. Estimate impact, effort, risk, and data sensitivity.
5. Create automation spec or loop spec stub.
6. Score ROI and readiness.
7. Add to backlog with owner and next action.
8. Re-rank backlog periodically.

## n8n Implementation Outline

Manual form/chat trigger -> Task classifier -> ROI scorer -> Backlog item creator -> Optional approval -> Versioned backlog update.

## Prompt Blocks

Backlog scorer: "Classify this manual task by frequency, time saved, revenue impact, complexity, risk, and build readiness. Recommend build now, prototype, defer, or ignore."

## Data Mappings

| Source | Target | Notes |
|---|---|---|
| Manual task | Backlog idea | Preserve raw wording |
| Frequency/time | ROI score | Estimate if missing |
| Systems | Build complexity | Note missing access |
| Sensitivity | Risk score | Approval needed |

## State/Logging Requirements

Log idea, owner, score, status, risks, next action, date added, date reviewed, and ready-to-activate flag.

## Evaluation Checks

- Is the task actually repeated?
- Is automation safer than a checklist?
- Is data access available?
- Is v1 simple enough?
- Is business value measurable?

## Human Approval Gates

Approval required before moving from backlog to build when workflow writes to CRM, sends externally, or uses sensitive data.

## Stop Condition

Stop when backlog item is created, rejected, merged with duplicate, or moved into build control.

## Error Handling

If value is unclear, mark as discovery. If system access is missing, add prerequisite. If risk is high, require eval before build.

## Test Payload

Use a fake manual-task prompt: "Every Friday I spend 45 minutes checking Gong calls for competitor mentions and writing a summary."

## Success Metrics

Backlog quality, build conversion rate, time saved estimate accuracy, and number of low-value automations avoided.

## Build Now Vs Later Recommendation

Build now as a Markdown backlog and Open WebUI workflow. Automate intake later if volume increases.

