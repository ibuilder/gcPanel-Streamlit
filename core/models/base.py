"""
Base model for database models.

This module provides a base class for all SQLAlchemy models.
"""

import datetime
import uuid
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from core.database.config import Base

class BaseModel(Base):
    """Base model with common attributes."""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        """
        Convert model to dictionary.
        
        Returns:
            dict: Dictionary representation of model
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}