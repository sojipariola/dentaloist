# app/services/email_service.py
import smtplib
from email.mime.text import MIMEText  # ← Correct import
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from app.models.models import EmailLog, db

class EmailService:
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        self.smtp_server = app.config.get('SMTP_SERVER')
        self.smtp_port = app.config.get('SMTP_PORT', 587)
        self.smtp_username = app.config.get('SMTP_USERNAME')
        self.smtp_password = app.config.get('SMTP_PASSWORD')
        self.default_sender = app.config.get('DEFAULT_SENDER')
    
    def send_email(self, to_email, subject, body, html_body=None, **kwargs):
        """Send email and log it"""
        
        # Create email log entry
        email_log = EmailLog(
            recipient_email=to_email,
            subject=subject,
            body=body,
            sender_email=self.default_sender,
            email_type=kwargs.get('email_type'),
            template_id=kwargs.get('template_id')
        )
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.default_sender
            msg['To'] = to_email
            msg['Date'] = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
            
            # Attach body parts
            msg.attach(MIMEText(body, 'plain'))
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            # Mark as sent
            email_log.status = 'sent'
            email_log.provider = 'smtp'
            
        except Exception as e:
            # Mark as failed
            email_log.status = 'failed'
            email_log.status_message = str(e)
            raise e
        
        finally:
            # Save log to database
            db.session.add(email_log)
            db.session.commit()
        
        return email_log

# Initialize email service
email_service = EmailService()


# In your routes or services
# from app.services.email_service import email_service

def send_welcome_email(user):
    subject = "Welcome to Dentaloist!"
    body = f"Hello {user.first_name},\n\nWelcome to our dental practice management system."
    html = f"<h1>Welcome {user.first_name}!</h1><p>Welcome to our system.</p>"
    
    try:
        email_log = email_service.send_email(
            to_email=user.email,
            subject=subject,
            body=body,
            html_body=html,
            email_type='welcome'
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False