"""
Engineering repository for engineering-specific database operations.

This module provides specialized repository methods for engineering documents
including RFIs, submittals, and other engineering records.
"""

import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from core.database.repository import Repository
from core.models.engineering import (
    Submittal, SubmittalStatus, SubmittalAttachment,
    Rfi, RfiStatus, RfiAttachment
)
from core.database.config import get_db_session

# Set up logging
logger = logging.getLogger(__name__)

class SubmittalRepository(Repository[Submittal]):
    """
    Submittal repository with specialized methods for submittal management.
    
    This class extends the base Repository with methods specific to Submittal entities.
    """
    
    def __init__(self):
        """Initialize with Submittal model"""
        super().__init__(Submittal)
    
    def get_by_number(self, project_id: int, submittal_number: str) -> Optional[Submittal]:
        """
        Get a submittal by its number within a project.
        
        Args:
            project_id: Project ID
            submittal_number: Submittal identifier
            
        Returns:
            Submittal instance or None if not found
        """
        try:
            with get_db_session() as db:
                return db.query(Submittal) \
                    .filter(
                        Submittal.project_id == project_id,
                        Submittal.submittal_number == submittal_number,
                        Submittal.is_active == True
                    ) \
                    .first()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_by_number: {str(e)}")
            return None
    
    def get_project_submittals(self, project_id: int, status: Optional[SubmittalStatus] = None) -> List[Submittal]:
        """
        Get all submittals for a project, optionally filtered by status.
        
        Args:
            project_id: Project ID
            status: Optional status filter
            
        Returns:
            List of submittals
        """
        try:
            with get_db_session() as db:
                query = db.query(Submittal) \
                    .filter(
                        Submittal.project_id == project_id,
                        Submittal.is_active == True
                    )
                
                if status:
                    query = query.filter(Submittal.status == status)
                
                return query.order_by(Submittal.submittal_number).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_project_submittals: {str(e)}")
            return []
    
    def get_user_submittals(self, user_id: int) -> List[Submittal]:
        """
        Get all submittals assigned to or created by a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of submittals
        """
        try:
            with get_db_session() as db:
                return db.query(Submittal) \
                    .filter(
                        (Submittal.assignee_id == user_id) | (Submittal.created_by_id == user_id),
                        Submittal.is_active == True
                    ) \
                    .order_by(Submittal.due_date) \
                    .all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_user_submittals: {str(e)}")
            return []
    
    def update_status(self, submittal_id: int, status: SubmittalStatus, notes: Optional[str] = None) -> bool:
        """
        Update the status of a submittal.
        
        Args:
            submittal_id: Submittal ID
            status: New status
            notes: Optional status update notes
            
        Returns:
            True if successful, False otherwise
        """
        data: Dict[str, Any] = {"status": status}
        
        if status in [SubmittalStatus.APPROVED, SubmittalStatus.APPROVED_AS_NOTED, 
                     SubmittalStatus.REVISE_AND_RESUBMIT, SubmittalStatus.REJECTED]:
            data["review_date"] = date.today()
            
        if notes:
            data["notes"] = notes
            
        try:
            return self.update(submittal_id, data) is not None
        except Exception as e:
            logger.error(f"Error updating submittal status: {str(e)}")
            return False
    
    def get_with_attachments(self, submittal_id: int) -> Optional[Submittal]:
        """
        Get a submittal with all its attachments.
        
        Args:
            submittal_id: Submittal ID
            
        Returns:
            Submittal with attachments or None if not found
        """
        try:
            with get_db_session() as db:
                return db.query(Submittal) \
                    .options(joinedload(Submittal.attachments)) \
                    .filter(
                        Submittal.id == submittal_id,
                        Submittal.is_active == True
                    ) \
                    .first()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_with_attachments: {str(e)}")
            return None
    
    def add_attachment(self, submittal_id: int, filename: str, file_path: str, 
                      file_size: Optional[int] = None, file_type: Optional[str] = None,
                      description: Optional[str] = None, uploaded_by_id: Optional[int] = None) -> Optional[SubmittalAttachment]:
        """
        Add an attachment to a submittal.
        
        Args:
            submittal_id: Submittal ID
            filename: Original filename
            file_path: Path to stored file
            file_size: Size of file in bytes
            file_type: MIME type of file
            description: Optional description
            uploaded_by_id: User ID who uploaded the file
            
        Returns:
            Created attachment or None if failed
        """
        try:
            with get_db_session() as db:
                attachment = SubmittalAttachment(
                    submittal_id=submittal_id,
                    filename=filename,
                    file_path=file_path,
                    file_size=file_size,
                    file_type=file_type,
                    description=description,
                    uploaded_by_id=uploaded_by_id
                )
                
                db.add(attachment)
                db.commit()
                db.refresh(attachment)
                return attachment
        except SQLAlchemyError as e:
            logger.error(f"Database error in add_attachment: {str(e)}")
            return None

