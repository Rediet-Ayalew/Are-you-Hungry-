from flask import Flask, url_for, render_template, request, jsonify, redirect
import requests
import qrcode
import pyodbc
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Azure SQL connection string
CONNECTION_STRING = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=sqlserverndibalekeralynette01.database.windows.net;"
    "Database=sqldbndibalekeralynette01;"
    "Uid=sqlserveradmin;"
    "Pwd=Password123;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

def get_user_id_from_db(username):
    """Fetch the user ID from the database based on the username."""
    try:
        # Connect to Azure SQL
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        # Query to fetch the user ID
        query = "SELECT user_id FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        # Close the connection
        cursor.close()
        conn.close()

        # Return the user ID if found
        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        print(f"Database error: {e}")
        return None

@app.route('/')
def home():
    return render_template('home.html')  # Render the home.html template

@app.route('/about')
def about():
    return render_template('about.html')  # Render the about page

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')  # Render the forgot password page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle form submission
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate the user (you can add your own validation logic here)
        user_id = get_user_id_from_db(username)
        if user_id:
            return redirect(url_for('profile', user_id=user_id))
        else:
            return "Invalid username or password. Please try again.", 401

    # Render the login page for GET requests
    return render_template('login.html')

@app.route('/profile/<int:user_id>')
def profile(user_id):
    # Fetch user data from the database (replace this with your actual database query logic)
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        # Query to fetch user details based on user_id
        query = "SELECT username, email, favorite_cuisines, dietary_restrictions FROM users WHERE user_id = ?"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        # Close the connection
        cursor.close()
        conn.close()

        if result:
            # Map the result to user data
            user_data = {
                "user_id": user_id,
                "username": result[0],
                "email": result[1],
                "favorite_cuisines": result[2].split(",") if result[2] else [],
                "dietary_restrictions": result[3].split(",") if result[3] else [],
            }
            return render_template('profile.html', user=user_data)
        else:
            return "User not found.", 404
    except Exception as e:
        print(f"Database error: {e}")
        return "An error occurred while fetching user data.", 500
   

@app.route('/register')
def register():
    return render_template('register.html')  # Render the register page


@app.route('/restaurants')
def restaurants():
    # Fetch restaurant data (replace this with your actual database or API logic)
    restaurants_data = [
        {"name": "Restaurant 1", "address": "123 Main St", "rating": 4.5},
        {"name": "Restaurant 2", "address": "456 Elm St", "rating": 4.0},
        {"name": "Restaurant 3", "address": "789 Oak St", "rating": 3.5},
    ]

    # Pass the data to the template
    return render_template('restaurants.html', restaurants=restaurants_data)


@app.route('/generate_qr')
def generate_qr():
    # Get the base URL dynamically
    app_url = url_for('home', _external=True)  # Dynamically fetch the app's base URL for the home page

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(app_url)
    qr.make(fit=True)

    # Create and save the QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("static/home_qr_code.png")  # Save the QR code as an image file

    return f"QR code generated for {app_url} and saved as 'home_qr_code.png'"

@app.route('/qr_code')
def qr_code():
    return app.send_static_file('home_qr_code.png')  # Serve the QR code image

if __name__ == '__main__':
    app.run(debug=True)
