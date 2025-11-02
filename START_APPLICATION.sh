#!/bin/bash
# Smart Cane GPS Tracker - Quick Start Script

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║           🦯 Smart Cane GPS Tracker v2.0 - Quick Start 🦯            ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if admin user exists
if [ ! -f "database.db" ]; then
    echo "📦 Creating database and admin user..."
    python3 create_admin.py
    echo ""
fi

echo "🚀 Starting FastAPI server..."
echo ""
echo "📍 Access points:"
echo "   • Login:     http://localhost:8080/login"
echo "   • Dashboard: http://localhost:8080/map"
echo "   • API Docs:  http://localhost:8080/docs"
echo ""
echo "🔐 Default credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start the server
python3 start_server.py
