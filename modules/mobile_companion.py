"""
Mobile Companion module for gcPanel.

This module provides a dedicated mobile interface for field personnel,
with PWA support for offline capabilities, optimized layouts for smaller screens,
and quick access to field-relevant features.
"""

import streamlit as st
from datetime import datetime, timedelta
import random
import json

# Import mobile utilities
from utils.mobile.responsive_layout import add_mobile_styles, create_responsive_card, create_mobile_list_item, create_mobile_tab_layout
from utils.mobile.pwa_support import setup_pwa, check_offline_status, cache_file_for_offline, get_cached_files

def render_mobile_companion():
    """Render the mobile companion dashboard optimized for field personnel."""
    # Add mobile-friendly styles
    add_mobile_styles()
    
    # Set up PWA support for offline access
    setup_pwa()
    
    # Check if we're in offline mode
    is_offline = check_offline_status()
    
    # Display header with project information
    from utils.mobile.components import render_mobile_header
    render_mobile_header("Highland Tower", "Field Companion")
    
    # Display offline indicator if needed
    if is_offline:
        st.warning("⚠️ You are currently in offline mode. Some features may be limited.")
    
    # Quick action buttons
    render_quick_actions()
    
    # Create a tabbed interface for different sections
    tabs = [
        {"icon": "📋", "label": "Activities", "content": render_todays_activities()},
        {"icon": "⚠️", "label": "Issues", "content": render_field_issues()},
        {"icon": "📄", "label": "Documents", "content": render_offline_documents()},
        {"icon": "✅", "label": "Safety", "content": render_safety_checklist()},
        {"icon": "🌤️", "label": "Weather", "content": render_weather_conditions()}
    ]
    
    selected_tab = create_mobile_tab_layout(tabs)
    
    # Add a floating action button for quick report using Streamlit's button
    # This removes the embedded HTML and uses standard Streamlit components
    report_button_col = st.container()
    with report_button_col:
        st.write("")  # Add some spacing
        if st.button("➕ Report Issue", key="report_issue_button", type="primary"):
            st.session_state.show_issue_form = True
            st.rerun()
    
    # Display issue form if needed
    if st.session_state.get("show_issue_form", False):
        with st.form("issue_report_form"):
            st.subheader("Report Field Issue")
            
            issue_type = st.selectbox("Issue Type", [
                "Safety Concern", "Quality Issue", "Material Shortage",
                "Equipment Problem", "Design Conflict", "Other"
            ])
            
            location = st.text_input("Location (Floor/Zone/Room)")
            description = st.text_area("Description")
            priority = st.select_slider("Priority", options=["Low", "Medium", "High", "Critical"])
            
            photo_col, assign_col = st.columns(2)
            with photo_col:
                photo = st.file_uploader("Add Photo", type=["jpg", "jpeg", "png"])
            
            with assign_col:
                assigned_to = st.selectbox("Assign to", [
                    "Site Supervisor", "Project Manager", "Safety Officer", 
                    "Quality Control", "Subcontractor"
                ])
            
            submit_col, cancel_col = st.columns(2)
            with submit_col:
                submit = st.form_submit_button("Submit Issue")
            
            with cancel_col:
                cancel = st.form_submit_button("Cancel")
            
            if submit:
                # Process issue submission
                st.success("Issue reported successfully!")
                st.session_state.show_issue_form = False
                st.rerun()
            
            if cancel:
                st.session_state.show_issue_form = False
                st.rerun()

