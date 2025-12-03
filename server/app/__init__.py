"""
Flask-SocketIO Chat Application Factory
Creates and configures the Flask application with SocketIO support
"""

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from config import get_config
import logging

# Initialize SocketIO (will be bound to app in create_app)
socketio = SocketIO()


def create_app(config_name=None):
    """
    Application factory function

    Args:
        config_name: Configuration environment (development, testing, production)

    Returns:
        Flask application instance
    """
    # Create Flask app
    app = Flask(__name__)

    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    # Initialize extensions
    CORS(app, resources={r"/*": {"origins": app.config['CORS_ORIGINS']}})

    # Initialize SocketIO with the app
    socketio.init_app(
        app,
        cors_allowed_origins=app.config['SOCKETIO_CORS_ALLOWED_ORIGINS'],
        async_mode=app.config['SOCKETIO_ASYNC_MODE'],
        ping_timeout=app.config['SOCKETIO_PING_TIMEOUT'],
        ping_interval=app.config['SOCKETIO_PING_INTERVAL'],
        logger=app.config['DEBUG'],
        engineio_logger=app.config['DEBUG']
    )

    # Set up logging
    from app.utils.logger import setup_logging
    setup_logging(app)

    # Initialize database
    from app.services.db_service import init_db
    with app.app_context():
        init_db(app)

    # Register blueprints
    from app.routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Register SocketIO event handlers
    from app.events import socket_events
    socket_events.register_handlers(socketio)

    # Log startup information
    app.logger.info(f"Flask-SocketIO Chat Server initialized")
    app.logger.info(f"Environment: {config_name or 'development'}")
    app.logger.info(f"Debug mode: {app.config['DEBUG']}")

    return app
