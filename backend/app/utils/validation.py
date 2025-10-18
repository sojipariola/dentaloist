# backend/app/utils/validation.py

from flask import jsonify
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
import re

def validate_invoice_data(data):
    """Validate invoice creation/update data"""
    required_fields = ['patient_id', 'issue_date', 'due_date', 'items']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate dates
    try:
        datetime.fromisoformat(data['issue_date'].replace('Z', '+00:00'))
        datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use ISO format.'}), 400
    
    # Validate items
    if not isinstance(data['items'], list) or len(data['items']) == 0:
        return jsonify({'error': 'Items must be a non-empty array'}), 400
    
    for item in data['items']:
        if 'description' not in item or 'unit_price' not in item or 'quantity' not in item:
            return jsonify({'error': 'Each item must have description, unit_price, and quantity'}), 400
        
        try:
            Decimal(str(item['unit_price']))
            int(item['quantity'])
        except (ValueError, InvalidOperation):
            return jsonify({'error': 'Invalid unit_price or quantity format'}), 400
    
    return None

def validate_payment_data(data):
    """Validate payment data"""
    required_fields = ['invoice_id', 'amount', 'method']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        amount = Decimal(str(data['amount']))
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'}), 400
    except (ValueError, InvalidOperation):
        return jsonify({'error': 'Invalid amount format'}), 400
    
    return None



