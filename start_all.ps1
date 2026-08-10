$ROOT = "C:\Users\Asus\Downloads\Health-AICare"
$PYTHON = "C:\Python314\python.exe"
$BASH = "C:\Program Files\Git\bin\bash.exe"

# ── Backend ──────────────────────────────────────────────────────────────────
$backendCmd = @"
cd '$ROOT\backend'
& '$PYTHON' -m uvicorn app.main:app --host 127.0.0.1 --port 22001 --reload
Read-Host 'Backend stopped - press Enter to close'
"@
$backendScript = "$env:TEMP\health_backend.ps1"
$backendCmd | Out-File -FilePath $backendScript -Encoding utf8

# ── Frontend ─────────────────────────────────────────────────────────────────
$frontendCmd = @"
cd '$ROOT\frontend'
npm run dev -- -p 22000
Read-Host 'Frontend stopped - press Enter to close'
"@
$frontendScript = "$env:TEMP\health_frontend.ps1"
$frontendCmd | Out-File -FilePath $frontendScript -Encoding utf8

# ── Docs ─────────────────────────────────────────────────────────────────────
$docsCmd = @"
cd '$ROOT\docs-site'
npm run start -- --port 22002 --host 127.0.0.1
Read-Host 'Docs stopped - press Enter to close'
"@
$docsScript = "$env:TEMP\health_docs.ps1"
$docsCmd | Out-File -FilePath $docsScript -Encoding utf8

# ── AI Engine ─────────────────────────────────────────────────────────────────
$aiCmd = @"
cd '$ROOT\ai'
`$env:PORT = '8080'
`$env:PYTHONUTF8 = '1'
# Load GEMINI_API_KEY from backend .env
Get-Content '$ROOT\backend\.env' | ForEach-Object {
    if (`$_ -match '^([A-Z_]+)=(.+)$') {
        [System.Environment]::SetEnvironmentVariable(`$matches[1], `$matches[2])
    }
}
& '$PYTHON' -m src.main
Read-Host 'AI Engine stopped - press Enter to close'
"@
$aiScript = "$env:TEMP\health_ai.ps1"
$aiCmd | Out-File -FilePath $aiScript -Encoding utf8

# ── Launch all in Windows Terminal tabs ───────────────────────────────────────
Write-Host "Launching Health-AICare servers in Windows Terminal..." -ForegroundColor Cyan

$wtArgs = "-w 0 " +
  "new-tab --title `"Backend :22001`" powershell -NoExit -ExecutionPolicy Bypass -File `"$backendScript`" `; " +
  "new-tab --title `"Frontend :22000`" powershell -NoExit -ExecutionPolicy Bypass -File `"$frontendScript`" `; " +
  "new-tab --title `"Docs :22002`" powershell -NoExit -ExecutionPolicy Bypass -File `"$docsScript`" `; " +
  "new-tab --title `"AI Engine :8080`" powershell -NoExit -ExecutionPolicy Bypass -File `"$aiScript`""

Start-Process wt -ArgumentList $wtArgs

Write-Host ""
Write-Host "Servers launched!" -ForegroundColor Green
Write-Host "  Backend:   http://localhost:22001" -ForegroundColor White
Write-Host "  Frontend:  http://localhost:22000" -ForegroundColor White
Write-Host "  Docs:      http://localhost:22002" -ForegroundColor White
Write-Host "  AI Engine: http://localhost:8080"  -ForegroundColor White
Write-Host ""
Write-Host "Check the Windows Terminal tabs for individual server logs." -ForegroundColor Yellow
