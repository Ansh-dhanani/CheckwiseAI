# CheckwiseAI Deployment Troubleshooting Guide

## 🚨 Common Deployment Issues & Solutions

### 1. ModuleNotFoundError: No module named 'diagnosis'

**Problem**: Deployment platform incorrectly references `diagnosis.api:app`

**Solutions**:
- ✅ Use `main:app` instead of `diagnosis.api:app` in deployment commands
- ✅ Ensure all deployment configs reference the correct module path
- ✅ Use the provided `main.py` entry point

### 2. gunicorn: command not found

**Problem**: Gunicorn not installed in deployment environment

**Solutions**:
- ✅ Added `gunicorn==21.2.0` to `requirements.txt`
- ✅ Use `python -m gunicorn` if direct command fails
- ✅ Verify requirements.txt is in the correct location

### 3. AI Model Files Not Found

**Problem**: Large model files (.joblib) not accessible during deployment

**Solutions**:
- ✅ Run `python build.py` to copy model files to root
- ✅ Ensure both model files are in the root directory:
  - `cbc_disease_model.joblib` (94.6MB)
  - `disease_label_encoder.joblib`
- ✅ Check deployment platform file size limits

## 🔧 Quick Fix Commands

### For Render.com:
```bash
# Ensure these files exist in root:
- main.py
- requirements.txt
- render.yaml
- cbc_disease_model.joblib
- disease_label_encoder.joblib

# Build Command: pip install -r requirements.txt && python build.py
# Start Command: gunicorn main:app --bind=0.0.0.0:$PORT
```

### For Heroku:
```bash
# Ensure these files exist in root:
- main.py
- requirements.txt
- Procfile
- cbc_disease_model.joblib
- disease_label_encoder.joblib

# Procfile: web: gunicorn main:app --bind=0.0.0.0:$PORT
```

### For Vercel:
```bash
# Use the existing vercel.json in backend/
# Ensure model files are accessible via build script
```

## 🔍 Debugging Steps

1. **Check File Structure**:
   ```
   CheckwiseAI/
   ├── main.py ✅
   ├── requirements.txt ✅
   ├── build.py ✅
   ├── cbc_disease_model.joblib ✅
   ├── disease_label_encoder.joblib ✅
   └── backend/
       └── api.py ✅
   ```

2. **Verify Dependencies**:
   - Python 3.9+
   - All packages in requirements.txt
   - Gunicorn for WSGI server

3. **Test Locally**:
   ```bash
   python build.py
   gunicorn main:app --bind=0.0.0.0:5000
   ```

## 📋 Deployment Checklist

- [ ] Run `python build.py` to copy model files
- [ ] Verify `main.py` exists in root
- [ ] Check `requirements.txt` includes gunicorn
- [ ] Ensure deployment platform uses `main:app`
- [ ] Confirm Python 3.9+ runtime
- [ ] Test endpoints after deployment

## 🎯 Platform-Specific Notes

### Render.com
- Use `render.yaml` configuration
- Set Python version to 3.9.0
- Build command includes `python build.py`

### Heroku
- Use `Procfile` configuration
- Add `runtime.txt` for Python version
- Ensure model files < 500MB limit

### Vercel
- Use serverless functions approach
- Model files must be optimized for cold starts
- Consider splitting into microservices

## 📞 Support

If issues persist:
1. Check deployment platform logs
2. Verify all files are uploaded correctly
3. Test the API endpoints manually
4. Review platform-specific documentation

---
*Last updated: September 2024*