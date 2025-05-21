"""
Subcontract components for the Contracts module.

This module provides the UI components for subcontract management including:
- Subcontract list view
- Subcontract details view
- Subcontract form (add/edit)
- Subcontract analysis view
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Sample data for demonstration
def generate_sample_subcontracts():
    """Generate sample subcontract data for demonstration"""
    return [
        {
            "ID": "SC-2025-001",
            "Title": "Structural Steel Installation",
            "Vendor": "Steel City LLC",
            "Trade": "Structural Steel",
            "Value": 2100000,
            "Start_Date": "2025-01-20",
            "End_Date": "2025-05-15",
            "Status": "Active"
        },
        {
            "ID": "SC-2025-002",
            "Title": "Electrical Systems - Main Building",
            "Vendor": "Modern Electrical Co.",
            "Trade": "Electrical",
            "Value": 1750000,
            "Start_Date": "2025-03-01",
            "End_Date": "2025-11-30",
            "Status": "Active"
        },
        {
            "ID": "SC-2025-003",
            "Title": "Plumbing Installation",
            "Vendor": "Quality Plumbing Services",
            "Trade": "Plumbing",
            "Value": 980000,
            "Start_Date": "2025-03-15",
            "End_Date": "2025-08-30",
            "Status": "Active"
        },
        {
            "ID": "SC-2025-004",
            "Title": "HVAC Systems Installation",
            "Vendor": "Premier HVAC Systems",
            "Trade": "HVAC",
            "Value": 1240000,
            "Start_Date": "2025-03-20",
            "End_Date": "2025-10-15",
            "Status": "Active"
        },
        {
            "ID": "SC-2025-005",
            "Title": "Foundation and Concrete Work",
            "Vendor": "Solid Foundations LLC",
            "Trade": "Concrete",
            "Value": 1550000,
            "Start_Date": "2025-01-05",
            "End_Date": "2025-04-30",
            "Status": "Complete"
        },
        {
            "ID": "SC-2025-006",
            "Title": "Interior Drywall and Framing",
            "Vendor": "Interior Specialists Inc.",
            "Trade": "Drywall",
            "Value": 875000,
            "Start_Date": "2025-05-01",
            "End_Date": "2025-09-30",
            "Status": "Pending"
        },
        {
            "ID": "SC-2025-007",
            "Title": "Exterior Landscaping",
            "Vendor": "Urban Landscape Design",
            "Trade": "Landscaping",
            "Value": 420000,
            "Start_Date": "2025-08-15",
            "End_Date": "2025-10-30",
            "Status": "Pending"
        }
    ]

def render_subcontract_list():
    """Render the subcontracts list view with filtering and sorting"""
    st.subheader("Subcontracts")
    
    # Get sample data
    subcontracts = generate_sample_subcontracts()
    
    with st.expander("Filters", expanded=True):
        # Create columns for the filters
        col1, col2 = st.columns(2)
        
        with col1:
            # Trade filter
            trades = ["All Trades"] + list(set(c["Trade"] for c in subcontracts))
            selected_trade = st.selectbox("Trade", trades, key="subcontract_trade_filter")
            
            # Status filter
            statuses = ["All Statuses"] + list(set(c["Status"] for c in subcontracts))
            selected_status = st.selectbox("Status", statuses, key="subcontract_status_filter")
        
        with col2:
            # Value range filter
            min_value = min(c["Value"] for c in subcontracts)
            max_value = max(c["Value"] for c in subcontracts)
            value_range = st.slider(
                "Subcontract Value Range ($)",
                min_value=int(min_value),
                max_value=int(max_value),
                value=(int(min_value), int(max_value)),
                step=50000,
                format="$%d"
            )
            
            # Search field
            search_term = st.text_input("Search", key="subcontract_search", placeholder="Search subcontracts...")
    
    # Filter the data based on selections
    filtered_subcontracts = subcontracts
    
    if selected_trade != "All Trades":
        filtered_subcontracts = [c for c in filtered_subcontracts if c["Trade"] == selected_trade]
    
    if selected_status != "All Statuses":
        filtered_subcontracts = [c for c in filtered_subcontracts if c["Status"] == selected_status]
    
    filtered_subcontracts = [c for c in filtered_subcontracts if c["Value"] >= value_range[0] and c["Value"] <= value_range[1]]
    
    if search_term:
        filtered_subcontracts = [c for c in filtered_subcontracts if 
                               search_term.lower() in c["Title"].lower() or 
                               search_term.lower() in c["ID"].lower() or
                               search_term.lower() in c["Vendor"].lower()]

    # Add button
    if st.button("➕ Add Subcontract", use_container_width=True):
        st.session_state.subcontract_view = "add"
        st.rerun()
    
    # Check if we have any results
    if not filtered_subcontracts:
        st.info("No subcontracts match your filters.")
        return
    
    # Show item count
    st.caption(f"Showing {len(filtered_subcontracts)} subcontracts")
    
    # Display the filtered subcontracts
    for subcontract in filtered_subcontracts:
        # Create a container for each subcontract
        subcontract_container = st.container()
        
        with subcontract_container:
            # Add a subtle divider between subcontracts
            st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
            
            # Create a row with columns for the subcontract data and action buttons
            row_container = st.container()
            
            # Create a more balanced row layout with condensed columns
            col1, col2, col3, col4, col_actions = row_container.columns([0.8, 3, 2, 1.5, 0.7])
            
            with col1:
                st.write(f"**{subcontract['ID']}**")
                st.caption(f"{subcontract['Trade']}")
            
            with col2:
                st.write(f"📄 **{subcontract['Title']}**")
                st.caption(f"Vendor: {subcontract['Vendor']}")
            
            with col3:
                # Combine date information into one block
                st.markdown(f"<small><b>Period:</b><br>{subcontract['Start_Date']} to {subcontract['End_Date']}</small>", unsafe_allow_html=True)
            
            with col4:
                # Contract value and status
                status_color = {
                    "Active": "green",
                    "Pending": "orange",
                    "Complete": "blue",
                    "Terminated": "red"
                }.get(subcontract['Status'], "grey")
                
                # Value and status in one block
                st.markdown(f"""
                <b>${subcontract['Value']:,}</b><br>
                <span style='color:{status_color};'><small>{subcontract['Status']}</small></span>
                """, unsafe_allow_html=True)
            
            # Action buttons in a single column
            with col_actions:
                # Create two buttons side by side in the actions column
                action_btn_cols = st.columns(2)
                
                # View button
                with action_btn_cols[0]:
                    if st.button("👁️", key=f"view_{subcontract['ID']}", help="View subcontract details"):
                        # Store subcontract details in session state
                        st.session_state.selected_subcontract_id = subcontract['ID'] 
                        st.session_state.selected_subcontract_data = subcontract
                        # Set view mode
                        st.session_state["subcontract_view"] = "view"
                        # Force refresh
                        st.rerun()
                
                # Edit button
                with action_btn_cols[1]:
                    if st.button("✏️", key=f"edit_{subcontract['ID']}", help="Edit subcontract"):
                        # Store subcontract data for editing
                        st.session_state.edit_subcontract_id = subcontract['ID']
                        st.session_state.edit_subcontract_data = subcontract
                        # Set edit mode 
                        st.session_state["subcontract_view"] = "edit"
                        # Force refresh
                        st.rerun()

def render_subcontract_details():
    """Render the subcontract details view (single record view)"""
    st.subheader("Subcontract Details")
    
    # Ensure we have a selected subcontract
    if not st.session_state.get("selected_subcontract_id"):
        st.error("No subcontract selected. Please select a subcontract from the list.")
        # Return to list view
        st.session_state.subcontract_view = "list"
        st.rerun()
        return
    
    # Get the selected subcontract data
    subcontract = st.session_state.get("selected_subcontract_data", None)
    
    if not subcontract:
        # If somehow we have an ID but no data, try to find it
        subcontracts = generate_sample_subcontracts()
        subcontract = next((c for c in subcontracts if c["ID"] == st.session_state.selected_subcontract_id), None)
        
        if not subcontract:
            st.error(f"Subcontract with ID {st.session_state.selected_subcontract_id} not found.")
            # Return to list view
            st.session_state.subcontract_view = "list"
            st.rerun()
            return
    
    # Display subcontract details
    with st.container():
        # Style for subcontract details
        st.markdown("""
        <style>
            .subcontract-details {
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 15px;
            }
            .subcontract-header {
                margin-bottom: 20px;
            }
            .subcontract-section {
                margin-top: 15px;
                margin-bottom: 15px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Start subcontract details container
        st.markdown('<div class="subcontract-details">', unsafe_allow_html=True)
        
        # Header section
        st.markdown(f'<div class="subcontract-header">', unsafe_allow_html=True)
        st.markdown(f"# {subcontract['Title']}")
        st.markdown(f"#### ID: {subcontract['ID']} | Trade: {subcontract['Trade']} | Status: {subcontract['Status']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Subcontract information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'<div class="subcontract-section">', unsafe_allow_html=True)
            st.markdown("### Subcontract Information")
            st.markdown(f"**Vendor:** {subcontract['Vendor']}")
            st.markdown(f"**Subcontract Value:** ${subcontract['Value']:,}")
            st.markdown(f"**Trade:** {subcontract['Trade']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="subcontract-section">', unsafe_allow_html=True)
            st.markdown("### Timeline")
            st.markdown(f"**Start Date:** {subcontract['Start_Date']}")
            st.markdown(f"**End Date:** {subcontract['End_Date']}")
            
            # Calculate duration and remaining time
            start_date = datetime.strptime(subcontract['Start_Date'], "%Y-%m-%d")
            end_date = datetime.strptime(subcontract['End_Date'], "%Y-%m-%d")
            total_days = (end_date - start_date).days
            days_remaining = (end_date - datetime.now()).days
            
            if days_remaining > 0:
                st.markdown(f"**Duration:** {total_days} days")
                st.markdown(f"**Remaining:** {days_remaining} days")
                
                # Progress bar
                progress = (total_days - days_remaining) / total_days
                st.progress(progress)
            else:
                st.markdown(f"**Duration:** {total_days} days")
                st.markdown(f"**Status:** Complete")
                st.progress(1.0)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Payment status (placeholder)
        st.markdown(f'<div class="subcontract-section">', unsafe_allow_html=True)
        st.markdown("### Payment Status")
        
        # Generate some random payment data
        total_value = subcontract['Value']
        paid_to_date = round(total_value * random.uniform(0.2, 0.8)) if subcontract['Status'] != 'Pending' else 0
        remaining = total_value - paid_to_date
        
        payment_col1, payment_col2 = st.columns(2)
        
        with payment_col1:
            st.markdown(f"**Total Value:** ${total_value:,}")
            st.markdown(f"**Paid to Date:** ${paid_to_date:,}")
            st.markdown(f"**Remaining:** ${remaining:,}")
        
        with payment_col2:
            # Payment progress
            payment_progress = paid_to_date / total_value if total_value > 0 else 0
            st.markdown(f"**Payment Progress:** {payment_progress:.1%}")
            st.progress(payment_progress)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Recent submittals (placeholder)
        st.markdown(f'<div class="subcontract-section">', unsafe_allow_html=True)
        st.markdown("### Recent Submittals")
        
        # Generate some random submittals
        submittals = []
        if subcontract['Status'] != 'Pending':
            num_submittals = random.randint(1, 4)
            for i in range(num_submittals):
                submittals.append({
                    "Date": (datetime.now() - timedelta(days=random.randint(10, 90))).strftime("%Y-%m-%d"),
                    "Description": random.choice([
                        "Product Data Sheets",
                        "Shop Drawings",
                        "Material Samples",
                        "Quality Certificates",
                        "Installation Methods"
                    ]),
                    "Status": random.choice(["Approved", "Approved as Noted", "Revise and Resubmit", "Rejected"])
                })
        
        if submittals:
            # Create a DataFrame for display
            submittals_df = pd.DataFrame(submittals)
            st.dataframe(submittals_df, use_container_width=True)
        else:
            st.info("No submittals have been received for this subcontract.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Actions
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✏️ Edit Subcontract", use_container_width=True):
                st.session_state.edit_subcontract_id = subcontract['ID']
                st.session_state.edit_subcontract_data = subcontract
                st.session_state.subcontract_view = "edit"
                st.rerun()
        
        with col2:
            if st.button("📊 View Analysis", use_container_width=True):
                st.session_state.subcontract_view = "analysis"
                st.rerun()
        
        # End the subcontract details container
        st.markdown('</div>', unsafe_allow_html=True)


def render_subcontract_form(is_edit=False):
    """Render the subcontract creation/edit form"""
    if is_edit:
        st.subheader("Edit Subcontract")
        # Ensure we have a subcontract to edit
        if not st.session_state.get("edit_subcontract_id"):
            st.error("No subcontract selected for editing. Please select a subcontract from the list.")
            # Return to list view
            st.session_state.subcontract_view = "list"
            st.rerun()
            return
        
        # Get the subcontract data for editing
        subcontract = st.session_state.get("edit_subcontract_data", {})
    else:
        st.subheader("Add New Subcontract")
        # Initialize empty subcontract for new entries
        subcontract = {
            "ID": f"SC-{datetime.now().year}-{random.randint(100, 999)}",
            "Title": "",
            "Vendor": "",
            "Trade": "",
            "Value": 0,
            "Start_Date": datetime.now().strftime("%Y-%m-%d"),
            "End_Date": (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d"),
            "Status": "Draft"
        }
    
    # Create the form
    with st.form(key="subcontract_form"):
        # Basic information
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Subcontract Title *", value=subcontract.get("Title", ""))
            
            # Trade dropdown
            trade_options = ["Structural Steel", "Electrical", "Plumbing", "HVAC", "Concrete", 
                            "Drywall", "Landscaping", "Roofing", "Masonry", "Painting", "Other"]
            selected_trade = st.selectbox(
                "Trade *", 
                trade_options, 
                index=trade_options.index(subcontract.get("Trade")) if subcontract.get("Trade") in trade_options else 0
            )
        
        with col2:
            # For display only
            if is_edit:
                st.text_input("Subcontract ID", value=subcontract.get("ID", ""), disabled=True)
            
            vendor = st.text_input("Vendor Name *", value=subcontract.get("Vendor", ""))
        
        # Financial information
        st.subheader("Financial Information")
        col1, col2 = st.columns(2)
        
        with col1:
            value = st.number_input(
                "Subcontract Value ($) *", 
                min_value=0, 
                value=int(subcontract.get("Value", 0)),
                step=10000
            )
            
            retainage = st.number_input(
                "Retainage Percentage (%)",
                min_value=0.0,
                max_value=20.0,
                value=float(subcontract.get("Retainage", 10.0)),
                step=0.5
            )
        
        with col2:
            # Status dropdown
            status_options = ["Draft", "Pending", "Active", "Complete", "Terminated"]
            selected_status = st.selectbox(
                "Status *",
                status_options,
                index=status_options.index(subcontract.get("Status")) if subcontract.get("Status") in status_options else 0
            )
            
            # Payment terms
            payment_terms = st.selectbox(
                "Payment Terms",
                ["Net 30", "Net 60", "Net 90", "Monthly", "Progress Based", "Custom"],
                index=0
            )
        
        # Timeline
        st.subheader("Timeline")
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input(
                "Start Date *",
                value=datetime.strptime(subcontract.get("Start_Date", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
            )
        
        with col2:
            end_date = st.date_input(
                "End Date *",
                value=datetime.strptime(subcontract.get("End_Date", (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d")), "%Y-%m-%d")
            )
        
        # Scope of Work
        scope = st.text_area("Scope of Work", value=subcontract.get("Scope", ""), height=150)
        
        # Notes (optional)
        notes = st.text_area("Notes", value=subcontract.get("Notes", ""), height=100)
        
        # Submit buttons
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button(
                "Save Subcontract" if is_edit else "Create Subcontract",
                use_container_width=True
            )
        
        with col2:
            cancel_button = st.form_submit_button(
                "Cancel",
                use_container_width=True
            )
    
    # Handle form submission
    if submit_button:
        # Validate required fields
        if not title:
            st.error("Please enter a subcontract title.")
            return
        
        if not vendor:
            st.error("Please enter a vendor name.")
            return
            
        # In a real app, this would save to database
        if is_edit:
            st.success(f"Subcontract '{title}' updated successfully!")
        else:
            st.success(f"Subcontract '{title}' created successfully!")
        
        # Return to list view
        st.session_state.subcontract_view = "list"
        st.rerun()
    
    if cancel_button:
        # Return to previous view
        st.session_state.subcontract_view = "list"
        st.rerun()


def render_subcontract_analysis():
    """Render the subcontract analysis view with charts and metrics"""
    st.subheader("Subcontract Analysis")
    
    # Get sample data
    subcontracts = generate_sample_subcontracts()
    
    # Calculate summary metrics
    total_value = sum(c["Value"] for c in subcontracts)
    active_value = sum(c["Value"] for c in subcontracts if c["Status"] == "Active")
    pending_value = sum(c["Value"] for c in subcontracts if c["Status"] == "Pending")
    complete_value = sum(c["Value"] for c in subcontracts if c["Status"] == "Complete")
    
    # Summary metrics
    st.subheader("Subcontract Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Subcontract Value", f"${total_value:,.0f}")
    
    with col2:
        active_percent = (active_value / total_value) * 100 if total_value > 0 else 0
        st.metric("Active", f"${active_value:,.0f}", f"{active_percent:.1f}% of total")
    
    with col3:
        pending_percent = (pending_value / total_value) * 100 if total_value > 0 else 0
        st.metric("Pending", f"${pending_value:,.0f}", f"{pending_percent:.1f}% of total")
    
    with col4:
        complete_percent = (complete_value / total_value) * 100 if total_value > 0 else 0
        st.metric("Completed", f"${complete_value:,.0f}", f"{complete_percent:.1f}% of total")
    
    # Trade Distribution Charts
    st.subheader("Subcontract Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution by trade
        trade_data = {}
        for subcontract in subcontracts:
            trade = subcontract["Trade"]
            if trade in trade_data:
                trade_data[trade] += subcontract["Value"]
            else:
                trade_data[trade] = subcontract["Value"]
        
        # Create a DataFrame for the chart
        trade_df = pd.DataFrame({
            'Trade': list(trade_data.keys()),
            'Value': list(trade_data.values())
        })
        
        st.write("#### Distribution by Trade")
        st.bar_chart(trade_df.set_index('Trade'))
    
    with col2:
        # Status distribution
        st.write("#### Distribution by Status")
        
        status_data = pd.DataFrame({
            'Status': ['Active', 'Pending', 'Complete'],
            'Value': [active_value, pending_value, complete_value]
        })
        
        st.bar_chart(status_data.set_index('Status'))
    
    # Subcontract Timeline
    st.subheader("Subcontract Timeline")
    
    # Create timeline data
    timeline_data = []
    for subcontract in subcontracts:
        start_date = datetime.strptime(subcontract["Start_Date"], "%Y-%m-%d")
        end_date = datetime.strptime(subcontract["End_Date"], "%Y-%m-%d")
        
        timeline_data.append({
            "Subcontract": subcontract["Title"],
            "Start": start_date,
            "End": end_date,
            "Value": subcontract["Value"],
            "Status": subcontract["Status"]
        })
    
    # Sort by start date
    timeline_data.sort(key=lambda x: x["Start"])
    
    # Create a DataFrame
    timeline_df = pd.DataFrame(timeline_data)
    
    # Format for display
    display_df = timeline_df.copy()
    display_df["Start"] = display_df["Start"].dt.strftime("%Y-%m-%d")
    display_df["End"] = display_df["End"].dt.strftime("%Y-%m-%d")
    display_df["Value"] = display_df["Value"].apply(lambda x: f"${x:,.0f}")
    
    # Display the table
    st.dataframe(display_df, use_container_width=True)