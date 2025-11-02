# ?? Smart Cane GPS Tracker v2.0

A modern, secure GPS tracking system with authentication and smart features built with FastAPI.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)

## ? Features

### ?? Authentication & Security
- **JWT-based Authentication**: Secure token-based auth
- **User Management**: Login/logout with session handling
- **Protected Routes**: API endpoints secured with Bearer tokens
- **Default Admin Account**: `admin` / `admin123`

### ?? Smart Features

#### 1. ?? Geofencing System
- Create virtual boundaries around locations
- Alert on zone entry/exit
- Multiple geofences per user
- Real-time breach detection
- Visual geofence display on map

#### 2. ?? Route History & Analytics
- Track movement history
- Route playback with timeline
- Distance and duration analytics
- Average speed calculation
- Daily activity summaries
- Save and replay named routes

### ?? Modern UI (2025 Design)
- **Responsive Design**: Works on all devices
- **Dark/Light Mode**: Theme toggle
- **Real-time Updates**: Live GPS tracking
- **Activity Logging**: Track all system events
- **Interactive Maps**: Multiple layers, custom markers

### ?? Technical Features
- **FastAPI Backend**: High-performance async API
- **SQLite Database**: Lightweight, serverless
- **RESTful API**: Well-documented with OpenAPI/Swagger
- **Real-time GPS**: Support for ESP32 hardware
- **Auto-refresh**: Background synchronization

## ?? Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python3 start_server.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### 3. Access the Application

- **Login Page**: http://localhost:8080/login
- **Main Interface**: http://localhost:8080/map
- **API Documentation**: http://localhost:8080/docs

### 4. Default Credentials

```
Username: admin
Password: admin123
```

## ??? Project Structure

```
/workspace/
??? app/
?   ??? __init__.py
?   ??? main.py                     # FastAPI application
?   ??? api/
?   ?   ??? __init__.py
?   ?   ??? routes.py               # GPS tracking routes
?   ?   ??? auth_routes.py          # Authentication routes
?   ?   ??? smart_routes.py         # Smart features routes
?   ?   ??? models.py               # GPS data models
?   ?   ??? auth_models.py          # Auth & smart feature models
?   ??? core/
?   ?   ??? __init__.py
?   ?   ??? config.py               # Configuration
?   ?   ??? database.py             # Database operations
?   ?   ??? security.py             # JWT & auth utilities
?   ??? services/
?   ?   ??? __init__.py
?   ?   ??? location_service.py     # Location business logic
?   ?   ??? auth_service.py         # Authentication service
?   ?   ??? geofence_service.py     # Geofencing service
?   ?   ??? route_service.py        # Route history service
?   ??? static/
?   ?   ??? css/
?   ?   ?   ??? styles.css          # Modern 2025 styles
?   ?   ??? js/
?   ?       ??? app.js              # Frontend application
?   ??? templates/
?       ??? index.html              # Main dashboard
?       ??? login.html              # Login page
??? database.db                      # SQLite database
??? requirements.txt                 # Python dependencies
??? start_server.py                  # Server startup script
??? esp32_sync_fastapi.py           # ESP32 sync tool
??? README.md                        # This file
```

## ?? API Documentation

### Authentication Endpoints

#### POST `/auth/register`
Register a new user
```json
{
  "username": "john_doe",
  "password": "secure123",
  "email": "john@example.com",
  "full_name": "John Doe"
}
```

#### POST `/auth/login`
Login and get JWT token
```json
{
  "username": "admin",
  "password": "admin123"
}
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "user_id": 1,
    "username": "admin",
    "email": "admin@smartcane.com"
  }
}
```

#### GET `/auth/me`
Get current user info (requires authentication)

Headers: `Authorization: Bearer <token>`

#### POST `/auth/logout`
Logout current user

### Smart Features Endpoints

#### Geofencing

**POST `/geofences`** - Create geofence
```json
{
  "name": "Home",
  "latitude": 10.7769,
  "longitude": 106.7009,
  "radius": 500,
  "alert_on_enter": true,
  "alert_on_exit": true
}
```

**GET `/geofences`** - List user's geofences

**DELETE `/geofences/{id}`** - Delete geofence

**GET `/geofence-alerts`** - Get recent alerts

**POST `/geofences/check`** - Check location against geofences

#### Route History

**GET `/route-history?hours=24`** - Get route history

