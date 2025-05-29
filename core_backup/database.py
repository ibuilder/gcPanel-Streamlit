"""
Enterprise Database Management for gcPanel Construction Platform

This module provides production-ready database operations with PostgreSQL integration,
connection pooling, and performance optimization for construction management workflows.
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class DatabaseManager:
    """Enterprise-grade database manager with connection pooling and optimization."""
    
    def __init__(self):
        """Initialize database connection with production configuration."""
        self.database_url = os.environ.get('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required for production deployment")
        
        # Configure production-ready connection pool
        self.engine = create_engine(
            self.database_url,
            poolclass=QueuePool,
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False  # Set to True for SQL debugging
        )
        
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.metadata = MetaData()
        
        # Initialize database schema
        self._create_tables()
        
        logger.info("Enterprise database connection established successfully")
    
    def _create_tables(self):
        """Create production database schema for construction management."""
        
        # Projects table
        projects_table = Table(
            'projects', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('project_name', String(255), nullable=False),
            Column('project_number', String(100), unique=True, nullable=False),
            Column('client_name', String(255)),
            Column('project_address', Text),
            Column('contract_value', Float),
            Column('start_date', DateTime),
            Column('estimated_completion', DateTime),
            Column('project_manager', String(255)),
            Column('status', String(50), default='Active'),
            Column('created_at', DateTime, default=datetime.utcnow),
            Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        )
        
        # Daily Reports table
        daily_reports_table = Table(
            'daily_reports', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('project_id', Integer, ForeignKey('projects.id')),
            Column('report_date', DateTime, nullable=False),
            Column('superintendent', String(255)),
            Column('foreman', String(255)),
            Column('weather_conditions', String(100)),
            Column('temperature_high', Integer),
            Column('temperature_low', Integer),
            Column('humidity', Integer),
            Column('total_crew_size', Integer),
            Column('work_performed', Text),
            Column('materials_received', Text),
            Column('equipment_used', Text),
            Column('safety_incidents', Boolean, default=False),
            Column('incident_description', Text),
            Column('progress_percentage', Float),
            Column('created_by', String(255)),
            Column('created_at', DateTime, default=datetime.utcnow)
        )
        
        # Quality Control Inspections table
        inspections_table = Table(
            'quality_inspections', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('project_id', Integer, ForeignKey('projects.id')),
            Column('inspection_id', String(50), unique=True),
            Column('inspection_type', String(100)),
            Column('inspection_date', DateTime),
            Column('inspector_name', String(255)),
            Column('inspector_certification', String(100)),
            Column('building_area', String(100)),
            Column('floor_level', String(50)),
            Column('work_scope', Text),
            Column('inspection_score', Float),
            Column('final_status', String(50)),
            Column('deficiencies_found', Boolean, default=False),
            Column('corrective_action', Text),
            Column('reinspection_required', Boolean, default=False),
            Column('created_at', DateTime, default=datetime.utcnow)
        )
        
        # AIA Payment Applications table
        payment_applications_table = Table(
            'payment_applications', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('project_id', Integer, ForeignKey('projects.id')),
            Column('application_number', Integer),
            Column('period_from', DateTime),
            Column('period_to', DateTime),
            Column('owner_name', String(255)),
            Column('contractor_name', String(255)),
            Column('architect_name', String(255)),
            Column('total_contract_sum', Float),
            Column('net_change_orders', Float),
            Column('contract_sum_to_date', Float),
            Column('total_completed_stored', Float),
            Column('retainage_percentage', Float),
            Column('retainage_amount', Float),
            Column('payment_due', Float),
            Column('status', String(50), default='Draft'),
            Column('created_at', DateTime, default=datetime.utcnow),
            Column('submitted_at', DateTime),
            Column('approved_at', DateTime)
        )
        
        # Users table for enhanced authentication
        users_table = Table(
            'users', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('username', String(100), unique=True, nullable=False),
            Column('email', String(255), unique=True, nullable=False),
            Column('password_hash', String(255)),
            Column('full_name', String(255)),
            Column('role', String(50), default='User'),
            Column('company', String(255)),
            Column('phone', String(20)),
            Column('is_active', Boolean, default=True),
            Column('last_login', DateTime),
            Column('created_at', DateTime, default=datetime.utcnow),
            Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        )
        
        # Audit Log table for compliance
        audit_log_table = Table(
            'audit_log', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('user_id', Integer, ForeignKey('users.id')),
            Column('action', String(100)),
            Column('table_name', String(100)),
            Column('record_id', Integer),
            Column('old_values', Text),
            Column('new_values', Text),
            Column('ip_address', String(50)),
            Column('user_agent', Text),
            Column('timestamp', DateTime, default=datetime.utcnow)
        )
        
        # Create all tables
        try:
            self.metadata.create_all(self.engine)
            logger.info("Database schema created successfully")
        except Exception as e:
            logger.error(f"Error creating database schema: {str(e)}")
            raise
    
    def get_session(self):
        """Get database session with proper error handling."""
        try:
            return self.SessionLocal()
        except Exception as e:
            logger.error(f"Error creating database session: {str(e)}")
            raise
    
    def execute_query(self, query: str, params: Dict = None) -> List[Dict]:
        """Execute SQL query with parameters and return results."""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params or {})
                if result.returns_rows:
                    columns = result.keys()
                    rows = result.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
                return []
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise
    
    def insert_data(self, table_name: str, data: Dict) -> int:
        """Insert data into specified table and return the ID."""
        try:
            # Add timestamp fields
            data['created_at'] = datetime.utcnow()
            if 'updated_at' in self.metadata.tables[table_name].columns:
                data['updated_at'] = datetime.utcnow()
            
            # Build insert query
            columns = ', '.join(data.keys())
            placeholders = ', '.join([f':{key}' for key in data.keys()])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) RETURNING id"
            
            result = self.execute_query(query, data)
            return result[0]['id'] if result else None
            
        except Exception as e:
            logger.error(f"Error inserting data into {table_name}: {str(e)}")
            raise
    
    def update_data(self, table_name: str, record_id: int, data: Dict) -> bool:
        """Update data in specified table."""
        try:
            # Add update timestamp
            data['updated_at'] = datetime.utcnow()
            
            # Build update query
            set_clause = ', '.join([f'{key} = :{key}' for key in data.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE id = :record_id"
            data['record_id'] = record_id
            
            with self.engine.connect() as connection:
                result = connection.execute(text(query), data)
                connection.commit()
                return result.rowcount > 0
                
        except Exception as e:
            logger.error(f"Error updating data in {table_name}: {str(e)}")
            raise
    
    def get_projects(self) -> List[Dict]:
        """Get all active projects."""
        query = """
        SELECT id, project_name, project_number, client_name, 
               project_manager, status, contract_value, start_date
        FROM projects 
        WHERE status = 'Active'
        ORDER BY project_name
        """
        return self.execute_query(query)
    
    def get_daily_reports(self, project_id: int = None, limit: int = 50) -> List[Dict]:
        """Get daily reports with optional project filter."""
        query = """
        SELECT dr.*, p.project_name
        FROM daily_reports dr
        JOIN projects p ON dr.project_id = p.id
        """
        params = {}
        
        if project_id:
            query += " WHERE dr.project_id = :project_id"
            params['project_id'] = project_id
        
        query += " ORDER BY dr.report_date DESC LIMIT :limit"
        params['limit'] = limit
        
        return self.execute_query(query, params)
    
    def log_audit_action(self, user_id: int, action: str, table_name: str, 
                        record_id: int, old_values: str = None, new_values: str = None):
        """Log user actions for compliance and audit trails."""
        try:
            audit_data = {
                'user_id': user_id,
                'action': action,
                'table_name': table_name,
                'record_id': record_id,
                'old_values': old_values,
                'new_values': new_values,
                'ip_address': st.session_state.get('client_ip', 'unknown'),
                'user_agent': 'gcPanel Web Application'
            }
            
            self.insert_data('audit_log', audit_data)
            logger.info(f"Audit log recorded: {action} on {table_name} by user {user_id}")
            
        except Exception as e:
            logger.error(f"Error logging audit action: {str(e)}")
    
    def get_performance_metrics(self) -> Dict:
        """Get database performance metrics for monitoring."""
        try:
            # Get table sizes and record counts
            query = """
            SELECT 
                schemaname,
                tablename,
                attname,
                n_distinct,
                correlation
            FROM pg_stats 
            WHERE schemaname = 'public'
            ORDER BY tablename, attname
            """
            
            stats = self.execute_query(query)
            
            # Get connection pool status
            pool_status = {
                'pool_size': self.engine.pool.size(),
                'checked_in': self.engine.pool.checkedin(),
                'checked_out': self.engine.pool.checkedout(),
                'invalid': self.engine.pool.invalidated()
            }
            
            return {
                'database_stats': stats,
                'connection_pool': pool_status,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting performance metrics: {str(e)}")
            return {}

# Global database instance
db_manager = None

def get_database():
    """Get or create database manager instance."""
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
    return db_manager

def init_database():
    """Initialize database connection for the application."""
    try:
        db = get_database()
        logger.info("Database initialized successfully")
        return db
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        st.error("⚠️ Database connection failed. Please check configuration.")
        return None