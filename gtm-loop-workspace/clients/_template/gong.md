# Gong

## Scope

| Data | Use | Status | Evidence |
| --- | --- | --- | --- |
| Call metadata | Matching, routing, reporting | Unknown | `TBD` |
| Transcripts | Signal extraction and summaries | Unknown | `TBD` |
| Trackers / topics | Trigger or scoring input | Unknown | `TBD` |
| Deal context | Briefing or enrichment | Unknown | `TBD` |

## Sensitivity Rules

- Treat transcripts, participants, deal content, and coaching notes as sensitive.
- Store summaries and evidence references, not raw transcript dumps.
- Redact customer, prospect, and commercial details in examples.

## Signals

| Signal | Source | Consumer | Transform | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| `TBD` | Transcript / tracker / score | HubSpot / AirOps / n8n | `TBD` | Unknown | `TBD` |

## Unknowns

- Which Gong API/export access is available?
- Which calls or trackers are in scope?
- What is the approved retention model for extracted signals?
