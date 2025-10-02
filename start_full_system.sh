#!/bin/bash

echo "Starting SaaSeer Full System..."
echo ""

echo "Starting Backend Server..."
cd backend
conda activate py12
python main.py &
BACKEND_PID=$!

echo "Waiting for backend to start..."
sleep 8

echo "Starting Frontend..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "Both servers are starting..."
echo "Backend: http://localhost:8000"
echo "Backend API Docs: http://localhost:8000/docs"
echo "Frontend: http://localhost:3000"
echo ""
echo "To test API connection:"
echo "1. Open browser console in frontend"
echo "2. Run: testSaaSeerAPI()"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait
