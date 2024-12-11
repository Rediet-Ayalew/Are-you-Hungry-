from flask import Flask, render_template, request, redirect, url_for, session, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
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
class RestaurantData(db.Model):
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
    password_hash = db.Column(db.String(128), nullable=False)  # Store hashed password
    favorite_cuisines = db.Column(db.Text)  # Store as JSON or comma-separated values
    dietary_restrictions = db.Column(db.Text)  # Store as JSON or comma-separated values
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Cuisine Mapping
CUISINE_MAPPING = {
    "American": [
        "American", "New American", "Southern", "Diners", "Burgers", 
        "Steakhouses", "Traditional American", "Fast Food", "Chicken Shop"
    ],
    "Asian": [
        "Asian", "Chinese", "Japanese", "Korean", "Thai", "Asian Fusion",
        "Sushi", "Vietnamese", "Pan Asian", "Filipino", "Sushi Bars", "Bubble Tea"
    ],
    "Italian": [
        "Italian", "Pizza", "Pasta Shops", "Tuscan", 
        "Sicilian", "Trattoria"
    ],
    "Mexican": [
        "Mexican", "Tex-Mex", "Tacos", "Burritos", 
        "Latin American", "Central American", "Food Trucks"
    ],
    "Mediterranean": [
        "Mediterranean", "Greek", "Middle Eastern", "Turkish", 
        "Lebanese", "Persian", "Moroccan"
    ],
    "All": [
        "Mediterranean", "Greek", "Middle Eastern", "Turkish", 
        "Lebanese", "Persian", "Moroccan", "American", "New American", "Southern", "Diners", "Burgers", 
        "Steakhouses", "Traditional American", "Fast Food", "Chicken Shop", "Asian", "Chinese", "Japanese", "Korean", "Thai", 
        "Sushi", "Vietnamese", "Pan Asian", "Filipino", "Sushi Bars", "Bubble Tea", "Asian Fusion", "Italian", "Pizza", "Pasta Shops", "Tuscan", 
        "Sicilian", "Trattoria", "Mexican", "Tex-Mex", "Tacos", "Burritos", 
        "Latin American", "Central American", "Food Trucks"
    ],
}

# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.user_id
            session['username'] = user.username
            return redirect(url_for('profile', user_id=user.user_id))
        else:
            return render_template('login.html', error_message="Invalid username or password")

    return render_template('login.html')

# Route for the restaurants page
@app.route('/restaurants', methods=['GET'])
def restaurants():
    if request.method == 'GET' and 'term' in request.args:
        return get_restaurants()  # Use helper function for restaurant search
    return render_template('restaurants.html')

# Helper function for restaurant search
@app.route('/restaurants/api', methods=['GET'])
def get_restaurants():
    try:
        cuisine = request.args.get('cuisine', None)  # Get cuisine from query params
        restaurants = search_restaurants("restaurants", 41.619549, -93.598022, 40000, 50)

        if cuisine:
            # Apply filtering based on cuisine
            filtered_categories = CUISINE_MAPPING.get(cuisine, [])
            result = [
                {
                    "name": r.get("name", "N/A"),
                    "address": ", ".join(r.get("location", {}).get("display_address", [])),
                    "rating": r.get("rating", None),
                    "website": r.get("url", "No website available"),
                    "cuisine": r.get("categories", [{}])[0].get("title", "No cuisine available"),
                    "phone": r.get("phone", "No phone available"),
                }
                for r in restaurants
                if any(cat.get("title") in filtered_categories for cat in r.get("categories", []))
            ]
        else:
            # No filtering; return all restaurants
            result = [
                {
                    "name": r.get("name", "N/A"),
                    "address": ", ".join(r.get("location", {}).get("display_address", [])),
                    "rating": r.get("rating", None),
                    "website": r.get("url", "No website available"),
                    "cuisine": r.get("categories", [{}])[0].get("title", "No cuisine available"),
                    "phone": r.get("phone", "No phone available"),
                }
                for r in restaurants
            ]

        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error fetching restaurants: {e}")
        return jsonify({"error": str(e)}), 500


# Route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        favorite_cuisines = request.form['favorite_cuisines']
        dietary_restrictions = request.form['dietary_restrictions']

        password_hash = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            favorite_cuisines=favorite_cuisines,
            dietary_restrictions=dietary_restrictions
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            return render_template('register.html', error_message=str(e))

    return render_template('register.html')

# Route for the profile page
@app.route('/profile/<int:user_id>')
def profile(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        return redirect(url_for('login'))

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

    return render_template('profile.html', user=user_data)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
