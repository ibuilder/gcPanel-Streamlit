"""
Highland Tower Development - Deliveries Management Module
Comprehensive delivery scheduling, tracking, and coordination system
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

def render_deliveries():
    """Render the comprehensive deliveries management interface"""
    
    st.title("🚛 Highland Tower Deliveries")
    st.markdown("**Comprehensive delivery scheduling, tracking, and coordination system**")
    
    # Real-time delivery status overview
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); padding: 1rem; border-radius: 12px; margin-bottom: 2rem;">
        <h3 style="color: white; margin: 0;">📊 Today's Delivery Operations</h3>
        <p style="color: #dbeafe; margin: 0.5rem 0 0 0;">Highland Tower Development - Live Tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🚛 Scheduled Today", "12", delta="3 more than yesterday")
    with col2:
        st.metric("✅ Completed", "8", delta="On schedule")
    with col3:
        st.metric("🕐 In Transit", "3", delta="Real-time tracking")
    with col4:
        st.metric("⚠️ Delayed", "1", delta="-2 vs last week", delta_color="inverse")
    
    # Main tabs for different delivery management aspects
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📅 Schedule & Coordination", 
        "📊 Live Tracking", 
        "📋 Delivery Forms", 
        "📈 Performance Analytics",
        "⚙️ Settings & Integration"
    ])
    
    with tab1:
        render_delivery_scheduling()
    
    with tab2:
        render_live_tracking()
    
    with tab3:
        render_delivery_forms()
    
    with tab4:
        render_delivery_analytics()
    
    with tab5:
        render_delivery_settings()

def render_delivery_scheduling():
    """Render delivery scheduling and coordination interface"""
    
    st.markdown("### 📅 Delivery Schedule Coordination")
    
    # Calendar view and scheduling controls
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🗓️ Weekly Delivery Calendar")
        
        # Create sample delivery schedule data
        delivery_schedule = [
            {
                "Date": "2025-01-27",
                "Time": "8:00 AM",
                "Material": "Steel Beams - Level 14",
                "Supplier": "Steel Fabricators Inc",
                "Quantity": "24 pieces",
                "Status": "Confirmed",
                "Crane_Required": "Yes",
                "Contact": "Mike Rodriguez"
            },
            {
                "Date": "2025-01-27", 
                "Time": "10:30 AM",
                "Material": "Concrete Mix - Level 13",
                "Supplier": "Highland Concrete",
                "Quantity": "45 cubic yards",
                "Status": "Confirmed",
                "Crane_Required": "No",
                "Contact": "Sarah Chen"
            },
            {
                "Date": "2025-01-28",
                "Time": "7:00 AM",
                "Material": "Rebar - Level 14",
                "Supplier": "Metro Steel Supply",
                "Quantity": "8 tons",
                "Status": "Pending",
                "Crane_Required": "Yes",
                "Contact": "David Kim"
            },
            {
                "Date": "2025-01-28",
                "Time": "2:00 PM",
                "Material": "MEP Equipment",
                "Supplier": "Advanced Building Systems",
                "Quantity": "HVAC Units (4)",
                "Status": "Confirmed",
                "Crane_Required": "Yes",
                "Contact": "Lisa Wong"
            }
        ]
        
        schedule_df = pd.DataFrame(delivery_schedule)
        
        # Enhanced schedule display with color coding
        for _, delivery in schedule_df.iterrows():
            status_color = {
                "Confirmed": "🟢",
                "Pending": "🟡", 
                "Delayed": "🔴",
                "Cancelled": "⚫"
            }.get(delivery["Status"], "🔵")
            
            crane_icon = "🏗️" if delivery["Crane_Required"] == "Yes" else "📦"
            
            st.markdown(f"""
            <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; background: white;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{status_color} {delivery['Date']} at {delivery['Time']}</strong>
                        <br>
                        {crane_icon} <strong>{delivery['Material']}</strong>
                        <br>
                        <em>{delivery['Supplier']} - {delivery['Quantity']}</em>
                        <br>
                        👤 Contact: {delivery['Contact']}
                    </div>
                    <div style="text-align: right;">
                        <span style="background: #dbeafe; color: #1e40af; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">
                            {delivery['Status']}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### ➕ Schedule New Delivery")
        
        with st.form("new_delivery_form"):
            delivery_date = st.date_input("📅 Delivery Date", datetime.now() + timedelta(days=1))
            delivery_time = st.time_input("🕐 Delivery Time", value=datetime.now().time())
            
            material_type = st.selectbox("📦 Material Type", [
                "Steel Beams", "Concrete Mix", "Rebar", "MEP Equipment",
                "Drywall", "Windows", "Roofing Materials", "Insulation",
                "Electrical Components", "Plumbing Fixtures"
            ])
            
            supplier = st.text_input("🏢 Supplier", placeholder="Supplier Company Name")
            quantity = st.text_input("📊 Quantity", placeholder="e.g., 24 pieces, 45 cubic yards")
            
            crane_required = st.selectbox("🏗️ Crane Required?", ["No", "Yes"])
            
            contact_person = st.text_input("👤 Site Contact", placeholder="Name of receiving personnel")
            
            special_instructions = st.text_area("📝 Special Instructions", 
                placeholder="Access requirements, safety considerations, etc.")
            
            submitted = st.form_submit_button("📅 Schedule Delivery", use_container_width=True)
            
            if submitted:
                st.success(f"""
                ✅ **Delivery Scheduled Successfully!**
                
                📅 **Date:** {delivery_date}  
                🕐 **Time:** {delivery_time}  
                📦 **Material:** {material_type}  
                🏢 **Supplier:** {supplier}  
                📊 **Quantity:** {quantity}  
                🏗️ **Crane:** {crane_required}  
                👤 **Contact:** {contact_person}
                
                📧 Confirmation sent to all stakeholders.
                """)

