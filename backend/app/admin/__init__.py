# backend/app/admin/__init__.py

from flask import url_for, Blueprint    
from app.admin.manager import admin_manager, AdminManager
from app.admin.views import BaseModelView, ModelView, UserModelView, PatientModelView, AppointmentModelView
from app.admin.routes import init_default_views, admin_bp
from app.admin.lookup_views import init_lookup_views
from app.admin.db_views import init_db_management_views
from app.models import db

def safe_url_for(endpoint, **values):
    """Safely generate URLs, returning '#' if endpoint doesn't exist"""
    try:
        return url_for(endpoint, **values)
    except Exception as e:
        print(f"URL generation error for {endpoint}: {e}")
        return '#'

@admin_bp.context_processor
def utility_processor():
    return {
        'safe_url_for': safe_url_for,
        'auth_logout_url': safe_url_for('auth.logout_route'),
        'get_model_count': get_model_count,
        'get_db_stats': get_db_stats
    }

def get_model_count(model_class):
    """Helper to get model count for templates"""
    try:
        return model_class.query.count()
    except:
        return 0

def get_db_stats():
    """Get database statistics for templates"""
    try:
        from sqlalchemy import inspect, text
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        stats = {
            'total_tables': len(tables),
            'total_records': 0,
            'table_counts': {}
        }
        
        # Get record counts for key tables
        key_tables = ['users', 'patients', 'appointments', 'treatments', 'organizations']
        for table in key_tables:
            if table in tables:
                try:
                    count = db.session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                    stats['table_counts'][table] = count
                    stats['total_records'] += count
                except:
                    stats['table_counts'][table] = 0
        
        return stats
    except:
        return {'total_tables': 0, 'total_records': 0, 'table_counts': {}}

# Import all admin modules
from app.admin import routes, views, auth, lookup_views, db_views

def init_admin(app):
    """Initialize the complete admin system"""
    # Register blueprint
    app.register_blueprint(admin_bp)
    
    # Initialize all views
    with app.app_context():
        init_default_views()
        init_lookup_views()
        init_db_management_views()
    
    print("✅ Complete Dentaloist Admin System Initialized")
    print("✅ Database Tables: All models + lookup tables")
    print("✅ Database Management: CLI integration")
    print("✅ Available at: /admin")
    
    return admin_manager