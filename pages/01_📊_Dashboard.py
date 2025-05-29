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

from utils.helpers import check_authentication
from components.dashboard_cards import render_dashboard_cards

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

# Dashboard content will be implemented here
render_dashboard_cards()