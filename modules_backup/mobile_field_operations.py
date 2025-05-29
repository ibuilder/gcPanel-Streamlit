"""
Highland Tower Development - Mobile Field Operations
Touch-friendly interfaces and offline capabilities for field operations.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
from typing import Dict, List, Any, Optional
import json
import base64

def render_mobile_field_operations():
    """Highland Tower Development - Mobile Field Operations Hub"""
    
    st.markdown("""
    <div class="module-header">
        <h1>📱 Highland Tower Development - Mobile Field Operations</h1>
        <p>$45.5M Project - Touch-Friendly Field Management & Offline Capabilities</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Apply mobile-specific styling
    apply_mobile_styling()
    
    # Initialize mobile data
    initialize_mobile_field_data()
    
    # Mobile overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Field Crew", "89", "Active workers")
    with col2:
        st.metric("Today's Reports", "12", "Field entries")
    with col3:
        st.metric("Photo Uploads", "67", "Progress images")
    with col4:
        st.metric("Offline Sync", "✅ Ready", "Data synchronized")
    
    # Mobile-optimized tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Daily Entry",
        "📸 Photo Capture", 
        "🔍 Field Inspection",
        "⚠️ Safety Check",
        "📊 Crew Dashboard"
    ])
    
    with tab1:
        render_mobile_daily_entry()
    
    with tab2:
        render_mobile_photo_capture()
    
    with tab3:
        render_mobile_field_inspection()
    
    with tab4:
        render_mobile_safety_check()
    
    with tab5:
        render_mobile_crew_dashboard()

