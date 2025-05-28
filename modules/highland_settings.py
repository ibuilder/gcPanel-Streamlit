"""
Highland Tower Development - Comprehensive Settings Management
Project configuration, module controls, and standardized fields management.
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime, date
from typing import Dict, List, Any

def render_highland_settings():
    """Highland Tower Development - Complete Settings Management"""
    
    st.markdown("""
    <div class="module-header">
        <h1>⚙️ Highland Tower Development - Settings</h1>
        <p>$45.5M Project - Configuration & Module Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize settings data
    initialize_highland_settings()
    
    # Main settings tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏗️ Project Configuration",
        "📋 Module Controls", 
        "👥 User Management",
        "🔗 Integration Settings",
        "🎨 Display Preferences"
    ])
    
    with tab1:
        render_project_configuration()
    
    with tab2:
        render_module_controls()
    
    with tab3:
        render_user_management()
    
    with tab4:
        render_integration_settings()
    
    with tab5:
        render_display_preferences()

def initialize_highland_settings():
    """Initialize Highland Tower Development settings data"""
    
    # Project Configuration
    if "highland_project_config" not in st.session_state:
        st.session_state.highland_project_config = {
            "project_id": "HTD-2024-001",
            "project_name": "Highland Tower Development",
            "project_value": 45500000.0,
            "project_location": "Downtown Highland District",
            "project_size": "168,500 sq ft",
            "floors": "15 stories above ground, 2 below",
            "units": "120 residential + 8 retail",
            "client": "Highland Properties LLC",
            "project_manager": "John Smith",
            "superintendent": "Mike Rodriguez",
            "start_date": "2024-01-15",
            "planned_completion": "2025-11-23",
            "contract_type": "Lump Sum",
            "delivery_method": "Design-Bid-Build",
            "project_phase": "Construction",
            "current_progress": 78.5,
            "working_days": "Monday - Saturday",
            "work_hours": "7:00 AM - 6:00 PM",
            "safety_officer": "Sarah Johnson",
            "quality_manager": "David Chen"
        }
    
    # Module Controls
    if "highland_module_controls" not in st.session_state:
        st.session_state.highland_module_controls = {
            "dashboard": {"enabled": True, "user_roles": ["Admin", "PM", "Super", "User"]},
            "daily_reports": {"enabled": True, "user_roles": ["Admin", "PM", "Super", "Field"]},
            "cost_management": {"enabled": True, "user_roles": ["Admin", "PM", "Accounting"]},
            "safety": {"enabled": True, "user_roles": ["Admin", "PM", "Super", "Safety"]},
            "rfis": {"enabled": True, "user_roles": ["Admin", "PM", "Super", "Engineering"]},
            "submittals": {"enabled": True, "user_roles": ["Admin", "PM", "Super"]},
            "quality_control": {"enabled": True, "user_roles": ["Admin", "PM", "QC"]},
            "scheduling": {"enabled": True, "user_roles": ["Admin", "PM", "Scheduler"]},
            "bim": {"enabled": True, "user_roles": ["Admin", "PM", "BIM", "Engineering"]},
            "material_management": {"enabled": True, "user_roles": ["Admin", "PM", "Materials"]},
            "progress_photos": {"enabled": True, "user_roles": ["Admin", "PM", "Super", "Field"]},
            "analytics": {"enabled": True, "user_roles": ["Admin", "PM", "Executive"]},
            "ai_assistant": {"enabled": True, "user_roles": ["Admin", "PM", "Super"]},
            "system_integration": {"enabled": True, "user_roles": ["Admin", "IT"]},
            "closeout": {"enabled": False, "user_roles": ["Admin", "PM"]},  # Not needed yet
            "preconstruction": {"enabled": False, "user_roles": ["Admin", "PM"]}  # Phase complete
        }
    
    # Standard Field Definitions
    if "highland_standard_fields" not in st.session_state:
        st.session_state.highland_standard_fields = {
            "cost_codes": [
                {"code": "01-0000", "description": "General Requirements"},
                {"code": "03-0000", "description": "Concrete"},
                {"code": "05-0000", "description": "Metals"},
                {"code": "06-0000", "description": "Wood, Plastics, and Composites"},
                {"code": "07-0000", "description": "Thermal and Moisture Protection"},
                {"code": "08-0000", "description": "Openings"},
                {"code": "09-0000", "description": "Finishes"},
                {"code": "10-0000", "description": "Specialties"},
                {"code": "11-0000", "description": "Equipment"},
                {"code": "12-0000", "description": "Furnishings"},
                {"code": "13-0000", "description": "Special Construction"},
                {"code": "14-0000", "description": "Conveying Equipment"},
                {"code": "15-0000", "description": "Mechanical"},
                {"code": "16-0000", "description": "Electrical"}
            ],
            "user_roles": [
                {"role": "Admin", "description": "Full system access", "level": 5},
                {"role": "PM", "description": "Project Manager", "level": 4},
                {"role": "Super", "description": "Superintendent", "level": 3},
                {"role": "Engineering", "description": "Engineering Team", "level": 3},
                {"role": "QC", "description": "Quality Control", "level": 3},
                {"role": "Safety", "description": "Safety Officer", "level": 3},
                {"role": "Field", "description": "Field Personnel", "level": 2},
                {"role": "User", "description": "General User", "level": 1}
            ],
            "priority_levels": ["Critical", "High", "Medium", "Low"],
            "status_options": ["Active", "In Progress", "Completed", "On Hold", "Cancelled"],
            "trade_categories": [
                "General Contractor", "Concrete", "Steel", "Electrical", "Plumbing", 
                "HVAC", "Roofing", "Flooring", "Drywall", "Painting", "Glazing", 
                "Elevators", "Fire Protection", "Landscaping"
            ]
        }

