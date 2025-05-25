"""
Progress Photos Module - Highland Tower Development
Advanced photo management with GPS tagging, categorization, and workflow integration
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import io
from PIL import Image
import base64

def render():
    """Render the comprehensive progress photos module"""
    st.title("📸 Progress Photos - Highland Tower Development")
    st.markdown("**Professional photo documentation with GPS tagging and workflow integration**")
    
    # Photo management overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Photos", "2,847", "+23 today")
    with col2:
        st.metric("This Week", "156", "+12% vs last week")
    with col3:
        st.metric("Storage Used", "18.7 GB", "82% of 25GB limit")
    with col4:
        st.metric("Avg Daily Upload", "28 photos", "Consistent tracking")
    
    # Main tabs for photo management
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📤 Upload Photos", "📋 Photo Gallery", "🗂️ Categories", "📍 GPS Mapping", "📊 Analytics", "⚙️ Settings"
    ])
    
    with tab1:
        render_photo_upload()
    
    with tab2:
        render_photo_gallery()
    
    with tab3:
        render_photo_categories()
    
    with tab4:
        render_gps_mapping()
    
    with tab5:
        render_photo_analytics()
    
    with tab6:
        render_photo_settings()

def render_photo_upload():
    """Enhanced photo upload with metadata capture"""
    st.subheader("📤 Upload Progress Photos")
    
    # Upload form
    with st.form("photo_upload_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_files = st.file_uploader(
                "Choose photos to upload",
                accept_multiple_files=True,
                type=['png', 'jpg', 'jpeg'],
                help="Select multiple photos for batch upload"
            )
            
            description = st.text_area(
                "Photo Description",
                placeholder="Describe what these photos show (e.g., Level 13 steel erection progress)"
            )
            
            category = st.selectbox(
                "Photo Category",
                [
                    "Structural Progress",
                    "MEP Installation", 
                    "Safety Inspections",
                    "Quality Control",
                    "Material Deliveries",
                    "Equipment Operations",
                    "Weather Conditions",
                    "Before/After",
                    "Milestone Documentation",
                    "Issue Documentation"
                ]
            )
        
        with col2:
            # Location details
            st.markdown("**📍 Location Details**")
            building_level = st.selectbox(
                "Building Level",
                ["Basement 2", "Basement 1", "Ground Floor"] + 
                [f"Level {i}" for i in range(1, 16)] + 
                ["Roof Level", "Exterior", "Site Area"]
            )
            
            zone = st.selectbox(
                "Zone/Area",
                ["Zone A (East)", "Zone B (West)", "Zone C (North)", "Zone D (South)", 
                 "Central Core", "Mechanical Room", "Stairwell", "Elevator Shaft", "Exterior"]
            )
            
            weather = st.selectbox(
                "Weather Conditions",
                ["Sunny", "Partly Cloudy", "Overcast", "Light Rain", "Heavy Rain", "Snow", "Windy"]
            )
            
            temperature = st.number_input("Temperature (°F)", value=72, min_value=-10, max_value=110)
            
            # Photo tags
            st.markdown("**🏷️ Tags**")
            tags = st.multiselect(
                "Select applicable tags",
                ["Critical Path", "Safety Issue", "Quality Concern", "Milestone", 
                 "Rework Required", "Approved Work", "Inspection Ready", "Client Review"]
            )
            
            # Priority level
            priority = st.radio(
                "Priority Level",
                ["Standard", "Important", "Critical"],
                help="Critical photos will be flagged for immediate review"
            )
        
        # Submit button
        submitted = st.form_submit_button("📤 Upload Photos", type="primary")
        
        if submitted and uploaded_files:
            # Process uploaded photos
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, uploaded_file in enumerate(uploaded_files):
                # Simulate photo processing
                progress = (i + 1) / len(uploaded_files)
                progress_bar.progress(progress)
                status_text.text(f"Processing {uploaded_file.name}...")
                
                # Here you would normally save to database/storage
                # For demo, we'll show success message
                
            st.success(f"✅ Successfully uploaded {len(uploaded_files)} photos!")
            st.info("📧 Notification sent to project team about new photos.")
            
            # Show upload summary
            with st.expander("Upload Summary"):
                st.write(f"**Photos:** {len(uploaded_files)} files")
                st.write(f"**Category:** {category}")
                st.write(f"**Location:** {building_level}, {zone}")
                st.write(f"**Weather:** {weather}, {temperature}°F")
                if tags:
                    st.write(f"**Tags:** {', '.join(tags)}")
                st.write(f"**Priority:** {priority}")

def render_photo_gallery():
    """Interactive photo gallery with filtering and search"""
    st.subheader("📋 Highland Tower Development Photo Gallery")
    
    # Search and filter controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        search_query = st.text_input("🔍 Search photos", placeholder="Enter keywords...")
    with col2:
        date_filter = st.selectbox("📅 Date Range", 
            ["Today", "This Week", "This Month", "Last 30 Days", "All Time"])
    with col3:
        category_filter = st.selectbox("🗂️ Category", 
            ["All Categories", "Structural Progress", "MEP Installation", "Safety Inspections", "Quality Control"])
    with col4:
        level_filter = st.selectbox("🏢 Level", 
            ["All Levels"] + [f"Level {i}" for i in range(1, 16)])
    
    # Sample photo data
    photos_data = [
        {
            "id": "HTD-2025-1247",
            "filename": "Level_13_Steel_Progress_052525.jpg",
            "description": "Level 13 steel beam installation - 85% complete",
            "category": "Structural Progress",
            "location": "Level 13, Zone A",
            "date": "2025-05-25",
            "time": "14:30",
            "photographer": "John Smith",
            "weather": "Sunny, 72°F",
            "tags": ["Critical Path", "Milestone"],
            "priority": "Important",
            "size": "4.2 MB",
            "approved": True
        },
        {
            "id": "HTD-2025-1246", 
            "filename": "MEP_Rough_In_Zone_C.jpg",
            "description": "Electrical rough-in installation in Zone C",
            "category": "MEP Installation",
            "location": "Level 11, Zone C",
            "date": "2025-05-25",
            "time": "11:15",
            "photographer": "Sarah Chen",
            "weather": "Partly Cloudy, 68°F",
            "tags": ["Inspection Ready"],
            "priority": "Standard",
            "size": "3.8 MB",
            "approved": True
        },
        {
            "id": "HTD-2025-1245",
            "filename": "Concrete_Pour_Quality_Check.jpg", 
            "description": "Quality control inspection of Level 12 concrete pour",
            "category": "Quality Control",
            "location": "Level 12, Central Core",
            "date": "2025-05-24",
            "time": "16:45",
            "photographer": "Mike Torres",
            "weather": "Overcast, 65°F",
            "tags": ["Quality Concern", "Approved Work"],
            "priority": "Important",
            "size": "5.1 MB",
            "approved": True
        },
        {
            "id": "HTD-2025-1244",
            "filename": "Safety_Inspection_Scaffolding.jpg",
            "description": "Weekly safety inspection of scaffolding systems",
            "category": "Safety Inspections", 
            "location": "Level 10, Exterior",
            "date": "2025-05-24",
            "time": "09:00",
            "photographer": "Jennifer Walsh",
            "weather": "Sunny, 70°F",
            "tags": ["Safety Issue", "Critical Path"],
            "priority": "Critical",
            "size": "3.4 MB",
            "approved": False
        }
    ]
    
    # Convert to DataFrame for filtering
    df = pd.DataFrame(photos_data)
    
    # Display photos in grid layout
    st.markdown("### Recent Photos")
    
    for i in range(0, len(photos_data), 2):
        col1, col2 = st.columns(2)
        
        # First photo
        with col1:
            if i < len(photos_data):
                photo = photos_data[i]
                render_photo_card(photo)
        
        # Second photo  
        with col2:
            if i + 1 < len(photos_data):
                photo = photos_data[i + 1]
                render_photo_card(photo)
    
    # Photo statistics
    st.markdown("---")
    st.subheader("📊 Photo Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Photos by category
        category_counts = df['category'].value_counts()
        fig = px.pie(values=category_counts.values, names=category_counts.index, 
                    title="Photos by Category")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Photos by priority
        priority_counts = df['priority'].value_counts()
        fig = px.bar(x=priority_counts.index, y=priority_counts.values,
                    title="Photos by Priority Level")
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        # Approval status
        approval_status = df['approved'].value_counts()
        labels = ['Approved', 'Pending Review'] if True in approval_status.index else ['Pending Review']
        fig = px.pie(values=approval_status.values, names=labels,
                    title="Approval Status")
        st.plotly_chart(fig, use_container_width=True)

def render_photo_card(photo):
    """Render individual photo card"""
    # Priority color coding
    priority_colors = {
        "Standard": "#28a745",
        "Important": "#ffc107", 
        "Critical": "#dc3545"
    }
    
    priority_color = priority_colors.get(photo['priority'], "#6c757d")
    
    # Status icon
    status_icon = "✅" if photo['approved'] else "⏳"
    
    st.markdown(f"""
    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 12px; margin-bottom: 16px; 
                border-left: 4px solid {priority_color};">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <h4 style="margin: 0; font-size: 14px;">{photo['id']}</h4>
            <span style="font-size: 18px;">{status_icon}</span>
        </div>
        
        <div style="background-color: #f8f9fa; height: 200px; border-radius: 4px; 
                    display: flex; align-items: center; justify-content: center; margin-bottom: 8px;">
            <span style="color: #6c757d;">📸 {photo['filename']}</span>
        </div>
        
        <div style="font-weight: 500; margin-bottom: 4px;">{photo['description']}</div>
        
        <div style="font-size: 12px; color: #6c757d; margin-bottom: 4px;">
            <strong>📍 Location:</strong> {photo['location']}<br>
            <strong>📅 Date:</strong> {photo['date']} at {photo['time']}<br>
            <strong>👤 Photographer:</strong> {photo['photographer']}<br>
            <strong>🌤️ Weather:</strong> {photo['weather']}
        </div>
        
        <div style="margin-bottom: 8px;">
            <strong>🗂️ Category:</strong> <span style="background-color: #e9ecef; padding: 2px 6px; 
                                                  border-radius: 3px; font-size: 11px;">{photo['category']}</span>
        </div>
        
        <div style="margin-bottom: 8px;">
            <strong>🏷️ Tags:</strong> {', '.join([f'<span style="background-color: #d1ecf1; padding: 1px 4px; border-radius: 2px; font-size: 10px;">{tag}</span>' for tag in photo['tags']])}
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 11px; color: #6c757d;">Size: {photo['size']}</span>
            <span style="background-color: {priority_color}; color: white; padding: 2px 6px; 
                         border-radius: 3px; font-size: 10px;">{photo['priority']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👁️ View", key=f"view_{photo['id']}"):
            st.info(f"Opening {photo['filename']}")
    with col2:
        if st.button("📝 Edit", key=f"edit_{photo['id']}"):
            st.info(f"Editing metadata for {photo['id']}")
    with col3:
        if st.button("📤 Share", key=f"share_{photo['id']}"):
            st.success(f"Sharing {photo['id']} with project team")

