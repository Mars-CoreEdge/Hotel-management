#!/usr/bin/env python3
"""
AI Reception Service for Grand Hotel Management System
Provides intelligent chat assistance for hotel bookings and information
"""

from dotenv import load_dotenv
import os

# Load environment variables at module level
load_dotenv()

from openai import OpenAI
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from ..database.database import Database
from ..services.booking_service import BookingService
from ..services.guest_service import GuestService

# Hotel Information for AI Context
HOTEL_CONTEXT = {
    "name": "Grand Hotel",
    "description": "A luxury hotel offering exceptional service and comfortable accommodations",
    "amenities": [
        "Free WiFi", "Swimming Pool", "Fitness Center", "Restaurant", 
        "Room Service", "Concierge", "Valet Parking", "Business Center"
    ],
    "room_types": {
        "Single": {
            "description": "Perfect for solo travelers with comfortable single bed",
            "capacity": "1 Guest",
            "features": ["Free WiFi", "Air Conditioning", "Private Bathroom", "TV"]
        },
        "Double": {
            "description": "Ideal for couples with queen-size bed and city view",
            "capacity": "2 Guests", 
            "features": ["Free WiFi", "Air Conditioning", "Private Bathroom", "TV", "Mini Fridge"]
        },
        "Suite": {
            "description": "Luxury suite with separate living area for extended stays",
            "capacity": "2-3 Guests",
            "features": ["Free WiFi", "Air Conditioning", "Private Bathroom", "TV", "Mini Fridge", "Seating Area"]
        },
        "Deluxe": {
            "description": "Premium room with enhanced comfort and elegant furnishings",
            "capacity": "2-3 Guests",
            "features": ["Free WiFi", "Air Conditioning", "Private Bathroom", "TV", "Mini Fridge", "Balcony"]
        },
        "Presidential": {
            "description": "Ultimate luxury experience with premium amenities",
            "capacity": "4 Guests",
            "features": ["Free WiFi", "Air Conditioning", "Private Bathroom", "TV", "Mini Fridge", "Balcony", "Room Service", "Jacuzzi"]
        }
    },
    "policies": {
        "check_in": "3:00 PM",
        "check_out": "11:00 AM",
        "cancellation": "Free cancellation up to 24 hours before check-in",
        "payment": "Payment required at booking confirmation",
        "pets": "Pet-friendly rooms available upon request",
        "smoking": "Non-smoking hotel with designated outdoor areas"
    }
}

