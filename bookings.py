import datetime
from restaurants import RESTAURANTS, get_restaurant_by_id



BOOKINGS = {}



BOOKING_DETAILS = {}
_next_booking_id = 101

def get_current_bookings(restaurant_id, date_str):
    """Gets booked seats for a restaurant on a specific date."""
    return BOOKINGS.get(restaurant_id, {}).get(date_str, {})

def get_restaurant_capacity(restaurant_id):
    """Gets the total capacity of a restaurant."""
    restaurant = get_restaurant_by_id(restaurant_id)
    return restaurant['capacity'] if restaurant else 0

def add_booking(restaurant_id, date_str, time_str, party_size, customer_name, customer_contact):
    """Adds a booking if space is available."""
    global _next_booking_id
    capacity = get_restaurant_capacity(restaurant_id)
    if capacity == 0:
        return {"success": False, "reason": "Invalid restaurant ID."}

    
    if restaurant_id not in BOOKINGS:
        BOOKINGS[restaurant_id] = {}
    if date_str not in BOOKINGS[restaurant_id]:
        BOOKINGS[restaurant_id][date_str] = {}

    current_bookings_at_time = BOOKINGS[restaurant_id][date_str].get(time_str, 0)

    if current_bookings_at_time + party_size <= capacity:
        BOOKINGS[restaurant_id][date_str][time_str] = current_bookings_at_time + party_size
        
        
        booking_id = f"BK{_next_booking_id}"
        BOOKING_DETAILS[booking_id] = {
            "booking_id": booking_id,
            "restaurant_id": restaurant_id,
            "restaurant_name": get_restaurant_by_id(restaurant_id)['name'],
            "date": date_str,
            "time": time_str,
            "party_size": party_size,
            "customer_name": customer_name,
            "customer_contact": customer_contact,
            "status": "Confirmed",
            "timestamp": datetime.datetime.now().isoformat()
        }
        _next_booking_id += 1
        
        print(f"DEBUG: Bookings for {restaurant_id} on {date_str}: {BOOKINGS[restaurant_id][date_str]}") 
        return {"success": True, "booking_id": booking_id, "details": BOOKING_DETAILS[booking_id]}
    else:
        available_seats = capacity - current_bookings_at_time
        return {"success": False, "reason": f"Not enough capacity. Only {available_seats} seats available at {time_str}."}

def check_restaurant_availability(restaurant_id, date_str, time_str, party_size):
    """Checks if a specific time slot is available."""
    capacity = get_restaurant_capacity(restaurant_id)
    if capacity == 0:
        return {"available": False, "reason": "Invalid restaurant ID."}
        
    current_bookings_at_time = get_current_bookings(restaurant_id, date_str).get(time_str, 0)
    
    if current_bookings_at_time + party_size <= capacity:
        return {"available": True}
    else:
        available_seats = capacity - current_bookings_at_time
        return {"available": False, "reason": f"Not enough seats. Only {available_seats} left."}




def cancel_reservation(booking_id):
    """Cancels a reservation by booking ID."""
    if booking_id not in BOOKING_DETAILS:
        return {"success": False, "reason": "Booking ID not found."}

    booking = BOOKING_DETAILS[booking_id]
    restaurant_id = booking["restaurant_id"]
    date_str = booking["date"]
    time_str = booking["time"]
    party_size = booking["party_size"]

    
    current_bookings_at_time = BOOKINGS[restaurant_id][date_str].get(time_str, 0)
    BOOKINGS[restaurant_id][date_str][time_str] = current_bookings_at_time - party_size

    
    booking["status"] = "Cancelled"
    booking["timestamp"] = datetime.datetime.now().isoformat()

    return {"success": True, "details": booking}

def modify_reservation(booking_id, new_date_str=None, new_time_str=None, new_party_size=None):
    """Modifies an existing reservation."""
    if booking_id not in BOOKING_DETAILS:
        return {"success": False, "reason": "Booking ID not found."}

    booking = BOOKING_DETAILS[booking_id]
    restaurant_id = booking["restaurant_id"]
    old_date_str = booking["date"]
    old_time_str = booking["time"]
    old_party_size = booking["party_size"]

    
    current_bookings_at_time = BOOKINGS[restaurant_id][old_date_str].get(old_time_str, 0)
    BOOKINGS[restaurant_id][old_date_str][old_time_str] = current_bookings_at_time - old_party_size

    
    if new_date_str:
        booking["date"] = new_date_str
    if new_time_str:
        booking["time"] = new_time_str
    if new_party_size:
        booking["party_size"] = new_party_size

    
    if restaurant_id not in BOOKINGS:
        BOOKINGS[restaurant_id] = {}
    if booking["date"] not in BOOKINGS[restaurant_id]:
        BOOKINGS[restaurant_id][booking["date"]] = {}

    new_bookings_at_time = BOOKINGS[restaurant_id][booking["date"]].get(booking["time"], 0)
    BOOKINGS[restaurant_id][booking["date"]][booking["time"]] = new_bookings_at_time + booking["party_size"]

    booking["status"] = "Modified"
    booking["timestamp"] = datetime.datetime.now().isoformat()

    return {"success": True, "details": booking}
