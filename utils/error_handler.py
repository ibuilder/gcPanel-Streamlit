"""
Enterprise Error Handler for Highland Tower Development Dashboard

Production-grade error handling and recovery system.
"""

import streamlit as st
import logging
import traceback
from datetime import datetime
from typing import Any, Callable, Optional
import functools

class ProductionErrorHandler:
    """Enterprise-grade error handler for Highland Tower Development."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup production logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/highland_tower_errors.log'),
                logging.StreamHandler()
            ]
        )
    
    def handle_gracefully(self, func: Callable) -> Callable:
        """Decorator for graceful error handling."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self._log_error(func.__name__, e)
                self._display_user_friendly_error(func.__name__, str(e))
                return None
        return wrapper
    
    def _log_error(self, function_name: str, error: Exception):
        """Log error with full context."""
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "function": function_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "user": st.session_state.get("current_user", {}).get("name", "Unknown"),
            "session_id": st.session_state.get("session_id", "unknown")
        }
        
        self.logger.error(f"Highland Tower Error: {error_data}")
    
    def _display_user_friendly_error(self, context: str, error_message: str):
        """Display user-friendly error message."""
        st.error(f"""
        🚧 **Highland Tower Development - Temporary Issue**
        
        We encountered a minor issue while processing your {context} request. 
        Our team has been notified and is working on a solution.
        
        **What you can do:**
        - Try refreshing the page
        - Contact your project administrator
        - Check back in a few minutes
        
        **Error Reference:** {datetime.now().strftime('%Y%m%d-%H%M%S')}
        """)

# Global error handler instance
error_handler = ProductionErrorHandler()