"""
Change Orders Module for gcPanel

This module implements the Change Orders functionality for the Contracts Management section,
using the standardized CRUD template for consistent styling and behavior.
"""

import streamlit as st
import os
import json
from datetime import datetime, timedelta
import random

from modules.crud_template import CrudModule
from assets.crud_styler import (
    apply_crud_styles, 
    render_form_actions, 
    render_crud_fieldset
)

class ChangeOrderModule(CrudModule):
    def __init__(self):
        """Initialize the Change Orders module with configuration."""
        super().__init__(
            module_name="Change Orders",
            data_file_path="data/contracts/change_orders.json",
            id_field="change_order_id",
            list_columns=["change_order_id", "title", "amount", "contract", "date_submitted", "status"],
            default_sort_field="change_order_id",
            default_sort_direction="asc",
            status_field="status",
            filter_options=["Draft", "Submitted", "Under Review", "Approved", "Rejected"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        statuses = ['Draft', 'Submitted', 'Under Review', 'Approved', 'Rejected']
        types = ['Owner Request', 'Design Change', 'Field Condition', 'Code Requirement', 'Value Engineering']
        contracts = ['OC-001', 'SC-001', 'SC-003', 'SC-004', 'SC-007']
        
        demo_items = []
        
        # Create several sample change orders
        for i in range(1, 11):
            submission_date = datetime.now() - timedelta(days=random.randint(7, 90))
            review_date = None
            if random.random() > 0.3:  # 70% chance to have a review date
                review_date = submission_date + timedelta(days=random.randint(3, 14))
            
            approval_date = None
            if review_date and random.random() > 0.4:  # 60% chance to have approval date if reviewed
                approval_date = review_date + timedelta(days=random.randint(1, 7))
            
            status = random.choice(statuses)
            amount = random.randint(-50000, 200000)  # Allow for negative change orders (credits)
            
            item = {
                'change_order_id': f'CO-{i:03d}',
                'title': f'Change Order {i}',
                'description': f'This is a sample change order {i}',
                'type': random.choice(types),
                'amount': amount,
                'contract': random.choice(contracts),
                'date_submitted': submission_date.strftime('%Y-%m-%d'),
                'date_reviewed': review_date.strftime('%Y-%m-%d') if review_date else None,
                'date_approved': approval_date.strftime('%Y-%m-%d') if approval_date else None,
                'status': status,
                'requested_by': 'John Smith',
                'approved_by': 'Jane Doe' if status == 'Approved' else None,
                'reason': f'Reason for change order {i}',
                'impact_description': 'This change order will affect...',
                'documents': [],
                'signatures': []
            }
            demo_items.append(item)
        
        # Save demo data
        self._save_items(demo_items)
    
    def _create_new_item_template(self):
        """Create a template for a new change order with default values."""
        change_order_id = self._generate_new_id()
        
        return {
            'change_order_id': f'CO-{int(change_order_id):03d}',
            'title': '',
            'description': '',
            'type': 'Owner Request',
            'amount': 0.00,
            'contract': 'OC-001',
            'date_submitted': datetime.now().strftime('%Y-%m-%d'),
            'date_reviewed': None,
            'date_approved': None,
            'status': 'Draft',
            'requested_by': '',
            'approved_by': None,
            'reason': '',
            'impact_description': '',
            'documents': [],
            'signatures': []
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for change orders."""
        items = self._get_items()
        
        # If no items exist yet, start with ID 1
        if not items:
            return "1"
        
        # Find the highest numerical ID and increment
        max_id = 0
        for item in items:
            change_order_id = item.get('change_order_id', '')
            if change_order_id.startswith('CO-'):
                try:
                    num = int(change_order_id.split('-')[1])
                    max_id = max(max_id, num)
                except:
                    pass
        
        return str(max_id + 1)
    
    def _get_status_class(self, status):
        """Get the status class for a given status value."""
        status_classes = {
            'Draft': 'secondary',
            'Submitted': 'info',
            'Under Review': 'warning',
            'Approved': 'success',
            'Rejected': 'danger'
        }
        return status_classes.get(status, 'secondary')
    
    def render_detail_view(self):
        """Render the detail view for creating, viewing, or editing a change order."""
        # Apply CRUD styles
        apply_crud_styles()
        
        base_key = self._get_state_key_prefix()
        
        # Get view mode
        is_new = st.session_state.get(f'{base_key}_view') == 'new'
        is_edit_mode = st.session_state.get(f'{base_key}_edit_mode', False)
        
        # Get item data
        if is_new:
            item = self._create_new_item_template()
            detail_title = "New Change Order"
        else:
            item_id = st.session_state.get(f'{base_key}_selected_id')
            item = self._get_item_by_id(item_id)
            if not item:
                st.error(f"Change Order with ID {item_id} not found")
                return
            detail_title = f"{item.get('title', item.get('change_order_id', 'Change Order'))}"
        
        # Render the detail container
        from assets.crud_styler import render_crud_detail_container, end_crud_detail_container
        
        mode_prefix = "New" if is_new else "Edit" if is_edit_mode else "View"
        container_title = f"{mode_prefix}: {detail_title}"
        
        detail_actions = render_crud_detail_container(
            title=container_title,
            is_new=is_new,
            back_button=True
        )
        
        # Check if back button was clicked
        if detail_actions['back_clicked']:
            st.session_state[f'{base_key}_view'] = 'list'
            st.rerun()
        
        # Display top action buttons for view mode
        if not is_new and not is_edit_mode:
            col1, col2, col3 = st.columns([1, 1, 6])
            with col1:
                if st.button("✏️ Edit", type="primary", key=f"edit_{base_key}_action"):
                    st.session_state[f'{base_key}_edit_mode'] = True
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", type="secondary", key=f"delete_{base_key}_action"):
                    st.warning("Are you sure you want to delete this change order?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key=f"confirm_delete_{base_key}"):
                            self._delete_item(item['change_order_id'])
                            st.success("Change order deleted successfully")
                            st.session_state[f'{base_key}_view'] = 'list'
                            st.rerun()
                    with confirm_col2:
                        if st.button("Cancel", key=f"cancel_delete_{base_key}"):
                            st.rerun()
        
        # Create form for editing or read-only view for viewing
        if is_edit_mode or is_new:
            with st.form(f"{base_key}_form"):
                # Basic Information Section
                def render_basic_info():
                    col1, col2 = st.columns(2)
                    with col1:
                        change_order_id = st.text_input("Change Order ID", value=item['change_order_id'], disabled=not is_new)
                    with col2:
                        title = st.text_input("Title", value=item['title'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        change_type = st.selectbox("Type", options=[
                            'Owner Request', 'Design Change', 'Field Condition', 'Code Requirement', 'Value Engineering'
                        ], index=['Owner Request', 'Design Change', 'Field Condition', 'Code Requirement', 'Value Engineering'].index(
                            item['type'] if item.get('type') in ['Owner Request', 'Design Change', 'Field Condition', 'Code Requirement', 'Value Engineering'] 
                            else 'Owner Request')
                        )
                    with col2:
                        status = st.selectbox("Status", options=[
                            'Draft', 'Submitted', 'Under Review', 'Approved', 'Rejected'
                        ], index=['Draft', 'Submitted', 'Under Review', 'Approved', 'Rejected'].index(
                            item['status'] if item['status'] in ['Draft', 'Submitted', 'Under Review', 'Approved', 'Rejected'] 
                            else 'Draft')
                        )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        contract = st.text_input("Contract ID", value=item['contract'])
                    with col2:
                        amount = st.number_input("Amount ($)", 
                                              value=float(item['amount']) if item.get('amount') is not None else 0.0,
                                              step=1000.0,
                                              format="%.2f")
                    
                    description = st.text_area("Description", value=item['description'], height=100)
                
                render_crud_fieldset("Basic Information", render_basic_info)
                
                # Details Section
                def render_details():
                    col1, col2 = st.columns(2)
                    with col1:
                        requested_by = st.text_input("Requested By", value=item['requested_by'])
                    with col2:
                        approved_by = st.text_input("Approved By", value=item['approved_by'] if item.get('approved_by') else '')
                    
                    reason = st.text_area("Reason", value=item['reason'], height=100)
                    impact_description = st.text_area("Impact Description", value=item['impact_description'], height=100)
                
                render_crud_fieldset("Details", render_details)
                
                # Dates Section
                def render_dates():
                    col1, col2 = st.columns(2)
                    with col1:
                        date_submitted = st.date_input("Date Submitted", 
                            value=datetime.strptime(item['date_submitted'], '%Y-%m-%d') if item['date_submitted'] else datetime.now()
                        )
                    with col2:
                        date_reviewed = st.date_input("Date Reviewed",
                            value=datetime.strptime(item['date_reviewed'], '%Y-%m-%d') if item.get('date_reviewed') else None
                        )
                    
                    date_approved = st.date_input("Date Approved",
                        value=datetime.strptime(item['date_approved'], '%Y-%m-%d') if item.get('date_approved') else None
                    )
                
                render_crud_fieldset("Dates", render_dates)
                
                # Form Actions
                form_actions = render_form_actions(
                    save_label="Save Change Order",
                    cancel_label="Cancel",
                    delete_label="Delete Change Order",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    # Update item with form values
                    updated_item = {
                        'change_order_id': change_order_id,
                        'title': title,
                        'description': description,
                        'type': change_type,
                        'amount': float(amount),
                        'contract': contract,
                        'date_submitted': date_submitted.strftime('%Y-%m-%d'),
                        'date_reviewed': date_reviewed.strftime('%Y-%m-%d') if date_reviewed else None,
                        'date_approved': date_approved.strftime('%Y-%m-%d') if date_approved else None,
                        'status': status,
                        'requested_by': requested_by,
                        'approved_by': approved_by if approved_by else None,
                        'reason': reason,
                        'impact_description': impact_description,
                        'documents': item.get('documents', []),
                        'signatures': item.get('signatures', [])
                    }
                    
                    # Save the updated item
                    self._save_item(updated_item)
                    
                    # Show success message and return to list view
                    st.success("Change order saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked'] and not is_new:
                    self._delete_item(item['change_order_id'])
                    st.success("Change order deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view
            # Basic Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Basic Information")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Change Order ID:** {item['change_order_id']}")
            with col2:
                st.markdown(f"**Title:** {item['title']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Type:** {item['type']}")
            with col2:
                status_html = f"""
                <div style="display: flex; align-items: center; background: transparent;">
                    <span class='crud-status crud-status-{self._get_status_class(item['status'])}' style="outline: none; box-shadow: none; border: none;">{item['status']}</span>
                </div>
                """
                st.markdown("**Status:**")
                st.markdown(status_html, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Contract ID:** {item['contract']}")
            with col2:
                # Format amount with positive/negative styling
                amount = float(item['amount'])
                amount_color = "green" if amount >= 0 else "red"
                amount_prefix = "+" if amount > 0 else ""
                st.markdown(f"**Amount:** <span style='color: {amount_color};'>{amount_prefix}${amount:,.2f}</span>", unsafe_allow_html=True)
            
            if item.get('description'):
                st.markdown(f"**Description:**")
                st.markdown(f"```{item['description']}```")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Details Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Details")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Requested By:** {item['requested_by']}")
            with col2:
                st.markdown(f"**Approved By:** {item.get('approved_by', 'Pending Approval')}")
            
            if item.get('reason'):
                st.markdown(f"**Reason:**")
                st.markdown(f"```{item['reason']}```")
            
            if item.get('impact_description'):
                st.markdown(f"**Impact Description:**")
                st.markdown(f"```{item['impact_description']}```")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Dates Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Dates")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Date Submitted:** {item['date_submitted']}")
            with col2:
                st.markdown(f"**Date Reviewed:** {item.get('date_reviewed', 'Not yet reviewed')}")
            
            st.markdown(f"**Date Approved:** {item.get('date_approved', 'Not yet approved')}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Signatures Section (if present)
            if len(item.get('signatures', [])) > 0:
                st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
                st.subheader("Digital Signatures")
                
                for sig in item.get('signatures', []):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**{sig.get('name', '')}**")
                    with col2:
                        st.markdown(f"Signed: {sig.get('date', '')}")
                st.markdown("</div>", unsafe_allow_html=True)
        
        end_crud_detail_container()

def render():
    """Render the Change Orders module."""
    st.title("Change Orders")
    
    # Create and render the Change Orders module
    change_orders = ChangeOrderModule()
    change_orders.render()