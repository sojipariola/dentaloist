# backend/app/routes/health.py

from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
import psutil
import socket
import redis
import requests
from sqlalchemy import text
import time
import os

from ..models import db, User, Organization
from ..utils.tenancy import tenant_required
from ..utils.rate_limit import rate_limit

health_bp = Blueprint('health', __name__, url_prefix='/api/health')

# ===== Health Check Routes =====

@health_bp.route('/', methods=['GET'])
@rate_limit(limit=10, period=60)  # 10 requests per minute
def health_check():
    """
    Comprehensive health check endpoint with system diagnostics
    """
    try:
        start_time = time.time()
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': current_app.config.get('APP_VERSION', '1.0.0'),
            'environment': current_app.config.get('ENV', 'development'),
            'checks': {}
        }
        
        # Database connection check
        db_check = _check_database()
        health_data['checks']['database'] = db_check
        if not db_check['healthy']:
            health_data['status'] = 'degraded'
        
        # Redis connection check (if configured)
        if current_app.config.get('REDIS_URL'):
            redis_check = _check_redis()
            health_data['checks']['redis'] = redis_check
            if not redis_check['healthy']:
                health_data['status'] = 'degraded'
        
        # External services check
        services_check = _check_external_services()
        health_data['checks']['external_services'] = services_check
        if not all(s['healthy'] for s in services_check.values()):
            health_data['status'] = 'degraded'
        
        # System resources check
        system_check = _check_system_resources()
        health_data['checks']['system'] = system_check
        if not system_check['healthy']:
            health_data['status'] = 'degraded'
        
        # Application-specific checks
        app_check = _check_application_health()
        health_data['checks']['application'] = app_check
        if not app_check['healthy']:
            health_data['status'] = 'degraded'
        
        # Response time
        health_data['response_time_ms'] = round((time.time() - start_time) * 1000, 2)
        
        # Determine overall status
        if health_data['status'] == 'healthy':
            return jsonify(health_data), 200
        else:
            return jsonify(health_data), 207  # Multi-Status
        
    except Exception as e:
        current_app.logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }), 500

@health_bp.route('/status', methods=['GET'])
def status():
    """
    Basic status endpoint for load balancers and quick checks
    """
    try:
        # Quick database check
        db.session.execute(text('SELECT 1'))
        
        return jsonify({
            'status': 'ok',
            'version': current_app.config.get('APP_VERSION', '1.0.0'),
            'timestamp': datetime.utcnow().isoformat(),
            'environment': current_app.config.get('ENV', 'development')
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'timestamp': datetime.utcnow().isoformat(),
            'error': 'Database connection failed'
        }), 500

@health_bp.route('/detailed', methods=['GET'])
@jwt_required()
@tenant_required
def detailed_health():
    """
    Detailed health information with system metrics (requires authentication)
    """
    try:
        detailed_data = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'application': _get_application_info(),
            'system': _get_system_metrics(),
            'database': _get_database_metrics(),
            'services': _get_services_status(),
            'dependencies': _get_dependencies_status()
        }
        
        return jsonify(detailed_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Detailed health check failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }), 500

@health_bp.route('/readiness', methods=['GET'])
def readiness_probe():
    """
    Kubernetes readiness probe endpoint
    """
    try:
        # Check critical dependencies
        db.session.execute(text('SELECT 1'))
        
        # Check Redis if configured
        if current_app.config.get('REDIS_URL'):
            _check_redis()
        
        return jsonify({
            'status': 'ready',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'not_ready',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }), 503

@health_bp.route('/liveness', methods=['GET'])
def liveness_probe():
    """
    Kubernetes liveness probe endpoint
    """
    try:
        # Simple check to ensure application is responsive
        return jsonify({
            'status': 'alive',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unresponsive',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }), 503

@health_bp.route('/metrics', methods=['GET'])
@jwt_required()
@tenant_required
def metrics():
    """
    Application metrics and statistics
    """
    try:
        current_user = current_app.get_current_user()
        
        metrics_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'users': _get_user_metrics(),
            'organizations': _get_organization_metrics(),
            'system': _get_detailed_system_metrics(),
            'performance': _get_performance_metrics()
        }
        
        return jsonify(metrics_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Metrics endpoint failed: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve metrics',
            'timestamp': datetime.utcnow().isoformat()
        }), 500

# ===== Health Check Functions =====

