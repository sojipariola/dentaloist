from .base import BaseModel
from . import db
from sqlalchemy import (Column, Integer, String, Text, Boolean, DateTime, ForeignKey, 
            JSON, Float, Numeric, CheckConstraint, LargeBinary, func, and_, or_)
from datetime import datetime

# =============================================================================
# RATE LIMITING & SECURITY
# =============================================================================

class RateLimiter(BaseModel):
    """Rate limiter configuration for different endpoints and actions"""
    __tablename__ = 'rate_limiters'
    
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    endpoint = db.Column(db.String(255))  # API endpoint pattern
    method = db.Column(db.String(10))  # HTTP method (GET, POST, etc.)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) 

    # Rate limiting configuration
    max_requests = db.Column(db.Integer, default=100)  # Requests per period
    period_seconds = db.Column(db.Integer, default=3600)  # Time period in seconds
    burst_capacity = db.Column(db.Integer, default=10)  # Burst capacity
    
    # Scope and targeting
    scope_type = db.Column(db.String(50), default='user')  # user, ip, global, tenant
    applies_to_authenticated = db.Column(db.Boolean, default=True)
    applies_to_anonymous = db.Column(db.Boolean, default=True)
    
    # Response configuration
    response_message = db.Column(db.Text, default='Rate limit exceeded')
    response_code = db.Column(db.Integer, default=429)
    
    # Management
    is_active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.Integer, default=0)  # Processing priority
    
    # Relationships
    user = db.relationship('User', back_populates='rate_limiters') 
    rate_limits = db.relationship('RateLimit', back_populates='rate_limiter', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<RateLimiter {self.name}>'


class RateLimit(BaseModel):
    """Individual rate limit counters and state"""
    __tablename__ = 'rate_limits'
    
    rate_limiter_id = db.Column(db.Integer, db.ForeignKey('rate_limiters.id'), nullable=False)
    
    # Identification
    identifier = db.Column(db.String(255), nullable=False)  # user_id, ip_address, etc.
    scope_type = db.Column(db.String(50), nullable=False)  # user, ip, global, tenant
    
    # Counter state
    request_count = db.Column(db.Integer, default=0)
    window_start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_request = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Burst handling
    burst_count = db.Column(db.Integer, default=0)
    burst_window_start = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Statistics
    total_requests = db.Column(db.Integer, default=0)
    total_blocked = db.Column(db.Integer, default=0)
    
    # Metadata
    user_agent = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    
    # Relationships
    # FIX: Add proper foreign key and relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # ← ADD THIS
    
    # Relationships
    rate_limiter = db.relationship('RateLimiter', backref='rate_limits')  # ← Use backref instead of back_populates
    user = db.relationship('User', backref='user_rate_limits')  # ← ADD THIS
    
    # Index
    __table_args__ = (
        db.Index('idx_rate_limit_identifier', 'identifier', 'scope_type'),
        db.Index('idx_rate_limit_window', 'window_start'),
        db.Index('idx_rate_limit_limiter', 'rate_limiter_id'),
    )
    
    def __repr__(self):
        return f'<RateLimit {self.identifier}@{self.rate_limiter_id}>'


# =============================================================================
# EMAIL & NOTIFICATION
# =============================================================================

class EmailLog(BaseModel):
    """Email sending history and tracking"""
    __tablename__ = 'email_logs'
    
    # Recipient information
    to_email = db.Column(db.String(255), nullable=False, index=True)
    to_name = db.Column(db.String(255))
    from_email = db.Column(db.String(255), nullable=False)
    from_name = db.Column(db.String(255))
    
    # Email content
    subject = db.Column(db.String(255), nullable=False)
    body_html = db.Column(db.Text)
    body_text = db.Column(db.Text)
    template_id = db.Column(db.String(100))  # Email template identifier
    
    # Status tracking
    status = db.Column(db.String(50), default='sent', index=True)  # sent, delivered, bounced, failed
    status_message = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    delivered_at = db.Column(db.DateTime)
    opened_at = db.Column(db.DateTime)
    
    # Provider information
    provider = db.Column(db.String(50))  # sendgrid, ses, smtp, etc.
    provider_message_id = db.Column(db.String(255))
    provider_response = db.Column(db.JSON)
    
    # Context
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), index=True)
    email_type = db.Column(db.String(100), index=True)  # welcome, notification, reset_password, etc.
    
    # Tracking
    open_count = db.Column(db.Integer, default=0)
    click_count = db.Column(db.Integer, default=0)
    tracking_id = db.Column(db.String(100), unique=True)
    
    # Relationships
    user = db.relationship('User', backref='user_email_logs')
    organization = db.relationship('Organization', backref='organization_email_logs')
    
    def __repr__(self):
        return f'<EmailLog {self.to_email} - {self.subject}>'


