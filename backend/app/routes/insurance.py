# backend/app/routes/insurance.py

from flask import Blueprint, request, jsonify, g, current_app
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from sqlalchemy import or_, and_, func, extract, case
import json

from ..models import (
    db, InsurancePlan, Patient, FamilyMember, InsuranceClaim, 
    User, Organization
)
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit
from ..utils.validation import validate_insurance_plan_data

insurance_bp = Blueprint('insurance', __name__, url_prefix='/api/insurance')

# ===== Insurance Plan Routes =====

@insurance_bp.route('/plans', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_insurance', 'manage_insurance'])
@rate_limit(limit=60, period=60)
def list_insurance_plans():
    """
    Get paginated list of insurance plans with filtering
    """
    try:
        current_user = get_current_user()
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        patient_id = request.args.get('patient_id')
        family_member_id = request.args.get('family_member_id')
        provider = request.args.get('provider')
        status = request.args.get('status')
        coverage_type = request.args.get('coverage_type')
        search = request.args.get('search')
        
        query = multi_tenant_query(InsurancePlan)
        
        # Apply filters
        if patient_id:
            query = query.filter(InsurancePlan.patient_id == patient_id)
        
        if family_member_id:
            query = query.filter(InsurancePlan.family_member_id == family_member_id)
        
        if provider:
            query = query.filter(InsurancePlan.insurance_provider.ilike(f'%{provider}%'))
        
        if status and status != 'all':
            if status == 'active':
                query = query.filter(InsurancePlan.is_active == True)
            elif status == 'inactive':
                query = query.filter(InsurancePlan.is_active == False)
            elif status == 'expired':
                current_date = datetime.utcnow().date()
                query = query.filter(
                    InsurancePlan.expiration_date < current_date,
                    InsurancePlan.is_active == True
                )
        
        if coverage_type and coverage_type != 'all':
            query = query.filter(InsurancePlan.coverage_type == coverage_type)
        
        if search:
            search_filter = or_(
                InsurancePlan.insurance_provider.ilike(f'%{search}%'),
                InsurancePlan.plan_name.ilike(f'%{search}%'),
                InsurancePlan.policy_number.ilike(f'%{search}%'),
                InsurancePlan.subscriber_name.ilike(f'%{search}%')
            )
            query = query.filter(search_filter)
        
        # Order by most recent
        insurance_plans = query.order_by(InsurancePlan.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Statistics
        stats = db.session.query(
            func.count(InsurancePlan.id),
            func.count(case([(InsurancePlan.is_active == True, 1)], else_=None)),
            func.count(case([(InsurancePlan.verification_status == 'verified', 1)], else_=None))
        ).filter(InsurancePlan.organization_id == g.tenant_id).first()
        
        return jsonify({
            'insurance_plans': [plan.to_dict(include_relationships=True) for plan in insurance_plans.items],
            'pagination': {
                'total': insurance_plans.total,
                'pages': insurance_plans.pages,
                'current_page': page,
                'per_page': per_page
            },
            'statistics': {
                'total_plans': stats[0] or 0,
                'active_plans': stats[1] or 0,
                'verified_plans': stats[2] or 0
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching insurance plans: {str(e)}")
        return jsonify({'error': 'Failed to fetch insurance plans'}), 500

@insurance_bp.route('/plans/<int:plan_id>', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_insurance', 'manage_insurance'])
def get_insurance_plan(plan_id):
    """
    Get detailed insurance plan information
    """
    try:
        plan = multi_tenant_query(InsurancePlan).filter_by(id=plan_id).first_or_404()
        
        # Calculate remaining annual maximum
        remaining_annual_max = plan.get_remaining_annual_maximum()
        
        response_data = plan.to_dict(include_relationships=True)
        response_data['remaining_annual_maximum'] = remaining_annual_max
        response_data['is_valid'] = plan.is_valid()
        
        # Get recent claims
        recent_claims = InsuranceClaim.query.filter_by(
            insurance_plan_id=plan_id
        ).order_by(InsuranceClaim.service_date.desc()).limit(5).all()
        
        return jsonify({
            'insurance_plan': response_data,
            'recent_claims': [claim.to_dict() for claim in recent_claims]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching insurance plan {plan_id}: {str(e)}")
        return jsonify({'error': 'Failed to fetch insurance plan'}), 500

@insurance_bp.route('/plans', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_insurance'])
def create_insurance_plan():
    """
    Create a new insurance plan
    """
    try:
        current_user = get_current_user()
        data = request.get_json()
        
        # Validate insurance plan data
        validation_error = validate_insurance_plan_data(data)
        if validation_error:
            return validation_error
        
        # Verify patient/family member belongs to current tenant
        if data.get('patient_id'):
            patient = multi_tenant_query(Patient).filter_by(id=data['patient_id']).first()
            if not patient:
                return jsonify({'error': 'Patient not found or access denied'}), 404
        
        if data.get('family_member_id'):
            family_member = multi_tenant_query(FamilyMember).filter_by(id=data['family_member_id']).first()
            if not family_member:
                return jsonify({'error': 'Family member not found or access denied'}), 404
        
        # Check if this should be the primary plan
        if data.get('is_primary', True):
            # Remove primary status from other plans for this patient/family member
            if data.get('patient_id'):
                InsurancePlan.query.filter_by(
                    patient_id=data['patient_id'],
                    is_primary=True
                ).update({'is_primary': False})
            elif data.get('family_member_id'):
                InsurancePlan.query.filter_by(
                    family_member_id=data['family_member_id'],
                    is_primary=True
                ).update({'is_primary': False})
        
        # Parse dates
        effective_date = datetime.fromisoformat(data['effective_date'].replace('Z', '+00:00')).date()
        expiration_date = None
        if data.get('expiration_date'):
            expiration_date = datetime.fromisoformat(data['expiration_date'].replace('Z', '+00:00')).date()
        
        subscriber_dob = None
        if data.get('subscriber_dob'):
            subscriber_dob = datetime.fromisoformat(data['subscriber_dob'].replace('Z', '+00:00')).date()
        
        plan = InsurancePlan(
            organization_id=g.tenant_id,
            patient_id=data.get('patient_id'),
            family_member_id=data.get('family_member_id'),
            insurance_provider=data['insurance_provider'],
            plan_name=data['plan_name'],
            policy_number=data['policy_number'],
            group_number=data.get('group_number'),
            subscriber_id=data.get('subscriber_id'),
            subscriber_name=data.get('subscriber_name'),
            subscriber_dob=subscriber_dob,
            subscriber_relationship=data.get('subscriber_relationship'),
            coverage_type=data['coverage_type'],
            effective_date=effective_date,
            expiration_date=expiration_date,
            is_primary=data.get('is_primary', True),
            is_active=data.get('is_active', True),
            benefits=data.get('benefits', {}),
            copay_info=data.get('copay_info', {}),
            deductible_info=data.get('deductible_info', {}),
            annual_maximum=data.get('annual_maximum'),
            notes=data.get('notes'),
            created_by=current_user.id
        )
        
        db.session.add(plan)
        db.session.commit()
        
        current_app.logger.info(f"Insurance plan created for organization {g.tenant_id} by user {current_user.id}")
        
        return jsonify({
            'message': 'Insurance plan created successfully',
            'insurance_plan': plan.to_dict(include_relationships=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating insurance plan: {str(e)}")
        return jsonify({'error': 'Failed to create insurance plan'}), 500

@insurance_bp.route('/plans/<int:plan_id>', methods=['PUT'])
@jwt_required()
@tenant_required
@permission_required(['manage_insurance'])
def update_insurance_plan(plan_id):
    """
    Update insurance plan information
    """
    try:
        plan = multi_tenant_query(InsurancePlan).filter_by(id=plan_id).first_or_404()
        data = request.get_json()
        
        # Validate update data
        validation_error = validate_insurance_plan_data(data, is_update=True)
        if validation_error:
            return validation_error
        
        # Handle primary plan status change
        if data.get('is_primary') and data['is_primary'] != plan.is_primary:
            # Remove primary status from other plans
            if plan.patient_id:
                InsurancePlan.query.filter(
                    InsurancePlan.patient_id == plan.patient_id,
                    InsurancePlan.id != plan_id,
                    InsurancePlan.is_primary == True
                ).update({'is_primary': False})
            elif plan.family_member_id:
                InsurancePlan.query.filter(
                    InsurancePlan.family_member_id == plan.family_member_id,
                    InsurancePlan.id != plan_id,
                    InsurancePlan.is_primary == True
                ).update({'is_primary': False})
        
        # Update allowed fields
        allowed_fields = [
            'insurance_provider', 'plan_name', 'policy_number', 'group_number',
            'subscriber_id', 'subscriber_name', 'subscriber_relationship',
            'coverage_type', 'is_primary', 'is_active', 'verification_status',
            'benefits', 'copay_info', 'deductible_info', 'annual_maximum', 'notes'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(plan, field, data[field])
        
        # Update dates if provided
        if 'effective_date' in data:
            plan.effective_date = datetime.fromisoformat(data['effective_date'].replace('Z', '+00:00')).date()
        
        if 'expiration_date' in data:
            plan.expiration_date = datetime.fromisoformat(data['expiration_date'].replace('Z', '+00:00')).date() if data['expiration_date'] else None
        
        if 'subscriber_dob' in data:
            plan.subscriber_dob = datetime.fromisoformat(data['subscriber_dob'].replace('Z', '+00:00')).date() if data['subscriber_dob'] else None
        
        # Update verification timestamp if status changed
        if 'verification_status' in data and data['verification_status'] != plan.verification_status:
            plan.last_verified = datetime.utcnow()
        
        plan.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Insurance plan updated successfully',
            'insurance_plan': plan.to_dict(include_relationships=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating insurance plan {plan_id}: {str(e)}")
        return jsonify({'error': 'Failed to update insurance plan'}), 500

@insurance_bp.route('/plans/<int:plan_id>', methods=['DELETE'])
@jwt_required()
@tenant_required
@permission_required(['manage_insurance'])
def delete_insurance_plan(plan_id):
    """
    Delete an insurance plan
    """
    try:
        plan = multi_tenant_query(InsurancePlan).filter_by(id=plan_id).first_or_404()
        
        # Check if plan has associated claims
        claim_count = InsuranceClaim.query.filter_by(insurance_plan_id=plan_id).count()
        if claim_count > 0:
            return jsonify({
                'error': 'Cannot delete insurance plan with associated claims. Archive instead.',
                'claim_count': claim_count
            }), 400
        
        db.session.delete(plan)
        db.session.commit()
        
        current_app.logger.info(f"Insurance plan {plan_id} deleted by user {g.user.id}")
        
        return jsonify({'message': 'Insurance plan deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting insurance plan {plan_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete insurance plan'}), 500

@insurance_bp.route('/plans/<int:plan_id>/verify', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_insurance'])
def verify_insurance_plan(plan_id):
    """
    Verify insurance plan eligibility and benefits
    """
    try:
        plan = multi_tenant_query(InsurancePlan).filter_by(id=plan_id).first_or_404()
        
        # In a real implementation, this would call an insurance verification API
        # For now, we'll simulate verification
        
        # Simulate verification process
        plan.verification_status = 'verified'
        plan.last_verified = datetime.utcnow()
        plan.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Insurance plan verified successfully',
            'verification_status': 'verified',
            'last_verified': plan.last_verified.isoformat()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error verifying insurance plan {plan_id}: {str(e)}")
        return jsonify({'error': 'Failed to verify insurance plan'}), 500

# ===== Insurance Benefits and Coverage =====

@insurance_bp.route('/plans/<int:plan_id>/coverage', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_insurance'])
def get_insurance_coverage(plan_id):
    """
    Get detailed coverage information for an insurance plan
    """
    try:
        plan = multi_tenant_query(InsurancePlan).filter_by(id=plan_id).first_or_404()
        
        # Calculate remaining benefits
        remaining_annual_max = plan.get_remaining_annual_maximum()
        
        coverage_data = {
            'plan_info': plan.to_basic_dict(),
            'benefits': plan.benefits,
            'copay_info': plan.copay_info,
            'deductible_info': plan.deductible_info,
            'annual_maximum': {
                'total': float(plan.annual_maximum) if plan.annual_maximum else None,
                'remaining': remaining_annual_max,
                'used': float(plan.annual_maximum) - remaining_annual_max if plan.annual_maximum and remaining_annual_max is not None else None
            },
            'is_valid': plan.is_valid(),
            'verification_status': plan.verification_status
        }
        
        return jsonify(coverage_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching insurance coverage for plan {plan_id}: {str(e)}")
        return jsonify({'error': 'Failed to fetch insurance coverage'}), 500

@insurance_bp.route('/coverage/check', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['view_insurance'])
def check_insurance_coverage():
    """
    Check insurance coverage for a specific procedure or service
    """
    try:
        data = request.get_json()
        plan_id = data.get('plan_id')
        procedure_code = data.get('procedure_code')
        service_date = data.get('service_date', datetime.utcnow().date().isoformat())
        
        if not plan_id or not procedure_code:
            return jsonify({'error': 'plan_id and procedure_code are required'}), 400
        
        plan = multi_tenant_query(InsurancePlan).filter_by(id=plan_id).first_or_404()
        
        # Parse service date
        service_date_obj = datetime.fromisoformat(service_date.replace('Z', '+00:00')).date()
        
        # Check if plan is valid for the service date
        if not plan.is_valid() or (plan.effective_date and plan.effective_date > service_date_obj) or \
           (plan.expiration_date and plan.expiration_date < service_date_obj):
            return jsonify({
                'covered': False,
                'reason': 'Insurance plan not valid for service date'
            }), 200
        
        # Simulate coverage check (in real implementation, this would use insurance API)
        # This is a simplified example
        coverage_result = {
            'covered': True,
            'procedure_code': procedure_code,
            'estimated_coverage': 80.0,  # 80% coverage
            'patient_responsibility': 20.0,  # 20% patient responsibility
            'requires_pre_authorization': False,
            'notes': 'Coverage estimated based on plan benefits'
        }
        
        # Check if procedure is in benefits
        if plan.benefits and 'covered_procedures' in plan.benefits:
            if procedure_code not in plan.benefits['covered_procedures']:
                coverage_result['covered'] = False
                coverage_result['reason'] = 'Procedure not covered by plan'
        
        return jsonify(coverage_result), 200
        
    except Exception as e:
        current_app.logger.error(f"Error checking insurance coverage: {str(e)}")
        return jsonify({'error': 'Failed to check insurance coverage'}), 500

# ===== Validation Utilities =====

def validate_insurance_plan_data(data, is_update=False):
    """Validate insurance plan data"""
    if not is_update:
        required_fields = ['insurance_provider', 'plan_name', 'policy_number', 'coverage_type', 'effective_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field.replace("_", " ").title()} is required'}), 400
    
    # Validate that either patient_id or family_member_id is provided, but not both
    if data.get('patient_id') and data.get('family_member_id'):
        return jsonify({'error': 'Cannot specify both patient_id and family_member_id'}), 400
    
    if not data.get('patient_id') and not data.get('family_member_id'):
        return jsonify({'error': 'Either patient_id or family_member_id is required'}), 400
    
    # Validate date formats
    date_fields = ['effective_date', 'expiration_date', 'subscriber_dob']
    for field in date_fields:
        if data.get(field):
            try:
                datetime.fromisoformat(data[field].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': f'Invalid {field.replace("_", " ")} format. Use ISO format (YYYY-MM-DD)'}), 400
    
    # Validate coverage type
    valid_coverage_types = ['dental', 'medical', 'vision', 'combined']
    if data.get('coverage_type') and data['coverage_type'] not in valid_coverage_types:
        return jsonify({'error': f'Invalid coverage type. Valid types: {", ".join(valid_coverage_types)}'}), 400
    
    return None