#!/bin/bash

echo "Starting SaaSeer Contract Management API..."
echo "=========================================="

echo "Activating conda environment 'py12'..."
conda activate py12

echo "Using enhanced startup script..."
python scripts/run_server.py
