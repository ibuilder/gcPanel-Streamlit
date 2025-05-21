"""
Standalone BIM Module initialization.

This module provides a self-contained BIM viewer that works independently
without interfering with other parts of the application.
"""

from modules.standalone_bim.simple_bim_viewer import render_standalone_bim

def render_bim_standalone():
    """Render the standalone BIM viewer."""
    render_standalone_bim()