"""
Test configuration and fixtures for gcPanel.

This module provides fixtures and configuration for testing
the gcPanel application.
"""

import os
import sys
import pytest
from unittest.mock import MagicMock

# Add parent directory to path to import application modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import application modules
from core.database.config import init_db, create_tables
from core.models.base import BaseModel
from core.models.user import User, Role, UserStatus
from core.auth.auth_service import hash_password, create_access_token

@pytest.fixture(scope="session")
def test_db():
    """Set up test database for the test session."""
    # Set environment to test
    os.environ["TESTING"] = "true"
    
    # Set SQLite in-memory database for testing
    os.environ["DB_PATH"] = ":memory:"
    
    # Initialize test database
    init_db()
    create_tables()
    
    yield
    
    # Cleanup not needed for in-memory database

@pytest.fixture
def db_session():
    """Get a database session for tests."""
    from core.database.config import get_db_session
    
    with get_db_session() as session:
        yield session

@pytest.fixture
def admin_user(db_session):
    """Create an admin user for testing."""
    # Create admin role
    admin_role = db_session.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        admin_role = Role(name="admin", description="Administrator role")
        db_session.add(admin_role)
    
    # Create test admin user
    admin = db_session.query(User).filter(User.username == "test_admin").first()
    if not admin:
        admin = User(
            username="test_admin",
            email="test_admin@example.com",
            password_hash=hash_password("password"),
            first_name="Test",
            last_name="Admin",
            status=UserStatus.ACTIVE
        )
        admin.roles.append(admin_role)
        db_session.add(admin)
        db_session.commit()
    
    # Create a token for the admin user
    token = create_access_token(admin.id)
    
    return {
        "user": admin,
        "token": token
    }

@pytest.fixture
def regular_user(db_session):
    """Create a regular user for testing."""
    # Create user role
    user_role = db_session.query(Role).filter(Role.name == "user").first()
    if not user_role:
        user_role = Role(name="user", description="Regular user role")
        db_session.add(user_role)
    
    # Create test regular user
    user = db_session.query(User).filter(User.username == "test_user").first()
    if not user:
        user = User(
            username="test_user",
            email="test_user@example.com",
            password_hash=hash_password("password"),
            first_name="Test",
            last_name="User",
            status=UserStatus.ACTIVE
        )
        user.roles.append(user_role)
        db_session.add(user)
        db_session.commit()
    
    # Create a token for the regular user
    token = create_access_token(user.id)
    
    return {
        "user": user,
        "token": token
    }

@pytest.fixture
def mock_streamlit():
    """Mock Streamlit module for testing."""
    mock_st = MagicMock()
    
    # Mock st.session_state as a dict
    mock_st.session_state = {}
    
    # Create common Streamlit functions as mocks
    mock_st.markdown = MagicMock()
    mock_st.header = MagicMock()
    mock_st.subheader = MagicMock()
    mock_st.text = MagicMock()
    mock_st.write = MagicMock()
    mock_st.checkbox = MagicMock(return_value=False)
    mock_st.button = MagicMock(return_value=False)
    mock_st.selectbox = MagicMock(return_value=None)
    mock_st.multiselect = MagicMock(return_value=[])
    mock_st.slider = MagicMock(return_value=0)
    mock_st.text_input = MagicMock(return_value="")
    mock_st.text_area = MagicMock(return_value="")
    mock_st.number_input = MagicMock(return_value=0)
    mock_st.date_input = MagicMock()
    
    return mock_st