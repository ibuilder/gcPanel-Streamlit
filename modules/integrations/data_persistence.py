"""
Data persistence module for external integrations.

This module handles saving and retrieving imported data from external platforms
in a reliable way with database support and session state fallback.

# Usage Example:
```python
from modules.integrations.data_persistence import (
    initialize_database,
    save_imported_data,
    get_imported_data,
    get_import_history
)

# Initialize the database connection
initialize_database()

# Save imported data from an external platform
data = [{"id": "doc-1", "name": "Floor Plan", "type": "Drawing"}]
dataset_id = save_imported_data(
    platform="procore",
    data_type="documents",
    data=data,
    import_method="merge"  # or "replace"
)

# Retrieve previously imported data
documents = get_imported_data(platform="procore", data_type="documents")

# Get import history for reporting
history_df = get_import_history(limit=50)
```

# Features:
- Automatic database initialization with session state fallback
- Support for both merge and replace import strategies
- Comprehensive import history tracking
- Support for various data formats (list of items, nested structures)
- Clean database management with proper relationships

# Data Types and Storage:
The module supports storing different types of imported data:
- Simple lists (documents, specifications, incidents)
- Complex nested structures (budget with items and summary)
- Hierarchical data (schedule with tasks and summary information)

# Database Schema:
- ImportedDataset: Tracks import metadata (platform, date, count)
- ImportedDataItem: Stores individual data items with source information

# Fallback Mechanism:
If a database connection isn't available, data is stored in session state
to ensure no data loss occurs during temporary database outages.
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import hashlib
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, JSON, DateTime, Float, Boolean, Text, ForeignKey, select, insert, update, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from typing import Dict, List, Any, Optional, Union, Tuple
from contextlib import contextmanager

# Initialize database connection
DATABASE_URL = os.environ.get("DATABASE_URL")
Base = declarative_base()

# Define models for imported data
class ImportedDataset(Base):
    """Model for tracking imported datasets."""
    __tablename__ = "imported_datasets"
    
    id = Column(Integer, primary_key=True)
    platform = Column(String(255), nullable=False)
    data_type = Column(String(255), nullable=False)
    import_date = Column(DateTime, default=datetime.now)
    item_count = Column(Integer, default=0)
    import_method = Column(String(255), default="merge")
    status = Column(String(50), default="complete")
    user_id = Column(Integer, nullable=True)  # Link to user who performed the import
    
    # Relationship to actual data
    items = relationship("ImportedDataItem", back_populates="dataset", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ImportedDataset(id={self.id}, platform='{self.platform}', data_type='{self.data_type}')>"

class ImportedDataItem(Base):
    """Model for individual imported data items."""
    __tablename__ = "imported_data_items"
    
    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("imported_datasets.id"))
    external_id = Column(String(255), nullable=True)  # ID from the external system
    item_type = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    data = Column(JSON, nullable=False)  # Store the full data as JSON
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationship to parent dataset
    dataset = relationship("ImportedDataset", back_populates="items")
    
    def __repr__(self):
        return f"<ImportedDataItem(id={self.id}, name='{self.name}')>"

# Database session management
engine = None
Session = None

def initialize_database():
    """Initialize the database connection and create tables if needed."""
    global engine, Session
    
    if not DATABASE_URL:
        st.warning("Database URL not set. Data will not be persisted.")
        return False
    
    try:
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(engine)
        return True
    except Exception as e:
        st.error(f"Failed to initialize database: {str(e)}")
        return False

@contextmanager
def db_session():
    """Context manager for database sessions."""
    if not Session:
        initialize_database()
        if not Session:
            yield None
            return
    
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def save_imported_data(platform: str, data_type: str, data: Any, import_method: str = "merge", user_id: Optional[int] = None) -> Optional[int]:
    """
    Save imported data to the database.
    
    Args:
        platform: Platform from which data was imported (e.g., "procore")
        data_type: Type of data imported (e.g., "documents", "bids")
        data: The data to save
        import_method: How to handle existing data ("merge" or "replace")
        user_id: ID of the user who performed the import
        
    Returns:
        Optional[int]: ID of the created dataset, or None on failure
    """
    if not initialize_database():
        # If database initialization fails, store in session state as fallback
        store_in_session_state(platform, data_type, data, import_method)
        return None
    
    try:
        with db_session() as session:
            if not session:
                store_in_session_state(platform, data_type, data, import_method)
                return None
            
            # Handle replace mode - remove existing data of this type from this platform
            if import_method == "replace":
                existing_datasets = session.query(ImportedDataset).filter(
                    ImportedDataset.platform == platform,
                    ImportedDataset.data_type == data_type
                ).all()
                
                for dataset in existing_datasets:
                    session.delete(dataset)
            
            # Create new dataset record
            item_count = 0
            if isinstance(data, list):
                item_count = len(data)
            elif isinstance(data, dict):
                if "items" in data and isinstance(data["items"], list):
                    item_count = len(data["items"])
                elif "tasks" in data and isinstance(data["tasks"], list):
                    item_count = len(data["tasks"])
            
            dataset = ImportedDataset(
                platform=platform,
                data_type=data_type,
                item_count=item_count,
                import_method=import_method,
                user_id=user_id
            )
            session.add(dataset)
            session.flush()  # Get dataset ID
            
            # Store individual items
            if isinstance(data, list):
                # Flat list of items (documents, bids, etc.)
                for item in data:
                    if not isinstance(item, dict):
                        continue
                        
                    new_item = ImportedDataItem(
                        dataset_id=dataset.id,
                        external_id=item.get("id"),
                        item_type=item.get("type"),
                        name=item.get("name"),
                        data=item
                    )
                    session.add(new_item)
            
            elif isinstance(data, dict):
                if "items" in data and isinstance(data["items"], list):
                    # Budget-like structure with items list
                    for item in data["items"]:
                        if not isinstance(item, dict):
                            continue
                            
                        new_item = ImportedDataItem(
                            dataset_id=dataset.id,
                            external_id=item.get("id"),
                            item_type="budget_item",
                            name=item.get("category", item.get("name")),
                            data=item
                        )
                        session.add(new_item)
                        
                    # Store summary as a special item
                    if "summary" in data and isinstance(data["summary"], dict):
                        summary_item = ImportedDataItem(
                            dataset_id=dataset.id,
                            item_type="summary",
                            name="Budget Summary",
                            data=data["summary"]
                        )
                        session.add(summary_item)
                
                elif "tasks" in data and isinstance(data["tasks"], list):
                    # Schedule-like structure with tasks list
                    for task in data["tasks"]:
                        if not isinstance(task, dict):
                            continue
                            
                        new_item = ImportedDataItem(
                            dataset_id=dataset.id,
                            external_id=task.get("id"),
                            item_type="schedule_task",
                            name=task.get("name"),
                            data=task
                        )
                        session.add(new_item)
                        
                    # Store summary as a special item
                    if "summary" in data and isinstance(data["summary"], dict):
                        summary_item = ImportedDataItem(
                            dataset_id=dataset.id,
                            item_type="summary",
                            name="Schedule Summary",
                            data=data["summary"]
                        )
                        session.add(summary_item)
            
            # Commit is handled by the context manager
            # Properly handle the SQLAlchemy Column type conversion
            if dataset is None:
                return None
                
            # Access the ID attribute carefully
            dataset_id = getattr(dataset, 'id', None)
            if dataset_id is not None:
                # For SQLAlchemy objects, we need to get the raw scalar value
                try:
                    # Try to extract scalar value or convert to integer
                    if hasattr(dataset_id, '_asdict'):
                        # Handle SQLAlchemy result objects
                        return int(dataset_id._asdict().get('id', 0))
                    elif hasattr(dataset_id, 'value'):
                        # Handle SQLAlchemy InstrumentedAttribute
                        return int(dataset_id.value)
                    else:
                        # Direct conversion attempt
                        return int(str(dataset_id))
                except (TypeError, ValueError, AttributeError) as e:
                    # Log the error for debugging
                    print(f"Error converting dataset_id: {e}")
                    # Return any integer-castable value
                    return 0
            return None
    
    except Exception as e:
        st.error(f"Failed to save imported data: {str(e)}")
        # Fall back to session state
        store_in_session_state(platform, data_type, data, import_method)
        return None

def get_imported_data(platform: Optional[str] = None, data_type: Optional[str] = None, limit: int = 1000) -> List[Dict[str, Any]]:
    """
    Retrieve imported data from the database.
    
    Args:
        platform: Optional filter by platform
        data_type: Optional filter by data type
        limit: Maximum number of datasets to return
        
    Returns:
        List[Dict[str, Any]]: List of imported datasets with items
    """
    if not initialize_database():
        # If database initialization fails, retrieve from session state
        return get_from_session_state(platform, data_type)
    
    try:
        with db_session() as session:
            if not session:
                return get_from_session_state(platform, data_type)
            
            # Build query based on filters
            query = session.query(ImportedDataset)
            
            # Properly handle SQLAlchemy filter conditions
            if platform is not None:
                query = query.filter(ImportedDataset.platform == platform)
                
            if data_type is not None:
                query = query.filter(ImportedDataset.data_type == data_type)
                
            # Order by most recent first and limit results
            query = query.order_by(ImportedDataset.import_date.desc()).limit(limit)
            
            # Execute query
            datasets = query.all()
            
            # Format results
            results = []
            for dataset in datasets:
                # Get dataset info
                dataset_info = {
                    "id": dataset.id,
                    "platform": dataset.platform,
                    "data_type": dataset.data_type,
                    "import_date": dataset.import_date.isoformat(),
                    "item_count": dataset.item_count,
                    "import_method": dataset.import_method,
                    "status": dataset.status
                }
                
                # Get items for this dataset
                items_query = session.query(ImportedDataItem).filter(ImportedDataItem.dataset_id == dataset.id)
                items = items_query.all()
                
                if data_type in ["budget", "schedule"]:
                    # Special handling for composite types
                    # Safely check item_type without using SQLAlchemy boolean conditions
                    summary_item = None
                    data_items = []
                    
                    for item in items:
                        item_type_val = str(item.item_type) if item.item_type is not None else ""
                        if item_type_val == "summary":
                            summary_item = item
                        else:
                            data_items.append(item)
                    
                    if data_type == "budget":
                        dataset_info["data"] = {
                            "items": [item.data for item in data_items],
                            "summary": summary_item.data if summary_item else {}
                        }
                    elif data_type == "schedule":
                        dataset_info["data"] = {
                            "tasks": [item.data for item in data_items],
                            "summary": summary_item.data if summary_item else {}
                        }
                else:
                    # Standard list of items
                    dataset_info["data"] = [item.data for item in items]
                
                results.append(dataset_info)
            
            return results
    
    except Exception as e:
        st.error(f"Failed to retrieve imported data: {str(e)}")
        # Fall back to session state
        return get_from_session_state(platform, data_type)

def delete_imported_data(dataset_id: int) -> bool:
    """
    Delete an imported dataset and all its items.
    
    Args:
        dataset_id: ID of the dataset to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not initialize_database():
        return False
    
    try:
        with db_session() as session:
            if not session:
                return False
                
            dataset = session.query(ImportedDataset).get(dataset_id)
            
            if not dataset:
                return False
                
            session.delete(dataset)  # This will cascade delete all items
            return True
    
    except Exception as e:
        st.error(f"Failed to delete imported data: {str(e)}")
        return False

