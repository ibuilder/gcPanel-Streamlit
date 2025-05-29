"""
Base Model Class for gcPanel MVC Architecture
Provides foundational CRUD operations and database integration
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, List, Any, Optional, Union
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BaseModel:
    """Base model class with CRUD operations and database integration"""
    
    def __init__(self, table_name: str, schema: Dict[str, Any]):
        self.table_name = table_name
        self.schema = schema
        self.session_key = f"{table_name}_data"
        self._connection = None
        
    def get_connection(self):
        """Get database connection with proper error handling"""
        if self._connection is None or self._connection.closed:
            try:
                database_url = os.getenv('DATABASE_URL')
                if database_url and not database_url.startswith('https://'):
                    self._connection = psycopg2.connect(
                        database_url,
                        cursor_factory=RealDictCursor
                    )
                    self._connection.autocommit = True
                    return self._connection
            except Exception as e:
                logger.error(f"Database connection failed: {e}")
        return self._connection
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute SELECT query with error handling"""
        conn = self.get_connection()
        if not conn:
            return self._get_session_data()
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return self._get_session_data()
    
    def execute_command(self, command: str, params: tuple = None) -> bool:
        """Execute INSERT/UPDATE/DELETE with error handling"""
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
    
    def _get_session_data(self) -> List[Dict]:
        """Fallback to session data when database unavailable"""
        import streamlit as st
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = []
        return st.session_state[self.session_key]
    
    def _save_to_session(self, data: List[Dict]):
        """Save data to session state"""
        import streamlit as st
        st.session_state[self.session_key] = data
    
    def get_all(self) -> List[Dict]:
        """Get all records"""
        query = f"SELECT * FROM {self.table_name} ORDER BY id DESC"
        return self.execute_query(query)
    
    def get_by_id(self, record_id: Union[int, str]) -> Optional[Dict]:
        """Get record by ID"""
        query = f"SELECT * FROM {self.table_name} WHERE id = %s"
        results = self.execute_query(query, (record_id,))
        return results[0] if results else None
    
    def create(self, data: Dict) -> bool:
        """Create new record"""
        # Filter data based on schema
        filtered_data = {k: v for k, v in data.items() if k in self.schema.get('fields', {})}
        
        if not filtered_data:
            return False
        
        # Build INSERT query
        fields = list(filtered_data.keys())
        values = list(filtered_data.values())
        placeholders = ', '.join(['%s'] * len(fields))
        field_names = ', '.join(fields)
        
        query = f"INSERT INTO {self.table_name} ({field_names}) VALUES ({placeholders})"
        
        success = self.execute_command(query, tuple(values))
        
        # Fallback to session storage
        if not success:
            session_data = self._get_session_data()
            new_id = max([item.get('id', 0) for item in session_data], default=0) + 1
            filtered_data['id'] = new_id
            filtered_data['created_at'] = datetime.now().isoformat()
            session_data.append(filtered_data)
            self._save_to_session(session_data)
            return True
        
        return success
    
    def update(self, record_id: Union[int, str], data: Dict) -> bool:
        """Update existing record"""
        # Filter data based on schema
        filtered_data = {k: v for k, v in data.items() if k in self.schema.get('fields', {})}
        
        if not filtered_data:
            return False
        
        # Build UPDATE query
        set_clause = ', '.join([f"{k} = %s" for k in filtered_data.keys()])
        values = list(filtered_data.values()) + [record_id]
        
        query = f"UPDATE {self.table_name} SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        
        success = self.execute_command(query, tuple(values))
        
        # Fallback to session storage
        if not success:
            session_data = self._get_session_data()
            for item in session_data:
                if str(item.get('id')) == str(record_id):
                    item.update(filtered_data)
                    item['updated_at'] = datetime.now().isoformat()
                    break
            self._save_to_session(session_data)
            return True
        
        return success
    
    def delete(self, record_id: Union[int, str]) -> bool:
        """Delete record"""
        query = f"DELETE FROM {self.table_name} WHERE id = %s"
        
        success = self.execute_command(query, (record_id,))
        
        # Fallback to session storage
        if not success:
            session_data = self._get_session_data()
            session_data = [item for item in session_data if str(item.get('id')) != str(record_id)]
            self._save_to_session(session_data)
            return True
        
        return success
    
    def search(self, search_term: str, fields: List[str] = None) -> List[Dict]:
        """Search records by term in specified fields"""
        if not fields:
            fields = list(self.schema.get('fields', {}).keys())
        
        # Build search query for database
        conditions = []
        params = []
        for field in fields:
            conditions.append(f"{field}::text ILIKE %s")
            params.append(f"%{search_term}%")
        
        where_clause = " OR ".join(conditions)
        query = f"SELECT * FROM {self.table_name} WHERE {where_clause} ORDER BY id DESC"
        
        results = self.execute_query(query, tuple(params))
        
        # Fallback to session search
        if not results:
            session_data = self._get_session_data()
            results = []
            for item in session_data:
                for field in fields:
                    if field in item and search_term.lower() in str(item[field]).lower():
                        results.append(item)
                        break
        
        return results
    
    def filter_by(self, field: str, value: Any) -> List[Dict]:
        """Filter records by field value"""
        query = f"SELECT * FROM {self.table_name} WHERE {field} = %s ORDER BY id DESC"
        
        results = self.execute_query(query, (value,))
        
        # Fallback to session filter
        if not results:
            session_data = self._get_session_data()
            results = [item for item in session_data if item.get(field) == value]
        
        return results
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert records to pandas DataFrame"""
        data = self.get_all()
        return pd.DataFrame(data) if data else pd.DataFrame()
    
    def get_field_options(self, field: str) -> List[str]:
        """Get unique values for a field (for dropdowns)"""
        query = f"SELECT DISTINCT {field} FROM {self.table_name} WHERE {field} IS NOT NULL ORDER BY {field}"
        
        results = self.execute_query(query)
        
        # Fallback to session data
        if not results:
            session_data = self._get_session_data()
            values = set()
            for item in session_data:
                if field in item and item[field] is not None:
                    values.add(item[field])
            return sorted(list(values))
        
        return [row[field] for row in results]
    
    def get_recent(self, limit: int = 10) -> List[Dict]:
        """Get recent records"""
        query = f"SELECT * FROM {self.table_name} ORDER BY created_at DESC LIMIT %s"
        
        results = self.execute_query(query, (limit,))
        
        # Fallback to session data
        if not results:
            session_data = self._get_session_data()
            return session_data[:limit]
        
        return results
    
    def count(self) -> int:
        """Get total record count"""
        query = f"SELECT COUNT(*) as count FROM {self.table_name}"
        
        results = self.execute_query(query)
        
        # Fallback to session data
        if not results:
            return len(self._get_session_data())
        
        return results[0]['count'] if results else 0
    
    def validate_data(self, data: Dict) -> Dict[str, List[str]]:
        """Validate data against schema"""
        errors = {}
        
        for field_name, field_config in self.schema.get('fields', {}).items():
            if field_config.get('required', False) and not data.get(field_name):
                if field_name not in errors:
                    errors[field_name] = []
                errors[field_name].append(f"{field_name} is required")
            
            # Type validation
            if field_name in data and data[field_name] is not None:
                field_type = field_config.get('type', 'text')
                value = data[field_name]
                
                if field_type == 'number' and not isinstance(value, (int, float)):
                    try:
                        float(value)
                    except (ValueError, TypeError):
                        if field_name not in errors:
                            errors[field_name] = []
                        errors[field_name].append(f"{field_name} must be a number")
                
                elif field_type == 'email' and '@' not in str(value):
                    if field_name not in errors:
                        errors[field_name] = []
                    errors[field_name].append(f"{field_name} must be a valid email")
        
        return errors