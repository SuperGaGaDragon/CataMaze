#!/bin/bash
# CataMaze API Server Startup Script

cd "$(dirname "$0")"

echo "Starting CataMaze API server..."
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
