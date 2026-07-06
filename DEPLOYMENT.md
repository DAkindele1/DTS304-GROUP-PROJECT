# SIBAS Deployment Guide - Streamlit Cloud

## 📋 Prerequisites

Before deploying, ensure you have:
- [ ] GitHub account
- [ ] Project pushed to GitHub
- [ ] Cloud database setup (PostgreSQL)
- [ ] Streamlit account (sign up at [streamlit.io/cloud](https://streamlit.io/cloud))

---

## 🚀 Step-by-Step Deployment

### 1. **Set Up a Cloud Database**

Choose one of these options:

#### Option A: Supabase (Recommended - Free tier available)
1. Go to [supabase.com](https://supabase.com) and sign up
2. Create a new project
3. Get your connection details:
   - Host: `Project URL` → copy the domain
   - Port: `5432` (default)
   - Database: `postgres`
   - User: `postgres`
   - Password: Copy from project settings

#### Option B: AWS RDS / Azure Database / Other
- Set up PostgreSQL database
- Note the connection credentials

#### Option C: Keep Using Local Database (for testing only)
- Database must be running and accessible via the internet (NOT recommended for production)

---

### 2. **Deploy to Streamlit Cloud**

1. **Go to [streamlit.io/cloud](https://streamlit.io/cloud)**
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Fill in the deployment form:**
   - **Repository:** Select your GitHub repo
   - **Branch:** `main` (or your default branch)
   - **Main file path:** `SIBAS/app/main.py`
5. **Click "Deploy"** → Streamlit Cloud will automatically install dependencies from `requirements.txt`

---

### 3. **Add Secrets to Streamlit Cloud**

After deployment completes:

1. **In your app**, click the **☰ menu** (top right)
2. **Select "Settings"**
3. **Click "Secrets"** in the left sidebar
4. **Paste your database credentials** in TOML format:

```toml
DB_NAME = "your_database_name"
DB_USER = "your_database_user"
DB_PASSWORD = "your_secure_password"
DB_HOST = "your_database_host.com"
DB_PORT = "5432"
```

5. **Save** and the app will automatically redeploy

---

### 4. **Test Your Deployment**

1. Wait for the app to load
2. Use the credentials from `CREDENTIALS_QUICK_REF.txt` to log in
3. Test all features:
   - [ ] Login works
   - [ ] Student dashboard displays data
   - [ ] Attendance upload works
   - [ ] Reports generate correctly

---

## 🔐 Secrets Management

### Local Development
- Secrets are stored in `.streamlit/secrets.toml`
- This file is **already gitignored** (won't be committed)
- Keep your local credentials safe

### Streamlit Cloud
- Secrets are managed via the web interface
- **Never commit secrets to GitHub**
- Each app environment has separate secrets

---

## 📊 Connecting the Database

Your code now uses Streamlit Secrets to connect. The connection string is built from:
- `DB_NAME` - Database name
- `DB_USER` - Database username  
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database hostname
- `DB_PORT` - Database port (usually 5432)

---

## 🐛 Troubleshooting

### "Database Connection Failure" Error
- [ ] Check if DB credentials in Secrets are correct
- [ ] Verify database is running and accessible
- [ ] For Supabase: ensure "SSL mode" is enabled for remote connections

### App Won't Deploy
- [ ] Check `requirements.txt` syntax
- [ ] Ensure `SIBAS/app/main.py` exists
- [ ] Check Streamlit Cloud logs for error messages

### Secrets Not Working
- [ ] Go to Settings → Secrets
- [ ] Verify all 5 variables are present: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- [ ] Redeploy the app after adding/updating secrets

---

## 📝 Next Steps

1. **Monitor your app** - Check logs if issues arise
2. **Set up backups** for your database
3. **Configure custom domain** (optional) in Streamlit Cloud settings
4. **Enable auto-deploys** from GitHub (optional)

---

## 🆘 Need Help?

- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- [Streamlit Secrets Docs](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/secrets-management)
- [Supabase Getting Started](https://supabase.com/docs/guides/getting-started)
