# 🚀 CheckwiseAI Backend Deployment Guide

## ✅ Fixed Issues
1. ✅ Added `gunicorn==21.2.0` to requirements.txt
2. ✅ Created proper deployment configuration files
3. ✅ Fixed module path (should be `api:app` not `diagnosis.api:app`)

## 📁 Deployment Files Created

### 1. **requirements.txt** (Updated)
```
flask==2.3.3
flask-cors==4.0.0
werkzeug==2.3.7
scikit-learn==1.3.0
pandas==2.0.3
joblib==1.3.2
numpy==1.24.3
gunicorn==21.2.0  ← ADDED
```

### 2. **Procfile** (Heroku/Render.com)
```
web: gunicorn api:app --bind=0.0.0.0:$PORT
```

### 3. **start.sh** (Shell Script)
```bash
#!/bin/bash
gunicorn api:app --bind=0.0.0.0:$PORT
```

### 4. **render.yaml** (Render.com Configuration)
```yaml
services:
  - type: web
    name: checkwise-api
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn api:app --bind=0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.8.10
      - key: PYTHONPATH
        value: .
```

### 5. **runtime.txt** (Python Version)
```
python-3.8.10
```

## 🌐 Platform-Specific Deployment Commands

### **Render.com**
1. Connect your GitHub repository
2. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn api:app --bind=0.0.0.0:$PORT`
   - **Environment**: Python 3.8

### **Heroku**
```bash
# Deploy to Heroku
git add .
git commit -m "Fix deployment configuration"
git push heroku main

# Or if main branch
git push heroku main:main
```

### **Vercel** (Serverless)
The existing `vercel.json` should work:
```json
{
  "version": 2,
  "builds": [{"src": "api.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "api.py"}]
}
```

### **Railway**
```bash
# Railway deployment
railway login
railway new
railway connect
git push origin main
```

## 🔧 Environment Variables
Set these in your deployment platform:
- `PORT`: Automatically set by most platforms
- `PYTHON_VERSION`: 3.8.10
- `PYTHONPATH`: . (current directory)

## 🧪 Test Deployment
After deployment, test these endpoints:
- `GET /` - API information
- `GET /api/health` - Health check
- `POST /api/predict` - AI prediction (with CBC data)

## 📊 Sample Test Request
```bash
curl -X POST https://your-api-url.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "WBC": 7.5,
    "RBC": 4.8,
    "HGB": 14,
    "HCT": 42,
    "PLT": 250,
    "Age": 35,
    "Gender": 1
  }'
```

## ⚠️ Important Notes
1. **Model Files**: Ensure `cbc_disease_model.joblib` (94.6MB) and `disease_label_encoder.joblib` are included
2. **Memory**: The AI model requires ~100MB RAM
3. **Cold Start**: First request may take 2-3 seconds (model loading)
4. **File Size**: Model files are large, some platforms have limits

## 🎯 Next Steps
1. Push the updated code to your repository
2. Redeploy on your platform
3. Test the `/api/health` endpoint
4. Update frontend API URL if needed