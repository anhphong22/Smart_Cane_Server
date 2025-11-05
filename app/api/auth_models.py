"""
Authentication models
"""
from pydantic import BaseModel, Field
from typing import Optional


class UserLogin(BaseModel):
    """Login request model"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin123"
            }
        }


class UserRegister(BaseModel):
    """User registration model"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    email: Optional[str] = Field(None, max_length=100)
    full_name: Optional[str] = Field(None, max_length=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "secure123",
                "email": "john@example.com",
                "full_name": "John Doe"
            }
        }


class Token(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    """User response model"""
    user_id: int
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    created_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "username": "admin",
                "email": "admin@example.com",
                "full_name": "Administrator",
                "created_at": "2025-11-02T10:00:00Z"
            }
        }


class Geofence(BaseModel):
    """Geofence model"""
    name: str = Field(..., max_length=100)
    latitude: float
    longitude: float
    radius: float = Field(..., gt=0, description="Radius in meters")
    alert_on_enter: bool = True
    alert_on_exit: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Home",
                "latitude": 10.7769,
                "longitude": 106.7009,
                "radius": 500,
                "alert_on_enter": True,
                "alert_on_exit": True
            }
        }


class GeofenceResponse(Geofence):
    """Geofence response model"""
    id: int
    user_id: int
    created_at: str
    is_active: bool = True


class GeofenceAlert(BaseModel):
    """Geofence alert model"""
    id: int
    geofence_id: int
    geofence_name: str
    alert_type: str  # 'enter' or 'exit'
    latitude: float
    longitude: float
    timestamp: str
