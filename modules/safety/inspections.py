"""
Safety Inspections Module for gcPanel

This module provides management of safety inspections with CRUD styling
for a consistent user experience across the application.
"""

import streamlit as st
import os
import json
from datetime import datetime, timedelta
import random
import pandas as pd

from modules.crud_template import CrudModule
from assets.crud_styler import (
    apply_crud_styles, 
    render_form_actions, 
    render_crud_fieldset
)

class SafetyInspectionModule(CrudModule):
    def __init__(self):
        """Initialize the Safety Inspections module with configuration."""
        super().__init__(
            module_name="Safety Inspections",
            data_file_path="data/safety/inspections.json",
            id_field="inspection_id",
            list_columns=["inspection_id", "inspection_date", "inspection_type", "location", "inspector", "status"],
            default_sort_field="inspection_date",
            default_sort_direction="desc",
            status_field="status",
            filter_options=["Scheduled", "In Progress", "Complete", "Pending Review", "Rework Required"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        inspection_types = [
            "Daily Site Walk", 
            "Weekly Safety Audit", 
            "Monthly Equipment Inspection", 
            "Quarterly Compliance Audit", 
            "Fall Protection Inspection", 
            "Fire Safety Inspection", 
            "Scaffolding Inspection",
            "Crane Inspection"
        ]
        
        locations = [
            "Level 1 - North", 
            "Level 2 - East", 
            "Level 3 - South",
            "Level 4 - West", 
            "Basement",
            "Roof", 
            "Exterior Scaffolding",
            "Loading Dock", 
            "Parking Area",
            "Entire Building"
        ]
        
        inspectors = [
            "John Smith (Safety Manager)", 
            "Maria Garcia (Site Supervisor)", 
            "Robert Johnson (QA/QC Manager)", 
            "Lisa Wong (EHS Specialist)", 
            "David Miller (Project Manager)",
            "OSHA Representative",
            "Third Party Inspector"
        ]
        
        statuses = ["Scheduled", "In Progress", "Complete", "Pending Review", "Rework Required"]
        
        # Demo inspections
        demo_items = []
        
        # Create sample inspections
        for i in range(1, 25):
            # Set dates based on realistic timeframes
            today = datetime.now()
            
            # Past, present, or future inspection
            days_offset = random.randint(-30, 30)
            inspection_date = today + timedelta(days=days_offset)
            
            # Randomize inspection details
            inspection_type = random.choice(inspection_types)
            location = random.choice(locations)
            inspector = random.choice(inspectors)
            
            # Determine status based on date
            if days_offset < -1:  # Past inspection
                status = random.choice(["Complete", "Pending Review", "Rework Required"])
                if status == "Complete":
                    score = random.randint(85, 100)
                elif status == "Pending Review":
                    score = random.randint(70, 95)
                else:  # Rework Required
                    score = random.randint(50, 75)
            elif days_offset < 1:  # Today or yesterday
                status = random.choice(["In Progress", "Scheduled", "Complete", "Pending Review"])
                if status == "Complete":
                    score = random.randint(80, 100)
                elif status == "Pending Review":
                    score = random.randint(75, 95)
                else:  # In Progress or Scheduled
                    score = None
            else:  # Future inspection
                status = "Scheduled"
                score = None
            
            # Generate checklist items based on inspection type
            checklist = []
            
            # Number of checklist items based on inspection type
            if "Daily" in inspection_type:
                num_checklist_items = random.randint(5, 10)
            elif "Weekly" in inspection_type:
                num_checklist_items = random.randint(10, 15)
            elif "Monthly" in inspection_type:
                num_checklist_items = random.randint(15, 25)
            else:
                num_checklist_items = random.randint(20, 30)
            
            if status != "Scheduled":
                # Generate checklist items with results
                for j in range(num_checklist_items):
                    if status == "Complete" or status == "Pending Review":
                        result = random.choices(
                            ["Pass", "Fail", "N/A"], 
                            weights=[0.8, 0.15, 0.05], 
                            k=1
                        )[0]
                    elif status == "In Progress":
                        # For in progress, some items might not be checked yet
                        result = random.choices(
                            ["Pass", "Fail", "N/A", None], 
                            weights=[0.5, 0.1, 0.05, 0.35], 
                            k=1
                        )[0]
                    else:  # Rework Required
                        result = random.choices(
                            ["Pass", "Fail", "N/A"], 
                            weights=[0.6, 0.35, 0.05], 
                            k=1
                        )[0]
                    
                    comments = None
                    if result == "Fail":
                        fail_comments = [
                            "Needs immediate attention",
                            "Not properly secured",
                            "Missing required component",
                            "Damaged and requires repair",
                            "Not compliant with regulations",
                            "Improper installation",
                            "Safety hazard identified"
                        ]
                        comments = random.choice(fail_comments)
                    
                    checklist.append({
                        "id": j + 1,
                        "description": self._generate_checklist_item(inspection_type, j),
                        "result": result,
                        "comments": comments
                    })
            else:
                # For scheduled inspections, just create the checklist without results
                for j in range(num_checklist_items):
                    checklist.append({
                        "id": j + 1,
                        "description": self._generate_checklist_item(inspection_type, j),
                        "result": None,
                        "comments": None
                    })
            
            # Create action items for inspections with failures
            action_items = []
            if status in ["Complete", "Pending Review", "Rework Required"]:
                # Find all failed items
                failed_items = [item for item in checklist if item.get("result") == "Fail"]
                
                for failed_item in failed_items:
                    action_due_date = inspection_date + timedelta(days=random.randint(1, 14))
                    
                    action_status = random.choice(["Open", "In Progress", "Complete"]) if status == "Complete" else "Open"
                    
                    action_items.append({
                        "description": f"Address: {failed_item['description']}",
                        "assigned_to": random.choice(inspectors.split("(")[0].strip() for inspector in inspectors),
                        "due_date": action_due_date.strftime('%Y-%m-%d'),
                        "status": action_status
                    })
            
            # Create the inspection record
            item = {
                'inspection_id': f'INSP-{i:03d}',
                'inspection_date': inspection_date.strftime('%Y-%m-%d'),
                'inspection_type': inspection_type,
                'location': location,
                'inspector': inspector,
                'status': status,
                'score': score,
                'notes': self._generate_inspection_notes(inspection_type, status) if random.random() > 0.3 else "",
                'checklist': checklist,
                'action_items': action_items,
                'attachments': []
            }
            
            demo_items.append(item)
        
        # Save demo data
        self._save_items(demo_items)
    
    def _generate_checklist_item(self, inspection_type, index):
        """Generate an appropriate checklist item based on inspection type."""
        # Common safety checklist items
        daily_items = [
            "Work areas are clean and free of debris",
            "Proper PPE is being worn by all workers",
            "Fire extinguishers are accessible and charged",
            "Exit pathways are clear and unobstructed",
            "First aid kits are stocked and accessible",
            "Proper signage is in place",
            "Tools and equipment are in good condition",
            "Electrical cords and connections are safe",
            "Trenches and excavations are properly protected",
            "Scaffolding is properly erected with guardrails",
            "Materials are stored safely",
            "Hazardous materials are properly labeled and stored",
            "Workers are using proper lifting techniques",
            "Adequate lighting is provided",
            "Workers are not exposed to fall hazards"
        ]
        
        equipment_items = [
            "Equipment is properly maintained",
            "Operator certifications are current",
            "Safety features are functioning correctly",
            "Warning labels and decals are legible",
            "Backup alarms are working",
            "Tire condition is acceptable",
            "Fluid levels are appropriate",
            "Controls are functioning properly",
            "Lights and signals are working",
            "Structural components are intact"
        ]
        
        fall_protection_items = [
            "Guardrails meet height requirements",
            "Personal fall arrest systems are inspected",
            "Anchor points are capable of supporting required loads",
            "Warning lines are properly placed",
            "Fall protection plan is available and current",
            "Workers using fall protection are trained",
            "Safety nets are properly installed",
            "Hole covers are secured and marked",
            "Ladder safety devices are functioning",
            "Scaffolding has proper guardrails"
        ]
        
        fire_safety_items = [
            "Fire extinguishers are properly charged",
            "Fire extinguishers are properly mounted",
            "Fire extinguishers are unobstructed",
            "Fire alarm pull stations are accessible",
            "Emergency exit signs are illuminated",
            "Exit routes are clear and unobstructed",
            "Fire sprinkler heads are unobstructed",
            "Fire doors close properly",
            "Flammable materials are properly stored",
            "No smoking signs are posted in appropriate areas"
        ]
        
        # Select appropriate checklist items based on inspection type
        if "Daily" in inspection_type:
            if index < len(daily_items):
                return daily_items[index]
            else:
                return daily_items[index % len(daily_items)]
        elif "Equipment" in inspection_type or "Crane" in inspection_type:
            if index < len(equipment_items):
                return equipment_items[index]
            else:
                return equipment_items[index % len(equipment_items)]
        elif "Fall" in inspection_type:
            if index < len(fall_protection_items):
                return fall_protection_items[index]
            else:
                return fall_protection_items[index % len(fall_protection_items)]
        elif "Fire" in inspection_type:
            if index < len(fire_safety_items):
                return fire_safety_items[index]
            else:
                return fire_safety_items[index % len(fire_safety_items)]
        else:
            # For all other inspection types, use a mix of items
            all_items = daily_items + equipment_items + fall_protection_items + fire_safety_items
            return all_items[index % len(all_items)]
    
    def _generate_inspection_notes(self, inspection_type, status):
        """Generate appropriate inspection notes based on type and status."""
        if status == "Scheduled":
            notes = [
                f"Standard {inspection_type} scheduled as per safety plan.",
                f"Follow standard {inspection_type} checklist and procedures.",
                f"Please coordinate with site supervisor before beginning the {inspection_type}.",
                f"This is a routine {inspection_type} required by project safety plan."
            ]
        elif status == "In Progress":
            notes = [
                f"{inspection_type} started at 9:30 AM, continuing throughout the day.",
                f"Partial completion of {inspection_type}, to be continued tomorrow.",
                f"Multiple areas require follow-up inspection.",
                f"Several items identified for immediate attention during initial inspection."
            ]
        elif status == "Complete":
            notes = [
                f"{inspection_type} completed with minor issues noted.",
                f"All areas passed {inspection_type} with satisfactory results.",
                f"{inspection_type} revealed good compliance with safety requirements.",
                f"Action items from {inspection_type} have been assigned to responsible parties."
            ]
        elif status == "Pending Review":
            notes = [
                f"{inspection_type} completed and awaiting final review by safety manager.",
                f"Documentation for {inspection_type} needs to be verified.",
                f"Several critical items in {inspection_type} require secondary verification.",
                f"Please expedite review of this {inspection_type} due to identified issues."
            ]
        else:  # Rework Required
            notes = [
                f"Several deficiencies identified during {inspection_type}. Re-inspection required after corrections.",
                f"Immediate action required based on {inspection_type} findings.",
                f"Failed {inspection_type} - critical safety issues must be addressed within 24 hours.",
                f"Multiple non-compliance items found during {inspection_type}. See action items for details."
            ]
        
        return random.choice(notes)
    
    def _create_new_item_template(self):
        """Create a template for a new safety inspection with default values."""
        item_id = self._generate_new_id()
        
        # Set default dates
        today = datetime.now()
        
        return {
            'inspection_id': f'INSP-{int(item_id):03d}',
            'inspection_date': today.strftime('%Y-%m-%d'),
            'inspection_type': '',
            'location': '',
            'inspector': '',
            'status': 'Scheduled',
            'score': None,
            'notes': '',
            'checklist': [],
            'action_items': [],
            'attachments': []
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for safety inspections."""
        items = self._get_items()
        
        # If no items exist yet, start with ID 1
        if not items:
            return "1"
        
        # Find the highest numerical ID and increment
        max_id = 0
        for item in items:
            item_id = item.get('inspection_id', '')
            if item_id.startswith('INSP-'):
                try:
                    num = int(item_id.split('-')[1])
                    max_id = max(max_id, num)
                except:
                    pass
        
        return str(max_id + 1)
    
    def _get_status_class(self, status):
        """Get the status class for a given status value."""
        status_classes = {
            'Scheduled': 'info',
            'In Progress': 'info',
            'Complete': 'success',
            'Pending Review': 'warning',
            'Rework Required': 'danger'
        }
        return status_classes.get(status, 'secondary')
    
    def render_detail_view(self):
        """Render the detail view for creating, viewing, or editing a safety inspection."""
        # Apply CRUD styles
        apply_crud_styles()
        
        base_key = self._get_state_key_prefix()
        
        # Get view mode
        is_new = st.session_state.get(f'{base_key}_view') == 'new'
        is_edit_mode = st.session_state.get(f'{base_key}_edit_mode', False)
        
        # Get item data
        if is_new:
            item = self._create_new_item_template()
            detail_title = "New Safety Inspection"
        else:
            item_id = st.session_state.get(f'{base_key}_selected_id')
            item = self._get_item_by_id(item_id)
            if not item:
                st.error(f"Safety Inspection with ID {item_id} not found")
                return
            detail_title = f"{item.get('inspection_id', '')}: {item.get('inspection_type', 'Safety Inspection')}"
        
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
            col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
            with col1:
                if st.button("✏️ Edit", type="primary", key=f"edit_{base_key}_action"):
                    st.session_state[f'{base_key}_edit_mode'] = True
                    st.rerun()
            with col2:
                if st.button("📄 PDF", type="secondary", key=f"pdf_{base_key}_action"):
                    st.info("This would generate a PDF inspection report in a production environment.")
            with col3:
                if st.button("🗑️ Delete", type="secondary", key=f"delete_{base_key}_action"):
                    st.warning("Are you sure you want to delete this inspection?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key=f"confirm_delete_{base_key}"):
                            self._delete_item(item['inspection_id'])
                            st.success("Safety inspection deleted successfully")
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
                        inspection_id = st.text_input("Inspection ID", value=item['inspection_id'], disabled=not is_new)
                    with col2:
                        inspection_type = st.selectbox("Inspection Type", options=[
                            '', 'Daily Site Walk', 'Weekly Safety Audit', 'Monthly Equipment Inspection', 
                            'Quarterly Compliance Audit', 'Fall Protection Inspection', 
                            'Fire Safety Inspection', 'Scaffolding Inspection', 'Crane Inspection'
                        ], index=0 if not item['inspection_type'] else ['', 'Daily Site Walk', 'Weekly Safety Audit', 
                                                                    'Monthly Equipment Inspection', 'Quarterly Compliance Audit', 
                                                                    'Fall Protection Inspection', 'Fire Safety Inspection', 
                                                                    'Scaffolding Inspection', 'Crane Inspection'].index(item['inspection_type']))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        inspection_date = st.date_input(
                            "Inspection Date", 
                            value=datetime.strptime(item['inspection_date'], '%Y-%m-%d') if item['inspection_date'] else datetime.now()
                        )
                    with col2:
                        status = st.selectbox("Status", options=[
                            'Scheduled', 'In Progress', 'Complete', 'Pending Review', 'Rework Required'
                        ], index=['Scheduled', 'In Progress', 'Complete', 'Pending Review', 'Rework Required'].index(item['status']))
                    
                    location = st.text_input("Location", value=item['location'])
                    inspector = st.text_input("Inspector", value=item['inspector'])
                    
                    # Score is only applicable for completed inspections
                    if status in ['Complete', 'Pending Review', 'Rework Required']:
                        score = st.slider("Score (%)", 0, 100, int(item['score']) if item.get('score') is not None else 85)
                    else:
                        score = None
                    
                    notes = st.text_area("Notes", value=item.get('notes', ''), height=100)
                    
                    return inspection_id, inspection_type, inspection_date, status, location, inspector, score, notes
                
                inspection_id, inspection_type, inspection_date, status, location, inspector, score, notes = render_crud_fieldset("Inspection Information", render_basic_info)
                
                # Checklist Section
                def render_checklist():
                    st.markdown("#### Inspection Checklist")
                    
                    # Initialize or get existing checklist
                    checklist = item.get('checklist', [])
                    updated_checklist = []
                    
                    if not checklist and inspection_type:
                        # Generate a new checklist based on the inspection type
                        num_items = 10  # Default number of items
                        
                        if "Daily" in inspection_type:
                            num_items = 8
                        elif "Weekly" in inspection_type:
                            num_items = 12
                        elif "Monthly" in inspection_type:
                            num_items = 15
                        elif "Quarterly" in inspection_type:
                            num_items = 20
                        
                        for i in range(num_items):
                            checklist.append({
                                "id": i + 1,
                                "description": self._generate_checklist_item(inspection_type, i),
                                "result": None,
                                "comments": None
                            })
                    
                    # Display existing checklist items with edit capability
                    for i, item in enumerate(checklist):
                        col1, col2, col3 = st.columns([5, 2, 3])
                        
                        with col1:
                            description = st.text_input(f"Item {i+1}", 
                                                    value=item['description'], 
                                                    key=f"checklist_desc_{i}")
                        
                        with col2:
                            result = st.selectbox("Result", 
                                               options=['', 'Pass', 'Fail', 'N/A'], 
                                               index=['', 'Pass', 'Fail', 'N/A'].index(item['result']) if item['result'] in ['Pass', 'Fail', 'N/A'] else 0,
                                               key=f"checklist_result_{i}")
                        
                        with col3:
                            comments = st.text_input("Comments", 
                                                 value=item.get('comments', ''), 
                                                 key=f"checklist_comments_{i}")
                        
                        # Add the updated item to the checklist
                        updated_checklist.append({
                            "id": item['id'],
                            "description": description,
                            "result": result if result else None,
                            "comments": comments if comments else None
                        })
                    
                    # Add new item button
                    if st.button("Add Checklist Item", key=f"add_checklist_item"):
                        new_id = len(updated_checklist) + 1
                        updated_checklist.append({
                            "id": new_id,
                            "description": "",
                            "result": None,
                            "comments": None
                        })
                    
                    return updated_checklist
                
                checklist = render_crud_fieldset("Inspection Checklist", render_checklist)
                
                # Action Items Section
                def render_action_items():
                    st.markdown("#### Action Items")
                    
                    # Initialize or get existing action items
                    action_items = item.get('action_items', [])
                    updated_action_items = []
                    
                    # Display existing action items with edit capability
                    for i, action in enumerate(action_items):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            description = st.text_input(f"Action {i+1}", 
                                                    value=action['description'], 
                                                    key=f"action_desc_{i}")
                        
                        with col2:
                            assigned_to = st.text_input("Assigned To", 
                                                    value=action.get('assigned_to', ''), 
                                                    key=f"action_assigned_{i}")
                        
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            due_date = st.date_input("Due Date", 
                                                 value=datetime.strptime(action['due_date'], '%Y-%m-%d') if action.get('due_date') else datetime.now() + timedelta(days=7),
                                                 key=f"action_due_{i}")
                        
                        with col2:
                            action_status = st.selectbox("Status", 
                                                     options=['Open', 'In Progress', 'Complete'], 
                                                     index=['Open', 'In Progress', 'Complete'].index(action.get('status', 'Open')),
                                                     key=f"action_status_{i}")
                        
                        # Add the updated action to the list
                        updated_action_items.append({
                            "description": description,
                            "assigned_to": assigned_to,
                            "due_date": due_date.strftime('%Y-%m-%d'),
                            "status": action_status
                        })
                        
                        st.markdown("---")
                    
                    # Add new action item button
                    if st.button("Add Action Item", key=f"add_action_item"):
                        updated_action_items.append({
                            "description": "",
                            "assigned_to": "",
                            "due_date": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                            "status": "Open"
                        })
                    
                    return updated_action_items
                
                action_items = render_crud_fieldset("Action Items", render_action_items)
                
                # Form Actions
                form_actions = render_form_actions(
                    save_label="Save Inspection",
                    cancel_label="Cancel",
                    delete_label="Delete Inspection",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    # Update item with form values
                    updated_item = {
                        'inspection_id': inspection_id,
                        'inspection_date': inspection_date.strftime('%Y-%m-%d'),
                        'inspection_type': inspection_type,
                        'location': location,
                        'inspector': inspector,
                        'status': status,
                        'score': score,
                        'notes': notes,
                        'checklist': checklist,
                        'action_items': action_items,
                        'attachments': item.get('attachments', [])
                    }
                    
                    # Save the updated item
                    self._save_item(updated_item)
                    
                    # Show success message and return to list view
                    st.success("Safety inspection saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked'] and not is_new:
                    self._delete_item(item['inspection_id'])
                    st.success("Safety inspection deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view
            # Inspection Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Inspection Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Inspection ID:** {item['inspection_id']}")
            with col2:
                st.markdown(f"**Inspection Type:** {item['inspection_type']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Inspection Date:** {item['inspection_date']}")
            with col2:
                # Show status with colored badge
                status_class = self._get_status_class(item['status'])
                status_html = f"""
                <div style="display: flex; align-items: center; background: transparent;">
                    <span class='crud-status crud-status-{status_class}' style="outline: none; box-shadow: none; border: none;">{item['status']}</span>
                </div>
                """
                st.markdown("**Status:**")
                st.markdown(status_html, unsafe_allow_html=True)
            
            st.markdown(f"**Location:** {item['location']}")
            st.markdown(f"**Inspector:** {item['inspector']}")
            
            if item.get('score') is not None:
                st.markdown(f"**Score:** {item['score']}%")
                
                # Show score as progress bar
                score_color = "green"
                if item['score'] < 70:
                    score_color = "red"
                elif item['score'] < 85:
                    score_color = "orange"
                
                st.markdown(f"""
                <div style="width: 100%; height: 10px; background-color: #f0f0f0; border-radius: 5px; margin-top: 5px;">
                    <div style="width: {item['score']}%; height: 100%; background-color: {score_color}; border-radius: 5px;"></div>
                </div>
                """, unsafe_allow_html=True)
            
            if item.get('notes'):
                st.markdown(f"**Notes:**")
                st.markdown(f"```{item['notes']}```")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Checklist Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Inspection Checklist")
            
            # Statistics for checklist
            checklist = item.get('checklist', [])
            
            if checklist:
                # Calculate statistics
                total_items = len(checklist)
                completed_items = sum(1 for c in checklist if c.get('result') is not None)
                pass_items = sum(1 for c in checklist if c.get('result') == 'Pass')
                fail_items = sum(1 for c in checklist if c.get('result') == 'Fail')
                na_items = sum(1 for c in checklist if c.get('result') == 'N/A')
                
                # Display statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Items", total_items)
                with col2:
                    st.metric("Completed", f"{completed_items}/{total_items}", f"{round(completed_items/total_items*100 if total_items > 0 else 0)}%")
                with col3:
                    st.metric("Pass", pass_items, f"{round(pass_items/total_items*100 if total_items > 0 else 0)}%")
                with col4:
                    st.metric("Fail", fail_items, f"{round(fail_items/total_items*100 if total_items > 0 else 0)}%")
                
                # Display checklist items in a table
                if st.checkbox("Show Full Checklist", value=True):
                    checklist_df = pd.DataFrame(checklist)
                    
                    # Format the dataframe for display
                    checklist_df = checklist_df[['id', 'description', 'result', 'comments']]
                    checklist_df = checklist_df.rename(columns={
                        'id': 'ID',
                        'description': 'Item',
                        'result': 'Result',
                        'comments': 'Comments'
                    })
                    
                    # Fill in missing values
                    checklist_df = checklist_df.fillna("")
                    
                    # Apply styling to the result column
                    def style_result(val):
                        if val == 'Pass':
                            return 'background-color: #d4edda; color: #155724; font-weight: bold;'
                        elif val == 'Fail':
                            return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
                        elif val == 'N/A':
                            return 'background-color: #e2e3e5; color: #383d41; font-weight: bold;'
                        return ''
                    
                    # Display the styled dataframe
                    st.dataframe(checklist_df.style.applymap(style_result, subset=['Result']))
                
                # Show only failed items
                if fail_items > 0:
                    st.markdown("### Failed Items")
                    failed_items = [c for c in checklist if c.get('result') == 'Fail']
                    
                    for failed_item in failed_items:
                        st.markdown(f"""
                        <div style="border-left: 3px solid #e74c3c; padding-left: 10px; margin-bottom: 10px;">
                            <div style="font-weight: 500;">{failed_item['description']}</div>
                            <div style="font-size: 0.9rem; color: #7f8c8d; margin-top: 3px;">
                                <strong>Comments:</strong> {failed_item.get('comments', 'No comments')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No checklist items available for this inspection.")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Action Items Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Action Items")
            
            action_items = item.get('action_items', [])
            
            if action_items:
                for i, action in enumerate(action_items):
                    # Determine status color
                    status_color = {
                        'Open': '#e74c3c',
                        'In Progress': '#3498db',
                        'Complete': '#2ecc71'
                    }.get(action.get('status', 'Open'), '#95a5a6')
                    
                    # Calculate days until due
                    due_date = datetime.strptime(action['due_date'], '%Y-%m-%d')
                    days_until_due = (due_date - datetime.now()).days
                    
                    st.markdown(f"""
                    <div style="border: 1px solid #f0f0f0; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div style="flex-grow: 1;">
                                <div style="font-weight: 500;">{action['description']}</div>
                                <div style="font-size: 0.85rem; margin-top: 5px;">
                                    <strong>Assigned To:</strong> {action.get('assigned_to', 'Unassigned')}
                                </div>
                            </div>
                            <div>
                                <span style="display: inline-block; padding: 3px 8px; background-color: {status_color}; 
                                          color: white; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">
                                    {action.get('status', 'Open')}
                                </span>
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 0.85rem;">
                            <div><strong>Due Date:</strong> {action['due_date']}</div>
                            <div>
                                {f'<span style="color: {"#e74c3c" if days_until_due < 0 else "#f39c12" if days_until_due < 3 else "#7f8c8d"};">{"Overdue" if days_until_due < 0 else f"Due in {days_until_due} days"}</span>' if action.get('status') != 'Complete' else '<span style="color: #2ecc71;">Completed</span>'}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No action items available for this inspection.")
            
            # Add action item button
            if st.button("➕ Add Action Item", key=f"add_action_{base_key}"):
                st.session_state[f'{base_key}_add_action'] = True
                
            if st.session_state.get(f'{base_key}_add_action', False):
                with st.form(f"action_form_{base_key}"):
                    action_description = st.text_input("Description")
                    assigned_to = st.text_input("Assigned To")
                    due_date = st.date_input("Due Date", value=datetime.now() + timedelta(days=7))
                    
                    action_cols = st.columns([1, 1])
                    with action_cols[0]:
                        save_action = st.form_submit_button("Save Action Item")
                    with action_cols[1]:
                        cancel_action = st.form_submit_button("Cancel")
                    
                    if save_action and action_description:
                        # Add action item to the inspection
                        new_action = {
                            'description': action_description,
                            'assigned_to': assigned_to,
                            'due_date': due_date.strftime('%Y-%m-%d'),
                            'status': 'Open'
                        }
                        
                        action_items = item.get('action_items', [])
                        action_items.append(new_action)
                        
                        # Update item with new action item
                        item['action_items'] = action_items
                        self._save_item(item)
                        
                        st.success("Action item added successfully")
                        st.session_state[f'{base_key}_add_action'] = False
                        st.rerun()
                    
                    if cancel_action:
                        st.session_state[f'{base_key}_add_action'] = False
                        st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Attachments Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Attachments")
            
            if not item.get('attachments'):
                st.info("No attachments for this inspection.")
                
                # Add attachment button
                if st.button("➕ Add Attachment", key=f"add_attachment_{base_key}"):
                    st.session_state[f'{base_key}_add_attachment'] = True
                    
                if st.session_state.get(f'{base_key}_add_attachment', False):
                    with st.form(f"attachment_form_{base_key}"):
                        file_name = st.text_input("File Name")
                        file_type = st.selectbox("File Type", options=["PDF", "DOC", "JPG", "PNG", "Other"])
                        file_description = st.text_input("Description")
                        
                        attachment_actions = st.columns([1, 1])
                        with attachment_actions[0]:
                            save_attachment = st.form_submit_button("Save Attachment")
                        with attachment_actions[1]:
                            cancel_attachment = st.form_submit_button("Cancel")
                        
                        if save_attachment and file_name:
                            # Add attachment to the item
                            new_attachment = {
                                'name': file_name,
                                'type': file_type,
                                'description': file_description,
                                'date_added': datetime.now().strftime('%Y-%m-%d'),
                                'added_by': "Current User"
                            }
                            
                            attachments = item.get('attachments', [])
                            attachments.append(new_attachment)
                            
                            # Update item with new attachment
                            item['attachments'] = attachments
                            self._save_item(item)
                            
                            st.success("Attachment added successfully")
                            st.session_state[f'{base_key}_add_attachment'] = False
                            st.rerun()
                        
                        if cancel_attachment:
                            st.session_state[f'{base_key}_add_attachment'] = False
                            st.rerun()
            else:
                # Display attachments
                for i, attachment in enumerate(item.get('attachments', [])):
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    with col1:
                        st.markdown(f"**{attachment['name']}**")
                    with col2:
                        st.markdown(f"Type: {attachment['type']}")
                    with col3:
                        st.markdown(f"Added: {attachment['date_added']}")
                    with col4:
                        if st.button("📄 View", key=f"view_attachment_{i}_{base_key}"):
                            st.info(f"Viewing {attachment['name']} (Demo Mode)")
                    
                    if attachment.get('description'):
                        st.markdown(f"_{attachment['description']}_")
                    
                    if i < len(item.get('attachments', [])) - 1:
                        st.markdown("---")
                
                # Add attachment button
                if st.button("➕ Add Attachment", key=f"add_attachment_{base_key}"):
                    st.session_state[f'{base_key}_add_attachment'] = True
                    
                if st.session_state.get(f'{base_key}_add_attachment', False):
                    with st.form(f"attachment_form_{base_key}"):
                        file_name = st.text_input("File Name")
                        file_type = st.selectbox("File Type", options=["PDF", "DOC", "JPG", "PNG", "Other"])
                        file_description = st.text_input("Description")
                        
                        attachment_actions = st.columns([1, 1])
                        with attachment_actions[0]:
                            save_attachment = st.form_submit_button("Save Attachment")
                        with attachment_actions[1]:
                            cancel_attachment = st.form_submit_button("Cancel")
                        
                        if save_attachment and file_name:
                            # Add attachment to the item
                            new_attachment = {
                                'name': file_name,
                                'type': file_type,
                                'description': file_description,
                                'date_added': datetime.now().strftime('%Y-%m-%d'),
                                'added_by': "Current User"
                            }
                            
                            attachments = item.get('attachments', [])
                            attachments.append(new_attachment)
                            
                            # Update item with new attachment
                            item['attachments'] = attachments
                            self._save_item(item)
                            
                            st.success("Attachment added successfully")
                            st.session_state[f'{base_key}_add_attachment'] = False
                            st.rerun()
                        
                        if cancel_attachment:
                            st.session_state[f'{base_key}_add_attachment'] = False
                            st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        end_crud_detail_container()