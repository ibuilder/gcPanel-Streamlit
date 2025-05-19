"""
Integration Module for gcPanel.

This module provides functionality to connect with external platforms
and import data from them into gcPanel.
"""

import streamlit as st
from modules.integrations.import_manager import render_integration_import_interface

def render_integrations():
    """Render the integrations module."""
    # Delegate to the import manager interface
    render_integration_import_interface()