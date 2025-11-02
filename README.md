# ?? Smart Cane GPS Tracker

A modern, real-time GPS tracking system for Smart Cane devices built with FastAPI and cutting-edge 2025 UI/UX design principles.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## ? Features

### ?? Modern UI/UX (2025 Design)
- **Modern Typography**: Inter & Space Grotesk fonts for enhanced readability
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Dark/Light Mode**: Automatic theme switching with smooth transitions
- **Real-time Updates**: Live GPS tracking with visual feedback
- **Activity Log**: Track all system activities in real-time
- **Smooth Animations**: Fluid transitions and micro-interactions

### ?? Technical Features
- **FastAPI Backend**: High-performance async API framework
- **SQLite Database**: Lightweight, serverless database
- **Real-time GPS Tracking**: Support for ESP32 hardware GPS modules
- **RESTful API**: Well-documented endpoints with OpenAPI/Swagger
- **Automatic Sync**: Background synchronization with ESP32 devices
- **CORS Support**: Cross-origin resource sharing enabled
- **Type Safety**: Pydantic models for data validation

### ?? Device Support
- ESP32 Smart Cane devices
- Multiple device tracking capability
- Real-time GPS data transmission
- Offline data buffering

## ??? Project Structure

```
smart-cane-gps-tracker/
??? app/
?   ??? __init__.py
?   ??? main.py                 # FastAPI application entry point
?   ??? api/
?   ?   ??? __init__.py
?   ?   ??? routes.py           # API route handlers
?   ?   ??? models.py           # Pydantic models
?   ??? core/
?   ?   ??? __init__.py
?   ?   ??? config.py           # Application configuration
?   ?   ??? database.py         # Database operations
?   ??? services/
?   ?   ??? __init__.py
?   ?   ??? location_service.py # Business logic
?   ??? static/
?   ?   ??? css/
?   ?   ?   ??? styles.css      # Modern 2025 styles
?   ?   ??? js/
?   ?   ?   ??? app.js          # Frontend JavaScript
?   ?   ??? images/             # Leaflet map images
?   ??? templates/
?       ??? index.html          # Main web interface
??? database.db                 # SQLite database
??? requirements.txt            # Python dependencies
??? esp32_sync_fastapi.py       # ESP32 synchronization script
??? start_server.py             # Server startup script
??? .env                        # Environment variables (optional)
??? README.md                   # This file
```

## ?? Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository** (or navigate to the project directory)

```bash
cd /workspace
```

2. **Create and activate virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment** (optional)

Create a `.env` file in the root directory:

```env
# Application
APP_NAME="Smart Cane GPS Tracker"
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8080

# ESP32
ESP32_DEVICE_ID=SmartCane01
ESP32_IP=10.241.12.160

# Timezone
SERVER_TIMEZONE=Asia/Ho_Chi_Minh
```

### Running the Application

#### Method 1: Using Uvicorn directly

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

#### Method 2: Using the startup script

```bash
python start_server.py
```

The server will start and display:
```
?? Smart Cane GPS Tracker v2.0.0
======================================================================
?? Server running on: http://0.0.0.0:8080
?? Local IP address: 192.168.1.x
?? Map interface: http://192.168.1.x:8080/map
?? API Documentation: http://192.168.1.x:8080/docs
?? Server timezone: Asia/Ho_Chi_Minh
?? ESP32 Device ID: SmartCane01
======================================================================
```

### Starting ESP32 Sync (Optional)

To enable automatic synchronization with ESP32 devices:

```bash
python esp32_sync_fastapi.py
```

## ?? API Documentation

### Interactive API Docs

Once the server is running, visit:
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

### Main Endpoints

#### Save Location (POST)
```http
POST /save_location
Content-Type: application/json

{
  "latitude": 10.7769,
  "longitude": 106.7009,
  "deviceId": "SmartCane01"
}
```

#### Save Location (GET)
```http
GET /save_location?latitude=10.7769&longitude=106.7009&deviceId=SmartCane01
```

#### Get Latest Location
```http
GET /api/get_latest_location?deviceId=SmartCane01&forceRealTime=false
```

#### Get Real-time GPS
```http
GET /api/get_real_gps?deviceId=SmartCane01
```

#### ESP32 Endpoints
```http
POST /esp32/save_location
GET /esp32/save_location?latitude=10.7769&longitude=106.7009
```

### Response Format

```json
{
  "latitude": 10.7769,
  "longitude": 106.7009,
  "timestamp_server": "2025-11-02T10:30:00Z",
  "date_local": "02/11/2025",
  "time_local": "17:30:00",
  "source": "ESP32_REAL_GPS"
}
```

