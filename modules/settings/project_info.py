import streamlit as st
import os
from utils.database import get_db_connection
from utils.auth import check_permission

# Module metadata
MODULE_DISPLAY_NAME = "Project Information"
MODULE_ICON = "info"

def init_database():
    """Initialize the database tables for project information"""
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        cursor = conn.cursor()
        
        # Create project_info table (using SQLite syntax)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key VARCHAR(100) NOT NULL UNIQUE,
                value TEXT,
                description TEXT,
                updated_by INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Check if default keys exist, if not add them
        default_keys = [
            ('project_name', '', 'Name of the project'),
            ('project_number', '', 'Project identifier or number'),
            ('project_address', '', 'Physical address of the project'),
            ('project_city', '', 'City of the project'),
            ('project_state', '', 'State of the project'),
            ('project_zip', '', 'ZIP code of the project'),
            ('project_country', 'USA', 'Country of the project'),
            ('owner_name', '', 'Name of the project owner'),
            ('owner_contact', '', 'Contact person for the owner'),
            ('owner_email', '', 'Email address for the owner contact'),
            ('owner_phone', '', 'Phone number for the owner contact'),
            ('architect_name', '', 'Name of the project architect'),
            ('architect_contact', '', 'Contact person for the architect'),
            ('architect_email', '', 'Email address for the architect contact'),
            ('architect_phone', '', 'Phone number for the architect contact'),
            ('contractor_name', '', 'Name of the general contractor'),
            ('contractor_contact', '', 'Contact person for the contractor'),
            ('contractor_email', '', 'Email address for the contractor contact'),
            ('contractor_phone', '', 'Phone number for the contractor contact'),
            ('project_start_date', '', 'Project start date'),
            ('project_end_date', '', 'Projected completion date'),
            ('project_description', '', 'Brief description of the project'),
            ('project_type', '', 'Type of construction project'),
            ('project_value', '', 'Total project value/budget'),
            ('project_square_footage', '', 'Total square footage of the project'),
            ('project_stories', '', 'Number of stories/floors'),
            ('project_delivery_method', '', 'Construction project delivery method'),
            ('project_contract_type', '', 'Primary contract structure'),
            ('project_procurement_strategy', '', 'Procurement and bidding strategy'),
            ('project_timezone', 'America/New_York', 'Project timezone')
        ]
        
        for key, default_value, description in default_keys:
            # Check if key already exists (SQLite doesn't support ON CONFLICT)
            cursor.execute("SELECT COUNT(*) FROM project_info WHERE key = ?", (key,))
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                    INSERT INTO project_info (key, value, description)
                    VALUES (?, ?, ?)
                ''', (key, default_value, description))
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        st.error(f"Error initializing project info database: {str(e)}")

def get_project_info():
    """Get all project information from the database"""
    try:
        conn = get_db_connection()
        if not conn:
            return {}
            
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT key, value, description
            FROM project_info
            ORDER BY id
        ''')
        
        project_info = {}
        for key, value, description in cursor.fetchall():
            project_info[key] = {
                'value': value,
                'description': description
            }
        
        cursor.close()
        conn.close()
        
        return project_info
        
    except Exception as e:
        st.error(f"Error fetching project info: {str(e)}")
        return {}

def update_project_info(key, value):
    """Update a project information field"""
    try:
        conn = get_db_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        
        # SQLite syntax for update with placeholders
        cursor.execute('''
            UPDATE project_info
            SET value = ?, updated_by = ?, updated_at = CURRENT_TIMESTAMP
            WHERE key = ?
        ''', (value, st.session_state.get('user_id'), key))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        st.error(f"Error updating project info: {str(e)}")
        return False

