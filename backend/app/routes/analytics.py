# routes/analytics.py

from flask import Blueprint, request, jsonify
from flask_login import current_user
from ..models import db
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Import auth and tenancy utilities
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

# RBAC Permission Constants
PERMISSION_VIEW_ANALYTICS = 'view_analytics'
PERMISSION_VIEW_REVENUE = 'view_revenue'
PERMISSION_VIEW_PATIENT_ANALYTICS = 'view_patient_analytics'

@analytics_bp.route('/dashboard', methods=['GET'])
@rate_limit(limit=100, period=3600)  # 100 requests per hour
@tenant_required
@permission_required(PERMISSION_VIEW_ANALYTICS)
def get_dashboard_analytics():
    """
    Get comprehensive dashboard analytics with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id if hasattr(current_user_obj, 'tenant_id') else None
        
        # Get date range (default to last 30 days)
        days = int(request.args.get('days', 30))
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Apply tenant filtering to all queries
        analytics_data = {
            'total_patients': _get_total_patients(tenant_id, start_date, end_date),
            'total_appointments': _get_total_appointments(tenant_id, start_date, end_date),
            'total_revenue': _get_total_revenue(tenant_id, start_date, end_date),
            'appointment_stats': _get_appointment_stats(tenant_id, start_date, end_date),
            'revenue_trend': _get_revenue_trend(tenant_id, start_date, end_date),
            'patient_growth': _get_patient_growth(tenant_id, start_date, end_date),
            'tenant_id': tenant_id,  # Include tenant info for debugging
            'time_period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            }
        }
        
        return jsonify(analytics_data), 200
        
    except ValueError as e:
        return jsonify({'error': 'Invalid parameter value', 'details': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@analytics_bp.route('/revenue', methods=['GET'])
@rate_limit(limit=50, period=3600)  # 50 requests per hour
@tenant_required
@permission_required(PERMISSION_VIEW_REVENUE)
def get_revenue_analytics():
    """
    Get detailed revenue analytics with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        days = int(request.args.get('days', 30))
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Granular revenue analytics with tenant filtering
        revenue_data = {
            'total': _get_total_revenue(tenant_id, start_date, end_date),
            'by_service': _get_revenue_by_service(tenant_id, start_date, end_date),
            'by_provider': _get_revenue_by_provider(tenant_id, start_date, end_date),
            'by_location': _get_revenue_by_location(tenant_id, start_date, end_date),
            'trend': _get_daily_revenue_trend(tenant_id, start_date, end_date),
            'comparison': _get_revenue_comparison(tenant_id, start_date, end_date),
            'metrics': {
                'average_transaction': _get_avg_transaction_value(tenant_id, start_date, end_date),
                'conversion_rate': _get_conversion_rate(tenant_id, start_date, end_date)
            }
        }
        
        return jsonify(revenue_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/patients', methods=['GET'])
@rate_limit(limit=80, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_PATIENT_ANALYTICS)
def get_patient_analytics():
    """
    Get patient analytics with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        days = int(request.args.get('days', 90))
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        patient_data = {
            'demographics': _get_patient_demographics(tenant_id),
            'acquisition': _get_patient_acquisition(tenant_id, start_date, end_date),
            'retention': _get_patient_retention(tenant_id, start_date, end_date),
            'geographic_distribution': _get_patient_geography(tenant_id)
        }
        
        return jsonify(patient_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/appointments', methods=['GET'])
@rate_limit(limit=60, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_ANALYTICS)
def get_appointment_analytics():
    """
    Get appointment analytics with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        days = int(request.args.get('days', 30))
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        appointment_data = {
            'volume_trend': _get_appointment_volume_trend(tenant_id, start_date, end_date),
            'cancellation_analysis': _get_cancellation_analysis(tenant_id, start_date, end_date),
            'wait_time_analysis': _get_wait_time_analysis(tenant_id, start_date, end_date),
            'provider_performance': _get_provider_appointment_stats(tenant_id, start_date, end_date)
        }
        
        return jsonify(appointment_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Helper functions with tenancy support
def _get_total_patients(tenant_id: str, start_date: datetime, end_date: datetime) -> int:
    """Get total patients for tenant within date range"""
    from ..models import Patient
    query = multi_tenant_query(Patient.query, tenant_id)
    return query.filter(Patient.created_at.between(start_date, end_date)).count()

def _get_total_appointments(tenant_id: str, start_date: datetime, end_date: datetime) -> int:
    """Get total appointments for tenant within date range"""
    from ..models import Appointment
    query = multi_tenant_query(Appointment.query, tenant_id)
    return query.filter(Appointment.scheduled_time.between(start_date, end_date)).count()

def _get_total_revenue(tenant_id: str, start_date: datetime, end_date: datetime) -> float:
    """Get total revenue for tenant within date range"""
    from ..models import Payment
    query = multi_tenant_query(Payment.query, tenant_id)
    result = query.filter(
        Payment.payment_date.between(start_date, end_date),
        Payment.status == 'completed'
    ).with_entities(db.func.sum(Payment.amount)).scalar()
    return float(result) if result else 0.0

def _get_appointment_stats(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, int]:
    """Get appointment statistics by status"""
    from ..models import Appointment
    query = multi_tenant_query(Appointment.query, tenant_id)
    stats = query.filter(Appointment.scheduled_time.between(start_date, end_date))\
                .group_by(Appointment.status)\
                .with_entities(Appointment.status, db.func.count(Appointment.id))\
                .all()
    return {status: count for status, count in stats}

def _get_revenue_trend(tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
    """Get daily revenue trend"""
    from ..models import Payment
    query = multi_tenant_query(Payment.query, tenant_id)
    trend = query.filter(
        Payment.payment_date.between(start_date, end_date),
        Payment.status == 'completed'
    ).group_by(db.func.date(Payment.payment_date))\
     .with_entities(db.func.date(Payment.payment_date), db.func.sum(Payment.amount))\
     .order_by(db.func.date(Payment.payment_date))\
     .all()
    
    return [{'date': date.isoformat(), 'revenue': float(amount)} for date, amount in trend]

def _get_patient_growth(tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
    """Get daily patient growth"""
    from ..models import Patient
    query = multi_tenant_query(Patient.query, tenant_id)
    growth = query.filter(Patient.created_at.between(start_date, end_date))\
                 .group_by(db.func.date(Patient.created_at))\
                 .with_entities(db.func.date(Patient.created_at), db.func.count(Patient.id))\
                 .order_by(db.func.date(Patient.created_at))\
                 .all()
    
    return [{'date': date.isoformat(), 'new_patients': count} for date, count in growth]

def _get_revenue_by_service(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, float]:
    """Get revenue breakdown by service type"""
    from ..models import Payment, Service
    query = multi_tenant_query(Payment.query.join(Service), tenant_id)
    revenue_by_service = query.filter(
        Payment.payment_date.between(start_date, end_date),
        Payment.status == 'completed'
    ).group_by(Service.name)\
     .with_entities(Service.name, db.func.sum(Payment.amount))\
     .all()
    
    return {service: float(amount) for service, amount in revenue_by_service}

def _get_revenue_by_provider(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, float]:
    """Get revenue breakdown by provider"""
    from ..models import Payment, User
    query = multi_tenant_query(Payment.query.join(User, Payment.provider_id == User.id), tenant_id)
    revenue_by_provider = query.filter(
        Payment.payment_date.between(start_date, end_date),
        Payment.status == 'completed'
    ).group_by(User.first_name, User.last_name)\
     .with_entities(
         db.func.concat(User.first_name, ' ', User.last_name).label('provider_name'),
         db.func.sum(Payment.amount)
     ).all()
    
    return {provider: float(amount) for provider, amount in revenue_by_provider}


# routes/analytics.py (continued)

def _get_revenue_by_location(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, float]:
    """Get revenue breakdown by location"""
    from ..models import Payment, Location
    query = multi_tenant_query(Payment.query.join(Location), tenant_id)
    revenue_by_location = query.filter(
        Payment.payment_date.between(start_date, end_date),
        Payment.status == 'completed'
    ).group_by(Location.name)\
     .with_entities(Location.name, db.func.sum(Payment.amount))\
     .all()
    
    return {location: float(amount) for location, amount in revenue_by_location}

def _get_daily_revenue_trend(tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
    """Get detailed daily revenue trend with comparison to previous period"""
    from ..models import Payment
    query = multi_tenant_query(Payment.query, tenant_id)
    
    # Current period trend
    current_trend = query.filter(
        Payment.payment_date.between(start_date, end_date),
        Payment.status == 'completed'
    ).group_by(db.func.date(Payment.payment_date))\
     .with_entities(db.func.date(Payment.payment_date), db.func.sum(Payment.amount))\
     .order_by(db.func.date(Payment.payment_date))\
     .all()
    
    # Previous period for comparison (same duration before start_date)
    prev_start_date = start_date - (end_date - start_date)
    prev_end_date = start_date - timedelta(days=1)
    
    prev_trend = query.filter(
        Payment.payment_date.between(prev_start_date, prev_end_date),
        Payment.status == 'completed'
    ).group_by(db.func.date(Payment.payment_date))\
     .with_entities(db.func.date(Payment.payment_date), db.func.sum(Payment.amount))\
     .order_by(db.func.date(Payment.payment_date))\
     .all()
    
    # Create a dictionary for quick lookup of previous period data
    prev_trend_dict = {date.isoformat(): float(amount) for date, amount in prev_trend}
    
    trend_data = []
    for date, amount in current_trend:
        date_str = date.isoformat()
        prev_amount = prev_trend_dict.get(date_str, 0)
        trend_data.append({
            'date': date_str,
            'revenue': float(amount),
            'previous_period_revenue': prev_amount,
            'growth_percentage': ((float(amount) - prev_amount) / prev_amount * 100) if prev_amount > 0 else 0
        })
    
    return trend_data

def _get_revenue_comparison(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get revenue comparison with previous period"""
    from ..models import Payment
    query = multi_tenant_query(Payment.query, tenant_id)
    
    # Current period revenue
    current_revenue = query.filter(
        Payment.payment_date.between(start_date, end_date),
        Payment.status == 'completed'
    ).with_entities(db.func.sum(Payment.amount)).scalar() or 0
    
    # Previous period revenue (same duration before start_date)
    prev_start_date = start_date - (end_date - start_date)
    prev_end_date = start_date - timedelta(days=1)
    
    prev_revenue = query.filter(
        Payment.payment_date.between(prev_start_date, prev_end_date),
        Payment.status == 'completed'
    ).with_entities(db.func.sum(Payment.amount)).scalar() or 0
    
    return {
        'current_period': float(current_revenue),
        'previous_period': float(prev_revenue),
        'absolute_change': float(current_revenue - prev_revenue),
        'percentage_change': ((current_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0,
        'period_duration_days': (end_date - start_date).days
    }

def _get_avg_transaction_value(tenant_id: str, start_date: datetime, end_date: datetime) -> float:
    """Get average transaction value"""
    from ..models import Payment
    query = multi_tenant_query(Payment.query, tenant_id)
    result = query.filter(
        Payment.payment_date.between(start_date, end_date),
        Payment.status == 'completed'
    ).with_entities(
        db.func.count(Payment.id),
        db.func.sum(Payment.amount)
    ).first()
    
    if result and result[0] > 0:
        return float(result[1]) / result[0]
    return 0.0

def _get_conversion_rate(tenant_id: str, start_date: datetime, end_date: datetime) -> float:
    """Get conversion rate (completed appointments vs total scheduled)"""
    from ..models import Appointment
    query = multi_tenant_query(Appointment.query, tenant_id)
    
    total_appointments = query.filter(
        Appointment.scheduled_time.between(start_date, end_date)
    ).count()
    
    completed_appointments = query.filter(
        Appointment.scheduled_time.between(start_date, end_date),
        Appointment.status == 'completed'
    ).count()
    
    if total_appointments > 0:
        return (completed_appointments / total_appointments) * 100
    return 0.0

def _get_patient_demographics(tenant_id: str) -> Dict[str, Any]:
    """Get patient demographic breakdown"""
    from ..models import Patient
    query = multi_tenant_query(Patient.query, tenant_id)
    
    # Age distribution
    age_distribution = query.with_entities(
        db.func.floor((db.func.extract('epoch', db.func.now() - Patient.date_of_birth) / 31556952) / 10) * 10,
        db.func.count(Patient.id)
    ).group_by(db.func.floor((db.func.extract('epoch', db.func.now() - Patient.date_of_birth) / 31556952) / 10) * 10)\
     .order_by(db.func.floor((db.func.extract('epoch', db.func.now() - Patient.date_of_birth) / 31556952) / 10) * 10)\
     .all()
    
    # Gender distribution
    gender_distribution = query.filter(Patient.gender.isnot(None))\
                              .group_by(Patient.gender)\
                              .with_entities(Patient.gender, db.func.count(Patient.id))\
                              .all()
    
    return {
        'age_distribution': {f"{int(age)}-{int(age)+9}": count for age, count in age_distribution if age is not None},
        'gender_distribution': {gender: count for gender, count in gender_distribution},
        'total_patients': query.count()
    }

def _get_patient_acquisition(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get patient acquisition metrics"""
    from ..models import Patient
    query = multi_tenant_query(Patient.query, tenant_id)
    
    # New patients by month
    new_patients = query.filter(Patient.created_at.between(start_date, end_date))\
                       .group_by(db.func.extract('year', Patient.created_at), db.func.extract('month', Patient.created_at))\
                       .with_entities(
                           db.func.extract('year', Patient.created_at).label('year'),
                           db.func.extract('month', Patient.created_at).label('month'),
                           db.func.count(Patient.id)
                       ).order_by('year', 'month')\
                       .all()
    
    # Referral source breakdown (assuming Patient has a referral_source field)
    referral_sources = query.filter(
        Patient.created_at.between(start_date, end_date),
        Patient.referral_source.isnot(None)
    ).group_by(Patient.referral_source)\
     .with_entities(Patient.referral_source, db.func.count(Patient.id))\
     .all()
    
    return {
        'new_patients_by_month': [{
            'year': int(year),
            'month': int(month),
            'count': count,
            'period': f"{int(year)}-{int(month):02d}"
        } for year, month, count in new_patients],
        'referral_sources': {source: count for source, count in referral_sources},
        'total_new_patients': query.filter(Patient.created_at.between(start_date, end_date)).count()
    }

def _get_patient_retention(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get patient retention metrics"""
    from ..models import Patient, Appointment
    patient_query = multi_tenant_query(Patient.query, tenant_id)
    appointment_query = multi_tenant_query(Appointment.query, tenant_id)
    
    # Patients with multiple appointments (retained)
    retained_patients = appointment_query.filter(
        Appointment.scheduled_time.between(start_date, end_date),
        Appointment.status == 'completed'
    ).group_by(Appointment.patient_id)\
     .having(db.func.count(Appointment.id) > 1)\
     .count()
    
    # Total active patients
    total_active_patients = appointment_query.filter(
        Appointment.scheduled_time.between(start_date, end_date),
        Appointment.status == 'completed'
    ).distinct(Appointment.patient_id).count()
    
    retention_rate = (retained_patients / total_active_patients * 100) if total_active_patients > 0 else 0
    
    return {
        'retained_patients': retained_patients,
        'total_active_patients': total_active_patients,
        'retention_rate': retention_rate,
        'churn_rate': 100 - retention_rate
    }

def _get_patient_geography(tenant_id: str) -> Dict[str, Any]:
    """Get patient geographic distribution"""
    from ..models import Patient
    query = multi_tenant_query(Patient.query, tenant_id)
    
    # By city
    by_city = query.filter(Patient.city.isnot(None))\
                  .group_by(Patient.city)\
                  .with_entities(Patient.city, db.func.count(Patient.id))\
                  .order_by(db.func.count(Patient.id).desc())\
                  .limit(10)\
                  .all()
    
    # By state
    by_state = query.filter(Patient.state.isnot(None))\
                   .group_by(Patient.state)\
                   .with_entities(Patient.state, db.func.count(Patient.id))\
                   .order_by(db.func.count(Patient.id).desc())\
                   .all()
    
    return {
        'by_city': {city: count for city, count in by_city},
        'by_state': {state: count for state, count in by_state},
        'total_with_location': query.filter(
            Patient.city.isnot(None) | Patient.state.isnot(None)
        ).count()
    }

def _get_appointment_volume_trend(tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
    """Get appointment volume trend over time"""
    from ..models import Appointment
    query = multi_tenant_query(Appointment.query, tenant_id)
    
    volume_trend = query.filter(Appointment.scheduled_time.between(start_date, end_date))\
                       .group_by(db.func.date(Appointment.scheduled_time))\
                       .with_entities(
                           db.func.date(Appointment.scheduled_time),
                           db.func.count(Appointment.id),
                           db.func.avg(Appointment.duration)
                       ).order_by(db.func.date(Appointment.scheduled_time))\
                       .all()
    
    return [{
        'date': date.isoformat(),
        'appointment_count': count,
        'average_duration': float(avg_duration) if avg_duration else 0
    } for date, count, avg_duration in volume_trend]

def _get_cancellation_analysis(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get appointment cancellation analysis"""
    from ..models import Appointment
    query = multi_tenant_query(Appointment.query, tenant_id)
    
    # Cancellation reasons breakdown
    cancellation_reasons = query.filter(
        Appointment.scheduled_time.between(start_date, end_date),
        Appointment.status == 'cancelled',
        Appointment.cancellation_reason.isnot(None)
    ).group_by(Appointment.cancellation_reason)\
     .with_entities(Appointment.cancellation_reason, db.func.count(Appointment.id))\
     .all()
    
    # Cancellation rate by time of day
    cancellation_by_hour = query.filter(
        Appointment.scheduled_time.between(start_date, end_date),
        Appointment.status == 'cancelled'
    ).group_by(db.func.extract('hour', Appointment.scheduled_time))\
     .with_entities(
         db.func.extract('hour', Appointment.scheduled_time).label('hour'),
         db.func.count(Appointment.id)
     ).order_by('hour')\
     .all()
    
    total_appointments = query.filter(Appointment.scheduled_time.between(start_date, end_date)).count()
    cancelled_appointments = query.filter(
        Appointment.scheduled_time.between(start_date, end_date),
        Appointment.status == 'cancelled'
    ).count()
    
    return {
        'cancellation_reasons': {reason: count for reason, count in cancellation_reasons},
        'cancellation_by_hour': {int(hour): count for hour, count in cancellation_by_hour},
        'total_cancelled': cancelled_appointments,
        'cancellation_rate': (cancelled_appointments / total_appointments * 100) if total_appointments > 0 else 0,
        'total_appointments': total_appointments
    }

def _get_wait_time_analysis(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get appointment wait time analysis"""
    from ..models import Appointment
    query = multi_tenant_query(Appointment.query, tenant_id)
    
    # Average wait time by provider and service type
    wait_time_stats = query.filter(
        Appointment.scheduled_time.between(start_date, end_date),
        Appointment.status == 'completed',
        Appointment.actual_wait_time.isnot(None)
    ).with_entities(
        db.func.avg(Appointment.actual_wait_time),
        db.func.min(Appointment.actual_wait_time),
        db.func.max(Appointment.actual_wait_time),
        db.func.stddev(Appointment.actual_wait_time)
    ).first()
    
    # Wait time distribution
    wait_time_distribution = query.filter(
        Appointment.scheduled_time.between(start_date, end_date),
        Appointment.status == 'completed',
        Appointment.actual_wait_time.isnot(None)
    ).group_by(
        db.func.floor(Appointment.actual_wait_time / 5) * 5
    ).with_entities(
        db.func.floor(Appointment.actual_wait_time / 5) * 5,
        db.func.count(Appointment.id)
    ).order_by(db.func.floor(Appointment.actual_wait_time / 5) * 5)\
     .all()
    
    return {
        'average_wait_time': float(wait_time_stats[0]) if wait_time_stats[0] else 0,
        'min_wait_time': float(wait_time_stats[1]) if wait_time_stats[1] else 0,
        'max_wait_time': float(wait_time_stats[2]) if wait_time_stats[2] else 0,
        'wait_time_stddev': float(wait_time_stats[3]) if wait_time_stats[3] else 0,
        'wait_time_distribution': {f"{int(bin)}-{int(bin)+4}": count for bin, count in wait_time_distribution},
        'total_appointments_with_wait_time': query.filter(
            Appointment.scheduled_time.between(start_date, end_date),
            Appointment.status == 'completed',
            Appointment.actual_wait_time.isnot(None)
        ).count()
    }

def _get_provider_appointment_stats(tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
    """Get appointment statistics by provider"""
    from ..models import Appointment, User
    query = multi_tenant_query(Appointment.query.join(User, Appointment.provider_id == User.id), tenant_id)
    
    provider_stats = query.filter(Appointment.scheduled_time.between(start_date, end_date))\
                         .group_by(User.id, User.first_name, User.last_name)\
                         .with_entities(
                             User.id,
                             User.first_name,
                             User.last_name,
                             db.func.count(Appointment.id),
                             db.func.avg(Appointment.duration),
                             db.func.avg(Appointment.actual_wait_time),
                             db.func.avg(db.func.extract('epoch', Appointment.actual_end_time - Appointment.actual_start_time))
                         ).all()
    
    return [{
        'provider_id': provider_id,
        'provider_name': f"{first_name} {last_name}",
        'total_appointments': count,
        'average_scheduled_duration': float(avg_duration) if avg_duration else 0,
        'average_wait_time': float(avg_wait_time) if avg_wait_time else 0,
        'average_actual_duration': float(avg_actual_duration) if avg_actual_duration else 0,
        'utilization_rate': (float(avg_actual_duration) / float(avg_duration) * 100) if avg_duration and avg_actual_duration else 0
    } for provider_id, first_name, last_name, count, avg_duration, avg_wait_time, avg_actual_duration in provider_stats]



@analytics_bp.errorhandler(403)
def handle_permission_error(e):
    return jsonify({'error': 'Access forbidden', 'message': 'Insufficient permissions'}), 403

@analytics_bp.errorhandler(401)
def handle_authentication_error(e):
    return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401

@analytics_bp.errorhandler(429)
def handle_rate_limit_error(e):
    return jsonify({'error': 'Rate limit exceeded', 'message': 'Too many requests'}), 429