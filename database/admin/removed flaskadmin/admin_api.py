from flask import Blueprint, jsonify, current_app
from flask_login import login_required, current_user
from app.models import db, User, Patient, Appointment, Organization
from sqlalchemy import func, Date
import datetime

admin_api = Blueprint('admin_api', __name__, url_prefix='/admin/api')

@admin_api.before_request
@login_required
def require_admin():
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        return jsonify({'error': 'Admin access required'}), 403

@admin_api.route('/stats')
def get_stats():
    """Get real-time admin statistics"""
    try:
        # Safely get counts with error handling
        total_users = User.query.filter_by(is_active=True).count() if hasattr(User, 'is_active') else User.query.count()
        total_patients = Patient.query.filter_by(is_active=True).count() if hasattr(Patient, 'is_active') else Patient.query.count()
        total_appointments = Appointment.query.filter_by(is_active=True).count() if hasattr(Appointment, 'is_active') else Appointment.query.count()
        total_organizations = Organization.query.filter_by(is_active=True).count() if hasattr(Organization, 'is_active') else Organization.query.count()
        
        # Safely calculate today's appointments
        today_appointments = 0
        try:
            # Try different possible date field names
            if hasattr(Appointment, 'appointment_date'):
                today_appointments = Appointment.query.filter(
                    func.date(Appointment.appointment_date) == func.current_date()
                ).count()
            elif hasattr(Appointment, 'date'):
                today_appointments = Appointment.query.filter(
                    func.date(Appointment.date) == func.current_date()
                ).count()
            elif hasattr(Appointment, 'scheduled_date'):
                today_appointments = Appointment.query.filter(
                    func.date(Appointment.scheduled_date) == func.current_date()
                ).count()
            elif hasattr(Appointment, 'created_at'):
                today_appointments = Appointment.query.filter(
                    func.date(Appointment.created_at) == func.current_date()
                ).count()
        except Exception as e:
            current_app.logger.warning(f"Could not calculate today's appointments: {e}")
        
        stats = {
            'total_users': total_users,
            'total_patients': total_patients,
            'total_appointments': total_appointments,
            'total_organizations': total_organizations,
            'today_appointments': today_appointments,
            'pending_payments': 0,  # Add your payment model logic
            'system_status': 'healthy',
            'last_updated': datetime.datetime.now().isoformat()
        }
        return jsonify(stats)
    except Exception as e:
        current_app.logger.error(f"Error fetching admin stats: {e}")
        return jsonify({'error': 'Failed to fetch statistics'}), 500

@admin_api.route('/events')
def get_events():
    """Server-sent events endpoint for real-time updates"""
    # For now, return empty array - implement SSE later
    return jsonify([])

@admin_api.route('/recent-activity')
def recent_activity():
    """Get recent system activity"""
    try:
        # Sample recent activity - replace with your actual audit trail
        activities = [
            {
                'type': 'info',
                'message': 'Admin dashboard accessed',
                'timestamp': datetime.datetime.now().isoformat(),
                'user': current_user.email
            },
            {
                'type': 'success',
                'message': 'System check completed',
                'timestamp': (datetime.datetime.now() - datetime.timedelta(minutes=5)).isoformat(),
                'user': 'system'
            }
        ]
        return jsonify(activities)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_api.route('/export-data', methods=['POST'])
def export_data():
    """Export system data"""
    try:
        # Add your export logic here
        return jsonify({
            'message': 'Export functionality coming soon', 
            'status': 'info'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_api.route('/clear-cache', methods=['POST'])
def clear_cache():
    """Clear system cache"""
    try:
        # Add cache clearing logic here
        return jsonify({
            'message': 'Cache clearing functionality coming soon', 
            'status': 'info'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_api.route('/system-check')
def system_check():
    """Perform system health check"""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        
        # Check essential models with safe attribute checking
        checks = {
            'database': 'healthy',
            'users_table': User.query.first() is not None,
            'patients_table': Patient.query.first() is not None if hasattr(Patient, 'query') else False,
            'appointments_table': Appointment.query.first() is not None if hasattr(Appointment, 'query') else False,
            'organizations_table': Organization.query.first() is not None if hasattr(Organization, 'query') else False
        }
        
        return jsonify({
            'status': 'healthy',
            'checks': checks,
            'timestamp': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.datetime.now().isoformat()
        }), 500

@admin_api.route('/search')
def search():
    """Search across admin models"""
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])
    
    try:
        # Basic search implementation - expand as needed
        results = []
        
        # Search users
        users = User.query.filter(
            User.email.ilike(f'%{query}%') | 
            (hasattr(User, 'first_name') and User.first_name.ilike(f'%{query}%')) |
            (hasattr(User, 'last_name') and User.last_name.ilike(f'%{query}%'))
        ).limit(5).all()
        
        for user in users:
            results.append({
                'type': 'user',
                'id': user.id,
                'name': getattr(user, 'email', 'Unknown'),
                'url': f"/admin/user/?id={user.id}"
            })
        
        # Search patients
        if hasattr(Patient, 'query'):
            patients = Patient.query.filter(
                (hasattr(Patient, 'first_name') and Patient.first_name.ilike(f'%{query}%')) |
                (hasattr(Patient, 'last_name') and Patient.last_name.ilike(f'%{query}%')) |
                (hasattr(Patient, 'email') and Patient.email.ilike(f'%{query}%'))
            ).limit(5).all()
            
            for patient in patients:
                results.append({
                    'type': 'patient',
                    'id': patient.id,
                    'name': f"{getattr(patient, 'first_name', '')} {getattr(patient, 'last_name', '')}".strip(),
                    'url': f"/admin/patient/?id={patient.id}"
                })
        
        return jsonify(results)
        
    except Exception as e:
        current_app.logger.error(f"Search error: {e}")
        return jsonify([])