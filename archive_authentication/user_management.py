"""
User Management System for Highland Tower Development
Enterprise-grade authentication and role-based access control
"""

import streamlit as st
import bcrypt
import jwt
import pandas as pd
from datetime import datetime, timedelta
import os
from typing import Optional, Dict, List
import uuid

class UserManager:
    """Enterprise user management with secure authentication"""
    
    def __init__(self):
        self.secret_key = os.environ.get('JWT_SECRET_KEY', 'highland-tower-dev-secret')
        self.session_timeout = 8  # hours
        
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_jwt_token(self, user_data: Dict) -> str:
        """Create JWT token for authenticated user"""
        payload = {
            'user_id': user_data['user_id'],
            'username': user_data['username'],
            'role': user_data['role'],
            'exp': datetime.utcnow() + timedelta(hours=self.session_timeout),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_jwt_token(self, token: str) -> Optional[Dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def get_user_database(self) -> List[Dict]:
        """
        Production user database for Highland Tower Development
        In production, this would connect to PostgreSQL
        """
        return [
            {
                'user_id': 'htd_001',
                'username': 'admin',
                'password_hash': self.hash_password('Highland2025!'),
                'role': 'admin',
                'full_name': 'System Administrator',
                'email': 'admin@highlandtower.com',
                'department': 'IT/Management',
                'phone': '+1-555-0100',
                'created_date': '2025-01-01',
                'last_login': None,
                'active': True,
                'permissions': ['read_all', 'write_all', 'manage_users', 'view_audit_logs', 'approve_changes']
            },
            {
                'user_id': 'htd_002',
                'username': 'pmgr_johnson',
                'password_hash': self.hash_password('ProjectMgr2025!'),
                'role': 'manager',
                'full_name': 'Sarah Johnson',
                'email': 'sarah.johnson@highlandtower.com',
                'department': 'Project Management',
                'phone': '+1-555-0101',
                'created_date': '2025-01-15',
                'last_login': '2025-05-25 14:30:00',
                'active': True,
                'permissions': ['read_all', 'write_rfis', 'write_daily_reports', 'write_quality', 'approve_changes']
            },
            {
                'user_id': 'htd_003',
                'username': 'super_chen',
                'password_hash': self.hash_password('Superintendent2025!'),
                'role': 'superintendent',
                'full_name': 'Mike Chen',
                'email': 'mike.chen@highlandtower.com',
                'department': 'Field Operations',
                'phone': '+1-555-0102',
                'created_date': '2025-02-01',
                'last_login': '2025-05-25 16:45:00',
                'active': True,
                'permissions': ['read_daily_reports', 'write_daily_reports', 'read_quality', 'write_quality', 'read_safety', 'write_safety']
            }
        ]
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user with username and password"""
        users = self.get_user_database()
        
        for user in users:
            if user['username'] == username and user['active']:
                if self.verify_password(password, user['password_hash']):
                    # Update last login
                    user['last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    return user
        return None

class SessionManager:
    """Manage user sessions with security controls"""
    
    def __init__(self):
        self.user_manager = UserManager()
    
    def login_user(self, username: str, password: str) -> bool:
        """Login user and create session"""
        user = self.user_manager.authenticate_user(username, password)
        
        if user:
            # Create JWT token
            token = self.user_manager.create_jwt_token(user)
            
            # Store in session state
            st.session_state.authenticated = True
            st.session_state.user_token = token
            st.session_state.user_id = user['user_id']
            st.session_state.username = user['username']
            st.session_state.user_role = user['role']
            st.session_state.full_name = user['full_name']
            st.session_state.user_email = user['email']
            st.session_state.user_department = user['department']
            st.session_state.user_permissions = user['permissions']
            st.session_state.login_time = datetime.now()
            
            return True
        return False
    
    def logout_user(self):
        """Logout user and clear session"""
        # Clear all session data
        keys_to_clear = [
            'authenticated', 'user_token', 'user_id', 'username', 'user_role',
            'full_name', 'user_email', 'user_department', 'user_permissions', 'login_time'
        ]
        
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    def is_session_valid(self) -> bool:
        """Check if current session is valid"""
        if not st.session_state.get('authenticated', False):
            return False
        
        token = st.session_state.get('user_token')
        if not token:
            return False
        
        # Verify JWT token
        payload = self.user_manager.verify_jwt_token(token)
        if not payload:
            self.logout_user()
            return False
        
        return True
    
    def require_permission(self, permission: str) -> bool:
        """Check if user has required permission"""
        if not self.is_session_valid():
            return False
        
        user_permissions = st.session_state.get('user_permissions', [])
        return permission in user_permissions or 'read_all' in user_permissions

# Initialize global instances
user_manager = UserManager()
session_manager = SessionManager()