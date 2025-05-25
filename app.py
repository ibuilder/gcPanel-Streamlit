"""
Highland Tower Development - Enterprise Construction Management Platform
$45.5M Mixed-Use Development - Primary Production Application

This is the main entry point for deployment, routing to the enterprise version.
"""

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