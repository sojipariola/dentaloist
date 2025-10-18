from flask import Blueprint

admin_bp = Blueprint('admin', __name__, 
                    url_prefix='/admin',
                    template_folder='templates',
                    static_folder='static')

@admin_bp.context_processor
def utility_processor():
    def get_first_item(dictionary):
        """Safely get first item from dictionary"""
        if dictionary and hasattr(dictionary, 'items'):
            items = list(dictionary.items())
            return items[0] if items else None
        return None
    
    def get_first_list_item(lst):
        """Safely get first item from list"""
        return lst[0] if lst and hasattr(lst, '__getitem__') else None
    
    return {
        'get_first_item': get_first_item,
        'get_first_list_item': get_first_list_item
    }

from app.admin import routes, views, auth