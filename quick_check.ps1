# CheckwiseAI Quick Status Check
Write-Host "CheckwiseAI Status Check" -ForegroundColor Cyan

# Check backend health
Write-Host "`nChecking Backend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "https://diagnosisai.onrender.com/api/health" -Method GET -TimeoutSec 10
    $health = $response.Content | ConvertFrom-Json
    
    Write-Host "Backend Status: $($health.status)" -ForegroundColor Green
    Write-Host "Models Loaded: $($health.models.disease_model_loaded -and $health.models.label_encoder_loaded)" -ForegroundColor $(if ($health.models.disease_model_loaded -and $health.models.label_encoder_loaded) { "Green" } else { "Red" })
    
    if ($health.models.model_status.status -eq "error") {
        Write-Host "Model Error: $($health.models.model_status.message)" -ForegroundColor Red
    }
    
} catch {
    Write-Host "Backend Error: $_" -ForegroundColor Red
}

# Check parameters endpoint
Write-Host "`nChecking Parameters Endpoint..." -ForegroundColor Yellow
try {
    $params = Invoke-WebRequest -Uri "https://diagnosisai.onrender.com/api/parameters" -Method GET -TimeoutSec 10
    Write-Host "Parameters Endpoint: OK" -ForegroundColor Green
} catch {
    Write-Host "Parameters Endpoint Error: $_" -ForegroundColor Red
}

# Check frontend
Write-Host "`nChecking Frontend..." -ForegroundColor Yellow
try {
    $frontend = Invoke-WebRequest -Uri "https://check-wise.netlify.app" -Method GET -TimeoutSec 10
    Write-Host "Frontend: OK" -ForegroundColor Green
} catch {
    Write-Host "Frontend Error: $_" -ForegroundColor Red
}

Write-Host "`nURLs:" -ForegroundColor Cyan
Write-Host "Frontend: https://check-wise.netlify.app"
Write-Host "Backend:  https://diagnosisai.onrender.com"