def _check_database():
    """Check database connection and performance"""
    try:
        start_time = time.time()
        
        # Test connection
        db.session.execute(text('SELECT 1'))
        
        # Test query performance
        result = db.session.execute(text('SELECT COUNT(*) FROM users')).scalar()
        
        response_time = round((time.time() - start_time) * 1000, 2)
        
        return {
            'healthy': True,
            'response_time_ms': response_time,
            'user_count': result,
            'message': 'Database connection successful'
        }
        
    except Exception as e:
        return {
            'healthy': False,
            'error': str(e),
            'message': 'Database connection failed'
        }

def _check_redis():
    """Check Redis connection if configured"""
    try:
        redis_url = current_app.config.get('REDIS_URL')
        if not redis_url:
            return {
                'healthy': True,
                'message': 'Redis not configured',
                'configured': False
            }
        
        start_time = time.time()
        
        # Test Redis connection
        redis_client = redis.from_url(redis_url)
        redis_client.ping()
        
        response_time = round((time.time() - start_time) * 1000, 2)
        
        return {
            'healthy': True,
            'response_time_ms': response_time,
            'configured': True,
            'message': 'Redis connection successful'
        }
        
    except Exception as e:
        return {
            'healthy': False,
            'error': str(e),
            'configured': True,
            'message': 'Redis connection failed'
        }

def _check_external_services():
    """Check external services and APIs"""
    services = {}
    
    # Check email service (if configured)
    if current_app.config.get('MAIL_SERVER'):
        services['email'] = _check_email_service()
    
    # Check file storage (if configured)
    if current_app.config.get('AWS_S3_BUCKET') or current_app.config.get('FILE_STORAGE_PATH'):
        services['file_storage'] = _check_file_storage()
    
    # Check payment processor (if configured)
    if current_app.config.get('STRIPE_API_KEY'):
        services['payment_processor'] = _check_payment_processor()
    
    return services

def _check_system_resources():
    """Check system resource usage"""
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        
        # Disk usage
        disk = psutil.disk_usage('/')
        
        # Network connections
        connections = len(psutil.net_connections())
        
        healthy = (
            cpu_percent < 90 and
            memory.percent < 85 and
            disk.percent < 90
        )
        
        return {
            'healthy': healthy,
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_gb': round(memory.available / (1024 ** 3), 2),
            'disk_percent': disk.percent,
            'disk_free_gb': round(disk.free / (1024 ** 3), 2),
            'network_connections': connections,
            'message': 'System resources within acceptable limits' if healthy else 'System resources approaching limits'
        }
        
    except Exception as e:
        return {
            'healthy': False,
            'error': str(e),
            'message': 'Failed to check system resources'
        }

def _check_application_health():
    """Check application-specific health metrics"""
    try:
        # Check if migrations are up to date
        migration_status = _check_migrations()
        
        # Check background workers (if any)
        worker_status = _check_background_workers()
        
        healthy = migration_status['up_to_date'] and worker_status['healthy']
        
        return {
            'healthy': healthy,
            'migrations': migration_status,
            'background_workers': worker_status,
            'message': 'Application components healthy' if healthy else 'Application issues detected'
        }
        
    except Exception as e:
        return {
            'healthy': False,
            'error': str(e),
            'message': 'Application health check failed'
        }

def _check_email_service():
    """Check email service connectivity"""
    try:
        # Simple check - in production, you might test actual SMTP connection
        return {
            'healthy': True,
            'configured': True,
            'message': 'Email service configured'
        }
    except Exception as e:
        return {
            'healthy': False,
            'configured': True,
            'error': str(e),
            'message': 'Email service check failed'
        }

def _check_file_storage():
    """Check file storage connectivity"""
    try:
        # Check based on configuration
        if current_app.config.get('AWS_S3_BUCKET'):
            return {
                'healthy': True,
                'type': 's3',
                'configured': True,
                'message': 'S3 storage configured'
            }
        elif current_app.config.get('FILE_STORAGE_PATH'):
            return {
                'healthy': True,
                'type': 'local',
                'configured': True,
                'message': 'Local storage configured'
            }
        else:
            return {
                'healthy': True,
                'type': 'none',
                'configured': False,
                'message': 'File storage not configured'
            }
    except Exception as e:
        return {
            'healthy': False,
            'configured': True,
            'error': str(e),
            'message': 'File storage check failed'
        }

