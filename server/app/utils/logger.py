"""
Logging Configuration
Sets up structured logging for the application
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
import os


def setup_logging(app):
    """
    Configure application logging

    Args:
        app: Flask application instance
    """
    # Get log level from config
    log_level_str = app.config.get('LOG_LEVEL', 'INFO')
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)

    # Set Flask app logger level
    app.logger.setLevel(log_level)

    # Remove default handlers
    app.logger.handlers.clear()

    # Create formatters
    detailed_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(simple_formatter if app.config['DEBUG'] else detailed_formatter)
    app.logger.addHandler(console_handler)

    # File handler (if LOG_FILE is configured)
    log_file = app.config.get('LOG_FILE')
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(detailed_formatter)
        app.logger.addHandler(file_handler)

    # Prevent propagation to avoid duplicate logs
    app.logger.propagate = False

    app.logger.info("Logging configured successfully")


def get_logger(name):
    """
    Get a logger instance

    Args:
        name: Logger name (usually __name__)

    Returns:
        logging.Logger: Configured logger
    """
    return logging.getLogger(name)
