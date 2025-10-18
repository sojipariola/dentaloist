# backend/app/routes/dashboard.py

from flask import Blueprint, request, jsonify, g, current_app
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_, case
from sqlalchemy.sql import expression
import json

from ..models import (
    db, Widget, User, Organization, Appointment, Invoice, 
    Patient, MedicalRecord, TreatmentPlan
)
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

# ===== Widget Management Routes =====

@dashboard_bp.route('/widgets', methods=['GET'])
@jwt_required()
@tenant_required
def get_widgets():
    """
    Get user's dashboard widgets with optional organization defaults
    """
    try:
        current_user = get_current_user()
        include_defaults = request.args.get('include_defaults', 'true').lower() == 'true'
        
        # Get user's personal widgets
        user_widgets = Widget.query.filter_by(
            user_id=current_user.id,
            is_visible=True
        ).order_by(Widget.position_y, Widget.position_x).all()
        
        response_data = [widget.to_dict() for widget in user_widgets]
        
        # Include organization default widgets if requested
        if include_defaults:
            org_widgets = Widget.query.filter(
                Widget.organization_id == g.tenant_id,
                Widget.user_id.is_(None),  # Organization defaults
                Widget.is_visible == True
            ).order_by(Widget.position_y, Widget.position_x).all()
            
            response_data.extend([widget.to_dict() for widget in org_widgets])
        
        return jsonify(response_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching widgets: {str(e)}")
        return jsonify({'error': 'Failed to fetch widgets'}), 500

@dashboard_bp.route('/widgets', methods=['POST'])
@jwt_required()
@tenant_required
def create_widget():
    """
    Create a new dashboard widget
    """
    try:
        data = request.get_json()
        current_user = get_current_user()
        
        # Validate widget type
        valid_types = [
            'appointment_stats', 'financial_overview', 'patient_metrics',
            'revenue_chart', 'appointment_calendar', 'task_list',
            'performance_metrics', 'treatment_plans', 'medical_records'
        ]
        
        if data['type'] not in valid_types:
            return jsonify({'error': 'Invalid widget type'}), 400
        
        # Determine position if not provided
        position_x = data.get('position_x', 0)
        position_y = data.get('position_y', 0)
        
        # Auto-position new widgets
        if position_x == 0 and position_y == 0:
            last_widget = Widget.query.filter_by(user_id=current_user.id).order_by(
                Widget.position_y.desc(), Widget.position_x.desc()
            ).first()
            
            if last_widget:
                position_x = (last_widget.position_x + last_widget.width) % 12
                position_y = last_widget.position_y + last_widget.height if position_x == 0 else last_widget.position_y
        
        widget = Widget(
            user_id=current_user.id,
            organization_id=g.tenant_id,
            type=data['type'],
            title=data['title'],
            data_source=data.get('data_source'),
            position_x=position_x,
            position_y=position_y,
            width=data.get('width', 4),  # Default 4 columns wide
            height=data.get('height', 3),  # Default 3 rows high
            config=data.get('config', {}),
            refresh_interval=data.get('refresh_interval', 300),  # 5 minutes default
            is_visible=data.get('is_visible', True)
        )
        
        db.session.add(widget)
        db.session.commit()
        
        return jsonify({
            'message': 'Widget created successfully',
            'widget': widget.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating widget: {str(e)}")
        return jsonify({'error': 'Failed to create widget'}), 500

@dashboard_bp.route('/widgets/<int:widget_id>', methods=['PUT'])
@jwt_required()
@tenant_required
def update_widget(widget_id):
    """
    Update widget configuration and layout
    """
    try:
        current_user = get_current_user()
        widget = Widget.query.get_or_404(widget_id)
        
        # Check ownership or admin rights
        if widget.user_id != current_user.id and not current_user.has_permission('manage_dashboard'):
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = [
            'position_x', 'position_y', 'width', 'height', 
            'title', 'config', 'refresh_interval', 'is_visible'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(widget, field, data[field])
        
        widget.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Widget updated successfully',
            'widget': widget.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating widget {widget_id}: {str(e)}")
        return jsonify({'error': 'Failed to update widget'}), 500

@dashboard_bp.route('/widgets/<int:widget_id>', methods=['DELETE'])
@jwt_required()
@tenant_required
def delete_widget(widget_id):
    """
    Delete a dashboard widget
    """
    try:
        current_user = get_current_user()
        widget = Widget.query.get_or_404(widget_id)
        
        # Check ownership or admin rights
        if widget.user_id != current_user.id and not current_user.has_permission('manage_dashboard'):
            return jsonify({'error': 'Access denied'}), 403
        
        db.session.delete(widget)
        db.session.commit()
        
        return jsonify({'message': 'Widget deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting widget {widget_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete widget'}), 500

@dashboard_bp.route('/widgets/reset', methods=['POST'])
@jwt_required()
@tenant_required
def reset_widgets():
    """
    Reset user's dashboard to organization defaults
    """
    try:
        current_user = get_current_user()
        
        # Delete user's current widgets
        Widget.query.filter_by(user_id=current_user.id).delete()
        
        # Copy organization default widgets for user
        org_widgets = Widget.query.filter(
            Widget.organization_id == g.tenant_id,
            Widget.user_id.is_(None),
            Widget.is_visible == True
        ).all()
        
        for org_widget in org_widgets:
            user_widget = Widget(
                user_id=current_user.id,
                organization_id=g.tenant_id,
                type=org_widget.type,
                title=org_widget.title,
                data_source=org_widget.data_source,
                position_x=org_widget.position_x,
                position_y=org_widget.position_y,
                width=org_widget.width,
                height=org_widget.height,
                config=org_widget.config,
                refresh_interval=org_widget.refresh_interval,
                is_visible=org_widget.is_visible
            )
            db.session.add(user_widget)
        
        db.session.commit()
        
        return jsonify({'message': 'Dashboard reset to default layout'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error resetting widgets: {str(e)}")
        return jsonify({'error': 'Failed to reset dashboard'}), 500

# ===== Widget Data Endpoints =====

@dashboard_bp.route('/data/appointment-stats', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_dashboard'])
def get_appointment_stats():
    """
    Get data for appointment statistics widget
    """
    try:
        time_range = request.args.get('time_range', 'today')  # today, week, month, year
        
        # Calculate date range
        now = datetime.utcnow()
        if time_range == 'today':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif time_range == 'week':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif time_range == 'month':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:  # year
            start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Query appointment statistics
        stats = db.session.query(
            func.count(Appointment.id),
            func.sum(case([(Appointment.status == 'completed', 1)], else_=0)),
            func.sum(case([(Appointment.status == 'cancelled', 1)], else_=0)),
            func.sum(case([(Appointment.status == 'no_show', 1)], else_=0)),
            func.avg(Appointment.amount).filter(Appointment.amount.isnot(None))
        ).filter(
            Appointment.organization_id == g.tenant_id,
            Appointment.start_time >= start_date
        ).first()
        
        total, completed, cancelled, no_shows, avg_revenue = stats
        
        # Upcoming appointments
        upcoming = db.session.query(
            Appointment.start_time,
            Patient.first_name,
            Patient.last_name,
            User.first_name.label('provider_first_name'),
            User.last_name.label('provider_last_name')
        ).join(Patient).join(User, Appointment.provider_id == User.id
        ).filter(
            Appointment.organization_id == g.tenant_id,
            Appointment.start_time >= now,
            Appointment.status.in_(['scheduled', 'confirmed'])
        ).order_by(Appointment.start_time.asc()).limit(5).all()
        
        return jsonify({
            'time_range': time_range,
            'stats': {
                'total': total or 0,
                'completed': completed or 0,
                'cancelled': cancelled or 0,
                'no_shows': no_shows or 0,
                'completion_rate': (completed / total * 100) if total > 0 else 0,
                'avg_revenue': float(avg_revenue or 0)
            },
            'upcoming_appointments': [
                {
                    'time': appt.start_time.isoformat(),
                    'patient_name': f"{appt.first_name} {appt.last_name}",
                    'provider_name': f"{appt.provider_first_name} {appt.provider_last_name}"
                }
                for appt in upcoming
            ]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching appointment stats: {str(e)}")
        return jsonify({'error': 'Failed to fetch appointment statistics'}), 500

@dashboard_bp.route('/data/financial-overview', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_dashboard', 'view_financial'])
def get_financial_overview():
    """
    Get data for financial overview widget
    """
    try:
        time_range = request.args.get('time_range', 'month')  # week, month, quarter, year
        
        # Calculate date range
        now = datetime.utcnow()
        if time_range == 'week':
            start_date = now - timedelta(days=7)
        elif time_range == 'month':
            start_date = now - timedelta(days=30)
        elif time_range == 'quarter':
            start_date = now - timedelta(days=90)
        else:  # year
            start_date = now - timedelta(days=365)
        
        # Financial metrics
        financial_data = db.session.query(
            func.sum(Invoice.total).label('total_revenue'),
            func.sum(Invoice.paid_amount).label('collected'),
            func.sum(Invoice.balance).label('outstanding'),
            func.count(Invoice.id).label('invoice_count')
        ).filter(
            Invoice.organization_id == g.tenant_id,
            Invoice.issue_date >= start_date,
            Invoice.status.in_(['paid', 'partial'])
        ).first()
        
        # Revenue by service type
        revenue_by_service = db.session.query(
            Appointment.service_type,
            func.sum(Invoice.total).label('revenue')
        ).join(Invoice, Invoice.appointment_id == Appointment.id
        ).filter(
            Invoice.organization_id == g.tenant_id,
            Invoice.issue_date >= start_date
        ).group_by(Appointment.service_type).all()
        
        return jsonify({
            'time_range': time_range,
            'financials': {
                'total_revenue': float(financial_data.total_revenue or 0),
                'collected': float(financial_data.collected or 0),
                'outstanding': float(financial_data.outstanding or 0),
                'invoice_count': financial_data.invoice_count or 0,
                'collection_rate': (financial_data.collected / financial_data.total_revenue * 100) 
                    if financial_data.total_revenue and financial_data.total_revenue > 0 else 0
            },
            'revenue_by_service': [
                {'service_type': service, 'revenue': float(revenue or 0)}
                for service, revenue in revenue_by_service
            ]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching financial overview: {str(e)}")
        return jsonify({'error': 'Failed to fetch financial data'}), 500

@dashboard_bp.route('/data/patient-metrics', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_dashboard'])
def get_patient_metrics():
    """
    Get data for patient metrics widget
    """
    try:
        # Patient statistics
        patient_stats = db.session.query(
            func.count(Patient.id),
            func.count(case([(Patient.is_active == True, 1)], else_=None)),
            func.count(case([(Patient.created_at >= datetime.utcnow() - timedelta(days=30), 1)], else_=None))
        ).filter(
            Patient.organization_id == g.tenant_id
        ).first()
        
        total_patients, active_patients, new_patients = patient_stats
        
        # Treatment plan statistics
        treatment_stats = db.session.query(
            TreatmentPlan.status,
            func.count(TreatmentPlan.id)
        ).filter(
            TreatmentPlan.organization_id == g.tenant_id
        ).group_by(TreatmentPlan.status).all()
        
        return jsonify({
            'patient_metrics': {
                'total_patients': total_patients or 0,
                'active_patients': active_patients or 0,
                'new_patients_30d': new_patients or 0,
                'activation_rate': (active_patients / total_patients * 100) if total_patients > 0 else 0
            },
            'treatment_plans': {
                status: count for status, count in treatment_stats
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching patient metrics: {str(e)}")
        return jsonify({'error': 'Failed to fetch patient metrics'}), 500

@dashboard_bp.route('/data/widget/<widget_type>', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_dashboard'])
def get_widget_data(widget_type):
    """
    Generic endpoint to get data for any widget type
    """
    try:
        # Map widget types to data functions
        data_functions = {
            'appointment_stats': get_appointment_stats,
            'financial_overview': get_financial_overview,
            'patient_metrics': get_patient_metrics,
            # Add more widget types as needed
        }
        
        if widget_type not in data_functions:
            return jsonify({'error': 'Invalid widget type'}), 400
        
        # Call the appropriate data function
        return data_functions[widget_type]()
        
    except Exception as e:
        current_app.logger.error(f"Error fetching widget data for {widget_type}: {str(e)}")
        return jsonify({'error': 'Failed to fetch widget data'}), 500

# ===== Dashboard Layout Management =====

@dashboard_bp.route('/layout', methods=['GET'])
@jwt_required()
@tenant_required
def get_dashboard_layout():
    """
    Get complete dashboard layout including widget positions
    """
    try:
        current_user = get_current_user()
        
        widgets = Widget.query.filter(
            (Widget.user_id == current_user.id) |
            (Widget.organization_id == g.tenant_id & Widget.user_id.is_(None))
        ).filter(
            Widget.is_visible == True
        ).order_by(Widget.position_y, Widget.position_x).all()
        
        return jsonify({
            'layout': [widget.to_dict() for widget in widgets],
            'user_id': current_user.id,
            'organization_id': g.tenant_id,
            'last_updated': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching dashboard layout: {str(e)}")
        return jsonify({'error': 'Failed to fetch dashboard layout'}), 500

@dashboard_bp.route('/layout', methods=['PUT'])
@jwt_required()
@tenant_required
def update_dashboard_layout():
    """
    Update multiple widget positions at once (for drag-and-drop)
    """
    try:
        current_user = get_current_user()
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({'error': 'Expected array of widget updates'}), 400
        
        for widget_update in data:
            widget_id = widget_update.get('id')
            if not widget_id:
                continue
            
            widget = Widget.query.get(widget_id)
            if not widget or widget.user_id != current_user.id:
                continue
            
            # Update position and size
            if 'position_x' in widget_update:
                widget.position_x = widget_update['position_x']
            if 'position_y' in widget_update:
                widget.position_y = widget_update['position_y']
            if 'width' in widget_update:
                widget.width = widget_update['width']
            if 'height' in widget_update:
                widget.height = widget_update['height']
            
            widget.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'message': 'Dashboard layout updated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating dashboard layout: {str(e)}")
        return jsonify({'error': 'Failed to update dashboard layout'}), 500