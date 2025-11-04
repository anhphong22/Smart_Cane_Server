"""
API route handlers
"""
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from typing import Optional
import datetime
import pytz
from .models import LocationRequest, LocationResponse, StatusResponse
from app.core.config import settings
from app.services.location_service import location_service

router = APIRouter()


@router.post("/save_location", response_model=StatusResponse, tags=["locations"])
async def save_location(location: LocationRequest):
    """
    Save GPS location data
    
    - **latitude**: Latitude coordinate
    - **longitude**: Longitude coordinate
    - **deviceId**: Device identifier (optional, defaults to SmartCane01)
    """
    try:
        success = location_service.save_location(
            latitude=location.latitude,
            longitude=location.longitude,
            device_id=location.deviceId
        )

        if success:
            return StatusResponse(
                status="success",
                message="Location saved",
                timestamp=datetime.datetime.now(pytz.timezone(settings.SERVER_TIMEZONE)).isoformat(),
                coordinates={"lat": location.latitude, "lon": location.longitude}
            )
        else:
            raise HTTPException(status_code=500, detail="Database operation failed")
    except Exception as e:
        print(f"? Error in /save_location: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/save_location", response_model=StatusResponse, tags=["locations"])
async def save_location_get(
    latitude: float = Query(..., description="Latitude coordinate"),
    longitude: float = Query(..., description="Longitude coordinate"),
    deviceId: str = Query(default="SmartCane01", description="Device identifier")
):
    """
    Save GPS location data via GET request (for ESP32 compatibility)
    """
    try:
        success = location_service.save_location(
            latitude=latitude,
            longitude=longitude,
            device_id=deviceId
        )

        if success:
            return StatusResponse(
                status="success",
                message="Location saved",
                timestamp=datetime.datetime.now(pytz.timezone(settings.SERVER_TIMEZONE)).isoformat(),
                coordinates={"lat": latitude, "lon": longitude}
            )
        else:
            raise HTTPException(status_code=500, detail="Database operation failed")
    except Exception as e:
        print(f"? Error in /save_location (GET): {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/esp32/save_location", response_model=StatusResponse, tags=["esp32"])
async def esp32_save_location(location: LocationRequest, request: Request):
    """
    Special endpoint for ESP32 device with detailed logging
    """
    try:
        success = location_service.save_location(
            latitude=location.latitude,
            longitude=location.longitude,
            device_id=location.deviceId
        )

        if success:
            current_time = datetime.datetime.now(pytz.timezone(settings.SERVER_TIMEZONE))
            time_str = current_time.strftime('%H:%M:%S')

            print(f"?? [{time_str}] ESP32 REAL DATA: Device={location.deviceId}, "
                  f"Lat={location.latitude:.6f}, Lon={location.longitude:.6f}")
            print(f"   ?? Source: ESP32 Hardware GPS")
            print(f"   ?? IP: {request.client.host}")

            return StatusResponse(
                status="success",
                message="ESP32 location saved",
                timestamp=current_time.isoformat(),
                coordinates={"lat": location.latitude, "lon": location.longitude}
            )
        else:
            raise HTTPException(status_code=500, detail="Database operation failed")
    except Exception as e:
        print(f"? ESP32 Error in /esp32/save_location: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/esp32/save_location", response_model=StatusResponse, tags=["esp32"])
async def esp32_save_location_get(
    latitude: float = Query(..., description="Latitude coordinate"),
    longitude: float = Query(..., description="Longitude coordinate"),
    deviceId: str = Query(default="SmartCane01", description="Device identifier"),
    request: Request = None
):
    """
    ESP32 endpoint via GET request
    """
    try:
        success = location_service.save_location(
            latitude=latitude,
            longitude=longitude,
            device_id=deviceId
        )

        if success:
            current_time = datetime.datetime.now(pytz.timezone(settings.SERVER_TIMEZONE))
            time_str = current_time.strftime('%H:%M:%S')

            print(f"?? [{time_str}] ESP32 REAL DATA: Device={deviceId}, "
                  f"Lat={latitude:.6f}, Lon={longitude:.6f}")
            print(f"   ?? Source: ESP32 Hardware GPS")
            print(f"   ?? IP: {request.client.host if request else 'unknown'}")

            return StatusResponse(
                status="success",
                message="ESP32 location saved",
                timestamp=current_time.isoformat(),
                coordinates={"lat": latitude, "lon": longitude}
            )
        else:
            raise HTTPException(status_code=500, detail="Database operation failed")
    except Exception as e:
        print(f"? ESP32 Error in /esp32/save_location (GET): {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/get_latest_location", response_model=Optional[LocationResponse], tags=["locations"])
async def get_latest_location(
    deviceId: str = Query(default="SmartCane01", description="Device identifier"),
    forceRealTime: bool = Query(default=False, description="Use current time instead of stored timestamp")
):
    """
    Get the latest GPS location for a device
    """
    try:
        data = location_service.get_latest_location(
            device_id=deviceId,
            force_real_time=forceRealTime
        )

        if data:
            return LocationResponse(**data)
        else:
            return JSONResponse(content=None, status_code=200)
    except Exception as e:
        print(f"? Error in /api/get_latest_location: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/get_real_gps", response_model=Optional[LocationResponse], tags=["locations"])
async def get_real_gps(
    deviceId: str = Query(default="SmartCane01", description="Device identifier")
):
    """
    Get real-time GPS data from database with current timestamp
    """
    try:
        print(f"?? API /api/get_real_gps: Querying for device_id: {deviceId}")

        data = location_service.get_real_gps(device_id=deviceId)

        if data:
            print(f"? Real-time GPS from DB: Lat={data['latitude']}, Lon={data['longitude']}")
            return LocationResponse(**data)
        else:
            print(f"? API /api/get_real_gps: No data found for device_id: {deviceId}")
            return JSONResponse(content=None, status_code=200)
    except Exception as e:
        print(f"? Error in /api/get_real_gps: {e}")
        raise HTTPException(status_code=500, detail=str(e))