# =============================================================================
# INTEGRATIONS & WEBHOOKS
# =============================================================================

class Integration(BaseModel):
    """External service integrations configuration"""
    __tablename__ = 'integrations'
    
    # Basic information
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    service_type = db.Column(db.String(50), nullable=False, index=True)  # payment, email, sms, calendar, etc.
    provider = db.Column(db.String(50), nullable=False, index=True)  # stripe, twilio, sendgrid, etc.
    
    # Configuration
    config = db.Column(db.JSON, default=dict)  # API keys, endpoints, settings
    webhook_config = db.Column(db.JSON, default=dict)  # Webhook endpoints and secrets
    
    # Status and health
    status = db.Column(db.String(20), default='active', index=True)  # active, inactive, error
    last_sync = db.Column(db.DateTime)
    last_error = db.Column(db.Text)
    error_count = db.Column(db.Integer, default=0)
    
    # Security
    is_secure = db.Column(db.Boolean, default=True)
    encryption_key = db.Column(db.String(255))  # For encrypting sensitive config data
    
    # Scope
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False, index=True)
    is_global = db.Column(db.Boolean, default=False)  # Available to all organizations
    
    # Features
    supports_webhooks = db.Column(db.Boolean, default=False)
    supports_sync = db.Column(db.Boolean, default=False)
    supports_async = db.Column(db.Boolean, default=True)
    
    # Versioning
    version = db.Column(db.String(20), default='1.0.0')
    api_version = db.Column(db.String(20))
    
    # Relationships
    organization = db.relationship('Organization', backref='integrations')
    integration_logs = db.relationship('IntegrationLog', back_populates='integration', cascade='all, delete-orphan')
    webhooks = db.relationship('Webhook', back_populates='integration', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Integration {self.name} ({self.provider})>'


class IntegrationLog(BaseModel):
    """Integration activity and error logging"""
    __tablename__ = 'integration_logs'
    
    integration_id = db.Column(db.Integer, db.ForeignKey('integrations.id'), nullable=False)
    
    # Log details
    action = db.Column(db.String(100), nullable=False, index=True)  # sync, webhook, api_call, etc.
    status = db.Column(db.String(20), default='success', index=True)  # success, error, warning
    message = db.Column(db.Text)
    details = db.Column(db.JSON)  # Request/response details
    
    # Request context
    request_url = db.Column(db.String(500))
    request_method = db.Column(db.String(10))
    request_headers = db.Column(db.JSON)
    request_body = db.Column(db.Text)
    
    # Response context
    response_code = db.Column(db.Integer)
    response_headers = db.Column(db.JSON)
    response_body = db.Column(db.Text)
    
    # Timing
    started_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    duration_ms = db.Column(db.Integer)  # Duration in milliseconds
    
    # Error handling
    error_type = db.Column(db.String(100))
    error_message = db.Column(db.Text)
    stack_trace = db.Column(db.Text)
    
    # Context
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    resource_type = db.Column(db.String(100))  # patient, appointment, etc.
    resource_id = db.Column(db.String(100))
    
    # Relationships
    integration = db.relationship('Integration', back_populates='integration_logs')
    user = db.relationship('User', backref='integration_logs')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_integration_log_action', 'integration_id', 'action'),
        db.Index('idx_integration_log_status', 'integration_id', 'status'),
        db.Index('idx_integration_log_time', 'started_at'),
    )
    
    def __repr__(self):
        return f'<IntegrationLog {self.integration.name} - {self.action}>'


