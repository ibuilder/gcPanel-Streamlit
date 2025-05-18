"""
Authentication service for gcPanel.

This module provides authentication functions including password hashing,
JWT token creation, and user validation.
"""

import os
import jwt
import logging
import bcrypt
from datetime import datetime, timedelta

# Setup logging
logger = logging.getLogger(__name__)

# Constants
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev_secret_key")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

def hash_password(password):
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    # Convert to bytes if string
    if isinstance(password, str):
        password = password.encode('utf-8')
    
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    
    # Return as string
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """
    Verify a password against a hash.
    
    Args:
        password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        bool: True if password matches, False otherwise
    """
    # Convert to bytes if string
    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    
    # Verify password
    try:
        return bcrypt.checkpw(password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification error: {str(e)}")
        return False

def create_access_token(user_id, expires_delta=None):
    """
    Create a JWT access token.
    
    Args:
        user_id: User ID to include in token
        expires_delta: Optional expiration time delta
        
    Returns:
        str: JWT token
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    expire = datetime.utcnow() + expires_delta
    
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access"
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def create_refresh_token(user_id):
    """
    Create a JWT refresh token.
    
    Args:
        user_id: User ID to include in token
        
    Returns:
        str: JWT token
    """
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh"
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    """
    Decode a JWT token.
    
    Args:
        token: JWT token
        
    Returns:
        dict: Token payload or None if invalid
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError as e:
        logger.error(f"Token decoding error: {str(e)}")
        return None

def get_user_from_token_payload(payload):
    """
    Get a user from a token payload.
    
    Args:
        payload: Token payload
        
    Returns:
        User: User object or None if not found
    """
    from core.database.config import get_db_session
    from core.models.user import User
    
    if not payload or "sub" not in payload:
        return None
    
    try:
        user_id = int(payload["sub"])
        
        with get_db_session() as session:
            return session.query(User).filter(User.id == user_id).first()
    
    except Exception as e:
        logger.error(f"Error getting user from token: {str(e)}")
        return None

def get_user_by_token(token):
    """
    Get a user by token.
    
    Args:
        token: JWT token
        
    Returns:
        User: User object or None if not found
    """
    payload = decode_token(token)
    return get_user_from_token_payload(payload)

def authenticate_user(username, password):
    """
    Authenticate a user with username and password.
    
    Args:
        username: Username
        password: Plain text password
        
    Returns:
        tuple: (User, error_message)
    """
    from core.database.config import get_db_session
    from core.models.user import User, UserStatus
    
    try:
        with get_db_session() as session:
            # Find user by username
            user = session.query(User).filter(User.username == username).first()
            
            if not user:
                return None, "Invalid username or password"
            
            # Check if user is active
            if user.status != UserStatus.ACTIVE:
                return None, f"User account is {user.status.value}"
            
            # Verify password
            if not verify_password(password, user.password_hash):
                # Update failed login attempts
                user.failed_login_attempts += 1
                session.commit()
                
                # Check if account should be locked
                if user.failed_login_attempts >= 5:
                    user.status = UserStatus.SUSPENDED
                    session.commit()
                    return None, "Account locked due to too many failed login attempts"
                
                return None, "Invalid username or password"
            
            # Reset failed login attempts
            user.failed_login_attempts = 0
            session.commit()
            
            return user, None
    
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return None, "Authentication error"

def generate_tokens(user_id):
    """
    Generate access and refresh tokens for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        dict: Access and refresh tokens
    """
    return {
        "access_token": create_access_token(user_id),
        "refresh_token": create_refresh_token(user_id),
        "token_type": "bearer"
    }

def refresh_access_token(refresh_token):
    """
    Refresh an access token using a refresh token.
    
    Args:
        refresh_token: Refresh token
        
    Returns:
        dict: New access token or None if invalid
    """
    payload = decode_token(refresh_token)
    
    if not payload:
        return None
    
    # Check token type
    if payload.get("type") != "refresh":
        return None
    
    # Get user
    user = get_user_from_token_payload(payload)
    
    if not user:
        return None
    
    # Generate new access token
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer"
    }