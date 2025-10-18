
# backend/app/routes/__init__.py
# Import all route blueprints
# from .admin import admin_api_bp
from .analytics import analytics_bp
from .appointments import appointments_bp
from .audit import audit_bp
from .auth import auth_bp
from .billing import billing_bp
from .clinical import clinical_bp
from .dashboard import dashboard_bp
from .family_members import family_members_bp
from .files import files_bp
from .health import health_bp
from .insurance import insurance_bp
from .integrations import integrations_bp
from .inventory import inventory_bp
from .labs import labs_bp
from .notifications import notifications_bp
from .organizations import organizations_bp
from .patients import patients_bp
from .prescriptions import prescriptions_bp
from .reports import reports_bp
from .settings import settings_bp
from .telemedicine import telemedicine_bp
from .users import users_bp
from .web_auth import web_bp
from .widget import widget_api_bp
from .test_routes import test_bp

# from ..admin_api import admin_api
    

# Register all blueprints
def register_routes(app):
    # app.register_blueprint(admin_api_bp, url_prefix='/api/admin')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(appointments_bp, url_prefix='/api/appointments')
    app.register_blueprint(audit_bp, url_prefix='/api/audit')
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(billing_bp, url_prefix='/api/billing')
    app.register_blueprint(clinical_bp, url_prefix='/api/clinical')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(family_members_bp, url_prefix='/api/family_members')
    app.register_blueprint(files_bp, url_prefix='/api/files')
    app.register_blueprint(health_bp, url_prefix='/api/health')
    app.register_blueprint(insurance_bp, url_prefix='/api/insurance')
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    app.register_blueprint(labs_bp, url_prefix='/api/labs')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
    app.register_blueprint(organizations_bp, url_prefix='/api/organizations')
    app.register_blueprint(patients_bp, url_prefix='/api/patients')
    app.register_blueprint(prescriptions_bp, url_prefix='/api/prescriptions')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')
    app.register_blueprint(telemedicine_bp, url_prefix='/api/telemedicine')
    app.register_blueprint(integrations_bp, url_prefix='/api/integrations')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(web_bp)  # No prefix for web routes
    app.register_blueprint(widget_api_bp, url_prefix='/api/widget')
    app.register_blueprint(test_bp)    
    # app.register_blueprint(admin_api)
    
