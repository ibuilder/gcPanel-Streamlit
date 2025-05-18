"""
User models for authentication and authorization.

This module defines the User and Role models for authentication and 
role-based access control (RBAC).
"""

import enum
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Table, Enum, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship
from core.models.base import BaseModel
from core.database.config import Base

# Many-to-many relationship between users and roles
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('role.id'), primary_key=True)
)

class UserStatus(enum.Enum):
    """User status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"
    LOCKED = "locked"  # Account locked due to failed login attempts

class User(BaseModel):
    """
    User model for authentication and permissions.
    
    Attributes:
        username (str): Unique username for login
        email (str): User email address
        password_hash (str): Hashed password (not stored in plaintext)
        first_name (str): User's first name
        last_name (str): User's last name
        status (UserStatus): Current user status
        roles (list): User's assigned roles
        mfa_enabled (bool): Whether multi-factor authentication is enabled
        mfa_secret (str): Secret key for MFA (encrypted)
        failed_login_attempts (int): Number of consecutive failed login attempts
        locked_until (datetime): When a locked account will be automatically unlocked
        password_changed_at (datetime): When password was last changed
        last_login (datetime): Last successful login time
        last_active (datetime): Last activity time for session management
    """
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE, nullable=False)
    
    # Security enhancements
    mfa_enabled = Column(Boolean, default=False, nullable=False)
    mfa_secret = Column(String(255), nullable=True)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)
    password_changed_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    last_active = Column(DateTime, nullable=True)
    
    # Relationships
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    
    @property
    def full_name(self):
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.username
    
    def has_role(self, role_name):
        """
        Check if user has a specific role.
        
        Args:
            role_name (str): Role name to check
            
        Returns:
            bool: True if user has role, False otherwise
        """
        return any(role.name == role_name for role in self.roles)
    
    def has_any_role(self, role_names):
        """
        Check if user has any of the specified roles.
        
        Args:
            role_names (list): List of role names to check
            
        Returns:
            bool: True if user has any role, False otherwise
        """
        return any(role.name in role_names for role in self.roles)

class Role(BaseModel):
    """
    Role model for permission management.
    
    Attributes:
        name (str): Unique role name (e.g., 'admin', 'editor')
        description (str): Role description
        users (list): Users assigned to this role
    """
    
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    
    # Relationships
    users = relationship("User", secondary=user_roles, back_populates="roles")
    
    def __repr__(self):
        """String representation of role"""
        return f"<Role name={self.name}>"