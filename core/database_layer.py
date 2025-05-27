"""
Pure Python Database Layer for Highland Tower Development
SQLAlchemy-based data persistence with zero UI dependencies

This provides a sustainable database foundation independent of any UI framework
"""

import os
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Date, Boolean, Text, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .data_models import RFIStatus, Priority, Discipline, ProjectStatus

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///highland_tower.db")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ProjectDB(Base):
    """Project database model"""
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    value = Column(Float, nullable=False)
    status = Column(SQLEnum(ProjectStatus), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    residential_units = Column(Integer, default=0)
    retail_units = Column(Integer, default=0)
    floors_above = Column(Integer, default=0)
    floors_below = Column(Integer, default=0)
    progress_percent = Column(Float, default=0.0)
    budget_remaining = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RFIDB(Base):
    """RFI database model"""
    __tablename__ = "rfis"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    number = Column(String(50), unique=True, nullable=False)
    subject = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=False)
    discipline = Column(SQLEnum(Discipline), nullable=False)
    priority = Column(SQLEnum(Priority), nullable=False)
    status = Column(SQLEnum(RFIStatus), nullable=False)
    submitted_by = Column(String(255), nullable=False)
    assigned_to = Column(String(255), nullable=False)
    submitted_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    cost_impact = Column(String(100))
    schedule_impact = Column(String(100))
    project_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SubcontractorDB(Base):
    """Subcontractor database model"""
    __tablename__ = "subcontractors"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_name = Column(String(255), nullable=False)
    contact_person = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    license_number = Column(String(100), nullable=False)
    insurance_expiry = Column(Date, nullable=False)
    specialties = Column(Text)  # JSON string of specialties list
    performance_rating = Column(Float, default=0.0)
    active_projects = Column(Integer, default=0)
    total_contract_value = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DatabaseManager:
    """Pure Python database operations manager"""
    
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
        Base.metadata.create_all(bind=engine)
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    def initialize_highland_tower_data(self):
        """Initialize Highland Tower Development project data"""
        session = self.get_session()
        try:
            # Check if Highland Tower project exists
            existing_project = session.query(ProjectDB).filter_by(name="Highland Tower Development").first()
            
            if not existing_project:
                # Create Highland Tower project
                highland_project = ProjectDB(
                    id="HTD-2024-001",
                    name="Highland Tower Development",
                    value=45500000.0,
                    status=ProjectStatus.ACTIVE,
                    start_date=date(2024, 1, 15),
                    end_date=date(2025, 12, 31),
                    residential_units=120,
                    retail_units=8,
                    floors_above=15,
                    floors_below=2,
                    progress_percent=67.3,
                    budget_remaining=15600000.0
                )
                session.add(highland_project)
                
                # Create sample RFIs
                sample_rfis = [
                    RFIDB(
                        id="HTD-RFI-001",
                        number="RFI-2025-001",
                        subject="Steel beam connection detail clarification Level 12-13",
                        description="Need clarification on connection detail for main structural beams at Grid Line A between floors 12-13. Current drawings show conflicting details.",
                        location="Level 12-13, Grid Line A-B",
                        discipline=Discipline.STRUCTURAL,
                        priority=Priority.HIGH,
                        status=RFIStatus.OPEN,
                        submitted_by="Mike Chen - Site Superintendent",
                        assigned_to="Highland Structural Engineering",
                        submitted_date=date(2025, 5, 20),
                        due_date=date(2025, 5, 27),
                        cost_impact="$15,000 - $25,000",
                        schedule_impact="2-3 days",
                        project_id="HTD-2024-001"
                    ),
                    RFIDB(
                        id="HTD-RFI-002",
                        number="RFI-2025-002",
                        subject="HVAC ductwork routing coordination Level 12 mechanical room",
                        description="HVAC ductwork conflicts with structural beams in north mechanical room. Need routing solution.",
                        location="Level 12 - Mechanical Room North",
                        discipline=Discipline.MEP,
                        priority=Priority.MEDIUM,
                        status=RFIStatus.IN_REVIEW,
                        submitted_by="Sarah Johnson - Project Manager",
                        assigned_to="Highland MEP Consultants",
                        submitted_date=date(2025, 5, 18),
                        due_date=date(2025, 5, 25),
                        cost_impact="$5,000 - $10,000",
                        schedule_impact="1-2 days",
                        project_id="HTD-2024-001"
                    )
                ]
                
                for rfi in sample_rfis:
                    session.add(rfi)
                
                # Create sample subcontractors
                import json
                sample_subcontractors = [
                    SubcontractorDB(
                        id="SUB-001",
                        company_name="Highland Construction Corp",
                        contact_person="Michael Torres",
                        email="m.torres@highlandconstruction.com",
                        phone="(555) 123-4567",
                        license_number="CA-LIC-123456",
                        insurance_expiry=date(2025, 12, 31),
                        specialties=json.dumps(["General Construction", "Concrete", "Steel"]),
                        performance_rating=4.8,
                        active_projects=3,
                        total_contract_value=28500000.0
                    ),
                    SubcontractorDB(
                        id="SUB-002",
                        company_name="Elite MEP Solutions",
                        contact_person="Jennifer Walsh",
                        email="j.walsh@elitemep.com",
                        phone="(555) 234-5678",
                        license_number="CA-MEP-789012",
                        insurance_expiry=date(2025, 11, 15),
                        specialties=json.dumps(["HVAC", "Electrical", "Plumbing"]),
                        performance_rating=4.5,
                        active_projects=2,
                        total_contract_value=8200000.0
                    )
                ]
                
                for sub in sample_subcontractors:
                    session.add(sub)
                
                session.commit()
                return True
            
            return False
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_all_rfis(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all RFIs with optional project filtering"""
        session = self.get_session()
        try:
            query = session.query(RFIDB)
            if project_id:
                query = query.filter_by(project_id=project_id)
            
            rfis = query.all()
            
            result = []
            for rfi in rfis:
                result.append({
                    "id": rfi.id,
                    "number": rfi.number,
                    "subject": rfi.subject,
                    "description": rfi.description,
                    "location": rfi.location,
                    "discipline": rfi.discipline.value,
                    "priority": rfi.priority.value,
                    "status": rfi.status.value,
                    "submitted_by": rfi.submitted_by,
                    "assigned_to": rfi.assigned_to,
                    "submitted_date": rfi.submitted_date.isoformat(),
                    "due_date": rfi.due_date.isoformat(),
                    "cost_impact": rfi.cost_impact,
                    "schedule_impact": rfi.schedule_impact,
                    "days_open": (date.today() - rfi.submitted_date).days,
                    "created_at": rfi.created_at.isoformat()
                })
            
            return result
            
        finally:
            session.close()
    
    def create_rfi(self, rfi_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new RFI in database"""
        session = self.get_session()
        try:
            # Generate new RFI number
            existing_count = session.query(RFIDB).filter_by(project_id=rfi_data.get("project_id", "HTD-2024-001")).count()
            new_number = f"RFI-2025-{existing_count + 1:03d}"
            new_id = f"HTD-RFI-{existing_count + 1:03d}"
            
            new_rfi = RFIDB(
                id=new_id,
                number=new_number,
                **rfi_data
            )
            
            session.add(new_rfi)
            session.commit()
            
            return {
                "id": new_rfi.id,
                "number": new_rfi.number,
                "created_at": new_rfi.created_at.isoformat()
            }
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_project_statistics(self, project_id: str = "HTD-2024-001") -> Dict[str, Any]:
        """Get comprehensive project statistics"""
        session = self.get_session()
        try:
            # RFI statistics
            total_rfis = session.query(RFIDB).filter_by(project_id=project_id).count()
            open_rfis = session.query(RFIDB).filter_by(project_id=project_id, status=RFIStatus.OPEN).count()
            critical_rfis = session.query(RFIDB).filter_by(project_id=project_id, priority=Priority.CRITICAL).count()
            
            # Subcontractor statistics
            total_subs = session.query(SubcontractorDB).count()
            avg_rating = session.query(SubcontractorDB).with_entities(
                session.query(SubcontractorDB.performance_rating).scalar_subquery()
            ).scalar() or 0
            
            # Project health
            project = session.query(ProjectDB).filter_by(id=project_id).first()
            
            return {
                "rfis": {
                    "total": total_rfis,
                    "open": open_rfis,
                    "critical": critical_rfis
                },
                "subcontractors": {
                    "total": total_subs,
                    "avg_rating": avg_rating
                },
                "project": {
                    "progress": project.progress_percent if project else 0,
                    "budget_remaining": project.budget_remaining if project else 0,
                    "value": project.value if project else 0
                }
            }
            
        finally:
            session.close()


# Global database manager instance
db_manager = DatabaseManager()