def render_live_tracking():
    """Render real-time delivery tracking interface"""
    
    st.markdown("### 📊 Live Delivery Tracking")
    
    # Real-time tracking map simulation
    st.markdown("#### 🗺️ Live GPS Tracking")
    
    # Create sample tracking data
    tracking_data = [
        {
            "Delivery_ID": "HTD-2025-0127-001",
            "Material": "Steel Beams - Level 14",
            "Supplier": "Steel Fabricators Inc",
            "Driver": "John Martinez",
            "Truck": "Truck #SF-204",
            "Status": "En Route",
            "ETA": "8:15 AM",
            "Distance": "12.3 miles",
            "Progress": 75,
            "Last_Update": "7:45 AM"
        },
        {
            "Delivery_ID": "HTD-2025-0127-002", 
            "Material": "Concrete Mix - Level 13",
            "Supplier": "Highland Concrete",
            "Driver": "Maria Santos",
            "Truck": "Mixer #HC-108",
            "Status": "Loading",
            "ETA": "10:45 AM", 
            "Distance": "8.7 miles",
            "Progress": 25,
            "Last_Update": "7:30 AM"
        },
        {
            "Delivery_ID": "HTD-2025-0127-003",
            "Material": "MEP Equipment",
            "Supplier": "Advanced Building Systems",
            "Driver": "Robert Chen",
            "Truck": "Flatbed #ABS-305",
            "Status": "Delayed",
            "ETA": "2:30 PM",
            "Distance": "15.2 miles", 
            "Progress": 10,
            "Last_Update": "7:50 AM"
        }
    ]
    
    for delivery in tracking_data:
        status_color = {
            "En Route": "🟢",
            "Loading": "🟡",
            "Delayed": "🔴",
            "Delivered": "✅"
        }.get(delivery["Status"], "🔵")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; background: white;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{status_color} {delivery['Delivery_ID']}</strong>
                        <br>
                        📦 <strong>{delivery['Material']}</strong>
                        <br>
                        🚛 {delivery['Driver']} - {delivery['Truck']}
                        <br>
                        📍 {delivery['Distance']} away • ETA: {delivery['ETA']}
                        <br>
                        <small>Last update: {delivery['Last_Update']}</small>
                    </div>
                </div>
                <div style="margin-top: 0.5rem;">
                    <div style="background: #f1f5f9; border-radius: 4px; height: 8px; overflow: hidden;">
                        <div style="background: #3b82f6; height: 100%; width: {delivery['Progress']}%; transition: width 0.3s;"></div>
                    </div>
                    <small style="color: #64748b;">{delivery['Progress']}% complete</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button(f"📞 Contact", key=f"contact_{delivery['Delivery_ID']}"):
                st.info(f"""
                **📞 Contact Information**
                
                👤 **Driver:** {delivery['Driver']}  
                📱 **Phone:** (555) 123-4567  
                🚛 **Truck:** {delivery['Truck']}  
                🏢 **Supplier:** {delivery['Supplier']}
                """)

