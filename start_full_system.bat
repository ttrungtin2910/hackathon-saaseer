@echo off
echo Starting SaaSeer Full System...
echo.

echo Starting Backend Server...
start "Backend" cmd /k "cd backend && conda activate py12 && python main.py"

echo Waiting for backend to start...
timeout /t 8 /nobreak > nul

echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm start"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Backend API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:3000
echo.
echo To test API connection:
echo 1. Open browser console in frontend
echo 2. Run: testSaaSeerAPI()
echo.
pause
