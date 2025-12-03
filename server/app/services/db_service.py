"""
Database Service
Handles SQLite database initialization and connection management
"""

import sqlite3
import os
from flask import g, current_app


def get_db():
    """
    Get database connection for current request context

    Returns:
        sqlite3.Connection: Database connection
    """
    if 'db' not in g:
        db_path = current_app.config['DATABASE_PATH']

        # Create database directory if it doesn't exist
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Close database connection at end of request

    Args:
        e: Exception if any
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db(app):
    """
    Initialize database tables

    Args:
        app: Flask application instance
    """
    # Register close_db to be called when request context ends
    app.teardown_appcontext(close_db)

    db_path = app.config['DATABASE_PATH']

    # Skip initialization for in-memory databases in testing
    if db_path == ':memory:':
        return

    # Create database directory if it doesn't exist
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables for future phases
    # Users table (Phase 4 and beyond)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Messages table (Phase 5 and beyond)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            recipient_id INTEGER,
            content TEXT NOT NULL,
            conversation_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users (id),
            FOREIGN KEY (recipient_id) REFERENCES users (id)
        )
    ''')

    # Sessions table (for future use)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id TEXT UNIQUE NOT NULL,
            socket_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

    app.logger.info(f"Database initialized at {db_path}")


def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Execute a database query

    Args:
        query: SQL query string
        params: Query parameters (tuple or dict)
        fetch_one: Return single row
        fetch_all: Return all rows

    Returns:
        Query results or None
    """
    db = get_db()
    cursor = db.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    if fetch_one:
        result = cursor.fetchone()
        return dict(result) if result else None
    elif fetch_all:
        results = cursor.fetchall()
        return [dict(row) for row in results]
    else:
        db.commit()
        return cursor.lastrowid