def validate_insurance_plan_data(data, is_update=False):
    """
    Validate insurance plan data with comprehensive checks
    
    Args:
        data: Dictionary containing insurance plan data
        is_update: Boolean indicating if this is for an update operation
    
    Returns:
        None if valid, JSON error response if invalid
    """
    # Required fields check (for create operations)
    if not is_update:
        required_fields = ['insurance_provider', 'plan_name', 'policy_number', 'coverage_type', 'effective_date']
        missing_fields = []
        
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field.replace('_', ' ').title())
        
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields,
                'message': f'The following fields are required: {", ".join(missing_fields)}'
            }), 400

    # Validate that either patient_id or family_member_id is provided, but not both
    if data.get('patient_id') and data.get('family_member_id'):
        return jsonify({
            'error': 'Invalid relationship',
            'message': 'Cannot specify both patient_id and family_member_id. Choose one.'
        }), 400

    if not is_update and not data.get('patient_id') and not data.get('family_member_id'):
        return jsonify({
            'error': 'Missing relationship',
            'message': 'Either patient_id or family_member_id is required'
        }), 400

    # Validate date formats and logic
    date_errors = []
    
    # Effective date validation
    if data.get('effective_date'):
        try:
            effective_date = datetime.fromisoformat(data['effective_date'].replace('Z', '+00:00')).date()
            # Check if effective date is in the future (this might be acceptable for some cases)
            if effective_date > datetime.utcnow().date() + timedelta(days=365):  # More than 1 year in future
                date_errors.append('Effective date cannot be more than 1 year in the future')
        except ValueError:
            date_errors.append('Invalid effective date format. Use ISO format (YYYY-MM-DD)')

    # Expiration date validation
    if data.get('expiration_date'):
        try:
            expiration_date = datetime.fromisoformat(data['expiration_date'].replace('Z', '+00:00')).date()
            
            # Check if expiration date is before effective date
            if data.get('effective_date'):
                effective_date = datetime.fromisoformat(data['effective_date'].replace('Z', '+00:00')).date()
                if expiration_date <= effective_date:
                    date_errors.append('Expiration date must be after effective date')
            
            # Check if expiration date is in the past (might be acceptable for historical records)
            if expiration_date < datetime.utcnow().date() - timedelta(days=30):  # More than 30 days in past
                date_errors.append('Expiration date cannot be more than 30 days in the past')
                
        except ValueError:
            date_errors.append('Invalid expiration date format. Use ISO format (YYYY-MM-DD)')

    # Subscriber DOB validation
    if data.get('subscriber_dob'):
        try:
            subscriber_dob = datetime.fromisoformat(data['subscriber_dob'].replace('Z', '+00:00')).date()
            
            # Check if DOB is realistic (not in the future and not too old)
            if subscriber_dob > datetime.utcnow().date():
                date_errors.append('Subscriber date of birth cannot be in the future')
            
            if subscriber_dob < datetime(1900, 1, 1).date():
                date_errors.append('Subscriber date of birth appears to be invalid')
                
        except ValueError:
            date_errors.append('Invalid subscriber date of birth format. Use ISO format (YYYY-MM-DD)')

    if date_errors:
        return jsonify({
            'error': 'Date validation failed',
            'date_errors': date_errors,
            'message': 'Please correct the date-related issues'
        }), 400

    # Validate coverage type
    valid_coverage_types = ['dental', 'medical', 'vision', 'combined', 'orthodontic', 'periodontal']
    if data.get('coverage_type') and data['coverage_type'] not in valid_coverage_types:
        return jsonify({
            'error': 'Invalid coverage type',
            'valid_types': valid_coverage_types,
            'message': f'Coverage type must be one of: {", ".join(valid_coverage_types)}'
        }), 400

    # Validate verification status
    valid_statuses = ['pending', 'verified', 'rejected', 'expired', 'suspended']
    if data.get('verification_status') and data['verification_status'] not in valid_statuses:
        return jsonify({
            'error': 'Invalid verification status',
            'valid_statuses': valid_statuses,
            'message': f'Verification status must be one of: {", ".join(valid_statuses)}'
        }), 400

    # Validate subscriber relationship
    valid_relationships = ['self', 'spouse', 'child', 'parent', 'domestic_partner', 'other']
    if data.get('subscriber_relationship') and data['subscriber_relationship'] not in valid_relationships:
        return jsonify({
            'error': 'Invalid subscriber relationship',
            'valid_relationships': valid_relationships,
            'message': f'Subscriber relationship must be one of: {", ".join(valid_relationships)}'
        }), 400

    # Validate string field lengths
    string_field_limits = {
        'insurance_provider': 200,
        'plan_name': 200,
        'policy_number': 100,
        'group_number': 100,
        'subscriber_id': 100,
        'subscriber_name': 200,
        'coverage_type': 100,
        'subscriber_relationship': 50
    }
    
    length_errors = []
    for field, max_length in string_field_limits.items():
        if data.get(field) and len(str(data[field])) > max_length:
            length_errors.append(f'{field.replace("_", " ").title()} exceeds maximum length of {max_length} characters')
    
    if length_errors:
        return jsonify({
            'error': 'Field length validation failed',
            'length_errors': length_errors,
            'message': 'Some fields exceed the maximum allowed length'
        }), 400

    # Validate numeric fields
    numeric_errors = []
    if data.get('annual_maximum'):
        try:
            annual_max = float(data['annual_maximum'])
            if annual_max < 0:
                numeric_errors.append('Annual maximum cannot be negative')
            if annual_max > 1000000:  # $1,000,000 limit
                numeric_errors.append('Annual maximum appears to be unrealistically high')
        except (ValueError, TypeError):
            numeric_errors.append('Annual maximum must be a valid number')

    if numeric_errors:
        return jsonify({
            'error': 'Numeric validation failed',
            'numeric_errors': numeric_errors,
            'message': 'Please check the numeric field values'
        }), 400

    # Validate JSON fields structure
    json_errors = []
    
    # Benefits validation
    if data.get('benefits'):
        if not isinstance(data['benefits'], dict):
            json_errors.append('Benefits must be a JSON object')
        else:
            # Validate common benefit structure
            benefits = data['benefits']
            if 'covered_procedures' in benefits and not isinstance(benefits['covered_procedures'], list):
                json_errors.append('Covered procedures must be a list')
            
            if 'coverage_percentage' in benefits:
                try:
                    coverage_pct = float(benefits['coverage_percentage'])
                    if not (0 <= coverage_pct <= 100):
                        json_errors.append('Coverage percentage must be between 0 and 100')
                except (ValueError, TypeError):
                    json_errors.append('Coverage percentage must be a valid number')

    # Copay info validation
    if data.get('copay_info'):
        if not isinstance(data['copay_info'], dict):
            json_errors.append('Copay information must be a JSON object')
        else:
            copay_info = data['copay_info']
            for key, value in copay_info.items():
                if isinstance(value, (int, float)) and value < 0:
                    json_errors.append(f'Copay for {key} cannot be negative')

    # Deductible info validation
    if data.get('deductible_info'):
        if not isinstance(data['deductible_info'], dict):
            json_errors.append('Deductible information must be a JSON object')
        else:
            deductible_info = data['deductible_info']
            for key, value in deductible_info.items():
                if isinstance(value, (int, float)) and value < 0:
                    json_errors.append(f'Deductible for {key} cannot be negative')

    if json_errors:
        return jsonify({
            'error': 'JSON structure validation failed',
            'json_errors': json_errors,
            'message': 'Please check the structure of JSON fields'
        }), 400

    # Validate email format if provided
    if data.get('subscriber_email'):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, data['subscriber_email']):
            return jsonify({
                'error': 'Invalid email format',
                'message': 'Please provide a valid email address for the subscriber'
            }), 400

    # Validate phone format if provided
    if data.get('subscriber_phone'):
        # Basic phone validation - allows international format
        phone_regex = r'^\+?[0-9]{1,3}?[-.\s]?\(?[0-9]{1,4}?\)?[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,9}$'
        if not re.match(phone_regex, data['subscriber_phone'].replace(' ', '').replace('-', '').replace('(', '').replace(')', '')):
            return jsonify({
                'error': 'Invalid phone number format',
                'message': 'Please provide a valid phone number for the subscriber'
            }), 400

    # Validate business logic: Cannot have both patient and family member
    if data.get('patient_id') and data.get('family_member_id'):
        return jsonify({
            'error': 'Conflicting relationships',
            'message': 'Insurance plan cannot be associated with both a patient and a family member simultaneously'
        }), 400

    # All validation passed
    return None


