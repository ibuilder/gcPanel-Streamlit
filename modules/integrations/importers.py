"""
Data Importers for External Integration Services.

This module provides functionality to import data from external construction management
platforms such as Procore, PlanGrid, FieldWire, and BuildingConnected.

# Overview
The importers module handles the actual communication with external platforms'
APIs to retrieve construction project data. It provides specialized functions
for different data types and platforms, with standardized responses for
consistent handling in the application.

# Usage Example:
```python
from modules.integrations.importers import (
    import_documents,
    import_specifications,
    import_bids,
    import_daily_reports
)

# Import documents from Procore
documents_result = import_documents("procore")
if "error" not in documents_result:
    documents_data = documents_result["data"]
    documents_source = documents_result["source"]
    # Process documents...

# Import specifications from Procore
specs_result = import_specifications("procore")
if "error" not in specs_result:
    specs_data = specs_result["data"]
    # Process specifications...
```

# Supported Platforms and Data Types:

1. Procore:
   - Documents
   - Specifications
   - Bids
   - Daily Reports
   - Budget
   - Schedule
   - Incidents

2. PlanGrid:
   - Documents
   - Daily Reports

3. FieldWire:
   - Documents
   - Daily Reports

4. BuildingConnected:
   - Bids

# Data Formats:
Each import function returns a standardized response dictionary:
- On success: {"data": [items], "source": "platform_name"}
- On error: {"error": "error_message"}

# Authentication:
This module relies on the authentication module to provide credentials
for API requests. Make sure authentication is properly configured before
using the import functions.

# Mock Data:
For development and demonstration purposes, this module includes mock data 
generators that simulate API responses. These are used when actual API
connections aren't available or during testing.
"""

import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
import os
from typing import Dict, List, Any, Optional

# Mock data functions for demonstration
# In a production environment, these would be replaced with actual API calls
def get_mock_documents(platform: str, count: int = 10) -> List[Dict]:
    """Generate mock document data for demonstration."""
    document_types = {
        "procore": ["Submittal", "Drawing", "RFI", "Contract", "Specification", "Invoice"],
        "plangrid": ["Sheet", "Drawing", "Punch List", "Task", "Field Report"],
        "fieldwire": ["Drawing", "Task", "Photo", "Form", "Report"],
        "buildingconnected": ["Bid", "RFI", "Prequalification", "Scope", "Contract"]
    }
    
    types = document_types.get(platform, ["Document"])
    
    documents = []
    for i in range(1, count + 1):
        doc_type = types[i % len(types)]
        documents.append({
            "id": f"{platform}-doc-{i}",
            "name": f"{doc_type} {i} - {platform.capitalize()} Sample",
            "type": doc_type,
            "size": f"{(i * 1.5) % 10:.1f} MB",
            "created_at": (datetime.now().replace(day=i % 28 + 1)).strftime("%Y-%m-%d"),
            "updated_at": (datetime.now().replace(day=i % 28 + 1)).strftime("%Y-%m-%d"),
            "status": ["Draft", "In Review", "Approved", "Rejected"][i % 4],
            "url": f"https://example.com/{platform}/documents/{i}"
        })
    
    return documents

def get_mock_specifications(count: int = 5) -> List[Dict]:
    """Generate mock specification data for demonstration."""
    specs = []
    divisions = [
        "Division 01 - General Requirements",
        "Division 03 - Concrete",
        "Division 04 - Masonry",
        "Division 05 - Metals",
        "Division 07 - Thermal and Moisture Protection",
        "Division 08 - Openings",
        "Division 09 - Finishes",
        "Division 22 - Plumbing",
        "Division 23 - HVAC",
        "Division 26 - Electrical"
    ]
    
    for i in range(1, count + 1):
        division = divisions[i % len(divisions)]
        specs.append({
            "id": f"spec-{i}",
            "name": f"{division} Specifications",
            "division": division,
            "section": f"Section {i * 100:04d}",
            "revision": f"Rev {i % 3}",
            "date": (datetime.now().replace(day=i % 28 + 1)).strftime("%Y-%m-%d"),
            "status": ["Draft", "For Review", "Approved", "For Construction"][i % 4],
            "size": f"{(i * 0.8) % 5:.1f} MB"
        })
    
    return specs

