param(
 [string]$Distribution = 'Ubuntu-24.04',
 [Parameter(ValueFromRemainingArguments = $true)][string[]]$TaskArguments
)
$ErrorActionPreference = 'Stop'
$taskCodexDirectory = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex' }
$taskLinuxDirectory = & wsl.exe -d $Distribution -- wslpath -u $taskCodexDirectory
if ($LASTEXITCODE -ne 0) { throw 'Could not resolve the selected Windows Codex history directory.' }
& wsl.exe -d $Distribution -- env "CODEX_HOME=$taskLinuxDirectory" /bin/bash -lc 'exec "$HOME/.local/bin/agtlog" "$@" --agent codex --offline' agtlog @TaskArguments
exit $LASTEXITCODE
