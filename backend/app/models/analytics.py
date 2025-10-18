




# WidgetConfig
"""Analytics models for Dentaloist"""
from .base import BaseModel
from . import db, WidgetType, User, Organization
from .lookups import AuditAction
from sqlalchemy import (Column, Integer, String, Text, Boolean, DateTime, ForeignKey, 
            JSON, Float, Numeric, CheckConstraint, LargeBinary, func, and_, or_)
from datetime import datetime


# =============================================================================
# CORE ANALYTICS CLASSES   
# =============================================================================

class AnalyticsDashboard(BaseModel):
    """Analytics dashboard model"""
    __tablename__ = 'analytics_dashboards'
    
    # Basic identification
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    
    # Configuration
    layout_config = db.Column(db.JSON, default=dict)
    filters = db.Column(db.JSON, default=dict)
    is_public = db.Column(db.Boolean, default=False)
    is_default = db.Column(db.Boolean, default=False)
    
    # Display properties
    theme = db.Column(db.String(50), default='light')
    refresh_interval = db.Column(db.Integer, default=300)  # seconds
    
    # Access control
    allowed_users = db.Column(db.JSON, default=list)  # List of user IDs who can access
    allowed_roles = db.Column(db.JSON, default=list)  # List of roles who can access
    
    # Relationships
    # widgets = db.relationship('AnalyticsWidget', back_populates='dashboard_widgets', cascade='all, delete-orphan', lazy='dynamic')
    widgets = db.relationship('AnalyticsWidget', back_populates='dashboard', cascade='all, delete-orphan', lazy='dynamic')
    layouts = db.relationship('DashboardLayout', backref='dashboard_layouts_analytics', cascade='all, delete-orphan')
    events = db.relationship('AnalyticsEvent', backref='dashboard_events_analytics')
    # Make sure these relationships exist:
    user = db.relationship('User', backref='analytics_dashboards')
    organization = db.relationship('Organization', back_populates='analytics_dashboards') 


class AnalyticsWidget(BaseModel):
    """Analytics widget model for dashboards"""
    __tablename__ = 'analytics_widgets'
    
    # Basic identification
    dashboard_id = db.Column(db.Integer, db.ForeignKey('analytics_dashboards.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    widget_type_id = db.Column(db.Integer, db.ForeignKey('widget_types.id'), nullable=False)
    
    # Data configuration
    data_source = db.Column(db.String(200), nullable=False)  # API endpoint, SQL query, etc.
    query_parameters = db.Column(db.JSON, default=dict)
    refresh_interval = db.Column(db.Integer, default=300)  # seconds
    
    # Display properties
    position_x = db.Column(db.Integer, default=0)
    position_y = db.Column(db.Integer, default=0)
    width = db.Column(db.Integer, default=4)
    height = db.Column(db.Integer, default=4)
    
    # Styling
    background_color = db.Column(db.String(7), default='#FFFFFF')  # Hex color
    text_color = db.Column(db.String(7), default='#000000')  # Hex color
    border_style = db.Column(db.String(20), default='solid')
    
    # Configuration
    configuration = db.Column(db.JSON, default=dict)  # Chart options, filters, etc.
    filters = db.Column(db.JSON, default=dict)  # User-applied filters
    
    # Visibility and state
    is_visible = db.Column(db.Boolean, default=True)
    is_enabled = db.Column(db.Boolean, default=True)
    is_resizable = db.Column(db.Boolean, default=True)
    is_draggable = db.Column(db.Boolean, default=True)
    
    # Caching
    cached_data = db.Column(db.JSON)
    cached_at = db.Column(DateTime)
    cache_ttl = db.Column(db.Integer, default=300)  # seconds
    
    # Performance metrics
    render_time = db.Column(db.Float)  # Time taken to render in milliseconds
    data_load_time = db.Column(db.Float)  # Time taken to load data in milliseconds
    
    # Relationships
    dashboard = db.relationship('AnalyticsDashboard', back_populates='widgets')
    widget_type = db.relationship('WidgetType', backref='widgets')
    data_cache = db.relationship('WidgetDataCache', backref='widget_data_cache', cascade='all, delete-orphan')
    events = db.relationship('AnalyticsEvent', backref='widget_analytics')

class Widget(BaseModel):
    """Legacy Widget model (consider migrating to AnalyticsWidget)"""
    __tablename__ = 'widgets'
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    widget_type = db.Column(db.String(50), nullable=False)
    configuration = db.Column(db.JSON, default=dict)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('legacy_widgets', lazy=True))

    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)
    organization = db.relationship("Organization", back_populates="organization_widgets")

    is_active = db.Column(db.Boolean, default=True)
    position = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Widget {self.name}>'


