from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from YelpAPI import search_restaurants

# Initialize Flask app
app = Flask(__name__)

# Database Configuration 
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
    __tablename__ = 'restaurant_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    website = db.Column(db.String(200))  # Store website if you want
    phone = db.Column(db.String(50))  # Store phone number
    cuisine = db.Column(db.String(100))  # Store cuisine type

class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    favorite_cuisines = db.Column(db.Text)  # Store as JSON or comma-separated values
    dietary_restrictions = db.Column(db.Text)  # Store as JSON or comma-separated values
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html')  

# Route for the login page
@app.route('/login')
def login():
    return render_template('login.html')  

# Route for the restaurants page
@app.route('/restaurants')
def restaurants():
    return render_template('restaurants.html')  

# Fetch restaurant data from YelpAPI.py
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    # Get search parameters from the URL query string
    search_term = request.args.get('term', 'restaurant')
    latitude = float(request.args.get('latitude', 41.619549))
    longitude = float(request.args.get('longitude', -93.598022))
    radius = int(request.args.get('radius', 40000))
    limit = int(request.args.get('limit', 10))

    # Fetch restaurants using the function from yelp.py
    restaurants = search_restaurants(search_term, latitude, longitude, radius, limit)

    # If no restaurants are found return an empty list
    if not restaurants:
        return jsonify({"message": "No restaurants found."}), 404

    # Otherwise, format and return the restaurant data as JSON
    result = []
    for business in restaurants:
        name = business.get("name", "N/A")
        address = ",".join(business.get("location", {}).get("display_address", []))
        rating = business.get("rating", "None")
        website = business.get("url", "No website available")
        categories = business.get("categories", [])
        cuisine = categories[0].get("title", "No cuisine available") if categories else "No cuisine available"
        phone = business.get("phone", "No phone available")

        # Store the restaurant data in the database
        new_restaurant = restaurant_data(
            name=name,
            address=address,
            rating=rating,
            website=website,
            phone=phone,
            cuisine=cuisine
        )

        db.session.add(new_restaurant)

        # Format the restaurant data into a dictionary
        restaurant_info = {
            "name": name,
            "address": address,
            "rating": rating,
            "website": website,
            "categories": categories,
            "cuisine": cuisine,
            "phone": phone
        }
        result.append(restaurant_info)

    # Commit the session after adding all restaurants
    db.session.commit()
    return jsonify(result) 

# Create user profiles
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not all(key in data for key in ('username', 'email', 'favorite_cuisines', 'dietary_restrictions')):
        return jsonify({"message": "Missing required fields"}), 400

    try:
        user = User(
            username=data['username'],
            email=data['email'],
            favorite_cuisines=data['favorite_cuisines'],
            dietary_restrictions=data['dietary_restrictions']
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created", "user_id": user.user_id}), 201
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

# Fetch user profiles
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user_data = {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "favorite_cuisines": user.favorite_cuisines,
        "dietary_restrictions": user.dietary_restrictions,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }
    return jsonify(user_data)

# Update user preferences
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    if 'favorite_cuisines' in data:
        user.favorite_cuisines = data['favorite_cuisines']
    if 'dietary_restrictions' in data:
        user.dietary_restrictions = data['dietary_restrictions']

    db.session.commit()
    return jsonify({"message": "User updated successfully"})

# Delete a user profile
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
