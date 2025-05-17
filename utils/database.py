import streamlit as st
import os
import sqlite3
import logging
from sqlalchemy import create_engine, text
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create data directory if it doesn't exist
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)

# Set SQLite database path
SQLITE_DB_PATH = 'data/gcpanel.db'

# Define database setup function
def initialize_db():
    """Initialize database connection and create tables if they don't exist"""
    try:
        # Check if we're in demo mode
        if 'demo_mode' in st.session_state and st.session_state.demo_mode:
            logging.info("Running in demo mode - skipping database initialization")
            return True
            
        # Get database connection using SQLAlchemy for better compatibility with Supabase
        engine = get_sqlalchemy_engine()
        if not engine:
            # If database connection fails, enable demo mode
            st.warning("⚠️ Database connection issue detected. Running in demo mode with local storage.")
            st.session_state.demo_mode = True
            return False
            
        # Create tables using SQLAlchemy
        with engine.connect() as conn:
            # Project table (using SQLite syntax)
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    start_date DATE,
                    end_date DATE,
                    status VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            
            # Sections table (using SQLite syntax)
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS sections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    display_name VARCHAR(100) NOT NULL,
                    icon VARCHAR(50),
                    sort_order INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            
            # Modules table (using SQLite syntax) - Create the table first before inserting data
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS modules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    section_id INTEGER REFERENCES sections(id),
                    name VARCHAR(100) NOT NULL,
                    display_name VARCHAR(100) NOT NULL,
                    icon VARCHAR(50),
                    sort_order INTEGER,
                    enabled BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            
            # Check if default sections exist, if not add them
            result = conn.execute(text("SELECT COUNT(*) FROM sections"))
            count = result.scalar()
            
            if count == 0:
                # Define default sections
                default_sections = [
                    ('preconstruction', 'Preconstruction', 'building', 1),
                    ('engineering', 'Engineering', 'clipboard', 2),
                    ('field', 'Field', 'hard-hat', 3),
                    ('safety', 'Safety', 'shield', 4),
                    ('contracts', 'Contracts', 'file-text', 5),
                    ('cost', 'Cost', 'dollar-sign', 6),
                    ('bim', 'BIM', '3d-model', 7),
                    ('closeout', 'Closeout', 'check-circle', 8),
                    ('resources', 'Resources', 'database', 9),
                    ('settings', 'Settings', 'settings', 10),
                    ('reports', 'Reports', 'bar-chart-2', 11)
                ]
                
                # Insert each section
                for section in default_sections:
                    conn.execute(
                        text("INSERT INTO sections (name, display_name, icon, sort_order) VALUES (:name, :display_name, :icon, :sort_order)"),
                        {"name": section[0], "display_name": section[1], "icon": section[2], "sort_order": section[3]}
                    )
                
                # Add default modules for each section
                # First get the section IDs
                sections_result = conn.execute(text("SELECT id, name FROM sections"))
                section_ids = {row[1]: row[0] for row in sections_result.fetchall()}
                
                # Define some default modules
                default_modules = [
                    # Preconstruction modules
                    (section_ids['preconstruction'], 'bid_packages', 'Bid Packages', 'package', 1),
                    (section_ids['preconstruction'], 'qualified_bidders', 'Qualified Bidders', 'users', 2),
                    # Engineering modules
                    (section_ids['engineering'], 'rfi', 'RFIs', 'help-circle', 1),
                    (section_ids['engineering'], 'file_explorer', 'Document Library', 'folder', 2),
                    # Field modules
                    (section_ids['field'], 'daily_reports', 'Daily Reports', 'clipboard', 1),
                    (section_ids['field'], 'photo_log', 'Photo Log', 'camera', 2),
                    # Safety modules
                    (section_ids['safety'], 'observations', 'Safety Observations', 'eye', 1),
                    (section_ids['safety'], 'incidents', 'Incident Reports', 'alert-triangle', 2),
                    # Contracts modules
                    (section_ids['contracts'], 'prime_contract', 'Prime Contract', 'file-text', 1),
                    (section_ids['contracts'], 'subcontracts', 'Subcontracts', 'file-minus', 2),
                    # Cost modules
                    (section_ids['cost'], 'budget', 'Budget', 'dollar-sign', 1),
                    (section_ids['cost'], 'change_orders', 'Change Orders', 'git-branch', 2),
                    # BIM modules
                    (section_ids['bim'], 'model_viewer', 'Model Viewer', '3d-model', 1),
                    (section_ids['bim'], 'clash_detection', 'Clash Detection', 'alert-circle', 2),
                    # Closeout modules
                    (section_ids['closeout'], 'warranties', 'Warranties', 'award', 1),
                    (section_ids['closeout'], 'as_built', 'As-Built Documents', 'file-plus', 2),
                    # Resources modules
                    (section_ids['resources'], 'locations', 'Locations', 'map-pin', 1),
                    (section_ids['resources'], 'equipment', 'Equipment', 'truck', 2),
                    # Settings modules
                    (section_ids['settings'], 'project_info', 'Project Info', 'info', 1),
                    (section_ids['settings'], 'user_management', 'User Management', 'users', 2),
                    # Reports modules
                    (section_ids['reports'], 'statistics', 'Statistics', 'bar-chart-2', 1),
                    (section_ids['reports'], 'exports', 'Export Reports', 'download', 2)
                ]
                
                # Insert default modules
                for module in default_modules:
                    conn.execute(
                        text("""
                            INSERT INTO modules 
                            (section_id, name, display_name, icon, sort_order, enabled) 
                            VALUES (:section_id, :name, :display_name, :icon, :sort_order, 1)
                        """),
                        {
                            "section_id": module[0], 
                            "name": module[1], 
                            "display_name": module[2], 
                            "icon": module[3], 
                            "sort_order": module[4]
                        }
                    )
            
            # Users table (using SQLite syntax)
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            '''))
            
            # Sessions table (using SQLite syntax)
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER REFERENCES users(id),
                    session_token VARCHAR(255) UNIQUE NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            
            # Bid packages table (using SQLite syntax)
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS bid_packages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    issue_date DATE,
                    due_date DATE,
                    project_id INTEGER REFERENCES projects(id),
                    status VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            
            # Qualified bidders table (using SQLite syntax)
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS qualified_bidders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name VARCHAR(100) NOT NULL,
                    contact_name VARCHAR(100) NOT NULL,
                    email VARCHAR(100),
                    phone VARCHAR(50),
                    specialty VARCHAR(100),
                    qualification_status VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            
            # Commit changes
            conn.commit()
        
        logging.info("Database initialized successfully")
        return True
    except Exception as e:
        st.error(f"Error initializing database: {str(e)}")
        logging.error(f"Database initialization error: {str(e)}")
        
        # Enable demo mode on error
        st.warning("⚠️ Database connection issue detected. Running in demo mode with local storage.")
        st.session_state.demo_mode = True
        return False

def get_db_connection():
    """Get a connection to the local SQLite database"""
    # Check if in demo mode
    if 'demo_mode' in st.session_state and st.session_state.demo_mode:
        logging.info("In demo mode - using local storage instead of database connection")
        return None
    
    # Connect to the SQLite database
    try:
        # Get SQLAlchemy engine for SQLite
        engine = get_sqlalchemy_engine()
        if not engine:
            st.error("Could not create SQLite database engine")
            st.session_state.demo_mode = True
            return None
            
        # Use SQLAlchemy to get a connection
        conn = engine.raw_connection()
        
        # Log success 
        st.session_state.db_connected = True
        logging.info("SQLite database connection successful")
        return conn
    except Exception as e:
        logging.error(f"SQLite database connection error: {str(e)}")
        # Enable demo mode on error
        st.session_state.demo_mode = True
        return None

def get_sqlalchemy_engine():
    """Get a SQLAlchemy engine for the local SQLite database"""
    try:
        # Create a SQLite database URL
        sqlite_url = f"sqlite:///{SQLITE_DB_PATH}"
        
        # Log the database connection
        logging.info(f"Connecting to local SQLite database: {SQLITE_DB_PATH}")
        
        # Create SQLAlchemy engine for SQLite
        engine = create_engine(sqlite_url)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            
        # Store connection info in session state
        st.session_state.db_url = sqlite_url
        
        logging.info("SQLite database connection successful")
        return engine
    except Exception as e:
        st.error(f"Error connecting to SQLite database: {str(e)}")
        logging.error(f"SQLite database error: {str(e)}")
        
        # Enable demo mode on error
        st.session_state.demo_mode = True
        return None
