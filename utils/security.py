"""
Security utilities for gcPanel production deployment.

This module provides security functions for authentication, validation,
and protection against common web vulnerabilities.
"""
import hashlib
import secrets
import re
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import streamlit as st

logger = logging.getLogger(__name__)

class SecurityManager:
    """Manages security operations for the application."""
    
    def __init__(self):
        self.failed_attempts = {}
        self.blocked_ips = {}
        
    def validate_input(self, input_text: str, input_type: str = "general") -> Tuple[bool, str]:
        """
        Validate input for security issues.
        
        Args:
            input_text: The input to validate
            input_type: Type of input (email, password, general)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not input_text:
            return False, "Input cannot be empty"
            
        # Check for SQL injection patterns
        sql_patterns = [
            r'\bunion\b', r'\bselect\b', r'\bdrop\b', r'\bdelete\b',
            r'\binsert\b', r'\bupdate\b', r'--', r';', r'\bor\b.*=.*=',
            r'\band\b.*=.*=', r'\/\*', r'\*\/'
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, input_text, re.IGNORECASE):
                logger.warning(f"SQL injection attempt detected: {pattern}")
                return False, "Invalid characters detected"
        
        # Check for XSS patterns
        xss_patterns = [
            r'<script', r'javascript:', r'onload=', r'onerror=',
            r'onclick=', r'onmouseover=', r'<iframe', r'<object',
            r'<embed', r'<link', r'<meta'
        ]
        
        for pattern in xss_patterns:
            if re.search(pattern, input_text, re.IGNORECASE):
                logger.warning(f"XSS attempt detected: {pattern}")
                return False, "Invalid content detected"
        
        # Email validation
        if input_type == "email":
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, input_text):
                return False, "Invalid email format"
        
        # Password validation
        if input_type == "password":
            if len(input_text) < 8:
                return False, "Password must be at least 8 characters"
            if not re.search(r'[A-Z]', input_text):
                return False, "Password must contain uppercase letter"
            if not re.search(r'[a-z]', input_text):
                return False, "Password must contain lowercase letter"
            if not re.search(r'\d', input_text):
                return False, "Password must contain number"
        
        return True, ""
    
    def hash_password(self, password: str) -> str:
        """Hash password using secure method."""
        salt = secrets.token_hex(32)
        pwdhash = hashlib.pbkdf2_hmac('sha256',
                                     password.encode('utf-8'),
                                     salt.encode('utf-8'),
                                     100000)
        return salt + pwdhash.hex()
    
    def verify_password(self, stored_password: str, provided_password: str) -> bool:
        """Verify password against stored hash."""
        salt = stored_password[:64]
        stored_hash = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha256',
                                     provided_password.encode('utf-8'),
                                     salt.encode('utf-8'),
                                     100000)
        return stored_hash == pwdhash.hex()
    
    def check_rate_limit(self, identifier: str, limit: int = 60, window: int = 60) -> bool:
        """
        Check if identifier exceeds rate limit.
        
        Args:
            identifier: IP address or user identifier
            limit: Maximum requests per window
            window: Time window in seconds
            
        Returns:
            True if within limit, False if exceeded
        """
        now = datetime.now()
        
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = []
        
        # Remove old attempts outside window
        self.failed_attempts[identifier] = [
            attempt for attempt in self.failed_attempts[identifier]
            if now - attempt < timedelta(seconds=window)
        ]
        
        if len(self.failed_attempts[identifier]) >= limit:
            logger.warning(f"Rate limit exceeded for {identifier}")
            return False
        
        self.failed_attempts[identifier].append(now)
        return True
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe storage."""
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Remove leading/trailing dots and spaces
        sanitized = sanitized.strip('. ')
        # Limit length
        if len(sanitized) > 255:
            name, ext = os.path.splitext(sanitized)
            sanitized = name[:251-len(ext)] + ext
        return sanitized
    
    def validate_file_upload(self, file, allowed_extensions: List[str], max_size_mb: int) -> Tuple[bool, str]:
        """
        Validate uploaded file for security.
        
        Args:
            file: Uploaded file object
            allowed_extensions: List of allowed file extensions
            max_size_mb: Maximum file size in MB
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not file:
            return False, "No file provided"
        
        # Check file extension
        file_ext = '.' + file.name.split('.')[-1].lower()
        if file_ext not in allowed_extensions:
            return False, f"File type {file_ext} not allowed"
        
        # Check file size
        if hasattr(file, 'size') and file.size > max_size_mb * 1024 * 1024:
            return False, f"File size exceeds {max_size_mb}MB limit"
        
        return True, ""

def get_client_ip() -> str:
    """Get client IP address (mock implementation for demo)."""
    # In production, this would extract real IP from headers
    return "127.0.0.1"

def log_security_event(event_type: str, details: Dict, severity: str = "INFO"):
    """Log security events for monitoring."""
    timestamp = datetime.now().isoformat()
    client_ip = get_client_ip()
    
    log_entry = {
        'timestamp': timestamp,
        'event_type': event_type,
        'client_ip': client_ip,
        'details': details,
        'severity': severity
    }
    
    if severity == "CRITICAL":
        logger.critical(f"Security Event: {log_entry}")
    elif severity == "WARNING":
        logger.warning(f"Security Event: {log_entry}")
    else:
        logger.info(f"Security Event: {log_entry}")

# Global security manager instance
security_manager = SecurityManager()