class RfiRepository(Repository[Rfi]):
    """
    RFI repository with specialized methods for RFI management.
    
    This class extends the base Repository with methods specific to RFI entities.
    """
    
    def __init__(self):
        """Initialize with RFI model"""
        super().__init__(Rfi)
    
    def get_by_number(self, project_id: int, rfi_number: str) -> Optional[Rfi]:
        """
        Get an RFI by its number within a project.
        
        Args:
            project_id: Project ID
            rfi_number: RFI identifier
            
        Returns:
            RFI instance or None if not found
        """
        try:
            with get_db_session() as db:
                return db.query(Rfi) \
                    .filter(
                        Rfi.project_id == project_id,
                        Rfi.rfi_number == rfi_number,
                        Rfi.is_active == True
                    ) \
                    .first()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_by_number: {str(e)}")
            return None
    
    def get_project_rfis(self, project_id: int, status: Optional[RfiStatus] = None) -> List[Rfi]:
        """
        Get all RFIs for a project, optionally filtered by status.
        
        Args:
            project_id: Project ID
            status: Optional status filter
            
        Returns:
            List of RFIs
        """
        try:
            with get_db_session() as db:
                query = db.query(Rfi) \
                    .filter(
                        Rfi.project_id == project_id,
                        Rfi.is_active == True
                    )
                
                if status:
                    query = query.filter(Rfi.status == status)
                
                return query.order_by(Rfi.rfi_number).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_project_rfis: {str(e)}")
            return []
    
    def get_user_rfis(self, user_id: int) -> List[Rfi]:
        """
        Get all RFIs assigned to or created by a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of RFIs
        """
        try:
            with get_db_session() as db:
                return db.query(Rfi) \
                    .filter(
                        (Rfi.assignee_id == user_id) | (Rfi.created_by_id == user_id),
                        Rfi.is_active == True
                    ) \
                    .order_by(Rfi.due_date) \
                    .all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_user_rfis: {str(e)}")
            return []
    
    def update_status(self, rfi_id: int, status: RfiStatus, answer: Optional[str] = None) -> bool:
        """
        Update the status of an RFI.
        
        Args:
            rfi_id: RFI ID
            status: New status
            answer: Optional RFI answer
            
        Returns:
            True if successful, False otherwise
        """
        data: Dict[str, Any] = {"status": status}
        
        if status in [RfiStatus.ANSWERED, RfiStatus.CLOSED]:
            data["response_date"] = date.today()
            
        if answer:
            data["answer"] = answer
            
        try:
            return self.update(rfi_id, data) is not None
        except Exception as e:
            logger.error(f"Error updating RFI status: {str(e)}")
            return False
    
    def get_with_attachments(self, rfi_id: int) -> Optional[Rfi]:
        """
        Get an RFI with all its attachments.
        
        Args:
            rfi_id: RFI ID
            
        Returns:
            RFI with attachments or None if not found
        """
        try:
            with get_db_session() as db:
                return db.query(Rfi) \
                    .options(joinedload(Rfi.attachments)) \
                    .filter(
                        Rfi.id == rfi_id,
                        Rfi.is_active == True
                    ) \
                    .first()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_with_attachments: {str(e)}")
            return None
    
    def add_attachment(self, rfi_id: int, filename: str, file_path: str, 
                      file_size: Optional[int] = None, file_type: Optional[str] = None,
                      description: Optional[str] = None, uploaded_by_id: Optional[int] = None) -> Optional[RfiAttachment]:
        """
        Add an attachment to an RFI.
        
        Args:
            rfi_id: RFI ID
            filename: Original filename
            file_path: Path to stored file
            file_size: Size of file in bytes
            file_type: MIME type of file
            description: Optional description
            uploaded_by_id: User ID who uploaded the file
            
        Returns:
            Created attachment or None if failed
        """
        try:
            with get_db_session() as db:
                attachment = RfiAttachment(
                    rfi_id=rfi_id,
                    filename=filename,
                    file_path=file_path,
                    file_size=file_size,
                    file_type=file_type,
                    description=description,
                    uploaded_by_id=uploaded_by_id
                )
                
                db.add(attachment)
                db.commit()
                db.refresh(attachment)
                return attachment
        except SQLAlchemyError as e:
            logger.error(f"Database error in add_attachment: {str(e)}")
            return None