# Scripts

Small standard-library utilities for maintaining the workspace.

## validate-json-payloads.py

Validates every `.json` file under `gtm-loop-workspace/payloads`.

Run from repo root:

```bash
python gtm-loop-workspace/scripts/validate-json-payloads.py
```

## generate-loop-index.py

Scans `gtm-loop-workspace/loops` and writes `gtm-loop-workspace/loops/INDEX.md` with loop names and first-paragraph summaries.

Run from repo root:

```bash
python gtm-loop-workspace/scripts/generate-loop-index.py
```
