RESTAURANTS = [
    {
        "id": "FS01", "name": "FoodieSpot Downtown Grill", "location_area": "Downtown",
        "address": "123 Main St, City Center", "cuisine": ["American", "Steakhouse"],
        "capacity": 80, "opening_hours": {"mon-fri": "11:00-22:00", "sat-sun": "12:00-23:00"},
        "price_range": "$$$", "ambiance": ["Business", "Casual", "Modern"],
        "description": "Classic American grill in the heart of downtown."
    },
    {
        "id": "FS02", "name": "FoodieSpot Seaside Bistro", "location_area": "Seaside",
        "address": "45 Beach Ave, Waterfront", "cuisine": ["Seafood", "French"],
        "capacity": 60, "opening_hours": {"tue-sun": "12:00-21:00", "mon": "closed"},
        "price_range": "$$$$", "ambiance": ["Romantic", "Scenic", "Cozy"],
        "description": "Fresh seafood and French-inspired dishes with ocean views."
    },
    {
        "id": "FS03", "name": "FoodieSpot Trattoria", "location_area": "Downtown",
        "address": "125 Main St, City Center", "cuisine": ["Italian", "Pizza"],
        "capacity": 50, "opening_hours": {"mon-sun": "12:00-22:00"},
        "price_range": "$$", "ambiance": ["Casual", "Family-Friendly", "Warm"],
        "description": "Authentic Italian pasta and pizza."
    },
    {
        "id": "FS04", "name": "FoodieSpot North End Cafe", "location_area": "North End",
        "address": "88 Maple Rd, North End", "cuisine": ["Cafe", "Sandwiches", "Vegetarian"],
        "capacity": 30, "opening_hours": {"mon-fri": "08:00-18:00", "sat": "09:00-17:00", "sun": "closed"},
        "price_range": "$", "ambiance": ["Casual", "Cozy", "Quiet"],
        "description": "Cozy cafe with great coffee, sandwiches, and vegetarian options."
    },
    {
        "id": "FS05", "name": "FoodieSpot Fusion Hub", "location_area": "Uptown",
        "address": "210 Tech Plaza, Uptown", "cuisine": ["Asian Fusion", "Sushi"],
        "capacity": 70, "opening_hours": {"mon-sat": "17:00-23:00", "sun": "closed"},
        "price_range": "$$$", "ambiance": ["Modern", "Lively", "Trendy"],
        "description": "Exciting Asian Fusion dishes and creative sushi rolls."
    },
    {
        "id": "FS06", "name": "FoodieSpot Taqueria", "location_area": "West Side",
        "address": "5 Sunset Blvd, West Side", "cuisine": ["Mexican"],
        "capacity": 40, "opening_hours": {"mon-sun": "11:00-21:00"},
        "price_range": "$$", "ambiance": ["Casual", "Lively", "Colorful"],
        "description": "Authentic street-style tacos and Mexican favorites."
    },
    {
        "id": "FS07", "name": "FoodieSpot Garden Terrace", "location_area": "Uptown",
        "address": "212 Tech Plaza, Uptown", "cuisine": ["Mediterranean", "Healthy"],
        "capacity": 90, "opening_hours": {"mon-sun": "12:00-22:00"},
        "price_range": "$$$", "ambiance": ["Elegant", "Outdoor Seating", "Relaxed"],
        "description": "Mediterranean cuisine with a focus on fresh ingredients and a beautiful terrace."
    },
    {
        "id": "FS08", "name": "FoodieSpot Downtown Deli", "location_area": "Downtown",
        "address": "130 Main St, City Center", "cuisine": ["Deli", "Sandwiches"],
        "capacity": 25, "opening_hours": {"mon-fri": "09:00-16:00", "sat-sun": "closed"},
        "price_range": "$", "ambiance": ["Casual", "Quick Bite"],
        "description": "Classic deli sandwiches and soups, perfect for a quick lunch."
    },
    {
        "id": "FS09", "name": "FoodieSpot Curry House", "location_area": "North End",
        "address": "90 Maple Rd, North End", "cuisine": ["Indian"],
        "capacity": 55, "opening_hours": {"tue-sun": "17:00-22:00", "mon": "closed"},
        "price_range": "$$", "ambiance": ["Casual", "Authentic", "Aromatic"],
        "description": "Flavorful Indian curries and traditional dishes."
    },
    {
        "id": "FS10", "name": "FoodieSpot BBQ Pit", "location_area": "West Side",
        "address": "15 Smokey Ln, West Side", "cuisine": ["BBQ", "American"],
        "capacity": 100, "opening_hours": {"wed-sun": "12:00-21:00", "mon-tue": "closed"},
        "price_range": "$$", "ambiance": ["Casual", "Rustic", "Lively"],
        "description": "Slow-smoked BBQ ribs, brisket, and classic sides."
    },
    {
        "id": "FS20", "name": "FoodieSpot Rooftop Bar", "location_area": "Downtown",
        "address": "500 Skyscraper Ave, Fl 30, City Center", "cuisine": ["Tapas", "Cocktails"],
        "capacity": 120, "opening_hours": {"mon-sat": "16:00-00:00", "sun": "16:00-22:00"},
        "price_range": "$$$$", "ambiance": ["Trendy", "Scenic View", "Upscale", "Lively"],
        "description": "Craft cocktails and small plates with stunning city views."
    }
]

def get_restaurant_by_id(restaurant_id):
    for r in RESTAURANTS:
        if r['id'] == restaurant_id:
            return r
    return None