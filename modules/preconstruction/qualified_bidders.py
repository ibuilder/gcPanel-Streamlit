import streamlit as st
import pandas as pd
from modules.base_module import BaseModule
from utils.database import get_db_connection
from utils.auth import check_permission

# Module metadata
MODULE_DISPLAY_NAME = "Qualified Bidders"
MODULE_ICON = "users"

# Define module columns
COLUMNS = [
    ('id', 'ID', 'integer'),
    ('company_name', 'Company Name', 'text'),
    ('contact_name', 'Contact Name', 'text'),
    ('email', 'Email', 'text'),
    ('phone', 'Phone', 'text'),
    ('address', 'Address', 'text'),
    ('city', 'City', 'text'),
    ('state', 'State', 'text'),
    ('zip_code', 'ZIP Code', 'text'),
    ('trade', 'Trade', 'text'),
    ('is_qualified', 'Qualified', 'boolean'),
    ('notes', 'Notes', 'text')
]

# Define form fields
FORM_FIELDS = [
    ('id', 'ID', 'integer', False, None),
    ('company_name', 'Company Name', 'text', True, None),
    ('contact_name', 'Contact Name', 'text', True, None),
    ('email', 'Email', 'text', True, None),
    ('phone', 'Phone', 'text', True, None),
    ('address', 'Address', 'text', False, None),
    ('city', 'City', 'text', False, None),
    ('state', 'State', 'select', False, ['', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']),
    ('zip_code', 'ZIP Code', 'text', False, None),
    ('trade', 'Trade', 'text', True, None),
    ('is_qualified', 'Qualified', 'boolean', False, None),
    ('notes', 'Notes', 'textarea', False, None)
]

# Create module instance
qualified_bidders_module = BaseModule('qualified_bidders', 'Qualified Bidders', COLUMNS, FORM_FIELDS)

def render_list():
    """Render the list view"""
    qualified_bidders_module.render_list()

def render_view():
    """Render the detail view"""
    qualified_bidders_module.render_view()

def render_form():
    """Render the form view"""
    qualified_bidders_module.render_form()
