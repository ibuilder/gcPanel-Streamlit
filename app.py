"""
Highland Tower Development - Enterprise Construction Management Platform
$45.5M Mixed-Use Development - PRODUCTION READY

🏗️ DEFAULT DEPLOYMENT: gcPanel Core Focused
✅ Production-optimized for 120 residential + 8 retail units
✅ Enterprise features: RFIs, Cost Management, Quality Control
✅ Real-time project tracking with 23 active RFIs
✅ Mobile-responsive design for field operations
✅ Professional styling with optimized spacing
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
    # Run the Highland Tower Core Focused application
    # (styling is now handled within the main function)
    highland_tower_main()

if __name__ == "__main__":
    main()