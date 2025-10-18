from flask import Blueprint, request, jsonify, g, current_app, send_file
# import current_user

from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from sqlalchemy import func, extract, case, and_, or_
from sqlalchemy.orm import aliased
import pandas as pd
from io import BytesIO
import json
from flask_login import current_user

from ..models import (
    db, FinancialReport, AnalyticsReport, Invoice, Payment, Appointment, Patient,
    User, Treatment, MedicalRecord, InsuranceClaim, Organization
)
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

# ===== Financial Report Routes =====

@reports_bp.route('/financial', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_analytics', 'view_billing'])
@rate_limit(limit=30, period=60)
def get_financial_reports():
    """
    Get list of saved financial reports with filtering and pagination
    """
    try:
        current_user = get_current_user()
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)
        is_template = request.args.get('is_template', type=bool)
        
        query = multi_tenant_query(FinancialReport)
        
        # Apply filters
        if is_template is not None:
            query = query.filter(FinancialReport.is_template == is_template)
        
        # Order by most recent
        reports = query.order_by(FinancialReport.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'reports': [report.to_dict() for report in reports.items],
            'pagination': {
                'total': reports.total,
                'pages': reports.pages,
                'current_page': page,
                'per_page': per_page
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching financial reports: {str(e)}")
        return jsonify({'error': 'Failed to fetch financial reports'}), 500

@reports_bp.route('/financial', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_analytics', 'manage_billing'])
def create_financial_report():
    """
    Create a new financial report or template
    """
    try:
        data = request.get_json()
        
        report = FinancialReport(
            organization_id=g.tenant_id,
            title=data['title'],
            description=data.get('description'),
            report_type=data.get('report_type', 'financial_summary'),
            parameters=data.get('parameters', {}),
            is_template=data.get('is_template', False),
            is_public=data.get('is_public', False),
            created_by=current_user.id
        )
        
        db.session.add(report)
        db.session.commit()
        
        return jsonify({
            'message': 'Financial report created successfully',
            'report': report.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating financial report: {str(e)}")
        return jsonify({'error': 'Failed to create financial report'}), 500

@reports_bp.route('/financial/summary', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_analytics', 'view_billing'])
def get_financial_summary():
    """
    Get financial summary report with advanced filtering
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        group_by = request.args.get('group_by', 'month')  # day, week, month, year
        
        # Parse dates with validation
        start_date_obj, end_date_obj = _parse_date_range(start_date, end_date)
        
        # Revenue analysis
        revenue_query = multi_tenant_query(Invoice).filter(
            Invoice.status.in_(['paid', 'partial']),
            Invoice.invoice_date.between(start_date_obj, end_date_obj)
        )
        
        # Group by period
        group_by_expr = _get_date_group_expression(Invoice.invoice_date, group_by)
        
        revenue_results = db.session.query(
            group_by_expr.label('period'),
            func.count(Invoice.id).label('invoice_count'),
            func.sum(Invoice.total_amount).label('total_revenue'),
            func.sum(Invoice.amount_paid).label('total_collected'),
            func.sum(Invoice.balance_due).label('outstanding_balance'),
            func.avg(Invoice.total_amount).label('average_invoice')
        ).group_by('period').order_by('period').all()
        
        # Payment analysis
        payment_results = db.session.query(
            Payment.payment_method,
            func.count(Payment.id).label('payment_count'),
            func.sum(Payment.amount).label('total_amount')
        ).filter(
            Payment.status == 'completed',
            Payment.payment_date.between(start_date_obj, end_date_obj)
        ).group_by(Payment.payment_method).all()
        
        # Insurance claims analysis
        insurance_results = db.session.query(
            InsuranceClaim.status,
            func.count(InsuranceClaim.id).label('claim_count'),
            func.sum(InsuranceClaim.claim_amount).label('total_claimed'),
            func.sum(InsuranceClaim.approved_amount).label('total_approved')
        ).filter(
            InsuranceClaim.submission_date.between(start_date_obj, end_date_obj)
        ).group_by(InsuranceClaim.status).all()
        
        # Calculate summary metrics
        total_revenue = sum(result.total_revenue or 0 for result in revenue_results)
        total_collected = sum(result.total_collected or 0 for result in revenue_results)
        collection_rate = (total_collected / total_revenue * 100) if total_revenue > 0 else 0
        
        report_data = {
            'summary': {
                'total_revenue': float(total_revenue),
                'total_collected': float(total_collected),
                'outstanding_balance': float(total_revenue - total_collected),
                'collection_rate': round(collection_rate, 2),
                'average_invoice': float(revenue_results[0].average_invoice) if revenue_results else 0,
                'total_invoices': sum(result.invoice_count or 0 for result in revenue_results)
            },
            'revenue_breakdown': [
                {
                    'period': result.period.strftime('%Y-%m-%d') if hasattr(result.period, 'strftime') else str(result.period),
                    'invoice_count': result.invoice_count,
                    'total_revenue': float(result.total_revenue or 0),
                    'total_collected': float(result.total_collected or 0),
                    'outstanding_balance': float(result.outstanding_balance or 0),
                    'average_invoice': float(result.average_invoice or 0)
                }
                for result in revenue_results
            ],
            'payment_methods': [
                {
                    'method': method.value if hasattr(method, 'value') else method,
                    'payment_count': count,
                    'total_amount': float(amount or 0)
                }
                for method, count, amount in payment_results
            ],
            'insurance_claims': [
                {
                    'status': status.value if hasattr(status, 'value') else status,
                    'claim_count': count,
                    'total_claimed': float(claimed or 0),
                    'total_approved': float(approved or 0)
                }
                for status, count, claimed, approved in insurance_results
            ],
            'time_period': {
                'start_date': start_date_obj.isoformat(),
                'end_date': end_date_obj.isoformat(),
                'group_by': group_by
            }
        }
        
        return jsonify(report_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Error generating financial summary report: {str(e)}")
        return jsonify({'error': 'Failed to generate financial summary report'}), 500

@reports_bp.route('/financial/aging', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_analytics', 'view_billing'])
def get_aging_report():
    """
    Get accounts receivable aging report
    """
    try:
        current_date = datetime.utcnow().date()
        
        aging_buckets = [
            ('current', 0, 0),      # Not yet due
            ('1-30', 1, 30),        # 1-30 days overdue
            ('31-60', 31, 60),      # 31-60 days overdue
            ('61-90', 61, 90),      # 61-90 days overdue
            ('91+', 91, None)       # Over 90 days overdue
        ]
        
        aging_data = {}
        total_outstanding = 0
        
        for bucket_name, days_min, days_max in aging_buckets:
            if bucket_name == 'current':
                # Current (not yet due) invoices
                query = multi_tenant_query(Invoice).filter(
                    Invoice.status.in_(['sent', 'viewed', 'partial']),
                    Invoice.balance_due > 0,
                    Invoice.due_date >= current_date
                )
            elif days_max is not None:
                # Specific aging bucket
                query = multi_tenant_query(Invoice).filter(
                    Invoice.status.in_(['sent', 'viewed', 'partial']),
                    Invoice.balance_due > 0,
                    Invoice.due_date.between(
                        current_date - timedelta(days=days_max),
                        current_date - timedelta(days=days_min)
                    )
                )
            else:
                # 91+ days overdue
                query = multi_tenant_query(Invoice).filter(
                    Invoice.status.in_(['sent', 'viewed', 'partial']),
                    Invoice.balance_due > 0,
                    Invoice.due_date <= current_date - timedelta(days=days_min)
                )
            
            bucket_invoices = query.all()
            bucket_total = sum(invoice.balance_due for invoice in bucket_invoices)
            aging_data[bucket_name] = {
                'amount': float(bucket_total),
                'invoice_count': len(bucket_invoices),
                'invoices': [{
                    'id': invoice.id,
                    'invoice_number': invoice.invoice_number,
                    'patient_name': f"{invoice.patient.first_name} {invoice.patient.last_name}" if invoice.patient else 'Unknown',
                    'due_date': invoice.due_date.isoformat() if invoice.due_date else None,
                    'amount': float(invoice.balance_due)
                } for invoice in bucket_invoices[:10]]  # Limit to first 10 for preview
            }
            total_outstanding += bucket_total
        
        return jsonify({
            'aging_data': aging_data,
            'total_outstanding': float(total_outstanding),
            'report_date': current_date.isoformat()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error generating aging report: {str(e)}")
        return jsonify({'error': 'Failed to generate aging report'}), 500

# ===== Analytics Report Routes =====

@reports_bp.route('/analytics', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_analytics'])
@rate_limit(limit=30, period=60)
def get_analytics_reports():
    """
    Get list of saved analytics reports with filtering and pagination
    """
    try:
        current_user = get_current_user()
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)
        is_template = request.args.get('is_template', type=bool)
        
        query = multi_tenant_query(AnalyticsReport)
        
        # Apply filters
        if is_template is not None:
            query = query.filter(AnalyticsReport.is_template == is_template)
        
        # Order by most recent
        reports = query.order_by(AnalyticsReport.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'reports': [report.to_dict() for report in reports.items],
            'pagination': {
                'total': reports.total,
                'pages': reports.pages,
                'current_page': page,
                'per_page': per_page
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching analytics reports: {str(e)}")
        return jsonify({'error': 'Failed to fetch analytics reports'}), 500

@reports_bp.route('/analytics', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_analytics'])
def create_analytics_report():
    """
    Create a new analytics report or template
    """
    try:
        data = request.get_json()
        
        report = AnalyticsReport(
            organization_id=g.tenant_id,
            title=data['title'],
            description=data.get('description'),
            report_type=data.get('report_type', 'dashboard_stats'),
            parameters=data.get('parameters', {}),
            is_template=data.get('is_template', False),
            is_public=data.get('is_public', False),
            created_by=current_user.id
        )
        
        db.session.add(report)
        db.session.commit()
        
        return jsonify({
            'message': 'Analytics report created successfully',
            'report': report.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating analytics report: {str(e)}")
        return jsonify({'error': 'Failed to create analytics report'}), 500

@reports_bp.route('/analytics/appointments', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_analytics'])
def get_appointment_analytics():
    """
    Get comprehensive appointment analytics report
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        provider_id = request.args.get('provider_id')
        
        start_date_obj, end_date_obj = _parse_date_range(start_date, end_date)
        
        # Base query
        query = multi_tenant_query(Appointment).filter(
            Appointment.start_time.between(start_date_obj, end_date_obj)
        )
        
        if provider_id:
            query = query.filter(Appointment.dentist_id == provider_id)
        
        # Calculate metrics
        total_appointments = query.count()
        
        status_counts = db.session.query(
            Appointment.status,
            func.count(Appointment.id)
        ).filter(
            Appointment.start_time.between(start_date_obj, end_date_obj)
        ).group_by(Appointment.status).all()
        
        # Provider performance
        provider_stats = db.session.query(
            User.first_name,
            User.last_name,
            func.count(Appointment.id).label('appointment_count'),
            func.avg(Appointment.duration).label('avg_duration'),
            func.avg(case(
                [(Appointment.status == 'completed', 1)],
                else_=0
            ) * 100).label('completion_rate')
        ).join(Appointment, User.id == Appointment.dentist_id
        ).filter(
            Appointment.start_time.between(start_date_obj, end_date_obj)
        ).group_by(User.id, User.first_name, User.last_name).all()
        
        # Service type analysis
        service_stats = db.session.query(
            Appointment.type,
            func.count(Appointment.id).label('appointment_count'),
            func.avg(Appointment.duration).label('avg_duration')
        ).filter(
            Appointment.start_time.between(start_date_obj, end_date_obj)
        ).group_by(Appointment.type).all()
        
        # Daily appointment volume
        daily_volume = db.session.query(
            func.date(Appointment.start_time).label('date'),
            func.count(Appointment.id).label('appointment_count')
        ).filter(
            Appointment.start_time.between(start_date_obj, end_date_obj)
        ).group_by(func.date(Appointment.start_time)).order_by('date').all()
        
        report_data = {
            'summary': {
                'total_appointments': total_appointments,
                'time_period': {
                    'start_date': start_date_obj.isoformat(),
                    'end_date': end_date_obj.isoformat()
                }
            },
            'status_breakdown': {
                status.value if hasattr(status, 'value') else status: count 
                for status, count in status_counts
            },
            'provider_performance': [
                {
                    'provider_name': f"{first_name} {last_name}",
                    'appointment_count': count,
                    'average_duration': float(avg_duration or 0),
                    'completion_rate': float(completion_rate or 0)
                }
                for first_name, last_name, count, avg_duration, completion_rate in provider_stats
            ],
            'service_analysis': [
                {
                    'service_type': service_type.value if hasattr(service_type, 'value') else service_type,
                    'appointment_count': count,
                    'average_duration': float(avg_duration or 0)
                }
                for service_type, count, avg_duration in service_stats
            ],
            'daily_volume': [
                {
                    'date': date.isoformat(),
                    'appointment_count': count
                }
                for date, count in daily_volume
            ]
        }
        
        return jsonify(report_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Error generating appointment analytics: {str(e)}")
        return jsonify({'error': 'Failed to generate appointment analytics'}), 500

@reports_bp.route('/analytics/patient-activity', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_analytics'])
def get_patient_activity_analytics():
    """
    Get patient activity and engagement analytics
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        start_date_obj, end_date_obj = _parse_date_range(start_date, end_date)
        
        # New patients
        new_patients = multi_tenant_query(Patient).filter(
            Patient.created_at.between(start_date_obj, end_date_obj)
        ).count()
        
        # Active patients (patients with appointments in period)
        active_patients = db.session.query(func.count(func.distinct(Appointment.patient_id))).filter(
            Appointment.start_time.between(start_date_obj, end_date_obj)
        ).scalar() or 0
        
        # Appointment frequency analysis
        appointment_frequency = db.session.query(
            func.count(Appointment.id).label('appointment_count'),
            func.count(func.distinct(Appointment.patient_id)).label('patient_count')
        ).filter(
            Appointment.start_time.between(start_date_obj, end_date_obj),
            Appointment.status == 'completed'
        ).first()
        
        avg_appointments_per_patient = (
            appointment_frequency.appointment_count / appointment_frequency.patient_count 
            if appointment_frequency.patient_count > 0 else 0
        )
        
        # Treatment compliance
        treatment_stats = db.session.query(
            Treatment.status,
            func.count(Treatment.id).label('treatment_count')
        ).filter(
            Treatment.created_at.between(start_date_obj, end_date_obj)
        ).group_by(Treatment.status).all()
        
        report_data = {
            'patient_metrics': {
                'new_patients': new_patients,
                'active_patients': active_patients,
                'total_appointments': appointment_frequency.appointment_count if appointment_frequency else 0,
                'avg_appointments_per_patient': round(avg_appointments_per_patient, 2)
            },
            'treatment_compliance': {
                status.value if hasattr(status, 'value') else status: count 
                for status, count in treatment_stats
            },
            'time_period': {
                'start_date': start_date_obj.isoformat(),
                'end_date': end_date_obj.isoformat()
            }
        }
        
        return jsonify(report_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Error generating patient activity analytics: {str(e)}")
        return jsonify({'error': 'Failed to generate patient activity analytics'}), 500

# ===== Export Routes =====

@reports_bp.route('/financial/export', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_analytics', 'view_billing'])
def export_financial_report():
    """
    Export financial report data in CSV format
    """
    try:
        report_type = request.args.get('type', 'summary')  # summary, aging, etc.
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if report_type == 'summary':
            data = _generate_financial_summary_data(start_date, end_date)
            filename = f"financial_summary_{datetime.utcnow().strftime('%Y%m%d')}.csv"
        elif report_type == 'aging':
            data = _generate_aging_report_data()
            filename = f"aging_report_{datetime.utcnow().strftime('%Y%m%d')}.csv"
        else:
            return jsonify({'error': 'Invalid report type'}), 400
        
        return _export_to_csv(data, filename)
            
    except Exception as e:
        current_app.logger.error(f"Error exporting financial report: {str(e)}")
        return jsonify({'error': 'Failed to export financial report'}), 500

@reports_bp.route('/analytics/export', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_analytics'])
def export_analytics_report():
    """
    Export analytics report data in CSV format
    """
    try:
        report_type = request.args.get('type', 'appointments')  # appointments, patient-activity, etc.
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if report_type == 'appointments':
            data = _generate_appointment_analytics_data(start_date, end_date)
            filename = f"appointment_analytics_{datetime.utcnow().strftime('%Y%m%d')}.csv"
        elif report_type == 'patient-activity':
            data = _generate_patient_activity_data(start_date, end_date)
            filename = f"patient_activity_{datetime.utcnow().strftime('%Y%m%d')}.csv"
        else:
            return jsonify({'error': 'Invalid report type'}), 400
        
        return _export_to_csv(data, filename)
            
    except Exception as e:
        current_app.logger.error(f"Error exporting analytics report: {str(e)}")
        return jsonify({'error': 'Failed to export analytics report'}), 500

# ===== Helper Functions =====

def _parse_date_range(start_date, end_date):
    """Parse and validate date range with defaults"""
    try:
        if not start_date:
            start_date_obj = datetime.utcnow() - timedelta(days=30)
        else:
            start_date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        
        if not end_date:
            end_date_obj = datetime.utcnow()
        else:
            end_date_obj = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # Validate date range
        if start_date_obj > end_date_obj:
            raise ValueError("Start date cannot be after end date")
        
        if (end_date_obj - start_date_obj).days > 365:
            raise ValueError("Date range cannot exceed 1 year")
        
        return start_date_obj, end_date_obj
        
    except ValueError as e:
        raise ValueError(f"Invalid date format: {str(e)}")

def _get_date_group_expression(column, group_by):
    """Get SQL expression for date grouping"""
    if group_by == 'day':
        return func.date(column)
    elif group_by == 'week':
        return func.date_trunc('week', column)
    elif group_by == 'month':
        return func.date_trunc('month', column)
    elif group_by == 'year':
        return func.date_trunc('year', column)
    else:
        return func.date(column)

def _generate_financial_summary_data(start_date, end_date):
    """Generate financial summary data for export"""
    # This would contain the actual data generation logic
    return {"message": "Financial summary data generation not implemented"}

def _generate_aging_report_data():
    """Generate aging report data for export"""
    return {"message": "Aging report data generation not implemented"}

def _generate_appointment_analytics_data(start_date, end_date):
    """Generate appointment analytics data for export"""
    return {"message": "Appointment analytics data generation not implemented"}

def _generate_patient_activity_data(start_date, end_date):
    """Generate patient activity data for export"""
    return {"message": "Patient activity data generation not implemented"}

def _export_to_csv(data, filename):
    """Export data to CSV format"""
    # Simple CSV implementation - you can enhance this based on your data structure
    if isinstance(data, dict) and 'message' in data:
        # For now, return a simple CSV with the message
        csv_data = "Report Data\n" + data['message']
    else:
        # Convert complex data to CSV (you'd implement this based on your data structure)
        csv_data = "Column1,Column2,Column3\nValue1,Value2,Value3\n"
    
    return send_file(
        BytesIO(csv_data.encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )