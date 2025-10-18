# backend/app/routes/clinical.py

from flask import Blueprint, request, jsonify, g, current_app
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from sqlalchemy import or_, and_, func, desc
import json
from werkzeug.utils import secure_filename
import os
import uuid

from ..models import (
    db, MedicalRecord, Patient, Appointment, TreatmentPlan, 
    Prescription, Allergy, Procedure, User
)
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit
from ..utils.validation import validate_medical_record_data, validate_vital_signs
from ..utils.file_storage import save_medical_file, delete_medical_file, get_medical_file_url

clinical_bp = Blueprint('clinical', __name__, url_prefix='/api/clinical')

# ===== Medical Records Routes =====

@clinical_bp.route('/records', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_clinical_records', 'manage_clinical_records'])
@rate_limit(limit=60, period=60)
def get_medical_records():
    """
    Get paginated medical records with advanced filtering and search
    """
    try:
        current_user = get_current_user()
        patient_id = request.args.get('patient_id')
        record_type = request.args.get('type')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        search = request.args.get('search')
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)  # Max 50 per page
        
        if not patient_id:
            return jsonify({'error': 'Patient ID is required'}), 400
        
        # Verify patient belongs to current tenant
        patient = multi_tenant_query(Patient).filter_by(id=patient_id).first()
        if not patient:
            return jsonify({'error': 'Patient not found or access denied'}), 404
        
        # Build query
        query = multi_tenant_query(MedicalRecord).filter_by(patient_id=patient_id)
        
        # Apply filters
        if record_type and record_type != 'all':
            query = query.filter(MedicalRecord.type == record_type)
        
        if date_from:
            try:
                date_from_obj = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
                query = query.filter(MedicalRecord.created_at >= date_from_obj)
            except ValueError:
                return jsonify({'error': 'Invalid date_from format. Use ISO format.'}), 400
        
        if date_to:
            try:
                date_to_obj = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
                query = query.filter(MedicalRecord.created_at <= date_to_obj)
            except ValueError:
                return jsonify({'error': 'Invalid date_to format. Use ISO format.'}), 400
        
        if search:
            search_filter = or_(
                MedicalRecord.title.ilike(f'%{search}%'),
                MedicalRecord.content.ilike(f'%{search}%'),
                MedicalRecord.diagnosis_codes.any(func.lower(func.cast(db.Text, 'code')).ilike(f'%{search.lower()}%')),
                MedicalRecord.procedure_codes.any(func.lower(func.cast(db.Text, 'code')).ilike(f'%{search.lower()}%'))
            )
            query = query.filter(search_filter)
        
        # Order by most recent first
        records = query.order_by(desc(MedicalRecord.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Get record type counts for statistics
        type_counts = db.session.query(
            MedicalRecord.type,
            func.count(MedicalRecord.id)
        ).filter(
            MedicalRecord.patient_id == patient_id,
            MedicalRecord.organization_id == g.tenant_id
        ).group_by(MedicalRecord.type).all()
        
        return jsonify({
            'records': [record.to_dict(include_creator=True) for record in records.items],
            'pagination': {
                'total': records.total,
                'pages': records.pages,
                'current_page': page,
                'per_page': per_page
            },
            'statistics': {
                'total_records': records.total,
                'type_counts': {record_type: count for record_type, count in type_counts}
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching medical records: {str(e)}")
        return jsonify({'error': 'Failed to fetch medical records'}), 500

@clinical_bp.route('/records/<int:record_id>', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_clinical_records', 'manage_clinical_records'])
def get_medical_record(record_id):
    """
    Get detailed medical record information
    """
    try:
        record = multi_tenant_query(MedicalRecord).filter_by(id=record_id).first_or_404()
        
        return jsonify({
            'record': record.to_dict(include_creator=True, include_attachments=True),
            'patient': record.patient.to_basic_dict() if record.patient else None
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching medical record {record_id}: {str(e)}")
        return jsonify({'error': 'Failed to fetch medical record'}), 500

@clinical_bp.route('/records', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_clinical_records'])
def create_medical_record():
    """
    Create a new medical record with comprehensive clinical data
    """
    try:
        data = request.get_json()
        
        # Validate medical record data
        validation_error = validate_medical_record_data(data)
        if validation_error:
            return validation_error
        
        # Verify patient belongs to current tenant
        patient = multi_tenant_query(Patient).filter_by(id=data['patient_id']).first()
        if not patient:
            return jsonify({'error': 'Patient not found or access denied'}), 404
        
        # Verify appointment belongs to current tenant (if provided)
        if data.get('appointment_id'):
            appointment = multi_tenant_query(Appointment).filter_by(id=data['appointment_id']).first()
            if not appointment:
                return jsonify({'error': 'Appointment not found or access denied'}), 404
        
        record = MedicalRecord(
            organization_id=g.tenant_id,
            patient_id=data['patient_id'],
            appointment_id=data.get('appointment_id'),
            type=data['type'],
            title=data['title'],
            content=data['content'],
            created_by=g.user.id,
            status=data.get('status', 'active'),
            priority=data.get('priority', 'normal'),
            diagnosis_codes=data.get('diagnosis_codes', []),
            procedure_codes=data.get('procedure_codes', []),
            vital_signs=data.get('vital_signs', {}),
            medications=data.get('medications', []),
            allergies=data.get('allergies', []),
            notes=data.get('notes', ''),
            follow_up_required=data.get('follow_up_required', False),
            follow_up_date=data.get('follow_up_date'),
            is_confidential=data.get('is_confidential', False)
        )
        
        db.session.add(record)
        db.session.commit()
        
        # Log record creation
        current_app.logger.info(f"Medical record created for patient {data['patient_id']} by user {g.user.id}")
        
        return jsonify({
            'message': 'Medical record created successfully',
            'record': record.to_dict(include_creator=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating medical record: {str(e)}")
        return jsonify({'error': 'Failed to create medical record'}), 500

@clinical_bp.route('/records/<int:record_id>', methods=['PUT'])
@jwt_required()
@tenant_required
@permission_required(['manage_clinical_records'])
def update_medical_record(record_id):
    """
    Update an existing medical record
    """
    try:
        record = multi_tenant_query(MedicalRecord).filter_by(id=record_id).first_or_404()
        
        # Check if record is locked (e.g., signed off)
        if record.is_locked:
            return jsonify({'error': 'Cannot modify locked medical record'}), 400
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = [
            'title', 'content', 'status', 'priority', 'diagnosis_codes',
            'procedure_codes', 'vital_signs', 'medications', 'allergies',
            'notes', 'follow_up_required', 'follow_up_date', 'is_confidential'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(record, field, data[field])
        
        record.updated_at = datetime.utcnow()
        record.updated_by = g.user.id
        db.session.commit()
        
        return jsonify({
            'message': 'Medical record updated successfully',
            'record': record.to_dict(include_creator=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating medical record {record_id}: {str(e)}")
        return jsonify({'error': 'Failed to update medical record'}), 500

@clinical_bp.route('/records/<int:record_id>', methods=['DELETE'])
@jwt_required()
@tenant_required
@permission_required(['manage_clinical_records'])
def delete_medical_record(record_id):
    """
    Delete a medical record (soft delete with audit trail)
    """
    try:
        record = multi_tenant_query(MedicalRecord).filter_by(id=record_id).first_or_404()
        
        if record.is_locked:
            return jsonify({'error': 'Cannot delete locked medical record'}), 400
        
        # Soft delete with audit information
        record.is_deleted = True
        record.deleted_at = datetime.utcnow()
        record.deleted_by = g.user.id
        db.session.commit()
        
        # Log deletion
        current_app.logger.warning(f"Medical record {record_id} soft-deleted by user {g.user.id}")
        
        return jsonify({'message': 'Medical record deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting medical record {record_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete medical record'}), 500

@clinical_bp.route('/records/<int:record_id>/lock', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_clinical_records'])
def lock_medical_record(record_id):
    """
    Lock a medical record to prevent further modifications
    """
    try:
        record = multi_tenant_query(MedicalRecord).filter_by(id=record_id).first_or_404()
        
        if record.is_locked:
            return jsonify({'error': 'Medical record is already locked'}), 400
        
        record.is_locked = True
        record.locked_at = datetime.utcnow()
        record.locked_by = g.user.id
        db.session.commit()
        
        return jsonify({'message': 'Medical record locked successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error locking medical record {record_id}: {str(e)}")
        return jsonify({'error': 'Failed to lock medical record'}), 500

# ===== File Attachment Routes =====

@clinical_bp.route('/records/<int:record_id>/attachments', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_clinical_records'])
def upload_medical_attachment(record_id):
    """
    Upload attachment for a medical record
    """
    try:
        record = multi_tenant_query(MedicalRecord).filter_by(id=record_id).first_or_404()
        
        if record.is_locked:
            return jsonify({'error': 'Cannot add attachments to locked medical record'}), 400
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type and size
        allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png', 'gif', 'txt', 'doc', 'docx'}
        max_file_size = 10 * 1024 * 1024  # 10MB
        
        if file.content_length > max_file_size:
            return jsonify({'error': 'File size exceeds 10MB limit'}), 400
        
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if file_extension not in allowed_extensions:
            return jsonify({'error': f'File type not allowed. Allowed types: {", ".join(allowed_extensions)}'}), 400
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Save file
        file_path = save_medical_file(file, unique_filename, g.tenant_id, record.patient_id)
        
        # Add attachment to record
        if not record.attachments:
            record.attachments = []
        
        attachment = {
            'id': str(uuid.uuid4()),
            'filename': filename,
            'storage_path': file_path,
            'uploaded_by': g.user.id,
            'uploaded_at': datetime.utcnow().isoformat(),
            'file_size': file.content_length,
            'mime_type': file.mimetype
        }
        
        record.attachments.append(attachment)
        db.session.commit()
        
        return jsonify({
            'message': 'File uploaded successfully',
            'attachment': attachment
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error uploading medical attachment: {str(e)}")
        return jsonify({'error': 'Failed to upload file'}), 500

@clinical_bp.route('/records/<int:record_id>/attachments/<attachment_id>', methods=['DELETE'])
@jwt_required()
@tenant_required
@permission_required(['manage_clinical_records'])
def delete_medical_attachment(record_id, attachment_id):
    """
    Delete an attachment from a medical record
    """
    try:
        record = multi_tenant_query(MedicalRecord).filter_by(id=record_id).first_or_404()
        
        if record.is_locked:
            return jsonify({'error': 'Cannot delete attachments from locked medical record'}), 400
        
        if not record.attachments:
            return jsonify({'error': 'No attachments found'}), 404
        
        # Find and remove attachment
        attachment = next((a for a in record.attachments if a['id'] == attachment_id), None)
        if not attachment:
            return jsonify({'error': 'Attachment not found'}), 404
        
        # Delete physical file
        delete_medical_file(attachment['storage_path'])
        
        # Remove from record
        record.attachments = [a for a in record.attachments if a['id'] != attachment_id]
        db.session.commit()
        
        return jsonify({'message': 'Attachment deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting medical attachment: {str(e)}")
        return jsonify({'error': 'Failed to delete attachment'}), 500

# ===== Clinical Dashboard Routes =====

@clinical_bp.route('/dashboard/patient/<int:patient_id>', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_clinical_records'])
def patient_clinical_dashboard(patient_id):
    """
    Get clinical dashboard for a specific patient
    """
    try:
        # Verify patient belongs to current tenant
        patient = multi_tenant_query(Patient).filter_by(id=patient_id).first()
        if not patient:
            return jsonify({'error': 'Patient not found or access denied'}), 404
        
        # Get recent records
        recent_records = multi_tenant_query(MedicalRecord).filter_by(
            patient_id=patient_id
        ).order_by(desc(MedicalRecord.created_at)).limit(10).all()
        
        # Get upcoming appointments
        upcoming_appointments = multi_tenant_query(Appointment).filter(
            Appointment.patient_id == patient_id,
            Appointment.start_time >= datetime.utcnow(),
            Appointment.status.in_(['scheduled', 'confirmed'])
        ).order_by(Appointment.start_time.asc()).limit(5).all()
        
        # Get active prescriptions
        active_prescriptions = multi_tenant_query(Prescription).filter(
            Prescription.patient_id == patient_id,
            Prescription.status == 'active'
        ).order_by(desc(Prescription.created_at)).limit(10).all()
        
        # Get allergies
        allergies = multi_tenant_query(Allergy).filter_by(patient_id=patient_id).all()
        
        # Get statistics
        record_stats = db.session.query(
            MedicalRecord.type,
            func.count(MedicalRecord.id)
        ).filter(
            MedicalRecord.patient_id == patient_id,
            MedicalRecord.organization_id == g.tenant_id
        ).group_by(MedicalRecord.type).all()
        
        return jsonify({
            'patient': patient.to_dict(),
            'recent_records': [record.to_dict(include_creator=True) for record in recent_records],
            'upcoming_appointments': [appt.to_dict() for appt in upcoming_appointments],
            'active_prescriptions': [rx.to_dict() for rx in active_prescriptions],
            'allergies': [allergy.to_dict() for allergy in allergies],
            'statistics': {
                'total_records': sum(count for _, count in record_stats),
                'record_types': {record_type: count for record_type, count in record_stats}
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching clinical dashboard for patient {patient_id}: {str(e)}")
        return jsonify({'error': 'Failed to fetch clinical dashboard'}), 500

@clinical_bp.route('/search', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_clinical_records'])
def search_clinical_data():
    """
    Search across clinical data with advanced filters
    """
    try:
        query = request.args.get('q')
        record_type = request.args.get('type')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Build search query
        search_query = multi_tenant_query(MedicalRecord)
        
        # Apply text search
        search_filter = or_(
            MedicalRecord.title.ilike(f'%{query}%'),
            MedicalRecord.content.ilike(f'%{query}%'),
            MedicalRecord.diagnosis_codes.any(func.lower(func.cast(db.Text, 'code')).ilike(f'%{query.lower()}%')),
            MedicalRecord.procedure_codes.any(func.lower(func.cast(db.Text, 'code')).ilike(f'%{query.lower()}%'))
        )
        search_query = search_query.filter(search_filter)
        
        # Apply filters
        if record_type and record_type != 'all':
            search_query = search_query.filter(MedicalRecord.type == record_type)
        
        if date_from:
            try:
                date_from_obj = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
                search_query = search_query.filter(MedicalRecord.created_at >= date_from_obj)
            except ValueError:
                return jsonify({'error': 'Invalid date_from format'}), 400
        
        if date_to:
            try:
                date_to_obj = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
                search_query = search_query.filter(MedicalRecord.created_at <= date_to_obj)
            except ValueError:
                return jsonify({'error': 'Invalid date_to format'}), 400
        
        # Execute search
        results = search_query.order_by(desc(MedicalRecord.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'results': [record.to_dict(include_patient=True, include_creator=True) for record in results.items],
            'pagination': {
                'total': results.total,
                'pages': results.pages,
                'current_page': page,
                'per_page': per_page
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error searching clinical data: {str(e)}")
        return jsonify({'error': 'Search failed'}), 500

# ===== Validation Utilities =====

def validate_medical_record_data(data):
    """Validate medical record data"""
    required_fields = ['patient_id', 'type', 'title', 'content']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate record type
    valid_types = ['consultation', 'examination', 'diagnosis', 'treatment', 'progress', 'surgery', 'lab', 'imaging', 'other']
    if data['type'] not in valid_types:
        return jsonify({'error': f'Invalid record type. Valid types: {", ".join(valid_types)}'}), 400
    
    # Validate vital signs if provided
    if data.get('vital_signs'):
        validation_error = validate_vital_signs(data['vital_signs'])
        if validation_error:
            return validation_error
    
    return None

def validate_vital_signs(vital_signs):
    """Validate vital signs data"""
    try:
        if 'blood_pressure' in vital_signs:
            bp = vital_signs['blood_pressure']
            if not isinstance(bp, dict) or 'systolic' not in bp or 'diastolic' not in bp:
                return jsonify({'error': 'Blood pressure must contain systolic and diastolic values'}), 400
        
        numeric_fields = ['heart_rate', 'respiratory_rate', 'temperature', 'oxygen_saturation', 'height', 'weight']
        for field in numeric_fields:
            if field in vital_signs:
                float(vital_signs[field])  # Will raise ValueError if not convertible
                
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid vital signs data format'}), 400
    
    return None