def get_mock_bid_data(count: int = 8) -> List[Dict]:
    """Generate mock bidding data for demonstration."""
    bids = []
    trades = ["Concrete", "Masonry", "Steel", "Carpentry", "Plumbing", "HVAC", "Electrical", "Landscaping"]
    
    for i in range(1, count + 1):
        trade = trades[i % len(trades)]
        bids.append({
            "id": f"bid-{i}",
            "trade": trade,
            "contractor": f"{trade} Specialists Inc.",
            "amount": f"${i * 125000:,}",
            "submitted": (datetime.now().replace(day=i % 28 + 1)).strftime("%Y-%m-%d"),
            "status": ["Received", "Under Review", "Shortlisted", "Awarded", "Rejected"][i % 5],
            "documents": i % 5 + 1
        })
    
    return bids

def get_mock_daily_reports(count: int = 7) -> List[Dict]:
    """Generate mock daily report data for demonstration."""
    reports = []
    
    for i in range(1, count + 1):
        reports.append({
            "id": f"report-{i}",
            "date": (datetime.now().replace(day=i % 28 + 1)).strftime("%Y-%m-%d"),
            "author": ["John Smith", "Sarah Johnson", "Michael Chen", "David Brown"][i % 4],
            "weather": ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"][i % 4],
            "temp_high": f"{65 + i % 15}°F",
            "temp_low": f"{45 + i % 15}°F",
            "workers": 15 + i % 20,
            "activities": ["Concrete Pouring", "Steel Erection", "Framing", "Electrical", "Plumbing"][i % 5],
            "notes": f"Day {i} of construction. Progress on schedule."
        })
    
    return reports

def get_mock_budget_data() -> Dict:
    """Generate mock budget data for demonstration."""
    budget_items = []
    categories = [
        "Preconstruction", "Site Work", "Concrete", "Masonry", "Metals", 
        "Wood & Plastics", "Thermal & Moisture", "Openings", "Finishes", 
        "Specialties", "Equipment", "Furnishings", "Special Construction", 
        "Conveying Systems", "Mechanical", "Electrical"
    ]
    
    for i, category in enumerate(categories):
        original = (i + 1) * 450000
        current = original + (i % 3 - 1) * 50000
        committed = current * (0.6 + (i % 5) * 0.1)
        spent = committed * (0.1 + (i % 10) * 0.1)
        
        budget_items.append({
            "id": f"budget-{i+1}",
            "category": category,
            "original_budget": f"${original:,}",
            "current_budget": f"${current:,}",
            "committed": f"${committed:.0f}",
            "spent": f"${spent:.0f}",
            "remaining": f"${current - spent:.0f}",
            "percent_complete": f"{(spent / current * 100):.1f}%"
        })
    
    summary = {
        "total_original": "$45,000,000",
        "total_current": "$45,500,000",
        "total_committed": "$32,150,000",
        "total_spent": "$18,725,000",
        "total_remaining": "$26,775,000",
        "overall_percent": "41.2%"
    }
    
    return {
        "items": budget_items,
        "summary": summary
    }