def validate_insurance_claim_data(data):
    """Validate insurance claim data"""
    required_fields = ['patient_id', 'appointment_id', 'insurance_provider', 'policy_number', 'submitted_amount']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        Decimal(str(data['submitted_amount']))
    except (ValueError, InvalidOperation):
        return jsonify({'error': 'Invalid submitted_amount format'}), 400
    
    return None

def validate_report_data(data):
    """Validate report creation/update data"""
    required_fields = ['title', 'report_type']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Additional validations can be added based on report_type and parameters
    
    return None

def validate_medical_record_data(data):
    """Validate medical record creation data"""
    required_fields = ['patient_id', 'type', 'title', 'content']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    return None

def validate_appointment_data(data):
    """Validate appointment creation/update data"""
    required_fields = ['patient_id', 'provider_id', 'service_id', 'start_time', 'end_time']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate datetime fields
    try:
        start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00'))
        if start_time >= end_time:
            return jsonify({'error': 'start_time must be before end_time'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use ISO format.'}), 400
    
    return None

def validate_vital_signs(data):
    """Validate vital signs data"""
    required_fields = ['patient_id', 'type', 'value', 'measured_at']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate measured_at datetime
    try:
        datetime.fromisoformat(data['measured_at'].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({'error': 'Invalid measured_at date format. Use ISO format.'}), 400
    
    return None

def validate_prescription(data):
    """Validate prescription creation data"""
    required_fields = ['patient_id', 'medication_name', 'dosage', 'frequency', 'prescribed_at']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate prescribed_at datetime
    try:
        datetime.fromisoformat(data['prescribed_at'].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({'error': 'Invalid prescribed_at date format. Use ISO format.'}), 400
    
    return None

def validate_inventory_item_data(data):
    """Validate inventory item data"""
    required_fields = ['name', 'quantity', 'unit_price']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        qty = int(data['quantity'])
        if qty < 0:
            return jsonify({'error': 'Quantity cannot be negative'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid quantity format'}), 400
    
    try:
        Decimal(str(data['unit_price']))
    except (ValueError, InvalidOperation):
        return jsonify({'error': 'Invalid unit_price format'}), 400
    
    return None

def validate_inventory_transaction_data(data):
    """Validate inventory transaction data"""
    required_fields = ['item_id', 'transaction_type', 'quantity']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    if data['transaction_type'] not in ['addition', 'removal', 'adjustment']:
        return jsonify({'error': 'Invalid transaction_type. Must be addition, removal, or adjustment'}), 400
    
    try:
        qty = int(data['quantity'])
        if qty <= 0:
            return jsonify({'error': 'Quantity must be positive'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid quantity format'}), 400
    
    return None


def validate_family_member_data(data):
    """
    Validate family member data before creating/updating
    """
    errors = []
    
    # Required fields
    required_fields = ['first_name', 'last_name', 'relationship', 'date_of_birth']
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"{field.replace('_', ' ').title()} is required")
    
    # Name validation
    if 'first_name' in data and data['first_name']:
        if len(data['first_name']) < 2:
            errors.append("First name must be at least 2 characters long")
        if not re.match(r'^[a-zA-Z\s\-]+$', data['first_name']):
            errors.append("First name can only contain letters, spaces, and hyphens")
    
    if 'last_name' in data and data['last_name']:
        if len(data['last_name']) < 2:
            errors.append("Last name must be at least 2 characters long")
        if not re.match(r'^[a-zA-Z\s\-]+$', data['last_name']):
            errors.append("Last name can only contain letters, spaces, and hyphens")
    
    # Relationship validation
    valid_relationships = ['spouse', 'child', 'parent', 'sibling', 'other']
    if 'relationship' in data and data['relationship']:
        if data['relationship'] not in valid_relationships:
            errors.append(f"Relationship must be one of: {', '.join(valid_relationships)}")
    
    # Date of birth validation
    if 'date_of_birth' in data and data['date_of_birth']:
        try:
            from datetime import datetime
            dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
            if dob > datetime.now():
                errors.append("Date of birth cannot be in the future")
        except ValueError:
            errors.append("Date of birth must be in YYYY-MM-DD format")
    
    # Email validation (optional field)
    if 'email' in data and data['email']:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['email']):
            errors.append("Invalid email format")
    
    # Phone validation (optional field)
    if 'phone' in data and data['phone']:
        # Basic phone validation - adjust as needed
        phone_pattern = r'^[\+]?[0-9\s\-\(\)]{10,15}$'
        if not re.match(phone_pattern, data['phone'].replace(' ', '')):
            errors.append("Invalid phone number format")
    
    return errors

# If you have other validation functions, they might look like:
def validate_patient_data(data):
    """Validate patient data"""
    errors = []
    # Add patient-specific validation logic
    return errors

def validate_appointment_data(data):
    """Validate appointment data"""
    errors = []
    # Add appointment-specific validation logic
    return errors



def validate_family_member_data(data):
    """Validate family member data"""
    errors = []
    
    # Required fields check
    required = ['first_name', 'last_name', 'relationship', 'date_of_birth']
    for field in required:
        if not data.get(field):
            errors.append(f"{field.replace('_', ' ').title()} is required")
    
    # Add your specific validation logic here
    return errors




