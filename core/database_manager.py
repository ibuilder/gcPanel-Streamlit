"""
Enterprise Database Manager for gcPanel Highland Tower Development

Provides PostgreSQL integration with connection pooling, migrations,
and enterprise-grade data management capabilities.
"""

import os
import logging
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
import streamlit as st
from datetime import datetime
import json
from typing import Dict, List, Any, Optional

class DatabaseManager:
    """Enterprise database manager with connection pooling and caching"""
    
    def __init__(self):
        self.connection_pool = None
        self.setup_logging()
        self.initialize_connection_pool()
    
    def setup_logging(self):
        """Setup database operation logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/database.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('DatabaseManager')
    
    def initialize_connection_pool(self):
        """Initialize PostgreSQL connection pool"""
        try:
            database_url = os.environ.get('DATABASE_URL')
            if not database_url:
                self.logger.error("DATABASE_URL environment variable not set")
                return
            
            # Create connection pool
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                1, 20,  # min and max connections
                database_url,
                application_name='gcPanel_Highland_Tower'
            )
            
            self.logger.info("Database connection pool initialized successfully")
            self.create_schema()
            
        except Exception as e:
            self.logger.error(f"Failed to initialize database connection pool: {e}")
            st.error("Database connection failed. Please check configuration.")
    
    @contextmanager
    def get_connection(self):
        """Get database connection from pool"""
        connection = None
        try:
            connection = self.connection_pool.getconn()
            yield connection
        except Exception as e:
            if connection:
                connection.rollback()
            self.logger.error(f"Database operation failed: {e}")
            raise
        finally:
            if connection:
                self.connection_pool.putconn(connection)
    
    def create_schema(self):
        """Create comprehensive database schema for Highland Tower Development"""
        schema_sql = """
        -- Projects table
        CREATE TABLE IF NOT EXISTS projects (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            status VARCHAR(50) DEFAULT 'Active',
            start_date DATE,
            end_date DATE,
            budget DECIMAL(15,2),
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Users and roles
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255),
            role VARCHAR(50) DEFAULT 'User',
            project_id INTEGER REFERENCES projects(id),
            active BOOLEAN DEFAULT TRUE,
            last_login TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- RFIs table
        CREATE TABLE IF NOT EXISTS rfis (
            id SERIAL PRIMARY KEY,
            rfi_number VARCHAR(50) UNIQUE NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            submitter_id INTEGER REFERENCES users(id),
            assigned_to_id INTEGER REFERENCES users(id),
            project_id INTEGER REFERENCES projects(id),
            status VARCHAR(50) DEFAULT 'Open',
            priority VARCHAR(20) DEFAULT 'Medium',
            submitted_date DATE,
            response_due_date DATE,
            response_date DATE,
            response TEXT,
            drawing_references TEXT,
            spec_references TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Daily Reports
        CREATE TABLE IF NOT EXISTS daily_reports (
            id SERIAL PRIMARY KEY,
            report_date DATE NOT NULL,
            project_id INTEGER REFERENCES projects(id),
            foreman_id INTEGER REFERENCES users(id),
            weather_conditions VARCHAR(100),
            temperature VARCHAR(20),
            wind_conditions VARCHAR(100),
            total_workers INTEGER DEFAULT 0,
            work_completed TEXT,
            materials_received TEXT,
            equipment_used TEXT,
            safety_notes TEXT,
            issues_concerns TEXT,
            created_by INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Quality Control
        CREATE TABLE IF NOT EXISTS quality_checks (
            id SERIAL PRIMARY KEY,
            check_number VARCHAR(50) UNIQUE NOT NULL,
            check_type VARCHAR(100) NOT NULL,
            location VARCHAR(255),
            inspector_id INTEGER REFERENCES users(id),
            project_id INTEGER REFERENCES projects(id),
            status VARCHAR(50) DEFAULT 'Scheduled',
            priority VARCHAR(20) DEFAULT 'Medium',
            scheduled_date TIMESTAMP,
            completed_date TIMESTAMP,
            result VARCHAR(50),
            notes TEXT,
            standard_reference VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Clash Detection
        CREATE TABLE IF NOT EXISTS clashes (
            id SERIAL PRIMARY KEY,
            clash_number VARCHAR(50) UNIQUE NOT NULL,
            description TEXT NOT NULL,
            location VARCHAR(255),
            project_id INTEGER REFERENCES projects(id),
            priority VARCHAR(20) DEFAULT 'Medium',
            status VARCHAR(50) DEFAULT 'Open',
            disciplines VARCHAR(100),
            assigned_to_id INTEGER REFERENCES users(id),
            date_found DATE,
            date_resolved DATE,
            resolution TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Resources Management
        CREATE TABLE IF NOT EXISTS personnel (
            id SERIAL PRIMARY KEY,
            employee_id VARCHAR(50) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            trade VARCHAR(100),
            crew VARCHAR(50),
            status VARCHAR(50) DEFAULT 'Active',
            hourly_rate DECIMAL(8,2),
            certification_status VARCHAR(50),
            safety_rating VARCHAR(10),
            contact_info JSONB,
            project_id INTEGER REFERENCES projects(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS equipment (
            id SERIAL PRIMARY KEY,
            equipment_id VARCHAR(50) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            type VARCHAR(100),
            status VARCHAR(50) DEFAULT 'Available',
            location VARCHAR(255),
            operator_id INTEGER REFERENCES personnel(id),
            daily_rate DECIMAL(10,2),
            maintenance_due DATE,
            project_id INTEGER REFERENCES projects(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS materials (
            id SERIAL PRIMARY KEY,
            material_id VARCHAR(50) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            quantity VARCHAR(100),
            unit VARCHAR(50),
            status VARCHAR(50) DEFAULT 'Ordered',
            supplier VARCHAR(255),
            delivery_date DATE,
            location VARCHAR(255),
            cost DECIMAL(12,2),
            quality_check VARCHAR(50),
            project_id INTEGER REFERENCES projects(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Audit logging
        CREATE TABLE IF NOT EXISTS audit_log (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            action VARCHAR(100) NOT NULL,
            table_name VARCHAR(100),
            record_id INTEGER,
            old_values JSONB,
            new_values JSONB,
            ip_address INET,
            user_agent TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Notifications
        CREATE TABLE IF NOT EXISTS notifications (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            title VARCHAR(255) NOT NULL,
            message TEXT,
            type VARCHAR(50) DEFAULT 'info',
            read BOOLEAN DEFAULT FALSE,
            action_url VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create indexes for performance
        CREATE INDEX IF NOT EXISTS idx_rfis_project ON rfis(project_id);
        CREATE INDEX IF NOT EXISTS idx_rfis_status ON rfis(status);
        CREATE INDEX IF NOT EXISTS idx_daily_reports_date ON daily_reports(report_date);
        CREATE INDEX IF NOT EXISTS idx_quality_checks_project ON quality_checks(project_id);
        CREATE INDEX IF NOT EXISTS idx_clashes_project ON clashes(project_id);
        CREATE INDEX IF NOT EXISTS idx_audit_log_user ON audit_log(user_id);
        CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log(timestamp);
        """
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(schema_sql)
                    conn.commit()
                    self.logger.info("Database schema created successfully")
                    self.seed_initial_data(conn)
        except Exception as e:
            self.logger.error(f"Failed to create database schema: {e}")
    
    def seed_initial_data(self, conn):
        """Seed initial data for Highland Tower Development"""
        try:
            with conn.cursor() as cursor:
                # Insert Highland Tower Development project
                cursor.execute("""
                    INSERT INTO projects (name, description, status, budget, location)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (
                    'Highland Tower Development',
                    'Mixed-use development with 120 residential and 8 retail units',
                    'Active',
                    45500000.00,
                    'Highland District, Downtown'
                ))
                
                # Insert sample users
                sample_users = [
                    ('admin', 'admin@highland-tower.com', 'Project Manager'),
                    ('john_smith', 'john.smith@highland-tower.com', 'Superintendent'),
                    ('sarah_chen', 'sarah.chen@highland-tower.com', 'Quality Inspector'),
                    ('mike_rodriguez', 'mike.rodriguez@highland-tower.com', 'Safety Manager')
                ]
                
                for username, email, role in sample_users:
                    cursor.execute("""
                        INSERT INTO users (username, email, role)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (username) DO NOTHING
                    """, (username, email, role))
                
                conn.commit()
                self.logger.info("Initial data seeded successfully")
                
        except Exception as e:
            self.logger.error(f"Failed to seed initial data: {e}")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute query and return results"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    
                    if cursor.description:
                        columns = [desc[0] for desc in cursor.description]
                        results = cursor.fetchall()
                        return [dict(zip(columns, row)) for row in results]
                    else:
                        conn.commit()
                        return []
                        
        except Exception as e:
            self.logger.error(f"Query execution failed: {e}")
            raise
    
    def log_user_action(self, user_id: int, action: str, table_name: str = None, 
                       record_id: int = None, old_values: Dict = None, 
                       new_values: Dict = None):
        """Log user actions for audit trail"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO audit_log (user_id, action, table_name, record_id, 
                                             old_values, new_values, timestamp)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        user_id, action, table_name, record_id,
                        json.dumps(old_values) if old_values else None,
                        json.dumps(new_values) if new_values else None,
                        datetime.now()
                    ))
                    conn.commit()
        except Exception as e:
            self.logger.error(f"Failed to log user action: {e}")

# Initialize global database manager
@st.cache_resource
def get_database_manager():
    """Get cached database manager instance"""
    return DatabaseManager()