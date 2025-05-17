"""
Database configuration module for gcPanel.

This module handles database connection setup and provides session management
for SQLAlchemy ORM.
"""

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Set up logging
logger = logging.getLogger(__name__)

# Create SQLAlchemy Base for models
Base = declarative_base()

# Database connection information
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///data/gcpanel.db')

def get_engine():
    """
    Create and return a SQLAlchemy engine instance.
    
    Returns:
        SQLAlchemy Engine: Configured engine for database operations
    """
    try:
        # Create engine with appropriate configuration
        engine = create_engine(
            DATABASE_URL,
            echo=False,  # Set to True for SQL query logging (development only)
            connect_args={"check_same_thread": False} if DATABASE_URL.startswith('sqlite') else {},
            pool_pre_ping=True,  # Check connection health before usage
            pool_recycle=3600,   # Recycle connections after 1 hour
        )
        logger.info(f"Database engine created for {DATABASE_URL.split('://')[0]}")
        return engine
    except Exception as e:
        logger.error(f"Error creating database engine: {str(e)}")
        raise

# Create global engine and session factory
engine = get_engine()
session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
SessionLocal = scoped_session(session_factory)

def get_db_session():
    """
    Create a new database session for use in application context.
    
    Returns:
        SQLAlchemy Session: Database session for ORM operations
    
    Usage:
        with get_db_session() as session:
            results = session.query(Model).all()
    """
    session = SessionLocal()
    try:
        return session
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        session.close()

def init_database():
    """
    Initialize the database by creating all tables defined in models.
    
    This function should be called during application startup after
    all models have been imported and registered.
    """
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database tables: {str(e)}")
        raise