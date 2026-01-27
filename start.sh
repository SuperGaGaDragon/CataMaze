#!/bin/bash
# CataMaze Startup Script for Railway

# Start FastAPI server (database init happens in app startup)
cd /app
uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
