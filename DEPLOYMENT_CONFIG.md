# CheckwiseAI - Complete Deployment Configuration Guide

## 🚀 Frontend Deployment - Netlify Configuration

### 1. Netlify Site Settings
- **Site Name**: `check-wise` (or your preferred name)
- **Build Command**: `npm run build`
- **Publish Directory**: `dist`
- **Node Version**: `18.x` or `20.x`

### 2. Environment Variables (Netlify Dashboard → Site Settings → Environment Variables)
```
VITE_API_URL=https://diagnosisai.onrender.com
```

### 3. netlify.toml Configuration
**File**: `frontend/netlify.toml`
```toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.js"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.css"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```

### 4. package.json Scripts (Verify these exist)
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

---

## ⚙️ Backend Deployment - Render Configuration

### 1. Render Service Settings
- **Service Type**: Web Service
- **Environment**: Python 3.9.x
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn main:app`
- **Instance Type**: Free (or paid for better performance)

### 2. Environment Variables (Render Dashboard → Environment)
```
PYTHON_VERSION=3.9.19
FLASK_APP=backend.api
FLASK_ENV=production
```

### 3. requirements.txt (Critical for numpy compatibility)
**File**: `requirements.txt`
```txt
flask==2.3.3
flask-cors==4.0.0
werkzeug==2.3.7
scikit-learn==1.2.2
pandas==2.0.3
joblib==1.2.0
numpy==1.24.3
gunicorn==21.2.0
```

### 4. main.py (Deployment Entry Point)
**File**: `main.py`
```python
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from api import app

# For deployment platforms
application = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

### 5. render.yaml (Optional - Infrastructure as Code)
**File**: `render.yaml`
```yaml
services:
  - type: web
    name: checkwise-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn main:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.19
      - key: FLASK_ENV
        value: production
```

---

## 📁 Required File Structure
```
CheckwiseAI/
├── main.py                          # Render entry point
├── requirements.txt                 # Python dependencies
├── render.yaml                      # Optional Render config
├── cbc_disease_model.joblib        # AI model (root)
├── disease_label_encoder.joblib    # Label encoder (root)
├── backend/
│   ├── api.py                      # Flask API
│   ├── cbc_disease_model.joblib    # AI model (backup)
│   └── disease_label_encoder.joblib # Label encoder (backup)
└── frontend/
    ├── netlify.toml                # Netlify config
    ├── package.json                # Node dependencies
    ├── vite.config.js              # Vite config
    └── src/
        └── components/
            └── DiagnosisForm.jsx   # Main component
```

---

## 🔧 Step-by-Step Deployment Process

### Netlify Deployment
1. **Connect Repository**: Link your GitHub repo to Netlify
2. **Set Build Settings**:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`
3. **Add Environment Variables**: `VITE_API_URL=https://diagnosisai.onrender.com`
4. **Deploy**: Netlify will auto-deploy on git push

### Render Deployment
1. **Connect Repository**: Link your GitHub repo to Render
2. **Service Settings**:
   - Root Directory: Leave blank (uses repo root)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app`
3. **Environment Variables**: Add `PYTHON_VERSION=3.9.19`
4. **Deploy**: Render will auto-deploy on git push

---

## 🐛 Common Issues & Solutions

### Issue 1: "numpy._core" Error
**Solution**: Use exact versions in requirements.txt above

### Issue 2: CORS Errors
**Solution**: Ensure backend has `flask-cors` configured:
```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
```

### Issue 3: Model Files Not Found
**Solution**: Keep model files in both root AND backend directories

### Issue 4: Build Failures
**Frontend**: Check Node.js version (use 18.x)
**Backend**: Use Python 3.9.x, not 3.10+

---

## ✅ Verification Checklist

### Before Deployment
- [ ] All required files are in correct locations
- [ ] Environment variables are set
- [ ] Dependencies versions match exactly
- [ ] Model files exist in both locations

### After Deployment
- [ ] Frontend loads without errors
- [ ] Backend health check returns 200
- [ ] API endpoints respond correctly
- [ ] Models load successfully
- [ ] Predictions work end-to-end

---

## 🔗 Quick Links
- **Frontend URL**: https://check-wise.netlify.app
- **Backend URL**: https://diagnosisai.onrender.com
- **Health Check**: https://diagnosisai.onrender.com/api/health
- **API Parameters**: https://diagnosisai.onrender.com/api/parameters