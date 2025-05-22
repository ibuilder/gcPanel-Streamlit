"""
Constructability Review Module for Pre-Construction

This module provides tools for constructability analysis:
- Design review for construction efficiency
- Construction sequencing
- Site logistics planning
- System coordination
- Risk identification
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def render_constructability():
    """Render the Constructability Review dashboard"""
    st.header("Constructability Review")
    
    # Create tabs for different constructability sections
    tabs = st.tabs([
        "Review Dashboard", 
        "Design Review", 
        "Sequencing", 
        "Site Logistics", 
        "System Coordination",
        "Risk Register"
    ])
    
    # Review Dashboard tab
    with tabs[0]:
        render_review_dashboard()
    
    # Design Review tab
    with tabs[1]:
        render_design_review()
    
    # Sequencing tab
    with tabs[2]:
        render_sequencing()
    
    # Site Logistics tab
    with tabs[3]:
        render_site_logistics()
    
    # System Coordination tab
    with tabs[4]:
        render_system_coordination()
        
    # Risk Register tab
    with tabs[5]:
        render_risk_register()

def render_review_dashboard():
    """Render the constructability review dashboard"""
    
    # Constructability stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Review Items",
            value="87",
            help="Total constructability review items"
        )
    
    with col2:
        st.metric(
            label="Open Items",
            value="32",
            delta="-5",
            delta_color="inverse",
            help="Open constructability items"
        )
    
    with col3:
        st.metric(
            label="Critical Issues",
            value="8",
            delta="-2",
            delta_color="inverse",
            help="Critical constructability issues"
        )
    
    with col4:
        st.metric(
            label="Completion",
            value="63%",
            delta="+5%",
            help="Percentage of resolved constructability items"
        )
    
    # Status by discipline
    st.subheader("Constructability Review Status by Discipline")
    
    discipline_data = pd.DataFrame({
        "Discipline": ["Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil", "Other"],
        "Completed": [12, 10, 8, 9, 7, 6, 3],
        "In Progress": [5, 4, 5, 4, 3, 2, 1],
        "Open": [8, 6, 7, 4, 3, 3, 1]
    })
    
    fig = px.bar(
        discipline_data,
        x="Discipline",
        y=["Completed", "In Progress", "Open"],
        title="Review Items by Discipline & Status",
        barmode="stack",
        color_discrete_sequence=["#38d39f", "#4a90e2", "#e53935"]
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity and critical issues
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recent Review Activity")
        
        activities = [
            {"action": "Updated MEP shaft clearance item", "user": "Mike R.", "time": "2 hours ago"},
            {"action": "Resolved structural connection issue", "user": "Sarah T.", "time": "4 hours ago"},
            {"action": "Added new facade access concern", "user": "John D.", "time": "Yesterday"},
            {"action": "Completed civil review", "user": "Lisa K.", "time": "Yesterday"},
            {"action": "Updated foundation detail comments", "user": "Robert M.", "time": "2 days ago"}
        ]
        
        for activity in activities:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                <div>{activity["action"]}</div>
                <div style="color: #6c757d; font-size: 13px;">
                    <span>{activity["user"]}</span> • <span>{activity["time"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Critical Issues")
        
        critical_issues = [
            {"id": "CR-023", "description": "MEP shaft clearance inadequate at floors 8-12", "discipline": "Mechanical", "responsible": "Mike R."},
            {"id": "CR-037", "description": "Foundation depth conflicts with existing utilities", "discipline": "Civil", "responsible": "John D."},
            {"id": "CR-045", "description": "Tower crane location requires foundation redesign", "discipline": "Structural", "responsible": "Sarah T."},
            {"id": "CR-052", "description": "Stair pressurization system requiring redesign", "discipline": "Mechanical", "responsible": "Mike R."},
            {"id": "CR-068", "description": "Loading dock clearance inadequate for fire trucks", "discipline": "Architectural", "responsible": "Lisa K."}
        ]
        
        for issue in critical_issues:
            st.markdown(f"""
            <div style="padding: 10px; border-left: 3px solid #e53935; margin-bottom: 8px; background-color: #f8f9fa;">
                <div style="font-weight: 500;">{issue["id"]}: {issue["description"]}</div>
                <div style="display: flex; justify-content: space-between; font-size: 12px; color: #6c757d;">
                    <span>Discipline: {issue["discipline"]}</span>
                    <span>Responsible: {issue["responsible"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_design_review():
    """Render the design review section"""
    st.subheader("Design Review for Constructability")
    
    # Filter controls
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.text_input("Search Review Items", placeholder="Enter keywords...")
    
    with col2:
        st.selectbox("Discipline", ["All Disciplines", "Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil"])
    
    with col3:
        st.selectbox("Status", ["All Status", "Open", "In Progress", "Resolved"])
    
    with col4:
        st.button("Add Review Item", type="primary")
    
    # Design review items
    review_items = [
        {"id": "CR-023", "description": "MEP shaft clearance inadequate at floors 8-12", "discipline": "Mechanical", "status": "Open", "priority": "Critical", "date": "Apr 5, 2025", "assigned": "Mike R."},
        {"id": "CR-037", "description": "Foundation depth conflicts with existing utilities", "discipline": "Civil", "status": "Open", "priority": "Critical", "date": "Apr 12, 2025", "assigned": "John D."},
        {"id": "CR-042", "description": "Precast panel connections require adjustment", "discipline": "Structural", "status": "In Progress", "priority": "Medium", "date": "Apr 15, 2025", "assigned": "Sarah T."},
        {"id": "CR-045", "description": "Tower crane location requires foundation redesign", "discipline": "Structural", "status": "Open", "priority": "Critical", "date": "Apr 18, 2025", "assigned": "Sarah T."},
        {"id": "CR-048", "description": "Elevator pit waterproofing detail insufficient", "discipline": "Architectural", "status": "In Progress", "priority": "Medium", "date": "Apr 20, 2025", "assigned": "Lisa K."},
        {"id": "CR-052", "description": "Stair pressurization system requiring redesign", "discipline": "Mechanical", "status": "Open", "priority": "Critical", "date": "Apr 22, 2025", "assigned": "Mike R."},
        {"id": "CR-056", "description": "Electrical room layout requires revisions", "discipline": "Electrical", "status": "In Progress", "priority": "Medium", "date": "Apr 25, 2025", "assigned": "Robert M."},
        {"id": "CR-061", "description": "Exterior wall system not coordinated with structure", "discipline": "Architectural", "status": "Resolved", "priority": "High", "date": "Apr 28, 2025", "assigned": "Lisa K."},
        {"id": "CR-064", "description": "Parking garage clear height insufficient", "discipline": "Architectural", "status": "Resolved", "priority": "High", "date": "May 1, 2025", "assigned": "Lisa K."},
        {"id": "CR-068", "description": "Loading dock clearance inadequate for fire trucks", "discipline": "Architectural", "status": "Open", "priority": "Critical", "date": "May 5, 2025", "assigned": "Lisa K."}
    ]
    
    # Create DataFrame
    df_review = pd.DataFrame(review_items)
    
    # Display with styling
    st.dataframe(
        df_review,
        column_config={
            "id": st.column_config.TextColumn("ID", width="small"),
            "description": st.column_config.TextColumn("Description", width="large"),
            "discipline": st.column_config.TextColumn("Discipline", width="small"),
            "status": st.column_config.TextColumn("Status", width="small"),
            "priority": st.column_config.TextColumn("Priority", width="small"),
            "date": st.column_config.TextColumn("Date", width="small"),
            "assigned": st.column_config.TextColumn("Assigned To", width="small")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Review item detail
    st.subheader("Review Item Details")
    
    selected_item = st.selectbox(
        "Select Item to View/Edit", 
        [f"{item['id']}: {item['description']}" for item in review_items]
    )
    
    # Extract ID from selection
    selected_id = selected_item.split(":")[0].strip()
    
    # Find the item
    item_data = next((item for item in review_items if item["id"] == selected_id), None)
    
    if item_data:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.text_input("Item ID", value=item_data["id"], disabled=True)
            st.text_area("Description", value=item_data["description"])
            st.text_area("Proposed Solution", value="Redesign MEP shaft with additional 8 inches clearance at all floors. Update architectural and structural drawings to reflect the change." if selected_id == "CR-023" else "")
            
            st.markdown("##### Attachments")
            st.file_uploader("Upload Supporting Documents", accept_multiple_files=True)
            
            # Mock attachments
            if selected_id in ["CR-023", "CR-037", "CR-045"]:
                st.markdown("""
                **Existing Attachments:**
                - Problem Area Photo.jpg
                - Markup Drawing.pdf
                - Reference Detail.pdf
                """)
        
        with col2:
            st.selectbox("Discipline", ["Mechanical", "Structural", "Architectural", "Electrical", "Plumbing", "Civil"], index=["Mechanical", "Structural", "Architectural", "Electrical", "Plumbing", "Civil"].index(item_data["discipline"]))
            st.selectbox("Status", ["Open", "In Progress", "Resolved"], index=["Open", "In Progress", "Resolved"].index(item_data["status"]))
            st.selectbox("Priority", ["Critical", "High", "Medium", "Low"], index=["Critical", "High", "Medium", "Low"].index(item_data["priority"]))
            st.date_input("Date Identified", value=datetime.strptime(item_data["date"], "%b %d, %Y"))
            st.selectbox("Assigned To", ["Mike R.", "John D.", "Sarah T.", "Lisa K.", "Robert M."], index=["Mike R.", "John D.", "Sarah T.", "Lisa K.", "Robert M."].index(item_data["assigned"]))
            
            st.markdown("##### Impact Assessment")
            st.selectbox("Schedule Impact", ["None", "Minor (1-3 days)", "Moderate (4-10 days)", "Significant (10+ days)"])
            st.selectbox("Cost Impact", ["None", "Minor (<$10K)", "Moderate ($10K-$50K)", "Significant (>$50K)"])
            st.selectbox("Coordination Impact", ["Single Trade", "Multiple Trades", "All Trades"])
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.button("Save Changes", type="primary")
        
        with col4:
            st.button("Delete Item")

def render_sequencing():
    """Render the construction sequencing section"""
    st.subheader("Construction Sequencing Analysis")
    
    # Explanation
    st.markdown("""
    Construction sequencing analysis identifies the optimal order of operations,
    critical path activities, and potential sequencing conflicts before construction begins.
    This helps prevent delays, rework, and inefficiencies during the construction phase.
    """)
    
    # Mock sequencing chart
    st.image("https://via.placeholder.com/800x300?text=Construction+Sequencing+Diagram", caption="Construction Sequencing Diagram")
    
    # Sequencing challenges
    st.markdown("#### Identified Sequencing Challenges")
    
    sequencing_items = [
        {"id": "SQ-01", "description": "Tower crane installation conflicts with early site work", "impact": "Moderate", "mitigation": "Reorganize site preparation sequence to accommodate crane base ahead of other work", "status": "Resolved"},
        {"id": "SQ-02", "description": "MEP rough-in schedule conflicts with exterior wall installation", "impact": "Significant", "mitigation": "Revise exterior wall sequence to allow for earlier MEP rough-in", "status": "In Progress"},
        {"id": "SQ-03", "description": "Elevator installation requires earlier core completion", "impact": "Moderate", "mitigation": "Accelerate core construction by two weeks", "status": "Resolved"},
        {"id": "SQ-04", "description": "Parking garage construction blocks site access for tower foundation", "impact": "Significant", "mitigation": "Revise construction phasing to complete tower foundation before garage", "status": "Open"},
        {"id": "SQ-05", "description": "Curtain wall installation requires completed roof for weather protection", "impact": "Minor", "mitigation": "Install temporary weather protection at top floors", "status": "Resolved"}
    ]
    
    # Create DataFrame
    df_sequencing = pd.DataFrame(sequencing_items)
    
    # Display with styling
    st.dataframe(
        df_sequencing,
        column_config={
            "id": st.column_config.TextColumn("ID", width="small"),
            "description": st.column_config.TextColumn("Description", width="large"),
            "impact": st.column_config.TextColumn("Schedule Impact", width="small"),
            "mitigation": st.column_config.TextColumn("Mitigation Strategy", width="large"),
            "status": st.column_config.TextColumn("Status", width="small")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Phase planning
    st.markdown("#### Construction Phase Planning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Critical Milestone Dependencies")
        
        dependencies = [
            {"milestone": "Foundation Complete", "dependent_on": "Site Excavation, Utilities Relocation"},
            {"milestone": "Structure to Level 5", "dependent_on": "Foundation Complete, Tower Crane Installation"},
            {"milestone": "Building Enclosure", "dependent_on": "Structure Complete, MEP Risers"},
            {"milestone": "Interior Finishes", "dependent_on": "Building Enclosure, MEP Rough-In"},
            {"milestone": "Commissioning", "dependent_on": "Interior Finishes, MEP Systems Complete"}
        ]
        
        for dep in dependencies:
            st.markdown(f"""
            <div style="padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px; margin-bottom: 10px;">
                <div style="font-weight: 500;">{dep["milestone"]}</div>
                <div style="font-size: 14px;">Dependent on: {dep["dependent_on"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("##### Trade Stacking Analysis")
        
        # Create data for chart
        trade_data = pd.DataFrame({
            "Month": [f"Month {i}" for i in range(1, 13)],
            "Earthwork": [8, 6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Concrete": [0, 4, 10, 12, 10, 8, 4, 0, 0, 0, 0, 0],
            "Steel": [0, 0, 5, 12, 15, 10, 5, 0, 0, 0, 0, 0],
            "MEP": [0, 0, 0, 2, 8, 15, 18, 20, 18, 15, 10, 5],
            "Enclosure": [0, 0, 0, 0, 2, 8, 15, 12, 8, 4, 0, 0],
            "Finishes": [0, 0, 0, 0, 0, 0, 5, 12, 18, 20, 15, 10]
        })
        
        # Reshape data for plotting
        plot_data = pd.DataFrame()
        for trade in ["Earthwork", "Concrete", "Steel", "MEP", "Enclosure", "Finishes"]:
            temp_df = pd.DataFrame({
                "Month": trade_data["Month"],
                "Workers": trade_data[trade],
                "Trade": trade
            })
            plot_data = pd.concat([plot_data, temp_df])
        
        # Create stacked area chart
        fig = px.area(
            plot_data, 
            x="Month", 
            y="Workers", 
            color="Trade",
            title="Trade Manpower Loading"
        )
        
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

def render_site_logistics():
    """Render the site logistics planning section"""
    st.subheader("Site Logistics Planning")
    
    # Site logistics plan
    st.markdown("#### Site Logistics Plan")
    
    # Mock site logistics plan image
    st.image("https://via.placeholder.com/800x500?text=Site+Logistics+Plan", caption="Site Logistics Plan")
    
    # Site logistics components
    logistics_items = [
        {"category": "Site Access", "elements": "Construction entrance, personnel entrance, delivery area, fire lane access", "notes": "Maintain 20' fire lane at all times", "status": "Finalized"},
        {"category": "Material Laydown", "elements": "Primary staging area, secondary staging area, prefabrication area", "notes": "Limited space requires just-in-time deliveries", "status": "Finalized"},
        {"category": "Vertical Transportation", "elements": "Tower crane location, material hoist, personnel hoist", "notes": "Tower crane must be relocated at month 8", "status": "In Review"},
        {"category": "Site Facilities", "elements": "Field office, worker facilities, parking", "notes": "Insufficient parking requires shuttle service", "status": "Finalized"},
        {"category": "Traffic Control", "elements": "Street closure plan, flaggers, delivery scheduling", "notes": "Limited delivery hours: 7am-10am", "status": "In Review"},
        {"category": "Utility Connections", "elements": "Temporary power, water, sewer", "notes": "Temporary power upgrade required for month 6", "status": "Finalized"}
    ]
    
    # Create DataFrame
    df_logistics = pd.DataFrame(logistics_items)
    
    # Display with styling
    st.dataframe(
        df_logistics,
        column_config={
            "category": st.column_config.TextColumn("Category", width="medium"),
            "elements": st.column_config.TextColumn("Elements", width="large"),
            "notes": st.column_config.TextColumn("Notes", width="large"),
            "status": st.column_config.TextColumn("Status", width="small")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Site constraints
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Site Constraints")
        
        constraints = [
            {"constraint": "Limited Site Area", "impact": "Restricted laydown area, tight access", "mitigation": "Just-in-time deliveries, offsite staging"},
            {"constraint": "Adjacent Buildings", "impact": "Limited crane swing, vibration concerns", "mitigation": "Crane anti-collision system, vibration monitoring"},
            {"constraint": "Underground Utilities", "impact": "Excavation restrictions, potential conflicts", "mitigation": "Detailed utility survey, hand excavation near utilities"},
            {"constraint": "Street Traffic", "impact": "Delivery challenges, public safety concerns", "mitigation": "Off-peak deliveries, traffic management plan"},
            {"constraint": "Noise Restrictions", "impact": "Limited working hours, productivity loss", "mitigation": "Sound barriers, quieter equipment selection"}
        ]
        
        for item in constraints:
            st.markdown(f"""
            <div style="padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px; margin-bottom: 10px;">
                <div style="font-weight: 500;">{item["constraint"]}</div>
                <div style="font-size: 14px;"><strong>Impact:</strong> {item["impact"]}</div>
                <div style="font-size: 14px;"><strong>Mitigation:</strong> {item["mitigation"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Delivery Zone Schedule")
        
        # Create data for delivery schedule
        delivery_data = pd.DataFrame({
            "Time Slot": ["7:00-8:00", "8:00-9:00", "9:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00"],
            "Monday": ["Concrete", "Steel", "MEP", "Available", "Available", "No Deliveries", "Available", "Available", "Cleanup Only"],
            "Tuesday": ["Concrete", "Steel", "MEP", "Available", "Available", "No Deliveries", "Finishes", "Available", "Cleanup Only"],
            "Wednesday": ["Concrete", "Available", "MEP", "Available", "Available", "No Deliveries", "Finishes", "Available", "Cleanup Only"],
            "Thursday": ["Concrete", "Steel", "MEP", "Available", "Available", "No Deliveries", "Finishes", "Available", "Cleanup Only"],
            "Friday": ["Concrete", "Steel", "MEP", "Available", "Available", "No Deliveries", "Available", "Available", "Cleanup Only"]
        })
        
        # Display schedule
        st.dataframe(
            delivery_data,
            column_config={
                "Time Slot": st.column_config.TextColumn("Time", width="small"),
                "Monday": st.column_config.TextColumn("Monday", width="small"),
                "Tuesday": st.column_config.TextColumn("Tuesday", width="small"),
                "Wednesday": st.column_config.TextColumn("Wednesday", width="small"),
                "Thursday": st.column_config.TextColumn("Thursday", width="small"),
                "Friday": st.column_config.TextColumn("Friday", width="small")
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Delivery management system
        st.markdown("#### Delivery Management")
        
        st.markdown("""
        The project will utilize an online delivery management system to coordinate all deliveries:
        
        - Subcontractors must schedule deliveries 48 hours in advance
        - Delivery slots are assigned based on project priorities
        - Just-in-time deliveries are coordinated with installation schedule
        - Delivery vehicles must check in at the logistics gate
        - Maximum onsite time: 1 hour per delivery
        """)

def render_system_coordination():
    """Render the system coordination section"""
    st.subheader("System Coordination")
    
    # System coordination explanation
    st.markdown("""
    System coordination review identifies and resolves conflicts between building systems
    before construction begins, reducing RFIs, change orders, and field conflicts.
    This process uses BIM coordination to detect clashes and optimize system routing.
    """)
    
    # BIM coordination
    st.markdown("#### BIM Coordination Status")
    
    # Mock BIM coordination image
    st.image("https://via.placeholder.com/800x400?text=BIM+Coordination+Model", caption="BIM Coordination Model")
    
    # Coordination zones
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Clash Groups",
            value="156",
            help="Total number of clash groups identified"
        )
    
    with col2:
        st.metric(
            label="Resolved Clashes",
            value="112",
            delta="+18",
            help="Resolved clash groups"
        )
    
    with col3:
        st.metric(
            label="Open Clashes",
            value="44",
            delta="-18",
            delta_color="inverse",
            help="Remaining clash groups to resolve"
        )
    
    # Coordination zones
    st.markdown("#### Coordination Zones")
    
    zones = [
        {"zone": "Mechanical Rooms", "status": "95% Complete", "critical_issues": 1, "next_review": "May 30, 2025"},
        {"zone": "Typical Floors (Residential)", "status": "80% Complete", "critical_issues": 2, "next_review": "May 25, 2025"},
        {"zone": "Typical Floors (Retail)", "status": "75% Complete", "critical_issues": 3, "next_review": "May 28, 2025"},
        {"zone": "Lobby & Amenity Spaces", "status": "60% Complete", "critical_issues": 5, "next_review": "June 5, 2025"},
        {"zone": "Parking Levels", "status": "40% Complete", "critical_issues": 8, "next_review": "June 10, 2025"}
    ]
    
    # Create a visual progress bar for each zone
    for zone in zones:
        percentage = int(zone["status"].split("%")[0])
        
        # Determine color based on percentage and critical issues
        if percentage >= 90:
            color = "#4CAF50"  # Green
        elif percentage >= 70:
            color = "#FF9800"  # Orange
        else:
            color = "#F44336"  # Red
            
        # Increase color intensity for critical issues
        critical_text = f"Critical Issues: {zone['critical_issues']}"
        critical_color = "#F44336" if zone["critical_issues"] > 0 else "#4CAF50"
        
        st.markdown(f"""
        <div style="padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <strong>{zone["zone"]}</strong>
                <span>Next Review: {zone["next_review"]}</span>
            </div>
            <div style="width: 100%; background-color: #f0f0f0; height: 20px; border-radius: 10px; overflow: hidden;">
                <div style="width: {percentage}%; background-color: {color}; height: 100%;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                <span>{zone["status"]}</span>
                <span style="color: {critical_color};">{critical_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Critical coordination issues
    st.markdown("#### Critical Coordination Issues")
    
    issues = [
        {"id": "CC-015", "description": "MEP conflicts in main mechanical room ceiling space", "systems": "HVAC, Plumbing, Electrical", "resolution": "Reposition main ductwork runs, lower ceiling height", "status": "In Progress"},
        {"id": "CC-023", "description": "Structural beam conflicts with HVAC main supply", "systems": "Structural, HVAC", "resolution": "Provide beam penetrations, reinforce as needed", "status": "In Progress"},
        {"id": "CC-031", "description": "Insufficient clearance for fire sprinkler mains", "systems": "Fire Protection, HVAC", "resolution": "Reroute sprinkler mains, adjust duct elevations", "status": "Open"},
        {"id": "CC-042", "description": "Electrical conduit racks conflict with plumbing", "systems": "Electrical, Plumbing", "resolution": "Reposition conduit racks, coordinate elevations", "status": "In Progress"},
        {"id": "CC-048", "description": "Ceiling plenum congestion in retail areas", "systems": "All MEP", "resolution": "Comprehensive recoordination of ceiling plenum", "status": "Open"}
    ]
    
    # Create DataFrame
    df_issues = pd.DataFrame(issues)
    
    # Display with styling
    st.dataframe(
        df_issues,
        column_config={
            "id": st.column_config.TextColumn("ID", width="small"),
            "description": st.column_config.TextColumn("Description", width="large"),
            "systems": st.column_config.TextColumn("Systems", width="medium"),
            "resolution": st.column_config.TextColumn("Resolution Approach", width="large"),
            "status": st.column_config.TextColumn("Status", width="small")
        },
        hide_index=True,
        use_container_width=True
    )

def render_risk_register():
    """Render the risk register section"""
    st.subheader("Constructability Risk Register")
    
    # Risk management explanation
    st.markdown("""
    The Constructability Risk Register identifies, assesses, and plans mitigation strategies for
    risks that could impact construction. This proactive approach helps prevent issues before
    they occur and provides contingency plans for identified risks.
    """)
    
    # Risk metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Risks",
            value="35",
            help="Total identified construction risks"
        )
    
    with col2:
        st.metric(
            label="High Priority",
            value="8",
            delta="-2",
            delta_color="inverse",
            help="High priority risks requiring immediate attention"
        )
    
    with col3:
        st.metric(
            label="Medium Priority",
            value="15",
            delta="+1",
            help="Medium priority risks to monitor"
        )
    
    with col4:
        st.metric(
            label="Low Priority",
            value="12",
            delta="+1",
            help="Low priority risks to track"
        )
    
    # Risk matrix
    st.markdown("#### Risk Assessment Matrix")
    
    # Create risk matrix data
    risk_counts = {
        ("Almost Certain", "Severe"): 1,
        ("Almost Certain", "Major"): 2,
        ("Almost Certain", "Moderate"): 1,
        ("Almost Certain", "Minor"): 0,
        ("Almost Certain", "Negligible"): 0,
        
        ("Likely", "Severe"): 1,
        ("Likely", "Major"): 2,
        ("Likely", "Moderate"): 3,
        ("Likely", "Minor"): 1,
        ("Likely", "Negligible"): 0,
        
        ("Possible", "Severe"): 0,
        ("Possible", "Major"): 2,
        ("Possible", "Moderate"): 4,
        ("Possible", "Minor"): 2,
        ("Possible", "Negligible"): 1,
        
        ("Unlikely", "Severe"): 0,
        ("Unlikely", "Major"): 1,
        ("Unlikely", "Moderate"): 2,
        ("Unlikely", "Minor"): 3,
        ("Unlikely", "Negligible"): 2,
        
        ("Rare", "Severe"): 0,
        ("Rare", "Major"): 0,
        ("Rare", "Moderate"): 1,
        ("Rare", "Minor"): 3,
        ("Rare", "Negligible"): 2
    }
    
    # Flatten the dictionary for DataFrame
    matrix_data = []
    for (likelihood, impact), count in risk_counts.items():
        matrix_data.append({"Likelihood": likelihood, "Impact": impact, "Count": count})
    
    # Create DataFrame
    df_matrix = pd.DataFrame(matrix_data)
    
    # Order for categories
    likelihood_order = ["Almost Certain", "Likely", "Possible", "Unlikely", "Rare"]
    impact_order = ["Severe", "Major", "Moderate", "Minor", "Negligible"]
    
    # Create pivot table
    matrix_pivot = df_matrix.pivot(index="Likelihood", columns="Impact", values="Count")
    
    # Reorder columns and index
    matrix_pivot = matrix_pivot.reindex(index=likelihood_order, columns=impact_order)
    
    # Fill NA with 0
    matrix_pivot = matrix_pivot.fillna(0).astype(int)
    
    # Display as heatmap
    fig = px.imshow(
        matrix_pivot,
        color_continuous_scale=["#4CAF50", "#FFEB3B", "#FF9800", "#F44336", "#B71C1C"],
        labels=dict(x="Impact", y="Likelihood", color="Count"),
        title="Risk Assessment Matrix"
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk register table
    st.markdown("#### Top Priority Risks")
    
    risks = [
        {"id": "R-005", "description": "Unexpected soil conditions requiring foundation redesign", "category": "Geotechnical", "likelihood": "Possible", "impact": "Major", "priority": "High", "mitigation": "Additional soil borings, foundation design contingency", "owner": "John D."},
        {"id": "R-008", "description": "Tower crane interference with adjacent building operations", "category": "Site Logistics", "likelihood": "Likely", "impact": "Major", "priority": "High", "mitigation": "Coordinate swing restrictions, develop communication protocol", "owner": "Mike R."},
        {"id": "R-012", "description": "MEP system coordination conflicts causing field rework", "category": "Systems Coordination", "likelihood": "Almost Certain", "impact": "Major", "priority": "High", "mitigation": "Enhanced BIM coordination, prefabrication of complex assemblies", "owner": "Sarah T."},
        {"id": "R-017", "description": "Curtain wall fabrication delays impacting enclosure schedule", "category": "Procurement", "likelihood": "Likely", "impact": "Major", "priority": "High", "mitigation": "Early procurement, factory visits, alternate suppliers", "owner": "Lisa K."},
        {"id": "R-023", "description": "Labor shortage for critical trades", "category": "Resources", "likelihood": "Possible", "impact": "Major", "priority": "High", "mitigation": "Early subcontractor outreach, alternative staffing plans", "owner": "Robert M."}
    ]
    
    # Create DataFrame
    df_risks = pd.DataFrame(risks)
    
    # Display with styling
    st.dataframe(
        df_risks,
        column_config={
            "id": st.column_config.TextColumn("ID", width="small"),
            "description": st.column_config.TextColumn("Description", width="large"),
            "category": st.column_config.TextColumn("Category", width="medium"),
            "likelihood": st.column_config.TextColumn("Likelihood", width="small"),
            "impact": st.column_config.TextColumn("Impact", width="small"),
            "priority": st.column_config.TextColumn("Priority", width="small"),
            "mitigation": st.column_config.TextColumn("Mitigation Strategy", width="large"),
            "owner": st.column_config.TextColumn("Owner", width="small")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Add new risk
    with st.expander("Add New Risk"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Risk Description", placeholder="Enter risk description...")
            st.selectbox("Risk Category", ["Geotechnical", "Structural", "MEP Systems", "Enclosure", "Finishes", "Site Logistics", "Procurement", "Resources", "Regulatory", "Weather", "Other"])
            st.text_area("Mitigation Strategy", placeholder="Describe mitigation approach...")
        
        with col2:
            st.selectbox("Likelihood", ["Almost Certain", "Likely", "Possible", "Unlikely", "Rare"])
            st.selectbox("Impact", ["Severe", "Major", "Moderate", "Minor", "Negligible"])
            st.selectbox("Priority", ["High", "Medium", "Low"])
            st.selectbox("Risk Owner", ["John D.", "Mike R.", "Sarah T.", "Lisa K.", "Robert M."])
        
        st.button("Add Risk", type="primary")