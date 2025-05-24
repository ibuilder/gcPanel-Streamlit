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
    tab1, tab2, tab3, tab4 = st.tabs(["Project Details", "Project Contacts", "Project Delivery Method", "Contract Information"])
    
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
        render_project_contacts_crud()
    
    with tab3:
        st.subheader("📋 Project Delivery Method")
        st.markdown("**Configure the construction project delivery method for Highland Tower Development**")
        
        with st.form("project_delivery_method_form"):
            st.markdown("### Construction Project Delivery Methods")
            st.markdown("*Based on industry standards from AIA and construction best practices*")
            
            # Primary Delivery Method Selection
            delivery_method = st.selectbox(
                "Primary Project Delivery Method",
                options=[
                    "",
                    "Design-Bid-Build (Traditional)",
                    "Design-Build (D-B)",
                    "Construction Manager at Risk (CMAR)",
                    "Construction Manager as Advisor (CMA)",
                    "Integrated Project Delivery (IPD)",
                    "Public-Private Partnership (P3)",
                    "Build-Operate-Transfer (BOT)"
                ],
                index=0 if not project_info.get('project_delivery_method', {}).get('value') else 
                      next((i for i, option in enumerate([
                          "", "Design-Bid-Build (Traditional)", "Design-Build (D-B)",
                          "Construction Manager at Risk (CMAR)", "Construction Manager as Advisor (CMA)",
                          "Integrated Project Delivery (IPD)", "Public-Private Partnership (P3)",
                          "Build-Operate-Transfer (BOT)"
                      ]) if option == project_info.get('project_delivery_method', {}).get('value')), 0),
                help="Select the primary project delivery method being used for this project"
            )
            
            # Show delivery method description
            delivery_descriptions = {
                "Design-Bid-Build (Traditional)": "Traditional sequential approach where design is completed first, then bid, then built. Owner has separate contracts with architect and contractor.",
                "Design-Build (D-B)": "Single entity provides both design and construction services under one contract, reducing project risk and timeline.",
                "Construction Manager at Risk (CMAR)": "CM provides preconstruction services then enters into GMP contract to deliver the project, sharing construction risk.",
                "Construction Manager as Advisor (CMA)": "CM acts as owner's agent throughout design and construction, providing expertise without construction risk.",
                "Integrated Project Delivery (IPD)": "Collaborative delivery method integrating people, systems, and practices into a process that harnesses talents of all participants.",
                "Public-Private Partnership (P3)": "Long-term contract between public agency and private sector entity for public infrastructure or services.",
                "Build-Operate-Transfer (BOT)": "Private entity finances, builds, and operates facility for specified period before transferring to public sector."
            }
            
            if delivery_method and delivery_method in delivery_descriptions:
                st.info(f"**{delivery_method}:** {delivery_descriptions[delivery_method]}")
            
            st.markdown("---")
            
            # Contract Type Selection
            contract_type = st.selectbox(
                "Primary Contract Type",
                options=[
                    "",
                    "Lump Sum (Fixed Price)",
                    "Cost Plus Fixed Fee",
                    "Cost Plus Percentage",
                    "Guaranteed Maximum Price (GMP)",
                    "Unit Price Contract",
                    "Time and Materials",
                    "Design-Build Lump Sum",
                    "Progressive Design-Build"
                ],
                index=0 if not project_info.get('project_contract_type', {}).get('value') else
                      next((i for i, option in enumerate([
                          "", "Lump Sum (Fixed Price)", "Cost Plus Fixed Fee", "Cost Plus Percentage",
                          "Guaranteed Maximum Price (GMP)", "Unit Price Contract", "Time and Materials",
                          "Design-Build Lump Sum", "Progressive Design-Build"
                      ]) if option == project_info.get('project_contract_type', {}).get('value')), 0),
                help="Select the primary contract structure for the project"
            )
            
            # Procurement Strategy
            procurement_strategy = st.selectbox(
                "Procurement Strategy",
                options=[
                    "",
                    "Open Competitive Bidding",
                    "Invitation to Bid (ITB)",
                    "Request for Proposals (RFP)",
                    "Request for Qualifications (RFQ)",
                    "Negotiated Selection",
                    "Best Value Selection",
                    "Qualifications Based Selection (QBS)",
                    "Two-Step Selection Process"
                ],
                index=0 if not project_info.get('project_procurement_strategy', {}).get('value') else
                      next((i for i, option in enumerate([
                          "", "Open Competitive Bidding", "Invitation to Bid (ITB)", "Request for Proposals (RFP)",
                          "Request for Qualifications (RFQ)", "Negotiated Selection", "Best Value Selection",
                          "Qualifications Based Selection (QBS)", "Two-Step Selection Process"
                      ]) if option == project_info.get('project_procurement_strategy', {}).get('value')), 0),
                help="Select the procurement and contractor selection strategy"
            )
            
            # Delivery Method Benefits and Considerations
            if delivery_method:
                st.markdown("### Key Characteristics")
                
                benefits_considerations = {
                    "Design-Bid-Build (Traditional)": {
                        "benefits": ["Clear price before construction", "Competitive bidding", "Established legal framework", "Owner control over design"],
                        "considerations": ["Longer project duration", "Limited contractor input during design", "Potential for change orders"]
                    },
                    "Design-Build (D-B)": {
                        "benefits": ["Single point of responsibility", "Faster project delivery", "Early contractor involvement", "Reduced change orders"],
                        "considerations": ["Less owner control over design details", "Need for clear performance specifications", "Contractor selection complexity"]
                    },
                    "Construction Manager at Risk (CMAR)": {
                        "benefits": ["Early cost feedback", "Constructability input", "Phased construction possible", "Risk transfer to CM"],
                        "considerations": ["GMP negotiation complexity", "Need for experienced CM", "Potential cost growth before GMP"]
                    },
                    "Construction Manager as Advisor (CMA)": {
                        "benefits": ["Independent cost advice", "No construction conflicts of interest", "Owner retains control", "Objective oversight"],
                        "considerations": ["Owner retains construction risk", "Need separate contractor procurement", "Additional fee for CM services"]
                    },
                    "Integrated Project Delivery (IPD)": {
                        "benefits": ["Enhanced collaboration", "Shared risk/reward", "Innovation encouraged", "Reduced waste"],
                        "considerations": ["Complex contractual arrangements", "Cultural change required", "Limited legal precedent"]
                    }
                }
                
                if delivery_method in benefits_considerations:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Key Benefits:**")
                        for benefit in benefits_considerations[delivery_method]["benefits"]:
                            st.markdown(f"• {benefit}")
                    
                    with col2:
                        st.markdown("**Key Considerations:**")
                        for consideration in benefits_considerations[delivery_method]["considerations"]:
                            st.markdown(f"• {consideration}")
            
            # Submit button
            if st.form_submit_button("Save Project Delivery Method"):
                # Update delivery method fields
                updates = {
                    'project_delivery_method': delivery_method,
                    'project_contract_type': contract_type,
                    'project_procurement_strategy': procurement_strategy
                }
                
                success = True
                for key, value in updates.items():
                    if not update_project_info(key, value):
                        success = False
                
                if success:
                    st.success("Project delivery method updated successfully")
                else:
                    st.error("Error updating project delivery method")
    
    with tab4:
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
    
    # Back button
    if st.button("Return to Project Information"):
        st.session_state.current_view = "list"
        st.rerun()

