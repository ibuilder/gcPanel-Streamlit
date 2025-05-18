"""
Documentation and contextual help system for gcPanel.

This module provides a documentation system with tooltips,
guided tours, and comprehensive user guides.
"""

import streamlit as st
import json
import os
import logging
from functools import wraps

# Setup logging
logger = logging.getLogger(__name__)

# Constants
DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
HELP_TOPICS_FILE = os.path.join(DOCS_DIR, "help_topics.json")

def ensure_docs_dir_exists():
    """Ensure documentation directory exists."""
    os.makedirs(DOCS_DIR, exist_ok=True)

def load_help_topics():
    """
    Load help topics from the help_topics.json file.
    
    Returns:
        dict: Help topics dictionary
    """
    ensure_docs_dir_exists()
    
    # Create default help topics file if it doesn't exist
    if not os.path.exists(HELP_TOPICS_FILE):
        default_topics = {
            "dashboard": {
                "title": "Dashboard",
                "description": "The Dashboard provides an overview of your project's status and key metrics.",
                "sections": [
                    {
                        "title": "Project Metrics",
                        "content": "This section displays key project metrics including schedule progress, budget status, and quality indicators."
                    },
                    {
                        "title": "Recent Activity",
                        "content": "The recent activity feed shows the latest updates and changes in your project."
                    }
                ]
            },
            "project_information": {
                "title": "Project Information",
                "description": "The Project Information module stores all essential details about your project.",
                "sections": [
                    {
                        "title": "Project Details",
                        "content": "This section contains basic project information such as name, type, budget, and timeline."
                    },
                    {
                        "title": "Project Team",
                        "content": "The team section lists all project team members and their contact information."
                    }
                ]
            }
        }
        
        with open(HELP_TOPICS_FILE, 'w') as f:
            json.dump(default_topics, f, indent=2)
        
        return default_topics
    
    # Load existing help topics
    try:
        with open(HELP_TOPICS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading help topics: {str(e)}")
        return {}

def get_help_topic(topic_id):
    """
    Get help content for a specific topic.
    
    Args:
        topic_id: Help topic identifier
        
    Returns:
        dict: Help topic content or None if not found
    """
    help_topics = load_help_topics()
    return help_topics.get(topic_id)

def render_help_content(topic_id):
    """
    Render help content for a specific topic.
    
    Args:
        topic_id: Help topic identifier
    """
    topic = get_help_topic(topic_id)
    
    if not topic:
        st.warning(f"Help topic '{topic_id}' not found.")
        return
    
    st.header(topic["title"])
    st.markdown(topic["description"])
    
    for section in topic.get("sections", []):
        st.subheader(section["title"])
        st.markdown(section["content"])
        
        # Add images if available
        if "image" in section:
            st.image(section["image"], caption=section.get("image_caption", ""))
        
        # Add videos if available
        if "video" in section:
            st.video(section["video"])

def tooltip(text, help_text):
    """
    Create a tooltip with help text.
    
    Args:
        text: Text to display
        help_text: Help text for the tooltip
        
    Returns:
        str: HTML for text with tooltip
    """
    tooltip_html = f"""
    <div class="tooltip-container">
        <span>{text}</span>
        <span class="tooltip-text">{help_text}</span>
    </div>
    """
    
    # Include the required CSS if not already added
    if "tooltip_css_added" not in st.session_state:
        tooltip_css = """
        <style>
        .tooltip-container {
            position: relative;
            display: inline-block;
            border-bottom: 1px dotted #3367D6;
        }
        
        .tooltip-container .tooltip-text {
            visibility: hidden;
            width: 200px;
            background-color: #333;
            color: #fff;
            text-align: center;
            border-radius: 4px;
            padding: 5px;
            position: absolute;
            z-index: 1000;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 0.8rem;
        }
        
        .tooltip-container .tooltip-text::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #333 transparent transparent transparent;
        }
        
        .tooltip-container:hover .tooltip-text {
            visibility: visible;
            opacity: 1;
        }
        </style>
        """
        st.markdown(tooltip_css, unsafe_allow_html=True)
        st.session_state.tooltip_css_added = True
    
    return tooltip_html

def with_help_button(func):
    """
    Decorator to add a help button to a page.
    
    Args:
        func: Function to decorate
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get function name as topic_id
        topic_id = func.__name__.replace("render_", "")
        
        # Add help button
        if st.button("📘 Help", key=f"help_btn_{topic_id}"):
            st.session_state.show_help = topic_id
        
        # Render help if requested
        if st.session_state.get("show_help") == topic_id:
            with st.expander("Help Guide", expanded=True):
                render_help_content(topic_id)
                if st.button("Close Help", key=f"close_help_{topic_id}"):
                    st.session_state.show_help = None
        
        # Call the original function
        return func(*args, **kwargs)
    
    return wrapper

def initialize_documentation():
    """Initialize the documentation system."""
    ensure_docs_dir_exists()
    
    # Create CSS for documentation components
    docs_css = """
    <style>
    .help-icon {
        color: #3367D6;
        cursor: pointer;
        margin-left: 5px;
    }
    
    .help-container {
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f8f9fa;
    }
    
    .help-title {
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .help-section {
        margin-top: 1rem;
    }
    
    .help-section-title {
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .onboarding-step {
        border-left: 3px solid #3367D6;
        padding-left: 1rem;
        margin-bottom: 1rem;
    }
    
    .onboarding-step-title {
        font-weight: bold;
        font-size: 1.1rem;
    }
    </style>
    """
    
    st.markdown(docs_css, unsafe_allow_html=True)

def render_user_guide():
    """Render the comprehensive user guide."""
    st.title("User Guide")
    
    # Sidebar for navigation
    st.sidebar.header("Guide Sections")
    sections = [
        "Getting Started",
        "Dashboard",
        "Project Information",
        "Scheduling",
        "Contracts",
        "Cost Management",
        "Documents",
        "BIM Integration",
        "Field Operations",
        "Reports"
    ]
    
    selected_section = st.sidebar.radio("Select a section", sections)
    
    # Main content
    if selected_section == "Getting Started":
        st.header("Getting Started with gcPanel")
        
        st.markdown("""
        Welcome to gcPanel, your comprehensive construction management platform. 
        This guide will help you get started with the system and learn how to use its key features.
        """)
        
        st.subheader("System Requirements")
        st.markdown("""
        - Modern web browser (Chrome, Firefox, Safari, or Edge)
        - Internet connection
        - Screen resolution of at least 1366x768 (desktop/laptop)
        - Mobile devices: iOS 12+ or Android 8+
        """)
        
        st.subheader("Logging In")
        st.markdown("""
        1. Navigate to your gcPanel URL
        2. Enter your username and password
        3. Click "Sign In"
        
        If you've forgotten your password, click the "Forgot Password" link on the login page.
        """)
        
        st.subheader("Navigation")
        st.markdown("""
        The gcPanel interface consists of:
        
        - **Left sidebar:** Main navigation menu
        - **Header:** Project selector, notifications, and user menu
        - **Main content area:** Module-specific content
        
        Click on any menu item in the sidebar to navigate to that module.
        """)
    
    elif selected_section == "Dashboard":
        st.header("Dashboard")
        
        st.markdown("""
        The Dashboard provides a high-level overview of your project's status and key metrics.
        """)
        
        st.subheader("Project Metrics")
        st.markdown("""
        The top section displays key project metrics including:
        
        - Schedule progress
        - Budget status
        - Quality indicators
        - Safety metrics
        
        These metrics are updated in real-time as data is entered into the system.
        """)
        
        st.subheader("Charts and Visualizations")
        st.markdown("""
        The Dashboard includes several charts to visualize project data:
        
        - Schedule progress chart
        - Budget allocation chart
        - Quality metrics chart
        
        Click on any chart to view more detailed information.
        """)
        
        st.subheader("Recent Activity")
        st.markdown("""
        The Recent Activity feed shows the latest updates and changes in your project,
        including new documents, RFIs, submittals, and important milestones.
        """)
    
    # Additional sections would be implemented similarly

def render_onboarding_tutorial():
    """Render an onboarding tutorial for new users."""
    st.title("Welcome to gcPanel!")
    
    st.markdown("""
    This tutorial will guide you through the basic features of gcPanel
    and help you get started with managing your construction projects.
    """)
    
    # Check if onboarding has been completed
    if "onboarding_complete" not in st.session_state:
        st.session_state.onboarding_complete = False
        st.session_state.onboarding_step = 1
    
    # Display current onboarding step
    if not st.session_state.onboarding_complete:
        step = st.session_state.onboarding_step
        
        st.progress(step / 5)  # 5 total steps
        
        if step == 1:
            st.subheader("Step 1: Navigating the Dashboard")
            
            st.markdown("""
            <div class="onboarding-step">
                <div class="onboarding-step-title">The Dashboard</div>
                <p>The Dashboard is your central hub for project information. Here you can see:</p>
                <ul>
                    <li>Project metrics and KPIs</li>
                    <li>Schedule and budget status</li>
                    <li>Recent activity</li>
                    <li>Important notifications</li>
                </ul>
                <p>Use the navigation menu on the left to access different modules.</p>
            </div>
            """, unsafe_allow_html=True)
            
        elif step == 2:
            st.subheader("Step 2: Project Information")
            
            st.markdown("""
            <div class="onboarding-step">
                <div class="onboarding-step-title">Project Information</div>
                <p>The Project Information module contains all essential details about your project:</p>
                <ul>
                    <li>Basic project information (name, type, location)</li>
                    <li>Project team members and contacts</li>
                    <li>Key project parameters</li>
                    <li>Project timeline</li>
                </ul>
                <p>You can edit project information by clicking the "Edit" button in the top-right corner.</p>
            </div>
            """, unsafe_allow_html=True)
            
        elif step == 3:
            st.subheader("Step 3: Documents Management")
            
            st.markdown("""
            <div class="onboarding-step">
                <div class="onboarding-step-title">Documents Management</div>
                <p>The Documents module helps you organize and manage all project documents:</p>
                <ul>
                    <li>Upload and categorize documents</li>
                    <li>Track document versions</li>
                    <li>Manage approvals and reviews</li>
                    <li>Search for documents</li>
                </ul>
                <p>Click "Add Document" to upload a new document to the system.</p>
            </div>
            """, unsafe_allow_html=True)
            
        elif step == 4:
            st.subheader("Step 4: BIM Integration")
            
            st.markdown("""
            <div class="onboarding-step">
                <div class="onboarding-step-title">BIM Integration</div>
                <p>The BIM module allows you to visualize your building information model:</p>
                <ul>
                    <li>View 3D models in the browser</li>
                    <li>Extract information from the model</li>
                    <li>Link documents to model elements</li>
                    <li>Track issues directly in the model</li>
                </ul>
                <p>Upload your IFC files to start using the BIM features.</p>
            </div>
            """, unsafe_allow_html=True)
            
        elif step == 5:
            st.subheader("Step 5: Customizing Your Experience")
            
            st.markdown("""
            <div class="onboarding-step">
                <div class="onboarding-step-title">Customizing Your Experience</div>
                <p>gcPanel can be customized to match your preferences:</p>
                <ul>
                    <li>Change theme (light/dark mode)</li>
                    <li>Configure notifications</li>
                    <li>Set up your user profile</li>
                    <li>Adjust accessibility settings</li>
                </ul>
                <p>Click on your profile picture in the top-right corner to access these settings.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if step > 1:
                if st.button("← Previous"):
                    st.session_state.onboarding_step -= 1
                    st.rerun()
        
        with col2:
            if step < 5:
                if st.button("Next →"):
                    st.session_state.onboarding_step += 1
                    st.rerun()
            else:
                if st.button("Complete Tutorial"):
                    st.session_state.onboarding_complete = True
                    st.rerun()
    
    else:
        st.success("Onboarding complete! You're ready to start using gcPanel.")
        
        if st.button("Restart Tutorial"):
            st.session_state.onboarding_complete = False
            st.session_state.onboarding_step = 1
            st.rerun()