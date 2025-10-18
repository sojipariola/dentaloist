# tests/conftest.py

import pytest
import tempfile
import os
from app import create_app, db as _db
from app.models import get_models


@pytest.fixture(scope='session')
def app():
    """Create application for the tests."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    
    _app = create_app()
    _app.config['TESTING'] = True
    _app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    _app.config['WTF_CSRF_ENABLED'] = False
    
    with _app.app_context():
        yield _app
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='session')
def db(app):
    """Create database for the tests."""
    _db.app = app
    _db.create_all()
    
    yield _db
    
    _db.session.close()
    _db.drop_all()


@pytest.fixture(scope='function')
def session(db):
    """Create a new database session for a test."""
    # Create a nested transaction
    connection = db.engine.connect()
    transaction = connection.begin()
    
    # Use the connection for the session
    session = db._make_scoped_session(options={'bind': connection})
    db.session = session
    
    yield session
    
    # Cleanup
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()