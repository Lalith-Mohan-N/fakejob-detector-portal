# Fake Job Detector Portal - Start Development Server
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

& .\venv\Scripts\Activate.ps1

Write-Host "Starting FastAPI server on http://localhost:8000" -ForegroundColor Cyan
Write-Host "Docs available at http://localhost:8000/docs" -ForegroundColor Cyan
Set-Location backend
uvicorn app.main:app --reload --port 8000
