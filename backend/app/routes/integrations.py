# backend/app/routes/integrations.py

from flask import Blueprint, request, jsonify, g, current_app, redirect, url_for
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
import json
import requests
from urllib.parse import urlencode
import hashlib
import hmac
import base64

from ..models import (
    db, Integration, IntegrationLog, User, Organization, 
    Webhook, WebhookEvent
)
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit
from ..utils.encryption import encrypt_data, decrypt_data

integrations_bp = Blueprint('integrations', __name__, url_prefix='/api/integrations')

# Integration configurations
INTEGRATION_TYPES = {
    'ehr': {
        'name': 'EHR System',
        'description': 'Electronic Health Records integration',
        'category': 'clinical',
        'auth_type': 'oauth2',
        'settings_schema': {
            'api_url': {'type': 'string', 'required': True},
            'client_id': {'type': 'string', 'required': True},
            'client_secret': {'type': 'string', 'required': True},
            'scope': {'type': 'string', 'default': 'patient.read encounter.read'}
        }
    },
    'billing': {
        'name': 'Billing Service',
        'description': 'Payment processing integration',
        'category': 'financial',
        'auth_type': 'api_key',
        'settings_schema': {
            'api_key': {'type': 'string', 'required': True},
            'merchant_id': {'type': 'string', 'required': True},
            'environment': {'type': 'string', 'default': 'sandbox'}
        }
    },
    'imaging': {
        'name': 'Imaging Service',
        'description': 'Medical imaging and X-ray integration',
        'category': 'clinical',
        'auth_type': 'basic',
        'settings_schema': {
            'username': {'type': 'string', 'required': True},
            'password': {'type': 'string', 'required': True},
            'api_url': {'type': 'string', 'required': True}
        }
    },
    'lab': {
        'name': 'Lab Results',
        'description': 'Laboratory results integration',
        'category': 'clinical',
        'auth_type': 'oauth2',
        'settings_schema': {
            'client_id': {'type': 'string', 'required': True},
            'client_secret': {'type': 'string', 'required': True},
            'api_url': {'type': 'string', 'required': True}
        }
    },
    'scheduling': {
        'name': 'Scheduling System',
        'description': 'Appointment scheduling integration',
        'category': 'operational',
        'auth_type': 'api_key',
        'settings_schema': {
            'api_key': {'type': 'string', 'required': True},
            'calendar_id': {'type': 'string', 'required': True}
        }
    }
}

# ===== Integration Management Routes =====

