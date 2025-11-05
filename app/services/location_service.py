"""
Location service for business logic
"""
import datetime
import pytz
from typing import Optional, Dict, Any
from ..core.config import settings
from ..core.database import get_db


class LocationService:
    """Service for handling location operations"""
    
    def __init__(self):
        try:
            self.timezone = pytz.timezone(settings.SERVER_TIMEZONE)
        except pytz.exceptions.UnknownTimeZoneError:
            print(f"!!! Warning: Unknown timezone '{settings.SERVER_TIMEZONE}'. Using UTC.")
            self.timezone = pytz.utc
    
    def save_location(self, latitude: float, longitude: float, device_id: str = "SmartCane01") -> bool:
        """
        Save location to database
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            device_id: Device identifier
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db() as conn:
                if conn is None:
                    return False
                
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO locations (device_id, latitude, longitude) VALUES (?, ?, ?)",
                    (device_id, latitude, longitude)
                )
                conn.commit()
                print(f"?? Location saved: Device={device_id}, Lat={latitude:.6f}, Lon={longitude:.6f}")
                return True
        except Exception as e:
            print(f"? Error saving location: {e}")
            return False
    
    def get_latest_location(self, device_id: str = "SmartCane01", force_real_time: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get latest location for a device
        
        Args:
            device_id: Device identifier
            force_real_time: Use current time instead of stored timestamp
            
        Returns:
            Optional[Dict]: Location data or None if not found
        """
        try:
            with get_db() as conn:
                if conn is None:
                    return None
                
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT latitude, longitude, timestamp_server "
                    "FROM locations WHERE device_id = ? ORDER BY id DESC LIMIT 1",
                    (device_id,)
                )
                location_row = cursor.fetchone()
                
                if location_row:
                    if force_real_time:
                        current_time = datetime.datetime.now(self.timezone)
                        utc_iso_string = current_time.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                        date_local = current_time.strftime('%d/%m/%Y')
                        time_local = current_time.strftime('%H:%M:%S')
                        source = "ESP32_REAL_GPS"
                    else:
                        utc_dt_naive = datetime.datetime.strptime(
                            location_row['timestamp_server'], '%Y-%m-%d %H:%M:%S'
                        )
                        utc_dt_aware = pytz.utc.localize(utc_dt_naive)
                        local_dt_aware = utc_dt_aware.astimezone(self.timezone)
                        utc_iso_string = utc_dt_aware.strftime('%Y-%m-%dT%H:%M:%SZ')
                        date_local = local_dt_aware.strftime('%d/%m/%Y')
                        time_local = local_dt_aware.strftime('%H:%M:%S')
                        source = "ESP32_STORED"
                    
                    return {
                        "latitude": location_row['latitude'],
                        "longitude": location_row['longitude'],
                        "timestamp_server": utc_iso_string,
                        "date_local": date_local,
                        "time_local": time_local,
                        "source": source
                    }
                return None
        except Exception as e:
            print(f"? Error getting latest location: {e}")
            return None
    
    def get_real_gps(self, device_id: str = "SmartCane01") -> Optional[Dict[str, Any]]:
        """
        Get real-time GPS data
        
        Args:
            device_id: Device identifier
            
        Returns:
            Optional[Dict]: Location data with current timestamp or None
        """
        try:
            with get_db() as conn:
                if conn is None:
                    return None
                
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT latitude, longitude FROM locations WHERE device_id = ? ORDER BY id DESC LIMIT 1",
                    (device_id,)
                )
                location_row = cursor.fetchone()
                
                if location_row:
                    current_time = datetime.datetime.now(self.timezone)
                    utc_iso_string = current_time.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                    date_local = current_time.strftime('%d/%m/%Y')
                    time_local = current_time.strftime('%H:%M:%S')
                    
                    return {
                        "latitude": location_row['latitude'],
                        "longitude": location_row['longitude'],
                        "timestamp_server": utc_iso_string,
                        "date_local": date_local,
                        "time_local": time_local,
                        "source": "ESP32_REAL_GPS_FROM_DB"
                    }
                return None
        except Exception as e:
            print(f"? Error getting real GPS: {e}")
            return None


# Global service instance
location_service = LocationService()
