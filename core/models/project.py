"""
Project models for construction management.

This module defines the Project model and related entities that form
the core of the construction management dashboard.
"""

import enum
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, Date, Enum, ForeignKey, Table, Integer, Boolean
from sqlalchemy.orm import relationship
from core.models.base import BaseModel
from core.database.config import Base

class ProjectStatus(enum.Enum):
    """Project status enumeration"""
    PLANNING = "planning"
    PRECONSTRUCTION = "preconstruction"
    CONSTRUCTION = "construction"
    CLOSEOUT = "closeout"
    COMPLETE = "complete"
    ON_HOLD = "on_hold"

class Project(BaseModel):
    """
    Project model representing a construction project.
    
    This is the central entity in the construction management system.
    
    Attributes:
        name (str): Project name
        code (str): Unique project code/number
        description (str): Project description
        status (ProjectStatus): Current project status
        start_date (Date): Planned/actual start date
        end_date (Date): Planned/actual end date
        address (str): Project location address
        city (str): Project city
        state (str): Project state/province
        zip_code (str): Project zip/postal code
        country (str): Project country
        budget (float): Total project budget
        owner_name (str): Project owner/client name
        architect_name (str): Project architect name
        team_members (list): Users assigned to project
    """
    
    # Basic project information
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PLANNING, nullable=False)
    
    # Project dates
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    
    # Location information
    address = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)
    
    # Financial information
    budget = Column(Float, nullable=True)
    
    # Key stakeholders
    owner_name = Column(String(100), nullable=True)
    architect_name = Column(String(100), nullable=True)
    
    # Relationships
    team_members = relationship("User", secondary="project_team_members", back_populates="projects")
    
    @property
    def location(self):
        """Get formatted location string"""
        parts = [part for part in [self.city, self.state, self.country] if part]
        return ", ".join(parts) if parts else "N/A"
    
    @property
    def duration_days(self):
        """Calculate project duration in days"""
        if not self.start_date or not self.end_date:
            return None
        return (self.end_date - self.start_date).days
    
    @property
    def is_active(self):
        """Check if project is currently active"""
        return self.status in [
            ProjectStatus.PRECONSTRUCTION,
            ProjectStatus.CONSTRUCTION,
            ProjectStatus.CLOSEOUT
        ]

# Many-to-many relationship between projects and users (team members)
project_team_members = Table(
    'project_team_members',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('project.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True)
)

# Add the projects relationship to User model
from core.models.user import User
User.projects = relationship("Project", secondary="project_team_members", back_populates="team_members")

class ProjectMilestone(BaseModel):
    """
    Project milestone representing key project events.
    
    Attributes:
        project_id (int): Associated project ID
        name (str): Milestone name
        description (str): Milestone description
        target_date (Date): Target completion date
        actual_date (Date): Actual completion date
        is_completed (bool): Whether milestone is completed
        project (Project): Associated project
    """
    
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    target_date = Column(Date, nullable=False)
    actual_date = Column(Date, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    project = relationship("Project", backref="milestones")
    
    @property
    def is_delayed(self):
        """Check if milestone is delayed"""
        if not self.is_completed and self.target_date:
            return self.target_date < datetime.now().date()
        elif self.is_completed and self.target_date and self.actual_date:
            return self.actual_date > self.target_date
        return False