$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PidFile = Join-Path $ProjectRoot "logs\app.pids.json"

if (!(Test-Path $PidFile)) {
    Write-Host "Arquivo de PID não encontrado: logs/app.pids.json"
    exit 0
}

$Pids = Get-Content $PidFile | ConvertFrom-Json

foreach ($procId in @($Pids.backend_pid, $Pids.frontend_pid)) {
    if ($null -eq $procId) { continue }
    $proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
    if ($proc) {
        Stop-Process -Id $procId -Force
        Write-Host "Processo finalizado: $procId"
    }
}

Remove-Item $PidFile -Force
Write-Host "Aplicação parada."
