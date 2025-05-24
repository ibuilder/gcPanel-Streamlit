"""
Enterprise Security Manager for gcPanel Highland Tower Development

Implements role-based access control, audit logging, and data encryption
for secure construction management operations.
"""

import jwt
import bcrypt
import secrets
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from cryptography.fernet import Fernet
import streamlit as st
import os
from functools import wraps
from enum import Enum

class UserRole(Enum):
    """User roles for Highland Tower Development project"""
    ADMIN = "admin"
    PROJECT_MANAGER = "project_manager"
    SUPERINTENDENT = "superintendent"
    FOREMAN = "foreman"
    INSPECTOR = "inspector"
    SUBCONTRACTOR = "subcontractor"
    VIEWER = "viewer"

class Permission(Enum):
    """System permissions"""
    READ_ALL = "read_all"
    WRITE_ALL = "write_all"
    READ_RFIS = "read_rfis"
    WRITE_RFIS = "write_rfis"
    READ_DAILY_REPORTS = "read_daily_reports"
    WRITE_DAILY_REPORTS = "write_daily_reports"
    READ_QUALITY = "read_quality"
    WRITE_QUALITY = "write_quality"
    READ_SAFETY = "read_safety"
    WRITE_SAFETY = "write_safety"
    MANAGE_USERS = "manage_users"
    VIEW_AUDIT_LOGS = "view_audit_logs"
    APPROVE_CHANGES = "approve_changes"

class SecurityManager:
    """Enterprise security manager with RBAC and encryption"""
    
    def __init__(self):
        self.jwt_secret = os.environ.get('JWT_SECRET_KEY', self._generate_secret())
        self.encryption_key = self._get_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.setup_logging()
        self.role_permissions = self._initialize_role_permissions()
    
    def setup_logging(self):
        """Setup security operation logging"""
        self.logger = logging.getLogger('SecurityManager')
    
    def _generate_secret(self) -> str:
        """Generate secure JWT secret"""
        return secrets.token_urlsafe(32)
    
    def _get_encryption_key(self) -> bytes:
        """Get or generate encryption key"""
        key = os.environ.get('ENCRYPTION_KEY')
        if not key:
            key = Fernet.generate_key()
            self.logger.warning("Generated new encryption key - store securely!")
        else:
            key = key.encode()
        return key
    
    def _initialize_role_permissions(self) -> Dict[UserRole, List[Permission]]:
        """Initialize role-based permissions for Highland Tower Development"""
        return {
            UserRole.ADMIN: [
                Permission.READ_ALL, Permission.WRITE_ALL, Permission.MANAGE_USERS,
                Permission.VIEW_AUDIT_LOGS, Permission.APPROVE_CHANGES
            ],
            UserRole.PROJECT_MANAGER: [
                Permission.READ_ALL, Permission.WRITE_ALL, Permission.APPROVE_CHANGES,
                Permission.VIEW_AUDIT_LOGS
            ],
            UserRole.SUPERINTENDENT: [
                Permission.READ_ALL, Permission.WRITE_DAILY_REPORTS, Permission.WRITE_QUALITY,
                Permission.WRITE_SAFETY, Permission.READ_RFIS, Permission.WRITE_RFIS
            ],
            UserRole.FOREMAN: [
                Permission.READ_DAILY_REPORTS, Permission.WRITE_DAILY_REPORTS,
                Permission.READ_SAFETY, Permission.WRITE_SAFETY, Permission.READ_RFIS
            ],
            UserRole.INSPECTOR: [
                Permission.READ_QUALITY, Permission.WRITE_QUALITY, Permission.READ_SAFETY,
                Permission.READ_RFIS, Permission.READ_DAILY_REPORTS
            ],
            UserRole.SUBCONTRACTOR: [
                Permission.READ_RFIS, Permission.WRITE_RFIS, Permission.READ_DAILY_REPORTS,
                Permission.READ_QUALITY
            ],
            UserRole.VIEWER: [
                Permission.READ_RFIS, Permission.READ_DAILY_REPORTS, Permission.READ_QUALITY,
                Permission.READ_SAFETY
            ]
        }
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def generate_jwt_token(self, user_id: int, username: str, role: UserRole) -> str:
        """Generate JWT token for user session"""
        payload = {
            'user_id': user_id,
            'username': username,
            'role': role.value,
            'project': 'highland_tower',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=8)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def verify_jwt_token(self, token: str) -> Optional[Dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError:
            self.logger.warning("Invalid token")
            return None
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return encrypted_data.decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        decrypted_data = self.cipher_suite.decrypt(encrypted_data.encode())
        return decrypted_data.decode()
    
    def has_permission(self, user_role: UserRole, permission: Permission) -> bool:
        """Check if user role has specific permission"""
        role_perms = self.role_permissions.get(user_role, [])
        return permission in role_perms or Permission.READ_ALL in role_perms
    
    def log_security_event(self, event_type: str, user_id: int = None, 
                          details: Dict = None, ip_address: str = None):
        """Log security events for audit trail"""
        event_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'details': details or {},
            'ip_address': ip_address,
            'project': 'highland_tower'
        }
        
        # In production, this would write to secure audit log
        self.logger.info(f"Security Event: {event_data}")
    
    def validate_session(self) -> Optional[Dict]:
        """Validate current user session"""
        if 'auth_token' not in st.session_state:
            return None
        
        token_data = self.verify_jwt_token(st.session_state.auth_token)
        if not token_data:
            # Clear invalid session
            if 'auth_token' in st.session_state:
                del st.session_state.auth_token
            return None
        
        return token_data

