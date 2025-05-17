"""
User repository for user-specific database operations.

This module provides specialized repository methods for user management
beyond the basic CRUD operations.
"""

import logging
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from core.database.repository import Repository
from core.models.user import User, Role
from core.database.config import get_db_session

# Set up logging
logger = logging.getLogger(__name__)

class UserRepository(Repository[User]):
    """
    User repository with specialized methods for user management.
    
    This class extends the base Repository with methods specific to User entities.
    """
    
    def __init__(self):
        """Initialize with User model"""
        super().__init__(User)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Get a user by username.
        
        Args:
            username: Username to search for
            
        Returns:
            User instance or None if not found
        """
        try:
            with get_db_session() as db:
                return db.query(User) \
                    .filter(User.username == username, User.is_active == True) \
                    .first()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_by_username: {str(e)}")
            return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email address.
        
        Args:
            email: Email address to search for
            
        Returns:
            User instance or None if not found
        """
        try:
            with get_db_session() as db:
                return db.query(User) \
                    .filter(User.email == email, User.is_active == True) \
                    .first()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_by_email: {str(e)}")
            return None
    
    def get_users_by_role(self, role_name: str) -> List[User]:
        """
        Get all users with a specific role.
        
        Args:
            role_name: Role name to filter by
            
        Returns:
            List of users with the specified role
        """
        try:
            with get_db_session() as db:
                return db.query(User) \
                    .join(User.roles) \
                    .filter(Role.name == role_name, User.is_active == True) \
                    .all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_users_by_role: {str(e)}")
            return []
    
    def add_role_to_user(self, user_id: int, role_name: str) -> bool:
        """
        Add a role to a user.
        
        Args:
            user_id: User ID
            role_name: Role name to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with get_db_session() as db:
                user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
                role = db.query(Role).filter(Role.name == role_name).first()
                
                if not user or not role:
                    return False
                    
                # Check if user already has this role
                if role not in user.roles:
                    user.roles.append(role)
                    db.commit()
                    
                return True
        except SQLAlchemyError as e:
            logger.error(f"Database error in add_role_to_user: {str(e)}")
            return False
    
    def remove_role_from_user(self, user_id: int, role_name: str) -> bool:
        """
        Remove a role from a user.
        
        Args:
            user_id: User ID
            role_name: Role name to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with get_db_session() as db:
                user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
                role = db.query(Role).filter(Role.name == role_name).first()
                
                if not user or not role:
                    return False
                    
                # Check if user has this role
                if role in user.roles:
                    user.roles.remove(role)
                    db.commit()
                    
                return True
        except SQLAlchemyError as e:
            logger.error(f"Database error in remove_role_from_user: {str(e)}")
            return False
    
    def change_password(self, user_id: int, new_password_hash: str) -> bool:
        """
        Update a user's password.
        
        Args:
            user_id: User ID
            new_password_hash: New hashed password
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with get_db_session() as db:
                user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
                
                if not user:
                    return False
                    
                user.password_hash = new_password_hash
                db.commit()
                return True
        except SQLAlchemyError as e:
            logger.error(f"Database error in change_password: {str(e)}")
            return False
    
    def deactivate_user(self, user_id: int) -> bool:
        """
        Deactivate a user (soft delete).
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        return self.delete(user_id)
    
    def reactivate_user(self, user_id: int) -> bool:
        """
        Reactivate a deactivated user.
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with get_db_session() as db:
                # Get user including inactive ones
                user = db.query(User).filter(User.id == user_id).first()
                
                if not user:
                    return False
                    
                user.is_active = True
                db.commit()
                return True
        except SQLAlchemyError as e:
            logger.error(f"Database error in reactivate_user: {str(e)}")
            return False