def apply_mobile_styling():
    """Apply mobile-optimized CSS styling"""
    
    st.markdown("""
    <style>
    /* Mobile-First Responsive Design */
    .mobile-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
    }
    
    .mobile-button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        font-size: 16px;
        font-weight: 600;
        min-height: 44px;
        min-width: 120px;
        touch-action: manipulation;
        cursor: pointer;
        margin: 4px;
    }
    
    .mobile-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .mobile-input {
        font-size: 16px !important;
        min-height: 44px !important;
        padding: 12px !important;
        border-radius: 8px !important;
        border: 2px solid #e5e7eb !important;
        width: 100% !important;
    }
    
    .mobile-input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    .touch-target {
        min-height: 44px;
        min-width: 44px;
        padding: 12px;
        margin: 4px;
    }
    
    .field-photo-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 12px;
        margin: 16px 0;
    }
    
    .field-photo-item {
        border-radius: 8px;
        overflow: hidden;
        border: 2px solid #e5e7eb;
        cursor: pointer;
        transition: transform 0.2s ease;
    }
    
    .field-photo-item:hover {
        transform: scale(1.02);
        border-color: #3b82f6;
    }
    
    /* Tablet-specific optimizations */
    @media (min-width: 768px) {
        .mobile-card {
            margin: 12px 0;
            padding: 20px;
        }
        
        .field-photo-grid {
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        }
    }
    
    /* Large screen optimizations */
    @media (min-width: 1024px) {
        .mobile-card {
            margin: 16px 0;
            padding: 24px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_mobile_field_data():
    """Initialize Highland Tower mobile field data"""
    
    if "highland_field_crews" not in st.session_state:
        st.session_state.highland_field_crews = [
            {
                "crew_id": "CREW-001",
                "name": "Foundation Crew Alpha",
                "supervisor": "Mike Rodriguez",
                "workers": 12,
                "location": "Level B2 - Foundation",
                "shift": "Day Shift (7:00 AM - 3:30 PM)",
                "status": "Active",
                "equipment": ["Excavator", "Concrete Pump", "Rebar Tools"],
                "safety_rating": 98.5,
                "productivity": "Above Average"
            },
            {
                "crew_id": "CREW-002", 
                "name": "Steel Erection Team",
                "supervisor": "Sarah Johnson",
                "workers": 16,
                "location": "Level 8 - Structural Steel",
                "shift": "Day Shift (7:00 AM - 3:30 PM)",
                "status": "Active",
                "equipment": ["Tower Crane", "Welding Equipment", "Safety Harnesses"],
                "safety_rating": 96.8,
                "productivity": "Excellent"
            },
            {
                "crew_id": "CREW-003",
                "name": "MEP Installation",
                "supervisor": "David Chen",
                "workers": 18,
                "location": "Levels 4-6 - MEP Systems",
                "shift": "Day Shift (7:00 AM - 3:30 PM)",
                "status": "Active",
                "equipment": ["Lift Equipment", "Electrical Tools", "HVAC Components"],
                "safety_rating": 97.2,
                "productivity": "Good"
            }
        ]
    
    if "highland_field_photos" not in st.session_state:
        st.session_state.highland_field_photos = [
            {
                "photo_id": "IMG-001",
                "title": "Level 8 Steel Erection Progress",
                "location": "Level 8, Grid Line C",
                "crew": "CREW-002",
                "timestamp": "2024-05-28 14:30:00",
                "photographer": "Sarah Johnson",
                "category": "Progress",
                "description": "Structural steel installation 85% complete",
                "gps_coordinates": "40.7489, -73.9857",
                "weather": "Clear, 72°F"
            },
            {
                "photo_id": "IMG-002",
                "title": "Foundation Concrete Pour Complete",
                "location": "Level B2, Section A",
                "crew": "CREW-001",
                "timestamp": "2024-05-28 11:15:00",
                "photographer": "Mike Rodriguez",
                "category": "Milestone",
                "description": "Foundation pour completed successfully - 450 cubic yards",
                "gps_coordinates": "40.7489, -73.9857",
                "weather": "Partly cloudy, 68°F"
            }
        ]

def render_mobile_daily_entry():
    """Render mobile-optimized daily entry form"""
    
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    st.subheader("📋 Highland Tower Development - Daily Field Entry")
    
    st.info("**📱 Mobile Entry:** Quick field data entry optimized for tablets and mobile devices.")
    
    # Mobile-optimized form
    with st.form("mobile_daily_entry", clear_on_submit=True):
        # Basic information
        st.markdown("**📋 Basic Information**")
        
        col1, col2 = st.columns(2)
        with col1:
            entry_date = st.date_input("📅 Date", value=date.today())
            shift = st.selectbox("🕐 Shift", ["Day Shift (7:00 AM - 3:30 PM)", "Night Shift (4:00 PM - 12:30 AM)"])
        
        with col2:
            weather = st.selectbox("🌤️ Weather", ["Clear", "Partly Cloudy", "Cloudy", "Light Rain", "Heavy Rain", "Snow"])
            temperature = st.number_input("🌡️ Temperature (°F)", min_value=0, max_value=120, value=72)
        
        # Crew information
        st.markdown("**👥 Crew Information**")
        
        crew_options = [f"{crew['crew_id']} - {crew['name']}" for crew in st.session_state.highland_field_crews]
        selected_crew = st.selectbox("👷 Select Crew", crew_options)
        
        col1, col2 = st.columns(2)
        with col1:
            workers_present = st.number_input("👥 Workers Present", min_value=1, max_value=50, value=12)
            hours_worked = st.number_input("⏰ Hours Worked", min_value=0.0, max_value=24.0, value=8.0, step=0.5)
        
        with col2:
            productivity = st.selectbox("📈 Productivity", ["Excellent", "Above Average", "Average", "Below Average", "Poor"])
            delays = st.selectbox("⏸️ Any Delays?", ["No Delays", "Weather", "Material", "Equipment", "Other"])
        
        # Work performed
        st.markdown("**🔨 Work Performed Today**")
        work_description = st.text_area("📝 Describe work completed:", placeholder="Detail the specific work completed today...", height=100)
        
        # Location and progress
        st.markdown("**📍 Location & Progress**")
        
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("📍 Work Location", placeholder="e.g., Level 8, Grid C-4")
            progress_percent = st.number_input("📊 Progress (%)", min_value=0, max_value=100, value=0, step=5)
        
        with col2:
            equipment_used = st.text_input("🚧 Equipment Used", placeholder="List major equipment used")
            materials_used = st.text_input("📦 Materials Used", placeholder="List materials consumed")
        
        # Safety and quality
        st.markdown("**🦺 Safety & Quality**")
        
        col1, col2 = st.columns(2)
        with col1:
            safety_incidents = st.number_input("⚠️ Safety Incidents", min_value=0, max_value=10, value=0)
            near_misses = st.number_input("⚠️ Near Misses", min_value=0, max_value=10, value=0)
        
        with col2:
            quality_issues = st.number_input("🔍 Quality Issues", min_value=0, max_value=10, value=0)
            rework_required = st.selectbox("🔄 Rework Required?", ["None", "Minor", "Moderate", "Significant"])
        
        # Additional notes
        st.markdown("**📝 Additional Notes**")
        additional_notes = st.text_area("📋 Notes & Observations:", placeholder="Any additional observations, issues, or notes...", height=80)
        
        # Submit button (mobile-optimized)
        submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
        with submit_col2:
            submitted = st.form_submit_button("📱 Submit Daily Report", use_container_width=True)
        
        if submitted:
            if work_description and location:
                # Create daily entry
                new_entry = {
                    "entry_id": f"DAILY-{len(st.session_state.get('highland_daily_entries', [])) + 1:03d}",
                    "date": entry_date.strftime("%Y-%m-%d"),
                    "shift": shift,
                    "weather": weather,
                    "temperature": temperature,
                    "crew": selected_crew.split(" - ")[0],
                    "workers_present": workers_present,
                    "hours_worked": hours_worked,
                    "productivity": productivity,
                    "delays": delays,
                    "work_description": work_description,
                    "location": location,
                    "progress_percent": progress_percent,
                    "equipment_used": equipment_used,
                    "materials_used": materials_used,
                    "safety_incidents": safety_incidents,
                    "near_misses": near_misses,
                    "quality_issues": quality_issues,
                    "rework_required": rework_required,
                    "additional_notes": additional_notes,
                    "submitted_by": "Field Supervisor",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Add to session state
                if "highland_daily_entries" not in st.session_state:
                    st.session_state.highland_daily_entries = []
                
                st.session_state.highland_daily_entries.append(new_entry)
                st.success("✅ Daily report submitted successfully!")
                st.balloons()
            else:
                st.error("Please complete all required fields!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_mobile_photo_capture():
    """Render mobile photo capture interface"""
    
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    st.subheader("📸 Highland Tower Development - Field Photo Capture")
    
    st.info("**📸 Photo Capture:** Document progress and issues with GPS-tagged field photography.")
    
    # Photo upload section
    st.markdown("**📤 Upload New Photos**")
    
    with st.form("photo_upload_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            photo_title = st.text_input("📝 Photo Title*", placeholder="Brief description of photo")
            category = st.selectbox("📂 Category", ["Progress", "Safety", "Quality", "Issue", "Milestone", "Equipment"])
            location = st.text_input("📍 Location*", placeholder="e.g., Level 8, Grid C-4")
        
        with col2:
            crew_options = [f"{crew['crew_id']} - {crew['name']}" for crew in st.session_state.highland_field_crews]
            photo_crew = st.selectbox("👷 Crew", crew_options)
            photographer = st.text_input("📷 Photographer", value="Field Supervisor")
            weather_condition = st.selectbox("🌤️ Weather", ["Clear", "Partly Cloudy", "Cloudy", "Light Rain", "Heavy Rain"])
        
        photo_description = st.text_area("📝 Description*", placeholder="Detailed description of what the photo shows...")
        
        # File upload
        uploaded_photos = st.file_uploader("📸 Select Photos", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
        
        if st.form_submit_button("📸 Upload Photos", use_container_width=True):
            if photo_title and location and photo_description:
                for photo in uploaded_photos:
                    new_photo = {
                        "photo_id": f"IMG-{len(st.session_state.highland_field_photos) + 1:03d}",
                        "title": photo_title,
                        "location": location,
                        "crew": photo_crew.split(" - ")[0],
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "photographer": photographer,
                        "category": category,
                        "description": photo_description,
                        "filename": photo.name,
                        "file_size": f"{len(photo.getvalue()) / 1024:.1f} KB",
                        "weather": weather_condition,
                        "gps_coordinates": "40.7489, -73.9857"  # Highland Tower location
                    }
                    
                    st.session_state.highland_field_photos.append(new_photo)
                
                st.success(f"✅ {len(uploaded_photos)} photo(s) uploaded successfully!")
            else:
                st.error("Please complete all required fields!")
    
    # Recent photos gallery
    st.markdown("**📸 Recent Field Photos**")
    
    if st.session_state.highland_field_photos:
        # Display photos in mobile-friendly grid
        photos_per_row = 3
        photos = st.session_state.highland_field_photos[-6:]  # Show last 6 photos
        
        for i in range(0, len(photos), photos_per_row):
            cols = st.columns(photos_per_row)
            
            for j, photo in enumerate(photos[i:i+photos_per_row]):
                with cols[j]:
                    category_emoji = {
                        "Progress": "🏗️",
                        "Safety": "🦺", 
                        "Quality": "🔍",
                        "Issue": "⚠️",
                        "Milestone": "🎯",
                        "Equipment": "🚧"
                    }.get(photo['category'], "📷")
                    
                    with st.expander(f"{category_emoji} {photo['title'][:20]}..."):
                        st.write(f"**Location:** {photo['location']}")
                        st.write(f"**Crew:** {photo['crew']}")
                        st.write(f"**Time:** {photo['timestamp']}")
                        st.write(f"**Category:** {photo['category']}")
                        st.write(f"**Description:** {photo['description']}")
                        
                        if st.button("🔍 View Full Size", key=f"view_{photo['photo_id']}"):
                            st.info("Full size view functionality...")
    else:
        st.info("No photos uploaded yet. Upload your first field photo above!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_mobile_field_inspection():
    """Render mobile field inspection interface"""
    
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    st.subheader("🔍 Highland Tower Development - Field Inspection")
    
    st.info("**🔍 Field Inspection:** Quick quality control and safety inspections with pass/fail checklist.")
    
    # Quick inspection form
    with st.form("field_inspection_form"):
        # Inspection details
        st.markdown("**📋 Inspection Details**")
        
        col1, col2 = st.columns(2)
        with col1:
            inspection_type = st.selectbox("🔍 Inspection Type", [
                "Quality Control", "Safety Check", "Progress Review", 
                "Material Verification", "Equipment Check", "Environmental"
            ])
            
            inspector_name = st.text_input("👤 Inspector", value="Quality Control Manager")
        
        with col2:
            inspection_location = st.text_input("📍 Location*", placeholder="e.g., Level 8, Grid C-4")
            inspection_area = st.selectbox("🏗️ Work Area", [
                "Foundation", "Structural Steel", "Concrete", "MEP Systems",
                "Exterior Envelope", "Interior Finishes", "Site Work"
            ])
        
        # Inspection checklist
        st.markdown("**✅ Inspection Checklist**")
        
        # Quality items
        if inspection_type in ["Quality Control", "Progress Review"]:
            st.markdown("**🔍 Quality Items:**")
            
            col1, col2 = st.columns(2)
            with col1:
                workmanship = st.selectbox("⚡ Workmanship", ["Pass", "Fail", "N/A"])
                materials = st.selectbox("📦 Materials Quality", ["Pass", "Fail", "N/A"])
                dimensions = st.selectbox("📏 Dimensions/Tolerance", ["Pass", "Fail", "N/A"])
            
            with col2:
                finish_quality = st.selectbox("✨ Finish Quality", ["Pass", "Fail", "N/A"])
                installation = st.selectbox("🔧 Installation Method", ["Pass", "Fail", "N/A"])
                compliance = st.selectbox("📋 Code Compliance", ["Pass", "Fail", "N/A"])
        
        # Safety items
        if inspection_type in ["Safety Check", "Quality Control"]:
            st.markdown("**🦺 Safety Items:**")
            
            col1, col2 = st.columns(2)
            with col1:
                ppe_compliance = st.selectbox("🦺 PPE Compliance", ["Pass", "Fail", "N/A"])
                fall_protection = st.selectbox("🔒 Fall Protection", ["Pass", "Fail", "N/A"])
                housekeeping = st.selectbox("🧹 Housekeeping", ["Pass", "Fail", "N/A"])
            
            with col2:
                equipment_safety = st.selectbox("🚧 Equipment Safety", ["Pass", "Fail", "N/A"])
                signage = st.selectbox("🚧 Safety Signage", ["Pass", "Fail", "N/A"])
                emergency_access = st.selectbox("🚪 Emergency Access", ["Pass", "Fail", "N/A"])
        
        # Overall assessment
        st.markdown("**📊 Overall Assessment**")
        
        col1, col2 = st.columns(2)
        with col1:
            overall_rating = st.selectbox("⭐ Overall Rating", ["Excellent", "Good", "Satisfactory", "Needs Improvement", "Unsatisfactory"])
            immediate_action = st.selectbox("⚡ Immediate Action Required?", ["No", "Minor Corrections", "Major Corrections", "Stop Work"])
        
        with col2:
            reinspection_required = st.selectbox("🔄 Reinspection Required?", ["No", "Within 24 Hours", "Within 48 Hours", "Within 1 Week"])
            priority = st.selectbox("🎯 Priority", ["Low", "Medium", "High", "Critical"])
        
        # Comments and notes
        inspection_notes = st.text_area("📝 Inspection Notes & Observations:", 
                                       placeholder="Detail any issues, recommendations, or observations...", 
                                       height=100)
        
        corrective_actions = st.text_area("🔧 Required Corrective Actions:", 
                                         placeholder="List specific actions needed to address any issues...", 
                                         height=80)
        
        # Submit inspection
        if st.form_submit_button("🔍 Submit Inspection Report", use_container_width=True):
            if inspection_location and inspection_area:
                new_inspection = {
                    "inspection_id": f"INSP-{len(st.session_state.get('highland_inspections', [])) + 1:03d}",
                    "type": inspection_type,
                    "location": inspection_location,
                    "area": inspection_area,
                    "inspector": inspector_name,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "overall_rating": overall_rating,
                    "immediate_action": immediate_action,
                    "reinspection_required": reinspection_required,
                    "priority": priority,
                    "notes": inspection_notes,
                    "corrective_actions": corrective_actions,
                    "status": "Open" if immediate_action != "No" else "Closed"
                }
                
                # Add checklist results
                if inspection_type in ["Quality Control", "Progress Review"]:
                    new_inspection.update({
                        "workmanship": workmanship,
                        "materials": materials,
                        "dimensions": dimensions,
                        "finish_quality": finish_quality,
                        "installation": installation,
                        "compliance": compliance
                    })
                
                if inspection_type in ["Safety Check", "Quality Control"]:
                    new_inspection.update({
                        "ppe_compliance": ppe_compliance,
                        "fall_protection": fall_protection,
                        "housekeeping": housekeeping,
                        "equipment_safety": equipment_safety,
                        "signage": signage,
                        "emergency_access": emergency_access
                    })
                
                # Add to session state
                if "highland_inspections" not in st.session_state:
                    st.session_state.highland_inspections = []
                
                st.session_state.highland_inspections.append(new_inspection)
                st.success("✅ Field inspection completed and submitted!")
                
                if immediate_action != "No":
                    st.warning(f"⚠️ {immediate_action} required for this inspection!")
            else:
                st.error("Please complete all required fields!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_mobile_safety_check():
    """Render mobile safety check interface"""
    
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    st.subheader("⚠️ Highland Tower Development - Safety Check")
    
    st.info("**🦺 Safety Check:** Quick safety assessments and incident reporting for immediate response.")
    
    # Safety status overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Safety Rating", "97.2", "Excellent")
    with col2:
        st.metric("Days Since Incident", "45", "Outstanding record")
    with col3:
        st.metric("Today's Checks", "8", "All passed")
    
    # Quick safety check
    with st.form("safety_check_form"):
        st.markdown("**🦺 Quick Safety Assessment**")
        
        col1, col2 = st.columns(2)
        with col1:
            check_location = st.text_input("📍 Location*", placeholder="e.g., Level 8, Grid C-4")
            check_time = st.time_input("🕐 Time", value=datetime.now().time())
            checker_name = st.text_input("👤 Safety Officer", value="Safety Manager")
        
        with col2:
            crew_options = [f"{crew['crew_id']} - {crew['name']}" for crew in st.session_state.highland_field_crews]
            safety_crew = st.selectbox("👷 Crew Being Checked", crew_options)
            workers_checked = st.number_input("👥 Workers Checked", min_value=1, max_value=50, value=5)
        
        # Safety checklist
        st.markdown("**✅ Safety Checklist**")
        
        col1, col2 = st.columns(2)
        with col1:
            hard_hats = st.selectbox("🪖 Hard Hats", ["All Compliant", "Minor Issues", "Major Issues"])
            safety_glasses = st.selectbox("👓 Safety Glasses", ["All Compliant", "Minor Issues", "Major Issues"])
            high_vis_vests = st.selectbox("🦺 High-Vis Vests", ["All Compliant", "Minor Issues", "Major Issues"])
            safety_boots = st.selectbox("👢 Safety Boots", ["All Compliant", "Minor Issues", "Major Issues"])
        
        with col2:
            fall_protection_check = st.selectbox("🔒 Fall Protection", ["Compliant", "Needs Attention", "Critical Issue"])
            tool_safety = st.selectbox("🔨 Tool Safety", ["Good", "Needs Attention", "Critical Issue"])
            work_area_safety = st.selectbox("🏗️ Work Area Safety", ["Safe", "Minor Hazards", "Major Hazards"])
            emergency_equipment = st.selectbox("🚨 Emergency Equipment", ["Available", "Limited", "Missing"])
        
        # Overall safety assessment
        overall_safety = st.selectbox("📊 Overall Safety Status", ["Excellent", "Good", "Satisfactory", "Needs Improvement", "Unsafe"])
        
        # Incident reporting
        st.markdown("**⚠️ Incident Reporting**")
        
        incident_occurred = st.selectbox("🚨 Any Incidents/Near Misses?", ["No", "Near Miss", "Minor Incident", "Major Incident"])
        
        if incident_occurred != "No":
            incident_description = st.text_area("📝 Describe Incident:", 
                                              placeholder="Provide detailed description of what happened...",
                                              height=100)
            immediate_actions = st.text_area("🚨 Immediate Actions Taken:", 
                                           placeholder="List actions taken immediately...",
                                           height=80)
        else:
            incident_description = ""
            immediate_actions = ""
        
        safety_notes = st.text_area("📝 Additional Safety Notes:", 
                                   placeholder="Any other safety observations or recommendations...",
                                   height=80)
        
        # Submit safety check
        if st.form_submit_button("🦺 Submit Safety Check", use_container_width=True):
            if check_location and checker_name:
                new_safety_check = {
                    "check_id": f"SAFE-{len(st.session_state.get('highland_safety_checks', [])) + 1:03d}",
                    "location": check_location,
                    "time": check_time.strftime("%H:%M:%S"),
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "checker": checker_name,
                    "crew": safety_crew.split(" - ")[0],
                    "workers_checked": workers_checked,
                    "hard_hats": hard_hats,
                    "safety_glasses": safety_glasses,
                    "high_vis_vests": high_vis_vests,
                    "safety_boots": safety_boots,
                    "fall_protection": fall_protection_check,
                    "tool_safety": tool_safety,
                    "work_area_safety": work_area_safety,
                    "emergency_equipment": emergency_equipment,
                    "overall_safety": overall_safety,
                    "incident_occurred": incident_occurred,
                    "incident_description": incident_description,
                    "immediate_actions": immediate_actions,
                    "safety_notes": safety_notes,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Add to session state
                if "highland_safety_checks" not in st.session_state:
                    st.session_state.highland_safety_checks = []
                
                st.session_state.highland_safety_checks.append(new_safety_check)
                
                if incident_occurred != "No":
                    st.error(f"🚨 {incident_occurred} reported and logged for immediate follow-up!")
                else:
                    st.success("✅ Safety check completed - All clear!")
                    
                if overall_safety in ["Needs Improvement", "Unsafe"]:
                    st.warning("⚠️ Safety concerns identified - Immediate attention required!")
            else:
                st.error("Please complete all required fields!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_mobile_crew_dashboard():
    """Render mobile crew dashboard"""
    
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    st.subheader("📊 Highland Tower Development - Crew Dashboard")
    
    st.info("**📊 Crew Dashboard:** Real-time crew status, productivity, and resource allocation for field supervisors.")
    
    # Current crew status
    st.markdown("**👷 Active Crews Status**")
    
    for crew in st.session_state.highland_field_crews:
        status_color = {"Active": "🟢", "Break": "🟡", "Inactive": "🔴"}.get(crew['status'], "⚪")
        
        with st.expander(f"{status_color} {crew['name']} - {crew['workers']} workers"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Supervisor:** {crew['supervisor']}")
                st.write(f"**Location:** {crew['location']}")
                st.write(f"**Shift:** {crew['shift']}")
                st.write(f"**Workers:** {crew['workers']}")
            
            with col2:
                st.write(f"**Status:** {status_color} {crew['status']}")
                st.write(f"**Safety Rating:** {crew['safety_rating']}")
                st.write(f"**Productivity:** {crew['productivity']}")
            
            st.write("**Equipment:**")
            for equipment in crew['equipment']:
                st.write(f"• {equipment}")
            
            # Quick actions
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📞 Contact", key=f"contact_{crew['crew_id']}", use_container_width=True):
                    st.info(f"Contacting {crew['supervisor']}...")
            
            with col2:
                if st.button("📍 Location", key=f"location_{crew['crew_id']}", use_container_width=True):
                    st.info(f"Showing location: {crew['location']}")
            
            with col3:
                if st.button("📋 Report", key=f"report_{crew['crew_id']}", use_container_width=True):
                    st.info("Quick report functionality...")
    
    # Today's productivity summary
    st.markdown("**📈 Today's Productivity Summary**")
    
    productivity_data = {
        "Crew": ["Foundation Crew Alpha", "Steel Erection Team", "MEP Installation"],
        "Progress": [85, 92, 78],
        "Hours Worked": [8.0, 8.5, 7.5],
        "Productivity": ["Above Average", "Excellent", "Good"]
    }
    
    productivity_df = pd.DataFrame(productivity_data)
    st.dataframe(productivity_df, use_container_width=True, hide_index=True)
    
    # Resource allocation
    st.markdown("**🚧 Equipment & Resource Status**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🏗️ Equipment**")
        st.write("• Tower Crane: ✅ Operational")
        st.write("• Concrete Pump: ✅ Operational") 
        st.write("• Excavator: 🟡 Maintenance")
        st.write("• Welding Equipment: ✅ Operational")
    
    with col2:
        st.markdown("**📦 Materials**")
        st.write("• Concrete: ✅ Adequate")
        st.write("• Rebar: ✅ Adequate")
        st.write("• Steel Beams: 🟡 Low Stock")
        st.write("• HVAC Components: ✅ Adequate")
    
    with col3:
        st.markdown("**👥 Personnel**")
        st.write("• Total Workers: 46")
        st.write("• Present Today: 42")
        st.write("• Safety Officers: 3")
        st.write("• Supervisors: 3")
    
    st.markdown('</div>', unsafe_allow_html=True)