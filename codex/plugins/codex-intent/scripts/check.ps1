[CmdletBinding()]
param(
    [string]$InstalledPluginRoot
)

$ErrorActionPreference = 'Stop'
$pluginRoot = [System.IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
$errors = [System.Collections.Generic.List[string]]::new()

function Assert-True {
    param([bool]$Condition, [string]$Message)

    if (-not $Condition) {
        $script:errors.Add($Message)
    }
}

function Assert-Match {
    param([string]$Text, [string]$Pattern, [string]$Message)

    Assert-True ([regex]::IsMatch($Text, $Pattern, 'Singleline')) $Message
}

function ConvertFrom-Utf8Base64 {
    param([string]$Value)

    [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($Value))
}

function Get-Sha256 {
    param([string]$Path)

    # .NET also works from WSL-launched Windows PowerShell when its module
    # search path does not expose Microsoft.PowerShell.Utility/Get-FileHash.
    $stream = [System.IO.File]::OpenRead($Path)
    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    try {
        [System.BitConverter]::ToString($sha256.ComputeHash($stream))
    }
    finally {
        $sha256.Dispose()
        $stream.Dispose()
    }
}

function Read-Utf8 {
    param([string]$Path)

    Get-Content -Raw -Encoding UTF8 -LiteralPath $Path
}

$requiredFiles = @(
    'plugin.json',
    '.codex-plugin/plugin.json',
    'skills/codex-intent/SKILL.md',
    'skills/codex-intent/agents/openai.yaml',
    'skills/codex-intent/references/protocol.md',
    'scripts/check.ps1'
)

foreach ($relativePath in $requiredFiles) {
    $absolutePath = Join-Path $pluginRoot $relativePath
    Assert-True (Test-Path -LiteralPath $absolutePath -PathType Leaf) "missing: $relativePath"
}

try {
    $manifestPath = Join-Path $pluginRoot '.codex-plugin/plugin.json'
    $manifest = Read-Utf8 $manifestPath | ConvertFrom-Json
    Assert-True ($manifest.name -ceq 'codex-intent') 'manifest name must be codex-intent'
    Assert-True ($manifest.version -match '^0[.]4[.]0-public$') 'manifest version must match the reviewed public adaptation'
    Assert-True ($manifest.skills -ceq './skills/') 'manifest skills path must be ./skills/'

    foreach ($unsupported in @('hooks', 'mcpServers', 'apps')) {
        Assert-True ($null -eq $manifest.PSObject.Properties[$unsupported]) "manifest must not declare $unsupported"
    }
}
catch {
    $errors.Add("manifest is not valid JSON: $($_.Exception.Message)")
}

$skillPath = Join-Path $pluginRoot 'skills/codex-intent/SKILL.md'
$skillText = Read-Utf8 $skillPath
$skillBytes = [System.IO.File]::ReadAllBytes($skillPath).Length
Assert-True ($skillBytes -le 12288) "SKILL.md exceeds 12 KiB: $skillBytes bytes"
Assert-True ($skillText.StartsWith("---`nname: codex-intent`n")) 'SKILL.md frontmatter must start with the expected name'

$protocolPath = Join-Path $pluginRoot 'skills/codex-intent/references/protocol.md'
$protocolText = Read-Utf8 $protocolPath

# One executable default contract; renewal must reuse it instead of carrying
# a second model/effort pair that can become stale independently.
$defaultsMatch = [regex]::Match($protocolText, '```json\s*(?<json>.*?)\s*```', 'Singleline')
Assert-True $defaultsMatch.Success 'protocol must declare its model defaults as JSON'
if ($defaultsMatch.Success) {
    try {
        $defaults = $defaultsMatch.Groups['json'].Value | ConvertFrom-Json
        Assert-True (-not [string]::IsNullOrWhiteSpace($defaults.model)) 'author preset example must retain the documented model'
        Assert-True (-not [string]::IsNullOrWhiteSpace($defaults.thinking)) 'author preset example must retain the documented effort'
        Assert-True (@($defaults.PSObject.Properties).Count -eq 2) 'default contract must contain only model and thinking; Fast is separately scoped'
    }
    catch {
        $errors.Add("invalid model defaults: $($_.Exception.Message)")
    }
}
$renewalMatch = [regex]::Match($protocolText, '(?m)^## 9[.].*?(?=^## 10[.])', 'Singleline, Multiline')
Assert-True $renewalMatch.Success 'intake renewal contract must exist'
if ($renewalMatch.Success) {
    Assert-True (-not [regex]::IsMatch($renewalMatch.Value, 'gpt-[a-z0-9.-]+|thinking\s*:')) 'renewal must reuse model defaults, not duplicate them'
}

foreach ($requiredPhrase in @(
    '# Codex Intent protocol v3',
    'mcp__codex_app__create_thread',
    'mcp__codex_app__set_thread_title',
    'Local',
    'Worktree',
    'projectless',
    'codex/TNNN-',
    '::created-thread{threadId=',
    '::created-thread{clientThreadId='
)) {
    Assert-True ($protocolText.Contains($requiredPhrase)) "missing protocol contract: $requiredPhrase"
}

$titleFixture = "T123 $([char]0x00B7) Title retention"
Assert-Match $titleFixture '^T\d{3} \u00B7 .+$' 'title fixture must satisfy the TNNN title format'

$promptMatch = [regex]::Match(
    $protocolText,
    '```text\s*(?<prompt>.*?)\s*```',
    'Singleline'
)
Assert-True $promptMatch.Success 'initial prompt template must be extractable from protocol.md'

if ($promptMatch.Success) {
    $promptTemplate = $promptMatch.Groups['prompt'].Value
    $fixedTitleLine = ConvertFrom-Utf8Base64 '5Zu65a6a44K/44Kk44OI44OrOiA8VE5OTiDCtyDmiJDmnpzlkI0+'
    $renameProhibition = ConvertFrom-Utf8Base64 '44GT44Gu44K/44K544Kv6Ieq6Lqr44Gu44K/44Kk44OI44Or44KS5oiQ5p6c5paH44CB5Y6f5paH44CBc3VtbWFyeeOAgXN0YXR1c+OAgeacgOe1guaIkOaenOOBuOWkieabtOOBl+OBquOBhOOBp+OBj+OBoOOBleOBhOOAgg=='
    $outcomeLabel = ConvertFrom-Utf8Base64 '5oiQ5p6cOg=='
    $currentTaskOnly = ConvertFrom-Utf8Base64 'dGhyZWFkSWTjgpLmjIflrprjgZvjgZpjdXJyZW50IHRhc2voh6rouqs='
    $noOtherTask = ConvertFrom-Utf8Base64 '5Yil44K/44K544Kv44GuSUTjgpLmjIflrprjgZfjgaZ0aXRsZeOCkuWkieabtOOBl+OBquOBhA=='
    Assert-True ($promptTemplate.StartsWith("$fixedTitleLine`n$renameProhibition")) 'initial prompt must start with the fixed title and rename prohibition'
    Assert-True ($promptTemplate.IndexOf($fixedTitleLine) -lt $promptTemplate.IndexOf($outcomeLabel)) 'fixed title must precede the outcome in the initial prompt'
    Assert-True ($promptTemplate.Contains($currentTaskOnly)) 'task-side repair must target only the current task without another thread ID'
    Assert-True ($promptTemplate.Contains($noOtherTask)) 'initial prompt must forbid repairing another task'
}

foreach ($contractCase in @(
    @{ Pattern = ConvertFrom-Utf8Base64 'Y3JlYXRlX3RocmVhZGDjga5gdGl0bGVg44Gv5b+F6aCI'; Message = 'create_thread title must be required' },
    @{ Pattern = ConvertFrom-Utf8Base64 'YOaIkOaenDpg44CBYOWOn+aWhzpg44CBZGVsZWdhdGlvbiB3cmFwcGVy44CBc3VtbWFyeeOAgXN0YXR1c+OAgeacgOe1guaIkOaenOOBi+OCiXRpdGxl44KS55Sf5oiQ44GX44G+44Gb44KT'; Message = 'prompt and delegation content must not become the title source' },
    @{ Pattern = ConvertFrom-Utf8Base64 '5oiQ5p6c5a6M5LqG44CBc3RhdHVz5aSJ5YyW44CBc3VtbWFyeeOAgeacgOe1guaIkOaenOOCkueQhueUseOBq+OCv+OCpOODiOODq+OCkuWkieabtOOBl+OBvuOBm+OCkw=='; Message = 'completion and status changes must not rename a task' },
    @{ Pattern = ConvertFrom-Utf8Base64 '5L2c5oiQ5pmC44Gu5Zu65a6a44K/44Kk44OI44Or44GM56K65a6a44GX44Gm44GE44KL5ZCM44GYdGhyZWFkIElE44Gg44GR'; Message = 'drift repair must be limited to the same created thread' },
    @{ Pattern = ConvertFrom-Utf8Base64 'YGNsaWVudFRocmVhZElkYOOCkmB0aHJlYWRJZGDjgajjgZfjgaZyZWFk44CBcGlu44CBdGl0bGUgcmVwYWly44G45rih44GX44G+44Gb44KT'; Message = 'queued clientThreadId must not be treated as threadId' },
    @{ Pattern = ConvertFrom-Utf8Base64 '5beh5Zue44CB5a6a5pyf55uj6KaW44CB54Sh5p2h5Lu244Gu5YaN5pu444GN6L6844G/44Gv6KGM44GE44G+44Gb44KT'; Message = 'title repair must remain a bounded one-shot safeguard' }
)) {
    Assert-True ($protocolText.Contains($contractCase.Pattern)) $contractCase.Message
}

Assert-True (-not $protocolText.Contains('tools.codex_app__create_thread')) 'deprecated dynamic create_thread path must not be used'

$textFiles = Get-ChildItem -LiteralPath $pluginRoot -Recurse -File | Where-Object {
    $_.Name -ne 'check.ps1' -and
    $_.Extension -in @('.md', '.yaml', '.yml', '.json', '.ps1', '.txt', '')
}
$allText = ($textFiles | ForEach-Object { Read-Utf8 $_.FullName }) -join "`n"

foreach ($forbidden in @(
    'workerThreadId',
    'sweep-lock[.]ps1',
    'set_thread_archived',
    'sk-[A-Za-z0-9_-]{20,}',
    'gh[pousr]_[A-Za-z0-9]{20,}',
    'BEGIN [A-Z ]*PRIVATE KEY'
)) {
    Assert-True (-not [regex]::IsMatch($allText, $forbidden, 'IgnoreCase')) "forbidden content detected: $forbidden"
}

# Optional read-only installation check. A valid source does not prove that
# the app is loading it; compare the complete package, not only the version.
$installedVerified = $false
if ($InstalledPluginRoot) {
    $installedRoot = [System.IO.Path]::GetFullPath($InstalledPluginRoot)
    if (-not (Test-Path -LiteralPath $installedRoot -PathType Container)) {
        $errors.Add("installed plugin root does not exist: $installedRoot")
    }
    elseif ($installedRoot.TrimEnd('\', '/') -eq $pluginRoot.TrimEnd('\', '/')) {
        $errors.Add('installed plugin root must differ from the source root')
    }
    else {
        $sourceFiles = @(Get-ChildItem -LiteralPath $pluginRoot -Recurse -File -Force)
        $installedFiles = @(Get-ChildItem -LiteralPath $installedRoot -Recurse -File -Force)
        Assert-True ($sourceFiles.Count -eq $installedFiles.Count) 'source/installed file counts differ'
        foreach ($sourceFile in $sourceFiles) {
            $relativePath = $sourceFile.FullName.Substring($pluginRoot.TrimEnd('\', '/').Length).TrimStart('\', '/')
            $installedPath = Join-Path $installedRoot $relativePath
            if (-not (Test-Path -LiteralPath $installedPath -PathType Leaf)) {
                $errors.Add("missing installed file: $relativePath")
                continue
            }
            $sourceHash = Get-Sha256 $sourceFile.FullName
            $installedHash = Get-Sha256 $installedPath
            Assert-True ($sourceHash -ceq $installedHash) "source/installed content differs: $relativePath"
        }
        $installedVerified = $errors.Count -eq 0
    }
}

if ($errors.Count -gt 0) {
    foreach ($validationError in $errors) {
        Write-Error $validationError -ErrorAction Continue
    }

    exit 1
}

[pscustomobject]@{
    ok = $true
    version = $manifest.version
    skillBytes = $skillBytes
    files = $requiredFiles.Count
    installedVerified = $installedVerified
} | ConvertTo-Json -Compress
