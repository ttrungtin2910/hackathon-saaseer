@echo off
REM Deploy script for SaaSeer Contract Management API

echo 🚀 SaaSeer Contract Management API - Deployment Script
echo ==================================================

REM Check if git is initialized
if not exist ".git" (
    echo ❌ Git repository not initialized
    echo 💡 Run: git init
    exit /b 1
)

REM Check git status
echo 📋 Checking git status...
git status --short

REM Add all files
echo 📁 Adding files to git...
git add .

REM Commit changes
echo 💾 Committing changes...
git commit -m "feat: Update SaaSeer Contract Management API - Enhanced null values support - Improved error handling - Updated documentation - Clean project structure"

REM Check if remote exists
git remote get-url origin >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Remote repository exists
    echo 📤 Pushing to remote...
    git push origin main
) else (
    echo 📝 No remote repository found
    echo 💡 To add a remote repository:
    echo    git remote add origin ^<repository-url^>
    echo    git push -u origin main
)

echo ✅ Deployment script completed!
echo 🌐 API Documentation: http://localhost:8000/docs
echo 🔍 Health Check: http://localhost:8000/health
