"""
Professional header component for gcPanel.

A clean, modern header implemented with pure Python Streamlit components.
"""

import streamlit as st

def render_header():
    """
    Render a simple, clean header using only Streamlit components.
    """
    # Menu options for dropdown with icons
    menu_options = {
        "Dashboard": {"label": "Dashboard", "icon": "📊"},
        "Project Information": {"label": "Project Information", "icon": "📋"},
        "Schedule": {"label": "Schedule", "icon": "📅"},
        "Safety": {"label": "Safety", "icon": "⚠️"},
        "Contracts": {"label": "Contracts", "icon": "📝"},
        "Cost Management": {"label": "Cost Management", "icon": "💰"},
        "Engineering": {"label": "Engineering", "icon": "🔧"},
        "Field Operations": {"label": "Field Operations", "icon": "🏗️"},
        "Documents": {"label": "Documents", "icon": "📄"},
        "BIM Viewer": {"label": "BIM", "icon": "🏢"},
        "Closeout": {"label": "Closeout", "icon": "✅"},
        "Settings": {"label": "Settings", "icon": "⚙️"}
    }
    
    # Get currently selected menu value from session state
    current_menu = st.session_state.get("current_menu", "Dashboard")
    
    # Create a three-column layout for the header
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Center the gcPanel logo with tower crane icon
        st.markdown("""
        <div style="text-align: center; padding-top: 10px;">
            <span style="font-size: 24px; font-weight: 700;">
                🏗️ gc<span style="color: #3b82f6;">Panel</span>
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col1:
        # Left aligned project info (switched positions with logo)
        st.caption("Project")
        st.write("Highland Tower Development")
    
    with col3:
        # Right aligned dropdown
        st.markdown("""
        <div style="text-align: right; padding-bottom: 5px;">
            <span style="font-size: 14px; color: #6b7280;">Navigation</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Format options to include icons
        formatted_options = [f"{menu_options[k]['icon']} {menu_options[k]['label']}" for k in menu_options.keys()]
        
        # Create a mapping from formatted options back to keys
        option_to_key = {f"{menu_options[k]['icon']} {menu_options[k]['label']}": k for k in menu_options.keys()}
        
        # Find current menu's formatted option
        current_formatted = f"{menu_options[current_menu]['icon']} {menu_options[current_menu]['label']}"
        
        selected_formatted = st.selectbox(
            "Navigation",
            options=formatted_options,
            index=formatted_options.index(current_formatted),
            key="header_nav_dropdown",
            label_visibility="collapsed"
        )
        
        # Convert selected formatted option back to key
        selected = option_to_key[selected_formatted]
        
        # Update session state if menu changed
        if selected != current_menu:
            st.session_state.current_menu = selected
            st.rerun()
    
    # Display a divider
    st.divider()
    
    # Breadcrumb and notification row
    col1, col2 = st.columns([11, 1])
    
    with col1:
        # Simple breadcrumb
        st.markdown(f'<span style="color: #3b82f6;">[Home](#)</span> > {current_menu}', unsafe_allow_html=True)
    
    with col2:
        # Fixed notification button (single instance, right-aligned)
        st.markdown(
            f'<div style="text-align: right;"><span style="position: relative; font-size: 1.2rem;">🔔<span style="position: absolute; top: -8px; right: -8px; background-color: #ef4444; color: white; border-radius: 50%; font-size: 0.7rem; padding: 2px 5px;">3</span></span></div>',
            unsafe_allow_html=True
        )