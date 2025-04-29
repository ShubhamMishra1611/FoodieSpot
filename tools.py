
import datetime
from restaurants import RESTAURANTS, get_restaurant_by_id
from bookings import check_restaurant_availability, add_booking

def search_restaurants(cuisine=None, location_area=None, price_range=None, ambiance=None, party_size=None, date=None, time=None):
    """
    Searches for restaurants based on criteria.
    If date, time, and party_size are provided, it can optionally check availability.
    """
    results = []
    for r in RESTAURANTS:
        match = True
        
        if cuisine:
            if isinstance(r['cuisine'], str):
                if not any(c.lower() in r['cuisine'].lower() for c in cuisine):
                    match = False
            elif isinstance(r['cuisine'], list):
                if not any(any(c.lower() in rc.lower() for rc in r['cuisine']) for c in cuisine):
                    match = False
            else:
                match = False  

        
        if cuisine:
             cuisine_lower = cuisine.lower()
             if isinstance(r['cuisine'], list):
                 if not any(c.lower() == cuisine_lower for c in r['cuisine']):
                     match = False
             elif isinstance(r['cuisine'], str):
                 if cuisine_lower != r['cuisine'].lower():
                     match = False
             else: 
                 match = False


        if location_area and location_area.lower() != r['location_area'].lower():
            match = False
        if price_range and price_range != r['price_range']:
            match = False
        if ambiance:
            ambiance_lower = ambiance.lower()
            if not any(a.lower() == ambiance_lower for a in r['ambiance']):
                 match = False


        if match:
            
            restaurant_info = r.copy()

            
            if date and time and party_size:
                 
                 availability = check_restaurant_availability(r['id'], date, time, party_size)
                 restaurant_info['availability_checked'] = True
                 restaurant_info['is_available_at_request'] = availability.get('available', False)
            else:
                 restaurant_info['availability_checked'] = False


            results.append(restaurant_info)

    
    results.sort(key=lambda x: x.get('is_available_at_request', False), reverse=True)

    
    max_results = 3
    return results[:max_results]


def make_reservation(restaurant_id, date, time, party_size, customer_name, customer_contact="Not Provided"):
    """Makes a reservation using the booking system."""
    
    if not all([restaurant_id, date, time, party_size, customer_name]):
        return {"success": False, "reason": "Missing required information (restaurant, date, time, party size, name)."}
    
    
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        datetime.datetime.strptime(time, '%H:%M')
    except ValueError:
        return {"success": False, "reason": "Invalid date or time format (use YYYY-MM-DD and HH:MM)."}

    result = add_booking(restaurant_id, date, time, party_size, customer_name, customer_contact)
    return result


AVAILABLE_TOOLS = {
    "search_restaurants": search_restaurants,
    "check_availability": check_restaurant_availability, 
    "make_reservation": make_reservation,
}


TOOL_DESCRIPTIONS = """
Available Tools:
[
    {
        "tool_name": "search_restaurants",
        "description": "Searches for restaurants based on criteria like cuisine, location, price, or ambiance. Can also check availability for a specific date, time, and party size if provided.",
        "parameters": [
            {"name": "cuisine", "type": "string", "description": "Type of food (e.g., 'Italian', 'Mexican', 'Seafood')"},
            {"name": "location_area", "type": "string", "description": "General area of the city (e.g., 'Downtown', 'Seaside', 'North End')"},
            {"name": "price_range", "type": "string", "description": "Price category (e.g., '$$', '$$$', '$$$$')"},
            {"name": "ambiance", "type": "string", "description": "Atmosphere keywords (e.g., 'Romantic', 'Casual', 'Lively')"},
            {"name": "party_size", "type": "integer", "description": "Number of people"},
            {"name": "date", "type": "string", "description": "Desired date (YYYY-MM-DD)"},
            {"name": "time", "type": "string", "description": "Desired time (HH:MM, 24-hour format)"}
        ]
    },
    {
        "tool_name": "make_reservation",
        "description": "Books a table at a specific restaurant for a given date, time, and party size.",
        "parameters": [
            {"name": "restaurant_id", "type": "string", "description": "The unique ID of the restaurant (e.g., 'FS01', 'FS03')."},
            {"name": "date", "type": "string", "description": "Date of booking (YYYY-MM-DD)"},
            {"name": "time", "type": "string", "description": "Time of booking (HH:MM, 24-hour format)"},
            {"name": "party_size", "type": "integer", "description": "Number of people for the booking"},
            {"name": "customer_name", "type": "string", "description": "Name for the reservation"},
            {"name": "customer_contact", "type": "string", "description": "(Optional) Phone number or email"}
        ]
    }
]
"""