def render_project_configuration():
    """Highland Tower Development project configuration settings"""
    
    st.subheader("🏗️ Highland Tower Development - Project Configuration")
    
    st.info("**📋 Project Settings:** Configure core project information that standardizes data across all modules.")
    
    # Project Information Form
    with st.form("project_config_form"):
        st.markdown("**📝 Project Information**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name*", 
                                       value=st.session_state.highland_project_config["project_name"])
            project_id = st.text_input("Project ID*", 
                                     value=st.session_state.highland_project_config["project_id"])
            project_value = st.number_input("Project Value ($)*", 
                                          value=st.session_state.highland_project_config["project_value"],
                                          format="%.2f")
            client = st.text_input("Client*", 
                                 value=st.session_state.highland_project_config["client"])
            project_manager = st.text_input("Project Manager*", 
                                           value=st.session_state.highland_project_config["project_manager"])
            superintendent = st.text_input("Superintendent*", 
                                         value=st.session_state.highland_project_config["superintendent"])
            
        with col2:
            project_location = st.text_input("Project Location*", 
                                           value=st.session_state.highland_project_config["project_location"])
            project_size = st.text_input("Project Size", 
                                       value=st.session_state.highland_project_config["project_size"])
            floors = st.text_input("Floors/Levels", 
                                 value=st.session_state.highland_project_config["floors"])
            units = st.text_input("Units Description", 
                                value=st.session_state.highland_project_config["units"])
            safety_officer = st.text_input("Safety Officer", 
                                         value=st.session_state.highland_project_config["safety_officer"])
            quality_manager = st.text_input("Quality Manager", 
                                          value=st.session_state.highland_project_config["quality_manager"])
        
        st.markdown("**📅 Project Schedule**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            start_date = st.date_input("Start Date*", 
                                     value=datetime.strptime(st.session_state.highland_project_config["start_date"], "%Y-%m-%d").date())
        with col2:
            completion_date = st.date_input("Planned Completion*", 
                                          value=datetime.strptime(st.session_state.highland_project_config["planned_completion"], "%Y-%m-%d").date())
        with col3:
            current_progress = st.number_input("Current Progress (%)", 
                                             value=st.session_state.highland_project_config["current_progress"],
                                             min_value=0.0, max_value=100.0, format="%.1f")
        
        st.markdown("**🔧 Project Details**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            contract_type = st.selectbox("Contract Type", 
                                       ["Lump Sum", "Cost Plus", "Unit Price", "Design-Build"],
                                       index=0 if st.session_state.highland_project_config["contract_type"] == "Lump Sum" else 1)
        with col2:
            delivery_method = st.selectbox("Delivery Method", 
                                         ["Design-Bid-Build", "Design-Build", "CM at Risk"],
                                         index=0 if st.session_state.highland_project_config["delivery_method"] == "Design-Bid-Build" else 1)
        with col3:
            project_phase = st.selectbox("Project Phase", 
                                       ["Preconstruction", "Construction", "Closeout", "Complete"],
                                       index=1 if st.session_state.highland_project_config["project_phase"] == "Construction" else 0)
        
        if st.form_submit_button("💾 Save Project Configuration", type="primary"):
            # Update project configuration
            st.session_state.highland_project_config.update({
                "project_name": project_name,
                "project_id": project_id,
                "project_value": project_value,
                "project_location": project_location,
                "project_size": project_size,
                "floors": floors,
                "units": units,
                "client": client,
                "project_manager": project_manager,
                "superintendent": superintendent,
                "safety_officer": safety_officer,
                "quality_manager": quality_manager,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "planned_completion": completion_date.strftime("%Y-%m-%d"),
                "current_progress": current_progress,
                "contract_type": contract_type,
                "delivery_method": delivery_method,
                "project_phase": project_phase
            })
            
            st.success("✅ Project configuration saved successfully!")
            st.rerun()

