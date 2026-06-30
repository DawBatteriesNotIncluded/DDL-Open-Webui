# Docker Open WebUI Setup

Your Open WebUI Docker container is expected to expose the UI/API on the host at:

```text
http://localhost:3000
```

Confirmed local Docker shape:

```text
open-webui  ghcr.io/open-webui/open-webui:ddl-local  0.0.0.0:3000->8080/tcp
ollama      ollama/ollama:latest                     11434/tcp
```

Verified on `2026-06-30`:

- `http://localhost:3000/health` returns `{"status": true}`.
- `http://localhost:3000/` returns HTTP 200.
- `http://localhost:3000/gtm-loop` returns HTTP 200.
- Open WebUI uses the repo compose project `ddl-open-webui`.
- Data is stored in Docker volume `ddl-open-webui_open-webui`.
- No HubSpot, Gong, AirOps, n8n API, or OpenAI API credential value is required for local UI testing.

## Start, Stop, Restart

From repo root:

```powershell
docker compose ps
docker compose up -d
docker compose restart open-webui
docker compose stop open-webui
```

Do not run `docker compose down -v` unless you intentionally want to remove local data volumes.

## GTM Workspace Mount

For local development, `docker-compose.override.yaml` mounts:

```text
./gtm-loop-workspace -> /app/gtm-loop-workspace:ro
```

The mount is read-only from the container. Edits to `gtm-loop-workspace/tasks/*.md` on the host are reflected by `GET /api/gtm-loop/tasks` and `/gtm-loop/board` after refresh, without rebuilding the image.

The `Dockerfile` still copies `gtm-loop-workspace` into the image. If the override is not used, Open WebUI falls back to that packaged copy.

## GTM Board Smoke Test

1. Open `http://localhost:3000/gtm-loop` while logged in.
2. Open `http://localhost:3000/gtm-loop/board`.
3. Confirm the board status panel shows `API: loaded`, `Tasks: 11`, and `Source: bind-mounted/dev`.
4. Confirm the five columns render: Planned, In Progress, Smoke Test, In Review, and Done.
5. Make a harmless local edit to a task `next_action`.
6. Refresh the board and confirm the edited text appears without rebuilding.
7. Revert the test edit.
8. Run `node scripts\validate-gtm-tasks.js`.

If the board shows `unauthorized`, the browser is not logged in or the session token is missing. Refresh after logging in; do not disable auth for this test.

## Auth Options

Preferred UI path:

1. Open your user menu.
2. Go to Settings.
3. Find Account/API Keys, or the equivalent API key section in your version.
4. Create/copy an API key.

Do not save the key into repo files.

This local build currently has API-key auth disabled. For this setup only, use a short-lived local JWT minted inside the Docker container.

## Run Setup Against Docker Open WebUI

From repo root with an API key:

```powershell
$env:OPENWEBUI_API_KEY="PASTE_TOKEN_HERE"
powershell -NoProfile -ExecutionPolicy Bypass -File .\gtm-loop-workspace\imports\setup-openwebui-docker.ps1
```

From repo root with a short-lived local JWT:

```powershell
$token = Get-Content -Raw .\gtm-loop-workspace\imports\create-local-openwebui-jwt.py | docker exec -i open-webui python -
powershell -NoProfile -ExecutionPolicy Bypass -File .\gtm-loop-workspace\imports\setup-openwebui-docker.ps1 -ApiKey $token.Trim()
```

If your base model changes:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\gtm-loop-workspace\imports\setup-openwebui-docker.ps1 -BaseModelId "gpt-5.4"
```

## What This Does

- Calls the Open WebUI API at `http://localhost:3000/api/v1`.
- Imports the GTM agent models.
- Creates/reuses Knowledge collections.
- Uploads Markdown files into Knowledge.
- Attaches Knowledge collections to the imported agent models.

## What This Does Not Do

- It does not modify Docker images.
- It does not edit Open WebUI source code.
- It does not write secrets to files.
- It does not activate n8n workflows.
- It does not send email or modify CRM data.

## If It Fails

- Confirm container is running: `docker ps`.
- Confirm UI loads at `http://localhost:3000`.
- Confirm the API key is valid.
- Confirm your user can import Workspace Models and create Knowledge.
- If model ID collision occurs, generate a new import file with different IDs.