**GET `/route-analytics?hours=24`** - Get route analytics only

**GET `/daily-summary?days=7`** - Get daily activity summary

**POST `/save-route`** - Save a named route

**GET `/saved-routes`** - Get user's saved routes

### GPS Tracking Endpoints

#### POST `/save_location`
Save GPS location
```json
{
  "latitude": 10.7769,
  "longitude": 106.7009,
  "deviceId": "SmartCane01"
}
```

#### GET `/api/get_latest_location`
Get latest GPS location

#### GET `/api/get_real_gps`
Get real-time GPS data

#### POST `/esp32/save_location`
ESP32-specific endpoint with detailed logging

## ?? Security

### JWT Authentication
- Token-based authentication
- Bearer token in Authorization header
- Tokens expire after 24 hours
- Secure password hashing with bcrypt

### Password Security
- Bcrypt hashing
- Salt rounds: Auto-configured
- Password minimum length: 6 characters

### API Security
- All smart features require authentication
- CORS configured
- SQL injection prevention (parameterized queries)
- XSS prevention (template escaping)

## ?? Smart Features Guide

### Geofencing

1. **Create a Geofence**
   - Click "Add Geofence" in the UI (or use API)
   - Set name, location, and radius
   - Enable entry/exit alerts

2. **Monitor Alerts**
   - Alerts appear in activity log
   - API endpoint for programmatic access
   - Alert history stored in database

3. **Use Cases**
   - Home/Safe Zone monitoring
   - Medical facility boundaries
   - Restricted area alerts

### Route History

1. **View Route**
   - Select time range (1 hour to 1 week)
   - Click "Show Route"
   - Route displayed as red line on map

2. **Analytics**
   - Total distance traveled
   - Duration
   - Average speed
   - Number of GPS points

3. **Daily Summary**
   - Activity overview per day
   - First and last activity times
   - Movement patterns

## ?? Configuration

### Environment Variables

Create `.env` file:
```env
APP_NAME="Smart Cane GPS Tracker"
APP_VERSION="2.0.0"
DEBUG=True

HOST=0.0.0.0
PORT=8080

DATABASE_URL=database.db
ESP32_DEVICE_ID=SmartCane01

SERVER_TIMEZONE=Asia/Ho_Chi_Minh
```

### Database Schema

The app automatically creates these tables:
- `users` - User accounts
- `locations` - GPS tracking data
- `geofences` - Geofence definitions
- `geofence_alerts` - Alert history
- `route_history` - Saved routes

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
    Serial.println("? GPS data sent");
  }
  
  http.end();
}
```

## ?? Testing

### Run API Tests

```bash
python3 test_api.py
```

### Manual Testing

1. Start server: `python3 start_server.py`
2. Open browser: http://localhost:8080/login
3. Login with admin/admin123
4. Test features:
   - GPS tracking
   - Create geofence
   - View route history
   - Toggle dark mode
   - Logout

## ?? Troubleshooting

### Port Already in Use
```bash
lsof -i :8080
kill -9 <PID>
```

### Database Errors
```bash
rm database.db
python3 start_server.py  # Will recreate database
```

### Authentication Issues
- Clear browser localStorage
- Delete and recreate admin user in database
- Check token expiration (24 hours)

### Dependencies Not Found
```bash
pip install -r requirements.txt --force-reinstall
```

## ?? Performance

- **Response Time**: <100ms for most API calls
- **Concurrent Users**: Supports multiple users
- **Database**: SQLite (suitable for small to medium deployments)
- **Map Rendering**: Client-side with Leaflet.js

## ?? Future Enhancements

- [ ] Multi-device dashboard
- [ ] WebSocket real-time updates
- [ ] Push notifications for geofence alerts
- [ ] Advanced analytics dashboard
- [ ] Export routes to GPX/KML
- [ ] Mobile app (PWA)
- [ ] Admin panel for user management

## ?? License

MIT License

## ?? Support

For issues and questions:
- Check the API documentation at `/docs`
- Review this README
- Open an issue on GitHub

## ?? Acknowledgments

- FastAPI framework
- Leaflet.js for maps
- OpenStreetMap contributors
- Inter & Space Grotesk fonts

---

**Built with ?? using FastAPI, Modern Web Technologies & 2025 Design Principles**

*Smart Cane GPS Tracker v2.0 - Secure, Smart, Modern*
