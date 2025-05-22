"""
Project Directory models for gcPanel.

This module provides database models for mapping users to projects
through their email addresses, enabling seamless authentication via
OAuth providers like Google, Microsoft, and Procore.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from core.models.base import BaseModel
from core.database.config import Base

class ProjectDirectory(BaseModel):
    """Project Directory model for mapping user emails to projects."""
    
    __tablename__ = "project_directory"
    
    email = Column(String(255), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    role = Column(String(100), nullable=True)  # Role within the project
    company = Column(String(255), nullable=True)
    position = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    project = relationship("Project", back_populates="directory_entries")
    
    def to_dict(self):
        """Convert directory entry to dictionary."""
        entry_dict = super().to_dict()
        
        # Add computed properties
        first_name = str(self.first_name) if self.first_name else ""
        last_name = str(self.last_name) if self.last_name else ""
        email = str(self.email) if self.email else ""
        
        if first_name and last_name:
            entry_dict["full_name"] = f"{first_name} {last_name}"
        elif first_name:
            entry_dict["full_name"] = first_name
        elif last_name:
            entry_dict["full_name"] = last_name
        else:
            entry_dict["full_name"] = email.split('@')[0] if '@' in email else email
        
        return entry_dict


# Update Project model to include directory entries
# This will need to be added to the Project model in core/models/project.py
"""
# Add to Project model:
directory_entries = relationship("ProjectDirectory", back_populates="project")
"""

class ProjectDirectoryAuthorizedSource(BaseModel):
    """
    Authorized email domains for project directory.
    
    This model defines which email domains (e.g., '@example.com')
    are automatically authorized for Project Directory entries,
    allowing for automatic user creation with appropriate permissions.
    """
    
    __tablename__ = "project_directory_authorized_sources"
    
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    domain = Column(String(255), nullable=False)  # e.g., "example.com"
    default_role = Column(String(100), nullable=True)  # Default role for users from this domain
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    project = relationship("Project")
    
    def to_dict(self):
        """Convert authorized source to dictionary."""
        return super().to_dict()