#!/usr/bin/env python3
"""
Create default admin user
Run this once to create the admin account
"""
import sys
sys.path.insert(0, '/workspace')

from app.services.auth_service import auth_service

def create_admin():
    print("Creating default admin user...")
    
    user_id = auth_service.create_user(
        username="admin",
        password="admin123",
        email="admin@smartcane.com",
        full_name="Administrator"
    )
    
    if user_id:
        print(f"? Admin user created successfully (ID: {user_id})")
        print("\n?? Login credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n??  Please change the password after first login!")
    else:
        print("? Failed to create admin user (may already exist)")
        print("   Try logging in with: admin / admin123")

if __name__ == "__main__":
    create_admin()
