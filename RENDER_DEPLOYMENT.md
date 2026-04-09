# 🚀 RENDER DEPLOYMENT GUIDE

## **STEP 1: Render.com pe Login Karo**
- Open: https://render.com
- Click **Sign in** → **GitHub** se login karo
- (Tere paas pehle se account hai, directly dashboard mein aayega)

---

## **STEP 2: New Web Service Create Karo**

1. **Dashboard** mein click karo **"New +"**
2. Select **"Web Service"**
3. **Connect GitHub Repo** select karo

```
Repository: jwt-oauth-api
(apna GitHub repo select karo)
```

4. **Click "Connect"**

---

## **STEP 3: Service Configuration**

### **Settings ko fill karo:**

| Field | Value |
|-------|-------|
| **Name** | `jwt-oauth-api` |
| **Environment** | `Python 3` |
| **Region** | `Singapore` (fastest for India) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port 8000` |
| **Instance Type** | `Free` (start mein) |

---

## **STEP 4: Environment Variables Set Karo**

**Dashboard mein "Environment" tab khol**

Ye sab variables add karo:

```
SECRET_KEY=<GENERATE NEW - see below>
ENVIRONMENT=production
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
FRONTEND_URL=https://your-frontend.com
GOOGLE_CLIENT_ID=your-google-id
GOOGLE_CLIENT_SECRET=your-google-secret
GITHUB_CLIENT_ID=your-github-id
GITHUB_CLIENT_SECRET=your-github-secret
```

### **NEW SECRET_KEY Generate Karo:**
```bash
# Terminal mein run karo:
python -c "import secrets; print(secrets.token_hex(32))"

# Output:
# a3f7c2e1b9d4a6f8c1e3b5d7a9f2c4e6b8d0a2c4e6f8a0b2c4e6f8a0b2c4

# Ye value .env mein paste karo Render pe
```

---

## **STEP 5: PostgreSQL Database Add Karo**

### **Option A: Render Managed Database (RECOMMENDED)**

1. Go to **Dashboard** → **"New +"** → **"PostgreSQL"**
2. Fill these values:
   ```
   Name: jwt-oauth-api-postgres
   Database: jwt_api_db
   User: api_user
   Region: Singapore (same as web service)
   ```
3. **Create Database**

3. Database create hone ke baad, Render **automatically** ek `DATABASE_URL` set karega
   - **Copy nahi karna manually!** Render khud set kar dega

4. Teri **Web Service ke environment** mein check karo:
   ```
   DATABASE_URL = postgresql://api_user:PASSWORD@HOST:5432/jwt_api_db
   ```
   (Render automatically add kar dega, tujhe bas confirm karna)

---

## **STEP 6: Database Connection Fix (IMPORTANT!)**

Tera `docker-compose.yml` aur `Dockerfile` Docker ke liye hain.  
Render deploy ke liye, edit kar:

### **Create `start.sh` (Render deploy ke liye):**

```bash
#!/bin/bash
# Render deployment script

# Apply migrations
alembic upgrade head

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### **Dockerfile update karo:**

Change **Start Command** from Docker to:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

(Yeh Render dashboard mein set hai, migrations manually run nahi honge)

**Better: Render Events (Pre-deploy hooks) use karo:**

1. Go to **Dashboard** → Web Service
2. Click **"Settings"** → **"Pre-deployment command"**
3. Add: `alembic upgrade head`

---

## **STEP 7: Deploy Karo!**

1. **Go to Web Service** → Click **"Deploy"** button
2. **Watch logs** (real-time mein dikhdega)

```
# Ye dekhai dega:
Building...
Installing dependencies...
Running pre-deployment command...
✓ alembic upgrade head (successful)
Starting application...
Uvicorn running on 0.0.0.0:8000
Application startup complete ✓
```

---

## **STEP 8: Test API**

Jab deployment complete ho:

1. **URL milega:** `https://jwt-oauth-api.onrender.com`

2. **Test karo:**
   ```
   # API Docs
   https://jwt-oauth-api.onrender.com/docs
   
   # Health check
   https://jwt-oauth-api.onrender.com/health
   ```

3. **API test in Swagger UI:**
   - `/auth/signup` - naya user banao
   - `/auth/login` - login karo
   - `/auth/logout` - logout karo

---

## **🔥 COMMON ISSUES & FIX**

### **Issue 1: Deployment fails - "No such file or directory: alembic"**
```
Fix: Add this to "Pre-deployment command":
alembic upgrade head
```

### **Issue 2: Database connection fails**
```
Check:
1. PostgreSQL service is health (dashboard mein check)
2. DATABASE_URL variable is set correctly
3. POSTGRES_PASSWORD matches

Render auto-sets DATABASE_URL when you create database,
bahut rarely manually set karna padta hai.
```

### **Issue 3: ModuleNotFoundError: No module named 'app'"**
```
Fix: Render automatically installs from requirements.txt
Agar problem ho toh ensure karw:
- requirements.txt present hai repo mein ✓
- All dependencies listed hain
```

### **Issue 4: 503 Service Unavailable**
```
Likely: Application still starting
Solution: Wait 30-60 seconds, refresh

Agar baad mein bhi continue ho:
Check logs mein kya error aa rahi hai
```

---

## **📋 COMPLETE CHECKLIST**

```
☐ Render account login
☐ GitHub repo connected
☐ Web Service created
☐ Environment variables set:
   ☐ SECRET_KEY (new one)
   ☐ ENVIRONMENT=production
   ☐ FRONTEND_URL
   ☐ OAuth credentials
☐ PostgreSQL database created
☐ DATABASE_URL auto-set by Render
☐ Pre-deployment command: "alembic upgrade head"
☐ Build Command: "pip install -r requirements.txt"
☐ Start Command: "uvicorn app.main:app --host 0.0.0.0 --port 8000"
☐ Deploy button clicked
☐ Logs check - no errors
☐ Test /health endpoint
☐ Test /docs (Swagger UI)
☐ Test /auth/signup
```

---

## **🎯 NEXT STEPS (Frontend Integration)**

Once API deployed on Render:

1. Update **Frontend FRONTEND_URL** to:
   ```
   FRONTEND_URL=https://jwt-oauth-api.onrender.com
   ```

2. In **frontend .env:**
   ```
   REACT_APP_API_URL=https://jwt-oauth-api.onrender.com
   ```

3. OAuth callbacks:
   - Google: Add `https://jwt-oauth-api.onrender.com/oauth/google/callback`
   - GitHub: Add `https://jwt-oauth-api.onrender.com/oauth/github/callback`

---

## **💡 TIPS**

✅ **Free Tier Works:**
- Tera application free tier pe run hoga
- 1 GB RAM, limited resources
- Good enough for development/testing

✅ **Auto-deploys:**
- Jab tu GitHub mein push karega
- Render automatically deploy kar dega

✅ **Logs Check:**
- Dashboard → Web Service → Logs
- Real-time mein see kar sakte ho

✅ **Restart Service:**
- If connection issue ho
- Dashboard → Settings → "Restart Service"

---

## **❌ DO NOT FORGET**

⚠️ **Never commit .env to GitHub**
```bash
# Check .gitignore
grep ".env" .gitignore  # Should show .env

# If .env is committed:
git rm --cached .env
git commit -m "Remove .env from git"
git push
```

⚠️ **Always use HTTPS callbacks** for OAuth

⚠️ **Generate NEW SECRET_KEY** for production

---

**Ready? Start deploy karo! 🚀**

Koi issue ho toh logs dekh ke batana!