class Webhook(BaseModel):
    """Webhook endpoints configuration"""
    __tablename__ = 'webhooks'
    
    integration_id = db.Column(db.Integer, db.ForeignKey('integrations.id'))
    
    # Basic configuration
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    target_url = db.Column(db.String(500), nullable=False)
    http_method = db.Column(db.String(10), default='POST')
    
    # Security
    secret = db.Column(db.String(255))  # For signature verification
    headers = db.Column(db.JSON, default=dict)  # Custom headers
    
    # Event subscription
    events = db.Column(db.JSON, default=list)  # List of events to subscribe to
    is_active = db.Column(db.Boolean, default=True, index=True)
    
    # Retry configuration
    max_retries = db.Column(db.Integer, default=3)
    retry_delay = db.Column(db.Integer, default=60)  # seconds
    timeout_seconds = db.Column(db.Integer, default=30)
    
    # Scope
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False, index=True)
    
    # Statistics
    total_attempts = db.Column(db.Integer, default=0)
    success_count = db.Column(db.Integer, default=0)
    failure_count = db.Column(db.Integer, default=0)
    last_attempt = db.Column(db.DateTime)
    
    # Relationships
    integration = db.relationship('Integration', back_populates='webhooks')
    organization = db.relationship('Organization', backref='webhooks')
    webhook_events = db.relationship('WebhookEvent', back_populates='webhook', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Webhook {self.name} -> {self.target_url}>'


class WebhookEvent(BaseModel):
    """Webhook event delivery attempts and history"""
    __tablename__ = 'webhook_events'
    
    webhook_id = db.Column(db.Integer, db.ForeignKey('webhooks.id'), nullable=False)
    
    # Event details
    event_type = db.Column(db.String(100), nullable=False, index=True)
    event_id = db.Column(db.String(100), nullable=False)  # Original event identifier
    payload = db.Column(db.JSON, nullable=False)
    
    # Delivery status
    status = db.Column(db.String(20), default='pending', index=True)  # pending, delivered, failed, retrying
    attempt_count = db.Column(db.Integer, default=0)
    last_attempt = db.Column(db.DateTime)
    next_retry = db.Column(db.DateTime)
    
    # Response details
    response_code = db.Column(db.Integer)
    response_body = db.Column(db.Text)
    response_headers = db.Column(db.JSON)
    
    # Error handling
    error_message = db.Column(db.Text)
    stack_trace = db.Column(db.Text)
    
    # Context
    triggered_by = db.Column(db.String(100))  # user, system, integration
    resource_type = db.Column(db.String(100))
    resource_id = db.Column(db.String(100))
    
    # Relationships
    webhook = db.relationship('Webhook', back_populates='webhook_events')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_webhook_event_status', 'webhook_id', 'status'),
        db.Index('idx_webhook_event_type', 'event_type'),
        db.Index('idx_webhook_event_time', 'created_at'),
    )
    
    def __repr__(self):
        return f'<WebhookEvent {self.event_type} -> {self.webhook.name}>'


# =============================================================================
# FILE MANAGEMENT
# =============================================================================

class FileRecord(BaseModel):
    """File upload and storage tracking"""
    __tablename__ = 'file_records'
    
    # File identification
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255))
    file_path = db.Column(db.String(500))  # Storage path
    file_url = db.Column(db.String(500))  # Public URL if available
    
    # File metadata
    mime_type = db.Column(db.String(100))
    file_size = db.Column(db.Integer)  # Size in bytes
    file_hash = db.Column(db.String(64))  # SHA-256 hash for deduplication
    
    # Storage information
    storage_provider = db.Column(db.String(50), default='local')  # local, s3, gcs, etc.
    bucket_name = db.Column(db.String(255))
    storage_key = db.Column(db.String(500))
    
    # Security and access
    is_public = db.Column(db.Boolean, default=False)
    access_key = db.Column(db.String(100))  # For signed URLs
    expires_at = db.Column(db.DateTime)  # For temporary files
    
    # Categorization
    file_type = db.Column(db.String(50), index=True)  # document, image, video, etc.
    category = db.Column(db.String(100), index=True)  # patient_documents, reports, etc.
    tags = db.Column(db.JSON, default=list)
    
    # Context
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False, index=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), index=True)
    
    # Usage tracking
    download_count = db.Column(db.Integer, default=0)
    last_download = db.Column(db.DateTime)
    
    # Versioning
    version = db.Column(db.Integer, default=1)
    parent_file_id = db.Column(db.Integer, db.ForeignKey('file_records.id'))  # For file versions
    
    # Relationships
    user = db.relationship('User', backref='user_file_records')
    organization = db.relationship('Organization', backref='organization_file_records')
    patient = db.relationship('Patient', backref='patient_file_records')

    parent_file = db.relationship('FileRecord', remote_side='FileRecord.id', backref='versions')
    
    def __repr__(self):
        return f'<FileRecord {self.filename} ({self.file_type})>'