def get_import_history(limit: int = 50) -> pd.DataFrame:
    """
    Get import history as a DataFrame.
    
    Args:
        limit: Maximum number of history items to return
        
    Returns:
        pd.DataFrame: DataFrame with import history
    """
    if not initialize_database():
        # If database initialization fails, use session state
        return get_history_from_session_state()
    
    try:
        with db_session() as session:
            if not session:
                return get_history_from_session_state()
                
            query = session.query(ImportedDataset).order_by(ImportedDataset.import_date.desc()).limit(limit)
            datasets = query.all()
            
            # Convert to DataFrame
            history_data = [{
                "ID": dataset.id,
                "Platform": dataset.platform,
                "Data Type": dataset.data_type,
                "Import Date": dataset.import_date,
                "Items": dataset.item_count,
                "Method": dataset.import_method,
                "Status": dataset.status
            } for dataset in datasets]
            
            # Define the column names to ensure consistency
            columns = ["ID", "Platform", "Data Type", "Import Date", "Items", "Method", "Status"]
            
            if not history_data:
                # Return empty DataFrame with correct columns
                return pd.DataFrame(columns=columns)
                
            # Create DataFrame with explicit column order to avoid LSP issues
            df = pd.DataFrame(history_data)
            return df[columns] if len(df.columns) > 0 else df
    
    except Exception as e:
        st.error(f"Failed to retrieve import history: {str(e)}")
        return get_history_from_session_state()

