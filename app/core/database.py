"""
Database connection and operations
"""
import sqlite3
from contextlib import contextmanager
from typing import Optional
import traceback
from .config import settings


def get_db_connection() -> Optional[sqlite3.Connection]:
    """
    Create a database connection
    
    Returns:
        Optional[sqlite3.Connection]: Database connection or None if failed
    """
    try:
        conn = sqlite3.connect(settings.DATABASE_URL, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"!!! CRITICAL: Could not connect to SQLite database: {e}")
        return None


@contextmanager
def get_db():
    """
    Context manager for database connections
    
    Yields:
        sqlite3.Connection: Database connection
    """
    conn = get_db_connection()
    try:
        yield conn
    finally:
        if conn:
            conn.close()


def create_tables():
    """Create database tables if they don't exist"""
    try:
        with get_db() as conn:
            if conn is None:
                raise Exception("Failed to get database connection.")
            
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id VARCHAR(50) DEFAULT 'SmartCane01',
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    timestamp_server DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            print("? Table 'locations' checked/created successfully in SQLite.")
    except Exception as e:
        print(f"? Error creating table 'locations' in SQLite: {e}")
        print(traceback.format_exc())


# Initialize database on module import
create_tables()
