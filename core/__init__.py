"""
Core module initialization for gcPanel.

This module initializes core services for the application.
"""

import logging
import os
from datetime import datetime

# Setup logging
logger = logging.getLogger(__name__)

def initialize_application():
    """Initialize core application services."""
    logger.info("Initializing core application services")
    
    # Initialize database
    try:
        from core.database.config import init_db
        init_db()
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
    
    # Initialize notification system
    try:
        from utils.notifications import initialize_notification_system
        initialize_notification_system()
    except Exception as e:
        logger.error(f"Notification system initialization failed: {str(e)}")
    
    # Initialize CDN if available
    try:
        from utils.cdn_manager import initialize_cdn
        initialize_cdn()
    except Exception as e:
        logger.error(f"CDN initialization failed: {str(e)}")
    
    # Initialize documentation system if available
    try:
        from utils.documentation import initialize_documentation
        initialize_documentation()
    except Exception as e:
        logger.error(f"Documentation system initialization failed: {str(e)}")
    
    # Log application startup
    logger.info(f"Application initialized at {datetime.now().isoformat()}")