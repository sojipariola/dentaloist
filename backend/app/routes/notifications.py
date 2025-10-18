# routes/notifications.py
from flask import Blueprint, request, jsonify
from flask_login import current_user
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Import auth and tenancy utilities
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit

from ..models import Notification, db

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

# RBAC Permission Constants
PERMISSION_VIEW_NOTIFICATIONS = 'view_notifications'
PERMISSION_MANAGE_NOTIFICATIONS = 'manage_notifications'
PERMISSION_SEND_NOTIFICATIONS = 'send_notifications'

@notifications_bp.route('/', methods=['GET'])
@rate_limit(limit=120, period=3600)  # 120 requests per hour
@tenant_required
@permission_required(PERMISSION_VIEW_NOTIFICATIONS)
def get_notifications():
    """
    Get notifications with advanced filtering, sorting, and tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)  # Cap at 100 per page
        
        # Filter parameters
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        notification_type = request.args.get('type')
        priority = request.args.get('priority')
        category = request.args.get('category')
        
        # Date range filtering
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        # Build base query with tenant filtering
        query = multi_tenant_query(Notification.query, tenant_id)
        query = query.filter(Notification.user_id == user_id)
        
        # Apply filters
        if unread_only:
            query = query.filter(Notification.is_read == False)
        if notification_type:
            query = query.filter(Notification.type == notification_type)
        if priority:
            query = query.filter(Notification.priority == priority)
        if category:
            query = query.filter(Notification.category == category)
        
        # Date range filtering
        if start_date_str:
            try:
                start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                query = query.filter(Notification.created_at >= start_date)
            except ValueError:
                return jsonify({'error': 'Invalid start_date format. Use ISO format.'}), 400
        
        if end_date_str:
            try:
                end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                query = query.filter(Notification.created_at <= end_date)
            except ValueError:
                return jsonify({'error': 'Invalid end_date format. Use ISO format.'}), 400
        
        # Sorting
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        if sort_order.lower() == 'asc':
            query = query.order_by(getattr(Notification, sort_by).asc())
        else:
            query = query.order_by(getattr(Notification, sort_by).desc())
        
        # Pagination
        notifications = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Get notification statistics
        stats = _get_notification_stats(tenant_id, user_id)
        
        return jsonify({
            'notifications': [notif.to_dict() for notif in notifications.items],
            'pagination': {
                'page': notifications.page,
                'per_page': notifications.per_page,
                'total': notifications.total,
                'pages': notifications.pages,
                'has_next': notifications.has_next,
                'has_prev': notifications.has_prev
            },
            'filters': {
                'unread_only': unread_only,
                'type': notification_type,
                'priority': priority,
                'category': category,
                'start_date': start_date_str,
                'end_date': end_date_str
            },
            'statistics': stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve notifications', 'details': str(e)}), 500

@notifications_bp.route('/<int:notification_id>', methods=['GET'])
@rate_limit(limit=150, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_NOTIFICATIONS)
def get_notification(notification_id):
    """
    Get a specific notification with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(Notification.query, tenant_id)
        notification = query.filter_by(id=notification_id, user_id=user_id).first()
        
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        
        # Mark as read when retrieved individually
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            db.session.commit()
        
        return jsonify(notification.to_dict(include_details=True)), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve notification', 'details': str(e)}), 500

