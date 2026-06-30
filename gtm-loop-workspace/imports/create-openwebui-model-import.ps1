param(
    [Parameter(Mandatory = $true)]
    [string] $BaseModelId,

    [string] $TemplatePath = ".\gtm-loop-workspace\imports\openwebui-models-import.json",
    [string] $OutputPath = ".\gtm-loop-workspace\imports\openwebui-models-import.generated.json"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $TemplatePath)) {
    throw "Template not found: $TemplatePath"
}

$content = Get-Content -Raw -LiteralPath $TemplatePath
$content = $content.Replace("__BASE_MODEL_ID__", $BaseModelId)

$null = $content | ConvertFrom-Json
$content | Set-Content -LiteralPath $OutputPath -Encoding UTF8

Write-Host "Wrote $OutputPath using base model: $BaseModelId"