def render_quick_actions():
    """Render quick action buttons for field tasks."""
    # Create a 2x2 grid of quick action buttons
    st.subheader("Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Use the mobile_card component instead of direct HTML
        if create_responsive_card(
            icon="🔍",
            title="QA Check",
            action="Quality assurance inspection form",
            button_text="QA Check",
            button_key="qa_check_btn"
        ):
            st.session_state.quick_action = "qa_check"
            st.rerun()
    
    with col2:
        # Use the mobile_card component instead of direct HTML
        if create_responsive_card(
            icon="📝",
            title="Daily Log",
            action="Record daily work activities",
            button_text="Daily Log",
            button_key="daily_log_btn"
        ):
            st.session_state.quick_action = "daily_log"
            st.rerun()
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Use the mobile_card component instead of direct HTML
        if create_responsive_card(
            icon="📦",
            title="Materials",
            action="Track material deliveries and usage",
            button_text="Materials",
            button_key="material_track_btn"
        ):
            st.session_state.quick_action = "materials"
            st.rerun()
    
    with col4:
        # Use the mobile_card component instead of direct HTML
        if create_responsive_card(
            icon="📸",
            title="Photo Doc",
            action="Document site conditions with photos",
            button_text="Photo Doc",
            button_key="photo_doc_btn"
        ):
            st.session_state.quick_action = "photo_doc"
            st.rerun()
    
    # Handle quick action selection
    if st.session_state.get("quick_action") == "qa_check":
        st.subheader("Quality Assurance Check")
        
        qa_type = st.selectbox("Check Type", [
            "Concrete Placement", "Steel Erection", "Mechanical Installation",
            "Electrical Installation", "Finishes Inspection"
        ])
        
        location = st.text_input("Location")
        notes = st.text_area("Inspection Notes")
        status = st.radio("Status", ["Pass", "Fail", "Pending Correction"])
        
        if st.button("Submit QA Check"):
            st.success("QA Check submitted successfully!")
            st.session_state.pop("quick_action")
            st.rerun()
            
        if st.button("Cancel", key="cancel_qa"):
            st.session_state.pop("quick_action")
            st.rerun()
    
    elif st.session_state.get("quick_action") == "daily_log":
        st.subheader("Daily Field Log")
        
        date = st.date_input("Date", datetime.now())
        weather = st.selectbox("Weather Conditions", [
            "Sunny", "Partly Cloudy", "Overcast", "Rain", "Snow", "Windy"
        ])
        
        temp_col, wind_col = st.columns(2)
        with temp_col:
            temperature = st.number_input("Temperature (°F)", 0, 120, 75)
        
        with wind_col:
            wind = st.number_input("Wind Speed (mph)", 0, 100, 5)
        
        workers = st.number_input("Workers on Site", 0, 500, 35)
        activities = st.text_area("Activities Performed")
        issues = st.text_area("Issues/Delays Encountered")
        
        if st.button("Submit Daily Log"):
            st.success("Daily Log submitted successfully!")
            st.session_state.pop("quick_action")
            st.rerun()
            
        if st.button("Cancel", key="cancel_log"):
            st.session_state.pop("quick_action")
            st.rerun()
    
    elif st.session_state.get("quick_action") == "materials":
        st.subheader("Material Tracking")
        
        material = st.selectbox("Material Type", [
            "Concrete", "Structural Steel", "Rebar", "Lumber", 
            "Mechanical Equipment", "Electrical Equipment", "Finishes"
        ])
        
        status = st.selectbox("Status", [
            "Received", "Inspected", "Rejected", "Installed"
        ])
        
        quantity = st.number_input("Quantity", 0, 10000, 1)
        location = st.text_input("Storage Location")
        notes = st.text_area("Notes")
        
        if st.button("Submit Material Update"):
            st.success("Material update submitted successfully!")
            st.session_state.pop("quick_action")
            st.rerun()
            
        if st.button("Cancel", key="cancel_material"):
            st.session_state.pop("quick_action")
            st.rerun()
    
    elif st.session_state.get("quick_action") == "photo_doc":
        st.subheader("Photo Documentation")
        
        photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])
        
        if photo:
            st.image(photo, use_column_width=True)
        
        type_col, location_col = st.columns(2)
        
        with type_col:
            photo_type = st.selectbox("Photo Type", [
                "Progress", "Issue", "Material", "Safety", "Quality"
            ])
        
        with location_col:
            location = st.text_input("Location")
        
        description = st.text_area("Description")
        
        if st.button("Submit Photo"):
            st.success("Photo submitted successfully!")
            st.session_state.pop("quick_action")
            st.rerun()
            
        if st.button("Cancel", key="cancel_photo"):
            st.session_state.pop("quick_action")
            st.rerun()

