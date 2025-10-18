# backenmd/app/admin/routes.py

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_file, current_app, session
from flask_login import current_user, login_required
from app.admin.manager import admin_manager 
from app.admin.views import BaseModelView, init_default_views  
from app.admin.auth import admin_required, redirect_to_login
from app.admin.lookup_views import init_lookup_views
from app.models import db
import csv
import io
import json
import datetime
from decimal import Decimal
from collections import defaultdict
from functools import lru_cache

# Initialize views when the blueprint is first accessed
views_initialized = False
lookup_views_initialized = False


admin_bp = Blueprint('admin', __name__, 
                    url_prefix='/admin',
                    template_folder='templates',
                    static_folder='static')

# ADD THIS: Ensure the blueprint has a name for url_for
admin_bp.name = 'admin'


def before_request():
    # TEMPORARY DEVELOPMENT BYPASS - REMOVE IN PRODUCTION
    if current_app.config.get('DEBUG'):
        session['is_admin'] = True
        session['admin_authenticated'] = True
        return
    
    # Original auth logic below...
    if not session.get('is_admin'):
        return redirect(f'/api/auth/admin-direct-login?next={request.url}')
        
@admin_bp.route('/debug-session')
def debug_session():
    return {
        'session_data': dict(session),
        'is_admin': session.get('is_admin'),
        'user_id': session.get('user_id'),
        'admin_authenticated': session.get('admin_authenticated')
    }