# =============================================================================
# ANALYTICS & REPORTING
# =============================================================================

class AnalyticsReport(BaseModel):
    """Analytics reports configuration and templates"""
    __tablename__ = 'analytics_reports'
    
    # Basic information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    report_type = db.Column(db.String(50), nullable=False, index=True)  # standard, custom, system
    
    # Configuration
    query_sql = db.Column(db.Text)  # SQL query for the report
    query_parameters = db.Column(db.JSON, default=dict)  # Parameter definitions
    visualization_config = db.Column(db.JSON, default=dict)  # Charts, tables, etc.
    
    # Categorization
    category = db.Column(db.String(100), index=True)
    tags = db.Column(db.JSON, default=list)
    
    # Access control
    is_public = db.Column(db.Boolean, default=False)
    allowed_roles = db.Column(db.JSON, default=list)
    allowed_users = db.Column(db.JSON, default=list)
    
    # Scope
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Performance
    estimated_runtime = db.Column(db.Integer)  # Estimated runtime in seconds
    cache_duration = db.Column(db.Integer, default=300)  # Cache results for X seconds
    last_run_duration = db.Column(db.Integer)  # Actual last run duration in seconds
    
    # Status
    is_active = db.Column(db.Boolean, default=True, index=True)
    validation_errors = db.Column(db.JSON)  # Query validation errors
    
    # Relationships
    organization = db.relationship('Organization', backref='analytics_reports')
    creator = db.relationship('User', backref='created_reports', foreign_keys=[created_by])
    report_runs = db.relationship('ReportRun', back_populates='report', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<AnalyticsReport {self.name}>'


class KPI(BaseModel):
    """Key Performance Indicators definition and configuration"""
    __tablename__ = 'kpis'
    
    # Basic information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    code = db.Column(db.String(100), nullable=False, unique=True, index=True)
    
    # Calculation
    calculation_sql = db.Column(db.Text)  # SQL for KPI calculation
    calculation_type = db.Column(db.String(50), default='absolute')  # absolute, percentage, ratio
    unit = db.Column(db.String(50))  # patients, dollars, percentage, etc.
    
    # Targets and thresholds
    target_value = db.Column(db.Numeric(15, 4))
    warning_threshold = db.Column(db.Numeric(15, 4))
    critical_threshold = db.Column(db.Numeric(15, 4))
    is_higher_better = db.Column(db.Boolean, default=True)
    
    # Categorization
    category = db.Column(db.String(100), index=True)
    department = db.Column(db.String(100), index=True)
    tags = db.Column(db.JSON, default=list)
    
    # Refresh configuration
    refresh_interval = db.Column(db.String(20), default='daily')  # hourly, daily, weekly, monthly
    last_calculated = db.Column(db.DateTime)
    next_calculation = db.Column(db.DateTime)
    
    # Scope
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), index=True)
    is_global = db.Column(db.Boolean, default=False)  # Available to all organizations
    
    # Status
    is_active = db.Column(db.Boolean, default=True, index=True)
    
    # Relationships
    organization = db.relationship('Organization', backref='kpis')
    kpi_history = db.relationship('KPIHistory', back_populates='kpi', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<KPI {self.name} ({self.code})>'


class KPIHistory(BaseModel):
    """Historical KPI values over time"""
    __tablename__ = 'kpi_history'
    
    kpi_id = db.Column(db.Integer, db.ForeignKey('kpis.id'), nullable=False)
    
    # Value and period
    value = db.Column(db.Numeric(15, 4), nullable=False)
    period_start = db.Column(db.DateTime, nullable=False, index=True)
    period_end = db.Column(db.DateTime, nullable=False)
    period_type = db.Column(db.String(20), default='day', index=True)  # hour, day, week, month, quarter, year
    
    # Context and metadata
    calculated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_points = db.Column(db.Integer)  # Number of data points used in calculation
    confidence_interval = db.Column(db.Numeric(5, 4))  # Statistical confidence
    
    # Breakdown (for drill-down)
    breakdown = db.Column(db.JSON)  # Department, provider, location breakdown
    
    # Relationships
    kpi = db.relationship('KPI', back_populates='kpi_history')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_kpi_history_period', 'kpi_id', 'period_start', 'period_end'),
        db.Index('idx_kpi_history_type', 'kpi_id', 'period_type'),
    )
    
    def __repr__(self):
        return f'<KPIHistory {self.kpi.code} = {self.value} @ {self.period_start}>'


