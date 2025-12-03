# Flask-SocketIO Chat Server

Phase 1-2 implementation: Basic WebSocket Connection and Echo Server

## Project Structure

```
server/
├── app.py                      # Main application entry point
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── test_client.html           # HTML test client
├── app/
│   ├── __init__.py           # App factory
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py           # User model (for future phases)
│   ├── events/
│   │   ├── __init__.py
│   │   └── socket_events.py  # SocketIO event handlers
│   ├── routes/
│   │   ├── __init__.py
│   │   └── api.py            # REST API routes
│   ├── services/
│   │   ├── __init__.py
│   │   └── db_service.py     # Database service
│   └── utils/
│       ├── __init__.py
│       └── logger.py         # Logging configuration
└── .gitignore
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Navigate to server directory
cd server

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env if needed (optional for development)
```

### 4. Run the Server

```bash
# Run the server
python app.py
```

The server will start on `http://localhost:5000` by default.

## Testing the Server

### Option 1: HTML Test Client (Recommended)

1. Open `test_client.html` in your web browser
2. Ensure server URL is set to `http://localhost:5000`
3. Click "Connect" button
4. Try the different features:
   - **Ping**: Test connection health
   - **Get Status**: Get server status and client count
   - **Echo**: Send a message and receive it back
   - **Message**: Send a chat message

### Option 2: REST API Endpoints

Test with curl or browser:

```bash
# Health check
curl http://localhost:5000/api/health

# Server status
curl http://localhost:5000/api/status

# Connected clients
curl http://localhost:5000/api/clients

# API info
curl http://localhost:5000/api
```

### Option 3: Python SocketIO Client

```python
import socketio

# Create a Socket.IO client
sio = socketio.Client()

# Connect to server
sio.connect('http://localhost:5000')

# Send echo
sio.emit('echo', 'Hello, Server!')

# Send message
sio.emit('message', {'content': 'Test message'})

# Disconnect
sio.disconnect()
```

## Available SocketIO Events

### Client to Server

| Event        | Description          | Data Format                   |
| ------------ | -------------------- | ----------------------------- |
| `connect`    | Establish connection | (automatic)                   |
| `disconnect` | Close connection     | (automatic)                   |
| `echo`       | Echo test            | Any data                      |
| `message`    | Send chat message    | `{'content': 'message text'}` |
| `ping`       | Health check         | (no data)                     |
| `get_status` | Get server status    | (no data)                     |

### Server to Client

| Event                 | Description          | Data Format                                                        |
| --------------------- | -------------------- | ------------------------------------------------------------------ |
| `connection_response` | Connection confirmed | `{'status', 'client_id', 'message', 'timestamp'}`                  |
| `client_joined`       | New client connected | `{'client_id', 'total_clients', 'timestamp'}`                      |
| `client_left`         | Client disconnected  | `{'client_id', 'total_clients', 'timestamp'}`                      |
| `echo_response`       | Echo reply           | `{'original_data', 'client_id', 'timestamp'}`                      |
| `message_response`    | Message echo         | `{'content', 'sender_id', 'timestamp'}`                            |
| `pong`                | Ping reply           | `{'client_id', 'timestamp'}`                                       |
| `status_response`     | Status info          | `{'client_id', 'total_clients', 'connected_clients', 'timestamp'}` |
| `error`               | Error message        | `{'error', 'message', 'timestamp'}`                                |

## Configuration

### Environment Variables

Edit `.env` file or set environment variables:

| Variable        | Default          | Description                                  |
| --------------- | ---------------- | -------------------------------------------- |
| `FLASK_ENV`     | `development`    | Environment (development/testing/production) |
| `HOST`          | `0.0.0.0`        | Server host                                  |
| `PORT`          | `5000`           | Server port                                  |
| `SECRET_KEY`    | (auto-generated) | Flask secret key                             |
| `CORS_ORIGINS`  | `*`              | Allowed CORS origins                         |
| `DATABASE_PATH` | `chat.db`        | SQLite database path                         |
| `LOG_LEVEL`     | `DEBUG`          | Logging level                                |
| `LOG_FILE`      | `server.log`     | Log file path                                |

### Production Configuration

For production deployment:

1. Set `FLASK_ENV=production`
2. Set a strong `SECRET_KEY`
3. Configure specific `CORS_ORIGINS` (comma-separated)
4. Use a proper WSGI server (gunicorn + eventlet)

## Architecture

### App Factory Pattern

The application uses Flask's app factory pattern for better testability and flexibility:

- `create_app()` function creates and configures the Flask app
- Different configurations for development, testing, and production
- SocketIO initialized with the app instance

### Blueprints

- **API Blueprint** (`/api`): REST API endpoints for health checks and status

### Database

- SQLite database with tables for users, messages, and sessions
- Tables created on startup (ready for future phases)
- Raw SQL queries via `db_service.py`

### Logging

- Structured logging to console and file
- Different log levels for different environments
- Request/event logging for debugging

## Next Steps (Future Phases)

This implementation covers Phase 1-2. Future phases will add:

- **Phase 3**: Multi-client broadcasting (send messages to all clients)
- **Phase 4**: User identity (usernames, user tracking)
- **Phase 5**: Database integration (persist messages)
- **Phase 6**: Direct messaging (send to specific users)
- **Phase 7**: Conversation threads (group messages by conversation)
- **Phase 8**: Authentication (login/registration with Flask sessions)
- **Phase 9**: Polish (typing indicators, online status, reconnection)
- **Phase 10**: Deployment (production setup)

## Troubleshooting

### Connection refused

- Ensure server is running
- Check that port 5000 is not in use
- Verify firewall settings

### CORS errors

- Check `CORS_ORIGINS` in config
- For development, use `*` to allow all origins

### Database errors

- Ensure database directory is writable
- Check `DATABASE_PATH` in config

### Module import errors

- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
