"""
Notification model for gcPanel.

This module provides the database model for system notifications.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from core.models.base import BaseModel

class Notification(BaseModel):
    """Notification model for storing user notifications."""
    
    __tablename__ = "notifications"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False, default="info")
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    
    def mark_as_read(self):
        """Mark notification as read."""
        self.is_read = True
        self.read_at = datetime.utcnow()
    
    def to_dict(self):
        """
        Convert notification to dictionary.
        
        Returns:
            dict: Dictionary representation of notification
        """
        notification_dict = super().to_dict()
        
        # Convert datetime objects to ISO format strings
        for key, value in notification_dict.items():
            if isinstance(value, datetime):
                notification_dict[key] = value.isoformat()
        
        return notification_dict