import streamlit as st
import pandas as pd
from modules.base_module import BaseModule
from utils.database import get_db_connection
from utils.auth import check_permission

# Module metadata
MODULE_DISPLAY_NAME = "Safety Observations"
MODULE_ICON = "eye"

# Define module columns
COLUMNS = [
    ('id', 'ID', 'integer'),
    ('observation_date', 'Date', 'date'),
    ('observer', 'Observer', 'text'),
    ('location', 'Location', 'text'),
    ('observation_type', 'Type', 'text'),
    ('description', 'Description', 'text'),
    ('severity', 'Severity', 'text'),
    ('corrective_action', 'Corrective Action', 'text'),
    ('responsible_party', 'Responsible Party', 'text'),
    ('due_date', 'Due Date', 'date'),
    ('status', 'Status', 'text'),
    ('closed_date', 'Closed Date', 'date'),
    ('photo_reference', 'Photo Reference', 'text')
]

# Define form fields
FORM_FIELDS = [
    ('id', 'ID', 'integer', False, None),
    ('observation_date', 'Observation Date', 'date', True, None),
    ('observer', 'Observer Name', 'text', True, None),
    ('location', 'Location', 'text', True, None),
    ('observation_type', 'Observation Type', 'select', True, ['Unsafe Act', 'Unsafe Condition', 'Near Miss', 'Good Catch', 'Positive Observation']),
    ('description', 'Description', 'textarea', True, None),
    ('severity', 'Severity', 'select', True, ['Low', 'Medium', 'High', 'Critical']),
    ('corrective_action', 'Corrective Action', 'textarea', False, None),
    ('responsible_party', 'Responsible Party', 'text', False, None),
    ('due_date', 'Due Date', 'date', False, None),
    ('status', 'Status', 'select', True, ['Open', 'In Progress', 'Closed', 'Verified']),
    ('closed_date', 'Closed Date', 'date', False, None),
    ('photo_reference', 'Photo Reference', 'text', False, None)
]

# Create module instance
safety_observations_module = BaseModule('safety_observations', 'Safety Observations', COLUMNS, FORM_FIELDS)

def render_list():
    """Render the list view with additional safety analytics"""
    # Render the standard list view
    safety_observations_module.render_list()
    
    # Add safety analytics
    st.subheader("Safety Analytics")
    
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        # Get safety data
        safety_df = pd.read_sql_query("""
            SELECT observation_type, severity, status, observation_date
            FROM safety_observations
            ORDER BY observation_date DESC
        """, conn)
        
        conn.close()
        
        if not safety_df.empty:
            # Create two columns for charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Observation types chart
                st.subheader("Observation Types")
                type_counts = safety_df['observation_type'].value_counts()
                st.bar_chart(type_counts)
                
                # Severity distribution
                st.subheader("Severity Distribution")
                severity_counts = safety_df['severity'].value_counts()
                st.bar_chart(severity_counts)
            
            with col2:
                # Status distribution
                st.subheader("Status Distribution")
                status_counts = safety_df['status'].value_counts()
                st.bar_chart(status_counts)
                
                # Trend over time (by month)
                st.subheader("Observations Over Time")
                safety_df['month'] = pd.to_datetime(safety_df['observation_date']).dt.to_period('M')
                monthly_counts = safety_df.groupby('month').size()
                st.line_chart(monthly_counts)
        else:
            st.info("No safety observation data available")
            
    except Exception as e:
        st.error(f"Error fetching safety data: {str(e)}")

def render_view():
    """Render the detail view"""
    safety_observations_module.render_view()

def render_form():
    """Render the form view"""
    safety_observations_module.render_form()