def render_list():
    """Render the project information overview"""
    st.title("Project Information")
    
    # Initialize database
    init_database()
    
    # Check permission
    if not check_permission('read'):
        st.error("You don't have permission to view project information")
        return
    
    # Get project info
    project_info = get_project_info()
    
    if not project_info:
        st.warning("Project information could not be loaded")
        return
    
    # Display project info in sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Project Details")
        
        # Project name
        if project_info.get('project_name', {}).get('value'):
            st.header(project_info['project_name']['value'])
        
        # Project description
        if project_info.get('project_description', {}).get('value'):
            st.write(project_info['project_description']['value'])
        
        # Project number
        if project_info.get('project_number', {}).get('value'):
            st.write(f"**Project Number:** {project_info['project_number']['value']}")
        
        # Project address
        address_parts = []
        if project_info.get('project_address', {}).get('value'):
            address_parts.append(project_info['project_address']['value'])
        
        city_state_zip = []
        if project_info.get('project_city', {}).get('value'):
            city_state_zip.append(project_info['project_city']['value'])
        
        if project_info.get('project_state', {}).get('value'):
            city_state_zip.append(project_info['project_state']['value'])
        
        if project_info.get('project_zip', {}).get('value'):
            city_state_zip.append(project_info['project_zip']['value'])
        
        if city_state_zip:
            address_parts.append(', '.join(city_state_zip))
        
        if project_info.get('project_country', {}).get('value'):
            address_parts.append(project_info['project_country']['value'])
        
        if address_parts:
            st.write("**Address:**")
            for part in address_parts:
                st.write(part)
        
        # Project dates
        dates = []
        if project_info.get('project_start_date', {}).get('value'):
            dates.append(f"**Start Date:** {project_info['project_start_date']['value']}")
        
        if project_info.get('project_end_date', {}).get('value'):
            dates.append(f"**End Date:** {project_info['project_end_date']['value']}")
        
        if dates:
            st.write("**Project Schedule:**")
            for date in dates:
                st.write(date)
        
        # Project metrics
        metrics = []
        if project_info.get('project_value', {}).get('value'):
            metrics.append(f"**Project Value:** {project_info['project_value']['value']}")
        
        if project_info.get('project_square_footage', {}).get('value'):
            metrics.append(f"**Square Footage:** {project_info['project_square_footage']['value']}")
        
        if project_info.get('project_stories', {}).get('value'):
            metrics.append(f"**Stories:** {project_info['project_stories']['value']}")
        
        if project_info.get('project_type', {}).get('value'):
            metrics.append(f"**Project Type:** {project_info['project_type']['value']}")
        
        if metrics:
            st.write("**Project Metrics:**")
            for metric in metrics:
                st.write(metric)
        
        # Project Delivery Method Section
        st.markdown("---")
        st.subheader("📋 Project Delivery Method")
        
        delivery_info = []
        if project_info.get('project_delivery_method', {}).get('value'):
            delivery_info.append(f"**Delivery Method:** {project_info['project_delivery_method']['value']}")
        
        if project_info.get('project_contract_type', {}).get('value'):
            delivery_info.append(f"**Contract Type:** {project_info['project_contract_type']['value']}")
        
        if project_info.get('project_procurement_strategy', {}).get('value'):
            delivery_info.append(f"**Procurement Strategy:** {project_info['project_procurement_strategy']['value']}")
        
        if delivery_info:
            for info in delivery_info:
                st.write(info)
        else:
            st.info("Project delivery method not yet defined. Use the edit form to configure.")
    
    with col2:
        st.subheader("Project Contacts")
        
        # Owner
        owner_info = []
        if project_info.get('owner_name', {}).get('value'):
            owner_info.append(f"**Name:** {project_info['owner_name']['value']}")
        
        if project_info.get('owner_contact', {}).get('value'):
            owner_info.append(f"**Contact:** {project_info['owner_contact']['value']}")
        
        if project_info.get('owner_email', {}).get('value'):
            owner_info.append(f"**Email:** {project_info['owner_email']['value']}")
        
        if project_info.get('owner_phone', {}).get('value'):
            owner_info.append(f"**Phone:** {project_info['owner_phone']['value']}")
        
        if owner_info:
            st.write("**Owner:**")
            for info in owner_info:
                st.write(info)
            st.write("")
        
        # Architect
        architect_info = []
        if project_info.get('architect_name', {}).get('value'):
            architect_info.append(f"**Name:** {project_info['architect_name']['value']}")
        
        if project_info.get('architect_contact', {}).get('value'):
            architect_info.append(f"**Contact:** {project_info['architect_contact']['value']}")
        
        if project_info.get('architect_email', {}).get('value'):
            architect_info.append(f"**Email:** {project_info['architect_email']['value']}")
        
        if project_info.get('architect_phone', {}).get('value'):
            architect_info.append(f"**Phone:** {project_info['architect_phone']['value']}")
        
        if architect_info:
            st.write("**Architect:**")
            for info in architect_info:
                st.write(info)
            st.write("")
        
        # Contractor
        contractor_info = []
        if project_info.get('contractor_name', {}).get('value'):
            contractor_info.append(f"**Name:** {project_info['contractor_name']['value']}")
        
        if project_info.get('contractor_contact', {}).get('value'):
            contractor_info.append(f"**Contact:** {project_info['contractor_contact']['value']}")
        
        if project_info.get('contractor_email', {}).get('value'):
            contractor_info.append(f"**Email:** {project_info['contractor_email']['value']}")
        
        if project_info.get('contractor_phone', {}).get('value'):
            contractor_info.append(f"**Phone:** {project_info['contractor_phone']['value']}")
        
        if contractor_info:
            st.write("**Contractor:**")
            for info in contractor_info:
                st.write(info)
            st.write("")
    
    # Edit button
    if check_permission('update'):
        if st.button("Edit Project Information"):
            st.session_state.current_view = "form"
            st.rerun()

