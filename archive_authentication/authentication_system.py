"""
Highland Tower Development - Complete Authentication & Registration System
Production-ready user management with email verification and role-based access
"""

import streamlit as st
import bcrypt
import sqlite3
import smtplib
import secrets
import re
from datetime import datetime, timedelta
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from typing import Dict, List, Optional, Tuple
import os

class UserAuthenticationSystem:
    """Complete user authentication and registration system"""
    
    def __init__(self):
        self.db_path = "highland_users.db"
        self.setup_database()
        self.email_enabled = self.check_email_config()
    
    def setup_database(self):
        """Initialize user database with proper schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                company TEXT,
                phone TEXT,
                is_verified BOOLEAN DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                verification_token TEXT,
                reset_token TEXT,
                reset_token_expires TIMESTAMP
            )
        ''')
        
        # Companies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                domain TEXT,
                subscription_type TEXT DEFAULT 'basic',
                max_users INTEGER DEFAULT 10,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # User sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_token TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create default admin user if none exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        if cursor.fetchone()[0] == 0:
            self.create_default_admin()
        
        conn.commit()
        conn.close()
    
    def create_default_admin(self):
        """Create default admin user for Highland Tower"""
        admin_password = self.hash_password("highland2024")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, first_name, last_name, role, company, is_verified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'highland_admin',
            'admin@highland-construction.com',
            admin_password,
            'Highland',
            'Administrator',
            'admin',
            'Highland Tower Development',
            1
        ))
        
        conn.commit()
        conn.close()
    
    def check_email_config(self) -> bool:
        """Check if email configuration is available"""
        required_vars = ['SMTP_HOST', 'SMTP_PORT', 'SMTP_USER', 'SMTP_PASSWORD']
        return all(os.environ.get(var) for var in required_vars)
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
        
        return True, "Password is strong"
    
    def register_user(self, user_data: Dict) -> Tuple[bool, str]:
        """Register new user with validation"""
        try:
            # Validate input
            if not self.validate_email(user_data['email']):
                return False, "Invalid email format"
            
            password_valid, password_msg = self.validate_password_strength(user_data['password'])
            if not password_valid:
                return False, password_msg
            
            # Check if user already exists
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM users WHERE email = ? OR username = ?", 
                          (user_data['email'], user_data['username']))
            if cursor.fetchone():
                conn.close()
                return False, "User with this email or username already exists"
            
            # Hash password and generate verification token
            password_hash = self.hash_password(user_data['password'])
            verification_token = secrets.token_urlsafe(32)
            
            # Insert user
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, first_name, last_name, 
                                 role, company, phone, verification_token)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_data['username'],
                user_data['email'],
                password_hash,
                user_data['first_name'],
                user_data['last_name'],
                user_data.get('role', 'user'),
                user_data.get('company', ''),
                user_data.get('phone', ''),
                verification_token
            ))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Send verification email if email is configured
            if self.email_enabled:
                self.send_verification_email(user_data['email'], verification_token)
                return True, f"Registration successful! Please check your email to verify your account."
            else:
                # Auto-verify if email not configured
                self.verify_user(verification_token)
                return True, "Registration successful! You can now log in."
            
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[Dict]]:
        """Authenticate user login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, email, password_hash, first_name, last_name, 
                       role, company, is_verified, is_active
                FROM users 
                WHERE (username = ? OR email = ?) AND is_active = 1
            ''', (username, username))
            
            user = cursor.fetchone()
            
            if user and self.verify_password(password, user[3]):
                if not user[8]:  # is_verified
                    conn.close()
                    return False, {"error": "Please verify your email before logging in"}
                
                # Update last login
                cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", 
                              (datetime.now(), user[0]))
                conn.commit()
                
                user_dict = {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'first_name': user[4],
                    'last_name': user[5],
                    'role': user[6],
                    'company': user[7],
                    'is_verified': user[8],
                    'is_active': user[9]
                }
                
                conn.close()
                return True, user_dict
            
            conn.close()
            return False, {"error": "Invalid username/email or password"}
            
        except Exception as e:
            return False, {"error": f"Authentication failed: {str(e)}"}
    
    def send_verification_email(self, email: str, token: str):
        """Send email verification"""
        try:
            smtp_host = os.environ.get('SMTP_HOST')
            smtp_port = int(os.environ.get('SMTP_PORT', 587))
            smtp_user = os.environ.get('SMTP_USER')
            smtp_password = os.environ.get('SMTP_PASSWORD')
            
            msg = MimeMultipart()
            msg['From'] = smtp_user
            msg['To'] = email
            msg['Subject'] = "Highland Tower Development - Email Verification"
            
            verification_url = f"http://localhost:5000/verify?token={token}"
            
            body = f"""
            Welcome to Highland Tower Development!
            
            Please click the following link to verify your email address:
            {verification_url}
            
            If you didn't register for this account, please ignore this email.
            
            Best regards,
            Highland Tower Development Team
            """
            
            msg.attach(MimeText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            server.quit()
            
        except Exception as e:
            st.error(f"Failed to send verification email: {e}")
    
    def verify_user(self, token: str) -> bool:
        """Verify user email with token"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM users WHERE verification_token = ?", (token,))
            user = cursor.fetchone()
            
            if user:
                cursor.execute("""
                    UPDATE users 
                    SET is_verified = 1, verification_token = NULL 
                    WHERE verification_token = ?
                """, (token,))
                conn.commit()
                conn.close()
                return True
            
            conn.close()
            return False
            
        except Exception as e:
            st.error(f"Verification failed: {e}")
            return False
    
    def request_password_reset(self, email: str) -> bool:
        """Request password reset"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            
            if user:
                reset_token = secrets.token_urlsafe(32)
                expires = datetime.now() + timedelta(hours=1)
                
                cursor.execute("""
                    UPDATE users 
                    SET reset_token = ?, reset_token_expires = ?
                    WHERE email = ?
                """, (reset_token, expires, email))
                conn.commit()
                
                if self.email_enabled:
                    self.send_reset_email(email, reset_token)
                
                conn.close()
                return True
            
            conn.close()
            return False
            
        except Exception as e:
            st.error(f"Password reset request failed: {e}")
            return False
    
    def reset_password(self, token: str, new_password: str) -> Tuple[bool, str]:
        """Reset password with token"""
        try:
            password_valid, password_msg = self.validate_password_strength(new_password)
            if not password_valid:
                return False, password_msg
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id FROM users 
                WHERE reset_token = ? AND reset_token_expires > ?
            """, (token, datetime.now()))
            
            user = cursor.fetchone()
            
            if user:
                password_hash = self.hash_password(new_password)
                cursor.execute("""
                    UPDATE users 
                    SET password_hash = ?, reset_token = NULL, reset_token_expires = NULL
                    WHERE reset_token = ?
                """, (password_hash, token))
                conn.commit()
                conn.close()
                return True, "Password reset successful"
            
            conn.close()
            return False, "Invalid or expired reset token"
            
        except Exception as e:
            return False, f"Password reset failed: {str(e)}"
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, username, email, first_name, last_name, role, company, 
                       phone, is_verified, is_active, created_at, last_login
                FROM users WHERE id = ?
            """, (user_id,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'first_name': user[3],
                    'last_name': user[4],
                    'role': user[5],
                    'company': user[6],
                    'phone': user[7],
                    'is_verified': user[8],
                    'is_active': user[9],
                    'created_at': user[10],
                    'last_login': user[11]
                }
            
            return None
            
        except Exception as e:
            st.error(f"Failed to get user: {e}")
            return None

def render_login_page():
    """Render enhanced login page with registration option"""
    auth_system = UserAuthenticationSystem()
    
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h1 style="color: #60a5fa; font-size: 3.5rem; margin-bottom: 1rem;">gcPanel</h1>
        <h2 style="color: #94a3b8; font-size: 1.8rem; margin-bottom: 0.5rem;">Highland Tower Development</h2>
        <p style="color: #64748b; font-size: 1.2rem; margin-bottom: 3rem;">
            Enterprise Construction Management Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login/Register tabs
    tab1, tab2 = st.tabs(["🔐 Login", "👤 Register"])
    
    with tab1:
        render_login_form(auth_system)
    
    with tab2:
        render_registration_form(auth_system)

def render_login_form(auth_system):
    """Render login form"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Sign In")
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username or Email", placeholder="Enter your username or email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_login, col_forgot = st.columns(2)
            
            with col_login:
                submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")
            
            with col_forgot:
                forgot_password = st.form_submit_button("Forgot Password?", use_container_width=True)
            
            if submitted and username and password:
                success, user_data = auth_system.authenticate_user(username, password)
                
                if success:
                    # Set session state
                    st.session_state.authenticated = True
                    st.session_state.user = user_data
                    st.session_state.username = user_data['username']
                    st.session_state.user_role = user_data['role']
                    st.session_state.user_permissions = get_role_permissions(user_data['role'])
                    
                    st.success(f"Welcome back, {user_data['first_name']}!")
                    st.rerun()
                else:
                    st.error(user_data.get('error', 'Login failed'))
            
            if forgot_password:
                st.session_state.show_password_reset = True
                st.rerun()

def render_registration_form(auth_system):
    """Render user registration form"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 👤 Create Account")
        
        with st.form("registration_form", clear_on_submit=True):
            col_name1, col_name2 = st.columns(2)
            
            with col_name1:
                first_name = st.text_input("First Name*", placeholder="John")
            
            with col_name2:
                last_name = st.text_input("Last Name*", placeholder="Smith")
            
            username = st.text_input("Username*", placeholder="Choose a unique username")
            email = st.text_input("Email*", placeholder="john.smith@company.com")
            
            col_pass1, col_pass2 = st.columns(2)
            
            with col_pass1:
                password = st.text_input("Password*", type="password", placeholder="Choose a strong password")
            
            with col_pass2:
                confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Confirm your password")
            
            company = st.text_input("Company", placeholder="Your company name")
            phone = st.text_input("Phone", placeholder="Optional phone number")
            
            role = st.selectbox("Role", ["user", "manager", "superintendent", "admin"], index=0)
            
            terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy*")
            
            submitted = st.form_submit_button("Create Account", use_container_width=True, type="primary")
            
            if submitted:
                if not all([first_name, last_name, username, email, password, confirm_password]):
                    st.error("Please fill in all required fields (marked with *)")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif not terms_accepted:
                    st.error("Please accept the Terms of Service")
                else:
                    user_data = {
                        'first_name': first_name,
                        'last_name': last_name,
                        'username': username,
                        'email': email,
                        'password': password,
                        'company': company,
                        'phone': phone,
                        'role': role
                    }
                    
                    success, message = auth_system.register_user(user_data)
                    
                    if success:
                        st.success(message)
                        st.info("You can now sign in using the Login tab")
                    else:
                        st.error(message)

def get_role_permissions(role: str) -> List[str]:
    """Get permissions for user role"""
    permissions = {
        'admin': ['all'],
        'manager': ['dashboard', 'reports', 'rfis', 'contracts', 'cost_management', 'analytics'],
        'superintendent': ['dashboard', 'daily_reports', 'safety', 'field_operations', 'quality_control'],
        'user': ['dashboard', 'daily_reports', 'safety']
    }
    return permissions.get(role, ['dashboard'])

def check_authentication():
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        render_login_page()
        return False
    
    return True