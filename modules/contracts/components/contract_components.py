"""
Contract components for the Contracts module.

This module provides the UI components for contract management including:
- Contract list view
- Contract details view
- Contract form (add/edit)
- Contract analysis view
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Sample data for demonstration
def generate_sample_contracts():
    """Generate sample contract data for demonstration"""
    return [
        {
            "ID": "CT-2025-001",
            "Title": "Highland Tower Main Construction",
            "Type": "GMP",
            "Contractor": "Premier Construction Inc.",
            "Value": 15500000,
            "Start_Date": "2025-01-15",
            "End_Date": "2026-08-30",
            "Status": "Active"
        },
        {
            "ID": "CT-2025-002",
            "Title": "Electrical Systems Installation",
            "Type": "Lump Sum",
            "Contractor": "Modern Electrical Co.",
            "Value": 1750000,
            "Start_Date": "2025-02-20",
            "End_Date": "2025-11-15",
            "Status": "Active"
        },
        {
            "ID": "CT-2025-003",
            "Title": "Plumbing and HVAC Services",
            "Type": "Cost Plus",
            "Contractor": "Quality Plumbing & HVAC",
            "Value": 2220000,
            "Start_Date": "2025-03-10",
            "End_Date": "2025-12-20",
            "Status": "Active"
        },
        {
            "ID": "CT-2025-004",
            "Title": "Foundation and Concrete Work",
            "Type": "Lump Sum", 
            "Contractor": "Solid Foundations LLC",
            "Value": 3100000,
            "Start_Date": "2025-01-10",
            "End_Date": "2025-05-30",
            "Status": "Complete"
        },
        {
            "ID": "CT-2025-005",
            "Title": "Exterior Finishes and Landscaping",
            "Type": "Cost Plus",
            "Contractor": "Urban Landscape Design",
            "Value": 980000,
            "Start_Date": "2025-06-15",
            "End_Date": "2025-09-30",
            "Status": "Pending"
        }
    ]

def render_contract_list():
    """Render the contracts list view with filtering and sorting"""
    st.subheader("Contracts")
    
    # Get sample data
    contracts = generate_sample_contracts()
    
    with st.expander("Filters", expanded=True):
        # Create columns for the filters
        col1, col2 = st.columns(2)
        
        with col1:
            # Type filter
            types = ["All Types"] + list(set(c["Type"] for c in contracts))
            selected_type = st.selectbox("Type", types, key="contract_type_filter")
            
            # Status filter
            statuses = ["All Statuses"] + list(set(c["Status"] for c in contracts))
            selected_status = st.selectbox("Status", statuses, key="contract_status_filter")
        
        with col2:
            # Value range filter
            min_value = min(c["Value"] for c in contracts)
            max_value = max(c["Value"] for c in contracts)
            value_range = st.slider(
                "Contract Value Range ($)",
                min_value=min_value,
                max_value=max_value,
                value=(min_value, max_value),
                step=100000,
                format="$%d"
            )
            
            # Search field
            search_term = st.text_input("Search", key="contract_search", placeholder="Search contracts...")
    
    # Filter the data based on selections
    filtered_contracts = contracts
    
    if selected_type != "All Types":
        filtered_contracts = [c for c in filtered_contracts if c["Type"] == selected_type]
    
    if selected_status != "All Statuses":
        filtered_contracts = [c for c in filtered_contracts if c["Status"] == selected_status]
    
    filtered_contracts = [c for c in filtered_contracts if c["Value"] >= value_range[0] and c["Value"] <= value_range[1]]
    
    if search_term:
        filtered_contracts = [c for c in filtered_contracts if 
                             search_term.lower() in c["Title"].lower() or 
                             search_term.lower() in c["ID"].lower() or
                             search_term.lower() in c["Contractor"].lower()]

    # Add button
    if st.button("➕ Add Contract", use_container_width=True):
        st.session_state.contract_view = "add"
        st.rerun()
    
    # Check if we have any results
    if not filtered_contracts:
        st.info("No contracts match your filters.")
        return
    
    # Show item count
    st.caption(f"Showing {len(filtered_contracts)} contracts")
    
    # Display the filtered contracts
    for contract in filtered_contracts:
        # Create a container for each contract
        contract_container = st.container()
        
        with contract_container:
            # Add a subtle divider between contracts
            st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
            
            # Create a row with columns for the contract data and action buttons
            row_container = st.container()
            
            # Create columns for the data display with action buttons inline
            col1, col2, col3, col4, col_actions = row_container.columns([0.8, 3, 2, 1.5, 0.7])
            
            with col1:
                st.write(f"**{contract['ID']}**")
                st.caption(f"{contract['Type']}")
            
            with col2:
                st.write(f"📄 **{contract['Title']}**")
                st.caption(f"Contractor: {contract['Contractor']}")
            
            with col3:
                # Combine date information into one block
                st.markdown(f"<small><b>Period:</b><br>{contract['Start_Date']} to {contract['End_Date']}</small>", unsafe_allow_html=True)
            
            with col4:
                # Contract value and status
                status_color = {
                    "Active": "green",
                    "Pending": "orange",
                    "Complete": "blue",
                    "Terminated": "red"
                }.get(contract['Status'], "grey")
                
                # Value and status in one block
                st.markdown(f"""
                <b>${contract['Value']:,}</b><br>
                <span style='color:{status_color};'><small>{contract['Status']}</small></span>
                """, unsafe_allow_html=True)
            
            # Action buttons in a single column
            with col_actions:
                # Create two buttons side by side in the actions column
                action_btn_cols = st.columns(2)
                
                # View button
                with action_btn_cols[0]:
                    if st.button("👁️", key=f"view_{contract['ID']}", help="View contract details"):
                        # Store contract details in session state
                        st.session_state.selected_contract_id = contract['ID'] 
                        st.session_state.selected_contract_data = contract
                        # Set view mode
                        st.session_state["contract_view"] = "view"
                        # Force refresh
                        st.rerun()
                
                # Edit button
                with action_btn_cols[1]:
                    if st.button("✏️", key=f"edit_{contract['ID']}", help="Edit contract"):
                        # Store contract data for editing
                        st.session_state.edit_contract_id = contract['ID']
                        st.session_state.edit_contract_data = contract
                        # Set edit mode 
                        st.session_state["contract_view"] = "edit"
                        # Force refresh
                        st.rerun()

def render_contract_details():
    """Render the contract details view (single record view)"""
    st.subheader("Contract Details")
    
    # Ensure we have a selected contract
    if not st.session_state.get("selected_contract_id"):
        st.error("No contract selected. Please select a contract from the list.")
        # Return to list view
        st.session_state.contract_view = "list"
        st.rerun()
        return
    
    # Get the selected contract data
    contract = st.session_state.get("selected_contract_data", None)
    
    if not contract:
        # If somehow we have an ID but no data, try to find it
        contracts = generate_sample_contracts()
        contract = next((c for c in contracts if c["ID"] == st.session_state.selected_contract_id), None)
        
        if not contract:
            st.error(f"Contract with ID {st.session_state.selected_contract_id} not found.")
            # Return to list view
            st.session_state.contract_view = "list"
            st.rerun()
            return
    
    # Display contract details
    with st.container():
        # Style for contract details
        st.markdown("""
        <style>
            .contract-details {
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 15px;
            }
            .contract-header {
                margin-bottom: 20px;
            }
            .contract-section {
                margin-top: 15px;
                margin-bottom: 15px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Start contract details container
        st.markdown('<div class="contract-details">', unsafe_allow_html=True)
        
        # Header section
        st.markdown(f'<div class="contract-header">', unsafe_allow_html=True)
        st.markdown(f"# {contract['Title']}")
        st.markdown(f"#### ID: {contract['ID']} | Type: {contract['Type']} | Status: {contract['Status']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Contract information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'<div class="contract-section">', unsafe_allow_html=True)
            st.markdown("### Contract Information")
            st.markdown(f"**Contractor:** {contract['Contractor']}")
            st.markdown(f"**Contract Value:** ${contract['Value']:,}")
            st.markdown(f"**Contract Type:** {contract['Type']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="contract-section">', unsafe_allow_html=True)
            st.markdown("### Timeline")
            st.markdown(f"**Start Date:** {contract['Start_Date']}")
            st.markdown(f"**End Date:** {contract['End_Date']}")
            
            # Calculate duration and remaining time
            start_date = datetime.strptime(contract['Start_Date'], "%Y-%m-%d")
            end_date = datetime.strptime(contract['End_Date'], "%Y-%m-%d")
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
        st.markdown(f'<div class="contract-section">', unsafe_allow_html=True)
        st.markdown("### Payment Status")
        
        # Generate some random payment data
        total_value = contract['Value']
        paid_to_date = round(total_value * random.uniform(0.2, 0.8)) if contract['Status'] != 'Pending' else 0
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
        
        # Recent change orders (placeholder)
        st.markdown(f'<div class="contract-section">', unsafe_allow_html=True)
        st.markdown("### Recent Change Orders")
        
        # Generate some random change orders
        change_orders = []
        if contract['Status'] != 'Pending':
            num_changes = random.randint(1, 3)
            for i in range(num_changes):
                change_amount = round(contract['Value'] * random.uniform(0.01, 0.05))
                change_orders.append({
                    "Date": (datetime.now() - timedelta(days=random.randint(10, 90))).strftime("%Y-%m-%d"),
                    "Description": random.choice([
                        "Additional Material Requirements",
                        "Scope Change - Added Features",
                        "Timeline Extension Request",
                        "Site Condition Adjustment",
                        "Regulatory Compliance Update"
                    ]),
                    "Amount": change_amount,
                    "Status": random.choice(["Approved", "Pending", "Under Review"])
                })
        
        if change_orders:
            # Create a DataFrame for display
            change_df = pd.DataFrame(change_orders)
            # Format the amount column
            change_df["Amount"] = change_df["Amount"].apply(lambda x: f"${x:,}")
            st.dataframe(change_df, use_container_width=True)
        else:
            st.info("No change orders have been submitted for this contract.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Actions
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✏️ Edit Contract", use_container_width=True):
                st.session_state.edit_contract_id = contract['ID']
                st.session_state.edit_contract_data = contract
                st.session_state.contract_view = "edit"
                st.rerun()
        
        with col2:
            if st.button("📊 View Analysis", use_container_width=True):
                st.session_state.contract_view = "analysis"
                st.rerun()
        
        # End the contract details container
        st.markdown('</div>', unsafe_allow_html=True)


def render_contract_form(is_edit=False):
    """Render the contract creation/edit form"""
    if is_edit:
        st.subheader("Edit Contract")
        # Ensure we have a contract to edit
        if not st.session_state.get("edit_contract_id"):
            st.error("No contract selected for editing. Please select a contract from the list.")
            # Return to list view
            st.session_state.contract_view = "list"
            st.rerun()
            return
        
        # Get the contract data for editing
        contract = st.session_state.get("edit_contract_data", {})
    else:
        st.subheader("Add New Contract")
        # Initialize empty contract for new entries
        contract = {
            "ID": f"CT-{datetime.now().year}-{random.randint(100, 999)}",
            "Title": "",
            "Type": "GMP",
            "Contractor": "",
            "Value": 0,
            "Start_Date": datetime.now().strftime("%Y-%m-%d"),
            "End_Date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "Status": "Draft"
        }
    
    # Create the form
    with st.form(key="contract_form"):
        # Basic information
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Contract Title *", value=contract.get("Title", ""))
            
            # Type dropdown
            contract_types = ["GMP", "Lump Sum", "Cost Plus", "Time and Materials", "Design-Build"]
            selected_type = st.selectbox(
                "Contract Type *", 
                contract_types, 
                index=contract_types.index(contract.get("Type")) if contract.get("Type") in contract_types else 0
            )
        
        with col2:
            # For display only
            if is_edit:
                st.text_input("Contract ID", value=contract.get("ID", ""), disabled=True)
            
            contractor = st.text_input("Contractor Name *", value=contract.get("Contractor", ""))
        
        # Financial information
        st.subheader("Financial Information")
        col1, col2 = st.columns(2)
        
        with col1:
            value = st.number_input(
                "Contract Value ($) *", 
                min_value=0, 
                value=int(contract.get("Value", 0)),
                step=10000
            )
            
            retainage = st.number_input(
                "Retainage Percentage (%)",
                min_value=0.0,
                max_value=20.0,
                value=float(contract.get("Retainage", 10.0)),
                step=0.5
            )
        
        with col2:
            # Status dropdown
            status_options = ["Draft", "Pending", "Active", "Complete", "Terminated"]
            selected_status = st.selectbox(
                "Status *",
                status_options,
                index=status_options.index(contract.get("Status")) if contract.get("Status") in status_options else 0
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
                value=datetime.strptime(contract.get("Start_Date", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
            )
        
        with col2:
            end_date = st.date_input(
                "End Date *",
                value=datetime.strptime(contract.get("End_Date", (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")), "%Y-%m-%d")
            )
        
        # Scope of Work
        scope = st.text_area("Scope of Work", value=contract.get("Scope", ""), height=150)
        
        # Notes (optional)
        notes = st.text_area("Notes", value=contract.get("Notes", ""), height=100)
        
        # Submit buttons
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button(
                "Save Contract" if is_edit else "Create Contract",
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
            st.error("Please enter a contract title.")
            return
        
        if not contractor:
            st.error("Please enter a contractor name.")
            return
            
        # In a real app, this would save to database
        if is_edit:
            st.success(f"Contract '{title}' updated successfully!")
        else:
            st.success(f"Contract '{title}' created successfully!")
        
        # Return to list view
        st.session_state.contract_view = "list"
        st.rerun()
    
    if cancel_button:
        # Return to previous view
        st.session_state.contract_view = "list"
        st.rerun()


def render_contract_analysis():
    """Render the contract analysis view with charts and metrics"""
    st.subheader("Contract Analysis")
    
    # Get sample data
    contracts = generate_sample_contracts()
    
    # Calculate summary metrics
    total_value = sum(c["Value"] for c in contracts)
    active_value = sum(c["Value"] for c in contracts if c["Status"] == "Active")
    pending_value = sum(c["Value"] for c in contracts if c["Status"] == "Pending")
    complete_value = sum(c["Value"] for c in contracts if c["Status"] == "Complete")
    
    # Summary metrics
    st.subheader("Contract Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Contract Value", f"${total_value:,.0f}")
    
    with col2:
        active_percent = (active_value / total_value) * 100 if total_value > 0 else 0
        st.metric("Active Contracts", f"${active_value:,.0f}", f"{active_percent:.1f}% of total")
    
    with col3:
        pending_percent = (pending_value / total_value) * 100 if total_value > 0 else 0
        st.metric("Pending Contracts", f"${pending_value:,.0f}", f"{pending_percent:.1f}% of total")
    
    with col4:
        complete_percent = (complete_value / total_value) * 100 if total_value > 0 else 0
        st.metric("Completed Contracts", f"${complete_value:,.0f}", f"{complete_percent:.1f}% of total")
    
    # Contract Distribution Charts
    st.subheader("Contract Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution by type
        type_data = {}
        for contract in contracts:
            contract_type = contract["Type"]
            if contract_type in type_data:
                type_data[contract_type] += contract["Value"]
            else:
                type_data[contract_type] = contract["Value"]
        
        # Create a DataFrame for the chart
        type_df = pd.DataFrame({
            'Contract Type': list(type_data.keys()),
            'Value': list(type_data.values())
        })
        
        st.write("#### Distribution by Contract Type")
        st.bar_chart(type_df.set_index('Contract Type'))
    
    with col2:
        # Status distribution
        st.write("#### Distribution by Status")
        
        status_data = pd.DataFrame({
            'Status': ['Active', 'Pending', 'Complete'],
            'Value': [active_value, pending_value, complete_value]
        })
        
        st.bar_chart(status_data.set_index('Status'))
    
    # Contract Timeline
    st.subheader("Contract Timeline")
    
    # Create timeline data
    timeline_data = []
    for contract in contracts:
        start_date = datetime.strptime(contract["Start_Date"], "%Y-%m-%d")
        end_date = datetime.strptime(contract["End_Date"], "%Y-%m-%d")
        
        timeline_data.append({
            "Contract": contract["Title"],
            "Start": start_date,
            "End": end_date,
            "Value": contract["Value"],
            "Status": contract["Status"]
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
    
    # Contract Value Over Time (placeholder)
    st.subheader("Contract Value Over Time")
    
    # Create sample cumulative contract value
    months = pd.date_range(
        start=min(timeline_data, key=lambda x: x["Start"])["Start"],
        end=max(timeline_data, key=lambda x: x["End"])["End"],
        freq='MS'
    ).strftime("%Y-%m")
    
    cumulative_value = []
    current_value = 0
    
    for month in months:
        # Add contracts that start this month
        for contract in contracts:
            contract_start = contract["Start_Date"][0:7]  # YYYY-MM
            if contract_start == month:
                current_value += contract["Value"]
        
        cumulative_value.append(current_value)
    
    # Create a DataFrame for the chart
    value_over_time = pd.DataFrame({
        'Month': months,
        'Cumulative Value': cumulative_value
    })
    
    # Plot the trend
    st.line_chart(value_over_time.set_index('Month'))