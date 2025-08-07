# CheckWise Deployment Guide

## 🚀 Deploy to Netlify (Frontend) + Vercel (Backend)

### Prerequisites
- GitHub account
- Netlify account
- Vercel account

---

## 📤 Step 1: Push to GitHub

1. **Initialize Git Repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: CheckWise CBC Analysis System"
   ```

2. **Create GitHub Repository**:
   - Go to GitHub.com
   - Create new repository named "checkwise"
   - Don't initialize with README (we already have one)

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/yourusername/checkwise.git
   git branch -M main
   git push -u origin main
   ```

---

## 🔧 Step 2: Deploy Backend to Vercel

1. **Go to Vercel Dashboard**:
   - Visit [vercel.com](https://vercel.com)
   - Sign in with GitHub

2. **Import Project**:
   - Click "New Project"
   - Import your GitHub repository
   - Select the `backend` folder as root directory

3. **Configure Deployment**:
   - **Framework Preset**: Other
   - **Root Directory**: `backend`
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

4. **Environment Variables** (if needed):
   - Add any environment variables your backend needs

5. **Deploy**:
   - Click "Deploy"
   - Wait for deployment to complete
   - Note your Vercel URL (e.g., `https://checkwise-api.vercel.app`)

---

## 🌐 Step 3: Deploy Frontend to Netlify

1. **Update API URL**:
   - Open `frontend/.env.production`
   - Replace with your actual Vercel URL:
     ```
     VITE_API_URL=https://your-actual-vercel-url.vercel.app
     ```
   - Also update `frontend/netlify.toml` with the same URL

2. **Commit Changes**:
   ```bash
   git add .
   git commit -m "Update API URL for production"
   git push
   ```

3. **Go to Netlify Dashboard**:
   - Visit [netlify.com](https://netlify.com)
   - Sign in with GitHub

4. **Import Project**:
   - Click "New site from Git"
   - Choose GitHub and select your repository
   - Configure build settings:
     - **Base directory**: `frontend`
     - **Build command**: `npm run build`
     - **Publish directory**: `frontend/dist`

5. **Deploy**:
   - Click "Deploy site"
   - Wait for deployment to complete

---

## ⚙️ Step 4: Configure CORS (Important!)

1. **Update Backend CORS**:
   - In your `backend/api.py`, update CORS configuration:
   ```python
   from flask_cors import CORS
   
   app = Flask(__name__)
   CORS(app, origins=[
       "http://localhost:5173",  # Local development
       "https://your-netlify-site.netlify.app"  # Production
   ])
   ```

2. **Commit and Redeploy**:
   ```bash
   git add .
   git commit -m "Configure CORS for production"
   git push
   ```

---

## 🔗 Step 5: Update URLs

1. **Get Your URLs**:
   - **Frontend**: `https://your-site-name.netlify.app`
   - **Backend**: `https://your-project-name.vercel.app`

2. **Update Frontend Config**:
   - Update `frontend/.env.production` with correct backend URL
   - Update `frontend/netlify.toml` with correct backend URL

3. **Final Deployment**:
   ```bash
   git add .
   git commit -m "Final URL configuration"
   git push
   ```

---

## ✅ Step 6: Test Deployment

1. **Test Frontend**:
   - Visit your Netlify URL
   - Check if the interface loads correctly

2. **Test Backend**:
   - Visit `https://your-vercel-url.vercel.app/api/health`
   - Should return JSON with health status

3. **Test Integration**:
   - Try uploading a file on the frontend
   - Test manual parameter entry
   - Verify predictions work

---

## 🐛 Troubleshooting

### Common Issues:

#### CORS Errors
- Update CORS origins in `backend/api.py`
- Include both localhost and production URLs

#### File Upload Issues
- Vercel has file size limits (4.5MB for free tier)
- Consider using external file storage for larger files

#### Build Failures
- Check Node.js version compatibility
- Verify all dependencies are listed correctly

#### API Timeout
- Vercel free tier has 10-second timeout
- Optimize file processing for faster response

---

## 📊 Monitoring & Maintenance

### Netlify:
- Check build logs in Netlify dashboard
- Monitor site analytics
- Set up custom domain if needed

### Vercel:
- Monitor function logs in Vercel dashboard
- Check performance metrics
- Set up alerts for errors

---

## 🔄 Continuous Deployment

Both platforms will automatically redeploy when you push to GitHub:

1. **Make changes locally**
2. **Commit and push**:
   ```bash
   git add .
   git commit -m "Your changes"
   git push
   ```
3. **Automatic deployment** triggers on both platforms

---

## 💡 Production Tips

1. **Environment Variables**:
   - Use environment variables for sensitive data
   - Never commit API keys or secrets

2. **Performance**:
   - Enable gzip compression
   - Optimize images and assets
   - Use CDN for static files

3. **Security**:
   - Implement rate limiting
   - Validate all inputs
   - Use HTTPS only

4. **Monitoring**:
   - Set up error tracking
   - Monitor API usage
   - Track user analytics

---

## 🎯 Final Checklist

- [ ] Backend deployed to Vercel
- [ ] Frontend deployed to Netlify
- [ ] CORS configured correctly
- [ ] API URLs updated in frontend
- [ ] File upload working
- [ ] Predictions working
- [ ] Error handling working
- [ ] Custom domain configured (optional)
- [ ] Analytics set up (optional)

Your CheckWise application is now live! 🎉