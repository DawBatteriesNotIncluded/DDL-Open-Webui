# Current Setup Audit

## Confirmed

- Open WebUI repository is present.
- Workspace branch: `gtm-loop-workspace-v1`.
- Personal workspace folder is isolated under `gtm-loop-workspace`.
- No Open WebUI core files are required for this v1.

## Assumed

- Open WebUI is already running or can be started by the user.
- n8n MCP is partially configured.
- HubSpot, Gong, Evergrowth, and AirOps access may vary by environment.

## Gaps To Verify

- Which Open WebUI version and MCP tool attachment method is active.
- Whether n8n MCP exposes read-only, create, update, and activation operations.
- Which credentials exist in n8n credential store.
- Whether HubSpot/Gong/Evergrowth API scopes are available.
- Where workflow logs should be stored.

