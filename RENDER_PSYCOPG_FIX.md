# Render Deployment Fix - psycopg v3 Driver Detection

## ❌ Problem
Render deployment failing with:
```
ModuleNotFoundError: No module named 'psycopg2'
```

Even though we installed `psycopg[binary]==3.1.18` (psycopg v3), SQLAlchemy was still trying to use psycopg2.

---

## ✅ Solution: Database URL Scheme Update

### The Issue
SQLAlchemy by default tries to import `psycopg2` when it sees:
```
postgresql://user:password@host/db
```

But we're using **psycopg v3** (not v2), so we need to explicitly tell SQLAlchemy which driver to use.

### The Fix
Change the DATABASE_URL scheme from:
```
postgresql://...
```

To:
```
postgresql+psycopg://...
```

This explicitly tells SQLAlchemy to use psycopg (v3) driver.

---

## 🔧 Changes Required on Render

### Step 1: Update Render Environment Variable
1. Go to **Render Dashboard** → Your Service
2. Click **Settings** → **Environment**
3. Find variable `DATABASE_URL`
4. Change from:
   ```
   postgresql://postgres.qkvqlqpswqjlnefgwqzf:dn5B4aBWuL6DoF7O@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres?sslmode=require
   ```
   To:
   ```
   postgresql+psycopg://postgres.qkvqlqpswqjlnefgwqzf:dn5B4aBWuL6DoF7O@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres?sslmode=require
   ```
   
**Just add `+psycopg` after `postgresql`!**

### Step 2: Manual Deploy
1. Go to **Render Dashboard** → Service
2. Click **Manual Deploy**
3. Check logs for successful startup

---

## ✅ Why This Works

| Driver | URL Scheme | Version | Status |
|--------|-----------|---------|--------|
| psycopg2 (old) | `postgresql://` | v2 | ❌ Not installed |
| psycopg (new) | `postgresql+psycopg://` | v3 | ✅ Installed |

When you use `postgresql+psycopg://`, SQLAlchemy:
1. Knows you want psycopg (v3)
2. Won't try to import psycopg2
3. Uses modern async-capable driver

---

## 🧪 Local Testing

Already verified locally:
```
✓ Config loaded
✓ Database engine with psycopg v3  
✓ App started with 22 endpoints
```

---

## 📝 Summary of all fixes

```
✅ SQLAlchemy 2.0.49 - Latest stable
✅ psycopg[binary]==3.1.18 - Modern PostgreSQL driver
✅ Python 3.12 - Stable LTS version
✅ DATABASE_URL with postgresql+psycopg:// - Explicit driver selection
✅ .python-version - Force Python 3.12 on Render
```

---

## 🚀 Next Steps

1. **Update Render DATABASE_URL** (add `+psycopg`)
2. **Manual Deploy** on Render
3. **Check logs** - should see successful startup
4. **Test `/health` endpoint** - should return `{"status": "ok"}`

Once you update the env var on Render and redeploy, everything should work! 🎉
