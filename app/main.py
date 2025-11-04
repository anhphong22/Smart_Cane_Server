"""
Smart Cane GPS Tracker - FastAPI Application
Modern GPS tracking system with real-time updates
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import socket
from pathlib import Path

from app.core.config import settings
from app.api.routes import router as main_router
from app.api.auth_routes import router as auth_router
from app.api.smart_routes import router as smart_router

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Real-time GPS tracking system for Smart Cane devices",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Include API routes
app.include_router(main_router)
app.include_router(auth_router)
app.include_router(smart_router)


@app.get("/", response_class=HTMLResponse, tags=["pages"])
async def root():
    """Root endpoint - redirects to map page"""
    return RedirectResponse(url="/map")


@app.get("/login", response_class=HTMLResponse, tags=["pages"])
async def login_page(request: Request):
    """Login page"""
    try:
        return templates.TemplateResponse("login.html", {"request": request})
    except Exception as e:
        print(f"❌ Error rendering login template: {e}")
        return HTMLResponse(
            content=f"<h1>Server Error</h1><p>Error rendering page: {str(e)}</p>",
            status_code=500
        )


@app.get("/map", response_class=HTMLResponse, tags=["pages"])
async def map_page(request: Request):
    """Main map display page"""
    try:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "device_id": settings.ESP32_DEVICE_ID,
                "app_name": settings.APP_NAME,
                "app_version": settings.APP_VERSION
            }
        )
    except Exception as e:
        print(f"❌ Error rendering template: {e}")
        return HTMLResponse(
            content=f"<h1>Server Error</h1><p>Error rendering page: {str(e)}</p>",
            status_code=500
        )


@app.get("/health", tags=["system"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


def get_local_ip() -> str:
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print(f"Could not get local IP address: {e}")
        return "127.0.0.1"


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    ip_address = get_local_ip()
    print("=" * 70)
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION}")
    print("=" * 70)
    print(f"📡 Server running on: http://{settings.HOST}:{settings.PORT}")
    print(f"🌐 Local IP address: {ip_address}")
    print(f"📍 Map interface: http://{ip_address}:{settings.PORT}/map")
    print(f"📚 API Documentation: http://{ip_address}:{settings.PORT}/docs")
    print(f"🌍 Server timezone: {settings.SERVER_TIMEZONE}")
    print(f"🔧 ESP32 Device ID: {settings.ESP32_DEVICE_ID}")
    print("=" * 70)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    print("\n👋 Shutting down Smart Cane GPS Tracker...")


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
