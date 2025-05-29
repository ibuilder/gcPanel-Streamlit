"""
Accessible UI components with ARIA attributes for gcPanel.

This module provides reusable UI components with proper ARIA attributes
for screen reader compatibility and keyboard navigation.
"""

import streamlit as st
import html

def accessible_card(title, content, icon=None, status=None, key=None):
    """
    Render an accessible card component with proper ARIA attributes.
    
    Args:
        title: Card title
        content: Card content
        icon: Optional icon for the card
        status: Optional status for the card (info, warning, success, error)
        key: Optional key for the component
    """
    # Determine card styling based on status
    status_class = ""
    if status == "info":
        status_class = "info-card"
        aria_label = f"Information: {title}"
    elif status == "warning":
        status_class = "warning-card"
        aria_label = f"Warning: {title}"
    elif status == "success":
        status_class = "success-card"
        aria_label = f"Success: {title}"
    elif status == "error":
        status_class = "error-card"
        aria_label = f"Error: {title}"
    else:
        aria_label = title
    
    # Construct the card HTML
    card_html = f"""
    <div 
        class="accessible-card {status_class}" 
        role="region" 
        aria-labelledby="{key}-title"
        tabindex="0"
    >
        <div class="card-header">
            {f'<span class="card-icon">{icon}</span>' if icon else ''}
            <h3 id="{key}-title">{html.escape(title)}</h3>
        </div>
        <div class="card-content">
            {content}
        </div>
    </div>
    """
    
    # Add card styles if not already added
    if "card_styles_added" not in st.session_state:
        st.markdown("""
        <style>
        .accessible-card {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            background-color: #ffffff;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            transition: box-shadow 0.3s;
        }
        
        .accessible-card:focus {
            outline: 2px solid #3367D6;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        
        .accessible-card:hover {
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }
        
        .card-icon {
            margin-right: 12px;
        }
        
        .card-header h3 {
            margin: 0;
            font-size: 18px;
            font-weight: 600;
        }
        
        .card-content {
            font-size: 14px;
        }
        
        /* Status styles */
        .info-card {
            border-left: 4px solid #3367D6;
        }
        
        .warning-card {
            border-left: 4px solid #FFC107;
        }
        
        .success-card {
            border-left: 4px solid #4CAF50;
        }
        
        .error-card {
            border-left: 4px solid #F44336;
        }
        </style>
        """, unsafe_allow_html=True)
        st.session_state.card_styles_added = True
    
    # Render the card
    st.markdown(card_html, unsafe_allow_html=True)

