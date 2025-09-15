-- Supabase Bookings Table Schema
-- This file contains the SQL to create the bookings table in Supabase

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

-- Create an index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_bookings_email ON bookings(email);

-- Create an index on created_at for sorting
CREATE INDEX IF NOT EXISTS idx_bookings_created_at ON bookings(created_at);

-- Enable Row Level Security (RLS)
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows anyone to insert bookings (for public booking form)
CREATE POLICY "Allow public booking insert" ON bookings
    FOR INSERT
    WITH CHECK (true);

-- Create a policy that allows anyone to read bookings (for public viewing)
CREATE POLICY "Allow public booking read" ON bookings
    FOR SELECT
    USING (true);

-- Enable real-time subscriptions for the bookings table
ALTER PUBLICATION supabase_realtime ADD TABLE bookings;
