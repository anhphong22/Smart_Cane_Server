"""
Authentication service
"""
import sqlite3
from typing import Optional, Dict, Any
from datetime import datetime
from ..core.database import get_db
from ..core.security import get_password_hash, verify_password, create_access_token


class AuthService:
    """Service for authentication operations"""
    
    def create_user(self, username: str, password: str, email: Optional[str] = None, 
                   full_name: Optional[str] = None) -> Optional[int]:
        """
        Create a new user
        
        Args:
            username: Username
            password: Plain text password
            email: Email address
            full_name: Full name
            
        Returns:
            Optional[int]: User ID if successful, None otherwise
        """
        try:
            with get_db() as conn:
                if conn is None:
                    return None
                
                cursor = conn.cursor()
                
                # Check if username exists
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                if cursor.fetchone():
                    return None  # Username already exists
                
                # Hash password and create user
                hashed_password = get_password_hash(password)
                cursor.execute(
                    """INSERT INTO users (username, password_hash, email, full_name, created_at) 
                       VALUES (?, ?, ?, ?, ?)""",
                    (username, hashed_password, email, full_name, datetime.utcnow().isoformat())
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"? Error creating user: {e}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with username and password
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            Optional[Dict]: User data if authenticated, None otherwise
        """
        try:
            with get_db() as conn:
                if conn is None:
                    return None
                
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, username, password_hash, email, full_name FROM users WHERE username = ?",
                    (username,)
                )
                user_row = cursor.fetchone()
                
                if not user_row:
                    return None
                
                # Verify password
                if not verify_password(password, user_row['password_hash']):
                    return None
                
                return {
                    "user_id": user_row['id'],
                    "username": user_row['username'],
                    "email": user_row['email'],
                    "full_name": user_row['full_name']
                }
        except Exception as e:
            print(f"? Error authenticating user: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            with get_db() as conn:
                if conn is None:
                    return None
                
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT id, username, email, full_name, created_at 
                       FROM users WHERE id = ?""",
                    (user_id,)
                )
                user_row = cursor.fetchone()
                
                if not user_row:
                    return None
                
                return {
                    "user_id": user_row['id'],
                    "username": user_row['username'],
                    "email": user_row['email'],
                    "full_name": user_row['full_name'],
                    "created_at": user_row['created_at']
                }
        except Exception as e:
            print(f"? Error getting user: {e}")
            return None
    
    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Login user and generate token
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            Optional[Dict]: Token and user data if successful
        """
        user = self.authenticate_user(username, password)
        if not user:
            return None
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user["username"], "user_id": user["user_id"]}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }


# Global service instance
auth_service = AuthService()
