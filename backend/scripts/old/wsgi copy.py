import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import eventlet, but don't fail if it's not available
    import eventlet
    # Only monkey patch if we're running the WSGI server
    if 'WERKZEUG_RUN_MAIN' not in os.environ:
        eventlet.monkey_patch()
    use_eventlet = True
except ImportError:
    use_eventlet = False
    print("⚠️ Eventlet not available, using standard WSGI")

from app import create_app

app = create_app()

if __name__ == "__main__":
    if use_eventlet and os.environ.get('FLASK_ENV') == 'production':
        print("🚀 Starting production server with eventlet...")
        eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
    else:
        print("🚀 Starting development server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
