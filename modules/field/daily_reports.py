import streamlit as st
import pandas as pd
from datetime import datetime, date
from modules.base_module import BaseModule
from utils.database import get_db_connection
from utils.auth import check_permission

# Module metadata
MODULE_DISPLAY_NAME = "Daily Reports"
MODULE_ICON = "clipboard"

# Define module columns
COLUMNS = [
    ('id', 'ID', 'integer'),
    ('report_date', 'Report Date', 'date'),
    ('report_by', 'Reported By', 'text'),
    ('weather_conditions', 'Weather Conditions', 'text'),
    ('temperature_low', 'Temperature Low (°F)', 'integer'),
    ('temperature_high', 'Temperature High (°F)', 'integer'),
    ('precipitation', 'Precipitation (in)', 'float'),
    ('workforce_count', 'Workforce Count', 'integer'),
    ('work_performed', 'Work Performed', 'text'),
    ('issues', 'Issues', 'text'),
    ('materials_delivered', 'Materials Delivered', 'text'),
    ('equipment_on_site', 'Equipment on Site', 'text'),
    ('delays', 'Delays', 'text'),
    ('visitors', 'Visitors', 'text'),
    ('safety_incidents', 'Safety Incidents', 'text')
]

# Define form fields
FORM_FIELDS = [
    ('id', 'ID', 'integer', False, None),
    ('report_date', 'Report Date', 'date', True, None),
    ('report_by', 'Reported By', 'text', True, None),
    ('weather_conditions', 'Weather Conditions', 'select', True, ['Clear', 'Partly Cloudy', 'Cloudy', 'Rain', 'Snow', 'Fog', 'Windy', 'Storm']),
    ('temperature_low', 'Temperature Low (°F)', 'integer', False, None),
    ('temperature_high', 'Temperature High (°F)', 'integer', False, None),
    ('precipitation', 'Precipitation (in)', 'number', False, None),
    ('workforce_count', 'Workforce Count', 'integer', True, None),
    ('work_performed', 'Work Performed', 'textarea', True, None),
    ('issues', 'Issues', 'textarea', False, None),
    ('materials_delivered', 'Materials Delivered', 'textarea', False, None),
    ('equipment_on_site', 'Equipment on Site', 'textarea', False, None),
    ('delays', 'Delays', 'textarea', False, None),
    ('visitors', 'Visitors', 'textarea', False, None),
    ('safety_incidents', 'Safety Incidents', 'textarea', False, None)
]

# Create module instance
daily_reports_module = BaseModule('daily_reports', 'Daily Reports', COLUMNS, FORM_FIELDS)

def render_list():
    """Render the list view with additional weather visualization"""
    # Render the standard list view
    daily_reports_module.render_list()
    
    # Add weather visualization
    st.subheader("Weather Trends")
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        # Get weather data from daily reports
        weather_df = pd.read_sql_query("""
            SELECT report_date, temperature_low, temperature_high, precipitation, weather_conditions
            FROM daily_reports
            WHERE report_date BETWEEN CURRENT_DATE - INTERVAL '30 days' AND CURRENT_DATE
            ORDER BY report_date
        """, conn)
        
        conn.close()
        
        if not weather_df.empty:
            # Plot temperature trends
            st.subheader("Temperature Trends (Last 30 Days)")
            st.line_chart(weather_df.set_index('report_date')[['temperature_low', 'temperature_high']])
            
            # Plot precipitation
            st.subheader("Precipitation (Last 30 Days)")
            st.bar_chart(weather_df.set_index('report_date')['precipitation'])
            
            # Show weather conditions distribution
            st.subheader("Weather Conditions Distribution")
            weather_counts = weather_df['weather_conditions'].value_counts()
            st.bar_chart(weather_counts)
        else:
            st.info("No weather data available for the last 30 days")
        
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")

def render_view():
    """Render the detail view"""
    daily_reports_module.render_view()

def render_form():
    """Render the form view with weather API integration"""
    st.title("Daily Report Form")
    
    # Check permissions
    editing_id = st.session_state.get('editing_id')
    if editing_id and not check_permission('update'):
        st.error("You don't have permission to update records")
        return
    elif not editing_id and not check_permission('create'):
        st.error("You don't have permission to create records")
        return
    
    # Load weather data if creating a new report
    if not editing_id:
        st.info("Creating a new daily report. Weather data will be populated automatically if available.")
        
        # In a real application, we would fetch weather data from an API
        # For this example, we'll use placeholder data
        weather_data = {
            'conditions': 'Partly Cloudy',
            'temp_low': 58,
            'temp_high': 72,
            'precipitation': 0.0
        }
    
    # Call the standard form renderer
    daily_reports_module.render_form()
