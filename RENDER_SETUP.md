# Render.com Manual Setup Instructions

## 🚨 Critical: Manual Dashboard Configuration Required

Since Render.com is not detecting the `render.yaml` file properly, you **must** configure the deployment manually in the dashboard:

### Step 1: Go to Render.com Dashboard
1. Log in to [render.com](https://render.com)
2. Find your CheckwiseAI service
3. Click on the service name

### Step 2: Update Build & Deploy Settings
Navigate to **Settings** → **Build & Deploy** and set:

**Root Directory:** ` ` (leave empty - use root)

**Build Command:**
```bash
pip install --upgrade pip && pip install -r requirements.txt && python build.py
```

**Start Command:**
```bash
gunicorn main:app --bind=0.0.0.0:$PORT
```

### Step 3: Environment Variables
Set these in **Settings** → **Environment**:
- `PYTHON_VERSION` = `3.9`

### Step 4: Deploy
Click **"Manual Deploy"** → **"Deploy Latest Commit"**

## 🔍 Troubleshooting

If build still fails:
1. Check the build logs for the exact error
2. Ensure the repository is properly connected
3. Verify all files are committed and pushed
4. Try clearing the build cache in Render dashboard

## ✅ Expected Build Process
```
1. Clone repository ✅
2. Find requirements.txt in root ✅ 
3. Install dependencies ✅
4. Run build.py (copy model files) ✅
5. Start with gunicorn main:app ✅
```