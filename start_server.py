#!/usr/bin/env python3
"""
Smart Cane GPS Tracker - Server Startup Script
Starts the FastAPI application with Uvicorn
"""

import uvicorn
from app.core.config import settings


def main():
    """Main function to start the server"""
    
    print("\n" + "=" * 70)
    print(f"?? Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print("=" * 70 + "\n")
    
    # Run the FastAPI application
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
        access_log=True
    )


if __name__ == "__main__":
    main()
