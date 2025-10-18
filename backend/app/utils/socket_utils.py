from flask_socketio import SocketIO
import logging

logger = logging.getLogger(__name__)

# Create socketio instance
socketio = SocketIO()

def get_socketio():
    return socketio

def init_socketio(app):
    # Determine the best async mode
    async_mode = None
    try:
        import eventlet
        async_mode = 'eventlet'
        logger.info("Using eventlet for Socket.IO async mode")
    except ImportError:
        try:
            import gevent
            async_mode = 'gevent'
            logger.info("Using gevent for Socket.IO async mode")
        except ImportError:
            async_mode = 'threading'
            logger.warning("Using threading mode for Socket.IO. Install eventlet or gevent for better performance.")
    
    try:
        socketio.init_app(
            app,
            cors_allowed_origins=app.config.get("CORS_ORIGINS", ["http://localhost:3000"]),
            async_mode=async_mode,
            logger=app.debug,
            engineio_logger=app.debug
        )
        logger.info(f"Socket.IO initialized with async_mode: {async_mode}")
    except Exception as e:
        logger.error(f"Failed to initialize Socket.IO: {e}")
        # Fallback to threading mode
        socketio.init_app(
            app,
            cors_allowed_origins=app.config.get("CORS_ORIGINS", ["http://localhost:3000"]),
            async_mode='threading',
            logger=app.debug,
            engineio_logger=app.debug
        )
        logger.info("Socket.IO initialized with threading fallback mode")