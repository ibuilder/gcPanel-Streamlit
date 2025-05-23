"""
Contracts Module for gcPanel

This module provides contract management functionality for the construction management dashboard.
Features include:
- Owner/Prime Contract management 
- Subcontract management
- Contract document tracking
- Digital signatures integration
- Status tracking and filtering
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

# Define subclasses for each contract type
class OwnerContractModule(CrudModule):
    def __init__(self):
        """Initialize the Owner Contracts module with configuration."""
        super().__init__(
            module_name="Owner Contracts",
            data_file_path="data/contracts/owner_contracts.json",
            id_field="contract_id",
            list_columns=["contract_id", "title", "type", "value", "execution_date", "status"],
            default_sort_field="contract_id",
            default_sort_direction="asc",
            status_field="status",
            filter_options=["Draft", "Issued", "Executed", "Active", "Complete", "Terminated"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        contract_types = ['GMP', 'Cost Plus', 'Lump Sum', 'CMAR', 'Design-Build']
        statuses = ['Draft', 'Issued', 'Executed', 'Active', 'Complete', 'Terminated']
        
        demo_items = []
        
        # Create the main owner contract for Highland Tower
        main_contract = {
            'contract_id': 'OC-001',
            'title': 'Highland Tower Development',
            'type': 'GMP',
            'owner_name': 'Highland Properties LLC',
            'contractor_name': 'GC Construction, Inc.',
            'value': 45500000.00,
            'execution_date': '2025-01-15',
            'commencement_date': '2025-02-01',
            'substantial_completion_date': '2027-04-30',
            'final_completion_date': '2027-06-30',
            'retainage_percentage': 5.0,
            'status': 'Active',
            'description': 'Construction of 15-story mixed-use building with 120 residential units and 8 retail spaces.',
            'signatures': [],
            'documents': [
                {'name': 'Owner Contract.pdf', 'date_uploaded': '2025-01-10', 'size': '2.4 MB'},
                {'name': 'Exhibit A - Scope of Work.pdf', 'date_uploaded': '2025-01-10', 'size': '1.1 MB'},
                {'name': 'Exhibit B - Schedule of Values.pdf', 'date_uploaded': '2025-01-10', 'size': '0.8 MB'}
            ]
        }
        demo_items.append(main_contract)
        
        # Create a few more sample owner contracts
        for i in range(2, 5):
            execution_date = datetime.now() - timedelta(days=random.randint(30, 180))
            commencement_date = execution_date + timedelta(days=random.randint(14, 30))
            substantial_completion = commencement_date + timedelta(days=random.randint(300, 700))
            final_completion = substantial_completion + timedelta(days=random.randint(30, 90))
            
            contract = {
                'contract_id': f'OC-{i:03d}',
                'title': f'Sample Project {i}',
                'type': random.choice(contract_types),
                'owner_name': f'Owner Company {i}',
                'contractor_name': 'GC Construction, Inc.',
                'value': round(random.uniform(5000000, 75000000), 2),
                'execution_date': execution_date.strftime('%Y-%m-%d'),
                'commencement_date': commencement_date.strftime('%Y-%m-%d'),
                'substantial_completion_date': substantial_completion.strftime('%Y-%m-%d'),
                'final_completion_date': final_completion.strftime('%Y-%m-%d'),
                'retainage_percentage': random.choice([5.0, 7.5, 10.0]),
                'status': random.choice(statuses),
                'description': f'Sample construction project {i} with general description.',
                'signatures': [],
                'documents': []
            }
            demo_items.append(contract)
        
        # Save demo data
        self._save_items(demo_items)
    
    def _create_new_item_template(self):
        """Create a template for a new owner contract with default values."""
        contract_id = self._generate_new_id()
        execution_date = datetime.now()
        commencement_date = execution_date + timedelta(days=15)
        substantial_completion_date = commencement_date + timedelta(days=365*2)
        final_completion_date = substantial_completion_date + timedelta(days=60)
        
        return {
            'contract_id': f'OC-{int(contract_id):03d}',
            'title': '',
            'type': 'GMP',
            'owner_name': '',
            'contractor_name': 'GC Construction, Inc.',
            'value': 0.00,
            'execution_date': execution_date.strftime('%Y-%m-%d'),
            'commencement_date': commencement_date.strftime('%Y-%m-%d'),
            'substantial_completion_date': substantial_completion_date.strftime('%Y-%m-%d'),
            'final_completion_date': final_completion_date.strftime('%Y-%m-%d'),
            'retainage_percentage': 5.0,
            'status': 'Draft',
            'description': '',
            'signatures': [],
            'documents': []
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for owner contracts."""
        items = self._get_items()
        
        # If no items exist yet, start with ID 1
        if not items:
            return "1"
        
        # Find the highest numerical ID and increment
        max_id = 0
        for item in items:
            contract_id = item.get('contract_id', '')
            if contract_id.startswith('OC-'):
                try:
                    num = int(contract_id.split('-')[1])
                    max_id = max(max_id, num)
                except:
                    pass
        
        return str(max_id + 1)
    
    def _get_status_class(self, status):
        """Get the status class for a given status value."""
        status_classes = {
            'Draft': 'secondary',
            'Issued': 'info',
            'Executed': 'primary',
            'Active': 'success',
            'Complete': 'success',
            'Terminated': 'danger'
        }
        return status_classes.get(status, 'secondary')
    
    def render_detail_view(self):
        """Render the detail view for creating, viewing, or editing an owner contract."""
        # Apply CRUD styles
        apply_crud_styles()
        
        base_key = self._get_state_key_prefix()
        
        # Get view mode
        is_new = st.session_state.get(f'{base_key}_view') == 'new'
        is_edit_mode = st.session_state.get(f'{base_key}_edit_mode', False)
        
        # Get item data
        if is_new:
            item = self._create_new_item_template()
            detail_title = "New Owner Contract"
        else:
            item_id = st.session_state.get(f'{base_key}_selected_id')
            item = self._get_item_by_id(item_id)
            if not item:
                st.error(f"Contract with ID {item_id} not found")
                return
            detail_title = f"{item.get('title', item.get('contract_id', 'Contract'))}"
        
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
                if st.button("✏️ Edit", type="primary"):
                    st.session_state[f'{base_key}_edit_mode'] = True
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", type="secondary"):
                    st.warning("Are you sure you want to delete this contract?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key="confirm_delete"):
                            self._delete_item(item['contract_id'])
                            st.success("Contract deleted successfully")
                            st.session_state[f'{base_key}_view'] = 'list'
                            st.rerun()
                    with confirm_col2:
                        if st.button("Cancel", key="cancel_delete"):
                            st.rerun()
        
        # Create form for editing or read-only view for viewing
        if is_edit_mode or is_new:
            with st.form("owner_contract_form"):
                # Basic Information Section
                def render_basic_info():
                    col1, col2 = st.columns(2)
                    with col1:
                        contract_id = st.text_input("Contract ID", value=item['contract_id'], disabled=not is_new)
                    with col2:
                        title = st.text_input("Title", value=item['title'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        contract_type = st.selectbox("Contract Type", options=[
                            'GMP', 'Cost Plus', 'Lump Sum', 'CMAR', 'Design-Build'
                        ], index=['GMP', 'Cost Plus', 'Lump Sum', 'CMAR', 'Design-Build'].index(
                            item['type'] if item['type'] in ['GMP', 'Cost Plus', 'Lump Sum', 'CMAR', 'Design-Build'] 
                            else 'GMP')
                        )
                    with col2:
                        status = st.selectbox("Status", options=[
                            'Draft', 'Issued', 'Executed', 'Active', 'Complete', 'Terminated'
                        ], index=['Draft', 'Issued', 'Executed', 'Active', 'Complete', 'Terminated'].index(
                            item['status'] if item['status'] in ['Draft', 'Issued', 'Executed', 'Active', 'Complete', 'Terminated'] 
                            else 'Draft')
                        )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        owner_name = st.text_input("Owner Name", value=item['owner_name'])
                    with col2:
                        contractor_name = st.text_input("Contractor Name", value=item['contractor_name'])
                    
                    value = st.number_input("Contract Value ($)", 
                                          value=float(item['value']) if item.get('value') is not None else 0.0,
                                          min_value=0.0, 
                                          step=10000.0,
                                          format="%.2f")
                    
                    description = st.text_area("Description", value=item['description'], height=100)
                
                render_crud_fieldset("Basic Information", render_basic_info)
                
                # Dates Section
                def render_dates():
                    col1, col2 = st.columns(2)
                    with col1:
                        execution_date = st.date_input("Execution Date", 
                            value=datetime.strptime(item['execution_date'], '%Y-%m-%d') if item['execution_date'] else datetime.now()
                        )
                    with col2:
                        commencement_date = st.date_input("Commencement Date", 
                            value=datetime.strptime(item['commencement_date'], '%Y-%m-%d') if item['commencement_date'] else (datetime.now() + timedelta(days=15))
                        )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        substantial_completion_date = st.date_input("Substantial Completion Date", 
                            value=datetime.strptime(item['substantial_completion_date'], '%Y-%m-%d') if item['substantial_completion_date'] else (datetime.now() + timedelta(days=365*2))
                        )
                    with col2:
                        final_completion_date = st.date_input("Final Completion Date", 
                            value=datetime.strptime(item['final_completion_date'], '%Y-%m-%d') if item['final_completion_date'] else (datetime.now() + timedelta(days=365*2+60))
                        )
                    
                    retainage_percentage = st.slider("Retainage Percentage", 
                                                   min_value=0.0, 
                                                   max_value=10.0, 
                                                   value=float(item['retainage_percentage']) if item.get('retainage_percentage') is not None else 5.0,
                                                   step=0.5,
                                                   format="%.1f%%")
                
                render_crud_fieldset("Contract Dates", render_dates)
                
                # Documents Section
                def render_documents():
                    st.write("Contract Documents")
                    
                    if not is_new and len(item.get('documents', [])) > 0:
                        for i, doc in enumerate(item.get('documents', [])):
                            doc_col1, doc_col2, doc_col3, doc_col4 = st.columns([3, 2, 1, 1])
                            with doc_col1:
                                st.write(doc.get('name', 'Document'))
                            with doc_col2:
                                st.write(doc.get('date_uploaded', ''))
                            with doc_col3:
                                st.write(doc.get('size', ''))
                            with doc_col4:
                                st.button("🔽", key=f"download_doc_{i}")
                    else:
                        st.write("No documents uploaded yet.")
                    
                    # In a real implementation, we'd add document upload functionality here
                    if st.button("➕ Add Document", key="add_document_btn"):
                        st.info("Document upload functionality would be implemented here in a production version.")
                
                render_crud_fieldset("Documents", render_documents)
                
                # Form Actions
                form_actions = render_form_actions(
                    save_label="Save Contract",
                    cancel_label="Cancel",
                    delete_label="Delete Contract",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    # Update item with form values
                    updated_item = {
                        'contract_id': contract_id,
                        'title': title,
                        'type': contract_type,
                        'owner_name': owner_name,
                        'contractor_name': contractor_name,
                        'value': float(value),
                        'execution_date': execution_date.strftime('%Y-%m-%d'),
                        'commencement_date': commencement_date.strftime('%Y-%m-%d'),
                        'substantial_completion_date': substantial_completion_date.strftime('%Y-%m-%d'),
                        'final_completion_date': final_completion_date.strftime('%Y-%m-%d'),
                        'retainage_percentage': float(retainage_percentage),
                        'status': status,
                        'description': description,
                        'signatures': item.get('signatures', []),
                        'documents': item.get('documents', [])
                    }
                    
                    # Save the updated item
                    self._save_item(updated_item)
                    
                    # Show success message and return to list view
                    st.success("Contract saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked'] and not is_new:
                    self._delete_item(item['contract_id'])
                    st.success("Contract deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view
            # Basic Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Basic Information")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Contract ID:** {item['contract_id']}")
            with col2:
                st.markdown(f"**Title:** {item['title']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Contract Type:** {item['type']}")
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
                st.markdown(f"**Owner Name:** {item['owner_name']}")
            with col2:
                st.markdown(f"**Contractor Name:** {item['contractor_name']}")
            
            st.markdown(f"**Contract Value:** ${float(item['value']):,.2f}")
            
            if item.get('description'):
                st.markdown(f"**Description:**")
                st.markdown(f"```{item['description']}```")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Dates Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Contract Dates")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Execution Date:** {item['execution_date']}")
            with col2:
                st.markdown(f"**Commencement Date:** {item['commencement_date']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Substantial Completion Date:** {item['substantial_completion_date']}")
            with col2:
                st.markdown(f"**Final Completion Date:** {item.get('final_completion_date', 'Not set')}")
            
            st.markdown(f"**Retainage Percentage:** {float(item['retainage_percentage']):,.1f}%")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Documents Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Documents")
            
            if len(item.get('documents', [])) > 0:
                for doc in item.get('documents', []):
                    col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                    with col1:
                        st.markdown(f"**{doc.get('name', 'Document')}**")
                    with col2:
                        st.markdown(f"Upload date: {doc.get('date_uploaded', '')}")
                    with col3:
                        st.markdown(f"Size: {doc.get('size', '')}")
                    with col4:
                        st.button("Download", key=f"download_{doc.get('name', '').replace(' ', '_')}")
            else:
                st.markdown("No documents have been uploaded for this contract.")
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


class SubcontractModule(CrudModule):
    def __init__(self):
        """Initialize the Subcontracts module with configuration."""
        super().__init__(
            module_name="Subcontracts",
            data_file_path="data/contracts/subcontracts.json",
            id_field="id",
            list_columns=["id", "company", "scope", "amount", "date", "status"],
            default_sort_field="id",
            default_sort_direction="asc",
            status_field="status",
            filter_options=["Draft", "Issued", "Executed", "In Progress", "Complete", "Terminated"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        trades = ['Concrete', 'Steel', 'Carpentry', 'Electrical', 'Plumbing', 'HVAC', 'Masonry', 'Roofing', 'Windows', 'Finishes']
        statuses = ['Draft', 'Issued', 'Executed', 'In Progress', 'Complete', 'Terminated']
        
        demo_items = []
        
        # Create several sample subcontracts for Highland Tower
        for i in range(1, 11):
            execution_date = datetime.now() - timedelta(days=random.randint(30, 180))
            
            item = {
                'subcontract_id': f'SC-{i:03d}',
                'subcontractor_name': f'{trades[i-1]} Specialists, Inc.',
                'trade': trades[i-1],
                'value': round(random.uniform(500000, 3000000), 2),
                'execution_date': execution_date.strftime('%Y-%m-%d'),
                'status': random.choice(statuses),
                'scope': f'All {trades[i-1].lower()} work for the Highland Tower project according to plans and specifications.',
                'start_date': (execution_date + timedelta(days=random.randint(7, 30))).strftime('%Y-%m-%d'),
                'completion_date': (execution_date + timedelta(days=random.randint(100, 500))).strftime('%Y-%m-%d'),
                'project': 'Highland Tower',
                'insurance_status': random.choice(['Compliant', 'Pending', 'Expired']),
                'contact_name': f'John {trades[i-1]}',
                'contact_email': f'john@{trades[i-1].lower()}specialists.com',
                'contact_phone': f'(555) {random.randint(100, 999)}-{random.randint(1000, 9999)}',
                'signatures': [],
                'documents': []
            }
            demo_items.append(item)
        
        # Save demo data
        self._save_items(demo_items)
    
    def _create_new_item_template(self):
        """Create a template for a new subcontract with default values."""
        subcontract_id = self._generate_new_id()
        execution_date = datetime.now()
        
        return {
            'subcontract_id': f'SC-{int(subcontract_id):03d}',
            'subcontractor_name': '',
            'trade': '',
            'value': 0.00,
            'execution_date': execution_date.strftime('%Y-%m-%d'),
            'status': 'Draft',
            'scope': '',
            'start_date': execution_date.strftime('%Y-%m-%d'),
            'completion_date': (execution_date + timedelta(days=180)).strftime('%Y-%m-%d'),
            'project': 'Highland Tower',
            'insurance_status': 'Pending',
            'contact_name': '',
            'contact_email': '',
            'contact_phone': '',
            'signatures': [],
            'documents': []
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for subcontracts."""
        items = self._get_items()
        
        # If no items exist yet, start with ID 1
        if not items:
            return "1"
        
        # Find the highest numerical ID and increment
        max_id = 0
        for item in items:
            subcontract_id = item.get('subcontract_id', '')
            if subcontract_id.startswith('SC-'):
                try:
                    num = int(subcontract_id.split('-')[1])
                    max_id = max(max_id, num)
                except:
                    pass
        
        return str(max_id + 1)
    
    def _get_status_class(self, status):
        """Get the status class for a given status value."""
        status_classes = {
            'Draft': 'secondary',
            'Issued': 'info',
            'Executed': 'primary',
            'In Progress': 'success',
            'Complete': 'success',
            'Terminated': 'danger'
        }
        return status_classes.get(status, 'secondary')
    
    def render_detail_view(self):
        """Render the detail view for creating, viewing, or editing a subcontract."""
        # Apply CRUD styles
        apply_crud_styles()
        
        base_key = self._get_state_key_prefix()
        
        # Get view mode
        is_new = st.session_state.get(f'{base_key}_view') == 'new'
        is_edit_mode = st.session_state.get(f'{base_key}_edit_mode', False)
        
        # Get item data
        if is_new:
            item = self._create_new_item_template()
            detail_title = "New Subcontract"
        else:
            item_id = st.session_state.get(f'{base_key}_selected_id')
            item = self._get_item_by_id(item_id)
            if not item:
                st.error(f"Subcontract with ID {item_id} not found")
                return
            detail_title = f"{item.get('subcontractor_name', item.get('subcontract_id', 'Subcontract'))}"
        
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
                if st.button("✏️ Edit", type="primary"):
                    st.session_state[f'{base_key}_edit_mode'] = True
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", type="secondary"):
                    st.warning("Are you sure you want to delete this subcontract?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key="confirm_delete"):
                            self._delete_item(item['subcontract_id'])
                            st.success("Subcontract deleted successfully")
                            st.session_state[f'{base_key}_view'] = 'list'
                            st.rerun()
                    with confirm_col2:
                        if st.button("Cancel", key="cancel_delete"):
                            st.rerun()
        
        # Create form for editing or read-only view for viewing
        if is_edit_mode or is_new:
            with st.form("subcontract_form"):
                # Basic Information Section
                def render_basic_info():
                    col1, col2 = st.columns(2)
                    with col1:
                        subcontract_id = st.text_input("Subcontract ID", value=item['subcontract_id'], disabled=not is_new)
                    with col2:
                        subcontractor_name = st.text_input("Subcontractor Name", value=item['subcontractor_name'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        trade = st.selectbox("Trade", options=[
                            '', 'Concrete', 'Steel', 'Carpentry', 'Electrical', 'Plumbing', 
                            'HVAC', 'Masonry', 'Roofing', 'Windows', 'Finishes', 'Other'
                        ], index=['', 'Concrete', 'Steel', 'Carpentry', 'Electrical', 'Plumbing', 
                               'HVAC', 'Masonry', 'Roofing', 'Windows', 'Finishes', 'Other'].index(
                            item['trade'] if item['trade'] in ['', 'Concrete', 'Steel', 'Carpentry', 'Electrical', 'Plumbing', 
                                                            'HVAC', 'Masonry', 'Roofing', 'Windows', 'Finishes', 'Other'] 
                            else '')
                        )
                    with col2:
                        status = st.selectbox("Status", options=[
                            'Draft', 'Issued', 'Executed', 'In Progress', 'Complete', 'Terminated'
                        ], index=['Draft', 'Issued', 'Executed', 'In Progress', 'Complete', 'Terminated'].index(
                            item['status'] if item['status'] in ['Draft', 'Issued', 'Executed', 'In Progress', 'Complete', 'Terminated'] 
                            else 'Draft')
                        )
                    
                    value = st.number_input("Subcontract Value ($)", 
                                          value=float(item['value']) if item.get('value') is not None else 0.0,
                                          min_value=0.0, 
                                          step=10000.0,
                                          format="%.2f")
                    
                    project = st.text_input("Project", value=item['project'])
                    
                    scope = st.text_area("Scope of Work", value=item['scope'], height=100)
                
                render_crud_fieldset("Basic Information", render_basic_info)
                
                # Dates Section
                def render_dates():
                    col1, col2 = st.columns(2)
                    with col1:
                        execution_date = st.date_input("Execution Date", 
                            value=datetime.strptime(item['execution_date'], '%Y-%m-%d') if item['execution_date'] else datetime.now()
                        )
                    with col2:
                        start_date = st.date_input("Start Date", 
                            value=datetime.strptime(item['start_date'], '%Y-%m-%d') if item.get('start_date') else datetime.now()
                        )
                    
                    completion_date = st.date_input("Completion Date", 
                        value=datetime.strptime(item['completion_date'], '%Y-%m-%d') if item.get('completion_date') else (datetime.now() + timedelta(days=180))
                    )
                    
                    insurance_status = st.selectbox("Insurance Status", options=[
                        'Pending', 'Compliant', 'Expired', 'Non-Compliant'
                    ], index=['Pending', 'Compliant', 'Expired', 'Non-Compliant'].index(
                        item['insurance_status'] if item.get('insurance_status') in ['Pending', 'Compliant', 'Expired', 'Non-Compliant'] 
                        else 'Pending')
                    )
                
                render_crud_fieldset("Dates & Compliance", render_dates)
                
                # Contact Information Section
                def render_contact():
                    col1, col2 = st.columns(2)
                    with col1:
                        contact_name = st.text_input("Contact Name", value=item.get('contact_name', ''))
                    with col2:
                        contact_email = st.text_input("Contact Email", value=item.get('contact_email', ''))
                    
                    contact_phone = st.text_input("Contact Phone", value=item.get('contact_phone', ''))
                
                render_crud_fieldset("Contact Information", render_contact)
                
                # Form Actions
                form_actions = render_form_actions(
                    save_label="Save Subcontract",
                    cancel_label="Cancel",
                    delete_label="Delete Subcontract",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    # Update item with form values
                    updated_item = {
                        'subcontract_id': subcontract_id,
                        'subcontractor_name': subcontractor_name,
                        'trade': trade,
                        'value': float(value),
                        'execution_date': execution_date.strftime('%Y-%m-%d'),
                        'status': status,
                        'scope': scope,
                        'start_date': start_date.strftime('%Y-%m-%d'),
                        'completion_date': completion_date.strftime('%Y-%m-%d'),
                        'project': project,
                        'insurance_status': insurance_status,
                        'contact_name': contact_name,
                        'contact_email': contact_email,
                        'contact_phone': contact_phone,
                        'signatures': item.get('signatures', []),
                        'documents': item.get('documents', [])
                    }
                    
                    # Save the updated item
                    self._save_item(updated_item)
                    
                    # Show success message and return to list view
                    st.success("Subcontract saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked'] and not is_new:
                    self._delete_item(item['subcontract_id'])
                    st.success("Subcontract deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view
            # Basic Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Basic Information")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Subcontract ID:** {item['subcontract_id']}")
            with col2:
                st.markdown(f"**Subcontractor Name:** {item['subcontractor_name']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Trade:** {item['trade']}")
            with col2:
                status_html = f"""
                <div style="display: flex; align-items: center; background: transparent;">
                    <span class='crud-status crud-status-{self._get_status_class(item['status'])}' style="outline: none; box-shadow: none; border: none;">{item['status']}</span>
                </div>
                """
                st.markdown("**Status:**")
                st.markdown(status_html, unsafe_allow_html=True)
            
            st.markdown(f"**Subcontract Value:** ${float(item['value']):,.2f}")
            st.markdown(f"**Project:** {item['project']}")
            
            if item.get('scope'):
                st.markdown(f"**Scope of Work:**")
                st.markdown(f"```{item['scope']}```")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Dates Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Dates & Compliance")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Execution Date:** {item['execution_date']}")
            with col2:
                st.markdown(f"**Start Date:** {item.get('start_date', 'Not set')}")
            
            st.markdown(f"**Completion Date:** {item.get('completion_date', 'Not set')}")
            
            insurance_status = item.get('insurance_status', 'Unknown')
            insurance_class = 'success' if insurance_status == 'Compliant' else 'warning' if insurance_status == 'Pending' else 'danger'
            insurance_html = f"""
            <div style="display: flex; align-items: center; background: transparent;">
                <span class='crud-status crud-status-{insurance_class}' style="outline: none; box-shadow: none; border: none;">{insurance_status}</span>
            </div>
            """
            st.markdown("**Insurance Status:**")
            st.markdown(insurance_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Contact Information Section
            if item.get('contact_name') or item.get('contact_email') or item.get('contact_phone'):
                st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
                st.subheader("Contact Information")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Contact Name:** {item.get('contact_name', 'Not provided')}")
                with col2:
                    st.markdown(f"**Contact Email:** {item.get('contact_email', 'Not provided')}")
                
                st.markdown(f"**Contact Phone:** {item.get('contact_phone', 'Not provided')}")
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


# Import Change Orders functionality
from modules.contracts.change_orders import ChangeOrderModule

def render_contract_analytics():
    """Render contract analytics and performance dashboard"""
    st.markdown("### 📊 Contract Performance Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Contract Values**")
        st.metric("Total Contract Value", "$45.5M", "Highland Tower")
        st.metric("Executed to Date", "$32.8M", "72% complete")
        st.metric("Remaining Value", "$12.7M", "28% remaining")
    
    with col2:
        st.markdown("**Contract Compliance**")
        st.metric("Change Orders", "8", "+2 this month")
        st.metric("Avg Processing Time", "5.2 days", "-1.3 vs target")
        st.metric("Signature Compliance", "96%", "+4% this quarter")
    
    with col3:
        st.markdown("**Financial Health**")
        st.metric("Payment Applications", "12", "All current")
        st.metric("Retainage Held", "$1.64M", "5% of completed work")
        st.metric("Outstanding Invoices", "$287K", "Within terms")

def render_digital_contract_workflow():
    """Render digital contract workflow with e-signatures"""
    st.markdown("### ✍️ Digital Contract Workflow")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Pending Signatures**")
        pending_contracts = [
            {"id": "CO-015", "title": "HVAC Change Order", "type": "Change Order", "value": "$45K", "days": 3},
            {"id": "SC-089", "title": "Electrical Subcontract", "type": "Subcontract", "value": "$2.1M", "days": 1},
            {"id": "CO-016", "title": "Foundation Revision", "type": "Change Order", "value": "$78K", "days": 5}
        ]
        
        for contract in pending_contracts:
            urgency_color = "#ff4444" if contract["days"] >= 5 else "#ff8800" if contract["days"] >= 3 else "#4CAF50"
            st.markdown(f"""
                <div style="border-left: 4px solid {urgency_color}; padding: 10px; margin: 5px 0; background-color: #f8f9fa;">
                    <strong>📝 {contract["id"]}: {contract["title"]}</strong><br>
                    <small>Type: {contract["type"]} | Value: {contract["value"]} | Pending: {contract["days"]} days</small>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Signature Status**")
        st.markdown("✅ **Owner**: Highland Properties LLC")
        st.markdown("⏳ **General Contractor**: Pending review")
        st.markdown("🔄 **Architect**: In progress")
        st.markdown("📧 **Legal**: Awaiting DocuSign")
        
        if st.button("📧 Send Reminder", type="primary"):
            st.success("Signature reminders sent to all pending parties!")

def render_contract_risk_assessment():
    """Render contract risk assessment and compliance monitoring"""
    st.markdown("### ⚖️ Contract Risk Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Risk Indicators**")
        risks = [
            {"category": "Payment Terms", "risk": "Low", "score": 2.1, "status": "Monitored"},
            {"category": "Change Order Volume", "risk": "Medium", "score": 6.8, "status": "Review Required"},
            {"category": "Schedule Delays", "risk": "Low", "score": 3.2, "status": "Monitored"},
            {"category": "Scope Creep", "risk": "Medium", "score": 5.9, "status": "Active Management"}
        ]
        
        for risk in risks:
            risk_color = "#4CAF50" if risk["risk"] == "Low" else "#ff8800" if risk["risk"] == "Medium" else "#ff4444"
            st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; border-radius: 5px;">
                    <strong>{risk["category"]}</strong><br>
                    <span style="color: {risk_color};">Risk: {risk["risk"]} ({risk["score"]}/10)</span><br>
                    <small>Status: {risk["status"]}</small>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Compliance Monitoring**")
        st.success("✅ Insurance certificates current")
        st.success("✅ Bond documentation complete")
        st.warning("⚠️ Safety training expires in 15 days")
        st.info("📋 Annual contract review due next month")

def render():
    """Render the Enhanced Contracts Management module."""
    st.title("📄 Enhanced Contract Management")
    
    # Contract Analytics Dashboard
    render_contract_analytics()
    
    # Digital Contract Workflow
    render_digital_contract_workflow()
    
    # Contract Risk Assessment
    render_contract_risk_assessment()
    
    # Create tabs for different contract types
    tab1, tab2, tab3 = st.tabs(["Owner Contracts", "Subcontracts", "Change Orders"])
    
    # Owner Contracts Tab
    with tab1:
        owner_contracts = OwnerContractModule()
        owner_contracts.render()
    
    # Subcontracts Tab
    with tab2:
        # Initialize Subcontracts module
        subcontracts = SubcontractModule()
        
        # Make sure demo data exists
        if not os.path.exists(subcontracts.data_file_path) or len(subcontracts._get_items()) == 0:
            subcontracts._initialize_demo_data()
            
        subcontracts.render()
    
    # Change Orders Tab
    with tab3:
        change_orders = ChangeOrderModule()
        change_orders.render()