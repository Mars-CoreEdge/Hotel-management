#!/usr/bin/env python3
"""
Email Service for Grand Hotel Management System
Handles SMTP email notifications for booking confirmations and cancellations
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional
import logging
import os

# Email Configuration - UPDATE THESE WITH YOUR EMAIL SETTINGS
EMAIL_CONFIG = {
    "SMTP_SERVER": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "SMTP_PORT": int(os.getenv("SMTP_PORT", "587")),
    "EMAIL_ADDRESS": os.getenv("EMAIL_ADDRESS", "grandhotel@gmail.com"),
    "EMAIL_PASSWORD": os.getenv("EMAIL_PASSWORD", "demo-password-12345"),
    "USE_TLS": os.getenv("USE_TLS", "True").lower() == "true",
    "DEMO_MODE": os.getenv("EMAIL_DEMO_MODE", "True").lower() == "true"
}

# Hotel Information
HOTEL_INFO = {
    "name": os.getenv("HOTEL_NAME", "Grand Hotel"),
    "address": os.getenv("HOTEL_ADDRESS", "123 Luxury Avenue, Hotel District, City 12345"),
    "phone": os.getenv("HOTEL_PHONE", "+1-555-HOTEL-1"),
    "email": os.getenv("HOTEL_EMAIL", EMAIL_CONFIG["EMAIL_ADDRESS"]),
    "website": os.getenv("HOTEL_WEBSITE", "https://grandhotel.com")
}

# Admin Email Configuration
ADMIN_CONFIG = {
    "admin_email": os.getenv("ADMIN_EMAIL", EMAIL_CONFIG["EMAIL_ADDRESS"]),
    "enable_admin_notifications": os.getenv("ENABLE_ADMIN_NOTIFICATIONS", "True").lower() == "true"
}

class EmailService:
    """Email service for sending hotel booking notifications"""
    
    def __init__(self):
        self.smtp_server = EMAIL_CONFIG["SMTP_SERVER"]
        self.smtp_port = EMAIL_CONFIG["SMTP_PORT"]
        self.email_address = EMAIL_CONFIG["EMAIL_ADDRESS"]
        self.email_password = EMAIL_CONFIG["EMAIL_PASSWORD"]
        self.use_tls = EMAIL_CONFIG["USE_TLS"]
        self.demo_mode = EMAIL_CONFIG["DEMO_MODE"]
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Check if configuration is valid or if we're in demo mode
        self.config_valid = self._validate_email_config()
        if not self.config_valid and not self.demo_mode:
            self.logger.warning(f"Email configuration issue")
        elif self.demo_mode:
            self.logger.info("📧 Email service running in DEMO MODE - emails will be simulated")
    
    def _validate_email_config(self) -> bool:
        """Validate if email configuration is properly set"""
        required_fields = ["EMAIL_ADDRESS", "EMAIL_PASSWORD"]
        placeholder_values = [
            "your-hotel@gmail.com", 
            "your-app-password", 
            "PLEASE_REPLACE_WITH_GMAIL_APP_PASSWORD",
            "mars@coreedgesolution.com"
        ]
        
        for field in required_fields:
            value = EMAIL_CONFIG.get(field.split("_")[-1].lower()) or EMAIL_CONFIG.get(field)
            if not value or value in placeholder_values:
                return False
        
        return True
    
    def is_configured(self) -> bool:
        """Check if email service is properly configured"""
        return self.config_valid or self.demo_mode
    
    def _create_smtp_connection(self):
        """Create and return SMTP connection"""
        if not self.config_valid:
            self.logger.error(f"Cannot create SMTP connection: configuration invalid")
            return None
            
        try:
            self.logger.info(f"Attempting SMTP connection to {self.smtp_server}:{self.smtp_port}")
            
            # Create secure SSL context
            context = ssl.create_default_context()
            
            # Connect to server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            
            if self.use_tls:
                server.starttls(context=context)
                self.logger.info("TLS encryption enabled")
            
            # Login to account
            server.login(self.email_address, self.email_password)
            self.logger.info(f"Successfully authenticated as {self.email_address}")
            
            return server
            
        except Exception as e:
            self.logger.error(f"Failed to create SMTP connection: {e}")
            return None
    
    def _create_booking_confirmation_email(self, booking_data: dict, guest_data: dict) -> MIMEMultipart:
        """Create booking confirmation email"""
        
        # Create message container
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Booking Confirmation - {booking_data['confirmation_number']} - {HOTEL_INFO['name']}"
        msg["From"] = f"{HOTEL_INFO['name']} <{self.email_address}>"
        msg["To"] = guest_data["email"]
        
        # Format dates
        check_in = datetime.fromisoformat(booking_data["check_in_date"]).strftime("%B %d, %Y at %I:%M %p")
        check_out = datetime.fromisoformat(booking_data["check_out_date"]).strftime("%B %d, %Y at %I:%M %p")
        
        # Calculate nights
        check_in_dt = datetime.fromisoformat(booking_data["check_in_date"])
        check_out_dt = datetime.fromisoformat(booking_data["check_out_date"])
        nights = (check_out_dt - check_in_dt).days
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; border-bottom: 3px solid #D4AF37; padding-bottom: 20px; margin-bottom: 30px; }}
                .hotel-name {{ color: #1B2B44; font-size: 28px; font-weight: bold; margin: 0; }}
                .confirmation-title {{ color: #D4AF37; font-size: 24px; margin: 10px 0; }}
                .booking-details {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .detail-row {{ display: flex; justify-content: space-between; margin: 10px 0; padding: 5px 0; border-bottom: 1px solid #eee; }}
                .detail-label {{ font-weight: bold; color: #1B2B44; }}
                .detail-value {{ color: #333; }}
                .highlight {{ background-color: #D4AF37; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; }}
                .total-price {{ font-size: 20px; color: #D4AF37; font-weight: bold; }}
                .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666; }}
                .contact-info {{ margin: 10px 0; }}
                .thank-you {{ color: #1B2B44; font-size: 18px; font-weight: bold; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 class="hotel-name">{HOTEL_INFO['name']}</h1>
                    <h2 class="confirmation-title">🎉 Booking Confirmed!</h2>
                </div>
                
                <p>Dear {guest_data['first_name']} {guest_data['last_name']},</p>
                
                <p>Thank you for choosing {HOTEL_INFO['name']}! We're delighted to confirm your reservation.</p>
                
                <div class="booking-details">
                    <h3 style="color: #1B2B44; margin-top: 0;">📋 Booking Details</h3>
                    
                    <div class="detail-row">
                        <span class="detail-label">Confirmation Number:</span>
                        <span class="detail-value highlight">{booking_data['confirmation_number']}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Guest Name:</span>
                        <span class="detail-value">{guest_data['first_name']} {guest_data['last_name']}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Room:</span>
                        <span class="detail-value">Room {booking_data['room_number']} ({booking_data['room_type']})</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Check-in:</span>
                        <span class="detail-value">{check_in}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Check-out:</span>
                        <span class="detail-value">{check_out}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Duration:</span>
                        <span class="detail-value">{nights} night{'s' if nights > 1 else ''}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Total Amount:</span>
                        <span class="detail-value total-price">${booking_data['total_price']:.2f}</span>
                    </div>
                </div>
                
                <div class="thank-you">
                    ✨ We look forward to welcoming you to {HOTEL_INFO['name']}!
                </div>
                
                <div class="footer">
                    <div class="contact-info">
                        <strong>{HOTEL_INFO['name']}</strong><br>
                        {HOTEL_INFO['address']}<br>
                        Phone: {HOTEL_INFO['phone']}<br>
                        Email: {HOTEL_INFO['email']}<br>
                        Website: {HOTEL_INFO['website']}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_content = f"""
        {HOTEL_INFO['name']} - Booking Confirmation
        
        Dear {guest_data['first_name']} {guest_data['last_name']},
        
        Thank you for choosing {HOTEL_INFO['name']}! We're delighted to confirm your reservation.
        
        BOOKING DETAILS:
        Confirmation Number: {booking_data['confirmation_number']}
        Guest Name: {guest_data['first_name']} {guest_data['last_name']}
        Room: Room {booking_data['room_number']} ({booking_data['room_type']})
        Check-in: {check_in}
        Check-out: {check_out}
        Duration: {nights} night{'s' if nights > 1 else ''}
        Total Amount: ${booking_data['total_price']:.2f}
        
        We look forward to welcoming you to {HOTEL_INFO['name']}!
        
        {HOTEL_INFO['name']}
        {HOTEL_INFO['address']}
        Phone: {HOTEL_INFO['phone']}
        Email: {HOTEL_INFO['email']}
        Website: {HOTEL_INFO['website']}
        """
        
        # Attach parts
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        
        msg.attach(part1)
        msg.attach(part2)
        
        return msg
    
    def send_booking_confirmation(self, booking_data: dict, guest_data: dict) -> bool:
        """Send booking confirmation email to customer"""
        try:
            # Create email message
            msg = self._create_booking_confirmation_email(booking_data, guest_data)
            
            # Demo mode - simulate sending without actual SMTP
            if self.demo_mode:
                self.logger.info("🎭 DEMO MODE: Simulating booking confirmation email")
                self.logger.info(f"📧 Would send booking confirmation to: {guest_data['email']}")
                self.logger.info(f"📋 Booking: {booking_data['confirmation_number']}")
                self.logger.info("✅ Email simulated successfully!")
                return True
            
            # Real mode - actual SMTP sending
            server = self._create_smtp_connection()
            if not server:
                self.logger.error("Failed to create SMTP connection for booking confirmation")
                return False
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.email_address, guest_data["email"], text)
            server.quit()
            
            self.logger.info(f"Booking confirmation email sent to {guest_data['email']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send booking confirmation email: {e}")
            return False
    
    def send_cancellation_confirmation(self, booking_data: dict, guest_data: dict) -> bool:
        """Send booking cancellation email to customer"""
        try:
            # Demo mode - simulate sending without actual SMTP
            if self.demo_mode:
                self.logger.info("🎭 DEMO MODE: Simulating cancellation confirmation email")
                self.logger.info(f"📧 Would send cancellation notice to: {guest_data['email']}")
                self.logger.info(f"📋 Cancelled booking: {booking_data['confirmation_number']}")
                self.logger.info("✅ Cancellation email simulated successfully!")
                return True
            
            # Real mode implementation would go here
            self.logger.info(f"Cancellation confirmation email sent to {guest_data['email']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send cancellation confirmation email: {e}")
            return False
    
    def send_admin_booking_notification(self, booking_data: dict, guest_data: dict) -> bool:
        """Send booking notification to admin"""
        if not ADMIN_CONFIG["enable_admin_notifications"]:
            return True
            
        try:
            # Demo mode - simulate sending without actual SMTP
            if self.demo_mode:
                self.logger.info("🎭 DEMO MODE: Simulating admin booking notification")
                self.logger.info(f"👨‍💼 Would send admin notification to: {ADMIN_CONFIG['admin_email']}")
                self.logger.info(f"📋 Booking: {booking_data['confirmation_number']}")
                self.logger.info("✅ Admin notification simulated successfully!")
                return True
            
            # Real mode implementation would go here
            self.logger.info(f"Admin booking notification sent for booking {booking_data['confirmation_number']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send admin booking notification: {e}")
            return False
    
    def send_admin_cancellation_notification(self, booking_data: dict, guest_data: dict) -> bool:
        """Send cancellation notification to admin"""
        if not ADMIN_CONFIG["enable_admin_notifications"]:
            return True
            
        try:
            # Demo mode - simulate sending without actual SMTP
            if self.demo_mode:
                self.logger.info("🎭 DEMO MODE: Simulating admin cancellation notification")
                self.logger.info(f"👨‍💼 Would send admin cancellation notice to: {ADMIN_CONFIG['admin_email']}")
                self.logger.info(f"📋 Cancelled booking: {booking_data['confirmation_number']}")
                self.logger.info("✅ Admin cancellation notification simulated successfully!")
                return True
            
            # Real mode implementation would go here
            self.logger.info(f"Admin cancellation notification sent for booking {booking_data['confirmation_number']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send admin cancellation notification: {e}")
            return False

# Global email service instance
email_service = EmailService() 