# Netlify Deployment Guide

## Manual Deployment Steps

1. Log in to Netlify
2. Click "Add new site" → "Import an existing project"
3. Connect to your GitHub repository
4. Configure build settings:
   - Base directory: `diagnosis-ui`
   - Build command: `npm install && npm run build`
   - Publish directory: `dist`
5. Add environment variables:
   - Key: `VITE_API_URL`
   - Value: `https://diagnosisai.onrender.com`
6. Click "Deploy site"

## Troubleshooting

If you encounter build errors:

1. Make sure you've specified the correct base directory (`diagnosis-ui`)
2. Check that the package.json file has compatible dependencies
3. Try setting Node.js version to 18 in the "Environment" settings
4. Review build logs for specific errors