def accessible_tabs(tabs_data, default_tab=0, key_prefix="tab"):
    """
    Render accessible tabs with proper ARIA attributes.
    
    Args:
        tabs_data: List of dictionaries with 'label' and 'content' keys
        default_tab: Index of the default tab to display
        key_prefix: Prefix for component keys
        
    Returns:
        int: Index of the selected tab
    """
    # Create tab items
    tab_items_html = '<div role="tablist" class="tabs-list">'
    
    for i, tab in enumerate(tabs_data):
        selected = "true" if i == default_tab else "false"
        tab_id = f"{key_prefix}-tab-{i}"
        panel_id = f"{key_prefix}-panel-{i}"
        
        tab_items_html += f"""
        <button 
            id="{tab_id}" 
            role="tab" 
            aria-selected="{selected}" 
            aria-controls="{panel_id}"
            tabindex="{0 if i == default_tab else -1}"
            class="tab-item {' active' if i == default_tab else ''}"
            onclick="selectTab(event, '{tab_id}', '{panel_id}')"
        >
            {html.escape(tab['label'])}
        </button>
        """
    
    tab_items_html += '</div>'
    
    # Create tab panels
    tab_panels_html = '<div class="tab-panels">'
    
    for i, tab in enumerate(tabs_data):
        hidden = "false" if i == default_tab else "true"
        tab_id = f"{key_prefix}-tab-{i}"
        panel_id = f"{key_prefix}-panel-{i}"
        
        tab_panels_html += f"""
        <div 
            id="{panel_id}" 
            role="tabpanel" 
            aria-labelledby="{tab_id}"
            tabindex="0"
            class="tab-panel{' active' if i == default_tab else ''}"
            hidden="{hidden}"
        >
            {tab['content']}
        </div>
        """
    
    tab_panels_html += '</div>'
    
    # Add tabs JavaScript
    tabs_js = """
    <script>
    function selectTab(event, tabId, panelId) {
        // Prevent default button action
        event.preventDefault();
        
        // Get tab elements
        const tabs = document.querySelectorAll('.tab-item');
        const panels = document.querySelectorAll('.tab-panel');
        
        // Deactivate all tabs and panels
        tabs.forEach(tab => {
            tab.setAttribute('aria-selected', 'false');
            tab.classList.remove('active');
            tab.setAttribute('tabindex', '-1');
        });
        
        panels.forEach(panel => {
            panel.setAttribute('hidden', 'true');
            panel.classList.remove('active');
        });
        
        // Activate selected tab and panel
        const selectedTab = document.getElementById(tabId);
        const selectedPanel = document.getElementById(panelId);
        
        selectedTab.setAttribute('aria-selected', 'true');
        selectedTab.classList.add('active');
        selectedTab.setAttribute('tabindex', '0');
        selectedTab.focus();
        
        selectedPanel.removeAttribute('hidden');
        selectedPanel.classList.add('active');
        
        // Store selection in local storage to persist across refreshes
        localStorage.setItem('activeTab', tabId);
    }
    
    document.addEventListener('keydown', function(e) {
        const activeTab = document.querySelector('.tab-item[aria-selected="true"]');
        if (!activeTab) return;
        
        const tabs = document.querySelectorAll('.tab-item');
        const tabsArray = Array.from(tabs);
        const currentIndex = tabsArray.indexOf(activeTab);
        
        // Left/Right arrow keys to navigate tabs
        if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
            let newIndex;
            
            if (e.key === 'ArrowLeft') {
                newIndex = currentIndex > 0 ? currentIndex - 1 : tabsArray.length - 1;
            } else {
                newIndex = currentIndex < tabsArray.length - 1 ? currentIndex + 1 : 0;
            }
            
            const newTab = tabsArray[newIndex];
            const tabId = newTab.getAttribute('id');
            const panelId = newTab.getAttribute('aria-controls');
            
            selectTab(e, tabId, panelId);
            e.preventDefault();
        }
    });
    
    // Restore active tab on page load
    document.addEventListener('DOMContentLoaded', function() {
        const storedTabId = localStorage.getItem('activeTab');
        if (storedTabId) {
            const storedTab = document.getElementById(storedTabId);
            if (storedTab) {
                const panelId = storedTab.getAttribute('aria-controls');
                selectTab({preventDefault: function(){}}, storedTabId, panelId);
            }
        }
    });
    </script>
    """
    
    # Add tabs styles if not already added
    if "tabs_styles_added" not in st.session_state:
        st.markdown("""
        <style>
        .tabs-list {
            display: flex;
            border-bottom: 1px solid #e0e0e0;
            margin-bottom: 16px;
            overflow-x: auto;
        }
        
        .tab-item {
            padding: 8px 16px;
            border: none;
            background: none;
            cursor: pointer;
            position: relative;
            white-space: nowrap;
        }
        
        .tab-item:focus {
            outline: none;
            box-shadow: none;
        }
        
        .tab-item::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background-color: transparent;
            transition: background-color 0.3s;
        }
        
        .tab-item.active::after {
            background-color: #3367D6;
        }
        
        .tab-item:focus::after {
            background-color: #3367D6;
        }
        
        .tab-panel {
            padding: 16px 0;
            animation: fadeIn 0.3s;
        }
        
        .tab-panel:focus {
            outline: none;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        </style>
        """, unsafe_allow_html=True)
        st.session_state.tabs_styles_added = True
    
    # Render tabs
    st.markdown(tab_items_html + tab_panels_html + tabs_js, unsafe_allow_html=True)
    
    # Set up a placeholder to track tab selection changes
    if f"{key_prefix}_selected_tab" not in st.session_state:
        st.session_state[f"{key_prefix}_selected_tab"] = default_tab
    
    # Return selected tab index
    return st.session_state[f"{key_prefix}_selected_tab"]