def get_mock_schedule_data() -> Dict:
    """Generate mock schedule data for demonstration."""
    tasks = []
    categories = [
        "Preconstruction", "Permitting", "Site Work", "Foundation", 
        "Structure", "Envelope", "Roofing", "MEP Rough-In",
        "Interior Framing", "Drywall", "Finishes", "MEP Finishes",
        "Commissioning", "Punchlist", "Final Inspection", "Closeout"
    ]
    
    start_date = datetime(2024, 10, 1)
    
    for i, category in enumerate(categories):
        duration = 20 + (i % 5) * 10
        start = start_date.replace(day=1 + (i * 15) % 28, month=((start_date.month - 1 + i // 2) % 12) + 1)
        end = start.replace(day=min(28, start.day + duration))
        
        actual_start = start
        if i < len(categories) // 2:  # Only earlier tasks have actual dates
            actual_end = actual_start.replace(day=min(28, actual_start.day + duration + (i % 3 - 1) * 5))
        else:
            actual_end = None
        
        tasks.append({
            "id": f"task-{i+1}",
            "name": category,
            "planned_start": start.strftime("%Y-%m-%d"),
            "planned_end": end.strftime("%Y-%m-%d"),
            "duration": f"{duration} days",
            "actual_start": actual_start.strftime("%Y-%m-%d") if i < len(categories) // 2 else "Not Started",
            "actual_end": actual_end.strftime("%Y-%m-%d") if actual_end else "In Progress" if i < len(categories) // 2 else "Not Started",
            "percent_complete": f"{min(100, i * 100 // len(categories) + (100 // len(categories)))}" if i < len(categories) // 2 else "0"
        })
    
    summary = {
        "start_date": "2024-10-01",
        "end_date": "2025-12-15",
        "duration": "440 days",
        "current_activity": "Interior Framing",
        "percent_complete": "42%",
        "on_schedule": "Yes"
    }
    
    return {
        "tasks": tasks,
        "summary": summary
    }

def get_mock_incidents(count: int = 5) -> List[Dict]:
    """Generate mock safety incident data for demonstration."""
    incidents = []
    
    incident_types = [
        "Near Miss", "First Aid", "Medical Treatment", "Lost Time", "Property Damage"
    ]
    
    for i in range(1, count + 1):
        incident_type = incident_types[i % len(incident_types)]
        incidents.append({
            "id": f"incident-{i}",
            "date": (datetime.now().replace(day=i % 28 + 1)).strftime("%Y-%m-%d"),
            "type": incident_type,
            "location": ["Level 3", "Basement", "East Wing", "Roof", "Site Perimeter"][i % 5],
            "reported_by": ["John Smith", "Sarah Johnson", "Michael Chen", "David Brown"][i % 4],
            "description": f"Incident involving {['falling object', 'slip and fall', 'equipment', 'electrical', 'material handling'][i % 5]}",
            "severity": ["Low", "Medium", "High"][i % 3],
            "status": ["Open", "Under Investigation", "Closed"][i % 3]
        })
    
    return incidents

# API Integration Functions
def get_integration_credentials(platform: str) -> Optional[Dict]:
    """Get the integration credentials for a platform from session state."""
    # Import here to avoid circular imports
    from modules.integrations.authentication import get_credentials, is_connected
    
    if not is_connected(platform):
        return None
    
    # Get stored credentials
    credentials = get_credentials(platform)
    if not credentials:
        return None
    
    # Return credentials with connection status
    return {"connected": True, "platform": platform, "credentials": credentials}

def fetch_procore_data(data_type: str) -> Dict:
    """
    Fetch data from Procore API.
    
    Args:
        data_type: Type of data to fetch (documents, specifications, bids, daily_reports, budget, schedule, incidents)
    
    Returns:
        Dictionary containing the fetched data or mock data for demonstration
    """
    credentials = get_integration_credentials("procore")
    if not credentials:
        st.error("Not connected to Procore. Please set up the integration first.")
        return {"error": "Not connected"}
    
    # In a real implementation, you would make actual API calls to Procore
    # For demonstration, we return mock data
    if data_type == "documents":
        return {"data": get_mock_documents("procore", 15), "source": "Procore"}
    elif data_type == "specifications":
        return {"data": get_mock_specifications(10), "source": "Procore"}
    elif data_type == "bids":
        return {"data": get_mock_bid_data(12), "source": "Procore"}
    elif data_type == "daily_reports":
        return {"data": get_mock_daily_reports(14), "source": "Procore"}
    elif data_type == "budget":
        return {"data": get_mock_budget_data(), "source": "Procore"}
    elif data_type == "schedule":
        return {"data": get_mock_schedule_data(), "source": "Procore"}
    elif data_type == "incidents":
        return {"data": get_mock_incidents(8), "source": "Procore"}
    else:
        return {"error": f"Unknown data type: {data_type}"}

def fetch_plangrid_data(data_type: str) -> Dict:
    """
    Fetch data from PlanGrid API.
    
    Args:
        data_type: Type of data to fetch (documents, sheets, tasks, field_reports)
    
    Returns:
        Dictionary containing the fetched data or mock data for demonstration
    """
    credentials = get_integration_credentials("plangrid")
    if not credentials:
        st.error("Not connected to PlanGrid. Please set up the integration first.")
        return {"error": "Not connected"}
    
    # In a real implementation, you would make actual API calls to PlanGrid
    # For demonstration, we return mock data
    if data_type == "documents":
        return {"data": get_mock_documents("plangrid", 12), "source": "PlanGrid"}
    elif data_type == "field_reports":
        return {"data": get_mock_daily_reports(10), "source": "PlanGrid"}
    else:
        return {"error": f"Unknown data type: {data_type}"}

def fetch_fieldwire_data(data_type: str) -> Dict:
    """
    Fetch data from FieldWire API.
    
    Args:
        data_type: Type of data to fetch (documents, tasks, daily_reports)
    
    Returns:
        Dictionary containing the fetched data or mock data for demonstration
    """
    credentials = get_integration_credentials("fieldwire")
    if not credentials:
        st.error("Not connected to FieldWire. Please set up the integration first.")
        return {"error": "Not connected"}
    
    # In a real implementation, you would make actual API calls to FieldWire
    # For demonstration, we return mock data
    if data_type == "documents":
        return {"data": get_mock_documents("fieldwire", 8), "source": "FieldWire"}
    elif data_type == "daily_reports":
        return {"data": get_mock_daily_reports(7), "source": "FieldWire"}
    else:
        return {"error": f"Unknown data type: {data_type}"}

def fetch_buildingconnected_data(data_type: str) -> Dict:
    """
    Fetch data from BuildingConnected API.
    
    Args:
        data_type: Type of data to fetch (bids, prequalifications, contracts)
    
    Returns:
        Dictionary containing the fetched data or mock data for demonstration
    """
    credentials = get_integration_credentials("buildingconnected")
    if not credentials:
        st.error("Not connected to BuildingConnected. Please set up the integration first.")
        return {"error": "Not connected"}
    
    # In a real implementation, you would make actual API calls to BuildingConnected
    # For demonstration, we return mock data
    if data_type == "bids":
        return {"data": get_mock_bid_data(15), "source": "BuildingConnected"}
    else:
        return {"error": f"Unknown data type: {data_type}"}

# Data import functions
def import_documents(platform: str) -> Dict:
    """Import documents from selected platform."""
    if platform == "procore":
        return fetch_procore_data("documents")
    elif platform == "plangrid":
        return fetch_plangrid_data("documents")
    elif platform == "fieldwire":
        return fetch_fieldwire_data("documents")
    else:
        return {"error": f"Document import not supported for {platform}"}

def import_specifications(platform: str) -> Dict:
    """Import specifications from selected platform."""
    if platform == "procore":
        return fetch_procore_data("specifications")
    else:
        return {"error": f"Specification import not supported for {platform}"}

def import_bids(platform: str) -> Dict:
    """Import bidding information from selected platform."""
    if platform == "procore":
        return fetch_procore_data("bids")
    elif platform == "buildingconnected":
        return fetch_buildingconnected_data("bids")
    else:
        return {"error": f"Bid import not supported for {platform}"}

def import_daily_reports(platform: str) -> Dict:
    """Import daily reports from selected platform."""
    if platform == "procore":
        return fetch_procore_data("daily_reports")
    elif platform == "plangrid":
        return fetch_plangrid_data("field_reports")
    elif platform == "fieldwire":
        return fetch_fieldwire_data("daily_reports")
    else:
        return {"error": f"Daily report import not supported for {platform}"}

def import_budget(platform: str) -> Dict:
    """Import budget information from selected platform."""
    if platform == "procore":
        return fetch_procore_data("budget")
    else:
        return {"error": f"Budget import not supported for {platform}"}

def import_schedule(platform: str) -> Dict:
    """Import schedule from selected platform."""
    if platform == "procore":
        return fetch_procore_data("schedule")
    else:
        return {"error": f"Schedule import not supported for {platform}"}

def import_incidents(platform: str) -> Dict:
    """Import safety incidents from selected platform."""
    if platform == "procore":
        return fetch_procore_data("incidents")
    else:
        return {"error": f"Incident import not supported for {platform}"}