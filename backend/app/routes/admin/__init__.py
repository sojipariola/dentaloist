from flask import Blueprint

admin_bp = Blueprint('admin', __name__, 
                    url_prefix='/admin',
                    template_folder='templates',
                    static_folder='static')

from app.admin import routes, views, auth