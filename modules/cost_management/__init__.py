"""
Cost Management Module for gcPanel

This module provides cost management functionality for the construction management dashboard
using the standardized CRUD template for consistent styling and behavior.
"""

import streamlit as st
import os
import json
from datetime import datetime, timedelta
import random
import pandas as pd

from modules.crud_template import CrudModule
from components.digital_signature import render_digital_signature_section, get_signature_summary, validate_required_signatures
from assets.crud_styler import (
    apply_crud_styles, 
    render_form_actions, 
    render_crud_fieldset
)

class BudgetItemModule(CrudModule):
    def __init__(self):
        """Initialize the Budget Items module with configuration."""
        super().__init__(
            module_name="Budget Items",
            data_file_path="data/cost_management/budget_items.json",
            id_field="budget_item_id",
            list_columns=["budget_item_id", "description", "cost_code", "budgeted_amount", "actual_amount", "status"],
            default_sort_field="budget_item_id",
            default_sort_direction="asc",
            status_field="status",
            filter_options=["Active", "Pending", "Complete", "Over Budget", "Under Budget"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        cost_codes = [
            "01-1000", "02-2000", "03-3000", "04-4000", "05-5000", 
            "06-6000", "07-7000", "08-8000", "09-9000", "10-1000"
        ]
        
        division_names = [
            "General Requirements", "Site Construction", "Concrete", "Masonry", "Metals",
            "Wood & Plastics", "Thermal & Moisture", "Doors & Windows", "Finishes", "Specialties"
        ]
        
        statuses = ["Active", "Pending", "Complete", "Over Budget", "Under Budget"]
        
        demo_items = []
        
        # Create the main budget items
        for i in range(1, 11):
            budgeted_amount = random.uniform(50000, 5000000)
            actual_amount = budgeted_amount * random.uniform(0.8, 1.2)  # Vary between 80% and 120% of budget
            
            # Determine status based on budget vs. actual
            if actual_amount > budgeted_amount * 1.05:
                status = "Over Budget"
            elif actual_amount < budgeted_amount * 0.95:
                status = "Under Budget"
            else:
                status = random.choice(["Active", "Pending", "Complete"])
            
            item = {
                'budget_item_id': f'B-{i:03d}',
                'description': f'{division_names[i-1]} - {random.choice(["Phase 1", "Phase 2", "Allowance", "Base Bid"])}',
                'cost_code': cost_codes[i-1],
                'division': f'Division {str(i).zfill(2)}',
                'budgeted_amount': round(budgeted_amount, 2),
                'actual_amount': round(actual_amount, 2),
                'variance': round(budgeted_amount - actual_amount, 2),
                'variance_percent': round(((budgeted_amount - actual_amount) / budgeted_amount) * 100, 2),
                'status': status,
                'notes': f'Budget notes for {division_names[i-1]}',
                'created_date': (datetime.now() - timedelta(days=random.randint(90, 180))).strftime('%Y-%m-%d'),
                'last_updated': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
            }
            demo_items.append(item)
        
        # Save demo data
        self._save_items(demo_items)
    
    def _create_new_item_template(self):
        """Create a template for a new budget item with default values."""
        budget_item_id = self._generate_new_id()
        
        return {
            'budget_item_id': f'B-{int(budget_item_id):03d}',
            'description': '',
            'cost_code': '',
            'division': '',
            'budgeted_amount': 0.00,
            'actual_amount': 0.00,
            'variance': 0.00,
            'variance_percent': 0.00,
            'status': 'Active',
            'notes': '',
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'last_updated': datetime.now().strftime('%Y-%m-%d')
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for budget items."""
        items = self._get_items()
        
        # If no items exist yet, start with ID 1
        if not items:
            return "1"
        
        # Find the highest numerical ID and increment
        max_id = 0
        for item in items:
            budget_item_id = item.get('budget_item_id', '')
            if budget_item_id.startswith('B-'):
                try:
                    num = int(budget_item_id.split('-')[1])
                    max_id = max(max_id, num)
                except:
                    pass
        
        return str(max_id + 1)
    
    def _get_status_class(self, status):
        """Get the status class for a given status value."""
        status_classes = {
            'Active': 'primary',
            'Pending': 'info',
            'Complete': 'success',
            'Over Budget': 'danger',
            'Under Budget': 'success'
        }
        return status_classes.get(status, 'secondary')
    
    def render_detail_view(self):
        """Render the detail view for creating, viewing, or editing a budget item."""
        # Apply CRUD styles
        apply_crud_styles()
        
        base_key = self._get_state_key_prefix()
        
        # Get view mode
        is_new = st.session_state.get(f'{base_key}_view') == 'new'
        is_edit_mode = st.session_state.get(f'{base_key}_edit_mode', False)
        
        # Get item data
        if is_new:
            item = self._create_new_item_template()
            detail_title = "New Budget Item"
        else:
            item_id = st.session_state.get(f'{base_key}_selected_id')
            item = self._get_item_by_id(item_id)
            if not item:
                st.error(f"Budget Item with ID {item_id} not found")
                return
            detail_title = f"{item.get('description', item.get('budget_item_id', 'Budget Item'))}"
        
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
                    st.warning("Are you sure you want to delete this budget item?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key=f"confirm_delete_{base_key}"):
                            self._delete_item(item['budget_item_id'])
                            st.success("Budget item deleted successfully")
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
                        budget_item_id = st.text_input("Budget Item ID", value=item['budget_item_id'], disabled=not is_new)
                    with col2:
                        description = st.text_input("Description", value=item['description'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        cost_code = st.text_input("Cost Code", value=item['cost_code'])
                    with col2:
                        division = st.text_input("Division", value=item['division'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        budgeted_amount = st.number_input("Budgeted Amount ($)", 
                                                       value=float(item['budgeted_amount']) if item.get('budgeted_amount') is not None else 0.0,
                                                       min_value=0.0,
                                                       step=1000.0,
                                                       format="%.2f")
                    with col2:
                        actual_amount = st.number_input("Actual Amount ($)", 
                                                     value=float(item['actual_amount']) if item.get('actual_amount') is not None else 0.0,
                                                     min_value=0.0,
                                                     step=1000.0,
                                                     format="%.2f")
                    
                    status = st.selectbox("Status", options=[
                        'Active', 'Pending', 'Complete', 'Over Budget', 'Under Budget'
                    ], index=['Active', 'Pending', 'Complete', 'Over Budget', 'Under Budget'].index(
                        item['status'] if item['status'] in ['Active', 'Pending', 'Complete', 'Over Budget', 'Under Budget'] 
                        else 'Active')
                    )
                    
                    notes = st.text_area("Notes", value=item['notes'], height=100)
                
                render_crud_fieldset("Basic Information", render_basic_info)
                
                # Form Actions
                form_actions = render_form_actions(
                    save_label="Save Budget Item",
                    cancel_label="Cancel",
                    delete_label="Delete Budget Item",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    # Calculate variance
                    variance = float(budgeted_amount) - float(actual_amount)
                    variance_percent = (variance / float(budgeted_amount)) * 100 if float(budgeted_amount) > 0 else 0
                    
                    # Update item with form values
                    updated_item = {
                        'budget_item_id': budget_item_id,
                        'description': description,
                        'cost_code': cost_code,
                        'division': division,
                        'budgeted_amount': float(budgeted_amount),
                        'actual_amount': float(actual_amount),
                        'variance': round(variance, 2),
                        'variance_percent': round(variance_percent, 2),
                        'status': status,
                        'notes': notes,
                        'created_date': item['created_date'],
                        'last_updated': datetime.now().strftime('%Y-%m-%d')
                    }
                    
                    # Save the updated item
                    self._save_item(updated_item)
                    
                    # Show success message and return to list view
                    st.success("Budget item saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked'] and not is_new:
                    self._delete_item(item['budget_item_id'])
                    st.success("Budget item deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view
            # Basic Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Basic Information")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Budget Item ID:** {item['budget_item_id']}")
            with col2:
                st.markdown(f"**Description:** {item['description']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Cost Code:** {item['cost_code']}")
            with col2:
                st.markdown(f"**Division:** {item['division']}")
            
            # Determine variance styling
            variance = float(item['variance'])
            variance_color = "green" if variance >= 0 else "red"
            variance_sign = "+" if variance > 0 else ""
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Budgeted Amount:** ${float(item['budgeted_amount']):,.2f}")
            with col2:
                st.markdown(f"**Actual Amount:** ${float(item['actual_amount']):,.2f}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Variance:** <span style='color: {variance_color};'>{variance_sign}${abs(variance):,.2f}</span>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Variance Percent:** <span style='color: {variance_color};'>{variance_sign}{abs(float(item['variance_percent'])):,.2f}%</span>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                status_html = f"""
                <div style="display: flex; align-items: center; background: transparent;">
                    <span class='crud-status crud-status-{self._get_status_class(item['status'])}' style="outline: none; box-shadow: none; border: none;">{item['status']}</span>
                </div>
                """
                st.markdown("**Status:**")
                st.markdown(status_html, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**Last Updated:** {item['last_updated']}")
            
            if item.get('notes'):
                st.markdown(f"**Notes:**")
                st.markdown(f"```{item['notes']}```")
                
            st.markdown("</div>", unsafe_allow_html=True)
        
        end_crud_detail_container()
    
    def render_budget_summary(self):
        """Render a summary of the budget data."""
        items = self._get_items()
        
        if not items:
            st.info("No budget data available.")
            return
            
        # Calculate budget totals
        total_budget = sum(item.get('budgeted_amount', 0) for item in items)
        total_actual = sum(item.get('actual_amount', 0) for item in items)
        total_variance = total_budget - total_actual
        total_variance_percent = (total_variance / total_budget) * 100 if total_budget > 0 else 0
        
        # Format as currency
        format_currency = lambda x: f"${x:,.2f}"
        
        # Determine variance styling
        variance_color = "green" if total_variance >= 0 else "red"
        variance_sign = "+" if total_variance > 0 else ""
        variance_status = "Under Budget" if total_variance > 0 else "Over Budget" if total_variance < 0 else "On Budget"
        
        # Create a summary card
        st.markdown(f"<div style='background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        
        st.subheader("Budget Summary")
        
        # Row 1: Budget and Actual
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Budget", value=format_currency(total_budget))
        with col2:
            st.metric(label="Total Actual Costs", value=format_currency(total_actual))
        with col3:
            st.metric(
                label="Variance", 
                value=f"{variance_sign}{format_currency(abs(total_variance))}", 
                delta=f"{variance_sign}{total_variance_percent:.2f}%",
                delta_color="normal" if total_variance >= 0 else "inverse"
            )
        
        # Create a progress bar showing budget utilization
        utilization_pct = (total_actual / total_budget) * 100 if total_budget > 0 else 0
        
        # Determine color based on utilization
        if utilization_pct > 100:
            color = "red"
        elif utilization_pct > 90:
            color = "orange"
        else:
            color = "green"
            
        st.markdown(f"### Budget Utilization: {utilization_pct:.1f}%")
        st.progress(min(utilization_pct / 100, 1.0))
        
        # Status Summary by division
        st.markdown("### Budget Status by Division")
        division_data = {}
        
        for item in items:
            division = item.get('division', 'Unknown')
            if division not in division_data:
                division_data[division] = {
                    'budgeted': 0,
                    'actual': 0
                }
            
            division_data[division]['budgeted'] += item.get('budgeted_amount', 0)
            division_data[division]['actual'] += item.get('actual_amount', 0)
        
        # Create dataframe for display
        df_data = []
        for division, data in division_data.items():
            variance = data['budgeted'] - data['actual']
            variance_pct = (variance / data['budgeted']) * 100 if data['budgeted'] > 0 else 0
            status = "Under Budget" if variance > 0 else "Over Budget" if variance < 0 else "On Budget"
            
            df_data.append({
                'Division': division,
                'Budgeted': format_currency(data['budgeted']),
                'Actual': format_currency(data['actual']),
                'Variance': format_currency(abs(variance)),
                'Variance %': f"{'+' if variance >= 0 else '-'}{abs(variance_pct):.2f}%",
                'Status': status
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


class InvoiceModule(CrudModule):
    def __init__(self):
        """Initialize the Invoices module with configuration."""
        super().__init__(
            module_name="Invoices",
            data_file_path="data/cost_management/invoices.json",
            id_field="invoice_id",
            list_columns=["invoice_id", "vendor", "amount", "invoice_date", "due_date", "status"],
            default_sort_field="invoice_date",
            default_sort_direction="desc",
            status_field="status",
            filter_options=["Draft", "Submitted", "Approved", "Paid", "Rejected"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        vendors = [
            "ABC Concrete", "Steel Solutions Inc.", "Modern Electrical", "Plumbing Masters",
            "HVAC Experts", "Glass & Window Co.", "Flooring Specialists", "Masonry Pros",
            "Site Work Partners", "Roofing Contractors"
        ]
        
        payment_methods = ["ACH", "Check", "Wire Transfer", "Credit Card"]
        statuses = ["Draft", "Submitted", "Approved", "Paid", "Rejected"]
        
        demo_items = []
        
        # Create several sample invoices
        for i in range(1, 21):
            invoice_date = datetime.now() - timedelta(days=random.randint(0, 90))
            due_date = invoice_date + timedelta(days=30)
            payment_date = None
            
            # Set status and payment date accordingly
            if random.random() < 0.25:  # 25% already paid
                status = "Paid"
                payment_date = invoice_date + timedelta(days=random.randint(1, 25))
            elif random.random() < 0.1:  # 10% rejected
                status = "Rejected"
            else:
                days_passed = (datetime.now() - invoice_date).days
                if days_passed < 3:
                    status = "Draft"
                elif days_passed < 10:
                    status = "Submitted"
                else:
                    status = "Approved"
            
            # Create the invoice
            invoice = {
                'invoice_id': f'INV-{i:04d}',
                'vendor': random.choice(vendors),
                'invoice_number': f'{chr(65 + random.randint(0, 25))}{chr(65 + random.randint(0, 25))}-{random.randint(1000, 9999)}',
                'description': f'Invoice for {random.choice(["materials", "labor", "equipment", "services"])}',
                'amount': round(random.uniform(1000, 100000), 2),
                'tax': round(random.uniform(0, 5000), 2),
                'total_amount': 0,  # Will calculate below
                'invoice_date': invoice_date.strftime('%Y-%m-%d'),
                'due_date': due_date.strftime('%Y-%m-%d'),
                'payment_date': payment_date.strftime('%Y-%m-%d') if payment_date else None,
                'payment_method': random.choice(payment_methods) if status == "Paid" else None,
                'status': status,
                'notes': f'Notes for invoice {i}',
                'budget_item': f'B-{random.randint(1, 10):03d}',
                'cost_code': f'{random.randint(1, 10):02d}-{random.randint(1000, 9999)}',
                'approver': 'John Smith' if status in ["Approved", "Paid"] else None
            }
            
            # Calculate total amount
            invoice['total_amount'] = round(invoice['amount'] + invoice['tax'], 2)
            
            demo_items.append(invoice)
        
        # Save demo data
        self._save_items(demo_items)
    
    def _create_new_item_template(self):
        """Create a template for a new invoice with default values."""
        invoice_id = self._generate_new_id()
        
        today = datetime.now()
        due_date = today + timedelta(days=30)
        
        return {
            'invoice_id': f'INV-{int(invoice_id):04d}',
            'vendor': '',
            'invoice_number': '',
            'description': '',
            'amount': 0.00,
            'tax': 0.00,
            'total_amount': 0.00,
            'invoice_date': today.strftime('%Y-%m-%d'),
            'due_date': due_date.strftime('%Y-%m-%d'),
            'payment_date': None,
            'payment_method': None,
            'status': 'Draft',
            'notes': '',
            'budget_item': '',
            'cost_code': '',
            'approver': None
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for invoices."""
        items = self._get_items()
        
        # If no items exist yet, start with ID 1
        if not items:
            return "1"
        
        # Find the highest numerical ID and increment
        max_id = 0
        for item in items:
            invoice_id = item.get('invoice_id', '')
            if invoice_id.startswith('INV-'):
                try:
                    num = int(invoice_id.split('-')[1])
                    max_id = max(max_id, num)
                except:
                    pass
        
        return str(max_id + 1)
    
    def _get_status_class(self, status):
        """Get the status class for a given status value."""
        status_classes = {
            'Draft': 'secondary',
            'Submitted': 'info',
            'Approved': 'primary',
            'Paid': 'success',
            'Rejected': 'danger'
        }
        return status_classes.get(status, 'secondary')
    
    def render_detail_view(self):
        """Render the detail view for creating, viewing, or editing an invoice."""
        # Apply CRUD styles
        apply_crud_styles()
        
        base_key = self._get_state_key_prefix()
        
        # Get view mode
        is_new = st.session_state.get(f'{base_key}_view') == 'new'
        is_edit_mode = st.session_state.get(f'{base_key}_edit_mode', False)
        
        # Get item data
        if is_new:
            item = self._create_new_item_template()
            detail_title = "New Invoice"
        else:
            item_id = st.session_state.get(f'{base_key}_selected_id')
            item = self._get_item_by_id(item_id)
            if not item:
                st.error(f"Invoice with ID {item_id} not found")
                return
            detail_title = f"{item.get('invoice_id', 'Invoice')}"
        
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
                    st.warning("Are you sure you want to delete this invoice?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key=f"confirm_delete_{base_key}"):
                            self._delete_item(item['invoice_id'])
                            st.success("Invoice deleted successfully")
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
                        invoice_id = st.text_input("Invoice ID", value=item['invoice_id'], disabled=not is_new)
                    with col2:
                        vendor = st.text_input("Vendor", value=item['vendor'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        invoice_number = st.text_input("Invoice Number", value=item.get('invoice_number', ''))
                    with col2:
                        status = st.selectbox("Status", options=[
                            'Draft', 'Submitted', 'Approved', 'Paid', 'Rejected'
                        ], index=['Draft', 'Submitted', 'Approved', 'Paid', 'Rejected'].index(
                            item['status'] if item['status'] in ['Draft', 'Submitted', 'Approved', 'Paid', 'Rejected'] 
                            else 'Draft')
                        )
                    
                    description = st.text_area("Description", value=item.get('description', ''), height=80)
                
                render_crud_fieldset("Basic Information", render_basic_info)
                
                # Financial Section
                def render_financial():
                    col1, col2 = st.columns(2)
                    with col1:
                        amount = st.number_input("Amount ($)", 
                                               value=float(item['amount']) if item.get('amount') is not None else 0.0,
                                               min_value=0.0,
                                               step=100.0,
                                               format="%.2f")
                    with col2:
                        tax = st.number_input("Tax ($)", 
                                           value=float(item['tax']) if item.get('tax') is not None else 0.0,
                                           min_value=0.0,
                                           step=10.0,
                                           format="%.2f")
                    
                    # Calculate and display total
                    total_amount = amount + tax
                    st.markdown(f"**Total Amount:** ${total_amount:,.2f}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        budget_item = st.text_input("Budget Item", value=item.get('budget_item', ''))
                    with col2:
                        cost_code = st.text_input("Cost Code", value=item.get('cost_code', ''))
                
                render_crud_fieldset("Financial Information", render_financial)
                
                # Dates Section
                def render_dates():
                    col1, col2 = st.columns(2)
                    with col1:
                        invoice_date = st.date_input("Invoice Date", 
                            value=datetime.strptime(item['invoice_date'], '%Y-%m-%d') if item['invoice_date'] else datetime.now()
                        )
                    with col2:
                        due_date = st.date_input("Due Date", 
                            value=datetime.strptime(item['due_date'], '%Y-%m-%d') if item['due_date'] else (datetime.now() + timedelta(days=30))
                        )
                    
                    # Only show payment fields if status is Paid
                    if status == 'Paid':
                        col1, col2 = st.columns(2)
                        with col1:
                            payment_date = st.date_input("Payment Date", 
                                value=datetime.strptime(item['payment_date'], '%Y-%m-%d') if item.get('payment_date') else datetime.now()
                            )
                        with col2:
                            payment_method = st.selectbox("Payment Method", options=[
                                '', 'ACH', 'Check', 'Wire Transfer', 'Credit Card'
                            ], index=['', 'ACH', 'Check', 'Wire Transfer', 'Credit Card'].index(
                                item.get('payment_method', '') if item.get('payment_method') in ['', 'ACH', 'Check', 'Wire Transfer', 'Credit Card'] 
                                else '')
                            )
                    else:
                        payment_date = None
                        payment_method = None
                    
                    # Show approver field if status is Approved or Paid
                    if status in ['Approved', 'Paid']:
                        approver = st.text_input("Approver", value=item.get('approver', ''))
                    else:
                        approver = None
                    
                    notes = st.text_area("Notes", value=item.get('notes', ''), height=80)
                
                render_crud_fieldset("Dates & Approval", render_dates)
                
                # Form Actions
                form_actions = render_form_actions(
                    save_label="Save Invoice",
                    cancel_label="Cancel",
                    delete_label="Delete Invoice",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    # Update item with form values
                    updated_item = {
                        'invoice_id': invoice_id,
                        'vendor': vendor,
                        'invoice_number': invoice_number,
                        'description': description,
                        'amount': float(amount),
                        'tax': float(tax),
                        'total_amount': float(amount) + float(tax),
                        'invoice_date': invoice_date.strftime('%Y-%m-%d'),
                        'due_date': due_date.strftime('%Y-%m-%d'),
                        'payment_date': payment_date.strftime('%Y-%m-%d') if payment_date else None,
                        'payment_method': payment_method,
                        'status': status,
                        'notes': notes,
                        'budget_item': budget_item,
                        'cost_code': cost_code,
                        'approver': approver
                    }
                    
                    # Save the updated item
                    self._save_item(updated_item)
                    
                    # Show success message and return to list view
                    st.success("Invoice saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked'] and not is_new:
                    self._delete_item(item['invoice_id'])
                    st.success("Invoice deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view
            # Basic Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Basic Information")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Invoice ID:** {item['invoice_id']}")
            with col2:
                st.markdown(f"**Vendor:** {item['vendor']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Invoice Number:** {item.get('invoice_number', '')}")
            with col2:
                status_html = f"""
                <div style="display: flex; align-items: center; background: transparent;">
                    <span class='crud-status crud-status-{self._get_status_class(item['status'])}' style="outline: none; box-shadow: none; border: none;">{item['status']}</span>
                </div>
                """
                st.markdown("**Status:**")
                st.markdown(status_html, unsafe_allow_html=True)
            
            if item.get('description'):
                st.markdown(f"**Description:**")
                st.markdown(f"```{item.get('description', '')}```")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Financial Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Financial Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Amount:** ${float(item['amount']):,.2f}")
            with col2:
                st.markdown(f"**Tax:** ${float(item['tax']):,.2f}")
            with col3:
                st.markdown(f"**Total Amount:** ${float(item['total_amount']):,.2f}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Budget Item:** {item.get('budget_item', '')}")
            with col2:
                st.markdown(f"**Cost Code:** {item.get('cost_code', '')}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Dates Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Dates & Approval")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Invoice Date:** {item['invoice_date']}")
            with col2:
                st.markdown(f"**Due Date:** {item['due_date']}")
            
            if item['status'] == 'Paid':
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Payment Date:** {item.get('payment_date', 'Not paid')}")
                with col2:
                    st.markdown(f"**Payment Method:** {item.get('payment_method', '')}")
            
            if item['status'] in ['Approved', 'Paid']:
                st.markdown(f"**Approver:** {item.get('approver', '')}")
            
            if item.get('notes'):
                st.markdown(f"**Notes:**")
                st.markdown(f"```{item.get('notes', '')}```")
            st.markdown("</div>", unsafe_allow_html=True)
        
        end_crud_detail_container()


# Import the AIA Billing functionality
from modules.cost_management.aia_billing import AIABillingModule

def render():
    """Render the Cost Management module."""
    st.title("Cost Management")
    
    # Create tabs for different cost management sections
    tab1, tab2, tab3, tab4 = st.tabs(["Budget Overview", "Budget Items", "Invoices", "AIA G702/G703 Billing"])
    
    # Budget Overview Tab
    with tab1:
        budget_module = BudgetItemModule()
        budget_module.render_budget_summary()
    
    # Budget Items Tab
    with tab2:
        budget_items = BudgetItemModule()
        budget_items.render()
    
    # Invoices Tab
    with tab3:
        invoices = InvoiceModule()
        invoices.render()
    
    # AIA G702/G703 Billing Tab
    with tab4:
        aia_billing = AIABillingModule()
        aia_billing.render()