def render_delivery_forms():
    """Render delivery documentation and forms"""
    
    st.markdown("### 📋 Delivery Documentation")
    
    # Receipt and inspection forms
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Delivery Receipt Form")
        
        with st.form("delivery_receipt"):
            delivery_id = st.text_input("🆔 Delivery ID", placeholder="HTD-2025-0127-001")
            received_by = st.text_input("👤 Received By", placeholder="Your name")
            
            material_condition = st.selectbox("📦 Material Condition", [
                "Excellent - No issues",
                "Good - Minor cosmetic damage",
                "Fair - Some damage noted", 
                "Poor - Significant damage",
                "Rejected - Unacceptable condition"
            ])
            
            quantity_received = st.text_input("📊 Quantity Received", placeholder="Actual quantity received")
            quantity_expected = st.text_input("📋 Quantity Expected", placeholder="Expected quantity")
            
            delivery_notes = st.text_area("📝 Notes", placeholder="Any additional comments or observations")
            
            photo_upload = st.file_uploader("📸 Upload Photos", 
                accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])
            
            receipt_submitted = st.form_submit_button("✅ Submit Receipt", use_container_width=True)
            
            if receipt_submitted:
                st.success("📋 **Delivery Receipt Submitted Successfully!**")
    
    with col2:
        st.markdown("#### 🔍 Quality Inspection Checklist")
        
        with st.form("quality_inspection"):
            st.markdown("**📋 Inspection Criteria**")
            
            criteria_checks = {
                "Material matches specifications": st.checkbox("Material matches specifications", value=True),
                "Quantity is correct": st.checkbox("Quantity is correct", value=True),
                "No visible damage": st.checkbox("No visible damage", value=True),
                "Proper packaging/protection": st.checkbox("Proper packaging/protection", value=True),
                "Documentation complete": st.checkbox("Documentation complete", value=True),
                "Storage requirements met": st.checkbox("Storage requirements met", value=True)
            }
            
            overall_rating = st.selectbox("⭐ Overall Rating", [
                "5 - Excellent", "4 - Good", "3 - Satisfactory", 
                "2 - Needs Improvement", "1 - Unacceptable"
            ])
            
            inspector_name = st.text_input("👤 Inspector Name", placeholder="Quality inspector name")
            inspection_notes = st.text_area("📝 Inspection Notes", 
                placeholder="Detailed inspection observations")
            
            inspection_submitted = st.form_submit_button("🔍 Submit Inspection", use_container_width=True)
            
            if inspection_submitted:
                passed_checks = sum(criteria_checks.values())
                total_checks = len(criteria_checks)
                
                st.success(f"""
                🔍 **Quality Inspection Completed!**
                
                ✅ **Passed:** {passed_checks}/{total_checks} criteria  
                ⭐ **Rating:** {overall_rating}  
                👤 **Inspector:** {inspector_name}
                """)

