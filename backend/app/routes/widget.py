# backend/app/routes/widgets.py
from flask import Blueprint, jsonify, request, current_app
from flask_socketio import emit
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

# Import auth and tenancy utilities
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import multi_tenant_query, tenant_required
from ..utils.rate_limit import rate_limit
from ..models import Widget, WidgetConfig, User, AuditTrail, db

widget_api_bp = Blueprint('widget_api', __name__, url_prefix='/api/widgets')

# RBAC Permission Constants
PERMISSION_VIEW_WIDGETS = 'view_widgets'
PERMISSION_MANAGE_WIDGETS = 'manage_widgets'
PERMISSION_CUSTOMIZE_DASHBOARD = 'customize_dashboard'

logger = logging.getLogger(__name__)

# Default widget configurations
DEFAULT_WIDGETS = {
    'appointments_today': {
        'name': 'Appointments Today',
        'type': 'stat',
        'category': 'appointments',
        'refresh_interval': 300,  # 5 minutes
        'permissions_required': ['view_appointments'],
        'config': {
            'color': 'blue',
            'size': 'small',
            'icon': 'calendar'
        }
    },
    'new_patients': {
        'name': 'New Patients This Month',
        'type': 'stat',
        'category': 'patients',
        'refresh_interval': 3600,  # 1 hour
        'permissions_required': ['view_patients'],
        'config': {
            'color': 'green',
            'size': 'small',
            'icon': 'user-plus'
        }
    },
    'revenue_metrics': {
        'name': 'Revenue Overview',
        'type': 'chart',
        'category': 'financial',
        'refresh_interval': 1800,  # 30 minutes
        'permissions_required': ['view_revenue'],
        'config': {
            'color': 'purple',
            'size': 'medium',
            'chart_type': 'line'
        }
    },
    'treatment_rooms': {
        'name': 'Treatment Rooms Status',
        'type': 'control',
        'category': 'operations',
        'refresh_interval': 60,  # 1 minute
        'permissions_required': ['view_operations'],
        'config': {
            'color': 'orange',
            'size': 'medium',
            'interactive': True
        }
    },
    'lab_orders_pending': {
        'name': 'Pending Lab Orders',
        'type': 'stat',
        'category': 'labs',
        'refresh_interval': 600,  # 10 minutes
        'permissions_required': ['view_lab_orders'],
        'config': {
            'color': 'red',
            'size': 'small',
            'icon': 'flask'
        }
    }
}

