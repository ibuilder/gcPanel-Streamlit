import streamlit as st
import pandas as pd
from modules.base_module import BaseModule
from utils.database import get_db_connection
from utils.auth import check_permission

# Module metadata
MODULE_DISPLAY_NAME = "Requests for Information"
MODULE_ICON = "help-circle"

# Define module columns
COLUMNS = [
    ('id', 'ID', 'integer'),
    ('rfi_number', 'RFI #', 'text'),
    ('title', 'Title', 'text'),
    ('description', 'Description', 'text'),
    ('submitted_date', 'Submitted Date', 'date'),
    ('response_due_date', 'Response Due Date', 'date'),
    ('response_date', 'Response Date', 'date'),
    ('status', 'Status', 'text'),
    ('submitter', 'Submitter', 'text'),
    ('assigned_to', 'Assigned To', 'text'),
    ('response', 'Response', 'text'),
    ('drawing_references', 'Drawing References', 'text'),
    ('spec_references', 'Spec References', 'text')
]

# Define form fields
FORM_FIELDS = [
    ('id', 'ID', 'integer', False, None),
    ('rfi_number', 'RFI #', 'text', True, None),
    ('title', 'Title', 'text', True, None),
    ('description', 'Description', 'textarea', True, None),
    ('submitted_date', 'Submitted Date', 'date', True, None),
    ('response_due_date', 'Response Due Date', 'date', True, None),
    ('response_date', 'Response Date', 'date', False, None),
    ('status', 'Status', 'select', True, ['Draft', 'Submitted', 'In Review', 'Responded', 'Closed']),
    ('submitter', 'Submitter', 'text', True, None),
    ('assigned_to', 'Assigned To', 'text', True, None),
    ('response', 'Response', 'textarea', False, None),
    ('drawing_references', 'Drawing References', 'text', False, None),
    ('spec_references', 'Spec References', 'text', False, None)
]

# Create module instance
rfi_module = BaseModule('rfi', 'Requests for Information', COLUMNS, FORM_FIELDS)

def render_list():
    """Render the list view"""
    rfi_module.render_list()

def render_view():
    """Render the detail view"""
    rfi_module.render_view()

def render_form():
    """Render the form view"""
    rfi_module.render_form()
