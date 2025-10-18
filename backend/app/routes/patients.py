# routes/patients.py
from flask import Blueprint, request, jsonify
from flask_login import current_user
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy import or_, and_

# Import auth and tenancy utilities
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit

from ..models import Patient, Appointment, Treatment, Invoice, db

patients_bp = Blueprint('patients', __name__, url_prefix='/api/patients')

# RBAC Permission Constants
PERMISSION_VIEW_PATIENTS = 'view_patients'
PERMISSION_CREATE_PATIENTS = 'create_patients'
PERMISSION_EDIT_PATIENTS = 'edit_patients'
PERMISSION_DELETE_PATIENTS = 'delete_patients'
PERMISSION_VIEW_PATIENT_MEDICAL_HISTORY = 'view_patient_medical_history'
PERMISSION_MANAGE_PATIENT_MEDICAL_HISTORY = 'manage_patient_medical_history'

@patients_bp.route('/', methods=['GET'])
@rate_limit(limit=100, period=3600)  # 100 requests per hour
@tenant_required
@permission_required(PERMISSION_VIEW_PATIENTS)
def get_patients():
    """
    Get patients with advanced filtering, sorting, and tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)  # Cap at 100 per page
        
        # Filter parameters
        search = request.args.get('search')
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        gender = request.args.get('gender')
        min_age = request.args.get('min_age', type=int)
        max_age = request.args.get('max_age', type=int)
        
        # Build base query with tenant filtering
        query = multi_tenant_query(Patient.query, tenant_id)
        
        # Apply filters
        if search:
            query = query.filter(
                or_(
                    Patient.first_name.ilike(f'%{search}%'),
                    Patient.last_name.ilike(f'%{search}%'),
                    Patient.email.ilike(f'%{search}%'),
                    Patient.phone.ilike(f'%{search}%'),
                    Patient.patient_id.ilike(f'%{search}%')  # Assuming patient_id field exists
                )
            )
        
        if active_only:
            query = query.filter(Patient.is_active == True)
        
        if gender:
            query = query.filter(Patient.gender == gender)
        
        # Age filtering
        if min_age or max_age:
            today = datetime.utcnow().date()
            if max_age:
                min_birth_date = today - timedelta(days=(max_age + 1) * 365)
                query = query.filter(Patient.date_of_birth >= min_birth_date)
            if min_age:
                max_birth_date = today - timedelta(days=min_age * 365)
                query = query.filter(Patient.date_of_birth <= max_birth_date)
        
        # Sorting
        sort_by = request.args.get('sort_by', 'last_name')
        sort_order = request.args.get('sort_order', 'asc')
        
        if sort_order.lower() == 'desc':
            query = query.order_by(getattr(Patient, sort_by).desc())
        else:
            query = query.order_by(getattr(Patient, sort_by).asc())
        
        # Pagination
        patients = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'patients': [patient.to_dict() for patient in patients.items],
            'pagination': {
                'page': patients.page,
                'per_page': patients.per_page,
                'total': patients.total,
                'pages': patients.pages,
                'has_next': patients.has_next,
                'has_prev': patients.has_prev
            },
            'filters': {
                'search': search,
                'active_only': active_only,
                'gender': gender,
                'min_age': min_age,
                'max_age': max_age
            },
            'summary': _get_patients_summary(tenant_id, query)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve patients', 'details': str(e)}), 500

@patients_bp.route('/<int:patient_id>', methods=['GET'])
@rate_limit(limit=120, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_PATIENTS)
def get_patient(patient_id):
    """
    Get a specific patient with comprehensive details and tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        query = multi_tenant_query(Patient.query, tenant_id)
        patient = query.filter_by(id=patient_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Get patient data with related information
        patient_data = patient.to_dict(include_details=True)
        
        # Add related data based on permissions
        if current_user_obj.has_permission(PERMISSION_VIEW_PATIENTS):
            patient_data['appointments'] = _get_patient_appointments(tenant_id, patient_id)
            patient_data['recent_treatments'] = _get_recent_treatments(tenant_id, patient_id)
            patient_data['financial_summary'] = _get_financial_summary(tenant_id, patient_id)
        
        if current_user_obj.has_permission(PERMISSION_VIEW_PATIENT_MEDICAL_HISTORY):
            patient_data['medical_history'] = _get_medical_history(tenant_id, patient_id)
        
        return jsonify(patient_data), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve patient', 'details': str(e)}), 500

@patients_bp.route('/', methods=['POST'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_CREATE_PATIENTS)
def create_patient():
    """
    Create a new patient with tenant isolation and validation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['first_name', 'last_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check for duplicate patients (same name + email/phone)
        duplicate_check = _check_duplicate_patient(tenant_id, data)
        if duplicate_check['is_duplicate']:
            return jsonify({
                'error': 'Potential duplicate patient found',
                'existing_patients': duplicate_check['existing_patients'],
                'suggestion': 'Please verify if this is a new patient or use the existing patient record'
            }), 409
        
        # Create patient
        patient = Patient(
            tenant_id=tenant_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data.get('email'),
            phone=data.get('phone'),
            date_of_birth=_parse_date(data.get('date_of_birth')),
            gender=data.get('gender'),
            created_by=user_id
        )
        
        # Optional fields
        optional_fields = [
            'address', 'city', 'state', 'zip_code', 'country',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation',
            'insurance_provider', 'insurance_id', 'primary_care_physician',
            'allergies', 'medications', 'medical_conditions'
        ]
        
        for field in optional_fields:
            if field in data:
                setattr(patient, field, data[field])
        
        db.session.add(patient)
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'create', 'patient', patient.id, 
                           f'Patient created: {patient.first_name} {patient.last_name}')
        
        return jsonify({
            'message': 'Patient created successfully',
            'patient': patient.to_dict(include_details=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create patient', 'details': str(e)}), 500

@patients_bp.route('/<int:patient_id>', methods=['PUT'])
@rate_limit(limit=50, period=3600)
@tenant_required
@permission_required(PERMISSION_EDIT_PATIENTS)
def update_patient(patient_id):
    """
    Update an existing patient with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(Patient.query, tenant_id)
        patient = query.filter_by(id=patient_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        data = request.get_json()
        
        # Update fields with validation
        updateable_fields = [
            'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender',
            'address', 'city', 'state', 'zip_code', 'country',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation',
            'insurance_provider', 'insurance_id', 'primary_care_physician',
            'allergies', 'medications', 'medical_conditions', 'is_active'
        ]
        
        changes = {}
        for field in updateable_fields:
            if field in data:
                old_value = getattr(patient, field)
                new_value = data[field]
                
                # Handle date fields
                if field == 'date_of_birth':
                    new_value = _parse_date(new_value)
                
                if old_value != new_value:
                    setattr(patient, field, new_value)
                    changes[field] = {'old': old_value, 'new': new_value}
        
        if changes:
            patient.updated_by = user_id
            patient.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Create audit trail entry
            _create_audit_trail(tenant_id, user_id, 'update', 'patient', patient.id, 
                               f'Patient updated: {changes}')
        
        return jsonify({
            'message': 'Patient updated successfully',
            'patient': patient.to_dict(include_details=True),
            'changes': changes if changes else 'No changes made'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update patient', 'details': str(e)}), 500

@patients_bp.route('/<int:patient_id>/medical-history', methods=['GET', 'POST', 'PUT'])
@rate_limit(limit=60, period=3600)
@tenant_required
def manage_medical_history(patient_id):
    """
    Manage patient medical history with proper permission checks
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        query = multi_tenant_query(Patient.query, tenant_id)
        patient = query.filter_by(id=patient_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        if request.method == 'GET':
            if not current_user_obj.has_permission(PERMISSION_VIEW_PATIENT_MEDICAL_HISTORY):
                return jsonify({'error': 'Insufficient permissions to view medical history'}), 403
            
            medical_history = _get_medical_history(tenant_id, patient_id)
            return jsonify(medical_history), 200
        
        elif request.method in ['POST', 'PUT']:
            if not current_user_obj.has_permission(PERMISSION_MANAGE_PATIENT_MEDICAL_HISTORY):
                return jsonify({'error': 'Insufficient permissions to manage medical history'}), 403
            
            data = request.get_json()
            
            # Update medical history fields
            medical_fields = [
                'allergies', 'medications', 'medical_conditions',
                'surgical_history', 'family_history', 'social_history',
                'dental_history', 'habits'
            ]
            
            changes = {}
            for field in medical_fields:
                if field in data:
                    old_value = getattr(patient, field, None)
                    new_value = data[field]
                    
                    if old_value != new_value:
                        setattr(patient, field, new_value)
                        changes[field] = {'old': old_value, 'new': new_value}
            
            if changes:
                patient.updated_by = current_user_obj.id
                patient.updated_at = datetime.utcnow()
                
                db.session.commit()
                
                # Create audit trail entry
                _create_audit_trail(tenant_id, current_user_obj.id, 'update', 'medical_history', patient.id, 
                                   'Medical history updated')
            
            return jsonify({
                'message': 'Medical history updated successfully',
                'changes': changes if changes else 'No changes made'
            }), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to manage medical history', 'details': str(e)}), 500

@patients_bp.route('/<int:patient_id>', methods=['DELETE'])
@rate_limit(limit=30, period=3600)
@tenant_required
@permission_required(PERMISSION_DELETE_PATIENTS)
def delete_patient(patient_id):
    """
    Delete (deactivate) a patient with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(Patient.query, tenant_id)
        patient = query.filter_by(id=patient_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Check if patient has active appointments
        active_appointments = multi_tenant_query(Appointment.query, tenant_id).filter(
            Appointment.patient_id == patient_id,
            Appointment.status.in_(['scheduled', 'confirmed'])
        ).count()
        
        if active_appointments > 0:
            return jsonify({
                'error': f'Cannot deactivate patient with {active_appointments} active appointments'
            }), 409
        
        # Check if patient has outstanding invoices
        outstanding_invoices = multi_tenant_query(Invoice.query, tenant_id).filter(
            Invoice.patient_id == patient_id,
            Invoice.status.in_(['pending', 'overdue'])
        ).count()
        
        if outstanding_invoices > 0:
            return jsonify({
                'error': f'Cannot deactivate patient with {outstanding_invoices} outstanding invoices'
            }), 409
        
        # Soft delete (deactivate)
        patient.is_active = False
        patient.deactivated_by = user_id
        patient.deactivated_at = datetime.utcnow()
        patient.updated_by = user_id
        patient.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'update', 'patient', patient.id, 
                           f'Patient deactivated: {patient.first_name} {patient.last_name}')
        
        return jsonify({
            'message': 'Patient deactivated successfully',
            'patient': patient.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to deactivate patient', 'details': str(e)}), 500

@patients_bp.route('/<int:patient_id>/reactivate', methods=['POST'])
@rate_limit(limit=30, period=3600)
@tenant_required
@permission_required(PERMISSION_EDIT_PATIENTS)
def reactivate_patient(patient_id):
    """
    Reactivate a previously deactivated patient
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(Patient.query, tenant_id)
        patient = query.filter_by(id=patient_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        if patient.is_active:
            return jsonify({'error': 'Patient is already active'}), 400
        
        patient.is_active = True
        patient.reactivated_by = user_id
        patient.reactivated_at = datetime.utcnow()
        patient.updated_by = user_id
        patient.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'update', 'patient', patient.id, 
                           f'Patient reactivated: {patient.first_name} {patient.last_name}')
        
        return jsonify({
            'message': 'Patient reactivated successfully',
            'patient': patient.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to reactivate patient', 'details': str(e)}), 500

@patients_bp.route('/stats', methods=['GET'])
@rate_limit(limit=80, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_PATIENTS)
def get_patient_statistics():
    """
    Get patient statistics and analytics
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        days = int(request.args.get('days', 365))  # Default to 1 year
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        stats = {
            'demographics': _get_demographic_stats(tenant_id),
            'growth_metrics': _get_growth_metrics(tenant_id, start_date, end_date),
            'activity_metrics': _get_activity_metrics(tenant_id, start_date, end_date),
            'retention_metrics': _get_retention_metrics(tenant_id, start_date, end_date)
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve patient statistics', 'details': str(e)}), 500

@patients_bp.route('/import', methods=['POST'])
@rate_limit(limit=10, period=3600)  # Very restrictive for imports
@tenant_required
@permission_required(PERMISSION_CREATE_PATIENTS)
def import_patients():
    """
    Import multiple patients from CSV or JSON data
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        data = request.get_json()
        patients_data = data.get('patients', [])
        
        if not isinstance(patients_data, list) or len(patients_data) == 0:
            return jsonify({'error': 'No patient data provided'}), 400
        
        if len(patients_data) > 100:  # Limit import size
            return jsonify({'error': 'Cannot import more than 100 patients at once'}), 400
        
        results = {
            'successful': [],
            'failed': [],
            'duplicates': []
        }
        
        for patient_data in patients_data:
            try:
                # Check for duplicates
                duplicate_check = _check_duplicate_patient(tenant_id, patient_data)
                if duplicate_check['is_duplicate']:
                    results['duplicates'].append({
                        'data': patient_data,
                        'reason': 'Duplicate patient found',
                        'existing_patients': duplicate_check['existing_patients']
                    })
                    continue
                
                # Create patient
                patient = Patient(
                    tenant_id=tenant_id,
                    first_name=patient_data['first_name'],
                    last_name=patient_data['last_name'],
                    email=patient_data.get('email'),
                    phone=patient_data.get('phone'),
                    date_of_birth=_parse_date(patient_data.get('date_of_birth')),
                    gender=patient_data.get('gender'),
                    created_by=user_id
                )
                
                db.session.add(patient)
                db.session.flush()  # Get the ID without committing
                
                results['successful'].append(patient.id)
                
            except Exception as e:
                results['failed'].append({
                    'data': patient_data,
                    'error': str(e)
                })
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'import', 'patient', None, 
                           f'Imported {len(results["successful"])} patients')
        
        return jsonify({
            'message': f'Import completed: {len(results["successful"])} successful, {len(results["failed"])} failed, {len(results["duplicates"])} duplicates',
            'results': results
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to import patients', 'details': str(e)}), 500

# Helper functions with tenant filtering
def _get_patients_summary(tenant_id: str, query: Any) -> Dict[str, Any]:
    """Get summary statistics for patients"""
    total_patients = query.count()
    active_patients = query.filter_by(is_active=True).count()
    
    # Count by gender
    gender_counts = query.filter(Patient.gender.isnot(None))\
                        .group_by(Patient.gender)\
                        .with_entities(Patient.gender, db.func.count(Patient.id))\
                        .all()
    
    # Count new patients this month
    start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    new_this_month = query.filter(Patient.created_at >= start_of_month).count()
    
    return {
        'total_patients': total_patients,
        'active_patients': active_patients,
        'inactive_patients': total_patients - active_patients,
        'gender_breakdown': {gender: count for gender, count in gender_counts},
        'new_this_month': new_this_month
    }

def _check_duplicate_patient(tenant_id: str, patient_data: Dict[str, Any]) -> Dict[str, Any]:
    """Check for potential duplicate patients"""
    query = multi_tenant_query(Patient.query, tenant_id)
    
    # Check by email
    if patient_data.get('email'):
        email_match = query.filter(
            Patient.email == patient_data['email'],
            Patient.is_active == True
        ).first()
        if email_match:
            return {
                'is_duplicate': True,
                'existing_patients': [email_match.to_dict()],
                'match_type': 'email'
            }
    
    # Check by phone
    if patient_data.get('phone'):
        phone_match = query.filter(
            Patient.phone == patient_data['phone'],
            Patient.is_active == True
        ).first()
        if phone_match:
            return {
                'is_duplicate': True,
                'existing_patients': [phone_match.to_dict()],
                'match_type': 'phone'
            }
    
    # Check by name and similar details
    name_matches = query.filter(
        Patient.first_name.ilike(patient_data['first_name']),
        Patient.last_name.ilike(patient_data['last_name']),
        Patient.is_active == True
    ).all()
    
    if name_matches:
        return {
            'is_duplicate': True,
            'existing_patients': [match.to_dict() for match in name_matches],
            'match_type': 'name'
        }
    
    return {'is_duplicate': False, 'existing_patients': []}

def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse date string to datetime object"""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except ValueError:
        return None

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

def _get_patient_appointments(tenant_id: str, patient_id: int) -> List[Dict]:
    """Get patient appointments with tenant filtering"""
    query = multi_tenant_query(Appointment.query, tenant_id)
    appointments = query.filter_by(patient_id=patient_id)\
                      .order_by(Appointment.start_time.desc())\
                      .limit(10)\
                      .all()
    return [appt.to_dict() for appt in appointments]

def _get_recent_treatments(tenant_id: str, patient_id: int) -> List[Dict]:
    """Get recent treatments with tenant filtering"""
    query = multi_tenant_query(Treatment.query, tenant_id)
    treatments = query.filter_by(patient_id=patient_id)\
                    .order_by(Treatment.treatment_date.desc())\
                    .limit(5)\
                    .all()
    return [treatment.to_dict() for treatment in treatments]

def _get_financial_summary(tenant_id: str, patient_id: int) -> Dict[str, Any]:
    """Get patient financial summary"""
    query = multi_tenant_query(Invoice.query, tenant_id)
    invoices = query.filter_by(patient_id=patient_id).all()
    
    total_invoiced = sum(invoice.amount for invoice in invoices)
    total_paid = sum(invoice.paid_amount for invoice in invoices)
    outstanding = total_invoiced - total_paid
    
    return {
        'total_invoiced': float(total_invoiced),
        'total_paid': float(total_paid),
        'outstanding_balance': float(outstanding),
        'invoice_count': len(invoices)
    }

def _get_medical_history(tenant_id: str, patient_id: int) -> Dict[str, Any]:
    """Get patient medical history"""
    query = multi_tenant_query(Patient.query, tenant_id)
    patient = query.filter_by(id=patient_id).first()
    
    if not patient:
        return {}
    
    return {
        'allergies': patient.allergies,
        'medications': patient.medications,
        'medical_conditions': patient.medical_conditions,
        'surgical_history': patient.surgical_history,
        'family_history': patient.family_history,
        'social_history': patient.social_history,
        'dental_history': patient.dental_history,
        'habits': patient.habits
    }

def _get_demographic_stats(tenant_id: str) -> Dict[str, Any]:
    """Get patient demographic statistics"""
    query = multi_tenant_query(Patient.query, tenant_id)
    
    # Age distribution
    age_distribution = query.filter(
        Patient.date_of_birth.isnot(None),
        Patient.is_active == True
    ).with_entities(
        db.func.floor((db.func.extract('epoch', db.func.now() - Patient.date_of_birth) / 31556952) / 10) * 10,
        db.func.count(Patient.id)
    ).group_by(db.func.floor((db.func.extract('epoch', db.func.now() - Patient.date_of_birth) / 31556952) / 10) * 10)\
     .all()
    
    # Gender distribution
    gender_distribution = query.filter(
        Patient.gender.isnot(None),
        Patient.is_active == True
    ).group_by(Patient.gender)\
     .with_entities(Patient.gender, db.func.count(Patient.id))\
     .all()
    
    return {
        'age_distribution': {f"{int(age)}-{int(age)+9}": count for age, count in age_distribution if age is not None},
        'gender_distribution': {gender: count for gender, count in gender_distribution},
        'total_active_patients': query.filter_by(is_active=True).count()
    }

def _get_growth_metrics(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get patient growth metrics"""
    query = multi_tenant_query(Patient.query, tenant_id)
    
    new_patients = query.filter(
        Patient.created_at.between(start_date, end_date)
    ).count()
    
    total_patients = query.filter(
        Patient.created_at <= end_date
    ).count()
    
    return {
        'new_patients': new_patients,
        'total_patients': total_patients,
        'growth_rate': (new_patients / total_patients * 100) if total_patients > 0 else 0
    }

def _get_activity_metrics(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get patient activity metrics"""
    appointment_query = multi_tenant_query(Appointment.query, tenant_id)
    active_patients = appointment_query.filter(
        Appointment.start_time.between(start_date, end_date)
    ).distinct(Appointment.patient_id).count()
    
    return {
        'active_patients': active_patients,
        'appointments_count': appointment_query.filter(
            Appointment.start_time.between(start_date, end_date)
        ).count()
    }

def _get_retention_metrics(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get patient retention metrics"""
    # This would typically involve more complex calculations
    # For now, return basic metrics
    query = multi_tenant_query(Patient.query, tenant_id)
    
    returning_patients = query.filter(
        Patient.created_at < start_date,
        Patient.is_active == True
    ).count()
    
    return {
        'returning_patients': returning_patients,
        'retention_rate': 0  # Would need more complex calculation
    }

@patients_bp.errorhandler(403)
def handle_permission_error(e):
    return jsonify({'error': 'Access forbidden', 'message': 'Insufficient permissions'}), 403

@patients_bp.errorhandler(401)
def handle_authentication_error(e):
    return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401

@patients_bp.errorhandler(429)
def handle_rate_limit_error(e):
    return jsonify({'error': 'Rate limit exceeded', 'message': 'Too many requests'}), 429