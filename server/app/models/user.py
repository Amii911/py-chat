"""
User Model
Database model for user management (Phase 4+)

This module will be expanded in future phases to include:
- User registration and authentication
- Password hashing
- User profile management
- Online status tracking
"""

from app.services.db_service import execute_query
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User:
    """User model for future authentication phases"""

    @staticmethod
    def create_user(username, password):
        """
        Create a new user (Phase 4+)

        Args:
            username: User's username
            password: User's plaintext password

        Returns:
            User ID if successful, None otherwise
        """
        password_hash = generate_password_hash(password)

        query = """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        """

        try:
            user_id = execute_query(query, (username, password_hash))
            return user_id
        except Exception as e:
            # Handle duplicate username or other errors
            return None

    @staticmethod
    def get_user_by_username(username):
        """
        Get user by username

        Args:
            username: User's username

        Returns:
            User dict or None
        """
        query = "SELECT * FROM users WHERE username = ?"
        return execute_query(query, (username,), fetch_one=True)

    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID

        Args:
            user_id: User's ID

        Returns:
            User dict or None
        """
        query = "SELECT * FROM users WHERE id = ?"
        return execute_query(query, (user_id,), fetch_one=True)

    @staticmethod
    def verify_password(username, password):
        """
        Verify user password

        Args:
            username: User's username
            password: User's plaintext password

        Returns:
            User dict if valid, None otherwise
        """
        user = User.get_user_by_username(username)

        if user and check_password_hash(user['password_hash'], password):
            return user

        return None

    @staticmethod
    def update_last_seen(user_id):
        """
        Update user's last seen timestamp

        Args:
            user_id: User's ID
        """
        query = "UPDATE users SET last_seen = ? WHERE id = ?"
        execute_query(query, (datetime.now(), user_id))
