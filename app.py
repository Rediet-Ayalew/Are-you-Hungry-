from flask import Flask, render_template, request, redirect, url_for, session, jsonify, current_app, flash 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from YelpAPI import search_restaurants
import pyodbc

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'password_secret_key_123'

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

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=sqlserverndibalekeralynette01.database.windows.net;"
    "DATABASE=sqldbndibalekeralynette01;"
    "UID=sqlserveradmin;"
    "PWD=Password123;"
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
    password_hash = db.Column(db.String(128), nullable=False)
    favorite_cuisines = db.Column(db.Text)
    dietary_restrictions = db.Column(db.Text)
    profile_icon = db.Column(db.String(200),  default='cool.png')
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
        "Italian", "Pasta Shops", "Tuscan", 
        "Sicilian", "Trattoria", "Beer Bar"
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
        "Latin American", "Central American", "Food Trucks", "Bars", "Beer Bar"
    ],
}

# Route for the homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')  # Ensure you have a home.html file in the templates folder

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password_hash, password):
                session['user_id'] = user.user_id
                session['username'] = user.username
                return redirect(url_for('profile', user_id=user.user_id))
            else:
                # Password is incorrect
                error_message = "Incorrect password."
                return render_template('login.html', error_message=error_message)
        else:
            # No user found
            error_message = "Username does not exist."
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')
    
#app route for log out 
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login'))

# Route for the restaurants page
@app.route('/restaurants', methods=['GET'])
def restaurants():
    if request.method == 'GET' and 'term' in request.args:
        return get_restaurants()  # Use helper function for restaurant search
    return render_template('restaurants.html')

@app.route('/submit-rating', methods=['POST'])
def submit_rating():
    data = request.get_json()
    rating = data.get('rating')

    if not rating:
        return jsonify({"error": "No rating received"}), 400

    # TODO: Save the rating to the database or log it
    print(f"Received rating: {rating}")

    return jsonify({"message": "Rating submitted successfully!"}), 200

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
        
        # Helps users realize they already have an account with the website
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', error_message="This email already exists. Please use a different email.")

        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            favorite_cuisines=favorite_cuisines,
            dietary_restrictions=dietary_restrictions
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

# Route for forgot password page
@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        
        # Check if the username exists in the database
        user = User.query.filter_by(username=username).first()
        
        if user:
            session['reset_user'] = username
            return redirect(url_for('create_password'))
        else:
            return render_template('forgotpassword.html', error_message='Username not found. Please try again.')
    
    return render_template('forgotpassword.html')


# Route for create password page
@app.route('/createpassword', methods=['GET', 'POST'])
def create_password():
    if 'reset_user' not in session:
        return redirect(url_for('forgotpassword'))  # Don't allow access if they didn't come from forgot password

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            return render_template('createpassword.html', error_message='Passwords do not match.')

        if len(new_password) < 8:
            return render_template('createpassword.html', error_message='Password must be at least 8 characters long.')

        # Find the user based on the session stored username
        user = User.query.filter_by(username=session['reset_user']).first()
        
        if user:
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            session.pop('reset_user', None)  # Clear reset_user session
            return redirect(url_for('login'))  # Redirect to the login page after resetting password
        else:
            return render_template('createpassword.html', error_message='User not found.')
    
    return render_template('createpassword.html')




# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')
    
# Route for the profile page
@app.route('/profile/<int:user_id>')
def profile(user_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Retrieve the user from the database
    user = User.query.get(user_id)
    if not user:
        return render_template('404.html'), 404

    # Process favorite cuisines and dietary restrictions
    favorite_cuisines = [cuisine.strip().lower() for cuisine in (user.favorite_cuisines or "").split(",") if cuisine.strip()]
    dietary_restrictions = [restriction.strip().lower() for restriction in (user.dietary_restrictions or "").split(",") if restriction.strip()]

    # Debugging information
    print(f"Favorite Cuisines: {favorite_cuisines}")
    print(f"Dietary Restrictions: {dietary_restrictions}")

    # Fetch recommendations
    latitude = 41.619549  # Example latitude
    longitude = -93.598022  # Example longitude
    all_restaurants = search_restaurants("restaurants", latitude, longitude, 25000, 20) or []
    recommended_restaurants = []
    for r in all_restaurants:
        restaurant_categories = [cat.get("title").lower() for cat in r.get("categories", [])]
        mapped_categories = [
            cuisine.lower() for cat in restaurant_categories
            for cuisine, mapped in CUISINE_MAPPING.items() if any(cat == m.lower() for m in mapped)
        ]
        if any(cat in favorite_cuisines for cat in mapped_categories):
            recommended_restaurants.append({
                "name": r.get("name", "N/A"),
                "address": ", ".join(r.get("location", {}).get("display_address", [])),
                "rating": r.get("rating", None),
                "website": r.get("url", "No website available"),
                "cuisine": restaurant_categories,
                "phone": r.get("phone", "No phone available"),
            })

    print(f"Recommended Restaurants: {recommended_restaurants}")

    # Render the profile template with recommendations
    return render_template(
        'profile.html',
        user=user,
        favorite_cuisines=favorite_cuisines,
        dietary_restrictions=dietary_restrictions,
        recommendations=recommended_restaurants
    )


#Route for Updating profile 
@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if not user:
        return redirect(url_for('login'))
    
    # Update user preferences only if provided
    favorite_cuisines = request.form.get('favorite_cuisines', None)
    dietary_restrictions = request.form.get('dietary_restrictions', None)
    profile_icon = request.form.get('profile_icon', None)

    # Only update fields if they are provided in the form
    if favorite_cuisines is not None and favorite_cuisines.strip():
        user.favorite_cuisines = favorite_cuisines.strip()
    if dietary_restrictions is not None and dietary_restrictions.strip():
        user.dietary_restrictions = dietary_restrictions.strip()
    if profile_icon is not None:
        user.profile_icon = profile_icon

    try:
        db.session.commit()
        return redirect(url_for('profile', user_id=user.user_id))
    except Exception as e:
        db.session.rollback()
        return render_template('profile.html', user=user, error_message=str(e))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

