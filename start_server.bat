@echo off
echo Starting SaaSeer Contract Management API...
echo ==========================================

echo Activating conda environment 'py12'...
call conda activate py12

echo Using enhanced startup script...
python scripts/run_server.py

pause
