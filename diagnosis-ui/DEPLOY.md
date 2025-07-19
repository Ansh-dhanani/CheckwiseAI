# Frontend Deployment Instructions

## Render.com Deployment

1. Log in to Render.com
2. Click "New" and select "Static Site"
3. Connect your GitHub repository
4. Configure the following settings:
   - Name: diagnosisai-frontend
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`
   - Environment Variables:
     - VITE_API_URL: https://diagnosisai.onrender.com

## Manual Deployment Steps

1. Build the frontend:
   ```
   npm install
   npm run build
   ```

2. The built files will be in the `dist` directory
3. Deploy these files to any static hosting service (Netlify, Vercel, etc.)