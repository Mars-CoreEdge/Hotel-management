from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

# Create base class for all models
Base = declarative_base()

class UserProfile(Base):
    """SQLAlchemy model for user profiles"""
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True, nullable=False)  # Supabase user ID
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    country = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Room(Base):
    """SQLAlchemy model for rooms"""
    __tablename__ = 'rooms'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_number = Column(String, unique=True, nullable=False)
    room_type = Column(String, nullable=False)  # Single, Double, Suite, etc.
    price_per_night = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    
    # Relationship to bookings
    bookings = relationship("Booking", back_populates="room")

class Guest(Base):
    """SQLAlchemy model for guests"""
    __tablename__ = 'guests'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to bookings
    bookings = relationship("Booking", back_populates="guest")

class Booking(Base):
    """SQLAlchemy model for bookings"""
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    guest_id = Column(Integer, ForeignKey('guests.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, default="confirmed", nullable=False)  # confirmed, cancelled, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    guest = relationship("Guest", back_populates="bookings")
    room = relationship("Room", back_populates="bookings") 