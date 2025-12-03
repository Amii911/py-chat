"""
REST API Routes
HTTP endpoints for server status and health checks
"""

from flask import Blueprint, jsonify, current_app
from datetime import datetime
from app.events.socket_events import connected_clients

# Create Blueprint
api_bp = Blueprint('api', __name__)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    Returns server status and basic information

    Returns:
        JSON response with server health status
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Flask-SocketIO Chat Server'
    }), 200


@api_bp.route('/status', methods=['GET'])
def server_status():
    """
    Server status endpoint
    Returns detailed server information

    Returns:
        JSON response with server status details
    """
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'service': 'Flask-SocketIO Chat Server',
        'version': '1.0.0',
        'phase': '1-2: Basic WebSocket & Echo',
        'connected_clients': len(connected_clients),
        'debug_mode': current_app.config['DEBUG'],
        'database': current_app.config['DATABASE_PATH']
    }), 200


@api_bp.route('/clients', methods=['GET'])
def get_clients():
    """
    Get connected clients
    Returns list of currently connected clients

    Returns:
        JSON response with connected clients information
    """
    clients_info = []
    for client_id, client_data in connected_clients.items():
        clients_info.append({
            'client_id': client_id,
            'connected_at': client_data['connected_at'].isoformat()
        })

    return jsonify({
        'total_clients': len(connected_clients),
        'clients': clients_info,
        'timestamp': datetime.now().isoformat()
    }), 200


@api_bp.route('/', methods=['GET'])
def api_root():
    """
    API root endpoint
    Returns available endpoints

    Returns:
        JSON response with API information
    """
    return jsonify({
        'service': 'Flask-SocketIO Chat Server API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'status': '/api/status',
            'clients': '/api/clients'
        },
        'websocket': {
            'events': ['connect', 'disconnect', 'echo', 'message', 'ping', 'get_status']
        },
        'timestamp': datetime.now().isoformat()
    }), 200


@api_bp.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors

    Args:
        error: Error object

    Returns:
        JSON error response
    """
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
        'timestamp': datetime.now().isoformat()
    }), 404


@api_bp.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors

    Args:
        error: Error object

    Returns:
        JSON error response
    """
    current_app.logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred',
        'timestamp': datetime.now().isoformat()
    }), 500
