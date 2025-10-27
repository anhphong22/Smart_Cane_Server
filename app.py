from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
import sqlite3
import datetime
import pytz
import config
import traceback
import sys

app = Flask(__name__, template_folder='app/templates')
CORS(app)

SERVER_TIMEZONE_STR = 'Asia/Ho_Chi_Minh'
try:
    SERVER_TIMEZONE = pytz.timezone(SERVER_TIMEZONE_STR)
except pytz.exceptions.UnknownTimeZoneError:
    print(f"!!! LOI: Khong tim thay múi giờ '{SERVER_TIMEZONE_STR}'. Su dung UTC lam mac dinh.")
    SERVER_TIMEZONE = pytz.utc

def get_db_connection():
    try:
        conn = sqlite3.connect(config.DATABASE_URL)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"!!! CRITICAL: Could not connect to SQLite database: {e}")
        return None

def create_table_if_not_exists():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Failed to get database connection.")
        
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id VARCHAR(50) DEFAULT 'SmartCane01',
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                timestamp_server DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        print("Table 'locations' checked/created successfully in SQLite.")
    except Exception as e:
        print(f"Error creating table 'locations' in SQLite: {e}")
        print(traceback.format_exc())
    finally:
        if conn:
            conn.close()

create_table_if_not_exists()