# Session state fallback functions
def store_in_session_state(platform: str, data_type: str, data: Any, import_method: str = "merge"):
    """
    Store imported data in session state as a fallback when database is unavailable.
    
    Args:
        platform: Platform from which data was imported
        data_type: Type of imported data
        data: The data to store
        import_method: How to handle existing data
    """
    # Initialize container if needed
    if "imported_data" not in st.session_state:
        st.session_state.imported_data = []
    
    # Handle replace mode
    if import_method == "replace":
        st.session_state.imported_data = [
            item for item in st.session_state.imported_data 
            if not (item["platform"] == platform and item["data_type"] == data_type)
        ]
    
    # Add new data
    item_count = 0
    if isinstance(data, list):
        item_count = len(data)
    elif isinstance(data, dict):
        if "items" in data and isinstance(data["items"], list):
            item_count = len(data["items"])
        elif "tasks" in data and isinstance(data["tasks"], list):
            item_count = len(data["tasks"])
    
    import_record = {
        "id": len(st.session_state.imported_data) + 1,
        "platform": platform,
        "data_type": data_type,
        "import_date": datetime.now().isoformat(),
        "item_count": item_count,
        "import_method": import_method,
        "status": "complete",
        "data": data
    }
    
    st.session_state.imported_data.append(import_record)
    
    # Also update the legacy format for compatibility
    key = f"imported_{data_type}"
    st.session_state[key] = {
        "data": data,
        "source": platform,
        "import_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "count": item_count
    }

