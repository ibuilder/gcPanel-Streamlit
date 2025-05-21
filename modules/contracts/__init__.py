"""
Contracts Module for gcPanel Construction Management Dashboard.

This module provides comprehensive contract management functionality
with integrated digital signature capabilities.
"""

import streamlit as st
from modules.contracts.service import ContractsService
from modules.contracts.integrated_contracts import render_integrated_contracts

def render_contracts():
    """Render the contracts module with integrated digital signatures."""
    # Initialize contract data and pass to the render function
    ContractsService.initialize_data_files()
    render_integrated_contracts()