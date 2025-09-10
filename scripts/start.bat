@echo off
echo ============================================================
echo 🚀 Starting Contract Management API with Conda Environment
echo ============================================================

echo 📦 Activating conda environment 'contract'...
call conda activate contract

if errorlevel 1 (
    echo ❌ Failed to activate conda environment 'contract'
    echo 💡 Please ensure 'contract' environment exists
    echo    Create with: conda create -n contract python=3.11
    pause
    exit /b 1
)

echo ✅ Conda environment activated successfully
echo 🚀 Starting application...
echo.

python start.py

pause
