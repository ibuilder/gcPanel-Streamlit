"""
Settings module for the gcPanel Construction Management Dashboard.

This module provides settings and configuration options for the application,
including theme settings, user preferences, system configuration, and
integration management for external services.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import colorsys
import json
import os

# Import integration manager
from utils.integration_manager import IntegrationManager, IntegrationType, IntegrationProvider

def render_settings():
    """Render the settings interface."""
    st.header("Settings")
    
    # Create settings tabs
    tabs = st.tabs(["Appearance", "User Preferences", "Integrations", "System", "About"])
    
    # Appearance Tab
    with tabs[0]:
        render_appearance_settings()
    
    # User Preferences Tab
    with tabs[1]:
        render_user_preferences()
        
    # Integrations Tab
    with tabs[2]:
        from modules.settings_components.integrations import render_integrations
        render_integrations()
    
    # System Tab
    with tabs[3]:
        render_system_settings()
    
    # About Tab
    with tabs[4]:
        render_about_page()

def render_appearance_settings():
    """Render appearance settings."""
    st.subheader("Appearance Settings")
    
    # Theme selection
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    
    st.markdown("### Theme Options")
    
    # Theme color selector
    st.write("#### Primary Color")
    # Create a grid of color options
    col1, col2, col3, col4, col5 = st.columns(5)
    
    theme_colors = {
        "Blue": "#3e79f7",
        "Indigo": "#5b21b6",
        "Purple": "#8b5cf6",
        "Pink": "#ec4899",
        "Red": "#ef4444",
        "Orange": "#f97316",
        "Yellow": "#f59e0b",
        "Green": "#10b981",
        "Teal": "#14b8a6",
        "Cyan": "#06b6d4"
    }
    
    # Select the active theme color
    current_color = st.session_state.get('theme_color', '#3e79f7')
    
    # Display color selection grid
    color_cols = [col1, col2, col3, col4, col5]
    
    i = 0
    for color_name, color_code in theme_colors.items():
        col = color_cols[i % 5]
        with col:
            # Use a button with the color as background
            is_selected = color_code == current_color
            border_style = "2px solid white" if not is_selected else "3px solid #f59e0b"
            
            st.markdown(f"""
            <div style="margin-bottom: 10px;">
                <div style="background-color: {color_code}; width: 100%; height: 40px; 
                           border-radius: 4px; cursor: pointer; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                           border: {border_style}" id="color-{color_name}"></div>
                <div style="font-size: 12px; text-align: center; margin-top: 4px;">{color_name}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Use a hidden button to capture the click
            if st.button(f"Select {color_name}", key=f"color_btn_{color_name}", help=f"Select {color_name} theme"):
                st.session_state.theme_color = color_code
                # In a real application, you would save this preference to a database
                st.rerun()
        
        i += 1
    
    # Create custom color palettes with visualizations
    st.write("#### Color Palettes")
    st.write("Preview of color palettes derived from your primary color")
    
    # Generate complementary colors based on the primary color
    primary_hex = st.session_state.get('theme_color', '#3e79f7')
    r, g, b = int(primary_hex[1:3], 16)/255, int(primary_hex[3:5], 16)/255, int(primary_hex[5:7], 16)/255
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    
    # Generate color variations
    colors = []
    
    # Complementary color (opposite on color wheel)
    compl_h = (h + 0.5) % 1.0
    compl_r, compl_g, compl_b = colorsys.hsv_to_rgb(compl_h, s, v)
    complementary = f"#{int(compl_r*255):02x}{int(compl_g*255):02x}{int(compl_b*255):02x}"
    
    # Analogous colors (adjacent on color wheel)
    analog_h1 = (h + 0.1) % 1.0
    r1, g1, b1 = colorsys.hsv_to_rgb(analog_h1, s, v)
    analogous1 = f"#{int(r1*255):02x}{int(g1*255):02x}{int(b1*255):02x}"
    
    analog_h2 = (h - 0.1) % 1.0
    r2, g2, b2 = colorsys.hsv_to_rgb(analog_h2, s, v)
    analogous2 = f"#{int(r2*255):02x}{int(g2*255):02x}{int(b2*255):02x}"
    
    # Triadic colors (three equally spaced colors on wheel)
    triad_h1 = (h + 1/3) % 1.0
    tr1, tg1, tb1 = colorsys.hsv_to_rgb(triad_h1, s, v)
    triadic1 = f"#{int(tr1*255):02x}{int(tg1*255):02x}{int(tb1*255):02x}"
    
    triad_h2 = (h + 2/3) % 1.0
    tr2, tg2, tb2 = colorsys.hsv_to_rgb(triad_h2, s, v)
    triadic2 = f"#{int(tr2*255):02x}{int(tg2*255):02x}{int(tb2*255):02x}"
    
    # Display color palettes with visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("##### Complementary Colors")
        st.markdown(f"""
        <div style="display: flex; margin-bottom: 15px;">
            <div style="flex: 1; height: 60px; background-color: {primary_hex}; border-radius: 4px 0 0 4px;"></div>
            <div style="flex: 1; height: 60px; background-color: {complementary}; border-radius: 0 4px 4px 0;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #6c757d;">
            <div>Primary: {primary_hex}</div>
            <div>Complementary: {complementary}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("##### Analogous Colors")
        st.markdown(f"""
        <div style="display: flex; margin-bottom: 15px;">
            <div style="flex: 1; height: 60px; background-color: {analogous2}; border-radius: 4px 0 0 4px;"></div>
            <div style="flex: 1; height: 60px; background-color: {primary_hex};"></div>
            <div style="flex: 1; height: 60px; background-color: {analogous1}; border-radius: 0 4px 4px 0;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #6c757d;">
            <div>{analogous2}</div>
            <div>{primary_hex}</div>
            <div>{analogous1}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.write("##### Triadic Colors")
        st.markdown(f"""
        <div style="display: flex; margin-bottom: 15px;">
            <div style="flex: 1; height: 60px; background-color: {primary_hex}; border-radius: 4px 0 0 4px;"></div>
            <div style="flex: 1; height: 60px; background-color: {triadic1};"></div>
            <div style="flex: 1; height: 60px; background-color: {triadic2}; border-radius: 0 4px 4px 0;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #6c757d;">
            <div>{primary_hex}</div>
            <div>{triadic1}</div>
            <div>{triadic2}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Shade and tint variations
        st.write("##### Shades & Tints")
        
        # Generate shades and tints
        tints = []
        shades = []
        
        for i in range(5):
            # Tints (lighter variations)
            tint_v = min(1.0, v + (1-v) * (i+1)/5)
            tint_r, tint_g, tint_b = colorsys.hsv_to_rgb(h, s, tint_v)
            tint = f"#{int(tint_r*255):02x}{int(tint_g*255):02x}{int(tint_b*255):02x}"
            tints.append(tint)
            
            # Shades (darker variations)
            shade_v = max(0, v * (5-i)/5)
            shade_r, shade_g, shade_b = colorsys.hsv_to_rgb(h, s, shade_v)
            shade = f"#{int(shade_r*255):02x}{int(shade_g*255):02x}{int(shade_b*255):02x}"
            shades.append(shade)
        
        # Display tints (light to dark)
        tints.reverse()  # So lightest is on top
        tint_divs = ''.join([f'<div style="height: 20px; background-color: {tint};"></div>' for tint in tints])
        
        # Display shades (light to dark)
        shade_divs = ''.join([f'<div style="height: 20px; background-color: {shade};"></div>' for shade in shades])
        
        st.markdown(f"""
        <div style="display: flex; margin-bottom: 15px;">
            <div style="flex: 1; border-radius: 4px 0 0 4px; overflow: hidden;">{tint_divs}</div>
            <div style="flex: 1; border-radius: 0 4px 4px 0; overflow: hidden;">{shade_divs}</div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #6c757d;">
            <div>Tints</div>
            <div>Shades</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional visual settings
    st.write("#### Highland Tower Professional Theme")
    st.info("🎨 Highland Tower Development uses a fixed professional enterprise theme with navy sidebar and clean white content areas for optimal readability and brand consistency.")
    
    st.markdown("""
    **Current Theme Features:**
    • Professional navy sidebar with Highland Tower branding
    • Clean white content areas for optimal readability
    • Enterprise-grade buttons and forms
    • Consistent color scheme across all modules
    • Mobile-responsive design for field operations
    """)
    
    # Apply visual changes
    if st.button("Refresh Interface", key="refresh_interface", type="primary"):
        st.success("Highland Tower interface refreshed successfully!")
            
    st.markdown('</div>', unsafe_allow_html=True)

def render_user_preferences():
    """Render user preferences settings."""
    st.subheader("User Preferences")
    
    # User profile and preferences
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    
    st.markdown("### Notification Settings")
    
    # Notification preferences with toggles
    notifications = {
        "Email Notifications": True,
        "RFI Updates": True,
        "Submittal Updates": True,
        "Schedule Changes": False,
        "Budget Alerts": True,
        "Daily Reports": False,
        "Safety Incidents": True,
        "Team Messages": False
    }
    
    # Display notification toggles
    for notification, default_value in notifications.items():
        state = st.toggle(notification, value=default_value)
    
    # Email notification frequency
    st.write("#### Notification Frequency")
    email_frequency = st.selectbox(
        "Email Digest Frequency",
        ["Immediately", "Daily Digest", "Weekly Digest", "None"],
        index=1
    )
    
    # Apply changes button
    st.button("Save Notification Preferences", type="primary")
    
    st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.15;'>", unsafe_allow_html=True)
    
    # Dashboard preferences
    st.markdown("### Dashboard Preferences")
    
    # Default page
    default_page = st.selectbox(
        "Default Dashboard View",
        ["Project Overview", "Cost Summary", "Schedule Summary", "Team Activity"],
        index=0
    )
    
    # Dashboard widgets
    st.write("#### Dashboard Widgets")
    st.caption("Select which widgets to display on your dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Project Progress", value=True)
        st.checkbox("Budget Summary", value=True)
        st.checkbox("Recent Activity", value=True)
        st.checkbox("Team Members", value=False)
    
    with col2:
        st.checkbox("Weather Forecast", value=True)
        st.checkbox("Key Dates", value=True)
        st.checkbox("Outstanding Items", value=True)
        st.checkbox("Quality Metrics", value=False)
    
    # Apply changes button
    st.button("Save Dashboard Preferences", type="primary")
            
    st.markdown('</div>', unsafe_allow_html=True)

def render_system_settings():
    """Render system settings."""
    st.subheader("System Settings")
    
    # System configuration settings
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    
    st.markdown("### Data Management")
    
    # Export/Import options
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("Export Data", help="Export all project data to CSV/Excel")
    
    with col2:
        st.button("Import Data", help="Import project data from CSV/Excel")
    
    # Data retention policy
    st.write("#### Data Retention")
    retention_policy = st.selectbox(
        "Document Retention Period",
        ["1 Year", "3 Years", "5 Years", "7 Years", "10 Years", "Forever"],
        index=3
    )
    
    # Backup settings
    st.write("#### Backup Settings")
    backup_frequency = st.selectbox(
        "Automatic Backup Frequency",
        ["Daily", "Weekly", "Monthly", "Never"],
        index=1
    )
    
    backup_time = st.time_input("Backup Time", value=datetime.strptime("02:00", "%H:%M").time())
    
    # Integration settings
    st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.15;'>", unsafe_allow_html=True)
    st.markdown("### Integrations")
    
    # API settings
    st.write("#### API Access")
    enable_api = st.toggle("Enable API Access", value=True)
    
    if enable_api:
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("API Key", value="••••••••••••••••", disabled=True)
        with col2:
            st.button("Regenerate API Key")
    
    # Third-party integrations with color badges
    st.write("#### Connected Services")
    
    integrations = [
        {"name": "Microsoft 365", "status": "Connected", "color": "#38d39f"},
        {"name": "Google Workspace", "status": "Not Connected", "color": "#ff5b5b"},
        {"name": "Procore", "status": "Connected", "color": "#38d39f"},
        {"name": "Autodesk BIM 360", "status": "Connected", "color": "#38d39f"},
        {"name": "Sage Accounting", "status": "Not Connected", "color": "#ff5b5b"},
        {"name": "Primavera P6", "status": "Connected", "color": "#38d39f"}
    ]
    
    for integration in integrations:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(integration["name"])
        with col2:
            st.markdown(f'<span style="background-color: {integration["color"]}20; color: {integration["color"]}; padding: 3px 8px; border-radius: 12px; font-size: 12px;">{integration["status"]}</span>', unsafe_allow_html=True)
        with col3:
            if integration["status"] == "Connected":
                st.button("Disconnect", key=f"disconnect_{integration['name'].lower().replace(' ', '_')}")
            else:
                st.button("Connect", key=f"connect_{integration['name'].lower().replace(' ', '_')}")
    
    # Save settings button
    st.button("Save System Settings", type="primary")
            
    st.markdown('</div>', unsafe_allow_html=True)

def render_about_page():
    """Render about page with version info and help resources."""
    st.subheader("About gcPanel")
    
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    
    # App logo and version
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("""
        <div style="background-color: #3e79f7; width: 100px; height: 100px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
            <span class="material-icons" style="font-size: 50px; color: white;">construction</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("# gcPanel")
        st.markdown("#### Construction Management Dashboard")
        st.markdown("Version 1.0.0 - May 2025")
    
    # System info
    st.markdown("### System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Platform:** Streamlit")
        st.markdown("**Database:** PostgreSQL")
        st.markdown("**Last Updated:** May 17, 2025")
    
    with col2:
        st.markdown("**License:** Enterprise")
        st.markdown("**Users:** 25/50")
        st.markdown("**Storage:** 45GB/100GB")
    
    # Features and modules
    st.markdown("### Available Modules")
    
    modules = [
        {"name": "Dashboard", "status": "Active"},
        {"name": "Project Management", "status": "Active"},
        {"name": "Engineering", "status": "Active"},
        {"name": "Field Operations", "status": "Active"},
        {"name": "Safety Management", "status": "Active"},
        {"name": "Contract Management", "status": "Active"},
        {"name": "Cost Management", "status": "Active"},
        {"name": "BIM Integration", "status": "Active"},
        {"name": "Closeout", "status": "Active"},
        {"name": "Quality Control", "status": "Available"},
        {"name": "Resource Management", "status": "Available"},
        {"name": "Reporting & Analytics", "status": "Available"}
    ]
    
    # Create a grid of modules with color indicators
    rows = [modules[i:i+3] for i in range(0, len(modules), 3)]
    
    for row in rows:
        cols = st.columns(3)
        for i, module in enumerate(row):
            with cols[i]:
                status_color = "#38d39f" if module["status"] == "Active" else "#f59e0b"
                st.markdown(f"""
                <div style="padding: 10px; border: 1px solid #eef2f7; border-radius: 8px; margin-bottom: 10px;">
                    <div style="font-weight: 500;">{module["name"]}</div>
                    <div style="font-size: 12px; color: {status_color};">{module["status"]}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Help and support
    st.markdown("### Help & Support")
    
    st.write("Need assistance with gcPanel? Contact our support team or access our help resources.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.button("User Guide", key="user_guide_btn")
    
    with col2:
        st.button("Video Tutorials", key="tutorials_btn")
    
    with col3:
        st.button("Contact Support", key="support_btn")
    
    # Legal info
    st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.15;'>", unsafe_allow_html=True)
    st.markdown("### Legal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("[Terms of Service](#)")
    
    with col2:
        st.markdown("[Privacy Policy](#)")
    
    st.markdown('</div>', unsafe_allow_html=True)