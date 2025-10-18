# backend/app/routes/family_members.py

from flask import Blueprint, request, jsonify, g, current_app
from flask_jwt_extended import jwt_required
from datetime import datetime
from sqlalchemy import or_, and_
import re

from ..models import (
    db, FamilyMember, Patient, User, Organization, 
    FamilyRelationship, InsurancePlan
)
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit
from ..utils.subscriptions import can_add_family_member, get_family_member_limit
from ..utils.validation import validate_family_member_data

family_members_bp = Blueprint("family_members", __name__, url_prefix="/api/family-members")


# At the top of app/routes/family_members.py (before the failing import)

# Temporary validation function
def validate_family_member_data(data):
    """Temporary validation - replace with proper implementation"""
    errors = []
    
    required = ['first_name', 'last_name', 'relationship', 'date_of_birth']
    for field in required:
        if not data.get(field):
            errors.append(f"{field} is required")
    
    return errors

# Then your existing imports
from ..utils.subscriptions import can_add_family_member, get_family_member_limit
# This import will now use the temporary function above



# ===== Family Member Routes =====

@family_members_bp.route("", methods=["GET"])
@jwt_required()
@tenant_required
@permission_required(['view_family_members', 'manage_family_members'])
@rate_limit(limit=60, period=60)
def list_family_members():
    """
    Get paginated list of family members with filtering and search
    """
    try:
        current_user = get_current_user()
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        search = request.args.get('search')
        patient_id = request.args.get('patient_id')
        relationship_type = request.args.get('relationship_type')
        
        query = multi_tenant_query(FamilyMember)
        
        # Apply filters
        if search:
            search_filter = or_(
                FamilyMember.first_name.ilike(f'%{search}%'),
                FamilyMember.last_name.ilike(f'%{search}%'),
                FamilyMember.email.ilike(f'%{search}%'),
                FamilyMember.phone.ilike(f'%{search}%')
            )
            query = query.filter(search_filter)
        
        if patient_id:
            query = query.filter(FamilyMember.patient_id == patient_id)
        
        if relationship_type:
            query = query.filter(FamilyMember.relationship_type == relationship_type)
        
        # Order by most recent
        family_members = query.order_by(FamilyMember.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Get family member count for subscription limits
        total_count = multi_tenant_query(FamilyMember).count()
        member_limit = get_family_member_limit(current_user)
        
        return jsonify({
            'family_members': [fm.to_dict(include_patient=True) for fm in family_members.items],
            'pagination': {
                'total': family_members.total,
                'pages': family_members.pages,
                'current_page': page,
                'per_page': per_page
            },
            'limits': {
                'current_count': total_count,
                'max_allowed': member_limit,
                'remaining': max(0, member_limit - total_count) if member_limit else None
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching family members: {str(e)}")
        return jsonify({'error': 'Failed to fetch family members'}), 500

@family_members_bp.route("/<int:fm_id>", methods=["GET"])
@jwt_required()
@tenant_required
@permission_required(['view_family_members', 'manage_family_members'])
def get_family_member(fm_id):
    """
    Get detailed family member information including relationships and insurance
    """
    try:
        fm = multi_tenant_query(FamilyMember).filter_by(id=fm_id).first_or_404()
        
        return jsonify({
            'family_member': fm.to_dict(include_patient=True, include_insurance=True),
            'relationships': [rel.to_dict() for rel in fm.relationships],
            'insurance_plans': [plan.to_basic_dict() for plan in fm.insurance_plans]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching family member {fm_id}: {str(e)}")
        return jsonify({'error': 'Failed to fetch family member'}), 500

@family_members_bp.route("", methods=["POST"])
@jwt_required()
@tenant_required
@permission_required(['manage_family_members'])
def create_family_member():
    """
    Create a new family member with validation and subscription checks
    """
    try:
        current_user = get_current_user()
        data = request.get_json()
        
        # Validate family member data
        validation_error = validate_family_member_data(data)
        if validation_error:
            return validation_error
        
        # Check subscription limits
        current_count = multi_tenant_query(FamilyMember).count()
        if not can_add_family_member(current_user, current_count):
            return jsonify({
                'message': 'Family member limit reached. Please upgrade your subscription.',
                'error': 'subscription_limit',
                'current_count': current_count,
                'max_allowed': get_family_member_limit(current_user)
            }), 403
        
        # Verify patient belongs to current tenant if provided
        if data.get('patient_id'):
            patient = multi_tenant_query(Patient).filter_by(id=data['patient_id']).first()
            if not patient:
                return jsonify({'error': 'Patient not found or access denied'}), 404
        
        # Create family member
        fm = FamilyMember(
            organization_id=g.tenant_id,
            patient_id=data.get('patient_id'),
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data.get('date_of_birth'),
            gender=data.get('gender'),
            relationship_type=data.get('relationship_type', 'family'),
            email=data.get('email'),
            phone=data.get('phone'),
            emergency_contact=data.get('emergency_contact', False),
            primary_contact=data.get('primary_contact', False),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            notes=data.get('notes')
        )
        
        db.session.add(fm)
        db.session.commit()
        
        # Log creation
        current_app.logger.info(f"Family member created for organization {g.tenant_id} by user {current_user.id}")
        
        return jsonify({
            'message': 'Family member created successfully',
            'family_member': fm.to_dict(include_patient=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating family member: {str(e)}")
        return jsonify({'error': 'Failed to create family member'}), 500

@family_members_bp.route("/<int:fm_id>", methods=["PUT"])
@jwt_required()
@tenant_required
@permission_required(['manage_family_members'])
def update_family_member(fm_id):
    """
    Update family member information
    """
    try:
        fm = multi_tenant_query(FamilyMember).filter_by(id=fm_id).first_or_404()
        data = request.get_json()
        
        # Validate update data
        validation_error = validate_family_member_data(data, is_update=True)
        if validation_error:
            return validation_error
        
        # Update allowed fields
        allowed_fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'relationship_type', 'email', 'phone', 'emergency_contact',
            'primary_contact', 'address', 'city', 'state', 'zip_code', 'notes'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(fm, field, data[field])
        
        fm.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Family member updated successfully',
            'family_member': fm.to_dict(include_patient=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating family member {fm_id}: {str(e)}")
        return jsonify({'error': 'Failed to update family member'}), 500

@family_members_bp.route("/<int:fm_id>", methods=["DELETE"])
@jwt_required()
@tenant_required
@permission_required(['manage_family_members'])
def delete_family_member(fm_id):
    """
    Delete a family member and associated relationships
    """
    try:
        fm = multi_tenant_query(FamilyMember).filter_by(id=fm_id).first_or_404()
        
        # Check if family member has active relationships
        if fm.relationships and len(fm.relationships) > 0:
            return jsonify({
                'error': 'Cannot delete family member with active relationships. Please remove relationships first.'
            }), 400
        
        # Check if family member has insurance plans
        if fm.insurance_plans and len(fm.insurance_plans) > 0:
            return jsonify({
                'error': 'Cannot delete family member with insurance plans. Please remove insurance plans first.'
            }), 400
        
        db.session.delete(fm)
        db.session.commit()
        
        current_app.logger.info(f"Family member {fm_id} deleted by user {g.user.id}")
        
        return jsonify({'message': 'Family member deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting family member {fm_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete family member'}), 500

# ===== Relationship Management Routes =====

@family_members_bp.route("/<int:fm_id>/relationships", methods=["GET"])
@jwt_required()
@tenant_required
@permission_required(['view_family_members', 'manage_family_members'])
def get_family_relationships(fm_id):
    """
    Get all relationships for a family member
    """
    try:
        fm = multi_tenant_query(FamilyMember).filter_by(id=fm_id).first_or_404()
        
        return jsonify({
            'relationships': [rel.to_dict(include_related=True) for rel in fm.relationships]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching relationships for family member {fm_id}: {str(e)}")
        return jsonify({'error': 'Failed to fetch relationships'}), 500

@family_members_bp.route("/<int:fm_id>/relationships", methods=["POST"])
@jwt_required()
@tenant_required
@permission_required(['manage_family_members'])
def create_family_relationship(fm_id):
    """
    Create a relationship between family members
    """
    try:
        fm = multi_tenant_query(FamilyMember).filter_by(id=fm_id).first_or_404()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('related_member_id') or not data.get('relationship_type'):
            return jsonify({'error': 'related_member_id and relationship_type are required'}), 400
        
        # Verify related member exists and belongs to same tenant
        related_member = multi_tenant_query(FamilyMember).filter_by(id=data['related_member_id']).first()
        if not related_member:
            return jsonify({'error': 'Related family member not found'}), 404
        
        # Check if relationship already exists
        existing_relationship = FamilyRelationship.query.filter(
            or_(
                and_(
                    FamilyRelationship.family_member_id == fm_id,
                    FamilyRelationship.related_member_id == data['related_member_id']
                ),
                and_(
                    FamilyRelationship.family_member_id == data['related_member_id'],
                    FamilyRelationship.related_member_id == fm_id
                )
            )
        ).first()
        
        if existing_relationship:
            return jsonify({'error': 'Relationship already exists'}), 400
        
        # Create relationship
        relationship = FamilyRelationship(
            family_member_id=fm_id,
            related_member_id=data['related_member_id'],
            relationship_type=data['relationship_type'],
            notes=data.get('notes')
        )
        
        db.session.add(relationship)
        db.session.commit()
        
        return jsonify({
            'message': 'Relationship created successfully',
            'relationship': relationship.to_dict(include_related=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating relationship: {str(e)}")
        return jsonify({'error': 'Failed to create relationship'}), 500

@family_members_bp.route("/relationships/<int:relationship_id>", methods=["DELETE"])
@jwt_required()
@tenant_required
@permission_required(['manage_family_members'])
def delete_family_relationship(relationship_id):
    """
    Delete a family relationship
    """
    try:
        relationship = FamilyRelationship.query.filter_by(id=relationship_id).first_or_404()
        
        # Verify both family members belong to current tenant
        fm1 = multi_tenant_query(FamilyMember).filter_by(id=relationship.family_member_id).first()
        fm2 = multi_tenant_query(FamilyMember).filter_by(id=relationship.related_member_id).first()
        
        if not fm1 or not fm2:
            return jsonify({'error': 'Relationship not found or access denied'}), 404
        
        db.session.delete(relationship)
        db.session.commit()
        
        return jsonify({'message': 'Relationship deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting relationship {relationship_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete relationship'}), 500

# ===== Insurance Management Routes =====

@family_members_bp.route("/<int:fm_id>/insurance", methods=["GET"])
@jwt_required()
@tenant_required
@permission_required(['view_family_members', 'manage_family_members'])
def get_family_member_insurance(fm_id):
    """
    Get insurance plans for a family member
    """
    try:
        fm = multi_tenant_query(FamilyMember).filter_by(id=fm_id).first_or_404()
        
        return jsonify({
            'insurance_plans': [plan.to_dict() for plan in fm.insurance_plans]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching insurance for family member {fm_id}: {str(e)}")
        return jsonify({'error': 'Failed to fetch insurance plans'}), 500

# ===== Validation Utilities =====

def validate_family_member_data(data, is_update=False):
    """Validate family member data"""
    if not is_update:
        required_fields = ['first_name', 'last_name']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({'error': f'{field.replace("_", " ").title()} is required'}), 400
    
    # Validate email format if provided
    if data.get('email'):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate phone format if provided
    if data.get('phone'):
        # Basic phone validation - adjust based on your requirements
        phone_regex = r'^\+?[0-9]{10,15}$'
        if not re.match(phone_regex, data['phone'].replace(' ', '').replace('-', '')):
            return jsonify({'error': 'Invalid phone number format'}), 400
    
    # Validate date format if provided
    if data.get('date_of_birth'):
        try:
            datetime.fromisoformat(data['date_of_birth'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use ISO format (YYYY-MM-DD)'}), 400
    
    return None

