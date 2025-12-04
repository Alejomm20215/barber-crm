# Setup script for Reflex linting environment
# Run from frontend directory: .\scripts\setup_linting.ps1

Write-Host "🔧 Setting up Reflex Linting Environment..." -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "rxconfig.py")) {
    Write-Host "❌ Error: Please run this script from the frontend directory" -ForegroundColor Red
    exit 1
}

# Activate virtual environment if it exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
    .\.venv\Scripts\Activate.ps1
}

# Install linting dependencies
Write-Host "📥 Installing linting dependencies..." -ForegroundColor Yellow
pip install ruff pre-commit detect-secrets --quiet

# Initialize pre-commit
Write-Host "🔗 Installing pre-commit hooks..." -ForegroundColor Yellow
pre-commit install

# Run initial lint check
Write-Host ""
Write-Host "🔍 Running initial lint check..." -ForegroundColor Yellow
Write-Host ""

# Run Ruff
Write-Host "--- Ruff Linter ---" -ForegroundColor Magenta
ruff check barber_crm/ --fix

# Run custom Reflex linter
Write-Host ""
Write-Host "--- Reflex Linter ---" -ForegroundColor Magenta
python scripts/reflex_linter.py

Write-Host ""
Write-Host "✅ Linting setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Available commands:" -ForegroundColor Cyan
Write-Host "  ruff check barber_crm/          - Run Ruff linter"
Write-Host "  ruff format barber_crm/         - Format code with Ruff"
Write-Host "  python scripts/reflex_linter.py - Run Reflex-specific linter"
Write-Host "  pre-commit run --all-files      - Run all pre-commit hooks"
Write-Host ""
