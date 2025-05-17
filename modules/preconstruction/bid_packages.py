import streamlit as st
import pandas as pd
from modules.base_module import BaseModule
from utils.database import get_db_connection
from utils.auth import check_permission

# Module metadata
MODULE_DISPLAY_NAME = "Bid Packages"
MODULE_ICON = "package"

# Define module columns
COLUMNS = [
    ('id', 'ID', 'integer'),
    ('package_number', 'Package #', 'text'),
    ('title', 'Title', 'text'),
    ('description', 'Description', 'text'),
    ('issue_date', 'Issue Date', 'date'),
    ('due_date', 'Due Date', 'date'),
    ('budget_amount', 'Budget Amount', 'float'),
    ('status', 'Status', 'text'),
    ('trade', 'Trade', 'text'),
    ('scope_included', 'Scope Included', 'text'),
    ('scope_excluded', 'Scope Excluded', 'text'),
    ('instructions', 'Instructions', 'text')
]

# Define form fields
FORM_FIELDS = [
    ('id', 'ID', 'integer', False, None),
    ('package_number', 'Package #', 'text', True, None),
    ('title', 'Title', 'text', True, None),
    ('description', 'Description', 'textarea', False, None),
    ('issue_date', 'Issue Date', 'date', True, None),
    ('due_date', 'Due Date', 'date', True, None),
    ('budget_amount', 'Budget Amount', 'number', False, None),
    ('status', 'Status', 'select', True, ['Draft', 'Issued', 'Addendum', 'Closed']),
    ('trade', 'Trade', 'text', True, None),
    ('scope_included', 'Scope Included', 'textarea', False, None),
    ('scope_excluded', 'Scope Excluded', 'textarea', False, None),
    ('instructions', 'Instructions', 'textarea', False, None)
]

# Create module instance
bid_packages_module = BaseModule('bid_packages', 'Bid Packages', COLUMNS, FORM_FIELDS)

def render_list():
    """Render the list view"""
    bid_packages_module.render_list()

def render_view():
    """Render the detail view"""
    bid_packages_module.render_view()

def render_form():
    """Render the form view"""
    bid_packages_module.render_form()
