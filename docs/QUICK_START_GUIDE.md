# 🚀 Quick Start Guide - Hotel Email System

## Overview
This guide will help you set up and run your hotel management system with email notifications for both customers and admins.

---

## 📧 Step 1: Configure Email Settings

### **1.1 Update Email Service Configuration**
Edit `email_service.py` and update these sections:

**Email Server Settings:**
```python
EMAIL_CONFIG = {
    "SMTP_SERVER": "smtp.gmail.com",                    # Change to your email provider
    "SMTP_PORT": 587,                                   # Usually 587 for TLS
    "EMAIL_ADDRESS": "grandhotel@yourdomain.com",       # ⚠️ CHANGE THIS!
    "EMAIL_PASSWORD": "your-app-password-here",         # ⚠️ CHANGE THIS!
    "USE_TLS": True
}
```

**Hotel Information:**
```python
HOTEL_INFO = {
    "name": "Grand Hotel",                              # Your hotel name
    "address": "123 Luxury Avenue, Hotel District",     # Your address
    "phone": "+1-555-HOTEL-1",                         # Your phone
    "email": "info@grandhotel.com",                    # Your contact email
    "website": "https://grandhotel.com"               # Your website
}
```

**Admin Notifications:**
```python
ADMIN_CONFIG = {
    "admin_email": "admin@grandhotel.com",             # ⚠️ CHANGE THIS!
    "enable_admin_notifications": True                 # Keep as True
}
```

### **1.2 Gmail Setup (Recommended for Testing)**
If using Gmail:
1. **Enable 2-Factor Authentication** on your Google account
2. **Create App Password**:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate new app password for "Mail"
   - Use this 16-character password in EMAIL_CONFIG

### **1.3 Other Email Providers**
**Outlook/Hotmail:**
```python
EMAIL_CONFIG = {
    "SMTP_SERVER": "smtp-mail.outlook.com",
    "SMTP_PORT": 587,
    "EMAIL_ADDRESS": "hotel@outlook.com",
    "EMAIL_PASSWORD": "your-password",
    "USE_TLS": True
}
```

---

## 🧪 Step 2: Test Email Configuration

### **2.1 Run Email Test**
```bash
python test_email.py
```

### **2.2 What the Test Does**
- Checks your email configuration
- Sends test emails to verify setup
- Tests both customer and admin email templates

### **2.3 Expected Output**
```
📧 GRAND HOTEL EMAIL CONFIGURATION TEST
============================================================
✅ Email service imported successfully
📋 Current Email Configuration:
   SMTP Server: smtp.gmail.com
   Email Address: hotel@yourdomain.com
   ...
📤 Will send test emails to: your-test@email.com
✅ Booking confirmation email sent successfully!
✅ Cancellation confirmation email test passed!
🎉 EMAIL CONFIGURATION TEST PASSED!
```

---

## 🖥️ Step 3: Start the Backend Server

### **3.1 Check for Running Processes**
If you see "port already in use" error, kill existing process:

**Windows:**
```bash
netstat -ano | findstr :8001
taskkill /PID [PID_NUMBER] /F
```

### **3.2 Start the Server**
```bash
python main.py
```

### **3.3 Expected Output**
```
✅ Email service loaded successfully
🏨 Initializing Hotel Management Database...
✅ Database tables created successfully!
INFO:     Started server process [XXXX]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

---

## 🌐 Step 4: Start the Frontend

### **4.1 Navigate to Frontend Directory**
```bash
cd fruit-store-ui
```

### **4.2 Start React App**
**Windows PowerShell (use separate commands):**
```bash
cd fruit-store-ui
npm start
```

### **4.3 Handle Port Conflicts**
If prompted "Something is already running on port 3000":
- Type `Y` to run on different port (usually 3001)
- Or kill the existing process

---

## 🎯 Step 5: Test the Complete Email Flow

### **5.1 Test Customer Booking Email**
1. Open frontend: `http://localhost:3000` (or 3001)
2. Click "Book Now"
3. Select dates and room
4. Fill booking form with **real email address**
5. Submit booking
6. Check your email for confirmation

### **5.2 Test Admin Notification**
1. Admin should receive notification at configured `admin_email`
2. Check admin inbox for booking alert

### **5.3 Test Cancellation Emails**
1. Go to "Manage Bookings"
2. Enter email used for booking
3. Cancel the booking
4. Check both customer and admin emails

---

## 📊 Step 6: Monitor Email Status

### **6.1 Server Logs**
Watch your server console for email status:
```
✅ Customer confirmation email sent to guest@email.com
✅ Admin notification email sent for booking BK000123
✅ Customer cancellation email sent to guest@email.com
✅ Admin cancellation notification sent for booking BK000123
```

### **6.2 API Response**
API will include email status:
```json
{
  "message": "Booking created successfully!",
  "confirmation_number": "BK000123",
  "email_sent": true
}
```

---

## 🔧 Troubleshooting

### **Common Issues:**

#### **"Email service not available"**
- ✅ Update `EMAIL_CONFIG` in `email_service.py`
- ✅ Install dependencies: `pip install email-validator jinja2`

#### **"Authentication failed"**
- ✅ Use App Password for Gmail (not regular password)
- ✅ Check email address and password are correct
- ✅ Verify SMTP server settings

#### **"Connection refused"**
- ✅ Check internet connection
- ✅ Verify SMTP server and port
- ✅ Check firewall settings

#### **"Port already in use"**
- ✅ Kill existing process on port 8001 or 3000
- ✅ Use different ports if needed

#### **Emails not received**
- ✅ Check spam/junk folder
- ✅ Verify email addresses are correct
- ✅ Check server logs for error messages

---

## 🎉 Success Checklist

When everything is working, you should have:

- ✅ **Backend running** on `http://localhost:8001`
- ✅ **Frontend running** on `http://localhost:3000`
- ✅ **Customer booking emails** sent automatically
- ✅ **Admin notification emails** for new bookings
- ✅ **Customer cancellation emails** sent automatically
- ✅ **Admin cancellation notifications** sent
- ✅ **Professional email templates** with hotel branding
- ✅ **Mobile-responsive emails** that work on all devices

---

## 📧 Email Features Summary

### **Customer Receives:**
- 🎉 Beautiful booking confirmation with all details
- ❌ Professional cancellation confirmation
- 📱 Mobile-friendly HTML emails
- 🏨 Complete hotel contact information

### **Admin Receives:**
- 🏨 New booking alerts with guest details
- ❌ Cancellation notifications with revenue impact
- 🔔 Action items and reminders
- 📊 Complete booking information

---

## 🆘 Need Help?

If you encounter issues:

1. **Check the logs** in your terminal
2. **Verify email configuration** in `email_service.py`
3. **Test email separately** with `python test_email.py`
4. **Check spam folders** for test emails
5. **Verify internet connection** and firewall settings

---

## 🚀 You're Ready!

Once everything is set up:
- **Customers get instant email confirmations**
- **Admins get real-time booking notifications**
- **Professional communication enhances your hotel's image**
- **Reduced customer service inquiries**

**Your hotel now provides world-class email communication!** 🏨✨📧 