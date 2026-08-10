Set-Location "C:\Users\Asus\Downloads\Health-AICare\backend"

# Force UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
$OutputEncoding            = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

$env:PYTHONIOENCODING = "utf-8"

# Load backend .env
Get-Content ".env" | ForEach-Object {
    if ($_ -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$') {
        $val = $Matches[2].Trim('"').Trim("'")
        [System.Environment]::SetEnvironmentVariable($Matches[1], $val)
    }
}

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Health-AICare Backend :22001  " -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# NO --reload flag to prevent reloader port conflict on Windows
C:\Python314\python.exe -X utf8 -m uvicorn app.main:app --host 0.0.0.0 --port 22001
