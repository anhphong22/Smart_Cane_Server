#!/usr/bin/env python3
"""
API Testing Script for Smart Cane GPS Tracker
Tests all API endpoints to ensure they work correctly
"""

import requests
import json
import sys
from datetime import datetime


BASE_URL = "http://localhost:8080"
TEST_DEVICE_ID = "SmartCane01"
TEST_LAT = 10.7769
TEST_LON = 106.7009


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_test(name, success, message=""):
    """Print test result"""
    status = "? PASS" if success else "? FAIL"
    print(f"{status} | {name}")
    if message:
        print(f"       {message}")


def test_health():
    """Test health endpoint"""
    print_header("Testing Health Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/health")
        success = response.status_code == 200
        data = response.json() if success else {}
        print_test("GET /health", success, json.dumps(data, indent=2))
        return success
    except Exception as e:
        print_test("GET /health", False, str(e))
        return False


def test_save_location_post():
    """Test save location with POST"""
    print_header("Testing Save Location (POST)")
    try:
        payload = {
            "latitude": TEST_LAT,
            "longitude": TEST_LON,
            "deviceId": TEST_DEVICE_ID
        }
        response = requests.post(
            f"{BASE_URL}/save_location",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        success = response.status_code == 200
        data = response.json() if success else {}
        print_test("POST /save_location", success, json.dumps(data, indent=2))
        return success
    except Exception as e:
        print_test("POST /save_location", False, str(e))
        return False


def test_save_location_get():
    """Test save location with GET"""
    print_header("Testing Save Location (GET)")
    try:
        params = {
            "latitude": TEST_LAT,
            "longitude": TEST_LON,
            "deviceId": TEST_DEVICE_ID
        }
        response = requests.get(f"{BASE_URL}/save_location", params=params)
        success = response.status_code == 200
        data = response.json() if success else {}
        print_test("GET /save_location", success, json.dumps(data, indent=2))
        return success
    except Exception as e:
        print_test("GET /save_location", False, str(e))
        return False


def test_get_latest_location():
    """Test get latest location"""
    print_header("Testing Get Latest Location")
    try:
        params = {"deviceId": TEST_DEVICE_ID}
        response = requests.get(f"{BASE_URL}/api/get_latest_location", params=params)
        success = response.status_code == 200
        data = response.json() if success else {}
        print_test("GET /api/get_latest_location", success, json.dumps(data, indent=2))
        return success
    except Exception as e:
        print_test("GET /api/get_latest_location", False, str(e))
        return False


def test_get_real_gps():
    """Test get real GPS"""
    print_header("Testing Get Real GPS")
    try:
        params = {"deviceId": TEST_DEVICE_ID}
        response = requests.get(f"{BASE_URL}/api/get_real_gps", params=params)
        success = response.status_code == 200
        data = response.json() if success else {}
        print_test("GET /api/get_real_gps", success, json.dumps(data, indent=2))
        return success
    except Exception as e:
        print_test("GET /api/get_real_gps", False, str(e))
        return False


def test_esp32_save_location():
    """Test ESP32 save location"""
    print_header("Testing ESP32 Save Location")
    try:
        payload = {
            "latitude": TEST_LAT + 0.001,
            "longitude": TEST_LON + 0.001,
            "deviceId": TEST_DEVICE_ID
        }
        response = requests.post(
            f"{BASE_URL}/esp32/save_location",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        success = response.status_code == 200
        data = response.json() if success else {}
        print_test("POST /esp32/save_location", success, json.dumps(data, indent=2))
        return success
    except Exception as e:
        print_test("POST /esp32/save_location", False, str(e))
        return False


def test_root_redirect():
    """Test root redirect"""
    print_header("Testing Root Redirect")
    try:
        response = requests.get(f"{BASE_URL}/", allow_redirects=False)
        success = response.status_code in [301, 302, 307, 308]
        print_test("GET / (redirect)", success, f"Redirects to: {response.headers.get('location', 'N/A')}")
        return success
    except Exception as e:
        print_test("GET / (redirect)", False, str(e))
        return False


def test_map_page():
    """Test map page"""
    print_header("Testing Map Page")
    try:
        response = requests.get(f"{BASE_URL}/map")
        success = response.status_code == 200 and "html" in response.headers.get("content-type", "").lower()
        print_test("GET /map", success, f"Content-Type: {response.headers.get('content-type')}")
        return success
    except Exception as e:
        print_test("GET /map", False, str(e))
        return False


def test_api_docs():
    """Test API documentation"""
    print_header("Testing API Documentation")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        success = response.status_code == 200
        print_test("GET /docs (Swagger UI)", success)
        return success
    except Exception as e:
        print_test("GET /docs", False, str(e))
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  ?? Smart Cane GPS Tracker - API Test Suite")
    print("=" * 70)
    print(f"  Base URL: {BASE_URL}")
    print(f"  Test Device ID: {TEST_DEVICE_ID}")
    print(f"  Test Coordinates: {TEST_LAT}, {TEST_LON}")
    print(f"  Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=5)
    except Exception as e:
        print("\n? ERROR: Cannot connect to server!")
        print(f"   Make sure the server is running at {BASE_URL}")
        print(f"   Error: {e}")
        sys.exit(1)

    # Run tests
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Save Location (POST)", test_save_location_post()))
    results.append(("Save Location (GET)", test_save_location_get()))
    results.append(("Get Latest Location", test_get_latest_location()))
    results.append(("Get Real GPS", test_get_real_gps()))
    results.append(("ESP32 Save Location", test_esp32_save_location()))
    results.append(("Root Redirect", test_root_redirect()))
    results.append(("Map Page", test_map_page()))
    results.append(("API Documentation", test_api_docs()))

    # Summary
    print("\n" + "=" * 70)
    print("  ?? Test Summary")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "?" if success else "?"
        print(f"{status} {name}")
    
    print("\n" + "-" * 70)
    print(f"  Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=" * 70 + "\n")

    if passed == total:
        print("?? All tests passed!")
        sys.exit(0)
    else:
        print(f"??  {total - passed} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
