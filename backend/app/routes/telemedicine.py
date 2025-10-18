# routes/telemedicine.py
from flask import Blueprint, request, jsonify
from flask_login import current_user
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from datetime import date


# Import auth and tenancy utilities
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit

from ..models import TelehealthSession, Patient, User, db

telemedicine_bp = Blueprint('telemedicine', __name__, url_prefix='/api/telemedicine')

# RBAC Permission Constants
PERMISSION_VIEW_TELEHEALTH_SESSIONS = 'view_telehealth_sessions'
PERMISSION_CREATE_TELEHEALTH_SESSIONS = 'create_telehealth_sessions'
PERMISSION_EDIT_TELEHEALTH_SESSIONS = 'edit_telehealth_sessions'
PERMISSION_DELETE_TELEHEALTH_SESSIONS = 'delete_telehealth_sessions'
PERMISSION_JOIN_TELEHEALTH_SESSIONS = 'join_telehealth_sessions'
PERMISSION_MANAGE_TELEHEALTH_SETTINGS = 'manage_telehealth_settings'

@telemedicine_bp.route('/sessions', methods=['GET'])
@rate_limit(limit=100, period=3600)  # 100 requests per hour
@tenant_required
@permission_required(PERMISSION_VIEW_TELEHEALTH_SESSIONS)
def get_sessions():
    """
    Get telehealth sessions with advanced filtering, sorting, and tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)  # Cap at 100 per page
        
        # Filter parameters
        patient_id = request.args.get('patient_id', type=int)
        provider_id = request.args.get('provider_id', type=int)
        status = request.args.get('status')
        session_type = request.args.get('type')
        
        # Date range filtering
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        # Build base query with tenant filtering
        query = multi_tenant_query(TelehealthSession.query, tenant_id)
        
        # Apply filters
        if patient_id:
            query = query.filter(TelehealthSession.patient_id == patient_id)
        if provider_id:
            query = query.filter(TelehealthSession.provider_id == provider_id)
        if status:
            query = query.filter(TelehealthSession.status == status)
        if session_type:
            query = query.filter(TelehealthSession.type == session_type)
        
        # Date range filtering
        if start_date_str:
            try:
                start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                query = query.filter(TelehealthSession.scheduled_start >= start_date)
            except ValueError:
                return jsonify({'error': 'Invalid start_date format. Use ISO format.'}), 400
        
        if end_date_str:
            try:
                end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                query = query.filter(TelehealthSession.scheduled_start <= end_date)
            except ValueError:
                return jsonify({'error': 'Invalid end_date format. Use ISO format.'}), 400
        
        # Default to upcoming sessions if no date range provided
        if not start_date_str and not end_date_str:
            query = query.filter(TelehealthSession.scheduled_start >= datetime.utcnow())
        
        # Sorting
        sort_by = request.args.get('sort_by', 'scheduled_start')
        sort_order = request.args.get('sort_order', 'asc')
        
        if sort_order.lower() == 'desc':
            query = query.order_by(getattr(TelehealthSession, sort_by).desc())
        else:
            query = query.order_by(getattr(TelehealthSession, sort_by).asc())
        
        # Pagination
        sessions = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'sessions': [session.to_dict(include_details=True) for session in sessions.items],
            'pagination': {
                'page': sessions.page,
                'per_page': sessions.per_page,
                'total': sessions.total,
                'pages': sessions.pages,
                'has_next': sessions.has_next,
                'has_prev': sessions.has_prev
            },
            'filters': {
                'patient_id': patient_id,
                'provider_id': provider_id,
                'status': status,
                'type': session_type,
                'start_date': start_date_str,
                'end_date': end_date_str
            },
            'summary': _get_sessions_summary(tenant_id, query)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve telehealth sessions', 'details': str(e)}), 500

@telemedicine_bp.route('/sessions/<int:session_id>', methods=['GET'])
@rate_limit(limit=120, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_TELEHEALTH_SESSIONS)
def get_session(session_id):
    """
    Get a specific telehealth session with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        query = multi_tenant_query(TelehealthSession.query, tenant_id)
        session = query.filter_by(id=session_id).first()
        
        if not session:
            return jsonify({'error': 'Telehealth session not found'}), 404
        
        return jsonify(session.to_dict(include_details=True)), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve telehealth session', 'details': str(e)}), 500

