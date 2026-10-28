# Registers the Windows scheduled task "YN-Data-Sync":
# every hour at :25 (and at logon) runs sync_local.py, which pulls the latest weather/news/stats
# from GitHub into this folder for the local server (127.0.0.1:8899).
# Remove later with:  Unregister-ScheduledTask -TaskName YN-Data-Sync -Confirm:$false
$ErrorActionPreference = 'Stop'
$root   = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$script = Join-Path $PSScriptRoot 'sync_local.py'

$py = (Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = Join-Path $env:LOCALAPPDATA 'Python\pythoncore-3.14-64\pythonw.exe' }
if (-not (Test-Path $py)) { $py = (Get-Command pyw.exe -ErrorAction SilentlyContinue).Source }
if (-not $py -or -not (Test-Path $py)) { throw 'pythonw.exe not found' }

$action    = New-ScheduledTaskAction -Execute $py -Argument "`"$script`"" -WorkingDirectory $root
$hourly    = New-ScheduledTaskTrigger -Once -At (Get-Date -Hour 0 -Minute 25 -Second 0) -RepetitionInterval (New-TimeSpan -Hours 1)
$logon     = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$settings  = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
               -ExecutionTimeLimit (New-TimeSpan -Minutes 5) -MultipleInstances IgnoreNew
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName 'YN-Data-Sync' -Description 'Pull latest weather/news/stats from GitHub into the local folder every hour (sync_local.py)' `
  -Action $action -Trigger @($hourly, $logon) -Settings $settings -Principal $principal -Force | Out-Null

Start-ScheduledTask -TaskName 'YN-Data-Sync'
Start-Sleep -Seconds 10
$info = Get-ScheduledTaskInfo -TaskName 'YN-Data-Sync'
Write-Host ''
Write-Host ('OK  task registered. last result: {0}   next run: {1}' -f $info.LastTaskResult, $info.NextRunTime)
$log = Join-Path $root '.git\sync_local.log'
if (Test-Path $log) { Get-Content $log -Encoding UTF8 -Tail 1 }
