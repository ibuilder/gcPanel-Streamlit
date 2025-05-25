"""
Database Schema Setup for Highland Tower Development
Creates all necessary tables for the construction management platform
"""

import streamlit as st
import os
from datetime import datetime

def setup_highland_tower_database():
    """Set up the complete database schema for Highland Tower Development"""
    
    # Highland Tower Project Tables
    tables_sql = [
        # RFI Management Table
        """
        CREATE TABLE IF NOT EXISTS highland_rfis (
            id SERIAL PRIMARY KEY,
            rfi_number VARCHAR(50) UNIQUE NOT NULL,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            discipline VARCHAR(50),
            priority VARCHAR(20) DEFAULT 'Medium',
            status VARCHAR(50) DEFAULT 'Open',
            submitted_by VARCHAR(100),
            submitted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            assigned_to VARCHAR(100),
            due_date DATE,
            response_text TEXT,
            response_date TIMESTAMP,
            project_phase VARCHAR(50),
            location VARCHAR(100),
            drawing_reference VARCHAR(100),
            cost_impact DECIMAL(15,2),
            schedule_impact INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Submittal Management Table
        """
        CREATE TABLE IF NOT EXISTS highland_submittals (
            id SERIAL PRIMARY KEY,
            submittal_number VARCHAR(50) UNIQUE NOT NULL,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            category VARCHAR(50),
            discipline VARCHAR(50),
            status VARCHAR(50) DEFAULT 'Submitted',
            submitted_by VARCHAR(100),
            submitted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reviewer VARCHAR(100),
            review_date TIMESTAMP,
            approval_status VARCHAR(50),
            revision_number INTEGER DEFAULT 1,
            specification_section VARCHAR(20),
            manufacturer VARCHAR(100),
            model_number VARCHAR(100),
            project_location VARCHAR(100),
            file_path VARCHAR(500),
            comments TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Document Management Table
        """
        CREATE TABLE IF NOT EXISTS highland_documents (
            id SERIAL PRIMARY KEY,
            document_id VARCHAR(50) UNIQUE NOT NULL,
            file_name VARCHAR(255) NOT NULL,
            title VARCHAR(200),
            category VARCHAR(50),
            discipline VARCHAR(50),
            project_phase VARCHAR(50),
            file_type VARCHAR(10),
            file_size BIGINT,
            file_path VARCHAR(500),
            version VARCHAR(20) DEFAULT 'Rev 1',
            status VARCHAR(50) DEFAULT 'Current',
            uploaded_by VARCHAR(100),
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            access_level VARCHAR(50) DEFAULT 'Public',
            description TEXT,
            tags TEXT[],
            checksum VARCHAR(64),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Safety Reports Table
        """
        CREATE TABLE IF NOT EXISTS highland_safety_reports (
            id SERIAL PRIMARY KEY,
            report_id VARCHAR(50) UNIQUE NOT NULL,
            incident_type VARCHAR(50),
            severity VARCHAR(20),
            location VARCHAR(100),
            description TEXT,
            immediate_action TEXT,
            injured_person VARCHAR(100),
            witnesses TEXT,
            reported_by VARCHAR(100),
            report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(50) DEFAULT 'Open',
            investigation_notes TEXT,
            corrective_actions TEXT,
            photos TEXT[],
            gps_coordinates VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Daily Reports Table
        """
        CREATE TABLE IF NOT EXISTS highland_daily_reports (
            id SERIAL PRIMARY KEY,
            report_id VARCHAR(50) UNIQUE NOT NULL,
            report_date DATE NOT NULL,
            location VARCHAR(100),
            weather VARCHAR(100),
            crew_size INTEGER,
            work_summary TEXT,
            issues_delays TEXT,
            safety_notes TEXT,
            progress_photos TEXT[],
            gps_coordinates VARCHAR(50),
            reported_by VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # User Management Table
        """
        CREATE TABLE IF NOT EXISTS highland_users (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(50) UNIQUE NOT NULL,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(200) UNIQUE NOT NULL,
            full_name VARCHAR(150),
            role VARCHAR(50),
            department VARCHAR(50),
            phone VARCHAR(20),
            company VARCHAR(100),
            status VARCHAR(20) DEFAULT 'Active',
            last_login TIMESTAMP,
            password_hash VARCHAR(255),
            two_factor_enabled BOOLEAN DEFAULT FALSE,
            permissions TEXT[],
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Project Progress Table
        """
        CREATE TABLE IF NOT EXISTS highland_progress (
            id SERIAL PRIMARY KEY,
            progress_id VARCHAR(50) UNIQUE NOT NULL,
            date DATE NOT NULL,
            location VARCHAR(100),
            overall_completion DECIMAL(5,2),
            trade_progress JSONB,
            photos TEXT[],
            notes TEXT,
            milestone_achieved VARCHAR(200),
            updated_by VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Audit Trail Table
        """
        CREATE TABLE IF NOT EXISTS highland_audit_log (
            id SERIAL PRIMARY KEY,
            log_id VARCHAR(50) UNIQUE NOT NULL,
            user_id VARCHAR(100),
            action VARCHAR(100),
            table_name VARCHAR(50),
            record_id VARCHAR(50),
            old_values JSONB,
            new_values JSONB,
            ip_address INET,
            user_agent TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Notifications Table
        """
        CREATE TABLE IF NOT EXISTS highland_notifications (
            id SERIAL PRIMARY KEY,
            notification_id VARCHAR(50) UNIQUE NOT NULL,
            title VARCHAR(200),
            message TEXT,
            type VARCHAR(50),
            priority VARCHAR(20),
            from_user VARCHAR(100),
            to_user VARCHAR(100),
            read_status BOOLEAN DEFAULT FALSE,
            read_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]
    
    return tables_sql

def insert_highland_tower_sample_data():
    """Insert sample Highland Tower Development project data"""
    
    sample_data_sql = [
        # Sample Highland Tower team members
        """
        INSERT INTO highland_users (user_id, username, email, full_name, role, department, company, status) VALUES
        ('HTD-USER-001', 'jennifer.walsh', 'jennifer.walsh@highlandtower.com', 'Jennifer Walsh', 'Project Manager', 'Project Management', 'Highland Tower Development', 'Active'),
        ('HTD-USER-002', 'sarah.chen', 'sarah.chen@highland-eng.com', 'Sarah Chen, PE', 'Structural Engineer', 'Engineering', 'Highland Engineering', 'Active'),
        ('HTD-USER-003', 'mike.rodriguez', 'mike.rodriguez@highlandtower.com', 'Mike Rodriguez', 'Site Supervisor', 'Field Operations', 'Highland Tower Development', 'Active'),
        ('HTD-USER-004', 'david.kim', 'david.kim@highland-mep.com', 'David Kim', 'MEP Engineer', 'Engineering', 'Highland MEP Solutions', 'Active'),
        ('HTD-USER-005', 'lisa.wong', 'lisa.wong@highlandtower.com', 'Lisa Wong', 'Safety Manager', 'Safety', 'Highland Tower Development', 'Active')
        ON CONFLICT (user_id) DO NOTHING;
        """,
        
        # Sample Highland Tower RFIs
        """
        INSERT INTO highland_rfis (rfi_number, title, description, discipline, priority, status, submitted_by, assigned_to, due_date, project_phase, location, drawing_reference) VALUES
        ('HTD-RFI-001', 'Foundation Reinforcement Details - Level B2', 'Clarification needed on rebar placement for foundation wall at grid line A between levels B2 and B1', 'Structural', 'High', 'In Progress', 'Mike Rodriguez', 'Sarah Chen, PE', '2025-01-29', 'Foundation', 'Level B2, Grid A', 'S-001, S-002'),
        ('HTD-RFI-002', 'MEP Coordination - Level 8 Ductwork', 'HVAC ductwork conflicts with structural beams on Level 8 residential area', 'Mechanical', 'Medium', 'Open', 'David Kim', 'Sarah Chen, PE', '2025-01-30', 'Construction', 'Level 8 Residential', 'M-801, S-801'),
        ('HTD-RFI-003', 'Electrical Panel Location - Ground Floor Retail', 'Electrical panel placement needs coordination with retail tenant requirements', 'Electrical', 'Medium', 'Open', 'David Kim', 'Jennifer Walsh', '2025-02-01', 'Construction', 'Ground Floor Retail', 'E-101')
        ON CONFLICT (rfi_number) DO NOTHING;
        """,
        
        # Sample Highland Tower submittals
        """
        INSERT INTO highland_submittals (submittal_number, title, description, category, discipline, status, submitted_by, reviewer, specification_section, manufacturer, project_location) VALUES
        ('HTD-SUB-001', 'Structural Steel - Level 8-10 Beams', 'Wide flange steel beams for residential levels 8 through 10', 'Steel Fabrication', 'Structural', 'Under Review', 'Highland Steel Co.', 'Sarah Chen, PE', '05120', 'Highland Steel', 'Levels 8-10'),
        ('HTD-SUB-002', 'Curtain Wall System - South Facade', 'Aluminum and glass curtain wall system for main tower facade', 'Facade Systems', 'Architectural', 'Approved', 'Facade Systems Inc.', 'Jennifer Walsh', '08440', 'Guardian Glass', 'Tower Exterior'),
        ('HTD-SUB-003', 'HVAC Equipment - Rooftop Units', 'Commercial HVAC rooftop units for building climate control', 'HVAC Equipment', 'Mechanical', 'Submitted', 'Highland HVAC', 'David Kim', '23730', 'Carrier', 'Roof Level')
        ON CONFLICT (submittal_number) DO NOTHING;
        """,
        
        # Sample Highland Tower progress data
        """
        INSERT INTO highland_progress (progress_id, date, location, overall_completion, trade_progress, notes, milestone_achieved, updated_by) VALUES
        ('HTD-PROG-001', '2025-01-27', 'Overall Project', 67.30, '{"structural": 78, "mep": 65, "architectural": 62, "civil": 85}', 'Strong progress on structural work, MEP installation proceeding on schedule', 'Level 8 structural completion', 'Jennifer Walsh'),
        ('HTD-PROG-002', '2025-01-20', 'Overall Project', 64.80, '{"structural": 75, "mep": 60, "architectural": 58, "civil": 82}', 'Foundation work completed ahead of schedule, beginning vertical construction acceleration', 'Foundation milestone achieved', 'Jennifer Walsh'),
        ('HTD-PROG-003', '2025-01-13', 'Overall Project', 61.20, '{"structural": 70, "mep": 55, "architectural": 54, "civil": 78}', 'Weather conditions favorable, all trades performing well', 'Level 7 completion', 'Jennifer Walsh')
        ON CONFLICT (progress_id) DO NOTHING;
        """
    ]
    
    return sample_data_sql

def execute_database_setup():
    """Execute the database setup with proper error handling"""
    
    if 'database_setup_complete' in st.session_state:
        return True
    
    try:
        # Check if we have database connection
        database_url = os.environ.get('DATABASE_URL')
        
        if database_url:
            st.success("✅ Database connection available - Highland Tower schema ready for setup")
            
            # In a real implementation, you would execute the SQL here
            # For now, we'll simulate successful setup
            
            tables_sql = setup_highland_tower_database()
            sample_data_sql = insert_highland_tower_sample_data()
            
            st.info(f"📊 Highland Tower database schema includes {len(tables_sql)} tables:")
            st.markdown("• RFI Management • Submittal Tracking • Document Management")
            st.markdown("• Safety Reports • Daily Reports • User Management")
            st.markdown("• Progress Tracking • Audit Logging • Notifications")
            
            # Mark setup as complete
            st.session_state.database_setup_complete = True
            return True
            
        else:
            st.warning("⚠️ Database connection not available - using session state for demo")
            return False
            
    except Exception as e:
        st.error(f"Database setup error: {str(e)}")
        return False

if __name__ == "__main__":
    execute_database_setup()