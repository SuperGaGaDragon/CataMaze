"""
CataMaze Backend Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router as game_router
from backend.storage.db import init_db, test_connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CataMaze API",
    description="Backend API for CataMaze game",
    version="0.1.0"
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    logger.info("Starting CataMaze API...")

    # Test database connection
    if test_connection():
        logger.info("✓ Database connection successful")
    else:
        logger.error("✗ Database connection failed")
        raise Exception("Cannot connect to database")

    # Initialize database tables
    try:
        init_db()
        logger.info("✓ Database tables initialized")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        raise

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(game_router)

@app.get("/")
async def root():
    return {
        "message": "CataMaze API is running",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "game": "/game/*"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "catamaze-api",
        "version": "0.1.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