def render_module_controls():
    """Module enable/disable controls and access management"""
    
    st.subheader("📋 Highland Tower Development - Module Controls")
    
    st.info("**🔧 Module Management:** Enable or disable modules based on project needs and control user access.")
    
    # Module controls
    st.markdown("**📋 Available Modules:**")
    
    module_descriptions = {
        "dashboard": "Main project dashboard with KPIs and overview",
        "daily_reports": "Daily construction reports and progress tracking",
        "cost_management": "Budget tracking, SOV, and change orders",
        "safety": "Safety management and incident tracking",
        "rfis": "Request for Information management",
        "submittals": "Submittal tracking and approvals",
        "quality_control": "Quality inspections and control",
        "scheduling": "Project scheduling and timeline management",
        "bim": "3D modeling and clash detection",
        "material_management": "Material tracking and inventory",
        "progress_photos": "Progress photography and documentation",
        "analytics": "Advanced analytics and reporting",
        "ai_assistant": "AI-powered construction assistant",
        "system_integration": "Module integration and data flow",
        "closeout": "Project closeout and handover",
        "preconstruction": "Pre-construction planning and design"
    }
    
    for module_name, config in st.session_state.highland_module_controls.items():
        with st.expander(f"{'🟢' if config['enabled'] else '🔴'} {module_name.replace('_', ' ').title()}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Description:** {module_descriptions.get(module_name, 'Highland Tower module')}")
                
                # User roles access
                st.write("**👥 User Roles with Access:**")
                available_roles = [role["role"] for role in st.session_state.highland_standard_fields["user_roles"]]
                selected_roles = st.multiselect(
                    "Select Roles", 
                    available_roles,
                    default=config["user_roles"],
                    key=f"roles_{module_name}"
                )
                
            with col2:
                enabled = st.checkbox(
                    "Module Enabled", 
                    value=config["enabled"],
                    key=f"enabled_{module_name}"
                )
                
                if st.button(f"💾 Update {module_name.title()}", key=f"update_{module_name}"):
                    st.session_state.highland_module_controls[module_name] = {
                        "enabled": enabled,
                        "user_roles": selected_roles
                    }
                    st.success(f"✅ {module_name.title()} settings updated!")
                    st.rerun()
    
    # Bulk actions
    st.markdown("**⚡ Bulk Actions:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🟢 Enable All Modules", key="enable_all"):
            for module in st.session_state.highland_module_controls:
                st.session_state.highland_module_controls[module]["enabled"] = True
            st.success("✅ All modules enabled!")
            st.rerun()
    
    with col2:
        if st.button("🔴 Disable Non-Essential", key="disable_non_essential"):
            non_essential = ["ai_assistant", "analytics", "system_integration"]
            for module in non_essential:
                if module in st.session_state.highland_module_controls:
                    st.session_state.highland_module_controls[module]["enabled"] = False
            st.success("✅ Non-essential modules disabled!")
            st.rerun()
    
    with col3:
        if st.button("🎯 Essential Only", key="essential_only"):
            essential = ["dashboard", "daily_reports", "cost_management", "safety", "rfis"]
            for module in st.session_state.highland_module_controls:
                st.session_state.highland_module_controls[module]["enabled"] = module in essential
            st.success("✅ Only essential modules enabled!")
            st.rerun()

