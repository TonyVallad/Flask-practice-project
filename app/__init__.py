from flask import Flask
from flask_cors import CORS
from .database import init_db
from .routes import main_bp

def create_app():
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object('config.Config')

    # Enable CORS
    CORS(app)

    # Initialize the database
    init_db()

    # Register blueprints (routes)
    app.register_blueprint(main_bp)

    return app
