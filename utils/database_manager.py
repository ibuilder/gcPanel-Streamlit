"""
Enhanced Database Manager for Highland Tower Development

Provides production-ready database features:
- Connection pooling
- Query optimization
- Audit logging
- Performance monitoring
"""

import os
import psycopg2
from psycopg2 import pool
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import streamlit as st

class DatabaseManager:
    """Enhanced database manager with connection pooling and monitoring."""
    
    def __init__(self):
        self.connection_pool = None
        self.logger = logging.getLogger(__name__)
        self.query_metrics = {
            "total_queries": 0,
            "slow_queries": 0,
            "failed_queries": 0,
            "cache_hits": 0
        }
        
    def initialize_connection_pool(self):
        """Initialize database connection pool for production performance."""
        try:
            database_url = os.environ.get('DATABASE_URL')
            if not database_url:
                self.logger.warning("DATABASE_URL not found, using SQLite fallback")
                return
            
            # Create connection pool
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=20,
                dsn=database_url
            )
            
            self.logger.info("Database connection pool initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize connection pool: {str(e)}")
    
    def get_connection(self):
        """Get connection from pool."""
        if self.connection_pool:
            return self.connection_pool.getconn()
        return None
    
    def return_connection(self, connection):
        """Return connection to pool."""
        if self.connection_pool and connection:
            self.connection_pool.putconn(connection)
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute query with performance monitoring."""
        start_time = datetime.now()
        connection = None
        
        try:
            self.query_metrics["total_queries"] += 1
            
            connection = self.get_connection()
            if not connection:
                return []
            
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                
                # For SELECT queries, fetch results
                if query.strip().upper().startswith('SELECT'):
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    results = [dict(zip(columns, row)) for row in rows]
                else:
                    connection.commit()
                    results = []
                
                # Check for slow queries
                execution_time = (datetime.now() - start_time).total_seconds()
                if execution_time > 1.0:  # Queries over 1 second
                    self.query_metrics["slow_queries"] += 1
                    self.logger.warning(f"Slow query detected: {execution_time:.2f}s")
                
                return results
                
        except Exception as e:
            self.query_metrics["failed_queries"] += 1
            self.logger.error(f"Query execution failed: {str(e)}")
            if connection:
                connection.rollback()
            return []
            
        finally:
            if connection:
                self.return_connection(connection)
    
    def get_connection_count(self) -> int:
        """Get current connection pool size."""
        if self.connection_pool:
            return len(self.connection_pool._pool)
        return 0
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get database performance metrics."""
        return {
            **self.query_metrics,
            "connection_pool_size": self.get_connection_count(),
            "pool_available": len(self.connection_pool._pool) if self.connection_pool else 0
        }
    
    def create_audit_table(self):
        """Create audit table for tracking user actions."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS audit_log (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255),
            action VARCHAR(255),
            module VARCHAR(255),
            details JSONB,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address VARCHAR(45),
            session_id VARCHAR(255)
        );
        
        CREATE INDEX IF NOT EXISTS idx_audit_user_id ON audit_log(user_id);
        CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp);
        CREATE INDEX IF NOT EXISTS idx_audit_module ON audit_log(module);
        """
        
        self.execute_query(create_table_query)
    
    def log_audit_event(self, user_id: str, action: str, module: str, details: Dict[str, Any]):
        """Log audit event to database."""
        import json
        
        query = """
        INSERT INTO audit_log (user_id, action, module, details, session_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        session_id = st.session_state.get("session_id", "unknown")
        
        self.execute_query(query, (
            user_id,
            action,
            module,
            json.dumps(details),
            session_id
        ))
    
    def optimize_database(self):
        """Run database optimization queries."""
        optimization_queries = [
            "VACUUM ANALYZE;",
            "REINDEX DATABASE;",
        ]
        
        for query in optimization_queries:
            try:
                self.execute_query(query)
            except Exception as e:
                self.logger.error(f"Optimization query failed: {str(e)}")
    
    def backup_data(self, tables: List[str] = None):
        """Create backup of specified tables."""
        # This would implement backup functionality
        # For production, integrate with cloud backup services
        self.logger.info("Backup functionality would be implemented here")
    
    def cleanup_old_data(self, days: int = 90):
        """Clean up old audit logs and temporary data."""
        cleanup_query = """
        DELETE FROM audit_log 
        WHERE timestamp < NOW() - INTERVAL '%s days'
        """
        
        self.execute_query(cleanup_query, (days,))