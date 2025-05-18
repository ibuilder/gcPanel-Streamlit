"""
User models for gcPanel.

This module provides database models for user authentication and roles.
"""

import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from core.models.base import BaseModel
from core.database.config import Base

# Define the association table for user-role many-to-many relationship
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True)
)

class UserStatus(enum.Enum):
    """User status enum."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"

class User(BaseModel):
    """User model for authentication and user information."""
    
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    failed_login_attempts = Column(Integer, default=0)
    
    # Relationships
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    notifications = relationship("Notification", back_populates="user")
    
    @hybrid_property
    def full_name(self):
        """Get the user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.username
    
    def has_role(self, role_name):
        """
        Check if the user has a specific role.
        
        Args:
            role_name: The name of the role to check
            
        Returns:
            bool: True if user has the role, False otherwise
        """
        return any(role.name == role_name for role in self.roles)
    
    def to_dict(self, include_password=False):
        """
        Convert user to dictionary.
        
        Args:
            include_password: Whether to include password hash in result
            
        Returns:
            dict: Dictionary representation of user
        """
        user_dict = super().to_dict()
        
        # Add computed properties
        user_dict["full_name"] = self.full_name
        
        # Add roles
        user_dict["roles"] = [role.name for role in self.roles]
        
        # Remove password hash unless explicitly requested
        if not include_password and "password_hash" in user_dict:
            del user_dict["password_hash"]
        
        return user_dict

class Role(BaseModel):
    """Role model for user permissions."""
    
    __tablename__ = "roles"
    
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    
    # Relationships
    users = relationship("User", secondary=user_roles, back_populates="roles")
    
    def to_dict(self):
        """
        Convert role to dictionary.
        
        Returns:
            dict: Dictionary representation of role
        """
        return super().to_dict()

class UserProfile(BaseModel):
    """User profile model for additional user information."""
    
    __tablename__ = "user_profiles"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    timezone = Column(String(50), default="UTC")
    avatar = Column(String(255), nullable=True)
    bio = Column(String(500), nullable=True)
    company = Column(String(100), nullable=True)
    job_title = Column(String(100), nullable=True)
    
    # Notification preferences
    email_notifications = Column(Boolean, default=True)
    sms_notifications = Column(Boolean, default=False)
    
    # UI preferences
    theme = Column(String(20), default="light")
    sidebar_collapsed = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", backref="profile")
    
    def to_dict(self):
        """
        Convert profile to dictionary.
        
        Returns:
            dict: Dictionary representation of profile
        """
        return super().to_dict()