def render_project_contacts_crud():
    """Render CRUD interface for project contacts with user creation and role management"""
    import json
    import uuid
    import hashlib
    from datetime import datetime
    from assets.crud_styler import apply_crud_styles
    
    # Apply CRUD styling
    apply_crud_styles()
    
    st.subheader("👥 Project Contacts Directory")
    st.markdown("**Highland Tower Development - Comprehensive Contact Management**")
    
    # Initialize contacts data file
    contacts_file = "data/project/contacts.json"
    os.makedirs(os.path.dirname(contacts_file), exist_ok=True)
    
    # Load existing contacts
    def load_contacts():
        if os.path.exists(contacts_file):
            try:
                with open(contacts_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_contacts(contacts):
        with open(contacts_file, 'w') as f:
            json.dump(contacts, f, indent=2)
    
    def create_user_account(contact):
        """Create user account with appropriate role permissions"""
        # Generate temporary password
        temp_password = f"Highland{contact['last_name']}{str(uuid.uuid4())[:6]}"
        password_hash = hashlib.sha256(temp_password.encode()).hexdigest()
        
        # Determine role based on organization type
        role_mapping = {
            "Owner/Client": "owner",
            "Architect": "architect", 
            "Engineer": "engineer",
            "General Contractor": "contractor",
            "Subcontractor": "subcontractor",
            "Consultant": "consultant",
            "City/Government": "authority",
            "Vendor/Supplier": "vendor"
        }
        
        user_role = role_mapping.get(contact['organization_type'], 'viewer')
        
        # Create user record
        user_data = {
            "id": str(uuid.uuid4()),
            "username": contact['email'],
            "email": contact['email'],
            "first_name": contact['first_name'],
            "last_name": contact['last_name'],
            "role": user_role,
            "organization": contact['organization'],
            "temp_password": temp_password,
            "password_hash": password_hash,
            "created_date": datetime.now().isoformat(),
            "contact_id": contact['id'],
            "status": "pending_activation",
            "permissions": get_role_permissions(user_role)
        }
        
        # Save user data
        users_file = "data/users/project_users.json"
        os.makedirs(os.path.dirname(users_file), exist_ok=True)
        
        users = []
        if os.path.exists(users_file):
            try:
                with open(users_file, 'r') as f:
                    users = json.load(f)
            except:
                users = []
        
        users.append(user_data)
        
        with open(users_file, 'w') as f:
            json.dump(users, f, indent=2)
        
        return user_data
    
    def get_role_permissions(role):
        """Define role-based permissions for Highland Tower Development"""
        permissions = {
            "owner": {
                "modules": ["all"],
                "actions": ["view", "create", "edit", "delete", "approve"],
                "description": "Full access to all project modules and data"
            },
            "architect": {
                "modules": ["documents", "bim", "field_operations", "meetings", "analytics"],
                "actions": ["view", "create", "edit"],
                "description": "Design documents, BIM, field coordination, meetings"
            },
            "engineer": {
                "modules": ["documents", "bim", "field_operations", "safety"],
                "actions": ["view", "create", "edit"],
                "description": "Engineering documents, BIM, field operations, safety"
            },
            "contractor": {
                "modules": ["all_except_contracts"],
                "actions": ["view", "create", "edit"],
                "description": "All modules except contract management"
            },
            "subcontractor": {
                "modules": ["documents", "field_operations", "safety", "meetings"],
                "actions": ["view", "create"],
                "description": "Field operations, safety, relevant documents"
            },
            "consultant": {
                "modules": ["documents", "meetings", "analytics"],
                "actions": ["view", "create"],
                "description": "Project documents, meetings, and analytics"
            },
            "authority": {
                "modules": ["documents", "safety", "analytics"],
                "actions": ["view"],
                "description": "Read-only access to permits, safety, compliance"
            },
            "vendor": {
                "modules": ["documents", "field_operations"],
                "actions": ["view"],
                "description": "Limited access to relevant documents and schedules"
            },
            "viewer": {
                "modules": ["documents", "analytics"],
                "actions": ["view"],
                "description": "Read-only access to basic project information"
            }
        }
        return permissions.get(role, permissions["viewer"])
    
    # Load current contacts
    contacts = load_contacts()
    
    # CRUD Actions
    action = st.radio(
        "Select Action",
        ["📋 View Contacts", "➕ Add Contact", "✏️ Edit Contact", "🗑️ Delete Contact"],
        horizontal=True
    )
    
    if action == "➕ Add Contact":
        st.markdown("### Add New Contact to Highland Tower Development")
        
        with st.form("add_contact_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name*", placeholder="John")
                last_name = st.text_input("Last Name*", placeholder="Smith")
                title = st.text_input("Job Title*", placeholder="Project Manager")
                organization = st.text_input("Organization*", placeholder="Highland Properties LLC")
            
            with col2:
                email = st.text_input("Email Address*", placeholder="john.smith@company.com")
                phone = st.text_input("Phone Number", placeholder="(555) 123-4567")
                mobile = st.text_input("Mobile Number", placeholder="(555) 987-6543")
                
                organization_type = st.selectbox(
                    "Organization Type*",
                    ["", "Owner/Client", "Architect", "Engineer", "General Contractor", 
                     "Subcontractor", "Consultant", "City/Government", "Vendor/Supplier"]
                )
            
            # Additional contact details
            st.markdown("#### Additional Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                address = st.text_area("Address", placeholder="123 Main Street\nSeattle, WA 98101")
                specialization = st.text_input("Specialization/Trade", placeholder="Structural Engineering")
            
            with col2:
                emergency_contact = st.text_input("Emergency Contact", placeholder="Name and phone")
                notes = st.text_area("Notes", placeholder="Additional information about this contact")
            
            # User account creation option
            create_account = st.checkbox(
                "🔐 Create User Account", 
                value=True,
                help="Automatically create a user account with appropriate role permissions"
            )
            
            if create_account:
                st.info("📧 A temporary password will be generated and emailed to the contact for account activation.")
            
            # Submit button
            if st.form_submit_button("➕ Add Contact", type="primary"):
                if first_name and last_name and email and organization and organization_type:
                    # Create new contact
                    new_contact = {
                        "id": str(uuid.uuid4()),
                        "first_name": first_name,
                        "last_name": last_name,
                        "full_name": f"{first_name} {last_name}",
                        "title": title,
                        "organization": organization,
                        "organization_type": organization_type,
                        "email": email,
                        "phone": phone,
                        "mobile": mobile,
                        "address": address,
                        "specialization": specialization,
                        "emergency_contact": emergency_contact,
                        "notes": notes,
                        "created_date": datetime.now().isoformat(),
                        "status": "Active",
                        "has_user_account": create_account
                    }
                    
                    # Add to contacts list
                    contacts.append(new_contact)
                    save_contacts(contacts)
                    
                    # Create user account if requested
                    if create_account:
                        user_data = create_user_account(new_contact)
                        st.success(f"✅ Contact added successfully!")
                        st.success(f"🔐 User account created for {email}")
                        st.info(f"📧 Temporary password: **{user_data['temp_password']}**")
                        st.info(f"👤 Role assigned: **{user_data['role'].title()}**")
                    else:
                        st.success(f"✅ Contact added successfully!")
                    
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (marked with *)")
    
    elif action == "📋 View Contacts":
        st.markdown("### Highland Tower Development Contact Directory")
        
        if not contacts:
            st.info("No contacts added yet. Use the 'Add Contact' option to get started.")
        else:
            # Filter and search options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                org_filter = st.selectbox(
                    "Filter by Organization Type",
                    ["All"] + list(set([c['organization_type'] for c in contacts if c.get('organization_type')]))
                )
            
            with col2:
                search_term = st.text_input("Search Contacts", placeholder="Search by name, organization, or email")
            
            with col3:
                st.metric("Total Contacts", len(contacts))
            
            # Filter contacts
            filtered_contacts = contacts
            
            if org_filter != "All":
                filtered_contacts = [c for c in filtered_contacts if c.get('organization_type') == org_filter]
            
            if search_term:
                search_term = search_term.lower()
                filtered_contacts = [
                    c for c in filtered_contacts 
                    if search_term in c.get('full_name', '').lower() or 
                       search_term in c.get('organization', '').lower() or 
                       search_term in c.get('email', '').lower()
                ]
            
            # Display contacts in cards
            for contact in filtered_contacts:
                with st.expander(f"👤 {contact['full_name']} - {contact['title']} ({contact['organization']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**📧 Email:** {contact['email']}")
                        if contact.get('phone'):
                            st.markdown(f"**📞 Phone:** {contact['phone']}")
                        if contact.get('mobile'):
                            st.markdown(f"**📱 Mobile:** {contact['mobile']}")
                        st.markdown(f"**🏢 Organization Type:** {contact['organization_type']}")
                    
                    with col2:
                        if contact.get('specialization'):
                            st.markdown(f"**⚡ Specialization:** {contact['specialization']}")
                        if contact.get('address'):
                            st.markdown(f"**📍 Address:** {contact['address']}")
                        st.markdown(f"**📅 Added:** {contact['created_date'][:10]}")
                        
                        # User account status
                        if contact.get('has_user_account'):
                            st.success("🔐 Has User Account")
                        else:
                            st.info("👤 Contact Only")
                    
                    if contact.get('notes'):
                        st.markdown(f"**📝 Notes:** {contact['notes']}")
    
    elif action == "✏️ Edit Contact":
        st.markdown("### Edit Contact Information")
        
        if not contacts:
            st.info("No contacts available to edit.")
        else:
            # Select contact to edit
            contact_options = [f"{c['full_name']} - {c['organization']}" for c in contacts]
            selected_contact_idx = st.selectbox("Select Contact to Edit", range(len(contact_options)), format_func=lambda x: contact_options[x])
            
            if selected_contact_idx is not None:
                contact = contacts[selected_contact_idx]
                
                with st.form("edit_contact_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        first_name = st.text_input("First Name*", value=contact.get('first_name', ''))
                        last_name = st.text_input("Last Name*", value=contact.get('last_name', ''))
                        title = st.text_input("Job Title*", value=contact.get('title', ''))
                        organization = st.text_input("Organization*", value=contact.get('organization', ''))
                    
                    with col2:
                        email = st.text_input("Email Address*", value=contact.get('email', ''))
                        phone = st.text_input("Phone Number", value=contact.get('phone', ''))
                        mobile = st.text_input("Mobile Number", value=contact.get('mobile', ''))
                        
                        org_types = ["Owner/Client", "Architect", "Engineer", "General Contractor", 
                                   "Subcontractor", "Consultant", "City/Government", "Vendor/Supplier"]
                        current_org_type = contact.get('organization_type', '')
                        org_idx = org_types.index(current_org_type) if current_org_type in org_types else 0
                        organization_type = st.selectbox("Organization Type*", org_types, index=org_idx)
                    
                    # Additional details
                    address = st.text_area("Address", value=contact.get('address', ''))
                    specialization = st.text_input("Specialization/Trade", value=contact.get('specialization', ''))
                    emergency_contact = st.text_input("Emergency Contact", value=contact.get('emergency_contact', ''))
                    notes = st.text_area("Notes", value=contact.get('notes', ''))
                    
                    # Submit button
                    if st.form_submit_button("💾 Update Contact", type="primary"):
                        if first_name and last_name and email and organization and organization_type:
                            # Update contact
                            contacts[selected_contact_idx].update({
                                "first_name": first_name,
                                "last_name": last_name,
                                "full_name": f"{first_name} {last_name}",
                                "title": title,
                                "organization": organization,
                                "organization_type": organization_type,
                                "email": email,
                                "phone": phone,
                                "mobile": mobile,
                                "address": address,
                                "specialization": specialization,
                                "emergency_contact": emergency_contact,
                                "notes": notes,
                                "updated_date": datetime.now().isoformat()
                            })
                            
                            save_contacts(contacts)
                            st.success("✅ Contact updated successfully!")
                            st.rerun()
                        else:
                            st.error("Please fill in all required fields (marked with *)")
    
    elif action == "🗑️ Delete Contact":
        st.markdown("### Delete Contact")
        
        if not contacts:
            st.info("No contacts available to delete.")
        else:
            contact_options = [f"{c['full_name']} - {c['organization']}" for c in contacts]
            selected_contact_idx = st.selectbox("Select Contact to Delete", range(len(contact_options)), format_func=lambda x: contact_options[x])
            
            if selected_contact_idx is not None:
                contact = contacts[selected_contact_idx]
                
                st.warning(f"⚠️ Are you sure you want to delete **{contact['full_name']}** from {contact['organization']}?")
                st.markdown("This action cannot be undone.")
                
                if contact.get('has_user_account'):
                    st.error("🔐 This contact has an associated user account that will also need to be deactivated.")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🗑️ Delete Contact", type="primary"):
                        contacts.pop(selected_contact_idx)
                        save_contacts(contacts)
                        st.success("✅ Contact deleted successfully!")
                        st.rerun()
                
                with col2:
                    if st.button("❌ Cancel"):
                        st.info("Delete operation cancelled.")
    
    # Contact statistics
    if contacts:
        st.markdown("---")
        st.markdown("### 📊 Contact Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_contacts = len(contacts)
            st.metric("Total Contacts", total_contacts)
        
        with col2:
            with_accounts = len([c for c in contacts if c.get('has_user_account')])
            st.metric("User Accounts", with_accounts)
        
        with col3:
            org_types = len(set([c['organization_type'] for c in contacts if c.get('organization_type')]))
            st.metric("Organization Types", org_types)
        
        with col4:
            organizations = len(set([c['organization'] for c in contacts if c.get('organization')]))
            st.metric("Organizations", organizations)
