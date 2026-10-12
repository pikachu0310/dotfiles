[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)][string]$ProjectPath,
    [Parameter(Mandatory)][string]$EditorPath,
    [string]$LogPath,
    [string]$ScenePath,
    [switch]$ForceD3D11
)

$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'Run this launcher in native Windows PowerShell.' }

$projectRoot = (Resolve-Path -LiteralPath $ProjectPath).ProviderPath.TrimEnd('\')
$editorExe = (Resolve-Path -LiteralPath $EditorPath).ProviderPath
if (-not (Test-Path -LiteralPath (Join-Path $projectRoot 'ProjectSettings/ProjectVersion.txt') -PathType Leaf)) {
    throw 'ProjectPath must be an existing Unity project.'
}
if ((Split-Path -Leaf $editorExe) -ne 'Unity.exe' -or -not (Test-Path -LiteralPath $editorExe -PathType Leaf)) {
    throw 'EditorPath must identify the installed Unity.exe for this project.'
}

# Inspect only; the owning chat must preserve work and normally stop its Editor.
$existing = @(Get-CimInstance Win32_Process -Filter "Name='Unity.exe'" | Where-Object {
    $projectArg = [regex]::Match([string]$_.CommandLine, '-projectPath\s+(?:"([^"]+)"|(\S+))', 'IgnoreCase')
    if (-not $projectArg.Success) { return $false }
    $runningPath = if ($projectArg.Groups[1].Success) { $projectArg.Groups[1].Value } else { $projectArg.Groups[2].Value }
    if (-not [IO.Path]::IsPathRooted($runningPath)) { return $false }
    $runningPath = [IO.Path]::GetFullPath($runningPath.Replace('/', '\')).TrimEnd('\')
    return [string]::Equals($runningPath, $projectRoot, [StringComparison]::OrdinalIgnoreCase)
})
if ($existing.Count) {
    throw "This project already has an Editor (PID $($existing.ProcessId -join ', ')). Preserve the Scene and SDK request and complete normal shutdown in its owning chat first."
}

function Quote-UnityArgument([string]$Value) {
    if ($Value.Contains('"') -or $Value.Contains("`r") -or $Value.Contains("`n")) {
        throw 'Paths must not contain quotes or line breaks.'
    }
    return '"' + $Value + '"'
}

$unityArguments = @('-projectPath', (Quote-UnityArgument $projectRoot))
if ($ForceD3D11) { $unityArguments += '-force-d3d11' }
if ($LogPath) {
    if (-not [IO.Path]::IsPathRooted($LogPath)) { throw 'LogPath must be absolute.' }
    $logFile = [IO.Path]::GetFullPath($LogPath)
    if (-not (Test-Path -LiteralPath (Split-Path -Parent $logFile) -PathType Container)) {
        throw 'The log directory must already exist.'
    }
    $unityArguments += @('-logFile', (Quote-UnityArgument $logFile))
}
if ($ScenePath) {
    if ([IO.Path]::IsPathRooted($ScenePath)) { throw 'ScenePath must be relative to ProjectPath.' }
    $sceneFile = [IO.Path]::GetFullPath((Join-Path $projectRoot $ScenePath))
    if (-not $sceneFile.StartsWith($projectRoot + '\', [StringComparison]::OrdinalIgnoreCase) -or
        -not (Test-Path -LiteralPath $sceneFile -PathType Leaf) -or
        [IO.Path]::GetExtension($sceneFile) -ne '.unity') {
        throw 'ScenePath must identify a saved .unity file inside this project.'
    }
    $unityArguments += @('-openscene', (Quote-UnityArgument $sceneFile))
}

if ($PSCmdlet.ShouldProcess($projectRoot, 'Launch the installed Unity Editor with WindowStyle Normal')) {
    $launchedEditor = Start-Process -FilePath $editorExe -ArgumentList $unityArguments -WindowStyle Normal -PassThru
    [pscustomobject]@{ ProcessId = $launchedEditor.Id; ProjectPath = $projectRoot; WindowStyle = 'Normal' }
}
# A returned PID does not prove visibility or readiness; verify fresh official windows.
