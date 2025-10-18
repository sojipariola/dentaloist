# routes/appointments.py
from flask import Blueprint, request, jsonify
from flask_login import current_user
from datetime import timedelta, datetime, date
from typing import Dict, Any, List, Optional
from sqlalchemy import and_, or_

# Import auth and tenancy utilities
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit

from ..models import Appointment, Patient, User, db

appointments_bp = Blueprint('appointments', __name__, url_prefix='/api/appointments')

# RBAC Permission Constants
PERMISSION_VIEW_APPOINTMENTS = 'view_appointments'
PERMISSION_CREATE_APPOINTMENTS = 'create_appointments'
PERMISSION_EDIT_APPOINTMENTS = 'edit_appointments'
PERMISSION_DELETE_APPOINTMENTS = 'delete_appointments'
PERMISSION_MANAGE_APPOINTMENTS = 'manage_appointments'

@appointments_bp.route('/', methods=['GET'])
@rate_limit(limit=100, period=3600)  # 100 requests per hour
@tenant_required
@permission_required(PERMISSION_VIEW_APPOINTMENTS)
def get_appointments():
    """
    Get appointments with advanced filtering, sorting, and tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)  # Cap at 100 per page
        
        # Filter parameters
        status = request.args.get('status')
        patient_id = request.args.get('patient_id', type=int)
        dentist_id = request.args.get('dentist_id', type=int)
        appointment_type = request.args.get('type')
        priority = request.args.get('priority')
        
        # Date range filtering
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        # Build base query with tenant filtering
        query = multi_tenant_query(Appointment.query, tenant_id)
        
        # Apply filters
        if status:
            query = query.filter(Appointment.status == status)
        if patient_id:
            query = query.filter(Appointment.patient_id == patient_id)
        if dentist_id:
            query = query.filter(Appointment.dentist_id == dentist_id)
        if appointment_type:
            query = query.filter(Appointment.type == appointment_type)
        if priority:
            query = query.filter(Appointment.priority == priority)
        
        # Date range filtering
        if start_date_str:
            try:
                start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                query = query.filter(Appointment.start_time >= start_date)
            except ValueError:
                return jsonify({'error': 'Invalid start_date format. Use ISO format.'}), 400
        
        if end_date_str:
            try:
                end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                query = query.filter(Appointment.start_time <= end_date)
            except ValueError:
                return jsonify({'error': 'Invalid end_date format. Use ISO format.'}), 400
        
        # Sorting
        sort_by = request.args.get('sort_by', 'start_time')
        sort_order = request.args.get('sort_order', 'desc')
        
        if sort_order.lower() == 'asc':
            query = query.order_by(getattr(Appointment, sort_by).asc())
        else:
            query = query.order_by(getattr(Appointment, sort_by).desc())
        
        # Pagination
        appointments = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'appointments': [appt.to_dict() for appt in appointments.items],
            'pagination': {
                'page': appointments.page,
                'per_page': appointments.per_page,
                'total': appointments.total,
                'pages': appointments.pages,
                'has_next': appointments.has_next,
                'has_prev': appointments.has_prev
            },
            'filters': {
                'status': status,
                'patient_id': patient_id,
                'dentist_id': dentist_id,
                'type': appointment_type,
                'priority': priority,
                'start_date': start_date_str,
                'end_date': end_date_str
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve appointments', 'details': str(e)}), 500

@appointments_bp.route('/<int:appointment_id>', methods=['GET'])
@rate_limit(limit=120, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_APPOINTMENTS)
def get_appointment(appointment_id):
    """
    Get a specific appointment with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        query = multi_tenant_query(Appointment.query, tenant_id)
        appointment = query.filter_by(id=appointment_id).first()
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        return jsonify(appointment.to_dict(include_details=True)), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve appointment', 'details': str(e)}), 500

