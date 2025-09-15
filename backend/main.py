#!/usr/bin/env python3
"""
Main entry point for Grand Hotel Management System
"""

from app.main import app
from app.config.settings import settings

if __name__ == "__main__":
    import uvicorn
    
    print(f"🏨 Starting {settings.APP_NAME}")
    print(f"📊 Version: {settings.APP_VERSION}")
    print(f"🌐 Server: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    ) 