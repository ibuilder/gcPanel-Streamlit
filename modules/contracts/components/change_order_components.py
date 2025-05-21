"""
Change Order components for the Contracts module.

This module provides the UI components for change order management including:
- Change order list view
- Change order details view
- Change order form (add/edit)
- Change order analysis view
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Sample data for demonstration
def generate_sample_change_orders():
    """Generate sample change order data for demonstration"""
    return [
        {
            "ID": "CO-2025-001",
            "Title": "Additional Steel Reinforcement",
            "Contract_ID": "CT-2025-001",
            "Contract_Title": "Highland Tower Main Construction",
            "Amount": 125000,
            "Impact_Days": 10,
            "Submit_Date": "2025-02-15",
            "Status": "Approved"
        },
        {
            "ID": "CO-2025-002",
            "Title": "Electrical Layout Revision",
            "Contract_ID": "CT-2025-002",
            "Contract_Title": "Electrical Systems Installation",
            "Amount": 45000,
            "Impact_Days": 5,
            "Submit_Date": "2025-03-10",
            "Status": "Approved"
        },
        {
            "ID": "CO-2025-003",
            "Title": "HVAC System Upgrade",
            "Contract_ID": "CT-2025-003", 
            "Contract_Title": "Plumbing and HVAC Services",
            "Amount": 78000,
            "Impact_Days": 8,
            "Submit_Date": "2025-03-25",
            "Status": "Pending"
        },
        {
            "ID": "CO-2025-004",
            "Title": "Foundation Design Modification",
            "Contract_ID": "CT-2025-004",
            "Contract_Title": "Foundation and Concrete Work",
            "Amount": 215000,
            "Impact_Days": 15,
            "Submit_Date": "2025-01-30",
            "Status": "Approved"
        },
        {
            "ID": "CO-2025-005",
            "Title": "Enhanced Landscaping Features",
            "Contract_ID": "CT-2025-005",
            "Contract_Title": "Exterior Finishes and Landscaping",
            "Amount": 35000,
            "Impact_Days": 0,
            "Submit_Date": "2025-03-05",
            "Status": "Under Review"
        },
        {
            "ID": "CO-2025-006",
            "Title": "Additional Plumbing Fixtures",
            "Contract_ID": "CT-2025-003",
            "Contract_Title": "Plumbing and HVAC Services",
            "Amount": 42000,
            "Impact_Days": 3,
            "Submit_Date": "2025-04-10",
            "Status": "Pending"
        },
        {
            "ID": "CO-2025-007",
            "Title": "Structural Steel Quantity Adjustment",
            "Contract_ID": "SC-2025-001",
            "Contract_Title": "Structural Steel Installation",
            "Amount": -35000,
            "Impact_Days": -2,
            "Submit_Date": "2025-02-25",
            "Status": "Approved"
        }
    ]

def render_change_order_list():
    """Render the change orders list view with filtering and sorting"""
    st.subheader("Change Orders")
    
    # Get sample data
    change_orders = generate_sample_change_orders()
    
    with st.expander("Filters", expanded=True):
        # Create columns for the filters
        col1, col2 = st.columns(2)
        
        with col1:
            # Status filter
            statuses = ["All Statuses"] + list(set(co["Status"] for co in change_orders))
            selected_status = st.selectbox("Status", statuses, key="change_order_status_filter")
            
            # Contract filter
            contracts = ["All Contracts"] + list(set(co["Contract_Title"] for co in change_orders))
            selected_contract = st.selectbox("Contract", contracts, key="change_order_contract_filter")
        
        with col2:
            # Amount range filter
            min_amount = min(co["Amount"] for co in change_orders)
            max_amount = max(co["Amount"] for co in change_orders)
            amount_range = st.slider(
                "Amount Range ($)",
                min_value=int(min_amount),
                max_value=int(max_amount),
                value=(int(min_amount), int(max_amount)),
                step=5000
            )
            
            # Search field
            search_term = st.text_input("Search", key="change_order_search", placeholder="Search change orders...")
    
    # Filter the data based on selections
    filtered_change_orders = change_orders
    
    if selected_status != "All Statuses":
        filtered_change_orders = [co for co in filtered_change_orders if co["Status"] == selected_status]
    
    if selected_contract != "All Contracts":
        filtered_change_orders = [co for co in filtered_change_orders if co["Contract_Title"] == selected_contract]
    
    filtered_change_orders = [co for co in filtered_change_orders if co["Amount"] >= amount_range[0] and co["Amount"] <= amount_range[1]]
    
    if search_term:
        filtered_change_orders = [co for co in filtered_change_orders if 
                                search_term.lower() in co["Title"].lower() or 
                                search_term.lower() in co["ID"].lower() or
                                search_term.lower() in co["Contract_Title"].lower()]

    # Add button
    if st.button("➕ Add Change Order", use_container_width=True):
        st.session_state.change_order_view = "add"
        st.rerun()
    
    # Check if we have any results
    if not filtered_change_orders:
        st.info("No change orders match your filters.")
        return
    
    # Show item count
    st.caption(f"Showing {len(filtered_change_orders)} change orders")
    
    # Display the filtered change orders
    for change_order in filtered_change_orders:
        # Create a container for each change order
        change_order_container = st.container()
        
        with change_order_container:
            # Add a subtle divider between change orders
            st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
            
            # Create a row with columns for the change order data and action buttons
            row_container = st.container()
            
            # Create a more balanced row layout with condensed columns
            col1, col2, col3, col4, col_actions = row_container.columns([0.8, 3, 2, 1.5, 0.7])
            
            with col1:
                st.write(f"**{change_order['ID']}**")
                st.caption(f"{change_order['Submit_Date']}")
            
            with col2:
                st.write(f"📝 **{change_order['Title']}**")
                st.caption(f"Contract: {change_order['Contract_Title']}")
            
            with col3:
                # Impact information
                impact_color = "red" if change_order["Impact_Days"] > 0 else "green"
                days_text = f"+{change_order['Impact_Days']} days" if change_order["Impact_Days"] > 0 else f"{change_order['Impact_Days']} days"
                
                # Show impact info
                st.markdown(f"""
                <small><b>Schedule Impact:</b><br>
                <span style='color:{impact_color};'>{days_text}</span></small>
                """, unsafe_allow_html=True)
            
            with col4:
                # Amount and status
                amount_color = "red" if change_order["Amount"] > 0 else "green"
                amount_prefix = "+" if change_order["Amount"] > 0 else ""
                
                status_color = {
                    "Approved": "green",
                    "Pending": "orange",
                    "Under Review": "blue",
                    "Rejected": "red"
                }.get(change_order['Status'], "grey")
                
                # Value and status in one block
                st.markdown(f"""
                <span style='color:{amount_color};'><b>{amount_prefix}${abs(change_order['Amount']):,}</b></span><br>
                <span style='color:{status_color};'><small>{change_order['Status']}</small></span>
                """, unsafe_allow_html=True)
            
            # Action buttons in a single column
            with col_actions:
                # Create two buttons side by side in the actions column
                action_btn_cols = st.columns(2)
                
                # View button
                with action_btn_cols[0]:
                    if st.button("👁️", key=f"view_{change_order['ID']}", help="View change order details"):
                        # Store change order details in session state
                        st.session_state.selected_change_order_id = change_order['ID'] 
                        st.session_state.selected_change_order_data = change_order
                        # Set view mode
                        st.session_state["change_order_view"] = "view"
                        # Force refresh
                        st.rerun()
                
                # Edit button
                with action_btn_cols[1]:
                    if st.button("✏️", key=f"edit_{change_order['ID']}", help="Edit change order"):
                        # Store change order data for editing
                        st.session_state.edit_change_order_id = change_order['ID']
                        st.session_state.edit_change_order_data = change_order
                        # Set edit mode 
                        st.session_state["change_order_view"] = "edit"
                        # Force refresh
                        st.rerun()

def render_change_order_details():
    """Render the change order details view (single record view)"""
    st.subheader("Change Order Details")
    
    # Ensure we have a selected change order
    if not st.session_state.get("selected_change_order_id"):
        st.error("No change order selected. Please select a change order from the list.")
        # Return to list view
        st.session_state.change_order_view = "list"
        st.rerun()
        return
    
    # Get the selected change order data
    change_order = st.session_state.get("selected_change_order_data", None)
    
    if not change_order:
        # If somehow we have an ID but no data, try to find it
        change_orders = generate_sample_change_orders()
        change_order = next((co for co in change_orders if co["ID"] == st.session_state.selected_change_order_id), None)
        
        if not change_order:
            st.error(f"Change order with ID {st.session_state.selected_change_order_id} not found.")
            # Return to list view
            st.session_state.change_order_view = "list"
            st.rerun()
            return
    
    # Display change order details
    with st.container():
        # Style for change order details
        st.markdown("""
        <style>
            .change-order-details {
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 15px;
            }
            .change-order-header {
                margin-bottom: 20px;
            }
            .change-order-section {
                margin-top: 15px;
                margin-bottom: 15px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Start change order details container
        st.markdown('<div class="change-order-details">', unsafe_allow_html=True)
        
        # Header section
        st.markdown(f'<div class="change-order-header">', unsafe_allow_html=True)
        st.markdown(f"# {change_order['Title']}")
        st.markdown(f"#### ID: {change_order['ID']} | Contract: {change_order['Contract_Title']} | Status: {change_order['Status']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Change order information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'<div class="change-order-section">', unsafe_allow_html=True)
            st.markdown("### Financial Impact")
            
            amount_color = "red" if change_order["Amount"] > 0 else "green"
            amount_prefix = "+" if change_order["Amount"] > 0 else ""
            
            st.markdown(f"**Change Amount:** <span style='color:{amount_color};'>{amount_prefix}${abs(change_order['Amount']):,}</span>", unsafe_allow_html=True)
            
            # Original and revised contract value (simulated)
            original_value = random.randint(1000000, 3000000)
            revised_value = original_value + change_order['Amount']
            
            st.markdown(f"**Original Contract Value:** ${original_value:,}")
            st.markdown(f"**Revised Contract Value:** ${revised_value:,}")
            
            # Percentage impact
            percentage = (change_order['Amount'] / original_value) * 100
            percentage_prefix = "+" if percentage > 0 else ""
            st.markdown(f"**Percentage Change:** {percentage_prefix}{percentage:.2f}%")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="change-order-section">', unsafe_allow_html=True)
            st.markdown("### Schedule Impact")
            
            # Show schedule impact
            impact_color = "red" if change_order["Impact_Days"] > 0 else "green"
            days_text = f"+{change_order['Impact_Days']} days" if change_order["Impact_Days"] > 0 else f"{change_order['Impact_Days']} days"
            
            st.markdown(f"**Schedule Impact:** <span style='color:{impact_color};'>{days_text}</span>", unsafe_allow_html=True)
            
            # Simulated dates
            original_completion = datetime.strptime("2025-12-15", "%Y-%m-%d")
            revised_completion = original_completion + timedelta(days=change_order['Impact_Days'])
            
            st.markdown(f"**Original Completion:** {original_completion.strftime('%Y-%m-%d')}")
            st.markdown(f"**Revised Completion:** {revised_completion.strftime('%Y-%m-%d')}")
            
            # Submit date
            st.markdown(f"**Submit Date:** {change_order['Submit_Date']}")
            
            # Approval date (simulated)
            if change_order['Status'] == "Approved":
                submit_date = datetime.strptime(change_order['Submit_Date'], "%Y-%m-%d")
                approval_date = submit_date + timedelta(days=random.randint(5, 15))
                st.markdown(f"**Approval Date:** {approval_date.strftime('%Y-%m-%d')}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Change order details (placeholder)
        st.markdown(f'<div class="change-order-section">', unsafe_allow_html=True)
        st.markdown("### Change Order Description")
        
        # Generate a random detailed description
        descriptions = [
            f"This change order addresses additional {change_order['Title'].lower()} requirements identified during construction. The modifications are necessary to meet updated building codes and owner specifications. The work includes material adjustments, labor reallocation, and extended equipment rental.",
            f"Due to unforeseen site conditions, this {change_order['Title'].lower()} change is required. The scope involves modifications to the original design to accommodate actual field conditions. Additional engineering review and coordination with subcontractors is included in this change order.",
            f"Owner-requested modifications to {change_order['Title'].lower()} specifications. This change includes upgraded materials and revised installation methods to meet the owner's updated requirements. The change affects both material costs and installation timeframes."
        ]
        
        st.markdown(random.choice(descriptions))
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Supporting documents (placeholder)
        st.markdown(f'<div class="change-order-section">', unsafe_allow_html=True)
        st.markdown("### Supporting Documents")
        
        document_types = ["Cost Estimate", "Schedule Impact Analysis", "Design Revision Drawings", "Specification Updates", "Owner Approval Letter"]
        
        # Generate some random documents
        documents = []
        num_docs = random.randint(2, 4)
        for i in range(num_docs):
            doc_type = random.choice(document_types)
            documents.append({
                "Name": f"{doc_type} - {change_order['ID']}",
                "Type": doc_type,
                "Date": (datetime.strptime(change_order['Submit_Date'], "%Y-%m-%d") - timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d")
            })
        
        # Display documents
        if documents:
            docs_df = pd.DataFrame(documents)
            st.dataframe(docs_df, use_container_width=True)
        else:
            st.info("No supporting documents have been uploaded for this change order.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Actions
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✏️ Edit Change Order", use_container_width=True):
                st.session_state.edit_change_order_id = change_order['ID']
                st.session_state.edit_change_order_data = change_order
                st.session_state.change_order_view = "edit"
                st.rerun()
        
        with col2:
            if st.button("📊 View Analysis", use_container_width=True):
                st.session_state.change_order_view = "analysis"
                st.rerun()
        
        # End the change order details container
        st.markdown('</div>', unsafe_allow_html=True)


def render_change_order_form(is_edit=False):
    """Render the change order creation/edit form"""
    if is_edit:
        st.subheader("Edit Change Order")
        # Ensure we have a change order to edit
        if not st.session_state.get("edit_change_order_id"):
            st.error("No change order selected for editing. Please select a change order from the list.")
            # Return to list view
            st.session_state.change_order_view = "list"
            st.rerun()
            return
        
        # Get the change order data for editing
        change_order = st.session_state.get("edit_change_order_data", {})
    else:
        st.subheader("Add New Change Order")
        # Initialize empty change order for new entries
        change_order = {
            "ID": f"CO-{datetime.now().year}-{random.randint(100, 999)}",
            "Title": "",
            "Contract_ID": "",
            "Contract_Title": "",
            "Amount": 0,
            "Impact_Days": 0,
            "Submit_Date": datetime.now().strftime("%Y-%m-%d"),
            "Status": "Draft"
        }
    
    # Create the form
    with st.form(key="change_order_form"):
        # Basic information
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Change Order Title *", value=change_order.get("Title", ""))
            
            # Contract dropdown
            # Simulated list of available contracts
            contracts = [
                {"id": "CT-2025-001", "title": "Highland Tower Main Construction"},
                {"id": "CT-2025-002", "title": "Electrical Systems Installation"},
                {"id": "CT-2025-003", "title": "Plumbing and HVAC Services"},
                {"id": "CT-2025-004", "title": "Foundation and Concrete Work"},
                {"id": "CT-2025-005", "title": "Exterior Finishes and Landscaping"},
                {"id": "SC-2025-001", "title": "Structural Steel Installation"}
            ]
            
            contract_options = [f"{c['id']} - {c['title']}" for c in contracts]
            
            # Find index of selected contract if editing
            selected_index = 0
            if is_edit and change_order.get("Contract_ID"):
                full_contract_option = f"{change_order.get('Contract_ID')} - {change_order.get('Contract_Title')}"
                if full_contract_option in contract_options:
                    selected_index = contract_options.index(full_contract_option)
            
            selected_contract = st.selectbox(
                "Contract *", 
                contract_options,
                index=selected_index
            )
            
            # Extract contract ID and title
            if selected_contract:
                contract_id = selected_contract.split(" - ")[0]
                contract_title = selected_contract[len(contract_id) + 3:]
        
        with col2:
            # For display only
            if is_edit:
                st.text_input("Change Order ID", value=change_order.get("ID", ""), disabled=True)
            
            # Status dropdown
            status_options = ["Draft", "Pending", "Under Review", "Approved", "Rejected"]
            
            # Find index of selected status if editing
            status_index = 0
            if is_edit and change_order.get("Status") in status_options:
                status_index = status_options.index(change_order.get("Status"))
            
            selected_status = st.selectbox(
                "Status *",
                status_options,
                index=status_index
            )
            
            # Submit date
            submit_date = st.date_input(
                "Submit Date *",
                value=datetime.strptime(change_order.get("Submit_Date", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
            )
        
        # Financial and schedule impact
        st.subheader("Change Impact")
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input(
                "Amount Change ($) *", 
                value=int(change_order.get("Amount", 0)),
                step=1000,
                help="Positive value for additional costs, negative for savings"
            )
        
        with col2:
            impact_days = st.number_input(
                "Schedule Impact (days)",
                value=int(change_order.get("Impact_Days", 0)),
                step=1,
                help="Positive value for schedule extension, negative for acceleration"
            )
        
        # Description
        st.subheader("Description")
        description = st.text_area(
            "Change Order Description *", 
            value=change_order.get("Description", ""),
            height=150,
            help="Provide a detailed description of the change and its justification"
        )
        
        # Supporting documentation
        st.subheader("Supporting Documentation")
        
        # Simulated document upload
        upload_file = st.file_uploader("Upload Supporting Documents", type=["pdf", "doc", "docx", "xls", "xlsx"], accept_multiple_files=True)
        
        # Submit buttons
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button(
                "Save Change Order" if is_edit else "Create Change Order",
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
            st.error("Please enter a change order title.")
            return
        
        if not description:
            st.error("Please provide a description for the change order.")
            return
            
        # In a real app, this would save to database
        if is_edit:
            st.success(f"Change Order '{title}' updated successfully!")
        else:
            st.success(f"Change Order '{title}' created successfully!")
        
        # Return to list view
        st.session_state.change_order_view = "list"
        st.rerun()
    
    if cancel_button:
        # Return to previous view
        st.session_state.change_order_view = "list"
        st.rerun()


def render_change_order_analysis():
    """Render the change order analysis view with charts and metrics"""
    st.subheader("Change Order Analysis")
    
    # Get sample data
    change_orders = generate_sample_change_orders()
    
    # Calculate summary metrics
    total_changes = len(change_orders)
    total_amount = sum(co["Amount"] for co in change_orders)
    approved_amount = sum(co["Amount"] for co in change_orders if co["Status"] == "Approved")
    pending_amount = sum(co["Amount"] for co in change_orders if co["Status"] in ["Pending", "Under Review"])
    
    # Calculate total contract values (simulated)
    original_contract_value = 8500000  # $8.5M simulated original value
    current_contract_value = original_contract_value + approved_amount
    
    # Summary metrics
    st.subheader("Change Order Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Change Orders", f"{total_changes}")
    
    with col2:
        percentage = (approved_amount / original_contract_value) * 100 if original_contract_value > 0 else 0
        st.metric("Total Change Amount", f"${total_amount:,.0f}", f"{percentage:.1f}% of original")
    
    with col3:
        st.metric("Approved Changes", f"${approved_amount:,.0f}")
    
    with col4:
        st.metric("Pending Changes", f"${pending_amount:,.0f}")
    
    # Change order distribution
    st.subheader("Change Order Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution by contract
        contract_data = {}
        for co in change_orders:
            contract = co["Contract_Title"]
            if contract in contract_data:
                contract_data[contract] += co["Amount"]
            else:
                contract_data[contract] = co["Amount"]
        
        # Create a DataFrame for the chart
        contract_df = pd.DataFrame({
            'Contract': list(contract_data.keys()),
            'Amount': list(contract_data.values())
        })
        
        st.write("#### Distribution by Contract")
        st.bar_chart(contract_df.set_index('Contract'))
    
    with col2:
        # Status distribution
        status_data = {}
        for co in change_orders:
            status = co["Status"]
            if status in status_data:
                status_data[status] += co["Amount"]
            else:
                status_data[status] = co["Amount"]
        
        # Create a DataFrame for the chart
        status_df = pd.DataFrame({
            'Status': list(status_data.keys()),
            'Amount': list(status_data.values())
        })
        
        st.write("#### Distribution by Status")
        st.bar_chart(status_df.set_index('Status'))
    
    # Change order trend over time
    st.subheader("Change Order Trend")
    
    # Group change orders by month
    change_orders_by_date = {}
    for co in change_orders:
        month = co["Submit_Date"][:7]  # YYYY-MM
        if month in change_orders_by_date:
            change_orders_by_date[month]["Count"] += 1
            change_orders_by_date[month]["Amount"] += co["Amount"]
        else:
            change_orders_by_date[month] = {
                "Count": 1,
                "Amount": co["Amount"]
            }
    
    # Sort by date
    sorted_months = sorted(change_orders_by_date.keys())
    
    # Create cumulative data
    cumulative_count = 0
    cumulative_amount = 0
    trend_data = []
    
    for month in sorted_months:
        cumulative_count += change_orders_by_date[month]["Count"]
        cumulative_amount += change_orders_by_date[month]["Amount"]
        
        trend_data.append({
            "Month": month,
            "Monthly Count": change_orders_by_date[month]["Count"],
            "Monthly Amount": change_orders_by_date[month]["Amount"],
            "Cumulative Count": cumulative_count,
            "Cumulative Amount": cumulative_amount
        })
    
    # Create a DataFrame
    trend_df = pd.DataFrame(trend_data)
    
    # Display count trend
    st.write("#### Change Order Count by Month")
    
    # Create monthly count chart
    count_chart = pd.DataFrame({
        'Month': trend_df["Month"],
        'Monthly': trend_df["Monthly Count"],
        'Cumulative': trend_df["Cumulative Count"]
    })
    
    st.line_chart(count_chart.set_index('Month'))
    
    # Display amount trend
    st.write("#### Change Order Amount by Month")
    
    # Create monthly amount chart
    amount_chart = pd.DataFrame({
        'Month': trend_df["Month"],
        'Monthly': trend_df["Monthly Amount"],
        'Cumulative': trend_df["Cumulative Amount"]
    })
    
    st.line_chart(amount_chart.set_index('Month'))
    
    # Change order impact analysis
    st.subheader("Change Order Impact Analysis")
    
    # Calculate contract growth
    growth_percentage = (approved_amount / original_contract_value) * 100 if original_contract_value > 0 else 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Original Contract Value", f"${original_contract_value:,.0f}")
        st.metric("Current Contract Value", f"${current_contract_value:,.0f}", f"{growth_percentage:.1f}%")
    
    with col2:
        # Calculate schedule impact
        total_schedule_impact = sum(co["Impact_Days"] for co in change_orders if co["Status"] == "Approved")
        st.metric("Total Schedule Impact", f"{total_schedule_impact} days")
        
        # Average change order processing time (simulated)
        st.metric("Avg. Processing Time", "12 days")