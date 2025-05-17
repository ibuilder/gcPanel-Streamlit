"""
Project repository for project-specific database operations.

This module provides specialized repository methods for project management
beyond the basic CRUD operations.
"""

import logging
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from core.database.repository import Repository
from core.models.project import Project, ProjectMilestone, ProjectStatus
from core.database.config import get_db_session

# Set up logging
logger = logging.getLogger(__name__)

class ProjectRepository(Repository[Project]):
    """
    Project repository with specialized methods for project management.
    
    This class extends the base Repository with methods specific to Project entities.
    """
    
    def __init__(self):
        """Initialize with Project model"""
        super().__init__(Project)
    
    def get_by_code(self, code: str) -> Optional[Project]:
        """
        Get a project by its unique code.
        
        Args:
            code: Project code to search for
            
        Returns:
            Project instance or None if not found
        """
        try:
            with get_db_session() as db:
                return db.query(Project) \
                    .filter(Project.code == code, Project.is_active == True) \
                    .first()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_by_code: {str(e)}")
            return None
    
    def get_active_projects(self) -> List[Project]:
        """
        Get all active projects (planning, preconstruction, construction, or closeout).
        
        Returns:
            List of active projects
        """
        try:
            with get_db_session() as db:
                return db.query(Project) \
                    .filter(
                        Project.is_active == True,
                        Project.status.in_([
                            ProjectStatus.PLANNING,
                            ProjectStatus.PRECONSTRUCTION,
                            ProjectStatus.CONSTRUCTION,
                            ProjectStatus.CLOSEOUT
                        ])
                    ) \
                    .order_by(Project.name) \
                    .all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_active_projects: {str(e)}")
            return []
    
    def get_user_projects(self, user_id: int) -> List[Project]:
        """
        Get all projects assigned to a specific user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of projects assigned to user
        """
        try:
            with get_db_session() as db:
                from core.models.user import User
                return db.query(Project) \
                    .join(Project.team_members) \
                    .filter(
                        Project.is_active == True,
                        User.id == user_id
                    ) \
                    .order_by(Project.name) \
                    .all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_user_projects: {str(e)}")
            return []
    
    def get_project_milestones(self, project_id: int) -> List[ProjectMilestone]:
        """
        Get all milestones for a specific project.
        
        Args:
            project_id: Project ID
            
        Returns:
            List of project milestones
        """
        try:
            with get_db_session() as db:
                return db.query(ProjectMilestone) \
                    .filter(
                        ProjectMilestone.project_id == project_id,
                        ProjectMilestone.is_active == True
                    ) \
                    .order_by(ProjectMilestone.target_date) \
                    .all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_project_milestones: {str(e)}")
            return []
    
    def add_team_member(self, project_id: int, user_id: int) -> bool:
        """
        Add a user to the project team.
        
        Args:
            project_id: Project ID
            user_id: User ID to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with get_db_session() as db:
                from core.models.user import User
                
                project = db.query(Project).filter(Project.id == project_id).first()
                user = db.query(User).filter(User.id == user_id).first()
                
                if not project or not user:
                    return False
                
                if user not in project.team_members:
                    project.team_members.append(user)
                    db.commit()
                
                return True
        except SQLAlchemyError as e:
            logger.error(f"Database error in add_team_member: {str(e)}")
            return False
    
    def remove_team_member(self, project_id: int, user_id: int) -> bool:
        """
        Remove a user from the project team.
        
        Args:
            project_id: Project ID
            user_id: User ID to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with get_db_session() as db:
                from core.models.user import User
                
                project = db.query(Project).filter(Project.id == project_id).first()
                user = db.query(User).filter(User.id == user_id).first()
                
                if not project or not user:
                    return False
                
                if user in project.team_members:
                    project.team_members.remove(user)
                    db.commit()
                
                return True
        except SQLAlchemyError as e:
            logger.error(f"Database error in remove_team_member: {str(e)}")
            return False
    
    def update_project_status(self, project_id: int, status: ProjectStatus) -> bool:
        """
        Update the status of a project.
        
        Args:
            project_id: Project ID
            status: New project status
            
        Returns:
            True if successful, False otherwise
        """
        try:
            return self.update(project_id, {"status": status}) is not None
        except Exception as e:
            logger.error(f"Error updating project status: {str(e)}")
            return False