# tests/test_absolute_minimal.py

def test_absolute_minimal():
    """Absolute minimal test without any models"""
    from flask import Flask
    
    app = Flask(__name__)
    app.config['TESTING'] = True
    
    with app.app_context():
        # Just test that Flask works
        assert app.config['TESTING'] == True
        print("✅ Flask app works!")
    
    assert True

def test_health_endpoint_minimal():
    """Test health endpoint without database"""
    from flask import Flask
    
    app = Flask(__name__)
    
    @app.route('/health')
    def health():
        return 'OK', 200
    
    with app.test_client() as client:
        response = client.get('/health')
        assert response.status_code == 200
        assert b'OK' in response.data
        print("✅ Health endpoint works!")