"""
Simple breadcrumbs component for navigation.

This module provides a simple breadcrumb trail using Streamlit's native components.
"""

import streamlit as st
from typing import List, Dict, Any

def simple_breadcrumbs(items: List[Dict[str, Any]]) -> None:
    """
    Display a simplified breadcrumb navigation trail using Streamlit components.
    
    Args:
        items: List of breadcrumb items, each with keys 'label' and 'path'
    """
    # Apply custom CSS for improved breadcrumb styling
    st.markdown("""
    <style>
    .breadcrumb-container {
        display: flex;
        align-items: center;
        padding: 10px 0;
        margin-bottom: 15px;
        overflow-x: auto;
        white-space: nowrap;
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 6px;
        padding: 8px 16px;
    }
    .breadcrumb-item {
        display: inline-flex;
        align-items: center;
        font-size: 14px;
        color: #6b7280;
        transition: color 0.2s ease;
        padding: 4px 8px;
        border-radius: 4px;
    }
    .breadcrumb-item.active {
        font-weight: 500;
        color: #3b82f6;
        background-color: rgba(59, 130, 246, 0.08);
    }
    .breadcrumb-item:not(.active):hover {
        color: #3b82f6;
        background-color: rgba(59, 130, 246, 0.05);
    }
    .breadcrumb-separator {
        margin: 0 5px;
        color: #9ca3af;
        font-size: 16px;
    }
    .stButton button {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        color: #6b7280 !important;
        font-size: 14px;
        padding: 2px 8px !important;
        height: auto !important;
        transition: all 0.2s ease;
        margin: 0 !important;
        min-width: auto !important;
    }
    .stButton button:hover {
        color: #3b82f6 !important;
        background-color: rgba(59, 130, 246, 0.05) !important;
        transform: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create HTML for breadcrumbs
    breadcrumb_html = '<div class="breadcrumb-container">'
    
    # Add each breadcrumb item
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        label = item.get('label', '')
        path = item.get('path', 'Dashboard')
        
        # Generate unique ID for each breadcrumb
        item_id = f"breadcrumb_{path.lower().replace(' ', '_')}_{i}"
        
        if is_last:
            # Current page (no click action)
            breadcrumb_html += f'<div class="breadcrumb-item active" id="{item_id}">{label}</div>'
        else:
            # Clickable breadcrumb
            breadcrumb_html += f'<div class="breadcrumb-item" id="{item_id}" onclick="window.parent.postMessage({{type: \'streamlit:setComponentValue\', key: \'{item_id}_clicked\', value: true}}, \'*\')" style="cursor: pointer;">{label}</div>'
        
        # Add separator
        if not is_last:
            breadcrumb_html += '<div class="breadcrumb-separator">›</div>'
    
    breadcrumb_html += '</div>'
    
    # Render the breadcrumb container
    st.markdown(breadcrumb_html, unsafe_allow_html=True)
    
    # Handle breadcrumb clicks
    for i, item in enumerate(items):
        if i == len(items) - 1:  # Skip the last (current) item
            continue
            
        path = item.get('path', 'Dashboard')
        item_id = f"breadcrumb_{path.lower().replace(' ', '_')}_{i}_clicked"
        
        if st.session_state.get(item_id, False):
            st.session_state[item_id] = False
            st.session_state.current_menu = path
            st.rerun()

def get_breadcrumbs_for_page(page: str) -> List[Dict[str, Any]]:
    """
    Get breadcrumb trail for a specific page.
    
    Args:
        page: The current page name
        
    Returns:
        List of breadcrumb items for the current page
    """
    # Base breadcrumb (Home)
    breadcrumb_items = [{"label": "Home", "path": "Dashboard"}]
    
    # Define breadcrumb paths for different sections
    if page == "Dashboard":
        return breadcrumb_items
    
    elif page == "Project Information":
        breadcrumb_items.append({"label": "Project Information", "path": "Project Information"})
        
    elif page == "Engineering & Documents" or page.startswith("Engineering & Documents"):
        breadcrumb_items.append({"label": "Engineering & Documents", "path": "Engineering & Documents"})
        
        if page == "Engineering & Documents/RFIs":
            breadcrumb_items.append({"label": "RFIs", "path": "Engineering & Documents/RFIs"})
        elif page == "Engineering & Documents/Submittals":
            breadcrumb_items.append({"label": "Submittals", "path": "Engineering & Documents/Submittals"})
        elif page == "Engineering & Documents/Drawings":
            breadcrumb_items.append({"label": "Drawings", "path": "Engineering & Documents/Drawings"})
            
    elif page == "BIM":
        breadcrumb_items.append({"label": "BIM", "path": "BIM"})
            
    elif page.startswith("Field Operations"):
        breadcrumb_items.append({"label": "Field Operations", "path": "Field Operations"})
        
        if page == "Field Operations/Daily Reports":
            breadcrumb_items.append({"label": "Daily Reports", "path": "Field Operations/Daily Reports"})
        elif page == "Field Operations/Quality Control":
            breadcrumb_items.append({"label": "Quality Control", "path": "Field Operations/Quality Control"})
    
    elif page.startswith("Safety"):
        breadcrumb_items.append({"label": "Safety", "path": "Safety"})
        
        if page == "Safety/Incidents":
            breadcrumb_items.append({"label": "Incidents", "path": "Safety/Incidents"})
        elif page == "Safety/Training":
            breadcrumb_items.append({"label": "Training", "path": "Safety/Training"})
    
    elif page.startswith("Contracts"):
        breadcrumb_items.append({"label": "Contracts", "path": "Contracts"})
        
        if page == "Contracts/Subcontracts":
            breadcrumb_items.append({"label": "Subcontracts", "path": "Contracts/Subcontracts"})
        elif page == "Contracts/Change Orders":
            breadcrumb_items.append({"label": "Change Orders", "path": "Contracts/Change Orders"})
    
    elif page.startswith("Cost Management"):
        breadcrumb_items.append({"label": "Cost Management", "path": "Cost Management"})
        
        if page == "Cost Management/Budget":
            breadcrumb_items.append({"label": "Budget", "path": "Cost Management/Budget"})
        elif page == "Cost Management/Forecasting":
            breadcrumb_items.append({"label": "Forecasting", "path": "Cost Management/Forecasting"})
    
    elif page == "Settings":
        breadcrumb_items.append({"label": "Settings", "path": "Settings"})
    
    return breadcrumb_items