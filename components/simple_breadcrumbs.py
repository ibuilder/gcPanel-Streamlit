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
    # Create a horizontal layout for the breadcrumbs
    cols = st.columns(len(items) * 2 - 1)
    
    # Add each breadcrumb item
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        
        # Breadcrumb item (in even columns)
        with cols[i * 2]:
            if is_last:
                # Current page (no click action)
                st.markdown(f"<div style='color: #3e79f7; font-weight: 500;'>{item.get('label')}</div>", unsafe_allow_html=True)
            else:
                # Clickable breadcrumb
                label = item.get('label', '')
                if st.button(label, key=f"breadcrumb_{i}", type="secondary", use_container_width=True):
                    st.session_state.menu = item.get('path', 'Dashboard')
                    st.rerun()
        
        # Separator (in odd columns)
        if not is_last:
            with cols[i * 2 + 1]:
                st.markdown("<div style='text-align: center; color: #6c757d;'>›</div>", unsafe_allow_html=True)

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