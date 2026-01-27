#!/bin/bash
# CataMaze Startup Script for Railway

# Initialize database
python -c "from backend.storage.db import init_db; init_db()" || echo "Database initialization failed, continuing..."

# Start FastAPI server
cd /app
uvicorn backend.api.routes:app --host 0.0.0.0 --port ${PORT:-8000}
