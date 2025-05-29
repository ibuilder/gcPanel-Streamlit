"""
Highland Tower Development - Production Data Management System
Real-time data handling with PostgreSQL integration and performance optimization
"""

import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

class HighlandDataManager:
    """Production data manager for Highland Tower Development project"""
    
    def __init__(self):
        self.connection = None
        self.connect_database()
    
    def connect_database(self):
        """Connect to production PostgreSQL database"""
        try:
            database_url = os.getenv('DATABASE_URL')
            if database_url:
                self.connection = psycopg2.connect(
                    database_url,
                    cursor_factory=RealDictCursor
                )
                self.initialize_tables()
            else:
                st.warning("Database connection not available - using simulation mode")
        except Exception as e:
            logging.error(f"Database connection error: {e}")
            st.warning("Database connection unavailable - operating in simulation mode")
    
    def initialize_tables(self):
        """Initialize Highland Tower data tables if they don't exist"""
        try:
            with self.connection.cursor() as cursor:
                # Project progress tracking
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS highland_progress (
                        id SERIAL PRIMARY KEY,
                        week_ending DATE NOT NULL,
                        planned_progress DECIMAL(5,2),
                        actual_progress DECIMAL(5,2),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Cost tracking by phase
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS highland_costs (
                        id SERIAL PRIMARY KEY,
                        phase VARCHAR(50) NOT NULL,
                        budgeted_amount DECIMAL(12,2),
                        spent_amount DECIMAL(12,2),
                        forecast_amount DECIMAL(12,2),
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # RFI management
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS highland_rfis (
                        id SERIAL PRIMARY KEY,
                        rfi_number VARCHAR(20) UNIQUE NOT NULL,
                        title VARCHAR(200) NOT NULL,
                        description TEXT,
                        status VARCHAR(20) DEFAULT 'Open',
                        priority VARCHAR(10) DEFAULT 'Medium',
                        submitted_by VARCHAR(100),
                        assigned_to VARCHAR(100),
                        due_date DATE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Daily reports
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS highland_daily_reports (
                        id SERIAL PRIMARY KEY,
                        report_date DATE NOT NULL,
                        weather VARCHAR(50),
                        crew_count INTEGER,
                        total_hours DECIMAL(8,2),
                        work_completed TEXT,
                        issues TEXT,
                        created_by VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                self.connection.commit()
                self.seed_initial_data()
                
        except Exception as e:
            logging.error(f"Table initialization error: {e}")
    
    def seed_initial_data(self):
        """Seed initial Highland Tower development data"""
        try:
            with self.connection.cursor() as cursor:
                # Check if data already exists
                cursor.execute("SELECT COUNT(*) FROM highland_progress")
                if cursor.fetchone()[0] == 0:
                    
                    # Insert progress data
                    progress_data = [
                        ('2024-01-07', 15.0, 12.0),
                        ('2024-01-14', 30.0, 28.0),
                        ('2024-01-21', 45.0, 48.0),
                        ('2024-01-28', 60.0, 65.0),
                        ('2024-02-04', 75.0, 68.0)
                    ]
                    
                    cursor.executemany("""
                        INSERT INTO highland_progress (week_ending, planned_progress, actual_progress)
                        VALUES (%s, %s, %s)
                    """, progress_data)
                    
                    # Insert cost data
                    cost_data = [
                        ('Foundation', 9000000.00, 8500000.00, 8500000.00),
                        ('Structure', 13500000.00, 12300000.00, 12800000.00),
                        ('MEP', 7200000.00, 6800000.00, 7100000.00),
                        ('Finishes', 4800000.00, 2900000.00, 4900000.00),
                        ('Sitework', 1000000.00, 700000.00, 950000.00)
                    ]
                    
                    cursor.executemany("""
                        INSERT INTO highland_costs (phase, budgeted_amount, spent_amount, forecast_amount)
                        VALUES (%s, %s, %s, %s)
                    """, cost_data)
                    
                    # Insert sample RFIs
                    rfi_data = [
                        ('RFI-2024-001', 'Foundation Waterproofing Details', 'Clarification needed on waterproofing membrane specifications', 'Open', 'High'),
                        ('RFI-2024-002', 'Structural Steel Connection Detail', 'Review connection detail for beam-to-column interface', 'In Review', 'Medium'),
                        ('RFI-2024-003', 'Electrical Panel Location', 'Confirm final location for main electrical panel', 'Closed', 'Low')
                    ]
                    
                    cursor.executemany("""
                        INSERT INTO highland_rfis (rfi_number, title, description, status, priority)
                        VALUES (%s, %s, %s, %s, %s)
                    """, rfi_data)
                    
                    self.connection.commit()
                    
        except Exception as e:
            logging.error(f"Data seeding error: {e}")
    
    def get_progress_data(self) -> pd.DataFrame:
        """Get Highland Tower progress data"""
        try:
            if self.connection:
                query = """
                    SELECT 
                        TO_CHAR(week_ending, 'YYYY-MM-DD') as week,
                        planned_progress,
                        actual_progress
                    FROM highland_progress 
                    ORDER BY week_ending
                """
                return pd.read_sql(query, self.connection)
            else:
                # Fallback simulation data
                return pd.DataFrame({
                    'week': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
                    'planned_progress': [15, 30, 45, 60, 75],
                    'actual_progress': [12, 28, 48, 65, 68]
                })
        except Exception as e:
            logging.error(f"Progress data retrieval error: {e}")
            return pd.DataFrame()
    
    def get_cost_data(self) -> pd.DataFrame:
        """Get Highland Tower cost data"""
        try:
            if self.connection:
                query = """
                    SELECT 
                        phase,
                        budgeted_amount / 1000000.0 as budget,
                        spent_amount / 1000000.0 as spent,
                        forecast_amount / 1000000.0 as forecast
                    FROM highland_costs 
                    ORDER BY phase
                """
                return pd.read_sql(query, self.connection)
            else:
                # Fallback simulation data
                return pd.DataFrame({
                    'phase': ['Foundation', 'Structure', 'MEP', 'Finishes', 'Sitework'],
                    'budget': [9.0, 13.5, 7.2, 4.8, 1.0],
                    'spent': [8.5, 12.3, 6.8, 2.9, 0.7],
                    'forecast': [8.5, 12.8, 7.1, 4.9, 0.95]
                })
        except Exception as e:
            logging.error(f"Cost data retrieval error: {e}")
            return pd.DataFrame()
    
    def get_rfi_data(self) -> pd.DataFrame:
        """Get Highland Tower RFI data"""
        try:
            if self.connection:
                query = """
                    SELECT 
                        rfi_number,
                        title,
                        status,
                        priority,
                        created_at::date as created_date
                    FROM highland_rfis 
                    ORDER BY created_at DESC
                """
                return pd.read_sql(query, self.connection)
            else:
                # Fallback simulation data
                return pd.DataFrame({
                    'rfi_number': ['RFI-2024-001', 'RFI-2024-002', 'RFI-2024-003'],
                    'title': ['Foundation Waterproofing', 'Steel Connection Detail', 'Electrical Panel Location'],
                    'status': ['Open', 'In Review', 'Closed'],
                    'priority': ['High', 'Medium', 'Low'],
                    'created_date': ['2024-01-15', '2024-01-18', '2024-01-20']
                })
        except Exception as e:
            logging.error(f"RFI data retrieval error: {e}")
            return pd.DataFrame()
    
    def add_rfi(self, rfi_data: Dict[str, Any]) -> bool:
        """Add new RFI to Highland Tower project"""
        try:
            if self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO highland_rfis (rfi_number, title, description, status, priority, submitted_by)
                        VALUES (%(rfi_number)s, %(title)s, %(description)s, %(status)s, %(priority)s, %(submitted_by)s)
                    """, rfi_data)
                    self.connection.commit()
                    return True
            return False
        except Exception as e:
            logging.error(f"RFI addition error: {e}")
            return False
    
    def update_progress(self, week_ending: str, planned: float, actual: float) -> bool:
        """Update Highland Tower progress data"""
        try:
            if self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO highland_progress (week_ending, planned_progress, actual_progress)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (week_ending) DO UPDATE SET
                        planned_progress = EXCLUDED.planned_progress,
                        actual_progress = EXCLUDED.actual_progress
                    """, (week_ending, planned, actual))
                    self.connection.commit()
                    return True
            return False
        except Exception as e:
            logging.error(f"Progress update error: {e}")
            return False
    
    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Get key metrics for Highland Tower dashboard"""
        try:
            metrics = {
                'total_budget': 45500000,  # $45.5M
                'current_spent': 31200000,  # $31.2M
                'progress_percent': 68,
                'active_rfis': 23,
                'active_workers': 147,
                'project_phase': 'Structure & MEP'
            }
            
            if self.connection:
                with self.connection.cursor() as cursor:
                    # Get actual spent amount
                    cursor.execute("SELECT SUM(spent_amount) FROM highland_costs")
                    spent_result = cursor.fetchone()
                    if spent_result and spent_result[0]:
                        metrics['current_spent'] = float(spent_result[0])
                    
                    # Get RFI count
                    cursor.execute("SELECT COUNT(*) FROM highland_rfis WHERE status != 'Closed'")
                    rfi_result = cursor.fetchone()
                    if rfi_result:
                        metrics['active_rfis'] = rfi_result[0]
                    
                    # Get latest progress
                    cursor.execute("SELECT actual_progress FROM highland_progress ORDER BY week_ending DESC LIMIT 1")
                    progress_result = cursor.fetchone()
                    if progress_result:
                        metrics['progress_percent'] = float(progress_result[0])
            
            return metrics
            
        except Exception as e:
            logging.error(f"Dashboard metrics error: {e}")
            return {
                'total_budget': 45500000,
                'current_spent': 31200000,
                'progress_percent': 68,
                'active_rfis': 23,
                'active_workers': 147,
                'project_phase': 'Structure & MEP'
            }

# Global data manager instance
@st.cache_resource
def get_data_manager():
    """Get or create the Highland Tower data manager instance"""
    return HighlandDataManager()

def clean_dataframe_for_display(df: pd.DataFrame) -> pd.DataFrame:
    """Clean dataframe for reliable Streamlit display"""
    if df.empty:
        return df
    
    df_clean = df.copy()
    
    # Convert all columns to appropriate types
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            # Try to convert to numeric first
            try:
                numeric_series = pd.to_numeric(df_clean[col], errors='ignore')
                if numeric_series.dtype != 'object':
                    df_clean[col] = numeric_series
                else:
                    # Ensure strings are clean
                    df_clean[col] = df_clean[col].astype(str)
            except:
                df_clean[col] = df_clean[col].astype(str)
    
    # Replace infinite values with NaN
    df_clean = df_clean.replace([float('inf'), float('-inf')], None)
    
    return df_clean