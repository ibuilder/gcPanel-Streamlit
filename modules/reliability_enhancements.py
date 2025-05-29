"""
Highland Tower Development - Reliability and Stability Enhancements
Production-grade error handling, data validation, and performance optimizations
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import logging
from typing import Any, Dict, List, Optional, Union
import traceback
from datetime import datetime

class DataValidator:
    """Validates and sanitizes data for reliable processing"""
    
    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Clean dataframe for reliable Arrow serialization"""
        try:
            df_clean = df.copy()
            
            # Convert string numbers to proper numeric types
            for col in df_clean.columns:
                if df_clean[col].dtype == 'object':
                    # Try to convert to numeric if possible
                    numeric_converted = pd.to_numeric(df_clean[col], errors='ignore')
                    if numeric_converted.dtype != 'object':
                        df_clean[col] = numeric_converted
                    else:
                        # Ensure strings are clean
                        df_clean[col] = df_clean[col].astype(str)
            
            # Replace infinite values
            df_clean = df_clean.replace([float('inf'), float('-inf')], None)
            
            return df_clean
            
        except Exception as e:
            st.error(f"Data cleaning error: {e}")
            return df
    
    @staticmethod
    def validate_chart_data(data: pd.DataFrame, required_cols: List[str]) -> bool:
        """Validate data before chart creation"""
        try:
            # Check if dataframe exists and has data
            if data is None or data.empty:
                return False
                
            # Check required columns exist
            if not all(col in data.columns for col in required_cols):
                return False
                
            # Check for valid numeric data where expected
            for col in required_cols:
                if data[col].dtype in ['object'] and not data[col].str.isnumeric().all():
                    # Try to convert
                    try:
                        data[col] = pd.to_numeric(data[col], errors='coerce')
                    except:
                        continue
            
            return True
            
        except Exception:
            return False

class ChartRenderer:
    """Reliable chart rendering with comprehensive error handling"""
    
    @staticmethod
    def create_safe_line_chart(data: pd.DataFrame, x_col: str, y_cols: List[str], 
                              title: str = "", height: int = 400) -> Optional[go.Figure]:
        """Create line chart with comprehensive error handling"""
        try:
            if not DataValidator.validate_chart_data(data, [x_col] + y_cols):
                return None
                
            fig = go.Figure()
            
            colors = ['#0066cc', '#10b981', '#ef4444', '#f59e0b', '#8b5cf6']
            
            for i, y_col in enumerate(y_cols):
                color = colors[i % len(colors)]
                fig.add_trace(go.Scatter(
                    x=data[x_col],
                    y=data[y_col],
                    mode='lines+markers',
                    name=y_col,
                    line=dict(color=color, width=3),
                    marker=dict(size=6)
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title=x_col,
                yaxis_title="Value",
                height=height,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", size=12)
            )
            
            return fig
            
        except Exception as e:
            logging.error(f"Line chart creation error: {e}")
            return None
    
    @staticmethod
    def create_safe_bar_chart(data: pd.DataFrame, x_col: str, y_cols: List[str], 
                             title: str = "", height: int = 400) -> Optional[go.Figure]:
        """Create bar chart with comprehensive error handling"""
        try:
            if not DataValidator.validate_chart_data(data, [x_col] + y_cols):
                return None
                
            fig = go.Figure()
            
            colors = ['#ef4444', '#0066cc', '#10b981', '#f59e0b', '#8b5cf6']
            
            for i, y_col in enumerate(y_cols):
                color = colors[i % len(colors)]
                fig.add_trace(go.Bar(
                    x=data[x_col],
                    y=data[y_col],
                    name=y_col,
                    marker_color=color
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title=x_col,
                yaxis_title="Value",
                height=height,
                barmode='group',
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", size=12)
            )
            
            return fig
            
        except Exception as e:
            logging.error(f"Bar chart creation error: {e}")
            return None

class ErrorHandler:
    """Centralized error handling for Highland Tower platform"""
    
    @staticmethod
    def safe_execute(func, fallback_func=None, *args, **kwargs):
        """Execute function with error handling and optional fallback"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            logging.error(traceback.format_exc())
            
            if fallback_func:
                try:
                    return fallback_func(*args, **kwargs)
                except Exception as fe:
                    logging.error(f"Fallback function error: {fe}")
            
            st.error(f"System error occurred. Please refresh the page or contact support.")
            return None
    
    @staticmethod
    def display_chart_with_fallback(chart_func, data: pd.DataFrame, fallback_message: str = "Data table view"):
        """Display chart with table fallback"""
        try:
            chart = chart_func()
            if chart:
                st.plotly_chart(chart, use_container_width=True)
            else:
                raise Exception("Chart creation failed")
                
        except Exception as e:
            st.warning(f"Chart display issue - showing {fallback_message}")
            cleaned_data = DataValidator.clean_dataframe(data)
            st.dataframe(cleaned_data, use_container_width=True)

class SessionStateManager:
    """Reliable session state management"""
    
    @staticmethod
    def initialize_safe_state(key: str, default_value: Any) -> Any:
        """Initialize session state with error handling"""
        try:
            if key not in st.session_state:
                st.session_state[key] = default_value
            return st.session_state[key]
        except Exception as e:
            logging.error(f"Session state initialization error for {key}: {e}")
            return default_value
    
    @staticmethod
    def update_safe_state(key: str, value: Any) -> bool:
        """Update session state with error handling"""
        try:
            st.session_state[key] = value
            return True
        except Exception as e:
            logging.error(f"Session state update error for {key}: {e}")
            return False

class PerformanceOptimizer:
    """Performance optimization utilities"""
    
    @staticmethod
    @st.cache_data(ttl=300)  # 5 minute cache
    def cached_data_load(data_source: str) -> pd.DataFrame:
        """Cache data loading for performance"""
        try:
            # Simulate data loading - replace with actual data source
            if data_source == "highland_progress":
                return pd.DataFrame({
                    'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
                    'Planned': [15, 30, 45, 60, 75],
                    'Actual': [12, 28, 48, 65, 68]
                })
            elif data_source == "highland_costs":
                return pd.DataFrame({
                    'Phase': ['Foundation', 'Structure', 'MEP', 'Finishes', 'Sitework'],
                    'Spent': [8.5, 12.3, 6.8, 2.9, 0.7],
                    'Budget': [9.0, 13.5, 7.2, 4.8, 1.0]
                })
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logging.error(f"Data loading error for {data_source}: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def optimize_dataframe_display(df: pd.DataFrame, max_rows: int = 1000) -> pd.DataFrame:
        """Optimize dataframe for display"""
        try:
            if len(df) > max_rows:
                st.warning(f"Showing first {max_rows} rows of {len(df)} total rows")
                return df.head(max_rows)
            return df
        except Exception as e:
            logging.error(f"Dataframe optimization error: {e}")
            return df

def apply_reliability_enhancements():
    """Apply all reliability enhancements to the Highland Tower platform"""
    
    # Configure logging
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    
    # Initialize critical session state
    SessionStateManager.initialize_safe_state('reliability_mode', True)
    SessionStateManager.initialize_safe_state('error_count', 0)
    SessionStateManager.initialize_safe_state('last_error_time', None)
    
    # Set page config for reliability
    try:
        st.set_page_config(
            page_title="Highland Tower Development",
            page_icon="🏗️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except Exception:
        pass  # Page config already set
    
    return True