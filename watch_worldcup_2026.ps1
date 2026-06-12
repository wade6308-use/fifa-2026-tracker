param(
  [int]$IntervalSeconds = 180,
  [string]$Python = "C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
)

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Updater = Join-Path $Root "scripts\update_worldcup_2026.py"
$Log = Join-Path $Root "update.log"

Write-Host "FIFA World Cup 26 自動更新已啟動。"
Write-Host "儀表板：$Root\index.html"
Write-Host "每 $IntervalSeconds 秒檢查一次。按 Ctrl+C 停止。"

while ($true) {
  $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
  try {
    $output = & $Python $Updater 2>&1
    "[$stamp] $output" | Tee-Object -FilePath $Log -Append
  } catch {
    "[$stamp] ERROR: $($_.Exception.Message)" | Tee-Object -FilePath $Log -Append
  }
  Start-Sleep -Seconds $IntervalSeconds
}
