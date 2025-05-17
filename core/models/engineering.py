"""
Engineering models for construction management.

This module defines models for engineering processes like RFIs, submittals,
change orders, and other engineering document types.
"""

import enum
from datetime import datetime
from sqlalchemy import Column, String, Text, Date, DateTime, Enum, ForeignKey, Integer, Boolean, Table
from sqlalchemy.orm import relationship
from core.models.base import BaseModel
from core.database.config import Base

class SubmittalStatus(enum.Enum):
    """Submittal status enumeration"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    APPROVED_AS_NOTED = "approved_as_noted"
    REVISE_AND_RESUBMIT = "revise_and_resubmit"
    REJECTED = "rejected"
    CLOSED = "closed"

class Submittal(BaseModel):
    """
    Submittal model representing a construction submittal document.
    
    Attributes:
        project_id (int): Associated project ID
        submittal_number (str): Unique submittal number/identifier
        title (str): Submittal title/description
        spec_section (str): Specification section reference
        status (SubmittalStatus): Current submittal status
        submission_date (Date): Date submitted
        due_date (Date): Review due date
        review_date (Date): Actual review completion date
        notes (str): Submittal notes/comments
        is_critical (bool): Whether this is a critical/high-priority submittal
        created_by_id (int): User ID who created the submittal
        assignee_id (int): User ID assigned to review the submittal
    """
    
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    submittal_number = Column(String(50), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    spec_section = Column(String(100), nullable=True)
    status = Column(Enum(SubmittalStatus), default=SubmittalStatus.DRAFT, nullable=False)
    submission_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)
    review_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    is_critical = Column(Boolean, default=False, nullable=False)
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    assignee_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    
    # Relationships
    project = relationship("Project", backref="submittals")
    created_by = relationship("User", foreign_keys=[created_by_id])
    assignee = relationship("User", foreign_keys=[assignee_id])
    attachments = relationship("SubmittalAttachment", back_populates="submittal", cascade="all, delete-orphan")
    
    @property
    def is_overdue(self):
        """Check if submittal review is overdue"""
        if self.due_date and self.status not in [
            SubmittalStatus.APPROVED,
            SubmittalStatus.APPROVED_AS_NOTED,
            SubmittalStatus.REJECTED,
            SubmittalStatus.CLOSED
        ]:
            return self.due_date < datetime.now().date()
        return False
    
    @property
    def days_remaining(self):
        """Calculate days remaining until due date"""
        if not self.due_date:
            return None
        
        if self.status in [
            SubmittalStatus.APPROVED,
            SubmittalStatus.APPROVED_AS_NOTED,
            SubmittalStatus.REJECTED,
            SubmittalStatus.CLOSED
        ]:
            return 0
            
        delta = self.due_date - datetime.now().date()
        return delta.days

class SubmittalAttachment(BaseModel):
    """
    Attachment model for submittal documents.
    
    Attributes:
        submittal_id (int): Associated submittal ID
        filename (str): Original filename
        file_path (str): Path to stored file
        file_size (int): Size of file in bytes
        file_type (str): MIME type of file
        description (str): Optional description of file
        uploaded_by_id (int): User ID who uploaded the file
    """
    
    submittal_id = Column(Integer, ForeignKey("submittal.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_size = Column(Integer, nullable=True)
    file_type = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    uploaded_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    
    # Relationships
    submittal = relationship("Submittal", back_populates="attachments")
    uploaded_by = relationship("User")

class RfiStatus(enum.Enum):
    """RFI status enumeration"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    ANSWERED = "answered"
    NEEDS_CLARIFICATION = "needs_clarification"
    CLOSED = "closed"

class Rfi(BaseModel):
    """
    Request for Information (RFI) model.
    
    Attributes:
        project_id (int): Associated project ID
        rfi_number (str): Unique RFI number/identifier
        subject (str): RFI subject/title
        question (str): The actual RFI question/request
        answer (str): Response to the RFI
        status (RfiStatus): Current RFI status
        submission_date (Date): Date submitted
        due_date (Date): Response due date
        response_date (Date): Actual response date
        is_critical (bool): Whether this is a critical/high-priority RFI
        created_by_id (int): User ID who created the RFI
        assignee_id (int): User ID assigned to answer the RFI
    """
    
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    rfi_number = Column(String(50), nullable=False, index=True)
    subject = Column(String(255), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    status = Column(Enum(RfiStatus), default=RfiStatus.DRAFT, nullable=False)
    submission_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)
    response_date = Column(Date, nullable=True)
    is_critical = Column(Boolean, default=False, nullable=False)
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    assignee_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    
    # Relationships
    project = relationship("Project", backref="rfis")
    created_by = relationship("User", foreign_keys=[created_by_id])
    assignee = relationship("User", foreign_keys=[assignee_id])
    attachments = relationship("RfiAttachment", back_populates="rfi", cascade="all, delete-orphan")
    
    @property
    def is_overdue(self):
        """Check if RFI response is overdue"""
        if self.due_date and self.status not in [RfiStatus.ANSWERED, RfiStatus.CLOSED]:
            return self.due_date < datetime.now().date()
        return False
    
    @property
    def days_open(self):
        """Calculate days the RFI has been open"""
        if not self.submission_date:
            return 0
            
        if self.status in [RfiStatus.ANSWERED, RfiStatus.CLOSED] and self.response_date:
            delta = self.response_date - self.submission_date
        else:
            delta = datetime.now().date() - self.submission_date
            
        return delta.days

class RfiAttachment(BaseModel):
    """
    Attachment model for RFI documents.
    
    Attributes:
        rfi_id (int): Associated RFI ID
        filename (str): Original filename
        file_path (str): Path to stored file
        file_size (int): Size of file in bytes
        file_type (str): MIME type of file
        description (str): Optional description of file
        uploaded_by_id (int): User ID who uploaded the file
    """
    
    rfi_id = Column(Integer, ForeignKey("rfi.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_size = Column(Integer, nullable=True)
    file_type = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    uploaded_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    
    # Relationships
    rfi = relationship("Rfi", back_populates="attachments")
    uploaded_by = relationship("User")