@app.route('/save_location', methods=['GET', 'POST'])
def save_location():
    conn = None
    try:
        if request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({"status": "error", "message": "Invalid JSON"}), 400
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            device_id = data.get('deviceId', 'SmartCane01')
        else:  # GET request
            latitude = request.args.get('latitude', type=float)
            longitude = request.args.get('longitude', type=float)
            device_id = request.args.get('deviceId', default='SmartCane01', type=str)

        if latitude is None or longitude is None:
            print("Error in /save_location: Missing latitude or longitude parameters.")
            return jsonify({"status": "error", "message": "Missing latitude or longitude"}), 400

        conn = get_db_connection()
        if conn is None:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO locations (device_id, latitude, longitude) VALUES (?, ?, ?)",
            (device_id, latitude, longitude)
        )
        conn.commit()
        print(f"Data saved to SQLite: Device={device_id}, Lat={latitude}, Lon={longitude}")
        return jsonify({"status": "success", "message": "Location saved"}), 200
    except Exception as e:
        print(f"!!! Error in /save_location route: {e}")
        print(traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/esp32/save_location', methods=['GET', 'POST'])
def esp32_save_location():
    """API endpoint đặc biệt cho ESP32 thực tế với logging chi tiết"""
    conn = None
    try:
        if request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({"status": "error", "message": "Invalid JSON"}), 400
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            device_id = data.get('deviceId', 'SmartCane01')
        else:  # GET request
            latitude = request.args.get('latitude', type=float)
            longitude = request.args.get('longitude', type=float)
            device_id = request.args.get('deviceId', default='SmartCane01', type=str)

        if latitude is None or longitude is None:
            print("❌ ESP32 Error: Missing latitude or longitude parameters.")
            return jsonify({"status": "error", "message": "Missing latitude or longitude"}), 400

        conn = get_db_connection()
        if conn is None:
            print("❌ ESP32 Error: Database connection failed")
            return jsonify({"status": "error", "message": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO locations (device_id, latitude, longitude) VALUES (?, ?, ?)",
            (device_id, latitude, longitude)
        )
        conn.commit()
        
        # Log chi tiết với timestamp thực tế
        current_time = datetime.datetime.now(SERVER_TIMEZONE).strftime('%H:%M:%S')
        print(f"🚀 [{current_time}] ESP32 REAL DATA: Device={device_id}, Lat={latitude:.6f}, Lon={longitude:.6f}")
        print(f"   📡 Source: ESP32 Hardware GPS")
        print(f"   🌐 IP: {request.remote_addr}")
        
        return jsonify({
            "status": "success", 
            "message": "ESP32 location saved",
            "timestamp": datetime.datetime.now(SERVER_TIMEZONE).isoformat(),
            "coordinates": {"lat": latitude, "lon": longitude}
        }), 200
    except Exception as e:
        print(f"❌ ESP32 Error in /esp32/save_location route: {e}")
        print(traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/get_latest_location', methods=['GET'])
def get_latest_location_api():
    conn = None
    try:
        device_id = request.args.get('deviceId', default='SmartCane01', type=str)
        force_real_time = request.args.get('forceRealTime', default='false', type=str).lower() == 'true'
        
        conn = get_db_connection()
        if conn is None:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500
            
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT latitude, longitude, timestamp_server "
            "FROM locations WHERE device_id = ? ORDER BY id DESC LIMIT 1",
            (device_id,)
        )
        location_row = cursor.fetchone()
        
        if location_row:
            # Nếu forceRealTime=true, sử dụng thời gian hiện tại
            if force_real_time:
                current_time = datetime.datetime.now(SERVER_TIMEZONE)
                utc_iso_string = current_time.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                date_local = current_time.strftime('%d/%m/%Y')
                time_local = current_time.strftime('%H:%M:%S')
                print(f"🕐 Force real-time: Using current server time")
            else:
                # Sử dụng thời gian từ database
                utc_dt_naive = datetime.datetime.strptime(location_row['timestamp_server'], '%Y-%m-%d %H:%M:%S')
                utc_dt_aware = pytz.utc.localize(utc_dt_naive)
                local_dt_aware = utc_dt_aware.astimezone(SERVER_TIMEZONE)
                utc_iso_string = utc_dt_aware.strftime('%Y-%m-%dT%H:%M:%SZ')
                date_local = local_dt_aware.strftime('%d/%m/%Y')
                time_local = local_dt_aware.strftime('%H:%M:%S')
                print(f"📅 Database time: Using stored timestamp")

            data_to_return = {
                "latitude": location_row['latitude'],
                "longitude": location_row['longitude'],
                "timestamp_server": utc_iso_string,
                "date_local": date_local,
                "time_local": time_local,
                "source": "ESP32_REAL_GPS" if force_real_time else "ESP32_STORED"
            }
            print(f"API /api/get_latest_location returning data: {data_to_return}")
            return jsonify(data_to_return)
        else:
            print(f"API /api/get_latest_location: No data found for device_id: {device_id}")
            return jsonify(None)
    except Exception as e:
        print(f"!!! Error in /api/get_latest_location route: {e}")
        print(traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/get_real_gps', methods=['GET'])
def get_real_gps():
    """
    Lấy dữ liệu GPS "gần thời gian thực" từ database local.
    Dữ liệu này được cập nhật bởi script esp32_auto_sync.py.
    """
    conn = None
    try:
        device_id = request.args.get('deviceId', default='SmartCane01', type=str)
        
        print(f"🔄 API /api/get_real_gps: Querying for device_id: {device_id}")
        conn = get_db_connection()
        if conn is None:
            print(f"❌ API /api/get_real_gps: Database connection failed for device_id: {device_id}")
            return jsonify({"status": "error", "message": "Database connection failed"}), 500
            
        cursor = conn.cursor() # <--- DÒNG ĐƯỢC THÊM VÀO
        
        cursor.execute(
            "SELECT latitude, longitude FROM locations WHERE device_id = ? ORDER BY id DESC LIMIT 1",
            (device_id,)
        )
        location_row = cursor.fetchone()
        
        if location_row:
            print(f"✅ API /api/get_real_gps: Found data: Lat={location_row['latitude']}, Lon={location_row['longitude']}")
            # Luôn sử dụng thời gian hiện tại của server cho "real-time"
            current_time = datetime.datetime.now(SERVER_TIMEZONE)
            utc_iso_string = current_time.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            date_local = current_time.strftime('%d/%m/%Y')
            time_local = current_time.strftime('%H:%M:%S')

            data_to_return = {
                "latitude": location_row['latitude'],
                "longitude": location_row['longitude'],
                "timestamp_server": utc_iso_string,
                "date_local": date_local,
                "time_local": time_local,
                "source": "ESP32_REAL_GPS_FROM_DB"
            }
            print(f"✅ Real-time GPS from DB: Lat={data_to_return['latitude']}, Lon={data_to_return['longitude']}")
            return jsonify(data_to_return)
        else:
            print(f"❌ API /api/get_real_gps: No data found for device_id: {device_id} in database.")
            return jsonify(None)
            
    except Exception as e:
        print(f"!!! Error in /api/get_real_gps route: {e}", file=sys.stderr)
        sys.stdout.write(traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/')
def home():
    """Root route that redirects to the map page"""
    print(f"--- Request received for root route (/) ---")
    return redirect('/map')

@app.route('/map')
def map_page():
    print(f"--- Request received for /map route ---")
    try:
        return render_template('map_display.html', device_id='SmartCane01')
    except Exception as e:
        print(f"!!! CRITICAL ERROR rendering template for /map: {e}", file=sys.stderr)
        sys.stdout.write(traceback.format_exc())
        return "<h1>Server Error</h1><p>Sorry, there was an error rendering this page. Please check server logs for more details.</p>", 500

if __name__ == '__main__':
    import socket

    def get_ip_address():
        try:
            # Create a socket object and connect to a remote host to get the local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except Exception as e:
            print(f"Could not get local IP address: {e}")
            return "127.0.0.1"

    ip_address = get_ip_address()
    print(f"Starting Flask server on host 0.0.0.0, port 8080...")
    print(f"Server timezone configured as: {SERVER_TIMEZONE_STR}")
    print(f"*** Your local IP address is: {ip_address} ***")
    print(f"*** Please use this IP address in your ESP32 code. ***")
    app.run(host='0.0.0.0', port=8080, debug=True)

#   source venv/bin/activate