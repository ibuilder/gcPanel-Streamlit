"""
Database models for gcPanel.

This module initializes the database models for the application.
"""

import logging

# Setup logging
logger = logging.getLogger(__name__)

def initialize_models():
    """Initialize database models."""
    # Import models to register them with SQLAlchemy
    try:
        from core.models.base import BaseModel
        from core.models.user import User, Role, UserProfile, UserStatus
        from core.models.notification import Notification
        
        logger.info("Database models initialized")
    except Exception as e:
        logger.error(f"Error initializing models: {str(e)}")