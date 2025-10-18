import os
import sys
import pytest
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add backend to Python path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

# Load test environment variables
load_dotenv('.env.test')

@pytest.fixture(scope='session')
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='session')
def backend_url():
    """Backend API URL for testing"""
    return os.getenv('TEST_BACKEND_URL', 'http://localhost:5000')

@pytest.fixture(scope='session') 
def frontend_url():
    """Frontend URL for testing"""
    return os.getenv('TEST_FRONTEND_URL', 'http://localhost:3000')

@pytest.fixture(scope='session')
def test_credentials():
    """Test user credentials"""
    return {
        'super_admin': {
            'email': 'sojipariola@gmail.com',
            'password': 'Soji1111'
        },
        'practice_admin': {
            'email': 'admin@brightsmile.com', 
            'password': 'test123'
        }
    }

@pytest.fixture(scope='session')
def test_tenants():
    """Test tenant data"""
    return {
        'bright_smile': 'org_001',
        'perfect_teeth': 'org_002', 
        'family_dental': 'org_003'
    }