from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .models import db  # Import SQLAlchemy instance from models.py
from .routes import main_bp

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('config.Config')

    # Initialize CORS
    CORS(app)

    # Initialize the database with the app
    db.init_app(app)

    # Register blueprints (routes)
    app.register_blueprint(main_bp)

    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
