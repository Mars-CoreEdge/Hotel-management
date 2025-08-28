from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import room_routes, guest_routes, booking_routes, customer_routes, ai_routes, auth_routes
from .database.database import Database
from .models.database_models import Base
from .config.settings import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = Database()
Base.metadata.create_all(bind=db.engine)

# Include routers
app.include_router(auth_routes.router)
app.include_router(room_routes.router)
app.include_router(guest_routes.router)
app.include_router(booking_routes.router)
app.include_router(customer_routes.router)
app.include_router(ai_routes.router)

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "endpoints": {
            "auth": "/auth",
            "rooms": "/rooms",
            "guests": "/guests",
            "bookings": "/bookings",
            "customer": "/customer",
            "ai": "/ai",
            "documentation": "/docs"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint for Docker and monitoring"""
    try:
        # Test database connection
        db.get_all_rooms()
        return {
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "database": "disconnected",
            "error": str(e)
        }

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.HOST, 
        port=settings.PORT,
        reload=settings.RELOAD
    ) 