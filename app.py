from flask import Flask, request, jsonify, g, render_template, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Path to your SQLite database
DATABASE = 'users.db'

# Function to connect to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Close the connection after each request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Helper function to query the database
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Route to add a new user via POST /users (API)
@app.route('/users', methods=['POST'])
def add_user():
    username = request.json['username']
    password = request.json['password']

    # Hash the password before saving
    hashed_password = generate_password_hash(password)

    db = get_db()
    db.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
               (username, hashed_password))
    db.commit()
    
    return jsonify({'message': 'User added successfully!'}), 201

# Route to retrieve users via GET /users (API)
@app.route('/users', methods=['GET'])
def get_users():
    users = query_db('SELECT id, username FROM users')
    users_list = [{'id': user[0], 'username': user[1]} for user in users]
    return jsonify(users_list), 200

# Route for index
@app.route('/')
def index():
    return render_template('index.html')

# Route to display the add user form (Web)
@app.route('/add_user', methods=['GET'])
def add_user_form():
    return render_template('add_user.html')

# Route to handle form submission and redirect to user list (Web)
@app.route('/add_user', methods=['POST'])
def add_user_web():
    username = request.form['username']
    password = request.form['password']

    hashed_password = generate_password_hash(password)

    db = get_db()
    db.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
               (username, hashed_password))
    db.commit()

    return redirect(url_for('list_users'))

# Route to display list of users (Web)
@app.route('/list_users', methods=['GET'])
def list_users():
    users = query_db('SELECT id, username FROM users')
    return render_template('list_users.html', users=users)

# Main block to run the app
if __name__ == '__main__':
    app.run(debug=True)
