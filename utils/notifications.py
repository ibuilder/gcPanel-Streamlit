"""
Notification utilities for gcPanel Construction Management Dashboard.

This module provides notification capabilities for the application, including
email and SMS notifications for delivery status updates and other important events.
"""

import os
from datetime import datetime
from enum import Enum
import logging
import json

# Setup logging
logger = logging.getLogger(__name__)

class NotificationType(Enum):
    """Types of notifications that can be sent"""
    DELIVERY_SCHEDULED = "delivery_scheduled"
    DELIVERY_CONFIRMED = "delivery_confirmed"
    DELIVERY_DELAYED = "delivery_delayed"
    DELIVERY_CANCELED = "delivery_canceled"
    DELIVERY_ARRIVED = "delivery_arrived"
    DELIVERY_INCOMPLETE = "delivery_incomplete"
    DELIVERY_REMINDER = "delivery_reminder"
    GENERAL_ANNOUNCEMENT = "general_announcement"

class NotificationPriority(Enum):
    """Notification priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

class NotificationMethod(Enum):
    """Methods for sending notifications"""
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"
    ALL = "all"

def send_notification(
    recipient, 
    subject, 
    message, 
    notification_type=NotificationType.GENERAL_ANNOUNCEMENT,
    priority=NotificationPriority.NORMAL,
    method=NotificationMethod.IN_APP,
    metadata=None
):
    """
    Send a notification to the specified recipient
    
    Args:
        recipient (str or list): Email address, phone number, or user ID
        subject (str): Notification subject
        message (str): Notification content
        notification_type (NotificationType): Type of notification
        priority (NotificationPriority): Priority level
        method (NotificationMethod): Delivery method
        metadata (dict): Additional data to include with the notification
        
    Returns:
        bool: True if notification was sent successfully
    """
    try:
        # Create notification record
        notification_record = {
            "recipient": recipient,
            "subject": subject,
            "message": message,
            "type": notification_type.value,
            "priority": priority.value,
            "method": method.value,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "status": "pending"
        }
        
        # Log the notification for auditing purposes
        logger.info(f"Sending notification: {json.dumps(notification_record)}")
        
        # In-app notifications are always stored
        if method in [NotificationMethod.IN_APP, NotificationMethod.ALL]:
            store_in_app_notification(notification_record)
        
        # Send via the appropriate channel(s)
        if method in [NotificationMethod.EMAIL, NotificationMethod.ALL]:
            success = send_email_notification(notification_record)
        
        if method in [NotificationMethod.SMS, NotificationMethod.ALL]:
            success = send_sms_notification(notification_record)
        
        # Update notification status
        notification_record["status"] = "sent" if success else "failed"
        
        return success
        
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")
        return False

def store_in_app_notification(notification):
    """
    Store an in-app notification for later retrieval
    
    Args:
        notification (dict): Notification data to store
        
    Returns:
        bool: True if notification was stored successfully
    """
    try:
        # In a production environment, this would store to a database
        # For now, we'll just store to a file to simulate the functionality
        
        # Create notifications directory if it doesn't exist
        os.makedirs("data/notifications", exist_ok=True)
        
        # Write to a notification log file
        recipient_id = notification["recipient"]
        if isinstance(recipient_id, list):
            recipient_id = "_".join(recipient_id)
        
        notification_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{recipient_id}"
        
        with open(f"data/notifications/{notification_id}.json", "w") as f:
            json.dump(notification, f)
        
        return True
        
    except Exception as e:
        logger.error(f"Error storing in-app notification: {str(e)}")
        return False

def send_email_notification(notification):
    """
    Send an email notification
    
    In a production environment, this would use a real email service.
    For now, we'll just simulate the functionality.
    
    Args:
        notification (dict): Notification data to send
        
    Returns:
        bool: True if notification was sent successfully
    """
    try:
        recipient = notification["recipient"]
        subject = notification["subject"]
        message = notification["message"]
        
        # In a production environment, this would use SMTP or an email service API
        logger.info(f"SIMULATION: Sending email to {recipient} with subject '{subject}'")
        
        # Simulated success
        return True
        
    except Exception as e:
        logger.error(f"Error sending email notification: {str(e)}")
        return False

def send_sms_notification(notification):
    """
    Send an SMS notification using Twilio
    
    Args:
        notification (dict): Notification data to send
        
    Returns:
        bool: True if notification was sent successfully
    """
    try:
        from twilio.rest import Client
        
        # Get Twilio credentials from environment
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        from_number = os.environ.get("TWILIO_PHONE_NUMBER")
        
        # Check if Twilio credentials are available
        if not all([account_sid, auth_token, from_number]):
            logger.warning("Twilio credentials not configured. SMS notification not sent.")
            return False
        
        recipient = notification["recipient"]
        message = notification["message"]
        
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Send message
        sms = client.messages.create(
            body=message,
            from_=from_number,
            to=recipient
        )
        
        logger.info(f"SMS sent with SID: {sms.sid}")
        return True
        
    except ImportError:
        logger.error("Twilio package not installed. SMS notification not sent.")
        return False
    except Exception as e:
        logger.error(f"Error sending SMS notification: {str(e)}")
        return False

def get_user_notifications(user_id, limit=10, include_read=False):
    """
    Get notifications for a specific user
    
    Args:
        user_id (str): User ID to retrieve notifications for
        limit (int): Maximum number of notifications to return
        include_read (bool): Whether to include notifications marked as read
        
    Returns:
        list: List of notification objects
    """
    # In a production environment, this would query a database
    # For now, we'll read from notification files to simulate the functionality
    
    try:
        notifications = []
        
        # Create notifications directory if it doesn't exist
        os.makedirs("data/notifications", exist_ok=True)
        
        # Check all notification files
        for filename in os.listdir("data/notifications"):
            if not filename.endswith(".json"):
                continue
                
            filepath = os.path.join("data/notifications", filename)
            
            try:
                with open(filepath, "r") as f:
                    notification = json.load(f)
                    
                recipient = notification.get("recipient")
                
                # Filter by user_id
                if recipient == user_id or (isinstance(recipient, list) and user_id in recipient):
                    # Check read status if needed
                    if include_read or not notification.get("read", False):
                        notifications.append(notification)
            except Exception as e:
                logger.error(f"Error reading notification file {filepath}: {str(e)}")
        
        # Sort by timestamp (newest first) and limit
        notifications.sort(key=lambda n: n.get("timestamp", ""), reverse=True)
        return notifications[:limit]
        
    except Exception as e:
        logger.error(f"Error retrieving notifications: {str(e)}")
        return []

def mark_notification_as_read(notification_id):
    """
    Mark a notification as read
    
    Args:
        notification_id (str): ID of the notification to mark as read
        
    Returns:
        bool: True if notification was marked as read successfully
    """
    try:
        filepath = os.path.join("data/notifications", f"{notification_id}.json")
        
        if not os.path.exists(filepath):
            logger.warning(f"Notification file not found: {filepath}")
            return False
            
        with open(filepath, "r") as f:
            notification = json.load(f)
            
        notification["read"] = True
        
        with open(filepath, "w") as f:
            json.dump(notification, f)
            
        return True
        
    except Exception as e:
        logger.error(f"Error marking notification as read: {str(e)}")
        return False

def send_delivery_notification(
    delivery_data, 
    notification_type, 
    recipients=None, 
    additional_message=None,
    methods=None
):
    """
    Send a notification about a delivery status change
    
    Args:
        delivery_data (dict): Delivery information
        notification_type (NotificationType): Type of notification to send
        recipients (list): List of recipient IDs/contact info (if None, uses default contacts)
        additional_message (str): Additional message to include
        methods (list): List of notification methods to use
        
    Returns:
        bool: True if notification was sent successfully
    """
    # Create a human-readable message based on notification type
    item_name = delivery_data.get("item_name", "Unknown item")
    delivery_date = delivery_data.get("delivery_date", "Unknown date")
    
    # Format date if it's a timestamp object
    if hasattr(delivery_date, "strftime"):
        delivery_date = delivery_date.strftime("%Y-%m-%d")
    
    supplier = delivery_data.get("supplier", "Unknown supplier")
    quantity = delivery_data.get("quantity", "")
    unit = delivery_data.get("unit", "")
    location = delivery_data.get("delivery_location", "the site")
    
    # Create a quantity string if both quantity and unit are present
    quantity_str = f"{quantity} {unit}" if quantity and unit else ""
    
    # Create the base message
    base_message = f"Delivery update for {item_name}"
    if quantity_str:
        base_message += f" ({quantity_str})"
    base_message += f" from {supplier}."
    
    # Add specific message based on notification type
    if notification_type == NotificationType.DELIVERY_SCHEDULED:
        subject = f"Delivery Scheduled: {item_name}"
        message = f"{base_message} Scheduled for delivery on {delivery_date} to {location}."
        priority = NotificationPriority.NORMAL
    
    elif notification_type == NotificationType.DELIVERY_CONFIRMED:
        subject = f"Delivery Confirmed: {item_name}"
        message = f"{base_message} Supplier has confirmed delivery for {delivery_date} to {location}."
        priority = NotificationPriority.NORMAL
    
    elif notification_type == NotificationType.DELIVERY_DELAYED:
        subject = f"Delivery Delayed: {item_name}"
        message = f"{base_message} Delivery has been delayed and will not arrive on {delivery_date} as scheduled."
        priority = NotificationPriority.HIGH
    
    elif notification_type == NotificationType.DELIVERY_CANCELED:
        subject = f"Delivery Canceled: {item_name}"
        message = f"{base_message} Delivery scheduled for {delivery_date} has been canceled."
        priority = NotificationPriority.HIGH
    
    elif notification_type == NotificationType.DELIVERY_ARRIVED:
        subject = f"Delivery Arrived: {item_name}"
        message = f"{base_message} Has arrived at {location}."
        priority = NotificationPriority.NORMAL
    
    elif notification_type == NotificationType.DELIVERY_INCOMPLETE:
        subject = f"Incomplete Delivery: {item_name}"
        message = f"{base_message} Delivered to {location} but is incomplete or damaged."
        priority = NotificationPriority.HIGH
    
    elif notification_type == NotificationType.DELIVERY_REMINDER:
        subject = f"Delivery Reminder: {item_name}"
        message = f"{base_message} Scheduled to arrive tomorrow at {location}."
        priority = NotificationPriority.LOW
    
    else:
        subject = f"Delivery Update: {item_name}"
        message = base_message
        priority = NotificationPriority.NORMAL
    
    # Add any additional message
    if additional_message:
        message += f" {additional_message}"
    
    # Set default recipients if none provided
    if not recipients:
        # In a real app, this would come from user roles in the database
        recipients = ["project_manager", "site_superintendent", "procurement_manager"]
    
    # Set default methods if none provided
    if not methods:
        methods = [NotificationMethod.IN_APP]
    
    # Send notifications by each specified method
    success = True
    for method in methods:
        result = send_notification(
            recipient=recipients,
            subject=subject,
            message=message,
            notification_type=notification_type,
            priority=priority,
            method=method,
            metadata=delivery_data
        )
        success = success and result
    
    return success