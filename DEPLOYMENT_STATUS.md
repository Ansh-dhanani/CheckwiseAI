# 🚨 CheckwiseAI Deployment Issues & Solutions

## Current Status
- ✅ **Frontend**: Deployed on Netlify at `https://check-wise.netlify.app`
- ❌ **Backend**: Failing to deploy on Render.com (requirements.txt error)
- ❌ **Connection**: Frontend can't connect to backend API

## 🔧 Issues Found

### 1. Backend Deployment Failure
**Problem**: Render.com build fails with "Could not open requirements file"
**Root Cause**: Dashboard settings not using render.yaml configuration

### 2. Frontend API URL Configuration
**Problem**: Frontend tries to connect to `localhost:5000` instead of deployed backend
**Root Cause**: Missing `VITE_API_URL` environment variable in Netlify

## ✅ Solutions Applied

### Backend Fix (Render.com)
1. **Manual Dashboard Configuration Required**:
   - Build Command: `pip install --upgrade pip && pip install -r requirements.txt && python build.py`
   - Start Command: `gunicorn main:app --bind=0.0.0.0:$PORT`
   - Environment: `PYTHON_VERSION=3.9`

### Frontend Fix (Netlify)
1. **Updated `netlify.toml`** with correct API URL:
   ```toml
   [build.environment]
   VITE_API_URL = "https://checkwise-ai.onrender.com"
   ```

2. **Created environment files**:
   - `.env.production` - Production API URL
   - `.env.example` - Development template

## 🎯 Next Steps

### Step 1: Fix Backend Deployment
1. Go to [render.com](https://render.com) dashboard
2. Update your CheckwiseAI service settings manually
3. Deploy latest commit

### Step 2: Update Frontend
1. Commit the frontend changes
2. Push to trigger Netlify rebuild
3. Verify API connection

### Step 3: Test End-to-End
Once both are deployed:
- Backend should be at: `https://checkwise-ai.onrender.com`
- Frontend should connect automatically

## 🔍 Expected URLs
- **Frontend**: `https://check-wise.netlify.app`
- **Backend**: `https://checkwise-ai.onrender.com`
- **API Endpoints**:
  - `GET /api/parameters`
  - `POST /api/validate`
  - `POST /api/predict`

## 🚀 Quick Test
Once backend is deployed, test these URLs:
- `https://checkwise-ai.onrender.com/api/parameters`
- Should return JSON with CBC parameter list

---
*Fix Status: Backend needs manual dashboard configuration, Frontend configured for production*