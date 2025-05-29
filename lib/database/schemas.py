"""
Database Schemas for Highland Tower Development
Production-ready PostgreSQL schemas for construction management
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional

class DatabaseManager:
    """Manage PostgreSQL database connections and operations"""
    
    def __init__(self):
        self.connection = None
        self.database_url = os.environ.get('DATABASE_URL')
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(
                self.database_url,
                cursor_factory=RealDictCursor
            )
            return True
        except Exception as e:
            st.error(f"Database connection failed: {str(e)}")
            return False
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict]]:
        """Execute query and return results"""
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description:
                    return cursor.fetchall()
                self.connection.commit()
                return []
        except Exception as e:
            st.error(f"Query execution failed: {str(e)}")
            self.connection.rollback()
            return None
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

class SchemaManager:
    """Manage database schema creation and migration"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def create_all_schemas(self):
        """Create all database schemas for Highland Tower Development"""
        schemas = [
            self.create_users_table(),
            self.create_projects_table(),
            self.create_rfis_table(),
            self.create_submittals_table(),
            self.create_daily_reports_table(),
            self.create_progress_photos_table(),
            self.create_quality_control_table(),
            self.create_subcontractors_table(),
            self.create_inspections_table(),
            self.create_issues_risks_table(),
            self.create_documents_table(),
            self.create_cost_management_table(),
            self.create_audit_logs_table()
        ]
        
        for schema_sql in schemas:
            result = self.db.execute_query(schema_sql)
            if result is None:
                st.error("Failed to create database schema")
                return False
        
        st.success("✅ All database schemas created successfully!")
        return True
    
    def create_users_table(self) -> str:
        """Users and authentication table"""
        return """
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR(50) PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role VARCHAR(50) NOT NULL,
            full_name VARCHAR(200) NOT NULL,
            email VARCHAR(200) UNIQUE NOT NULL,
            department VARCHAR(100),
            phone VARCHAR(20),
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            active BOOLEAN DEFAULT TRUE,
            permissions TEXT[], -- Array of permissions
            profile_image TEXT,
            emergency_contact VARCHAR(200),
            certifications TEXT[],
            CONSTRAINT valid_role CHECK (role IN ('admin', 'manager', 'superintendent', 'foreman', 'inspector', 'user'))
        );
        
        CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
        CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
        CREATE INDEX IF NOT EXISTS idx_users_active ON users(active);
        """
    
    def create_projects_table(self) -> str:
        """Main project information table"""
        return """
        CREATE TABLE IF NOT EXISTS projects (
            project_id VARCHAR(50) PRIMARY KEY,
            project_name VARCHAR(300) NOT NULL,
            project_code VARCHAR(50) UNIQUE NOT NULL,
            description TEXT,
            project_type VARCHAR(100),
            status VARCHAR(50) DEFAULT 'active',
            start_date DATE,
            planned_end_date DATE,
            actual_end_date DATE,
            total_budget DECIMAL(15,2),
            current_spent DECIMAL(15,2) DEFAULT 0,
            location_address TEXT,
            location_coordinates POINT,
            project_manager_id VARCHAR(50) REFERENCES users(user_id),
            superintendent_id VARCHAR(50) REFERENCES users(user_id),
            client_name VARCHAR(200),
            client_contact VARCHAR(200),
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata JSONB, -- Additional project metadata
            CONSTRAINT valid_status CHECK (status IN ('planning', 'active', 'on_hold', 'completed', 'cancelled'))
        );
        
        CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
        CREATE INDEX IF NOT EXISTS idx_projects_manager ON projects(project_manager_id);
        """
    
    def create_rfis_table(self) -> str:
        """Request for Information table"""
        return """
        CREATE TABLE IF NOT EXISTS rfis (
            rfi_id VARCHAR(50) PRIMARY KEY,
            project_id VARCHAR(50) REFERENCES projects(project_id),
            rfi_number VARCHAR(100) NOT NULL,
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            location VARCHAR(300),
            discipline VARCHAR(100),
            priority VARCHAR(20) DEFAULT 'medium',
            status VARCHAR(50) DEFAULT 'open',
            submitted_by VARCHAR(50) REFERENCES users(user_id),
            assigned_to VARCHAR(50) REFERENCES users(user_id),
            submitted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            required_response_date DATE,
            response_date TIMESTAMP,
            response TEXT,
            cost_impact DECIMAL(12,2),
            schedule_impact_days INTEGER,
            attachments TEXT[], -- Array of file paths
            related_drawings TEXT[],
            tags TEXT[],
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT valid_priority CHECK (priority IN ('low', 'medium', 'high', 'critical')),
            CONSTRAINT valid_status CHECK (status IN ('open', 'in_review', 'answered', 'closed', 'on_hold'))
        );
        
        CREATE INDEX IF NOT EXISTS idx_rfis_project ON rfis(project_id);
        CREATE INDEX IF NOT EXISTS idx_rfis_status ON rfis(status);
        CREATE INDEX IF NOT EXISTS idx_rfis_priority ON rfis(priority);
        CREATE INDEX IF NOT EXISTS idx_rfis_submitted_by ON rfis(submitted_by);
        """
    
    def create_submittals_table(self) -> str:
        """Submittals management table"""
        return """
        CREATE TABLE IF NOT EXISTS submittals (
            submittal_id VARCHAR(50) PRIMARY KEY,
            project_id VARCHAR(50) REFERENCES projects(project_id),
            submittal_number VARCHAR(100) NOT NULL,
            title TEXT NOT NULL,
            specification_section VARCHAR(50),
            contractor_id VARCHAR(50) REFERENCES users(user_id),
            reviewer_id VARCHAR(50) REFERENCES users(user_id),
            submittal_type VARCHAR(50),
            status VARCHAR(50) DEFAULT 'submitted',
            priority VARCHAR(20) DEFAULT 'medium',
            submitted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_date DATE,
            reviewed_date TIMESTAMP,
            approved_date TIMESTAMP,
            revision_number INTEGER DEFAULT 1,
            cost_impact DECIMAL(12,2),
            schedule_impact_days INTEGER,
            attachments TEXT[],
            review_comments TEXT,
            rejection_reason TEXT,
            tags TEXT[],
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT valid_status CHECK (status IN ('submitted', 'under_review', 'approved', 'approved_as_noted', 'rejected', 'resubmit'))
        );
        
        CREATE INDEX IF NOT EXISTS idx_submittals_project ON submittals(project_id);
        CREATE INDEX IF NOT EXISTS idx_submittals_status ON submittals(status);
        CREATE INDEX IF NOT EXISTS idx_submittals_contractor ON submittals(contractor_id);
        """
    
    def create_daily_reports_table(self) -> str:
        """Daily reports table"""
        return """
        CREATE TABLE IF NOT EXISTS daily_reports (
            report_id VARCHAR(50) PRIMARY KEY,
            project_id VARCHAR(50) REFERENCES projects(project_id),
            report_date DATE NOT NULL,
            submitted_by VARCHAR(50) REFERENCES users(user_id),
            weather_conditions VARCHAR(200),
            temperature_high INTEGER,
            temperature_low INTEGER,
            work_performed TEXT,
            crew_count INTEGER,
            hours_worked DECIMAL(5,2),
            safety_incidents INTEGER DEFAULT 0,
            safety_notes TEXT,
            materials_delivered TEXT[],
            equipment_used TEXT[],
            visitors TEXT[],
            photos TEXT[], -- Array of photo file paths
            issues_encountered TEXT,
            tomorrow_plan TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_daily_reports_project ON daily_reports(project_id);
        CREATE INDEX IF NOT EXISTS idx_daily_reports_date ON daily_reports(report_date);
        CREATE INDEX IF NOT EXISTS idx_daily_reports_submitted_by ON daily_reports(submitted_by);
        """
    
    def create_progress_photos_table(self) -> str:
        """Progress photos table"""
        return """
        CREATE TABLE IF NOT EXISTS progress_photos (
            photo_id VARCHAR(50) PRIMARY KEY,
            project_id VARCHAR(50) REFERENCES projects(project_id),
            filename VARCHAR(300) NOT NULL,
            file_path TEXT NOT NULL,
            file_size_mb DECIMAL(8,2),
            dimensions VARCHAR(20),
            location VARCHAR(300),
            category VARCHAR(100),
            description TEXT,
            photographer_id VARCHAR(50) REFERENCES users(user_id),
            photo_date DATE NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(50) DEFAULT 'approved',
            tags TEXT[],
            gps_coordinates POINT,
            related_rfi_id VARCHAR(50) REFERENCES rfis(rfi_id),
            related_daily_report_id VARCHAR(50) REFERENCES daily_reports(report_id),
            metadata JSONB, -- EXIF data, camera settings, etc.
            CONSTRAINT valid_status CHECK (status IN ('under_review', 'approved', 'rejected'))
        );
        
        CREATE INDEX IF NOT EXISTS idx_progress_photos_project ON progress_photos(project_id);
        CREATE INDEX IF NOT EXISTS idx_progress_photos_date ON progress_photos(photo_date);
        CREATE INDEX IF NOT EXISTS idx_progress_photos_category ON progress_photos(category);
        """
    
    def create_quality_control_table(self) -> str:
        """Quality control inspections table"""
        return """
        CREATE TABLE IF NOT EXISTS quality_inspections (
            inspection_id VARCHAR(50) PRIMARY KEY,
            project_id VARCHAR(50) REFERENCES projects(project_id),
            inspection_type VARCHAR(100) NOT NULL,
            location VARCHAR(300),
            inspector_id VARCHAR(50) REFERENCES users(user_id),
            scheduled_date DATE,
            completed_date TIMESTAMP,
            status VARCHAR(50) DEFAULT 'scheduled',
            result VARCHAR(50),
            checklist_items JSONB, -- Dynamic checklist based on inspection type
            deficiencies_found TEXT[],
            corrective_actions TEXT[],
            photos TEXT[],
            documents TEXT[],
            notes TEXT,
            followup_required BOOLEAN DEFAULT FALSE,
            followup_date DATE,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT valid_status CHECK (status IN ('scheduled', 'in_progress', 'completed', 'cancelled')),
            CONSTRAINT valid_result CHECK (result IN ('pass', 'fail', 'conditional_pass', 'pending'))
        );
        
        CREATE INDEX IF NOT EXISTS idx_quality_inspections_project ON quality_inspections(project_id);
        CREATE INDEX IF NOT EXISTS idx_quality_inspections_status ON quality_inspections(status);
        CREATE INDEX IF NOT EXISTS idx_quality_inspections_inspector ON quality_inspections(inspector_id);
        """
    
    def create_subcontractors_table(self) -> str:
        """Subcontractors management table"""
        return """
        CREATE TABLE IF NOT EXISTS subcontractors (
            subcontractor_id VARCHAR(50) PRIMARY KEY,
            company_name VARCHAR(300) NOT NULL,
            contact_person VARCHAR(200),
            email VARCHAR(200),
            phone VARCHAR(20),
            address TEXT,
            trade_specialty VARCHAR(100),
            license_number VARCHAR(100),
            insurance_expiry DATE,
            prequalification_status VARCHAR(50),
            performance_rating DECIMAL(3,2), -- 1.00 to 5.00
            projects_completed INTEGER DEFAULT 0,
            current_projects TEXT[], -- Array of project IDs
            certifications TEXT[],
            safety_record JSONB,
            financial_info JSONB,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            active BOOLEAN DEFAULT TRUE
        );
        
        CREATE INDEX IF NOT EXISTS idx_subcontractors_trade ON subcontractors(trade_specialty);
        CREATE INDEX IF NOT EXISTS idx_subcontractors_status ON subcontractors(prequalification_status);
        """
    
    def create_inspections_table(self) -> str:
        """Building inspections table"""
        return """
        CREATE TABLE IF NOT EXISTS building_inspections (
            inspection_id VARCHAR(50) PRIMARY KEY,
            project_id VARCHAR(50) REFERENCES projects(project_id),
            inspection_type VARCHAR(100) NOT NULL,
            inspector_name VARCHAR(200),
            inspector_agency VARCHAR(200),
            scheduled_date DATE,
            completed_date TIMESTAMP,
            status VARCHAR(50) DEFAULT 'scheduled',
            result VARCHAR(50),
            permit_number VARCHAR(100),
            location VARCHAR(300),
            inspection_items JSONB,
            violations TEXT[],
            corrections_required TEXT[],
            reinspection_required BOOLEAN DEFAULT FALSE,
            reinspection_date DATE,
            fees DECIMAL(10,2),
            notes TEXT,
            documents TEXT[],
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_building_inspections_project ON building_inspections(project_id);
        CREATE INDEX IF NOT EXISTS idx_building_inspections_type ON building_inspections(inspection_type);
        CREATE INDEX IF NOT EXISTS idx_building_inspections_status ON building_inspections(status);
        """
    
    def create_issues_risks_table(self) -> str:
        """Issues and risks management table"""
        return """
        CREATE TABLE IF NOT EXISTS issues_risks (
            item_id VARCHAR(50) PRIMARY KEY,
            project_id VARCHAR(50) REFERENCES projects(project_id),
            item_type VARCHAR(20) NOT NULL, -- 'issue' or 'risk'
            title VARCHAR(300) NOT NULL,
            description TEXT,
            category VARCHAR(100),
            severity VARCHAR(20),
            probability VARCHAR(20), -- For risks
            impact_cost DECIMAL(12,2),
            impact_schedule_days INTEGER,
            status VARCHAR(50) DEFAULT 'open',
            identified_by VARCHAR(50) REFERENCES users(user_id),
            assigned_to VARCHAR(50) REFERENCES users(user_id),
            identified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            target_resolution_date DATE,
            actual_resolution_date TIMESTAMP,
            mitigation_plan TEXT,
            mitigation_actions TEXT[],
            lessons_learned TEXT,
            related_items TEXT[], -- Related issue/risk IDs
            attachments TEXT[],
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT valid_item_type CHECK (item_type IN ('issue', 'risk')),
            CONSTRAINT valid_severity CHECK (severity IN ('low', 'medium', 'high', 'critical')),
            CONSTRAINT valid_status CHECK (status IN ('open', 'in_progress', 'resolved', 'closed', 'on_hold'))
        );
        
        CREATE INDEX IF NOT EXISTS idx_issues_risks_project ON issues_risks(project_id);
        CREATE INDEX IF NOT EXISTS idx_issues_risks_type ON issues_risks(item_type);
        CREATE INDEX IF NOT EXISTS idx_issues_risks_status ON issues_risks(status);
        """
    
    def create_documents_table(self) -> str:
        """Documents management table"""
        return """
        CREATE TABLE IF NOT EXISTS documents (
            document_id VARCHAR(50) PRIMARY KEY,
            project_id VARCHAR(50) REFERENCES projects(project_id),
            filename VARCHAR(300) NOT NULL,
            file_path TEXT NOT NULL,
            file_type VARCHAR(20),
            file_size_mb DECIMAL(8,2),
            document_type VARCHAR(100),
            category VARCHAR(100),
            version VARCHAR(20) DEFAULT '1.0',
            status VARCHAR(50) DEFAULT 'current',
            title TEXT,
            description TEXT,
            author_id VARCHAR(50) REFERENCES users(user_id),
            uploaded_by VARCHAR(50) REFERENCES users(user_id),
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            review_date TIMESTAMP,
            approved_date TIMESTAMP,
            expiry_date DATE,
            tags TEXT[],
            access_level VARCHAR(20) DEFAULT 'project', -- 'public', 'project', 'restricted'
            download_count INTEGER DEFAULT 0,
            metadata JSONB,
            checksum VARCHAR(64), -- File integrity check
            CONSTRAINT valid_status CHECK (status IN ('draft', 'under_review', 'current', 'superseded', 'archived'))
        );
        
        CREATE INDEX IF NOT EXISTS idx_documents_project ON documents(project_id);
        CREATE INDEX IF NOT EXISTS idx_documents_type ON documents(document_type);
        CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);
        """
    
    def create_cost_management_table(self) -> str:
        """Cost management and budget tracking table"""
        return """
        CREATE TABLE IF NOT EXISTS cost_items (
            cost_id VARCHAR(50) PRIMARY KEY,
            project_id VARCHAR(50) REFERENCES projects(project_id),
            cost_code VARCHAR(50),
            description TEXT NOT NULL,
            category VARCHAR(100),
            budget_amount DECIMAL(15,2),
            committed_amount DECIMAL(15,2) DEFAULT 0,
            actual_amount DECIMAL(15,2) DEFAULT 0,
            forecast_amount DECIMAL(15,2),
            variance_amount DECIMAL(15,2) GENERATED ALWAYS AS (actual_amount - budget_amount) STORED,
            unit_of_measure VARCHAR(20),
            quantity DECIMAL(10,2),
            unit_cost DECIMAL(10,2),
            responsible_party VARCHAR(50) REFERENCES users(user_id),
            vendor_supplier VARCHAR(200),
            purchase_order VARCHAR(100),
            invoice_number VARCHAR(100),
            payment_status VARCHAR(50) DEFAULT 'pending',
            transaction_date DATE,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_cost_items_project ON cost_items(project_id);
        CREATE INDEX IF NOT EXISTS idx_cost_items_category ON cost_items(category);
        CREATE INDEX IF NOT EXISTS idx_cost_items_code ON cost_items(cost_code);
        """
    
    def create_audit_logs_table(self) -> str:
        """Audit logs for tracking all system changes"""
        return """
        CREATE TABLE IF NOT EXISTS audit_logs (
            log_id SERIAL PRIMARY KEY,
            user_id VARCHAR(50) REFERENCES users(user_id),
            action VARCHAR(100) NOT NULL,
            table_name VARCHAR(100),
            record_id VARCHAR(50),
            old_values JSONB,
            new_values JSONB,
            ip_address INET,
            user_agent TEXT,
            session_id VARCHAR(100),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_audit_logs_user ON audit_logs(user_id);
        CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);
        CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);
        CREATE INDEX IF NOT EXISTS idx_audit_logs_table ON audit_logs(table_name);
        """

# Initialize database manager
db_manager = DatabaseManager()
schema_manager = SchemaManager()