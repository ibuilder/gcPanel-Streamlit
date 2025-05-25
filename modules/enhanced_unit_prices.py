"""
Enhanced Unit Prices Module - Highland Tower Development
Consolidated Materials, Equipment, Labor & Subcontractor Management
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def render():
    """Render the enhanced unit prices module with subcontractor capabilities"""
    st.title("💲 Unit Prices - Highland Tower Development")
    st.markdown("**Comprehensive Materials, Equipment, Labor & Subcontractor Cost Management**")
    
    # User role-based access
    user_role = st.session_state.get("user_role", "viewer")
    user_company = st.session_state.get("user_company", "Highland Tower Development")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧱 Materials", "🚜 Equipment", "👷 Labor", "🏢 Subcontractors", "📊 Analysis"
    ])
    
    with tab1:
        render_materials_section(user_role, user_company)
    
    with tab2:
        render_equipment_section(user_role, user_company)
    
    with tab3:
        render_labor_section(user_role, user_company)
    
    with tab4:
        render_subcontractor_section(user_role, user_company)
    
    with tab5:
        render_analysis_section()

def render_materials_section(user_role, user_company):
    """Materials cost management with subcontractor input"""
    st.header("🧱 Material Cost Management")
    
    # Action buttons based on role
    if user_role in ["admin", "project_manager", "subcontractor"]:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("➕ Add Material Item"):
                st.session_state.show_material_form = True
        with col2:
            if st.button("📝 Update Prices"):
                st.session_state.show_price_update = True
        with col3:
            if st.button("📊 Export Materials"):
                st.session_state.show_export = True
    
    # Add/Edit material form
    if st.session_state.get("show_material_form", False):
        render_material_form(user_role, user_company)
    
    # Highland Tower Development authentic materials data
    materials_data = get_highland_tower_materials(user_company)
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        category_filter = st.selectbox("Category", 
            ["All", "Structural Steel", "Concrete", "MEP", "Finishes", "Glass"])
    with col2:
        supplier_filter = st.selectbox("Supplier", 
            ["All", "Steel Fabricators Inc", "NYC Concrete", "HVAC Systems"])
    with col3:
        status_filter = st.selectbox("Status", 
            ["All", "Current", "Pending Approval", "Updated"])
    with col4:
        show_variance = st.checkbox("Show Cost Variance Only", False)
    
    # Filter data
    filtered_data = filter_materials_data(materials_data, category_filter, 
                                        supplier_filter, status_filter, show_variance)
    
    # Display materials table
    st.dataframe(filtered_data, use_container_width=True)
    
    # Cost impact summary
    if not filtered_data.empty:
        total_budget = (filtered_data["Budget_Price"] * filtered_data["Quantity"]).sum()
        total_current = (filtered_data["Current_Price"] * filtered_data["Quantity"]).sum()
        variance = total_current - total_budget
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Budget Total", f"${total_budget:,.2f}")
        col2.metric("Current Total", f"${total_current:,.2f}")
        col3.metric("Variance", f"${variance:,.2f}", 
                   delta=f"{(variance/total_budget)*100:.1f}%" if total_budget > 0 else "0%")

def render_equipment_section(user_role, user_company):
    """Equipment cost management"""
    st.header("🚜 Equipment Cost Management")
    
    # Equipment data
    equipment_data = get_highland_tower_equipment()
    
    # Equipment overview
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Equipment", "12 units")
    col2.metric("Monthly Cost", "$245,600")
    col3.metric("Utilization Rate", "87.5%")
    col4.metric("Maintenance Due", "3 units")
    
    # Equipment table
    st.subheader("Equipment Inventory & Costs")
    st.dataframe(equipment_data, use_container_width=True)

def render_labor_section(user_role, user_company):
    """Labor rates and crew management"""
    st.header("👷 Labor Rate Management")
    
    # Action buttons based on role
    if user_role in ["admin", "project_manager", "site_superintendent"]:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📥 Receive Labor", type="primary"):
                st.session_state.show_receive_labor = True
        with col2:
            if st.button("➕ Add Crew"):
                st.session_state.show_add_crew = True
        with col3:
            if st.button("📊 Update Rates"):
                st.session_state.show_update_rates = True
        with col4:
            if st.button("📈 Labor Analytics"):
                st.session_state.show_labor_analytics = True
    
    # Receive Labor form
    if st.session_state.get("show_receive_labor", False):
        render_receive_labor_form(user_role, user_company)
    
    # Add Crew form
    if st.session_state.get("show_add_crew", False):
        render_add_crew_form(user_role, user_company)
    
    # Labor rates data
    labor_data = get_highland_tower_labor_rates()
    
    # Labor overview
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Crews", "8 crews")
    col2.metric("Daily Labor Cost", "$28,450")
    col3.metric("Productivity Index", "112.5%")
    col4.metric("Overtime Hours", "24 hrs")
    
    # Labor rates table
    st.subheader("Trade Labor Rates")
    st.dataframe(labor_data, use_container_width=True)

def render_subcontractor_section(user_role, user_company):
    """Subcontractor pricing management"""
    st.header("🏢 Subcontractor Pricing")
    
    # Check if user is a subcontractor
    is_subcontractor = user_role == "subcontractor"
    can_edit = user_role in ["admin", "project_manager", "subcontractor"]
    
    if is_subcontractor:
        st.info(f"Welcome {user_company}! You can add and edit your unit prices below.")
    
    # Subcontractor action buttons
    if can_edit:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("➕ Add Unit Price"):
                st.session_state.show_subcontractor_form = True
        with col2:
            if st.button("📝 Update My Prices") if is_subcontractor else st.button("📝 Update Prices"):
                st.session_state.show_price_update_form = True
        with col3:
            if st.button("📋 Submit for Approval"):
                st.session_state.show_approval_form = True
    
    # Subcontractor pricing form
    if st.session_state.get("show_subcontractor_form", False):
        render_subcontractor_pricing_form(user_role, user_company)
    
    # Subcontractor data
    subcontractor_data = get_subcontractor_pricing_data(user_company if is_subcontractor else None)
    
    # Display subcontractor pricing
    st.subheader("Subcontractor Unit Prices")
    
    # Filter by subcontractor company if admin
    if not is_subcontractor:
        company_filter = st.selectbox("Filter by Company", 
            ["All Companies", "Elite Steel Works", "Metro Electric", "Precision Concrete", "HVAC Masters"])
        if company_filter != "All Companies":
            subcontractor_data = subcontractor_data[subcontractor_data["Company"] == company_filter]
    
    st.dataframe(subcontractor_data, use_container_width=True)

def render_analysis_section():
    """Cost analysis and trends"""
    st.header("📊 Cost Analysis & Trends")
    
    # Cost trend analysis
    create_cost_trend_charts()
    
    # Variance analysis
    create_variance_analysis()

def render_material_form(user_role, user_company):
    """Form for adding/editing materials"""
    st.subheader("Add/Edit Material Item")
    
    with st.form("material_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            item_code = st.text_input("Item Code", placeholder="STL-W24-62")
            description = st.text_area("Description", placeholder="W24x62 Steel Beam - ASTM A992")
            unit = st.selectbox("Unit", ["LF", "SF", "CY", "EA", "TON", "LB"])
            category = st.selectbox("Category", 
                ["Structural Steel", "Concrete", "MEP", "Finishes", "Glass"])
        
        with col2:
            budget_price = st.number_input("Budget Price", min_value=0.0, step=0.01)
            current_price = st.number_input("Current Price", min_value=0.0, step=0.01)
            supplier = st.text_input("Supplier", placeholder="Steel Fabricators Inc")
            lead_time = st.number_input("Lead Time (days)", min_value=0, step=1)
        
        submitted = st.form_submit_button("💾 Save Material")
        
        if submitted:
            # Save material data (would integrate with database)
            st.success(f"✅ Material {item_code} saved successfully!")
            st.session_state.show_material_form = False
            st.rerun()

def render_subcontractor_pricing_form(user_role, user_company):
    """Form for subcontractors to add/edit their pricing"""
    st.subheader(f"Add Unit Price - {user_company}")
    
    with st.form("subcontractor_pricing_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            work_item = st.text_input("Work Item", placeholder="Structural Steel Installation")
            unit_of_measure = st.selectbox("Unit", ["LF", "SF", "CY", "EA", "TON", "HR"])
            unit_price = st.number_input("Unit Price ($)", min_value=0.0, step=0.01)
            trade = st.selectbox("Trade", 
                ["Structural Steel", "Electrical", "Plumbing", "HVAC", "Concrete", "Finishes"])
        
        with col2:
            scope_description = st.text_area("Scope Description")
            includes = st.text_area("Includes", placeholder="Labor, equipment, small tools...")
            excludes = st.text_area("Excludes", placeholder="Permits, crane time...")
            valid_until = st.date_input("Valid Until", 
                value=datetime.now() + timedelta(days=30))
        
        notes = st.text_area("Additional Notes")
        
        submitted = st.form_submit_button("💾 Submit for Approval")
        
        if submitted:
            st.success(f"✅ Unit price submitted for approval!")
            st.info("💡 Your pricing will be reviewed by the project team.")
            st.session_state.show_subcontractor_form = False
            st.rerun()

def get_highland_tower_materials(user_company=None):
    """Get Highland Tower Development materials data"""
    materials = pd.DataFrame([
        {
            "Item_Code": "STL-W24-62",
            "Description": "W24x62 Steel Beam - ASTM A992",
            "Category": "Structural Steel",
            "Unit": "LF",
            "Budget_Price": 45.80,
            "Current_Price": 47.20,
            "Quantity": 2450,
            "Supplier": "Steel Fabricators Inc",
            "Last_Updated": "2025-05-20",
            "Status": "Current"
        },
        {
            "Item_Code": "CON-4000PSI",
            "Description": "4000 PSI Concrete",
            "Category": "Concrete", 
            "Unit": "CY",
            "Budget_Price": 125.00,
            "Current_Price": 128.50,
            "Quantity": 850,
            "Supplier": "NYC Concrete",
            "Last_Updated": "2025-05-18",
            "Status": "Current"
        },
        {
            "Item_Code": "RBR-#5",
            "Description": "Rebar #5 Grade 60",
            "Category": "Structural Steel",
            "Unit": "TON",
            "Budget_Price": 850.00,
            "Current_Price": 875.00,
            "Quantity": 125,
            "Supplier": "Steel Fabricators Inc",
            "Last_Updated": "2025-05-15",
            "Status": "Updated"
        }
    ])
    
    # Calculate variance
    materials["Variance_%"] = ((materials["Current_Price"] - materials["Budget_Price"]) / materials["Budget_Price"] * 100).round(1)
    materials["Total_Budget"] = materials["Budget_Price"] * materials["Quantity"]
    materials["Total_Current"] = materials["Current_Price"] * materials["Quantity"]
    
    return materials

def get_highland_tower_equipment():
    """Get Highland Tower equipment data"""
    return pd.DataFrame([
        {
            "Equipment_ID": "CR-250T-01",
            "Description": "250-Ton Tower Crane",
            "Type": "Rental",
            "Daily_Rate": 2850.00,
            "Monthly_Rate": 72000.00,
            "Utilization_%": 94.5,
            "Status": "Active",
            "Location": "Level 13"
        },
        {
            "Equipment_ID": "EX-350-02", 
            "Description": "CAT 350 Excavator",
            "Type": "Owned",
            "Daily_Rate": 875.00,
            "Monthly_Rate": 22000.00,
            "Utilization_%": 78.2,
            "Status": "Active",
            "Location": "Site Yard"
        }
    ])

def get_highland_tower_labor_rates():
    """Get Highland Tower labor rates"""
    return pd.DataFrame([
        {
            "Trade": "Structural Steel Workers",
            "Base_Rate": 42.50,
            "Overtime_Rate": 63.75,
            "Benefits": 28.40,
            "Total_Rate": 70.90,
            "Crew_Size": 12,
            "Union": "Local 40"
        },
        {
            "Trade": "Electricians",
            "Base_Rate": 38.75,
            "Overtime_Rate": 58.13,
            "Benefits": 26.20,
            "Total_Rate": 64.95,
            "Crew_Size": 8,
            "Union": "Local 3"
        }
    ])

def get_subcontractor_pricing_data(user_company=None):
    """Get subcontractor pricing data"""
    data = pd.DataFrame([
        {
            "Company": "Elite Steel Works",
            "Work_Item": "Structural Steel Installation",
            "Unit": "TON",
            "Unit_Price": 2850.00,
            "Status": "Approved",
            "Valid_Until": "2025-06-30",
            "Last_Updated": "2025-05-20"
        },
        {
            "Company": "Metro Electric",
            "Work_Item": "Electrical Rough-In",
            "Unit": "SF",
            "Unit_Price": 12.50,
            "Status": "Pending",
            "Valid_Until": "2025-06-15",
            "Last_Updated": "2025-05-18"
        },
        {
            "Company": "Precision Concrete",
            "Work_Item": "Concrete Placement",
            "Unit": "CY",
            "Unit_Price": 165.00,
            "Status": "Approved",
            "Valid_Until": "2025-07-01",
            "Last_Updated": "2025-05-15"
        }
    ])
    
    if user_company and user_company != "Highland Tower Development":
        data = data[data["Company"] == user_company]
    
    return data

def filter_materials_data(data, category, supplier, status, show_variance):
    """Filter materials data based on selections"""
    filtered = data.copy()
    
    if category != "All":
        filtered = filtered[filtered["Category"] == category]
    if supplier != "All":
        filtered = filtered[filtered["Supplier"] == supplier] 
    if status != "All":
        filtered = filtered[filtered["Status"] == status]
    if show_variance:
        filtered = filtered[abs(filtered["Variance_%"]) > 1.0]
    
    return filtered

def create_cost_trend_charts():
    """Create cost trend visualization"""
    # Sample trend data
    dates = pd.date_range(start='2025-01-01', end='2025-05-25', freq='W')
    steel_prices = np.random.normal(45.80, 2, len(dates)).cumsum() * 0.1 + 45.80
    concrete_prices = np.random.normal(125.00, 3, len(dates)).cumsum() * 0.05 + 125.00
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=steel_prices, name="Steel Beams", line=dict(color='#1f77b4')))
    fig.add_trace(go.Scatter(x=dates, y=concrete_prices, name="Concrete", line=dict(color='#ff7f0e')))
    
    fig.update_layout(
        title="Material Cost Trends - Highland Tower Development",
        xaxis_title="Date",
        yaxis_title="Price per Unit ($)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_variance_analysis():
    """Create variance analysis chart"""
    variance_data = pd.DataFrame({
        "Category": ["Structural Steel", "Concrete", "MEP", "Finishes"],
        "Budget_Variance_%": [3.1, 2.8, -1.2, 4.5],
        "Impact_$": [15600, 8200, -2400, 12800]
    })
    
    fig = px.bar(variance_data, x="Category", y="Budget_Variance_%", 
                color="Budget_Variance_%", 
                title="Cost Variance by Category",
                color_continuous_scale="RdYlBu_r")
    
    st.plotly_chart(fig, use_container_width=True)

def render_receive_labor_form(user_role, user_company):
    """Render form for receiving labor on Highland Tower Development"""
    st.subheader("📥 Receive Labor - Highland Tower Development")
    
    with st.form("receive_labor_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Labor Details**")
            crew_type = st.selectbox("Crew Type", [
                "Structural Steel Workers", "Concrete Workers", "Electricians", 
                "Plumbers", "HVAC Technicians", "General Laborers", "Equipment Operators"
            ])
            crew_size = st.number_input("Number of Workers", min_value=1, max_value=50, value=8)
            shift_type = st.selectbox("Shift", ["Day Shift", "Night Shift", "Weekend"])
            start_time = st.time_input("Start Time", value=pd.to_datetime("07:00").time())
            
        with col2:
            st.markdown("**Assignment Details**")
            work_location = st.selectbox("Work Location", [
                "Level 13 - Steel Erection", "Level 11 - MEP Rough-in", 
                "Level 9 - Concrete Pour", "Site Yard", "Basement - Foundation"
            ])
            supervisor = st.selectbox("Supervisor", [
                "Mike Rodriguez - Steel Foreman", "Sarah Chen - Concrete Foreman",
                "David Park - MEP Supervisor", "Lisa Johnson - General Foreman"
            ])
            work_description = st.text_area("Work Description", 
                placeholder="Describe the specific work to be performed...")
            estimated_duration = st.number_input("Estimated Duration (hours)", min_value=1, max_value=16, value=8)
        
        # Safety requirements
        st.markdown("**Safety Requirements**")
        safety_col1, safety_col2 = st.columns(2)
        with safety_col1:
            safety_meeting = st.checkbox("Pre-shift safety meeting completed", value=True)
            ppe_verified = st.checkbox("PPE verified and documented", value=True)
        with safety_col2:
            hazard_assessment = st.checkbox("Job hazard assessment completed", value=True)
            permits_current = st.checkbox("All permits current and valid", value=True)
        
        submitted = st.form_submit_button("✅ Confirm Labor Received", type="primary")
        
        if submitted:
            st.success(f"✅ Labor received: {crew_size} {crew_type} assigned to {work_location}")
            st.info(f"📋 Supervisor: {supervisor} | Estimated: {estimated_duration} hours")
            st.session_state.show_receive_labor = False
            st.rerun()

def render_add_crew_form(user_role, user_company):
    """Render form for adding new crew to Highland Tower Development"""
    st.subheader("➕ Add New Crew - Highland Tower Development")
    
    with st.form("add_crew_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Crew Information**")
            crew_name = st.text_input("Crew Name", placeholder="Steel Crew Alpha")
            trade = st.selectbox("Trade", [
                "Structural Steel", "Concrete", "Electrical", "Plumbing", 
                "HVAC", "General Labor", "Equipment Operation", "Carpentry"
            ])
            crew_leader = st.text_input("Crew Leader", placeholder="John Smith")
            contact_number = st.text_input("Contact Number", placeholder="(555) 123-4567")
            
        with col2:
            st.markdown("**Crew Composition**")
            journeymen = st.number_input("Journeymen", min_value=0, max_value=20, value=3)
            apprentices = st.number_input("Apprentices", min_value=0, max_value=10, value=2)
            helpers = st.number_input("Helpers/Laborers", min_value=0, max_value=15, value=3)
            total_crew = journeymen + apprentices + helpers
            st.metric("Total Crew Size", total_crew)
        
        # Rate information
        st.markdown("**Rate Information**")
        rate_col1, rate_col2, rate_col3 = st.columns(3)
        with rate_col1:
            journeyman_rate = st.number_input("Journeyman Rate ($/hr)", min_value=25.0, max_value=100.0, value=42.50)
        with rate_col2:
            apprentice_rate = st.number_input("Apprentice Rate ($/hr)", min_value=15.0, max_value=60.0, value=32.50)
        with rate_col3:
            helper_rate = st.number_input("Helper Rate ($/hr)", min_value=15.0, max_value=40.0, value=22.50)
        
        # Certifications
        st.markdown("**Certifications & Requirements**")
        cert_col1, cert_col2 = st.columns(2)
        with cert_col1:
            osha_certified = st.checkbox("OSHA 30 Certified", value=True)
            drug_tested = st.checkbox("Drug testing current", value=True)
        with cert_col2:
            background_checked = st.checkbox("Background check completed", value=True)
            union_status = st.selectbox("Union Status", ["Union", "Non-Union", "Mixed"])
        
        submitted = st.form_submit_button("👥 Add Crew to Project", type="primary")
        
        if submitted:
            daily_cost = (journeymen * journeyman_rate + apprentices * apprentice_rate + helpers * helper_rate) * 8
            st.success(f"✅ Crew '{crew_name}' added to Highland Tower Development")
            st.info(f"💰 Estimated daily cost: ${daily_cost:,.2f}")
            st.session_state.show_add_crew = False
            st.rerun()

def render_labor_analytics_section():
    """Render labor analytics and performance metrics"""
    st.subheader("📈 Labor Analytics - Highland Tower Development")
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Productivity Rate", "112%", "+8% this week")
    with col2:
        st.metric("Attendance Rate", "94.5%", "+2.1%")
    with col3:
        st.metric("Safety Score", "98.2%", "0 incidents")
    with col4:
        st.metric("Overtime Hours", "124 hrs", "-15% vs last week")
    
    # Labor productivity chart
    productivity_data = pd.DataFrame({
        "Week": ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"],
        "Steel_Crew": [98, 102, 108, 112, 115],
        "Concrete_Crew": [95, 101, 105, 110, 112],
        "MEP_Crew": [88, 92, 98, 105, 108]
    })
    
    fig = px.line(productivity_data, x="Week", y=["Steel_Crew", "Concrete_Crew", "MEP_Crew"],
                 title="Weekly Productivity Index by Trade (%)",
                 labels={"value": "Productivity Index (%)", "variable": "Crew Type"})
    st.plotly_chart(fig, use_container_width=True)
    
    # Labor cost analysis
    st.markdown("#### 💰 Labor Cost Analysis")
    cost_breakdown = pd.DataFrame({
        "Trade": ["Structural Steel", "Concrete", "Electrical", "Plumbing", "HVAC"],
        "Budgeted_Hours": [2400, 1800, 1600, 1200, 1000],
        "Actual_Hours": [2280, 1850, 1520, 1180, 980],
        "Variance_Hours": [-120, 50, -80, -20, -20],
        "Cost_Impact": [-5040, 2100, -3360, -840, -840]
    })
    
    st.dataframe(cost_breakdown, use_container_width=True)
    
    # Action recommendations
    st.markdown("#### 🎯 Recommendations")
    st.success("✅ Steel crew exceeding productivity targets - consider bonus incentive")
    st.warning("⚠️ Concrete crew slightly over budget - monitor for next pour")
    st.info("💡 Overall labor efficiency up 8% - excellent progress")