def render_todays_activities():
    """Render today's scheduled activities."""
    # Get today's date for display
    today = datetime.now().strftime("%A, %B %d")
    
    content = f"""
    <h3 style="margin-bottom: 15px;">Today's Activities ({today})</h3>
    """
    
    # Sample activities for demonstration
    activities = [
        {
            "title": "Concrete Pour - Level 3 West",
            "time": "7:00 AM - 10:00 AM",
            "status": "Completed",
            "team": "Concrete Crew"
        },
        {
            "title": "Electrical Rough-in - Level 4",
            "time": "8:00 AM - 4:00 PM",
            "status": "In Progress",
            "team": "Electrical"
        },
        {
            "title": "Safety Meeting - All Personnel",
            "time": "12:00 PM - 12:30 PM",
            "status": "Upcoming",
            "team": "All Crews"
        },
        {
            "title": "Structural Inspection - Level 2",
            "time": "2:00 PM - 3:00 PM",
            "status": "Upcoming",
            "team": "QA/QC"
        },
        {
            "title": "Material Delivery - Windows",
            "time": "3:30 PM - 4:30 PM",
            "status": "Upcoming",
            "team": "Receiving"
        }
    ]
    
    # Display activity list
    for activity in activities:
        status_color = {
            "Completed": "#10b981",  # Green
            "In Progress": "#3b82f6",  # Blue
            "Upcoming": "#6b7280"  # Gray
        }.get(activity["status"], "#6b7280")
        
        content += f"""
        <div style="background-color: white; border-radius: 8px; padding: 12px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <div style="font-weight: 600;">{activity["title"]}</div>
                <div style="color: {status_color}; font-weight: 500; font-size: 0.9rem;">{activity["status"]}</div>
            </div>
            <div style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">
                ⏱️ {activity["time"]} • 👥 {activity["team"]}
            </div>
        </div>
        """
    
    return content

def render_field_issues():
    """Render field issues reporting section."""
    from utils.mobile.components import render_mobile_tag, render_list_item, render_card_with_icon
    
    st.subheader("Field Issues")
    
    # Sample issues for demonstration
    issues = [
        {
            "id": "ISS-127",
            "title": "Plumbing conflict with HVAC duct",
            "location": "Level 5, Unit 512",
            "priority": "High",
            "status": "Open",
            "reported_by": "Mike Chen",
            "date": "Today, 9:15 AM"
        },
        {
            "id": "ISS-126",
            "title": "Missing electrical boxes per drawing",
            "location": "Level 4, East Corridor",
            "priority": "Medium",
            "status": "Assigned",
            "reported_by": "Sarah Johnson",
            "date": "Yesterday, 3:30 PM"
        },
        {
            "id": "ISS-125",
            "title": "Concrete honeycomb in column",
            "location": "Level 2, Column C4",
            "priority": "High",
            "status": "In Progress",
            "reported_by": "John Smith",
            "date": "May 18, 11:20 AM"
        },
        {
            "id": "ISS-124",
            "title": "Damaged drywall from water leak",
            "location": "Level 6, Units 605-608",
            "priority": "Medium", 
            "status": "Resolved",
            "reported_by": "Lisa Rodriguez",
            "date": "May 17, 8:45 AM" 
        }
    ]
    
    # Display issues list using Streamlit components
    for issue in issues:
        # Set colors based on priority and status
        priority_colors = {
            "Low": ("green", "#E8F5E9"),
            "Medium": ("orange", "#FFF3E0"),
            "High": ("red", "#FFEBEE"),
            "Critical": ("darkred", "#FFD7D7")
        }
        
        status_colors = {
            "Open": ("red", "#FFEBEE"),
            "Assigned": ("orange", "#FFF3E0"),
            "In Progress": ("blue", "#E3F2FD"),
            "Resolved": ("green", "#E8F5E9")
        }
        
        priority_color, priority_bg = priority_colors.get(issue["priority"], ("gray", "#F5F5F5"))
        status_color, status_bg = status_colors.get(issue["status"], ("gray", "#F5F5F5"))
        
        # Create a nice card for each issue
        with st.container():
            # Title row with status
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{issue['title']}**")
            with col2:
                st.markdown(
                    f"<span style='color:{status_color};font-weight:500;'>{issue['status']}</span>", 
                    unsafe_allow_html=True
                )
            
            # Location info
            st.caption(f"📍 {issue['location']}")
            
            # Bottom row with priority, ID, and date
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(
                    f"<span style='background-color:{priority_bg};color:{priority_color};padding:2px 6px;border-radius:4px;font-size:0.8rem;'>{issue['priority']}</span> <span style='color:#666;font-size:0.8rem;'>{issue['id']}</span>", 
                    unsafe_allow_html=True
                )
            with col2:
                st.caption(f"{issue['date']}")
            
            # Add a light divider
            st.markdown("---")
    
    # Empty string to satisfy the return type expected by the caller
    return ""