def accessible_alert(message, type="info", dismissible=True, key=None):
    """
    Render an accessible alert component with proper ARIA attributes.
    
    Args:
        message: Alert message
        type: Alert type (info, warning, success, error)
        dismissible: Whether the alert can be dismissed
        key: Optional key for the component
    """
    # Determine alert style and icon
    alert_class = f"alert-{type}"
    alert_role = "alert"
    
    if type == "info":
        icon = "ℹ️"
    elif type == "warning":
        icon = "⚠️"
    elif type == "success":
        icon = "✅"
    elif type == "error":
        icon = "❌"
        alert_role = "alertdialog"
    else:
        icon = "ℹ️"
    
    # Construct the alert HTML
    alert_id = f"alert-{key}" if key else f"alert-{hash(message) % 10000}"
    
    alert_html = f"""
    <div 
        id="{alert_id}"
        class="accessible-alert {alert_class}" 
        role="{alert_role}"
        aria-live="assertive"
        aria-atomic="true"
    >
        <div class="alert-content">
            <span class="alert-icon">{icon}</span>
            <span class="alert-message">{html.escape(message)}</span>
        </div>
        {f'<button class="alert-dismiss" aria-label="Dismiss" onClick="document.getElementById(\'{alert_id}\').style.display=\'none\'">×</button>' if dismissible else ''}
    </div>
    """
    
    # Add alert styles if not already added
    if "alert_styles_added" not in st.session_state:
        st.markdown("""
        <style>
        .accessible-alert {
            padding: 12px 16px;
            margin-bottom: 16px;
            border-radius: 4px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .alert-content {
            display: flex;
            align-items: center;
            flex: 1;
        }
        
        .alert-icon {
            margin-right: 12px;
        }
        
        .alert-message {
            flex: 1;
        }
        
        .alert-dismiss {
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            padding: 0 8px;
            margin-left: 8px;
        }
        
        .alert-info {
            background-color: #E3F2FD;
            border-left: 4px solid #3367D6;
            color: #0D47A1;
        }
        
        .alert-warning {
            background-color: #FFF8E1;
            border-left: 4px solid #FFC107;
            color: #FF8F00;
        }
        
        .alert-success {
            background-color: #E8F5E9;
            border-left: 4px solid #4CAF50;
            color: #2E7D32;
        }
        
        .alert-error {
            background-color: #FFEBEE;
            border-left: 4px solid #F44336;
            color: #C62828;
        }
        </style>
        """, unsafe_allow_html=True)
        st.session_state.alert_styles_added = True
    
    # Render the alert
    st.markdown(alert_html, unsafe_allow_html=True)

def accessible_dialog(title, content, open_button_text="Open Dialog", key=None):
    """
    Render an accessible dialog component with proper ARIA attributes.
    
    Args:
        title: Dialog title
        content: Dialog content
        open_button_text: Text for the button that opens the dialog
        key: Optional key for the component
    """
    dialog_id = f"dialog-{key}" if key else f"dialog-{hash(title) % 10000}"
    
    # Construct the dialog HTML
    dialog_html = f"""
    <div>
        <button 
            class="dialog-open-button"
            onclick="openDialog('{dialog_id}')"
            aria-haspopup="dialog"
        >
            {html.escape(open_button_text)}
        </button>
        
        <div 
            id="{dialog_id}" 
            class="dialog-backdrop" 
            aria-hidden="true"
            onclick="closeDialog('{dialog_id}', event)"
        >
            <div 
                class="dialog-container" 
                role="dialog" 
                aria-labelledby="{dialog_id}-title" 
                aria-modal="true"
                tabindex="-1"
            >
                <div class="dialog-header">
                    <h2 id="{dialog_id}-title" class="dialog-title">{html.escape(title)}</h2>
                    <button 
                        class="dialog-close" 
                        aria-label="Close dialog"
                        onclick="closeDialog('{dialog_id}')"
                    >
                        ×
                    </button>
                </div>
                <div class="dialog-content">
                    {content}
                </div>
            </div>
        </div>
    </div>
    """
    
    # Add dialog JavaScript
    dialog_js = """
    <script>
    function openDialog(dialogId) {
        const dialog = document.getElementById(dialogId);
        const dialogContainer = dialog.querySelector('.dialog-container');
        
        // Show dialog
        dialog.style.display = 'flex';
        dialog.setAttribute('aria-hidden', 'false');
        
        // Focus dialog container
        setTimeout(() => {
            dialogContainer.focus();
        }, 50);
        
        // Trap focus in dialog
        dialog.addEventListener('keydown', trapFocus);
        
        // Close on escape
        dialog.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeDialog(dialogId);
            }
        });
        
        // Prevent body scrolling
        document.body.style.overflow = 'hidden';
    }
    
    function closeDialog(dialogId, event) {
        // If clicking on backdrop (not content), close dialog
        if (event && event.target !== event.currentTarget) {
            return;
        }
        
        const dialog = document.getElementById(dialogId);
        
        // Hide dialog
        dialog.style.display = 'none';
        dialog.setAttribute('aria-hidden', 'true');
        
        // Remove event listeners
        dialog.removeEventListener('keydown', trapFocus);
        
        // Restore body scrolling
        document.body.style.overflow = '';
        
        // Return focus to open button
        const openButton = document.querySelector(`button[onclick="openDialog('${dialogId}')"]`);
        if (openButton) {
            openButton.focus();
        }
    }
    
    function trapFocus(e) {
        if (e.key !== 'Tab') return;
        
        const dialog = e.currentTarget;
        const focusableElements = dialog.querySelectorAll('a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])');
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        if (e.shiftKey) {
            // Shift+Tab: going backward
            if (document.activeElement === firstElement) {
                lastElement.focus();
                e.preventDefault();
            }
        } else {
            // Tab: going forward
            if (document.activeElement === lastElement) {
                firstElement.focus();
                e.preventDefault();
            }
        }
    }
    </script>
    """
    
    # Add dialog styles if not already added
    if "dialog_styles_added" not in st.session_state:
        st.markdown("""
        <style>
        .dialog-open-button {
            background-color: #3367D6;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .dialog-open-button:hover {
            background-color: #2850a7;
        }
        
        .dialog-backdrop {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        
        .dialog-container {
            background-color: white;
            border-radius: 8px;
            width: 90%;
            max-width: 500px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        }
        
        .dialog-container:focus {
            outline: none;
        }
        
        .dialog-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .dialog-title {
            margin: 0;
            font-size: 18px;
            font-weight: 600;
        }
        
        .dialog-close {
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            padding: 0 8px;
        }
        
        .dialog-content {
            padding: 16px;
        }
        </style>
        """, unsafe_allow_html=True)
        st.session_state.dialog_styles_added = True
    
    # Render the dialog
    st.markdown(dialog_html + dialog_js, unsafe_allow_html=True)

