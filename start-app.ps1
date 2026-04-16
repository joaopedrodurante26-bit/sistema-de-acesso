param(
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

$Python = Join-Path $ProjectRoot ".venv-win\Scripts\python.exe"
if (!(Test-Path $Python)) {
    throw "Python do ambiente virtual não encontrado em '.venv-win\Scripts\python.exe'."
}

$BackendLogDir = Join-Path $ProjectRoot "logs\backend"
$FrontendLogDir = Join-Path $ProjectRoot "logs\frontend"
New-Item -ItemType Directory -Force -Path $BackendLogDir | Out-Null
New-Item -ItemType Directory -Force -Path $FrontendLogDir | Out-Null

$BackendOut = Join-Path $BackendLogDir "server.out.log"
$BackendErr = Join-Path $BackendLogDir "server.err.log"
$FrontendOut = Join-Path $FrontendLogDir "static.out.log"
$FrontendErr = Join-Path $FrontendLogDir "static.err.log"

$BackendCmd = "backend/run.py"
$FrontendArgs = @("-m", "http.server", "5500", "--directory", "frontend")

$BackendProc = Start-Process -FilePath $Python -ArgumentList $BackendCmd -WorkingDirectory $ProjectRoot -RedirectStandardOutput $BackendOut -RedirectStandardError $BackendErr -PassThru
$FrontendProc = Start-Process -FilePath $Python -ArgumentList $FrontendArgs -WorkingDirectory $ProjectRoot -RedirectStandardOutput $FrontendOut -RedirectStandardError $FrontendErr -PassThru

Start-Sleep -Seconds 2

$HealthOk = $false
for ($i = 0; $i -lt 10; $i++) {
    try {
        $resp = Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/health" -UseBasicParsing -TimeoutSec 2
        if ($resp.StatusCode -eq 200) {
            $HealthOk = $true
            break
        }
    } catch {
        Start-Sleep -Milliseconds 500
    }
}

$AppUrl = "http://127.0.0.1:5500/pages/login.html"

$PidFile = Join-Path $ProjectRoot "logs\app.pids.json"
$PidPayload = @{
    backend_pid = $BackendProc.Id
    frontend_pid = $FrontendProc.Id
    started_at = (Get-Date).ToString("s")
    app_url = $AppUrl
}
$PidPayload | ConvertTo-Json | Set-Content -Path $PidFile -Encoding UTF8

Write-Host "Backend PID: $($BackendProc.Id)"
Write-Host "Frontend PID: $($FrontendProc.Id)"
Write-Host "Frontend URL: $AppUrl"
if ($HealthOk) {
    Write-Host "API health: OK (http://127.0.0.1:5000/api/health)"
} else {
    Write-Host "API health: não confirmou dentro do tempo esperado. Verifique logs/backend/server.err.log"
}

if (-not $NoBrowser) {
    Start-Process $AppUrl | Out-Null
}
