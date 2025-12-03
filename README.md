# Barbershop CRM - Enterprise-Grade Multi-Tenant System

A production-ready Barbershop CRM built with **Django**, **Supabase**, **SQLAlchemy**, **Reflex**, **Kubernetes**, **Redis**, **Celery**, and **CI/CD Pipeline**.

---

## 📚 Documentation Index

**🚀 New to this project? Start here:**

1. **[QUICKSTART.md](QUICKSTART.md)** ⭐ - Get up and running in 10 minutes
2. **[COMPLETE_OVERVIEW.md](COMPLETE_OVERVIEW.md)** - Full project summary
3. **[TESTING_SECURITY.md](TESTING_SECURITY.md)** - Testing & security details

**📖 Additional Documentation:**

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - What's been built
- **[SECURITY.md](SECURITY.md)** - Security policy
- **[BRANCH_PROTECTION.md](BRANCH_PROTECTION.md)** - GitHub setup guide
- **[SUPABASE_RLS.md](SUPABASE_RLS.md)** - Database RLS policies

---

## 🎯 Quick Start

```powershell
# 1. Setup Supabase (get credentials from supabase.com)
# 2. Update backend/.env with your credentials
# 3. Start the application

# Option A: Docker Compose (Recommended)
docker-compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser

# Option B: Quick Start Script
.\start.ps1
```

**Access:** http://localhost:8000 (API) | http://localhost:8000/admin (Admin)

**Full instructions:** See [QUICKSTART.md](QUICKSTART.md)

---

## 🏗️ Architecture

- **Monolithic Backend**: Django REST Framework
- **Database**: Supabase (PostgreSQL) with Row Level Security (RLS)
- **ORM**: SQLAlchemy + Django ORM
- **Frontend**: Reflex (Python-based reactive UI)
- **Cache & Queue**: Redis
- **Task Queue**: Celery + Celery Beat
- **Monitoring**: Flower
- **Container Orchestration**: Kubernetes (K8s)
- **CI/CD**: GitHub Actions

## 📊 Database Schema

### Tables

- **businesses** - Multi-tenant business entities
- **staff** - Barbers, stylists, managers
- **customers** - Client management with visit tracking
- **services** - Service catalog with pricing
- **appointments** - Booking system with status tracking

All tables include `business_id` for multi-tenant isolation via Supabase RLS.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Kubernetes cluster (for production)
- Supabase account

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo>
cd barber-crm
```

2. **Configure environment variables**
```bash
cd backend
cp .env.example .env
# Edit .env with your Supabase credentials
```

3. **Run with Docker Compose**
```bash
docker-compose up -d
```

Services will be available at:
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- Flower (Celery monitoring): http://localhost:5555
- Redis: localhost:6379

### Manual Setup (Backend)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Manual Setup (Frontend)

```bash
cd frontend
python -m venv .venv
.venv\Scripts\activate  # Windows

pip install reflex
reflex run
```

## 🔐 Supabase Setup

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Get your connection string and API keys

### 2. Enable RLS Policies

```sql
-- Enable RLS on all tables
ALTER TABLE businesses ENABLE ROW LEVEL SECURITY;
ALTER TABLE staff ENABLE ROW LEVEL SECURITY;
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE services ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;

-- Example policy for customers table
CREATE POLICY "business_can_access_own_rows" 
ON customers 
FOR SELECT 
USING (business_id = auth.jwt()->>'business_id');

-- Repeat for INSERT, UPDATE, DELETE operations
```

### 3. Update .env file

```env
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_SERVICE_KEY=your_service_key_here
DATABASE_URL=postgresql://postgres:password@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
```

## 🎯 API Endpoints

### Authentication
- `POST /api-auth/login/` - Login
- `POST /api-auth/logout/` - Logout

### Resources
- `GET/POST /api/businesses/` - Business CRUD
- `GET/POST /api/staff/` - Staff management
- `GET/POST /api/customers/` - Customer management
- `GET/POST /api/services/` - Service catalog
- `GET/POST /api/appointments/` - Appointment booking

### Health Checks
- `GET /healthz/` - Basic health check
- `GET /livez/` - Liveness probe
- `GET /readyz/` - Readiness probe (checks DB + Redis)

## ☸️ Kubernetes Deployment

### 1. Build and Push Docker Image

```bash
docker build -t your-registry/barber-crm-backend:latest ./backend
docker push your-registry/barber-crm-backend:latest
```

### 2. Update K8s Secrets

```bash
# Edit k8s/secrets.yaml with your actual credentials
kubectl apply -f k8s/secrets.yaml
```

### 3. Deploy to Kubernetes

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/celery.yaml
kubectl apply -f k8s/ingress.yaml
```

