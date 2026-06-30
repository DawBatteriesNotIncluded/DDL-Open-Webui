param(
    [string] $ApiKey = $env:OPENWEBUI_API_KEY,
    [string] $OpenWebUIUrl = "http://localhost:3000",
    [string] $BaseModelId = "gpt-5.4",
    [switch] $ForceUploadFiles
)

$ErrorActionPreference = "Stop"

$container = docker ps --filter "name=open-webui" --format "{{.Names}}" | Select-Object -First 1
if (-not $container) {
    throw "Could not find a running Docker container named open-webui. Check 'docker ps'."
}

Write-Host "Found Open WebUI container: $container"
Write-Host "Using Open WebUI URL: $OpenWebUIUrl"

$argsList = @(
    "-NoProfile",
    "-ExecutionPolicy",
    "Bypass",
    "-File",
    ".\gtm-loop-workspace\imports\setup-openwebui-workspace.ps1",
    "-OpenWebUIUrl",
    $OpenWebUIUrl,
    "-BaseModelId",
    $BaseModelId
)

if ($ApiKey) {
    $argsList += @("-ApiKey", $ApiKey)
}

if ($ForceUploadFiles) {
    $argsList += "-ForceUploadFiles"
}

& powershell @argsList

