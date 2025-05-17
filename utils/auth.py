import streamlit as st
import bcrypt
import uuid
import logging
from datetime import datetime, timedelta
from utils.database import get_db_connection, get_sqlalchemy_engine
from sqlalchemy import text

# Role permissions
ROLE_PERMISSIONS = {
    "administrator": ["create", "read", "update", "delete"],
    "editor": ["create", "read", "update"],
    "contributor": ["create", "read"],
    "viewer": ["read"]
}

def initialize_auth():
    """Initialize authentication tables in the database"""
    try:
        # Use SQLAlchemy for better compatibility with Supabase
        engine = get_sqlalchemy_engine()
        if not engine:
            st.error("Could not connect to database. Please check your connection settings.")
            logging.error("Failed to get database engine for auth initialization")
            return
        
        # Use SQLAlchemy to create tables and manage data
        with engine.connect() as conn:
            # Create users table if it doesn't exist
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            '''))
            
            # Create sessions table if it doesn't exist
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    session_token VARCHAR(255) UNIQUE NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            
            # Check if admin user exists, create if not
            result = conn.execute(text("SELECT COUNT(*) FROM users WHERE username = 'admin'"))
            admin_exists = result.scalar()
            
            if not admin_exists:
                # Create default admin user if none exists
                password = "admin123"  # In production, this should be a secure, random password
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                conn.execute(
                    text("INSERT INTO users (username, email, password_hash, role) VALUES (:username, :email, :password_hash, :role)"),
                    {"username": "admin", "email": "admin@example.com", "password_hash": password_hash, "role": "administrator"}
                )
            
            # Commit changes
            conn.commit()
            
        logging.info("Authentication initialized successfully")
        
    except Exception as e:
        st.error(f"Error initializing authentication: {str(e)}")
        logging.error(f"Authentication initialization error: {str(e)}")

def check_authentication():
    """Check if user is authenticated, if not show login form"""
    if st.session_state.authenticated:
        return True
    
    # Check for demo mode
    if 'demo_mode' in st.session_state and st.session_state.demo_mode:
        st.title("gcPanel Login (Demo Mode)")
        
        # Demo mode message
        st.info("⚠️ Running in demo mode with local storage. Your data will not be saved to a database.")
        
        # Create login/register tabs
        tab1, tab2 = st.tabs(["Login", "Demo Login"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit_button = st.form_submit_button("Login")
                
                if submit_button:
                    # In demo mode, accept any login
                    if username and password:
                        # Set session state for demo login
                        st.session_state.authenticated = True
                        st.session_state.user_id = 1
                        st.session_state.username = username
                        st.session_state.user_role = "administrator"
                        st.session_state.session_token = "demo-token"
                        
                        st.success("Demo login successful!")
                        st.rerun()
                    else:
                        st.error("Please enter username and password")
        
        with tab2:
            with st.form("demo_login_form"):
                st.write("Use quick login with demo credentials:")
                demo_button = st.form_submit_button("Login as Admin")
                
                if demo_button:
                    # Set session state for demo login
                    st.session_state.authenticated = True
                    st.session_state.user_id = 1
                    st.session_state.username = "admin"
                    st.session_state.user_role = "administrator"
                    st.session_state.session_token = "demo-token"
                    
                    st.success("Demo login successful!")
                    st.rerun()
    else:
        # Regular login process with database
        st.title("gcPanel Login")
        
        # Create login/register tabs
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit_button = st.form_submit_button("Login")
                
                if submit_button:
                    if authenticate_user(username, password):
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
        
        with tab2:
            with st.form("register_form"):
                new_username = st.text_input("Username")
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                
                # In a real app, you'd check with an admin for role assignment
                # For simplicity, we're defaulting new users to 'viewer'
                register_button = st.form_submit_button("Register")
                
                if register_button:
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif register_user(new_username, new_email, new_password, "viewer"):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Registration failed. Username or email may already be in use.")
    
    return False

def authenticate_user(username, password):
    """Authenticate a user with username and password"""
    try:
        # Get SQLAlchemy engine for database connection
        engine = get_sqlalchemy_engine()
        if not engine:
            st.error("Could not connect to database. Please check your connection settings.")
            logging.error("Failed to get database engine for user authentication")
            return False
        
        # Use SQLAlchemy to authenticate user
        with engine.connect() as conn:
            # Get user from database
            result = conn.execute(
                text("SELECT id, username, password_hash, role FROM users WHERE username = :username"),
                {"username": username}
            )
            
            user = result.fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
                user_id, username, _, role = user
                
                # Create a new session
                session_token = str(uuid.uuid4())
                expires_at = datetime.now() + timedelta(days=1)
                
                # Store session in database
                conn.execute(
                    text("INSERT INTO sessions (user_id, session_token, expires_at) VALUES (:user_id, :session_token, :expires_at)"),
                    {"user_id": user_id, "session_token": session_token, "expires_at": expires_at}
                )
                
                # Update last login
                conn.execute(
                    text("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = :user_id"),
                    {"user_id": user_id}
                )
                
                # Commit changes
                conn.commit()
                
                # Set session state
                st.session_state.authenticated = True
                st.session_state.user_id = user_id
                st.session_state.username = username
                st.session_state.user_role = role
                st.session_state.session_token = session_token
                
                logging.info(f"User {username} authenticated successfully")
                return True
            else:
                logging.warning(f"Failed authentication attempt for username: {username}")
                return False
                
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        logging.error(f"Authentication error: {str(e)}")
        return False

def register_user(username, email, password, role):
    """Register a new user"""
    try:
        # Get SQLAlchemy engine for database connection
        engine = get_sqlalchemy_engine()
        if not engine:
            st.error("Could not connect to database. Please check your connection settings.")
            logging.error("Failed to get database engine for user registration")
            return False
        
        # Use SQLAlchemy to register user
        with engine.connect() as conn:
            # Check if username or email already exists
            result = conn.execute(
                text("SELECT COUNT(*) FROM users WHERE username = :username OR email = :email"),
                {"username": username, "email": email}
            )
            
            count = result.scalar()
            if count and count > 0:
                logging.warning(f"Registration failed: Username or email already exists - {username}, {email}")
                return False
            
            # Hash the password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insert new user
            conn.execute(
                text("INSERT INTO users (username, email, password_hash, role) VALUES (:username, :email, :password_hash, :role)"),
                {"username": username, "email": email, "password_hash": password_hash, "role": role}
            )
            
            # Commit changes
            conn.commit()
            
            logging.info(f"User registered successfully: {username}, role: {role}")
            return True
            
    except Exception as e:
        st.error(f"Registration error: {str(e)}")
        logging.error(f"Registration error: {str(e)}")
        return False

def logout_user():
    """Log out the current user"""
    if 'session_token' in st.session_state:
        try:
            # Get SQLAlchemy engine for database connection
            engine = get_sqlalchemy_engine()
            if engine:
                # Use SQLAlchemy to remove session
                with engine.connect() as conn:
                    # Remove session from database
                    conn.execute(
                        text("DELETE FROM sessions WHERE session_token = :session_token"),
                        {"session_token": st.session_state.session_token}
                    )
                    
                    # Commit changes
                    conn.commit()
                    
                    logging.info(f"User {st.session_state.get('username', 'unknown')} logged out successfully")
            else:
                logging.warning("Could not connect to database during logout")
                
        except Exception as e:
            st.error(f"Logout error: {str(e)}")
            logging.error(f"Logout error: {str(e)}")
    
    # Clear session state
    for key in ['authenticated', 'user_id', 'username', 'user_role', 'session_token']:
        if key in st.session_state:
            del st.session_state[key]
    
    st.rerun()

def check_permission(action):
    """Check if current user has permission to perform action"""
    if not st.session_state.authenticated:
        return False
    
    role = st.session_state.user_role
    if role not in ROLE_PERMISSIONS:
        return False
    
    return action in ROLE_PERMISSIONS[role]
