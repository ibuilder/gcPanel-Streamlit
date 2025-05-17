import streamlit as st
import pandas as pd
import numpy as np
from uuid import uuid4

def card(title, content, width="100%"):
    """Create a styled card component with title and content
    
    Args:
        title (str): The card title
        content: The card content (can be a string or a function returning HTML/components)
        width (str): CSS width value
    """
    card_id = f"card_{uuid4().hex[:8]}"
    
    st.markdown(f"""
    <div class="card" style="width: {width};" id="{card_id}">
        <div class="card-header">
            <h3 class="card-title">{title}</h3>
        </div>
        <div class="card-content">
    """, unsafe_allow_html=True)
    
    # Content can be a string (HTML) or a callable (function that renders components)
    if callable(content):
        content()
    else:
        st.markdown(f"{content}", unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def toggle_button(label, value, on_change=None, key=None):
    """Create a toggle button component
    
    Args:
        label (str): Button label
        value (bool): Current toggle state
        on_change: Function to call when toggled
        key (str): Unique key for this component
    """
    if key is None:
        key = f"toggle_{uuid4().hex[:8]}"
        
    toggle_id = f"toggle_{key}"
    checked = "checked" if value else ""
    
    st.markdown(f"""
    <div class="toggle-container">
        <label for="{toggle_id}" class="toggle-label">{label}</label>
        <label class="toggle-switch">
            <input type="checkbox" id="{toggle_id}" {checked}>
            <span class="toggle-slider"></span>
        </label>
    </div>
    <style>
    .toggle-container {{
        display: flex;
        align-items: center;
        margin-bottom: 12px;
    }}
    
    .toggle-label {{
        margin-right: 10px;
        flex: 1;
    }}
    
    .toggle-switch {{
        position: relative;
        display: inline-block;
        width: 46px;
        height: 24px;
    }}
    
    .toggle-switch input {{
        opacity: 0;
        width: 0;
        height: 0;
    }}
    
    .toggle-slider {{
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: var(--divider-color);
        transition: .3s;
        border-radius: 34px;
    }}
    
    .toggle-slider:before {{
        position: absolute;
        content: "";
        height: 18px;
        width: 18px;
        left: 3px;
        bottom: 3px;
        background-color: var(--card-bg, #fff);
        transition: .3s;
        border-radius: 50%;
    }}
    
    input:checked + .toggle-slider {{
        background-color: var(--primary-color);
    }}
    
    input:checked + .toggle-slider:before {{
        transform: translateX(22px);
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Hidden button for functionality
    return st.checkbox("", value=value, key=key, on_change=on_change, label_visibility="collapsed")

def icon_button(icon, tooltip, on_click=None, key=None):
    """Create an icon button with tooltip
    
    Args:
        icon (str): Icon name (using material icons)
        tooltip (str): Tooltip text
        on_click: Function to call when clicked
        key (str): Unique key for this component
    """
    if key is None:
        key = f"icon_btn_{uuid4().hex[:8]}"
        
    st.markdown(f"""
    <style>
    .icon-button-{key} {{
        background-color: transparent;
        border: none;
        color: var(--text-primary);
        border-radius: 50%;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: background-color 0.3s;
    }}
    
    .icon-button-{key}:hover {{
        background-color: rgba(255, 255, 255, 0.1);
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Use small columns for layout
    col = st.columns([1, 10])[0]
    with col:
        result = st.button("", key=key)
        st.markdown(f"""
        <div style="position: relative; top: -40px; height: 0;">
            <button class="icon-button-{key}" title="{tooltip}">
                <span class="material-icons">{icon}</span>
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    if result and on_click:
        on_click()
        
    return result

def dashboard_card(title, metric_value, secondary_text=None, icon=None, color="#1e88e5"):
    """Create a dashboard metric card
    
    Args:
        title (str): Card title
        metric_value: The primary value to display
        secondary_text (str): Optional secondary text
        icon (str): Optional Material icon name
        color (str): Card accent color
    """
    card_id = f"dash_card_{uuid4().hex[:8]}"
    
    # Determine accent class based on color
    accent_class = ""
    if color == "#388e3c" or color == "green":
        accent_class = "secondary"
    elif color == "#f57c00" or color == "orange":
        accent_class = "accent"
    elif color == "#0288d1" or color == "blue":
        accent_class = "info"
    
    st.markdown(f"""
    <div class="metric-card {accent_class}" id="{card_id}">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{metric_value}</div>
        {f'<div class="metric-subtext">{secondary_text}</div>' if secondary_text else ''}
        {f'<span class="material-icons" style="position: absolute; top: 12px; right: 12px; color: rgba(255,255,255,0.2); font-size: 24px;">{icon}</span>' if icon else ''}
    </div>
    """, unsafe_allow_html=True)

def status_pill(status, text=None):
    """Create a status pill for statuses like 'Approved', 'Pending', etc.
    
    Args:
        status (str): Status value (approved, pending, rejected, revise)
        text (str): Optional text override (defaults to status value)
    """
    if text is None:
        text = status.capitalize()
    
    # Define icon for each status
    icons = {
        'approved': 'check_circle',
        'pending': 'hourglass_top',
        'rejected': 'cancel',
        'revise': 'edit',
        'complete': 'task_alt'
    }
    
    icon = icons.get(status.lower(), 'help')
    
    st.markdown(f"""
    <div class="status-pill status-{status.lower()}">
        <span class="material-icons status-pill-icon">{icon}</span>
        {text}
    </div>
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
    if key is None:
        key = f"nav_btn_{uuid4().hex[:8]}"
        
    selected_class = "active" if selected else ""
    
    # Create the visible nav item
    st.markdown(f"""
    <div class="sidebar-nav-item {selected_class}" id="{key}">
        <span class="material-icons">{icon}</span>
        <span style="flex: 1;">{label}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Hidden button for functionality
    col = st.container()
    col.markdown('<div style="height: 0;"></div>', unsafe_allow_html=True)
    result = col.button("", key=key)
    
    if result and on_click:
        on_click()
        
    return result

def data_chart(data, chart_type="bar", height=300):
    """Create a simplified chart using Streamlit's built-in charting
    
    Args:
        data: Chart data (formatted for the specific chart type)
        chart_type (str): Chart type (bar, line, pie)
        height (int): Chart height in pixels
    """
    chart_container = st.container()
    
    if chart_type == "bar":
        chart_container.bar_chart(data, height=height)
    elif chart_type == "line":
        chart_container.line_chart(data, height=height)
    elif chart_type == "pie":
        # For pie charts, we need to manually plot with matplotlib
        import matplotlib.pyplot as plt
        import io
        
        fig, ax = plt.subplots()
        ax.pie(data.values, labels=data.index, autopct='%1.1f%%')
        ax.axis('equal')
        
        # Convert plot to image
        buf = io.BytesIO()
        fig.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        
        chart_container.image(buf, width=height)  # Use height as width for proportional sizing

def progress_bar(value, total=100, label=None, color="#1e88e5"):
    """Create a styled progress bar
    
    Args:
        value (float): Current progress value
        total (float): Maximum progress value
        label (str): Optional label to display
        color (str): Progress bar color
    """
    percent = min(100, max(0, (value / total) * 100))
    
    # Choose bar class based on percentage or color
    bar_class = ""
    if color == "#4caf50" or color == "green":
        bar_class = "success"
    elif color == "#ff9800" or color == "orange":
        bar_class = "warning" 
    elif color == "#f44336" or color == "red":
        bar_class = "danger"
    
    # Display label if provided
    if label:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <div>{label}</div>
            <div>{value}/{total} ({percent:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Render the progress bar with a modern style
    st.markdown(f"""
    <div class="modern-progress-container">
        <div class="modern-progress-bar {bar_class}" style="width: {percent}%;"></div>
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
    if key is None:
        key = f"info_box_{uuid4().hex[:8]}"
    
    # Define colors and icons based on type
    colors = {
        "info": "var(--info-color, #2196f3)",
        "success": "var(--success-color, #4caf50)",
        "warning": "var(--warning-color, #ff9800)",
        "error": "var(--error-color, #f44336)"
    }
    
    icons = {
        "info": "info",
        "success": "check_circle",
        "warning": "warning",
        "error": "error"
    }
    
    color = colors.get(type, colors["info"])
    icon = icons.get(type, icons["info"])
    
    # Create info box without any dismiss options to prevent raw HTML
    st.markdown(f"""
    <div id="info-box-{key}" style="
        background-color: rgba(0, 0, 0, 0.1);
        border-left: 4px solid {color};
        padding: 15px;
        margin: 15px 0;
        border-radius: 4px;
        position: relative;
    ">
        <div style="display: flex;">
            <span class="material-icons" style="margin-right: 10px; color: {color};">
                {icon}
            </span>
            <div style="flex: 1;">
                {content}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def modal_dialog(title, content=None, open_button_text="Open", open_button_icon=None, key=None):
    """Create a modal dialog component
    
    Args:
        title (str): The modal title
        content: Content function or HTML string
        open_button_text (str): Text for the button that opens the modal
        open_button_icon (str): Icon for the open button
        key (str): Unique component key
        
    Returns:
        is_open (bool): Whether the modal is currently open
    """
    if key is None:
        key = f"modal_{uuid4().hex[:8]}"
    
    # Initialize state
    if f"modal_open_{key}" not in st.session_state:
        st.session_state[f"modal_open_{key}"] = False
    
    # Button to open the modal
    button_cols = st.columns([1, 5])
    with button_cols[0]:
        if st.button(open_button_text, key=f"modal_btn_{key}"):
            st.session_state[f"modal_open_{key}"] = True
            st.rerun()
    
    # Add icon if specified
    if open_button_icon:
        with button_cols[0]:
            st.markdown(f"""
            <div style="position: relative; top: -38px; left: 10px;">
                <span class="material-icons">{open_button_icon}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Modal dialog
    if st.session_state[f"modal_open_{key}"]:
        # Modal overlay
        st.markdown(f"""
        <div class="modal-overlay" id="modal-overlay-{key}">
            <div class="modal-container">
                <div class="modal-header">
                    <h3>{title}</h3>
                    <span class="material-icons modal-close" id="modal-close-{key}">close</span>
                </div>
                <div class="modal-content">
                    <!-- Content will be rendered by Streamlit below -->
                </div>
                <div class="modal-footer">
                    <button class="modal-cancel" id="modal-cancel-{key}">Cancel</button>
                    <button class="modal-confirm" id="modal-confirm-{key}">Confirm</button>
                </div>
            </div>
        </div>
        
        <style>
        .modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }}
        
        .modal-container {{
            background-color: var(--card-bg);
            border-radius: 8px;
            width: 90%;
            max-width: 600px;
            max-height: 80vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }}
        
        .modal-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            border-bottom: 1px solid var(--divider-color);
        }}
        
        .modal-header h3 {{
            margin: 0;
            font-size: 18px;
            font-weight: 500;
        }}
        
        .modal-close {{
            cursor: pointer;
            font-size: 20px;
            color: var(--text-secondary);
        }}
        
        .modal-content {{
            padding: 20px;
            overflow-y: auto;
            max-height: calc(80vh - 130px);
        }}
        
        .modal-footer {{
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            padding: 15px 20px;
            border-top: 1px solid var(--divider-color);
        }}
        
        .modal-cancel, .modal-confirm {{
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .modal-cancel {{
            background-color: transparent;
            border: 1px solid var(--divider-color);
            color: var(--text-secondary);
        }}
        
        .modal-confirm {{
            background-color: var(--primary-color);
            border: none;
            color: white;
        }}
        </style>
        
        <script>
            // Close the modal when clicking close button
            document.getElementById("modal-close-{key}").addEventListener("click", function() {{
                document.getElementById("modal-overlay-{key}").style.display = "none";
                // Notify Streamlit
                window.streamlitMessageListener.setComponentValue({{"modal_action": "close"}});
            }});
            
            // Close when clicking cancel
            document.getElementById("modal-cancel-{key}").addEventListener("click", function() {{
                document.getElementById("modal-overlay-{key}").style.display = "none";
                // Notify Streamlit
                window.streamlitMessageListener.setComponentValue({{"modal_action": "cancel"}});
            }});
            
            // Close and confirm
            document.getElementById("modal-confirm-{key}").addEventListener("click", function() {{
                document.getElementById("modal-overlay-{key}").style.display = "none";
                // Notify Streamlit
                window.streamlitMessageListener.setComponentValue({{"modal_action": "confirm"}});
            }});
        </script>
        """, unsafe_allow_html=True)
        
        # Render modal content
        modal_container = st.container()
        with modal_container:
            if callable(content):
                content()
            elif content:
                st.markdown(content, unsafe_allow_html=True)
            
            # Add close button at the bottom as well
            if st.button("Close Modal", key=f"close_modal_btn_{key}"):
                st.session_state[f"modal_open_{key}"] = False
                st.rerun()
    
    return st.session_state[f"modal_open_{key}"]

def confirmation_dialog(message, confirm_text="Confirm", cancel_text="Cancel", key=None):
    """Create a confirmation dialog
    
    Args:
        message (str): The confirmation message
        confirm_text (str): Text for the confirm button
        cancel_text (str): Text for the cancel button
        key (str): Unique component key
        
    Returns:
        confirmed (bool): True if confirmed, False if canceled, None if not yet answered
    """
    if key is None:
        key = f"confirm_{uuid4().hex[:8]}"
    
    # Initialize state
    if f"confirmed_{key}" not in st.session_state:
        st.session_state[f"confirmed_{key}"] = None
    
    # Show dialog in a card
    st.markdown(f"""
    <div class="card" style="padding: 20px; margin-bottom: 20px;">
        <div style="margin-bottom: 15px;">
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(cancel_text, key=f"cancel_{key}"):
            st.session_state[f"confirmed_{key}"] = False
            st.rerun()
    
    with col2:
        if st.button(confirm_text, key=f"confirm_{key}", type="primary"):
            st.session_state[f"confirmed_{key}"] = True
            st.rerun()
    
    return st.session_state[f"confirmed_{key}"]