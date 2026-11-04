# sync-drive-inbox.ps1 — pulls new files from GitHub branch "drive-inbox" into the Drive for Desktop folder.
# Runs every 2 minutes via Task Scheduler. No git needed. Never deletes anything in Drive.
$ErrorActionPreference = 'Stop'
$Repo   = 'hmdalkhudhari/files'
$Branch = 'drive-inbox'
$Dest   = 'G:\My Drive\Hamad Content'
$Work   = Join-Path $env:LOCALAPPDATA 'drive-inbox'
$Log    = Join-Path $Work 'sync.log'
New-Item -ItemType Directory -Force -Path $Work | Out-Null
function Log($m){ Add-Content -Path $Log -Value ("{0} {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $m) }
try {
  if (-not (Test-Path $Dest)) { Log "Dest missing: $Dest"; exit 0 }
  $hdr = @{ 'User-Agent'='drive-inbox-sync' }
  $sha = (Invoke-RestMethod -Headers $hdr -Uri "https://api.github.com/repos/$Repo/commits/$Branch").sha
  $last = if (Test-Path "$Work\last.sha") { Get-Content "$Work\last.sha" } else { '' }
  if ($sha -eq $last) { exit 0 }
  $zip = "$Work\inbox.zip"; $ext = "$Work\extract"
  Invoke-WebRequest -Headers $hdr -Uri "https://api.github.com/repos/$Repo/zipball/$Branch" -OutFile $zip
  if (Test-Path $ext) { Remove-Item $ext -Recurse -Force }
  Expand-Archive -Path $zip -DestinationPath $ext -Force
  $root = Get-ChildItem $ext | Select-Object -First 1
  $src = Join-Path $root.FullName 'inbox'
  if (Test-Path $src) {
    # copy new/changed files only; never delete in Drive
    robocopy $src $Dest /E /XO /R:2 /W:2 /NFL /NDL /NJH /NJS /XF README.md | Out-Null
    Log "synced $sha"
  } else { Log "no inbox folder in $sha" }
  Set-Content "$Work\last.sha" $sha
} catch { Log ("ERR " + $_.Exception.Message) }
