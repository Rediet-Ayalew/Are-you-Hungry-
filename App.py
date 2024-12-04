from flask import Flask, jsonify, request
from YelpAPI import search_restaurants
from flask_sqlalchemy import SQLAlchemy

#Initialize Flask app
app = Flask(__name__)

DATABASE_CONFIG = {
    'server': 'sqlserverndibalekeralynette01.database.windows.net',
    'database': 'sqldbndibalekeralynette01',
    'username': 'sqlserveradmin',
    'password': 'Password123',
    'driver': 'ODBC Driver 18 for SQL Server'
}

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mssql+pyodbc://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}"
    f"@{DATABASE_CONFIG['server']}/{DATABASE_CONFIG['database']}?driver={DATABASE_CONFIG['driver']}"
)

db = SQLAlchemy(app)

# Define models
class restaurant_data(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False, )
    rating = db.Column(db.Float, nullable=False)
    cuisine = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    website = db.Column(db.String(200), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

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
        return jsonify({"message": "No restaurants found."}), 404

        #Otherwise, format and return the restaurant data as JSON
    result = []
    for business in restaurants:
        name = business.get("name", "N/A")
        address = ",".join(business.get("location", {}).get("display_address", []))
        rating = business.get("rating", "None")
        website = business.get("url", "No website available")
        categories = business.get("categories", [])
        cuisine = categories[0].get("title", "No cuisine available") if categories else "No cuisine available"
        phone = business.get("phone", "No phone available")

        new_restaurant = restaurant_data(
            name=name,
            address=address,
            rating=rating,
            website=website, 
            cuisine=cuisine,
            phone=phone
        )

        db.session.add(new_restaurant)

        #Format the restaarant data into a dictionary
        restaurant_info = {
            "id": new_restaurant.id,
            "name" : name,
            "address" : address,
            "rating" : rating,
            "website" : website,
            "categories" : categories,
            "cuisine" : cuisine,
            "phone" : phone
        }
        result.append(restaurant_info)

    db.session.commit()
    return jsonify(result) 

#run the app
if __name__ == '__main__':
    app.run(debug=True)

