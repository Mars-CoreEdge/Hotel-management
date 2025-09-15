# Supabase Booking Integration Setup Guide

This guide will help you set up the enhanced chatbot booking functionality with Supabase real-time subscriptions.

## Prerequisites

1. A Supabase project (create one at [supabase.com](https://supabase.com))
2. Your Supabase project URL and anonymous key
3. Node.js and npm installed

## Step 1: Create the Bookings Table

Run the following SQL in your Supabase SQL Editor:

```sql
-- Create the bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    room_type TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_bookings_email ON bookings(email);
CREATE INDEX IF NOT EXISTS idx_bookings_created_at ON bookings(created_at);

-- Enable Row Level Security (RLS)
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;

-- Create policies for public access
CREATE POLICY "Allow public booking insert" ON bookings
    FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Allow public booking read" ON bookings
    FOR SELECT
    USING (true);

-- Enable real-time subscriptions
ALTER PUBLICATION supabase_realtime ADD TABLE bookings;
```

## Step 2: Configure Environment Variables

Create a `.env` file in the `fruit-store-ui` directory:

```env
# Supabase Configuration
REACT_APP_SUPABASE_URL=https://your-project-id.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-supabase-anon-key-here

# API Configuration
REACT_APP_API_URL=http://localhost:8001
```

Replace the values with your actual Supabase credentials:
- Get your project URL from your Supabase dashboard
- Get your anonymous key from Settings > API

## Step 3: Install Dependencies

The required dependencies are already included in `package.json`:
- `@supabase/supabase-js`: ^2.56.0

If you need to install them manually:
```bash
cd fruit-store-ui
npm install @supabase/supabase-js
```

## Step 4: Test the Implementation

1. Start your backend server:
```bash
python main.py
```

2. Start your frontend:
```bash
cd fruit-store-ui
npm start
```

3. Navigate to the AI Reception page
4. Try booking a room by chatting with the AI:
   - "I'd like to book a room"
   - "My name is John Doe"
   - "My email is john@example.com"
   - "My phone is 555-123-4567"
   - "I want to check in on 2024-01-15"
   - "I want to check out on 2024-01-18"
   - "I'd like a deluxe room"

## Features Implemented

### 1. Supabase Integration
- ✅ Bookings table with proper schema
- ✅ Real-time subscriptions for new bookings
- ✅ Secure environment variable configuration
- ✅ Error handling and validation

### 2. Enhanced Chatbot
- ✅ Automatic booking extraction from conversation
- ✅ Supabase booking creation
- ✅ Fallback to original booking system
- ✅ Real-time booking notifications

### 3. User Interface
- ✅ Toast notifications for booking confirmations
- ✅ Real-time connection status indicator
- ✅ Recent bookings display
- ✅ "Manage Bookings" button in success toast
- ✅ Professional styling and animations

### 4. Real-time Features
- ✅ Live updates when new bookings are created
- ✅ Connection status monitoring
- ✅ Automatic reconnection on connection loss
- ✅ Recent bookings list updates in real-time

## File Structure

```
fruit-store-ui/
├── src/
│   ├── components/
│   │   ├── Toast.js          # Toast notification component
│   │   └── Toast.css         # Toast styling
│   ├── services/
│   │   └── bookingService.js # Supabase booking service
│   ├── hooks/
│   │   └── useRealtimeBookings.js # Real-time subscription hook
│   ├── config/
│   │   └── supabase.js       # Supabase client configuration
│   └── AIReception.js        # Enhanced chatbot component
├── .env                      # Environment variables
└── package.json             # Dependencies

supabase_bookings_schema.sql  # Database schema
```

## Troubleshooting

### Common Issues

1. **"Supabase client not initialized" error**
   - Check your `.env` file has correct values
   - Ensure environment variables are prefixed with `REACT_APP_`
   - Restart your development server after adding environment variables

2. **Real-time connection not working**
   - Verify the bookings table is added to the realtime publication
   - Check your Supabase project's real-time settings
   - Look for connection errors in the browser console

3. **Booking creation fails**
   - Check the browser console for detailed error messages
   - Verify the bookings table exists and has the correct schema
   - Ensure RLS policies allow public inserts

4. **Toast notifications not showing**
   - Check if the Toast component is properly imported
   - Verify the CSS file is included
   - Look for JavaScript errors in the console

### Testing Real-time Features

1. Open the AI Reception in two browser tabs
2. Create a booking in one tab
3. Watch the other tab receive the real-time update
4. Check the "Recent Bookings" section updates automatically

## Security Notes

- The current setup allows public read/write access to bookings
- For production, consider implementing proper authentication
- Add input validation and sanitization
- Consider rate limiting for booking creation

## Next Steps

1. Add user authentication for secure bookings
2. Implement booking management features
3. Add email notifications for bookings
4. Create admin dashboard for booking management
5. Add booking status tracking (confirmed, cancelled, etc.)

## Support

If you encounter any issues:
1. Check the browser console for errors
2. Verify your Supabase configuration
3. Ensure all environment variables are set correctly
4. Check the network tab for failed API calls
