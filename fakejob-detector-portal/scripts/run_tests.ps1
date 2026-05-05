# Fake Job Detector Portal - Windows Test Runner
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

& .\venv\Scripts\Activate.ps1

Write-Host "Running tests..." -ForegroundColor Cyan
pytest tests/ -v

Write-Host "Tests complete." -ForegroundColor Cyan
