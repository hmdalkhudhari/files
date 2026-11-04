# install.ps1 — one-time: copies the sync script and registers a scheduled task every 2 minutes.
$Work = Join-Path $env:LOCALAPPDATA 'drive-inbox'
New-Item -ItemType Directory -Force -Path $Work | Out-Null
Invoke-WebRequest -Headers @{ 'User-Agent'='drive-inbox-sync' } -Uri 'https://raw.githubusercontent.com/hmdalkhudhari/files/drive-inbox/sync-drive-inbox.ps1' -OutFile "$Work\sync-drive-inbox.ps1"
$action  = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$Work\sync-drive-inbox.ps1`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 2) -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName 'DriveInboxSync' -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null
Start-ScheduledTask -TaskName 'DriveInboxSync'
Write-Host 'DriveInboxSync installed (every 2 min).'
