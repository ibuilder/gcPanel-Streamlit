"""
Database configuration for gcPanel.

This module provides database connection and session management.
"""

import os
import logging
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

# Setup logging
logger = logging.getLogger(__name__)

# Base class for all models
Base = declarative_base()

# Global session factory
Session = None
engine = None

def init_db():
    """Initialize database connection."""
    global Session, engine
    
    # Get database URL from environment
    database_url = os.environ.get("DATABASE_URL", "")
    
    if not database_url:
        # Fallback to SQLite
        db_path = os.environ.get("DB_PATH", "data/gcpanel.db")
        database_url = f"sqlite:///{db_path}"
        
        # Ensure directory exists for SQLite
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        if database_url.startswith("postgresql"):
            logger.info("Connecting to PostgreSQL database")
            
            # Connect to PostgreSQL
            engine = sa.create_engine(
                database_url,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=1800,
                echo=False
            )
        else:
            logger.info("Connecting to SQLite database")
            
            # Connect to SQLite
            engine = sa.create_engine(
                database_url,
                connect_args={"check_same_thread": False},
                echo=False
            )
        
        # Create session factory
        Session = scoped_session(sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        ))
        
        # Initialize models
        from core.models import initialize_models
        initialize_models()
        
        # Test connection
        engine.connect()
        logger.info("Database connection successful")
        
        return True
    
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        return False

def create_tables():
    """Create all tables that don't exist yet."""
    if engine is None:
        init_db()
    
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")

@contextmanager
def get_db_session():
    """Get a database session."""
    if Session is None:
        init_db()
    
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_engine():
    """Get SQLAlchemy engine."""
    if engine is None:
        init_db()
    
    return engine