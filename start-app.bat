@echo off
echo ========================================
echo Starting CheckWise Application
echo ========================================

:: Get the current directory
set CURRENT_DIR=%~dp0

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

:: Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    pause
    exit /b 1
)

:: Check if backend directory exists
if not exist "%CURRENT_DIR%backend" (
    echo ERROR: backend directory not found
    pause
    exit /b 1
)

:: Check if frontend directory exists
if not exist "%CURRENT_DIR%frontend" (
    echo ERROR: frontend directory not found
    pause
    exit /b 1
)

:: Check and install Python dependencies
echo Checking Python dependencies...
cd /d "%CURRENT_DIR%backend"
python -c "import flask, flask_cors, sklearn, pandas, joblib, numpy, PyPDF2, PIL, pytesseract, openpyxl" >nul 2>&1
if errorlevel 1 (
    echo Installing Python dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install Python dependencies
        pause
        exit /b 1
    )
)

:: Check and install Node.js dependencies
echo Checking Node.js dependencies...
cd /d "%CURRENT_DIR%frontend"
if not exist node_modules (
    echo Installing Node.js dependencies...
    npm install
    if errorlevel 1 (
        echo ERROR: Failed to install Node.js dependencies
        pause
        exit /b 1
    )
)

echo Starting Flask API server...
start "Flask API" cmd /k "cd /d "%CURRENT_DIR%backend" && python api.py"

:: Wait a moment for the API to start
timeout /t 3 /nobreak >nul

echo Starting React development server...
start "React App" cmd /k "cd /d "%CURRENT_DIR%frontend" && npm run dev"

echo.
echo ========================================
echo Dependencies checked and installed!
echo Both services are starting...
echo Flask API: http://localhost:5000
echo React App: http://localhost:5173
echo ========================================
echo.
echo Press any key to exit...
pause >nul