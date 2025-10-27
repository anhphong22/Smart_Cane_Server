#!/usr/bin/env python3
"""
Test Real GPS System - Kiểm tra hệ thống GPS thực tế
"""

import requests
import json
import time
from datetime import datetime
import pytz

# Cấu hình
SERVER_TIMEZONE_STR = 'Asia/Ho_Chi_Minh'
try:
    SERVER_TIMEZONE = pytz.timezone(SERVER_TIMEZONE_STR)
except pytz.exceptions.UnknownTimeZoneError:
    print(f"!!! LOI: Khong tim thay múi giờ '{SERVER_TIMEZONE_STR}'. Su dung UTC lam mac dinh.")
    SERVER_TIMEZONE = pytz.utc

WEB_SERVER_URL = "http://localhost:8080"
ESP32_DEVICE_ID = "SmartCane01"

def test_real_gps_endpoint():
    """Test endpoint lấy GPS thực tế"""
    print("🕐 Testing Real GPS Endpoint...")
    print("=" * 50)
    
    try:
        # Test endpoint mới
        response = requests.get(
            f"{WEB_SERVER_URL}/api/get_real_gps?deviceId={ESP32_DEVICE_ID}",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Real GPS endpoint working!")
            print(f"   Latitude: {data['latitude']}")
            print(f"   Longitude: {data['longitude']}")
            print(f"   Time: {data['time_local']}")
            print(f"   Date: {data['date_local']}")
            print(f"   Source: {data['source']}")
            return True
        else:
            print(f"❌ Real GPS endpoint failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Real GPS endpoint error: {e}")
        return False

def test_stored_data_endpoint():
    """Test endpoint lấy dữ liệu đã lưu"""
    print("\n📅 Testing Stored Data Endpoint...")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{WEB_SERVER_URL}/api/get_latest_location?deviceId={ESP32_DEVICE_ID}",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Stored data endpoint working!")
            print(f"   Latitude: {data['latitude']}")
            print(f"   Longitude: {data['longitude']}")
            print(f"   Time: {data['time_local']}")
            print(f"   Date: {data['date_local']}")
            print(f"   Source: {data.get('source', 'N/A')}")
            return True
        else:
            print(f"❌ Stored data endpoint failed: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Stored data endpoint error: {e}")
        return False

def test_force_real_time():
    """Test endpoint với forceRealTime parameter"""
    print("\n🔄 Testing Force Real Time Parameter...")
    print("=" * 50)
    
    try:
        response = requests.get(
            f"{WEB_SERVER_URL}/api/get_latest_location?deviceId={ESP32_DEVICE_ID}&forceRealTime=true",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Force real time working!")
            print(f"   Latitude: {data['latitude']}")
            print(f"   Longitude: {data['longitude']}")
            print(f"   Time: {data['time_local']}")
            print(f"   Date: {data['date_local']}")
            print(f"   Source: {data.get('source', 'N/A')}")
            return True
        else:
            print(f"❌ Force real time failed: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Force real time error: {e}")
        return False

def compare_timestamps():
    """So sánh timestamp giữa các endpoint"""
    print("\n⏰ Comparing Timestamps...")
    print("=" * 50)
    
    current_time = datetime.now(SERVER_TIMEZONE)
    print(f"Current server time: {current_time.strftime('%H:%M:%S %d/%m/%Y')}")
    
    # Test real GPS
    try:
        response = requests.get(f"{WEB_SERVER_URL}/api/get_real_gps?deviceId={ESP32_DEVICE_ID}", timeout=5)
        if response.status_code == 200:
            real_data = response.json()
            print(f"Real GPS time: {real_data['time_local']} {real_data['date_local']}")
        else:
            print("❌ Could not get real GPS data for comparison")
    except:
        print("❌ Error getting real GPS data for comparison")
    
    # Test stored data
    try:
        response = requests.get(f"{WEB_SERVER_URL}/api/get_latest_location?deviceId={ESP32_DEVICE_ID}", timeout=5)
        if response.status_code == 200:
            stored_data = response.json()
            print(f"Stored data time: {stored_data['time_local']} {stored_data['date_local']}")
        else:
            print("❌ Could not get stored data for comparison")
    except:
        print("❌ Error getting stored data for comparison")

def main():
    """Main test function"""
    print("🚀 REAL GPS SYSTEM TEST")
    print("=" * 60)
    print(f"Web Server: {WEB_SERVER_URL}")
    print(f"Device ID: {ESP32_DEVICE_ID}")
    print(f"Server Timezone: {SERVER_TIMEZONE_STR}")
    print("=" * 60)
    
    # Chạy các test
    tests = [
        ("Real GPS Endpoint", test_real_gps_endpoint),
        ("Stored Data Endpoint", test_stored_data_endpoint),
        ("Force Real Time", test_force_real_time),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    # So sánh timestamps
    compare_timestamps()
    
    # Tổng kết
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Real GPS system is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the logs above for details.")

if __name__ == "__main__":
    main()
