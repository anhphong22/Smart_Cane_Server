"""
Smart features API routes - Geofencing and Route History
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from .auth_models import Geofence, GeofenceResponse, GeofenceAlert
from ..services.geofence_service import geofence_service
from ..services.route_service import route_service
from ..core.security import get_current_user

router = APIRouter(tags=["smart-features"])


# ========== Geofencing Routes ==========

@router.post("/geofences", response_model=GeofenceResponse, status_code=201)
async def create_geofence(
    geofence_data: Geofence,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new geofence zone
    
    - **name**: Name of the geofence (e.g., "Home", "Office")
    - **latitude**: Center latitude
    - **longitude**: Center longitude
    - **radius**: Radius in meters
    - **alert_on_enter**: Trigger alert when entering zone
    - **alert_on_exit**: Trigger alert when exiting zone
    """
    geofence_id = geofence_service.create_geofence(
        user_id=current_user['user_id'],
        name=geofence_data.name,
        latitude=geofence_data.latitude,
        longitude=geofence_data.longitude,
        radius=geofence_data.radius,
        alert_on_enter=geofence_data.alert_on_enter,
        alert_on_exit=geofence_data.alert_on_exit
    )
    
    if not geofence_id:
        raise HTTPException(status_code=500, detail="Failed to create geofence")
    
    geofences = geofence_service.get_user_geofences(current_user['user_id'])
    created_geofence = next((g for g in geofences if g['id'] == geofence_id), None)
    
    if not created_geofence:
        raise HTTPException(status_code=500, detail="Geofence created but not found")
    
    return GeofenceResponse(**created_geofence)


@router.get("/geofences", response_model=List[GeofenceResponse])
async def get_geofences(current_user: dict = Depends(get_current_user)):
    """Get all active geofences for the current user"""
    geofences = geofence_service.get_user_geofences(current_user['user_id'])
    return [GeofenceResponse(**g) for g in geofences]


@router.delete("/geofences/{geofence_id}")
async def delete_geofence(
    geofence_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Delete (deactivate) a geofence"""
    success = geofence_service.delete_geofence(geofence_id, current_user['user_id'])
    
    if not success:
        raise HTTPException(status_code=404, detail="Geofence not found")
    
    return {"status": "success", "message": "Geofence deleted"}


@router.get("/geofence-alerts", response_model=List[GeofenceAlert])
async def get_geofence_alerts(
    limit: int = Query(default=10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """Get recent geofence alerts"""
    alerts = geofence_service.get_recent_alerts(current_user['user_id'], limit)
    return [GeofenceAlert(**a) for a in alerts]


@router.post("/geofences/check")
async def check_geofences(
    latitude: float,
    longitude: float,
    current_user: dict = Depends(get_current_user)
):
    """Check if current location triggers any geofence alerts"""
    alerts = geofence_service.check_geofence_breach(
        current_user['user_id'],
        latitude,
        longitude
    )
    
    # Create alert records
    for alert in alerts:
        geofence_service.create_alert(
            alert['geofence_id'],
            alert['alert_type'],
            latitude,
            longitude
        )
    
    return {
        "alerts_triggered": len(alerts),
        "alerts": alerts
    }


# ========== Route History Routes ==========

@router.get("/route-history")
async def get_route_history(
    device_id: str = Query(default="SmartCane01"),
    hours: int = Query(default=24, ge=1, le=168),
    current_user: dict = Depends(get_current_user)
):
    """
    Get location history for route playback
    
    - **device_id**: Device identifier
    - **hours**: Hours of history to retrieve (1-168)
    """
    route_points = route_service.get_route_history(
        user_id=current_user['user_id'],
        device_id=device_id,
        hours=hours
    )
    
    analytics = route_service.analyze_route(route_points)
    
    return {
        "route_points": route_points,
        "analytics": analytics
    }


@router.get("/route-analytics")
async def get_route_analytics(
    device_id: str = Query(default="SmartCane01"),
    hours: int = Query(default=24, ge=1, le=168),
    current_user: dict = Depends(get_current_user)
):
    """Get route analytics without full point data"""
    route_points = route_service.get_route_history(
        user_id=current_user['user_id'],
        device_id=device_id,
        hours=hours
    )
    
    return route_service.analyze_route(route_points)


@router.get("/daily-summary")
async def get_daily_summary(
    device_id: str = Query(default="SmartCane01"),
    days: int = Query(default=7, ge=1, le=30),
    current_user: dict = Depends(get_current_user)
):
    """
    Get daily activity summary
    
    - **device_id**: Device identifier
    - **days**: Number of days to summarize (1-30)
    """
    summaries = route_service.get_daily_summary(
        user_id=current_user['user_id'],
        device_id=device_id,
        days=days
    )
    
    return {"summaries": summaries}


@router.post("/save-route")
async def save_route(
    device_id: str,
    route_name: str,
    start_time: str,
    end_time: str,
    total_distance: float,
    current_user: dict = Depends(get_current_user)
):
    """Save a named route to history"""
    route_id = route_service.save_route(
        user_id=current_user['user_id'],
        device_id=device_id,
        route_name=route_name,
        start_time=start_time,
        end_time=end_time,
        total_distance=total_distance
    )
    
    if not route_id:
        raise HTTPException(status_code=500, detail="Failed to save route")
    
    return {
        "status": "success",
        "route_id": route_id,
        "message": f"Route '{route_name}' saved successfully"
    }


@router.get("/saved-routes")
async def get_saved_routes(current_user: dict = Depends(get_current_user)):
    """Get user's saved routes"""
    routes = route_service.get_saved_routes(current_user['user_id'])
    return {"routes": routes}
