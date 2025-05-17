"""
Base model for all database models in gcPanel.

This module defines the Base model class with common fields and methods
that all database models will inherit from.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, Boolean
from sqlalchemy.ext.declarative import declared_attr
from core.database.config import Base

class BaseModel(Base):
    """
    Base model class that all database models will inherit from.
    
    This abstract class provides common fields and functionality for all models:
    - id: Primary key
    - created_at: Creation timestamp
    - updated_at: Last update timestamp
    - created_by: User who created the record
    - is_active: Soft deletion flag
    """
    
    # Make class abstract (won't create a table)
    __abstract__ = True
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String, nullable=True)
    
    # Soft deletion
    is_active = Column(Boolean, default=True, nullable=False)
    
    @declared_attr
    def __tablename__(cls):
        """
        Automatically generate table name from class name.
        
        Table names will be snake_case versions of the class name.
        Example: UserProfile -> user_profile
        """
        from re import sub
        # Convert CamelCase to snake_case
        name = sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        return name
    
    def to_dict(self):
        """
        Convert model instance to dictionary.
        
        Returns:
            dict: Model data as dictionary
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def from_dict(cls, data):
        """
        Create model instance from dictionary.
        
        Args:
            data (dict): Data to create model from
            
        Returns:
            BaseModel: New model instance
        """
        return cls(**{k: v for k, v in data.items() if k in cls.__table__.columns.keys()})