def render_offline_documents():
    """Render offline-capable document access."""
    st.subheader("Offline Documents")
    st.caption("Documents cached for offline access. Tap to view.")
    
    # Get cached documents (in a real app, this would use the cache_file_for_offline function)
    documents = [
        {
            "id": "DOC-001",
            "title": "Foundation Specifications",
            "type": "Technical Specification",
            "size": "2.4 MB", 
            "cached_date": "May 18, 2025"
        },
        {
            "id": "DOC-015",
            "title": "Floor Plans - Residential Levels 1-7",
            "type": "Drawing Set",
            "size": "18.7 MB",
            "cached_date": "May 18, 2025"
        },
        {
            "id": "DOC-023",
            "title": "Electrical Layout - Retail Spaces",
            "type": "Drawing Set",
            "size": "9.2 MB",
            "cached_date": "May 17, 2025"
        },
        {
            "id": "DOC-047",
            "title": "Highland Tower Project Schedule",
            "type": "Schedule",
            "size": "1.8 MB",
            "cached_date": "May 17, 2025"
        },
        {
            "id": "DOC-089",
            "title": "Safety Protocols & Procedures",
            "type": "Manual",
            "size": "3.5 MB",
            "cached_date": "May 16, 2025"
        }
    ]
    
    # Display document list
    for doc in documents:
        doc_icon = {
            "Technical Specification": "📄",
            "Drawing Set": "🗺️",
            "Schedule": "📅",
            "Manual": "📚",
            "Report": "📊"
        }.get(doc["type"], "📄")
        
        # Create a card for each document
        st.container()
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.markdown(f"### {doc_icon}")
            
        with col2:
            st.markdown(f"**{doc['title']}**")
            st.caption(f"{doc['type']} • {doc['size']} • Cached {doc['cached_date']}")
        
        st.markdown("---")
    
    # Add option to cache more documents
    st.container()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("Cache More Documents", key="cache_more_docs")
    
    # Empty string to satisfy the return type expected by the caller
    return ""

def render_offline_document_item(doc, icon="📄"):
    """Render a single offline document item."""
    # This function is no longer needed as we're using Streamlit components directly
    # Keeping it for backwards compatibility
    return ""

def render_safety_checklist():
    """Render safety checklist for field personnel."""
    st.subheader("Safety Checklist")
    st.caption("Complete daily safety inspection before beginning work.")
    
    if "safety_checklist_complete" not in st.session_state:
        st.session_state.safety_checklist_complete = False
    
    if "safety_checklist_items" not in st.session_state:
        st.session_state.safety_checklist_items = {
            "ppe": False,
            "hazards": False,
            "equipment": False,
            "fire_extinguishers": False,
            "first_aid": False,
            "emergency_exits": False,
            "fall_protection": False,
            "housekeeping": False
        }
    
    # Create the checklist UI using Streamlit components
    st.container()
    with st.expander("Daily Safety Inspection", expanded=True):
        all_complete = render_checklist_items()
    
    # For tab interface compatibility, we need to return an empty string
    # The actual functionality happens via streamlit interface elements
    return ""

