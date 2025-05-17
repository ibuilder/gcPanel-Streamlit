"""
Breadcrumbs component for navigation.

This module provides a breadcrumb trail to show the user's current location in the application.
"""

import streamlit as st
from typing import List, Dict, Any, Optional, Tuple

def breadcrumbs(items: List[Dict[str, Any]], current_page: str) -> None:
    """
    Display breadcrumb navigation trail.
    
    Args:
        items: List of breadcrumb items, each with keys 'label' and 'path'
        current_page: The label of the current page
    """
    # Create the HTML for the breadcrumbs
    breadcrumbs_html = """
    <nav aria-label="breadcrumb" style="margin-bottom: 15px;">
        <ol class="breadcrumb" style="display: flex; list-style: none; padding: 0; margin: 0; background-color: transparent;">
    """
    
    # Add each breadcrumb item
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        is_current = item.get('label') == current_page
        
        if is_current or is_last:
            # Current page or last item (active)
            breadcrumbs_html += f"""
            <li class="breadcrumb-item active" style="color: #3e79f7; font-weight: 500;" aria-current="page">
                {item.get('label')}
            </li>
            """
        else:
            # Clickable breadcrumb
            breadcrumbs_html += f"""
            <li class="breadcrumb-item" style="margin-right: 10px;">
                <a href="#" style="color: #6c757d; text-decoration: none;" 
                   onclick="stSetQuery({{nav_to: '{item.get('path')}'}})">
                    {item.get('label')}
                </a>
                <span style="margin: 0 5px; color: #6c757d;">/</span>
            </li>
            """
    
    breadcrumbs_html += """
        </ol>
    </nav>
    """
    
    # Display the breadcrumbs
    st.markdown(breadcrumbs_html, unsafe_allow_html=True)

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
        
    elif page.startswith("Engineering"):
        breadcrumb_items.append({"label": "Engineering", "path": "Engineering"})
        
        if page == "Engineering/RFIs":
            breadcrumb_items.append({"label": "RFIs", "path": "Engineering/RFIs"})
        elif page == "Engineering/Submittals":
            breadcrumb_items.append({"label": "Submittals", "path": "Engineering/Submittals"})
            
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
    
    elif page.startswith("BIM"):
        breadcrumb_items.append({"label": "BIM", "path": "BIM"})
        
        if page == "BIM/Models":
            breadcrumb_items.append({"label": "Models", "path": "BIM/Models"})
        elif page == "BIM/Coordination":
            breadcrumb_items.append({"label": "Coordination", "path": "BIM/Coordination"})
    
    elif page.startswith("Settings"):
        breadcrumb_items.append({"label": "Settings", "path": "Settings"})
        
        if page == "Settings/Appearance":
            breadcrumb_items.append({"label": "Appearance", "path": "Settings/Appearance"})
        elif page == "Settings/User Preferences":
            breadcrumb_items.append({"label": "User Preferences", "path": "Settings/User Preferences"})
    
    return breadcrumb_items