from . import socketio

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.emit('connection_response', {'data': 'Connected to Flask server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('widget_event')
def handle_widget_event(data):
    print(f'Received widget event: {data}')
    response = {
        'status': 'success',
        'message': 'Widget event processed',
        'data': data,
        'timestamp': '2024-01-01T12:00:00Z'
    }
    socketio.emit('widget_response', response)

@socketio.on('widget_update')
def handle_widget_update(data):
    print(f'Widget update received: {data}')
    socketio.emit('widget_broadcast', data, broadcast=True)