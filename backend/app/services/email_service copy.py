# services/email_service.py
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from flask import current_app, render_template
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import os
import jinja2
from pathlib import Path

# Import models for database operations
from ..models import EmailLog, User, Organization, db

class EmailService:
    """
    Comprehensive email service with templating, tracking, and multi-tenant support
    """
    
    def __init__(self, app=None):
        self.app = app
        self.logger = logging.getLogger(__name__)
        self.template_loader = jinja2.FileSystemLoader([
            'templates/emails',
            'app/templates/emails'
        ])
        self.template_env = jinja2.Environment(loader=self.template_loader)
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize email service with Flask app"""
        self.app = app
        self.config = app.config
        
        # Configure template environment
        self.template_env.globals.update({
            'app_name': self.config.get('APP_NAME', 'Dental Practice Pro'),
            'current_year': datetime.now().year,
            'support_email': self.config.get('SUPPORT_EMAIL', 'support@example.com')
        })
    
    def send_email(self, 
                   to_emails: Union[str, List[str]], 
                   subject: str, 
                   template_name: str = None,
                   template_vars: Dict[str, Any] = None,
                   html_body: str = None,
                   text_body: str = None,
                   tenant_id: str = None,
                   user_id: int = None,
                   category: str = 'general',
                   attachments: List[Dict] = None) -> bool:
        """
        Send email with comprehensive tracking and templating
        
        Args:
            to_emails: Single email or list of emails
            subject: Email subject
            template_name: Name of template to use
            template_vars: Variables for template rendering
            html_body: Pre-rendered HTML body
            text_body: Plain text body
            tenant_id: Tenant ID for multi-tenant tracking
            user_id: User ID who triggered the email
            category: Email category for filtering
            attachments: List of attachment dicts with 'filename' and 'content'
        
        Returns:
            bool: Success status
        """
        try:
            # Validate inputs
            if not to_emails:
                self.logger.error("No recipient emails provided")
                return False
            
            if isinstance(to_emails, str):
                to_emails = [to_emails]
            
            # Validate email addresses
            valid_emails = []
            for email in to_emails:
                if self._validate_email(email):
                    valid_emails.append(email)
                else:
                    self.logger.warning(f"Invalid email address: {email}")
            
            if not valid_emails:
                self.logger.error("No valid email addresses provided")
                return False
            
            # Render templates if provided
            html_content, text_content = self._render_content(
                template_name, template_vars, html_body, text_body
            )
            
            if not html_content and not text_content:
                self.logger.error("No email content provided")
                return False
            
            # Create email message
            message = self._create_message(
                valid_emails, subject, html_content, text_content, attachments
            )
            
            # Send email
            success = self._send_smtp_message(valid_emails, message)
            
            # Log email attempt
            self._log_email(
                valid_emails, subject, success, tenant_id, user_id, category
            )
            
            return success
            
        except Exception as e:
            self.logger.error(f"Email sending failed: {str(e)}")
            # Log failed attempt
            self._log_email(
                to_emails, subject, False, tenant_id, user_id, category, str(e)
            )
            return False
    
    def send_template_email(self, 
                          template_name: str,
                          to_emails: Union[str, List[str]],
                          template_vars: Dict[str, Any],
                          tenant_id: str = None,
                          user_id: int = None,
                          category: str = 'template') -> bool:
        """
        Send email using a predefined template
        
        Args:
            template_name: Name of the template to use
            to_emails: Recipient email(s)
            template_vars: Variables for template rendering
            tenant_id: Tenant ID
            user_id: User ID
            category: Email category
        
        Returns:
            bool: Success status
        """
        # Get template configuration
        template_config = self._get_template_config(template_name)
        
        if not template_config:
            self.logger.error(f"Template not found: {template_name}")
            return False
        
        # Merge template variables with defaults
        full_vars = {**template_config.get('default_vars', {}), **template_vars}
        
        # Render subject template
        subject_template = self.template_env.from_string(template_config['subject'])
        subject = subject_template.render(**full_vars)
        
        return self.send_email(
            to_emails=to_emails,
            subject=subject,
            template_name=template_name,
            template_vars=full_vars,
            tenant_id=tenant_id,
            user_id=user_id,
            category=category
        )
    
    def send_bulk_email(self,
                       recipients: List[Dict[str, Any]],
                       template_name: str,
                       template_vars: Dict[str, Any],
                       tenant_id: str = None,
                       user_id: int = None,
                       batch_size: int = 50) -> Dict[str, Any]:
        """
        Send bulk emails with rate limiting and tracking
        
        Args:
            recipients: List of recipient dicts with 'email' and optional 'vars'
            template_name: Template to use
            template_vars: Base template variables
            tenant_id: Tenant ID
            user_id: User ID
            batch_size: Number of emails per batch
        
        Returns:
            Dict with results and statistics
        """
        results = {
            'total': len(recipients),
            'successful': 0,
            'failed': 0,
            'errors': []
        }
        
        for i in range(0, len(recipients), batch_size):
            batch = recipients[i:i + batch_size]
            
            for recipient in batch:
                try:
                    # Merge recipient-specific variables
                    recipient_vars = {**template_vars, **recipient.get('vars', {})}
                    
                    success = self.send_template_email(
                        template_name=template_name,
                        to_emails=recipient['email'],
                        template_vars=recipient_vars,
                        tenant_id=tenant_id,
                        user_id=user_id,
                        category='bulk'
                    )
                    
                    if success:
                        results['successful'] += 1
                    else:
                        results['failed'] += 1
                        results['errors'].append({
                            'email': recipient['email'],
                            'error': 'Send failed'
                        })
                
                except Exception as e:
                    results['failed'] += 1
                    results['errors'].append({
                        'email': recipient.get('email', 'unknown'),
                        'error': str(e)
                    })
            
            # Rate limiting between batches
            if i + batch_size < len(recipients):
                import time
                time.sleep(1)  # 1 second delay between batches
        
        return results
    
    def _render_content(self, 
                       template_name: str, 
                       template_vars: Dict[str, Any],
                       html_body: str,
                       text_body: str) -> tuple:
        """Render email content from templates or provided bodies"""
        html_content = html_body
        text_content = text_body
        
        if template_name:
            try:
                # Render HTML template
                html_template = self.template_env.get_template(f"{template_name}.html")
                html_content = html_template.render(**(template_vars or {}))
                
                # Try to render text template
                try:
                    text_template = self.template_env.get_template(f"{template_name}.txt")
                    text_content = text_template.render(**(template_vars or {}))
                except jinja2.TemplateNotFound:
                    # Generate text version from HTML if no text template
                    text_content = self._html_to_text(html_content)
                    
            except jinja2.TemplateNotFound:
                self.logger.error(f"Email template not found: {template_name}")
                return None, None
            except Exception as e:
                self.logger.error(f"Template rendering failed: {str(e)}")
                return None, None
        
        return html_content, text_content
    
    def _create_message(self, 
                       to_emails: List[str], 
                       subject: str, 
                       html_content: str, 
                       text_content: str,
                       attachments: List[Dict]) -> MIMEMultipart:
        """Create MIME message with attachments"""
        message = MIMEMultipart('mixed')
        message['From'] = self.config.get('MAIL_DEFAULT_SENDER', 'noreply@example.com')
        message['To'] = ', '.join(to_emails)
        message['Subject'] = subject
        
        # Create alternative part for HTML and text
        alternative = MIMEMultipart('alternative')
        message.attach(alternative)
        
        # Add text part
        if text_content:
            text_part = MIMEText(text_content, 'plain')
            alternative.attach(text_part)
        
        # Add HTML part
        if html_content:
            html_part = MIMEText(html_content, 'html')
            alternative.attach(html_part)
        
        # Add attachments
        if attachments:
            for attachment in attachments:
                attachment_part = MIMEApplication(
                    attachment['content'],
                    Name=attachment['filename']
                )
                attachment_part['Content-Disposition'] = f'attachment; filename="{attachment["filename"]}"'
                message.attach(attachment_part)
        
        return message
    
    def _send_smtp_message(self, to_emails: List[str], message: MIMEMultipart) -> bool:
        """Send message via SMTP"""
        try:
            # Use test mode if configured
            if self.config.get('MAIL_SUPPRESS_SEND'):
                self.logger.info(f"Email suppressed (test mode): {to_emails}")
                return True
            
            # SMTP configuration
            smtp_host = self.config.get('MAIL_SERVER', 'localhost')
            smtp_port = self.config.get('MAIL_PORT', 587)
            smtp_username = self.config.get('MAIL_USERNAME')
            smtp_password = self.config.get('MAIL_PASSWORD')
            use_tls = self.config.get('MAIL_USE_TLS', True)
            use_ssl = self.config.get('MAIL_USE_SSL', False)
            
            # Create SMTP connection
            if use_ssl:
                server = smtplib.SMTP_SSL(smtp_host, smtp_port)
            else:
                server = smtplib.SMTP(smtp_host, smtp_port)
            
            # Start TLS if required
            if use_tls and not use_ssl:
                server.starttls()
            
            # Login if credentials provided
            if smtp_username and smtp_password:
                server.login(smtp_username, smtp_password)
            
            # Send email
            server.send_message(message)
            server.quit()
            
            self.logger.info(f"Email sent successfully to: {to_emails}")
            return True
            
        except Exception as e:
            self.logger.error(f"SMTP sending failed: {str(e)}")
            return False
    
    def _log_email(self, 
                  to_emails: List[str], 
                  subject: str, 
                  success: bool, 
                  tenant_id: str, 
                  user_id: int, 
                  category: str, 
                  error_message: str = None):
        """Log email attempt to database"""
        try:
            email_log = EmailLog(
                tenant_id=tenant_id,
                user_id=user_id,
                recipient_emails=','.join(to_emails),
                subject=subject,
                category=category,
                success=success,
                error_message=error_message,
                sent_at=datetime.utcnow()
            )
            
            db.session.add(email_log)
            db.session.commit()
            
        except Exception as e:
            self.logger.error(f"Failed to log email: {str(e)}")
    
    def _validate_email(self, email: str) -> bool:
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _html_to_text(self, html_content: str) -> str:
        """Convert HTML to plain text (basic implementation)"""
        import re
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html_content)
        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _get_template_config(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get template configuration"""
        templates = {
            'welcome': {
                'subject': 'Welcome to {{app_name}}',
                'default_vars': {
                    'welcome_message': 'Thank you for joining our dental practice!'
                }
            },
            'appointment_reminder': {
                'subject': 'Appointment Reminder - {{appointment_date}}',
                'default_vars': {
                    'reminder_type': '24_hour'
                }
            },
            'password_reset': {
                'subject': 'Password Reset Request',
                'default_vars': {
                    'reset_url': '#'
                }
            },
            'two_factor_code': {
                'subject': 'Your Verification Code',
                'default_vars': {
                    'code': '000000'
                }
            },
            'invoice': {
                'subject': 'Invoice #{{invoice_number}}',
                'default_vars': {
                    'due_date': 'N/A',
                    'amount': '0.00'
                }
            },
            'lab_results': {
                'subject': 'Lab Results Available',
                'default_vars': {
                    'test_type': 'General Test'
                }
            }
        }
        
        return templates.get(template_name)
    
    def get_email_stats(self, tenant_id: str = None, days: int = 30) -> Dict[str, Any]:
        """Get email statistics for a tenant"""
        try:
            query = EmailLog.query
            
            if tenant_id:
                query = query.filter_by(tenant_id=tenant_id)
            
            start_date = datetime.utcnow() - timedelta(days=days)
            query = query.filter(EmailLog.sent_at >= start_date)
            
            total_emails = query.count()
            successful_emails = query.filter_by(success=True).count()
            failed_emails = total_emails - successful_emails
            
            # Category breakdown
            category_stats = db.session.query(
                EmailLog.category,
                db.func.count(EmailLog.id)
            ).filter(EmailLog.sent_at >= start_date)
            
            if tenant_id:
                category_stats = category_stats.filter_by(tenant_id=tenant_id)
            
            category_stats = category_stats.group_by(EmailLog.category).all()
            
            return {
                'total_emails': total_emails,
                'successful_emails': successful_emails,
                'failed_emails': failed_emails,
                'success_rate': (successful_emails / total_emails * 100) if total_emails > 0 else 0,
                'category_breakdown': {category: count for category, count in category_stats},
                'period_days': days
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get email stats: {str(e)}")
            return {}
    
    def resend_failed_emails(self, email_log_ids: List[int]) -> Dict[str, Any]:
        """Resend failed emails"""
        results = {
            'attempted': len(email_log_ids),
            'successful': 0,
            'failed': 0,
            'details': []
        }
        
        for log_id in email_log_ids:
            try:
                email_log = EmailLog.query.get(log_id)
                if not email_log:
                    results['details'].append({'id': log_id, 'error': 'Not found'})
                    results['failed'] += 1
                    continue
                
                # Extract recipient emails
                recipient_emails = email_log.recipient_emails.split(',')
                
                # Resend email (simplified - in practice you'd need original content)
                success = self.send_email(
                    to_emails=recipient_emails,
                    subject=f"RESEND: {email_log.subject}",
                    text_body="Original email content not available for resend. Please contact support.",
                    tenant_id=email_log.tenant_id,
                    user_id=email_log.user_id,
                    category=f"resend_{email_log.category}"
                )
                
                if success:
                    results['successful'] += 1
                    results['details'].append({'id': log_id, 'status': 'resent'})
                else:
                    results['failed'] += 1
                    results['details'].append({'id': log_id, 'error': 'Resend failed'})
                    
            except Exception as e:
                results['failed'] += 1
                results['details'].append({'id': log_id, 'error': str(e)})
        
        return results

# Global email service instance
email_service = EmailService()

# Convenience functions
def send_email(to_emails, subject, **kwargs):
    """Convenience function for sending emails"""
    return email_service.send_email(to_emails, subject, **kwargs)

def send_template_email(template_name, to_emails, template_vars, **kwargs):
    """Convenience function for sending template emails"""
    return email_service.send_template_email(template_name, to_emails, template_vars, **kwargs)

def get_email_stats(tenant_id=None, days=30):
    """Convenience function for getting email statistics"""
    return email_service.get_email_stats(tenant_id, days)