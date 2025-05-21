"""
Standalone BIM module for gcPanel.

This module provides BIM (Building Information Modeling) functionality
in a self-contained manner to avoid conflicts with other modules.
"""

from modules.standalone_bim.simple_bim_viewer import render_standalone_bim

def render_bim_standalone():
    """Render the standalone BIM viewer"""
    render_standalone_bim()