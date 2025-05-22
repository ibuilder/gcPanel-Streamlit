"""
Production Error Handler for gcPanel

This module provides centralized error handling and logging for production deployment.
"""
import logging
import traceback
import streamlit as st
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class ProductionErrorHandler:
    """Handles errors in a production-safe manner."""
    
    @staticmethod
    def handle_error(error: Exception, context: Optional[Dict[str, Any]] = None, 
                     user_message: str = "An error occurred. Please try again.") -> None:
        """
        Handle errors in production environment.
        
        Args:
            error: The exception that occurred
            context: Additional context about the error
            user_message: User-friendly error message
        """
        error_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Log the full error details for debugging
        logger.error(f"Error ID: {error_id}")
        logger.error(f"Error Type: {type(error).__name__}")
        logger.error(f"Error Message: {str(error)}")
        logger.error(f"Context: {context}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Show user-friendly error message
        st.error(f"{user_message} (Error ID: {error_id})")
        
    @staticmethod
    def handle_data_error(error: Exception, operation: str = "data operation") -> None:
        """Handle data-related errors."""
        ProductionErrorHandler.handle_error(
            error,
            context={"operation": operation},
            user_message=f"Unable to complete {operation}. Please check your data and try again."
        )
        
    @staticmethod
    def handle_auth_error(error: Exception) -> None:
        """Handle authentication errors."""
        ProductionErrorHandler.handle_error(
            error,
            context={"type": "authentication"},
            user_message="Authentication failed. Please check your credentials and try again."
        )
        
    @staticmethod
    def handle_file_error(error: Exception, filename: str = "") -> None:
        """Handle file operation errors."""
        ProductionErrorHandler.handle_error(
            error,
            context={"type": "file_operation", "filename": filename},
            user_message="File operation failed. Please check the file and try again."
        )

def safe_execute(func, *args, **kwargs):
    """
    Safely execute a function with error handling.
    
    Args:
        func: Function to execute
        *args: Function arguments
        **kwargs: Function keyword arguments
        
    Returns:
        Function result or None if error occurred
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        ProductionErrorHandler.handle_error(e)
        return None