"""
Equipment Management Module for gcPanel

This module manages construction equipment inventory using the standardized CRUD template.
"""

import streamlit as st
from datetime import datetime, timedelta
import random
import os

from modules.crud_template import CrudModule
from assets.crud_styler import render_form_actions, render_crud_fieldset, apply_crud_styles

# Define the Equipment Management CRUD module
class EquipmentModule(CrudModule):
    def __init__(self):
        """Initialize the Equipment Management module with configuration."""
        super().__init__(
            module_name="Equipment",
            data_file_path="data/equipment/inventory.json",
            id_field="equipment_id",
            list_columns=["equipment_id", "name", "category", "status", "location", "last_maintenance", "next_maintenance"],
            default_sort_field="equipment_id",
            default_sort_direction="asc",
            status_field="status",
            filter_options=["Active", "In Use", "Under Maintenance", "Out of Service", "Retired"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        statuses = ['Active', 'In Use', 'Under Maintenance', 'Out of Service', 'Retired']
        categories = ['Heavy Equipment', 'Power Tools', 'Vehicles', 'Scaffolding', 'Electrical Equipment', 'Safety Equipment']
        locations = ['Main Storage', 'Northeast Site', 'South Building', 'Tool Shed', 'Equipment Yard', 'Warehouse B']
        manufacturers = ['Caterpillar', 'John Deere', 'Volvo Construction', 'Komatsu', 'Hitachi', 'Bobcat', 'JCB']
        
        demo_items = []
        for i in range(1, 16):
            purchase_date = datetime.now() - timedelta(days=random.randint(30, 1825))  # 1 month to 5 years ago
            last_maintenance = datetime.now() - timedelta(days=random.randint(1, 180))  # up to 6 months ago
            next_maintenance = last_maintenance + timedelta(days=random.randint(90, 365))  # 3 months to 1 year after last
            
            item = {
                'equipment_id': f'EQ-{i:04d}',
                'name': f'{"".join(random.choice(categories).split()[:1])} {random.choice(["XL", "Pro", "Max", "Ultra", "Heavy", "Light"])} {random.randint(100, 999)}',
                'category': random.choice(categories),
                'description': f'This is a {random.choice(["heavy-duty", "standard", "specialized", "high-performance"])} piece of equipment used for construction operations.',
                'status': random.choice(statuses),
                'location': random.choice(locations),
                'manufacturer': random.choice(manufacturers),
                'model': f'Model {random.choice(["A", "B", "C", "X", "Z"])}{random.randint(10, 99)}',
                'serial_number': f'SN-{random.randint(10000, 99999)}',
                'purchase_date': purchase_date.strftime('%Y-%m-%d'),
                'purchase_cost': round(random.uniform(1000, 150000), 2),
                'last_maintenance': last_maintenance.strftime('%Y-%m-%d'),
                'next_maintenance': next_maintenance.strftime('%Y-%m-%d'),
                'maintenance_history': [],
                'assigned_to': '',
                'notes': ''
            }
            demo_items.append(item)
        
        # Save demo data
        self._save_items(demo_items)
    
    def _create_new_item_template(self):
        """Create a template for a new equipment item with default values."""
        equipment_id = self._generate_new_id()
        return {
            'equipment_id': f'EQ-{int(equipment_id):04d}',
            'name': '',
            'category': 'Heavy Equipment',
            'description': '',
            'status': 'Active',
            'location': '',
            'manufacturer': '',
            'model': '',
            'serial_number': '',
            'purchase_date': datetime.now().strftime('%Y-%m-%d'),
            'purchase_cost': 0.0,
            'last_maintenance': datetime.now().strftime('%Y-%m-%d'),
            'next_maintenance': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
            'maintenance_history': [],
            'assigned_to': '',
            'notes': ''
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for equipment."""
        items = self._get_items()
        
        # If no items exist yet, start with ID 1
        if not items:
            return "1"
        
        # Find the highest numerical ID and increment
        max_id = 0
        for item in items:
            equipment_id = item.get('equipment_id', '')
            if equipment_id.startswith('EQ-'):
                try:
                    num = int(equipment_id.split('-')[1])
                    max_id = max(max_id, num)
                except:
                    pass
        
        return str(max_id + 1)
    
    def render_detail_view(self):
        """Render the detail view for creating, viewing, or editing equipment."""
        # Apply CRUD styles
        apply_crud_styles()
        
        base_key = self._get_state_key_prefix()
        
        # Get view mode
        is_new = st.session_state.get(f'{base_key}_view') == 'new'
        is_edit_mode = st.session_state.get(f'{base_key}_edit_mode', False)
        
        # Get item data
        if is_new:
            item = self._create_new_item_template()
            detail_title = "New Equipment"
        else:
            item_id = st.session_state.get(f'{base_key}_selected_id')
            item = self._get_item_by_id(item_id)
            if not item:
                st.error(f"Equipment with ID {item_id} not found")
                return
            detail_title = f"{item.get('name', item.get('equipment_id', 'Equipment'))}"
        
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
                    st.warning("Are you sure you want to delete this equipment?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key="confirm_delete"):
                            self._delete_item(item['equipment_id'])
                            st.success("Equipment deleted successfully")
                            st.session_state[f'{base_key}_view'] = 'list'
                            st.rerun()
                    with confirm_col2:
                        if st.button("Cancel", key="cancel_delete"):
                            st.rerun()
        
        # Create form for editing or read-only view for viewing
        if is_edit_mode or is_new:
            with st.form("equipment_form"):
                # Basic Information Section
                def render_basic_info():
                    col1, col2 = st.columns(2)
                    with col1:
                        equipment_id = st.text_input("Equipment ID", value=item['equipment_id'], disabled=not is_new)
                    with col2:
                        name = st.text_input("Name", value=item['name'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        category = st.selectbox("Category", options=[
                            'Heavy Equipment', 'Power Tools', 'Vehicles', 'Scaffolding', 
                            'Electrical Equipment', 'Safety Equipment', 'Other'
                        ], index=['Heavy Equipment', 'Power Tools', 'Vehicles', 'Scaffolding', 
                                'Electrical Equipment', 'Safety Equipment', 'Other'].index(
                                    item['category'] if item['category'] in ['Heavy Equipment', 'Power Tools', 'Vehicles', 
                                                                            'Scaffolding', 'Electrical Equipment', 'Safety Equipment', 'Other'] 
                                    else 'Other')
                        )
                    with col2:
                        status = st.selectbox("Status", options=[
                            'Active', 'In Use', 'Under Maintenance', 'Out of Service', 'Retired'
                        ], index=['Active', 'In Use', 'Under Maintenance', 'Out of Service', 'Retired'].index(
                            item['status'] if item['status'] in ['Active', 'In Use', 'Under Maintenance', 'Out of Service', 'Retired'] 
                            else 'Active')
                        )
                    
                    description = st.text_area("Description", value=item['description'], height=100)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        location = st.text_input("Location", value=item['location'])
                    with col2:
                        assigned_to = st.text_input("Assigned To", value=item.get('assigned_to', ''))
                
                render_crud_fieldset("Basic Information", render_basic_info)
                
                # Specifications Section
                def render_specifications():
                    col1, col2 = st.columns(2)
                    with col1:
                        manufacturer = st.text_input("Manufacturer", value=item['manufacturer'])
                    with col2:
                        model = st.text_input("Model", value=item['model'])
                    
                    serial_number = st.text_input("Serial Number", value=item['serial_number'])
                
                render_crud_fieldset("Specifications", render_specifications)
                
                # Financial Information Section
                def render_financial():
                    col1, col2 = st.columns(2)
                    with col1:
                        purchase_date = st.date_input("Purchase Date", 
                            value=datetime.strptime(item['purchase_date'], '%Y-%m-%d') if item['purchase_date'] else datetime.now()
                        )
                    with col2:
                        purchase_cost = st.number_input("Purchase Cost ($)", 
                            value=float(item['purchase_cost']) if item.get('purchase_cost') else 0.0,
                            step=100.0
                        )
                
                render_crud_fieldset("Financial Information", render_financial)
                
                # Maintenance Section
                def render_maintenance():
                    col1, col2 = st.columns(2)
                    with col1:
                        last_maintenance = st.date_input("Last Maintenance Date", 
                            value=datetime.strptime(item['last_maintenance'], '%Y-%m-%d') if item['last_maintenance'] else datetime.now()
                        )
                    with col2:
                        next_maintenance = st.date_input("Next Maintenance Date",
                            value=datetime.strptime(item['next_maintenance'], '%Y-%m-%d') if item['next_maintenance'] else (datetime.now() + timedelta(days=90))
                        )
                    
                    notes = st.text_area("Maintenance Notes", value=item.get('notes', ''), height=100)
                
                render_crud_fieldset("Maintenance", render_maintenance)
                
                # Form Actions
                form_actions = render_form_actions(
                    save_label="Save Equipment",
                    cancel_label="Cancel",
                    delete_label="Delete Equipment",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    # Update item with form values
                    updated_item = {
                        'equipment_id': equipment_id,
                        'name': name,
                        'category': category,
                        'description': description,
                        'status': status,
                        'location': location,
                        'manufacturer': manufacturer,
                        'model': model,
                        'serial_number': serial_number,
                        'purchase_date': purchase_date.strftime('%Y-%m-%d'),
                        'purchase_cost': float(purchase_cost),
                        'last_maintenance': last_maintenance.strftime('%Y-%m-%d'),
                        'next_maintenance': next_maintenance.strftime('%Y-%m-%d'),
                        'maintenance_history': item.get('maintenance_history', []),
                        'assigned_to': assigned_to,
                        'notes': notes
                    }
                    
                    # Check if maintenance date has been updated, and if so, add to history
                    if item.get('last_maintenance') != updated_item['last_maintenance']:
                        history_entry = {
                            'date': updated_item['last_maintenance'],
                            'type': 'Regular Maintenance',
                            'notes': notes,
                            'performed_by': assigned_to if assigned_to else 'Unknown'
                        }
                        updated_item['maintenance_history'] = [history_entry] + updated_item['maintenance_history']
                    
                    # Save the updated item
                    self._save_item(updated_item)
                    
                    # Show success message and return to list view
                    st.success("Equipment saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked'] and not is_new:
                    self._delete_item(item['equipment_id'])
                    st.success("Equipment deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view
            # Basic Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Basic Information")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Equipment ID:** {item['equipment_id']}")
            with col2:
                st.markdown(f"**Name:** {item['name']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Category:** {item['category']}")
            with col2:
                status_html = f"""
                <div style="display: flex; align-items: center; background: transparent;">
                    <span class='crud-status crud-status-{self._get_status_class(item['status'])}' style="outline: none; box-shadow: none; border: none;">{item['status']}</span>
                </div>
                """
                st.markdown("**Status:**")
                st.markdown(status_html, unsafe_allow_html=True)
            
            st.markdown(f"**Description:**")
            st.markdown(f"```{item['description']}```")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Location:** {item['location']}")
            with col2:
                st.markdown(f"**Assigned To:** {item.get('assigned_to', 'Unassigned')}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Specifications Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Specifications")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Manufacturer:** {item['manufacturer']}")
            with col2:
                st.markdown(f"**Model:** {item['model']}")
            
            st.markdown(f"**Serial Number:** {item['serial_number']}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Financial Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Financial Information")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Purchase Date:** {item['purchase_date']}")
            with col2:
                st.markdown(f"**Purchase Cost:** ${float(item['purchase_cost']):,.2f}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Maintenance Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Maintenance")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Last Maintenance:** {item['last_maintenance']}")
            with col2:
                st.markdown(f"**Next Maintenance:** {item['next_maintenance']}")
            
            if item.get('notes'):
                st.markdown(f"**Maintenance Notes:**")
                st.markdown(f"```{item.get('notes', '')}```")
            
            # Show maintenance history if it exists
            if item.get('maintenance_history'):
                st.markdown("### Maintenance History")
                for i, entry in enumerate(item['maintenance_history']):
                    st.markdown(f"**{entry.get('date', 'Unknown date')} - {entry.get('type', 'Maintenance')}**")
                    st.markdown(f"Performed by: {entry.get('performed_by', 'Unknown')}")
                    if entry.get('notes'):
                        st.markdown(f"Notes: {entry.get('notes')}")
                    if i < len(item['maintenance_history']) - 1:
                        st.markdown("---")
            st.markdown("</div>", unsafe_allow_html=True)
        
        end_crud_detail_container()

# Function to render the module
def render():
    """Render the Equipment Management module."""
    st.title("Equipment Management")
    
    # Create and render the Equipment module
    equipment = EquipmentModule()
    equipment.render()