"""
Security utilities for gcPanel.

This module provides security hardening functions to protect 
against common web vulnerabilities.
"""

import re
import html
import secrets
import logging
from urllib.parse import urlparse

# Setup logging
logger = logging.getLogger(__name__)

def generate_csrf_token():
    """
    Generate a secure CSRF token.
    
    Returns:
        str: A secure random token
    """
    return secrets.token_hex(32)

def validate_csrf_token(session_token, request_token):
    """
    Validate CSRF token using constant time comparison.
    
    Args:
        session_token: Token stored in session
        request_token: Token from request
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not session_token or not request_token:
        return False
    
    # Use constant time comparison to prevent timing attacks
    return secrets.compare_digest(session_token, request_token)

def sanitize_input(input_string):
    """
    Sanitize user input to prevent XSS attacks.
    
    Args:
        input_string: String to sanitize
        
    Returns:
        str: Sanitized string
    """
    if not input_string:
        return ""
    
    # Convert to string if not already
    if not isinstance(input_string, str):
        input_string = str(input_string)
    
    # HTML escape
    return html.escape(input_string)

def validate_url(url):
    """
    Validate URL to prevent open redirect vulnerabilities.
    
    Args:
        url: URL to validate
        
    Returns:
        bool: True if safe, False otherwise
    """
    if not url:
        return False
    
    try:
        # Parse URL
        parsed = urlparse(url)
        
        # Only allow http and https schemes
        if parsed.scheme not in ('http', 'https'):
            return False
        
        # Check if domain and path exist
        if not parsed.netloc or parsed.netloc == '':
            return False
            
        return True
    except Exception as e:
        logger.error(f"URL validation error: {str(e)}")
        return False

def validate_redirect_url(url, allowed_domains=None):
    """
    Validate redirect URL to prevent open redirect vulnerabilities.
    
    Args:
        url: Redirect URL to validate
        allowed_domains: List of allowed domains
        
    Returns:
        bool: True if safe, False otherwise
    """
    if not url:
        return False
    
    try:
        # Parse URL
        parsed = urlparse(url)
        
        # Allow relative URLs
        if not parsed.netloc:
            return True
            
        # Check against allowed domains
        if allowed_domains and parsed.netloc in allowed_domains:
            return True
            
        # Disallow external domains by default
        return False
    except Exception as e:
        logger.error(f"Redirect URL validation error: {str(e)}")
        return False

def validate_filename(filename):
    """
    Validate filenames to prevent path traversal attacks.
    
    Args:
        filename: Filename to validate
        
    Returns:
        bool: True if safe, False otherwise
    """
    if not filename:
        return False
    
    # Check for directory traversal patterns
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    
    # Only allow alphanumeric, dash, underscore, and period
    if not re.match(r'^[\w\-\.]+$', filename):
        return False
        
    return True

def set_security_headers():
    """
    Get security headers for HTTP response.
    
    Returns:
        dict: Security headers
    """
    headers = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;",
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Cache-Control': 'no-store, max-age=0'
    }
    
    # Return headers to be applied as needed
    return headers

def apply_security_headers():
    """
    Apply security headers using Streamlit.
    """
    headers = set_security_headers()
    
    # Apply headers through HTML since Streamlit doesn't provide direct header control
    header_html = '<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; script-src \'self\' \'unsafe-inline\' \'unsafe-eval\'; style-src \'self\' \'unsafe-inline\'; img-src \'self\' data:;">'
    header_html += '<meta http-equiv="X-Content-Type-Options" content="nosniff">'
    header_html += '<meta http-equiv="X-Frame-Options" content="SAMEORIGIN">'
    header_html += '<meta http-equiv="X-XSS-Protection" content="1; mode=block">'
    header_html += '<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">'
    
    import streamlit as st
    st.markdown(header_html, unsafe_allow_html=True)

def secure_file_upload(uploaded_file):
    """
    Securely handle file uploads.
    
    Args:
        uploaded_file: File from streamlit file_uploader
        
    Returns:
        tuple: (is_safe, message)
    """
    if not uploaded_file:
        return False, "No file provided"
    
    # Validate filename
    if not validate_filename(uploaded_file.name):
        return False, "Invalid filename. Only alphanumeric characters, dashes, underscores, and periods are allowed."
    
    # Check file size (limit to 10MB)
    if uploaded_file.size > 10 * 1024 * 1024:
        return False, "File too large. Maximum size is 10MB."
    
    # Basic content type validation
    allowed_types = {
        'text/plain', 'text/csv', 'application/pdf',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'image/jpeg', 'image/png', 'image/gif'
    }
    
    if uploaded_file.type not in allowed_types:
        return False, f"Unsupported file type: {uploaded_file.type}"
    
    return True, "File is safe"