@appointments_bp.route('/today', methods=['GET'])
@rate_limit(limit=80, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_APPOINTMENTS)
def get_today_appointments():
    """
    Get today's appointments for the tenant
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        # Get today's date
        today = datetime.now().date()
        
        # Query appointments for today with tenant filtering
        query = multi_tenant_query(Appointment.query, tenant_id)
        appointments = query.filter(
            db.func.date(Appointment.start_time) == today
        ).order_by(Appointment.start_time.asc()).all()
        
        appointments_data = []
        for appointment in appointments:
            appointments_data.append({
                'id': appointment.id,
                'title': appointment.title,
                'description': appointment.description,
                'type': appointment.type,
                'status': appointment.status,
                'start_time': appointment.start_time.isoformat() if appointment.start_time else None,
                'end_time': appointment.end_time.isoformat() if appointment.end_time else None,
                'duration': appointment.duration,
                'patient': {
                    'id': appointment.patient.id,
                    'first_name': appointment.patient.first_name,
                    'last_name': appointment.patient.last_name,
                    'email': appointment.patient.email,
                    'phone': appointment.patient.phone
                } if appointment.patient else None,
                'dentist': {
                    'id': appointment.dentist.id,
                    'first_name': appointment.dentist.first_name,
                    'last_name': appointment.dentist.last_name,
                    'specialty': appointment.dentist.specialty
                } if appointment.dentist else None,
                'room': appointment.room,
                'priority': appointment.priority,
                'cost': float(appointment.cost) if appointment.cost else None,
                'payment_status': appointment.payment_status
            })
        
        return jsonify(appointments_data), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve today\'s appointments', 'details': str(e)}), 500

@appointments_bp.route('/upcoming', methods=['GET'])
@rate_limit(limit=80, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_APPOINTMENTS)
def get_upcoming_appointments():
    """
    Get upcoming appointments (next 7 days) for the tenant
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        # Get current datetime
        now = datetime.now()
        
        # Query upcoming appointments (next 7 days) with tenant filtering
        upcoming_start = now
        upcoming_end = now + timedelta(days=7)
        
        query = multi_tenant_query(Appointment.query, tenant_id)
        appointments = query.filter(
            Appointment.start_time >= upcoming_start,
            Appointment.start_time <= upcoming_end
        ).order_by(Appointment.start_time.asc()).all()
        
        appointments_data = []
        for appointment in appointments:
            appointments_data.append({
                'id': appointment.id,
                'title': appointment.title,
                'description': appointment.description,
                'type': appointment.type,
                'status': appointment.status,
                'start_time': appointment.start_time.isoformat() if appointment.start_time else None,
                'end_time': appointment.end_time.isoformat() if appointment.end_time else None,
                'duration': appointment.duration,
                'patient': {
                    'id': appointment.patient.id,
                    'first_name': appointment.patient.first_name,
                    'last_name': appointment.patient.last_name,
                    'email': appointment.patient.email
                } if appointment.patient else None,
                'dentist': {
                    'id': appointment.dentist.id,
                    'first_name': appointment.dentist.first_name,
                    'last_name': appointment.dentist.last_name
                } if appointment.dentist else None,
                'room': appointment.room,
                'priority': appointment.priority,
                'cost': float(appointment.cost) if appointment.cost else None,
                'payment_status': appointment.payment_status
            })
        
        return jsonify(appointments_data), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve upcoming appointments', 'details': str(e)}), 500

