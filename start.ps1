# Quick Start Script for Barbershop CRM

Write-Host "🚀 Barbershop CRM - Quick Start" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
}
catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Ask user for setup method
Write-Host ""
Write-Host "Choose setup method:" -ForegroundColor Cyan
Write-Host "1. Docker Compose (Recommended for quick start)"
Write-Host "2. Manual Setup (Backend only)"
Write-Host "3. Exit"
Write-Host ""

$choice = Read-Host "Enter choice (1-3)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🐳 Starting with Docker Compose..." -ForegroundColor Cyan
        
        # Check if .env exists
        if (-not (Test-Path "backend\.env")) {
            Write-Host "⚠️  No .env file found. Creating from template..." -ForegroundColor Yellow
            Copy-Item "backend\.env" "backend\.env.backup" -ErrorAction SilentlyContinue
        }
        
        Write-Host "Building and starting services..." -ForegroundColor Yellow
        docker-compose up -d --build
        
        Write-Host ""
        Write-Host "✅ Services started!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📍 Access your services:" -ForegroundColor Cyan
        Write-Host "   Backend API: http://localhost:8000" -ForegroundColor White
        Write-Host "   Admin Panel: http://localhost:8000/admin" -ForegroundColor White
        Write-Host "   Flower (Celery): http://localhost:5555" -ForegroundColor White
        Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
        Write-Host ""
        Write-Host "⚠️  Note: You need to configure Supabase credentials in backend\.env" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "📝 Next steps:" -ForegroundColor Cyan
        Write-Host "   1. Update backend\.env with your Supabase credentials"
        Write-Host "   2. Run migrations: docker-compose exec backend python manage.py migrate"
        Write-Host "   3. Create superuser: docker-compose exec backend python manage.py createsuperuser"
        Write-Host ""
    }
    
    "2" {
        Write-Host ""
        Write-Host "🔧 Manual Setup..." -ForegroundColor Cyan
        
        # Check if virtual environment exists
        if (-not (Test-Path "backend\.venv")) {
            Write-Host "Creating virtual environment..." -ForegroundColor Yellow
            Set-Location backend
            python -m venv .venv
            Set-Location ..
        }
        
        Write-Host "Activating virtual environment..." -ForegroundColor Yellow
        Set-Location backend
        .\.venv\Scripts\Activate.ps1
        
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt
        
        Write-Host ""
        Write-Host "⚠️  Make sure to:" -ForegroundColor Yellow
        Write-Host "   1. Update .env with your Supabase credentials"
        Write-Host "   2. Start Redis: docker run -d -p 6379:6379 redis:7-alpine"
        Write-Host ""
        
        $runMigrations = Read-Host "Run migrations now? (y/n)"
        if ($runMigrations -eq "y") {
            Write-Host "Running migrations..." -ForegroundColor Yellow
            python manage.py migrate
        }
        
        $createSuperuser = Read-Host "Create superuser? (y/n)"
        if ($createSuperuser -eq "y") {
            python manage.py createsuperuser
        }
        
        Write-Host ""
        Write-Host "✅ Setup complete!" -ForegroundColor Green
        Write-Host ""
        Write-Host "To start the server:" -ForegroundColor Cyan
        Write-Host "   python manage.py runserver" -ForegroundColor White
        Write-Host ""
        Write-Host "To start Celery worker:" -ForegroundColor Cyan
        Write-Host "   celery -A config worker --loglevel=info" -ForegroundColor White
        Write-Host ""
    }
    
    "3" {
        Write-Host "Exiting..." -ForegroundColor Yellow
        exit 0
    }
    
    default {
        Write-Host "Invalid choice. Exiting..." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "📚 For more information, see README.md" -ForegroundColor Cyan
Write-Host ""
