"""
Highland Tower Development - Enterprise Construction Management Platform
$45.5M Mixed-Use Development - Production Ready Application

DEFAULT DEPLOYMENT: gcPanel Core Focused
This is the primary production entry point using the latest stable version.
All features optimized for the Highland Tower Development project.
"""

import streamlit as st

# Set page config FIRST before any other Streamlit commands
st.set_page_config(
    page_title="Highland Tower Development - gcPanel Core Focused",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import the Highland Tower Core Focused implementation (DEFAULT)
from gcpanel_core_focused import main as highland_tower_main, apply_highland_tower_styling

def main():
    """
    Highland Tower Development Production Deployment
    
    DEFAULT VERSION: gcPanel Core Focused
    - Enterprise user management and security
    - Real-time project tracking ($45.5M project)
    - 23 Active RFIs in Engineering module
    - Advanced cost management and analytics
    - Quality control and progress photos
    - Mobile-responsive design
    """
    # Apply Highland Tower enterprise styling
    apply_highland_tower_styling()
    
    # Run the Highland Tower Core Focused application
    highland_tower_main()

if __name__ == "__main__":
    main()