def get_from_session_state(platform: Optional[str] = None, data_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get imported data from session state.
    
    Args:
        platform: Optional filter by platform
        data_type: Optional filter by data type
        
    Returns:
        List[Dict[str, Any]]: List of imported datasets with items
    """
    if "imported_data" not in st.session_state:
        return []
    
    results = st.session_state.imported_data
    
    # Apply filters
    if platform:
        results = [item for item in results if item["platform"] == platform]
        
    if data_type:
        results = [item for item in results if item["data_type"] == data_type]
    
    # Sort by import date, newest first
    results.sort(key=lambda x: x.get("import_date", ""), reverse=True)
    
    return results

def get_history_from_session_state() -> pd.DataFrame:
    """
    Get import history from session state.
    
    Returns:
        pd.DataFrame: DataFrame with import history
    """
    if "imported_data" not in st.session_state:
        # Return empty DataFrame with correct columns
        return pd.DataFrame(columns=["ID", "Platform", "Data Type", "Import Date", "Items", "Method", "Status"])
    
    # Convert to DataFrame format
    history_data = [{
        "ID": item["id"],
        "Platform": item["platform"],
        "Data Type": item["data_type"],
        "Import Date": item["import_date"],
        "Items": item["item_count"],
        "Method": item["import_method"],
        "Status": item["status"]
    } for item in st.session_state.imported_data]
    
    if not history_data:
        # Return empty DataFrame with correct columns
        return pd.DataFrame(columns=["ID", "Platform", "Data Type", "Import Date", "Items", "Method", "Status"])
    
    df = pd.DataFrame(history_data)
    
    # Sort by import date, newest first
    df = df.sort_values(by="Import Date", ascending=False)
    
    return df