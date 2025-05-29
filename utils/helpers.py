"""
Helper functions for gcPanel application
"""

import streamlit as st
import pandas as pd
from datetime import datetime

def check_authentication() -> bool:
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    return st.session_state.authenticated

def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'username' not in st.session_state:
        st.session_state.username = ""
    
    if 'user_role' not in st.session_state:
        st.session_state.user_role = ""
    
    if 'daily_reports' not in st.session_state:
        st.session_state.daily_reports = []
    
    if 'contracts' not in st.session_state:
        st.session_state.contracts = []
    
    if 'rfis' not in st.session_state:
        st.session_state.rfis = []

def clean_dataframe_for_display(df):
    """Clean DataFrame to prevent Arrow serialization errors"""
    if df is None or df.empty:
        return df
    
    # Convert all columns to string to prevent serialization issues
    cleaned_df = df.copy()
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype == 'object':
            cleaned_df[col] = cleaned_df[col].astype(str)
        elif pd.api.types.is_datetime64_any_dtype(cleaned_df[col]):
            cleaned_df[col] = cleaned_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    return cleaned_df