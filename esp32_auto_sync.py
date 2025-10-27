#!/usr/bin/env python3
"""
ESP32 Auto Sync - Chạy đồng bộ tự động trong background
Script này sẽ chạy liên tục để đồng bộ dữ liệu từ ESP32 với web
"""

import sys
import os
import time
import signal
from datetime import datetime
import pytz

# Import từ esp32_sync.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import các hàm cần thiết
from esp32_sync import (
    start_auto_sync, stop_auto_sync, sync_running,
    SERVER_TIMEZONE, SYNC_INTERVAL, ESP32_DEVICE_ID
)

def signal_handler(sig, frame):
    """Xử lý tín hiệu Ctrl+C"""
    print("\n🛑 Nhận tín hiệu dừng...")
    stop_auto_sync()
    print("✅ Auto-sync stopped successfully")
    sys.exit(0)

def main():
    """Main function cho auto sync"""
    # Đăng ký signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=" * 60)
    print("🚀 ESP32 AUTO SYNC - BACKGROUND MODE")
    print("=" * 60)
    print(f"Device ID: {ESP32_DEVICE_ID}")
    print(f"Sync Interval: {SYNC_INTERVAL} seconds")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Bắt đầu auto sync
    start_auto_sync()
    
    try:
        # Chạy vô hạn, hiển thị status mỗi 60 giây
        while True:
            time.sleep(60)
            
            if sync_running:
                current_time = datetime.now(SERVER_TIMEZONE).strftime('%H:%M:%S')
                print(f"[{current_time}] 📡 Auto-sync running...")
            else:
                print("❌ Auto-sync stopped unexpectedly!")
                break
                
    except KeyboardInterrupt:
        pass
    finally:
        stop_auto_sync()
        print("👋 Auto-sync terminated")

if __name__ == "__main__":
    main()
