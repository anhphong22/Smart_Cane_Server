#!/usr/bin/env python3
"""
ESP32 Sync Script - Đồng bộ dữ liệu với ESP32 Smart Cane
Tự động đồng bộ dữ liệu GPS từ ESP32 với web interface
"""

import requests
import json
import time
import sqlite3
import config
import threading
from datetime import datetime
import pytz
import signal
import sys

# Cấu hình
SERVER_TIMEZONE_STR = 'Asia/Ho_Chi_Minh'
try:
    SERVER_TIMEZONE = pytz.timezone(SERVER_TIMEZONE_STR)
except pytz.exceptions.UnknownTimeZoneError:
    print(f"!!! LOI: Khong tim thay múi giờ '{SERVER_TIMEZONE_STR}'. Su dung UTC lam mac dinh.")
    SERVER_TIMEZONE = pytz.utc

# ESP32_DEVICE_ID = "SmartCane01"

# Cấu hình đồng bộ tự động
AUTO_SYNC_ENABLED = True
SYNC_INTERVAL = 10  # giây
WEB_SERVER_PORT = 8080
WEB_SERVER_HOST = "localhost"
ESP32_DEVICE_ID = "SmartCane01" # Moved here for better grouping with WEB_SERVER_HOST/PORT

# Biến global cho đồng bộ
sync_running = False
sync_thread = None

def get_db_connection():
    """Kết nối đến SQLite database"""
    try:
        conn = sqlite3.connect(config.DATABASE_URL)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"!!! CRITICAL: Could not connect to SQLite database: {e}")
        return None

def save_to_local_db(data):
    """Lưu dữ liệu ESP32 vào database local"""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        # Use the timestamp from the Flask API response if available, otherwise use current time
        timestamp_server = data.get('timestamp_server', datetime.now(SERVER_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S'))
        cursor.execute(
            "INSERT INTO locations (device_id, latitude, longitude, timestamp_server) VALUES (?, ?, ?, ?)",
            (ESP32_DEVICE_ID, data['latitude'], data['longitude'], timestamp_server)
        )
        conn.commit()
        return True

    except Exception as e:
        print(f"❌ Error saving to local DB: {e}")
        return False
    finally:
        if conn:
            conn.close()

def auto_sync_worker():
    """Worker thread cho đồng bộ tự động"""
    global sync_running

    print(f"🔄 Auto-sync worker started (interval: {SYNC_INTERVAL}s)")

    while sync_running:
        try:
            current_time = datetime.now(SERVER_TIMEZONE).strftime('%H:%M:%S')

            # Fetch GPS data from Flask API
            flask_api_url = f"http://{WEB_SERVER_HOST}:{WEB_SERVER_PORT}/api/get_real_gps?deviceId={ESP32_DEVICE_ID}"
            response = requests.get(flask_api_url)
            response.raise_for_status() # Raise an exception for HTTP errors

            gps_data = response.json()

            if gps_data and gps_data.get('latitude') is not None and gps_data.get('longitude') is not None:
                data_to_save = {
                    'latitude': gps_data['latitude'],
                    'longitude': gps_data['longitude'],
                    'timestamp_server': gps_data.get('timestamp_server', datetime.now(SERVER_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S'))
                }
                if save_to_local_db(data_to_save):
                    print(f"[{current_time}] ✅ Auto-sync: Saved GPS data from Flask API: Lat={data_to_save['latitude']:.6f}, Lon={data_to_save['longitude']:.6f}")
                else:
                    print(f"[{current_time}] ❌ Auto-sync: Failed to save GPS data from Flask API.")
            else:
                print(f"[{current_time}] ⏳ Auto-sync: No fresh GPS data from Flask API or data is incomplete.")

        except requests.exceptions.RequestException as e:
            print(f"[{current_time}] ❌ Auto-sync HTTP error: {e}")
        except json.JSONDecodeError:
            print(f"[{current_time}] ❌ Auto-sync JSON decode error from Flask API response.")
        except Exception as e:
            print(f"[{current_time}] ❌ Auto-sync general error: {e}")

        time.sleep(SYNC_INTERVAL)

def start_auto_sync():
    """Bắt đầu đồng bộ tự động"""
    global sync_running, sync_thread

    if sync_running:
        print("⚠️ Auto-sync đã đang chạy!")
        return

    sync_running = True
    sync_thread = threading.Thread(target=auto_sync_worker, daemon=True)
    sync_thread.start()
    print(f"🚀 Auto-sync started (interval: {SYNC_INTERVAL}s)")

def stop_auto_sync():
    """Dừng đồng bộ tự động"""
    global sync_running

    if not sync_running:
        print("⚠️ Auto-sync chưa chạy!")
        return

    sync_running = False
    if sync_thread:
        sync_thread.join(timeout=2)
    print("🛑 Auto-sync stopped")

def signal_handler(sig, frame):
    """Xử lý tín hiệu Ctrl+C"""
    print("\n🛑 Nhận tín hiệu dừng...")
    stop_auto_sync()
    sys.exit(0)

def main():
    """Main function"""
    # Đăng ký signal handler cho Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    print("=" * 60)
    print("🚀 ESP32 SMART CANE SYNC TOOL")
    print("=" * 60)

    # Automatically start auto-sync when the script runs
    start_auto_sync()

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
            if not sync_running: # If auto-sync stops unexpectedly, exit main
                break
    except KeyboardInterrupt:
        pass
    finally:
        stop_auto_sync()
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()