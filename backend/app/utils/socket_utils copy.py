from flask_socketio import SocketIO

# Create socketio instance
# socketio = SocketIO()
socketio = SocketIO(cors_allowed_origins="*", async_mode="eventlet")


def get_socketio():
    from flask import current_app
    return socketio

def init_socketio(app):
    # ---- Initialize SocketIO with the app ----
    socketio.init_app(
        app,
        cors_allowed_origins=app.config.get("CORS_ORIGINS", ["http://localhost:3000"]),
        async_mode='eventlet',
        logger=True,
        engineio_logger=True
    )
    return socketio