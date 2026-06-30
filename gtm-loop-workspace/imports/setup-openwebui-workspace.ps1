param(
    [string] $OpenWebUIUrl = $env:OPENWEBUI_URL,
    [string] $ApiKey = $env:OPENWEBUI_API_KEY,
    [string] $BaseModelId = "gpt-5.4",
    [string] $WorkspaceRoot = ".\gtm-loop-workspace",
    [string] $ImportFile = ".\gtm-loop-workspace\imports\openwebui-workstation-agent.gpt-5.4.json",
    [string[]] $KnowledgeGroupNames = @("GTM Workbench Core Pack"),
    [switch] $SkipModels,
    [switch] $SkipKnowledge,
    [switch] $SkipModelKnowledgeAttach,
    [switch] $ForceUploadFiles
)

$ErrorActionPreference = "Stop"

function Fail($Message) {
    throw "[gtm-loop-setup] $Message"
}

function Get-ApiBase($Url) {
    if ([string]::IsNullOrWhiteSpace($Url)) {
        Fail "OpenWebUIUrl is required. Set OPENWEBUI_URL or pass -OpenWebUIUrl."
    }
    $trimmed = $Url.TrimEnd("/")
    if ($trimmed.EndsWith("/api/v1")) {
        return $trimmed
    }
    return "$trimmed/api/v1"
}

function Invoke-OpenWebUIJson {
    param(
        [Parameter(Mandatory = $true)][string] $Method,
        [Parameter(Mandatory = $true)][string] $Path,
        [object] $Body = $null
    )

    $uri = "$script:ApiBase$Path"
    $headers = @{
        authorization = "Bearer $script:Token"
        Accept = "application/json"
    }

    if ($null -eq $Body) {
        return Invoke-RestMethod -Method $Method -Uri $uri -Headers $headers
    }

    $json = $Body | ConvertTo-Json -Depth 100
    return Invoke-RestMethod -Method $Method -Uri $uri -Headers $headers -ContentType "application/json" -Body $json
}

function Upload-OpenWebUIFile {
    param(
        [Parameter(Mandatory = $true)][string] $Path,
        [Parameter(Mandatory = $true)][string] $RelativePath
    )

    Add-Type -AssemblyName System.Net.Http

    $client = [System.Net.Http.HttpClient]::new()
    $client.DefaultRequestHeaders.Authorization = [System.Net.Http.Headers.AuthenticationHeaderValue]::new("Bearer", $script:Token)
    $client.DefaultRequestHeaders.Accept.ParseAdd("application/json")

    $form = [System.Net.Http.MultipartFormDataContent]::new()
    $stream = [System.IO.File]::OpenRead((Resolve-Path -LiteralPath $Path))
    $fileContent = [System.Net.Http.StreamContent]::new($stream)
    $fileContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse("text/markdown")
    $form.Add($fileContent, "file", [System.IO.Path]::GetFileName($Path))

    $metadata = @{ name = $RelativePath; source = "gtm-loop-workspace" } | ConvertTo-Json -Compress
    $form.Add([System.Net.Http.StringContent]::new($metadata), "metadata")

    try {
        $response = $client.PostAsync("$script:ApiBase/files/?process=true", $form).GetAwaiter().GetResult()
        $body = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
        if (-not $response.IsSuccessStatusCode) {
            Fail "File upload failed for $RelativePath ($($response.StatusCode)): $body"
        }
        return $body | ConvertFrom-Json
    } finally {
        $stream.Dispose()
        $form.Dispose()
        $client.Dispose()
    }
}

function Get-ExistingKnowledgeByName {
    param([Parameter(Mandatory = $true)][string] $Name)

    $encoded = [System.Uri]::EscapeDataString($Name)
    $result = Invoke-OpenWebUIJson -Method GET -Path "/knowledge/search?query=$encoded"
    $items = @($result.items)
    return $items | Where-Object { $_.name -eq $Name } | Select-Object -First 1
}

function Ensure-KnowledgeCollection {
    param(
        [Parameter(Mandatory = $true)][string] $Name,
        [string] $Description = ""
    )

    $existing = Get-ExistingKnowledgeByName -Name $Name
    if ($existing) {
        Write-Host "Knowledge exists: $Name ($($existing.id))"
        return $existing
    }

    Write-Host "Creating Knowledge: $Name"
    return Invoke-OpenWebUIJson -Method POST -Path "/knowledge/create" -Body @{
        name = $Name
        description = $Description
        access_grants = @()
    }
}

function Get-KnowledgeFiles {
    param([Parameter(Mandatory = $true)][string] $KnowledgeId)

    $result = Invoke-OpenWebUIJson -Method GET -Path "/knowledge/$KnowledgeId/files?page=1&limit=500"
    return @($result.items)
}

function Add-FileToKnowledge {
    param(
        [Parameter(Mandatory = $true)][string] $KnowledgeId,
        [Parameter(Mandatory = $true)][string] $FileId
    )

    return Invoke-OpenWebUIJson -Method POST -Path "/knowledge/$KnowledgeId/file/add" -Body @{
        file_id = $FileId
    }
}

function Import-Models {
    if (-not (Test-Path -LiteralPath $ImportFile)) {
        Fail "Import file not found: $ImportFile"
    }

    $models = Get-Content -Raw -LiteralPath $ImportFile | ConvertFrom-Json
    foreach ($model in @($models)) {
        $model.base_model_id = $BaseModelId
    }

    Write-Host "Importing $(@($models).Count) models with base model '$BaseModelId'"
    Invoke-OpenWebUIJson -Method POST -Path "/models/import" -Body @{ models = @($models) } | Out-Null
    return @($models)
}

