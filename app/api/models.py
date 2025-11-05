"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LocationRequest(BaseModel):
    """Request model for saving location"""
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    deviceId: Optional[str] = Field(default="SmartCane01", description="Device identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "latitude": 10.7769,
                "longitude": 106.7009,
                "deviceId": "SmartCane01"
            }
        }


class LocationResponse(BaseModel):
    """Response model for location data"""
    latitude: float
    longitude: float
    timestamp_server: str
    date_local: str
    time_local: str
    source: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "latitude": 10.7769,
                "longitude": 106.7009,
                "timestamp_server": "2025-11-02T10:30:00Z",
                "date_local": "02/11/2025",
                "time_local": "17:30:00",
                "source": "ESP32_REAL_GPS"
            }
        }


class StatusResponse(BaseModel):
    """Generic status response"""
    status: str
    message: str
    timestamp: Optional[str] = None
    coordinates: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Location saved successfully",
                "timestamp": "2025-11-02T10:30:00Z",
                "coordinates": {"lat": 10.7769, "lon": 106.7009}
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    status: str = "error"
    message: str
    detail: Optional[str] = None
