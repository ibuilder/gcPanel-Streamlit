"""
Authentication components for Streamlit interface.

This module provides UI components for user authentication including
login, registration, and user profile management.
"""

import streamlit as st
from core.auth.auth_service import authenticate_user, create_user, get_user_by_token
from core.auth.user_repository import UserRepository
from core.models.user import UserStatus

def login_component():
    """
    Display login form and handle authentication.
    
    Returns:
        bool: True if login is successful, False otherwise
    """
    st.subheader("Login to gcPanel")
    
    # Create login form with improved styling
    col1, col2 = st.columns([3, 2])
    
    with col1:
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            remember = st.checkbox("Remember me")
            submit = st.form_submit_button("Log In")
            
            if submit:
                if not username or not password:
                    st.error("Please enter both username and password")
                    return False
                    
                # Authenticate user
                try:
                    user, token = authenticate_user(username, password)
                    
                    if user and token:
                        # Store authentication in session state
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        st.session_state.token = token
                        st.session_state.remember_me = remember
                        st.success(f"Welcome back, {user.full_name}!")
                        return True
                    else:
                        st.error("Invalid username or password")
                        return False
                except Exception as e:
                    st.error(f"Login error: {str(e)}")
                    return False
        
        # Reset password link
        st.markdown("<div style='text-align: center; margin-top: 10px;'><a href='#' style='color: #2a9fd6;'>Forgot Password?</a></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Quick Access")
        st.markdown("""
        **Default Admin Login:**
        - Username: admin
        - Password: admin
        
        Once logged in, you'll be able to:
        - Create and manage projects
        - Review RFIs and submittals
        - Monitor project statuses
        - Generate reports
        """)
    
    return False

def register_component():
    """
    Display registration form and handle user creation.
    
    Returns:
        bool: True if registration is successful, False otherwise
    """
    st.subheader("Create a New Account")
    
    # Create registration form with improved styling
    col1, col2 = st.columns(2)
    
    with st.form("register_form", clear_on_submit=False):
        with col1:
            username = st.text_input("Username", help="Choose a unique username")
            email = st.text_input("Email", help="Enter a valid email address")
            first_name = st.text_input("First Name")
        
        with col2:
            last_name = st.text_input("Last Name")
            password = st.text_input("Password", type="password", 
                help="Use at least 8 characters with letters and numbers")
            confirm_password = st.text_input("Confirm Password", type="password")
        
        # Default role selection
        st.markdown("---")
        role = st.selectbox("Account Type", 
            ["Project Manager", "Contractor", "Engineer", "Owner"], 
            index=0)
        
        # Terms and conditions
        terms = st.checkbox("I agree to the Terms and Conditions")
        
        # Submit button
        submit = st.form_submit_button("Create Account")
        
        if submit:
            # Validate inputs
            if not username or not email or not password:
                st.error("Username, email, and password are required")
                return False
                
            if password != confirm_password:
                st.error("Passwords do not match")
                return False
                
            if not terms:
                st.error("You must accept the Terms and Conditions")
                return False
                
            if len(password) < 8:
                st.warning("Password should be at least 8 characters long")
                return False
            
            # Map role selection to role name for database
            role_map = {
                "Project Manager": "project_manager",
                "Contractor": "contractor",
                "Engineer": "engineer",
                "Owner": "owner"
            }
            role_name = role_map.get(role, "user")
                
            # Create user with selected role
            try:
                user = create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    roles=[role_name]
                )
                
                if user:
                    st.success("Registration successful! You can now log in.")
                    # Add a helpful next step message
                    st.info("Please go to the Login tab to sign in with your new account.")
                    return True
                else:
                    st.error("Registration failed. Username or email may already exist.")
                    return False
            except Exception as e:
                st.error(f"An error occurred during registration: {str(e)}")
                return False
    
    # Additional information
    st.markdown("---")
    st.markdown("### Why join gcPanel?")
    
    benefit_col1, benefit_col2 = st.columns(2)
    
    with benefit_col1:
        st.markdown("✅ **Streamlined Project Management**")
        st.markdown("✅ **Real-time Collaboration**")
    
    with benefit_col2:
        st.markdown("✅ **Document Control**")
        st.markdown("✅ **Mobile Access**")
    
    return False

def logout():
    """
    Log out current user and clear session state.
    """
    if "authenticated" in st.session_state:
        st.session_state.authenticated = False
        
    if "user" in st.session_state:
        del st.session_state.user
        
    if "token" in st.session_state:
        del st.session_state.token

def check_authentication():
    """
    Check if user is authenticated with valid token.
    
    Returns:
        bool: True if authenticated, False otherwise
    """
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        return False
        
    if "token" not in st.session_state:
        return False
        
    # Verify token is valid
    user = get_user_by_token(st.session_state.token)
    
    if not user or user.status != UserStatus.ACTIVE:
        logout()
        return False
        
    # Update session state with fresh user data
    st.session_state.user = user
    return True

def user_profile_component():
    """
    Display user profile information.
    
    This component shows information about the currently logged-in user
    and provides controls to update profile settings.
    """
    if not check_authentication():
        st.warning("Please log in to view your profile")
        return
    
    user = st.session_state.user
    
    st.subheader("User Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text(f"Username: {user.username}")
        st.text(f"Email: {user.email}")
        st.text(f"Full Name: {user.full_name}")
        st.text(f"Status: {user.status.value}")
        
        roles = ", ".join([role.name for role in user.roles]) if user.roles else "None"
        st.text(f"Roles: {roles}")
    
    with col2:
        st.subheader("Update Password")
        
        with st.form("password_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            submit = st.form_submit_button("Update Password")
            
            if submit:
                # Validate inputs
                if not current_password or not new_password or not confirm_password:
                    st.error("All fields are required")
                    return
                    
                if new_password != confirm_password:
                    st.error("New passwords do not match")
                    return
                
                # Verify current password
                if not authenticate_user(user.username, current_password)[0]:
                    st.error("Current password is incorrect")
                    return
                    
                # Update password
                user_repo = UserRepository()
                from core.auth.auth_service import hash_password
                if user_repo.change_password(user.id, hash_password(new_password)):
                    st.success("Password updated successfully")
                else:
                    st.error("Failed to update password")