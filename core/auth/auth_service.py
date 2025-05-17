"""
Authentication service for user management and authentication.

This module provides functions for user authentication, password hashing,
and user management operations.
"""

import logging
import bcrypt
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.models.user import User, Role, UserStatus
from core.database.config import get_db_session

# Set up logging
logger = logging.getLogger(__name__)

# JWT Configuration (should be moved to settings in production)
JWT_SECRET = "your-secret-key-here"  # In production, use a secure environment variable
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60 * 24  # 24 hours

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def create_access_token(user_id: int, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token for user authentication.
    
    Args:
        user_id: User ID to encode in token
        expires_delta: Optional custom expiration time
        
    Returns:
        str: JWT access token
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=JWT_EXPIRATION_MINUTES)
        
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str) -> (User, str):
    """
    Authenticate a user with username and password.
    
    Args:
        username: Username
        password: Plain text password
        
    Returns:
        tuple: (User object if authenticated, access token) or (None, None)
    """
    try:
        with get_db_session() as db:
            user = db.query(User).filter(User.username == username).first()
            
            if not user:
                logger.warning(f"Authentication failed: User {username} not found")
                return None, None
                
            if user.status != UserStatus.ACTIVE:
                logger.warning(f"Authentication failed: User {username} is {user.status.value}")
                return None, None
                
            if not verify_password(password, user.password_hash):
                logger.warning(f"Authentication failed: Invalid password for user {username}")
                return None, None
                
            # Authentication successful, create access token
            access_token = create_access_token(user.id)
            logger.info(f"User {username} authenticated successfully")
            return user, access_token
    except SQLAlchemyError as e:
        logger.error(f"Database error during authentication: {str(e)}")
        return None, None
    except Exception as e:
        logger.error(f"Unexpected error during authentication: {str(e)}")
        return None, None

def get_user_by_token(token: str) -> User:
    """
    Get user from JWT token.
    
    Args:
        token: JWT access token
        
    Returns:
        User: User object if token is valid, None otherwise
    """
    try:
        # Decode the token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = int(payload.get("sub"))
        
        # Get user from database
        with get_db_session() as db:
            user = db.query(User).filter(User.id == user_id).first()
            return user
    except jwt.PyJWTError as e:
        logger.warning(f"Invalid token: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error getting user from token: {str(e)}")
        return None

def create_user(username: str, email: str, password: str, first_name: str = None, 
                last_name: str = None, roles: list = None) -> User:
    """
    Create a new user.
    
    Args:
        username: Username
        email: Email address
        password: Plain text password (will be hashed)
        first_name: Optional first name
        last_name: Optional last name
        roles: Optional list of role names
        
    Returns:
        User: Created user or None if failed
    """
    try:
        with get_db_session() as db:
            # Check if user already exists
            existing_user = db.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                logger.warning(f"User creation failed: Username or email already exists")
                return None
                
            # Create new user
            new_user = User(
                username=username,
                email=email,
                password_hash=hash_password(password),
                first_name=first_name,
                last_name=last_name,
                status=UserStatus.ACTIVE
            )
            
            # Add roles if specified
            if roles:
                role_objects = db.query(Role).filter(Role.name.in_(roles)).all()
                new_user.roles = role_objects
                
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            logger.info(f"User {username} created successfully")
            return new_user
    except SQLAlchemyError as e:
        logger.error(f"Database error during user creation: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during user creation: {str(e)}")
        return None

def initialize_auth():
    """
    Initialize authentication system with default roles and admin user.
    
    This function should be called during application startup.
    """
    try:
        with get_db_session() as db:
            # Create default roles if they don't exist
            default_roles = [
                {"name": "admin", "description": "Administrator with full access"},
                {"name": "project_manager", "description": "Project manager with high level access"},
                {"name": "engineer", "description": "Engineering team member"},
                {"name": "field", "description": "Field team member"},
                {"name": "viewer", "description": "Read-only access"}
            ]
            
            for role_data in default_roles:
                role = db.query(Role).filter(Role.name == role_data["name"]).first()
                if not role:
                    role = Role(**role_data)
                    db.add(role)
            
            # Commit role changes
            db.commit()
            
            # Create admin user if it doesn't exist
            admin = db.query(User).filter(User.username == "admin").first()
            if not admin:
                # Get admin role
                admin_role = db.query(Role).filter(Role.name == "admin").first()
                
                # Create admin user
                admin = User(
                    username="admin",
                    email="admin@example.com",
                    password_hash=hash_password("admin"),  # Change in production!
                    first_name="Admin",
                    last_name="User",
                    status=UserStatus.ACTIVE
                )
                admin.roles = [admin_role]
                db.add(admin)
                db.commit()
                
            logger.info("Authentication system initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing authentication system: {str(e)}")
        raise