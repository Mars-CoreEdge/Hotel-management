# 📧 Email Setup Guide for Grand Hotel Management System

## Overview
This guide will help you set up email notifications for customer bookings and cancellations. When customers book or cancel reservations, they will automatically receive professional email confirmations.

## ✨ Email Features

### **Booking Confirmation Emails**
- ✅ Professional HTML email templates with hotel branding
- 📋 Complete booking details with confirmation number
- 🏨 Hotel contact information and policies
- 📱 Mobile-responsive design
- 🎨 Luxury hotel aesthetic with gold/navy color scheme

### **Cancellation Confirmation Emails**
- ❌ Booking cancellation confirmation
- 💰 Refund policy information
- 📞 Contact details for further assistance
- 🔄 Professional cancellation notification

---

## 🚀 Quick Setup

### **Step 1: Update Email Configuration**

Edit the `email_service.py` file and update the `EMAIL_CONFIG` section:

```python
EMAIL_CONFIG = {
    "SMTP_SERVER": "your-smtp-server.com",    # Your SMTP server
    "SMTP_PORT": 587,                         # Usually 587 for TLS
    "EMAIL_ADDRESS": "hotel@yourdomain.com",  # Your hotel email
    "EMAIL_PASSWORD": "your-app-password",    # Your email password/app password
    "USE_TLS": True                          # Use TLS encryption
}
```

### **Step 2: Update Hotel Information**

Update the `HOTEL_INFO` section in `email_service.py`:

```python
HOTEL_INFO = {
    "name": "Your Hotel Name",
    "address": "123 Your Hotel Address, City, State 12345",
    "phone": "+1-555-YOUR-PHONE",
    "email": "info@yourhotel.com",
    "website": "https://yourhotel.com"
}
```

---

## 📧 Email Provider Setup

### **Option 1: Gmail (Recommended for Testing)**

1. **Enable 2-Factor Authentication** on your Google account
2. **Create an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use this password in the configuration

**Gmail Configuration:**
```python
EMAIL_CONFIG = {
    "SMTP_SERVER": "smtp.gmail.com",
    "SMTP_PORT": 587,
    "EMAIL_ADDRESS": "yourhotel@gmail.com",
    "EMAIL_PASSWORD": "your-16-char-app-password",
    "USE_TLS": True
}
```

### **Option 2: Outlook/Hotmail**

**Outlook Configuration:**
```python
EMAIL_CONFIG = {
    "SMTP_SERVER": "smtp-mail.outlook.com",
    "SMTP_PORT": 587,
    "EMAIL_ADDRESS": "yourhotel@outlook.com",
    "EMAIL_PASSWORD": "your-password",
    "USE_TLS": True
}
```

### **Option 3: Custom SMTP Server**

If you have your own email server or use a hosting provider:

```python
EMAIL_CONFIG = {
    "SMTP_SERVER": "mail.yourdomain.com",
    "SMTP_PORT": 587,  # or 465 for SSL
    "EMAIL_ADDRESS": "noreply@yourdomain.com",
    "EMAIL_PASSWORD": "your-password",
    "USE_TLS": True  # or False if using SSL on port 465
}
```

### **Option 4: Business Email Services**

**SendGrid, Mailgun, Amazon SES**, etc. - Use their SMTP settings.

---

## 🔧 Installation & Testing

### **Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 2: Update Configuration**
Edit `email_service.py` with your SMTP settings.

### **Step 3: Test Email Configuration**
```bash
python test_email.py
```

### **Step 4: Start the Server**
```bash
python main.py
```

### **Step 5: Test Booking Email**
Create a test booking through the frontend and check if you receive the confirmation email.

---

## 🛠️ Troubleshooting

### **Common Issues:**

#### **"Authentication failed"**
- ✅ Check that your email and password are correct
- ✅ For Gmail: Use App Password, not your regular password
- ✅ Enable "Less secure app access" if using regular password (not recommended)

#### **"Connection refused"**
- ✅ Check SMTP server address and port
- ✅ Verify your internet connection
- ✅ Check if your firewall blocks the SMTP port

#### **"TLS/SSL errors"**
- ✅ Try with `USE_TLS: False` if using port 465
- ✅ Try with different ports (587, 465, 25)

#### **Emails not being sent**
- ✅ Check server logs for error messages
- ✅ Verify email configuration is correct
- ✅ Test with a simple email client first

### **Debug Mode:**
To see detailed email sending logs, the system will print status messages:
- ✅ `Confirmation email sent to customer@email.com`
- ⚠️ `Failed to send confirmation email to customer@email.com`
- ❌ `Email sending error: [error details]`

---

## 🎨 Email Template Customization

### **Styling:**
The email templates use professional HTML with:
- **Hotel branding colors** (Gold #D4AF37, Navy #1B2B44)
- **Responsive design** for mobile devices
- **Professional typography** for readability
- **Structured layout** with clear sections

### **Customizing Templates:**
Edit the `_create_booking_confirmation_email()` and `_create_cancellation_email()` methods in `email_service.py` to:
- Change colors and styling
- Add your hotel logo
- Modify text content
- Add additional information

---

## 🔒 Security Best Practices

### **Email Security:**
1. **Use App Passwords** instead of regular passwords
2. **Enable TLS encryption** for secure transmission
3. **Use dedicated email account** for hotel notifications
4. **Regularly rotate passwords**
5. **Monitor email sending logs**

### **Privacy:**
- Emails contain guest personal information
- Ensure SMTP connection is encrypted
- Don't log email content or passwords
- Follow data protection regulations

---

## 📊 Monitoring & Analytics

### **Email Delivery Tracking:**
- Check server logs for email sending status
- Monitor email bounce rates
- Track customer engagement with confirmations

### **Server Logs:**
```
✅ Confirmation email sent to guest@email.com for booking BK000123
⚠️  Failed to send confirmation email to guest@email.com
❌ Email sending error: [Errno 111] Connection refused
```

---

## 🎉 Ready to Go!

Once configured, your hotel management system will automatically:

1. **Send confirmation emails** when customers make bookings
2. **Send cancellation emails** when bookings are cancelled
3. **Include all booking details** with professional formatting
4. **Provide hotel contact information** for customer service
5. **Maintain professional appearance** matching your hotel brand

### **Test the Complete Flow:**
1. Make a test booking through the frontend
2. Check your email for the confirmation
3. Cancel the booking through "Manage Bookings"
4. Check your email for the cancellation confirmation

**Your hotel now provides professional email communications to enhance the customer experience!** 🏨✨

---

## 📞 Support

If you need help with email setup:
1. Check the troubleshooting section above
2. Verify your email provider's SMTP settings
3. Test with a simple email client first
4. Check firewall and network settings

**Happy emailing!** 📧🎉 