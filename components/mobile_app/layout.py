"""
Mobile application layout component for gcPanel.

This module provides layout components optimized for mobile devices,
allowing users to access the construction management system on smartphones and tablets.
"""

import streamlit as st
from datetime import datetime

def render_mobile_header():
    """
    Render a mobile-optimized header for the app.
    """
    # Current date
    current_date = datetime.now().strftime("%b %d, %Y")
    
    # Mobile header with logo, project selector and menu button
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; 
                padding: 10px 0; border-bottom: 1px solid #DADCE0;">
        <div style="display: flex; align-items: center;">
            <img src="static/img/gcpanel.png" style="height: 30px; margin-right: 10px;">
            <div>
                <div style="font-weight: 600; color: #3367D6;">gcPanel</div>
                <div style="font-size: 12px; color: #5F6368;">{}</div>
            </div>
        </div>
        <div>
            <button id="mobile-menu-btn" style="background: none; border: none; cursor: pointer;">
                <span class="material-icons" style="font-size: 24px; color: #3367D6;">menu</span>
            </button>
        </div>
    </div>
    """.format(current_date), unsafe_allow_html=True)

def render_mobile_bottom_nav():
    """
    Render a mobile-optimized bottom navigation bar.
    """
    # Get current page to highlight active item
    current_page = st.session_state.get("mobile_page", "dashboard")
    
    # Bottom navigation with icons for main sections
    st.markdown("""
    <style>
        .mobile-bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: white;
            display: flex;
            justify-content: space-around;
            padding: 10px 0;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
            z-index: 1000;
        }
        
        .mobile-nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-decoration: none;
            color: #5F6368;
            font-size: 12px;
        }
        
        .mobile-nav-item.active {
            color: #3367D6;
        }
        
        .mobile-nav-item .material-icons {
            font-size: 20px;
            margin-bottom: 2px;
        }
    </style>
    
    <div class="mobile-bottom-nav">
        <a href="#" class="mobile-nav-item {}" id="nav-dashboard" onclick="setActivePage('dashboard')">
            <span class="material-icons">dashboard</span>
            <span>Dashboard</span>
        </a>
        <a href="#" class="mobile-nav-item {}" id="nav-tasks" onclick="setActivePage('tasks')">
            <span class="material-icons">assignment</span>
            <span>Tasks</span>
        </a>
        <a href="#" class="mobile-nav-item {}" id="nav-photos" onclick="setActivePage('photos')">
            <span class="material-icons">photo_camera</span>
            <span>Photos</span>
        </a>
        <a href="#" class="mobile-nav-item {}" id="nav-docs" onclick="setActivePage('docs')">
            <span class="material-icons">description</span>
            <span>Documents</span>
        </a>
        <a href="#" class="mobile-nav-item {}" id="nav-more" onclick="setActivePage('more')">
            <span class="material-icons">more_horiz</span>
            <span>More</span>
        </a>
    </div>
    
    <script>
        function setActivePage(page) {
            // Update active class visually
            document.querySelectorAll('.mobile-nav-item').forEach(item => {
                item.classList.remove('active');
            });
            document.getElementById('nav-' + page).classList.add('active');
            
            // Store in session state via form submission
            const formData = new FormData();
            formData.append('mobile_page', page);
            
            fetch(window.location.href, {
                method: 'POST',
                body: formData
            }).then(() => {
                window.location.reload();
            });
        }
        
        // Set initial active state
        document.getElementById('nav-{}').classList.add('active');
    </script>
    """.format(
        "active" if current_page == "dashboard" else "",
        "active" if current_page == "tasks" else "",
        "active" if current_page == "photos" else "",
        "active" if current_page == "docs" else "",
        "active" if current_page == "more" else "",
        current_page
    ), unsafe_allow_html=True)

def render_mobile_frame(content_callback):
    """
    Render a mobile device frame with the provided content.
    
    Args:
        content_callback: Function to call to render content inside the frame
    """
    # Apply mobile-specific styling
    st.markdown("""
    <style>
        /* Mobile device frame */
        .mobile-frame {
            max-width: 375px;
            margin: 0 auto;
            border: 12px solid #333;
            border-radius: 36px;
            padding: 0;
            background-color: #333;
            box-shadow: 0px 10px 20px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .mobile-frame-notch {
            position: relative;
            width: 100%;
            height: 48px;
            background-color: #333;
            border-radius: 24px 24px 0 0;
            margin-bottom: 1px;
        }
        
        .mobile-frame-notch-content {
            position: absolute;
            width: 150px;
            height: 28px;
            background-color: #111;
            border-radius: 14px;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
        }
        
        .mobile-frame-content {
            width: 100%;
            height: 600px;
            overflow-y: auto;
            background-color: white;
        }
        
        .mobile-frame-home {
            position: relative;
            width: 100%;
            height: 48px;
            background-color: #333;
            border-radius: 0 0 24px 24px;
            margin-top: 1px;
        }
        
        .mobile-frame-home-button {
            position: absolute;
            width: 120px;
            height: 5px;
            background-color: #999;
            border-radius: 5px;
            bottom: 12px;
            left: 50%;
            transform: translateX(-50%);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Render the mobile device frame
    st.markdown("""
    <div class="mobile-frame">
        <div class="mobile-frame-notch">
            <div class="mobile-frame-notch-content"></div>
        </div>
        <div class="mobile-frame-content">
    """, unsafe_allow_html=True)
    
    # Call the content callback to render inside the frame
    content_callback()
    
    # Close the frame
    st.markdown("""
        </div>
        <div class="mobile-frame-home">
            <div class="mobile-frame-home-button"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)