def render_checklist_items(readonly=False):
    """Render safety checklist items and return if all are checked."""
    checklist_items = [
        {
            "id": "ppe",
            "label": "All workers have proper PPE (hard hat, safety glasses, gloves, vests)"
        },
        {
            "id": "hazards",
            "label": "Work area is free of potential hazards and properly marked"
        },
        {
            "id": "equipment",
            "label": "All equipment and tools are in good working condition"
        },
        {
            "id": "fire_extinguishers",
            "label": "Fire extinguishers are accessible and properly charged"
        },
        {
            "id": "first_aid",
            "label": "First aid kits are stocked and accessible"
        },
        {
            "id": "emergency_exits",
            "label": "Emergency exits are clear and accessible"
        },
        {
            "id": "fall_protection",
            "label": "Fall protection is in place where required"
        },
        {
            "id": "housekeeping",
            "label": "Site is clean and materials are properly stored"
        }
    ]
    
    for item in checklist_items:
        checked = st.checkbox(
            item["label"],
            value=st.session_state.safety_checklist_items[item["id"]],
            disabled=readonly,
            key=f"safety_{item['id']}"
        )
        st.session_state.safety_checklist_items[item["id"]] = checked
    
    # Check if all items are complete
    all_complete = all(st.session_state.safety_checklist_items.values())
    
    if all_complete and not st.session_state.safety_checklist_complete:
        if st.button("Submit Safety Checklist"):
            st.session_state.safety_checklist_complete = True
            st.success("Safety checklist completed and submitted!")
    
    if st.session_state.safety_checklist_complete:
        st.info("✅ Safety checklist completed for today.")
        
        if st.button("Reset Checklist"):
            for key in st.session_state.safety_checklist_items:
                st.session_state.safety_checklist_items[key] = False
            st.session_state.safety_checklist_complete = False
            st.rerun()
    
    return all_complete

def render_weather_conditions():
    """Render current and forecasted weather conditions."""
    from utils.mobile.components import render_weather_card, render_mobile_alerts
    
    st.subheader("Weather Conditions")
    
    # Current conditions display
    current_weather = {
        "condition": "Partly Cloudy",
        "temperature": "72°F",
        "feels_like": "70°F",
        "humidity": "45%",
        "wind": "8 mph NW",
        "precipitation": "0%"
    }
    
    # Use our reusable weather card component
    render_weather_card(
        temperature=current_weather["temperature"],
        conditions=current_weather["condition"],
        forecast="Clear skies expected for the next 24 hours with temperatures ranging from 65-75°F.",
        location="Highland Tower Site"
    )
    
    # Display additional weather details
    col1, col2 = st.columns(2)
    with col1:
        st.caption("Feels Like")
        st.write(current_weather["feels_like"])
        
        st.caption("Wind")
        st.write(current_weather["wind"])
    
    with col2:
        st.caption("Humidity")
        st.write(current_weather["humidity"])
        
        st.caption("Precipitation")
        st.write(current_weather["precipitation"])
    
    # 5-Day Forecast section
    st.subheader("5-Day Forecast")
    
    # Create a 5-day forecast using Streamlit components
    forecast_data = [
        {"day": "Today", "temp_high": "72°F", "temp_low": "65°F", "condition": "Partly Cloudy", "icon": "⛅"},
        {"day": "Tomorrow", "temp_high": "75°F", "temp_low": "67°F", "condition": "Sunny", "icon": "☀️"},
        {"day": "Wednesday", "temp_high": "70°F", "temp_low": "63°F", "condition": "Showers", "icon": "🌧️"},
        {"day": "Thursday", "temp_high": "68°F", "temp_low": "60°F", "condition": "Partly Cloudy", "icon": "⛅"},
        {"day": "Friday", "temp_high": "73°F", "temp_low": "66°F", "condition": "Sunny", "icon": "☀️"}
    ]
    
    # Display the forecast in a grid
    cols = st.columns(5)
    for i, day in enumerate(forecast_data):
        with cols[i]:
            st.markdown(f"**{day['day']}**")
            st.markdown(f"{day['icon']} {day['condition']}")
            st.markdown(f"High: {day['temp_high']}")
            st.markdown(f"Low: {day['temp_low']}")
    
    # Add weather alerts
    weather_alerts = [
        {
            "text": "Rain Expected Thursday. Take precautions to protect open areas and schedule work accordingly.",
            "type": "warning",
            "icon": "⚠️"
        }
    ]
    
    render_mobile_alerts(weather_alerts)

# Helper function for sending notifications
def send_notification(user_id, template_name, **kwargs):
    """
    Send a notification to a user using a template.
    
    Args:
        user_id (str): ID of the user to notify
        template_name (str): Name of the notification template to use
        **kwargs: Template variables
    """
    # In a real app, this would send the notification to the user
    # Here we just print what would be sent
    print(f"Notification to user {user_id} using template {template_name}")
    print(f"Template variables: {kwargs}")
    
    return True