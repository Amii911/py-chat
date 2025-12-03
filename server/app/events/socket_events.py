"""
SocketIO Event Handlers
Handles WebSocket events for chat functionality

Phase 1-2: Basic WebSocket Connection and Echo Server
"""

from flask import request
from flask_socketio import emit, join_room, leave_room
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Store connected clients (in-memory for Phase 1-2)
# Structure: {session_id: {'socket_id': str, 'connected_at': datetime}}
connected_clients = {}


def register_handlers(socketio):
    """
    Register all SocketIO event handlers

    Args:
        socketio: SocketIO instance
    """

    @socketio.on('connect')
    def handle_connect():
        """
        Handle client connection (Phase 1)
        Triggered when a client establishes WebSocket connection
        """
        client_id = request.sid
        connected_clients[client_id] = {
            'socket_id': client_id,
            'connected_at': datetime.now()
        }

        logger.info(f"Client connected: {client_id}")
        logger.debug(f"Total connected clients: {len(connected_clients)}")

        # Send connection confirmation to client
        emit('connection_response', {
            'status': 'connected',
            'client_id': client_id,
            'message': 'Successfully connected to chat server',
            'timestamp': datetime.now().isoformat()
        })

        # Broadcast to all other clients that someone joined
        emit('client_joined', {
            'client_id': client_id,
            'total_clients': len(connected_clients),
            'timestamp': datetime.now().isoformat()
        }, broadcast=True, include_self=False)


    @socketio.on('disconnect')
    def handle_disconnect():
        """
        Handle client disconnection
        Triggered when a client closes WebSocket connection
        """
        client_id = request.sid

        if client_id in connected_clients:
            del connected_clients[client_id]
            logger.info(f"Client disconnected: {client_id}")
            logger.debug(f"Remaining connected clients: {len(connected_clients)}")

            # Broadcast to all clients that someone left
            emit('client_left', {
                'client_id': client_id,
                'total_clients': len(connected_clients),
                'timestamp': datetime.now().isoformat()
            }, broadcast=True)
        else:
            logger.warning(f"Disconnect from unknown client: {client_id}")


    @socketio.on('echo')
    def handle_echo(data):
        """
        Handle echo messages (Phase 2)
        Echoes back exactly what the client sends

        Args:
            data: Message data from client
        """
        client_id = request.sid
        logger.debug(f"Echo request from {client_id}: {data}")

        # Echo back to the sender
        emit('echo_response', {
            'original_data': data,
            'client_id': client_id,
            'timestamp': datetime.now().isoformat()
        })


    @socketio.on('message')
    def handle_message(data):
        """
        Handle chat messages (Phase 2+)
        Receives message and echoes it back for now
        In future phases, this will broadcast to other clients

        Args:
            data: Message data (expected to be dict with 'content' key)
        """
        client_id = request.sid
        logger.info(f"Message from {client_id}: {data}")

        # Validate message data
        if not isinstance(data, dict):
            emit('error', {
                'error': 'Invalid message format',
                'message': 'Message must be a JSON object',
                'timestamp': datetime.now().isoformat()
            })
            return

        content = data.get('content', '')

        if not content:
            emit('error', {
                'error': 'Empty message',
                'message': 'Message content cannot be empty',
                'timestamp': datetime.now().isoformat()
            })
            return

        # Echo message back to sender (Phase 2 behavior)
        emit('message_response', {
            'content': content,
            'sender_id': client_id,
            'timestamp': datetime.now().isoformat()
        })


    @socketio.on('ping')
    def handle_ping():
        """
        Handle ping requests for connection health check

        Responds with pong
        """
        client_id = request.sid
        logger.debug(f"Ping from {client_id}")

        emit('pong', {
            'client_id': client_id,
            'timestamp': datetime.now().isoformat()
        })


    @socketio.on('get_status')
    def handle_get_status():
        """
        Handle status request
        Returns server and connection status
        """
        client_id = request.sid

        emit('status_response', {
            'client_id': client_id,
            'total_clients': len(connected_clients),
            'connected_clients': list(connected_clients.keys()),
            'timestamp': datetime.now().isoformat()
        })


    @socketio.on_error_default
    def default_error_handler(e):
        """
        Default error handler for unhandled exceptions in event handlers

        Args:
            e: Exception
        """
        client_id = request.sid
        logger.error(f"SocketIO error from {client_id}: {str(e)}", exc_info=True)

        emit('error', {
            'error': 'Server error',
            'message': 'An unexpected error occurred',
            'timestamp': datetime.now().isoformat()
        })


    logger.info("SocketIO event handlers registered")
