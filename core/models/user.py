"""
User models for authentication and authorization.

This module defines the User and Role models for authentication and 
role-based access control (RBAC).
"""

import enum
from sqlalchemy import Column, String, ForeignKey, Table, Enum, Integer
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
    """User account status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    LOCKED = "locked"

class User(BaseModel):
    """
    User model for authentication and user profile information.
    
    Attributes:
        username (str): Unique username for login
        email (str): User's email address
        password_hash (str): Hashed password (never store plain text)
        first_name (str): User's first name
        last_name (str): User's last name
        status (UserStatus): Account status
        roles (list): User's roles for authorization
    """
    
    # User authentication fields
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # User profile fields
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE, nullable=False)
    
    # Relationships
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    
    @property
    def full_name(self):
        """Get user's full name or username if name is not set"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def has_role(self, role_name):
        """
        Check if user has a specific role.
        
        Args:
            role_name (str): Name of role to check
            
        Returns:
            bool: True if user has role, False otherwise
        """
        return any(role.name == role_name for role in self.roles)
    
    def has_permission(self, permission_name):
        """
        Check if user has a specific permission through any of their roles.
        
        Args:
            permission_name (str): Name of permission to check
            
        Returns:
            bool: True if user has permission, False otherwise
        """
        for role in self.roles:
            if any(perm.name == permission_name for perm in role.permissions):
                return True
        return False

class Role(BaseModel):
    """
    Role model for role-based access control.
    
    Attributes:
        name (str): Unique role name
        description (str): Role description
        permissions (list): Permissions granted by this role
        users (list): Users with this role
    """
    
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    
    # Relationships
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")
    users = relationship("User", secondary=user_roles, back_populates="roles")

# Many-to-many relationship between roles and permissions
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('role.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permission.id'), primary_key=True)
)

class Permission(BaseModel):
    """
    Permission model for fine-grained access control.
    
    Attributes:
        name (str): Unique permission name
        description (str): Permission description
        roles (list): Roles that include this permission
    """
    
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    
    # Relationships
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")