class WidgetConfig(BaseModel):
    """Widget configuration model"""
    __tablename__ = 'widget_configs'
    
    widget_id = db.Column(db.Integer, db.ForeignKey('widgets.id'), nullable=False)
    config_key = db.Column(db.String(100), nullable=False)
    config_value = db.Column(db.Text)
    config_type = db.Column(db.String(20), default='string')
    
    # ADD THESE FIELDS IF THEY'RE MISSING:
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id')) 
    
    # ADD THESE RELATIONSHIPS:
    user = db.relationship('User', backref='user_widget_configs') 
    organization = db.relationship('Organization', backref='organization_widget_configs') 
    widget = db.relationship('Widget', backref='configs')  # ← MAKE SURE THIS EXISTS

    def __repr__(self):
        return f'<WidgetConfig {self.config_key}>'


# =============================================================================
# SUPPORTING CLASSES
# =============================================================================

class DashboardLayout(BaseModel):
    """Dashboard layout configurations"""
    __tablename__ = 'dashboard_layouts'
    
    dashboard_id = db.Column(db.Integer, db.ForeignKey('analytics_dashboards.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    layout_name = db.Column(db.String(100), nullable=False)  # 'default', 'mobile', 'print', etc.
    
    # Layout configuration
    layout_config = db.Column(db.JSON, default=dict)  # Grid layout configuration
    widget_positions = db.Column(db.JSON, default=dict)  # Specific widget positions
    breakpoint = db.Column(db.String(20), default='desktop')  # 'desktop', 'tablet', 'mobile'
    
    # Display settings
    zoom_level = db.Column(db.Float, default=1.0)
    grid_size = db.Column(db.Integer, default=12)  # CSS grid size
    
    # Relationships
    user = db.relationship('User', backref='user_dashboard_layouts')


class WidgetDataCache(BaseModel):
    """Cache for widget data to improve performance"""
    __tablename__ = 'widget_data_cache'
    
    widget_id = db.Column(db.Integer, db.ForeignKey('analytics_widgets.id'), nullable=False)
    cache_key = db.Column(db.String(255), nullable=False)  # Unique key for cached data
    data = db.Column(db.JSON, nullable=False)  # Cached data
    expires_at = db.Column(DateTime, nullable=False)  # When this cache entry expires
    
    # Metadata
    data_size = db.Column(db.Integer)  # Size of cached data in bytes
    query_hash = db.Column(db.String(64))  # Hash of the query parameters


class Notification(BaseModel):
    """Notification model"""
    __tablename__ = 'notifications'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), default='info')
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    action_url = db.Column(db.String(500))
    priority = db.Column(db.String(20), default='medium')
    
    # Relationships
    user = db.relationship('User', back_populates='notifications')


# =============================================================================
# EVENT TRACKING & AUDIT CLASSES
# =============================================================================

class AnalyticsEvent(BaseModel):
    """Analytics events tracking"""
    __tablename__ = 'analytics_events'
    
    # Event identification 
    event_type = db.Column(db.String(100), nullable=False)  # 'widget_view', 'dashboard_view', 'filter_applied', etc.
    event_name = db.Column(db.String(200), nullable=False)  # Human-readable event name
    
    # Context
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    dashboard_id = db.Column(db.Integer, db.ForeignKey('analytics_dashboards.id'))
    widget_id = db.Column(db.Integer, db.ForeignKey('analytics_widgets.id'))
    
    # Event data
    event_data = db.Column(db.JSON, default=dict)  # Additional event data
    meta_data = db.Column(db.JSON, default=dict)  # Technical metadata
    
    # Client information
    user_agent = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    session_id = db.Column(db.String(100))
    
    # Timestamps
    event_timestamp = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='user_analytics_events')
    organization = db.relationship('Organization', backref='organization_analytics_events')


