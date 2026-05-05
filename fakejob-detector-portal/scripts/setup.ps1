# Fake Job Detector Portal - Windows Setup Script
$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Fake Job Detector Portal - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

# Step 1: Virtual Environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    python -m venv venv
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor Yellow
}

& .\venv\Scripts\Activate.ps1

# Step 2: Install Dependencies
Write-Host "Installing dependencies..." -ForegroundColor Green
pip install -r backend/requirements.txt

# Step 3: Environment File
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env from template..." -ForegroundColor Green
    Copy-Item .env.example .env
    Write-Host "Please edit .env with your credentials." -ForegroundColor Yellow
}

# Step 4: Download Dataset
Write-Host "Downloading EMSCAD dataset..." -ForegroundColor Green
python scripts/download_data.py

# Step 5: Train Models
Write-Host "Training ML models..." -ForegroundColor Green
Set-Location backend
python -m app.ml_models.train
Set-Location $ProjectRoot

# Step 6: Seed Database
Write-Host "Seeding database..." -ForegroundColor Green
python scripts/seed_db.py

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup complete! Run: cd backend; uvicorn app.main:app --reload" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
