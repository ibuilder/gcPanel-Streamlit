"""
Mobile Field Companion Module for gcPanel.

This module provides specialized mobile-friendly views and functionality
for field personnel who need to access construction data on-site.
"""

import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime, timedelta
from utils.mobile.responsive_layout import add_mobile_styles, create_responsive_card

def render_mobile_field_companion():
    """Render the mobile field companion interface."""
    # Apply mobile optimizations
    add_mobile_styles()
    
    st.title("Field Companion")
    
    # Display offline indicator with custom styling
    st.markdown("""
    <div class="offline-indicator">
        You are currently offline. Only saved data is available.
    </div>
    """, unsafe_allow_html=True)
    
    # Top quick actions
    st.subheader("Quick Actions")
    
    # Create a responsive grid for quick action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📸 Capture Photo", use_container_width=True):
            st.session_state.mobile_view = "photo_capture"
    
    with col2:
        if st.button("📝 Daily Log", use_container_width=True):
            st.session_state.mobile_view = "daily_log"
    
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("✓ Checklist", use_container_width=True):
            st.session_state.mobile_view = "checklist"
    
    with col4:
        if st.button("⚠️ Report Issue", use_container_width=True):
            st.session_state.mobile_view = "report_issue"
    
    # Initialize the mobile view if not set
    if "mobile_view" not in st.session_state:
        st.session_state.mobile_view = "dashboard"
    
    # Render the selected mobile view
    current_view = st.session_state.mobile_view
    
    if current_view == "dashboard":
        render_field_dashboard()
    elif current_view == "photo_capture":
        render_photo_capture()
    elif current_view == "daily_log":
        render_daily_log()
    elif current_view == "checklist":
        render_checklist()
    elif current_view == "report_issue":
        render_issue_report()
    
    # Bottom navigation
    st.markdown("""
    <style>
    .mobile-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
    }
    
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        color: #333;
        text-decoration: none;
        font-size: 0.8rem;
        cursor: pointer;
    }
    
    .nav-icon {
        font-size: 1.5rem;
        margin-bottom: 4px;
    }
    
    .active {
        color: #3B82F6;
    }
    </style>
    
    <div class="mobile-nav">
        <div class="nav-item" id="nav-home">
            <div class="nav-icon">🏠</div>
            <div>Home</div>
        </div>
        <div class="nav-item" id="nav-tasks">
            <div class="nav-icon">📋</div>
            <div>Tasks</div>
        </div>
        <div class="nav-item" id="nav-docs">
            <div class="nav-icon">📄</div>
            <div>Docs</div>
        </div>
        <div class="nav-item" id="nav-profile">
            <div class="nav-icon">👤</div>
            <div>Profile</div>
        </div>
    </div>
    
    <script>
    // Add click handlers for navigation
    document.getElementById('nav-home').addEventListener('click', function() {
        // Set a value in localStorage that will be detected on page reload
        localStorage.setItem('mobileView', 'dashboard');
        window.location.reload();
    });
    
    document.getElementById('nav-tasks').addEventListener('click', function() {
        localStorage.setItem('mobileView', 'checklist');
        window.location.reload();
    });
    
    document.getElementById('nav-docs').addEventListener('click', function() {
        localStorage.setItem('mobileView', 'documents');
        window.location.reload();
    });
    
    document.getElementById('nav-profile').addEventListener('click', function() {
        localStorage.setItem('mobileView', 'profile');
        window.location.reload();
    });
    
    // Check localStorage on page load
    document.addEventListener('DOMContentLoaded', function() {
        const view = localStorage.getItem('mobileView');
        if (view) {
            // Here we would normally update Streamlit, but we can't directly
            // So we'll just mark the active tab
            const navItems = document.querySelectorAll('.nav-item');
            navItems.forEach(item => item.classList.remove('active'));
            
            if (view === 'dashboard') {
                document.getElementById('nav-home').classList.add('active');
            } else if (view === 'checklist') {
                document.getElementById('nav-tasks').classList.add('active');
            } else if (view === 'documents') {
                document.getElementById('nav-docs').classList.add('active');
            } else if (view === 'profile') {
                document.getElementById('nav-profile').classList.add('active');
            }
        }
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Add some spacing at the bottom to prevent content from being hidden by nav bar
    st.markdown("<div style='height:70px'></div>", unsafe_allow_html=True)

def render_field_dashboard():
    """Render the field dashboard view."""
    st.subheader("Today's Overview")
    
    # Project details card
    create_responsive_card(
        title="Highland Tower Development",
        content="Currently at 85% completion. 3 tasks assigned to you today."
    )
    
    # Project progress
    st.markdown("### Project Progress")
    
    progress = 85
    st.progress(progress / 100)
    st.markdown(f"**{progress}%** complete")
    
    # Weather information
    st.markdown("### Weather at Job Site")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Current:** 72°F, Partly Cloudy")
    with col2:
        st.markdown("**Forecast:** Light rain expected at 2PM")
    
    # Today's schedule
    st.markdown("### Today's Schedule")
    
    # Mock data for today's schedule
    today_schedule = [
        {"time": "8:00 AM", "task": "Team Huddle", "location": "Site Office"},
        {"time": "9:30 AM", "task": "Concrete Pour Inspection", "location": "Floor 12"},
        {"time": "1:00 PM", "task": "Safety Inspection", "location": "Floors 10-14"},
        {"time": "3:30 PM", "task": "Subcontractor Meeting", "location": "Site Office"}
    ]
    
    for item in today_schedule:
        st.markdown(f"**{item['time']}** - {item['task']} *({item['location']})*")
    
    # Recent activity
    st.markdown("### Recent Site Activity")
    
    # Mock data for recent activity
    recent_activity = [
        {"time": "Yesterday", "activity": "Electrical rough-in completed on floors 10-12"},
        {"time": "2 days ago", "activity": "Window installation started on floor 14"},
        {"time": "3 days ago", "activity": "Plumbing inspection passed on floors 8-9"}
    ]
    
    for item in recent_activity:
        st.markdown(f"**{item['time']}**: {item['activity']}")

def render_photo_capture():
    """Render the photo capture interface."""
    st.subheader("Capture Site Photo")
    
    # Back button
    if st.button("← Back to Dashboard"):
        st.session_state.mobile_view = "dashboard"
        st.rerun()
    
    # Photo capture interface
    st.markdown("Capture a photo for documentation:")
    
    # In a real app, this would use JavaScript to access the device camera
    # For this demo, we'll use a file uploader
    uploaded_file = st.file_uploader("Choose a photo", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        # Photo metadata
        st.markdown("### Photo Details")
        
        # Location
        location = st.selectbox(
            "Location",
            ["Floor 1", "Floor 2", "Floor 3", "Floor 4", "Floor 5", "Floor 6", 
             "Floor 7", "Floor 8", "Floor 9", "Floor 10", "Floor 11", "Floor 12",
             "Floor 13", "Floor 14", "Floor 15", "Site Exterior", "Basement 1", "Basement 2"]
        )
        
        # Category
        category = st.selectbox(
            "Category",
            ["Progress Documentation", "Safety Issue", "Quality Control", 
             "Material Delivery", "As-Built Condition", "Other"]
        )
        
        # Description
        description = st.text_area("Description", "")
        
        # Tags
        tags = st.text_input("Tags (comma separated)")
        
        # Save button
        if st.button("Save Photo"):
            st.success("Photo saved successfully!")
            
            # In a real app, this would save to a database
            # For this demo, we'll just show success message
            
            # Option to add another photo or return to dashboard
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Add Another Photo"):
                    st.rerun()
            
            with col2:
                if st.button("Return to Dashboard"):
                    st.session_state.mobile_view = "dashboard"
                    st.rerun()

def render_daily_log():
    """Render the daily log interface."""
    st.subheader("Daily Field Log")
    
    # Back button
    if st.button("← Back to Dashboard"):
        st.session_state.mobile_view = "dashboard"
        st.rerun()
    
    # Date selection with default to today
    log_date = st.date_input("Log Date", datetime.now())
    
    # Weather conditions
    st.markdown("### Weather Conditions")
    col1, col2 = st.columns(2)
    
    with col1:
        temperature = st.number_input("Temperature (°F)", value=72)
    
    with col2:
        weather_condition = st.selectbox(
            "Conditions",
            ["Clear", "Partly Cloudy", "Cloudy", "Rain", "Snow", "Windy"]
        )
    
    # Workforce
    st.markdown("### Workforce")
    
    # Companies present
    companies_present = st.multiselect(
        "Companies On Site",
        ["Highland Construction", "ABC Electrical", "XYZ Plumbing", 
         "Metro Concrete", "City Inspectors", "Ace Glass", "Western HVAC"]
    )
    
    # Worker counts
    col1, col2 = st.columns(2)
    
    with col1:
        worker_count = st.number_input("Total Workers on Site", min_value=0, value=25)
    
    with col2:
        hours_worked = st.number_input("Total Hours Worked", min_value=0, value=200)
    
    # Work completed
    st.markdown("### Work Completed")
    work_completed = st.text_area("Describe work completed today", height=100)
    
    # Materials delivered
    st.markdown("### Materials Delivered")
    materials_delivered = st.text_area("List materials delivered to site", height=100)
    
    # Equipment used
    st.markdown("### Equipment Used")
    equipment_used = st.text_area("List equipment used on site", height=100)
    
    # Issues/Delays
    st.markdown("### Issues or Delays")
    issues = st.text_area("Note any issues or delays", height=100)
    
    # Notes
    st.markdown("### General Notes")
    notes = st.text_area("Additional notes", height=100)
    
    # Photos
    st.markdown("### Attach Photos")
    photos = st.file_uploader("Upload photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    # Save button
    if st.button("Save Daily Log"):
        st.success("Daily log saved successfully!")
        
        # In a real app, this would save to a database
        # For this demo, we'll just show a success message
        
        if st.button("Return to Dashboard"):
            st.session_state.mobile_view = "dashboard"
            st.rerun()

def render_checklist():
    """Render the checklist interface."""
    st.subheader("Field Checklists")
    
    # Back button
    if st.button("← Back to Dashboard"):
        st.session_state.mobile_view = "dashboard"
        st.rerun()
    
    # Checklist type selection
    checklist_type = st.selectbox(
        "Checklist Type",
        ["Safety Inspection", "Quality Control", "Pre-Pour Concrete", 
         "MEP Rough-In", "Building Envelope", "Final Inspection"]
    )
    
    # Location
    location = st.selectbox(
        "Location",
        ["Floor 1", "Floor 2", "Floor 3", "Floor 4", "Floor 5", "Floor 6", 
         "Floor 7", "Floor 8", "Floor 9", "Floor 10", "Floor 11", "Floor 12",
         "Floor 13", "Floor 14", "Floor 15", "Site Exterior", "Basement 1", "Basement 2"]
    )
    
    # Initialize checklist items in session state if not present
    if "checklist_items" not in st.session_state:
        # Define default checklist items based on type
        if checklist_type == "Safety Inspection":
            st.session_state.checklist_items = [
                {"text": "Personal protective equipment being worn", "checked": False},
                {"text": "Fall protection in place", "checked": False},
                {"text": "Fire extinguishers accessible", "checked": False},
                {"text": "Emergency exits clear", "checked": False},
                {"text": "Warning signs posted", "checked": False},
                {"text": "Equipment inspected and tagged", "checked": False},
                {"text": "First aid kit fully stocked", "checked": False},
                {"text": "Proper lighting in work areas", "checked": False},
                {"text": "Trip hazards removed", "checked": False},
                {"text": "SDS sheets available for materials", "checked": False}
            ]
        elif checklist_type == "Quality Control":
            st.session_state.checklist_items = [
                {"text": "Work complies with approved plans", "checked": False},
                {"text": "Material quality meets specifications", "checked": False},
                {"text": "Proper tolerances maintained", "checked": False},
                {"text": "Surface finish as specified", "checked": False},
                {"text": "No visible defects", "checked": False},
                {"text": "Dimensions verified", "checked": False},
                {"text": "Installation methods follow guidelines", "checked": False},
                {"text": "Equipment operates correctly", "checked": False},
                {"text": "Testing performed and passed", "checked": False},
                {"text": "Previous deficiencies corrected", "checked": False}
            ]
        elif checklist_type == "Pre-Pour Concrete":
            st.session_state.checklist_items = [
                {"text": "Formwork secure and properly braced", "checked": False},
                {"text": "Reinforcement size and spacing correct", "checked": False},
                {"text": "Embedments and sleeves positioned correctly", "checked": False},
                {"text": "Formwork clean of debris", "checked": False},
                {"text": "Required concrete strength verified", "checked": False},
                {"text": "Subgrade properly prepared", "checked": False},
                {"text": "Moisture barrier installed (if required)", "checked": False},
                {"text": "Concrete delivery scheduled", "checked": False},
                {"text": "Finishing tools on site", "checked": False},
                {"text": "Curing materials available", "checked": False}
            ]
        else:
            # Generic checklist for other types
            st.session_state.checklist_items = [
                {"text": "Item 1", "checked": False},
                {"text": "Item 2", "checked": False},
                {"text": "Item 3", "checked": False},
                {"text": "Item 4", "checked": False},
                {"text": "Item 5", "checked": False}
            ]
    
    # Display checklist items
    st.markdown("### Checklist Items")
    
    # Update checklist items based on selections
    items_to_update = []
    
    for i, item in enumerate(st.session_state.checklist_items):
        checked = st.checkbox(item["text"], value=item["checked"], key=f"item_{i}")
        items_to_update.append({"text": item["text"], "checked": checked})
    
    # Update session state
    st.session_state.checklist_items = items_to_update
    
    # Add custom items
    st.markdown("### Add Custom Item")
    new_item = st.text_input("New checklist item")
    
    if st.button("Add Item") and new_item:
        st.session_state.checklist_items.append({"text": new_item, "checked": False})
        st.rerun()
    
    # Notes
    st.markdown("### Notes")
    notes = st.text_area("Additional notes or observations", height=100)
    
    # Photos
    st.markdown("### Attach Photos")
    photos = st.file_uploader("Upload supporting photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    # Save button
    if st.button("Save Checklist"):
        # Calculate completion percentage
        total_items = len(st.session_state.checklist_items)
        checked_items = sum(1 for item in st.session_state.checklist_items if item["checked"])
        completion_pct = 0 if total_items == 0 else (checked_items / total_items) * 100
        
        st.success(f"Checklist saved successfully! Completion: {completion_pct:.0f}%")
        
        # In a real app, this would save to a database
        # For this demo, we'll just show a success message
        
        if st.button("Return to Dashboard"):
            st.session_state.mobile_view = "dashboard"
            st.rerun()

def render_issue_report():
    """Render the issue reporting interface."""
    st.subheader("Report Issue")
    
    # Back button
    if st.button("← Back to Dashboard"):
        st.session_state.mobile_view = "dashboard"
        st.rerun()
    
    # Issue details
    st.markdown("### Issue Details")
    
    # Issue type
    issue_type = st.selectbox(
        "Issue Type",
        ["Safety Hazard", "Quality Issue", "Design Conflict", "Material Defect", 
         "Schedule Delay", "Equipment Problem", "Other"]
    )
    
    # Severity
    severity = st.select_slider(
        "Severity",
        options=["Low", "Medium", "High", "Critical"]
    )
    
    # Location
    location = st.selectbox(
        "Location",
        ["Floor 1", "Floor 2", "Floor 3", "Floor 4", "Floor 5", "Floor 6", 
         "Floor 7", "Floor 8", "Floor 9", "Floor 10", "Floor 11", "Floor 12",
         "Floor 13", "Floor 14", "Floor 15", "Site Exterior", "Basement 1", "Basement 2"]
    )
    
    # Description
    description = st.text_area("Describe the issue in detail", height=150)
    
    # Affected trades
    affected_trades = st.multiselect(
        "Affected Trades",
        ["General Contractor", "Structural", "Electrical", "Plumbing", "HVAC", 
         "Drywall", "Painting", "Flooring", "Concrete", "Steel", "Masonry", 
         "Glass/Glazing", "Roofing", "Elevators"]
    )
    
    # Immediate actions taken
    immediate_actions = st.text_area("Immediate actions taken (if any)", height=100)
    
    # Photos
    st.markdown("### Attach Photos")
    photos = st.file_uploader("Upload photos of the issue", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    # Assign to
    assign_to = st.selectbox(
        "Assign To",
        ["Project Manager", "Superintendent", "Safety Manager", "Quality Control", 
         "Field Engineer", "Subcontractor Manager"]
    )
    
    # Priority assignment
    priority = st.select_slider(
        "Priority",
        options=["Low", "Medium", "High", "Urgent"]
    )
    
    # Submit button
    if st.button("Submit Issue Report"):
        st.success("Issue report submitted successfully!")
        
        # In a real app, this would save to a database and notify the assigned person
        # For this demo, we'll just show a success message
        
        if st.button("Return to Dashboard"):
            st.session_state.mobile_view = "dashboard"
            st.rerun()