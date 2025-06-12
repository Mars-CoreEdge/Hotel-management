import requests
import json
from datetime import datetime, timedelta

def test_room_endpoints():
    base_url = "http://localhost:8001"
    
    print("🧪 Testing FastAPI Hotel Room Management Endpoints")
    print("=" * 60)
    
    # Test 1: GET /rooms - Get all rooms
    print("\n1️⃣  Testing GET /rooms")
    try:
        response = requests.get(f"{base_url}/rooms")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            rooms = response.json()
            print(f"   ✅ Success! Found {len(rooms)} rooms")
            if rooms:
                print(f"   📋 Sample room: {rooms[0]}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: GET /rooms/available - Get available rooms
    print("\n2️⃣  Testing GET /rooms/available")
    try:
        response = requests.get(f"{base_url}/rooms/available")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            available_rooms = response.json()
            print(f"   ✅ Success! Found {len(available_rooms)} available rooms")
            if available_rooms:
                print(f"   📋 Sample available room: {available_rooms[0]}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: POST /rooms - Create new room
    print("\n3️⃣  Testing POST /rooms")
    new_room_data = {
        "room_number": "TEST-API-001",
        "room_type": "Suite",
        "price_per_night": 250.0
    }
    try:
        response = requests.post(
            f"{base_url}/rooms", 
            json=new_room_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success! Created room: {result['room']['room_number']}")
            created_room_id = result['room']['id']
            print(f"   🆔 Room ID: {created_room_id}")
            return created_room_id
        else:
            print(f"   ❌ Failed: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None
    
def test_update_delete(room_id):
    base_url = "http://localhost:8001"
    
    if room_id is None:
        print("\n⚠️  Skipping UPDATE and DELETE tests (no room ID)")
        return
    
    # Test 4: PUT /rooms/{room_id} - Update room
    print(f"\n4️⃣  Testing PUT /rooms/{room_id}")
    update_data = {
        "room_number": "TEST-API-001-UPDATED",
        "room_type": "Presidential",
        "price_per_night": 500.0,
        "is_available": False
    }
    try:
        response = requests.put(
            f"{base_url}/rooms/{room_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success! Updated room: {result['room']['room_number']}")
            print(f"   📝 New price: ${result['room']['price_per_night']}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: DELETE /rooms/{room_id} - Delete room
    print(f"\n5️⃣  Testing DELETE /rooms/{room_id}")
    try:
        response = requests.delete(f"{base_url}/rooms/{room_id}")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success! {result['message']}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_guest_endpoints():
    base_url = "http://localhost:8001"
    
    print("\n" + "=" * 60)
    print("👥 Testing Guest Management Endpoints")
    print("=" * 60)
    
    # Test 1: GET /guests - Get all guests
    print("\n1️⃣  Testing GET /guests")
    try:
        response = requests.get(f"{base_url}/guests")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            guests = response.json()
            print(f"   ✅ Success! Found {len(guests)} guests")
            if guests:
                print(f"   📋 Sample guest: {guests[0]}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: POST /guests - Create new guest
    print("\n2️⃣  Testing POST /guests")
    new_guest_data = {
        "first_name": "Test",
        "last_name": "User", 
        "email": "test.user@example.com",
        "phone": "+1-555-9999"
    }
    try:
        response = requests.post(
            f"{base_url}/guests",
            json=new_guest_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success! Created guest: {result['guest']['first_name']} {result['guest']['last_name']}")
            created_guest_id = result['guest']['id']
            print(f"   🆔 Guest ID: {created_guest_id}")
            return created_guest_id
        else:
            print(f"   ❌ Failed: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_guest_update_delete(guest_id):
    base_url = "http://localhost:8001"
    
    if guest_id is None:
        print("\n⚠️  Skipping Guest UPDATE and DELETE tests (no guest ID)")
        return
    
    # Test 3: PUT /guests/{guest_id} - Update guest
    print(f"\n3️⃣  Testing PUT /guests/{guest_id}")
    update_data = {
        "first_name": "Updated",
        "last_name": "TestUser",
        "email": "updated.testuser@example.com",
        "phone": "+1-555-8888"
    }
    try:
        response = requests.put(
            f"{base_url}/guests/{guest_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success! Updated guest: {result['guest']['first_name']} {result['guest']['last_name']}")
            print(f"   📧 New email: {result['guest']['email']}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: DELETE /guests/{guest_id} - Delete guest
    print(f"\n4️⃣  Testing DELETE /guests/{guest_id}")
    try:
        response = requests.delete(f"{base_url}/guests/{guest_id}")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success! {result['message']}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_booking_endpoints():
    base_url = "http://localhost:8001"
    
    print("\n" + "=" * 60)
    print("📅 Testing Booking Management Endpoints")
    print("=" * 60)
    
    # Test 1: GET /bookings - Get all bookings
    print("\n1️⃣  Testing GET /bookings")
    try:
        response = requests.get(f"{base_url}/bookings")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            bookings = response.json()
            print(f"   ✅ Success! Found {len(bookings)} bookings")
            if bookings:
                print(f"   📋 Sample booking: {bookings[0]}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: POST /bookings - Create new booking
    print("\n2️⃣  Testing POST /bookings")
    # Calculate dates for a 3-night stay
    check_in = datetime.now() + timedelta(days=1)
    check_out = check_in + timedelta(days=3)
    
    new_booking_data = {
        "guest_id": 1,  # Assuming first guest exists
        "room_id": 1,   # Assuming first room exists
        "check_in_date": check_in.isoformat(),
        "check_out_date": check_out.isoformat(),
        "total_price": 240.0  # 3 nights * 80/night
    }
    try:
        response = requests.post(
            f"{base_url}/bookings",
            json=new_booking_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success! Created booking for: {result['booking']['guest_name']}")
            print(f"   🏨 Room: {result['booking']['room_number']}")
            created_booking_id = result['booking']['id']
            print(f"   🆔 Booking ID: {created_booking_id}")
            return created_booking_id
        else:
            print(f"   ❌ Failed: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_booking_delete(booking_id):
    base_url = "http://localhost:8001"
    
    if booking_id is None:
        print("\n⚠️  Skipping Booking DELETE test (no booking ID)")
        return
    
    # Test 3: DELETE /bookings/{booking_id} - Cancel booking
    print(f"\n3️⃣  Testing DELETE /bookings/{booking_id}")
    try:
        response = requests.delete(f"{base_url}/bookings/{booking_id}")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success! {result['message']}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_root_endpoint():
    base_url = "http://localhost:8001"
    
    print("\n" + "=" * 60)
    print("🏠 Testing Root Endpoint")
    print("=" * 60)
    
    print("\n1️⃣  Testing GET /")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success! API Info:")
            print(f"   📝 Message: {result['message']}")
            print(f"   📊 Version: {result['version']}")
            print(f"   🔗 Available endpoints: {list(result['endpoints'].keys())}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Comprehensive API Endpoint Tests...")
    
    # Test server connection first
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        print("✅ Server is reachable!")
    except Exception as e:
        print(f"❌ Cannot reach server: {e}")
        print("🔧 Make sure FastAPI server is running: python main.py")
        exit(1)
    
    # Run all tests
    test_root_endpoint()
    
    room_id = test_room_endpoints()
    test_update_delete(room_id)
    
    guest_id = test_guest_endpoints()
    test_guest_update_delete(guest_id)
    
    booking_id = test_booking_endpoints()
    test_booking_delete(booking_id)
    
    print("\n" + "=" * 60)
    print("🎉 All Endpoint Testing Completed!")
    print("📊 Check the results above for any issues.")
    print("🌐 Visit http://localhost:8001/docs for interactive API documentation") 