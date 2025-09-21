# CheckwiseAI Deployment Status Checker
Write-Host "Checking CheckwiseAI Deployment Status..." -ForegroundColor Cyan

try {
    $response = Invoke-WebRequest -Uri "https://diagnosisai.onrender.com/api/health" -Method GET
    $health = $response.Content | ConvertFrom-Json
    
    Write-Host "`nDeployment Status: " -NoNewline
    if ($health.status -eq "healthy") {
        Write-Host $health.status -ForegroundColor Green
    } else {
        Write-Host $health.status -ForegroundColor Yellow
    }
    
    Write-Host "ML Libraries Available: " -NoNewline
    if ($health.system.ml_libraries_available) {
        Write-Host "YES" -ForegroundColor Green
    } else {
        Write-Host "NO" -ForegroundColor Red
    }
    
    Write-Host "Models Loaded: " -NoNewline
    if ($health.models.disease_model_loaded -and $health.models.label_encoder_loaded) {
        Write-Host "YES" -ForegroundColor Green
    } else {
        Write-Host "NO" -ForegroundColor Red
    }
    
    if ($health.models.model_status.status -eq "error") {
        Write-Host "Model Error: " -NoNewline -ForegroundColor Red
        Write-Host $health.models.model_status.message
    }
    
    Write-Host "`nFrontend URL: https://check-wise.netlify.app" -ForegroundColor Cyan
    Write-Host "Backend URL: https://diagnosisai.onrender.com" -ForegroundColor Cyan
    
} catch {
    Write-Host "Failed to check deployment status: $_" -ForegroundColor Red
}