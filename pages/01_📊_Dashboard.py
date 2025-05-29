"""
Dashboard Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import check_authentication, initialize_session_state
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Dashboard - gcPanel",
    page_icon="📊",
    layout="wide"
)

if not check_authentication():
    st.switch_page("app.py")

st.title("📊 Project Dashboard")
st.markdown("Highland Tower Development - $45.5M Mixed-Use Development")
st.markdown("---")

# Initialize session state
initialize_session_state()

# Project Overview Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Project Progress", "78.5%", "2.3%")

with col2:
    st.metric("Active RFIs", "12", "-3")

with col3:
    st.metric("Budget Status", "$35.2M", "Under")

with col4:
    st.metric("Schedule", "On Track", "1 day ahead")

# Charts and visualizations
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Progress Overview")
    progress_data = pd.DataFrame({
        'Phase': ['Foundation', 'Structure', 'MEP', 'Finishes'],
        'Progress': [95, 78, 45, 12]
    })
    
    fig = px.bar(progress_data, x='Phase', y='Progress', 
                title="Construction Phase Progress")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Budget Tracking")
    budget_data = pd.DataFrame({
        'Category': ['Labor', 'Materials', 'Equipment', 'Other'],
        'Spent': [12500000, 18200000, 3100000, 1400000],
        'Budget': [15000000, 20000000, 4000000, 2000000]
    })
    
    fig = px.bar(budget_data, x='Category', y=['Spent', 'Budget'],
                title="Budget vs Actual Spending", barmode='group')
    st.plotly_chart(fig, use_container_width=True)