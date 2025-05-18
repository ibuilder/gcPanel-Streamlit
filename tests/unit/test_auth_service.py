"""
Unit tests for authentication service.

This module tests the core authentication functionality
to ensure secure user authentication.
"""

import pytest
import jwt
from datetime import datetime, timedelta

from core.auth.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_user_by_token
)
from core.models.user import User, UserStatus

def test_password_hashing():
    """Test password hashing and verification."""
    # Test password hashing
    password = "securePassword123"
    hashed = hash_password(password)
    
    # Ensure hash is not the original password
    assert hashed != password
    
    # Verify hashed password
    assert verify_password(password, hashed)
    
    # Verify incorrect password fails
    assert not verify_password("wrongPassword", hashed)

def test_access_token_creation():
    """Test JWT access token creation and validation."""
    # Create token
    user_id = 123
    token = create_access_token(user_id)
    
    # Verify token is a string
    assert isinstance(token, str)
    
    # Decode token
    secret = jwt.decode(token, options={"verify_signature": False})
    
    # Verify payload
    assert secret["sub"] == str(user_id)
    assert "exp" in secret
    assert secret["type"] == "access"

def test_refresh_token_creation():
    """Test JWT refresh token creation and validation."""
    # Create token
    user_id = 123
    token = create_refresh_token(user_id)
    
    # Verify token is a string
    assert isinstance(token, str)
    
    # Decode token
    secret = jwt.decode(token, options={"verify_signature": False})
    
    # Verify payload
    assert secret["sub"] == str(user_id)
    assert "exp" in secret
    assert secret["type"] == "refresh"

def test_token_expiration():
    """Test token expiration time."""
    user_id = 123
    expires_delta = timedelta(minutes=5)
    
    # Create token with custom expiration
    token = create_access_token(user_id, expires_delta=expires_delta)
    
    # Decode token
    secret = jwt.decode(token, options={"verify_signature": False})
    
    # Verify expiration time is approximately correct (within 1 second)
    expected_exp = datetime.utcnow() + expires_delta
    token_exp = datetime.fromtimestamp(secret["exp"])
    
    # Allow 1 second difference due to processing time
    assert abs((token_exp - expected_exp).total_seconds()) < 1

@pytest.mark.usefixtures("test_db")
def test_get_user_by_token(admin_user):
    """Test retrieving a user by token."""
    # Get user from token
    user = get_user_by_token(admin_user["token"])
    
    # Verify user
    assert user is not None
    assert user.username == "test_admin"
    assert user.email == "test_admin@example.com"
    
    # Verify invalid token
    assert get_user_by_token("invalid_token") is None

@pytest.mark.usefixtures("test_db")
def test_user_roles(admin_user, regular_user):
    """Test user role functionality."""
    # Verify admin user has admin role
    admin = admin_user["user"]
    assert admin.has_role("admin")
    
    # Verify regular user does not have admin role
    user = regular_user["user"]
    assert not user.has_role("admin")
    assert user.has_role("user")