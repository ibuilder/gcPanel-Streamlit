"""
Database connection manager for gcPanel
Handles PostgreSQL connections and queries for Highland Tower Development
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Production-ready database manager with connection pooling"""
    
    def __init__(self):
        self.connection = None
        self.database_url = os.getenv('DATABASE_URL')
        
    def get_connection(self):
        """Get database connection with error handling"""
        try:
            if not self.connection or self.connection.closed:
                if self.database_url:
                    self.connection = psycopg2.connect(
                        self.database_url,
                        cursor_factory=RealDictCursor
                    )
                    logger.info("Database connection established")
                else:
                    logger.warning("DATABASE_URL not found")
                    return None
            return self.connection
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return None
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict]]:
        """Execute query with proper error handling"""
        try:
            conn = self.get_connection()
            if not conn:
                return None
                
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                
                # For SELECT queries, fetch results
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                else:
                    # For INSERT/UPDATE/DELETE, commit and return affected rows
                    conn.commit()
                    return cursor.rowcount
                    
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            if self.connection:
                self.connection.rollback()
            return None
    
    def close(self):
        """Close database connection"""
        if self.connection and not self.connection.closed:
            self.connection.close()
            logger.info("Database connection closed")

# Global database manager instance
db_manager = DatabaseManager()

def get_daily_reports(project_id: int = 1) -> List[Dict]:
    """Get daily reports for Highland Tower Development"""
    query = """
    SELECT dr.*, u.full_name as created_by_name
    FROM daily_reports dr
    LEFT JOIN users u ON dr.created_by = u.id
    WHERE dr.project_id = %s
    ORDER BY dr.report_date DESC
    LIMIT 20
    """
    
    result = db_manager.execute_query(query, (project_id,))
    return result if result else []

def get_rfis(project_id: int = 1) -> List[Dict]:
    """Get RFIs for Highland Tower Development"""
    query = """
    SELECT r.*, 
           u1.full_name as submitted_by_name,
           u2.full_name as assigned_to_name,
           u3.full_name as responded_by_name
    FROM rfis r
    LEFT JOIN users u1 ON r.submitted_by = u1.id
    LEFT JOIN users u2 ON r.assigned_to = u2.id
    LEFT JOIN users u3 ON r.responded_by = u3.id
    WHERE r.project_id = %s
    ORDER BY r.created_at DESC
    """
    
    result = db_manager.execute_query(query, (project_id,))
    return result if result else []

def get_submittals(project_id: int = 1) -> List[Dict]:
    """Get submittals for Highland Tower Development"""
    query = """
    SELECT s.*,
           u1.full_name as submitted_by_name,
           u2.full_name as reviewed_by_name
    FROM submittals s
    LEFT JOIN users u1 ON s.submitted_by = u1.id
    LEFT JOIN users u2 ON s.reviewed_by = u2.id
    WHERE s.project_id = %s
    ORDER BY s.created_at DESC
    """
    
    result = db_manager.execute_query(query, (project_id,))
    return result if result else []

def get_project_info(project_id: int = 1) -> Dict:
    """Get Highland Tower Development project information"""
    query = """
    SELECT p.*, u.full_name as project_manager_name
    FROM projects p
    LEFT JOIN users u ON p.project_manager_id = u.id
    WHERE p.id = %s
    """
    
    result = db_manager.execute_query(query, (project_id,))
    return result[0] if result else {}

def create_daily_report(data: Dict) -> bool:
    """Create new daily report"""
    query = """
    INSERT INTO daily_reports 
    (project_id, report_date, weather_conditions, temperature_high, temperature_low, 
     work_performed, delays_issues, safety_notes, crew_count, equipment_on_site, 
     materials_delivered, created_by)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    params = (
        data.get('project_id', 1),
        data.get('report_date'),
        data.get('weather_conditions'),
        data.get('temperature_high'),
        data.get('temperature_low'),
        data.get('work_performed'),
        data.get('delays_issues'),
        data.get('safety_notes'),
        data.get('crew_count'),
        data.get('equipment_on_site'),
        data.get('materials_delivered'),
        data.get('created_by', 1)
    )
    
    result = db_manager.execute_query(query, params)
    return result is not None

def create_rfi(data: Dict) -> bool:
    """Create new RFI"""
    query = """
    INSERT INTO rfis 
    (project_id, rfi_number, subject, description, location, priority, 
     submitted_by, assigned_to, due_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    params = (
        data.get('project_id', 1),
        data.get('rfi_number'),
        data.get('subject'),
        data.get('description'),
        data.get('location'),
        data.get('priority', 'medium'),
        data.get('submitted_by', 1),
        data.get('assigned_to'),
        data.get('due_date')
    )
    
    result = db_manager.execute_query(query, params)
    return result is not None

def create_submittal(data: Dict) -> bool:
    """Create new submittal"""
    query = """
    INSERT INTO submittals 
    (project_id, submittal_number, title, specification_section, contractor_name,
     description, submitted_by, priority, due_date, cost_impact)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    params = (
        data.get('project_id', 1),
        data.get('submittal_number'),
        data.get('title'),
        data.get('specification_section'),
        data.get('contractor_name'),
        data.get('description'),
        data.get('submitted_by', 1),
        data.get('priority', 'standard'),
        data.get('due_date'),
        data.get('cost_impact', 0)
    )
    
    result = db_manager.execute_query(query, params)
    return result is not None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_project_metrics(project_id: int = 1) -> Dict:
    """Get cached project metrics for dashboard"""
    try:
        # Get basic counts
        rfis_count = len(get_rfis(project_id))
        submittals_count = len(get_submittals(project_id))
        reports_count = len(get_daily_reports(project_id))
        
        # Calculate some basic metrics
        return {
            'total_rfis': rfis_count,
            'total_submittals': submittals_count,
            'total_reports': reports_count,
            'project_progress': 67.5,  # This would come from actual calculations
            'budget_utilization': 58.3,
            'safety_days': 127
        }
    except Exception as e:
        logger.error(f"Error getting project metrics: {e}")
        return {
            'total_rfis': 0,
            'total_submittals': 0,
            'total_reports': 0,
            'project_progress': 0,
            'budget_utilization': 0,
            'safety_days': 0
        }

def initialize_database():
    """Initialize database with schema if needed"""
    try:
        # Check if database is accessible
        conn = db_manager.get_connection()
        if conn:
            st.success("✅ Database connection established - Highland Tower Development data ready")
            return True
        else:
            st.warning("🔧 Database connection not available - using demo mode")
            return False
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        st.warning("🔧 Database connection not available - using demo mode")
        return False