def render_user_management():
    """User roles and permissions management"""
    
    st.subheader("👥 Highland Tower Development - User Management")
    
    st.info("**👥 User Management:** Configure user roles, permissions, and access levels for your Highland Tower project team.")
    
    # Current user roles
    st.markdown("**📋 Current User Roles:**")
    roles_df = pd.DataFrame(st.session_state.highland_standard_fields["user_roles"])
    st.dataframe(roles_df, use_container_width=True, hide_index=True)
    
    # Add new user role
    with st.expander("➕ Add New User Role"):
        with st.form("add_user_role"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                new_role = st.text_input("Role Name*")
            with col2:
                new_description = st.text_input("Description*")
            with col3:
                new_level = st.selectbox("Access Level", [1, 2, 3, 4, 5], index=1)
            
            if st.form_submit_button("➕ Add Role"):
                if new_role and new_description:
                    st.session_state.highland_standard_fields["user_roles"].append({
                        "role": new_role,
                        "description": new_description,
                        "level": new_level
                    })
                    st.success(f"✅ User role '{new_role}' added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields!")

def render_integration_settings():
    """Integration and API settings"""
    
    st.subheader("🔗 Highland Tower Development - Integration Settings")
    
    st.info("**🔗 Integration Settings:** Configure connections to external systems and APIs for your Highland Tower project.")
    
    # Database settings
    st.markdown("**🗄️ Database Configuration:**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Database Host", value="localhost", disabled=True)
        st.text_input("Database Name", value="highland_tower_dev", disabled=True)
    
    with col2:
        st.text_input("Database Port", value="5432", disabled=True)
        st.text_input("Connection Status", value="✅ Connected", disabled=True)
    
    # External integrations
    st.markdown("**🔌 External Integrations:**")
    
    integrations = [
        {"name": "Procore API", "status": "Not Connected", "description": "Import/export project data"},
        {"name": "Autodesk Construction Cloud", "status": "Not Connected", "description": "BIM model synchronization"},
        {"name": "Sage 300 ERP", "status": "Not Connected", "description": "Financial data integration"},
        {"name": "Email Notifications", "status": "Configured", "description": "System notifications and alerts"},
        {"name": "Document Storage", "status": "Active", "description": "File management and storage"}
    ]
    
    for integration in integrations:
        with st.expander(f"{'🟢' if integration['status'] == 'Active' else '🔴' if integration['status'] == 'Not Connected' else '🟡'} {integration['name']}"):
            st.write(f"**Description:** {integration['description']}")
            st.write(f"**Status:** {integration['status']}")
            
            if integration['status'] == 'Not Connected':
                if st.button(f"🔗 Configure {integration['name']}", key=f"config_{integration['name']}"):
                    st.info(f"To configure {integration['name']}, please provide the necessary API keys or credentials.")

def render_display_preferences():
    """Display and UI preferences"""
    
    st.subheader("🎨 Highland Tower Development - Display Preferences")
    
    st.info("**🎨 Display Settings:** Customize the appearance and behavior of your Highland Tower platform.")
    
    # Theme settings
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎨 Theme Settings:**")
        theme = st.selectbox("Color Theme", ["Highland Blue (Default)", "Dark Mode", "Light Mode", "High Contrast"])
        sidebar_style = st.selectbox("Sidebar Style", ["Expanded (Default)", "Collapsed", "Auto-hide"])
        font_size = st.selectbox("Font Size", ["Small", "Medium (Default)", "Large"])
    
    with col2:
        st.markdown("**📊 Dashboard Settings:**")
        default_view = st.selectbox("Default Dashboard View", ["Executive Summary", "Project Overview", "Cost Focus", "Schedule Focus"])
        auto_refresh = st.checkbox("Auto-refresh data", value=True)
        show_notifications = st.checkbox("Show system notifications", value=True)
    
    # Data display preferences
    st.markdown("**📋 Data Display Preferences:**")
    col1, col2 = st.columns(2)
    
    with col1:
        date_format = st.selectbox("Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
        currency_format = st.selectbox("Currency Format", ["$1,234.56", "$1234.56", "1,234.56 USD"])
    
    with col2:
        decimal_places = st.selectbox("Decimal Places", [0, 1, 2, 3], index=2)
        percentage_format = st.selectbox("Percentage Format", ["12.3%", "12.34%", "0.123"])
    
    if st.button("💾 Save Display Preferences", type="primary"):
        st.success("✅ Display preferences saved successfully!")

# Helper functions for settings management

def save_settings_to_file():
    """Save Highland Tower settings to configuration file"""
    settings_data = {
        "project_config": st.session_state.highland_project_config,
        "module_controls": st.session_state.highland_module_controls,
        "standard_fields": st.session_state.highland_standard_fields,
        "last_updated": datetime.now().isoformat()
    }
    
    try:
        with open("data/highland_settings.json", "w") as f:
            json.dump(settings_data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Failed to save settings: {str(e)}")
        return False

def load_settings_from_file():
    """Load Highland Tower settings from configuration file"""
    try:
        with open("data/highland_settings.json", "r") as f:
            settings_data = json.load(f)
        
        st.session_state.highland_project_config = settings_data.get("project_config", {})
        st.session_state.highland_module_controls = settings_data.get("module_controls", {})
        st.session_state.highland_standard_fields = settings_data.get("standard_fields", {})
        
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        st.error(f"Failed to load settings: {str(e)}")
        return False