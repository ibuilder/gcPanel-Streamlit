"""
PostgreSQL Database Connection Manager for gcPanel
Handles database connections, initialization, and operations
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.database_url = os.getenv('DATABASE_URL')
        
    def get_connection(self):
        """Get database connection"""
        if not self.database_url or self.database_url.startswith('https://'):
            logger.warning("Invalid database URL format. Database functionality disabled.")
            return None
            
        if self.connection is None or self.connection.closed:
            try:
                self.connection = psycopg2.connect(
                    self.database_url,
                    cursor_factory=RealDictCursor
                )
                self.connection.autocommit = True
                logger.info("Database connection established")
            except Exception as e:
                logger.error(f"Failed to connect to database: {e}")
                return None
        return self.connection
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute a SELECT query and return results"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return []
    
    def execute_command(self, command: str, params: tuple = None) -> bool:
        """Execute INSERT/UPDATE/DELETE commands"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(command, params)
                return True
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return False
    
    def initialize_schema(self):
        """Initialize database schema"""
        schema_commands = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                role VARCHAR(50) DEFAULT 'user',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP WITH TIME ZONE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                location VARCHAR(255),
                start_date DATE,
                end_date DATE,
                budget DECIMAL(15, 2),
                status VARCHAR(50) DEFAULT 'active',
                project_manager_id INTEGER REFERENCES users(id),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS daily_reports (
                id SERIAL PRIMARY KEY,
                project_id INTEGER REFERENCES projects(id),
                report_date DATE NOT NULL,
                weather VARCHAR(50),
                temperature INTEGER,
                wind VARCHAR(50),
                crew_size INTEGER,
                work_performed TEXT,
                issues_delays TEXT,
                tomorrow_plan TEXT,
                safety_incidents INTEGER DEFAULT 0,
                inspections TEXT,
                materials_delivered TEXT,
                created_by INTEGER REFERENCES users(id),
                status VARCHAR(50) DEFAULT 'active',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            INSERT INTO projects (id, name, description, location, start_date, end_date, budget, status) 
            VALUES (1, 'Highland Tower Development', 'Mixed-use development with residential and commercial spaces', 
                    'Downtown Highland District', '2024-01-15', '2026-03-30', 45500000.00, 'active')
            ON CONFLICT (id) DO NOTHING
            """,
            """
            INSERT INTO users (id, username, password_hash, email, first_name, last_name, role) 
            VALUES (1, 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 
                    'admin@highland-tower.com', 'Admin', 'User', 'admin')
            ON CONFLICT (username) DO NOTHING
            """
        ]
        
        for command in schema_commands:
            self.execute_command(command)
        
        logger.info("Database schema initialized")
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and not self.connection.closed:
            self.connection.close()
            logger.info("Database connection closed")

# Global database manager instance
@st.cache_resource
def get_db_manager():
    """Get cached database manager instance"""
    db_manager = DatabaseManager()
    db_manager.initialize_schema()
    return db_manager

# Database operation functions
def save_daily_report(report_data: Dict) -> bool:
    """Save daily report to database"""
    db = get_db_manager()
    
    query = """
    INSERT INTO daily_reports (project_id, report_date, weather, temperature, wind, 
                              crew_size, work_performed, issues_delays, tomorrow_plan, 
                              safety_incidents, inspections, materials_delivered, created_by, status)
    VALUES (1, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1, 'active')
    """
    
    params = (
        report_data['date'],
        report_data['weather'],
        report_data['temperature'],
        report_data['wind'],
        report_data['crew_size'],
        report_data['work_performed'],
        report_data['issues_delays'],
        report_data['tomorrow_plan'],
        report_data['safety_incidents'],
        report_data['inspections'],
        report_data['materials_delivered']
    )
    
    return db.execute_command(query, params)

def get_daily_reports() -> List[Dict]:
    """Get all daily reports from database"""
    db = get_db_manager()
    
    query = """
    SELECT dr.*, u.username as created_by_name 
    FROM daily_reports dr
    LEFT JOIN users u ON dr.created_by = u.id
    WHERE dr.project_id = 1
    ORDER BY dr.report_date DESC
    """
    
    return db.execute_query(query)

def authenticate_user(username: str, password_hash: str) -> Optional[Dict]:
    """Authenticate user against database"""
    db = get_db_manager()
    
    query = """
    SELECT id, username, email, first_name, last_name, role
    FROM users 
    WHERE username = %s AND password_hash = %s
    """
    
    results = db.execute_query(query, (username, password_hash))
    return results[0] if results else None

def update_user_login(user_id: int):
    """Update user last login timestamp"""
    db = get_db_manager()
    
    query = """
    UPDATE users 
    SET last_login = CURRENT_TIMESTAMP 
    WHERE id = %s
    """
    
    return db.execute_command(query, (user_id,))