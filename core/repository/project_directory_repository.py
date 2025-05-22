"""
Project Directory Repository for gcPanel.

This module provides repository functions for managing project directory entries
including adding, removing, and verifying email addresses.
"""

import logging
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError

from core.database.repository import Repository
from core.models.project_directory import ProjectDirectory
from core.database.config import get_db_session

logger = logging.getLogger(__name__)

class ProjectDirectoryRepository(Repository[ProjectDirectory]):
    """
    Repository for project directory operations.
    
    This class extends the base Repository for ProjectDirectory-specific operations
    such as checking if an email exists in the project directory.
    """
    
    def __init__(self):
        """Initialize with ProjectDirectory model"""
        super().__init__(ProjectDirectory)
    
    def get_by_email(self, email: str) -> List[ProjectDirectory]:
        """
        Get all project directory entries for a given email.
        
        Args:
            email: Email address to search for
            
        Returns:
            List of ProjectDirectory objects matching the email
        """
        try:
            with get_db_session() as db:
                return db.query(ProjectDirectory) \
                    .filter(ProjectDirectory.email == email, 
                            ProjectDirectory.is_active == True) \
                    .all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_by_email: {str(e)}")
            return []
    
    def is_email_in_project(self, email: str, project_id: int) -> bool:
        """
        Check if an email exists in a specific project directory.
        
        Args:
            email: Email address to check
            project_id: Project ID to check
            
        Returns:
            True if email exists in project directory, False otherwise
        """
        try:
            with get_db_session() as db:
                count = db.query(ProjectDirectory) \
                    .filter(ProjectDirectory.email == email,
                            ProjectDirectory.project_id == project_id,
                            ProjectDirectory.is_active == True) \
                    .count()
                return count > 0
        except SQLAlchemyError as e:
            logger.error(f"Database error in is_email_in_project: {str(e)}")
            return False
    
    def get_projects_for_email(self, email: str) -> List[int]:
        """
        Get all project IDs where an email appears in the directory.
        
        Args:
            email: Email address to search for
            
        Returns:
            List of project IDs where email exists in directory
        """
        try:
            with get_db_session() as db:
                results = db.query(ProjectDirectory.project_id) \
                    .filter(ProjectDirectory.email == email,
                            ProjectDirectory.is_active == True) \
                    .all()
                return [r[0] for r in results]
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_projects_for_email: {str(e)}")
            return []
    
    def add_to_directory(self, email: str, project_id: int, role: str = None, 
                         first_name: str = None, last_name: str = None,
                         company: str = None, position: str = None,
                         phone: str = None) -> Optional[int]:
        """
        Add an email to a project directory.
        
        Args:
            email: Email address to add
            project_id: Project ID to add to
            role: Role within the project
            first_name: First name
            last_name: Last name
            company: Company name
            position: Position title
            phone: Phone number
            
        Returns:
            ID of new directory entry or None if failed
        """
        try:
            # First check if already exists
            if self.is_email_in_project(email, project_id):
                logger.info(f"Email {email} already exists in project {project_id}")
                return None
            
            # Create new directory entry
            entry = ProjectDirectory(
                email=email,
                project_id=project_id,
                role=role,
                first_name=first_name,
                last_name=last_name,
                company=company,
                position=position,
                phone=phone,
                is_active=True
            )
            
            return self.create(entry)
        except Exception as e:
            logger.error(f"Error adding email to directory: {str(e)}")
            return None
    
    def remove_from_directory(self, email: str, project_id: int) -> bool:
        """
        Remove an email from a project directory.
        
        Args:
            email: Email address to remove
            project_id: Project ID to remove from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with get_db_session() as db:
                entry = db.query(ProjectDirectory) \
                    .filter(ProjectDirectory.email == email,
                            ProjectDirectory.project_id == project_id,
                            ProjectDirectory.is_active == True) \
                    .first()
                
                if not entry:
                    logger.info(f"Email {email} not found in project {project_id}")
                    return False
                
                # Soft delete
                entry.is_active = False
                db.commit()
                return True
        except SQLAlchemyError as e:
            logger.error(f"Database error in remove_from_directory: {str(e)}")
            return False
    
    def bulk_add_to_directory(self, entries: List[dict]) -> int:
        """
        Add multiple entries to project directory.
        
        Args:
            entries: List of dictionaries with entry information
                [
                    {
                        'email': 'user@example.com',
                        'project_id': 1,
                        'role': 'Project Manager',
                        'first_name': 'John',
                        'last_name': 'Doe',
                        'company': 'ABC Construction',
                        'position': 'Senior Manager',
                        'phone': '555-123-4567'
                    },
                    ...
                ]
                
        Returns:
            Number of entries successfully added
        """
        count = 0
        for entry in entries:
            try:
                if self.add_to_directory(
                    email=entry.get('email'),
                    project_id=entry.get('project_id'),
                    role=entry.get('role'),
                    first_name=entry.get('first_name'),
                    last_name=entry.get('last_name'),
                    company=entry.get('company'),
                    position=entry.get('position'),
                    phone=entry.get('phone')
                ):
                    count += 1
            except Exception as e:
                logger.error(f"Error adding entry {entry.get('email')}: {str(e)}")
                continue
        
        return count