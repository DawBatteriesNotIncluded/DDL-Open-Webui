# Imports

This folder contains portable import/setup files for using the GTM Loop Workspace in Open WebUI.

## Files

- `openwebui-workstation-agent.gpt-5.4.json`: ready-to-import Workstation Agent for the hardened v1 workbench.
- `openwebui-workstation-agent.import.json`: Workstation Agent import template. Replace `__BASE_MODEL_ID__` before importing if not using `gpt-5.4`.
- `openwebui-models-import.json`: model import template for Open WebUI. Replace `__BASE_MODEL_ID__` before importing.
- `openwebui-models-import.gpt-5.4.json`: ready-to-import file based on the local dummy export you provided.
- `openwebui-models-import.gpt-5.4.unique.json`: collision-safe ready-to-import file with `gtm-loop-v1-*` model IDs.
- `create-openwebui-model-import.ps1`: helper that creates `openwebui-models-import.generated.json` with your real base model ID.
- `setup-openwebui-workspace.ps1`: API-based setup script that imports models, creates Knowledge collections, uploads workspace Markdown, and attaches Knowledge to the imported models.
- `setup-openwebui-docker.ps1`: Docker-aware wrapper for local Open WebUI exposed at `http://localhost:3000`.
- `create-local-openwebui-jwt.py`: container-side helper for minting a short-lived local JWT when API-key auth is disabled.
- `openwebui-workspace-manifest.json`: source-of-truth manifest for the full workspace, including Knowledge uploads, tool recommendations, test prompts, and file groups.

## Recommended For This Machine

Use the Workstation Agent first:

```text
gtm-loop-workspace/imports/openwebui-workstation-agent.gpt-5.4.json
```

Attach the `GTM Workbench Core Pack` Knowledge collection from `openwebui-workspace-manifest.json`.

Use this specialist bundle later only when needed:

```text
gtm-loop-workspace/imports/openwebui-models-import.gpt-5.4.unique.json
```

The specialist bundle matches the dummy export shape you provided:

- `base_model_id`: `gpt-5.4`
- n8n MCP tool ID: `server:mcp:n8n-mcp`
- model capabilities include file context, web search, code interpreter, terminal, citations, status updates, and builtin tools.
- model IDs use the collision-safe `gtm-loop-v1-*` pattern.

## Why The Base Model Is Required

Open WebUI Workspace Models are wrappers around an existing model connection. The import file must point each custom model at a real `base_model_id` from your instance, such as an Ollama, OpenAI-compatible, LiteLLM, or other configured model ID.

The placeholder `__BASE_MODEL_ID__` will not work until replaced.

## Create The Real Import File

From repo root, run:

```powershell
.\gtm-loop-workspace\imports\create-openwebui-model-import.ps1 -BaseModelId "YOUR_EXISTING_BASE_MODEL_ID"
```

If Windows blocks `.ps1` execution, use:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\gtm-loop-workspace\imports\create-openwebui-model-import.ps1 -BaseModelId "YOUR_EXISTING_BASE_MODEL_ID"
```

Example:

```powershell
.\gtm-loop-workspace\imports\create-openwebui-model-import.ps1 -BaseModelId "gpt-4.1"
```

This writes:

```text
gtm-loop-workspace/imports/openwebui-models-import.generated.json
```

Import the generated file, not the template.

## How To Import Models

1. Open Open WebUI.
2. Go to Workspace -> Models or Admin Settings -> Models, depending on your permissions/UI.
3. Click Import.
4. Select `gtm-loop-workspace/imports/openwebui-models-import.gpt-5.4.unique.json`, or select `openwebui-models-import.generated.json` if you generated one with a different base model.
5. After import, open each model and confirm the base model, system prompt, prompt suggestions, and capabilities.
6. Upload Knowledge files first, then attach the relevant Knowledge collections to each model.
7. Enable n8n MCP only for the recommended agents and only after confirming permissions.

## One-Command API Setup

This is the closest option to "just work" without editing Open WebUI internals. It uses the supported API and requires an Open WebUI API key/token.

For your Docker setup with a normal Open WebUI token/API key, use:

```powershell
$env:OPENWEBUI_API_KEY="PASTE_TOKEN_HERE"
powershell -NoProfile -ExecutionPolicy Bypass -File .\gtm-loop-workspace\imports\setup-openwebui-docker.ps1
```

The wrapper targets `http://localhost:3000`, matching the local `open-webui` Docker container.

If API-key auth is disabled, mint a short-lived local JWT from inside the container and use it for this setup run:

```powershell
$token = Get-Content -Raw .\gtm-loop-workspace\imports\create-local-openwebui-jwt.py | docker exec -i open-webui python -
powershell -NoProfile -ExecutionPolicy Bypass -File .\gtm-loop-workspace\imports\setup-openwebui-docker.ps1 -ApiKey $token.Trim()
```

This JWT expires after 2 hours and is not written to repo files.

Generic API setup:

```powershell
$env:OPENWEBUI_URL="http://localhost:3000"
$env:OPENWEBUI_API_KEY="PASTE_TOKEN_HERE"
powershell -NoProfile -ExecutionPolicy Bypass -File .\gtm-loop-workspace\imports\setup-openwebui-workspace.ps1
```

Optional parameters:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\gtm-loop-workspace\imports\setup-openwebui-workspace.ps1 -BaseModelId "gpt-5.4"
```

To import the older specialist-agent bundle instead:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\gtm-loop-workspace\imports\setup-openwebui-workspace.ps1 -ImportFile ".\gtm-loop-workspace\imports\openwebui-models-import.gpt-5.4.unique.json"
```

Use `-ForceUploadFiles` if you want to re-upload files even when matching file names are already in the target Knowledge collection.

The script will:

- Import the Workstation Agent by default.
- Create/reuse Knowledge collections from `openwebui-workspace-manifest.json`.
- Upload Markdown files into those Knowledge collections.
- Attach the GTM Workbench Core Pack to the Workstation Agent.

The script will not:

- Activate n8n workflows.
- Send emails.
- Modify CRM records.
- Store secrets in repo files.

## Important Limitation

Knowledge attachments and external tool IDs are not included in `openwebui-models-import.json` because Open WebUI stores Knowledge and tool references using instance-specific IDs after upload/registration. Use `openwebui-workspace-manifest.json` as the attachment plan.

## If Import Still Fails

- Confirm your user has permission to import Workspace Models.
- Confirm the file you imported is valid JSON and is a raw array of model objects.
- Confirm `__BASE_MODEL_ID__` is not present in the generated file.
- Confirm the base model ID exactly matches an existing model ID shown in Open WebUI.
- If Open WebUI says a model ID is already registered, create a new import file with different `id` values or use the provided `openwebui-models-import.gpt-5.4.unique.json`.
- Try importing one model at a time by copying one object from the generated array into a temporary JSON array.
