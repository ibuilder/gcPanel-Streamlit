"""
Repository pattern implementation for data access operations.

This module provides a base repository class that can be extended
for different entity types to handle database operations.
"""

import logging
from typing import List, Optional, TypeVar, Generic, Type, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.models.base import BaseModel
from core.database.config import get_db_session

# Set up logging
logger = logging.getLogger(__name__)

# Generic type for models
T = TypeVar('T', bound=BaseModel)

class Repository(Generic[T]):
    """
    Generic repository for database operations on models.
    
    This base class provides CRUD operations for any model type
    that inherits from BaseModel.
    
    Attributes:
        model_class: The SQLAlchemy model class this repository works with
    """
    
    def __init__(self, model_class: Type[T]):
        """
        Initialize repository with model class.
        
        Args:
            model_class: SQLAlchemy model class
        """
        self.model_class = model_class
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get all active records of model type with pagination.
        
        Args:
            skip: Number of records to skip (offset)
            limit: Maximum number of records to return
            
        Returns:
            List of model instances
        """
        try:
            with get_db_session() as db:
                return db.query(self.model_class) \
                    .filter(self.model_class.is_active == True) \
                    .order_by(self.model_class.id) \
                    .offset(skip) \
                    .limit(limit) \
                    .all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_all for {self.model_class.__name__}: {str(e)}")
            return []
    
    def get_by_id(self, id: int) -> Optional[T]:
        """
        Get a single record by ID.
        
        Args:
            id: Primary key value
            
        Returns:
            Model instance or None if not found
        """
        try:
            with get_db_session() as db:
                return db.query(self.model_class) \
                    .filter(self.model_class.id == id, self.model_class.is_active == True) \
                    .first()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_by_id for {self.model_class.__name__}: {str(e)}")
            return None
    
    def create(self, data: Dict[str, Any]) -> Optional[T]:
        """
        Create a new record.
        
        Args:
            data: Dictionary with model field values
            
        Returns:
            Created model instance or None if failed
        """
        try:
            with get_db_session() as db:
                obj = self.model_class(**data)
                db.add(obj)
                db.commit()
                db.refresh(obj)
                return obj
        except SQLAlchemyError as e:
            logger.error(f"Database error in create for {self.model_class.__name__}: {str(e)}")
            return None
    
    def update(self, id: int, data: Dict[str, Any]) -> Optional[T]:
        """
        Update an existing record.
        
        Args:
            id: Primary key value
            data: Dictionary with field values to update
            
        Returns:
            Updated model instance or None if failed
        """
        try:
            with get_db_session() as db:
                obj = db.query(self.model_class) \
                    .filter(self.model_class.id == id, self.model_class.is_active == True) \
                    .first()
                
                if not obj:
                    return None
                
                # Update fields
                for key, value in data.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                
                db.commit()
                db.refresh(obj)
                return obj
        except SQLAlchemyError as e:
            logger.error(f"Database error in update for {self.model_class.__name__}: {str(e)}")
            return None
    
    def delete(self, id: int) -> bool:
        """
        Soft delete a record by setting is_active to False.
        
        Args:
            id: Primary key value
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with get_db_session() as db:
                obj = db.query(self.model_class) \
                    .filter(self.model_class.id == id, self.model_class.is_active == True) \
                    .first()
                
                if not obj:
                    return False
                
                # Soft delete
                obj.is_active = False
                db.commit()
                return True
        except SQLAlchemyError as e:
            logger.error(f"Database error in delete for {self.model_class.__name__}: {str(e)}")
            return False
    
    def hard_delete(self, id: int) -> bool:
        """
        Permanently delete a record from database.
        
        Args:
            id: Primary key value
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with get_db_session() as db:
                obj = db.query(self.model_class) \
                    .filter(self.model_class.id == id) \
                    .first()
                
                if not obj:
                    return False
                
                # Hard delete
                db.delete(obj)
                db.commit()
                return True
        except SQLAlchemyError as e:
            logger.error(f"Database error in hard_delete for {self.model_class.__name__}: {str(e)}")
            return False
    
    def count(self) -> int:
        """
        Count active records of model type.
        
        Returns:
            Number of active records
        """
        try:
            with get_db_session() as db:
                return db.query(self.model_class) \
                    .filter(self.model_class.is_active == True) \
                    .count()
        except SQLAlchemyError as e:
            logger.error(f"Database error in count for {self.model_class.__name__}: {str(e)}")
            return 0
    
    def exists(self, id: int) -> bool:
        """
        Check if record exists by ID.
        
        Args:
            id: Primary key value
            
        Returns:
            True if record exists, False otherwise
        """
        try:
            with get_db_session() as db:
                return db.query(db.query(self.model_class).filter(
                    self.model_class.id == id,
                    self.model_class.is_active == True
                ).exists()).scalar()
        except SQLAlchemyError as e:
            logger.error(f"Database error in exists for {self.model_class.__name__}: {str(e)}")
            return False