## ?? UI Features

### Dashboard Components

1. **Header Section**
   - Application logo and title
   - Version badge
   - Theme toggle (Light/Dark mode)

2. **Device Status Panel**
   - Real-time connection status
   - Device information
   - GPS coordinates display
   - Last update timestamp
   - Sync status indicator

3. **Activity Log**
   - Real-time activity tracking
   - Color-coded log entries
   - Auto-scrolling with history limit

4. **Interactive Map**
   - OpenStreetMap and Satellite views
   - Custom markers with animations
   - Popup information windows
   - Fullscreen mode
   - Auto-centering

5. **Control Buttons**
   - Get Real-time GPS
   - Center Map
   - Theme Toggle
   - Clear Activity Log

### Keyboard Shortcuts

- **F11**: Toggle fullscreen (browser default)
- **Ctrl + R**: Refresh page

## ?? Configuration

### Application Settings

Edit `app/core/config.py` or use environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | Smart Cane GPS Tracker | Application name |
| `APP_VERSION` | 2.0.0 | Version number |
| `HOST` | 0.0.0.0 | Server host |
| `PORT` | 8080 | Server port |
| `DATABASE_URL` | database.db | SQLite database path |
| `ESP32_DEVICE_ID` | SmartCane01 | Default device ID |
| `SERVER_TIMEZONE` | Asia/Ho_Chi_Minh | Server timezone |
| `AUTO_SYNC_ENABLED` | True | Enable auto-sync |
| `SYNC_INTERVAL` | 10 | Sync interval (seconds) |

## ?? Security Considerations

### Production Deployment

1. **Disable Debug Mode**
   ```python
   DEBUG = False
   ```

2. **Configure CORS**
   ```python
   CORS_ORIGINS = ["https://yourdomain.com"]
   ```

3. **Use Environment Variables**
   - Store sensitive data in `.env` file
   - Never commit `.env` to version control

4. **HTTPS**
   - Use reverse proxy (Nginx/Apache)
   - Enable SSL/TLS certificates

5. **Database Backup**
   - Regular backups of `database.db`
   - Use external storage for production

## ?? Testing

### Run Tests

```bash
pytest tests/
```

### Manual Testing

1. Open browser: http://localhost:8080
2. Verify map loads correctly
3. Test "Get Real-time GPS" button
4. Check activity log updates
5. Toggle theme (light/dark)
6. Test on mobile device

## ?? ESP32 Integration

### ESP32 Code Example

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

const char* serverURL = "http://192.168.1.x:8080/esp32/save_location";

void sendGPS(float lat, float lon) {
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  
  String payload = "{\"latitude\":" + String(lat, 6) + 
                   ",\"longitude\":" + String(lon, 6) + 
                   ",\"deviceId\":\"SmartCane01\"}";
  
  int httpCode = http.POST(payload);
  
  if (httpCode == 200) {
    Serial.println("? GPS data sent successfully");
  }
  
  http.end();
}
```

## ?? Troubleshooting

### Common Issues

**Issue**: Server won't start
- **Solution**: Check if port 8080 is already in use
  ```bash
  lsof -i :8080
  kill -9 <PID>
  ```

**Issue**: Map not loading
- **Solution**: Check internet connection (Leaflet CDN required)

**Issue**: GPS data not updating
- **Solution**: 
  - Verify ESP32 device is connected
  - Check network connectivity
  - Review server logs

**Issue**: Database errors
- **Solution**: 
  - Ensure write permissions on database file
  - Delete and recreate `database.db`

## ?? Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## ?? License

This project is licensed under the MIT License.

## ?? Authors

- Smart Cane Team

## ?? Acknowledgments

- FastAPI framework
- Leaflet.js for maps
- OpenStreetMap contributors
- Inter & Space Grotesk fonts

## ?? Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation
- Review the API docs at `/docs`

## ?? Version History

### Version 2.0.0 (2025-11-02)
- ? Complete refactor from Flask to FastAPI
- ?? Modern 2025 UI/UX design
- ?? Enhanced responsive design
- ?? Dark/Light theme support
- ?? Activity logging system
- ??? Improved map interface
- ?? Comprehensive API documentation
- ??? Professional codebase structure

### Version 1.0.0
- Initial Flask implementation
- Basic GPS tracking
- SQLite database
- Simple web interface

---

**Built with ?? using FastAPI and Modern Web Technologies**