function Get-ModelById {
    param([Parameter(Mandatory = $true)][string] $ModelId)

    $encoded = [System.Uri]::EscapeDataString($ModelId)
    return Invoke-OpenWebUIJson -Method GET -Path "/models/model?id=$encoded"
}

function Update-Model {
    param([Parameter(Mandatory = $true)] $Model)

    Invoke-OpenWebUIJson -Method POST -Path "/models/model/update" -Body @{
        id = $Model.id
        base_model_id = $Model.base_model_id
        name = $Model.name
        meta = $Model.meta
        params = $Model.params
        access_grants = @($Model.access_grants)
        is_active = $Model.is_active
    } | Out-Null
}

if ([string]::IsNullOrWhiteSpace($ApiKey)) {
    Fail "ApiKey is required. Set OPENWEBUI_API_KEY or pass -ApiKey. Do not store real tokens in repo files."
}

$script:ApiBase = Get-ApiBase -Url $OpenWebUIUrl
$script:Token = $ApiKey
$resolvedWorkspace = Resolve-Path -LiteralPath $WorkspaceRoot
$manifestPath = Join-Path $resolvedWorkspace "imports\openwebui-workspace-manifest.json"

if (-not (Test-Path -LiteralPath $manifestPath)) {
    Fail "Manifest not found: $manifestPath"
}

$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json

Write-Host "Open WebUI API: $script:ApiBase"
Write-Host "Workspace: $resolvedWorkspace"

$createdModels = @()
if (-not $SkipModels) {
    $createdModels = Import-Models
} else {
    $createdModels = Get-Content -Raw -LiteralPath $ImportFile | ConvertFrom-Json
}

$knowledgeByName = @{}
if (-not $SkipKnowledge) {
    foreach ($group in @($manifest.knowledge_upload_groups)) {
        if ($KnowledgeGroupNames.Count -gt 0 -and $KnowledgeGroupNames -notcontains $group.collection_name) {
            continue
        }

        $knowledge = Ensure-KnowledgeCollection -Name $group.collection_name -Description "GTM Loop Workspace collection: $($group.collection_name)"
        $knowledgeByName[$group.collection_name] = $knowledge

        $existingFiles = @{}
        foreach ($file in @(Get-KnowledgeFiles -KnowledgeId $knowledge.id)) {
            $fileName = $file.meta.name
            if (-not $fileName) { $fileName = $file.filename }
            if ($fileName) { $existingFiles[$fileName] = $true }
        }

        foreach ($relative in @($group.files)) {
            $path = Join-Path $resolvedWorkspace $relative
            if (-not (Test-Path -LiteralPath $path)) {
                Write-Warning "Missing workspace file, skipping: $relative"
                continue
            }

            if (-not $ForceUploadFiles -and $existingFiles.ContainsKey($relative)) {
                Write-Host "Knowledge file exists, skipping: $($group.collection_name) -> $relative"
                continue
            }

            Write-Host "Uploading: $($group.collection_name) -> $relative"
            $file = Upload-OpenWebUIFile -Path $path -RelativePath $relative
            Add-FileToKnowledge -KnowledgeId $knowledge.id -FileId $file.id | Out-Null
        }
    }
} else {
    foreach ($group in @($manifest.knowledge_upload_groups)) {
        if ($KnowledgeGroupNames.Count -gt 0 -and $KnowledgeGroupNames -notcontains $group.collection_name) {
            continue
        }

        $existing = Get-ExistingKnowledgeByName -Name $group.collection_name
        if ($existing) {
            $knowledgeByName[$group.collection_name] = $existing
        }
    }
}

if (-not $SkipModelKnowledgeAttach) {
    $knowledgeMapByModelName = @{
        "GTM Loop Workstation Agent" = @("GTM Workbench Core Pack")
        "GTM Loop Architect Agent" = @("GTM Loop Operating System", "GTM Loop Specs", "GTM Build System", "GTM Integration Notes", "GTM Workflow Templates", "GTM Prompts And Evals")
        "GTM Build Controller Agent" = @("GTM Loop Operating System", "GTM Build System", "GTM Loop Specs", "GTM Integration Notes", "GTM Prompts And Evals")
        "GTM Flow Builder Agent" = @("GTM Build System", "GTM Integration Notes", "GTM Workflow Templates", "GTM Loop Specs")
        "GTM Workflow Debugger Agent" = @("GTM Build System", "GTM Integration Notes", "GTM Prompts And Evals")
        "GTM Eval and QA Agent" = @("GTM Loop Operating System", "GTM Build System", "GTM Loop Specs", "GTM Prompts And Evals")
    }

    foreach ($importModel in @($createdModels)) {
        $model = Get-ModelById -ModelId $importModel.id
        $collectionNames = @($knowledgeMapByModelName[$model.name])
        if ($collectionNames.Count -eq 0) {
            Write-Host "No Knowledge mapping for model: $($model.name)"
            continue
        }

        $knowledgeItems = @()
        foreach ($collectionName in $collectionNames) {
            if ($knowledgeByName.ContainsKey($collectionName)) {
                $item = $knowledgeByName[$collectionName]
                $knowledgeItems += [ordered]@{
                    id = $item.id
                    name = $item.name
                    description = $item.description
                    type = "collection"
                }
            } else {
                Write-Warning "Knowledge collection not available for model $($model.name): $collectionName"
            }
        }

        if ($knowledgeItems.Count -gt 0) {
            $model.meta | Add-Member -NotePropertyName knowledge -NotePropertyValue $knowledgeItems -Force
            Write-Host "Attaching $($knowledgeItems.Count) Knowledge collections to model: $($model.name)"
            Update-Model -Model $model
        }
    }
}

Write-Host ""
Write-Host "GTM Loop Workspace setup complete."
Write-Host "Next: open Open WebUI -> Workspace -> Models and verify the imported GTM agents."
