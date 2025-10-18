# app/services/email_service.py
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import jinja2
from flask import current_app

# Import models
from ..models import EmailLog, db

logger = logging.getLogger(__name__)

class EmailService:
    """
    Unified email service with templating, tracking, and multi-tenant support
    """
    
    def __init__(self, app=None):
        self.app = app
        self.logger = logger
        self.template_loader = jinja2.FileSystemLoader([
            'app/templates/emails',
            'templates/emails'
        ])
        self.template_env = jinja2.Environment(loader=self.template_loader)
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize email service with Flask app"""
        self.app = app
        
        # Configure template environment
        self.template_env.globals.update({
            'app_name': app.config.get('APP_NAME', 'Dentaloist'),
            'current_year': datetime.now().year,
            'support_email': app.config.get('SUPPORT_EMAIL', 'support@dentaloist.com')
        })
    
    def send_email(self, 
                   to_email: str, 
                   subject: str, 
                   body: str = None,
                   html_body: str = None,
                   email_type: str = None,
                   template_id: str = None,
                   **kwargs) -> EmailLog:
        """
        Send email and log it (simplified version from your first implementation)
        """
        # Create email log entry
        email_log = EmailLog(
            recipient_email=to_email,
            subject=subject,
            body=body or '',
            sender_email=self.app.config.get('DEFAULT_SENDER', 'noreply@dentaloist.com'),
            email_type=email_type,
            template_id=template_id
        )
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.app.config.get('DEFAULT_SENDER', 'noreply@dentaloist.com')
            msg['To'] = to_email
            msg['Date'] = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
            
            # Attach body parts
            if body:
                msg.attach(MIMEText(body, 'plain'))
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))
            
            # Get SMTP configuration
            smtp_server = self.app.config.get('SMTP_SERVER', 'localhost')
            smtp_port = self.app.config.get('SMTP_PORT', 587)
            smtp_username = self.app.config.get('SMTP_USERNAME')
            smtp_password = self.app.config.get('SMTP_PASSWORD')
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                if smtp_username and smtp_password:
                    server.login(smtp_username, smtp_password)
                server.send_message(msg)
            
            # Mark as sent
            email_log.status = 'sent'
            email_log.provider = 'smtp'
            
        except Exception as e:
            # Mark as failed
            email_log.status = 'failed'
            email_log.status_message = str(e)
            self.logger.error(f"Failed to send email to {to_email}: {e}")
            raise e
        
        finally:
            # Save log to database
            db.session.add(email_log)
            db.session.commit()
        
        return email_log
    
    def send_template_email(self, 
                          template_name: str,
                          to_email: str,
                          template_vars: Dict[str, Any] = None,
                          **kwargs) -> bool:
        """
        Send email using a template
        """
        try:
            # Render templates
            html_content, text_content = self._render_template(
                template_name, template_vars or {}
            )
            
            if not html_content and not text_content:
                self.logger.error(f"No content rendered for template: {template_name}")
                return False
            
            # Send email
            email_log = self.send_email(
                to_email=to_email,
                subject=template_vars.get('subject', f"Message from {self.app.config.get('APP_NAME', 'Dentaloist')}"),
                body=text_content,
                html_body=html_content,
                email_type='template',
                template_id=template_name,
                **kwargs
            )
            
            return email_log.status == 'sent'
            
        except Exception as e:
            self.logger.error(f"Template email failed: {e}")
            return False
    
    def _render_template(self, 
                        template_name: str, 
                        template_vars: Dict[str, Any]) -> tuple:
        """Render email template"""
        try:
            # Render HTML template
            html_template = self.template_env.get_template(f"{template_name}.html")
            html_content = html_template.render(**(template_vars or {}))
            
            # Try to render text template
            try:
                text_template = self.template_env.get_template(f"{template_name}.txt")
                text_content = text_template.render(**(template_vars or {}))
            except jinja2.TemplateNotFound:
                # Generate text version from HTML
                text_content = self._html_to_text(html_content)
            
            return html_content, text_content
            
        except jinja2.TemplateNotFound:
            self.logger.error(f"Email template not found: {template_name}")
            return None, None
        except Exception as e:
            self.logger.error(f"Template rendering failed: {e}")
            return None, None
    
    def _html_to_text(self, html_content: str) -> str:
        """Convert HTML to plain text"""
        import re
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html_content)
        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def send_welcome_email(self, user) -> bool:
        """Send welcome email to new user"""
        try:
            template_vars = {
                'user': user,
                'app_name': self.app.config.get('APP_NAME', 'Dentaloist'),
                'login_url': self.app.config.get('LOGIN_URL', '/login'),
                'support_email': self.app.config.get('SUPPORT_EMAIL', 'support@dentaloist.com')
            }
            
            return self.send_template_email(
                template_name='welcome',
                to_email=user.email,
                template_vars=template_vars,
                email_type='welcome'
            )
            
        except Exception as e:
            self.logger.error(f"Welcome email failed for user {user.email}: {e}")
            return False
    
    def send_password_reset_email(self, user, reset_token) -> bool:
        """Send password reset email"""
        try:
            reset_url = f"{self.app.config.get('FRONTEND_URL', '')}/reset-password?token={reset_token}"
            
            template_vars = {
                'user': user,
                'reset_url': reset_url,
                'expiry_hours': self.app.config.get('PASSWORD_RESET_EXPIRY', 24)
            }
            
            return self.send_template_email(
                template_name='password_reset',
                to_email=user.email,
                template_vars=template_vars,
                email_type='password_reset'
            )
            
        except Exception as e:
            self.logger.error(f"Password reset email failed for user {user.email}: {e}")
            return False
    
    def send_2fa_code_email(self, user, code) -> bool:
        """Send 2FA verification code email"""
        try:
            template_vars = {
                'user': user,
                'code': code,
                'expiry_minutes': 10  # 2FA codes typically expire quickly
            }
            
            return self.send_template_email(
                template_name='two_factor',
                to_email=user.email,
                template_vars=template_vars,
                email_type='2fa_code'
            )
            
        except Exception as e:
            self.logger.error(f"2FA code email failed for user {user.email}: {e}")
            return False

# Global email service instance
email_service = EmailService()

# Convenience functions
def init_email_service(app):
    """Initialize the email service with Flask app"""
    email_service.init_app(app)

def send_welcome_email(user):
    """Convenience function for sending welcome emails"""
    return email_service.send_welcome_email(user)

def send_password_reset_email(user, reset_token):
    """Convenience function for sending password reset emails"""
    return email_service.send_password_reset_email(user, reset_token)

def send_2fa_code_email(user, code):
    """Convenience function for sending 2FA code emails"""
    return email_service.send_2fa_code_email(user, code)

def send_email(to_email, subject, **kwargs):
    """Convenience function for sending emails"""
    return email_service.send_email(to_email, subject, **kwargs)

def send_template_email(template_name, to_email, template_vars, **kwargs):
    """Convenience function for sending template emails"""
    return email_service.send_template_email(template_name, to_email, template_vars, **kwargs)