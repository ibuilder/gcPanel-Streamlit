"""
Highland Tower Development - Enterprise Construction Management Platform
$45.5M Mixed-Use Development - Primary Production Application

This is the main entry point for deployment, routing to the enterprise version.
"""

import streamlit as st

# Set page config FIRST before any other Streamlit commands
st.set_page_config(
    page_title="Highland Tower Development - gcPanel",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import the current best Highland Tower implementation
from gcpanel_core_focused import main as highland_tower_main, apply_highland_tower_styling

def main():
    """Main entry point for Highland Tower Development production deployment"""
    # Apply enterprise styling
    apply_highland_tower_styling()
    
    # Run the Highland Tower enterprise application
    highland_tower_main()

if __name__ == "__main__":
    main()