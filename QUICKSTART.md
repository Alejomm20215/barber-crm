# 🚀 Quick Start Guide - Barbershop CRM

This guide will get your Barbershop CRM up and running in **under 10 minutes**.

## Prerequisites

Before you begin, ensure you have:

- ✅ Python 3.11+ installed
- ✅ Docker Desktop installed and running
- ✅ Git installed
- ✅ A Supabase account (free tier works)

## Option 1: Quick Start with Docker (Recommended)

### Step 1: Clone and Setup

```powershell
# Navigate to the project
cd c:\Users\am532\barber-crm

# Copy environment file
cd backend
Copy-Item .env .env.example
```

### Step 2: Configure Supabase

1. **Create a Supabase Project:**
   - Go to https://supabase.com
   - Click "New Project"
   - Note your project URL and keys

2. **Update `.env` file:**
   ```env
   SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
   SUPABASE_SERVICE_KEY=your_service_key_here
   DATABASE_URL=postgresql://postgres:your_password@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
   SECRET_KEY=your-secret-key-here-change-in-production
   DEBUG=True
   REDIS_URL=redis://redis:6379/0
   ```

3. **Apply RLS Policies:**
   - Open Supabase SQL Editor
   - Copy/paste from `SUPABASE_RLS.md`
   - Run all SQL commands

### Step 3: Start with Docker Compose

```powershell
# From project root
docker-compose up -d

# Check if services are running
docker-compose ps
```

### Step 4: Run Migrations

```powershell
# Run database migrations
docker-compose exec backend python manage.py migrate

# Create a superuser
docker-compose exec backend python manage.py createsuperuser
```

### Step 5: Access Your Application

- **Backend API:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin
- **API Docs:** http://localhost:8000/api/
- **Flower (Celery):** http://localhost:5555
- **Frontend:** http://localhost:3000

### Step 6: Test the API

```powershell
# Health check
curl http://localhost:8000/healthz/

# Check readiness
curl http://localhost:8000/readyz/
```

---

## Option 2: Manual Setup (Development)

### Step 1: Backend Setup

```powershell
# Navigate to backend
cd c:\Users\am532\barber-crm\backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configure .env (same as Option 1, Step 2)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Step 2: Start Redis (Required)

```powershell
# In a new terminal
docker run -d -p 6379:6379 redis:7-alpine
```

### Step 3: Start Celery Worker (Optional)

```powershell
# In a new terminal, activate venv first
cd c:\Users\am532\barber-crm\backend
.\.venv\Scripts\Activate.ps1

# Start worker
celery -A config worker --loglevel=info
```

### Step 4: Start Celery Beat (Optional)

```powershell
# In a new terminal, activate venv first
cd c:\Users\am532\barber-crm\backend
.\.venv\Scripts\Activate.ps1

# Start beat scheduler
celery -A config beat --loglevel=info
```

### Step 5: Frontend Setup

```powershell
# In a new terminal
cd c:\Users\am532\barber-crm\frontend

# Create virtual environment
python -m venv .venv

# Activate
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start Reflex
reflex run
```

---

## Option 3: Using the Quick Start Script

```powershell
# From project root
.\start.ps1

# Follow the interactive prompts
```

---

## Verify Installation

### 1. Check Backend Health

```powershell
# Test health endpoints
curl http://localhost:8000/healthz/
curl http://localhost:8000/livez/
curl http://localhost:8000/readyz/
```

Expected response:
```json
{"status": "healthy"}
```

### 2. Access Admin Panel

1. Go to http://localhost:8000/admin
2. Login with your superuser credentials
3. You should see all the models (Businesses, Staff, Customers, etc.)

### 3. Test API Endpoints

```powershell
# Login to get session cookie (using PowerShell)
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
Invoke-WebRequest -Uri "http://localhost:8000/api-auth/login/" `
  -Method POST `
  -Body @{username='admin'; password='yourpassword'} `
  -WebSession $session

# List businesses
Invoke-RestMethod -Uri "http://localhost:8000/api/businesses/" `
  -WebSession $session
```

---

## Running Tests

### Run All Tests

```powershell
cd backend
.\.venv\Scripts\Activate.ps1

# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific test file
pytest apps/businesses/tests.py

# Run specific test
pytest apps/businesses/tests.py::TestBusinessModel::test_create_business
```

### View Coverage Report

```powershell
# Open coverage report in browser
start htmlcov/index.html
```

---

## Common Issues & Solutions

### Issue: Docker not running
```
❌ Docker is not running. Please start Docker Desktop.
```
**Solution:** Start Docker Desktop and wait for it to fully start.

### Issue: Port already in use
```
Error: Port 8000 is already in use
```
**Solution:** 
```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID <PID> /F
```

### Issue: Database connection error
```
django.db.utils.OperationalError: could not connect to server
```
**Solution:** 
- Verify your `DATABASE_URL` in `.env`
- Check Supabase project is active
- Ensure network connectivity

### Issue: Redis connection error
```
redis.exceptions.ConnectionError: Error connecting to Redis
```
**Solution:**
```powershell
# Start Redis with Docker
docker run -d -p 6379:6379 redis:7-alpine

# Or check if Redis container is running
docker ps | findstr redis
```

### Issue: Module not found
```
ModuleNotFoundError: No module named 'apps'
```
**Solution:**
```powershell
# Make sure you're in the backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Next Steps

### 1. Create Your First Business

```powershell
# Using Django shell
python manage.py shell
```

```python
from django.contrib.auth.models import User
from apps.businesses.models import Business

# Get your user
user = User.objects.first()

# Create a business
business = Business.objects.create(
    name="My Barbershop",
    owner=user,
    phone="555-1234",
    email="contact@mybarbershop.com",
    address="123 Main St, City, State"
)

print(f"Created business: {business.name}")
```

### 2. Add Staff Members

Via Admin Panel:
1. Go to http://localhost:8000/admin
2. Click "Staff" → "Add Staff"
3. Fill in the details
4. Save

### 3. Add Services

Via Admin Panel:
1. Go to http://localhost:8000/admin
2. Click "Services" → "Add Service"
3. Fill in name, price, duration
4. Save

### 4. Create Appointments

Via API:
```powershell
# Use Postman or curl to POST to /api/appointments/
```

---

## Development Workflow

### 1. Install Pre-commit Hooks

```powershell
cd c:\Users\am532\barber-crm

# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Stopping the Application

### Docker Compose

```powershell
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Manual Setup

```powershell
# Press Ctrl+C in each terminal running:
# - Django server
# - Celery worker
# - Celery beat
# - Reflex

# Stop Redis container
docker stop <redis-container-id>
```

---

## Useful Commands

### Django

```powershell
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

### Docker

```powershell
# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend

# Restart a service
docker-compose restart backend

# Rebuild and restart
docker-compose up -d --build
```

### Testing

```powershell
# Run tests
pytest

# Run with coverage
pytest --cov

# Run specific markers
pytest -m unit
pytest -m integration

# Run in parallel
pytest -n auto
```

---

## Production Deployment

See `README.md` for full production deployment instructions including:
- Building Docker images
- Kubernetes deployment
- CI/CD setup
- Environment configuration

---

## Getting Help

- 📖 **Documentation:** See `README.md` and `PROJECT_SUMMARY.md`
- 🔒 **Security:** See `SECURITY.md`
- 🌿 **Branch Protection:** See `BRANCH_PROTECTION.md`
- 🗄️ **Database:** See `SUPABASE_RLS.md`

---

**Happy coding! 🚀**
