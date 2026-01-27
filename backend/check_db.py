"""
Database verification script
Run this to check if database is initialized correctly
"""
from backend.storage.db import engine, init_db, test_connection
from backend.storage.models import Game, Log
from sqlalchemy import inspect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_database():
    """Check database connection and tables"""

    # Test connection
    logger.info("Testing database connection...")
    if not test_connection():
        logger.error("✗ Database connection failed")
        return False
    logger.info("✓ Database connection successful")

    # Check if tables exist
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    logger.info(f"Found {len(tables)} tables in database")

    expected_tables = ['games', 'logs']  # Adjust based on your models

    for table in expected_tables:
        if table in tables:
            logger.info(f"  ✓ Table '{table}' exists")

            # Show columns
            columns = inspector.get_columns(table)
            logger.info(f"    Columns: {', '.join([c['name'] for c in columns])}")
        else:
            logger.warning(f"  ✗ Table '{table}' is missing")

    return len(tables) > 0

def initialize_database():
    """Initialize database tables"""
    logger.info("Initializing database tables...")
    try:
        init_db()
        logger.info("✓ Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "init":
        # Initialize database
        if initialize_database():
            check_database()
    else:
        # Just check database
        if not check_database():
            logger.info("\nTo initialize database, run:")
            logger.info("  python backend/check_db.py init")