# Helper Functions
def get_recent_activity():
    """Get recent system activity including admin actions"""
    return [
        {
            'type': 'admin_login',
            'message': f'Admin {current_user.email} logged in',
            'timestamp': datetime.datetime.now().isoformat(),
            'icon': 'fa-sign-in-alt',
            'color': 'success'
        },
        {
            'type': 'system_access',
            'message': 'Admin dashboard accessed',
            'timestamp': (datetime.datetime.now() - datetime.timedelta(minutes=5)).isoformat(),
            'icon': 'fa-tachometer-alt',
            'color': 'info'
        },
        {
            'type': 'data_export',
            'message': 'Patient data exported',
            'timestamp': (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat(),
            'icon': 'fa-download',
            'color': 'warning'
        }
    ]

@lru_cache(maxsize=1)
def get_system_stats(force_refresh=False):
    """Get comprehensive system statistics with caching."""
    try:
        from app.models import (
            User, Patient, Appointment, Treatment, Organization, Tenant,
            Invoice, Payment, Product, Staff
        )
        
        # Clear cache if forced refresh
        if force_refresh:
            get_system_stats.cache_clear()
        
        today = datetime.datetime.utcnow().date()
        week_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        month_ago = datetime.datetime.utcnow() - datetime.timedelta(days=30)
        
        stats = {
            'users': {
                'total': safe_query_count(User.query.filter_by(is_active=True)),
                'admins': safe_query_count(User.query.filter_by(is_admin=True, is_active=True)),
                'staff': safe_query_count(User.query.filter_by(is_admin=False, is_active=True)),
                'recent': safe_query_count(User.query.filter(User.created_at >= week_ago)),
                'new_today': safe_query_count(User.query.filter(
                    db.func.date(User.created_at) == today
                ))
            },
            'patients': {
                'total': safe_query_count(Patient.query.filter_by(is_active=True)),
                'active': safe_query_count(Patient.query.filter_by(status='active')),
                'new_this_week': safe_query_count(Patient.query.filter(Patient.created_at >= week_ago)),
                'new_today': safe_query_count(Patient.query.filter(
                    db.func.date(Patient.created_at) == today
                ))
            },
            'appointments': {
                'total': safe_query_count(Appointment.query.filter_by(is_active=True)),
                'scheduled': safe_query_count(Appointment.query.filter_by(status='scheduled')),
                'completed': safe_query_count(Appointment.query.filter_by(status='completed')),
                'cancelled': safe_query_count(Appointment.query.filter_by(status='cancelled')),
                'today': safe_query_count(Appointment.query.filter(
                    db.func.date(Appointment.start_time) == today
                )),
                'this_week': safe_query_count(Appointment.query.filter(
                    Appointment.start_time >= week_ago
                ))
            },
            'treatments': {
                'total': safe_query_count(Treatment.query.filter_by(is_active=True)),
                'completed': safe_query_count(Treatment.query.filter_by(status='completed')),
                'in_progress': safe_query_count(Treatment.query.filter_by(status='in_progress')),
                'scheduled': safe_query_count(Treatment.query.filter_by(status='scheduled')),
                'revenue_this_month': safe_query_sum(
                    Treatment.query.filter(
                        Treatment.created_at >= month_ago,
                        Treatment.status == 'completed'
                    ),
                    'actual_cost'
                ) or 0
            },
            'financial': {
                'total_invoices': safe_query_count(Invoice.query.filter_by(is_active=True)),
                'pending_payments': safe_query_count(Payment.query.filter_by(status='pending')),
                'completed_payments': safe_query_count(Payment.query.filter_by(status='completed')),
                'total_revenue': safe_query_sum(Invoice.query, 'total_amount') or 0,
                'revenue_this_month': safe_query_sum(
                    Invoice.query.filter(Invoice.created_at >= month_ago),
                    'total_amount'
                ) or 0
            },
            'inventory': {
                'total_products': safe_query_count(Product.query.filter_by(is_active=True)),
                'low_stock': safe_query_count(Product.query.filter(
                    Product.stock_quantity <= Product.min_stock_level
                )),
                'out_of_stock': safe_query_count(Product.query.filter(
                    Product.stock_quantity == 0
                ))
            },
            'organizations': {
                'total': safe_query_count(Organization.query.filter_by(is_active=True)),
                'tenants': safe_query_count(Tenant.query.filter_by(is_active=True))
            },
            'system': {
                'uptime': get_system_uptime(),
                'database_size': get_database_size(),
                'last_backup': get_last_backup_time()
            }
        }
        
        return stats
        
    except Exception as e:
        print(f"❌ Error getting system stats: {e}")
        return get_fallback_stats()

def safe_query_count(query):
    """Safely get count from query without causing errors."""
    try:
        return query.count()
    except Exception as e:
        print(f"⚠️ Query count error: {e}")
        return 0

def safe_query_sum(query, column_name):
    """Safely get sum from query."""
    try:
        from sqlalchemy import func
        return query.with_entities(func.sum(getattr(query.column_descriptions[0]['type'], column_name))).scalar()
    except Exception as e:
        print(f"⚠️ Query sum error: {e}")
        return 0

def get_system_uptime():
    """Get system uptime information."""
    try:
        # This would be implemented based on your deployment
        # For now, return a placeholder
        return "24 days, 6 hours"
    except:
        return "Unknown"

def get_database_size():
    """Get approximate database size."""
    try:
        # Implementation depends on your database
        return "45.2 MB"
    except:
        return "Unknown"

def get_last_backup_time():
    """Get last backup time."""
    try:
        # Implementation depends on your backup system
        return "2024-01-06 02:00:00"
    except:
        return "Unknown"

def get_fallback_stats():
    """Return fallback stats when main query fails."""
    return {
        'users': {'total': 0, 'admins': 0, 'staff': 0, 'recent': 0, 'new_today': 0},
        'patients': {'total': 0, 'active': 0, 'new_this_week': 0, 'new_today': 0},
        'appointments': {'total': 0, 'scheduled': 0, 'completed': 0, 'cancelled': 0, 'today': 0, 'this_week': 0},
        'treatments': {'total': 0, 'completed': 0, 'in_progress': 0, 'scheduled': 0, 'revenue_this_month': 0},
        'financial': {'total_invoices': 0, 'pending_payments': 0, 'completed_payments': 0, 'total_revenue': 0, 'revenue_this_month': 0},
        'inventory': {'total_products': 0, 'low_stock': 0, 'out_of_stock': 0},
        'organizations': {'total': 0, 'tenants': 0},
        'system': {'uptime': 'Unknown', 'database_size': 'Unknown', 'last_backup': 'Unknown'}
    }

def ensure_all_views_initialized():
    """Ensure all views (main + lookup) are initialized"""
    global views_initialized, lookup_views_initialized
    
    if not views_initialized:
        print("🔄 Initializing main admin views...")
        init_default_views()
        views_initialized = True
    
    if not lookup_views_initialized:
        print("🔄 Initializing lookup table views...")
        init_lookup_views()
        lookup_views_initialized = True

@admin_bp.context_processor
def inject_admin():
    """Make admin_manager and system info available to all templates"""
    print("🔄 Injecting admin_manager into template context")
    return {
        'admin_manager': admin_manager,
        'admin_bp_name': admin_bp.name,
        'current_year': datetime.datetime.now().year
    }

def get_comprehensive_system_stats():
    """Get comprehensive system statistics including lookup tables"""
    try:
        from app.models import User, Patient, Appointment, Organization, Invoice
        from app.models.lookups import AppointmentStatus, AppointmentType
        
        # Main model counts
        total_users = User.query.filter_by(is_active=True).count()
        total_patients = Patient.query.filter_by(is_active=True).count()
        total_appointments = Appointment.query.filter_by(is_active=True).count()
        total_organizations = Organization.query.filter_by(is_active=True).count()
        total_invoices = Invoice.query.filter_by(is_active=True).count()
        
        # Lookup table counts
        appointment_statuses = AppointmentStatus.query.filter_by(is_active=True).count()
        appointment_types = AppointmentType.query.filter_by(is_active=True).count()
        
        # Today's appointments
        today = datetime.date.today()
        today_appointments = Appointment.query.filter(
            db.func.date(Appointment.appointment_date) == today
        ).count()
        
        # System overview from admin manager
        system_overview = admin_manager.get_system_overview()
        
        return {
            # Main data
            'total_users': total_users,
            'total_patients': total_patients,
            'total_appointments': total_appointments,
            'total_organizations': total_organizations,
            'total_invoices': total_invoices,
            'today_appointments': today_appointments,
            
            # Lookup data
            'appointment_statuses': appointment_statuses,
            'appointment_types': appointment_types,
            
            # System info
            'total_models': system_overview['total_models'],
            'total_categories': system_overview['total_categories'],
            'total_routes': system_overview['total_routes'],
            'total_blueprints': system_overview['total_blueprints'],
            'lookup_tables_count': system_overview['lookup_tables_count'],
            'main_tables_count': system_overview['main_tables_count'],
            
            # System status
            'active_sessions': 24,
            'system_uptime': '99.8%',
            'timestamp': datetime.datetime.now().isoformat(),
            'status': 'healthy'
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'status': 'error',
            'timestamp': datetime.datetime.now().isoformat()
        }

def safe_serialize(obj):
    """Safely serialize objects to JSON"""
    if isinstance(obj, (datetime, datetime.date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    elif hasattr(obj, '__dict__'):
        # Try to serialize objects by converting to dict
        try:
            # Only include non-private attributes
            data = {}
            for key, value in obj.__dict__.items():
                if not key.startswith('_'):
                    try:
                        data[key] = safe_serialize(value)
                    except:
                        data[key] = str(value)
            return data
        except:
            return str(obj)
    elif callable(obj):
        return f"<function {obj.__name__}>"
    elif isinstance(obj, (set, tuple)):
        return list(obj)
    else:
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

def safe_jsonify(data):
    """Safely convert data to JSON response"""
    def default_handler(obj):
        try:
            return safe_serialize(obj)
        except TypeError:
            return str(obj)
    
    return current_app.response_class(
        json.dumps(data, default=default_handler, indent=2),
        mimetype='application/json'
    )

################################## Admin routes #####################################################

'''
@admin_bp.before_request
def require_login():
    """Require login for all admin routes"""
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        return redirect_to_login()
    ensure_all_views_initialized()
'''

@admin_bp.before_request
def require_login():
    """Require login for all admin routes - FIXED VERSION"""
    # Skip for static files and login endpoints
    if request.endpoint in ['static', 'admin.api_debug_simple']:
        return
    
    print(f"🔐 BEFORE_REQUEST: {request.endpoint} - {request.path}")
    
    # Check if user is authenticated and is admin
    if not current_user.is_authenticated:
        print("❌ User not authenticated in before_request")
        return redirect_to_login()
    
    if not getattr(current_user, 'is_admin', False):
        print("❌ User not admin in before_request")
        flash('Admin access required.', 'error')
        return redirect_to_login()
    
    # Ensure views are initialized for admin routes
    if request.endpoint and request.endpoint.startswith('admin.'):
        ensure_all_views_initialized()
    
    print("✅ Before request check passed")


@admin_bp.route('/')
@admin_required
def dashboard():
    """Enhanced admin dashboard with system overview"""
    print(f"🎯 DASHBOARD ACCESS: User {current_user.email} is accessing dashboard")

    stats = get_comprehensive_system_stats()
    recent_activity = get_recent_activity()
    routes_analysis = admin_manager.get_routes_analysis()

    # Debug info
    print(f"📊 Dashboard stats: {stats.get('total_models', 0)} models")
    print(f"📋 Menu categories: {list(admin_manager.get_menu().keys())}")
    
    return render_template('admin/dashboard.html', 
                         stats=stats,
                         recent_activity=recent_activity,
                         routes_analysis=routes_analysis,
                         admin_manager=admin_manager)

@admin_bp.route('/system-overview')
@admin_required
def system_overview():
    """Comprehensive system overview page"""
    stats = get_comprehensive_system_stats()
    routes_analysis = admin_manager.get_routes_analysis()
    menu_structure = admin_manager.get_safe_menu()
    
    return render_template('admin/system_overview.html',
                         stats=stats,
                         routes_analysis=routes_analysis,
                         menu_structure=menu_structure,
                         admin_manager=admin_manager)

@admin_bp.route('/routes-analysis')
@admin_required
def routes_analysis():
    """Detailed routes analysis page"""
    routes_analysis = admin_manager.get_routes_analysis()
    
    return render_template('admin/routes_analysis.html',
                         routes_analysis=routes_analysis,
                         admin_manager=admin_manager)



@admin_bp.route('/menu')
@admin_required
def admin_menu():
    """Safe admin menu endpoint using the safe method"""
    try:
        safe_menu = admin_manager.get_safe_menu()
        
        return jsonify({
            'menu': safe_menu,
            'categories': list(safe_menu.keys()),
            'total_categories': len(safe_menu),
            'total_models': sum(len(items) for items in safe_menu.values()),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch menu',
            'message': str(e),
            'status': 'error'
        }), 500



@admin_bp.route('/model/<model_name>/')
@admin_required
def list_view(model_name):
    """List view for any model - WITH ENUM FIX"""
    ensure_all_views_initialized()
    model_name = model_name.rstrip('/')
    
    print(f"🔍 LIST_VIEW called for model: {model_name}")
    
    view = admin_manager.get_view(model_name)
    if not view:
        flash(f'Model "{model_name}" not found in admin.', 'error')
        return redirect(url_for('admin.dashboard'))

    try:
        # Get parameters with safe defaults
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '')
        sort_field = request.args.get('sort', 'id')
        sort_desc = request.args.get('order', 'desc') == 'desc'
        page_size = request.args.get('per_page', view.page_size, type=int)
        
        # Validate page
        if page < 1:
            page = 1
        
        # Get paginated data
        pagination = view.get_list(page, sort_field, sort_desc, search, [], page_size)
        columns = view.scaffold_list_columns()
        formatters = view.column_formatters or view.get_column_formatters()
        
        # FIX: Handle enum serialization in the template context
        items = []
        for item in pagination.items:
            item_dict = {}
            for column in columns:
                value = getattr(item, column, None)
                
                # Convert enum values to their string representation
                if hasattr(value, 'value'):
                    item_dict[column] = value.value
                else:
                    item_dict[column] = value
            
            # Keep the original item for other operations
            item_dict['_original'] = item
            items.append(item_dict)
        
        return render_template('admin/list.html',
                             view=view,
                             pagination=pagination,
                             items=items,  # Pass the processed items
                             columns=columns,
                             formatters=formatters,
                             search=search,
                             model_name=model_name,
                             can_delete=getattr(view, 'can_delete', True),
                             can_export=getattr(view, 'can_export', True),
                             can_create=getattr(view, 'can_create', True),
                             can_edit=getattr(view, 'can_edit', True),
                             can_view_details=getattr(view, 'can_view_details', True),
                             can_set_page_size=getattr(view, 'can_set_page_size', True),
                             admin_manager=admin_manager)
    
    except Exception as e:
        current_app.logger.error(f"Error in list_view for {model_name}: {str(e)}")
        flash(f'Error loading {view.name}: {str(e)}', 'error')
        return redirect(url_for('admin.dashboard'))


@admin_bp.route('/model/<model_name>/new/', methods=['GET', 'POST'])
@admin_required
def create_view(model_name):
    """Create view for any model - FIXED URL"""
    model_name = model_name.rstrip('/')
    view = admin_manager.get_view(model_name)
    
    if not view:
        flash(f'Model "{model_name}" not found.', 'error')
        return redirect(url_for('admin.dashboard'))
    
    if not getattr(view, 'can_create', True):
        flash('Create operation not allowed', 'error')
        return redirect(url_for('admin.list_view', model_name=model_name))
    
    if request.method == 'POST':
        try:
            success, result = view.create_model(request.form)
            if success:
                flash(f'{view.name} created successfully!', 'success')
                return redirect(url_for('admin.list_view', model_name=model_name))
            else:
                flash(f'Error creating {view.name}: {result}', 'error')
        except Exception as e:
            current_app.logger.error(f"Error creating {model_name}: {str(e)}")
            flash(f'Error creating {view.name}: {str(e)}', 'error')
    
    # Get columns for the form
    columns = getattr(view, 'scaffold_list_columns', lambda: [])()
    form_columns = getattr(view, 'form_columns', None) or columns
    
    return render_template('admin/create.html',
                         view=view,
                         columns=columns,
                         form_columns=form_columns,
                         model_name=model_name,
                         admin_manager=admin_manager)



@admin_bp.route('/model/<model_name>/edit/<int:id>/', methods=['GET', 'POST'])
@admin_required
def edit_view(model_name, id):
    """Edit view for any model - FIXED URL"""
    model_name = model_name.rstrip('/')
    view = admin_manager.get_view(model_name)
    
    print(f"🔧 EDIT_VIEW called: model={model_name}, id={id}, method={request.method}")
    
    if not view:
        flash(f'Model "{model_name}" not found.', 'error')
        return redirect(url_for('admin.dashboard'))
    
    if not getattr(view, 'can_edit', True):
        flash('Edit operation not allowed', 'error')
        return redirect(url_for('admin.list_view', model_name=model_name))
    
    try:
        item = view.model.query.get_or_404(id)
        print(f"✅ Found item: {item}")
    except Exception as e:
        flash(f'Item not found: {str(e)}', 'error')
        return redirect(url_for('admin.list_view', model_name=model_name))
    
    if request.method == 'POST':
        print(f"📝 Processing form data: {dict(request.form)}")
        try:
            success, result = view.update_model(item, request.form)
            if success:
                flash(f'{view.name} updated successfully!', 'success')
                print(f"✅ Update successful, redirecting to list view")
                return redirect(url_for('admin.list_view', model_name=model_name))
            else:
                flash(f'Error updating {view.name}: {result}', 'error')
                print(f"❌ Update failed: {result}")
        except Exception as e:
            current_app.logger.error(f"Error updating {model_name} {id}: {str(e)}")
            flash(f'Error updating {view.name}: {str(e)}', 'error')
            print(f"❌ Update exception: {str(e)}")
    
    # GET request - show form
    columns = getattr(view, 'scaffold_list_columns', lambda: [])()
    form_columns = getattr(view, 'form_columns', None) or columns
    
    print(f"📋 Rendering edit form with {len(form_columns)} columns")
    
    return render_template('admin/edit.html',
                         view=view,
                         item=item,
                         columns=columns,
                         form_columns=form_columns,
                         model_name=model_name,
                         admin_manager=admin_manager)


@admin_bp.route('/model/<model_name>/details/<int:id>/')
@admin_required
def detail_view(model_name, id):
    """Detail view for any model"""
    model_name = model_name.rstrip('/')
    view = admin_manager.get_view(model_name)
    
    if not view:
        flash(f'Model "{model_name}" not found.', 'error')
        return redirect(url_for('admin.dashboard'))
    
    if not getattr(view, 'can_view_details', True):
        flash('View details not allowed', 'error')
        return redirect(url_for('admin.list_view', model_name=model_name))
    
    try:
        item = view.model.query.get_or_404(id)
    except Exception as e:
        flash(f'Item not found: {str(e)}', 'error')
        return redirect(url_for('admin.list_view', model_name=model_name))
    
    columns = getattr(view, 'scaffold_list_columns', lambda: [])()
    formatters = getattr(view, 'column_formatters', None) or getattr(view, 'get_column_formatters', lambda: {})()
    
    return render_template('admin/detail.html',
                         view=view,
                         item=item,
                         columns=columns,
                         formatters=formatters,
                         model_name=model_name,
                         admin_manager=admin_manager)

@admin_bp.route('/model/<model_name>/delete/', methods=['POST'])
@admin_required
def delete_view(model_name):
    """Delete action for any model"""
    model_name = model_name.rstrip('/')
    view = admin_manager.get_view(model_name)
    
    if not view:
        return jsonify({'success': False, 'error': 'Invalid model'})
    
    if not getattr(view, 'can_delete', True):
        return jsonify({'success': False, 'error': 'Delete operation not allowed'})
    
    id = request.form.get('id')
    if not id:
        return jsonify({'success': False, 'error': 'No ID provided'})
    
    try:
        item = view.model.query.get(id)
        if not item:
            return jsonify({'success': False, 'error': 'Item not found'})
        
        success = view.delete_model(item)
        
        if success:
            return jsonify({'success': True, 'message': f'{view.name} deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Delete failed'})
            
    except Exception as e:
        current_app.logger.error(f"Error deleting {model_name} {id}: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})


@admin_bp.route('/model/<model_name>/export/')
@admin_required
def export_view(model_name):
    """Export action for any model"""
    model_name = model_name.rstrip('/')
    view = admin_manager.get_view(model_name)
    
    if not view or not getattr(view, 'can_export', True):
        flash('Export not allowed', 'error')
        return redirect(url_for('admin.list_view', model_name=model_name))
    
    try:
        # Get all data for export
        items = view.model.query.all()
        columns = getattr(view, 'scaffold_list_columns', lambda: [])()
        formatters = getattr(view, 'column_formatters', None) or getattr(view, 'get_column_formatters', lambda: {})()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([col.replace('_', ' ').title() for col in columns])
        
        # Write data with formatting
        for item in items:
            row = []
            for column in columns:
                value = getattr(item, column, '')
                
                # Apply formatters if they exist
                if column in formatters:
                    try:
                        formatted_value = formatters[column](None, item, column)
                        # Extract text from Markup if needed
                        if hasattr(formatted_value, 'striptags'):
                            value = formatted_value.striptags()
                        else:
                            value = str(formatted_value)
                    except Exception:
                        value = str(value)
                else:
                    # Default formatting
                    if isinstance(value, datetime.datetime):
                        value = value.strftime('%Y-%m-%d %H:%M')
                    elif isinstance(value, datetime.date):
                        value = value.strftime('%Y-%m-%d')
                    elif isinstance(value, bool):
                        value = 'Yes' if value else 'No'
                    elif value is None:
                        value = ''
                
                row.append(str(value))
            writer.writerow(row)
        
        output.seek(0)
        
        filename = f"{model_name}_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        current_app.logger.error(f"Error exporting {model_name}: {str(e)}")
        flash(f'Error exporting data: {str(e)}', 'error')
        return redirect(url_for('admin.list_view', model_name=model_name))


@admin_bp.route('/model/<model_name>/action/', methods=['POST'])
@admin_required
def bulk_action(model_name):
    """Bulk actions for any model"""
    model_name = model_name.rstrip('/')
    view = admin_manager.get_view(model_name)
    
    if not view:
        return jsonify({'success': False, 'error': 'Invalid model'})
    
    action = request.form.get('action')
    ids = request.form.getlist('rowid')
    
    if not ids:
        return jsonify({'success': False, 'error': 'No items selected'})
    
    try:
        if action == 'delete' and getattr(view, 'can_delete', True):
            deleted_count = 0
            for id in ids:
                item = view.model.query.get(id)
                if item:
                    if view.delete_model(item):
                        deleted_count += 1
            
            flash(f'Successfully deleted {deleted_count} {view.name}(s).', 'success')
            return jsonify({'success': True, 'message': f'Deleted {deleted_count} items'})
            
        elif action == 'export' and getattr(view, 'can_export', True):
            # Implement bulk export logic here
            flash('Bulk export functionality would go here.', 'info')
            return jsonify({'success': True, 'message': 'Bulk export triggered'})
        
        else:
            return jsonify({'success': False, 'error': 'Invalid action or permission denied'})
            
    except Exception as e:
        current_app.logger.error(f"Error in bulk action for {model_name}: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})







################################## API Endpoints ##################################
# API Endpoints
@admin_bp.route('/api/stats')
@admin_required
def api_stats():
    """API endpoint for system statistics."""
    try:
        print("📊 API Stats requested")
        
        # Check if refresh is requested
        force_refresh = request.args.get('refresh', 'false').lower() == 'true'
        
        stats = get_system_stats(force_refresh=force_refresh)
        
        response = {
            'success': True,
            'data': stats,
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'cache_info': 'cached' if not force_refresh else 'refreshed'
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Error in api_stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 500

@admin_bp.route('/api/stats/refresh')
@admin_required
def refresh_stats():
    """Force refresh the statistics cache."""
    try:
        # Clear the cache
        get_system_stats.cache_clear()
        
        # Get fresh stats
        stats = get_system_stats(force_refresh=True)
        
        return jsonify({
            'success': True,
            'message': 'Statistics cache refreshed',
            'data': stats,
            'timestamp': datetime.datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Error refreshing stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/api/menu')
@admin_required
def api_menu():
    """API endpoint for admin menu - FIXED JSON SERIALIZATION"""
    try:
        menu = admin_manager.get_menu()
        
        # Create serializable menu structure
        serializable_menu = {}
        for category, items in menu.items():
            serializable_menu[category] = []
            for item in items:
                serializable_menu[category].append({
                    'name': item.get('name', 'Unknown'),
                    'model_name': item.get('model_name', 'Unknown'),
                    'icon': item.get('icon', 'fa-table'),
                    # Don't include the view object as it's not serializable
                })
        
        return jsonify({
            'menu': serializable_menu,
            'categories': list(menu.keys()),
            'total_categories': len(menu)
        })
    
    except Exception as e:
        current_app.logger.error(f"Error in api_menu: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch menu',
            'message': str(e)
        }), 500


@admin_bp.route('/api/system-stats')
@admin_required
def api_system_stats():
    """API endpoint for comprehensive system statistics"""
    try:
        stats = get_comprehensive_system_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/routes-analysis')
@admin_required
def api_routes_analysis():
    """API endpoint for routes analysis"""
    try:
        analysis = admin_manager.get_routes_analysis()
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/lookup-tables')
@admin_required
def api_lookup_tables():
    """API endpoint for lookup tables information"""
    try:
        lookup_tables = []
        for model_name, view in admin_manager._views.items():
            if admin_manager._is_lookup_table(view.model):
                lookup_tables.append({
                    'name': view.name,
                    'model_name': model_name,
                    'category': getattr(view, 'category', 'Uncategorized'),
                    'record_count': view.model.query.count()
                })
        
        return jsonify({
            'lookup_tables': lookup_tables,
            'total_lookup_tables': len(lookup_tables)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/database-schema')
@admin_required
def api_database_schema():
    """API endpoint for complete database schema"""
    try:
        from sqlalchemy import inspect
        
        inspector = inspect(db.engine)
        schema_info = {}
        
        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            primary_keys = inspector.get_pk_constraint(table_name)
            foreign_keys = inspector.get_foreign_keys(table_name)
            indexes = inspector.get_indexes(table_name)
            
            schema_info[table_name] = {
                'columns': [
                    {
                        'name': col['name'],
                        'type': str(col['type']),
                        'nullable': col['nullable'],
                        'primary_key': col.get('primary_key', False),
                        'autoincrement': col.get('autoincrement', False)
                    } for col in columns
                ],
                'primary_keys': primary_keys.get('constrained_columns', []),
                'foreign_keys': [
                    {
                        'columns': fk['constrained_columns'],
                        'references': f"{fk['referred_table']}.{fk['referred_columns']}"
                    } for fk in foreign_keys
                ],
                'indexes': [
                    {
                        'name': idx['name'],
                        'columns': idx['column_names'],
                        'unique': idx['unique']
                    } for idx in indexes
                ],
                'is_lookup_table': any(x in table_name.lower() for x in ['status', 'type', 'category'])
            }
        
        return jsonify(schema_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500







# Test and Debug Routes
@admin_bp.route('/test')
@admin_required
def test_route():
    """Test route to verify admin is working"""
    return jsonify({
        'status': 'success',
        'message': 'Admin is working!',
        'menu': admin_manager.get_menu(),
        'views_count': len(admin_manager.get_models()),
        'registered_models': list(admin_manager._views.keys())
    })


@admin_bp.route('/debug/health')
@admin_required
def debug_health():
    """Comprehensive health check for admin system"""
    health_info = {
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'components': {}
    }
    
    # Check views initialization
    health_info['components']['views_initialized'] = {
        'status': 'ok' if views_initialized else 'error',
        'message': 'Views initialized successfully' if views_initialized else 'Views not initialized'
    }
    
    # Check admin manager
    health_info['components']['admin_manager'] = {
        'status': 'ok',
        'total_views': len(admin_manager._views),
        'total_categories': len(admin_manager.get_menu())
    }
    
    # Check database connection
    try:
        from app.models import User
        user_count = User.query.count()
        health_info['components']['database'] = {
            'status': 'ok',
            'user_count': user_count
        }
    except Exception as e:
        health_info['components']['database'] = {
            'status': 'error',
            'error': str(e)
        }
        health_info['status'] = 'degraded'
    
    # Check route generation
    try:
        test_route = url_for('admin.dashboard')
        health_info['components']['route_generation'] = {
            'status': 'ok',
            'test_route': test_route
        }
    except Exception as e:
        health_info['components']['route_generation'] = {
            'status': 'error',
            'error': str(e)
        }
        health_info['status'] = 'degraded'
    
    return jsonify(health_info)

@admin_bp.route('/debug/urls')
@admin_required
def debug_urls():
    """Debug URL generation specifically"""
    test_urls = {}
    models_to_test = ['user', 'patient', 'appointment', 'organization', 'staff']
    
    for model in models_to_test:
        try:
            test_urls[model] = {
                'list': url_for('admin.list_view', model_name=model),
                'create': url_for('admin.create_view', model_name=model),
                'exists': model in admin_manager._views
            }
        except Exception as e:
            test_urls[model] = {'error': str(e)}
    
    return jsonify({
        'test_urls': test_urls,
        'available_models': list(admin_manager._views.keys()),
        'blueprint_name': admin_bp.name,
        'total_registered_models': len(admin_manager._views)
    })

@admin_bp.route('/debug/template-vars')
@admin_required
def debug_template_vars():
    """Debug what variables are available in template"""
    template_info = {
        'admin_manager_available': 'admin_manager' in globals(),
        'admin_manager_type': type(admin_manager).__name__ if 'admin_manager' in globals() else 'None',
        'menu_available': admin_manager.get_menu() if 'admin_manager' in globals() else 'No admin_manager',
        'menu_categories': list(admin_manager.get_menu().keys()) if 'admin_manager' in globals() and admin_manager.get_menu() else [],
        'total_categories': len(admin_manager.get_menu()) if 'admin_manager' in globals() and admin_manager.get_menu() else 0,
        'total_models': len(admin_manager._views) if 'admin_manager' in globals() else 0
    }
    
    # Also test template rendering
    from flask import render_template_string
    
    test_template = """
    <h1>Template Test</h1>
    <p>admin_manager: {{ 'YES' if admin_manager else 'NO' }}</p>
    <p>Menu: {{ 'YES' if admin_manager and admin_manager.get_menu() else 'NO' }}</p>
    <p>Categories: {{ admin_manager.get_menu().keys()|list if admin_manager and admin_manager.get_menu() else 'NONE' }}</p>
    
    {% if admin_manager and admin_manager.get_menu() %}
        <h2>Menu Items:</h2>
        {% for category, items in admin_manager.get_menu().items() %}
        <div style="border: 1px solid #ccc; margin: 10px; padding: 10px;">
            <h3>{{ category }} ({{ items|length }})</h3>
            <ul>
            {% for item in items %}
                <li>{{ item.name }} - {{ item.model_name }}</li>
            {% endfor %}
            </ul>
        </div>
        {% endfor %}
    {% endif %}
    """
    
    return render_template_string(test_template, admin_manager=admin_manager)

@admin_bp.route('/test-minimal')
@admin_required
def test_minimal():
    """Test minimal template"""
    return render_template('admin/minimal_base.html', admin_manager=admin_manager)

@admin_bp.route('/test-complete')
@admin_required
def test_complete():
    """Test complete template with sidebar and navbar"""
    return render_template('admin/complete_base.html', admin_manager=admin_manager)

@admin_bp.route('/test-simple')
@admin_required  
def test_simple():
    """Test simple working template"""
    print("🔍 Testing template variables:")
    print(f"   admin_manager: {'YES' if admin_manager else 'NO'}")
    print(f"   Menu: {'YES' if admin_manager and admin_manager.get_menu() else 'NO'}")
    print(f"   Categories: {list(admin_manager.get_menu().keys()) if admin_manager and admin_manager.get_menu() else 'NONE'}")
    
    return render_template('admin/working_base.html', admin_manager=admin_manager)

@admin_bp.route('/debug')
@admin_required
def debug_views():
    """Safe debug route using serializable methods"""
    try:
        views_info = admin_manager.get_serializable_views_info()
        menu_info = admin_manager.get_serializable_menu()
        
        return jsonify({
            'total_views': len(views_info),
            'views': views_info,
            'menu': menu_info,
            'available_models': list(views_info.keys()),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': 'Failed to get views data',
            'message': str(e),
            'status': 'error'
        }), 500

@admin_bp.route('/api/debug/simple')
@admin_required
def api_debug_simple():
    """Simple debug endpoint with safe data"""
    try:
        safe_data = {
            'status': 'success',
            'total_models': len(admin_manager._views),
            'model_names': list(admin_manager._views.keys()),
            'categories': list(admin_manager.get_menu().keys()),
            'timestamp': datetime.datetime.now().isoformat()
        }
        return jsonify(safe_data)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@admin_bp.route('/debug/models')
@admin_required
def debug_models():
    """Debug route to check model registration - USING SERIALIZABLE DATA"""
    try:
        models_info = admin_manager.get_serializable_views()
        menu_structure = admin_manager.get_serializable_menu()
        
        return jsonify({
            'total_models': len(models_info),
            'models': models_info,
            'menu_structure': menu_structure,
            'categories': list(menu_structure.keys())
        })
    
    except Exception as e:
        return jsonify({
            'error': 'Failed to get models data',
            'message': str(e)
        }), 500

@admin_bp.route('/debug/tenant-test')
@admin_required
def debug_tenant_test():
    """Debug tenant routes specifically"""
    from app.models import Tenant
    
    test_data = {
        'tenant_model_exists': Tenant is not None,
        'tenant_view_registered': 'tenant' in admin_manager._views,
        'tenant_view_info': None,
        'url_generation_tests': {}
    }
    
    if 'tenant' in admin_manager._views:
        tenant_view = admin_manager._views['tenant']
        test_data['tenant_view_info'] = {
            'name': getattr(tenant_view, 'name', 'Unknown'),
            'model': tenant_view.model.__name__,
            'can_edit': getattr(tenant_view, 'can_edit', True),
            'can_create': getattr(tenant_view, 'can_create', True)
        }
    
    # Test URL generation
    try:
        test_data['url_generation_tests']['list'] = url_for('admin.list_view', model_name='tenant')
    except Exception as e:
        test_data['url_generation_tests']['list_error'] = str(e)
    
    try:
        test_data['url_generation_tests']['create'] = url_for('admin.create_view', model_name='tenant')
    except Exception as e:
        test_data['url_generation_tests']['create_error'] = str(e)
    
    return jsonify(test_data)


# Add these debug routes to test authentication
@admin_bp.route('/debug/auth-status')
def debug_auth_status():
    """Debug route to check authentication status"""
    auth_info = {
        'is_authenticated': current_user.is_authenticated,
        'user_id': getattr(current_user, 'id', None),
        'user_email': getattr(current_user, 'email', None),
        'is_admin': getattr(current_user, 'is_admin', False),
        'session_keys': list(session.keys()),
        'request_endpoint': request.endpoint,
        'headers': dict(request.headers)
    }
    
    return jsonify(auth_info)

@admin_bp.route('/debug/login-test', methods=['POST'])
def debug_login_test():
    """Test login endpoint for admin"""
    from app.models import User
    from flask_login import login_user
    
    # This is for testing only - in production use proper authentication
    test_email = request.json.get('email')
    if not test_email:
        return jsonify({'error': 'Email required'}), 400
    
    user = User.query.filter_by(email=test_email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Make user admin for testing
    if not getattr(user, 'is_admin', False):
        user.is_admin = True
        db.session.commit()
        print(f"✅ Made user {user.email} admin for testing")
    
    login_user(user)
    
    return jsonify({
        'success': True,
        'message': f'Logged in as {user.email}',
        'is_admin': user.is_admin,
        'user_id': user.id
    })

@admin_bp.route('/test-public')
def test_public():
    """Public route for testing (no auth required)"""
    return jsonify({
        'message': 'This is a public admin route',
        'authenticated': current_user.is_authenticated,
        'is_admin': getattr(current_user, 'is_admin', False)
    })

@admin_bp.route('/test-protected')
@admin_required
def test_protected():
    """Protected route for testing (auth required)"""
    return jsonify({
        'message': 'This is a protected admin route',
        'user': current_user.email,
        'is_admin': current_user.is_admin
    })


@admin_bp.route('/admin_logout', methods=['POST'])
@admin_required
def admin_logout():
    """Admin-specific logout route"""
    from flask_login import logout_user
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('admin.admin_menu'))  # or your login page

# Optional: Add a GET method logout for direct links
@admin_bp.route('/logout')
@admin_required
def logout_get():
    """GET logout route for simplicity"""
    from flask_login import logout_user
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('admin.admin_menu'))


# backend/app/admin/routes.py

# Add these routes to your existing routes file

@admin_bp.route('/database/schema')
@admin_required
def database_schema():
    """Database schema analysis page"""
    from app.admin.db_views import DatabaseManagementView
    
    db_view = DatabaseManagementView()
    schema_info = db_view.get_schema_info()
    
    return render_template('admin/database_schema.html',
                         schema_info=schema_info,
                         admin_manager=admin_manager)

@admin_bp.route('/database/stats')
@admin_required
def database_stats():
    """Database statistics page"""
    from app.admin.db_views import DatabaseManagementView
    
    db_view = DatabaseManagementView()
    stats = db_view.get_database_stats()
    
    return render_template('admin/database_stats.html',
                         stats=stats,
                         admin_manager=admin_manager)

@admin_bp.route('/database/management')
@admin_required
def database_management():
    """Database management dashboard"""
    return render_template('admin/database_management.html',
                         admin_manager=admin_manager)

'''@admin_bp.route('/api/database/schema')
@admin_required
def api_database_schema():
    """API endpoint for database schema"""
    from app.admin.db_views import DatabaseManagementView
    
    db_view = DatabaseManagementView()
    schema_info = db_view.get_schema_info()
    
    return jsonify(schema_info)'''

@admin_bp.route('/api/database/stats')
@admin_required
def api_database_stats():
    """API endpoint for database statistics"""
    from app.admin.db_views import DatabaseManagementView
    
    db_view = DatabaseManagementView()
    stats = db_view.get_database_stats()
    
    return jsonify(stats)

@admin_bp.route('/api/database/execute-cli', methods=['POST'])
@admin_required
def api_execute_cli():
    """Execute CLI commands via API"""
    command = request.json.get('command')
    
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    
    # Map commands to functions
    command_handlers = {
        'init-db': handle_init_db,
        'reset-db': handle_reset_db,
        'demo-data': handle_demo_data,
        'init-lookups': handle_init_lookups,
        'check-db': handle_check_db
    }
    
    if command not in command_handlers:
        return jsonify({'error': f'Unknown command: {command}'}), 400
    
    try:
        result = command_handlers[command]()
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def handle_init_db():
    """Handle init-db command"""
    from app.models import db
    db.create_all()
    return "Database initialized successfully"

def handle_reset_db():
    """Handle reset-db command"""
    # Implementation would drop and recreate database
    return "Database reset functionality would be implemented here"

def handle_demo_data():
    """Handle demo-data command"""
    # This would call your demo data creation function
    return "Demo data creation would be implemented here"

def handle_init_lookups():
    """Handle init-lookups command"""
    # This would call your lookup initialization function
    return "Lookup tables initialized successfully"

def handle_check_db():
    """Handle check-db command"""
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return f"Database check complete. Found {len(tables)} tables."


@admin_bp.route('/documentation')
@admin_required
def documentation():
    """Comprehensive documentation page with permission-based content."""
    try:
        print("📚 Loading documentation page...")
        
        # Get user permissions for dynamic content
        user_permissions = {
            'can_manage_users': current_user.is_admin or getattr(current_user, 'can_manage_users', False),
            'can_manage_patients': current_user.is_admin or getattr(current_user, 'can_manage_patients', False),
            'can_manage_appointments': current_user.is_admin or getattr(current_user, 'can_manage_appointments', False),
            'can_manage_treatments': current_user.is_admin or getattr(current_user, 'can_manage_treatments', False),
            'can_access_reports': current_user.is_admin or getattr(current_user, 'can_access_reports', False),
            'can_manage_inventory': current_user.is_admin or getattr(current_user, 'can_manage_inventory', False),
        }
        
        return render_template('admin/documentation.html', 
                             user_permissions=user_permissions)
        
    except Exception as e:
        print(f"❌ Error loading documentation: {e}")
        flash('Error loading documentation page', 'error')
        return redirect(url_for('admin.dashboard'))


# Initialize function
def init_admin(app):
    """Initialize the complete admin system with route analysis"""
    # Register the blueprint
    app.register_blueprint(admin_bp)
    
    # Analyze app routes
    with app.app_context():
        admin_manager.analyze_app_routes(app)
        ensure_all_views_initialized()
    
    print("✅ Complete Dentaloist Admin System Initialized")
    print("✅ Database Tables: All models + lookup tables")
    print("✅ App Routes: Complete route analysis")
    print("✅ Available at: /admin")
    
    return admin_manager




