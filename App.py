from flask import Flask, jsonify, request
from yelp import search_restaurants

#Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Hungry and Undecided"})

#Fetch restaurant data from Yelp.py
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    #Get search parameters from the URL query string
    search_term = request.args.get('term', 'restaurant')
    latitude = float(request.args.get('latitude', 41.619549))
    longitude = float(request.args.get('longitude', -93.598022))
    radius = int(request.args.get('radius', 40000))
    limit = int(request.args.get('limit', 10))

    #Fetch restuarants using the function from yelp.py
    restaurants = search_restaurants(search_term, latitude, longitude, radius, limit)

    #if no restuarants are found return an empty list
    if not restaurants:
        return jsonify({"message": "No restuarnts found."}), 404

        #Otherwise, format and return the restaurant data as JSON
        result = []
        for business in restaurants:
            name = business.get("name", "N/A")
            address = ",".join(business.get("location", {}).get("display_address", []))
            rating = business.get("rating", "N/A")
            website = business.get("url", "No website available")
            categories = business.get("categories", [])
            cuisine = categories[0].get("title", "No cuisine available") if categories else "No cuisine available"
            phone = business.get("phone", "No phone available")

            #Format the restauarant data into a dictionary
            resturant_info = {
                "name" : name,
                "address" : address,
                "rating" : rating,
                "website" : website,
                "categories" : categories,
                "cuisine" : cuisine,
                "phone" : phone
            }
            reuslt.append(restaurant_info)

        return jsonify(result)

#run the app
if __name__ == '__main__':
    app.run(debug=True)

