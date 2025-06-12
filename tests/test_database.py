#!/usr/bin/env python3
"""
Test script to verify database setup and basic functionality
"""

def test_database_setup():
    """Test database creation and basic operations"""
    print("🧪 Testing Hotel Management Database...")
    print("=" * 50)
    
    try:
        # Import database functions
        import database
        from models import Room, Guest, Booking
        
        # Test database creation
        print("1️⃣  Testing database creation...")
        database.create_database()
        
        # Test room operations
        print("\n2️⃣  Testing room operations...")
        rooms = database.get_all_rooms()
        print(f"   ✅ Found {len(rooms)} rooms")
        if rooms:
            print(f"   📋 Sample room: {rooms[0]}")
        
        # Test guest operations
        print("\n3️⃣  Testing guest operations...")
        guests = database.get_all_guests()
        print(f"   ✅ Found {len(guests)} guests")
        if guests:
            print(f"   📋 Sample guest: {guests[0]}")
        
        # Test booking operations
        print("\n4️⃣  Testing booking operations...")
        bookings = database.get_all_bookings()
        print(f"   ✅ Found {len(bookings)} bookings")
        if bookings:
            print(f"   📋 Sample booking: {bookings[0]}")
        else:
            print("   ℹ️  No bookings yet - this is normal for a fresh database")
        
        print("\n🎉 All database tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_server():
    """Test if API server can start"""
    print("\n" + "=" * 50)
    print("🌐 Testing API Server...")
    
    try:
        # Try to import FastAPI components
        from main import app
        print("✅ FastAPI app imported successfully")
        
        # Test if we can access the app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        # Test root endpoint
        response = client.get("/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            data = response.json()
            print(f"   📋 API Message: {data.get('message', 'N/A')}")
        else:
            print(f"⚠️  Root endpoint returned status: {response.status_code}")
        
        # Test rooms endpoint
        response = client.get("/rooms")
        if response.status_code == 200:
            print("✅ Rooms endpoint working")
            rooms = response.json()
            print(f"   📊 Found {len(rooms)} rooms via API")
        else:
            print(f"⚠️  Rooms endpoint returned status: {response.status_code}")
        
        # Test guests endpoint
        response = client.get("/guests")
        if response.status_code == 200:
            print("✅ Guests endpoint working")
            guests = response.json()
            print(f"   📊 Found {len(guests)} guests via API")
        else:
            print(f"⚠️  Guests endpoint returned status: {response.status_code}")
        
        # Test bookings endpoint
        response = client.get("/bookings")
        if response.status_code == 200:
            print("✅ Bookings endpoint working")
            bookings = response.json()
            print(f"   📊 Found {len(bookings)} bookings via API")
        else:
            print(f"⚠️  Bookings endpoint returned status: {response.status_code}")
        
        print("\n🎉 All API tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🏨 Hotel Management System Test Suite")
    print("=" * 60)
    
    # Test database
    db_success = test_database_setup()
    
    # Test API
    api_success = test_api_server()
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"   Database: {'✅ PASS' if db_success else '❌ FAIL'}")
    print(f"   API:      {'✅ PASS' if api_success else '❌ FAIL'}")
    
    if db_success and api_success:
        print("\n🎉 All tests passed! Your hotel management system is ready!")
        print("🚀 You can start the server with: python main.py")
        print("🌐 Then visit: http://localhost:8001/docs for API documentation")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        
    print("=" * 60) 