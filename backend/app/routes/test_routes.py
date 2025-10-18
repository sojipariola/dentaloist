# app/routes/test_routes.py
from flask import Blueprint, jsonify, request
from datetime import datetime

test_bp = Blueprint("test", __name__)

@test_bp.route("/api/test-cors1", methods=["GET"])
def test_cors1():
    return jsonify({"message": "CORS is fully working!"}), 200

@test_bp.route('/api/test-cors2', methods=['GET', 'OPTIONS'])
def test_cors2():
    if request.method == 'OPTIONS':
        return '', 200
    
    return {
        'message': 'CORS is working!',
        'origin': request.headers.get('Origin'),
        'authorization': request.headers.get('Authorization'),
        'cors_headers': {
            'access_control_allow_origin': request.headers.get('Access-Control-Allow-Origin'),
            'access_control_allow_credentials': request.headers.get('Access-Control-Allow-Credentials')
        }
    }

@test_bp.route('/api/test-cors', methods=['GET', 'POST', 'OPTIONS'])
def test_cors():
    """
    Test endpoint for CORS verification - bypasses tenancy for testing
    """
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'message': 'Preflight OK'})
        return response
    
    # Check headers for debugging
    headers_info = {
        'origin': request.headers.get('Origin'),
        'authorization': request.headers.get('Authorization'),
        'content_type': request.headers.get('Content-Type'),
        'user_agent': request.headers.get('User-Agent')
    }
    
    return jsonify({
        'message': 'CORS test successful!',
        'headers_received': headers_info,
        'method': request.method,
        'cors_status': 'Working',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


'''
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Authorization" \
     -X OPTIONS --verbose http://localhost:5000/api/test-cors



curl -H "Origin: http://localhost:3000" \
     -H "Authorization: Bearer fake-token" \
     --verbose http://localhost:5000/api/test-cors


# Test GET with Authorization header
curl -H "Origin: http://localhost:3000" \
     -H "Authorization: Bearer test-token-123" \
     -X GET http://localhost:5000/api/test-cors

# Test POST with data
curl -H "Origin: http://localhost:3000" \
     -H "Authorization: Bearer test-token-123" \
     -H "Content-Type: application/json" \
     -X POST \
     -d '{"test": "data"}' \
     http://localhost:5000/api/test-cors
     


curl -H "Origin: http://localhost:3000" \
     -H "Authorization: Bearer your-actual-token" \
     -H "X-Tenant-ID: default" \
     -X GET http://localhost:5000/api/test-cors

curl -X POST http://localhost:5000/api/auth/login   -H "Content-Type: application/json"   -H "Origin: http://localhost:3000"   -d '{
    "email": "sojipariola@gmail.com",
    "password": "Soji1111"
  }'   -v






// Nuclear option - clear everything
localStorage.clear()
sessionStorage.clear()
indexedDB.deleteDatabase('auth-storage')
window.location.href = '/'



localStorage.clear()
sessionStorage.clear()
window.location.reload()

'''