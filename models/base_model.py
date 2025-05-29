"""
Base Model for gcPanel Construction Management Platform
Provides common CRUD operations and data handling
"""

from typing import Dict, List, Any, Optional
import pandas as pd
from datetime import datetime
import streamlit as st

class BaseModel:
    """Base model class with common CRUD operations"""
    
    def __init__(self, session_key: str, schema: Dict[str, Any]):
        self.session_key = session_key
        self.schema = schema
        self._ensure_session_state()
    
    def _ensure_session_state(self):
        """Ensure session state exists for this model"""
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = []
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all records"""
        return st.session_state[self.session_key]
    
    def get_by_id(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific record by ID"""
        for record in self.get_all():
            if record.get('id') == record_id:
                return record
        return None
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record"""
        # Add timestamp and ID if not provided
        if 'id' not in data:
            data['id'] = self._generate_id()
        if 'created_at' not in data:
            data['created_at'] = datetime.now().isoformat()
        
        # Validate against schema
        validated_data = self._validate_data(data)
        
        # Add to session state
        st.session_state[self.session_key].append(validated_data)
        return validated_data
    
    def update(self, record_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing record"""
        records = st.session_state[self.session_key]
        for i, record in enumerate(records):
            if record.get('id') == record_id:
                # Merge data with existing record
                updated_record = {**record, **data}
                updated_record['updated_at'] = datetime.now().isoformat()
                
                # Validate against schema
                validated_data = self._validate_data(updated_record)
                
                # Update in session state
                st.session_state[self.session_key][i] = validated_data
                return validated_data
        return None
    
    def delete(self, record_id: str) -> bool:
        """Delete a record"""
        records = st.session_state[self.session_key]
        for i, record in enumerate(records):
            if record.get('id') == record_id:
                del st.session_state[self.session_key][i]
                return True
        return False
    
    def filter_records(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter records based on criteria"""
        records = self.get_all()
        filtered = records.copy()
        
        for key, value in filters.items():
            if value and value != "All":
                filtered = [r for r in filtered if r.get(key) == value]
        
        return filtered
    
    def search_records(self, search_term: str, search_fields: List[str]) -> List[Dict[str, Any]]:
        """Search records in specified fields"""
        if not search_term:
            return self.get_all()
        
        results = []
        for record in self.get_all():
            for field in search_fields:
                if field in record and search_term.lower() in str(record[field]).lower():
                    results.append(record)
                    break
        
        return results
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert records to DataFrame"""
        records = self.get_all()
        if not records:
            return pd.DataFrame()
        return pd.DataFrame(records)
    
    def _generate_id(self) -> str:
        """Generate a unique ID for new records"""
        prefix = self.schema.get('id_prefix', 'ID')
        existing_ids = [r.get('id', '') for r in self.get_all()]
        
        counter = 1
        while f"{prefix}-{counter:03d}" in existing_ids:
            counter += 1
        
        return f"{prefix}-{counter:03d}"
    
    def _validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against schema"""
        validated = {}
        
        for field, field_config in self.schema.get('fields', {}).items():
            if field in data:
                validated[field] = data[field]
            elif field_config.get('required', False):
                raise ValueError(f"Required field '{field}' is missing")
        
        # Add any additional fields not in schema
        for key, value in data.items():
            if key not in validated:
                validated[key] = value
        
        return validated