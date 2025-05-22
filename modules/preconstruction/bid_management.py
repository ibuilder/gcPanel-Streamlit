"""
Bid Management Module for Pre-Construction

This module provides comprehensive bid management capabilities:
- Bid package creation and management
- Contractor prequalification
- Bid solicitation and tracking
- Bid analysis and comparison
- Award recommendation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def render_bid_management():
    """Render the Bid Management dashboard"""
    st.header("Bid Management")
    
    # Create tabs for different bid management sections
    tabs = st.tabs([
        "Bid Packages", 
        "Subcontractor Prequalification", 
        "Bid Tracking", 
        "Bid Analysis",
        "Award Recommendations"
    ])
    
    # Bid Packages tab
    with tabs[0]:
        render_bid_packages()
    
    # Subcontractor Prequalification tab
    with tabs[1]:
        render_subcontractor_prequalification()
    
    # Bid Tracking tab
    with tabs[2]:
        render_bid_tracking()
    
    # Bid Analysis tab
    with tabs[3]:
        render_bid_analysis()
    
    # Award Recommendations tab
    with tabs[4]:
        render_award_recommendations()

def render_bid_packages():
    """Render the bid packages section"""
    st.subheader("Bid Packages")
    
    # Package status summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Packages",
            value="28",
            help="Total number of bid packages for this project"
        )
    
    with col2:
        st.metric(
            label="Packages Released",
            value="18",
            delta="+3",
            help="Bid packages released to subcontractors"
        )
    
    with col3:
        st.metric(
            label="Packages Awarded",
            value="12",
            help="Bid packages that have been awarded"
        )
    
    with col4:
        st.metric(
            label="Remaining",
            value="10",
            help="Bid packages yet to be released"
        )
    
    # Add new package button
    col1, col2 = st.columns([4, 1])
    with col2:
        st.button("Add New Package", type="primary")
    
    # Bid package list
    bid_packages = [
        {"id": "BP-01", "name": "Earthwork & Site Utilities", "status": "Awarded", "released": "Jan 15, 2025", "due": "Feb 15, 2025", "awarded": "Mar 1, 2025", "amount": 3250000},
        {"id": "BP-02", "name": "Concrete", "status": "Awarded", "released": "Jan 15, 2025", "due": "Feb 15, 2025", "awarded": "Mar 1, 2025", "amount": 7500000},
        {"id": "BP-03", "name": "Structural Steel", "status": "Awarded", "released": "Feb 1, 2025", "due": "Mar 1, 2025", "awarded": "Mar 15, 2025", "amount": 4800000},
        {"id": "BP-04", "name": "Masonry", "status": "Awarded", "released": "Feb 1, 2025", "due": "Mar 1, 2025", "awarded": "Mar 15, 2025", "amount": 1250000},
        {"id": "BP-05", "name": "Waterproofing & Roofing", "status": "Awarded", "released": "Feb 15, 2025", "due": "Mar 15, 2025", "awarded": "Apr 1, 2025", "amount": 1850000},
        {"id": "BP-06", "name": "Exterior Cladding", "status": "Awarded", "released": "Feb 15, 2025", "due": "Mar 15, 2025", "awarded": "Apr 1, 2025", "amount": 3750000},
        {"id": "BP-07", "name": "Windows & Glazing", "status": "Awarded", "released": "Feb 15, 2025", "due": "Mar 15, 2025", "awarded": "Apr 1, 2025", "amount": 2900000},
        {"id": "BP-08", "name": "HVAC", "status": "Awarded", "released": "Mar 1, 2025", "due": "Apr 1, 2025", "awarded": "Apr 15, 2025", "amount": 3650000},
        {"id": "BP-09", "name": "Plumbing", "status": "Awarded", "released": "Mar 1, 2025", "due": "Apr 1, 2025", "awarded": "Apr 15, 2025", "amount": 2800000},
        {"id": "BP-10", "name": "Electrical", "status": "Awarded", "released": "Mar 1, 2025", "due": "Apr 1, 2025", "awarded": "Apr 15, 2025", "amount": 4750000},
        {"id": "BP-11", "name": "Fire Protection", "status": "Awarded", "released": "Mar 1, 2025", "due": "Apr 1, 2025", "awarded": "Apr 15, 2025", "amount": 1450000},
        {"id": "BP-12", "name": "Elevators", "status": "Awarded", "released": "Mar 15, 2025", "due": "Apr 15, 2025", "awarded": "May 1, 2025", "amount": 1250000},
        {"id": "BP-13", "name": "Drywall & Framing", "status": "Bidding", "released": "Mar 15, 2025", "due": "May 1, 2025", "awarded": "", "amount": 0},
        {"id": "BP-14", "name": "Flooring", "status": "Bidding", "released": "Apr 1, 2025", "due": "May 15, 2025", "awarded": "", "amount": 0},
        {"id": "BP-15", "name": "Painting", "status": "Bidding", "released": "Apr 1, 2025", "due": "May 15, 2025", "awarded": "", "amount": 0},
        {"id": "BP-16", "name": "Doors & Hardware", "status": "Bidding", "released": "Apr 15, 2025", "due": "May 30, 2025", "awarded": "", "amount": 0},
        {"id": "BP-17", "name": "Millwork & Casework", "status": "Bidding", "released": "Apr 15, 2025", "due": "May 30, 2025", "awarded": "", "amount": 0},
        {"id": "BP-18", "name": "Landscaping", "status": "Released", "released": "May 1, 2025", "due": "Jun 15, 2025", "awarded": "", "amount": 0},
        {"id": "BP-19", "name": "Kitchen Equipment", "status": "Pending", "released": "", "due": "", "awarded": "", "amount": 0},
        {"id": "BP-20", "name": "Signage", "status": "Pending", "released": "", "due": "", "awarded": "", "amount": 0}
    ]
    
    # Create DataFrame
    df_packages = pd.DataFrame(bid_packages)
    
    # Format amount column
    df_packages["Contract Amount"] = df_packages["amount"].apply(lambda x: f"${x:,.0f}" if x > 0 else "-")
    
    # Status-based styling
    def highlight_status(status):
        if status == "Awarded":
            return "background-color: #d1e7dd; color: #0f5132"
        elif status == "Bidding":
            return "background-color: #cfe2ff; color: #084298"
        elif status == "Released":
            return "background-color: #fff3cd; color: #664d03"
        else:
            return "background-color: #f8f9fa; color: #6c757d"
    
    # Convert to styleable dataframe
    df_styled = pd.DataFrame()
    df_styled["Package ID"] = df_packages["id"]
    df_styled["Package Name"] = df_packages["name"]
    df_styled["Status"] = df_packages["status"].apply(lambda x: f"{x}")
    df_styled["Released Date"] = df_packages["released"]
    df_styled["Due Date"] = df_packages["due"]
    df_styled["Award Date"] = df_packages["awarded"]
    df_styled["Contract Amount"] = df_packages["Contract Amount"]
    
    # Display dataframe with styling
    st.dataframe(
        df_styled,
        column_config={
            "Package ID": st.column_config.TextColumn("Package ID", width="small"),
            "Package Name": st.column_config.TextColumn("Package Name", width="medium"),
            "Status": st.column_config.TextColumn("Status", width="small"),
            "Released Date": st.column_config.TextColumn("Released", width="small"),
            "Due Date": st.column_config.TextColumn("Due", width="small"),
            "Award Date": st.column_config.TextColumn("Awarded", width="small"),
            "Contract Amount": st.column_config.TextColumn("Amount", width="small"),
        },
        hide_index=True,
        use_container_width=True,
    )
    
    # Package details
    with st.expander("Package Details View"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Select Package", [f"{pkg['id']} - {pkg['name']}" for pkg in bid_packages])
            
            st.markdown("#### Package Information")
            st.text_input("Package Name", value="Earthwork & Site Utilities")
            st.text_input("Package ID", value="BP-01")
            st.text_area("Scope of Work", value="Site preparation, excavation, grading, underground utilities installation, storm drainage systems, and site concrete work.")
            
            st.markdown("#### Schedule")
            col3, col4 = st.columns(2)
            with col3:
                st.date_input("Release Date", value=datetime(2025, 1, 15))
                st.date_input("Due Date", value=datetime(2025, 2, 15))
            with col4:
                st.date_input("Award Date", value=datetime(2025, 3, 1))
                st.selectbox("Status", ["Awarded", "Bidding", "Released", "Pending"])
        
        with col2:
            st.markdown("#### Bidders")
            st.dataframe(
                pd.DataFrame({
                    "Company": ["ABC Excavation", "Highland Contractors", "Metro Utilities", "Urban Excavators"],
                    "Status": ["Invited", "Invited", "Invited", "Invited"],
                    "Bid Amount": ["$3,250,000", "$3,450,000", "$3,380,000", "$3,520,000"]
                }),
                hide_index=True,
                use_container_width=True
            )
            
            st.markdown("#### Documents")
            st.checkbox("Specifications", value=True)
            st.checkbox("Drawings", value=True)
            st.checkbox("Addenda", value=True)
            st.checkbox("Bid Form", value=True)
            
            st.markdown("#### Notes")
            st.text_area("Package Notes", value="- Pre-bid meeting: Jan 25, 2025\n- Questions due: Feb 1, 2025\n- Early mobilization required")

def render_subcontractor_prequalification():
    """Render the subcontractor prequalification section"""
    st.subheader("Subcontractor Prequalification")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Prequalification status metrics
        status_col1, status_col2, status_col3, status_col4 = st.columns(4)
        
        with status_col1:
            st.metric(
                label="Total Subcontractors",
                value="96",
                delta="+8",
                delta_color="normal"
            )
        
        with status_col2:
            st.metric(
                label="Prequalified",
                value="72",
                delta="+5",
                delta_color="normal"
            )
        
        with status_col3:
            st.metric(
                label="In Review",
                value="12",
                delta="+2",
                delta_color="normal"
            )
        
        with status_col4:
            st.metric(
                label="Rejected",
                value="12",
                delta="+1",
                delta_color="normal"
            )
        
        # Subcontractor search and filter
        search_col1, search_col2, search_col3 = st.columns([2, 1, 1])
        
        with search_col1:
            st.text_input("Search Subcontractors", placeholder="Enter subcontractor name...")
        
        with search_col2:
            st.selectbox("Filter by Trade", ["All Trades", "Earthwork", "Concrete", "Steel", "Masonry", "Carpentry", "Roofing", "Plumbing", "HVAC", "Electrical"])
        
        with search_col3:
            st.selectbox("Status", ["All Status", "Prequalified", "In Review", "Rejected"])
        
        # Subcontractor list
        subcontractors = [
            {"company": "ABC Excavation", "trade": "Earthwork", "status": "Prequalified", "bonding": "$10M", "experience": "15 years", "safety": "Excellent"},
            {"company": "Highland Concrete", "trade": "Concrete", "status": "Prequalified", "bonding": "$25M", "experience": "22 years", "safety": "Excellent"},
            {"company": "Structural Steel Inc", "trade": "Steel", "status": "Prequalified", "bonding": "$20M", "experience": "18 years", "safety": "Good"},
            {"company": "Mason Brothers", "trade": "Masonry", "status": "Prequalified", "bonding": "$8M", "experience": "25 years", "safety": "Excellent"},
            {"company": "Elite Roofing", "trade": "Roofing", "status": "In Review", "bonding": "$5M", "experience": "12 years", "safety": "Good"},
            {"company": "Highland Drywall", "trade": "Carpentry", "status": "Prequalified", "bonding": "$7M", "experience": "10 years", "safety": "Good"},
            {"company": "Metro Mechanical", "trade": "HVAC", "status": "Prequalified", "bonding": "$15M", "experience": "20 years", "safety": "Excellent"},
            {"company": "Precision Plumbing", "trade": "Plumbing", "status": "Prequalified", "bonding": "$12M", "experience": "16 years", "safety": "Good"},
            {"company": "Power City Electric", "trade": "Electrical", "status": "Prequalified", "bonding": "$18M", "experience": "25 years", "safety": "Excellent"},
            {"company": "Urban Interiors", "trade": "Carpentry", "status": "Rejected", "bonding": "$3M", "experience": "5 years", "safety": "Poor"}
        ]
        
        # Create DataFrame
        df_subs = pd.DataFrame(subcontractors)
        
        # Display with styling
        st.dataframe(
            df_subs,
            column_config={
                "company": st.column_config.TextColumn("Company Name", width="medium"),
                "trade": st.column_config.TextColumn("Trade", width="small"),
                "status": st.column_config.TextColumn("Status", width="small"),
                "bonding": st.column_config.TextColumn("Bonding Capacity", width="small"),
                "experience": st.column_config.TextColumn("Experience", width="small"),
                "safety": st.column_config.TextColumn("Safety Rating", width="small")
            },
            hide_index=True,
            use_container_width=True
        )
    
    with col2:
        # Prequalification form
        st.markdown("#### Prequalification Form")
        
        with st.form("prequalification_form"):
            st.text_input("Company Name", placeholder="Enter company name")
            st.selectbox("Trade Category", ["Earthwork", "Concrete", "Steel", "Masonry", "Carpentry", "Roofing", "Plumbing", "HVAC", "Electrical"])
            st.text_input("Contact Name", placeholder="Primary contact name")
            st.text_input("Email", placeholder="Email address")
            st.text_input("Phone", placeholder="Phone number")
            
            st.selectbox("Years in Business", ["1-5 years", "6-10 years", "11-15 years", "16-20 years", "20+ years"])
            st.text_input("Annual Revenue", placeholder="e.g. $5,000,000")
            st.text_input("Bonding Capacity", placeholder="e.g. $10,000,000")
            st.selectbox("Safety Rating", ["Excellent", "Good", "Average", "Poor"])
            
            st.file_uploader("Upload Financial Statement", type=["pdf"])
            st.file_uploader("Upload Safety Records", type=["pdf"])
            st.file_uploader("Upload Insurance Certificate", type=["pdf"])
            
            st.form_submit_button("Submit Prequalification")
        
        # Review criteria
        with st.expander("Prequalification Criteria"):
            st.markdown("""
            #### Required Documents
            - Financial statements (past 3 years)
            - Insurance certificates
            - Safety records (EMR rating)
            - References from similar projects
            - Company history and capacity
            
            #### Review Criteria
            - Financial stability
            - Experience on similar projects
            - Safety record
            - Bonding capacity
            - Quality of work
            - References
            """)

def render_bid_tracking():
    """Render the bid tracking section"""
    st.subheader("Bid Tracking")
    
    # Package selection
    st.selectbox(
        "Select Bid Package", 
        ["BP-13: Drywall & Framing", "BP-14: Flooring", "BP-15: Painting", "BP-16: Doors & Hardware", "BP-17: Millwork & Casework", "BP-18: Landscaping"]
    )
    
    # Key dates
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Released:** Mar 15, 2025")
    
    with col2:
        st.markdown("**Pre-bid Meeting:** Apr 5, 2025")
    
    with col3:
        st.markdown("**Due:** May 1, 2025")
    
    # Bidder tracking
    st.markdown("#### Bidder Tracking")
    
    bidders = [
        {"company": "Precision Drywall Inc.", "status": "Package Received", "pre_bid": "Attended", "questions": 3, "addenda": "Yes", "bid_received": "No", "bid_amount": "-"},
        {"company": "Highland Interiors", "status": "Package Received", "pre_bid": "Attended", "questions": 5, "addenda": "Yes", "bid_received": "No", "bid_amount": "-"},
        {"company": "Quality Partition Systems", "status": "Package Received", "pre_bid": "Attended", "questions": 0, "addenda": "Yes", "bid_received": "No", "bid_amount": "-"},
        {"company": "Metro Drywall", "status": "Package Received", "pre_bid": "No Show", "questions": 0, "addenda": "Yes", "bid_received": "No", "bid_amount": "-"},
        {"company": "Framing Specialists LLC", "status": "Package Received", "pre_bid": "Attended", "questions": 2, "addenda": "Yes", "bid_received": "No", "bid_amount": "-"},
        {"company": "Advanced Interior Systems", "status": "Declined to Bid", "pre_bid": "N/A", "questions": 0, "addenda": "N/A", "bid_received": "No", "bid_amount": "-"}
    ]
    
    # Create DataFrame
    df_bidders = pd.DataFrame(bidders)
    
    # Display with styling
    st.dataframe(
        df_bidders,
        column_config={
            "company": st.column_config.TextColumn("Company", width="medium"),
            "status": st.column_config.TextColumn("Status", width="small"),
            "pre_bid": st.column_config.TextColumn("Pre-bid Meeting", width="small"),
            "questions": st.column_config.NumberColumn("Questions", width="small"),
            "addenda": st.column_config.TextColumn("Addenda", width="small"),
            "bid_received": st.column_config.TextColumn("Bid Received", width="small"),
            "bid_amount": st.column_config.TextColumn("Bid Amount", width="small")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # RFI tracking
    st.markdown("#### Bid Questions/RFIs")
    
    rfis = [
        {"id": "RFI-045", "company": "Precision Drywall Inc.", "question": "Are the shaft walls included in this scope?", "date": "Apr 10, 2025", "answered": "Yes", "answer": "Yes, shaft walls are included in this scope per specification section 09 21 16."},
        {"id": "RFI-046", "company": "Highland Interiors", "question": "What is the required fire rating for corridor walls?", "date": "Apr 12, 2025", "answered": "Yes", "answer": "Corridor walls require 1-hour fire rating per drawing A2.01."},
        {"id": "RFI-048", "company": "Highland Interiors", "question": "Are specialty ceiling systems included in this package?", "date": "Apr 12, 2025", "answered": "Yes", "answer": "Yes, all ceiling systems shown on drawings A9 series are included."},
        {"id": "RFI-052", "company": "Precision Drywall Inc.", "question": "Is mockup required for typical apartment unit?", "date": "Apr 15, 2025", "answered": "Yes", "answer": "Yes, one complete apartment unit mockup is required prior to full production."},
        {"id": "RFI-058", "company": "Framing Specialists LLC", "question": "Who is responsible for in-wall blocking?", "date": "Apr 18, 2025", "answered": "Yes", "answer": "All in-wall blocking for fixtures and accessories is part of this scope."},
        {"id": "RFI-059", "company": "Highland Interiors", "question": "What is the schedule for level 5 finish areas?", "date": "Apr 18, 2025", "answered": "No", "answer": ""}
    ]
    
    # Create DataFrame
    df_rfis = pd.DataFrame(rfis)
    
    # Display with styling
    st.dataframe(
        df_rfis,
        column_config={
            "id": st.column_config.TextColumn("RFI #", width="small"),
            "company": st.column_config.TextColumn("Company", width="medium"),
            "question": st.column_config.TextColumn("Question", width="large"),
            "date": st.column_config.TextColumn("Date", width="small"),
            "answered": st.column_config.TextColumn("Answered", width="small"),
            "answer": st.column_config.TextColumn("Response", width="large")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Addenda tracking
    with st.expander("Addenda Tracking"):
        st.markdown("#### Addenda Issued")
        
        addenda = [
            {"number": "Addendum 1", "date": "Apr 12, 2025", "description": "Updated wall types and fire rating requirements."},
            {"number": "Addendum 2", "date": "Apr 18, 2025", "description": "Revised ceiling details and added soffit requirements."}
        ]
        
        for a in addenda:
            st.markdown(f"""
            <div style="padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between;">
                    <strong>{a["number"]}</strong>
                    <span>Issued: {a["date"]}</span>
                </div>
                <div style="margin-top: 5px;">{a["description"]}</div>
            </div>
            """, unsafe_allow_html=True)

def render_bid_analysis():
    """Render the bid analysis section"""
    st.subheader("Bid Analysis")
    
    # Package selection
    st.selectbox(
        "Select Completed Bid Package", 
        ["BP-01: Earthwork & Site Utilities", "BP-02: Concrete", "BP-03: Structural Steel", "BP-04: Masonry", 
         "BP-05: Waterproofing & Roofing", "BP-06: Exterior Cladding", "BP-07: Windows & Glazing", 
         "BP-08: HVAC", "BP-09: Plumbing", "BP-10: Electrical", "BP-11: Fire Protection", "BP-12: Elevators"]
    )
    
    # Bid summary
    st.markdown("#### Bid Summary - BP-01: Earthwork & Site Utilities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Budget",
            value="$3,500,000",
            help="Original budget for this package"
        )
    
    with col2:
        st.metric(
            label="Low Bid",
            value="$3,250,000",
            delta="-$250,000",
            delta_color="inverse",
            help="Lowest received bid"
        )
    
    with col3:
        st.metric(
            label="Average Bid",
            value="$3,400,000",
            delta="-$100,000",
            delta_color="inverse",
            help="Average of all received bids"
        )
    
    # Bid comparison
    st.markdown("#### Bid Comparison")
    
    bids = [
        {"company": "ABC Excavation", "bid_amount": 3250000, "complete": "Yes", "exceptions": "None", "schedule": "Compliant", "recommended": "Yes"},
        {"company": "Highland Contractors", "bid_amount": 3450000, "complete": "Yes", "exceptions": "Rock removal", "schedule": "Compliant", "recommended": "No"},
        {"company": "Metro Utilities", "bid_amount": 3380000, "complete": "Yes", "exceptions": "None", "schedule": "Compliant", "recommended": "No"},
        {"company": "Urban Excavators", "bid_amount": 3520000, "complete": "Yes", "exceptions": "None", "schedule": "Compliant", "recommended": "No"}
    ]
    
    # Create DataFrame
    df_bids = pd.DataFrame(bids)
    
    # Format amount column
    df_bids["Bid Amount"] = df_bids["bid_amount"].apply(lambda x: f"${x:,.0f}")
    
    # Create variance column
    target = 3500000  # Budget amount
    df_bids["Variance"] = df_bids["bid_amount"].apply(lambda x: f"${(x - target):,.0f}")
    df_bids["Variance %"] = df_bids["bid_amount"].apply(lambda x: f"{(x - target) / target * 100:.1f}%")
    
    # Display with styling
    st.dataframe(
        df_bids[["company", "Bid Amount", "Variance", "Variance %", "complete", "exceptions", "schedule", "recommended"]],
        column_config={
            "company": "Contractor",
            "Bid Amount": "Bid Amount",
            "Variance": "Variance",
            "Variance %": "Variance %",
            "complete": "Complete Bid",
            "exceptions": "Exceptions",
            "schedule": "Schedule",
            "recommended": "Recommended"
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Bid comparison chart
    bid_chart_data = pd.DataFrame({
        "Contractor": [b["company"] for b in bids],
        "Amount": [b["bid_amount"] for b in bids]
    })
    
    # Add budget line
    budget_line = pd.DataFrame({
        "Contractor": bid_chart_data["Contractor"],
        "Budget": [target] * len(bid_chart_data)
    })
    
    fig = px.bar(
        bid_chart_data,
        x="Contractor",
        y="Amount",
        text_auto='.2s',
        title="Bid Comparison"
    )
    
    # Add budget line
    fig.add_trace(
        px.line(
            budget_line, 
            x="Contractor", 
            y="Budget",
            color_discrete_sequence=["red"]
        ).data[0]
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Scope comparison
    with st.expander("Detailed Scope Comparison"):
        st.markdown("#### Scope Comparison")
        
        scope_items = [
            "Site clearing and preparation",
            "Excavation and backfill",
            "Underground utilities",
            "Storm drainage system",
            "Site concrete",
            "Erosion control",
            "Dewatering",
            "Rock removal",
            "Parking lot base preparation"
        ]
        
        # Create scope comparison matrix
        scope_matrix = []
        
        for item in scope_items:
            # For this example, we'll just make ABC and Metro complete coverage
            # and others have some exceptions
            row = {
                "Scope Item": item,
                "ABC Excavation": "✓",
                "Highland Contractors": "✓" if item != "Rock removal" else "✗",
                "Metro Utilities": "✓",
                "Urban Excavators": "✓" if item != "Dewatering" else "Partial"
            }
            scope_matrix.append(row)
        
        # Create DataFrame
        df_scope = pd.DataFrame(scope_matrix)
        
        # Display with styling
        st.dataframe(
            df_scope,
            hide_index=True,
            use_container_width=True
        )

def render_award_recommendations():
    """Render the award recommendations section"""
    st.subheader("Award Recommendations")
    
    # Current recommendation
    st.markdown("#### Current Recommendation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Package:** BP-01: Earthwork & Site Utilities
        
        **Recommended Contractor:** ABC Excavation
        
        **Bid Amount:** $3,250,000
        
        **Variance from Budget:** -$250,000 (-7.1%)
        
        **Recommendation Justification:**
        ABC Excavation submitted the lowest bid with no exceptions. They have successfully completed similar work on three previous projects with our company. Their schedule compliance is excellent, and they included all specified scope items. Their safety record meets our requirements, and they have adequate bonding capacity.
        """)
    
    with col2:
        st.markdown("#### Action Required")
        
        st.radio(
            "Recommendation Decision",
            ["Approve Award", "Request Additional Information", "Reject - Rebid Package", "Negotiate Scope/Price"]
        )
        
        st.text_area("Comments")
        
        st.button("Submit Decision", type="primary")
    
    # All recommendations
    st.markdown("#### All Award Recommendations")
    
    recommendations = [
        {"package": "BP-01: Earthwork", "contractor": "ABC Excavation", "amount": "$3,250,000", "status": "Approved", "date": "Mar 1, 2025"},
        {"package": "BP-02: Concrete", "contractor": "Highland Concrete", "amount": "$7,500,000", "status": "Approved", "date": "Mar 1, 2025"},
        {"package": "BP-03: Steel", "contractor": "Midwest Steel", "amount": "$4,800,000", "status": "Approved", "date": "Mar 15, 2025"},
        {"package": "BP-04: Masonry", "contractor": "Mason Brothers", "amount": "$1,250,000", "status": "Approved", "date": "Mar 15, 2025"},
        {"package": "BP-05: Waterproofing", "contractor": "Shield Roofing", "amount": "$1,850,000", "status": "Approved", "date": "Apr 1, 2025"},
        {"package": "BP-06: Cladding", "contractor": "Exterior Systems Inc", "amount": "$3,750,000", "status": "Approved", "date": "Apr 1, 2025"},
        {"package": "BP-07: Glazing", "contractor": "Clear View Glass", "amount": "$2,900,000", "status": "Approved", "date": "Apr 1, 2025"},
        {"package": "BP-08: HVAC", "contractor": "Comfort Mechanical", "amount": "$3,650,000", "status": "Approved", "date": "Apr 15, 2025"},
        {"package": "BP-09: Plumbing", "contractor": "Precision Plumbing", "amount": "$2,800,000", "status": "Approved", "date": "Apr 15, 2025"},
        {"package": "BP-10: Electrical", "contractor": "Power Systems Inc", "amount": "$4,750,000", "status": "Approved", "date": "Apr 15, 2025"},
        {"package": "BP-11: Fire Protection", "contractor": "Guardian Fire", "amount": "$1,450,000", "status": "Approved", "date": "Apr 15, 2025"},
        {"package": "BP-12: Elevators", "contractor": "Vertical Transit", "amount": "$1,250,000", "status": "Approved", "date": "May 1, 2025"}
    ]
    
    # Create DataFrame
    df_recs = pd.DataFrame(recommendations)
    
    # Display with styling
    st.dataframe(
        df_recs,
        column_config={
            "package": "Bid Package",
            "contractor": "Contractor",
            "amount": "Contract Amount",
            "status": "Status",
            "date": "Award Date"
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Savings summary
    st.markdown("#### Budget Performance Summary")
    
    savings_data = pd.DataFrame({
        "Category": ["Earthwork", "Concrete", "Steel", "Masonry", "Waterproofing", "Cladding", 
                    "Glazing", "HVAC", "Plumbing", "Electrical", "Fire Protection", "Elevators"],
        "Budget": [3500000, 7750000, 5000000, 1200000, 2000000, 3800000, 
                  3000000, 3750000, 2750000, 4900000, 1500000, 1300000],
        "Award": [3250000, 7500000, 4800000, 1250000, 1850000, 3750000, 
                 2900000, 3650000, 2800000, 4750000, 1450000, 1250000]
    })
    
    # Calculate variance
    savings_data["Variance"] = savings_data["Award"] - savings_data["Budget"]
    savings_data["Variance %"] = savings_data["Variance"] / savings_data["Budget"] * 100
    
    # Total row
    totals = {
        "Category": "TOTAL",
        "Budget": savings_data["Budget"].sum(),
        "Award": savings_data["Award"].sum(),
        "Variance": savings_data["Variance"].sum(),
        "Variance %": savings_data["Variance"].sum() / savings_data["Budget"].sum() * 100
    }
    
    savings_data = pd.concat([savings_data, pd.DataFrame([totals])], ignore_index=True)
    
    # Format for display
    display_data = savings_data.copy()
    display_data["Budget"] = display_data["Budget"].apply(lambda x: f"${x:,.0f}")
    display_data["Award"] = display_data["Award"].apply(lambda x: f"${x:,.0f}")
    display_data["Variance"] = display_data["Variance"].apply(lambda x: f"${x:,.0f}")
    display_data["Variance %"] = display_data["Variance %"].apply(lambda x: f"{x:.1f}%")
    
    # Display with styling
    st.dataframe(
        display_data,
        hide_index=True,
        use_container_width=True
    )
    
    # Budget performance chart
    fig = px.bar(
        savings_data[:-1],  # Exclude total row
        x="Category",
        y=["Budget", "Award"],
        barmode="group",
        title="Budget vs. Award by Package",
        text_auto='.2s'
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)