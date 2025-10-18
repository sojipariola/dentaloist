import os
from app import db
from flask import current_app

def get_database_type():
    """Returns the type of database currently configured"""
    db_url = current_app.config.get('SQLALCHEMY_DATABASE_URI', '')
    
    if db_url.startswith('postgresql://'):
        return 'postgresql'
    elif db_url.startswith('sqlite://'):
        return 'sqlite'
    else:
        return 'unknown'

def is_postgresql():
    return get_database_type() == 'postgresql'

def is_sqlite():
    return get_database_type() == 'sqlite'

def get_database_name():
    """Extracts database name from connection string"""
    db_url = current_app.config.get('SQLALCHEMY_DATABASE_URI', '')
    
    if is_postgresql():
        # postgresql://user:pass@host:port/dbname
        return db_url.split('/')[-1].split('?')[0]
    elif is_sqlite():
        # sqlite:///path/to/database.db
        return db_url.split('/')[-1]
    return 'unknown'

def check_database_connection():
    """Test database connection"""
    try:
        db.session.execute('SELECT 1')
        return True, f"Connected to {get_database_type()} database: {get_database_name()}"
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"