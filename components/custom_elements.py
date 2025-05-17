import streamlit as st

def card(title, content, width="100%"):
    """Create a styled card component with title and content
    
    Args:
        title (str): The card title
        content: The card content (can be a string or a function returning HTML/components)
        width (str): CSS width value
    """
    # Create card container with CSS styling
    st.markdown(f"""
    <div style="width: {width}; margin: 10px 0; border-radius: 8px; 
               box-shadow: 0 2px 4px rgba(0,0,0,0.1); overflow: hidden; 
               background-color: var(--card-bg, white);">
        <div style="background-color: var(--primary-color, #1e88e5); color: white; 
                   padding: 10px 16px; font-weight: 500; font-size: 1.1rem;">
            {title}
        </div>
        <div style="padding: 16px;">
            {content if isinstance(content, str) else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # If content is a function, call it in a container
    if callable(content):
        with st.container():
            content()

def toggle_button(label, value, on_change=None, key=None):
    """Create a toggle button component
    
    Args:
        label (str): Button label
        value (bool): Current toggle state
        on_change: Function to call when toggled
        key (str): Unique key for this component
    """
    # Create styled button with toggle appearance
    bg_color = "#1e88e5" if value else "rgba(255, 255, 255, 0.05)"
    text_color = "white"
    
    st.markdown(f"""
    <style>
    .toggle-btn-{key} {{
        background-color: {bg_color};
        color: {text_color};
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        padding: 5px 10px;
        font-size: 14px;
        font-weight: 500;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
        display: inline-block;
        width: 100%;
    }}
    .toggle-btn-{key}:hover {{
        background-color: {"#1565c0" if value else "rgba(255, 255, 255, 0.1)"};
    }}
    </style>
    <div class="toggle-btn-{key}" id="toggle-btn-{key}">{label}</div>
    """, unsafe_allow_html=True)
    
    # Use a regular button for the actual state toggle
    # The button can be hidden with CSS if needed
    return value

def icon_button(icon, tooltip, on_click=None, key=None):
    """Create an icon button with tooltip
    
    Args:
        icon (str): Icon name (using material icons)
        tooltip (str): Tooltip text
        on_click: Function to call when clicked
        key (str): Unique key for this component
    """
    # Use normal Streamlit button but style it to look like an icon button
    button_html = f"""
    <style>
    .icon-btn-{key} {{
        background-color: transparent;
        color: var(--primary-color, #1e88e5);
        border: none;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: background-color 0.3s;
    }}
    .icon-btn-{key}:hover {{
        background-color: rgba(0, 0, 0, 0.05);
    }}
    .tooltip-{key} {{
        position: relative;
        display: inline-block;
    }}
    .tooltip-{key} .tooltip-text {{
        visibility: hidden;
        width: auto;
        min-width: 80px;
        background-color: rgba(0, 0, 0, 0.7);
        color: #fff;
        text-align: center;
        border-radius: 4px;
        padding: 5px 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
        pointer-events: none;
    }}
    .tooltip-{key}:hover .tooltip-text {{
        visibility: visible;
        opacity: 1;
    }}
    </style>
    <div class="tooltip-{key}">
        <button class="icon-btn-{key}">
            <span class="material-icons">{icon}</span>
        </button>
        <span class="tooltip-text">{tooltip}</span>
    </div>
    """
    
    st.markdown(button_html, unsafe_allow_html=True)
    
    # Return a hidden button for the action
    return False

def dashboard_card(title, metric_value, secondary_text=None, icon=None, color="#1e88e5"):
    """Create a dashboard metric card
    
    Args:
        title (str): Card title
        metric_value: The primary value to display
        secondary_text (str): Optional secondary text
        icon (str): Optional Material icon name
        color (str): Card accent color
    """
    # Add Material Icons link if not already in the page
    st.markdown("""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    # Create the dashboard card with CSS
    icon_html = f"""<div class="material-icons" style="font-size: 24px;">{icon}</div>""" if icon else ""
    secondary_html = f"""<div style="color: #777; font-size: 12px;">{secondary_text}</div>""" if secondary_text else ""
    
    st.markdown(f"""
    <div style="padding: 16px; border-radius: 8px; border-left: 4px solid {color}; 
              box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin: 10px 0; 
              background-color: var(--card-bg, white);">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <div style="color: #777; font-size: 14px;">{title}</div>
                <div style="font-size: 24px; font-weight: bold; color: {color};">{metric_value}</div>
                {secondary_html}
            </div>
            <div style="width: 40px; height: 40px; border-radius: 50%; 
                     background-color: {color}20; color: {color}; 
                     display: flex; align-items: center; justify-content: center;">
                {icon_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def status_pill(status, text=None):
    """Create a status pill for statuses like 'Approved', 'Pending', etc.
    
    Args:
        status (str): Status value (approved, pending, rejected, revise)
        text (str): Optional text override (defaults to status value)
    """
    status = status.lower()
    
    # Map status to colors
    colors = {
        "approved": {"bg": "#e8f5e9", "color": "#2e7d32"},
        "pending": {"bg": "#e3f2fd", "color": "#1565c0"},
        "rejected": {"bg": "#ffebee", "color": "#c62828"},
        "revise": {"bg": "#fff3e0", "color": "#ef6c00"},
        "draft": {"bg": "#f5f5f5", "color": "#616161"},
        "complete": {"bg": "#e8f5e9", "color": "#2e7d32"},
        "in progress": {"bg": "#e3f2fd", "color": "#1565c0"}
    }
    
    # Default to pending if status not found
    bg_color = colors.get(status, colors["pending"])["bg"]
    text_color = colors.get(status, colors["pending"])["color"]
    
    # Create the status pill with CSS
    st.markdown(f"""
    <span style="display: inline-block; background-color: {bg_color}; color: {text_color}; 
               border-radius: 12px; padding: 2px 8px; font-size: 0.75rem; font-weight: 500;">
        {text or status.capitalize()}
    </span>
    """, unsafe_allow_html=True)

def nav_button(label, icon, selected, on_click=None, key=None):
    """Create a navigation button for sidebar
    
    Args:
        label (str): Button label
        icon (str): Material icon name
        selected (bool): Whether this item is currently selected
        on_click: Function to call when clicked
        key (str): Unique key for this component
    """
    # Add Material Icons link if not already in the page
    st.markdown("""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    # Create the navigation button with CSS
    bg_color = "#1e88e5" if selected else "transparent"
    hover_bg = "#1976d2" if selected else "rgba(255, 255, 255, 0.1)"
    
    st.markdown(f"""
    <style>
    .nav-btn-{key} {{
        display: flex;
        align-items: center;
        padding: 8px 16px;
        border-radius: 4px;
        margin-bottom: 4px;
        background-color: {bg_color};
        color: white;
        cursor: pointer;
        transition: background-color 0.3s;
        text-decoration: none;
        border: none;
        width: 100%;
        text-align: left;
    }}
    .nav-btn-{key}:hover {{
        background-color: {hover_bg};
    }}
    </style>
    <button class="nav-btn-{key}" id="nav-btn-{key}">
        <span class="material-icons" style="margin-right: 8px;">{icon}</span>
        {label}
    </button>
    """, unsafe_allow_html=True)
    
    # Return a placeholder for the action
    return selected

def data_chart(data, chart_type="bar", height=300):
    """Create a simplified chart using Streamlit's built-in charting
    
    Args:
        data: Chart data (formatted for the specific chart type)
        chart_type (str): Chart type (bar, line, pie)
        height (int): Chart height in pixels
    """
    if chart_type == "bar":
        # For bar charts, data should be a DataFrame
        st.bar_chart(data, height=height)
    elif chart_type == "line":
        st.line_chart(data, height=height)
    elif chart_type == "pie":
        # Streamlit doesn't have a built-in pie chart, use Plotly or other libraries if needed
        st.text("Pie charts are not directly supported. Use Plotly or Matplotlib for pie charts.")
    else:
        st.text(f"Chart type '{chart_type}' not supported.")

def progress_bar(value, total=100, label=None, color="#1e88e5"):
    """Create a styled progress bar
    
    Args:
        value (float): Current progress value
        total (float): Maximum progress value
        label (str): Optional label to display
        color (str): Progress bar color
    """
    percentage = min(100, max(0, (value / total * 100)))
    
    label_html = f"""<div style="margin-bottom: 5px;">{label}</div>""" if label else ""
    
    st.markdown(f"""
    {label_html}
    <div style="width: 100%; background-color: #eee; border-radius: 4px; overflow: hidden;">
        <div style="width: {percentage}%; height: 8px; background-color: {color};"></div>
    </div>
    <div style="display: flex; justify-content: space-between; font-size: 12px; color: #777; margin-top: 2px;">
        <span>0%</span>
        <span>{percentage:.1f}%</span>
        <span>100%</span>
    </div>
    """, unsafe_allow_html=True)

def info_box(content, type="info", dismissible=False, key=None):
    """Create an information alert box
    
    Args:
        content (str): Box content
        type (str): Box type (info, success, warning, error)
        dismissible (bool): Whether the box can be dismissed
        key (str): Unique key for this component
    """
    # Map types to colors
    colors = {
        "info": {"bg": "#e3f2fd", "color": "#1565c0", "icon": "info"},
        "success": {"bg": "#e8f5e9", "color": "#2e7d32", "icon": "check_circle"},
        "warning": {"bg": "#fff3e0", "color": "#ef6c00", "icon": "warning"},
        "error": {"bg": "#ffebee", "color": "#c62828", "icon": "error"}
    }
    
    bg_color = colors.get(type, colors["info"])["bg"]
    text_color = colors.get(type, colors["info"])["color"]
    icon = colors.get(type, colors["info"])["icon"]
    
    # Add Material Icons link if not already in the page
    st.markdown("""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div id="info-box-{key}" style="background-color: {bg_color}; color: {text_color}; padding: 12px 16px;
                border-radius: 4px; margin: 10px 0; display: flex; align-items: flex-start;">
        <span class="material-icons" style="margin-right: 12px;">{icon}</span>
        <div style="flex: 1;">
            {content}
        </div>
        {
        f'''
        <span class="material-icons" style="cursor: pointer;" 
              onclick="document.getElementById('info-box-{key}').style.display='none'">
            close
        </span>
        ''' if dismissible else ''
        }
    </div>
    """, unsafe_allow_html=True)