@telemedicine_bp.route('/sessions', methods=['POST'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_CREATE_TELEHEALTH_SESSIONS)
def create_session():
    """
    Create a new telehealth session with tenant isolation and validation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['patient_id', 'type', 'scheduled_start', 'duration']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if patient belongs to the same tenant
        patient_query = multi_tenant_query(Patient.query, tenant_id)
        patient = patient_query.filter_by(id=data['patient_id']).first()
        if not patient:
            return jsonify({'error': 'Patient not found or access denied'}), 404
        
        # Parse datetime
        try:
            scheduled_start = datetime.fromisoformat(data['scheduled_start'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid scheduled_start format. Use ISO format.'}), 400
        
        # Validate session time (must be in future)
        if scheduled_start < datetime.utcnow():
            return jsonify({'error': 'Session must be scheduled in the future'}), 400
        
        # Check provider availability
        provider_id = data.get('provider_id', user_id)  # Default to current user
        
        # Verify provider belongs to tenant
        provider_query = multi_tenant_query(User.query, tenant_id)
        provider = provider_query.filter_by(id=provider_id).first()
        if not provider:
            return jsonify({'error': 'Provider not found or access denied'}), 404
        
        # Check for scheduling conflicts
        conflict_check = _check_scheduling_conflict(tenant_id, provider_id, scheduled_start, data['duration'])
        if conflict_check['has_conflict']:
            return jsonify({
                'error': 'Scheduling conflict detected',
                'conflicts': conflict_check['conflicting_sessions'],
                'available_slots': conflict_check['available_slots']
            }), 409
        
        # Create session
        session = TelehealthSession(
            tenant_id=tenant_id,
            patient_id=data['patient_id'],
            provider_id=provider_id,
            type=data['type'],
            scheduled_start=scheduled_start,
            duration=data['duration'],
            status='scheduled',
            created_by=user_id
        )
        
        # Optional fields
        optional_fields = [
            'title', 'description', 'notes', 'meeting_url', 'meeting_id',
            'meeting_password', 'recording_consent', 'billing_code'
        ]
        
        for field in optional_fields:
            if field in data:
                setattr(session, field, data[field])
        
        # Generate meeting details if not provided
        if not session.meeting_url:
            meeting_details = _generate_meeting_details(session)
            session.meeting_url = meeting_details['url']
            session.meeting_id = meeting_details['id']
            session.meeting_password = meeting_details['password']
        
        db.session.add(session)
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'create', 'telehealth_session', session.id, 
                           f'Telehealth session created for {patient.first_name} {patient.last_name}')
        
        # Send notifications (in real implementation)
        _send_session_notifications(session, 'created')
        
        return jsonify({
            'message': 'Telehealth session created successfully',
            'session': session.to_dict(include_details=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create telehealth session', 'details': str(e)}), 500

@telemedicine_bp.route('/sessions/<int:session_id>', methods=['PUT'])
@rate_limit(limit=50, period=3600)
@tenant_required
@permission_required(PERMISSION_EDIT_TELEHEALTH_SESSIONS)
def update_session(session_id):
    """
    Update an existing telehealth session with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(TelehealthSession.query, tenant_id)
        session = query.filter_by(id=session_id).first()
        
        if not session:
            return jsonify({'error': 'Telehealth session not found'}), 404
        
        # Check if session can be modified
        if session.status in ['in_progress', 'completed', 'cancelled']:
            return jsonify({'error': f'Cannot modify session with status: {session.status}'}), 400
        
        data = request.get_json()
        
        # Check for scheduling conflicts if time is being changed
        if 'scheduled_start' in data or 'duration' in data:
            new_start = datetime.fromisoformat(data['scheduled_start'].replace('Z', '+00:00')) if 'scheduled_start' in data else session.scheduled_start
            new_duration = data.get('duration', session.duration)
            
            conflict_check = _check_scheduling_conflict(tenant_id, session.provider_id, new_start, new_duration, session_id)
            if conflict_check['has_conflict']:
                return jsonify({
                    'error': 'Scheduling conflict detected',
                    'conflicts': conflict_check['conflicting_sessions'],
                    'available_slots': conflict_check['available_slots']
                }), 409
        
        # Update fields
        updateable_fields = [
            'title', 'description', 'type', 'scheduled_start', 'duration',
            'notes', 'meeting_url', 'meeting_id', 'meeting_password',
            'recording_consent', 'billing_code'
        ]
        
        changes = {}
        for field in updateable_fields:
            if field in data:
                old_value = getattr(session, field)
                new_value = data[field]
                
                if field == 'scheduled_start' and isinstance(new_value, str):
                    new_value = datetime.fromisoformat(new_value.replace('Z', '+00:00'))
                    if new_value < datetime.utcnow():
                        return jsonify({'error': 'Session must be scheduled in the future'}), 400
                
                if old_value != new_value:
                    setattr(session, field, new_value)
                    changes[field] = {'old': old_value, 'new': new_value}
        
        if changes:
            session.updated_by = user_id
            session.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Create audit trail entry
            _create_audit_trail(tenant_id, user_id, 'update', 'telehealth_session', session.id, 
                               f'Telehealth session updated: {changes}')
            
            # Send update notifications
            _send_session_notifications(session, 'updated')
        
        return jsonify({
            'message': 'Telehealth session updated successfully',
            'session': session.to_dict(include_details=True),
            'changes': changes if changes else 'No changes made'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update telehealth session', 'details': str(e)}), 500

@telemedicine_bp.route('/sessions/<int:session_id>/start', methods=['POST'])
@rate_limit(limit=30, period=3600)
@tenant_required
@permission_required(PERMISSION_JOIN_TELEHEALTH_SESSIONS)
def start_session(session_id):
    """
    Start a telehealth session
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(TelehealthSession.query, tenant_id)
        session = query.filter_by(id=session_id).first()
        
        if not session:
            return jsonify({'error': 'Telehealth session not found'}), 404
        
        if session.status != 'scheduled':
            return jsonify({'error': f'Cannot start session with status: {session.status}'}), 400
        
        # Check if user is authorized to start this session
        if user_id not in [session.provider_id, session.patient_id] and not current_user_obj.has_permission(PERMISSION_EDIT_TELEHEALTH_SESSIONS):
            return jsonify({'error': 'Not authorized to start this session'}), 403
        
        # Store old status for audit trail
        old_status = session.status
        
        session.status = 'in_progress'
        session.actual_start = datetime.utcnow()
        session.updated_by = user_id
        session.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'update', 'telehealth_session', session.id, 
                           'Telehealth session started')
        
        return jsonify({
            'message': 'Telehealth session started successfully',
            'session': session.to_dict(include_details=True),
            'meeting_details': {
                'url': session.meeting_url,
                'id': session.meeting_id,
                'password': session.meeting_password
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to start telehealth session', 'details': str(e)}), 500

@telemedicine_bp.route('/sessions/<int:session_id>/end', methods=['POST'])
@rate_limit(limit=30, period=3600)
@tenant_required
@permission_required(PERMISSION_JOIN_TELEHEALTH_SESSIONS)
def end_session(session_id):
    """
    End a telehealth session
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(TelehealthSession.query, tenant_id)
        session = query.filter_by(id=session_id).first()
        
        if not session:
            return jsonify({'error': 'Telehealth session not found'}), 404
        
        if session.status != 'in_progress':
            return jsonify({'error': f'Cannot end session with status: {session.status}'}), 400
        
        # Check if user is authorized to end this session
        if user_id not in [session.provider_id, session.patient_id] and not current_user_obj.has_permission(PERMISSION_EDIT_TELEHEALTH_SESSIONS):
            return jsonify({'error': 'Not authorized to end this session'}), 403
        
        data = request.get_json()
        
        # Store old status for audit trail
        old_status = session.status
        
        session.status = 'completed'
        session.actual_end = datetime.utcnow()
        session.notes = data.get('session_notes', session.notes)
        session.updated_by = user_id
        session.updated_at = datetime.utcnow()
        
        # Calculate actual duration
        if session.actual_start and session.actual_end:
            session.actual_duration = (session.actual_end - session.actual_start).total_seconds() / 60
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'update', 'telehealth_session', session.id, 
                           'Telehealth session completed')
        
        return jsonify({
            'message': 'Telehealth session ended successfully',
            'session': session.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to end telehealth session', 'details': str(e)}), 500

@telemedicine_bp.route('/sessions/<int:session_id>/cancel', methods=['POST'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_EDIT_TELEHEALTH_SESSIONS)
def cancel_session(session_id):
    """
    Cancel a telehealth session
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(TelehealthSession.query, tenant_id)
        session = query.filter_by(id=session_id).first()
        
        if not session:
            return jsonify({'error': 'Telehealth session not found'}), 404
        
        if session.status in ['completed', 'cancelled']:
            return jsonify({'error': f'Cannot cancel session with status: {session.status}'}), 400
        
        data = request.get_json()
        cancellation_reason = data.get('cancellation_reason', '')
        
        if not cancellation_reason:
            return jsonify({'error': 'Cancellation reason is required'}), 400
        
        # Store old status for audit trail
        old_status = session.status
        
        session.status = 'cancelled'
        session.cancelled_by = user_id
        session.cancellation_date = datetime.utcnow()
        session.cancellation_reason = cancellation_reason
        session.updated_by = user_id
        session.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'update', 'telehealth_session', session.id, 
                           f'Telehealth session cancelled. Reason: {cancellation_reason}')
        
        # Send cancellation notifications
        _send_session_notifications(session, 'cancelled')
        
        return jsonify({
            'message': 'Telehealth session cancelled successfully',
            'session': session.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to cancel telehealth session', 'details': str(e)}), 500

@telemedicine_bp.route('/sessions/<int:session_id>/join', methods=['POST'])
@rate_limit(limit=60, period=3600)
@tenant_required
@permission_required(PERMISSION_JOIN_TELEHEALTH_SESSIONS)
def join_session(session_id):
    """
    Join a telehealth session (get meeting details)
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(TelehealthSession.query, tenant_id)
        session = query.filter_by(id=session_id).first()
        
        if not session:
            return jsonify({'error': 'Telehealth session not found'}), 404
        
        # Check if user is authorized to join this session
        if user_id not in [session.provider_id, session.patient_id] and not current_user_obj.has_permission(PERMISSION_VIEW_TELEHEALTH_SESSIONS):
            return jsonify({'error': 'Not authorized to join this session'}), 403
        
        # Check session status
        if session.status not in ['scheduled', 'in_progress']:
            return jsonify({'error': f'Cannot join session with status: {session.status}'}), 400
        
        # Check if session is ready to start (within 15 minutes of scheduled time)
        time_until_start = (session.scheduled_start - datetime.utcnow()).total_seconds() / 60
        if time_until_start > 15 and session.status == 'scheduled':
            return jsonify({'error': 'Session is not ready to start yet'}), 400
        
        # Record join time for analytics
        if user_id == session.patient_id:
            session.patient_joined_at = datetime.utcnow()
        elif user_id == session.provider_id:
            session.provider_joined_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'join', 'telehealth_session', session.id, 
                           'Joined telehealth session')
        
        return jsonify({
            'message': 'Session join details retrieved successfully',
            'meeting_details': {
                'url': session.meeting_url,
                'id': session.meeting_id,
                'password': session.meeting_password,
                'session_status': session.status
            },
            'session_info': {
                'title': session.title,
                'patient_name': _get_patient_name(session.patient_id),
                'provider_name': _get_provider_name(session.provider_id),
                'scheduled_start': session.scheduled_start.isoformat()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to join telehealth session', 'details': str(e)}), 500

@telemedicine_bp.route('/availability', methods=['GET'])
@rate_limit(limit=80, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_TELEHEALTH_SESSIONS)
def check_availability():
    """
    Check provider availability for telehealth sessions
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        provider_id = request.args.get('provider_id', type=int)
        date_str = request.args.get('date')
        duration = request.args.get('duration', 30, type=int)
        
        if not provider_id or not date_str:
            return jsonify({'error': 'provider_id and date are required'}), 400
        
        try:
            target_date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use ISO format.'}), 400
        
        # Verify provider belongs to tenant
        provider_query = multi_tenant_query(User.query, tenant_id)
        provider = provider_query.filter_by(id=provider_id).first()
        if not provider:
            return jsonify({'error': 'Provider not found or access denied'}), 404
        
        availability = _get_provider_availability(tenant_id, provider_id, target_date, duration)
        
        return jsonify({
            'provider': {
                'id': provider.id,
                'name': f"{provider.first_name} {provider.last_name}",
                'specialty': provider.specialty
            },
            'date': target_date.isoformat(),
            'duration_minutes': duration,
            'availability': availability
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to check availability', 'details': str(e)}), 500

@telemedicine_bp.route('/stats', methods=['GET'])
@rate_limit(limit=60, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_TELEHEALTH_SESSIONS)
def get_telehealth_statistics():
    """
    Get telehealth statistics and analytics
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        days = int(request.args.get('days', 30))
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        stats = {
            'usage_metrics': _get_usage_metrics(tenant_id, start_date, end_date),
            'provider_metrics': _get_provider_metrics(tenant_id, start_date, end_date),
            'patient_engagement': _get_patient_engagement(tenant_id, start_date, end_date),
            'technical_metrics': _get_technical_metrics(tenant_id, start_date, end_date)
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve telehealth statistics', 'details': str(e)}), 500

# Helper functions with tenant filtering
def _get_sessions_summary(tenant_id: str, query: Any) -> Dict[str, Any]:
    """Get summary statistics for telehealth sessions"""
    total_sessions = query.count()
    
    # Count by status
    status_counts = query.with_entities(
        TelehealthSession.status, db.func.count(TelehealthSession.id)
    ).group_by(TelehealthSession.status).all()
    
    # Count upcoming sessions
    upcoming_sessions = query.filter(
        TelehealthSession.scheduled_start >= datetime.utcnow(),
        TelehealthSession.status == 'scheduled'
    ).count()
    
    return {
        'total_sessions': total_sessions,
        'status_breakdown': {status: count for status, count in status_counts},
        'upcoming_sessions': upcoming_sessions
    }

def _check_scheduling_conflict(tenant_id: str, provider_id: int, start_time: datetime, duration: int, exclude_session_id: int = None) -> Dict[str, Any]:
    """Check for scheduling conflicts"""
    end_time = start_time + timedelta(minutes=duration)
    
    query = multi_tenant_query(TelehealthSession.query, tenant_id)
    conflicting_sessions = query.filter(
        TelehealthSession.provider_id == provider_id,
        TelehealthSession.status.in_(['scheduled', 'in_progress']),
        db.or_(
            db.and_(TelehealthSession.scheduled_start < end_time, 
                   TelehealthSession.scheduled_start + db.func.make_interval(mins=TelehealthSession.duration) > start_time)
        )
    )
    
    if exclude_session_id:
        conflicting_sessions = conflicting_sessions.filter(TelehealthSession.id != exclude_session_id)
    
    conflicts = conflicting_sessions.all()
    
    return {
        'has_conflict': len(conflicts) > 0,
        'conflicting_sessions': [session.to_dict() for session in conflicts],
        'available_slots': _get_available_slots(tenant_id, provider_id, start_time.date(), duration) if conflicts else []
    }

def _get_available_slots():
    pass

def _generate_meeting_details(session: TelehealthSession) -> Dict[str, str]:
    """Generate meeting details for telehealth session"""
    # In production, this would integrate with video conferencing APIs like Zoom, Twilio, etc.
    # For now, generate placeholder details
    import secrets
    import string
    
    meeting_id = ''.join(secrets.choice(string.digits) for _ in range(9))
    password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
    
    return {
        'url': f"https://telehealth.example.com/join/{meeting_id}",
        'id': meeting_id,
        'password': password
    }

def _send_session_notifications(session: TelehealthSession, action: str):
    """Send notifications for session actions"""
    # This would integrate with your notification system
    # Placeholder implementation
    pass

def _create_audit_trail(tenant_id: str, user_id: int, action: str, resource_type: str, resource_id: int, details: str):
    """Create an audit trail entry"""
    from ..models import AuditTrail
    
    audit_entry = AuditTrail(
        tenant_id=tenant_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    
    db.session.add(audit_entry)

def _get_provider_availability(tenant_id: str, provider_id: int, date: date, duration: int) -> List[Dict]:
    """Get provider availability for a specific date"""
    # This would consider working hours, existing appointments, etc.
    # Simplified implementation for demonstration
    
    start_of_day = datetime.combine(date, datetime.min.time())
    end_of_day = datetime.combine(date, datetime.max.time())
    
    query = multi_tenant_query(TelehealthSession.query, tenant_id)
    booked_sessions = query.filter(
        TelehealthSession.provider_id == provider_id,
        TelehealthSession.scheduled_start.between(start_of_day, end_of_day),
        TelehealthSession.status.in_(['scheduled', 'in_progress'])
    ).order_by(TelehealthSession.scheduled_start).all()
    
    # Generate available slots (simplified)
    available_slots = []
    current_time = datetime.combine(date, datetime.strptime('09:00', '%H:%M').time())
    end_time = datetime.combine(date, datetime.strptime('17:00', '%H:%M').time())
    
    while current_time + timedelta(minutes=duration) <= end_time:
        slot_end = current_time + timedelta(minutes=duration)
        slot_available = True
        
        for session in booked_sessions:
            session_end = session.scheduled_start + timedelta(minutes=session.duration)
            if not (slot_end <= session.scheduled_start or current_time >= session_end):
                slot_available = False
                break
        
        if slot_available:
            available_slots.append({
                'start_time': current_time.isoformat(),
                'end_time': slot_end.isoformat(),
                'duration_minutes': duration
            })
        
        current_time += timedelta(minutes=15)  # Check every 15 minutes
    
    return available_slots

def _get_patient_name(patient_id: int) -> str:
    """Get patient name by ID"""
    patient = Patient.query.get(patient_id)
    return f"{patient.first_name} {patient.last_name}" if patient else "Unknown Patient"

def _get_provider_name(provider_id: int) -> str:
    """Get provider name by ID"""
    provider = User.query.get(provider_id)
    return f"Dr. {provider.first_name} {provider.last_name}" if provider else "Unknown Provider"

def _get_usage_metrics(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get telehealth usage metrics"""
    query = multi_tenant_query(TelehealthSession.query, tenant_id)
    sessions = query.filter(TelehealthSession.created_at.between(start_date, end_date))
    
    total_sessions = sessions.count()
    completed_sessions = sessions.filter_by(status='completed').count()
    average_duration = sessions.filter(
        TelehealthSession.actual_duration.isnot(None)
    ).with_entities(db.func.avg(TelehealthSession.actual_duration)).scalar()
    
    return {
        'total_sessions': total_sessions,
        'completed_sessions': completed_sessions,
        'completion_rate': (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0,
        'average_duration_minutes': float(average_duration) if average_duration else 0
    }

def _get_provider_metrics(tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
    """Get provider telehealth metrics"""
    query = multi_tenant_query(TelehealthSession.query.join(User), tenant_id)
    provider_metrics = query.filter(TelehealthSession.created_at.between(start_date, end_date))\
                          .group_by(User.id, User.first_name, User.last_name)\
                          .with_entities(
                              User.id,
                              User.first_name,
                              User.last_name,
                              db.func.count(TelehealthSession.id),
                              db.func.avg(TelehealthSession.actual_duration)
                          ).all()
    
    return [{
        'provider_id': provider_id,
        'provider_name': f"{first_name} {last_name}",
        'session_count': count,
        'average_duration_minutes': float(avg_duration) if avg_duration else 0
    } for provider_id, first_name, last_name, count, avg_duration in provider_metrics]

def _get_patient_engagement(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get patient engagement metrics"""
    query = multi_tenant_query(TelehealthSession.query, tenant_id)
    sessions = query.filter(TelehealthSession.created_at.between(start_date, end_date))
    
    unique_patients = sessions.distinct(TelehealthSession.patient_id).count()
    sessions_with_join = sessions.filter(TelehealthSession.patient_joined_at.isnot(None)).count()
    
    return {
        'unique_patients': unique_patients,
        'sessions_with_patient_join': sessions_with_join,
        'patient_join_rate': (sessions_with_join / sessions.count() * 100) if sessions.count() > 0 else 0
    }

def _get_technical_metrics(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get technical metrics for telehealth"""
    # This would typically include connection quality, etc.
    # Placeholder implementation
    return {
        'average_connection_quality': 4.5,
        'failed_sessions': 0,
        'technical_issue_rate': 0.0
    }

@telemedicine_bp.errorhandler(403)
def handle_permission_error(e):
    return jsonify({'error': 'Access forbidden', 'message': 'Insufficient permissions'}), 403

@telemedicine_bp.errorhandler(401)
def handle_authentication_error(e):
    return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401

@telemedicine_bp.errorhandler(429)
def handle_rate_limit_error(e):
    return jsonify({'error': 'Rate limit exceeded', 'message': 'Too many requests'}), 429