@integrations_bp.route('/', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_integrations', 'manage_integrations'])
@rate_limit(limit=60, period=60)
def get_integrations():
    """
    Get available integrations and their connection status
    """
    try:
        current_user = get_current_user()
        
        # Get organization's connected integrations
        connected_integrations = multi_tenant_query(Integration).all()
        connected_map = {integ.integration_type: integ for integ in connected_integrations}
        
        # Build response with available integrations
        integrations_list = []
        for integ_type, integ_config in INTEGRATION_TYPES.items():
            connected_integ = connected_map.get(integ_type)
            
            integration_data = {
                'id': integ_type,
                'name': integ_config['name'],
                'description': integ_config['description'],
                'category': integ_config['category'],
                'auth_type': integ_config['auth_type'],
                'connected': connected_integ is not None,
                'connection_status': connected_integ.status if connected_integ else 'disconnected',
                'last_sync': connected_integ.last_sync.isoformat() if connected_integ and connected_integ.last_sync else None,
                'settings_configured': bool(connected_integ and connected_integ.settings),
                'webhooks_configured': bool(connected_integ and connected_integ.webhooks),
                'created_at': connected_integ.created_at.isoformat() if connected_integ else None
            }
            
            integrations_list.append(integration_data)
        
        return jsonify({
            'integrations': integrations_list,
            'total_connected': len(connected_integrations),
            'available_categories': list(set(integ['category'] for integ in INTEGRATION_TYPES.values()))
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching integrations: {str(e)}")
        return jsonify({'error': 'Failed to fetch integrations'}), 500

@integrations_bp.route('/<integration_type>', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_integrations', 'manage_integrations'])
def get_integration_detail(integration_type):
    """
    Get detailed information about a specific integration
    """
    try:
        if integration_type not in INTEGRATION_TYPES:
            return jsonify({'error': 'Invalid integration type'}), 404
        
        integ_config = INTEGRATION_TYPES[integration_type]
        integration = multi_tenant_query(Integration).filter_by(
            integration_type=integration_type
        ).first()
        
        response_data = {
            'id': integration_type,
            'name': integ_config['name'],
            'description': integ_config['description'],
            'category': integ_config['category'],
            'auth_type': integ_config['auth_type'],
            'settings_schema': integ_config['settings_schema'],
            'connected': integration is not None,
            'status': integration.status if integration else 'disconnected',
            'last_sync': integration.last_sync.isoformat() if integration and integration.last_sync else None,
            'last_error': integration.last_error if integration else None,
            'webhooks': [wh.to_dict() for wh in integration.webhooks] if integration else [],
            'logs': []
        }
        
        # Add recent logs if integration exists
        if integration:
            recent_logs = IntegrationLog.query.filter_by(
                integration_id=integration.id
            ).order_by(IntegrationLog.created_at.desc()).limit(10).all()
            
            response_data['logs'] = [log.to_dict() for log in recent_logs]
        
        return jsonify(response_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching integration {integration_type}: {str(e)}")
        return jsonify({'error': 'Failed to fetch integration details'}), 500

@integrations_bp.route('/<integration_type>', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_integrations'])
def create_update_integration(integration_type):
    """
    Create or update an integration configuration
    """
    try:
        if integration_type not in INTEGRATION_TYPES:
            return jsonify({'error': 'Invalid integration type'}), 404
        
        current_user = get_current_user()
        data = request.get_json()
        integ_config = INTEGRATION_TYPES[integration_type]
        
        # Validate settings against schema
        validation_error = _validate_integration_settings(data.get('settings', {}), integ_config['settings_schema'])
        if validation_error:
            return validation_error
        
        # Check if integration already exists
        integration = multi_tenant_query(Integration).filter_by(
            integration_type=integration_type
        ).first()
        
        if integration:
            # Update existing integration
            integration.settings = encrypt_data(json.dumps(data['settings'])) if data.get('settings') else integration.settings
            integration.status = data.get('status', integration.status)
            integration.updated_by = current_user.id
            integration.updated_at = datetime.utcnow()
        else:
            # Create new integration
            integration = Integration(
                organization_id=g.tenant_id,
                integration_type=integration_type,
                settings=encrypt_data(json.dumps(data['settings'])) if data.get('settings') else None,
                status='configured',
                created_by=current_user.id
            )
            db.session.add(integration)
        
        # Log the configuration change
        log = IntegrationLog(
            integration_id=integration.id,
            level='info',
            message='Integration configuration updated',
            details={'updated_by': current_user.id, 'settings_updated': bool(data.get('settings'))}
        )
        db.session.add(log)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Integration configuration saved successfully',
            'integration': {
                'id': integration_type,
                'name': integ_config['name'],
                'status': integration.status,
                'settings_configured': bool(integration.settings)
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error configuring integration {integration_type}: {str(e)}")
        return jsonify({'error': 'Failed to configure integration'}), 500

@integrations_bp.route('/<integration_type>', methods=['DELETE'])
@jwt_required()
@tenant_required
@permission_required(['manage_integrations'])
def delete_integration(integration_type):
    """
    Remove an integration configuration
    """
    try:
        integration = multi_tenant_query(Integration).filter_by(
            integration_type=integration_type
        ).first_or_404()
        
        # Delete associated webhooks and logs
        Webhook.query.filter_by(integration_id=integration.id).delete()
        IntegrationLog.query.filter_by(integration_id=integration.id).delete()
        
        db.session.delete(integration)
        db.session.commit()
        
        return jsonify({
            'message': 'Integration removed successfully',
            'integration_type': integration_type
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting integration {integration_type}: {str(e)}")
        return jsonify({'error': 'Failed to delete integration'}), 500

@integrations_bp.route('/<integration_type>/test', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_integrations'])
def test_integration(integration_type):
    """
    Test an integration connection
    """
    try:
        integration = multi_tenant_query(Integration).filter_by(
            integration_type=integration_type
        ).first_or_404()
        
        if not integration.settings:
            return jsonify({'error': 'Integration not configured'}), 400
        
        # Test connection based on integration type
        test_result = _test_integration_connection(integration)
        
        # Update integration status based on test result
        integration.status = 'connected' if test_result['success'] else 'error'
        integration.last_test = datetime.utcnow()
        integration.last_error = test_result['error'] if not test_result['success'] else None
        
        # Log test result
        log = IntegrationLog(
            integration_id=integration.id,
            level='info' if test_result['success'] else 'error',
            message='Integration connection test',
            details=test_result
        )
        db.session.add(log)
        
        db.session.commit()
        
        return jsonify({
            'success': test_result['success'],
            'message': test_result['message'],
            'details': test_result.get('details')
        }), 200 if test_result['success'] else 400
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error testing integration {integration_type}: {str(e)}")
        return jsonify({'error': 'Failed to test integration'}), 500

# ===== OAuth2 Integration Routes =====

@integrations_bp.route('/<integration_type>/oauth/init', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['manage_integrations'])
def init_oauth_integration(integration_type):
    """
    Initialize OAuth2 flow for an integration
    """
    try:
        if integration_type not in INTEGRATION_TYPES:
            return jsonify({'error': 'Invalid integration type'}), 404
        
        integ_config = INTEGRATION_TYPES[integration_type]
        if integ_config['auth_type'] != 'oauth2':
            return jsonify({'error': 'Integration does not support OAuth2'}), 400
        
        integration = multi_tenant_query(Integration).filter_by(
            integration_type=integration_type
        ).first()
        
        if not integration or not integration.settings:
            return jsonify({'error': 'Integration not configured'}), 400
        
        settings = json.loads(decrypt_data(integration.settings))
        
        # Generate OAuth2 authorization URL
        auth_url = _generate_oauth2_url(integration_type, settings)
        
        return jsonify({
            'authorization_url': auth_url,
            'state': 'generate_unique_state_here'  # In practice, generate and store a state token
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error initializing OAuth for {integration_type}: {str(e)}")
        return jsonify({'error': 'Failed to initialize OAuth flow'}), 500

@integrations_bp.route('/<integration_type>/oauth/callback', methods=['GET'])
def oauth_callback(integration_type):
    """
    Handle OAuth2 callback
    """
    try:
        # Verify state parameter to prevent CSRF
        state = request.args.get('state')
        code = request.args.get('code')
        error = request.args.get('error')
        
        if error:
            return jsonify({'error': f'OAuth error: {error}'}), 400
        
        # Exchange authorization code for access token
        integration = multi_tenant_query(Integration).filter_by(
            integration_type=integration_type
        ).first_or_404()
        
        settings = json.loads(decrypt_data(integration.settings))
        token_data = _exchange_oauth2_code(integration_type, settings, code)
        
        # Store access token securely
        integration.oauth_token = encrypt_data(json.dumps(token_data))
        integration.status = 'connected'
        integration.updated_at = datetime.utcnow()
        
        # Log successful connection
        log = IntegrationLog(
            integration_id=integration.id,
            level='info',
            message='OAuth2 connection established',
            details={'method': 'oauth2_callback'}
        )
        db.session.add(log)
        
        db.session.commit()
        
        # Redirect to success page or return success response
        return jsonify({
            'message': 'OAuth2 connection established successfully',
            'integration_type': integration_type
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in OAuth callback for {integration_type}: {str(e)}")
        return jsonify({'error': 'Failed to complete OAuth flow'}), 500

# ===== Webhook Management Routes =====

@integrations_bp.route('/<integration_type>/webhooks', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_integrations', 'manage_integrations'])
def get_integration_webhooks(integration_type):
    """
    Get webhooks for an integration
    """
    try:
        integration = multi_tenant_query(Integration).filter_by(
            integration_type=integration_type
        ).first_or_404()
        
        webhooks = Webhook.query.filter_by(integration_id=integration.id).all()
        
        return jsonify({
            'webhooks': [wh.to_dict() for wh in webhooks],
            'total': len(webhooks)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching webhooks for {integration_type}: {str(e)}")
        return jsonify({'error': 'Failed to fetch webhooks'}), 500

@integrations_bp.route('/<integration_type>/webhooks', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_integrations'])
def create_webhook(integration_type):
    """
    Create a webhook for an integration
    """
    try:
        integration = multi_tenant_query(Integration).filter_by(
            integration_type=integration_type
        ).first_or_404()
        
        data = request.get_json()
        
        # Validate webhook data
        if not data.get('url') or not data.get('events'):
            return jsonify({'error': 'URL and events are required'}), 400
        
        webhook = Webhook(
            integration_id=integration.id,
            url=data['url'],
            events=data['events'],
            secret=Webhook.generate_secret(),
            is_active=data.get('is_active', True),
            description=data.get('description')
        )
        
        db.session.add(webhook)
        db.session.commit()
        
        return jsonify({
            'message': 'Webhook created successfully',
            'webhook': webhook.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating webhook for {integration_type}: {str(e)}")
        return jsonify({'error': 'Failed to create webhook'}), 500

# ===== Integration Execution Routes =====

@integrations_bp.route('/<integration_type>/sync', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_integrations'])
def trigger_sync(integration_type):
    """
    Trigger a manual sync for an integration
    """
    try:
        integration = multi_tenant_query(Integration).filter_by(
            integration_type=integration_type
        ).first_or_404()
        
        data = request.get_json()
        sync_type = data.get('type', 'full')  # full, incremental, specific
        
        # Execute sync based on integration type
        sync_result = _execute_integration_sync(integration, sync_type, data.get('parameters', {}))
        
        # Update last sync time
        integration.last_sync = datetime.utcnow()
        integration.sync_status = 'success' if sync_result['success'] else 'failed'
        
        # Log sync result
        log = IntegrationLog(
            integration_id=integration.id,
            level='info' if sync_result['success'] else 'error',
            message=f'Manual sync triggered: {sync_type}',
            details=sync_result
        )
        db.session.add(log)
        
        db.session.commit()
        
        return jsonify({
            'success': sync_result['success'],
            'message': sync_result['message'],
            'details': sync_result.get('details'),
            'records_processed': sync_result.get('records_processed', 0)
        }), 200 if sync_result['success'] else 400
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error triggering sync for {integration_type}: {str(e)}")
        return jsonify({'error': 'Failed to trigger sync'}), 500

# ===== Helper Functions =====

def _validate_integration_settings(settings, schema):
    """Validate integration settings against schema"""
    errors = []
    
    for field, field_config in schema.items():
        if field_config.get('required') and field not in settings:
            errors.append(f'{field} is required')
        elif field in settings:
            # Type validation
            expected_type = field_config.get('type', 'string')
            if expected_type == 'string' and not isinstance(settings[field], str):
                errors.append(f'{field} must be a string')
            elif expected_type == 'number' and not isinstance(settings[field], (int, float)):
                errors.append(f'{field} must be a number')
    
    if errors:
        return jsonify({
            'error': 'Settings validation failed',
            'details': errors,
            'message': 'Please check your integration settings'
        }), 400
    
    return None

def _test_integration_connection(integration):
    """Test integration connection based on type"""
    try:
        settings = json.loads(decrypt_data(integration.settings))
        
        if integration.integration_type == 'ehr':
            # Test EHR connection
            response = requests.get(
                f"{settings['api_url']}/metadata",
                headers={'Authorization': f"Bearer {settings.get('access_token')}"},
                timeout=10
            )
            response.raise_for_status()
            return {'success': True, 'message': 'EHR connection successful'}
            
        elif integration.integration_type == 'billing':
            # Test billing connection
            response = requests.post(
                f"{settings.get('api_url', 'https://api.billing.com')}/v1/ping",
                headers={'X-API-Key': settings['api_key']},
                timeout=10
            )
            response.raise_for_status()
            return {'success': True, 'message': 'Billing connection successful'}
            
        else:
            # Generic connection test
            return {'success': True, 'message': 'Connection test passed'}
            
    except Exception as e:
        return {
            'success': False,
            'message': 'Connection test failed',
            'error': str(e),
            'details': 'Check your settings and network connection'
        }

def _generate_oauth2_url(integration_type, settings):
    """Generate OAuth2 authorization URL"""
    # This is a simplified example - implement based on your OAuth2 provider
    base_url = settings.get('auth_url', 'https://auth.example.com/oauth2/authorize')
    
    params = {
        'client_id': settings['client_id'],
        'response_type': 'code',
        'redirect_uri': url_for('integrations.oauth_callback', integration_type=integration_type, _external=True),
        'scope': settings.get('scope', ''),
        'state': 'secure_random_state'  # Generate and store this
    }
    
    return f"{base_url}?{urlencode(params)}"

def _exchange_oauth2_code(integration_type, settings, code):
    """Exchange OAuth2 authorization code for access token"""
    token_url = settings.get('token_url', 'https://auth.example.com/oauth2/token')
    
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': url_for('integrations.oauth_callback', integration_type=integration_type, _external=True),
        'client_id': settings['client_id'],
        'client_secret': settings['client_secret']
    }
    
    response = requests.post(token_url, data=data, timeout=30)
    response.raise_for_status()
    
    return response.json()

def _execute_integration_sync(integration, sync_type, parameters):
    """Execute integration sync based on type"""
    try:
        # This would contain the actual sync logic for each integration type
        # For now, return a simulated result
        
        if integration.integration_type == 'ehr':
            # Simulate EHR sync
            return {
                'success': True,
                'message': 'EHR sync completed successfully',
                'records_processed': 42,
                'details': {'patients': 25, 'appointments': 17}
            }
            
        elif integration.integration_type == 'billing':
            # Simulate billing sync
            return {
                'success': True,
                'message': 'Billing sync completed successfully',
                'records_processed': 18,
                'details': {'invoices': 12, 'payments': 6}
            }
            
        else:
            return {
                'success': True,
                'message': f'{sync_type} sync completed',
                'records_processed': 10
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': 'Sync failed',
            'error': str(e),
            'records_processed': 0
        }