@notifications_bp.route('/<int:notification_id>/read', methods=['POST'])
@rate_limit(limit=100, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_NOTIFICATIONS)
def mark_as_read(notification_id):
    """
    Mark a specific notification as read
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(Notification.query, tenant_id)
        notification = query.filter_by(id=notification_id, user_id=user_id).first()
        
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        
        if notification.is_read:
            return jsonify({'message': 'Notification is already read'}), 200
        
        notification.is_read = True
        notification.read_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Notification marked as read',
            'notification': notification.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to mark notification as read', 'details': str(e)}), 500

@notifications_bp.route('/<int:notification_id>/unread', methods=['POST'])
@rate_limit(limit=100, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_NOTIFICATIONS)
def mark_as_unread(notification_id):
    """
    Mark a specific notification as unread
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(Notification.query, tenant_id)
        notification = query.filter_by(id=notification_id, user_id=user_id).first()
        
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        
        if not notification.is_read:
            return jsonify({'message': 'Notification is already unread'}), 200
        
        notification.is_read = False
        notification.read_at = None
        db.session.commit()
        
        return jsonify({
            'message': 'Notification marked as unread',
            'notification': notification.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to mark notification as unread', 'details': str(e)}), 500

@notifications_bp.route('/read-all', methods=['POST'])
@rate_limit(limit=50, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_NOTIFICATIONS)
def mark_all_as_read():
    """
    Mark all notifications as read for the current user
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        # Get unread notifications count before update
        unread_count = multi_tenant_query(Notification.query, tenant_id).filter_by(
            user_id=user_id, is_read=False
        ).count()
        
        if unread_count == 0:
            return jsonify({'message': 'No unread notifications'}), 200
        
        # Mark all as read
        updated_count = multi_tenant_query(Notification.query, tenant_id).filter_by(
            user_id=user_id, is_read=False
        ).update({
            'is_read': True,
            'read_at': datetime.utcnow()
        })
        
        db.session.commit()
        
        return jsonify({
            'message': f'Marked {updated_count} notifications as read',
            'marked_read': updated_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to mark notifications as read', 'details': str(e)}), 500

@notifications_bp.route('/clear-all', methods=['POST'])
@rate_limit(limit=30, period=3600)
@tenant_required
@permission_required(PERMISSION_MANAGE_NOTIFICATIONS)
def clear_all_notifications():
    """
    Clear all notifications for the current user (mark as read and archive)
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        # Get total notifications count before update
        total_count = multi_tenant_query(Notification.query, tenant_id).filter_by(
            user_id=user_id
        ).count()
        
        if total_count == 0:
            return jsonify({'message': 'No notifications to clear'}), 200
        
        # Mark all as read and archived
        updated_count = multi_tenant_query(Notification.query, tenant_id).filter_by(
            user_id=user_id
        ).update({
            'is_read': True,
            'is_archived': True,
            'read_at': datetime.utcnow(),
            'archived_at': datetime.utcnow()
        })
        
        db.session.commit()
        
        return jsonify({
            'message': f'Cleared {updated_count} notifications',
            'cleared_count': updated_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to clear notifications', 'details': str(e)}), 500

@notifications_bp.route('/preferences', methods=['GET', 'PUT'])
@rate_limit(limit=60, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_NOTIFICATIONS)
def manage_notification_preferences():
    """
    Get or update notification preferences for the current user
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        if request.method == 'GET':
            preferences = _get_notification_preferences(tenant_id, user_id)
            return jsonify(preferences), 200
        
        elif request.method == 'PUT':
            data = request.get_json()
            updated_preferences = _update_notification_preferences(tenant_id, user_id, data)
            return jsonify({
                'message': 'Notification preferences updated successfully',
                'preferences': updated_preferences
            }), 200
            
    except Exception as e:
        return jsonify({'error': 'Failed to manage notification preferences', 'details': str(e)}), 500

@notifications_bp.route('/send', methods=['POST'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_SEND_NOTIFICATIONS)
def send_notification():
    """
    Send a notification to one or more users (admin/lab staff functionality)
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        sender_id = current_user_obj.id
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_ids', 'title', 'message']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        user_ids = data['user_ids']
        if not isinstance(user_ids, list) or len(user_ids) == 0:
            return jsonify({'error': 'user_ids must be a non-empty list'}), 400
        
        # Verify all users belong to the same tenant
        from ..models import User
        user_query = multi_tenant_query(User.query, tenant_id)
        valid_users = user_query.filter(User.id.in_(user_ids)).all()
        
        if len(valid_users) != len(user_ids):
            return jsonify({'error': 'One or more users not found or access denied'}), 400
        
        # Create notifications
        notifications = []
        for user_id in user_ids:
            notification = Notification(
                tenant_id=tenant_id,
                user_id=user_id,
                title=data['title'],
                message=data['message'],
                type=data.get('type', 'system'),
                priority=data.get('priority', 'medium'),
                category=data.get('category', 'general'),
                action_url=data.get('action_url'),
                sender_id=sender_id
            )
            
            notifications.append(notification)
            db.session.add(notification)
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, sender_id, 'create', 'notification', None, 
                           f'Sent notification to {len(user_ids)} users: {data["title"]}')
        
        return jsonify({
            'message': f'Notification sent to {len(user_ids)} users successfully',
            'sent_count': len(user_ids),
            'notification_ids': [n.id for n in notifications]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to send notification', 'details': str(e)}), 500

@notifications_bp.route('/stats', methods=['GET'])
@rate_limit(limit=80, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_NOTIFICATIONS)
def get_notification_statistics():
    """
    Get notification statistics and analytics
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        days = int(request.args.get('days', 30))
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        stats = {
            'user_stats': _get_user_notification_stats(tenant_id, user_id, start_date, end_date),
            'engagement_metrics': _get_engagement_metrics(tenant_id, user_id, start_date, end_date),
            'category_breakdown': _get_category_breakdown(tenant_id, user_id, start_date, end_date)
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve notification statistics', 'details': str(e)}), 500

@notifications_bp.route('/bulk-action', methods=['POST'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_NOTIFICATIONS)
def bulk_notification_actions():
    """
    Perform bulk actions on notifications (read, unread, archive)
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        data = request.get_json()
        
        action = data.get('action')  # read, unread, archive, delete
        notification_ids = data.get('notification_ids', [])
        
        if not action or not notification_ids:
            return jsonify({'error': 'action and notification_ids are required'}), 400
        
        if action not in ['read', 'unread', 'archive', 'delete']:
            return jsonify({'error': 'Invalid action. Use read, unread, archive, or delete'}), 400
        
        query = multi_tenant_query(Notification.query, tenant_id)
        notifications = query.filter(
            Notification.id.in_(notification_ids),
            Notification.user_id == user_id
        ).all()
        
        if len(notifications) != len(notification_ids):
            return jsonify({'error': 'One or more notifications not found or access denied'}), 400
        
        update_data = {}
        if action == 'read':
            update_data = {'is_read': True, 'read_at': datetime.utcnow()}
        elif action == 'unread':
            update_data = {'is_read': False, 'read_at': None}
        elif action == 'archive':
            update_data = {'is_archived': True, 'archived_at': datetime.utcnow()}
        elif action == 'delete':
            # Actually delete the notifications
            for notification in notifications:
                db.session.delete(notification)
            db.session.commit()
            return jsonify({
                'message': f'Deleted {len(notifications)} notifications successfully',
                'deleted_count': len(notifications)
            }), 200
        
        # Update notifications
        for notification in notifications:
            for key, value in update_data.items():
                setattr(notification, key, value)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Performed {action} action on {len(notifications)} notifications successfully',
            'processed_count': len(notifications)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to perform bulk action', 'details': str(e)}), 500

# Helper functions with tenant filtering
def _get_notification_stats(tenant_id: str, user_id: int) -> Dict[str, Any]:
    """Get notification statistics for the user"""
    query = multi_tenant_query(Notification.query, tenant_id)
    user_notifications = query.filter_by(user_id=user_id)
    
    total_count = user_notifications.count()
    unread_count = user_notifications.filter_by(is_read=False).count()
    high_priority_count = user_notifications.filter_by(priority='high', is_read=False).count()
    
    # Count by type
    type_counts = user_notifications.filter_by(is_read=False)\
                                  .group_by(Notification.type)\
                                  .with_entities(Notification.type, db.func.count(Notification.id))\
                                  .all()
    
    return {
        'total_count': total_count,
        'unread_count': unread_count,
        'high_priority_unread': high_priority_count,
        'unread_by_type': {notif_type: count for notif_type, count in type_counts}
    }

def _get_notification_preferences(tenant_id: str, user_id: int) -> Dict[str, Any]:
    """Get notification preferences for the user"""
    # This would typically come from a UserPreferences model
    # For now, return default preferences
    return {
        'email_notifications': True,
        'push_notifications': True,
        'sms_notifications': False,
        'categories': {
            'appointments': True,
            'lab_results': True,
            'billing': True,
            'system': True,
            'marketing': False
        },
        'quiet_hours': {
            'enabled': False,
            'start_time': '22:00',
            'end_time': '07:00'
        },
        'priority_filter': 'medium'  # low, medium, high, all
    }

def _update_notification_preferences(tenant_id: str, user_id: int, preferences_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update notification preferences for the user"""
    # This would typically update a UserPreferences model
    # For now, just return the received data with defaults
    default_preferences = _get_notification_preferences(tenant_id, user_id)
    updated_preferences = {**default_preferences, **preferences_data}
    return updated_preferences

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

def _get_user_notification_stats(tenant_id: str, user_id: int, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get user notification statistics for a date range"""
    query = multi_tenant_query(Notification.query, tenant_id)
    notifications = query.filter(
        Notification.user_id == user_id,
        Notification.created_at.between(start_date, end_date)
    )
    
    total_received = notifications.count()
    read_count = notifications.filter_by(is_read=True).count()
    clicked_count = notifications.filter(Notification.action_taken.isnot(None)).count()
    
    return {
        'total_received': total_received,
        'read_count': read_count,
        'clicked_count': clicked_count,
        'read_rate': (read_count / total_received * 100) if total_received > 0 else 0,
        'click_through_rate': (clicked_count / total_received * 100) if total_received > 0 else 0
    }

def _get_engagement_metrics(tenant_id: str, user_id: int, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get notification engagement metrics"""
    query = multi_tenant_query(Notification.query, tenant_id)
    notifications = query.filter(
        Notification.user_id == user_id,
        Notification.created_at.between(start_date, end_date)
    )
    
    # Average time to read
    avg_time_to_read = notifications.filter(
        Notification.is_read == True,
        Notification.read_at.isnot(None)
    ).with_entities(
        db.func.avg(Notification.read_at - Notification.created_at)
    ).scalar()
    
    return {
        'average_time_to_read_minutes': avg_time_to_read.total_seconds() / 60 if avg_time_to_read else 0,
        'most_engaged_category': _get_most_engaged_category(tenant_id, user_id, start_date, end_date)
    }

def _get_most_engaged_category(tenant_id: str, user_id: int, start_date: datetime, end_date: datetime) -> str:
    """Get the category with highest engagement"""
    query = multi_tenant_query(Notification.query, tenant_id)
    category_engagement = query.filter(
        Notification.user_id == user_id,
        Notification.created_at.between(start_date, end_date),
        Notification.is_read == True
    ).group_by(Notification.category)\
     .with_entities(
         Notification.category,
         db.func.count(Notification.id),
         db.func.avg(Notification.read_at - Notification.created_at)
     ).order_by(db.func.count(Notification.id).desc())\
     .first()
    
    return category_engagement[0] if category_engagement else 'None'

def _get_category_breakdown(tenant_id: str, user_id: int, start_date: datetime, end_date: datetime) -> Dict[str, int]:
    """Get notification breakdown by category"""
    query = multi_tenant_query(Notification.query, tenant_id)
    category_breakdown = query.filter(
        Notification.user_id == user_id,
        Notification.created_at.between(start_date, end_date)
    ).group_by(Notification.category)\
     .with_entities(Notification.category, db.func.count(Notification.id))\
     .all()
    
    return {category: count for category, count in category_breakdown}

@notifications_bp.errorhandler(403)
def handle_permission_error(e):
    return jsonify({'error': 'Access forbidden', 'message': 'Insufficient permissions'}), 403

@notifications_bp.errorhandler(401)
def handle_authentication_error(e):
    return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401

@notifications_bp.errorhandler(429)
def handle_rate_limit_error(e):
    return jsonify({'error': 'Rate limit exceeded', 'message': 'Too many requests'}), 429