"""
Database configuration module.

This module handles database connection and session management.
"""

import os
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Setup logging
logger = logging.getLogger(__name__)

# Create declarative base for models
Base = declarative_base()

# Database configuration
DB_PATH = os.environ.get("DB_PATH", "data/gcpanel.db")
SQLITE_URL = f"sqlite:///{DB_PATH}"

# Create engine and session factory
engine = None
Session = None

def init_db():
    """
    Initialize database connection and session factory.
    
    This function should be called at application startup.
    """
    global engine, Session
    
    try:
        # Ensure data directory exists
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        # Create engine with SQLite connection
        logger.info(f"Connecting to local SQLite database: {DB_PATH}")
        engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
        
        # Create session factory
        Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        
        # Test connection
        with get_db_session() as db:
            db.execute(text("SELECT 1"))
            logger.info("SQLite database connection successful")
            
        return True
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        return False

@contextmanager
def get_db_session():
    """
    Get a database session using context manager.
    
    Usage:
        with get_db_session() as db:
            result = db.query(Model).all()
            
    Returns:
        SQLAlchemy session
    """
    if Session is None:
        init_db()
        
    session = Session()
    try:
        yield session
    except Exception as e:
        logger.error(f"Session error: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

def create_tables():
    """
    Create all database tables defined in models.
    
    This function should be called after all models are imported.
    """
    try:
        # Import all models to ensure they're registered with Base
        from core.models import base
        from core.models import user
        from core.models import project
        from core.models import engineering
        from core.models import config
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        return False

def drop_tables():
    """
    Drop all database tables.
    
    WARNING: This will delete all data! Use with caution.
    """
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
        return True
    except Exception as e:
        logger.error(f"Error dropping database tables: {str(e)}")
        return False