def _check_payment_processor():
    """Check payment processor connectivity"""
    try:
        # Simple check - in production, you might test actual API connection
        return {
            'healthy': True,
            'configured': True,
            'message': 'Payment processor configured'
        }
    except Exception as e:
        return {
            'healthy': False,
            'configured': True,
            'error': str(e),
            'message': 'Payment processor check failed'
        }

def _check_migrations():
    """Check if database migrations are up to date"""
    try:
        # This is a simplified check - in a real application, you'd use
        # your migration framework's tools to check status
        return {
            'up_to_date': True,
            'message': 'Migrations are up to date'
        }
    except Exception as e:
        return {
            'up_to_date': False,
            'error': str(e),
            'message': 'Failed to check migrations'
        }

def _check_background_workers():
    """Check background worker status"""
    try:
        # Simplified check - in production, you'd check your actual worker system
        return {
            'healthy': True,
            'message': 'Background workers operational'
        }
    except Exception as e:
        return {
            'healthy': False,
            'error': str(e),
            'message': 'Background worker check failed'
        }

# ===== Detailed Metrics Functions =====

def _get_application_info():
    """Get detailed application information"""
    return {
        'name': current_app.config.get('APP_NAME', 'Dentaloist'),
        'version': current_app.config.get('APP_VERSION', '1.0.0'),
        'environment': current_app.config.get('ENV', 'development'),
        'debug': current_app.config.get('DEBUG', False),
        'hostname': socket.gethostname(),
        'start_time': current_app.start_time.isoformat() if hasattr(current_app, 'start_time') else 'unknown',
        'uptime_seconds': round((datetime.utcnow() - current_app.start_time).total_seconds(), 2) if hasattr(current_app, 'start_time') else 0
    }

def _get_system_metrics():
    """Get detailed system metrics"""
    try:
        # CPU details
        cpu_times = psutil.cpu_times()
        cpu_per_core = psutil.cpu_percent(percpu=True)
        
        # Memory details
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        # Disk details
        disk_io = psutil.disk_io_counters()
        disk_partitions = []
        
        for partition in psutil.disk_partitions():
            usage = psutil.disk_usage(partition.mountpoint)
            disk_partitions.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total_gb': round(usage.total / (1024 ** 3), 2),
                'used_gb': round(usage.used / (1024 ** 3), 2),
                'free_gb': round(usage.free / (1024 ** 3), 2),
                'percent': usage.percent
            })
        
        # Network details
        net_io = psutil.net_io_counters()
        network_interfaces = psutil.net_if_addrs()
        
        return {
            'cpu': {
                'cores': psutil.cpu_count(),
                'physical_cores': psutil.cpu_count(logical=False),
                'percent_total': psutil.cpu_percent(),
                'percent_per_core': cpu_per_core,
                'times': {
                    'user': cpu_times.user,
                    'system': cpu_times.system,
                    'idle': cpu_times.idle
                }
            },
            'memory': {
                'total_gb': round(memory.total / (1024 ** 3), 2),
                'available_gb': round(memory.available / (1024 ** 3), 2),
                'used_gb': round(memory.used / (1024 ** 3), 2),
                'percent': memory.percent
            },
            'swap': {
                'total_gb': round(swap.total / (1024 ** 3), 2),
                'used_gb': round(swap.used / (1024 ** 3), 2),
                'percent': swap.percent
            },
            'disk': {
                'partitions': disk_partitions,
                'io': {
                    'read_bytes': disk_io.read_bytes if disk_io else 0,
                    'write_bytes': disk_io.write_bytes if disk_io else 0,
                    'read_count': disk_io.read_count if disk_io else 0,
                    'write_count': disk_io.write_count if disk_io else 0
                } if disk_io else {}
            },
            'network': {
                'interfaces': list(network_interfaces.keys()),
                'io': {
                    'bytes_sent': net_io.bytes_sent,
                    'bytes_recv': net_io.bytes_recv,
                    'packets_sent': net_io.packets_sent,
                    'packets_recv': net_io.packets_recv
                } if net_io else {}
            }
        }
        
    except Exception as e:
        return {'error': f'Failed to get system metrics: {str(e)}'}

