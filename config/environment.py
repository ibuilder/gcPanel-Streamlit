"""
Environment Configuration for gcPanel Production Deployment
Handles environment variables and production settings
"""

import os
from typing import Dict, Any
import streamlit as st

class EnvironmentConfig:
    """Environment configuration manager"""
    
    def __init__(self):
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self.database_url = os.getenv('DATABASE_URL')
        self.secret_key = os.getenv('SECRET_KEY', 'highland-tower-dev-key')
        
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration"""
        return {
            'url': self.database_url,
            'pool_size': int(os.getenv('DB_POOL_SIZE', '10')),
            'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', '5')),
            'pool_timeout': int(os.getenv('DB_POOL_TIMEOUT', '30'))
        }
    
    def get_file_upload_config(self) -> Dict[str, Any]:
        """Get file upload configuration"""
        return {
            'max_file_size': int(os.getenv('MAX_FILE_SIZE', '52428800')),  # 50MB
            'upload_directory': os.getenv('UPLOAD_DIR', 'uploads'),
            'allowed_extensions': {
                'documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
                'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
                'cad': ['.dwg', '.dxf', '.ifc', '.rvt'],
                'archive': ['.zip', '.rar', '.7z', '.tar', '.gz']
            }
        }
    
    def get_security_config(self) -> Dict[str, Any]:
        """Get security configuration"""
        return {
            'session_timeout': int(os.getenv('SESSION_TIMEOUT', '3600')),  # 1 hour
            'password_hash_rounds': int(os.getenv('PASSWORD_HASH_ROUNDS', '12')),
            'enable_2fa': os.getenv('ENABLE_2FA', 'false').lower() == 'true',
            'max_login_attempts': int(os.getenv('MAX_LOGIN_ATTEMPTS', '5'))
        }
    
    def get_integration_config(self) -> Dict[str, Any]:
        """Get external integration configuration"""
        return {
            'procore': {
                'client_id': os.getenv('PROCORE_CLIENT_ID'),
                'client_secret': os.getenv('PROCORE_CLIENT_SECRET'),
                'company_id': os.getenv('PROCORE_COMPANY_ID'),
                'api_base_url': os.getenv('PROCORE_API_URL', 'https://api.procore.com')
            },
            'autodesk': {
                'client_id': os.getenv('AUTODESK_CLIENT_ID'),
                'client_secret': os.getenv('AUTODESK_CLIENT_SECRET'),
                'api_base_url': os.getenv('AUTODESK_API_URL', 'https://developer.api.autodesk.com')
            },
            'quickbooks': {
                'client_id': os.getenv('QUICKBOOKS_CLIENT_ID'),
                'client_secret': os.getenv('QUICKBOOKS_CLIENT_SECRET'),
                'sandbox': os.getenv('QUICKBOOKS_SANDBOX', 'true').lower() == 'true'
            }
        }
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment.lower() == 'production'
    
    def validate_configuration(self) -> Dict[str, bool]:
        """Validate environment configuration"""
        validation = {
            'database': bool(self.database_url),
            'secret_key': bool(self.secret_key),
            'environment': bool(self.environment)
        }
        
        # Check integration credentials
        integration_config = self.get_integration_config()
        for service, config in integration_config.items():
            validation[f'{service}_configured'] = all(
                bool(config.get(key)) for key in ['client_id', 'client_secret'] 
                if key in config
            )
        
        return validation

# Global configuration instance
@st.cache_resource
def get_config():
    """Get cached configuration instance"""
    return EnvironmentConfig()

def display_configuration_status():
    """Display configuration status in admin panel"""
    config = get_config()
    validation = config.validate_configuration()
    
    st.subheader("System Configuration Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Core Configuration**")
        for key, status in validation.items():
            if not key.endswith('_configured'):
                icon = "✅" if status else "❌"
                st.write(f"{icon} {key.replace('_', ' ').title()}")
    
    with col2:
        st.markdown("**External Integrations**")
        for key, status in validation.items():
            if key.endswith('_configured'):
                service_name = key.replace('_configured', '').title()
                icon = "✅" if status else "❌"
                st.write(f"{icon} {service_name}")
    
    # Environment details
    with st.expander("Environment Details"):
        st.write(f"**Environment:** {config.environment}")
        st.write(f"**Production Mode:** {config.is_production()}")
        
        if config.database_url:
            st.write(f"**Database:** Connected")
        else:
            st.warning("Database URL not configured")
    
    return validation