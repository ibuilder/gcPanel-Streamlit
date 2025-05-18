"""
Error handling utilities for the application.

This module provides standardized error handling functions and classes
to ensure consistent error responses throughout the application.
"""

import logging
import traceback
import sys
from enum import Enum
from datetime import datetime

# Setup logging
logger = logging.getLogger(__name__)

class ErrorSeverity(Enum):
    """Severity levels for application errors"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Categories of application errors"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    DATABASE = "database"
    VALIDATION = "validation"
    EXTERNAL_SERVICE = "external_service"
    BUSINESS_LOGIC = "business_logic"
    SYSTEM = "system"
    UNKNOWN = "unknown"

class AppError:
    """
    Application error class for standardized error handling.
    
    Attributes:
        message (str): Human-readable error message
        severity (ErrorSeverity): Error severity level
        category (ErrorCategory): Error category
        code (str): Unique error code
        timestamp (datetime): When the error occurred
        details (dict): Additional error details
        traceback (str): Stack trace (only in development)
    """
    
    def __init__(
        self, 
        message, 
        severity=ErrorSeverity.ERROR,
        category=ErrorCategory.UNKNOWN,
        code=None,
        details=None,
        exception=None
    ):
        """Initialize error object with provided information"""
        self.message = message
        self.severity = severity
        self.category = category
        self.code = code or f"{category.value}_{severity.value}"
        self.timestamp = datetime.utcnow()
        self.details = details or {}
        self.traceback = None
        
        # Capture traceback if exception provided
        if exception:
            self.details["exception_type"] = type(exception).__name__
            self.details["exception_message"] = str(exception)
            self.traceback = "".join(traceback.format_exception(
                type(exception), exception, exception.__traceback__
            ))
    
    def to_dict(self, include_traceback=False):
        """Convert error to dictionary representation"""
        error_dict = {
            "message": self.message,
            "severity": self.severity.value,
            "category": self.category.value,
            "code": self.code,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details
        }
        
        if include_traceback and self.traceback:
            error_dict["traceback"] = self.traceback
            
        return error_dict
    
    def log(self):
        """Log the error with appropriate severity"""
        log_message = f"[{self.code}] {self.message}"
        
        if self.details:
            log_message += f" Details: {self.details}"
            
        if self.severity == ErrorSeverity.DEBUG:
            logger.debug(log_message, exc_info=self.traceback is not None)
        elif self.severity == ErrorSeverity.INFO:
            logger.info(log_message)
        elif self.severity == ErrorSeverity.WARNING:
            logger.warning(log_message)
        elif self.severity == ErrorSeverity.ERROR:
            logger.error(log_message, exc_info=self.traceback is not None)
        elif self.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message, exc_info=self.traceback is not None)

def handle_error(exception, message=None, severity=None, category=None, details=None):
    """
    Handle an exception with standardized error processing.
    
    Args:
        exception: The exception to handle
        message: Custom error message (defaults to exception message)
        severity: ErrorSeverity level (determined automatically if not provided)
        category: ErrorCategory (determined automatically if not provided)
        details: Additional error details
        
    Returns:
        AppError: Standardized error object
    """
    # Determine message
    if not message:
        message = str(exception)
    
    # Determine severity based on exception type
    if severity is None:
        if isinstance(exception, (ValueError, TypeError, KeyError)):
            severity = ErrorSeverity.WARNING
        else:
            severity = ErrorSeverity.ERROR
    
    # Determine category based on exception type and module
    if category is None:
        exception_module = exception.__class__.__module__
        
        if "auth" in exception_module:
            category = ErrorCategory.AUTHENTICATION
        elif "database" in exception_module or "sqlalchemy" in exception_module:
            category = ErrorCategory.DATABASE
        elif "validation" in exception_module:
            category = ErrorCategory.VALIDATION
        else:
            category = ErrorCategory.UNKNOWN
    
    # Create error object
    error = AppError(
        message=message,
        severity=severity,
        category=category,
        details=details,
        exception=exception
    )
    
    # Log the error
    error.log()
    
    return error

def format_user_error_message(error):
    """
    Format an error message suitable for displaying to end users.
    
    This function creates user-friendly error messages without exposing
    sensitive information.
    
    Args:
        error: AppError object or exception
        
    Returns:
        str: User-friendly error message
    """
    if isinstance(error, AppError):
        # Format based on error category
        if error.category == ErrorCategory.AUTHENTICATION:
            return "Authentication failed. Please check your credentials and try again."
        elif error.category == ErrorCategory.AUTHORIZATION:
            return "You don't have permission to perform this action."
        elif error.category == ErrorCategory.VALIDATION:
            return f"Invalid input: {error.message}"
        elif error.category == ErrorCategory.DATABASE:
            return "A database error occurred. Please try again later."
        elif error.category == ErrorCategory.EXTERNAL_SERVICE:
            return "Unable to communicate with an external service. Please try again later."
        else:
            return "An unexpected error occurred. Please try again later."
    else:
        # Generic message for raw exceptions
        return "An unexpected error occurred. Please try again later."

def capture_exception():
    """
    Capture the current exception information.
    
    This function should be called from within an except block.
    
    Returns:
        AppError: Standardized error object for the current exception
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return handle_error(exc_value)