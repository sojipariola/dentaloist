import pytest
import tempfile
import os

@pytest.fixture(scope='session')
def app():
    """Create application for testing without importing problematic models"""
    # Create temporary database
    db_fd, db_path = tempfile.mkstemp()
    
    class TestConfig:
        TESTING = True
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SECRET_KEY = 'test-secret'
        JWT_SECRET_KEY = 'test-jwt-secret'
        WTF_CSRF_ENABLED = False
    
    # Import here to avoid early import issues
    from app import create_app
    app = create_app(TestConfig)
    
    with app.app_context():
        from app.models import db
        # Drop all first to avoid index conflicts
        db.drop_all()
        db.create_all()
        yield app
        db.drop_all()
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def session(app):
    with app.app_context():
        from app.models import db
        connection = db.engine.connect()
        transaction = connection.begin()
        session = db.session
        yield session
        session.close()
        transaction.rollback()
        connection.close()