class ReportSchedule(BaseModel):
    """Automated report scheduling configuration"""
    __tablename__ = 'report_schedules'
    
    # Basic information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Scheduling configuration
    schedule_type = db.Column(db.String(20), default='recurring', index=True)  # one_time, recurring
    cron_expression = db.Column(db.String(100))  # For recurring schedules
    run_at = db.Column(db.DateTime)  # For one-time schedules
    timezone = db.Column(db.String(50), default='UTC')
    
    # Report configuration
    report_id = db.Column(db.Integer, db.ForeignKey('analytics_reports.id'))
    report_parameters = db.Column(db.JSON, default=dict)
    output_format = db.Column(db.String(20), default='pdf')  # pdf, excel, csv, html
    
    # Delivery configuration
    delivery_method = db.Column(db.String(50), default='email')  # email, webhook, storage
    delivery_config = db.Column(db.JSON, default=dict)  # Email addresses, webhook URLs, etc.
    
    # Scope
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Status and history
    is_active = db.Column(db.Boolean, default=True, index=True)
    last_run = db.Column(db.DateTime)
    next_run = db.Column(db.DateTime, index=True)
    total_runs = db.Column(db.Integer, default=0)
    success_count = db.Column(db.Integer, default=0)
    
    # Retention
    keep_results_days = db.Column(db.Integer, default=30)  # How long to keep report results
    
    # Relationships
    organization = db.relationship('Organization', backref='report_schedules')
    creator = db.relationship('User', backref='created_report_schedules', foreign_keys=[created_by])
    report = db.relationship('AnalyticsReport', backref='schedules')
    report_runs = db.relationship('ReportRun', back_populates='schedule', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ReportSchedule {self.name}>'


class ReportRun(BaseModel):
    """Individual report execution instances"""
    __tablename__ = 'report_runs'
    
    report_id = db.Column(db.Integer, db.ForeignKey('analytics_reports.id'))
    schedule_id = db.Column(db.Integer, db.ForeignKey('report_schedules.id'))
    
    # Execution context
    triggered_by = db.Column(db.String(50), default='user', index=True)  # user, schedule, api
    triggered_by_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Parameters and configuration
    parameters = db.Column(db.JSON, default=dict)
    output_format = db.Column(db.String(20), default='pdf')
    
    # Execution status
    status = db.Column(db.String(20), default='pending', index=True)  # pending, running, completed, failed
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    duration_seconds = db.Column(db.Integer)
    
    # Results
    result_file_id = db.Column(db.Integer, db.ForeignKey('file_records.id'))
    result_data = db.Column(db.JSON)  # Summary data for quick access
    row_count = db.Column(db.Integer)  # Number of rows in report
    
    # Error handling
    error_message = db.Column(db.Text)
    stack_trace = db.Column(db.Text)
    retry_count = db.Column(db.Integer, default=0)
    
    # Performance
    memory_used_mb = db.Column(db.Integer)
    query_duration_seconds = db.Column(db.Integer)
    
    # Relationships
    report = db.relationship('AnalyticsReport', back_populates='report_runs')
    schedule = db.relationship('ReportSchedule', back_populates='report_runs')
    triggered_user = db.relationship('User', backref='triggered_report_runs', foreign_keys=[triggered_by_user])
    result_file = db.relationship('FileRecord', backref='report_run', foreign_keys=[result_file_id])
    
    # Indexes
    __table_args__ = (
        db.Index('idx_report_run_status', 'report_id', 'status'),
        db.Index('idx_report_run_time', 'created_at'),
    )
    
    def __repr__(self):
        return f'<ReportRun {self.report.name} - {self.status}>'


class DataExport(BaseModel):
    """Data export requests and history"""
    __tablename__ = 'data_exports'
    
    # Export configuration
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    export_type = db.Column(db.String(50), nullable=False, index=True)  # patients, appointments, financial, etc.
    
    # Data selection
    filters = db.Column(db.JSON, default=dict)
    date_range_start = db.Column(db.DateTime)
    date_range_end = db.Column(db.DateTime)
    selected_fields = db.Column(db.JSON, default=list)
    
    # Format and delivery
    format = db.Column(db.String(20), default='csv', index=True)  # csv, excel, json, xml
    compression = db.Column(db.String(20), default='none')  # none, zip, gzip
    delivery_method = db.Column(db.String(50), default='download')  # download, email, webhook
    
    # Execution status
    status = db.Column(db.String(20), default='pending', index=True)  # pending, processing, completed, failed
    progress = db.Column(db.Integer, default=0)  # 0-100 percentage
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Results
    result_file_id = db.Column(db.Integer, db.ForeignKey('file_records.id'))
    file_size = db.Column(db.Integer)  # Size in bytes
    record_count = db.Column(db.Integer)  # Number of records exported
    
    # Error handling
    error_message = db.Column(db.Text)
    stack_trace = db.Column(db.Text)
    
    # Security and access
    is_sensitive = db.Column(db.Boolean, default=False)
    access_token = db.Column(db.String(100))  # For secure download links
    expires_at = db.Column(db.DateTime)  # When download link expires
    
    # Context
    requested_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False, index=True)
    
    # Relationships
    requested_user = db.relationship('User', backref='user_data_exports', foreign_keys=[requested_by])
    organization = db.relationship('Organization', backref='organization_data_exports')
    result_file = db.relationship('FileRecord', backref='data_export', foreign_keys=[result_file_id])
    
    # Indexes
    __table_args__ = (
        db.Index('idx_data_export_status', 'organization_id', 'status'),
        db.Index('idx_data_export_type', 'export_type', 'created_at'),
    )
    
    def __repr__(self):
        return f'<DataExport {self.name} - {self.status}>'


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def cleanup_old_data():
    """Clean up old system data based on retention policies"""
    from datetime import datetime, timedelta
    
    # Clean up old rate limits (keep 30 days)
    rate_limit_cutoff = datetime.utcnow() - timedelta(days=30)
    deleted_rate_limits = RateLimit.query.filter(
        RateLimit.window_start < rate_limit_cutoff
    ).delete()
    
    # Clean up old integration logs (keep 90 days)
    integration_log_cutoff = datetime.utcnow() - timedelta(days=90)
    deleted_integration_logs = IntegrationLog.query.filter(
        IntegrationLog.created_at < integration_log_cutoff
    ).delete()
    
    # Clean up old webhook events (keep 30 days)
    webhook_event_cutoff = datetime.utcnow() - timedelta(days=30)
    deleted_webhook_events = WebhookEvent.query.filter(
        WebhookEvent.created_at < webhook_event_cutoff
    ).delete()
    
    # Clean up old email logs (keep 180 days)
    email_log_cutoff = datetime.utcnow() - timedelta(days=180)
    deleted_email_logs = EmailLog.query.filter(
        EmailLog.sent_at < email_log_cutoff
    ).delete()
    
    db.session.commit()
    
    return {
        'rate_limits': deleted_rate_limits,
        'integration_logs': deleted_integration_logs,
        'webhook_events': deleted_webhook_events,
        'email_logs': deleted_email_logs
    }
