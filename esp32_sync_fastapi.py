#!/usr/bin/env python3
"""
ESP32 Sync Script for FastAPI - Smart Cane GPS Tracker
Automatically synchronizes GPS data from ESP32 with FastAPI web interface
"""

import requests
import json
import time
import sqlite3
import threading
from datetime import datetime
import pytz
import signal
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings

# Configuration
SERVER_TIMEZONE_STR = settings.SERVER_TIMEZONE
try:
    SERVER_TIMEZONE = pytz.timezone(SERVER_TIMEZONE_STR)
except pytz.exceptions.UnknownTimeZoneError:
    print(f"!!! Warning: Unknown timezone '{SERVER_TIMEZONE_STR}'. Using UTC.")
    SERVER_TIMEZONE = pytz.utc

# Sync settings
AUTO_SYNC_ENABLED = settings.AUTO_SYNC_ENABLED
SYNC_INTERVAL = settings.SYNC_INTERVAL
WEB_SERVER_PORT = settings.PORT
WEB_SERVER_HOST = "localhost"
ESP32_DEVICE_ID = settings.ESP32_DEVICE_ID

# Global sync variables
sync_running = False
sync_thread = None


def get_db_connection():
    """Get database connection"""
    try:
        conn = sqlite3.connect(settings.DATABASE_URL)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"!!! CRITICAL: Could not connect to SQLite database: {e}")
        return None


def save_to_local_db(data):
    """
    Save ESP32 data to local database
    
    Args:
        data: GPS data dictionary
        
    Returns:
        bool: True if successful, False otherwise
    """
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        timestamp_server = data.get('timestamp_server', datetime.now(SERVER_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S'))
        
        cursor.execute(
            "INSERT INTO locations (device_id, latitude, longitude, timestamp_server) VALUES (?, ?, ?, ?)",
            (ESP32_DEVICE_ID, data['latitude'], data['longitude'], timestamp_server)
        )
        conn.commit()
        return True

    except Exception as e:
        print(f"? Error saving to local DB: {e}")
        return False
    finally:
        if conn:
            conn.close()


def auto_sync_worker():
    """Worker thread for automatic synchronization"""
    global sync_running

    print(f"?? Auto-sync worker started (interval: {SYNC_INTERVAL}s)")

    while sync_running:
        try:
            current_time = datetime.now(SERVER_TIMEZONE).strftime('%H:%M:%S')

            # Fetch GPS data from FastAPI endpoint
            api_url = f"http://{WEB_SERVER_HOST}:{WEB_SERVER_PORT}/api/get_real_gps?deviceId={ESP32_DEVICE_ID}"
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()

            gps_data = response.json()

            if gps_data and gps_data.get('latitude') is not None and gps_data.get('longitude') is not None:
                data_to_save = {
                    'latitude': gps_data['latitude'],
                    'longitude': gps_data['longitude'],
                    'timestamp_server': gps_data.get('timestamp_server', datetime.now(SERVER_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S'))
                }
                
                if save_to_local_db(data_to_save):
                    print(f"[{current_time}] ? Auto-sync: Saved GPS data: Lat={data_to_save['latitude']:.6f}, Lon={data_to_save['longitude']:.6f}")
                else:
                    print(f"[{current_time}] ? Auto-sync: Failed to save GPS data.")
            else:
                print(f"[{current_time}] ? Auto-sync: No fresh GPS data available.")

        except requests.exceptions.RequestException as e:
            print(f"[{current_time}] ? Auto-sync HTTP error: {e}")
        except json.JSONDecodeError:
            print(f"[{current_time}] ? Auto-sync JSON decode error.")
        except Exception as e:
            print(f"[{current_time}] ? Auto-sync general error: {e}")

        time.sleep(SYNC_INTERVAL)


def start_auto_sync():
    """Start automatic synchronization"""
    global sync_running, sync_thread

    if sync_running:
        print("?? Auto-sync already running!")
        return

    sync_running = True
    sync_thread = threading.Thread(target=auto_sync_worker, daemon=True)
    sync_thread.start()
    print(f"?? Auto-sync started (interval: {SYNC_INTERVAL}s)")


def stop_auto_sync():
    """Stop automatic synchronization"""
    global sync_running

    if not sync_running:
        print("?? Auto-sync not running!")
        return

    sync_running = False
    if sync_thread:
        sync_thread.join(timeout=2)
    print("?? Auto-sync stopped")


def signal_handler(sig, frame):
    """Handle Ctrl+C signal"""
    print("\n?? Received stop signal...")
    stop_auto_sync()
    sys.exit(0)


def main():
    """Main function"""
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    print("=" * 70)
    print("?? ESP32 SMART CANE SYNC TOOL (FastAPI)")
    print("=" * 70)
    print(f"Server: http://{WEB_SERVER_HOST}:{WEB_SERVER_PORT}")
    print(f"Device ID: {ESP32_DEVICE_ID}")
    print(f"Timezone: {SERVER_TIMEZONE_STR}")
    print(f"Sync Interval: {SYNC_INTERVAL}s")
    print("=" * 70)

    # Automatically start auto-sync
    if AUTO_SYNC_ENABLED:
        start_auto_sync()
    else:
        print("?? Auto-sync is disabled in settings")

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
            if not sync_running:
                break
    except KeyboardInterrupt:
        pass
    finally:
        stop_auto_sync()
        print("?? Goodbye!")


if __name__ == "__main__":
    main()
