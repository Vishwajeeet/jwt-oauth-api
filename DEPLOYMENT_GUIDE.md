# 🚀 JWT OAuth API - Complete Deployment Guide

## 📋 Table of Contents
1. [Local Development](#local-development)
2. [Database Setup (Supabase)](#database-setup)
3. [Render Deployment](#render-deployment)
4. [Critical Fixes Applied](#critical-fixes-applied)
5. [Troubleshooting](#troubleshooting)

---

## 🏠 Local Development

### Prerequisites
- Python 3.12+
- PostgreSQL connection (Supabase)
- Virtual environment

### Setup

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure .env file
cp .env.example .env  # Edit with your credentials

# 4. Run migrations
alembic upgrade head

# 5. Start development server
uvicorn app.main:app --reload
```

**Server running at:** `http://localhost:8000`  
**API Docs:** `http://localhost:8000/docs`  
**ReDoc:** `http://localhost:8000/redoc`

---

## 🗄️ Database Setup (Supabase)

### Step 1: Get Supabase Connection String
1. Go to [supabase.com](https://supabase.com)
2. Create project → Copy Connection String
3. Ensure `?sslmode=require` is in the URL

### Step 2: Update .env
```env
DATABASE_URL=postgresql+psycopg://user:password@aws-*.pooler.supabase.com:5432/postgres?sslmode=require
```

**⚠️ CRITICAL:** Use `postgresql+psycopg://` (not `postgresql://`)  
This tells SQLAlchemy to use psycopg v3 driver.

### Step 3: Run Migrations
```bash
alembic upgrade head
```

---

## 🎯 Render Deployment

### Step 1: Configure on Render Dashboard

1. **Create Web Service** on [render.com](https://render.com)
2. Connect GitHub repository
3. Set **Environment** to `docker`

### Step 2: Set Environment Variables

Go to **Settings → Environment** and add:

```
DATABASE_URL=postgresql+psycopg://user:password@aws-*.pooler.supabase.com:5432/postgres?sslmode=require
SECRET_KEY=<generate-with: python -c "import secrets; print(secrets.token_hex(32))">
ENVIRONMENT=production
FRONTEND_URL=https://your-domain.com
GOOGLE_CLIENT_ID=<your-value>
GOOGLE_CLIENT_SECRET=<your-value>
GITHUB_CLIENT_ID=<your-value>
GITHUB_CLIENT_SECRET=<your-value>
```

### Step 3: Deploy

1. Render auto-deploys from GitHub on push
2. Or manually: **Service → Manual Deploy**
3. Check logs for successful build

### Step 4: Verify

```bash
# Test health endpoint
curl https://your-service.render.com/health

# Should return:
# {"status": "ok", "message": "JWT OAuth API is running"}
```

---

## ✅ Critical Fixes Applied

### 1. ✅ Config Indentation & Validation
**File:** `app/config.py`

**Issue:** Validator decorator not properly indented + extra env vars rejected

**Fix:**
```python
@field_validator("DATABASE_URL")
@classmethod
def assemble_db_connection(cls, v: PostgresDsn) -> str:
    return str(v)

class Config:
    env_file = ".env"
    extra = "ignore"  # Allow unused env vars
```

---

### 2. ✅ Database Connection Pooling
**File:** `app/database.py`

**Issue:** Generic pooling config doesn't work well with Supabase

**Fix:**
```python
if settings.ENVIRONMENT == "production":
    # Production: Conservative pooling for Supabase limits
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,     # Validate connections
        pool_recycle=3600,      # Recycle hourly
        echo=False
    )
else:
    # Development: Simple null pool
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=NullPool,
        echo=True
    )
```

---

### 3. ✅ Python 3.12 Enforcement
**File:** `Dockerfile` + `.python-version`

**Issue:** Render was using Python 3.14 (too new, unstable)

**Fix:**
- Dockerfile: `FROM python:3.12-slim`
- Created `.python-version` file with `3.12.0`

---

### 4. ✅ psycopg v3 Driver
**File:** `requirements.txt`

**Issue:** psycopg2-binary not compatible with Python 3.14

**Fix:**
```
psycopg[binary]==3.1.18  # Modern PostgreSQL driver with async support
sqlalchemy==2.0.49       # Latest stable SQLAlchemy
```

---

### 5. ✅ Database URL Scheme
**File:** `.env`

**Issue:** SQLAlchemy tried to load psycopg2 despite psycopg v3 installed

**Fix:** Change URL scheme from:
```
postgresql://user:password@host/db
```

To:
```
postgresql+psycopg://user:password@host/db
```

This explicitly tells SQLAlchemy to use psycopg (v3) driver.

---

### 6. ✅ Alembic Startup Script
**File:** `Dockerfile`

**Issue:** Migrations and app startup needed proper error handling

**Fix:**
```dockerfile
RUN echo '#!/bin/sh\nset -e\necho "Running database migrations..."\nalembic upgrade head\necho "Starting application on port ${PORT:-8000}..."\nexec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
```

---

### 7. ✅ Docker Compose for Development
**File:** `docker-compose.yml`

**Issue:** Local PostgreSQL not needed (using Supabase)

**Fix:** Removed local PostgreSQL service, kept only API service that connects to Supabase

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Suite
```bash
pytest tests/test_auth.py -v
pytest tests/test_oauth.py -v
pytest tests/test_users.py -v
pytest tests/test_tasks.py -v
```

### Test Coverage
```bash
pytest --cov=app tests/
```

**Current Status:** 20 tests passing ✅

---

## 🔒 Security Checklist

- [x] CORS configured for specific domains (not wildcard)
- [x] Passwords validated with 8+ chars, uppercase, digits
- [x] JWT tokens with expiration (15 min access, 7 day refresh)
- [x] Rate limiting on sensitive endpoints
- [x] SSL/TLS enforced via `?sslmode=require`
- [x] Non-root user in Docker
- [x] Health checks configured
- [x] No credentials in code (uses .env)

---

## 📊 Tech Stack

| Component | Version | Status |
|-----------|---------|--------|
| Python | 3.12 LTS | ✅ |
| FastAPI | 0.111.0 | ✅ |
| SQLAlchemy | 2.0.49 | ✅ |
| psycopg | 3.1.18 | ✅ |
| Alembic | 1.13.1 | ✅ |
| Uvicorn | 0.29.0 | ✅ |
| Pydantic | 2.13.0 | ✅ |
| PostgreSQL (Supabase) | Latest | ✅ |

---

## 🛠️ Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'psycopg2'`
**Fix:** Ensure DATABASE_URL uses `postgresql+psycopg://` scheme

### Issue: Database connection refused
**Fix:** Verify DATABASE_URL in Render environment variables

### Issue: Render deployment fails
**Steps:**
1. Check Render logs: **Dashboard → Logs**
2. Verify all env variables set
3. Ensure `.env` file has `?sslmode=require`
4. Manual deploy: **Service → Manual Deploy**

### Issue: Alembic migrations fail
**Fix:** Run locally first to test:
```bash
alembic upgrade head
```

### Issue: Port already in use
**Fix:** Render sets PORT automatically. Don't hardcode port numbers.

---

## 📸 Quick Reference

### Health Check
```bash
curl http://localhost:8000/health
```

### API Documentation
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Database Migrations
```bash
# View current state
alembic current

# View migration history
alembic history

# Generate migration from model changes
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### Environment Variables
```bash
# Generate random SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Test database connection
alembic upgrade head
```

---

## 📝 Key Files

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI app setup |
| `app/config.py` | Environment variables |
| `app/database.py` | SQLAlchemy engine |
| `alembic/env.py` | Migration configuration |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container configuration |
| `docker-compose.yml` | Development environment |
| `render.yaml` | Render deployment config |
| `.python-version` | Python version constraint |

---

## 🔗 Resources

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)
- [Supabase Docs](https://supabase.com/docs)
- [Render Docs](https://render.com/docs)
- [psycopg v3](https://www.psycopg.org/psycopg3/)

---

## ✉️ Support

For issues:
1. Check logs: `docker logs` or Render dashboard
2. Verify environment variables
3. Test locally first: `uvicorn app.main:app --reload`
4. Check database connection: `alembic upgrade head`

---

**Last Updated:** April 13, 2026  
**Status:** All systems operational ✅
