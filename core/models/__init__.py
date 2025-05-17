"""
Model package initialization.

This module initializes the models package and imports all model modules
to ensure they are registered with SQLAlchemy.
"""

from core.models.base import BaseModel
from core.models.user import User, Role, UserStatus
from core.models.project import Project, ProjectStatus, ProjectMilestone
from core.models.engineering import (
    Submittal, SubmittalStatus, SubmittalAttachment,
    Rfi, RfiStatus, RfiAttachment
)
from core.models.config import AppConfig