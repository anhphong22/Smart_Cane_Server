"""
Route History Service - Smart Feature 2
Tracks and replays historical routes with analytics
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import math
from ..core.database import get_db


class RouteService:
    """Service for route history tracking and playback"""
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in meters"""
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
    
    def get_route_history(self, user_id: int, device_id: str = "SmartCane01", 
                         hours: int = 24) -> List[Dict[str, Any]]:
        """
        Get location history for route playback
        
        Args:
            user_id: User ID
            device_id: Device identifier
            hours: Number of hours to look back
            
        Returns:
            List of location points with timestamps
        """
        try:
            with get_db() as conn:
                if conn is None:
                    return []
                
                cursor = conn.cursor()
                since_time = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
                
                cursor.execute(
                    """SELECT id, latitude, longitude, timestamp_server
                       FROM locations
                       WHERE device_id = ? AND timestamp_server >= ?
                       ORDER BY timestamp_server ASC""",
                    (device_id, since_time)
                )
                
                route_points = []
                for row in cursor.fetchall():
                    route_points.append({
                        "id": row['id'],
                        "latitude": row['latitude'],
                        "longitude": row['longitude'],
                        "timestamp": row['timestamp_server']
                    })
                
                return route_points
        except Exception as e:
            print(f"? Error getting route history: {e}")
            return []
    
    def analyze_route(self, route_points: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze route data and generate statistics
        
        Args:
            route_points: List of location points
            
        Returns:
            Dictionary with route analytics
        """
        if not route_points or len(route_points) < 2:
            return {
                "total_distance": 0,
                "total_points": len(route_points),
                "duration_minutes": 0,
                "average_speed": 0,
                "start_time": None,
                "end_time": None
            }
        
        # Calculate total distance
        total_distance = 0
        for i in range(len(route_points) - 1):
            p1 = route_points[i]
            p2 = route_points[i + 1]
            distance = self.calculate_distance(
                p1['latitude'], p1['longitude'],
                p2['latitude'], p2['longitude']
            )
            total_distance += distance
        
        # Calculate duration
        try:
            start_time = datetime.fromisoformat(route_points[0]['timestamp'].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(route_points[-1]['timestamp'].replace('Z', '+00:00'))
            duration = (end_time - start_time).total_seconds() / 60  # minutes
        except:
            duration = 0
            start_time = None
            end_time = None
        
        # Calculate average speed (km/h)
        average_speed = 0
        if duration > 0:
            average_speed = (total_distance / 1000) / (duration / 60)
        
        return {
            "total_distance": round(total_distance, 2),  # meters
            "total_distance_km": round(total_distance / 1000, 2),  # kilometers
            "total_points": len(route_points),
            "duration_minutes": round(duration, 2),
            "average_speed": round(average_speed, 2),  # km/h
            "start_time": route_points[0]['timestamp'],
            "end_time": route_points[-1]['timestamp'],
            "start_location": {
                "latitude": route_points[0]['latitude'],
                "longitude": route_points[0]['longitude']
            },
            "end_location": {
                "latitude": route_points[-1]['latitude'],
                "longitude": route_points[-1]['longitude']
            }
        }
    
    def get_daily_summary(self, user_id: int, device_id: str = "SmartCane01", 
                         days: int = 7) -> List[Dict[str, Any]]:
        """
        Get daily activity summary
        
        Args:
            user_id: User ID
            device_id: Device identifier
            days: Number of days to analyze
            
        Returns:
            List of daily summaries
        """
        try:
            with get_db() as conn:
                if conn is None:
                    return []
                
                cursor = conn.cursor()
                since_date = (datetime.utcnow() - timedelta(days=days)).date().isoformat()
                
                cursor.execute(
                    """SELECT DATE(timestamp_server) as date,
                              COUNT(*) as points_count,
                              MIN(timestamp_server) as first_activity,
                              MAX(timestamp_server) as last_activity
                       FROM locations
                       WHERE device_id = ? AND DATE(timestamp_server) >= ?
                       GROUP BY DATE(timestamp_server)
                       ORDER BY date DESC""",
                    (device_id, since_date)
                )
                
                summaries = []
                for row in cursor.fetchall():
                    summaries.append({
                        "date": row['date'],
                        "points_count": row['points_count'],
                        "first_activity": row['first_activity'],
                        "last_activity": row['last_activity']
                    })
                
                return summaries
        except Exception as e:
            print(f"? Error getting daily summary: {e}")
            return []
    
    def save_route(self, user_id: int, device_id: str, route_name: str,
                   start_time: str, end_time: str, total_distance: float) -> Optional[int]:
        """Save a named route to history"""
        try:
            with get_db() as conn:
                if conn is None:
                    return None
                
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO route_history 
                       (user_id, device_id, route_name, start_time, end_time, total_distance)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (user_id, device_id, route_name, start_time, end_time, total_distance)
                )
                conn.commit()
                print(f"? Route '{route_name}' saved for user {user_id}")
                return cursor.lastrowid
        except Exception as e:
            print(f"? Error saving route: {e}")
            return None
    
    def get_saved_routes(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user's saved routes"""
        try:
            with get_db() as conn:
                if conn is None:
                    return []
                
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT id, device_id, route_name, start_time, end_time, total_distance
                       FROM route_history
                       WHERE user_id = ?
                       ORDER BY start_time DESC""",
                    (user_id,)
                )
                
                routes = []
                for row in cursor.fetchall():
                    routes.append({
                        "id": row['id'],
                        "device_id": row['device_id'],
                        "route_name": row['route_name'],
                        "start_time": row['start_time'],
                        "end_time": row['end_time'],
                        "total_distance": row['total_distance']
                    })
                
                return routes
        except Exception as e:
            print(f"? Error getting saved routes: {e}")
            return []


# Global service instance
route_service = RouteService()
