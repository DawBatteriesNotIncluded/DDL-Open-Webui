# Solve Issue Workflow

Use when something is broken, unclear, failing, mismatched, or producing bad output.

## Intake

| Field | Notes |
| --- | --- |
| Symptom | What is happening? |
| Expected behavior | What should happen? |
| Impact | Who or what is affected? |
| Systems | HubSpot / Gong / AirOps / n8n / custom API / repo / other |
| Last known good | Date, version, workflow, or unknown |
| Evidence available | Logs, payloads, screenshots, workflow run, source path, owner statement |

## Steps

1. Create or update one `board.md` card under `Investigating`.
2. Read the active client folder and relevant system file.
3. Capture confirmed facts before proposing a fix.
4. Classify the issue:
   - prompt;
   - data;
   - API;
   - auth;
   - schema;
   - mapping;
   - rate limit;
   - environment/config;
   - workflow logic;
   - architecture;
   - unknown.
5. Identify the smallest safe reproduction using fake/redacted data.
6. Decide whether the fix is:
   - documentation/context update;
   - workflow design change;
   - n8n/AirOps change;
   - code change for Codex;
   - owner/access question.
7. Update the owning client file.
8. Create or update `build-handoff.md` when implementation is needed.
9. Record validation in `validation-notes.md`.
10. Move the board card to `Validating`, `Blocked`, or `Done`.

## Output

```markdown
# Issue: <name>

## Symptom

## Impact

## Confirmed

## Confirmed Mismatch

## Unknowns

## Likely Root Cause
Mark as `Inferred` unless directly proven.

## Smallest Safe Fix

## Build Handoff Needed
Yes / No

## Validation

## Next Action
```

## Done Means

- Root cause is confirmed or clearly labeled as inferred.
- A fix, handoff, or owner question exists.
- Validation notes are updated or blocker is recorded.
- Board card reflects current stage.
