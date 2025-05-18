"""
Pagination utilities for gcPanel.

This module provides functions for implementing database query pagination,
especially for large datasets, to improve load times and performance.
"""

import streamlit as st
import math

def paginate_query(query, page=1, per_page=25):
    """
    Paginate a SQLAlchemy query.
    
    Args:
        query: SQLAlchemy query object
        page: Page number (starting from 1)
        per_page: Items per page
        
    Returns:
        tuple: (paginated_query, total_pages, total_items)
    """
    # Get total count without loading all records
    total = query.count()
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    
    # Adjust page if out of bounds
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    # Apply pagination
    offset = (page - 1) * per_page
    paginated_query = query.limit(per_page).offset(offset)
    
    return paginated_query, total_pages, total

def render_pagination_controls(current_page, total_pages, on_page_change=None, 
                              align="center", key_prefix="page_control"):
    """
    Render pagination controls in Streamlit.
    
    Args:
        current_page: Current page number
        total_pages: Total number of pages
        on_page_change: Callback function when page changes
        align: Alignment of controls ("left", "center", or "right")
        key_prefix: Prefix for control keys to avoid conflicts
        
    Returns:
        int: New page number if changed, otherwise current_page
    """
    if total_pages <= 1:
        return current_page
    
    # Create container based on alignment
    if align == "center":
        cols = st.columns([1, 3, 1])
        container = cols[1]
    elif align == "right":
        cols = st.columns([4, 1])
        container = cols[1]
    else:  # left
        container = st
    
    with container:
        # Create a row for pagination controls
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        
        # Previous page button
        with col1:
            prev_disabled = current_page <= 1
            if st.button("⬅️", key=f"{key_prefix}_prev", disabled=prev_disabled):
                current_page -= 1
                if on_page_change:
                    on_page_change(current_page)
        
        # Go to first page
        with col2:
            first_disabled = current_page <= 1
            if st.button("⏮️", key=f"{key_prefix}_first", disabled=first_disabled):
                current_page = 1
                if on_page_change:
                    on_page_change(current_page)
        
        # Page indicator
        with col3:
            st.markdown(f"<div style='text-align: center'>Page {current_page} of {total_pages}</div>", unsafe_allow_html=True)
        
        # Go to last page
        with col4:
            last_disabled = current_page >= total_pages
            if st.button("⏭️", key=f"{key_prefix}_last", disabled=last_disabled):
                current_page = total_pages
                if on_page_change:
                    on_page_change(current_page)
        
        # Next page button
        with col5:
            next_disabled = current_page >= total_pages
            if st.button("➡️", key=f"{key_prefix}_next", disabled=next_disabled):
                current_page += 1
                if on_page_change:
                    on_page_change(current_page)
    
    return current_page

def initialize_session_pagination_state(key, default_page=1, default_per_page=25):
    """
    Initialize pagination state in session.
    
    Args:
        key: Key for this pagination state
        default_page: Default page number
        default_per_page: Default items per page
    """
    pagination_key = f"pagination_{key}"
    
    if pagination_key not in st.session_state:
        st.session_state[pagination_key] = {
            "page": default_page,
            "per_page": default_per_page
        }

def get_pagination_state(key):
    """
    Get pagination state from session.
    
    Args:
        key: Key for this pagination state
        
    Returns:
        dict: Pagination state
    """
    pagination_key = f"pagination_{key}"
    
    if pagination_key not in st.session_state:
        initialize_session_pagination_state(key)
    
    return st.session_state[pagination_key]

def set_pagination_state(key, page=None, per_page=None):
    """
    Set pagination state in session.
    
    Args:
        key: Key for this pagination state
        page: Page number to set
        per_page: Items per page to set
    """
    pagination_key = f"pagination_{key}"
    
    if pagination_key not in st.session_state:
        initialize_session_pagination_state(key)
    
    if page is not None:
        st.session_state[pagination_key]["page"] = page
    
    if per_page is not None:
        st.session_state[pagination_key]["per_page"] = per_page

def paginated_data_display(data, key, display_function, 
                          per_page_options=None, default_per_page=25,
                          align="center"):
    """
    Display paginated data with controls.
    
    Args:
        data: List of data items to paginate
        key: Key for this pagination state
        display_function: Function to display a single page of data
        per_page_options: List of items per page options
        default_per_page: Default items per page
        align: Alignment of pagination controls
    """
    # Initialize pagination state
    initialize_session_pagination_state(key, default_page=1, default_per_page=default_per_page)
    pagination_state = get_pagination_state(key)
    
    # Items per page selector
    if per_page_options:
        col1, col2 = st.columns([1, 4])
        with col1:
            new_per_page = st.selectbox(
                "Items per page", 
                per_page_options,
                index=per_page_options.index(pagination_state["per_page"]) if pagination_state["per_page"] in per_page_options else 0,
                key=f"{key}_per_page"
            )
            
            if new_per_page != pagination_state["per_page"]:
                pagination_state["per_page"] = new_per_page
                pagination_state["page"] = 1  # Reset to first page
    
    # Calculate pagination
    total_items = len(data)
    per_page = pagination_state["per_page"]
    total_pages = math.ceil(total_items / per_page) if total_items > 0 else 1
    current_page = pagination_state["page"]
    
    # Adjust current page if out of bounds
    if current_page < 1:
        current_page = 1
    if current_page > total_pages:
        current_page = total_pages
    
    # Get current page data
    start_idx = (current_page - 1) * per_page
    end_idx = min(start_idx + per_page, total_items)
    page_data = data[start_idx:end_idx]
    
    # Display the data
    display_function(page_data)
    
    # Render pagination controls
    def on_page_change(new_page):
        pagination_state["page"] = new_page
    
    new_page = render_pagination_controls(
        current_page, 
        total_pages, 
        on_page_change=on_page_change,
        align=align,
        key_prefix=f"{key}_pagination"
    )
    
    # Update page if changed
    if new_page != current_page:
        pagination_state["page"] = new_page