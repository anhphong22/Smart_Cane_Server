#!/usr/bin/env python3
"""
Smart Cane Server Startup Script
Khởi động cả web server và ESP32 auto sync
"""

import subprocess
import sys
import os
import time
import signal
import threading
from datetime import datetime

def signal_handler(sig, frame):
    """Xử lý tín hiệu Ctrl+C"""
    print("\n🛑 Nhận tín hiệu dừng...")
    print("Đang dừng tất cả services...")
    
    # Dừng các process
    if 'web_process' in globals() and web_process:
        web_process.terminate()
        print("✅ Web server stopped")
    
    if 'sync_process' in globals() and sync_process:
        sync_process.terminate()
        print("✅ Auto sync stopped")
    
    sys.exit(0)

def run_web_server():
    """Chạy Flask web server"""
    print("🌐 Starting web server...")
    try:
        process = subprocess.Popen([
            sys.executable, 'app.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # In output từ web server
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"[WEB] {output.strip()}")
                
        return process
    except Exception as e:
        print(f"❌ Error starting web server: {e}")
        return None

def run_auto_sync():
    """Chạy ESP32 auto sync"""
    print("🔄 Starting auto sync...")
    try:
        process = subprocess.Popen([
            sys.executable, 'esp32_auto_sync.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # In output từ auto sync
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"[SYNC] {output.strip()}")
                
        return process
    except Exception as e:
        print(f"❌ Error starting auto sync: {e}")
        return None

def main():
    """Main function"""
    # Đăng ký signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=" * 60)
    print("🚀 SMART CANE SERVER STARTUP")
    print("=" * 60)
    print("Starting web server and auto sync...")
    print("Press Ctrl+C to stop all services")
    print("=" * 60)
    
    global web_process, sync_process
    web_process = None
    sync_process = None
    
    try:
        # Chờ một chút để đảm bảo mọi thứ sẵn sàng
        time.sleep(2)
        
        # Chạy web server trong thread riêng
        web_thread = threading.Thread(target=run_web_server, daemon=True)
        web_thread.start()
        
        # Chờ web server khởi động
        time.sleep(5)
        
        # Chạy auto sync trong thread riêng
        sync_thread = threading.Thread(target=run_auto_sync, daemon=True)
        sync_thread.start()
        
        print("\n✅ All services started!")
        print("🌐 Web Interface: http://localhost:8080")
        print("📡 ESP32 Auto Sync: Running in background")
        print("\nPress Ctrl+C to stop all services")
        
        # Chạy vô hạn
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        pass
    finally:
        print("\n🛑 Stopping all services...")
        
        if web_process:
            web_process.terminate()
        if sync_process:
            sync_process.terminate()
            
        print("✅ All services stopped")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
