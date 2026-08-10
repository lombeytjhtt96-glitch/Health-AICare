Set-Location "C:\Users\Asus\Downloads\Health-AICare\ai"

$env:PORT = "8080"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

# Load env vars from backend .env
$envFile = "C:\Users\Asus\Downloads\Health-AICare\backend\.env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$') {
            [System.Environment]::SetEnvironmentVariable($Matches[1], $Matches[2].Trim('"').Trim("'"))
        }
    }
    Write-Host "Loaded .env from backend" -ForegroundColor Cyan
}

Write-Host "Starting AI Engine on port 8080..." -ForegroundColor Yellow
C:\Python314\python.exe -m src.main