def render_photo_categories():
    """Photo category management"""
    st.subheader("🗂️ Photo Categories & Organization")
    
    # Category overview
    categories_data = pd.DataFrame([
        {"Category": "Structural Progress", "Photos": 847, "Last Updated": "2 hours ago", "Auto-Tag": True},
        {"Category": "MEP Installation", "Photos": 523, "Last Updated": "4 hours ago", "Auto-Tag": True},
        {"Category": "Safety Inspections", "Photos": 312, "Last Updated": "1 day ago", "Auto-Tag": False},
        {"Category": "Quality Control", "Photos": 298, "Last Updated": "6 hours ago", "Auto-Tag": True},
        {"Category": "Material Deliveries", "Photos": 267, "Last Updated": "3 hours ago", "Auto-Tag": False},
        {"Category": "Equipment Operations", "Photos": 189, "Last Updated": "2 days ago", "Auto-Tag": False},
        {"Category": "Weather Conditions", "Photos": 156, "Last Updated": "1 hour ago", "Auto-Tag": True},
        {"Category": "Before/After", "Photos": 134, "Last Updated": "1 day ago", "Auto-Tag": False},
        {"Category": "Milestone Documentation", "Photos": 89, "Last Updated": "3 days ago", "Auto-Tag": False},
        {"Category": "Issue Documentation", "Photos": 32, "Last Updated": "5 hours ago", "Auto-Tag": True}
    ])
    
    st.dataframe(categories_data, use_container_width=True)
    
    # Category management tools
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Create New Category")
        with st.form("new_category_form"):
            new_category = st.text_input("Category Name")
            description = st.text_area("Description")
            auto_tag = st.checkbox("Enable Auto-Tagging")
            color = st.color_picker("Category Color", "#3498db")
            
            if st.form_submit_button("Create Category"):
                st.success(f"✅ Created category: {new_category}")
    
    with col2:
        st.subheader("⚙️ Category Settings")
        selected_category = st.selectbox("Select Category", categories_data['Category'].tolist())
        
        if selected_category:
            st.info(f"Managing settings for: **{selected_category}**")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🏷️ Bulk Re-tag"):
                    st.success("Re-tagging all photos in category...")
            with col_b:
                if st.button("📊 View Analytics"):
                    st.info("Opening category analytics...")

