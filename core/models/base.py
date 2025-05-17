"""
Base model for SQLAlchemy models.

This module defines a base model class that all other models will inherit from,
providing common fields and functionality.
"""

import datetime
from sqlalchemy import Column, Integer, Boolean, DateTime
from sqlalchemy.ext.declarative import declared_attr
from core.database.config import Base

class BaseModel(Base):
    """
    Base model class for all entities.
    
    This abstract base class provides common fields and functionality that
    all model classes should inherit.
    
    Attributes:
        id (int): Primary key
        created_at (datetime): Record creation timestamp
        updated_at (datetime): Record last update timestamp
        is_active (bool): Soft deletion flag
    """
    
    # Make this class abstract
    __abstract__ = True
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)
    
    # Soft deletion flag
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Common methods
    @declared_attr
    def __tablename__(cls):
        """
        Generate table name automatically based on class name.
        
        This converts CamelCase class names to snake_case table names.
        """
        name = cls.__name__
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')
    
    def to_dict(self):
        """
        Convert model to dictionary.
        
        Returns:
            Dictionary representation of model
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self):
        """String representation of model"""
        return f"<{self.__class__.__name__} id={self.id}>"