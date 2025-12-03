"""
Flask-SocketIO Chat Server
Main application entry point

Phase 1-2: Basic WebSocket Connection and Echo Server
"""

import os
from app import create_app, socketio

# Get environment from environment variable
env = os.environ.get('FLASK_ENV', 'development')

# Create application instance
app = create_app(env)

if __name__ == '__main__':
    # Get host and port from config
    host = app.config['HOST']
    port = app.config['PORT']
    debug = app.config['DEBUG']

    # Print startup information
    print("=" * 60)
    print("Flask-SocketIO Chat Server")
    print("=" * 60)
    print(f"Environment: {env}")
    print(f"Debug Mode: {debug}")
    print(f"Server URL: http://{host}:{port}")
    print(f"API Endpoints: http://{host}:{port}/api")
    print(f"WebSocket: ws://{host}:{port}")
    print("=" * 60)
    print("Press CTRL+C to quit")
    print()

    # Run the application with SocketIO
    socketio.run(
        app,
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug,
        log_output=debug
    )