def render_gps_mapping():
    """GPS mapping and location tracking"""
    st.subheader("📍 GPS Mapping & Location Tracking")
    
    st.info("🗺️ **Interactive Site Map** - Photos are automatically geo-tagged with precise coordinates")
    
    # Mock coordinates for Highland Tower Development site
    site_center = {"lat": 47.6205, "lon": -122.3493}  # Seattle coordinates
    
    # Sample photo locations
    photo_locations = pd.DataFrame([
        {"lat": 47.6205, "lon": -122.3493, "photo_count": 45, "location": "Main Entrance", "recent_photo": "2 hours ago"},
        {"lat": 47.6207, "lon": -122.3495, "photo_count": 32, "location": "East Wing Construction", "recent_photo": "4 hours ago"},
        {"lat": 47.6203, "lon": -122.3491, "photo_count": 28, "location": "West Wing Foundation", "recent_photo": "6 hours ago"},
        {"lat": 47.6209, "lon": -122.3497, "photo_count": 19, "location": "Material Storage", "recent_photo": "1 day ago"},
        {"lat": 47.6201, "lon": -122.3489, "photo_count": 15, "location": "Equipment Staging", "recent_photo": "2 days ago"}
    ])
    
    # Map visualization using Plotly
    fig = px.scatter_mapbox(
        photo_locations,
        lat="lat",
        lon="lon", 
        size="photo_count",
        hover_name="location",
        hover_data=["photo_count", "recent_photo"],
        color="photo_count",
        size_max=15,
        zoom=17,
        title="Highland Tower Development - Photo Locations"
    )
    
    fig.update_layout(
        mapbox_style="open-street-map",
        height=400,
        margin={"r":0,"t":50,"l":0,"b":0}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Location statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("GPS-Tagged Photos", "2,124", "74.6% of total")
    with col2:
        st.metric("Location Accuracy", "±3 meters", "Excellent precision")
    with col3:
        st.metric("Site Coverage", "95%", "Comprehensive documentation")
    
    # Location-based photo summary
    st.subheader("📊 Photos by Location")
    st.dataframe(photo_locations, use_container_width=True)

def render_photo_analytics():
    """Photo analytics and insights"""
    st.subheader("📊 Photo Analytics & Insights")
    
    # Time-based analytics
    col1, col2 = st.columns(2)
    
    with col1:
        # Photos over time
        time_data = pd.DataFrame({
            "Date": pd.date_range("2025-05-01", "2025-05-25", freq="D"),
            "Photos": [23, 28, 31, 19, 25, 33, 29, 27, 24, 30, 35, 22, 26, 31, 28, 25, 29, 32, 27, 24, 30, 28, 26, 31, 29]
        })
        
        fig = px.line(time_data, x="Date", y="Photos", 
                     title="Daily Photo Upload Trends")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Photos by time of day
        time_of_day_data = pd.DataFrame({
            "Hour": list(range(24)),
            "Photos": [0, 0, 0, 0, 0, 0, 2, 15, 45, 67, 89, 78, 56, 67, 89, 78, 45, 23, 12, 5, 2, 1, 0, 0]
        })
        
        fig = px.bar(time_of_day_data, x="Hour", y="Photos",
                    title="Photo Activity by Hour of Day")
        st.plotly_chart(fig, use_container_width=True)
    
    # Quality metrics
    st.subheader("🎯 Quality Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Photo Quality Score", "94.2%", "+2.1% this month")
    with col2:
        st.metric("Metadata Completeness", "87.6%", "+5.2% improvement")
    with col3:
        st.metric("Auto-Tag Accuracy", "91.8%", "Machine learning improving")
    with col4:
        st.metric("Duplicate Detection", "2.3%", "Low duplicate rate")
    
    # Photographer performance
    st.subheader("👤 Photographer Performance")
    
    photographer_data = pd.DataFrame([
        {"Photographer": "John Smith", "Photos": 456, "Quality Score": 96.2, "Avg Response Time": "2.3 hours"},
        {"Photographer": "Sarah Chen", "Photos": 398, "Quality Score": 94.8, "Avg Response Time": "1.8 hours"},
        {"Photographer": "Mike Torres", "Photos": 367, "Quality Score": 93.1, "Avg Response Time": "3.1 hours"},
        {"Photographer": "Jennifer Walsh", "Photos": 289, "Quality Score": 95.4, "Avg Response Time": "2.7 hours"},
        {"Photographer": "David Park", "Photos": 234, "Quality Score": 92.7, "Avg Response Time": "4.2 hours"}
    ])
    
    st.dataframe(photographer_data, use_container_width=True)

def render_photo_settings():
    """Photo management settings"""
    st.subheader("⚙️ Photo Management Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📤 Upload Settings**")
        max_file_size = st.slider("Max File Size (MB)", 1, 50, 10)
        auto_resize = st.checkbox("Auto-resize large images", value=True)
        watermark = st.checkbox("Add project watermark", value=False)
        gps_required = st.checkbox("Require GPS coordinates", value=True)
        
        st.markdown("**🔔 Notification Settings**")
        email_notifications = st.checkbox("Email notifications for new photos", value=True)
        critical_alerts = st.checkbox("Instant alerts for critical photos", value=True)
        daily_summary = st.checkbox("Daily photo summary report", value=True)
    
    with col2:
        st.markdown("**🏷️ Auto-Tagging Settings**")
        enable_ai_tagging = st.checkbox("Enable AI-powered auto-tagging", value=True)
        confidence_threshold = st.slider("AI Confidence Threshold", 0.5, 1.0, 0.8)
        auto_approve_tags = st.checkbox("Auto-approve high-confidence tags", value=False)
        
        st.markdown("**💾 Storage Settings**")
        backup_enabled = st.checkbox("Automatic cloud backup", value=True)
        compression_level = st.selectbox("Image Compression", ["None", "Low", "Medium", "High"])
        retention_period = st.selectbox("Photo Retention", ["1 year", "2 years", "5 years", "Permanent"])
    
    # Save settings
    if st.button("💾 Save Settings", type="primary"):
        st.success("✅ Settings saved successfully!")
        st.info("📧 Settings change notification sent to administrators.")

if __name__ == "__main__":
    render()