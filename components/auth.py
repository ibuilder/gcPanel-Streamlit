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
    
    # Create login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Log In")
        
        if submit:
            if not username or not password:
                st.error("Please enter both username and password")
                return False
                
            # Authenticate user
            user, token = authenticate_user(username, password)
            
            if user and token:
                # Store authentication in session state
                st.session_state.authenticated = True
                st.session_state.user = user
                st.session_state.token = token
                st.success(f"Welcome back, {user.full_name}!")
                return True
            else:
                st.error("Invalid username or password")
                return False
    
    return False

def register_component():
    """
    Display registration form and handle user creation.
    
    Returns:
        bool: True if registration is successful, False otherwise
    """
    st.subheader("Create a New Account")
    
    # Create registration form
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        submit = st.form_submit_button("Register")
        
        if submit:
            # Validate inputs
            if not username or not email or not password:
                st.error("Username, email, and password are required")
                return False
                
            if password != confirm_password:
                st.error("Passwords do not match")
                return False
                
            # Create user
            user = create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            if user:
                st.success("Registration successful! You can now log in.")
                return True
            else:
                st.error("Username or email already exists")
                return False
    
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