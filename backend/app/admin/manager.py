# backend/app/admin/manager.py

from flask import url_for, current_app
from collections import defaultdict
import inspect as py_inspect
from sqlalchemy import inspect as db_inspect

class AdminManager:
    """Complete Admin Manager with route analysis and lookup table support"""
    
    def __init__(self, name='Admin', template_mode='bootstrap4', url='/admin', endpoint='admin'):
        self.name = name
        self.template_mode = template_mode
        self.url = url
        self.endpoint = endpoint
        self._views = {}
        self._menu = {}
        self._categories_order = []
        self._routes_analysis = {}
        self._lookup_tables = {}
    
    def analyze_app_routes(self, app):
        """Analyze all Flask routes in the application"""
        print("🔍 Analyzing application routes...")
        
        self._routes_analysis = {
            'routes': [],
            'endpoints_by_blueprint': defaultdict(list),
            'methods_by_route': defaultdict(list),
            'blueprints': set()
        }
        
        with app.test_request_context():
            for rule in app.url_map.iter_rules():
                if rule.endpoint != 'static':  # Skip static files
                    route_info = {
                        'endpoint': rule.endpoint,
                        'methods': sorted(list(rule.methods - {'HEAD', 'OPTIONS'})),
                        'path': rule.rule,
                        'blueprint': self._get_blueprint_from_endpoint(rule.endpoint),
                        'is_admin': rule.rule.startswith('/admin')
                    }
                    self._routes_analysis['routes'].append(route_info)
                    self._routes_analysis['endpoints_by_blueprint'][route_info['blueprint']].append(route_info)
                    self._routes_analysis['blueprints'].add(route_info['blueprint'])
                    
                    for method in route_info['methods']:
                        self._routes_analysis['methods_by_route'][method].append(route_info['path'])
        
        print(f"✅ Found {len(self._routes_analysis['routes'])} routes across {len(self._routes_analysis['blueprints'])} blueprints")
        return self._routes_analysis
    
    def _get_blueprint_from_endpoint(self, endpoint):
        """Extract blueprint name from endpoint"""
        if '.' in endpoint:
            return endpoint.split('.')[0]
        return 'main'
    
    def add_category(self, name, icon=None):
        """Add a category with optional icon"""
        if name not in self._menu:
            self._menu[name] = []
            if name not in self._categories_order:
                self._categories_order.append(name)
        return name
    
    def add_view(self, view, name=None, category=None):
        """Add a view to admin with proper category handling"""
        if name:
            view.name = name
        else:
            view.name = view.model.__name__
        
        # Use model_name for URL routing
        model_name = view.model.__name__.lower()
        self._views[model_name] = view
        
        # Use the provided category OR the view's category attribute OR default to Uncategorized
        category_name = category or getattr(view, 'category', None) or 'Uncategorized'
        
        # Ensure category exists
        self.add_category(category_name)
        
        # Create menu item with ALL required fields
        menu_item = {
            'name': view.name,
            'model_name': model_name,
            'view': view,
            'icon': self._get_icon_for_model(model_name),
            'is_lookup_table': self._is_lookup_table(view.model)
        }
        
        # Add to menu
        self._menu[category_name].append(menu_item)
        
        print(f"✅ Added admin view for {view.name} (model: {model_name}) in category {category_name}")
        return view
    
    def _is_lookup_table(self, model):
        """Check if a model is a lookup table"""
        lookup_indicators = ['status', 'type', 'category', 'lookup']
        table_name = model.__tablename__.lower() if hasattr(model, '__tablename__') else ''
        return any(indicator in table_name for indicator in lookup_indicators)
    
    def get_view(self, model_name):
        """Get view by model name"""
        model_name = model_name.rstrip('/').lower()
        
        # Try exact match first
        if model_name in self._views:
            return self._views[model_name]
        
        # Try partial match
        for key, view in self._views.items():
            if key in model_name or model_name in key:
                return view
        
        return None
    
    def _get_icon_for_model(self, model_name):
        """Get appropriate icons for different models"""
        icon_map = {
            # Lookup Tables
            'appointmentstatus': 'fa-calendar-check',
            'appointmenttype': 'fa-calendar-alt',
            'treatmentstatus': 'fa-teeth',
            'treatmenttype': 'fa-tooth',
            'invoicestatus': 'fa-file-invoice',
            'paymentstatus': 'fa-money-bill-wave',
            'paymentmethod': 'fa-credit-card',
            'gender': 'fa-venus-mars',
            'prioritylevel': 'fa-flag',
            'allergyseverity': 'fa-allergies',
            'medicationroute': 'fa-pills',
            
            # Main Models
            'user': 'fa-users',
            'organization': 'fa-building',
            'tenant': 'fa-database',
            'role': 'fa-user-tag',
            'staff': 'fa-user-md',
            'subscription': 'fa-credit-card',
            'patient': 'fa-user-injured',
            'appointment': 'fa-calendar-check',
            'treatment': 'fa-teeth',
            'treatmentplan': 'fa-clipboard-list',
            'clinicalnote': 'fa-file-medical',
            'allergy': 'fa-allergies',
            'prescription': 'fa-prescription',
            'vitalsign': 'fa-heartbeat',
            'invoice': 'fa-file-invoice',
            'payment': 'fa-money-bill-wave',
            'insuranceplan': 'fa-shield-alt',
            'insuranceclaim': 'fa-file-contract',
            'expense': 'fa-receipt',
            'financialreport': 'fa-chart-line',
            'product': 'fa-box',
            'productcategory': 'fa-tags',
            'supplier': 'fa-truck',
            'purchaseorder': 'fa-clipboard-check',
            'inventorytransaction': 'fa-exchange-alt',
            'notification': 'fa-bell',
            'audittrail': 'fa-history',
            'securityevent': 'fa-shield-alt',
            'loginattempt': 'fa-sign-in-alt',
            'familymember': 'fa-user-friends'
        }
        return icon_map.get(model_name, 'fa-table')
    
    def get_menu(self):
        """Get menu structure sorted by category order"""
        # Return menu in the order of categories_order
        sorted_menu = {}
        for category in self._categories_order:
            if category in self._menu and self._menu[category]:
                sorted_menu[category] = self._menu[category]
        
        # Add any remaining categories that have items
        for category, items in self._menu.items():
            if category not in sorted_menu and items:
                sorted_menu[category] = items
        
        return sorted_menu
    
    def get_routes_analysis(self):
        """Get comprehensive route analysis"""
        return self._routes_analysis
    
    def get_system_overview(self):
        """Get complete system overview for dashboard"""
        return {
            'total_models': len(self._views),
            'total_categories': len(self._menu),
            'total_routes': len(self._routes_analysis.get('routes', [])),
            'total_blueprints': len(self._routes_analysis.get('blueprints', set())),
            'lookup_tables_count': len([v for v in self._views.values() if self._is_lookup_table(v.model)]),
            'main_tables_count': len([v for v in self._views.values() if not self._is_lookup_table(v.model)])
        }

    def get_models(self):
        """Get all registered models"""
        return [view for view in self._views.values()]
    
    def get_categories(self):
        """Get all categories"""
        return list(self._menu.keys())
    
    def get_views_in_category(self, category):
        """Get all views in a specific category"""
        return self._menu.get(category, [])
    
    def get_all_model_names(self):
        """Get all registered model names"""
        return list(self._views.keys())
    
    def debug_menu_state(self):
        """Debug method to check menu state"""
        return {
            'total_views': len(self._views),
            'total_categories': len(self._menu),
            'categories': list(self._menu.keys()),
            'category_counts': {cat: len(items) for cat, items in self._menu.items()},
            'views_registered': list(self._views.keys())
        }
    
    def get_serializable_views(self):
        """Get views information with only serializable data"""
        serializable_views = {}
        
        for model_name, view in self._views.items():
            serializable_views[model_name] = {
                'name': getattr(view, 'name', 'Unknown'),
                'model_class': view.model.__name__,
                'category': getattr(view, 'category', 'Uncategorized'),
                'view_class': view.__class__.__name__,
                'can_create': getattr(view, 'can_create', True),
                'can_edit': getattr(view, 'can_edit', True),
                'can_delete': getattr(view, 'can_delete', True),
            }
        
        return serializable_views
    
    def get_serializable_views_info(self):
        """Get views information in serializable format"""
        views_info = {}
        
        for model_name, view in self._views.items():
            views_info[model_name] = {
                'name': getattr(view, 'name', 'Unknown'),
                'model_class': view.model.__name__,
                'view_class': view.__class__.__name__,
                'category': getattr(view, 'category', 'Uncategorized'),
                'endpoint': getattr(view, 'endpoint', model_name),
                'page_size': getattr(view, 'page_size', 50),
                'can_create': getattr(view, 'can_create', True),
                'can_edit': getattr(view, 'can_edit', True),
                'can_delete': getattr(view, 'can_delete', True),
                'can_export': getattr(view, 'can_export', True),
                'can_view_details': getattr(view, 'can_view_details', True),
            }
        
        return views_info
    
    def get_serializable_menu(self):
        """Get menu structure in serializable format"""
        menu = self.get_menu()
        serializable_menu = {}
        
        for category, items in menu.items():
            serializable_menu[category] = []
            for item in items:
                menu_item = {
                    'name': item.get('name', 'Unknown'),
                    'model_name': item.get('model_name', 'Unknown'),
                    'icon': item.get('icon', 'fa-table'),
                }
                # Don't include the view object itself
                if 'view' in item and item['view']:
                    menu_item['view_class'] = item['view'].__class__.__name__
                    menu_item['model_class'] = item['view'].model.__name__
                
                serializable_menu[category].append(menu_item)
        
        return serializable_menu


        



    def get_safe_menu(self):
        """Get menu structure with ONLY serializable data"""
        menu = self.get_menu()
        safe_menu = {}
        
        for category, items in menu.items():
            safe_menu[category] = []
            for item in items:
                # Create safe item with only basic data types
                safe_item = {
                    'name': str(item.get('name', 'Unknown')),
                    'model_name': str(item.get('model_name', 'Unknown')),
                    'icon': str(item.get('icon', 'fa-table')),
                    'is_lookup_table': item.get('is_lookup_table', False)
                }
                
                # Don't include the view object, just its metadata
                if 'view' in item and item['view']:
                    view = item['view']
                    safe_item['view_class'] = view.__class__.__name__
                    safe_item['can_create'] = getattr(view, 'can_create', True)
                    safe_item['can_edit'] = getattr(view, 'can_edit', True)
                    safe_item['can_delete'] = getattr(view, 'can_delete', True)
                
                safe_menu[category].append(safe_item)
        
        return safe_menu

# Create the global admin_manager instance
admin_manager = AdminManager(name='Dentaloist Admin')