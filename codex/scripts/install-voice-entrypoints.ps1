# Creates user-facing entry points through the documented codex:// deep link.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}$')]
    [string]$IntakeThreadId
)

$ErrorActionPreference = 'Stop'
$entryUrl = 'codex://threads/' + $IntakeThreadId.ToLowerInvariant()
$entryText = "[InternetShortcut]`r`nURL=$entryUrl`r`n`r`n[CodexVoiceEntry]`r`nVersion=1`r`n"
$desktopPath = [Environment]::GetFolderPath('DesktopDirectory')
$programsPath = [Environment]::GetFolderPath('Programs')
if (-not $desktopPath -or -not $programsPath) {
    throw 'Windows desktop or Start menu folder is unavailable.'
}
$destinations = @(
    (Join-Path $desktopPath 'Codex 音声受付.url'),
    (Join-Path $programsPath 'Codex 音声受付.url')
)

# Validate every destination before writing either entry.
foreach ($destination in $destinations) {
    if (Test-Path -LiteralPath $destination) {
        $existing = Get-Content -LiteralPath $destination -Raw
        if ($existing -notmatch '(?m)^\[CodexVoiceEntry\]\r?$') {
            throw "An existing unmanaged shortcut would be overwritten: $destination"
        }
    }
}
foreach ($destination in $destinations) {
    [IO.File]::WriteAllText($destination, $entryText, [Text.Encoding]::ASCII)
    $installed = [IO.File]::ReadAllText($destination)
    if ($installed -ne $entryText) {
        throw "Shortcut verification failed: $destination"
    }
    [pscustomobject]@{ Path = $destination; URL = $entryUrl }
}
