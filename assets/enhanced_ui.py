"""
Enhanced UI styles for gcPanel

This module provides modern, professional styling improvements for the entire application,
creating a more polished user interface inspired by industry-leading construction management platforms.
"""

import streamlit as st

def apply_enhanced_styles():
    """
    Apply enhanced UI styles to the application.
    
    This function adds custom CSS to improve the overall look and feel,
    making the interface more modern, professional, and visually appealing.
    """
    st.markdown("""
    <style>
    /* Force removal of sidebar from all pages */
    [data-testid="stSidebar"] {display: none !important; width: 0 !important; min-width: 0 !important;}
    .st-emotion-cache-1cypcdb {display: none !important; width: 0 !important;}
    .st-emotion-cache-z5fcl4 {display: none !important; width: 0 !important;}
    .st-emotion-cache-15z6y4i {display: none !important; width: 0 !important;}
    .st-emotion-cache-1nm2qx3 {display: none !important; width: 0 !important;}
    section[data-testid="stSidebarUserContent"] {display: none !important; width: 0 !important;}
    .st-emotion-cache-10oheav {display: none !important; width: 0 !important;}
    [data-testid="collapsedControl"] {display: none !important; width: 0 !important;}
    nav[data-testid="stSidebar"] {display: none !important; width: 0 !important;}
    #Sidebar {display: none !important; width: 0 !important;}
    button[kind="headerNoPadding"] {display: none !important; width: 0 !important;}
    /* Adjust main content for no sidebar */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        margin-left: 0 !important;
        max-width: none !important;
        width: 100% !important;
    }
    /* Remove sidebar space */
    .st-emotion-cache-18ni7ap {
        left: 0 !important;
        width: 100% !important;
    }
    
    /* Header Styling */
    header {
        background-color: #ffffff;
        border-bottom: 1px solid #e0e0e0;
    }
    
    h1, h2, h3, h4 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    h1 {
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid #f0f0f0;
    }
    
    h2 {
        font-size: 1.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-size: 1.2rem;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }
    
    /* Card and Container Styling */
    div[data-testid="stVerticalBlock"] > div:has(div.element-container) {
        background-color: white;
        border-radius: 0.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        overflow: hidden;
    }
    
    /* White Containers */
    div[style*="background-color: white"] {
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        border-radius: 8px;
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 4px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .stButton > button[kind="primary"] {
        background-color: #2e86de;
    }
    
    .stButton > button[kind="secondary"] {
        border: 1px solid #e0e0e0;
    }
    
    /* Status Badge Styling */
    .crud-status {
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.2px;
    }
    
    .crud-status-success {
        background-color: #d4f8e8;
        color: #0a6e3f;
    }
    
    .crud-status-info {
        background-color: #d7e9f7;
        color: #0a4a7a;
    }
    
    .crud-status-warning {
        background-color: #fff4d4;
        color: #8a6400;
    }
    
    .crud-status-danger {
        background-color: #ffe8e8;
        color: #9a0c28;
    }
    
    .crud-status-secondary {
        background-color: #f0f0f0;
        color: #444444;
    }
    
    /* Table Styling */
    table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        border: 1px solid #f0f0f0;
        border-radius: 8px;
        overflow: hidden;
    }
    
    thead tr {
        background-color: #f8f9fa;
    }
    
    thead th {
        padding: 10px 15px;
        text-align: left;
        font-weight: 600;
        font-size: 0.85rem;
        color: #495057;
        border-bottom: 1px solid #e9ecef;
    }
    
    tbody tr {
        border-bottom: 1px solid #f0f0f0;
    }
    
    tbody tr:hover {
        background-color: #f9fafb;
    }
    
    tbody td {
        padding: 10px 15px;
        font-size: 0.9rem;
    }
    
    /* Form Field Styling */
    div[data-baseweb="input"] {
        border-radius: 4px;
    }
    
    div[data-baseweb="select"] {
        border-radius: 4px;
    }
    
    div[data-baseweb="textarea"] {
        border-radius: 4px;
    }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] {
        font-weight: 600;
        color: #3a506b;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem;
    }
    
    /* Sidebar Navigation Enhancement */
    [data-testid="stSidebar"] {
        background-color: #fdfdfd;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 1rem;
    }
    
    .sidebar .sidebar-content {
        background-color: #fdfdfd;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        padding: 0px 16px;
        color: #777777;
        border-radius: 4px 4px 0px 0px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #2c3e50 !important;
        font-weight: 600;
        border-top: 2px solid #2e86de;
        border-right: 1px solid #e0e0e0;
        border-left: 1px solid #e0e0e0;
    }
    
    /* Project Card Styling */
    .project-card {
        border: 1px solid #f0f0f0;
        border-radius: 8px;
        overflow: hidden;
        transition: all 0.2s ease;
    }
    
    .project-card:hover {
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    
    .project-card-header {
        background-color: #f9fafb;
        padding: 12px 15px;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .project-card-body {
        padding: 15px;
    }
    
    /* Progress Bar Styling */
    [data-testid="stProgress"] > div {
        border-radius: 10px;
    }
    
    [data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #2e86de, #60a5fa);
    }
    
    /* Dropdown & Selectbox Styling */
    div[data-baseweb="select"] > div {
        border-radius: 4px;
        border-color: #e0e0e0;
    }
    
    div[data-baseweb="select"]:hover > div {
        border-color: #2e86de;
    }
    
    /* Date Picker Styling */
    div[data-baseweb="datepicker"] button,
    div[data-baseweb="datepicker"] div[role="button"] {
        border-radius: 4px;
    }
    
    /* Responsive Layout Adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 0.5rem;
        }
        
        h1 {
            font-size: 1.5rem;
        }
        
        h2 {
            font-size: 1.3rem;
        }
        
        tbody td {
            padding: 8px 10px;
            font-size: 0.85rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_project_header(project_name, project_number="", address="", status="In Progress"):
    """
    Create a professional project header using pure Python and Streamlit components.
    
    Args:
        project_name (str): Name of the project
        project_number (str, optional): Project number/ID
        address (str, optional): Project address
        status (str, optional): Project status
    """
    # Apply custom CSS for streamlit UI
    apply_streamlit_styles()
    
    # Create three columns for the header in a single row
    col1, col2, col3 = st.columns([1, 2, 1])
    
    # First column: Logo with tower crane icon
    with col1:
        st.markdown(
            f'<div style="display: flex; align-items: center;">',
            unsafe_allow_html=True
        )
        logo_col1, logo_col2 = st.columns([0.3, 0.7])
        with logo_col1:
            st.markdown(
                '<div style="background-color: #00a8e8; padding: 8px; border-radius: 4px; '
                'display: flex; justify-content: center; align-items: center; width: 32px; height: 32px;">'
                '<span style="color: white; font-weight: bold; font-size: 14px;">gc</span>'
                '</div>',
                unsafe_allow_html=True
            )
        with logo_col2:
            st.markdown(
                '<span style="color: #2e86de; font-weight: 600; margin-left: 2px;">Panel</span>',
                unsafe_allow_html=True
            )
            # Tower crane icon - hidden reference to SVG
            show_tower_crane_icon()
    
    # Second column: Project Information
    with col2:
        st.markdown(
            f'<div style="text-align: center;">'
            f'<div style="font-weight: 600; color: #2c3e50; font-size: 0.95rem;">{project_name}</div>'
            f'<div style="color: #7f8c8d; font-size: 0.75rem;">$45.5M • 168,500 sq ft • 15 stories above ground, 2 below</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    
    # Third column: Navigation Menu
    with col3:
        # Create a pure Python navigation component
        create_navigation_dropdown()
        
    # Add a horizontal line to separate header from content
    st.markdown('<hr style="margin: 0; padding: 0; height: 1px; border: none; '
                'background-color: #e0e0e0; margin-bottom: 10px;">', 
                unsafe_allow_html=True)


def apply_streamlit_styles():
    """Apply styles using pure Python and streamlit functions"""
    # Use streamlit native functions to apply styles
    st.markdown("""
        <style>
            /* Remove padding and margin */
            .block-container {
                padding-top: 0;
                padding-bottom: 0;
                margin-top: 0;
            }
            
            /* Hide default elements */
            header {display: none;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Adjust vertical spacing */
            section.main > div:first-child {padding-top: 0 !important;}
            div[data-testid="stVerticalBlock"] {gap: 0;}
            
            /* Custom column padding */
            div[data-testid="column"] {padding: 0 !important;}
            
            /* Streamlit elements - reduce default margins */
            .stButton, .stSelectbox {margin-bottom: 0;}
            
            /* Remove button styling */
            .stButton > button {
                background-color: transparent;
                border: none;
                padding: 0;
                font-weight: normal;
                color: inherit;
            }
            
            /* Navigation styles */
            .nav-dropdown {
                margin-top: 5px;
                cursor: pointer;
                border-radius: 4px;
                padding: 5px;
                background-color: #f0f3f6;
            }
            
            /* Override button hover */
            .stButton > button:hover {
                background-color: #f5f8fd;
                color: #4a90e2;
            }
            
            /* Create space for navigation buttons */
            .nav-item {
                margin-bottom: 4px;
                text-align: left;
            }
        </style>
    """, unsafe_allow_html=True)


def show_tower_crane_icon():
    """Display the tower crane icon using streamlit"""
    # Reference to the tower crane SVG - in pure Python
    tower_crane = """
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" 
         fill="none" stroke="#2e86de" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="6" y="4" width="4" height="6"></rect>
            <line x1="8" y1="1" x2="8" y2="4"></line>
            <line x1="8" y1="10" x2="8" y2="23"></line>
            <line x1="8" y1="4" x2="16" y2="4"></line>
            <line x1="16" y1="4" x2="16" y2="10"></line>
            <line x1="16" y1="10" x2="20" y2="10"></line>
        </svg>
    """
    # Use streamlit markdown to render it
    st.markdown(tower_crane, unsafe_allow_html=True)


def create_navigation_dropdown():
    """Create a navigation dropdown using Streamlit components"""
    # Set up navigation items as a Python dictionary
    nav_items = {
        "Dashboard": "Dashboard",
        "Pre-Construction": "PreConstruction",
        "Engineering": "Engineering",
        "Field Operations": "FieldOperations",
        "Safety": "Safety", 
        "Contracts": "Contracts",
        "Cost Management": "CostManagement",
        "BIM": "BIM",
        "Closeout": "Closeout",
        "Resources": "Resources"
    }
    
    # Get current menu from Python session state
    current_menu = st.session_state.get("current_menu", "Dashboard")
    
    # Create dropdown label
    st.markdown(
        '<span style="color: #7f8c8d; font-size: 0.8rem;">Navigation</span>',
        unsafe_allow_html=True
    )
    
    # Use streamlit selectbox for dropdown
    selected_option = st.selectbox(
        label="Navigation", 
        options=list(nav_items.keys()),
        index=list(nav_items.keys()).index(next((k for k, v in nav_items.items() if v == current_menu), "Dashboard")),
        label_visibility="collapsed"
    )
    
    # Update session state when selection changes
    if selected_option and nav_items[selected_option] != current_menu:
        st.session_state.current_menu = nav_items[selected_option]
        st.rerun()


def handle_navigation_click(menu_value):
    """Handle navigation click using pure Python"""
    # Update session state with Python
    st.session_state.current_menu = menu_value
    # Force rerun with Python
    st.rerun()

def create_metrics_dashboard(metrics_data):
    """
    Create a professional metrics dashboard with cards.
    
    Args:
        metrics_data (list): List of dictionaries with metric information
            [
                {
                    'label': 'Budget',
                    'value': '$12.5M',
                    'delta': '-2.3%',
                    'delta_color': 'normal',
                    'icon': '💰'
                },
                ...
            ]
    """
    cols = st.columns(len(metrics_data))
    
    for i, metric in enumerate(metrics_data):
        with cols[i]:
            st.markdown(f"""
            <div style="background-color: white; border-radius: 8px; padding: 15px; text-align: center; 
                      box-shadow: 0 2px 5px rgba(0,0,0,0.05); border: 1px solid #f0f0f0; height: 100%;">
                <div style="font-size: 1.8rem; margin-bottom: 8px;">{metric.get('icon', '')}</div>
                <div style="font-size: 0.85rem; color: #7f8c8d; margin-bottom: 5px;">{metric['label']}</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #2c3e50;">{metric['value']}</div>
                <div style="font-size: 0.75rem; color: {'#27ae60' if 'normal' in metric.get('delta_color', '') else '#e74c3c'}; 
                         margin-top: 5px; font-weight: 500;">
                    {metric.get('delta', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)

def create_team_member_card(name, role, email, phone=None, photo_url=None):
    """
    Create a professional team member card.
    
    Args:
        name (str): Team member name
        role (str): Team member role/position
        email (str): Team member email
        phone (str, optional): Team member phone number
        photo_url (str, optional): URL to team member photo
    """
    initials = ''.join([name.split()[0][0], name.split()[-1][0]]) if len(name.split()) > 1 else name[0:2]
    
    card_html = f"""
    <div style="display: flex; background-color: white; border-radius: 8px; overflow: hidden; 
              margin-bottom: 10px; border: 1px solid #f0f0f0; padding: 12px;">
        <div style="width: 50px; height: 50px; border-radius: 25px; background-color: #3498db; 
                 color: white; display: flex; align-items: center; justify-content: center; 
                 font-weight: 600; margin-right: 15px;">
            {initials.upper()}
        </div>
        <div style="flex-grow: 1;">
            <div style="font-weight: 600; color: #2c3e50;">{name}</div>
            <div style="font-size: 0.85rem; color: #7f8c8d;">{role}</div>
            <div style="font-size: 0.8rem; margin-top: 5px; color: #2980b9;">{email}</div>
            {f'<div style="font-size: 0.8rem; color: #7f8c8d;">{phone}</div>' if phone else ''}
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def render_gantt_chart_html(tasks):
    """
    Render a professional Gantt chart using HTML/CSS.
    
    Args:
        tasks (list): List of dictionaries with task information
            [
                {
                    'name': 'Task 1',
                    'start_date': '2025-05-01',
                    'end_date': '2025-05-15',
                    'progress': 75,
                    'status': 'In Progress'
                },
                ...
            ]
    """
    # Calculate date range
    import datetime
    
    # Convert string dates to datetime objects
    for task in tasks:
        task['start_date_obj'] = datetime.datetime.strptime(task['start_date'], '%Y-%m-%d')
        task['end_date_obj'] = datetime.datetime.strptime(task['end_date'], '%Y-%m-%d')
    
    min_date = min([task['start_date_obj'] for task in tasks])
    max_date = max([task['end_date_obj'] for task in tasks])
    
    # Add some padding
    min_date = min_date - datetime.timedelta(days=3)
    max_date = max_date + datetime.timedelta(days=3)
    
    total_days = (max_date - min_date).days
    
    # Generate HTML for the Gantt chart
    gantt_html = f"""
    <div style="overflow-x: auto; margin-top: 20px;">
        <div style="min-width: 800px;">
            <div style="display: flex;">
                <div style="width: 200px; font-weight: 600; padding: 10px; 
                         background-color: #f8f9fa; border-right: 1px solid #e9ecef;">
                    Task
                </div>
                <div style="flex-grow: 1; position: relative; height: 40px; 
                         background-color: #f8f9fa; border-bottom: 1px solid #e9ecef;">
    """
    
    # Add date headers
    current_date = min_date
    while current_date <= max_date:
        position_percent = ((current_date - min_date).days / total_days) * 100
        date_str = current_date.strftime('%b %d')
        
        gantt_html += f"""
        <div style="position: absolute; left: {position_percent}%; transform: translateX(-50%); 
                  font-size: 0.75rem; top: 12px; color: #7f8c8d;">
            {date_str}
        </div>
        """
        
        current_date += datetime.timedelta(days=7)
    
    gantt_html += """
                </div>
            </div>
    """
    
    # Add tasks
    for task in tasks:
        start_percent = ((task['start_date_obj'] - min_date).days / total_days) * 100
        duration_percent = ((task['end_date_obj'] - task['start_date_obj']).days / total_days) * 100
        
        status_color = {
            'Complete': '#27ae60',
            'In Progress': '#3498db',
            'Not Started': '#95a5a6',
            'Delayed': '#e74c3c',
            'On Hold': '#f39c12'
        }.get(task.get('status', 'Not Started'), '#3498db')
        
        progress = task.get('progress', 0)
        
        gantt_html += f"""
        <div style="display: flex; border-bottom: 1px solid #f0f0f0;">
            <div style="width: 200px; padding: 10px; font-size: 0.9rem; border-right: 1px solid #f0f0f0;">
                {task['name']}
            </div>
            <div style="flex-grow: 1; position: relative; height: 40px;">
                <div style="position: absolute; left: {start_percent}%; width: {duration_percent}%; top: 10px; 
                          height: 20px; background-color: #f0f0f0; border-radius: 4px; overflow: hidden;">
                    <div style="width: {progress}%; height: 100%; background-color: {status_color};"></div>
                </div>
            </div>
        </div>
        """
    
    gantt_html += """
        </div>
    </div>
    """
    
    st.markdown(gantt_html, unsafe_allow_html=True)

def create_data_card(title, data_items, show_more_url=None):
    """
    Create a professional data card for displaying lists of items.
    
    Args:
        title (str): Card title
        data_items (list): List of dictionaries with item information
            [
                {
                    'label': 'Item 1',
                    'value': 'Value 1',
                    'status': 'Active',
                    'date': '2025-05-21'
                },
                ...
            ]
        show_more_url (str, optional): URL for "Show More" link
    """
    card_html = f"""
    <div style="background-color: white; border-radius: 8px; overflow: hidden; 
              border: 1px solid #f0f0f0; margin-bottom: 20px;">
        <div style="padding: 12px 15px; border-bottom: 1px solid #f0f0f0; 
                 background-color: #f9fafb; display: flex; justify-content: space-between; align-items: center;">
            <div style="font-weight: 600; color: #2c3e50;">{title}</div>
            {f'<a href="{show_more_url}" style="font-size: 0.8rem; color: #3498db; text-decoration: none;">Show All</a>' 
              if show_more_url else ''}
        </div>
        <div style="padding: 0;">
    """
    
    for item in data_items:
        status = item.get('status')
        status_color = {
            'Active': '#27ae60',
            'Pending': '#f39c12',
            'Complete': '#2ecc71',
            'On Hold': '#95a5a6',
            'Overdue': '#e74c3c'
        }.get(status, '#7f8c8d')
        
        card_html += f"""
        <div style="padding: 12px 15px; border-bottom: 1px solid #f0f0f0; display: flex; align-items: center;">
            <div style="flex-grow: 1;">
                <div style="font-weight: 500; color: #2c3e50;">{item['label']}</div>
                <div style="font-size: 0.85rem; color: #7f8c8d; margin-top: 3px;">{item.get('value', '')}</div>
            </div>
            <div style="display: flex; flex-direction: column; align-items: flex-end;">
                {f'<div style="font-size: 0.7rem; padding: 2px 8px; background-color: {status_color}; color: white; border-radius: 10px; margin-bottom: 5px;">{status}</div>' if status else ''}
                {f'<div style="font-size: 0.75rem; color: #7f8c8d;">{item.get("date", "")}</div>' if item.get('date') else ''}
            </div>
        </div>
        """
    
    card_html += """
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)