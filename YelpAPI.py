import requests

 

# Replace with your actual Yelp API Key

API_KEY = "vglYxzlpvwnbD7VDU7nNM7vg_ryERVU6fryvQBajmlqdj7V6MqHXw1ijaHNNanDdUYhX5qftRu_oq_5oo9-6HQ8-MJOFPNPNnN7hr5gRyISEVg5cmrnWpch5_dk7Z3Yx"
 

# Define constants

BASE_URL = "https://api.yelp.com/v3/businesses/search"

HEADERS = {

    "Authorization": f"Bearer {API_KEY}"

}

 

def search_restaurants(term, latitude, longitude, radius=20000, limit=100):

    """

    Searches for restaurants using the Yelp API.

 

    Args:

        term (str): Search term (e.g., "restaurant").

        latitude (float): Latitude of the search location.

        longitude (float): Longitude of the search location.

        radius (int): Search radius in meters (default: 20,000 meters / ~12 miles).

        limit (int): Maximum number of results to return (default: 50).

 

    Returns:

        list: A list of dictionaries containing business details.

    """

    # Define search parameters

    params = {

        "term": term,

        "latitude": latitude,

        "longitude": longitude,

        "radius": radius,

        "limit": limit

    }

 

    try:
        # Print out debug information
        print(f"Requesting Yelp API with params: {params}")
        print(f"Headers: {HEADERS}")

        # Make the GET request

        response = requests.get(BASE_URL, headers=HEADERS, params=params)

        # Print out full response details
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")

        response.raise_for_status()  # Raise an exception for HTTP errors

        # Print out raw response JSON for debugging
        response_json = response.json()
        print(f"Response JSON: {response_json}")

        return response.json().get("businesses", [])

 

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        print(f"Response text: {e.response.text if hasattr(e, 'response') else 'No response'}")
        return []
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return []

 

def display_restaurants(businesses):

    """

    Displays restaurant information.

 

    Args:

        businesses (list): List of businesses returned by the Yelp API.

    """

    if not businesses:

        print("No restaurants found.")

        return

 

    for business in businesses:

        name = business.get("name", "N/A")

        address = ", ".join(business.get("location", {}).get("display_address", []))

        rating = business.get("rating", "N/A")

        website = business.get("url", "No website available")
        
        categories = business.get("categories", [])
        cuisine = "No cuisine available"
        if categories:
            # Use the first category title as the cuisine
            cuisine = categories[0].get("title", "No cuisine available")

        phone = business.get("phone", "No phone available")

        print(f"Name: {name}, Address: {address}, Rating: {rating}, Website: {website}, Cuisines: {cuisine}, PhoneNumber: {phone}")

 

if __name__ == "__main__":

    # Define search parameters

    search_term = "restaurant"

    latitude = 41.619549

    longitude = -93.598022

    radius = 40000  # almost 20 miles in meters

    limit = 10      # Max results per request

 

    # Search and display restaurants

    restaurants = search_restaurants(search_term, latitude, longitude, radius, limit)

    display_restaurants(restaurants)