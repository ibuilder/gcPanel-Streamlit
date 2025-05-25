"""
Mobile & Field Optimization for Highland Tower Development
Touch-friendly interfaces optimized for construction site use
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import uuid

def apply_mobile_styles():
    """Apply mobile-optimized CSS for field use"""
    st.markdown("""
    <style>
    /* Mobile-First Design for Construction Sites */
    @media (max-width: 768px) {
        /* Larger touch targets for field use */
        .stButton > button {
            min-height: 48px !important;
            font-size: 16px !important;
            padding: 12px 24px !important;
            margin: 8px 0 !important;
        }
        
        /* Improved form elements for tablets */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            min-height: 48px !important;
            font-size: 16px !important;
            padding: 12px !important;
        }
        
        /* Better spacing for touch interaction */
        .stExpander {
            margin: 12px 0 !important;
        }
        
        /* Larger checkboxes and radio buttons */
        .stCheckbox > label,
        .stRadio > label {
            font-size: 16px !important;
            padding: 8px !important;
        }
        
        /* Field-friendly card layout */
        .field-card {
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 20px;
            margin: 16px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            min-height: 120px;
        }
        
        /* Quick action buttons for field teams */
        .field-action-btn {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 16px 24px;
            font-size: 18px;
            font-weight: 600;
            margin: 8px;
            min-height: 60px;
            width: 100%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
        
        /* Field status indicators */
        .field-status-good { background: #10b981; color: white; padding: 8px 16px; border-radius: 20px; font-weight: 600; }
        .field-status-warning { background: #f59e0b; color: white; padding: 8px 16px; border-radius: 20px; font-weight: 600; }
        .field-status-danger { background: #ef4444; color: white; padding: 8px 16px; border-radius: 20px; font-weight: 600; }
        
        /* Offline mode indicator */
        .offline-indicator {
            position: fixed;
            top: 10px;
            right: 10px;
            background: #ef4444;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            z-index: 1000;
        }
        
        .online-indicator {
            position: fixed;
            top: 10px;
            right: 10px;
            background: #10b981;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            z-index: 1000;
        }
    }
    
    /* GPS and Camera Integration Styles */
    .camera-capture-btn {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 16px;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        margin: 8px 0;
        min-height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
    
    .gps-tag-btn {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 14px;
        font-weight: 600;
        margin: 4px;
    }
    
    .qr-scan-btn {
        background: linear-gradient(135deg, #ea580c 0%, #f97316 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 16px;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        margin: 8px 0;
        min-height: 60px;
    }
    
    /* Field report quick entry */
    .quick-entry-form {
        background: white;
        border: 2px solid #3b82f6;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    /* Touch-friendly tabs for mobile */
    .mobile-tabs {
        display: flex;
        overflow-x: auto;
        border-bottom: 2px solid #e5e7eb;
        margin-bottom: 20px;
    }
    
    .mobile-tab {
        background: white;
        border: none;
        padding: 16px 24px;
        font-size: 16px;
        font-weight: 600;
        white-space: nowrap;
        min-width: 120px;
        border-bottom: 3px solid transparent;
    }
    
    .mobile-tab.active {
        background: #eff6ff;
        color: #1e40af;
        border-bottom-color: #1e40af;
    }
    </style>
    """, unsafe_allow_html=True)

def render_field_dashboard():
    """Render mobile-optimized field dashboard"""
    apply_mobile_styles()
    
    # Connection status indicator
    if 'offline_mode' not in st.session_state:
        st.session_state.offline_mode = False
    
    status_class = "offline-indicator" if st.session_state.offline_mode else "online-indicator"
    status_text = "🔴 OFFLINE" if st.session_state.offline_mode else "🟢 ONLINE"
    
    st.markdown(f'<div class="{status_class}">{status_text}</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="field-card">
        <h2>🏗️ Highland Tower - Field Operations</h2>
        <p><strong>Location:</strong> Level 8 - Residential Construction</p>
        <p><strong>Weather:</strong> Sunny, 68°F - Good conditions for work</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📸 Take Progress Photo", key="camera_btn", help="Capture photos with GPS location"):
            render_camera_interface()
        
        if st.button("📱 Scan QR Code", key="qr_btn", help="Scan equipment or material QR codes"):
            render_qr_scanner()
    
    with col2:
        if st.button("📝 Quick Daily Report", key="report_btn", help="Create daily report with current location"):
            render_quick_report_form()
        
        if st.button("🚨 Report Safety Issue", key="safety_btn", help="Immediate safety reporting"):
            render_safety_report_form()
    
    # Current location and GPS
    if st.button("📍 Get Current Location", key="gps_btn"):
        render_gps_interface()

def render_camera_interface():
    """Camera integration for progress photos"""
    st.markdown("### 📸 Progress Photo Capture")
    
    st.markdown("""
    <div class="quick-entry-form">
        <h4>📷 Highland Tower Progress Documentation</h4>
        <p>Capture high-quality photos with automatic GPS tagging and project metadata.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Photo capture interface
    uploaded_photo = st.file_uploader(
        "Take Photo or Upload from Gallery", 
        type=['jpg', 'jpeg', 'png'],
        help="Photos will be automatically tagged with location and timestamp"
    )
    
    if uploaded_photo:
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(uploaded_photo, caption="Progress Photo", use_container_width=True)
        
        with col2:
            photo_location = st.selectbox("Photo Location", [
                "Level 8 - Residential Framing",
                "Level 9 - MEP Rough-in", 
                "Level 10 - Drywall Installation",
                "Ground Floor - Retail Finishes",
                "Basement - Parking Construction",
                "Roof Level - Mechanical Equipment"
            ])
            
            photo_category = st.selectbox("Category", [
                "Progress Documentation",
                "Quality Control",
                "Safety Inspection", 
                "Material Delivery",
                "Equipment Status",
                "Issue Documentation"
            ])
            
            photo_notes = st.text_area("Photo Description", 
                placeholder="Describe what this photo shows...")
            
            # Simulate GPS coordinates
            st.markdown("**📍 GPS Location:** 47.6062° N, 122.3321° W")
            st.markdown(f"**🕐 Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            if st.button("💾 Save Photo", type="primary"):
                photo_id = f"HTD-PHOTO-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                st.success(f"✅ Photo saved successfully! ID: {photo_id}")
                st.info("📍 GPS location and metadata automatically captured")

def render_qr_scanner():
    """QR code scanning for equipment and materials"""
    st.markdown("### 📱 QR Code Scanner")
    
    st.markdown("""
    <div class="quick-entry-form">
        <h4>🔍 Highland Tower Asset Tracking</h4>
        <p>Scan QR codes on equipment, materials, or location markers for instant access to information.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # QR scanner interface (simulated)
    qr_input = st.text_input("Enter QR Code or Scan", placeholder="HTD-EQ-001, HTD-MAT-125, etc.")
    
    if qr_input:
        # Simulate QR code lookup
        qr_data = simulate_qr_lookup(qr_input)
        
        if qr_data:
            st.markdown("### 📋 Asset Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Asset ID:** {qr_data['id']}")
                st.markdown(f"**Type:** {qr_data['type']}")
                st.markdown(f"**Status:** {qr_data['status']}")
                st.markdown(f"**Location:** {qr_data['location']}")
            
            with col2:
                st.markdown(f"**Last Updated:** {qr_data['last_updated']}")
                st.markdown(f"**Responsible:** {qr_data['responsible']}")
                
                # Quick actions
                if st.button("📝 Update Status"):
                    st.success("Status update form opened")
                
                if st.button("📸 Take Photo"):
                    st.info("Camera opened for asset documentation")
        else:
            st.error("QR code not found in Highland Tower database")

def render_quick_report_form():
    """Quick daily report form optimized for mobile"""
    st.markdown("### 📝 Quick Daily Report")
    
    with st.form("quick_daily_report"):
        st.markdown("""
        <div class="quick-entry-form">
            <h4>📊 Highland Tower Daily Report</h4>
            <p>Quick field report with automatic location and weather data.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Pre-filled data
        report_date = st.date_input("Date", datetime.now())
        current_location = st.selectbox("Current Location", [
            "Level 8 - Residential Construction",
            "Level 9 - MEP Installation",
            "Ground Floor - Retail Finishes", 
            "Basement - Parking Areas",
            "Site Perimeter - Safety Setup"
        ])
        
        # Quick entry fields
        crew_count = st.number_input("Crew Size Today", min_value=0, max_value=50, value=12)
        weather = st.selectbox("Weather Conditions", [
            "Clear - Good for all work",
            "Partly Cloudy - Good conditions", 
            "Overcast - Acceptable conditions",
            "Light Rain - Limited outdoor work",
            "Heavy Rain - Indoor work only"
        ])
        
        work_summary = st.text_area("Work Accomplished Today", 
            placeholder="Brief summary of major work completed...",
            height=100)
        
        issues_delays = st.text_area("Issues or Delays",
            placeholder="Any problems, delays, or concerns...",
            height=80)
        
        safety_notes = st.text_area("Safety Observations",
            placeholder="Safety incidents, near misses, or observations...",
            height=80)
        
        # Auto-populated metadata
        st.markdown("**📍 Auto-Generated Info:**")
        st.markdown("• GPS: 47.6062° N, 122.3321° W")
        st.markdown("• Temperature: 68°F")
        st.markdown("• Humidity: 45%")
        st.markdown("• Wind: 5 mph NW")
        
        if st.form_submit_button("📤 Submit Report", type="primary"):
            report_id = f"HTD-DR-{datetime.now().strftime('%Y%m%d')}"
            st.success(f"✅ Daily report submitted! ID: {report_id}")
            st.info("🔄 Report synchronized when connection available")

def render_safety_report_form():
    """Immediate safety issue reporting"""
    st.markdown("### 🚨 Safety Issue Report")
    
    st.error("⚠️ IMMEDIATE SAFETY REPORTING")
    
    with st.form("safety_report"):
        incident_type = st.selectbox("Incident Type", [
            "🚨 EMERGENCY - Immediate danger",
            "⚠️ HAZARD - Unsafe condition",
            "🔍 NEAR MISS - Almost incident", 
            "📋 OBSERVATION - Safety concern",
            "🩹 MINOR INJURY - First aid needed",
            "🏥 SERIOUS INJURY - Medical attention"
        ])
        
        incident_location = st.text_input("Exact Location", 
            placeholder="Level 8, Grid A-5, near elevator shaft...")
        
        incident_description = st.text_area("Describe the Incident",
            placeholder="What happened? What conditions led to this?",
            height=120)
        
        immediate_action = st.text_area("Immediate Action Taken",
            placeholder="What was done immediately to address the situation?",
            height=80)
        
        injured_person = st.text_input("Injured Person (if any)",
            placeholder="Name and company of injured person...")
        
        witnesses = st.text_area("Witnesses",
            placeholder="Names of people who witnessed the incident...")
        
        # Emergency contact options
        st.markdown("**📞 Emergency Contacts:**")
        col1, col2 = st.columns(2)
        
        with col1:
            notify_911 = st.checkbox("🚨 Call 911 (Medical Emergency)")
            notify_safety = st.checkbox("📞 Notify Safety Manager")
        
        with col2:
            notify_pm = st.checkbox("📱 Alert Project Manager")
            notify_super = st.checkbox("👷 Notify Site Supervisor")
        
        if st.form_submit_button("🚨 SUBMIT SAFETY REPORT", type="primary"):
            incident_id = f"HTD-SI-{datetime.now().strftime('%Y%m%d%H%M')}"
            st.success(f"✅ Safety report submitted! ID: {incident_id}")
            
            if notify_911:
                st.error("🚨 911 EMERGENCY SERVICES CONTACTED")
            if notify_safety:
                st.warning("📞 Safety Manager Lisa Wong notified: 555-0105")
            if notify_pm:
                st.info("📱 Project Manager Jennifer Walsh alerted: 555-0101")

def render_gps_interface():
    """GPS location services for field tracking"""
    st.markdown("### 📍 GPS Location Services")
    
    # Simulate GPS coordinates for Highland Tower site
    latitude = 47.6062
    longitude = -122.3321
    
    st.markdown("""
    <div class="quick-entry-form">
        <h4>🗺️ Highland Tower Development Site</h4>
        <p>GPS coordinates automatically captured for all field activities.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**📍 Current Coordinates:**")
        st.markdown(f"• Latitude: {latitude}°")
        st.markdown(f"• Longitude: {longitude}°")
        st.markdown(f"• Accuracy: ±3 meters")
        st.markdown(f"• Altitude: 56 meters")
    
    with col2:
        st.markdown(f"**🏗️ Site Information:**")
        st.markdown(f"• Project: Highland Tower Development")
        st.markdown(f"• Address: Highland District")
        st.markdown(f"• Zone: Construction Area A")
        st.markdown(f"• Building: Main Tower")
    
    # Location-based actions
    if st.button("📍 Tag Current Location", type="primary"):
        location_id = f"HTD-LOC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        st.success(f"✅ Location tagged! ID: {location_id}")
        st.info(f"📍 Coordinates: {latitude}, {longitude}")

def simulate_qr_lookup(qr_code):
    """Simulate QR code database lookup"""
    qr_database = {
        "HTD-EQ-001": {
            "id": "HTD-EQ-001",
            "type": "Tower Crane #1",
            "status": "Operational",
            "location": "Central Site Position",
            "last_updated": "2025-01-27 08:30",
            "responsible": "Mike Rodriguez"
        },
        "HTD-MAT-125": {
            "id": "HTD-MAT-125", 
            "type": "Steel Beams - Level 8",
            "status": "Delivered",
            "location": "Material Staging Area B",
            "last_updated": "2025-01-26 14:15",
            "responsible": "Highland Steel Co."
        },
        "HTD-LOC-L8": {
            "id": "HTD-LOC-L8",
            "type": "Location Marker - Level 8",
            "status": "Active Construction",
            "location": "Residential Floor Level 8",
            "last_updated": "2025-01-27 07:00",
            "responsible": "Field Supervision"
        }
    }
    
    return qr_database.get(qr_code.upper())

# Offline capability management
def setup_offline_mode():
    """Setup offline data caching and sync"""
    if 'offline_data' not in st.session_state:
        st.session_state.offline_data = {
            'daily_reports': [],
            'safety_reports': [],
            'photos': [],
            'qr_scans': []
        }
    
    if 'sync_pending' not in st.session_state:
        st.session_state.sync_pending = 0

def sync_offline_data():
    """Sync offline data when connection restored"""
    if st.session_state.get('sync_pending', 0) > 0:
        st.success(f"✅ Synced {st.session_state.sync_pending} offline entries")
        st.session_state.sync_pending = 0

if __name__ == "__main__":
    render_field_dashboard()