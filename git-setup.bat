@echo off
echo ========================================
echo Setting up CheckWise Git Repository
echo ========================================

:: Initialize git repository
git init

:: Add all files
git add .

:: Create initial commit
git commit -m "Initial commit: CheckWise CBC Analysis System"

:: Add remote origin (replace with your repository URL)
echo.
echo Please add your remote repository URL:
echo git remote add origin https://github.com/yourusername/checkwise.git
echo.
echo Then push to main:
echo git branch -M main
echo git push -u origin main
echo.

pause