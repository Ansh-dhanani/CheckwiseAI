# Frontend Deployment Guide

## Option 1: Deploy on Render.com

1. Log in to Render.com
2. Click "New" and select "Static Site"
3. Connect your GitHub repository
4. Configure the following settings:
   - Name: diagnosisai-frontend
   - Root Directory: diagnosis/diagnosis-ui
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`
   - Environment Variables:
     - VITE_API_URL: https://diagnosisai.onrender.com

## Option 2: Deploy on Netlify

1. Log in to Netlify
2. Click "New site from Git"
3. Connect your GitHub repository
4. Configure the following settings:
   - Base directory: diagnosis/diagnosis-ui
   - Build command: `npm install && npm run build`
   - Publish directory: `dist`
   - Environment variables:
     - VITE_API_URL: https://diagnosisai.onrender.com

## Option 3: Deploy on Vercel

1. Log in to Vercel
2. Click "New Project"
3. Import your GitHub repository
4. Configure the following settings:
   - Framework Preset: Vite
   - Root Directory: diagnosis/diagnosis-ui
   - Build Command: `npm install && npm run build`
   - Output Directory: `dist`
   - Environment Variables:
     - VITE_API_URL: https://diagnosisai.onrender.com