class AIService:
    """AI-powered reception service for hotel management"""
    
    def __init__(self):
        self.openai_client = None
        self.db = Database()
        self.booking_service = BookingService()
        self.guest_service = GuestService()
        self.initialize_openai()
    
    def get_openai_config(self):
        """Get OpenAI configuration dynamically from environment variables"""
        return {
            "api_key": os.getenv("OPENAI_API_KEY", "your-openai-api-key-here"),
            "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            "max_tokens": int(os.getenv("OPENAI_MAX_TOKENS", "500")),
            "temperature": float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        }
    
    def initialize_openai(self):
        """Initialize OpenAI client"""
        try:
            config = self.get_openai_config()
            if config["api_key"] and config["api_key"] != "your-openai-api-key-here":
                self.openai_client = OpenAI(api_key=config["api_key"])
                print("✅ OpenAI client initialized successfully")
            else:
                print("⚠️  OpenAI API key not configured")
                self.openai_client = None
        except Exception as e:
            print(f"❌ Failed to initialize OpenAI: {e}")
            self.openai_client = None
    
    def get_hotel_data(self) -> Dict:
        """Get current hotel data for AI context"""
        try:
            rooms = self.db.get_all_rooms()
            available_rooms = self.db.get_available_rooms()
            bookings = self.db.get_all_bookings()
            
            # Calculate occupancy
            total_rooms = len(rooms)
            occupied_rooms = total_rooms - len(available_rooms)
            occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
            
            return {
                "total_rooms": total_rooms,
                "available_rooms": len(available_rooms),
                "occupied_rooms": occupied_rooms,
                "occupancy_rate": round(occupancy_rate, 1),
                "room_details": available_rooms,
                "recent_bookings": len(bookings)
            }
        except Exception as e:
            print(f"Error getting hotel data: {e}")
            return {"error": "Unable to fetch hotel data"}
    
    def create_system_prompt(self) -> str:
        """Create system prompt with hotel context"""
        hotel_data = self.get_hotel_data()
        
        system_prompt = f"""
        You are the AI Reception Assistant for {HOTEL_CONTEXT['name']}, a luxury hotel management system.
        
        HOTEL INFORMATION:
        - Name: {HOTEL_CONTEXT['name']}
        - Description: {HOTEL_CONTEXT['description']}
        - Total Rooms: {hotel_data.get('total_rooms', 'N/A')}
        - Available Rooms: {hotel_data.get('available_rooms', 'N/A')}
        - Current Occupancy: {hotel_data.get('occupancy_rate', 'N/A')}%
        
        ROOM TYPES & PRICING:
        """
        
        # Add room type information
        for room_type, details in HOTEL_CONTEXT['room_types'].items():
            system_prompt += f"\n- {room_type}: {details['description']} (Capacity: {details['capacity']})"
        
        system_prompt += f"""
        
        HOTEL AMENITIES:
        {', '.join(HOTEL_CONTEXT['amenities'])}
        
        POLICIES:
        - Check-in: {HOTEL_CONTEXT['policies']['check_in']}
        - Check-out: {HOTEL_CONTEXT['policies']['check_out']}
        - Cancellation: {HOTEL_CONTEXT['policies']['cancellation']}
        - Payment: {HOTEL_CONTEXT['policies']['payment']}
        
        CAPABILITIES:
        You can help guests with:
        1. Room availability and information
        2. Booking assistance and guidance
        3. Hotel amenities and services
        4. Check-in/check-out procedures
        5. Local recommendations
        6. Hotel policies and procedures
        7. Booking modifications and cancellations
        
        IMPORTANT GUIDELINES:
        - Always be professional, friendly, and helpful
        - Provide accurate information about rooms and policies
        - If you cannot help with something, politely direct them to human staff
        - Use the guest's name if they provide it
        - Suggest appropriate room types based on their needs
        - Mention current availability when relevant
        
        Current real-time hotel status: {hotel_data.get('available_rooms', 0)} rooms available out of {hotel_data.get('total_rooms', 0)} total rooms.
        
        BOOKING CAPABILITIES:
        You can now DIRECTLY BOOK and CANCEL rooms for guests! Here's how:
        
        BOOKING PROCESS:
        1. When a guest wants to book, collect these details:
           - Guest name (first and last)
           - Email address (ANY email address - new guests will be created automatically)
           - Phone number
           - Check-in date (YYYY-MM-DD format)
           - Check-out date (YYYY-MM-DD format)
           - Room type preference (Single, Double, Suite, Deluxe, Presidential)
        
        2. Use this EXACT format to trigger booking:
        "BOOK_ROOM: {{guest_name: 'John Doe', email: 'john@email.com', phone: '+1234567890', check_in: '2024-01-15', check_out: '2024-01-17', room_type: 'Double'}}"
        
        IMPORTANT: You can book for ANY email address - the system will automatically:
        - Create new guest profiles for new emails
        - Use existing profiles for returning guests
        - Handle all guest management seamlessly
        
        CANCELLATION PROCESS:
        1. For cancellations, ask for:
           - Booking ID (if they have it) OR
           - Guest email address
        
        2. Use this EXACT format to trigger cancellation:
        "CANCEL_BOOKING: {{booking_id: '123'}}" OR "CANCEL_BOOKING: {{email: 'john@email.com'}}"
        
        IMPORTANT INSTRUCTIONS:
        - When a guest provides ALL required booking information in one message, IMMEDIATELY process the booking using the BOOK_ROOM format
        - If ANY information is missing, ask for it politely before booking
        - ALWAYS execute bookings automatically when you have: guest name, email, phone, check-in date, check-out date, and room type
        - DO NOT ask for confirmation - just book immediately when all data is provided
        - Provide clear booking confirmations with booking ID after successful booking
        - For cancellations, confirm the cancellation policy (free cancellation up to 24 hours)
        - Be friendly and helpful throughout the process
        """
        
        return system_prompt
    
    def get_room_recommendations(self, guest_requirements: str) -> List[Dict]:
        """Get room recommendations based on guest requirements"""
        try:
            available_rooms = self.db.get_available_rooms()
            
            # Simple recommendation logic (can be enhanced with AI)
            recommendations = []
            guest_req_lower = guest_requirements.lower()
            
            for room in available_rooms:
                room_type = room['room_type']
                room_info = HOTEL_CONTEXT['room_types'].get(room_type, {})
                
                # Basic matching logic
                score = 0
                if 'single' in guest_req_lower and room_type == 'Single':
                    score += 10
                elif 'double' in guest_req_lower and room_type == 'Double':
                    score += 10
                elif 'suite' in guest_req_lower and room_type == 'Suite':
                    score += 10
                elif 'luxury' in guest_req_lower and room_type in ['Suite', 'Presidential']:
                    score += 8
                elif 'budget' in guest_req_lower and room_type in ['Single', 'Double']:
                    score += 8
                
                if score > 0:
                    recommendations.append({
                        **room,
                        "description": room_info.get('description', ''),
                        "features": room_info.get('features', []),
                        "capacity": room_info.get('capacity', ''),
                        "score": score
                    })
            
            # Sort by score and return top recommendations
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            return recommendations[:3]  # Top 3 recommendations
            
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []
    
    def parse_booking_request(self, ai_response: str) -> Dict:
        """Parse booking request from AI response"""
        # More flexible pattern to handle line breaks and quoted strings
        booking_pattern = r"BOOK_ROOM:\s*\{([^}]+)\}"
        match = re.search(booking_pattern, ai_response, re.DOTALL | re.MULTILINE)
        
        if match:
            try:
                # Extract the booking data
                booking_data_str = "{" + match.group(1) + "}"
                # Clean up the string and make it proper JSON
                booking_data_str = booking_data_str.replace("'", '"')
                # Remove line breaks and extra whitespace
                booking_data_str = re.sub(r'\s+', ' ', booking_data_str)
                # Remove any trailing commas before closing brace
                booking_data_str = re.sub(r',\s*}', '}', booking_data_str)
                
                print(f"Parsing booking data: {booking_data_str}")
                booking_data = json.loads(booking_data_str)
                return {"found": True, "data": booking_data}
            except Exception as e:
                print(f"Error parsing booking request: {e}")
                print(f"Original response excerpt: {ai_response[max(0, ai_response.find('BOOK_ROOM')-50):ai_response.find('BOOK_ROOM')+200]}")
                print(f"Extracted data: {booking_data_str}")
                
                # Try a more aggressive cleanup
                try:
                    # Extract just the content between the braces more carefully
                    content = match.group(1)
                    # Split by commas and clean each part
                    pairs = []
                    for part in content.split(','):
                        part = part.strip()
                        if ':' in part:
                            key, value = part.split(':', 1)
                            key = key.strip().strip("'\"")
                            value = value.strip().strip("'\"")
                            pairs.append(f'"{key}": "{value}"')
                    
                    booking_data_str = "{" + ", ".join(pairs) + "}"
                    print(f"Retry parsing: {booking_data_str}")
                    booking_data = json.loads(booking_data_str)
                    return {"found": True, "data": booking_data}
                except Exception as e2:
                    print(f"Second attempt failed: {e2}")
                    return {"found": False, "error": "Invalid booking format"}
        
        return {"found": False}
    
    def parse_cancellation_request(self, ai_response: str) -> Dict:
        """Parse cancellation request from AI response"""
        cancel_pattern = r"CANCEL_BOOKING:\s*\{([^}]+)\}"
        match = re.search(cancel_pattern, ai_response, re.DOTALL | re.MULTILINE)
        
        if match:
            try:
                # Extract the cancellation data
                cancel_data_str = "{" + match.group(1) + "}"
                # Clean up the string and make it proper JSON
                cancel_data_str = cancel_data_str.replace("'", '"')
                # Remove line breaks and extra whitespace
                cancel_data_str = re.sub(r'\s+', ' ', cancel_data_str)
                # Remove any trailing commas before closing brace
                cancel_data_str = re.sub(r',\s*}', '}', cancel_data_str)
                
                print(f"Parsing cancellation data: {cancel_data_str}")
                cancel_data = json.loads(cancel_data_str)
                return {"found": True, "data": cancel_data}
            except Exception as e:
                print(f"Error parsing cancellation request: {e}")
                return {"found": False, "error": "Invalid cancellation format"}
        
        return {"found": False}
    
    def process_ai_booking(self, booking_data: Dict) -> Dict:
        """Process AI-initiated booking"""
        try:
            # Validate required fields
            required_fields = ['guest_name', 'email', 'phone', 'check_in', 'check_out', 'room_type']
            for field in required_fields:
                if field not in booking_data:
                    return {"success": False, "error": f"Missing required field: {field}"}
            
            # Validate dates
            check_in_date = datetime.strptime(booking_data['check_in'], '%Y-%m-%d').date()
            check_out_date = datetime.strptime(booking_data['check_out'], '%Y-%m-%d').date()
            
            if check_in_date >= check_out_date:
                return {"success": False, "error": "Check-out date must be after check-in date"}
            
            if check_in_date < datetime.now().date():
                return {"success": False, "error": "Check-in date cannot be in the past"}
            
            # Get available rooms for the date range
            availability = self.booking_service.check_room_availability(
                booking_data['check_in'], 
                booking_data['check_out']
            )
            
            # Find a room of the requested type
            available_rooms = self.db.get_available_rooms()
            suitable_room = None
            for room in available_rooms:
                if (room['room_type'].lower() == booking_data['room_type'].lower() and 
                    room['id'] in availability['available_rooms']):
                    suitable_room = room
                    break
            
            if not suitable_room:
                return {
                    "success": False, 
                    "error": f"No {booking_data['room_type']} rooms available for the selected dates"
                }
            
            # Calculate total price
            nights = (check_out_date - check_in_date).days
            total_price = suitable_room['price_per_night'] * nights
            
            # Parse guest name
            name_parts = booking_data['guest_name'].split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            # Create customer booking using the booking service
            from ..models.booking import CustomerBookingCreate
            customer_booking = CustomerBookingCreate(
                room_id=suitable_room['id'],
                first_name=first_name,
                last_name=last_name,
                email=booking_data['email'],
                phone=booking_data['phone'],
                check_in_date=booking_data['check_in'],
                check_out_date=booking_data['check_out'],
                total_price=total_price
            )
            
            new_booking = self.booking_service.create_customer_booking(customer_booking)
            
            return {
                "success": True,
                "booking_id": new_booking['id'],
                "room_number": new_booking['room_number'],
                "room_type": new_booking['room_type'],
                "total_price": total_price,
                "nights": nights,
                "guest_name": booking_data['guest_name'],
                "guest_email": booking_data['email'],
                "confirmation_number": new_booking['confirmation_number']
            }
            
        except Exception as e:
            print(f"Error processing AI booking: {e}")
            return {"success": False, "error": f"Booking failed: {str(e)}"}
    
    def process_ai_cancellation(self, cancel_data: Dict) -> Dict:
        """Process AI-initiated cancellation"""
        try:
            if 'booking_id' in cancel_data:
                booking_id = int(cancel_data['booking_id'])
                cancelled_booking = self.booking_service.cancel_booking(booking_id)
                
                if cancelled_booking:
                    return {
                        "success": True,
                        "booking_id": cancelled_booking['id'],
                        "room_number": cancelled_booking.get('room_number', 'N/A'),
                        "guest_name": cancelled_booking.get('guest_name', 'N/A')
                    }
                else:
                    return {"success": False, "error": "Booking not found"}
                    
            elif 'email' in cancel_data:
                email = cancel_data['email'].lower()
                bookings = self.booking_service.get_bookings_by_email(email)
                
                if not bookings:
                    return {"success": False, "error": "No bookings found for this email address"}
                
                # Cancel the most recent booking
                latest_booking = bookings[-1]
                cancelled_booking = self.booking_service.cancel_booking(latest_booking['id'])
                
                if cancelled_booking:
                    return {
                        "success": True,
                        "booking_id": cancelled_booking['id'],
                        "room_number": cancelled_booking.get('room_number', 'N/A'),
                        "guest_name": cancelled_booking.get('guest_name', 'N/A')
                    }
                else:
                    return {"success": False, "error": "Failed to cancel booking"}
            else:
                return {"success": False, "error": "Please provide either booking ID or email address"}
                
        except Exception as e:
            print(f"Error processing AI cancellation: {e}")
            return {"success": False, "error": f"Cancellation failed: {str(e)}"}

    def chat_with_ai(self, user_message: str, conversation_history: List[Dict] = None) -> Dict:
        """Chat with AI reception assistant"""
        
        if not self.openai_client:
            return {
                "response": "I'm sorry, but the AI reception service is currently unavailable. Please contact our human staff for assistance.",
                "success": False,
                "error": "OpenAI not configured"
            }
        
        try:
            # Prepare conversation history
            if conversation_history is None:
                conversation_history = []
            
            # Create messages for OpenAI
            messages = [
                {"role": "system", "content": self.create_system_prompt()}
            ]
            
            # Add conversation history
            for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                messages.append(msg)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Get AI response
            response = self.openai_client.chat.completions.create(
                model=self.get_openai_config()["model"],
                messages=messages,
                max_tokens=self.get_openai_config()["max_tokens"],
                temperature=self.get_openai_config()["temperature"]
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Check for booking requests in AI response
            booking_request = self.parse_booking_request(ai_response)
            if booking_request["found"]:
                booking_result = self.process_ai_booking(booking_request["data"])
                
                if booking_result["success"]:
                    # Remove the booking command from response and add confirmation
                    ai_response = re.sub(r"BOOK_ROOM:\s*\{[^}]+\}", "", ai_response).strip()
                    ai_response += f"\n\n🎉 **BOOKING CONFIRMED!** 🎉\n"
                    ai_response += f"✅ Booking ID: #{booking_result['booking_id']}\n"
                    ai_response += f"🏨 Room: {booking_result['room_number']} ({booking_result['room_type']})\n"
                    ai_response += f"👤 Guest: {booking_result['guest_name']}\n"
                    ai_response += f"📧 Email: {booking_result['guest_email']}\n"
                    ai_response += f"💰 Total Price: ₹{booking_result['total_price']} for {booking_result['nights']} nights\n"
                    ai_response += f"🎫 Confirmation Number: {booking_result['confirmation_number']}\n"
                    ai_response += f"📧 Confirmation details will be sent to your email.\n"
                    ai_response += f"🌟 Thank you for choosing Grand Hotel!\n\n"
                    ai_response += f"📋 **To View Your Booking:**\n"
                    ai_response += f"• Click 'Management Dashboard' → 'Booking Management' to see all bookings\n"
                    ai_response += f"• Your booking will appear in the system within 30 seconds\n"
                    ai_response += f"• Save your Booking ID #{booking_result['booking_id']} for future reference\n"
                    ai_response += f"• Use your email ({booking_result['guest_email']}) to manage bookings"
                else:
                    # Remove the booking command and add error message
                    ai_response = re.sub(r"BOOK_ROOM:\s*\{[^}]+\}", "", ai_response).strip()
                    ai_response += f"\n\n❌ **Booking Failed:** {booking_result['error']}\n"
                    ai_response += "Please provide the correct information and I'll try again."
            
            # Check for cancellation requests in AI response
            cancel_request = self.parse_cancellation_request(ai_response)
            if cancel_request["found"]:
                cancel_result = self.process_ai_cancellation(cancel_request["data"])
                
                if cancel_result["success"]:
                    # Remove the cancellation command from response and add confirmation
                    ai_response = re.sub(r"CANCEL_BOOKING:\s*\{[^}]+\}", "", ai_response).strip()
                    ai_response += f"\n\n✅ **BOOKING CANCELLED!** ✅\n"
                    ai_response += f"🆔 Booking ID: #{cancel_result['booking_id']}\n"
                    ai_response += f"🏨 Room: {cancel_result['room_number']}\n"
                    ai_response += f"👤 Guest: {cancel_result['guest_name']}\n"
                    ai_response += f"📧 Cancellation confirmation will be sent to your email.\n"
                    ai_response += f"💙 We hope to serve you again in the future!"
                else:
                    # Remove the cancellation command and add error message
                    ai_response = re.sub(r"CANCEL_BOOKING:\s*\{[^}]+\}", "", ai_response).strip()
                    ai_response += f"\n\n❌ **Cancellation Failed:** {cancel_result['error']}\n"
                    ai_response += "Please check your booking details and try again."
            
            # Check if user is asking for room recommendations
            if any(keyword in user_message.lower() for keyword in ['recommend', 'suggest', 'room', 'availability']):
                recommendations = self.get_room_recommendations(user_message)
                
                if recommendations:
                    ai_response += "\n\n🏨 Based on your requirements, here are my top room recommendations:\n"
                    for i, room in enumerate(recommendations, 1):
                        ai_response += f"\n{i}. Room {room['room_number']} - {room['room_type']}"
                        ai_response += f"\n   • Price: ₹{room['price_per_night']}/night"
                        ai_response += f"\n   • {room['description']}"
                        ai_response += f"\n   • Capacity: {room['capacity']}"
            
            return {
                "response": ai_response,
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "model_used": self.get_openai_config()["model"],
                "booking_processed": booking_request.get("found", False),
                "cancellation_processed": cancel_request.get("found", False)
            }
            
        except Exception as e:
            print(f"Error in AI chat: {e}")
            return {
                "response": "I apologize, but I'm experiencing technical difficulties. Please try again or contact our human staff for immediate assistance.",
                "success": False,
                "error": str(e)
            }
    
    def get_booking_info(self, email: str) -> Dict:
        """Get booking information for a guest"""
        try:
            bookings = self.booking_service.get_bookings_by_email(email)
            
            if bookings:
                return {
                    "found": True,
                    "bookings": bookings,
                    "count": len(bookings)
                }
            else:
                return {
                    "found": False,
                    "message": "No bookings found for this email address"
                }
        except Exception as e:
            return {
                "found": False,
                "error": str(e)
            }

# Global AI reception service instance
ai_reception_service = AIService() 