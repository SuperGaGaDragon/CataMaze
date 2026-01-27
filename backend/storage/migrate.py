"""
Database migration script.
Automatically creates all tables.
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from storage.db import init_db, test_connection, DATABASE_URL


def run_migrations():
    """
    Run database migrations.
    Creates all tables if they don't exist.
    """
    print("=" * 60)
    print("CataMaze Database Migration")
    print("=" * 60)
    print()

    # Show database URL (masked password)
    masked_url = DATABASE_URL
    if "@" in masked_url and ":" in masked_url:
        parts = masked_url.split("@")
        creds = parts[0].split("://")[1]
        if ":" in creds:
            user = creds.split(":")[0]
            masked_url = masked_url.replace(creds, f"{user}:****")

    print(f"Database URL: {masked_url}")
    print()

    # Test connection
    print("Testing database connection...")
    if not test_connection():
        print("✗ Connection failed!")
        print()
        print("Please check:")
        print("  1. DATABASE_URL environment variable is set correctly")
        print("  2. Database server is running and accessible")
        print("  3. Credentials are correct")
        return False

    print("✓ Connection successful")
    print()

    # Run migrations
    print("Creating tables...")
    try:
        init_db()
        print("✓ Tables created successfully")
        print()
        print("Tables:")
        print("  - games")
        print("  - logs")
        print()
        print("=" * 60)
        print("Migration complete!")
        print("=" * 60)
        return True
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        return False


if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)