@appointments_bp.route('/availability', methods=['GET'])
@rate_limit(limit=50, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_APPOINTMENTS)
def check_availability():
    """
    Check appointment availability for a dentist and time slot
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        dentist_id = request.args.get('dentist_id', type=int)
        start_time_str = request.args.get('start_time')
        duration = request.args.get('duration', type=int)
        appointment_id = request.args.get('appointment_id', type=int)  # For editing existing appointment
        
        if not dentist_id or not start_time_str:
            return jsonify({'error': 'dentist_id and start_time are required'}), 400
        
        try:
            start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid start_time format. Use ISO format.'}), 400
        
        if not duration:
            duration = 30  # Default duration in minutes
        
        end_time = start_time + timedelta(minutes=duration)
        
        # Check for overlapping appointments with tenant filtering
        query = multi_tenant_query(Appointment.query, tenant_id)
        overlapping_appointments = query.filter(
            Appointment.dentist_id == dentist_id,
            Appointment.status.notin_(['cancelled', 'completed']),
            or_(
                and_(Appointment.start_time < end_time, Appointment.end_time > start_time),
                Appointment.start_time.between(start_time, end_time),
                Appointment.end_time.between(start_time, end_time)
            )
        )
        
        # Exclude current appointment if editing
        if appointment_id:
            overlapping_appointments = overlapping_appointments.filter(Appointment.id != appointment_id)
        
        is_available = overlapping_appointments.count() == 0
        
        # Get available time slots for the day if requested
        available_slots = []
        if request.args.get('get_slots') == 'true':
            available_slots = _get_available_slots(tenant_id, dentist_id, start_time.date(), duration)
        
        return jsonify({
            'available': is_available,
            'overlapping_appointments': [appt.to_dict() for appt in overlapping_appointments.all()] if not is_available else [],
            'requested_slot': {
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'duration_minutes': duration
            },
            'available_slots': available_slots
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to check availability', 'details': str(e)}), 500

@appointments_bp.route('/', methods=['POST'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_CREATE_APPOINTMENTS)
def create_appointment():
    """
    Create a new appointment with tenant isolation and validation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['patient_id', 'dentist_id', 'title', 'type', 'start_time']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if patient and dentist belong to the same tenant
        patient_query = multi_tenant_query(Patient.query, tenant_id)
        patient = patient_query.filter_by(id=data['patient_id']).first()
        if not patient:
            return jsonify({'error': 'Patient not found or access denied'}), 404
        
        dentist_query = multi_tenant_query(User.query, tenant_id)
        dentist = dentist_query.filter_by(id=data['dentist_id']).first()
        if not dentist:
            return jsonify({'error': 'Dentist not found or access denied'}), 404
        
        # Parse datetime
        try:
            start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00')) if data.get('end_time') else None
        except ValueError:
            return jsonify({'error': 'Invalid datetime format. Use ISO format.'}), 400
        
        # Calculate duration if not provided
        duration = data.get('duration')
        if not duration and end_time:
            duration = (end_time - start_time).total_seconds() / 60  # Convert to minutes
        
        # Check availability
        availability_check = _check_availability(tenant_id, data['dentist_id'], start_time, duration or 30)
        if not availability_check['available']:
            return jsonify({
                'error': 'Time slot not available',
                'conflicts': availability_check['conflicts'],
                'available_slots': availability_check['available_slots']
            }), 409
        
        # Create appointment
        appointment = Appointment(
            tenant_id=tenant_id,
            patient_id=data['patient_id'],
            dentist_id=data['dentist_id'],
            title=data['title'],
            type=data['type'],
            start_time=start_time,
            end_time=end_time,
            duration=duration or 30,
            created_by=user_id
        )
        
        # Optional fields
        optional_fields = ['description', 'room', 'priority', 'cost', 'payment_status']
        for field in optional_fields:
            if field in data:
                setattr(appointment, field, data[field])
        
        db.session.add(appointment)
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'create', 'appointment', appointment.id, 'Appointment created')
        
        return jsonify({
            'message': 'Appointment created successfully',
            'appointment': appointment.to_dict(include_details=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create appointment', 'details': str(e)}), 500

@appointments_bp.route('/<int:appointment_id>', methods=['PUT'])
@rate_limit(limit=50, period=3600)
@tenant_required
@permission_required(PERMISSION_EDIT_APPOINTMENTS)
def update_appointment(appointment_id):
    """
    Update an existing appointment with tenant isolation and validation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(Appointment.query, tenant_id)
        appointment = query.filter_by(id=appointment_id).first()
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        data = request.get_json()
        
        # Check if patient and dentist belong to the same tenant if being updated
        if 'patient_id' in data:
            patient_query = multi_tenant_query(Patient.query, tenant_id)
            patient = patient_query.filter_by(id=data['patient_id']).first()
            if not patient:
                return jsonify({'error': 'Patient not found or access denied'}), 404
        
        if 'dentist_id' in data:
            dentist_query = multi_tenant_query(User.query, tenant_id)
            dentist = dentist_query.filter_by(id=data['dentist_id']).first()
            if not dentist:
                return jsonify({'error': 'Dentist not found or access denied'}), 404
        
        # Check availability if time is being changed
        if 'start_time' in data or 'duration' in data:
            new_start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00')) if 'start_time' in data else appointment.start_time
            new_duration = data.get('duration', appointment.duration)
            
            availability_check = _check_availability(tenant_id, data.get('dentist_id', appointment.dentist_id), new_start_time, new_duration, appointment_id)
            if not availability_check['available']:
                return jsonify({
                    'error': 'Time slot not available',
                    'conflicts': availability_check['conflicts'],
                    'available_slots': availability_check['available_slots']
                }), 409
        
        # Update fields
        updateable_fields = [
            'title', 'description', 'type', 'status', 'start_time', 'end_time',
            'duration', 'room', 'priority', 'patient_id', 'dentist_id', 'cost',
            'payment_status'
        ]
        
        changes = {}
        for field in updateable_fields:
            if field in data:
                old_value = getattr(appointment, field)
                new_value = data[field]
                
                if field in ['start_time', 'end_time'] and isinstance(new_value, str):
                    new_value = datetime.fromisoformat(new_value.replace('Z', '+00:00'))
                
                if old_value != new_value:
                    setattr(appointment, field, new_value)
                    changes[field] = {'old': old_value, 'new': new_value}
        
        if changes:
            appointment.updated_by = user_id
            appointment.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Create audit trail entry
            _create_audit_trail(tenant_id, user_id, 'update', 'appointment', appointment.id, f'Appointment updated: {changes}')
        
        return jsonify({
            'message': 'Appointment updated successfully',
            'appointment': appointment.to_dict(include_details=True),
            'changes': changes if changes else 'No changes made'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update appointment', 'details': str(e)}), 500

@appointments_bp.route('/<int:appointment_id>', methods=['DELETE'])
@rate_limit(limit=30, period=3600)
@tenant_required
@permission_required(PERMISSION_DELETE_APPOINTMENTS)
def delete_appointment(appointment_id):
    """
    Delete an appointment with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(Appointment.query, tenant_id)
        appointment = query.filter_by(id=appointment_id).first()
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Create audit trail before deletion
        _create_audit_trail(tenant_id, user_id, 'delete', 'appointment', appointment.id, 'Appointment deleted')
        
        db.session.delete(appointment)
        db.session.commit()
        
        return jsonify({'message': 'Appointment deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete appointment', 'details': str(e)}), 500

@appointments_bp.route('/<int:appointment_id>/cancel', methods=['POST'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_MANAGE_APPOINTMENTS)
def cancel_appointment(appointment_id):
    """
    Cancel an appointment with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(Appointment.query, tenant_id)
        appointment = query.filter_by(id=appointment_id).first()
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        if appointment.status == 'cancelled':
            return jsonify({'error': 'Appointment is already cancelled'}), 400
        
        data = request.get_json()
        
        # Store old status for audit trail
        old_status = appointment.status
        
        appointment.status = 'cancelled'
        appointment.cancellation_reason = data.get('reason')
        appointment.cancellation_date = datetime.utcnow()
        appointment.cancelled_by = user_id
        appointment.updated_by = user_id
        appointment.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'update', 'appointment', appointment.id, 
                           f'Appointment cancelled. Reason: {data.get("reason", "No reason provided")}. Old status: {old_status}')
        
        return jsonify({
            'message': 'Appointment cancelled successfully',
            'appointment': appointment.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to cancel appointment', 'details': str(e)}), 500

@appointments_bp.route('/<int:appointment_id>/complete', methods=['POST'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_MANAGE_APPOINTMENTS)
def complete_appointment(appointment_id):
    """
    Mark an appointment as completed with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(Appointment.query, tenant_id)
        appointment = query.filter_by(id=appointment_id).first()
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        if appointment.status == 'completed':
            return jsonify({'error': 'Appointment is already completed'}), 400
        
        # Store old status for audit trail
        old_status = appointment.status
        
        appointment.status = 'completed'
        appointment.completed_at = datetime.utcnow()
        appointment.updated_by = user_id
        appointment.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'update', 'appointment', appointment.id, 
                           f'Appointment completed. Old status: {old_status}')
        
        return jsonify({
            'message': 'Appointment marked as completed',
            'appointment': appointment.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to complete appointment', 'details': str(e)}), 500

# Helper functions with tenant filtering
def _check_availability(tenant_id: str, dentist_id: int, start_time: datetime, duration: int, exclude_appointment_id: int = None) -> Dict[str, Any]:
    """Check appointment availability for a dentist"""
    end_time = start_time + timedelta(minutes=duration)
    
    query = multi_tenant_query(Appointment.query, tenant_id)
    overlapping_appointments = query.filter(
        Appointment.dentist_id == dentist_id,
        Appointment.status.notin_(['cancelled', 'completed']),
        or_(
            and_(Appointment.start_time < end_time, Appointment.end_time > start_time),
            Appointment.start_time.between(start_time, end_time),
            Appointment.end_time.between(start_time, end_time)
        )
    )
    
    if exclude_appointment_id:
        overlapping_appointments = overlapping_appointments.filter(Appointment.id != exclude_appointment_id)
    
    conflicts = overlapping_appointments.all()
    
    return {
        'available': len(conflicts) == 0,
        'conflicts': [appt.to_dict() for appt in conflicts],
        'available_slots': _get_available_slots(tenant_id, dentist_id, start_time.date(), duration) if conflicts else []
    }

def _get_available_slots(tenant_id: str, dentist_id: int, date: date, duration: int) -> List[Dict]:
    """Get available time slots for a dentist on a specific date"""
    # This is a simplified implementation
    # In production, you'd consider working hours, breaks, etc.
    
    start_of_day = datetime.combine(date, datetime.min.time())
    end_of_day = datetime.combine(date, datetime.max.time())
    
    query = multi_tenant_query(Appointment.query, tenant_id)
    booked_appointments = query.filter(
        Appointment.dentist_id == dentist_id,
        Appointment.status.notin_(['cancelled', 'completed']),
        Appointment.start_time.between(start_of_day, end_of_day)
    ).order_by(Appointment.start_time).all()
    
    # Generate available slots (simplified)
    available_slots = []
    current_time = datetime.combine(date, datetime.strptime('09:00', '%H:%M').time())
    end_time = datetime.combine(date, datetime.strptime('17:00', '%H:%M').time())
    
    while current_time + timedelta(minutes=duration) <= end_time:
        slot_end = current_time + timedelta(minutes=duration)
        slot_available = True
        
        for appt in booked_appointments:
            if not (slot_end <= appt.start_time or current_time >= appt.end_time):
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
    db.session.commit()