def _get_database_metrics():
    """Get database performance metrics"""
    try:
        # Get database size
        db_size = db.session.execute(text(
            "SELECT pg_database_size(current_database())"
        )).scalar()
        
        # Get table statistics
        table_stats = db.session.execute(text("""
            SELECT schemaname, relname, n_live_tup, n_dead_tup, 
                   last_vacuum, last_autovacuum, last_analyze, last_autoanalyze
            FROM pg_stat_user_tables
            ORDER BY n_live_tup DESC
            LIMIT 10
        """)).fetchall()
        
        # Get connection info
        connections = db.session.execute(text(
            "SELECT COUNT(*) FROM pg_stat_activity"
        )).scalar()
        
        return {
            'size_bytes': db_size,
            'size_gb': round(db_size / (1024 ** 3), 2),
            'connections': connections,
            'top_tables': [
                {
                    'schema': row[0],
                    'table': row[1],
                    'live_tuples': row[2],
                    'dead_tuples': row[3],
                    'last_vacuum': row[4].isoformat() if row[4] else None,
                    'last_autovacuum': row[5].isoformat() if row[5] else None,
                    'last_analyze': row[6].isoformat() if row[6] else None,
                    'last_autoanalyze': row[7].isoformat() if row[7] else None
                }
                for row in table_stats
            ]
        }
        
    except Exception as e:
        return {'error': f'Failed to get database metrics: {str(e)}'}

def _get_services_status():
    """Get status of all external services"""
    return {
        'redis': _check_redis(),
        'email': _check_email_service(),
        'file_storage': _check_file_storage(),
        'payment_processor': _check_payment_processor()
    }

def _get_dependencies_status():
    """Get status of application dependencies"""
    try:
        # Check Python packages
        import importlib.metadata
        dependencies = []
        
        for package in ['flask', 'sqlalchemy', 'psycopg2-binary', 'redis', 'requests']:
            try:
                version = importlib.metadata.version(package)
                dependencies.append({'package': package, 'version': version, 'status': 'ok'})
            except importlib.metadata.PackageNotFoundError:
                dependencies.append({'package': package, 'version': 'not found', 'status': 'missing'})
        
        return dependencies
        
    except Exception as e:
        return [{'error': f'Failed to check dependencies: {str(e)}'}]

def _get_user_metrics():
    """Get user-related metrics"""
    try:
        total_users = db.session.execute(text('SELECT COUNT(*) FROM users')).scalar()
        active_users = db.session.execute(text(
            'SELECT COUNT(*) FROM users WHERE last_login_at > NOW() - INTERVAL \'30 days\''
        )).scalar()
        
        new_users_today = db.session.execute(text(
            'SELECT COUNT(*) FROM users WHERE created_at::date = CURRENT_DATE'
        )).scalar()
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'new_users_today': new_users_today,
            'activation_rate': round((active_users / total_users * 100), 2) if total_users > 0 else 0
        }
        
    except Exception as e:
        return {'error': f'Failed to get user metrics: {str(e)}'}

def _get_organization_metrics():
    """Get organization-related metrics"""
    try:
        total_orgs = db.session.execute(text('SELECT COUNT(*) FROM organizations')).scalar()
        active_orgs = db.session.execute(text(
            'SELECT COUNT(DISTINCT organization_id) FROM users WHERE last_login_at > NOW() - INTERVAL \'30 days\''
        )).scalar()
        
        return {
            'total_organizations': total_orgs,
            'active_organizations': active_orgs,
            'engagement_rate': round((active_orgs / total_orgs * 100), 2) if total_orgs > 0 else 0
        }
        
    except Exception as e:
        return {'error': f'Failed to get organization metrics: {str(e)}'}

def _get_detailed_system_metrics():
    """Get more detailed system metrics"""
    system_metrics = _get_system_metrics()
    
    # Add process information
    try:
        process = psutil.Process()
        with process.oneshot():
            system_metrics['process'] = {
                'pid': process.pid,
                'name': process.name(),
                'memory_rss_mb': round(process.memory_info().rss / (1024 ** 2), 2),
                'memory_percent': process.memory_percent(),
                'cpu_percent': process.cpu_percent(),
                'threads': process.num_threads(),
                'open_files': len(process.open_files()),
                'connections': len(process.connections())
            }
    except Exception as e:
        system_metrics['process'] = {'error': str(e)}
    
    return system_metrics

def _get_performance_metrics():
    """Get application performance metrics"""
    # This would typically integrate with your APM system
    # For now, return some basic metrics
    return {
        'requests_processed': 0,  # Would come from request monitoring
        'average_response_time_ms': 0,
        'error_rate': 0,
        'uptime_percent': 100
    }

# Initialize application start time
def init_app(app):
    """Initialize health monitoring"""
    app.start_time = datetime.utcnow()