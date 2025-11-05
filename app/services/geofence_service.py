"""
Geofencing service - Smart Feature 1
Monitors device location and triggers alerts when entering/exiting defined zones
"""
import math
from typing import List, Optional, Dict, Any
from datetime import datetime
from ..core.database import get_db


class GeofenceService:
    """Service for geofencing operations"""
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two GPS coordinates using Haversine formula
        
        Args:
            lat1, lon1: First coordinate
            lat2, lon2: Second coordinate
            
        Returns:
            float: Distance in meters
        """
        R = 6371000  # Earth's radius in meters
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_phi / 2) ** 2 +
             math.cos(phi1) * math.cos(phi2) *
             math.sin(delta_lambda / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def create_geofence(self, user_id: int, name: str, latitude: float, 
                       longitude: float, radius: float, alert_on_enter: bool = True,
                       alert_on_exit: bool = True) -> Optional[int]:
        """Create a new geofence"""
        try:
            with get_db() as conn:
                if conn is None:
                    return None
                
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO geofences 
                       (user_id, name, latitude, longitude, radius, alert_on_enter, alert_on_exit)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (user_id, name, latitude, longitude, radius, alert_on_enter, alert_on_exit)
                )
                conn.commit()
                print(f"? Geofence '{name}' created for user {user_id}")
                return cursor.lastrowid
        except Exception as e:
            print(f"? Error creating geofence: {e}")
            return None
    
    def get_user_geofences(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all geofences for a user"""
        try:
            with get_db() as conn:
                if conn is None:
                    return []
                
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT id, name, latitude, longitude, radius, 
                              alert_on_enter, alert_on_exit, is_active, created_at
                       FROM geofences 
                       WHERE user_id = ? AND is_active = 1
                       ORDER BY created_at DESC""",
                    (user_id,)
                )
                
                geofences = []
                for row in cursor.fetchall():
                    geofences.append({
                        "id": row['id'],
                        "user_id": user_id,
                        "name": row['name'],
                        "latitude": row['latitude'],
                        "longitude": row['longitude'],
                        "radius": row['radius'],
                        "alert_on_enter": bool(row['alert_on_enter']),
                        "alert_on_exit": bool(row['alert_on_exit']),
                        "is_active": bool(row['is_active']),
                        "created_at": row['created_at']
                    })
                
                return geofences
        except Exception as e:
            print(f"? Error getting geofences: {e}")
            return []
    
    def check_geofence_breach(self, user_id: int, latitude: float, 
                             longitude: float) -> List[Dict[str, Any]]:
        """
        Check if current location breaches any geofences
        
        Returns list of triggered geofences with alert type
        """
        alerts = []
        geofences = self.get_user_geofences(user_id)
        
        for geofence in geofences:
            distance = self.calculate_distance(
                latitude, longitude,
                geofence['latitude'], geofence['longitude']
            )
            
            inside = distance <= geofence['radius']
            
            # Check for entry/exit
            if inside and geofence['alert_on_enter']:
                alerts.append({
                    "geofence_id": geofence['id'],
                    "geofence_name": geofence['name'],
                    "alert_type": "enter",
                    "distance": distance
                })
            elif not inside and geofence['alert_on_exit']:
                alerts.append({
                    "geofence_id": geofence['id'],
                    "geofence_name": geofence['name'],
                    "alert_type": "exit",
                    "distance": distance
                })
        
        return alerts
    
    def create_alert(self, geofence_id: int, alert_type: str, 
                    latitude: float, longitude: float) -> Optional[int]:
        """Create a geofence alert"""
        try:
            with get_db() as conn:
                if conn is None:
                    return None
                
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO geofence_alerts 
                       (geofence_id, alert_type, latitude, longitude)
                       VALUES (?, ?, ?, ?)""",
                    (geofence_id, alert_type, latitude, longitude)
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"? Error creating alert: {e}")
            return None
    
    def get_recent_alerts(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent geofence alerts for a user"""
        try:
            with get_db() as conn:
                if conn is None:
                    return []
                
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT a.id, a.geofence_id, g.name as geofence_name,
                              a.alert_type, a.latitude, a.longitude, 
                              a.timestamp, a.is_read
                       FROM geofence_alerts a
                       JOIN geofences g ON a.geofence_id = g.id
                       WHERE g.user_id = ?
                       ORDER BY a.timestamp DESC
                       LIMIT ?""",
                    (user_id, limit)
                )
                
                alerts = []
                for row in cursor.fetchall():
                    alerts.append({
                        "id": row['id'],
                        "geofence_id": row['geofence_id'],
                        "geofence_name": row['geofence_name'],
                        "alert_type": row['alert_type'],
                        "latitude": row['latitude'],
                        "longitude": row['longitude'],
                        "timestamp": row['timestamp'],
                        "is_read": bool(row['is_read'])
                    })
                
                return alerts
        except Exception as e:
            print(f"? Error getting alerts: {e}")
            return []
    
    def delete_geofence(self, geofence_id: int, user_id: int) -> bool:
        """Delete (deactivate) a geofence"""
        try:
            with get_db() as conn:
                if conn is None:
                    return False
                
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE geofences SET is_active = 0 WHERE id = ? AND user_id = ?",
                    (geofence_id, user_id)
                )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"? Error deleting geofence: {e}")
            return False


# Global service instance
geofence_service = GeofenceService()
