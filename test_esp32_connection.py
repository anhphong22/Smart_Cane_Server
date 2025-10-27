#!/usr/bin/env python3
"""
Test script để kiểm tra ESP32 có thể kết nối đến server không
"""

import requests
import json

def test_esp32_connection():
    """Test xem ESP32 có thể gửi dữ liệu đến server không"""
    
    # Thông tin từ code ESP32
    ESP32_SERVER_IP = "10.241.12.160"  # IP trong code ESP32
    ESP32_SERVER_PORT = 8080
    ESP32_DEVICE_ID = "SmartCane01"
    
    # Tọa độ thực từ SMS
    LAT = 10.847239
    LON = 106.785896
    
    print("🔍 Testing ESP32 Connection...")
    print(f"ESP32 Server IP: {ESP32_SERVER_IP}")
    print(f"ESP32 Server Port: {ESP32_SERVER_PORT}")
    print(f"ESP32 Device ID: {ESP32_DEVICE_ID}")
    print(f"Real GPS Coordinates: {LAT}, {LON}")
    print("-" * 50)
    
    # Test 1: Kiểm tra server có accessible không
    try:
        response = requests.get(f"http://{ESP32_SERVER_IP}:{ESP32_SERVER_PORT}/api/get_latest_location?deviceId={ESP32_DEVICE_ID}", timeout=5)
        if response.status_code == 200:
            print("✅ ESP32 có thể kết nối đến server")
            data = response.json()
            print(f"   Current data: {data['latitude']}, {data['longitude']}")
        else:
            print(f"❌ ESP32 không thể kết nối đến server (HTTP {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ ESP32 không thể kết nối đến server: {e}")
    
    # Test 2: Simulate ESP32 gửi dữ liệu
    try:
        url = f"http://{ESP32_SERVER_IP}:{ESP32_SERVER_PORT}/save_location"
        params = {
            "latitude": LAT,
            "longitude": LON,
            "deviceId": ESP32_DEVICE_ID
        }
        
        print(f"\n🔄 Simulating ESP32 sending data...")
        print(f"URL: {url}")
        print(f"Params: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            print("✅ ESP32 có thể gửi dữ liệu thành công")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ ESP32 gửi dữ liệu thất bại (HTTP {response.status_code})")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ESP32 gửi dữ liệu thất bại: {e}")
    
    # Test 3: Kiểm tra localhost (để so sánh)
    try:
        response = requests.get(f"http://localhost:8080/api/get_latest_location?deviceId={ESP32_DEVICE_ID}", timeout=5)
        if response.status_code == 200:
            print("\n✅ Localhost server hoạt động bình thường")
            data = response.json()
            print(f"   Latest data: {data['latitude']}, {data['longitude']}")
            print(f"   Time: {data['time_local']}")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Localhost server có vấn đề: {e}")

if __name__ == "__main__":
    test_esp32_connection()