def render_delivery_analytics():
    """Render delivery performance analytics and reports"""
    
    st.markdown("### 📈 Delivery Performance Analytics")
    
    # Key performance indicators
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 On-Time Delivery Rate", "94.2%", delta="2.1% improvement")
    with col2:
        st.metric("⏱️ Average Delivery Time", "2.3 hrs", delta="-0.4 hrs vs plan")
    with col3:
        st.metric("💰 Delivery Cost Efficiency", "$847/delivery", delta="-$23 vs budget")
    
    # Charts and visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Weekly Delivery Volume")
        
        # Sample delivery volume data
        volume_data = {
            "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
            "Deliveries": [45, 52, 48, 58],
            "On_Time": [42, 49, 46, 55]
        }
        
        fig = px.bar(volume_data, x="Week", y=["Deliveries", "On_Time"],
                    title="Weekly Delivery Performance",
                    color_discrete_map={"Deliveries": "#3b82f6", "On_Time": "#10b981"})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🏢 Supplier Performance")
        
        # Sample supplier performance data
        supplier_data = {
            "Supplier": ["Steel Fabricators Inc", "Highland Concrete", "Metro Steel Supply", "Advanced Building Systems"],
            "On_Time_Rate": [96.5, 92.1, 89.8, 94.2],
            "Quality_Score": [9.2, 8.8, 8.5, 9.0]
        }
        
        supplier_df = pd.DataFrame(supplier_data)
        
        fig = px.scatter(supplier_df, x="On_Time_Rate", y="Quality_Score",
                        size="Quality_Score", color="Supplier",
                        title="Supplier Performance Matrix")
        st.plotly_chart(fig, use_container_width=True)

def render_delivery_settings():
    """Render delivery system settings and integrations"""
    
    st.markdown("### ⚙️ Delivery System Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔧 System Settings")
        
        auto_notifications = st.checkbox("📧 Auto Email Notifications", value=True)
        sms_alerts = st.checkbox("📱 SMS Delivery Alerts", value=True)
        gps_tracking = st.checkbox("📍 GPS Tracking Integration", value=True)
        photo_required = st.checkbox("📸 Require Delivery Photos", value=True)
        
        notification_lead = st.slider("⏰ Notification Lead Time (hours)", 1, 24, 4)
        
        st.markdown("#### 📞 Emergency Contacts")
        
        emergency_contacts = {
            "Site Supervisor": "Mike Rodriguez - (555) 123-4567",
            "Crane Operator": "Sarah Chen - (555) 234-5678", 
            "Security": "Highland Security - (555) 345-6789",
            "Traffic Control": "City Traffic Dept - (555) 456-7890"
        }
        
        for role, contact in emergency_contacts.items():
            st.text_input(f"👤 {role}", value=contact)
    
    with col2:
        st.markdown("#### 🔌 Integration Settings")
        
        st.markdown("**📊 ERP Integration**")
        sage_integration = st.checkbox("Sage 300 Construction", value=True)
        if sage_integration:
            st.text_input("🔑 Sage API Key", type="password", placeholder="Enter Sage API key")
            st.selectbox("📊 Sync Frequency", ["Real-time", "Every 15 minutes", "Hourly", "Daily"])
        
        st.markdown("**🚛 Logistics Partners**")
        fedex_integration = st.checkbox("FedEx Freight", value=False)
        ups_integration = st.checkbox("UPS Freight", value=False)
        local_carriers = st.checkbox("Local Carrier Network", value=True)
        
        st.markdown("**📍 GPS & Tracking**")
        gps_provider = st.selectbox("GPS Provider", ["Geotab", "Verizon Connect", "Samsara", "Fleet Complete"])
        tracking_interval = st.selectbox("Update Interval", ["30 seconds", "1 minute", "5 minutes", "10 minutes"])
        
        if st.button("💾 Save Settings", use_container_width=True):
            st.success("⚙️ **Settings Saved Successfully!**")