### 4. Verify Deployment

```bash
kubectl get pods -n barber-crm
kubectl get svc -n barber-crm
kubectl get ingress -n barber-crm
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Tests** - Runs pytest with coverage
2. **Builds** - Creates Docker image
3. **Pushes** - Uploads to container registry
4. **Deploys** - Updates K8s deployment

### Required Secrets

Add these to your GitHub repository secrets:

- `KUBECONFIG` - Base64 encoded kubeconfig file
- `GITHUB_TOKEN` - Automatically provided

## 📦 Project Structure

```
barber-crm/
├── backend/
│   ├── apps/
│   │   ├── businesses/
│   │   ├── staff/
│   │   ├── customers/
│   │   ├── services/
│   │   └── appointments/
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── celery.py
│   │   └── health.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   └── (Reflex app)
├── k8s/
│   ├── namespace.yaml
│   ├── secrets.yaml
│   ├── configmap.yaml
│   ├── backend.yaml
│   ├── celery.yaml
│   ├── redis.yaml
│   └── ingress.yaml
├── .github/
│   └── workflows/
│       └── ci-cd.yml
└── docker-compose.yml
```

## 🛠️ Tech Stack Details

### Backend
- **Django 5.0+** - Web framework
- **Django REST Framework** - API
- **SQLAlchemy** - Advanced ORM layer
- **Celery** - Async task processing
- **Redis** - Caching & message broker
- **Gunicorn** - WSGI server

### Frontend
- **Reflex** - Python-based reactive UI framework

### Infrastructure
- **Docker** - Containerization
- **Kubernetes** - Orchestration
- **GitHub Actions** - CI/CD
- **Nginx Ingress** - Load balancing

### Database
- **Supabase (PostgreSQL)** - Managed database with RLS

## 🔧 Development Commands

### Django
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run dev server
python manage.py runserver
```

### Celery
```bash
# Start worker
celery -A config worker --loglevel=info

# Start beat scheduler
celery -A config beat --loglevel=info

# Start Flower monitoring
celery -A config flower
```

### Docker
```bash
# Build
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📈 Monitoring

- **Flower**: http://localhost:5555 - Celery task monitoring
- **Django Admin**: http://localhost:8000/admin - Database management
- **Health Endpoints**: `/healthz/`, `/livez/`, `/readyz/`

## 🔒 Security Features

- ✅ Row Level Security (RLS) via Supabase
- ✅ Multi-tenant data isolation
- ✅ Environment-based secrets
- ✅ K8s secrets management
- ✅ CORS protection
- ✅ CSRF protection
- ✅ Authentication required for all API endpoints

## 📝 MVP Features

### Backend ✅
- [x] Business CRUD with multi-tenant support
- [x] Staff management with roles
- [x] Customer tracking with visit history
- [x] Service catalog
- [x] Appointment booking system
- [x] Supabase integration
- [x] RLS-enforced isolation
- [x] REST API with DRF
- [x] Health check endpoints

### Frontend 🚧
- [ ] Dashboard UI
- [ ] Customer list + add/edit
- [ ] Appointment scheduler
- [ ] Staff management
- [ ] Service management

### DevOps ✅
- [x] Docker containerization
- [x] Docker Compose for local dev
- [x] Kubernetes manifests
- [x] Horizontal Pod Autoscaler
- [x] CI/CD pipeline
- [x] Health probes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

MIT License

## 👨‍💻 Author

Built with ❤️ for modern barbershop management
