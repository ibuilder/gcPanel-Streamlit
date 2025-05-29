"""
Highland Tower Development - SQLAlchemy Database Models
Production-ready ORM models for construction management data
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
import os

Base = declarative_base()

class User(Base):
    """User model for authentication and role management"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    role = Column(String(20), default='user')
    company_id = Column(Integer, ForeignKey('companies.id'))
    phone = Column(String(20))
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    last_login = Column(DateTime)
    
    company = relationship("Company", back_populates="users")
    rfis = relationship("RFI", back_populates="created_by_user")
    daily_reports = relationship("DailyReport", back_populates="created_by_user")

class Company(Base):
    """Company model for multi-tenant support"""
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    domain = Column(String(100))
    subscription_type = Column(String(20), default='basic')
    max_users = Column(Integer, default=10)
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    
    users = relationship("User", back_populates="company")
    projects = relationship("Project", back_populates="company")

class Project(Base):
    """Project model for Highland Tower construction projects"""
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    project_number = Column(String(50), unique=True)
    description = Column(Text)
    company_id = Column(Integer, ForeignKey('companies.id'))
    contract_value = Column(Float)
    start_date = Column(DateTime)
    completion_date = Column(DateTime)
    status = Column(String(20), default='active')
    location = Column(String(200))
    project_manager_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=func.now())
    
    company = relationship("Company", back_populates="projects")
    project_manager = relationship("User")
    rfis = relationship("RFI", back_populates="project")
    daily_reports = relationship("DailyReport", back_populates="project")
    change_orders = relationship("ChangeOrder", back_populates="project")
    cost_codes = relationship("CostCode", back_populates="project")

class RFI(Base):
    """Request for Information model"""
    __tablename__ = 'rfis'
    
    id = Column(Integer, primary_key=True)
    rfi_number = Column(String(50), nullable=False)
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(200))
    specification_section = Column(String(50))
    status = Column(String(20), default='open')
    priority = Column(String(10), default='medium')
    project_id = Column(Integer, ForeignKey('projects.id'))
    created_by = Column(Integer, ForeignKey('users.id'))
    assigned_to = Column(Integer, ForeignKey('users.id'))
    due_date = Column(DateTime)
    response = Column(Text)
    cost_impact = Column(Float, default=0.0)
    schedule_impact = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    project = relationship("Project", back_populates="rfis")
    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="rfis")
    assigned_to_user = relationship("User", foreign_keys=[assigned_to])

class DailyReport(Base):
    """Daily construction report model"""
    __tablename__ = 'daily_reports'
    
    id = Column(Integer, primary_key=True)
    report_date = Column(DateTime, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    created_by = Column(Integer, ForeignKey('users.id'))
    weather = Column(String(100))
    temperature_high = Column(Integer)
    temperature_low = Column(Integer)
    work_performed = Column(Text)
    crew_count = Column(Integer)
    equipment_used = Column(Text)
    materials_delivered = Column(Text)
    safety_incidents = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    project = relationship("Project", back_populates="daily_reports")
    created_by_user = relationship("User", back_populates="daily_reports")

class ChangeOrder(Base):
    """Change order model for contract modifications"""
    __tablename__ = 'change_orders'
    
    id = Column(Integer, primary_key=True)
    change_order_number = Column(String(50), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    description = Column(Text, nullable=False)
    reason = Column(String(100))
    amount = Column(Float, nullable=False)
    status = Column(String(20), default='pending')
    requested_by = Column(Integer, ForeignKey('users.id'))
    approved_by = Column(Integer, ForeignKey('users.id'))
    requested_date = Column(DateTime, default=func.now())
    approved_date = Column(DateTime)
    effective_date = Column(DateTime)
    
    project = relationship("Project", back_populates="change_orders")
    requested_by_user = relationship("User", foreign_keys=[requested_by])
    approved_by_user = relationship("User", foreign_keys=[approved_by])

class CostCode(Base):
    """Cost code model for project cost tracking"""
    __tablename__ = 'cost_codes'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(20), nullable=False)
    description = Column(String(200), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    phase = Column(String(50))
    category = Column(String(50))
    unit_of_measure = Column(String(20))
    budgeted_amount = Column(Float, default=0.0)
    actual_amount = Column(Float, default=0.0)
    committed_amount = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    
    project = relationship("Project", back_populates="cost_codes")

class Submittal(Base):
    """Submittal model for document approval workflow"""
    __tablename__ = 'submittals'
    
    id = Column(Integer, primary_key=True)
    submittal_number = Column(String(50), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    specification_section = Column(String(50))
    status = Column(String(20), default='pending')
    submitted_by = Column(Integer, ForeignKey('users.id'))
    reviewed_by = Column(Integer, ForeignKey('users.id'))
    submitted_date = Column(DateTime, default=func.now())
    review_date = Column(DateTime)
    due_date = Column(DateTime)
    file_path = Column(String(500))
    comments = Column(Text)
    
    project = relationship("Project")
    submitted_by_user = relationship("User", foreign_keys=[submitted_by])
    reviewed_by_user = relationship("User", foreign_keys=[reviewed_by])

class SafetyIncident(Base):
    """Safety incident model for safety management"""
    __tablename__ = 'safety_incidents'
    
    id = Column(Integer, primary_key=True)
    incident_number = Column(String(50), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    incident_date = Column(DateTime, nullable=False)
    location = Column(String(200))
    description = Column(Text, nullable=False)
    severity = Column(String(20))
    injured_person = Column(String(100))
    witness = Column(String(100))
    immediate_action = Column(Text)
    root_cause = Column(Text)
    corrective_action = Column(Text)
    reported_by = Column(Integer, ForeignKey('users.id'))
    status = Column(String(20), default='open')
    created_at = Column(DateTime, default=func.now())
    
    project = relationship("Project")
    reported_by_user = relationship("User")

class Document(Base):
    """Document model for file management"""
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255))
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    file_type = Column(String(50))
    category = Column(String(50))
    description = Column(Text)
    uploaded_by = Column(Integer, ForeignKey('users.id'))
    uploaded_at = Column(DateTime, default=func.now())
    version = Column(String(10), default='1.0')
    is_active = Column(Boolean, default=True)
    
    project = relationship("Project")
    uploaded_by_user = relationship("User")

class IntegrationCredential(Base):
    """Integration credentials model for external platform API keys"""
    __tablename__ = 'integration_credentials'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    platform = Column(String(50), nullable=False)
    credentials = Column(JSON, nullable=False)  # Encrypted JSON storage
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    company = relationship("Company")

class AuditLog(Base):
    """Audit log model for tracking system changes"""
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(50), nullable=False)
    table_name = Column(String(50))
    record_id = Column(Integer)
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    timestamp = Column(DateTime, default=func.now())
    
    user = relationship("User")

class DatabaseManager:
    """Database connection and session management"""
    
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL', 'postgresql://localhost/highland_tower')
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Get database session"""
        session = self.SessionLocal()
        try:
            return session
        except Exception:
            session.close()
            raise
    
    def close_session(self, session):
        """Close database session"""
        session.close()

# Initialize database manager
db_manager = DatabaseManager()