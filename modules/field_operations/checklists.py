"""
Checklists module for Field Operations.

This module provides comprehensive checklist functionality including:
- Pre-built checklist templates for common construction activities
- Custom checklist creation
- Progress tracking and completion status
- Digital signatures and approvals
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
from typing import Dict, List, Any

class ChecklistManager:
    """Manages checklists and checklist templates for field operations."""
    
    def __init__(self):
        self.data_dir = "data/field_operations"
        self.templates_file = f"{self.data_dir}/checklist_templates.json"
        self.checklists_file = f"{self.data_dir}/checklists.json"
        self._ensure_data_directory()
        self._initialize_templates()
    
    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _initialize_templates(self):
        """Initialize default checklist templates if they don't exist."""
        if not os.path.exists(self.templates_file):
            default_templates = self._get_default_templates()
            self._save_templates(default_templates)
    
    def _get_default_templates(self) -> List[Dict[str, Any]]:
        """Get default checklist templates."""
        return [
            {
                "template_id": "concrete_pour",
                "name": "Concrete Pour Checklist",
                "category": "Concrete Work",
                "description": "Pre-pour inspection and quality control checklist",
                "items": [
                    {"id": 1, "description": "Verify formwork is clean and properly oiled", "required": True, "category": "Preparation"},
                    {"id": 2, "description": "Check reinforcement placement and spacing", "required": True, "category": "Reinforcement"},
                    {"id": 3, "description": "Verify concrete mix design and temperature", "required": True, "category": "Materials"},
                    {"id": 4, "description": "Check weather conditions are suitable", "required": True, "category": "Conditions"},
                    {"id": 5, "description": "Ensure proper access for concrete trucks", "required": True, "category": "Logistics"},
                    {"id": 6, "description": "Verify placement equipment is ready", "required": True, "category": "Equipment"},
                    {"id": 7, "description": "Check vibration equipment is available", "required": True, "category": "Equipment"},
                    {"id": 8, "description": "Confirm finishing tools are prepared", "required": False, "category": "Finishing"}
                ]
            },
            {
                "template_id": "electrical_rough_in",
                "name": "Electrical Rough-In Inspection",
                "category": "Electrical",
                "description": "Electrical rough-in inspection checklist before drywall",
                "items": [
                    {"id": 1, "description": "Verify all outlet boxes are properly secured", "required": True, "category": "Installation"},
                    {"id": 2, "description": "Check wire routing and support", "required": True, "category": "Installation"},
                    {"id": 3, "description": "Confirm proper wire gauge for circuits", "required": True, "category": "Compliance"},
                    {"id": 4, "description": "Verify GFCI protection where required", "required": True, "category": "Safety"},
                    {"id": 5, "description": "Check panel labeling and circuit identification", "required": True, "category": "Documentation"},
                    {"id": 6, "description": "Verify grounding and bonding connections", "required": True, "category": "Safety"},
                    {"id": 7, "description": "Test continuity of circuits", "required": True, "category": "Testing"},
                    {"id": 8, "description": "Confirm smoke detector rough-in", "required": True, "category": "Life Safety"}
                ]
            },
            {
                "template_id": "steel_erection",
                "name": "Steel Erection Safety Checklist",
                "category": "Structural Steel",
                "description": "Safety checklist for structural steel erection activities",
                "items": [
                    {"id": 1, "description": "Verify crane inspection is current", "required": True, "category": "Equipment"},
                    {"id": 2, "description": "Check rigging equipment and capacity", "required": True, "category": "Rigging"},
                    {"id": 3, "description": "Confirm fall protection systems in place", "required": True, "category": "Fall Protection"},
                    {"id": 4, "description": "Verify competent person on site", "required": True, "category": "Personnel"},
                    {"id": 5, "description": "Check weather conditions for lifting", "required": True, "category": "Conditions"},
                    {"id": 6, "description": "Ensure proper communication systems", "required": True, "category": "Communication"},
                    {"id": 7, "description": "Verify exclusion zones are established", "required": True, "category": "Safety"},
                    {"id": 8, "description": "Check connection materials availability", "required": True, "category": "Materials"}
                ]
            },
            {
                "template_id": "excavation_safety",
                "name": "Excavation Safety Checklist",
                "category": "Earthwork",
                "description": "Safety checklist for excavation and trenching operations",
                "items": [
                    {"id": 1, "description": "Verify utilities have been located and marked", "required": True, "category": "Utilities"},
                    {"id": 2, "description": "Check soil classification and conditions", "required": True, "category": "Soil Analysis"},
                    {"id": 3, "description": "Ensure proper sloping or shoring system", "required": True, "category": "Protection"},
                    {"id": 4, "description": "Verify competent person inspection", "required": True, "category": "Inspection"},
                    {"id": 5, "description": "Check atmospheric testing if required", "required": True, "category": "Atmosphere"},
                    {"id": 6, "description": "Ensure proper egress routes", "required": True, "category": "Access"},
                    {"id": 7, "description": "Verify spoil pile placement", "required": True, "category": "Materials"},
                    {"id": 8, "description": "Check water control measures", "required": True, "category": "Water Management"}
                ]
            },
            {
                "template_id": "hvac_startup",
                "name": "HVAC System Startup Checklist",
                "category": "Mechanical",
                "description": "Commissioning checklist for HVAC system startup",
                "items": [
                    {"id": 1, "description": "Verify all equipment is properly installed", "required": True, "category": "Installation"},
                    {"id": 2, "description": "Check electrical connections and power", "required": True, "category": "Electrical"},
                    {"id": 3, "description": "Verify refrigerant charges and levels", "required": True, "category": "Refrigeration"},
                    {"id": 4, "description": "Check ductwork installation and sealing", "required": True, "category": "Ductwork"},
                    {"id": 5, "description": "Test control systems and sequences", "required": True, "category": "Controls"},
                    {"id": 6, "description": "Verify air and water flow rates", "required": True, "category": "Performance"},
                    {"id": 7, "description": "Check filter installation and type", "required": True, "category": "Air Quality"},
                    {"id": 8, "description": "Test safety and alarm systems", "required": True, "category": "Safety"}
                ]
            },
            {
                "template_id": "fire_protection",
                "name": "Fire Protection System Test",
                "category": "Life Safety",
                "description": "Testing checklist for fire protection systems",
                "items": [
                    {"id": 1, "description": "Verify sprinkler head installation and spacing", "required": True, "category": "Sprinklers"},
                    {"id": 2, "description": "Check water supply pressure and flow", "required": True, "category": "Water Supply"},
                    {"id": 3, "description": "Test fire pump operation", "required": True, "category": "Pumps"},
                    {"id": 4, "description": "Verify alarm and notification devices", "required": True, "category": "Alarms"},
                    {"id": 5, "description": "Check fire department connection", "required": True, "category": "Connections"},
                    {"id": 6, "description": "Test control panel functions", "required": True, "category": "Controls"},
                    {"id": 7, "description": "Verify proper pipe support and hangers", "required": True, "category": "Installation"},
                    {"id": 8, "description": "Check system documentation", "required": True, "category": "Documentation"}
                ]
            }
        ]
    
    def _save_templates(self, templates: List[Dict[str, Any]]):
        """Save templates to file."""
        with open(self.templates_file, 'w') as f:
            json.dump(templates, f, indent=2)
    
    def get_templates(self) -> List[Dict[str, Any]]:
        """Get all checklist templates."""
        try:
            with open(self.templates_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def get_checklists(self) -> List[Dict[str, Any]]:
        """Get all active checklists."""
        try:
            with open(self.checklists_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_checklist(self, checklist: Dict[str, Any]):
        """Save a checklist."""
        checklists = self.get_checklists()
        
        # Check if updating existing checklist
        updated = False
        for i, existing in enumerate(checklists):
            if existing.get('checklist_id') == checklist.get('checklist_id'):
                checklists[i] = checklist
                updated = True
                break
        
        if not updated:
            checklists.append(checklist)
        
        with open(self.checklists_file, 'w') as f:
            json.dump(checklists, f, indent=2)


def render_checklists():
    """Render the checklists interface."""
    st.subheader("🔍 Field Checklists")
    
    # Initialize checklist manager
    if 'checklist_manager' not in st.session_state:
        st.session_state.checklist_manager = ChecklistManager()
    
    manager = st.session_state.checklist_manager
    
    # Create tabs for different checklist functions
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Active Checklists", "📝 Templates", "➕ Create New", "📊 Analytics"])
    
    with tab1:
        render_active_checklists(manager)
    
    with tab2:
        render_checklist_templates(manager)
    
    with tab3:
        render_create_checklist(manager)
    
    with tab4:
        render_checklist_analytics(manager)


def render_active_checklists(manager: ChecklistManager):
    """Render active checklists view."""
    st.markdown("### Active Checklists")
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("📋 New Checklist", key="new_checklist_btn"):
            st.session_state.show_create_checklist = True
    with col2:
        if st.button("📄 Export Report", key="export_checklists_btn"):
            st.success("Checklist report exported successfully!")
    
    # Get active checklists
    checklists = manager.get_checklists()
    
    if not checklists:
        st.info("No active checklists found. Create a new checklist from a template to get started.")
        return
    
    # Filter options
    with st.expander("Filter Options"):
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Status", ["All", "In Progress", "Completed", "Overdue"])
        with col2:
            category_filter = st.selectbox("Category", ["All", "Concrete Work", "Electrical", "Structural Steel", "Earthwork", "Mechanical", "Life Safety"])
        with col3:
            project_filter = st.selectbox("Project", ["All", "Highland Tower", "City Center", "Riverside Apartments"])
    
    # Display checklists
    for checklist in checklists:
        # Apply filters
        if status_filter != "All" and checklist.get('status') != status_filter:
            continue
        if category_filter != "All" and checklist.get('category') != category_filter:
            continue
        if project_filter != "All" and checklist.get('project') != project_filter:
            continue
        
        # Calculate completion percentage
        total_items = len(checklist.get('items', []))
        completed_items = sum(1 for item in checklist.get('items', []) if item.get('completed', False))
        completion_pct = (completed_items / total_items * 100) if total_items > 0 else 0
        
        # Status styling
        status = checklist.get('status', 'In Progress')
        status_color = {
            'Completed': '#d1fae5',
            'In Progress': '#e0f2fe',
            'Overdue': '#fee2e2'
        }.get(status, '#f5f5f4')
        
        # Create checklist card
        with st.container():
            st.markdown(f"""
            <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; margin-bottom: 16px; background-color: {status_color};">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <h4 style="margin: 0; color: #1f2937;">{checklist.get('name', 'Unnamed Checklist')}</h4>
                        <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">{checklist.get('description', '')}</p>
                        <p style="margin: 4px 0; color: #6b7280; font-size: 12px;">
                            📍 {checklist.get('project', 'Unknown Project')} • 
                            📅 {checklist.get('date_created', 'Unknown Date')} • 
                            👤 {checklist.get('inspector', 'Unknown Inspector')}
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #1f2937; font-weight: bold; font-size: 18px;">{completion_pct:.0f}%</div>
                        <div style="color: #6b7280; font-size: 12px;">{completed_items}/{total_items} items</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show checklist details button
            if st.button(f"View Details", key=f"view_{checklist.get('checklist_id')}"):
                render_checklist_details(manager, checklist)


def render_checklist_details(manager: ChecklistManager, checklist: Dict[str, Any]):
    """Render detailed view of a checklist."""
    st.markdown("---")
    st.markdown(f"### 📋 {checklist.get('name', 'Checklist Details')}")
    
    # Checklist header info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Project:** {checklist.get('project', 'N/A')}")
        st.markdown(f"**Category:** {checklist.get('category', 'N/A')}")
    with col2:
        st.markdown(f"**Inspector:** {checklist.get('inspector', 'N/A')}")
        st.markdown(f"**Date:** {checklist.get('date_created', 'N/A')}")
    with col3:
        st.markdown(f"**Status:** {checklist.get('status', 'N/A')}")
        st.markdown(f"**Priority:** {checklist.get('priority', 'Normal')}")
    
    st.markdown("---")
    
    # Group items by category
    items = checklist.get('items', [])
    categories = {}
    for item in items:
        cat = item.get('category', 'General')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    # Display items by category
    updated_items = []
    for category, cat_items in categories.items():
        st.markdown(f"#### {category}")
        
        for item in cat_items:
            col1, col2 = st.columns([1, 6])
            
            with col1:
                # Checkbox for completion
                completed = st.checkbox(
                    "", 
                    value=item.get('completed', False),
                    key=f"item_{checklist.get('checklist_id')}_{item.get('id')}"
                )
                item['completed'] = completed
            
            with col2:
                # Item description
                required_mark = " ⚠️" if item.get('required', False) else ""
                st.markdown(f"**{item.get('description', 'No description')}{required_mark}**")
                
                # Notes field
                notes = st.text_area(
                    "Notes",
                    value=item.get('notes', ''),
                    key=f"notes_{checklist.get('checklist_id')}_{item.get('id')}",
                    height=50,
                    label_visibility="collapsed",
                    placeholder="Add notes or observations..."
                )
                item['notes'] = notes
            
            updated_items.append(item)
    
    # Update checklist with new item states
    checklist['items'] = updated_items
    
    # Calculate new completion status
    total_items = len(updated_items)
    completed_items = sum(1 for item in updated_items if item.get('completed', False))
    completion_pct = (completed_items / total_items * 100) if total_items > 0 else 0
    
    if completion_pct == 100:
        checklist['status'] = 'Completed'
        checklist['completion_date'] = datetime.now().isoformat()
    elif completion_pct > 0:
        checklist['status'] = 'In Progress'
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💾 Save Progress", key=f"save_{checklist.get('checklist_id')}"):
            manager.save_checklist(checklist)
            st.success("Checklist progress saved!")
    
    with col2:
        if st.button("✅ Mark Complete", key=f"complete_{checklist.get('checklist_id')}"):
            # Mark all items as complete
            for item in checklist['items']:
                item['completed'] = True
            checklist['status'] = 'Completed'
            checklist['completion_date'] = datetime.now().isoformat()
            manager.save_checklist(checklist)
            st.success("Checklist marked as complete!")
    
    with col3:
        if st.button("📄 Generate Report", key=f"report_{checklist.get('checklist_id')}"):
            st.success("Checklist report generated successfully!")
    
    with col4:
        if st.button("🔙 Back to List", key=f"back_{checklist.get('checklist_id')}"):
            st.rerun()


def render_checklist_templates(manager: ChecklistManager):
    """Render checklist templates view."""
    st.markdown("### 📝 Checklist Templates")
    
    # Get templates
    templates = manager.get_templates()
    
    if not templates:
        st.warning("No checklist templates found.")
        return
    
    # Group templates by category
    categories = {}
    for template in templates:
        cat = template.get('category', 'General')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(template)
    
    # Display templates by category
    for category, cat_templates in categories.items():
        st.markdown(f"#### {category}")
        
        for template in cat_templates:
            with st.expander(f"📋 {template.get('name', 'Unnamed Template')}"):
                st.markdown(f"**Description:** {template.get('description', 'No description')}")
                st.markdown(f"**Number of Items:** {len(template.get('items', []))}")
                
                # Show sample items
                items = template.get('items', [])[:5]  # Show first 5 items
                if items:
                    st.markdown("**Sample Items:**")
                    for item in items:
                        required_mark = " ⚠️" if item.get('required', False) else ""
                        st.markdown(f"• {item.get('description', 'No description')}{required_mark}")
                    
                    if len(template.get('items', [])) > 5:
                        st.markdown(f"*... and {len(template.get('items', [])) - 5} more items*")
                
                # Create checklist from template button
                if st.button(f"Create Checklist", key=f"create_from_{template.get('template_id')}"):
                    st.session_state.selected_template = template
                    st.session_state.show_create_from_template = True
                    st.rerun()


def render_create_checklist(manager: ChecklistManager):
    """Render create new checklist interface."""
    st.markdown("### ➕ Create New Checklist")
    
    # Check if creating from template
    if st.session_state.get('show_create_from_template', False) and 'selected_template' in st.session_state:
        render_create_from_template(manager)
        return
    
    # Create new checklist form
    with st.form("new_checklist_form"):
        st.markdown("#### Checklist Information")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Checklist Name*", placeholder="Enter checklist name")
            project = st.selectbox("Project*", ["Highland Tower", "City Center", "Riverside Apartments"])
            inspector = st.text_input("Inspector*", placeholder="Enter inspector name")
        
        with col2:
            category = st.selectbox("Category*", ["Concrete Work", "Electrical", "Structural Steel", "Earthwork", "Mechanical", "Life Safety", "General"])
            priority = st.selectbox("Priority", ["Low", "Normal", "High", "Critical"])
            due_date = st.date_input("Due Date", value=date.today())
        
        description = st.text_area("Description", placeholder="Enter checklist description")
        
        st.markdown("#### Checklist Items")
        st.markdown("Add individual checklist items:")
        
        # Dynamic item creation
        if 'new_checklist_items' not in st.session_state:
            st.session_state.new_checklist_items = [{"description": "", "required": False, "category": "General"}]
        
        # Display current items
        for i, item in enumerate(st.session_state.new_checklist_items):
            col1, col2, col3, col4 = st.columns([4, 2, 1, 1])
            
            with col1:
                desc = st.text_input(f"Item Description", value=item['description'], key=f"item_desc_{i}")
                st.session_state.new_checklist_items[i]['description'] = desc
            
            with col2:
                cat = st.selectbox(f"Category", ["General", "Preparation", "Safety", "Quality", "Documentation"], 
                                 index=["General", "Preparation", "Safety", "Quality", "Documentation"].index(item.get('category', 'General')), 
                                 key=f"item_cat_{i}")
                st.session_state.new_checklist_items[i]['category'] = cat
            
            with col3:
                req = st.checkbox("Required", value=item['required'], key=f"item_req_{i}")
                st.session_state.new_checklist_items[i]['required'] = req
            
            with col4:
                if st.button("🗑️", key=f"delete_item_{i}") and len(st.session_state.new_checklist_items) > 1:
                    st.session_state.new_checklist_items.pop(i)
                    st.rerun()
        
        # Add new item button
        if st.button("➕ Add Item"):
            st.session_state.new_checklist_items.append({"description": "", "required": False, "category": "General"})
            st.rerun()
        
        # Submit button
        submitted = st.form_submit_button("Create Checklist")
        
        if submitted:
            if name and project and inspector:
                # Create new checklist
                checklist_id = f"custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # Filter out empty items
                items = [
                    {
                        "id": i+1,
                        "description": item['description'],
                        "required": item['required'],
                        "category": item['category'],
                        "completed": False,
                        "notes": ""
                    }
                    for i, item in enumerate(st.session_state.new_checklist_items)
                    if item['description'].strip()
                ]
                
                if items:
                    new_checklist = {
                        "checklist_id": checklist_id,
                        "name": name,
                        "description": description,
                        "project": project,
                        "category": category,
                        "inspector": inspector,
                        "priority": priority,
                        "status": "In Progress",
                        "date_created": datetime.now().strftime('%Y-%m-%d'),
                        "due_date": due_date.strftime('%Y-%m-%d'),
                        "items": items
                    }
                    
                    manager.save_checklist(new_checklist)
                    st.success(f"Checklist '{name}' created successfully!")
                    
                    # Reset form
                    st.session_state.new_checklist_items = [{"description": "", "required": False, "category": "General"}]
                else:
                    st.error("Please add at least one checklist item.")
            else:
                st.error("Please fill in all required fields.")


def render_create_from_template(manager: ChecklistManager):
    """Render create checklist from template interface."""
    template = st.session_state.selected_template
    
    st.markdown(f"### Creating from Template: {template.get('name')}")
    st.markdown(f"**Template Description:** {template.get('description')}")
    
    with st.form("create_from_template_form"):
        st.markdown("#### Project Information")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Checklist Name*", value=template.get('name', ''))
            project = st.selectbox("Project*", ["Highland Tower", "City Center", "Riverside Apartments"])
            inspector = st.text_input("Inspector*", placeholder="Enter inspector name")
        
        with col2:
            priority = st.selectbox("Priority", ["Low", "Normal", "High", "Critical"], index=1)
            due_date = st.date_input("Due Date", value=date.today())
        
        description = st.text_area("Description", value=template.get('description', ''))
        
        st.markdown("#### Template Items Preview")
        st.markdown(f"This checklist will include {len(template.get('items', []))} items:")
        
        # Show template items
        for item in template.get('items', []):
            required_mark = " ⚠️" if item.get('required', False) else ""
            st.markdown(f"• **{item.get('category', 'General')}:** {item.get('description', 'No description')}{required_mark}")
        
        # Submit button
        submitted = st.form_submit_button("Create Checklist from Template")
        
        if submitted:
            if name and project and inspector:
                # Create checklist from template
                checklist_id = f"template_{template.get('template_id')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # Copy template items
                items = [
                    {
                        "id": item.get('id'),
                        "description": item.get('description'),
                        "required": item.get('required', False),
                        "category": item.get('category', 'General'),
                        "completed": False,
                        "notes": ""
                    }
                    for item in template.get('items', [])
                ]
                
                new_checklist = {
                    "checklist_id": checklist_id,
                    "template_id": template.get('template_id'),
                    "name": name,
                    "description": description,
                    "project": project,
                    "category": template.get('category'),
                    "inspector": inspector,
                    "priority": priority,
                    "status": "In Progress",
                    "date_created": datetime.now().strftime('%Y-%m-%d'),
                    "due_date": due_date.strftime('%Y-%m-%d'),
                    "items": items
                }
                
                manager.save_checklist(new_checklist)
                st.success(f"Checklist '{name}' created successfully from template!")
                
                # Reset state
                del st.session_state.selected_template
                st.session_state.show_create_from_template = False
                st.rerun()
            else:
                st.error("Please fill in all required fields.")
    
    # Cancel button
    if st.button("Cancel"):
        del st.session_state.selected_template
        st.session_state.show_create_from_template = False
        st.rerun()


def render_checklist_analytics(manager: ChecklistManager):
    """Render checklist analytics and reporting."""
    st.markdown("### 📊 Checklist Analytics")
    
    checklists = manager.get_checklists()
    
    if not checklists:
        st.info("No checklist data available for analytics.")
        return
    
    # Calculate metrics
    total_checklists = len(checklists)
    completed_checklists = sum(1 for c in checklists if c.get('status') == 'Completed')
    in_progress_checklists = sum(1 for c in checklists if c.get('status') == 'In Progress')
    
    # Calculate average completion rate
    total_items = sum(len(c.get('items', [])) for c in checklists)
    completed_items = sum(sum(1 for item in c.get('items', []) if item.get('completed', False)) for c in checklists)
    avg_completion_rate = (completed_items / total_items * 100) if total_items > 0 else 0
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Checklists", total_checklists)
    
    with col2:
        st.metric("Completed", completed_checklists, f"{(completed_checklists/total_checklists*100):.1f}%")
    
    with col3:
        st.metric("In Progress", in_progress_checklists)
    
    with col4:
        st.metric("Avg Completion Rate", f"{avg_completion_rate:.1f}%")
    
    # Checklist completion by category
    st.markdown("#### Completion by Category")
    
    category_data = {}
    for checklist in checklists:
        category = checklist.get('category', 'General')
        status = checklist.get('status', 'Unknown')
        
        if category not in category_data:
            category_data[category] = {'Completed': 0, 'In Progress': 0, 'Overdue': 0}
        
        if status in category_data[category]:
            category_data[category][status] += 1
    
    if category_data:
        category_df = pd.DataFrame(category_data).T.fillna(0)
        st.bar_chart(category_df)
    
    # Recent activity
    st.markdown("#### Recent Checklist Activity")
    
    # Sort checklists by date
    sorted_checklists = sorted(checklists, key=lambda x: x.get('date_created', ''), reverse=True)
    
    for checklist in sorted_checklists[:5]:  # Show latest 5
        total_items = len(checklist.get('items', []))
        completed_items = sum(1 for item in checklist.get('items', []) if item.get('completed', False))
        completion_pct = (completed_items / total_items * 100) if total_items > 0 else 0
        
        st.markdown(f"""
        **{checklist.get('name', 'Unnamed')}** - {checklist.get('project', 'Unknown Project')}  
        Status: {checklist.get('status', 'Unknown')} | Progress: {completion_pct:.0f}% | Date: {checklist.get('date_created', 'Unknown')}
        """)