def render_view():
    """Render the project information detail view"""
    # Redirect to list view as it already shows all details
    render_list()

def render_form():
    """Render the form for editing project information"""
    st.title("Edit Project Information")
    
    # Check permission
    if not check_permission('update'):
        st.error("You don't have permission to update project information")
        return
    
    # Get project info
    project_info = get_project_info()
    
    if not project_info:
        st.warning("Project information could not be loaded")
        return
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Project Details", "Project Contacts", "Project Delivery Method", "Contract Information", "Project Settings"])
    
    with tab1:
        st.subheader("Project Details")
        
        with st.form("project_details_form"):
            # Project Name
            project_name = st.text_input(
                "Project Name",
                value=project_info.get('project_name', {}).get('value', ''),
                help=project_info.get('project_name', {}).get('description', '')
            )
            
            # Project Number
            project_number = st.text_input(
                "Project Number",
                value=project_info.get('project_number', {}).get('value', ''),
                help=project_info.get('project_number', {}).get('description', '')
            )
            
            # Project Description
            project_description = st.text_area(
                "Project Description",
                value=project_info.get('project_description', {}).get('value', ''),
                help=project_info.get('project_description', {}).get('description', '')
            )
            
            # Project Type
            project_type = st.text_input(
                "Project Type",
                value=project_info.get('project_type', {}).get('value', ''),
                help=project_info.get('project_type', {}).get('description', '')
            )
            
            # Address information
            col1, col2 = st.columns(2)
            
            with col1:
                project_address = st.text_input(
                    "Address",
                    value=project_info.get('project_address', {}).get('value', ''),
                    help=project_info.get('project_address', {}).get('description', '')
                )
                
                project_city = st.text_input(
                    "City",
                    value=project_info.get('project_city', {}).get('value', ''),
                    help=project_info.get('project_city', {}).get('description', '')
                )
            
            with col2:
                project_state = st.text_input(
                    "State",
                    value=project_info.get('project_state', {}).get('value', ''),
                    help=project_info.get('project_state', {}).get('description', '')
                )
                
                project_zip = st.text_input(
                    "ZIP Code",
                    value=project_info.get('project_zip', {}).get('value', ''),
                    help=project_info.get('project_zip', {}).get('description', '')
                )
                
                project_country = st.text_input(
                    "Country",
                    value=project_info.get('project_country', {}).get('value', 'USA'),
                    help=project_info.get('project_country', {}).get('description', '')
                )
            
            # Project dates
            col1, col2 = st.columns(2)
            
            with col1:
                project_start_date = st.text_input(
                    "Start Date (YYYY-MM-DD)",
                    value=project_info.get('project_start_date', {}).get('value', ''),
                    help=project_info.get('project_start_date', {}).get('description', '')
                )
            
            with col2:
                project_end_date = st.text_input(
                    "End Date (YYYY-MM-DD)",
                    value=project_info.get('project_end_date', {}).get('value', ''),
                    help=project_info.get('project_end_date', {}).get('description', '')
                )
            
            # Project metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                project_value = st.text_input(
                    "Project Value ($)",
                    value=project_info.get('project_value', {}).get('value', ''),
                    help=project_info.get('project_value', {}).get('description', '')
                )
            
            with col2:
                project_square_footage = st.text_input(
                    "Square Footage",
                    value=project_info.get('project_square_footage', {}).get('value', ''),
                    help=project_info.get('project_square_footage', {}).get('description', '')
                )
            
            with col3:
                project_stories = st.text_input(
                    "Number of Stories",
                    value=project_info.get('project_stories', {}).get('value', ''),
                    help=project_info.get('project_stories', {}).get('description', '')
                )
            
            # Submit button
            if st.form_submit_button("Save Project Details"):
                # Update all the fields
                updates = {
                    'project_name': project_name,
                    'project_number': project_number,
                    'project_description': project_description,
                    'project_type': project_type,
                    'project_address': project_address,
                    'project_city': project_city,
                    'project_state': project_state,
                    'project_zip': project_zip,
                    'project_country': project_country,
                    'project_start_date': project_start_date,
                    'project_end_date': project_end_date,
                    'project_value': project_value,
                    'project_square_footage': project_square_footage,
                    'project_stories': project_stories
                }
                
                success = True
                for key, value in updates.items():
                    if not update_project_info(key, value):
                        success = False
                
                if success:
                    st.success("Project details updated successfully")
                else:
                    st.error("Error updating project details")
    
    with tab2:
        st.subheader("Project Contacts")
        
        with st.form("project_contacts_form"):
            # Owner information
            st.write("**Owner Information**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                owner_name = st.text_input(
                    "Owner Name",
                    value=project_info.get('owner_name', {}).get('value', ''),
                    help=project_info.get('owner_name', {}).get('description', '')
                )
                
                owner_contact = st.text_input(
                    "Contact Person",
                    value=project_info.get('owner_contact', {}).get('value', ''),
                    help=project_info.get('owner_contact', {}).get('description', '')
                )
            
            with col2:
                owner_email = st.text_input(
                    "Email",
                    value=project_info.get('owner_email', {}).get('value', ''),
                    help=project_info.get('owner_email', {}).get('description', '')
                )
                
                owner_phone = st.text_input(
                    "Phone",
                    value=project_info.get('owner_phone', {}).get('value', ''),
                    help=project_info.get('owner_phone', {}).get('description', '')
                )
            
            st.write("---")
            
            # Architect information
            st.write("**Architect Information**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                architect_name = st.text_input(
                    "Architect Name",
                    value=project_info.get('architect_name', {}).get('value', ''),
                    help=project_info.get('architect_name', {}).get('description', '')
                )
                
                architect_contact = st.text_input(
                    "Contact Person",
                    value=project_info.get('architect_contact', {}).get('value', ''),
                    help=project_info.get('architect_contact', {}).get('description', '')
                )
            
            with col2:
                architect_email = st.text_input(
                    "Email",
                    value=project_info.get('architect_email', {}).get('value', ''),
                    help=project_info.get('architect_email', {}).get('description', '')
                )
                
                architect_phone = st.text_input(
                    "Phone",
                    value=project_info.get('architect_phone', {}).get('value', ''),
                    help=project_info.get('architect_phone', {}).get('description', '')
                )
            
            st.write("---")
            
            # Contractor information
            st.write("**Contractor Information**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                contractor_name = st.text_input(
                    "Contractor Name",
                    value=project_info.get('contractor_name', {}).get('value', ''),
                    help=project_info.get('contractor_name', {}).get('description', '')
                )
                
                contractor_contact = st.text_input(
                    "Contact Person",
                    value=project_info.get('contractor_contact', {}).get('value', ''),
                    help=project_info.get('contractor_contact', {}).get('description', '')
                )
            
            with col2:
                contractor_email = st.text_input(
                    "Email",
                    value=project_info.get('contractor_email', {}).get('value', ''),
                    help=project_info.get('contractor_email', {}).get('description', '')
                )
                
                contractor_phone = st.text_input(
                    "Phone",
                    value=project_info.get('contractor_phone', {}).get('value', ''),
                    help=project_info.get('contractor_phone', {}).get('description', '')
                )
            
            # Submit button
            if st.form_submit_button("Save Contact Information"):
                # Update all the fields
                updates = {
                    'owner_name': owner_name,
                    'owner_contact': owner_contact,
                    'owner_email': owner_email,
                    'owner_phone': owner_phone,
                    'architect_name': architect_name,
                    'architect_contact': architect_contact,
                    'architect_email': architect_email,
                    'architect_phone': architect_phone,
                    'contractor_name': contractor_name,
                    'contractor_contact': contractor_contact,
                    'contractor_email': contractor_email,
                    'contractor_phone': contractor_phone
                }
                
                success = True
                for key, value in updates.items():
                    if not update_project_info(key, value):
                        success = False
                
                if success:
                    st.success("Contact information updated successfully")
                else:
                    st.error("Error updating contact information")
    
    with tab3:
        st.subheader("AIA Contract Document Numbering")
        st.markdown("**Configure contract documents using the official AIA numbering system**")
        
        with st.form("aia_contract_numbering_form"):
            st.markdown("#### AIA Document Number Format: **SERIES-TYPE-DELIVERY-SEQUENCE-EDITION**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # AIA Series
                aia_series = st.selectbox(
                    "AIA Document Series",
                    options=[
                        "A - Owner-Architect Agreements",
                        "B - Owner-Contractor Agreements", 
                        "C - Other Agreements",
                        "D - Documents",
                        "G - Forms for Contract Administration and Project Management"
                    ],
                    index=1,  # Default to B - Owner-Contractor
                    help="Select the AIA document series that applies to this project"
                )
                
                # AIA Type
                aia_type = st.selectbox(
                    "Document Type",
                    options=[
                        "1 - Prime Agreements",
                        "2 - Conditions or Scope of the Agreements",
                        "3 - Bonds or Qualifications",
                        "4 - Agreements between Prime and Sub-Contractors",
                        "5 - Guides",
                        "7 - Bid Documents and Construction Forms",
                        "8 - Forms or Documents Specific to the Architect"
                    ],
                    index=0,  # Default to 1 - Prime Agreements
                    help="Select the type of contract document"
                )
                
                # Project Delivery Method
                aia_delivery = st.selectbox(
                    "Project Delivery Method",
                    options=[
                        "0 - Traditional Design-Bid-Build",
                        "1 - Design-Build",
                        "2 - Construction Manager as Adviser",
                        "3 - Construction Manager as Constructor", 
                        "4 - Integrated Project Delivery (IPD)",
                        "5 - Public-Private Partnership",
                        "6 - Multiple Prime Contracting"
                    ],
                    index=0,  # Default to Traditional
                    help="Select the project delivery method being used"
                )
            
            with col2:
                # Sequence Number
                aia_sequence = st.selectbox(
                    "Document Sequence",
                    options=[
                        "1 - First in Series",
                        "2 - Second in Series", 
                        "3 - Third in Series",
                        "4 - Fourth in Series",
                        "5 - Fifth in Series"
                    ],
                    index=0,  # Default to First
                    help="Select the sequence number for this document type"
                )
                
                # Edition Year
                aia_edition = st.selectbox(
                    "AIA Document Edition",
                    options=[
                        "2017 - 2017 Edition",
                        "2014 - 2014 Edition",
                        "2007 - 2007 Edition",
                        "1997 - 1997 Edition"
                    ],
                    index=0,  # Default to 2017
                    help="Select the AIA document edition year"
                )
                
                # Generated Contract Number Display
                st.markdown("#### Generated Contract Number:")
                series_code = aia_series.split(' - ')[0]
                type_code = aia_type.split(' - ')[0] 
                delivery_code = aia_delivery.split(' - ')[0]
                sequence_code = aia_sequence.split(' - ')[0]
                edition_code = aia_edition.split(' - ')[0]
                
                contract_number = f"{series_code}{type_code}{delivery_code}{sequence_code}™–{edition_code}"
                st.code(contract_number, language=None)
                
                st.markdown("**Highland Tower Development Primary Contract:**")
                st.markdown(f"**{contract_number}**")
            
            # Contract Details
            st.markdown("---")
            st.markdown("#### Contract Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                contract_title = st.text_input(
                    "Contract Title",
                    value=project_info.get('contract_title', {}).get('value', 'Highland Tower Development Construction Agreement'),
                    help="Official title of the contract document"
                )
                
                contract_value = st.text_input(
                    "Contract Value",
                    value=project_info.get('contract_value', {}).get('value', '$45,500,000'),
                    help="Total contract value for the project"
                )
            
            with col2:
                contract_date = st.date_input(
                    "Contract Execution Date",
                    help="Date when the contract was executed"
                )
                
                retainage_percentage = st.number_input(
                    "Retainage Percentage",
                    min_value=0.0,
                    max_value=15.0,
                    value=5.0,
                    step=0.5,
                    help="Percentage of retainage to be held"
                )
            
            # Submit button
            if st.form_submit_button("Save Contract Information", type="primary"):
                # Update contract information
                updates = {
                    'aia_series': aia_series,
                    'aia_type': aia_type,
                    'aia_delivery': aia_delivery,
                    'aia_sequence': aia_sequence,
                    'aia_edition': aia_edition,
                    'contract_number': contract_number,
                    'contract_title': contract_title,
                    'contract_value': contract_value,
                    'contract_date': str(contract_date),
                    'retainage_percentage': str(retainage_percentage)
                }
                
                success = True
                for key, value in updates.items():
                    if not update_project_info(key, value):
                        success = False
                
                if success:
                    st.success(f"✅ Contract information updated successfully! Contract Number: **{contract_number}**")
                else:
                    st.error("Error updating contract information")
    
    with tab4:
        st.subheader("Project Settings")
        
        with st.form("project_settings_form"):
            # Timezone
            project_timezone = st.selectbox(
                "Project Timezone",
                options=[
                    "America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles",
                    "America/Anchorage", "America/Honolulu", "America/Phoenix", "America/Puerto_Rico"
                ],
                index=0 if project_info.get('project_timezone', {}).get('value', '') not in [
                    "America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles",
                    "America/Anchorage", "America/Honolulu", "America/Phoenix", "America/Puerto_Rico"
                ] else [
                    "America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles",
                    "America/Anchorage", "America/Honolulu", "America/Phoenix", "America/Puerto_Rico"
                ].index(project_info.get('project_timezone', {}).get('value', '')),
                help=project_info.get('project_timezone', {}).get('description', '')
            )
            
            # Submit button
            if st.form_submit_button("Save Project Settings"):
                # Update the fields
                if update_project_info('project_timezone', project_timezone):
                    st.success("Project settings updated successfully")
                else:
                    st.error("Error updating project settings")
    
    # Back button
    if st.button("Return to Project Information"):
        st.session_state.current_view = "list"
        st.rerun()
