$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$envPath = Join-Path $repoRoot ".env"

if (-not (Test-Path $envPath)) {
    throw ".env not found at $envPath"
}

$envLines = Get-Content $envPath
$token = ($envLines | Where-Object { $_ -match "^N8N_MCP_AUTH_TOKEN=" } | Select-Object -First 1) -replace "^N8N_MCP_AUTH_TOKEN=", ""

if ([string]::IsNullOrWhiteSpace($token)) {
    throw "N8N_MCP_AUTH_TOKEN is missing or empty in .env"
}

$existing = docker ps -a --filter "name=^n8n-mcp-direct$" --format "{{.Names}}"
if ($existing -eq "n8n-mcp-direct") {
    $running = docker ps --filter "name=^n8n-mcp-direct$" --format "{{.Names}}"
    if ($running -eq "n8n-mcp-direct") {
        Write-Host "n8n direct MCP is already running on port 8812."
        exit 0
    }

    docker start n8n-mcp-direct | Out-Null
    Write-Host "Started existing n8n direct MCP container on port 8812."
    exit 0
}

docker run -d `
    --name n8n-mcp-direct `
    --restart unless-stopped `
    -p 8812:3000 `
    -e AUTH_TOKEN="$token" `
    -e N8N_API_URL="https://n8n.acacium.com/" `
    -e N8N_API_KEY="se://docker/mcp/n8n.api_key" `
    mcp/n8n n8n-mcp serve --host=0.0.0.0 --port=3000 | Out-Null

Write-Host "Started n8n direct MCP on http://localhost:8812/mcp"
