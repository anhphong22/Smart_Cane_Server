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
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    email VARCHAR(100),
                    full_name VARCHAR(100),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Locations table with user reference
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id VARCHAR(50) DEFAULT 'SmartCane01',
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    timestamp_server DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Geofences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS geofences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    radius REAL NOT NULL,
                    alert_on_enter BOOLEAN DEFAULT 1,
                    alert_on_exit BOOLEAN DEFAULT 1,
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Geofence alerts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS geofence_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    geofence_id INTEGER NOT NULL,
                    alert_type VARCHAR(10) NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_read BOOLEAN DEFAULT 0,
                    FOREIGN KEY (geofence_id) REFERENCES geofences(id)
                )
            ''')
            
            # Route history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS route_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    device_id VARCHAR(50) NOT NULL,
                    route_name VARCHAR(100),
                    start_time DATETIME NOT NULL,
                    end_time DATETIME,
                    total_distance REAL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            conn.commit()
            print("? All database tables checked/created successfully.")
            print("?? To create admin user, run: python3 create_admin.py")
    except Exception as e:
        print(f"? Error creating tables in SQLite: {e}")
        print(traceback.format_exc())


# Initialize database on module import
create_tables()
