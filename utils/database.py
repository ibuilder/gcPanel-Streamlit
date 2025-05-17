import streamlit as st
import os
import psycopg2
from sqlalchemy import create_engine, text
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define database setup function
def initialize_db():
    """Initialize database connection and create tables if they don't exist"""
    try:
        # Get database connection using SQLAlchemy for better compatibility with Supabase
        engine = get_sqlalchemy_engine()
        if not engine:
            st.error("Could not connect to database. Please check your connection settings.")
            return
            
        # Create tables using SQLAlchemy
        with engine.connect() as conn:
            # Project table
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS projects (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    start_date DATE,
                    end_date DATE,
                    status VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            
            # Sections table
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS sections (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    display_name VARCHAR(100) NOT NULL,
                    icon VARCHAR(50),
                    sort_order INTEGER,
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
            
            # Modules table
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS modules (
                    id SERIAL PRIMARY KEY,
                    section_id INTEGER REFERENCES sections(id),
                    name VARCHAR(100) NOT NULL,
                    display_name VARCHAR(100) NOT NULL,
                    icon VARCHAR(50),
                    sort_order INTEGER,
                    enabled BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            
            # Commit changes
            conn.commit()
        
        st.success("Database initialized successfully")
    except Exception as e:
        st.error(f"Error initializing database: {str(e)}")

def get_db_connection():
    """Get a connection to the database"""
    # Load database URL from environment or session state
    db_url = os.environ.get('DATABASE_URL')
    
    # First try environment variable
    if db_url:
        st.session_state.db_url = db_url
        # Log the URL for debugging (masked password)
        try:
            parts = db_url.split('@')
            if len(parts) > 1:
                masked_url = parts[0].split(':')[0] + ':****@' + parts[1]
                logging.info(f"Using database URL: {masked_url}")
        except Exception:
            logging.info("Using database URL from environment (masked)")
    # Then try session state
    else:
        db_url = st.session_state.get('db_url')
    
    if not db_url:
        # If no connection string is available, show a form to collect it
        st.warning("Database connection not configured")
        with st.form("db_connection_form"):
            new_db_url = st.text_input("Enter Supabase Database Connection URL:")
            submitted = st.form_submit_button("Connect")
            
            if submitted and new_db_url:
                st.session_state.db_url = new_db_url
                st.success("Database connection established")
                st.rerun()
        return None
    
    # Connect to the database
    try:
        # Create SQLAlchemy engine and use that for better compatibility
        engine = get_sqlalchemy_engine()
        if not engine:
            st.error("Could not create database engine")
            return None
            
        # Use SQLAlchemy to get a connection
        conn = engine.raw_connection()
        
        # Log success 
        st.session_state.db_connected = True
        logging.info("Database connection successful")
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {str(e)}")
        logging.error(f"Database connection error: {str(e)}")
        # Clear the connection string if it's invalid
        if 'db_url' in st.session_state:
            del st.session_state.db_url
        return None

def get_sqlalchemy_engine():
    """Get a SQLAlchemy engine for the database"""
    # Try using DATABASE_URL from environment first
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        # Fall back to session state
        db_url = st.session_state.get('db_url')
    
    if not db_url:
        # Create a form to collect the database URL
        st.warning("Database connection not configured")
        with st.form("db_connection_form"):
            new_db_url = st.text_input("Enter Supabase Database Connection URL:")
            submitted = st.form_submit_button("Connect")
            
            if submitted and new_db_url:
                st.session_state.db_url = new_db_url
                st.success("Database connection established")
                st.rerun()
        return None
    
    # Don't use the SUPABASE_URL for database connections
    if db_url.startswith('https://'):
        logging.error("Invalid database URL format - detected website URL instead of database connection string")
        st.error("Invalid database URL format. Please provide a PostgreSQL connection string.")
        
        # Show a form to get the correct database URL
        with st.form("db_connection_fix_form"):
            st.info("Please enter the PostgreSQL connection string from Supabase:")
            st.markdown("""
            To get the correct connection string:
            1. Go to your Supabase project dashboard
            2. Click on "Project Settings" in the left sidebar
            3. Select "Database" 
            4. Find and copy the "Connection string" in PostgreSQL format
            """)
            new_db_url = st.text_input("PostgreSQL Connection String:")
            submitted = st.form_submit_button("Connect")
            
            if submitted and new_db_url:
                # Update session state with the new URL
                st.session_state.db_url = new_db_url
                # Also update environment variable
                os.environ['DATABASE_URL'] = new_db_url
                st.success("Database connection established")
                st.rerun()
        return None
    
    try:
        # Log attempt to create engine
        logging.info(f"Attempting to create SQLAlchemy engine")
        
        # Create engine for Supabase connection
        engine = create_engine(
            db_url,
            connect_args={
                "sslmode": "require"
            }
        )
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            
        logging.info("SQLAlchemy engine created successfully")
        return engine
    except Exception as e:
        st.error(f"Error creating SQLAlchemy engine: {str(e)}")
        logging.error(f"SQLAlchemy engine error: {str(e)}")
        
        # Show a form to get the correct database URL
        with st.form("db_connection_error_form"):
            st.error(f"Database connection error: {str(e)}")
            st.info("Please enter the correct PostgreSQL connection string from Supabase:")
            new_db_url = st.text_input("PostgreSQL Connection String:")
            submitted = st.form_submit_button("Connect")
            
            if submitted and new_db_url:
                # Update session state with the new URL
                st.session_state.db_url = new_db_url
                # Also update environment variable
                os.environ['DATABASE_URL'] = new_db_url
                st.success("Database connection established")
                st.rerun()
        
        return None
