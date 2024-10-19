from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash
from .database import get_db, query_db

# Create a Blueprint for your routes
main_bp = Blueprint('main', __name__)

# =====================
# Form Routes
# =====================

# Homepage route (for the web interface)
@main_bp.route('/')
def index():
    return render_template('index.html')

# Route to render the 'add user' form page
@main_bp.route('/add_user', methods=['GET'])
def add_user_form():
    return render_template('add_user.html')

# Route to handle form submission and add user
@main_bp.route('/add_user', methods=['POST'])
def add_user_form_submit():
    # Get the data from the form
    username = request.form['username']
    password = request.form['password']
    
    # Hash the password
    hashed_password = generate_password_hash(password)

    # Insert user into the database
    db = get_db()
    db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    db.commit()

    # Redirect to the list_users page after successfully adding a user
    return redirect(url_for('main.list_users'))

# Route to render the user list page (for the web interface)
@main_bp.route('/list_users', methods=['GET'])
def list_users():
    users = query_db('SELECT id, username FROM users')
    return render_template('list_users.html', users=users)


# =====================
# API Routes
# =====================

# API route to add a user via JSON
@main_bp.route('/api/users', methods=['POST'])
def api_add_user():
    # Check if the request is JSON
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert user into the database
        db = get_db()
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        db.commit()

        return jsonify({'message': 'User added successfully!'}), 201
    else:
        return jsonify({'error': 'Invalid request format, must be JSON'}), 400

# API route to get the list of users in JSON format
@main_bp.route('/api/users', methods=['GET'])
def api_get_users():
    users = query_db('SELECT id, username FROM users')
    users_list = [{'id': user[0], 'username': user[1]} for user in users]
    return jsonify(users_list), 200
