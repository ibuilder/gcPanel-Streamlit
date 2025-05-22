"""
Hazards Management Module for gcPanel

This module provides tracking and management of workplace hazards with CRUD styling
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

class HazardModule(CrudModule):
    def __init__(self):
        """Initialize the Hazards module with configuration."""
        super().__init__(
            module_name="Hazards",
            data_file_path="data/safety/hazards.json",
            id_field="hazard_id",
            list_columns=["hazard_id", "identification_date", "hazard_type", "location", "severity", "status"],
            default_sort_field="identification_date",
            default_sort_direction="desc",
            status_field="status",
            filter_options=["Open", "Mitigated", "Closed", "In Progress"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        hazard_types = [
            "Fall Hazard", 
            "Electrical Hazard", 
            "Chemical Hazard", 
            "Mechanical Hazard", 
            "Confined Space", 
            "Fire Hazard", 
            "Ergonomic Hazard",
            "Noise Hazard",
            "Struck-By Hazard",
            "Caught-In/Between Hazard"
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
            "Mechanical Room",
            "Elevator Shaft",
            "Stairwell"
        ]
        
        severities = ["Low", "Medium", "High", "Critical"]
        statuses = ["Open", "Mitigated", "Closed", "In Progress"]
        
        # Personnel for reporting and assignments
        personnel = [
            "John Smith", 
            "Maria Garcia", 
            "Robert Johnson", 
            "Lisa Wong", 
            "David Miller",
            "Sarah Adams", 
            "Michael Chen", 
            "Emma Wilson"
        ]
        
        # Demo hazards
        demo_items = []
        
        # Create sample hazards
        for i in range(1, 26):
            # Set dates based on realistic timeframes
            identification_date = datetime.now() - timedelta(days=random.randint(1, 60))
            
            # Randomize hazard details
            hazard_type = random.choice(hazard_types)
            location = random.choice(locations)
            severity = random.choice(severities)
            
            # Determine status based on date and severity
            days_since = (datetime.now() - identification_date).days
            
            if severity == "Critical":
                if days_since < 7:
                    status = random.choice(["Open", "In Progress"])
                else:
                    status = random.choice(["Mitigated", "Closed"])
            elif severity == "High":
                if days_since < 14:
                    status = random.choice(["Open", "In Progress"])
                else:
                    status = random.choice(["Mitigated", "Closed"])
            else:
                if days_since < 21:
                    status = random.choice(["Open", "In Progress"])
                else:
                    status = random.choice(["Mitigated", "Closed"])
            
            # Generate description based on hazard type
            description = self._generate_hazard_description(hazard_type)
            
            # Create potential impacts
            potential_impacts = self._generate_potential_impacts(hazard_type, severity)
            
            # Create corrective actions
            corrective_actions = []
            
            if status != "Open":
                num_actions = random.randint(1, 3)
                
                for j in range(num_actions):
                    action_date = identification_date + timedelta(days=random.randint(1, 7))
                    action_status = "Complete" if status in ["Mitigated", "Closed"] else "In Progress"
                    
                    corrective_actions.append({
                        "action": self._generate_corrective_action(hazard_type),
                        "responsible_party": random.choice(personnel),
                        "due_date": (action_date + timedelta(days=random.randint(3, 14))).strftime('%Y-%m-%d'),
                        "status": action_status,
                        "notes": "" if random.random() > 0.5 else f"Priority action required due to {severity.lower()} severity."
                    })
            
            # Create the hazard record
            item = {
                'hazard_id': f'HAZ-{i:03d}',
                'identification_date': identification_date.strftime('%Y-%m-%d'),
                'hazard_type': hazard_type,
                'location': location,
                'severity': severity,
                'status': status,
                'description': description,
                'reported_by': random.choice(personnel),
                'potential_impacts': potential_impacts,
                'corrective_actions': corrective_actions,
                'mitigation_date': (identification_date + timedelta(days=random.randint(3, 21))).strftime('%Y-%m-%d') if status in ["Mitigated", "Closed"] else None,
                'attachments': []
            }
            
            demo_items.append(item)
        
        # Save demo data
        self._save_items(demo_items)
    
    def _generate_hazard_description(self, hazard_type):
        """Generate a description based on hazard type."""
        descriptions = {
            "Fall Hazard": [
                "Missing guardrails on scaffold platform at height of 15ft.",
                "Unprotected floor opening (2ft x 2ft) near elevator shaft.",
                "Damaged guardrail system on 4th floor balcony area.",
                "Improperly secured ladder near stairwell opening.",
                "Missing toe boards on elevated work platform."
            ],
            "Electrical Hazard": [
                "Exposed electrical wiring near water source in basement.",
                "Damaged extension cord with exposed conductors in common area.",
                "Inadequate lockout/tagout procedures at main electrical panel.",
                "Overloaded electrical circuit in temporary site office.",
                "Improper grounding of electrical equipment in wet conditions."
            ],
            "Chemical Hazard": [
                "Improper storage of incompatible chemicals in maintenance area.",
                "Missing labels on chemical containers in storage room.",
                "Inadequate ventilation in painting area with high VOC content.",
                "Chemical spill not properly contained near material storage.",
                "Missing safety data sheets for hazardous materials in use."
            ],
            "Mechanical Hazard": [
                "Unguarded rotating machinery in mechanical room.",
                "Damaged tools with missing safety guards being used by workers.",
                "Compressed gas cylinders stored without securing chains.",
                "Pinch points not guarded on material handling equipment.",
                "Power tools missing safety guards or shields."
            ],
            "Confined Space": [
                "Confined space entry without proper atmospheric testing.",
                "Missing confined space permit for utility vault work.",
                "Inadequate ventilation in below-grade utility vault.",
                "No attendant present during confined space operations.",
                "Lack of retrieval equipment for confined space emergency."
            ],
            "Fire Hazard": [
                "Blocked fire exits in construction area.",
                "Flammable materials stored near ignition sources.",
                "Fire extinguishers not readily accessible in work area.",
                "Hot work being performed without proper fire watch.",
                "Excess accumulation of combustible materials and debris."
            ],
            "Ergonomic Hazard": [
                "Workers manually lifting heavy materials without assistance.",
                "Repetitive motion tasks without proper breaks or rotation.",
                "Improper workstation setup causing awkward postures.",
                "Extended reaching and overhead work without proper breaks.",
                "Vibrating tools being used for extended periods without controls."
            ],
            "Noise Hazard": [
                "Workers exposed to high noise levels without hearing protection.",
                "Multiple high-noise operations occurring simultaneously.",
                "No noise monitoring in areas exceeding 85 dBA.",
                "Damaged or improper hearing protection being used.",
                "No noise hazard warning signs in high-noise areas."
            ],
            "Struck-By Hazard": [
                "Materials being hoisted over worker pathways without barriers.",
                "Vehicle operations in congested work areas without spotters.",
                "Unsecured tools and materials at elevated work areas.",
                "Crane operating with suspended load over active work zone.",
                "Inadequate barriers between heavy equipment and workers."
            ],
            "Caught-In/Between Hazard": [
                "Unprotected trench over 5ft deep with workers inside.",
                "Equipment with unguarded moving parts being operated.",
                "Material stacked unsafely with potential for collapse.",
                "Workers positioned between fixed objects and moving equipment.",
                "Inadequate shoring in excavation with loose soil conditions."
            ]
        }
        
        # Return a random description for the given hazard type
        return random.choice(descriptions.get(hazard_type, ["Unspecified hazard identified during site inspection."]))
    
    def _generate_potential_impacts(self, hazard_type, severity):
        """Generate potential impacts based on hazard type and severity."""
        health_impacts = {
            "Low": [
                "Minor injuries requiring first aid treatment.",
                "Temporary discomfort or irritation.",
                "Short-term exposure with minimal health effects."
            ],
            "Medium": [
                "Injuries requiring medical treatment beyond first aid.",
                "Partial hearing loss or vision impairment.",
                "Respiratory issues requiring medical attention.",
                "Musculoskeletal injuries resulting in restricted work."
            ],
            "High": [
                "Serious injuries requiring hospitalization.",
                "Long-term health effects or chronic conditions.",
                "Permanent partial disability.",
                "Severe burns or respiratory damage."
            ],
            "Critical": [
                "Life-threatening injuries.",
                "Permanent total disability.",
                "Fatality potential.",
                "Multiple serious injuries or extensive health impacts."
            ]
        }
        
        # Select appropriate impacts based on severity
        selected_impacts = []
        
        # Add 1-2 health impacts
        selected_impacts.extend(random.sample(health_impacts[severity], k=min(2, len(health_impacts[severity]))))
        
        # Add hazard-specific impacts
        if hazard_type == "Fall Hazard":
            selected_impacts.append(f"Fall from height causing {severity.lower()} severity injuries.")
        elif hazard_type == "Electrical Hazard":
            selected_impacts.append(f"Electrical shock or burn with {severity.lower()} severity outcomes.")
        elif hazard_type == "Chemical Hazard":
            selected_impacts.append(f"Chemical exposure causing {severity.lower()} health effects.")
        elif hazard_type == "Fire Hazard":
            selected_impacts.append(f"Fire outbreak with {severity.lower()} impact on personnel and property.")
        
        # Add property or project impacts
        if severity in ["High", "Critical"]:
            selected_impacts.append("Significant property damage and project delays.")
        elif severity == "Medium":
            selected_impacts.append("Moderate property damage and some project disruption.")
        else:
            selected_impacts.append("Minor property damage or brief project interruption.")
        
        return selected_impacts
    
    def _generate_corrective_action(self, hazard_type):
        """Generate appropriate corrective action based on hazard type."""
        actions = {
            "Fall Hazard": [
                "Install compliant guardrail system with mid-rails and toe boards.",
                "Cover and secure all floor openings with proper covers.",
                "Implement 100% tie-off policy for all elevated work.",
                "Replace damaged fall protection equipment immediately.",
                "Conduct fall protection training for all affected workers."
            ],
            "Electrical Hazard": [
                "Replace damaged electrical cords and inspect all power tools.",
                "Implement proper lockout/tagout procedures with training.",
                "Install GFCI protection for all electrical equipment in wet areas.",
                "Ensure proper grounding of all electrical systems and equipment.",
                "Relocate electrical equipment away from water sources."
            ],
            "Chemical Hazard": [
                "Reorganize chemical storage to separate incompatible materials.",
                "Label all chemical containers according to Hazard Communication requirements.",
                "Improve ventilation in areas with chemical use or storage.",
                "Provide appropriate PPE for chemical handling and clean-up.",
                "Conduct chemical hazard training for all affected workers."
            ],
            "Mechanical Hazard": [
                "Install machine guards on all equipment with moving parts.",
                "Replace damaged tools and equipment with properly guarded alternatives.",
                "Secure compressed gas cylinders with chains or approved racks.",
                "Conduct machine guarding training for equipment operators.",
                "Implement equipment inspection program before each use."
            ],
            "Confined Space": [
                "Implement proper confined space entry permit system.",
                "Provide atmospheric testing equipment and training.",
                "Ensure adequate ventilation for all confined space operations.",
                "Assign dedicated attendant for all confined space entries.",
                "Provide emergency retrieval equipment at all confined space locations."
            ],
            "Fire Hazard": [
                "Clear all egress paths and maintain minimum 44-inch clearance.",
                "Relocate flammable materials away from ignition sources.",
                "Mount additional fire extinguishers throughout the work area.",
                "Implement hot work permit system with dedicated fire watch.",
                "Remove excess combustible materials and improve housekeeping."
            ],
            "Ergonomic Hazard": [
                "Provide mechanical lifting aids for heavy materials.",
                "Implement task rotation for repetitive motion activities.",
                "Adjust workstation heights to promote neutral postures.",
                "Provide ergonomic tools designed to reduce strain.",
                "Conduct ergonomic awareness training for all workers."
            ],
            "Noise Hazard": [
                "Provide appropriate hearing protection with proper training.",
                "Implement engineering controls to reduce noise at source.",
                "Conduct noise monitoring and establish hearing conservation program.",
                "Post high noise area warnings and require hearing protection.",
                "Schedule high-noise activities during low-occupancy periods."
            ],
            "Struck-By Hazard": [
                "Establish controlled access zones with physical barriers.",
                "Require spotters for all equipment operations in congested areas.",
                "Secure all materials and tools at elevated work areas.",
                "Prohibit work under suspended loads in all cases.",
                "Improve visibility with high-visibility clothing for all workers."
            ],
            "Caught-In/Between Hazard": [
                "Install trench protective systems for all excavations over 5 feet deep.",
                "Install machine guarding on all equipment with pinch points.",
                "Implement proper material stacking procedures to prevent collapse.",
                "Establish zones where workers are prohibited during equipment operation.",
                "Conduct training on recognition of caught-in/between hazards."
            ]
        }
        
        # Return a random action for the given hazard type
        return random.choice(actions.get(hazard_type, ["Address identified hazard through appropriate control measures."]))
    
    def _create_new_item_template(self):
        """Create a template for a new hazard with default values."""
        item_id = self._generate_new_id()
        
        # Set default dates
        today = datetime.now()
        
        return {
            'hazard_id': f'HAZ-{int(item_id):03d}',
            'identification_date': today.strftime('%Y-%m-%d'),
            'hazard_type': '',
            'location': '',
            'severity': '',
            'status': 'Open',
            'description': '',
            'reported_by': '',
            'potential_impacts': [],
            'corrective_actions': [],
            'mitigation_date': None,
            'attachments': []
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for hazards."""
        items = self._get_items()
        
        # If no items exist yet, start with ID 1
        if not items:
            return "1"
        
        # Find the highest numerical ID and increment
        max_id = 0
        for item in items:
            item_id = item.get('hazard_id', '')
            if item_id.startswith('HAZ-'):
                try:
                    num = int(item_id.split('-')[1])
                    max_id = max(max_id, num)
                except:
                    pass
        
        return str(max_id + 1)
    
    def _get_status_class(self, status):
        """Get the status class for a given status value."""
        status_classes = {
            'Open': 'danger',
            'In Progress': 'warning',
            'Mitigated': 'info',
            'Closed': 'success'
        }
        return status_classes.get(status, 'secondary')
    
    def _get_severity_class(self, severity):
        """Get the severity class for a given severity value."""
        severity_classes = {
            'Low': 'success',
            'Medium': 'info',
            'High': 'warning',
            'Critical': 'danger'
        }
        return severity_classes.get(severity, 'secondary')
    
    def render_detail_view(self):
        """Render the detail view for creating, viewing, or editing a hazard."""
        # Apply CRUD styles
        apply_crud_styles()
        
        base_key = self._get_state_key_prefix()
        
        # Get view mode
        is_new = st.session_state.get(f'{base_key}_view') == 'new'
        is_edit_mode = st.session_state.get(f'{base_key}_edit_mode', False)
        
        # Get item data
        if is_new:
            item = self._create_new_item_template()
            detail_title = "New Hazard"
        else:
            item_id = st.session_state.get(f'{base_key}_selected_id')
            item = self._get_item_by_id(item_id)
            if not item:
                st.error(f"Hazard with ID {item_id} not found")
                return
            detail_title = f"{item.get('hazard_id', '')}: {item.get('hazard_type', 'Hazard')}"
        
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
                    st.info("This would generate a PDF hazard report in a production environment.")
            with col3:
                if st.button("🗑️ Delete", type="secondary", key=f"delete_{base_key}_action"):
                    st.warning("Are you sure you want to delete this hazard?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key=f"confirm_delete_{base_key}"):
                            self._delete_item(item['hazard_id'])
                            st.success("Hazard deleted successfully")
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
                        hazard_id = st.text_input("Hazard ID", value=item['hazard_id'], disabled=not is_new)
                    with col2:
                        hazard_type = st.selectbox(
                            "Hazard Type", 
                            options=[
                                '', 'Fall Hazard', 'Electrical Hazard', 'Chemical Hazard', 
                                'Mechanical Hazard', 'Confined Space', 'Fire Hazard',
                                'Ergonomic Hazard', 'Noise Hazard', 'Struck-By Hazard',
                                'Caught-In/Between Hazard'
                            ],
                            index=0 if not item['hazard_type'] else [
                                '', 'Fall Hazard', 'Electrical Hazard', 'Chemical Hazard', 
                                'Mechanical Hazard', 'Confined Space', 'Fire Hazard',
                                'Ergonomic Hazard', 'Noise Hazard', 'Struck-By Hazard',
                                'Caught-In/Between Hazard'
                            ].index(item['hazard_type'])
                        )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        identification_date = st.date_input(
                            "Identification Date", 
                            value=datetime.strptime(item['identification_date'], '%Y-%m-%d') if item['identification_date'] else datetime.now()
                        )
                    with col2:
                        status = st.selectbox(
                            "Status", 
                            options=['Open', 'In Progress', 'Mitigated', 'Closed'],
                            index=['Open', 'In Progress', 'Mitigated', 'Closed'].index(item['status'])
                        )
                    
                    location = st.text_input("Location", value=item['location'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        severity = st.selectbox(
                            "Severity", 
                            options=['', 'Low', 'Medium', 'High', 'Critical'],
                            index=0 if not item['severity'] else ['', 'Low', 'Medium', 'High', 'Critical'].index(item['severity'])
                        )
                    with col2:
                        reported_by = st.text_input("Reported By", value=item['reported_by'])
                    
                    description = st.text_area("Description", value=item['description'], height=100)
                    
                    # If status is Mitigated or Closed, show mitigation date field
                    if status in ['Mitigated', 'Closed']:
                        mitigation_date = st.date_input(
                            "Mitigation Date", 
                            value=datetime.strptime(item['mitigation_date'], '%Y-%m-%d') if item.get('mitigation_date') else datetime.now()
                        )
                    else:
                        mitigation_date = None
                    
                    return (
                        hazard_id, hazard_type, identification_date, status, location, 
                        severity, reported_by, description, mitigation_date
                    )
                
                (
                    hazard_id, hazard_type, identification_date, status, location, 
                    severity, reported_by, description, mitigation_date
                ) = render_crud_fieldset("Hazard Information", render_basic_info)
                
                # Potential Impacts Section
                def render_potential_impacts():
                    st.markdown("#### Potential Impacts")
                    
                    # Initialize or get existing potential impacts
                    potential_impacts = item.get('potential_impacts', [])
                    updated_impacts = []
                    
                    # Display existing impacts with edit capability
                    for i, impact in enumerate(potential_impacts):
                        impact_text = st.text_area(
                            f"Impact {i+1}", 
                            value=impact, 
                            height=60,
                            key=f"impact_{i}"
                        )
                        
                        if impact_text:
                            updated_impacts.append(impact_text)
                    
                    # Add new impact button
                    if st.button("Add Impact", key=f"add_impact"):
                        updated_impacts.append("")
                    
                    # Generate suggested impacts if hazard type and severity are selected
                    if hazard_type and severity and len(updated_impacts) == 0:
                        st.info("Based on the hazard type and severity, here are suggested potential impacts:")
                        suggested_impacts = self._generate_potential_impacts(hazard_type, severity)
                        
                        for i, impact in enumerate(suggested_impacts):
                            use_impact = st.checkbox(f"Use: {impact}", key=f"use_impact_{i}")
                            if use_impact:
                                updated_impacts.append(impact)
                    
                    return updated_impacts
                
                potential_impacts = render_crud_fieldset("Potential Impacts", render_potential_impacts)
                
                # Corrective Actions Section
                def render_corrective_actions():
                    st.markdown("#### Corrective Actions")
                    
                    # Initialize or get existing corrective actions
                    corrective_actions = item.get('corrective_actions', [])
                    updated_actions = []
                    
                    # Display existing actions with edit capability
                    for i, action in enumerate(corrective_actions):
                        st.markdown(f"##### Action {i+1}")
                        
                        action_text = st.text_area(
                            "Action", 
                            value=action.get('action', ''), 
                            height=60,
                            key=f"action_{i}"
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            responsible_party = st.text_input(
                                "Responsible Party", 
                                value=action.get('responsible_party', ''),
                                key=f"responsible_{i}"
                            )
                        with col2:
                            due_date = st.date_input(
                                "Due Date", 
                                value=datetime.strptime(action.get('due_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d'),
                                key=f"due_date_{i}"
                            )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            action_status = st.selectbox(
                                "Status", 
                                options=['Open', 'In Progress', 'Complete'],
                                index=['Open', 'In Progress', 'Complete'].index(action.get('status', 'Open')),
                                key=f"action_status_{i}"
                            )
                        with col2:
                            notes = st.text_input(
                                "Notes", 
                                value=action.get('notes', ''),
                                key=f"notes_{i}"
                            )
                        
                        if action_text:
                            updated_actions.append({
                                'action': action_text,
                                'responsible_party': responsible_party,
                                'due_date': due_date.strftime('%Y-%m-%d'),
                                'status': action_status,
                                'notes': notes
                            })
                        
                        st.markdown("---")
                    
                    # Add new action button
                    if st.button("Add Corrective Action", key=f"add_action"):
                        updated_actions.append({
                            'action': "",
                            'responsible_party': "",
                            'due_date': datetime.now().strftime('%Y-%m-%d'),
                            'status': "Open",
                            'notes': ""
                        })
                    
                    # Generate suggested corrective action if hazard type is selected
                    if hazard_type and len(updated_actions) == 0:
                        st.info("Based on the hazard type, here is a suggested corrective action:")
                        suggested_action = self._generate_corrective_action(hazard_type)
                        
                        use_action = st.checkbox(f"Use: {suggested_action}", key=f"use_action")
                        if use_action:
                            updated_actions.append({
                                'action': suggested_action,
                                'responsible_party': "",
                                'due_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                                'status': "Open",
                                'notes': ""
                            })
                    
                    return updated_actions
                
                corrective_actions = render_crud_fieldset("Corrective Actions", render_corrective_actions)
                
                # Form Actions
                form_actions = render_form_actions(
                    save_label="Save Hazard",
                    cancel_label="Cancel",
                    delete_label="Delete Hazard",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    # Update item with form values
                    updated_item = {
                        'hazard_id': hazard_id,
                        'identification_date': identification_date.strftime('%Y-%m-%d'),
                        'hazard_type': hazard_type,
                        'location': location,
                        'severity': severity,
                        'status': status,
                        'description': description,
                        'reported_by': reported_by,
                        'potential_impacts': potential_impacts,
                        'corrective_actions': corrective_actions,
                        'mitigation_date': mitigation_date.strftime('%Y-%m-%d') if mitigation_date else None,
                        'attachments': item.get('attachments', [])
                    }
                    
                    # Save the updated item
                    self._save_item(updated_item)
                    
                    # Show success message and return to list view
                    st.success("Hazard saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked'] and not is_new:
                    self._delete_item(item['hazard_id'])
                    st.success("Hazard deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view
            # Hazard Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Hazard Information")
            
            # Display severity badge prominently
            severity = item.get('severity', '')
            if severity:
                severity_class = self._get_severity_class(severity)
                st.markdown(f"""
                <div style="float: right; margin-top: -40px;">
                    <span class='crud-status crud-status-{severity_class}' 
                          style="font-size: 0.9rem; padding: 5px 15px;">
                        {severity} Severity
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Hazard ID:** {item['hazard_id']}")
            with col2:
                st.markdown(f"**Hazard Type:** {item['hazard_type']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Identification Date:** {item['identification_date']}")
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
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Reported By:** {item['reported_by']}")
            with col2:
                if item.get('mitigation_date'):
                    st.markdown(f"**Mitigation Date:** {item['mitigation_date']}")
            
            if item.get('description'):
                st.markdown(f"**Description:**")
                st.markdown(f"```{item['description']}```")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Potential Impacts Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Potential Impacts")
            
            potential_impacts = item.get('potential_impacts', [])
            
            if potential_impacts:
                # Display potential impacts as a list
                for impact in potential_impacts:
                    st.markdown(f"""
                    <div style="border-left: 3px solid #3498db; padding-left: 10px; margin-bottom: 10px;">
                        <div style="font-size: 0.95rem;">{impact}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No potential impacts have been identified for this hazard.")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Corrective Actions Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Corrective Actions")
            
            corrective_actions = item.get('corrective_actions', [])
            
            if corrective_actions:
                # Display corrective actions
                for i, action in enumerate(corrective_actions):
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
                                <div style="font-weight: 500;">{action['action']}</div>
                                <div style="font-size: 0.85rem; margin-top: 5px;">
                                    <strong>Responsible Party:</strong> {action.get('responsible_party', 'Unassigned')}
                                </div>
                                {f'<div style="font-size: 0.85rem; margin-top: 3px; font-style: italic;">{action.get("notes", "")}</div>' if action.get('notes') else ''}
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
                st.info("No corrective actions have been specified for this hazard.")
                
            # Add corrective action button
            if st.button("➕ Add Corrective Action", key=f"add_action_{base_key}"):
                st.session_state[f'{base_key}_add_action'] = True
                
            if st.session_state.get(f'{base_key}_add_action', False):
                with st.form(f"action_form_{base_key}"):
                    action_text = st.text_area("Action Description")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        responsible_party = st.text_input("Responsible Party")
                    with col2:
                        due_date = st.date_input("Due Date", value=datetime.now() + timedelta(days=7))
                    
                    action_cols = st.columns([1, 1])
                    with action_cols[0]:
                        save_action = st.form_submit_button("Save Action")
                    with action_cols[1]:
                        cancel_action = st.form_submit_button("Cancel")
                    
                    if save_action and action_text:
                        # Add corrective action to the hazard
                        new_action = {
                            'action': action_text,
                            'responsible_party': responsible_party,
                            'due_date': due_date.strftime('%Y-%m-%d'),
                            'status': 'Open',
                            'notes': ""
                        }
                        
                        actions = item.get('corrective_actions', [])
                        actions.append(new_action)
                        
                        # Update item with new action
                        item['corrective_actions'] = actions
                        self._save_item(item)
                        
                        st.success("Corrective action added successfully")
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
                st.info("No attachments for this hazard.")
                
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