def require_permission(permission: Permission):
    """Decorator to require specific permission for function access"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            security_manager = get_security_manager()
            session_data = security_manager.validate_session()
            
            if not session_data:
                st.error("Please log in to access this feature")
                st.stop()
            
            user_role = UserRole(session_data['role'])
            
            if not security_manager.has_permission(user_role, permission):
                st.error("You don't have permission to access this feature")
                st.stop()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_role(required_role: UserRole):
    """Decorator to require specific role for function access"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            security_manager = get_security_manager()
            session_data = security_manager.validate_session()
            
            if not session_data:
                st.error("Please log in to access this feature")
                st.stop()
            
            user_role = UserRole(session_data['role'])
            
            if user_role != required_role and user_role != UserRole.ADMIN:
                st.error(f"This feature requires {required_role.value} role")
                st.stop()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@st.cache_resource
def get_security_manager():
    """Get cached security manager instance"""
    return SecurityManager()

class AuditLogger:
    """Comprehensive audit logging for compliance"""
    
    def __init__(self):
        self.security_manager = get_security_manager()
        self.setup_logging()
    
    def setup_logging(self):
        """Setup audit logging"""
        self.logger = logging.getLogger('AuditLogger')
        
        # Create audit log handler
        audit_handler = logging.FileHandler('logs/audit.log')
        audit_formatter = logging.Formatter(
            '%(asctime)s - AUDIT - %(message)s'
        )
        audit_handler.setFormatter(audit_formatter)
        self.logger.addHandler(audit_handler)
        self.logger.setLevel(logging.INFO)
    
    def log_user_action(self, action: str, resource: str = None, 
                       details: Dict = None):
        """Log user actions with full context"""
        session_data = self.security_manager.validate_session()
        
        audit_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': session_data.get('user_id') if session_data else None,
            'username': session_data.get('username') if session_data else 'anonymous',
            'role': session_data.get('role') if session_data else 'unknown',
            'action': action,
            'resource': resource,
            'details': details or {},
            'project': 'highland_tower',
            'session_id': st.session_state.get('session_id', 'unknown')
        }
        
        self.logger.info(f"USER_ACTION: {audit_entry}")
    
    def log_data_access(self, table_name: str, operation: str, 
                       record_count: int = 1):
        """Log data access operations"""
        session_data = self.security_manager.validate_session()
        
        access_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': session_data.get('user_id') if session_data else None,
            'operation': operation,
            'table_name': table_name,
            'record_count': record_count,
            'project': 'highland_tower'
        }
        
        self.logger.info(f"DATA_ACCESS: {access_entry}")
    
    def log_security_violation(self, violation_type: str, details: Dict):
        """Log security violations"""
        session_data = self.security_manager.validate_session()
        
        violation_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': session_data.get('user_id') if session_data else None,
            'violation_type': violation_type,
            'details': details,
            'project': 'highland_tower',
            'severity': 'HIGH'
        }
        
        self.logger.warning(f"SECURITY_VIOLATION: {violation_entry}")

@st.cache_resource  
def get_audit_logger():
    """Get cached audit logger instance"""
    return AuditLogger()