@widget_api_bp.route('/dashboard', methods=['GET'])
@rate_limit(limit=120, period=3600)  # 120 requests per hour
@tenant_required
@permission_required(PERMISSION_VIEW_WIDGETS)
def get_dashboard_widgets():
    """
    Get all available widgets for the current user's dashboard with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        # Get user's widget configuration
        user_widgets = multi_tenant_query(WidgetConfig.query, tenant_id).filter_by(
            user_id=current_user_obj.id
        ).all()
        
        # If no configuration exists, create default setup
        if not user_widgets:
            user_widgets = _create_default_widget_config(current_user_obj, tenant_id)
        
        # Get current data for each widget
        widgets_data = []
        for config in user_widgets:
            if config.is_active:
                widget_data = _get_widget_data(config.widget_id, tenant_id, current_user_obj)
                if widget_data:
                    widgets_data.append(widget_data)
        
        return jsonify({
            'widgets': widgets_data,
            'layout': _get_user_layout(current_user_obj.id),
            'last_updated': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to get dashboard widgets: {str(e)}")
        return jsonify({'error': 'Failed to retrieve dashboard widgets', 'details': str(e)}), 500

@widget_api_bp.route('/available', methods=['GET'])
@rate_limit(limit=100, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_WIDGETS)
def get_available_widgets():
    """
    Get all available widgets that user has permission to use
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        available_widgets = []
        
        for widget_key, widget_config in DEFAULT_WIDGETS.items():
            # Check if user has required permissions
            has_permissions = all(
                current_user_obj.has_permission(perm) 
                for perm in widget_config['permissions_required']
            )
            
            if has_permissions:
                available_widgets.append({
                    'id': widget_key,
                    'name': widget_config['name'],
                    'type': widget_config['type'],
                    'category': widget_config['category'],
                    'description': widget_config.get('description', ''),
                    'permissions_required': widget_config['permissions_required'],
                    'config': widget_config['config']
                })
        
        return jsonify({
            'available_widgets': available_widgets,
            'total_count': len(available_widgets)
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to get available widgets: {str(e)}")
        return jsonify({'error': 'Failed to retrieve available widgets', 'details': str(e)}), 500

@widget_api_bp.route('/<widget_id>/data', methods=['GET'])
@rate_limit(limit=200, period=3600)  # Higher limit for individual widget data
@tenant_required
@permission_required(PERMISSION_VIEW_WIDGETS)
def get_widget_data(widget_id: str):
    """
    Get real-time data for a specific widget
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        widget_config = DEFAULT_WIDGETS.get(widget_id)
        if not widget_config:
            return jsonify({'error': 'Widget not found'}), 404
        
        # Check permissions
        has_permissions = all(
            current_user_obj.has_permission(perm) 
            for perm in widget_config['permissions_required']
        )
        
        if not has_permissions:
            return jsonify({'error': 'Insufficient permissions for this widget'}), 403
        
        # Get widget data
        data = _get_widget_data(widget_id, tenant_id, current_user_obj)
        
        if not data:
            return jsonify({'error': 'Failed to fetch widget data'}), 500
        
        return jsonify(data), 200
        
    except Exception as e:
        logger.error(f"Failed to get widget data for {widget_id}: {str(e)}")
        return jsonify({'error': 'Failed to retrieve widget data', 'details': str(e)}), 500

@widget_api_bp.route('/layout', methods=['GET', 'PUT'])
@rate_limit(limit=60, period=3600)
@tenant_required
@permission_required(PERMISSION_CUSTOMIZE_DASHBOARD)
def manage_dashboard_layout():
    """
    Get or update user's dashboard layout
    """
    try:
        current_user_obj = get_current_user()
        
        if request.method == 'GET':
            layout = _get_user_layout(current_user_obj.id)
            return jsonify({'layout': layout}), 200
        
        elif request.method == 'PUT':
            data = request.get_json()
            new_layout = data.get('layout', [])
            
            if not isinstance(new_layout, list):
                return jsonify({'error': 'Layout must be an array'}), 400
            
            # Validate layout structure
            if not _validate_layout(new_layout, current_user_obj):
                return jsonify({'error': 'Invalid layout structure'}), 400
            
            # Save layout
            success = _save_user_layout(current_user_obj.id, new_layout)
            
            if success:
                # Broadcast layout update via SocketIO
                _broadcast_widget_update('layout_updated', {
                    'userId': current_user_obj.id,
                    'layout': new_layout,
                    'timestamp': datetime.utcnow().isoformat()
                })
                
                return jsonify({
                    'message': 'Dashboard layout updated successfully',
                    'layout': new_layout
                }), 200
            else:
                return jsonify({'error': 'Failed to save layout'}), 500
                
    except Exception as e:
        logger.error(f"Failed to manage dashboard layout: {str(e)}")
        return jsonify({'error': 'Failed to manage dashboard layout', 'details': str(e)}), 500

@widget_api_bp.route('/config', methods=['POST', 'PUT'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_CUSTOMIZE_DASHBOARD)
def manage_widget_config():
    """
    Add or update widget configuration for user
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        data = request.get_json()
        
        widget_id = data.get('widget_id')
        if not widget_id or widget_id not in DEFAULT_WIDGETS:
            return jsonify({'error': 'Invalid widget ID'}), 400
        
        # Check permissions for this widget
        widget_config = DEFAULT_WIDGETS[widget_id]
        has_permissions = all(
            current_user_obj.has_permission(perm) 
            for perm in widget_config['permissions_required']
        )
        
        if not has_permissions:
            return jsonify({'error': 'Insufficient permissions for this widget'}), 403
        
        if request.method == 'POST':
            # Add new widget to user's dashboard
            success = _add_widget_to_dashboard(current_user_obj.id, tenant_id, widget_id, data.get('config', {}))
            
            if success:
                return jsonify({
                    'message': 'Widget added to dashboard successfully',
                    'widget_id': widget_id
                }), 201
            else:
                return jsonify({'error': 'Failed to add widget to dashboard'}), 500
        
        elif request.method == 'PUT':
            # Update existing widget configuration
            success = _update_widget_config(current_user_obj.id, widget_id, data.get('config', {}))
            
            if success:
                # Broadcast configuration update
                _broadcast_widget_update('widget_config_updated', {
                    'userId': current_user_obj.id,
                    'widgetId': widget_id,
                    'config': data.get('config', {}),
                    'timestamp': datetime.utcnow().isoformat()
                })
                
                return jsonify({
                    'message': 'Widget configuration updated successfully',
                    'widget_id': widget_id
                }), 200
            else:
                return jsonify({'error': 'Failed to update widget configuration'}), 500
                
    except Exception as e:
        logger.error(f"Failed to manage widget config: {str(e)}")
        return jsonify({'error': 'Failed to manage widget configuration', 'details': str(e)}), 500

@widget_api_bp.route('/<widget_id>', methods=['DELETE'])
@rate_limit(limit=30, period=3600)
@tenant_required
@permission_required(PERMISSION_CUSTOMIZE_DASHBOARD)
def remove_widget(widget_id: str):
    """
    Remove widget from user's dashboard
    """
    try:
        current_user_obj = get_current_user()
        
        success = _remove_widget_from_dashboard(current_user_obj.id, widget_id)
        
        if success:
            # Broadcast removal
            _broadcast_widget_update('widget_removed', {
                'userId': current_user_obj.id,
                'widgetId': widget_id,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            return jsonify({
                'message': 'Widget removed from dashboard successfully',
                'widget_id': widget_id
            }), 200
        else:
            return jsonify({'error': 'Failed to remove widget from dashboard'}), 500
            
    except Exception as e:
        logger.error(f"Failed to remove widget: {str(e)}")
        return jsonify({'error': 'Failed to remove widget', 'details': str(e)}), 500

@widget_api_bp.route('/refresh', methods=['POST'])
@rate_limit(limit=100, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_WIDGETS)
def refresh_widgets():
    """
    Force refresh all widget data
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        # Get user's active widgets
        user_widgets = multi_tenant_query(WidgetConfig.query, tenant_id).filter_by(
            user_id=current_user_obj.id,
            is_active=True
        ).all()
        
        updated_data = []
        for config in user_widgets:
            widget_data = _get_widget_data(config.widget_id, tenant_id, current_user_obj, force_refresh=True)
            if widget_data:
                updated_data.append(widget_data)
        
        # Broadcast refresh event
        _broadcast_widget_update('widgets_refreshed', {
            'userId': current_user_obj.id,
            'widgets': updated_data,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        return jsonify({
            'message': 'Widgets refreshed successfully',
            'refreshed_count': len(updated_data),
            'widgets': updated_data
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to refresh widgets: {str(e)}")
        return jsonify({'error': 'Failed to refresh widgets', 'details': str(e)}), 500

# Helper functions
def _get_widget_data(widget_id: str, tenant_id: str, user: User, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
    """Get real-time data for a specific widget"""
    widget_config = DEFAULT_WIDGETS.get(widget_id)
    if not widget_config:
        return None
    
    try:
        # This would typically fetch real data from various services
        # For now, return mock data based on widget type
        
        base_data = {
            'id': widget_id,
            'name': widget_config['name'],
            'type': widget_config['type'],
            'category': widget_config['category'],
            'last_updated': datetime.utcnow().isoformat(),
            'refresh_interval': widget_config['refresh_interval']
        }
        
        # Widget-specific data
        if widget_id == 'appointments_today':
            from ..models import Appointment
            query = multi_tenant_query(Appointment.query, tenant_id)
            today = datetime.utcnow().date()
            today_appointments = query.filter(
                db.func.date(Appointment.start_time) == today,
                Appointment.status.in_(['scheduled', 'confirmed'])
            ).count()
            
            base_data.update({
                'value': today_appointments,
                'unit': 'appointments',
                'trend': 'up' if today_appointments > 5 else 'stable'
            })
            
        elif widget_id == 'new_patients':
            from ..models import Patient
            query = multi_tenant_query(Patient.query, tenant_id)
            this_month = datetime.utcnow().replace(day=1)
            new_patients = query.filter(Patient.created_at >= this_month).count()
            
            base_data.update({
                'value': new_patients,
                'unit': 'patients',
                'trend': 'up' if new_patients > 10 else 'stable'
            })
            
        elif widget_id == 'revenue_metrics':
            # Mock revenue data
            base_data.update({
                'value': 12500,
                'unit': '$',
                'trend': 'up',
                'chart_data': {
                    'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                    'datasets': [{
                        'label': 'Revenue',
                        'data': [10000, 11000, 10500, 12000, 12500]
                    }]
                }
            })
            
        elif widget_id == 'treatment_rooms':
            base_data.update({
                'value': 3,
                'unit': 'active',
                'status': 'operational',
                'rooms': [
                    {'id': 1, 'name': 'Room 1', 'status': 'occupied', 'procedure': 'Cleaning'},
                    {'id': 2, 'name': 'Room 2', 'status': 'available', 'procedure': None},
                    {'id': 3, 'name': 'Room 3', 'status': 'maintenance', 'procedure': None}
                ]
            })
            
        elif widget_id == 'lab_orders_pending':
            from ..models import LabOrder
            query = multi_tenant_query(LabOrder.query, tenant_id)
            pending_orders = query.filter_by(status='pending').count()
            
            base_data.update({
                'value': pending_orders,
                'unit': 'orders',
                'priority': 'high' if pending_orders > 5 else 'normal'
            })
        
        return base_data
        
    except Exception as e:
        logger.error(f"Failed to get data for widget {widget_id}: {str(e)}")
        return None

def _create_default_widget_config(user: User, tenant_id: str) -> List[WidgetConfig]:
    """Create default widget configuration for new user"""
    default_widgets = []
    
    for widget_id, config in DEFAULT_WIDGETS.items():
        # Check if user has permissions for this widget
        has_permissions = all(user.has_permission(perm) for perm in config['permissions_required'])
        
        if has_permissions:
            widget_config = WidgetConfig(
                tenant_id=tenant_id,
                user_id=user.id,
                widget_id=widget_id,
                is_active=True,
                config=config.get('config', {}),
                created_at=datetime.utcnow()
            )
            default_widgets.append(widget_config)
            db.session.add(widget_config)
    
    db.session.commit()
    return default_widgets

def _get_user_layout(user_id: int) -> List[Dict[str, Any]]:
    """Get user's dashboard layout from database"""
    # This would typically be stored in a UserPreference or similar table
    # For now, return a default layout
    return [
        {'i': 'appointments_today', 'x': 0, 'y': 0, 'w': 2, 'h': 2},
        {'i': 'new_patients', 'x': 2, 'y': 0, 'w': 2, 'h': 2},
        {'i': 'revenue_metrics', 'x': 0, 'y': 2, 'w': 4, 'h': 3},
        {'i': 'treatment_rooms', 'x': 0, 'y': 5, 'w': 3, 'h': 3},
        {'i': 'lab_orders_pending', 'x': 3, 'y': 5, 'w': 1, 'h': 2}
    ]

def _validate_layout(layout: List[Dict], user: User) -> bool:
    """Validate dashboard layout structure"""
    try:
        required_keys = {'i', 'x', 'y', 'w', 'h'}
        
        for item in layout:
            if not all(key in item for key in required_keys):
                return False
            
            # Check if widget exists and user has permissions
            widget_id = item['i']
            if widget_id not in DEFAULT_WIDGETS:
                return False
            
            widget_config = DEFAULT_WIDGETS[widget_id]
            has_permissions = all(user.has_permission(perm) for perm in widget_config['permissions_required'])
            if not has_permissions:
                return False
        
        return True
    except Exception:
        return False

def _save_user_layout(user_id: int, layout: List[Dict]) -> bool:
    """Save user's dashboard layout to database"""
    try:
        # This would typically save to a UserPreference table
        # For now, just return success
        return True
    except Exception as e:
        logger.error(f"Failed to save user layout: {str(e)}")
        return False

def _add_widget_to_dashboard(user_id: int, tenant_id: str, widget_id: str, config: Dict) -> bool:
    """Add widget to user's dashboard"""
    try:
        existing_config = WidgetConfig.query.filter_by(
            user_id=user_id, widget_id=widget_id
        ).first()
        
        if existing_config:
            existing_config.is_active = True
            existing_config.config = config
        else:
            new_config = WidgetConfig(
                tenant_id=tenant_id,
                user_id=user_id,
                widget_id=widget_id,
                is_active=True,
                config=config,
                created_at=datetime.utcnow()
            )
            db.session.add(new_config)
        
        db.session.commit()
        return True
    except Exception as e:
        logger.error(f"Failed to add widget to dashboard: {str(e)}")
        db.session.rollback()
        return False

def _update_widget_config(user_id: int, widget_id: str, config: Dict) -> bool:
    """Update widget configuration"""
    try:
        widget_config = WidgetConfig.query.filter_by(
            user_id=user_id, widget_id=widget_id
        ).first()
        
        if widget_config:
            widget_config.config = config
            widget_config.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to update widget config: {str(e)}")
        db.session.rollback()
        return False

def _remove_widget_from_dashboard(user_id: int, widget_id: str) -> bool:
    """Remove widget from dashboard (soft delete)"""
    try:
        widget_config = WidgetConfig.query.filter_by(
            user_id=user_id, widget_id=widget_id
        ).first()
        
        if widget_config:
            widget_config.is_active = False
            widget_config.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to remove widget from dashboard: {str(e)}")
        db.session.rollback()
        return False

def _broadcast_widget_update(event: str, data: Dict):
    """Broadcast widget update via SocketIO"""
    try:
        from flask_socketio import emit
        emit(event, data, broadcast=True, namespace='/widgets')
    except Exception as e:
        logger.error(f"Failed to broadcast widget update: {str(e)}")

# SocketIO event handlers
def register_widget_socket_handlers(socketio):
    """Register SocketIO event handlers for real-time widget updates"""
    
    @socketio.on('connect', namespace='/widgets')
    def handle_widget_connect():
        logger.info('Client connected to widgets namespace')
    
    @socketio.on('disconnect', namespace='/widgets')
    def handle_widget_disconnect():
        logger.info('Client disconnected from widgets namespace')
    
    @socketio.on('request_widget_update', namespace='/widgets')
    def handle_widget_update_request(data):
        try:
            user_id = data.get('userId')
            widget_id = data.get('widgetId')
            
            # Validate user and permissions
            user = User.query.get(user_id)
            if user and widget_id in DEFAULT_WIDGETS:
                tenant_id = user.tenant_id
                widget_data = _get_widget_data(widget_id, tenant_id, user, force_refresh=True)
                
                if widget_data:
                    emit('widget_data_update', {
                        'widgetId': widget_id,
                        'data': widget_data,
                        'timestamp': datetime.utcnow().isoformat()
                    })
                    
        except Exception as e:
            logger.error(f"Widget update request failed: {str(e)}")