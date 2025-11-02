# ?? Quick Start Guide

Get your Smart Cane GPS Tracker up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
# Navigate to project directory
cd /workspace

# Activate virtual environment (if using one)
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

## Step 2: Start the Server

### Option A: Using the startup script (Recommended)
```bash
python3 start_server.py
```

### Option B: Using uvicorn directly
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## Step 3: Access the Application

Once the server starts, you'll see:
```
?? Smart Cane GPS Tracker v2.0.0
======================================================================
?? Server running on: http://0.0.0.0:8080
?? Local IP address: 192.168.1.x
?? Map interface: http://192.168.1.x:8080/map
?? API Documentation: http://192.168.1.x:8080/docs
======================================================================
```

Open your browser and go to:
- **Main Interface**: http://localhost:8080/map
- **API Docs**: http://localhost:8080/docs

## Step 4: Test the Application

### Manual Test
1. Open http://localhost:8080/map in your browser
2. Click the "Get Real-time GPS" button
3. Watch the map update with location data

### Automated Test
```bash
# In a new terminal, run the test script
python3 test_api.py
```

## Step 5: Configure ESP32 (Optional)

If you have an ESP32 device:

1. Update the ESP32 code with your server IP:
```cpp
const char* serverURL = "http://YOUR_SERVER_IP:8080/esp32/save_location";
```

2. Start the sync script:
```bash
python3 esp32_sync_fastapi.py
```

## Common Commands

### Start Server
```bash
python3 start_server.py
```

### Start ESP32 Sync
```bash
python3 esp32_sync_fastapi.py
```

### Run Tests
```bash
python3 test_api.py
```

### View API Documentation
```bash
# Start server first, then open browser to:
http://localhost:8080/docs
```

## Troubleshooting

### Port Already in Use
```bash
# Kill process using port 8080
lsof -i :8080
kill -9 <PID>

# Or change port in .env file
echo "PORT=8081" > .env
```

### Dependencies Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database Issues
```bash
# Remove and recreate database
rm database.db
python3 start_server.py
```

## Next Steps

- ?? Read the [README.md](README.md) for detailed documentation
- ?? Check [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) if migrating from Flask
- ?? Run tests with `python3 test_api.py`
- ?? Customize the UI in `app/static/css/styles.css`
- ?? Configure settings in `app/core/config.py` or `.env`

## Need Help?

- Check the [README.md](README.md) for detailed information
- View API documentation at http://localhost:8080/docs
- Review the code in the `app/` directory
- Open an issue on GitHub

---

**Happy Tracking! ????**
