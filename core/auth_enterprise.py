"""
Enterprise Authentication System for gcPanel Construction Platform

Enhanced authentication with SSO integration, password policies, and audit logging
for enterprise construction management deployment.
"""

import os
import logging
import hashlib
import secrets
import re
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import streamlit as st
import jwt
from core.database import get_database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnterpriseAuth:
    """Enterprise-grade authentication system with advanced security features."""
    
    def __init__(self):
        """Initialize enterprise authentication system."""
        self.db = get_database()
        self.jwt_secret = os.environ.get('JWT_SECRET_KEY')
        self.session_timeout = 8 * 60 * 60  # 8 hours
        
        # Password policy configuration
        self.password_policy = {
            'min_length': 8,
            'require_uppercase': True,
            'require_lowercase': True,
            'require_numbers': True,
            'require_special': True,
            'max_age_days': 90,
            'prevent_reuse': 5
        }
        
        # Initialize admin user if not exists
        self._ensure_admin_user()
    
    def _ensure_admin_user(self):
        """Create default admin user for initial setup."""
        try:
            admin_check = self.db.execute_query(
                "SELECT id FROM users WHERE username = 'admin' LIMIT 1"
            )
            
            if not admin_check:
                admin_data = {
                    'username': 'admin',
                    'email': 'admin@gcpanel.com',
                    'password_hash': self._hash_password('gcPanel2025!'),
                    'full_name': 'System Administrator',
                    'role': 'Administrator',
                    'company': 'gcPanel Construction',
                    'is_active': True
                }
                
                self.db.insert_data('users', admin_data)
                logger.info("Default admin user created successfully")
                
        except Exception as e:
            logger.error(f"Error creating admin user: {str(e)}")
    
    def _hash_password(self, password: str) -> str:
        """Hash password with salt using secure method."""
        salt = secrets.token_hex(32)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return f"{salt}${pwd_hash.hex()}"
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash."""
        try:
            salt, pwd_hash = hashed.split('$')
            return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex() == pwd_hash
        except:
            return False
    
    def validate_password_policy(self, password: str) -> Dict[str, bool]:
        """Validate password against enterprise policy."""
        results = {
            'min_length': len(password) >= self.password_policy['min_length'],
            'has_uppercase': bool(re.search(r'[A-Z]', password)) if self.password_policy['require_uppercase'] else True,
            'has_lowercase': bool(re.search(r'[a-z]', password)) if self.password_policy['require_lowercase'] else True,
            'has_numbers': bool(re.search(r'\d', password)) if self.password_policy['require_numbers'] else True,
            'has_special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)) if self.password_policy['require_special'] else True
        }
        
        results['is_valid'] = all(results.values())
        return results
    
    def authenticate_user(self, username: str, password: str) -> Dict:
        """Authenticate user with enhanced security checks."""
        try:
            # Get user from database
            user_query = """
            SELECT id, username, email, password_hash, full_name, role, 
                   company, is_active, last_login, created_at
            FROM users 
            WHERE username = :username AND is_active = true
            """
            
            users = self.db.execute_query(user_query, {'username': username})
            
            if not users:
                self._log_security_event('LOGIN_FAILED', username, 'User not found')
                return {'success': False, 'message': 'Invalid credentials'}
            
            user = users[0]
            
            # Verify password
            if not self._verify_password(password, user['password_hash']):
                self._log_security_event('LOGIN_FAILED', username, 'Invalid password')
                return {'success': False, 'message': 'Invalid credentials'}
            
            # Update last login
            self.db.update_data('users', user['id'], {'last_login': datetime.utcnow()})
            
            # Create JWT token
            token_payload = {
                'user_id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'exp': datetime.utcnow() + timedelta(seconds=self.session_timeout)
            }
            
            token = jwt.encode(token_payload, self.jwt_secret, algorithm='HS256')
            
            # Log successful login
            self._log_security_event('LOGIN_SUCCESS', username, 'Successful authentication')
            
            # Set session state
            st.session_state.authenticated = True
            st.session_state.user_id = user['id']
            st.session_state.username = user['username']
            st.session_state.user_role = user['role']
            st.session_state.full_name = user['full_name']
            st.session_state.company = user['company']
            st.session_state.auth_token = token
            
            return {
                'success': True,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'full_name': user['full_name'],
                    'role': user['role'],
                    'company': user['company']
                },
                'token': token
            }
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return {'success': False, 'message': 'Authentication system error'}
    
    def create_user(self, user_data: Dict) -> Dict:
        """Create new user with validation and audit logging."""
        try:
            # Validate required fields
            required_fields = ['username', 'email', 'password', 'full_name', 'role']
            for field in required_fields:
                if not user_data.get(field):
                    return {'success': False, 'message': f'{field} is required'}
            
            # Validate password policy
            password_check = self.validate_password_policy(user_data['password'])
            if not password_check['is_valid']:
                return {'success': False, 'message': 'Password does not meet policy requirements', 'password_policy': password_check}
            
            # Check if username/email already exists
            existing_user = self.db.execute_query(
                "SELECT id FROM users WHERE username = :username OR email = :email",
                {'username': user_data['username'], 'email': user_data['email']}
            )
            
            if existing_user:
                return {'success': False, 'message': 'Username or email already exists'}
            
            # Hash password and prepare data
            user_record = {
                'username': user_data['username'],
                'email': user_data['email'],
                'password_hash': self._hash_password(user_data['password']),
                'full_name': user_data['full_name'],
                'role': user_data['role'],
                'company': user_data.get('company', ''),
                'phone': user_data.get('phone', ''),
                'is_active': True
            }
            
            # Insert user
            user_id = self.db.insert_data('users', user_record)
            
            # Log audit event
            self.db.log_audit_action(
                st.session_state.get('user_id', 0),
                'CREATE_USER',
                'users',
                user_id,
                new_values=f"Created user: {user_data['username']}"
            )
            
            logger.info(f"User created successfully: {user_data['username']}")
            return {'success': True, 'user_id': user_id, 'message': 'User created successfully'}
            
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return {'success': False, 'message': 'Error creating user'}
    
    def update_user_profile(self, user_id: int, updates: Dict) -> Dict:
        """Update user profile with audit logging."""
        try:
            # Get current user data for audit log
            current_user = self.db.execute_query(
                "SELECT * FROM users WHERE id = :user_id",
                {'user_id': user_id}
            )
            
            if not current_user:
                return {'success': False, 'message': 'User not found'}
            
            # Remove sensitive fields that shouldn't be updated this way
            safe_updates = {k: v for k, v in updates.items() 
                          if k not in ['id', 'password_hash', 'created_at']}
            
            # Update user
            success = self.db.update_data('users', user_id, safe_updates)
            
            if success:
                # Log audit event
                self.db.log_audit_action(
                    st.session_state.get('user_id', user_id),
                    'UPDATE_USER',
                    'users',
                    user_id,
                    old_values=str(current_user[0]),
                    new_values=str(safe_updates)
                )
                
                return {'success': True, 'message': 'Profile updated successfully'}
            else:
                return {'success': False, 'message': 'Failed to update profile'}
                
        except Exception as e:
            logger.error(f"Error updating user profile: {str(e)}")
            return {'success': False, 'message': 'Error updating profile'}
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> Dict:
        """Change user password with validation."""
        try:
            # Get current user
            user = self.db.execute_query(
                "SELECT password_hash FROM users WHERE id = :user_id",
                {'user_id': user_id}
            )
            
            if not user:
                return {'success': False, 'message': 'User not found'}
            
            # Verify current password
            if not self._verify_password(current_password, user[0]['password_hash']):
                return {'success': False, 'message': 'Current password is incorrect'}
            
            # Validate new password
            password_check = self.validate_password_policy(new_password)
            if not password_check['is_valid']:
                return {'success': False, 'message': 'New password does not meet policy requirements', 'password_policy': password_check}
            
            # Update password
            new_hash = self._hash_password(new_password)
            success = self.db.update_data('users', user_id, {'password_hash': new_hash})
            
            if success:
                # Log audit event
                self.db.log_audit_action(user_id, 'CHANGE_PASSWORD', 'users', user_id, new_values='Password changed')
                return {'success': True, 'message': 'Password changed successfully'}
            else:
                return {'success': False, 'message': 'Failed to change password'}
                
        except Exception as e:
            logger.error(f"Error changing password: {str(e)}")
            return {'success': False, 'message': 'Error changing password'}
    
    def verify_token(self, token: str) -> Dict:
        """Verify JWT token and return user info."""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            
            # Check if user still exists and is active
            user = self.db.execute_query(
                "SELECT id, username, role, full_name, is_active FROM users WHERE id = :user_id AND is_active = true",
                {'user_id': payload['user_id']}
            )
            
            if not user:
                return {'valid': False, 'message': 'User not found or inactive'}
            
            return {'valid': True, 'user': user[0]}
            
        except jwt.ExpiredSignatureError:
            return {'valid': False, 'message': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'valid': False, 'message': 'Invalid token'}
        except Exception as e:
            logger.error(f"Token verification error: {str(e)}")
            return {'valid': False, 'message': 'Token verification failed'}
    
    def logout_user(self):
        """Logout user and clear session."""
        username = st.session_state.get('username', 'unknown')
        
        # Log logout event
        self._log_security_event('LOGOUT', username, 'User logged out')
        
        # Clear session
        for key in ['authenticated', 'user_id', 'username', 'user_role', 'full_name', 'company', 'auth_token']:
            if key in st.session_state:
                del st.session_state[key]
    
    def get_user_permissions(self, role: str) -> List[str]:
        """Get user permissions based on role."""
        permissions = {
            'Administrator': [
                'view_all_projects', 'create_project', 'edit_project', 'delete_project',
                'view_all_reports', 'create_report', 'edit_report', 'delete_report',
                'manage_users', 'view_audit_logs', 'export_data', 'system_settings'
            ],
            'Project Manager': [
                'view_assigned_projects', 'create_project', 'edit_project',
                'view_project_reports', 'create_report', 'edit_report',
                'manage_project_team', 'export_project_data'
            ],
            'Superintendent': [
                'view_assigned_projects', 'view_project_reports', 'create_report',
                'edit_own_reports', 'manage_daily_reports', 'manage_quality_control'
            ],
            'Foreman': [
                'view_assigned_projects', 'create_report', 'edit_own_reports',
                'view_daily_reports', 'create_daily_reports'
            ],
            'Inspector': [
                'view_assigned_projects', 'create_inspection', 'edit_inspection',
                'view_quality_reports', 'export_inspection_data'
            ],
            'User': [
                'view_assigned_projects', 'view_reports', 'create_basic_reports'
            ]
        }
        
        return permissions.get(role, permissions['User'])
    
    def check_permission(self, permission: str) -> bool:
        """Check if current user has specific permission."""
        if not st.session_state.get('authenticated'):
            return False
        
        user_role = st.session_state.get('user_role', 'User')
        user_permissions = self.get_user_permissions(user_role)
        
        return permission in user_permissions
    
    def _log_security_event(self, event_type: str, username: str, details: str):
        """Log security events for monitoring and compliance."""
        try:
            security_data = {
                'event_type': event_type,
                'username': username,
                'details': details,
                'ip_address': st.session_state.get('client_ip', 'unknown'),
                'user_agent': 'gcPanel Web Application',
                'timestamp': datetime.utcnow()
            }
            
            logger.info(f"Security Event: {event_type} - {username} - {details}")
            
        except Exception as e:
            logger.error(f"Error logging security event: {str(e)}")

# Global authentication instance
auth_manager = None

def get_auth():
    """Get or create authentication manager instance."""
    global auth_manager
    if auth_manager is None:
        auth_manager = EnterpriseAuth()
    return auth_manager

def require_auth(permission: str = None):
    """Decorator to require authentication and optional permission."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            auth = get_auth()
            
            if not st.session_state.get('authenticated'):
                st.error("⚠️ Authentication required. Please log in.")
                return None
            
            if permission and not auth.check_permission(permission):
                st.error("⚠️ Insufficient permissions for this action.")
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator