"""
Configuration module for Flask-SocketIO Chat Application
Supports multiple environments: development, testing, production
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class with common settings"""

    # Flask Core
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

    # Server
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))

    # CORS
    cors_env = os.environ.get('CORS_ORIGINS', '*')
    if cors_env == '*':
        CORS_ORIGINS = '*'
        SOCKETIO_CORS_ALLOWED_ORIGINS = '*'
    else:
        CORS_ORIGINS = cors_env.split(',')
        SOCKETIO_CORS_ALLOWED_ORIGINS = CORS_ORIGINS

    # SocketIO
    SOCKETIO_ASYNC_MODE = 'eventlet'
    SOCKETIO_PING_TIMEOUT = 60
    SOCKETIO_PING_INTERVAL = 25

    # Database
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'chat.db')

    # Session
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True

    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'server.log')


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DATABASE_PATH = ':memory:'  # Use in-memory database for tests
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production environment configuration"""
    # In production, SECRET_KEY must be set via environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")

    # Production-specific settings
    LOG_LEVEL = 'WARNING'
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
    if not CORS_ORIGINS or CORS_ORIGINS == ['']:
        raise ValueError("CORS_ORIGINS must be explicitly set in production")


# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env_name=None):
    """
    Get configuration object based on environment name

    Args:
        env_name: Environment name (development, testing, production)

    Returns:
        Configuration class
    """
    if env_name is None:
        env_name = os.environ.get('FLASK_ENV', 'development')

    return config_by_name.get(env_name, config_by_name['default'])
