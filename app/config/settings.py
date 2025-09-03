import os
from typing import List

class Settings:
    """Application settings and configuration"""
    
    # Application Info
    APP_NAME: str = "Grand Hotel Management System"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API for managing hotel rooms, guests, and bookings"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8001"))
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///hotel.db")
    
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    
    # JWT Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ]
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "500"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    # Email Configuration
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS", "grandhotel@gmail.com")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "demo-password-12345")
    USE_TLS: bool = os.getenv("USE_TLS", "True").lower() == "true"
    EMAIL_DEMO_MODE: bool = os.getenv("EMAIL_DEMO_MODE", "True").lower() == "true"
    
    # Hotel Information
    HOTEL_NAME: str = os.getenv("HOTEL_NAME", "Grand Hotel")
    HOTEL_ADDRESS: str = os.getenv("HOTEL_ADDRESS", "123 Luxury Avenue, Hotel District, City 12345")
    HOTEL_PHONE: str = os.getenv("HOTEL_PHONE", "+1-555-HOTEL-1")
    HOTEL_EMAIL: str = os.getenv("EMAIL_ADDRESS", EMAIL_ADDRESS)
    HOTEL_WEBSITE: str = os.getenv("HOTEL_WEBSITE", "https://grandhotel.com")
    
    # Admin Configuration
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", EMAIL_ADDRESS)
    ENABLE_ADMIN_NOTIFICATIONS: bool = os.getenv("ENABLE_ADMIN_NOTIFICATIONS", "True").lower() == "true"
    
    # Development/Debug Settings
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    RELOAD: bool = os.getenv("RELOAD", "False").lower() == "true"
    
    class Config:
        case_sensitive = True

# Create global settings instance
settings = Settings() 