def accessible_tooltip(text, tooltip_content, position="top", key=None):
    """
    Render an accessible tooltip component with proper ARIA attributes.
    
    Args:
        text: Text to display
        tooltip_content: Content for the tooltip
        position: Position of the tooltip (top, bottom, left, right)
        key: Optional key for the component
    """
    tooltip_id = f"tooltip-{key}" if key else f"tooltip-{hash(text) % 10000}"
    position_class = f"tooltip-{position}"
    
    # Construct the tooltip HTML
    tooltip_html = f"""
    <div class="tooltip-container">
        <span 
            class="tooltip-trigger"
            tabindex="0"
            aria-describedby="{tooltip_id}"
        >
            {html.escape(text)}
        </span>
        <div id="{tooltip_id}" role="tooltip" class="tooltip {position_class}">
            {html.escape(tooltip_content)}
            <div class="tooltip-arrow"></div>
        </div>
    </div>
    """
    
    # Add tooltip styles if not already added
    if "tooltip_styles_added" not in st.session_state:
        st.markdown("""
        <style>
        .tooltip-container {
            position: relative;
            display: inline-block;
        }
        
        .tooltip-trigger {
            border-bottom: 1px dotted #3367D6;
            cursor: help;
        }
        
        .tooltip {
            visibility: hidden;
            position: absolute;
            background-color: #333;
            color: white;
            text-align: center;
            border-radius: 4px;
            padding: 8px;
            z-index: 100;
            opacity: 0;
            transition: opacity 0.3s;
            width: max-content;
            max-width: 200px;
            font-size: 12px;
        }
        
        .tooltip-arrow {
            position: absolute;
            width: 0;
            height: 0;
            border-style: solid;
        }
        
        /* Tooltip positions */
        .tooltip-top {
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
        }
        
        .tooltip-top .tooltip-arrow {
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px 5px 0;
            border-color: #333 transparent transparent transparent;
        }
        
        .tooltip-bottom {
            top: 125%;
            left: 50%;
            transform: translateX(-50%);
        }
        
        .tooltip-bottom .tooltip-arrow {
            bottom: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 0 5px 5px;
            border-color: transparent transparent #333 transparent;
        }
        
        .tooltip-left {
            right: 125%;
            top: 50%;
            transform: translateY(-50%);
        }
        
        .tooltip-left .tooltip-arrow {
            left: 100%;
            top: 50%;
            margin-top: -5px;
            border-width: 5px 0 5px 5px;
            border-color: transparent transparent transparent #333;
        }
        
        .tooltip-right {
            left: 125%;
            top: 50%;
            transform: translateY(-50%);
        }
        
        .tooltip-right .tooltip-arrow {
            right: 100%;
            top: 50%;
            margin-top: -5px;
            border-width: 5px 5px 5px 0;
            border-color: transparent #333 transparent transparent;
        }
        
        /* Show tooltip on hover/focus */
        .tooltip-trigger:hover + .tooltip,
        .tooltip-trigger:focus + .tooltip {
            visibility: visible;
            opacity: 1;
        }
        </style>
        """, unsafe_allow_html=True)
        st.session_state.tooltip_styles_added = True
    
    # Render the tooltip
    st.markdown(tooltip_html, unsafe_allow_html=True)

def initialize_aria_components():
    """Initialize ARIA components for the application."""
    # Add global styles for keyboard focus
    st.markdown("""
    <style>
    /* Ensure keyboard focus is visible for all interactive elements */
    *:focus {
        outline: 3px solid #3367D6 !important;
        outline-offset: 2px !important;
    }
    
    /* Make focus visible in high contrast mode */
    @media (forced-colors: active) {
        *:focus {
            outline: 3px solid CanvasText !important;
        }
    }
    
    /* Screenreader only content */
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border-width: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add skip to content link
    st.markdown("""
    <a href="#main-content" class="sr-only sr-only-focusable">Skip to main content</a>
    <div id="main-content" tabindex="-1"></div>
    """, unsafe_allow_html=True)