class AuditTrail(BaseModel):
    """
    Comprehensive audit trail model for tracking all significant actions in the system.
    Used for security, compliance, and debugging purposes.
    """
    __tablename__ = 'audit_trails'
    
    # Core audit information
    action = db.Column(db.String(100), nullable=False, index=True)  # CREATE, UPDATE, DELETE, LOGIN, etc.
    resource_type = db.Column(db.String(100), nullable=False, index=True)  # User, Organization, Patient, etc.
    resource_id = db.Column(db.String(100), nullable=False, index=True)  # ID of the affected resource
    resource_name = db.Column(db.String(200))  # Human-readable name of the resource
    
    # User and context information
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    user_email = db.Column(db.String(120), index=True)  # Denormalized for performance
    user_role = db.Column(db.String(50), index=True)  # Denormalized user role
    
    # Organization context
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), index=True)
    organization_name = db.Column(db.String(200))  # Denormalized organization name
    
    # Change details
    old_values = db.Column(db.JSON)  # Previous state (for UPDATE actions)
    new_values = db.Column(db.JSON)  # New state (for CREATE/UPDATE actions)
    changed_fields = db.Column(db.JSON)  # List of fields that were changed
    
    # Request and environment context
    ip_address = db.Column(db.String(45), index=True)
    user_agent = db.Column(db.Text)
    request_method = db.Column(db.String(10))  # GET, POST, PUT, DELETE, etc.
    request_path = db.Column(db.String(500))  # API endpoint or route
    request_params = db.Column(db.JSON)  # Query parameters or form data
    
    # Session and security context
    session_id = db.Column(db.String(100), index=True)
    client_id = db.Column(db.String(100))  # OAuth client ID or API key
    trace_id = db.Column(db.String(100))  # For distributed tracing
    
    # Status and metadata
    status = db.Column(db.String(20), default='success', index=True)  # success, failure, warning
    status_code = db.Column(db.Integer)  # HTTP status code
    error_message = db.Column(db.Text)  # Error details if action failed
    
    # Performance metrics
    duration_ms = db.Column(db.Integer)  # How long the action took in milliseconds
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Additional metadata
    meta_data = db.Column(db.JSON, default=dict)  # Additional context-specific data
    tags = db.Column(db.JSON, default=list)  # Categorization tags
    
    # Relationships
    user = db.relationship('User', backref='user_audit_trails', foreign_keys=[user_id])
    organization = db.relationship('Organization', backref='organization_audit_trails', foreign_keys=[organization_id])
    
    def __repr__(self):
        return f'<AuditTrail {self.action} {self.resource_type} {self.resource_id} by {self.user_email}>'
    
    def to_dict(self, include_sensitive=False):
        """Convert audit trail to dictionary, with option to include sensitive data"""
        data = {
            'id': self.id,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'resource_name': self.resource_name,
            'user_id': self.user_id,
            'user_email': self.user_email,
            'user_role': self.user_role,
            'organization_id': self.organization_id,
            'organization_name': self.organization_name,
            'ip_address': self.ip_address if include_sensitive else None,
            'request_method': self.request_method,
            'request_path': self.request_path,
            'status': self.status,
            'status_code': self.status_code,
            'duration_ms': self.duration_ms,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'tags': self.tags,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_sensitive:
            data.update({
                'old_values': self.old_values,
                'new_values': self.new_values,
                'changed_fields': self.changed_fields,
                'user_agent': self.user_agent,
                'request_params': self.request_params,
                'session_id': self.session_id,
                'client_id': self.client_id,
                'trace_id': self.trace_id,
                'error_message': self.error_message,
                'metadata': self.metadata
            })
        
        return data


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_widget_types_by_category(category=None):
    """Get widget types, optionally filtered by category"""
    query = WidgetType.query.filter_by(is_active=True)
    if category:
        query = query.filter_by(category=category)
    return query.order_by(WidgetType.name).all()


def get_user_dashboards(user_id, organization_id):
    """Get dashboards accessible to a user"""
    
    user = User.query.get(user_id)
    if not user:
        return []
    
    # Get public dashboards and user's personal dashboards
    query = AnalyticsDashboard.query.filter(
        db.or_(
            AnalyticsDashboard.is_public == True,
            AnalyticsDashboard.user_id == user_id
        )
    )
    
    # Filter by organization
    query = query.filter_by(organization_id=organization_id)
    
    return query.order_by(AnalyticsDashboard.name).all()


def clear_widget_cache(widget_id=None):
    """Clear widget data cache"""
    if widget_id:
        # Clear cache for specific widget
        WidgetDataCache.query.filter_by(widget_id=widget_id).delete()
    else:
        # Clear all expired cache entries
        WidgetDataCache.query.filter(WidgetDataCache.expires_at < datetime.utcnow()).delete()
    
    db.session.commit()


def record_analytics_event(event_type, event_name, user_id=None, organization_id=None, 
                          dashboard_id=None, widget_id=None, event_data=None, metadata=None,
                          user_agent=None, ip_address=None, session_id=None):
    """Record an analytics event"""
    event = AnalyticsEvent(
        event_type=event_type,
        event_name=event_name,
        user_id=user_id,
        organization_id=organization_id,
        dashboard_id=dashboard_id,
        widget_id=widget_id,
        event_data=event_data or {},
        metadata=metadata or {},
        user_agent=user_agent,
        ip_address=ip_address,
        session_id=session_id
    )
    
    db.session.add(event)
    db.session.commit()
    
    return event


def record_audit(action, resource_type, resource_id, user_id=None, 
                organization_id=None, old_values=None, new_values=None,
                ip_address=None, user_agent=None, request_method=None,
                request_path=None, request_params=None, session_id=None,
                client_id=None, trace_id=None, status='success', 
                status_code=200, error_message=None, duration_ms=None,
                metadata=None, tags=None, db_session=None):
    """
    Record an audit trail entry with comprehensive context.
    """

    
    # Use provided session or default session
    session = db_session or db.session
    
    # Get user and organization details if IDs are provided
    user_email = user_role = None
    organization_name = None
    
    if user_id:
        user = session.query(User).get(user_id)
        if user:
            user_email = user.email
            # Get user role (you might need to adjust this based on your role system)
            user_role = getattr(user, 'role', None)
            if hasattr(user_role, 'name'):
                user_role = user_role.name
            elif hasattr(user_role, 'value'):
                user_role = user_role.value
    
    if organization_id:
        org = session.query(Organization).get(organization_id)
        if org:
            organization_name = org.name
    
    # Determine resource name if not provided in metadata
    resource_name = None
    if metadata and 'resource_name' in metadata:
        resource_name = metadata['resource_name']
    
    # Determine changed fields for UPDATE actions
    changed_fields = None
    if action == AuditAction.UPDATE and old_values and new_values:
        changed_fields = list(set(old_values.keys()) & set(new_values.keys()))
    
    # Create audit trail record
    audit = AuditTrail(
        action=action,
        resource_type=resource_type,
        resource_id=str(resource_id),  # Ensure string for consistency
        resource_name=resource_name,
        user_id=user_id,
        user_email=user_email,
        user_role=user_role,
        organization_id=organization_id,
        organization_name=organization_name,
        old_values=old_values,
        new_values=new_values,
        changed_fields=changed_fields,
        ip_address=ip_address,
        user_agent=user_agent,
        request_method=request_method,
        request_path=request_path,
        request_params=request_params,
        session_id=session_id,
        client_id=client_id,
        trace_id=trace_id,
        status=status,
        status_code=status_code,
        error_message=error_message,
        duration_ms=duration_ms,
        metadata=metadata or {},
        tags=tags or []
    )
    
    session.add(audit)
    
    # Commit if using default session (caller handles commit if providing session)
    if not db_session:
        session.commit()
    
    return audit


def get_audit_logs(filters=None, page=1, per_page=50, include_sensitive=False):
    """
    Retrieve audit logs with filtering and pagination.
    """
    query = AuditTrail.query
    
    if filters:
        # Apply filters
        if 'user_id' in filters:
            query = query.filter(AuditTrail.user_id == filters['user_id'])
        if 'organization_id' in filters:
            query = query.filter(AuditTrail.organization_id == filters['organization_id'])
        if 'action' in filters:
            query = query.filter(AuditTrail.action == filters['action'])
        if 'resource_type' in filters:
            query = query.filter(AuditTrail.resource_type == filters['resource_type'])
        if 'resource_id' in filters:
            query = query.filter(AuditTrail.resource_id == str(filters['resource_id']))
        if 'status' in filters:
            query = query.filter(AuditTrail.status == filters['status'])
        if 'date_from' in filters:
            query = query.filter(AuditTrail.timestamp >= filters['date_from'])
        if 'date_to' in filters:
            query = query.filter(AuditTrail.timestamp <= filters['date_to'])
        if 'ip_address' in filters:
            query = query.filter(AuditTrail.ip_address == filters['ip_address'])
    
    # Order by timestamp descending (newest first)
    query = query.order_by(AuditTrail.timestamp.desc())
    
    # Paginate
    pagination = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    # Convert to dictionaries
    audit_records = [audit.to_dict(include_sensitive=include_sensitive) 
                    for audit in pagination.items]
    
    return audit_records, pagination.total


def cleanup_old_audit_logs(days_to_keep=90):
    """
    Clean up audit logs older than specified days.
    """
    from datetime import datetime, timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
    
    # Delete old records
    deleted_count = AuditTrail.query.filter(
        AuditTrail.timestamp < cutoff_date
    ).delete()
    
    db.session.commit()
    
    return deleted_count