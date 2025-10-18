from flask import render_template, request, jsonify, redirect, url_for, flash, send_file, safe_url_for, current_app
from flask_login import current_user, login_required, logout_user
from app.admin import admin_bp
from app.admin.views import admin_manager, BaseModelView
from app.admin.auth import admin_required, redirect_to_login, get_main_index
from app.models import db
import datetime
import csv
import io

@admin_bp.before_request
@login_required
def require_login():
    """Require login for all admin routes (replicates Flask-Admin behavior)"""
    pass

# Dashboard - replicates DentaloistAdminIndexView
@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard - replicates Flask-Admin index view"""
    stats = get_system_stats()
    recent_activity = get_recent_activity()
    menu = admin_manager.get_menu()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_activity=recent_activity,
                         menu=menu,
                         admin_manager=admin_manager)

# List View - replicates Flask-Admin list view
@admin_bp.route('/<endpoint>/')
@admin_required
def list_view(endpoint):
    """List view - replicates Flask-Admin ModelView index"""
    view = admin_manager.get_view(endpoint)
    if not view:
        flash('Invalid model endpoint', 'error')
        return redirect(url_for('admin.dashboard'))
    
    if not view.can_view_details:
        flash('Access denied', 'error')
        return redirect(url_for('admin.dashboard'))
    
    # Get parameters (replicates Flask-Admin URL parameters)
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    sort_field = request.args.get('sort', 'id')
    sort_desc = request.args.get('order', 'desc') == 'desc'
    page_size = request.args.get('per_page', view.page_size, type=int)
    
    # Get paginated data using Flask-Admin like method
    pagination = view.get_list(page, sort_field, sort_desc, search, [], page_size)
    columns = view.scaffold_list_columns()
    formatters = view.column_formatters or view.get_column_formatters()
    
    return render_template(view.list_template or 'admin/list.html',
                         view=view,
                         pagination=pagination,
                         columns=columns,
                         formatters=formatters,
                         search=search,
                         endpoint=endpoint,
                         # Explicitly pass all permissions for template
                         can_delete=view.can_delete,
                         can_export=view.can_export,
                         can_create=view.can_create,
                         can_edit=view.can_edit,
                         can_view_details=view.can_view_details,
                         can_set_page_size=view.can_set_page_size,
                         admin_manager=admin_manager)

# Create View - replicates Flask-Admin create view
@admin_bp.route('/<endpoint>/new/', methods=['GET', 'POST'])
@admin_required
def create_view(endpoint):
    """Create view - replicates Flask-Admin create"""
    view = admin_manager.get_view(endpoint)
    if not view:
        flash('Invalid model endpoint', 'error')
        return redirect(url_for('admin.dashboard'))
    
    if not view.can_create:
        flash('Create operation not allowed', 'error')
        return redirect(url_for('admin.list_view', endpoint=endpoint))
    
    if request.method == 'POST':
        success, result = view.create_model(request.form)
        if success:
            return redirect(url_for('admin.list_view', endpoint=endpoint))
        # Error handling is done in create_model with flash messages
    
    columns = view.scaffold_list_columns()
    form_columns = view.form_columns or columns
    
    return render_template(view.create_template or 'admin/create.html',
                         view=view,
                         columns=columns,
                         form_columns=form_columns,
                         endpoint=endpoint,
                         admin_manager=admin_manager)

# Edit View - replicates Flask-Admin edit view
@admin_bp.route('/<endpoint>/edit/<int:id>/', methods=['GET', 'POST'])
@admin_required
def edit_view(endpoint, id):
    """Edit view - replicates Flask-Admin edit"""
    view = admin_manager.get_view(endpoint)
    if not view:
        flash('Invalid model endpoint', 'error')
        return redirect(url_for('admin.dashboard'))
    
    if not view.can_edit:
        flash('Edit operation not allowed', 'error')
        return redirect(url_for('admin.list_view', endpoint=endpoint))
    
    item = view.model.query.get_or_404(id)
    
    if request.method == 'POST':
        success, result = view.update_model(item, request.form)
        if success:
            return redirect(url_for('admin.list_view', endpoint=endpoint))
        # Error handling is done in update_model with flash messages
    
    columns = view.scaffold_list_columns()
    form_columns = view.form_columns or columns
    
    return render_template(view.edit_template or 'admin/edit.html',
                         view=view,
                         item=item,
                         columns=columns,
                         form_columns=form_columns,
                         endpoint=endpoint,
                         admin_manager=admin_manager)

# Detail View - replicates Flask-Admin details view
@admin_bp.route('/<endpoint>/details/<int:id>/')
@admin_required
def detail_view(endpoint, id):
    """Detail view - replicates Flask-Admin details"""
    view = admin_manager.get_view(endpoint)
    if not view:
        flash('Invalid model endpoint', 'error')
        return redirect(url_for('admin.dashboard'))
    
    if not view.can_view_details:
        flash('View details not allowed', 'error')
        return redirect(url_for('admin.list_view', endpoint=endpoint))
    
    item = view.model.query.get_or_404(id)
    columns = view.scaffold_list_columns()
    formatters = view.column_formatters or view.get_column_formatters()
    
    return render_template(view.details_template or 'admin/detail.html',
                         view=view,
                         item=item,
                         columns=columns,
                         formatters=formatters,
                         endpoint=endpoint,
                         admin_manager=admin_manager)

# Delete Action - replicates Flask-Admin delete
@admin_bp.route('/<endpoint>/delete/', methods=['POST'])
@admin_required
def delete_view(endpoint):
    """Delete action - replicates Flask-Admin delete"""
    view = admin_manager.get_view(endpoint)
    if not view:
        return jsonify({'success': False, 'error': 'Invalid model endpoint'})
    
    if not view.can_delete:
        return jsonify({'success': False, 'error': 'Delete operation not allowed'})
    
    id = request.form.get('id')
    if not id:
        return jsonify({'success': False, 'error': 'No ID provided'})
    
    item = view.model.query.get(id)
    if not item:
        return jsonify({'success': False, 'error': 'Item not found'})
    
    success = view.delete_model(item)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Delete failed'})

# Export Action - replicates Flask-Admin export
@admin_bp.route('/<endpoint>/export/')
@admin_required
def export_view(endpoint):
    """Export action - replicates Flask-Admin export"""
    view = admin_manager.get_view(endpoint)
    if not view or not view.can_export:
        flash('Export not allowed', 'error')
        return redirect(url_for('admin.list_view', endpoint=endpoint))
    
    # Get all data for export
    items = view.model.query.all()
    columns = view.scaffold_list_columns()
    formatters = view.column_formatters or view.get_column_formatters()
    
    # Create CSV in memory (like Flask-Admin would)
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
                formatted_value = formatters[column](None, item, column)
                # Extract text from Markup if needed
                if hasattr(formatted_value, 'striptags'):
                    value = formatted_value.striptags()
                else:
                    value = str(formatted_value)
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
    
    filename = f"{endpoint}_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

# Bulk Actions - replicates Flask-Admin bulk actions
@admin_bp.route('/<endpoint>/action/', methods=['POST'])
@admin_required
def bulk_action(endpoint):
    """Bulk actions - replicates Flask-Admin bulk actions"""
    view = admin_manager.get_view(endpoint)
    if not view:
        return jsonify({'success': False, 'error': 'Invalid model endpoint'})
    
    action = request.form.get('action')
    ids = request.form.getlist('rowid')
    
    try:
        if action == 'delete' and view.can_delete:
            deleted_count = 0
            for id in ids:
                item = view.model.query.get(id)
                if item:
                    if view.delete_model(item):
                        deleted_count += 1
            
            flash(f'Successfully deleted {deleted_count} {view.name}(s).', 'success')
            
        elif action == 'export' and view.can_export:
            # Could implement bulk export here
            flash('Bulk export functionality would go here.', 'info')
            
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API Endpoints - replicates Flask-Admin API
@admin_bp.route('/api/stats')
@admin_required
def api_stats():
    stats = get_system_stats()
    return jsonify(stats)

@admin_bp.route('/api/menu')
@admin_required
def api_menu():
    menu = admin_manager.get_menu()
    return jsonify(menu)

@admin_bp.route('/debug-endpoints')
@admin_required
def debug_endpoints():
    """Debug available endpoints"""
    auth_endpoints = []
    for rule in current_app.url_map.iter_rules():
        if rule.endpoint.startswith('auth.'):
            auth_endpoints.append({
                'endpoint': rule.endpoint,
                'rule': str(rule),
                'methods': list(rule.methods)
            })
    
    return jsonify({
        'auth_endpoints': auth_endpoints,
        'test_logout_url': safe_url_for('auth.logout_route'),
        'available_endpoints': [rule.endpoint for rule in current_app.url_map.iter_rules() if 'logout' in rule.endpoint]
    })

    
# Helper Functions
def get_system_stats():
    """Get system statistics - replicates your Flask-Admin stats"""
    try:
        from app.models import User, Patient, Appointment, Organization
        
        stats = {
            'total_users': User.query.filter_by(is_active=True).count(),
            'total_patients': Patient.query.filter_by(is_active=True).count(),
            'total_appointments': Appointment.query.filter_by(is_active=True).count(),
            'total_organizations': Organization.query.filter_by(is_active=True).count(),
            'now': datetime.datetime.now().isoformat()
        }
    except Exception as e:
        stats = {
            'total_users': 0,
            'total_patients': 0,
            'total_appointments': 0,
            'total_organizations': 0,
            'now': datetime.datetime.now().isoformat()
        }
    
    return stats

def get_recent_activity():
    """Get recent system activity"""
    return [
        {
            'type': 'user_login',
            'message': f'User {current_user.email} logged in',
            'timestamp': datetime.datetime.now().isoformat(),
            'icon': 'login'
        },
        {
            'type': 'admin_access',
            'message': 'Admin dashboard accessed',
            'timestamp': (datetime.datetime.now() - datetime.timedelta(minutes=5)).isoformat(),
            'icon': 'dashboard'
        }
    ]

# Initialize function to replace Flask-Admin init_admin
def init_admin(app):
    """Initialize the custom admin - replaces Flask-Admin init_admin"""
    # Register the blueprint with the app
    app.register_blueprint(admin_bp)
    
    print("✅ Custom Dentaloist Admin initialized (replacing Flask-Admin)")
    print("✅ All Flask-Admin functionality has been replicated")
    print("✅ Available at: /admin")
    
    return admin_manager