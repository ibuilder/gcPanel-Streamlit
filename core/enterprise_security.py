"""
Enterprise-Grade Security Framework for gcPanel
Production-ready security, authentication, and data protection
"""

import streamlit as st
import hashlib
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import jwt

class EnterpriseSecurityManager:
    """Enterprise-grade security management for production deployment"""
    
    def __init__(self):
        self.security_config = {
            "session_timeout": 480,  # 8 hours
            "max_login_attempts": 5,
            "password_policy": {
                "min_length": 8,
                "require_uppercase": True,
                "require_lowercase": True,
                "require_numbers": True,
                "require_special": True
            },
            "audit_logging": True,
            "encryption_enabled": True
        }
        self._setup_security_logging()
        self._initialize_security_state()
    
    def _setup_security_logging(self):
        """Setup comprehensive security logging"""
        os.makedirs("logs/security", exist_ok=True)
        
        security_logger = logging.getLogger('gcpanel.security')
        if not security_logger.handlers:
            handler = logging.FileHandler('logs/security/security_audit.log')
            formatter = logging.Formatter(
                '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            security_logger.addHandler(handler)
            security_logger.setLevel(logging.INFO)
    
    def _initialize_security_state(self):
        """Initialize security-related session state"""
        if 'security_initialized' not in st.session_state:
            st.session_state.security_initialized = True
            st.session_state.login_attempts = 0
            st.session_state.last_activity = datetime.now()
            st.session_state.session_id = self._generate_session_id()
    
    def _generate_session_id(self) -> str:
        """Generate secure session ID"""
        import secrets
        return secrets.token_urlsafe(32)
    
    def authenticate_user(self, username: str, password: str) -> Dict:
        """Authenticate user with enterprise security measures"""
        try:
            # Check for account lockout
            if st.session_state.get('login_attempts', 0) >= self.security_config['max_login_attempts']:
                self._log_security_event("ACCOUNT_LOCKED", username, {
                    "reason": "Exceeded maximum login attempts"
                })
                return {
                    "success": False, 
                    "message": "Account temporarily locked due to multiple failed attempts"
                }
            
            # Load user credentials
            users_file = "data/security/users.json"
            if not os.path.exists(users_file):
                self._create_default_users()
            
            with open(users_file, 'r') as f:
                users = json.load(f)
            
            # Validate credentials
            user_data = users.get(username)
            if user_data and self._verify_password(password, user_data['password_hash']):
                # Successful authentication
                st.session_state.authenticated = True
                st.session_state.current_user = username
                st.session_state.user_role = user_data.get('role', 'user')
                st.session_state.login_attempts = 0
                st.session_state.last_activity = datetime.now()
                
                self._log_security_event("LOGIN_SUCCESS", username, {
                    "role": user_data.get('role', 'user'),
                    "session_id": st.session_state.session_id
                })
                
                return {"success": True, "message": "Authentication successful"}
            else:
                # Failed authentication
                st.session_state.login_attempts = st.session_state.get('login_attempts', 0) + 1
                
                self._log_security_event("LOGIN_FAILED", username, {
                    "attempt_number": st.session_state.login_attempts,
                    "reason": "Invalid credentials"
                })
                
                return {
                    "success": False, 
                    "message": f"Invalid credentials. Attempts: {st.session_state.login_attempts}/{self.security_config['max_login_attempts']}"
                }
                
        except Exception as e:
            self._log_security_event("AUTH_ERROR", username, {
                "error": str(e),
                "type": "system_error"
            })
            return {"success": False, "message": "Authentication system error"}
    
    def _create_default_users(self):
        """Create default users for production"""
        os.makedirs("data/security", exist_ok=True)
        
        default_users = {
            "admin": {
                "password_hash": self._hash_password("GcPanel2024!"),
                "role": "admin",
                "full_name": "System Administrator",
                "email": "admin@gcpanel.com",
                "created_date": datetime.now().isoformat(),
                "last_login": None,
                "active": True
            },
            "project_manager": {
                "password_hash": self._hash_password("ProjectMgr2024!"),
                "role": "project_manager", 
                "full_name": "Project Manager",
                "email": "pm@gcpanel.com",
                "created_date": datetime.now().isoformat(),
                "last_login": None,
                "active": True
            },
            "field_supervisor": {
                "password_hash": self._hash_password("FieldSuper2024!"),
                "role": "supervisor",
                "full_name": "Field Supervisor",
                "email": "supervisor@gcpanel.com", 
                "created_date": datetime.now().isoformat(),
                "last_login": None,
                "active": True
            }
        }
        
        with open("data/security/users.json", 'w') as f:
            json.dump(default_users, f, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using secure method"""
        import bcrypt
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def check_session_validity(self) -> bool:
        """Check if current session is valid"""
        if not st.session_state.get('authenticated', False):
            return False
        
        # Check session timeout
        last_activity = st.session_state.get('last_activity')
        if last_activity:
            if isinstance(last_activity, str):
                last_activity = datetime.fromisoformat(last_activity)
            
            if datetime.now() - last_activity > timedelta(minutes=self.security_config['session_timeout']):
                self._log_security_event("SESSION_TIMEOUT", st.session_state.get('current_user', 'unknown'), {
                    "session_id": st.session_state.get('session_id'),
                    "last_activity": last_activity.isoformat()
                })
                self.logout_user()
                return False
        
        # Update last activity
        st.session_state.last_activity = datetime.now()
        return True
    
    def logout_user(self):
        """Securely logout user"""
        if st.session_state.get('authenticated'):
            self._log_security_event("LOGOUT", st.session_state.get('current_user', 'unknown'), {
                "session_id": st.session_state.get('session_id'),
                "session_duration": str(datetime.now() - st.session_state.get('last_activity', datetime.now()))
            })
        
        # Clear authentication state
        for key in ['authenticated', 'current_user', 'user_role', 'session_id']:
            if key in st.session_state:
                del st.session_state[key]
        
        st.session_state.login_attempts = 0
    
    def validate_data_access(self, module: str, action: str, user_role: str = None) -> bool:
        """Validate user access to data based on role"""
        if not user_role:
            user_role = st.session_state.get('user_role', 'guest')
        
        # Role-based access control matrix
        access_matrix = {
            "admin": {
                "all_modules": ["read", "write", "delete", "admin"],
                "restrictions": []
            },
            "project_manager": {
                "allowed_modules": ["dashboard", "contracts", "cost_management", "safety", "field_operations", "documents"],
                "allowed_actions": ["read", "write"],
                "restricted_actions": ["delete", "admin"]
            },
            "supervisor": {
                "allowed_modules": ["dashboard", "field_operations", "safety", "documents"],
                "allowed_actions": ["read", "write"],
                "restricted_actions": ["delete", "admin", "financial"]
            },
            "user": {
                "allowed_modules": ["dashboard"],
                "allowed_actions": ["read"],
                "restricted_actions": ["write", "delete", "admin", "financial"]
            }
        }
        
        role_config = access_matrix.get(user_role, access_matrix["user"])
        
        # Check module access
        if "all_modules" in role_config:
            module_allowed = True
        else:
            module_allowed = module in role_config.get("allowed_modules", [])
        
        # Check action access
        if "all_modules" in role_config:
            action_allowed = action not in role_config.get("restrictions", [])
        else:
            action_allowed = action in role_config.get("allowed_actions", [])
        
        access_granted = module_allowed and action_allowed
        
        if not access_granted:
            self._log_security_event("ACCESS_DENIED", st.session_state.get('current_user', 'unknown'), {
                "module": module,
                "action": action,
                "user_role": user_role,
                "reason": "Insufficient permissions"
            })
        
        return access_granted
    
    def _log_security_event(self, event_type: str, username: str, details: Dict):
        """Log security events for audit trail"""
        try:
            logger = logging.getLogger('gcpanel.security')
            
            event_data = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "username": username,
                "ip_address": "127.0.0.1",  # In production, capture real IP
                "user_agent": "gcPanel",    # In production, capture real user agent
                "session_id": st.session_state.get('session_id', 'unknown'),
                "details": details
            }
            
            logger.info(json.dumps(event_data))
            
            # Also store in structured format for analytics
            events_file = "logs/security/security_events.json"
            if os.path.exists(events_file):
                with open(events_file, 'r') as f:
                    events = json.load(f)
            else:
                events = {"events": []}
            
            events["events"].append(event_data)
            
            # Keep only last 1000 events
            events["events"] = events["events"][-1000:]
            
            with open(events_file, 'w') as f:
                json.dump(events, f, indent=2)
                
        except Exception as e:
            # Fallback logging to prevent security logging failures
            print(f"Security logging failed: {str(e)}")
    
    def get_security_metrics(self) -> Dict:
        """Get security metrics for monitoring"""
        try:
            events_file = "logs/security/security_events.json"
            if os.path.exists(events_file):
                with open(events_file, 'r') as f:
                    events_data = json.load(f)
                
                events = events_data.get("events", [])
                
                # Calculate metrics
                total_events = len(events)
                failed_logins = len([e for e in events if e["event_type"] == "LOGIN_FAILED"])
                successful_logins = len([e for e in events if e["event_type"] == "LOGIN_SUCCESS"])
                access_denied = len([e for e in events if e["event_type"] == "ACCESS_DENIED"])
                
                return {
                    "total_security_events": total_events,
                    "failed_logins_24h": failed_logins,
                    "successful_logins_24h": successful_logins,
                    "access_denied_24h": access_denied,
                    "security_score": max(0, 100 - (failed_logins * 5) - (access_denied * 10))
                }
            
            return {
                "total_security_events": 0,
                "failed_logins_24h": 0,
                "successful_logins_24h": 0,
                "access_denied_24h": 0,
                "security_score": 100
            }
            
        except Exception:
            return {"error": "Unable to calculate security metrics"}

# Global security manager instance
security_manager = EnterpriseSecurityManager()

def get_security_manager():
    """Get security manager instance"""
    return security_manager

def require_authentication(func):
    """Decorator to require authentication for functions"""
    def wrapper(*args, **kwargs):
        if not security_manager.check_session_validity():
            st.error("🔒 Authentication required. Please log in.")
            st.stop()
        return func(*args, **kwargs)
    return wrapper

def require_role(required_role: str):
    """Decorator to require specific role for functions"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            user_role = st.session_state.get('user_role', 'guest')
            
            role_hierarchy = {
                "admin": 4,
                "project_manager": 3,
                "supervisor": 2,
                "user": 1,
                "guest": 0
            }
            
            if role_hierarchy.get(user_role, 0) < role_hierarchy.get(required_role, 0):
                st.error(f"🚫 Access denied. {required_role.title()} role required.")
                st.stop()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator