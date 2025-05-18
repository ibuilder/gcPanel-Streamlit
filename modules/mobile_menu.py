"""
Mobile menu component for the gcPanel application.

This module adds the mobile companion app to the main menu.
"""

from components.page_header import render_page_header
from modules.mobile_companion import mobile_companion_page

def render_mobile_menu():
    """
    Render the mobile companion app page.
    """
    # Display page header with action buttons
    actions = render_page_header("Mobile Companion", add_button=True, edit_button=True)
    
    # Call the mobile companion page
    mobile_companion_page()