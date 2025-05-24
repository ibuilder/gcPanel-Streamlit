"""
Notification Manager for Highland Tower Development

Handles real-time notifications, alerts, and communication across the platform.
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

class NotificationManager:
    """Manages notifications and alerts for the Highland Tower Development dashboard."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.notification_types = {
            "info": "ℹ️",
            "warning": "⚠️", 
            "error": "❌",
            "success": "✅",
            "urgent": "🚨"
        }
    
    def initialize(self):
        """Initialize notification system."""
        if "notifications" not in st.session_state:
            st.session_state.notifications = []
        
        if "notification_preferences" not in st.session_state:
            st.session_state.notification_preferences = {
                "email_enabled": True,
                "browser_enabled": True,
                "mobile_enabled": True,
                "sound_enabled": False
            }
    
    def add_notification(self, title: str, message: str, notification_type: str = "info", 
                        module: str = "System", urgent: bool = False):
        """Add a new notification."""
        notification = {
            "id": f"notif_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            "title": title,
            "message": message,
            "type": notification_type,
            "module": module,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "read": False,
            "urgent": urgent,
            "icon": self.notification_types.get(notification_type, "📢")
        }
        
        st.session_state.notifications.insert(0, notification)
        
        # Keep only last 50 notifications
        st.session_state.notifications = st.session_state.notifications[:50]
        
        self.logger.info(f"Notification added: {title}")
    
    def get_notifications(self, unread_only: bool = False) -> List[Dict[str, Any]]:
        """Get notifications, optionally filtering for unread only."""
        notifications = st.session_state.get("notifications", [])
        
        if unread_only:
            return [n for n in notifications if not n["read"]]
        
        return notifications
    
    def mark_as_read(self, notification_id: str):
        """Mark notification as read."""
        notifications = st.session_state.get("notifications", [])
        
        for notification in notifications:
            if notification["id"] == notification_id:
                notification["read"] = True
                break
    
    def get_unread_count(self) -> int:
        """Get count of unread notifications."""
        return len(self.get_notifications(unread_only=True))
    
    def clear_old_notifications(self, days: int = 7):
        """Clear notifications older than specified days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        notifications = st.session_state.get("notifications", [])
        
        filtered_notifications = []
        for notification in notifications:
            notification_date = datetime.strptime(notification["timestamp"], "%Y-%m-%d %H:%M:%S")
            if notification_date > cutoff_date:
                filtered_notifications.append(notification)
        
        st.session_state.notifications = filtered_notifications
    
    def create_rfi_notification(self, rfi_id: str, action: str):
        """Create RFI-specific notification."""
        messages = {
            "created": f"New RFI {rfi_id} has been created",
            "updated": f"RFI {rfi_id} has been updated", 
            "responded": f"Response received for RFI {rfi_id}",
            "closed": f"RFI {rfi_id} has been closed"
        }
        
        self.add_notification(
            title=f"RFI {action.title()}",
            message=messages.get(action, f"RFI {rfi_id} status changed"),
            notification_type="info",
            module="RFIs"
        )
    
    def create_submittal_notification(self, submittal_id: str, action: str):
        """Create submittal-specific notification."""
        messages = {
            "submitted": f"Submittal {submittal_id} has been submitted",
            "reviewed": f"Submittal {submittal_id} review completed",
            "approved": f"Submittal {submittal_id} has been approved",
            "rejected": f"Submittal {submittal_id} has been rejected"
        }
        
        notification_type = "success" if action == "approved" else "warning" if action == "rejected" else "info"
        
        self.add_notification(
            title=f"Submittal {action.title()}",
            message=messages.get(action, f"Submittal {submittal_id} status changed"),
            notification_type=notification_type,
            module="Submittals"
        )
    
    def create_safety_notification(self, message: str, urgent: bool = False):
        """Create safety-related notification."""
        self.add_notification(
            title="Safety Alert",
            message=message,
            notification_type="urgent" if urgent else "warning",
            module="Safety",
            urgent=urgent
        )
    
    def create_schedule_notification(self, message: str):
        """Create schedule-related notification."""
        self.add_notification(
            title="Schedule Update",
            message=message,
            notification_type="info",
            module="Schedule"
        )