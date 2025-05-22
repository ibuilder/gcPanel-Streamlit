"""
Production Configuration for gcPanel

This module contains production-ready configuration settings for security,
performance, and reliability.
"""
import os
import logging
from datetime import timedelta

class ProductionConfig:
    """Production configuration settings."""
    
    # Security Settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-in-production')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'change-this-in-production')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', '15'))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get('REFRESH_TOKEN_EXPIRE_DAYS', '7'))
    
    # Database Settings
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DATABASE_POOL_SIZE = int(os.environ.get('DATABASE_POOL_SIZE', '10'))
    DATABASE_MAX_OVERFLOW = int(os.environ.get('DATABASE_MAX_OVERFLOW', '20'))
    
    # Application Settings
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    ENVIRONMENT = os.environ.get('ENVIRONMENT', 'production')
    
    # Security Headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'"
    }
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT_PER_MINUTE', '60'))
    LOGIN_ATTEMPTS_LIMIT = int(os.environ.get('LOGIN_ATTEMPTS_LIMIT', '5'))
    LOCKOUT_DURATION_MINUTES = int(os.environ.get('LOCKOUT_DURATION_MINUTES', '15'))
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/gcpanel.log')
    
    # File Upload Limits
    MAX_FILE_SIZE_MB = int(os.environ.get('MAX_FILE_SIZE_MB', '50'))
    ALLOWED_FILE_EXTENSIONS = ['.pdf', '.dwg', '.xlsx', '.docx', '.jpg', '.png', '.ifc']
    
    # Session Settings
    SESSION_TIMEOUT_MINUTES = int(os.environ.get('SESSION_TIMEOUT_MINUTES', '60'))
    
    @classmethod
    def validate_config(cls):
        """Validate critical configuration settings."""
        errors = []
        
        if cls.SECRET_KEY == 'change-this-in-production':
            errors.append("SECRET_KEY must be set to a secure value in production")
            
        if cls.JWT_SECRET_KEY == 'change-this-in-production':
            errors.append("JWT_SECRET_KEY must be set to a secure value in production")
            
        if not cls.DATABASE_URL:
            errors.append("DATABASE_URL must be configured")
            
        if cls.DEBUG and cls.ENVIRONMENT == 'production':
            errors.append("DEBUG mode should be disabled in production")
            
        return errors

def setup_logging():
    """Configure production logging."""
    config = ProductionConfig()
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)