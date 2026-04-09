# ⚡ RENDER DEPLOYMENT - QUICK REFERENCE

## 🚀 5-MINUTE SETUP

### **1️⃣ New Web Service**
```
Dashboard → New + → Web Service
Select: Git repository (jwt-oauth-api)
```

### **2️⃣ Basic Settings**
```
Name:           jwt-oauth-api
Environment:    Python 3
Region:         Singapore
Build:          pip install -r requirements.txt
Start:          uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### **3️⃣ Environment Variables** (Dashboard → Environment)
```
SECRET_KEY                    = [GENERATE NEW]
ENVIRONMENT                   = production
ACCESS_TOKEN_EXPIRE_MINUTES   = 15
REFRESH_TOKEN_EXPIRE_DAYS     = 7
FRONTEND_URL                  = https://your-domain.com
GOOGLE_CLIENT_ID              = [from Google Cloud]
GOOGLE_CLIENT_SECRET          = [from Google Cloud]
GITHUB_CLIENT_ID              = [from GitHub OAuth]
GITHUB_CLIENT_SECRET          = [from GitHub OAuth]
```

### **4️⃣ Database Setup**
```
Dashboard → New + → PostgreSQL
Name:   jwt-oauth-api-postgres
DB:     jwt_api_db
User:   api_user
Region: Singapore (SAME as Web Service!)
```
**Render automatically sets `DATABASE_URL` ✅**

### **5️⃣ Pre-deployment Command**
```
Settings → Pre-deployment command:
alembic upgrade head
```

### **6️⃣ Deploy**
```
Click: Deploy button
Wait: 2-3 minutes
Check: Logs for "Application startup complete ✓"
```

---

## ✅ TEST

```
https://jwt-oauth-api.onrender.com/health
https://jwt-oauth-api.onrender.com/docs
```

---

## 🔑 Generate SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 📝 MIGRATION COMMAND

Automatic via pre-deployment command:
```
alembic upgrade head
```

---

## ⚠️ IMPORTANT

- ✅ PostgreSQL region = Web Service region (Singapore!)
- ✅ Generate NEW SECRET_KEY (old one exposed in git)
- ✅ .env is in .gitignore (not in repo)
- ✅ OAuth credentials from Google Cloud Console
- ✅ GitHub OAuth credentials from GitHub Settings
