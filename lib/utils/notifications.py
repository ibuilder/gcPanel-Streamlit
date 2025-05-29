"""
Notification utilities for gcPanel.

This module provides functions for sending notifications
via email and SMS for various application events.
"""

import os
import logging
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import threading
from twilio.rest import Client

# Setup logging
logger = logging.getLogger(__name__)

# Constants
NOTIFICATION_CONFIG_FILE = "config/notifications.json"
NOTIFICATION_TEMPLATES_DIR = "templates/notifications"

# Notification Types
class NotificationType:
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    SUCCESS = "success"

# Notification Channels
class NotificationChannel:
    IN_APP = "in_app"
    EMAIL = "email"
    SMS = "sms"

def ensure_dirs_exist():
    """Ensure notification directories exist."""
    os.makedirs(os.path.dirname(NOTIFICATION_CONFIG_FILE), exist_ok=True)
    os.makedirs(NOTIFICATION_TEMPLATES_DIR, exist_ok=True)

def load_notification_config():
    """
    Load notification configuration.
    
    Returns:
        dict: Notification configuration
    """
    ensure_dirs_exist()
    
    if not os.path.exists(NOTIFICATION_CONFIG_FILE):
        # Create default config
        default_config = {
            "channels": {
                "in_app": {
                    "enabled": True
                },
                "email": {
                    "enabled": False,
                    "from_email": "noreply@example.com",
                    "smtp_server": "smtp.example.com",
                    "smtp_port": 587,
                    "smtp_use_tls": True,
                    "smtp_username": "",
                    "smtp_password": ""
                },
                "sms": {
                    "enabled": False,
                    "twilio_account_sid": "",
                    "twilio_auth_token": "",
                    "twilio_phone_number": ""
                }
            },
            "notification_levels": {
                "info": ["in_app"],
                "warning": ["in_app", "email"],
                "critical": ["in_app", "email", "sms"],
                "success": ["in_app"]
            },
            "user_preferences": {
                "default": {
                    "in_app": True,
                    "email": True,
                    "sms": False
                }
            }
        }
        
        with open(NOTIFICATION_CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    try:
        with open(NOTIFICATION_CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading notification config: {str(e)}")
        return {}

def save_notification_config(config):
    """
    Save notification configuration.
    
    Args:
        config: Notification configuration to save
    """
    ensure_dirs_exist()
    
    with open(NOTIFICATION_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_template(template_name):
    """
    Get a notification template.
    
    Args:
        template_name: Name of the template
        
    Returns:
        dict: Template with subject and body
    """
    template_file = os.path.join(NOTIFICATION_TEMPLATES_DIR, f"{template_name}.json")
    
    if not os.path.exists(template_file):
        # Create a default template
        default_template = {
            "subject": "Notification from gcPanel",
            "body": "This is a notification from gcPanel."
        }
        
        with open(template_file, 'w') as f:
            json.dump(default_template, f, indent=2)
        
        return default_template
    
    try:
        with open(template_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading template {template_name}: {str(e)}")
        return {
            "subject": "Notification from gcPanel",
            "body": "This is a notification from gcPanel."
        }

def format_template(template, context):
    """
    Format a template with context variables.
    
    Args:
        template: Template dict with subject and body
        context: Dict of variables to substitute
        
    Returns:
        dict: Formatted template
    """
    subject = template.get("subject", "")
    body = template.get("body", "")
    
    # Simple string formatting
    for key, value in context.items():
        placeholder = f"{{{key}}}"
        subject = subject.replace(placeholder, str(value))
        body = body.replace(placeholder, str(value))
    
    return {
        "subject": subject,
        "body": body
    }

def send_in_app_notification(user_id, subject, body, notification_type=NotificationType.INFO):
    """
    Send an in-app notification.
    
    Args:
        user_id: ID of the user to notify
        subject: Notification subject
        body: Notification body
        notification_type: Type of notification
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from core.database.config import get_db_session
        from core.models.notification import Notification
        
        with get_db_session() as session:
            notification = Notification(
                user_id=user_id,
                subject=subject,
                body=body,
                notification_type=notification_type,
                created_at=datetime.utcnow(),
                is_read=False
            )
            
            session.add(notification)
            session.commit()
            
            return True
    
    except Exception as e:
        logger.error(f"Error sending in-app notification: {str(e)}")
        return False

def send_email_notification(to_email, subject, body):
    """
    Send an email notification.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body (HTML)
        
    Returns:
        bool: True if successful, False otherwise
    """
    config = load_notification_config()
    email_config = config.get("channels", {}).get("email", {})
    
    if not email_config.get("enabled", False):
        logger.warning("Email notifications are disabled")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = email_config.get("from_email", "noreply@example.com")
        msg["To"] = to_email
        
        # Attach HTML content
        msg.attach(MIMEText(body, "html"))
        
        # Send email
        with smtplib.SMTP(
            email_config.get("smtp_server"),
            email_config.get("smtp_port", 587)
        ) as server:
            if email_config.get("smtp_use_tls", True):
                server.starttls()
            
            if email_config.get("smtp_username") and email_config.get("smtp_password"):
                server.login(
                    email_config.get("smtp_username"),
                    email_config.get("smtp_password")
                )
            
            server.send_message(msg)
        
        return True
    
    except Exception as e:
        logger.error(f"Error sending email notification: {str(e)}")
        return False

def send_sms_notification(to_phone, message):
    """
    Send an SMS notification using Twilio.
    
    Args:
        to_phone: Recipient phone number
        message: SMS message
        
    Returns:
        bool: True if successful, False otherwise
    """
    config = load_notification_config()
    sms_config = config.get("channels", {}).get("sms", {})
    
    if not sms_config.get("enabled", False):
        logger.warning("SMS notifications are disabled")
        return False
    
    # Get Twilio credentials
    account_sid = sms_config.get("twilio_account_sid") or os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = sms_config.get("twilio_auth_token") or os.environ.get("TWILIO_AUTH_TOKEN")
    from_phone = sms_config.get("twilio_phone_number") or os.environ.get("TWILIO_PHONE_NUMBER")
    
    if not all([account_sid, auth_token, from_phone]):
        logger.error("Missing Twilio credentials")
        return False
    
    try:
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Send SMS
        message = client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone
        )
        
        logger.info(f"SMS sent with SID: {message.sid}")
        return True
    
    except Exception as e:
        logger.error(f"Error sending SMS notification: {str(e)}")
        return False

def send_notification(
    user_id, 
    template_name, 
    context=None, 
    notification_type=NotificationType.INFO,
    channels=None
):
    """
    Send a notification to a user through configured channels.
    
    Args:
        user_id: ID of the user to notify
        template_name: Name of the notification template
        context: Dict of variables to substitute in the template
        notification_type: Type of notification
        channels: List of channels to use (defaults to configured channels for the notification type)
        
    Returns:
        dict: Results by channel
    """
    if context is None:
        context = {}
    
    config = load_notification_config()
    
    # Get user
    try:
        from core.database.config import get_db_session
        from core.models.user import User
        
        with get_db_session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                logger.error(f"User not found: {user_id}")
                return {channel: False for channel in ["in_app", "email", "sms"]}
    
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        return {channel: False for channel in ["in_app", "email", "sms"]}
    
    # Get template
    template = get_template(template_name)
    formatted = format_template(template, context)
    
    # Determine channels to use
    if channels is None:
        channels = config.get("notification_levels", {}).get(notification_type, ["in_app"])
    
    # Check user preferences
    user_preferences = config.get("user_preferences", {}).get(str(user_id), config.get("user_preferences", {}).get("default", {}))
    
    # Send notifications
    results = {}
    
    def send_notifications_async():
        if "in_app" in channels and user_preferences.get("in_app", True):
            results["in_app"] = send_in_app_notification(
                user_id,
                formatted["subject"],
                formatted["body"],
                notification_type
            )
        
        if "email" in channels and user_preferences.get("email", True) and user.email:
            results["email"] = send_email_notification(
                user.email,
                formatted["subject"],
                formatted["body"]
            )
        
        if "sms" in channels and user_preferences.get("sms", False) and user.phone_number:
            # Truncate message for SMS (160 chars)
            sms_message = formatted["subject"] + ": " + formatted["body"]
            if len(sms_message) > 160:
                sms_message = sms_message[:157] + "..."
                
            results["sms"] = send_sms_notification(
                user.phone_number,
                sms_message
            )
    
    # Run notifications in a separate thread to not block the main thread
    thread = threading.Thread(target=send_notifications_async)
    thread.daemon = True
    thread.start()
    
    return results

def mark_notification_read(notification_id):
    """
    Mark an in-app notification as read.
    
    Args:
        notification_id: ID of the notification
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from core.database.config import get_db_session
        from core.models.notification import Notification
        
        with get_db_session() as session:
            notification = session.query(Notification).filter(Notification.id == notification_id).first()
            
            if notification:
                notification.is_read = True
                notification.read_at = datetime.utcnow()
                session.commit()
                return True
            
            return False
    
    except Exception as e:
        logger.error(f"Error marking notification as read: {str(e)}")
        return False

def get_unread_notifications(user_id):
    """
    Get unread in-app notifications for a user.
    
    Args:
        user_id: ID of the user
        
    Returns:
        list: Unread notifications
    """
    try:
        from core.database.config import get_db_session
        from core.models.notification import Notification
        
        with get_db_session() as session:
            notifications = session.query(Notification).\
                filter(Notification.user_id == user_id, Notification.is_read == False).\
                order_by(Notification.created_at.desc()).\
                all()
            
            return [n.to_dict() for n in notifications]
    
    except Exception as e:
        logger.error(f"Error getting unread notifications: {str(e)}")
        return []

def get_recent_notifications(user_id, limit=10):
    """
    Get recent notifications for a user.
    
    Args:
        user_id: ID of the user
        limit: Maximum number of notifications to return
        
    Returns:
        list: Recent notifications
    """
    try:
        from core.database.config import get_db_session
        from core.models.notification import Notification
        
        with get_db_session() as session:
            notifications = session.query(Notification).\
                filter(Notification.user_id == user_id).\
                order_by(Notification.created_at.desc()).\
                limit(limit).\
                all()
            
            return [n.to_dict() for n in notifications]
    
    except Exception as e:
        logger.error(f"Error getting recent notifications: {str(e)}")
        return []

def initialize_notification_system():
    """Initialize the notification system."""
    ensure_dirs_exist()
    load_notification_config()
    
    # Create notification model if it doesn't exist
    try:
        from core.models.notification import Notification
        logger.info("Notification model initialized")
    except ImportError:
        logger.warning("Notification model not available")
    
    # Create default templates
    create_default_templates()

# Convenience functions for specific modules
def send_delivery_notification(user_id, delivery_data):
    """
    Send a notification for a delivery.
    
    Args:
        user_id: ID of the user to notify
        delivery_data: Dict containing delivery information
        
    Returns:
        dict: Results by channel
    """
    context = {
        "delivery_id": delivery_data.get("id", ""),
        "delivery_name": delivery_data.get("name", "Unknown Delivery"),
        "delivery_date": delivery_data.get("date", ""),
        "supplier": delivery_data.get("supplier", ""),
        "location": delivery_data.get("location", "")
    }
    
    return send_notification(
        user_id=user_id,
        template_name="delivery_notification",
        context=context,
        notification_type=NotificationType.INFO,
        channels=["in_app", "email"]
    )

def create_default_templates():
    """Create default notification templates."""
    templates = {
        "welcome": {
            "subject": "Welcome to gcPanel!",
            "body": "Hello {first_name},<br><br>Welcome to gcPanel, your comprehensive construction management platform. We're excited to have you on board!<br><br>The gcPanel Team"
        },
        "password_reset": {
            "subject": "Password Reset Request",
            "body": "Hello {first_name},<br><br>You have requested a password reset. Please use the following link to reset your password:<br><br>{reset_link}<br><br>If you did not request this reset, please ignore this email.<br><br>The gcPanel Team"
        },
        "document_approved": {
            "subject": "Document Approved: {document_name}",
            "body": "Hello {first_name},<br><br>The document '{document_name}' has been approved by {approver_name}.<br><br>You can view the document here: {document_link}<br><br>The gcPanel Team"
        },
        "rfi_response": {
            "subject": "RFI Response: {rfi_number}",
            "body": "Hello {first_name},<br><br>A response has been provided for RFI #{rfi_number}: {rfi_subject}.<br><br>Response: {response_text}<br><br>You can view the RFI here: {rfi_link}<br><br>The gcPanel Team"
        },
        "schedule_update": {
            "subject": "Schedule Update: {project_name}",
            "body": "Hello {first_name},<br><br>The schedule for project '{project_name}' has been updated.<br><br>Key changes:<br>{changes}<br><br>You can view the updated schedule here: {schedule_link}<br><br>The gcPanel Team"
        }
    }
    
    ensure_dirs_exist()
    
    for name, template in templates.items():
        template_file = os.path.join(NOTIFICATION_TEMPLATES_DIR, f"{name}.json")
        
        if not os.path.exists(template_file):
            with open(template_file, 'w') as f:
                json.dump(template, f, indent=2)