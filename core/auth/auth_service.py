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

# JWT Configuration
import os
# Get JWT secret from environment or use a default for development
JWT_SECRET = os.environ.get("JWT_SECRET", "your-secret-key-here")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60 * 8  # 8 hours - shorter for better security
JWT_REFRESH_EXPIRATION_DAYS = 7  # 7 days for refresh tokens

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

def create_access_token(user_id: int, expires_delta: timedelta = None, token_type: str = "access") -> str:
    """
    Create a JWT token for user authentication.
    
    Args:
        user_id: User ID to encode in token
        expires_delta: Optional custom expiration time
        token_type: Type of token ("access" or "refresh")
        
    Returns:
        str: JWT token
    """
    if expires_delta is None:
        if token_type == "refresh":
            expires_delta = timedelta(days=JWT_REFRESH_EXPIRATION_DAYS)
        else:
            expires_delta = timedelta(minutes=JWT_EXPIRATION_MINUTES)
        
    expire = datetime.utcnow() + expires_delta
    
    # Add more claims for better security
    jti = os.urandom(16).hex()  # Unique token ID
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": jti,
        "type": token_type
    }
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id: int) -> str:
    """
    Create a JWT refresh token for obtaining new access tokens.
    
    Args:
        user_id: User ID to encode in token
        
    Returns:
        str: JWT refresh token
    """
    return create_access_token(user_id, token_type="refresh")

def authenticate_user(username: str, password: str, mfa_code: str = None) -> tuple:
    """
    Authenticate a user with username and password, with optional MFA.
    
    Args:
        username: Username or email
        password: Plain text password
        mfa_code: Optional MFA verification code
        
    Returns:
        tuple: (User, access_token, refresh_token, requires_mfa) or (None, None, None, False)
    """
    try:
        with get_db_session() as db:
            # Check for user by username OR email for better UX
            user = db.query(User).filter(
                (User.username == username) | (User.email == username)
            ).first()
            
            if not user:
                logger.warning(f"Authentication failed: User {username} not found")
                return None, None, None, False
                
            if user.status != UserStatus.ACTIVE:
                logger.warning(f"Authentication failed: User {username} is {user.status.value}")
                return None, None, None, False
                
            # Verify password with constant-time comparison to prevent timing attacks
            if not verify_password(password, user.password_hash):
                # Record failed login attempt
                user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
                
                # Lock account after too many failed attempts (configurable)
                if user.failed_login_attempts >= 5:  # Threshold for account locking
                    user.status = UserStatus.LOCKED
                    user.locked_until = datetime.utcnow() + timedelta(minutes=30)  # Lock for 30 minutes
                    logger.warning(f"User {username} account locked due to too many failed login attempts")
                
                db.commit()
                logger.warning(f"Authentication failed: Invalid password for user {username}")
                return None, None, None, False
                
            # Reset failed login attempts on successful password verification
            if user.failed_login_attempts:
                user.failed_login_attempts = 0
                db.commit()
            
            # Handle MFA if enabled for user
            if getattr(user, 'mfa_enabled', False) and not mfa_code:
                logger.info(f"MFA required for user {username}")
                return user, None, None, True
                
            # Verify MFA code if required
            if getattr(user, 'mfa_enabled', False) and mfa_code:
                if not verify_mfa_code(user, mfa_code):
                    logger.warning(f"Authentication failed: Invalid MFA code for user {username}")
                    return None, None, None, False
            
            # Authentication successful, create tokens
            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)
            
            # Update last login time
            user.last_login = datetime.utcnow()
            db.commit()
            
            logger.info(f"User {username} authenticated successfully")
            return user, access_token, refresh_token, False
    except SQLAlchemyError as e:
        logger.error(f"Database error during authentication: {str(e)}")
        return None, None, None, False
    except Exception as e:
        logger.error(f"Unexpected error during authentication: {str(e)}")
        return None, None, None, False

def verify_mfa_code(user: User, mfa_code: str) -> bool:
    """
    Verify a multi-factor authentication code.
    
    Args:
        user: User object
        mfa_code: MFA verification code
        
    Returns:
        bool: True if code is valid, False otherwise
    """
    # Placeholder for MFA verification logic
    # In production, use a library like pyotp for TOTP implementation
    # or integrate with external MFA providers
    
    # For development, we'll accept any 6-digit code
    if mfa_code.isdigit() and len(mfa_code) == 6:
        return True
    return False

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
        
        # Get user from database with eager loading of roles
        from sqlalchemy.orm import joinedload
        with get_db_session() as db:
            user = db.query(User).options(joinedload(User.roles)).filter(User.id == user_id).first()
            
            if user:
                # Create a detached copy of the user with roles already loaded
                # to prevent DetachedInstanceError when accessing roles outside of the session
                user_copy = User(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    password_hash=user.password_hash,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    status=user.status,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                    is_active=user.is_active
                )
                
                # Manually set roles (already loaded by joinedload)
                user_copy._roles = list(user.roles)
                
                return user_copy
            return None
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
            
            # Track if any roles were added
            roles_added = False
            
            for role_data in default_roles:
                role = db.query(Role).filter(Role.name == role_data["name"]).first()
                if not role:
                    role = Role(**role_data)
                    db.add(role)
                    roles_added = True
            
            # Only commit if roles were added
            if roles_added:
                db.commit()
                logger.info("Default roles created")
            
            # Check if admin user exists by username OR email (to avoid unique constraint errors)
            admin = db.query(User).filter(
                (User.username == "admin") | (User.email == "admin@example.com")
            ).first()
            
            if not admin:
                # Get admin role
                admin_role = db.query(Role).filter(Role.name == "admin").first()
                if not admin_role:
                    logger.error("Admin role not found during initialization")
                    return False
                
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
                logger.info("Admin user created")
            else:
                # Make sure existing admin has the admin role
                admin_role = db.query(Role).filter(Role.name == "admin").first()
                if admin_role and admin_role not in admin.roles:
                    admin.roles.append(admin_role)
                    db.commit()
                    logger.info("Added admin role to existing admin user")
                
            logger.info("Authentication system initialized successfully")
            return True
    except Exception as e:
        logger.error(f"Error initializing authentication system: {str(e)}")
        # Don't crash on initialization error, return False instead
        return False