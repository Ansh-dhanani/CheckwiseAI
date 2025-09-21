# CheckwiseAI Deployment Setup Script
# Run this to verify your deployment configuration

Write-Host "🚀 CheckwiseAI Deployment Configuration Checker" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Check if all critical files exist
$criticalFiles = @(
    "main.py",
    "requirements.txt", 
    "cbc_disease_model.joblib",
    "disease_label_encoder.joblib",
    "backend\api.py",
    "backend\cbc_disease_model.joblib", 
    "backend\disease_label_encoder.joblib",
    "frontend\netlify.toml",
    "frontend\package.json"
)

Write-Host "`n📁 Checking Critical Files:" -ForegroundColor Yellow
foreach ($file in $criticalFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file - MISSING!" -ForegroundColor Red
    }
}

# Check requirements.txt content
Write-Host "`n📦 Checking requirements.txt:" -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    $requirements = Get-Content "requirements.txt"
    $expectedPackages = @("flask==2.3.3", "scikit-learn==1.2.2", "numpy==1.24.3", "gunicorn==21.2.0")
    
    foreach ($package in $expectedPackages) {
        if ($requirements -contains $package) {
            Write-Host "✅ $package" -ForegroundColor Green
        } else {
            Write-Host "❌ $package - VERSION MISMATCH!" -ForegroundColor Red
        }
    }
}

# Check backend health
Write-Host "`n🔍 Checking Backend Status:" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "https://diagnosisai.onrender.com/api/health" -Method GET -TimeoutSec 10
    $health = $response.Content | ConvertFrom-Json
    
    if ($health.status -eq "healthy") {
        Write-Host "✅ Backend Status: HEALTHY" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Backend Status: DEGRADED" -ForegroundColor Yellow
    }
    
    if ($health.models.disease_model_loaded -and $health.models.label_encoder_loaded) {
        Write-Host "✅ Models: LOADED" -ForegroundColor Green
    } else {
        Write-Host "❌ Models: NOT LOADED" -ForegroundColor Red
        Write-Host "   Error: $($health.models.model_status.message)" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ Backend: NOT ACCESSIBLE" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
}

# Check frontend
Write-Host "`n🌐 Checking Frontend:" -ForegroundColor Yellow
try {
    $frontendResponse = Invoke-WebRequest -Uri "https://check-wise.netlify.app" -Method GET -TimeoutSec 10
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend: ACCESSIBLE" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Frontend: NOT ACCESSIBLE" -ForegroundColor Red
}

Write-Host "`n🔗 Deployment URLs:" -ForegroundColor Cyan
Write-Host "Frontend: https://check-wise.netlify.app" -ForegroundColor White
Write-Host "Backend:  https://diagnosisai.onrender.com" -ForegroundColor White
Write-Host "Health:   https://diagnosisai.onrender.com/api/health" -ForegroundColor White

Write-Host "`n📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Fix any missing files above" -ForegroundColor White
Write-Host "2. Update requirements.txt with exact versions" -ForegroundColor White
Write-Host "3. Commit and push changes to trigger redeployment" -ForegroundColor White
Write-Host "4. Wait 2-3 minutes for deployment to complete" -ForegroundColor White
Write-Host "5. Test predictions on frontend" -ForegroundColor White