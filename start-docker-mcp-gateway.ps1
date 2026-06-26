$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$envPath = Join-Path $repoRoot ".env"
$logPath = Join-Path $repoRoot "docker-mcp-gateway.log"

if (-not (Test-Path $envPath)) {
    throw ".env not found at $envPath"
}

$tokenLine = Get-Content $envPath | Where-Object { $_ -match "^MCP_GATEWAY_AUTH_TOKEN=" } | Select-Object -First 1
if (-not $tokenLine) {
    throw "MCP_GATEWAY_AUTH_TOKEN is missing from .env"
}

$token = $tokenLine -replace "^MCP_GATEWAY_AUTH_TOKEN=", ""
if ([string]::IsNullOrWhiteSpace($token)) {
    throw "MCP_GATEWAY_AUTH_TOKEN is empty"
}

$listener = Get-NetTCPConnection -LocalPort 8811 -ErrorAction SilentlyContinue |
    Where-Object { $_.State -eq "Listen" } |
    Select-Object -First 1

if ($listener) {
    Write-Host "Docker MCP Gateway is already listening on port 8811."
    exit 0
}

$command = "`$env:MCP_GATEWAY_AUTH_TOKEN='$token'; docker mcp gateway run --transport streaming --port 8811 --servers playwright --servers n8n --long-lived *> '$logPath'"
$encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($command))

$psi = [System.Diagnostics.ProcessStartInfo]::new()
$psi.FileName = "$PSHOME\powershell.exe"
$psi.Arguments = "-NoProfile -ExecutionPolicy Bypass -EncodedCommand $encoded"
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true

$process = [System.Diagnostics.Process]::Start($psi)
Write-Host "Started Docker MCP Gateway on port 8811. PID=$($process.Id)"
Write-Host "Log: $logPath"
