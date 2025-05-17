"""
Core package initialization.

This module initializes the core application package.
"""

import logging

# Set up root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s"
)

# Initialize package
from core.database.config import init_db, create_tables
from core.auth.auth_service import initialize_auth

def initialize_application():
    """
    Initialize the application.
    
    This function sets up the database connection, creates tables,
    and initializes the authentication system.
    
    Returns:
        bool: True if initialization was successful, False otherwise
    """
    # Initialize database
    if not init_db():
        logging.error("Database initialization failed")
        return False
        
    # Create tables
    if not create_tables():
        logging.error("Database table creation failed")
        return False
    
    # Initialize authentication
    try:
        initialize_auth()
        logging.info("Authentication initialized successfully")
    except Exception as e:
        logging.error(f"Authentication initialization failed: {str(e)}")
        return False
    
    logging.info("Database initialized successfully")
    return True