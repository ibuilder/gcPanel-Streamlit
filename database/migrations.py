"""
Database Migrations for Highland Tower Development
PostgreSQL Standard Implementation
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
from datetime import datetime

def get_db_connection():
    """Get standardized PostgreSQL connection for Highland Tower Development"""
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            st.error("🔴 Database connection required for Highland Tower Development")
            return None
            
        conn = psycopg2.connect(
            database_url,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        st.error(f"🔴 Highland Tower database connection failed: {str(e)}")
        return None

def create_highland_tower_tables():
    """Create standardized Highland Tower Development tables"""
    
    conn = get_db_connection()
    if not conn:
        return False
        
    try:
        cursor = conn.cursor()
        
        # Projects table for Highland Tower Development
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                project_value DECIMAL(12, 2),
                completion_percentage DECIMAL(5, 2),
                start_date DATE,
                end_date DATE,
                status VARCHAR(50) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Cost management table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cost_management (
                id SERIAL PRIMARY KEY,
                project_id INTEGER REFERENCES projects(id),
                total_budget DECIMAL(12, 2),
                spent_to_date DECIMAL(12, 2),
                committed_costs DECIMAL(12, 2),
                forecast_variance DECIMAL(12, 2),
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # RFIs table for Engineering module
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rfis (
                id SERIAL PRIMARY KEY,
                project_id INTEGER REFERENCES projects(id),
                rfi_number VARCHAR(50) UNIQUE,
                title VARCHAR(255),
                description TEXT,
                status VARCHAR(50) DEFAULT 'open',
                priority VARCHAR(20) DEFAULT 'medium',
                submitted_by VARCHAR(100),
                assigned_to VARCHAR(100),
                date_submitted DATE DEFAULT CURRENT_DATE,
                date_response_due DATE,
                date_responded DATE,
                response_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Daily reports table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_reports (
                id SERIAL PRIMARY KEY,
                project_id INTEGER REFERENCES projects(id),
                report_date DATE DEFAULT CURRENT_DATE,
                weather_conditions VARCHAR(100),
                crew_count INTEGER,
                work_performed TEXT,
                safety_notes TEXT,
                delays_issues TEXT,
                submitted_by VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Safety incidents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS safety_incidents (
                id SERIAL PRIMARY KEY,
                project_id INTEGER REFERENCES projects(id),
                incident_date DATE DEFAULT CURRENT_DATE,
                incident_type VARCHAR(100),
                description TEXT,
                severity VARCHAR(20),
                injured_person VARCHAR(100),
                immediate_action TEXT,
                investigation_status VARCHAR(50) DEFAULT 'pending',
                reported_by VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Quality control inspections
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quality_inspections (
                id SERIAL PRIMARY KEY,
                project_id INTEGER REFERENCES projects(id),
                inspection_date DATE DEFAULT CURRENT_DATE,
                area_inspected VARCHAR(255),
                inspection_type VARCHAR(100),
                status VARCHAR(20), -- pass, fail, conditional
                defects_found INTEGER DEFAULT 0,
                inspector_name VARCHAR(100),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Document management
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                project_id INTEGER REFERENCES projects(id),
                document_name VARCHAR(255),
                document_type VARCHAR(100),
                file_path VARCHAR(500),
                uploaded_by VARCHAR(100),
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                version_number INTEGER DEFAULT 1,
                status VARCHAR(50) DEFAULT 'active'
            );
        """)
        
        # Progress photos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress_photos (
                id SERIAL PRIMARY KEY,
                project_id INTEGER REFERENCES projects(id),
                photo_date DATE DEFAULT CURRENT_DATE,
                location VARCHAR(255),
                gps_coordinates VARCHAR(100),
                description TEXT,
                file_path VARCHAR(500),
                photographer VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Owner billing (AIA G702/G703)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS owner_bills (
                id SERIAL PRIMARY KEY,
                project_id INTEGER REFERENCES projects(id),
                application_number INTEGER,
                period_ending DATE,
                total_contract_amount DECIMAL(12, 2),
                work_completed_to_date DECIMAL(12, 2),
                less_retainage DECIMAL(12, 2),
                amount_due DECIMAL(12, 2),
                status VARCHAR(50) DEFAULT 'draft',
                digital_signature_data TEXT,
                signed_by VARCHAR(100),
                signed_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        st.error(f"🔴 Highland Tower table creation failed: {str(e)}")
        return False

def insert_highland_tower_sample_data():
    """Insert Highland Tower Development sample data"""
    
    conn = get_db_connection()
    if not conn:
        return False
        
    try:
        cursor = conn.cursor()
        
        # Insert Highland Tower project
        cursor.execute("""
            INSERT INTO projects (name, project_value, completion_percentage, status)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, ("Highland Tower Development", 45500000.00, 67.3, "active"))
        
        # Get project ID
        cursor.execute("SELECT id FROM projects WHERE name = %s", ("Highland Tower Development",))
        project_result = cursor.fetchone()
        
        if project_result:
            project_id = project_result['id']
            
            # Insert cost data
            cursor.execute("""
                INSERT INTO cost_management (project_id, total_budget, spent_to_date, committed_costs, forecast_variance)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, (project_id, 45500000.00, 28650000.00, 14200000.00, -2100000.00))
            
            # Insert sample RFIs
            sample_rfis = [
                ("HTD-RFI-001", "MEP Coordination Level 12", "Clarification needed on HVAC routing in mechanical room", "open", "high"),
                ("HTD-RFI-002", "Structural Connection Detail", "Steel beam connection detail at grid line B-5", "in_review", "medium"),
                ("HTD-RFI-003", "Facade Panel Installation", "Window wall attachment method for north elevation", "responded", "low")
            ]
            
            for rfi_number, title, description, status, priority in sample_rfis:
                cursor.execute("""
                    INSERT INTO rfis (project_id, rfi_number, title, description, status, priority, submitted_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (rfi_number) DO NOTHING;
                """, (project_id, rfi_number, title, description, status, priority, "Project Engineer"))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        st.error(f"🔴 Highland Tower sample data insertion failed: {str(e)}")
        return False

def run_migration():
    """Run complete Highland Tower Development migration"""
    
    st.info("🔄 Running Highland Tower Development database migration...")
    
    # Create tables
    if create_highland_tower_tables():
        st.success("✅ Highland Tower tables created successfully")
        
        # Insert sample data
        if insert_highland_tower_sample_data():
            st.success("✅ Highland Tower sample data inserted successfully")
            st.info("🏗️ Highland Tower Development database is ready for production!")
            return True
        else:
            st.warning("⚠️ Tables created but sample data insertion failed")
            return False
    else:
        st.error("🔴 Highland Tower table creation failed")
        return False

def get_project_data():
    """Get Highland Tower project data with PostgreSQL standard queries"""
    
    conn = get_db_connection()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor()
        
        # Get project info
        cursor.execute("""
            SELECT p.*, c.total_budget, c.spent_to_date, c.forecast_variance
            FROM projects p
            LEFT JOIN cost_management c ON p.id = c.project_id
            WHERE p.name = %s
        """, ("Highland Tower Development",))
        
        project_data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return dict(project_data) if project_data else None
        
    except Exception as e:
        st.error(f"🔴 Highland Tower data retrieval failed: {str(e)}")
        return None

def get_active_rfis():
    """Get active RFIs for Highland Tower with PostgreSQL queries"""
    
    conn = get_db_connection()
    if not conn:
        return []
        
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT r.*, p.name as project_name
            FROM rfis r
            JOIN projects p ON r.project_id = p.id
            WHERE p.name = %s AND r.status IN (%s, %s)
            ORDER BY r.date_submitted DESC
        """, ("Highland Tower Development", "open", "in_review"))
        
        rfis = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [dict(rfi) for rfi in rfis]
        
    except Exception as e:
        st.error(f"🔴 Highland Tower RFI retrieval failed: {str(e)}")
        return []

def save_owner_bill_signature(bill_id, signature_data, signed_by):
    """Save digital signature for owner bill with PostgreSQL"""
    
    conn = get_db_connection()
    if not conn:
        return False
        
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE owner_bills 
            SET digital_signature_data = %s, 
                signed_by = %s, 
                signed_date = %s,
                status = %s
            WHERE id = %s
        """, (signature_data, signed_by, datetime.now(), "signed", bill_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        st.error(f"🔴 Highland Tower signature save failed: {str(e)}")
        return False

if __name__ == "__main__":
    run_migration()