"""
Contracts module for the gcPanel Construction Management Dashboard.

This module provides contract management features including tracking
contracts, change orders, and payment applications.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import plotly.express as px
import plotly.graph_objects as go

# Import form components
from components.contracts_forms import contract_form, change_order_form

def render_contracts():
    """Render the contracts module"""
    
    # Header
    st.title("Contracts Management")
    
    # Tab navigation for contracts sections
    tab1, tab2, tab3, tab4 = st.tabs(["Contracts", "Change Orders", "Payment Applications", "Financial"])
    
    # Contracts Tab
    with tab1:
        render_contract_list()
    
    # Change Orders Tab
    with tab2:
        render_change_orders()
    
    # Payment Applications Tab
    with tab3:
        render_payment_applications()
    
    # Financial Tab
    with tab4:
        render_financial_summary()

def render_contract_list():
    """Render the contracts listing and details section"""
    
    # Header with Create Contract button
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.header("Project Contracts")
    
    with col3:
        if st.button("Create New Contract", type="primary", key="create_contract_btn", use_container_width=True):
            st.session_state.show_contract_form = True
            st.session_state.edit_contract_id = None
    
    # Contract creation/edit form
    if st.session_state.get("show_contract_form", False):
        # Get contract data if editing
        contract_to_edit = None
        if st.session_state.get("edit_contract_id"):
            contract_to_edit = next((c for c in contracts if c.get("id") == st.session_state.get("edit_contract_id")), None)
        
        # Use the enhanced form component
        form_submitted, form_data = contract_form(
            is_edit=st.session_state.get("edit_contract_id") is not None,
            contract_data=contract_to_edit
        )
        
        if form_submitted and form_data:
            # In a real app, this would save to database
            
            # Update or create contract
            if st.session_state.get("edit_contract_id"):
                # Update existing contract
                for i, contract in enumerate(contracts):
                    if contract["id"] == st.session_state.get("edit_contract_id"):
                        contracts[i].update(form_data)
                        break
                st.success("Contract updated successfully!")
            else:
                # Add new contract to the list
                contracts.insert(0, form_data)  # Add to beginning of list
                st.success("Contract created successfully!")
            
            # Reset form state
            st.session_state.show_contract_form = False
            st.session_state.edit_contract_id = None
            
            # Force rerender
            st.rerun()
    
    # Sample data for contracts
    contracts = [
        {
            "id": f"CT-{2025}-{i:03d}",
            "name": f"{random.choice(['Main Building', 'Site Work', 'Electrical', 'Plumbing', 'HVAC', 'Roofing', 'Landscaping', 'Structural', 'Concrete', 'Finishes'])} {random.choice(['Contract', 'Subcontract', 'Agreement', 'Services Agreement'])}",
            "vendor": random.choice([
                "Reliable Construction Inc.", "Elite Electrical Services", "Supreme Plumbing Co.", 
                "Advanced HVAC Systems", "Quality Roofing Ltd.", "Green Landscaping", 
                "Structural Masters", "Concrete Solutions", "Premium Finishes", "Global Services"
            ]),
            "type": random.choice(["Prime Contract", "Subcontract", "Purchase Order", "Services Agreement"]),
            "status": random.choice(["Draft", "Issued", "Executed", "In Progress", "On Hold", "Completed", "Terminated"]),
            "issue_date": datetime.now() - timedelta(days=random.randint(30, 180)),
            "execution_date": datetime.now() - timedelta(days=random.randint(15, 150)) if random.random() > 0.2 else None,
            "completion_date": datetime.now() + timedelta(days=random.randint(30, 180)),
            "original_value": round(random.uniform(50000, 2000000), 2),
            "current_value": 0,  # This will be calculated
            "approved_changes": 0,  # This will be calculated
            "pending_changes": 0,  # This will be calculated
            "retention_rate": random.choice([0.0, 0.05, 0.1]),
            "retention_held": 0,  # This will be calculated
            "paid_to_date": 0,  # This will be calculated
            "remaining_balance": 0,  # This will be calculated
            "scope": random.choice([
                "Complete construction of building shell and core", 
                "All electrical installations and wiring", 
                "Complete plumbing systems installation",
                "HVAC system installation and commissioning",
                "Roofing installation and waterproofing",
                "Exterior and interior landscaping",
                "Structural steel erection",
                "All concrete work including foundations",
                "Interior finishes, paint, and fixtures",
                "Consulting services for construction management"
            ]),
            "contact_name": random.choice(["John Smith", "Jane Doe", "Robert Johnson", "Mary Williams", "David Brown", "Sarah Miller"]),
            "contact_email": f"contact{random.randint(1, 100)}@example.com",
            "contact_phone": f"({random.randint(100, 999)})-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        } for i in range(1, 11)
    ]
    
    # Create change orders
    change_orders = []
    for i in range(1, 41):
        contract_id = random.choice([c["id"] for c in contracts])
        contract = next(c for c in contracts if c["id"] == contract_id)
        
        # Generate change order with realistic status progression
        status = random.choices(
            ["Draft", "Pending Approval", "Approved", "Rejected"], 
            weights=[0.1, 0.2, 0.6, 0.1], 
            k=1
        )[0]
        
        # Generate amount (positive for additions, negative for deductions)
        amount = random.uniform(-50000, 200000)
        
        change_orders.append({
            "id": f"CO-{2025}-{i:03d}",
            "contract_id": contract_id,
            "contract_name": contract["name"],
            "title": f"Change Order {i}",
            "description": random.choice([
                "Additional scope requested by owner",
                "Design changes requiring additional work",
                "Unforeseen field conditions requiring remediation",
                "Code compliance modifications",
                "Schedule acceleration costs",
                "Material substitution due to supply chain issues",
                "Reduced scope requested by owner",
                "Value engineering changes",
                "Weather-related delays and mitigation",
                "Site condition discoveries requiring design changes"
            ]),
            "status": status,
            "amount": amount,
            "submission_date": datetime.now() - timedelta(days=random.randint(1, 90)),
            "approval_date": datetime.now() - timedelta(days=random.randint(1, 30)) if status == "Approved" else None,
            "days_to_respond": random.randint(1, 30) if status != "Draft" else None,
            "time_extension": random.randint(0, 30) if random.random() > 0.7 else 0,
        })
    
    # Create payment applications
    payment_applications = []
    for i in range(1, 31):
        contract_id = random.choice([c["id"] for c in contracts])
        contract = next(c for c in contracts if c["id"] == contract_id)
        
        # Generate realistic payment application with proper status flow
        status = random.choices(
            ["Draft", "Submitted", "Under Review", "Approved", "Paid", "Rejected"], 
            weights=[0.05, 0.1, 0.2, 0.25, 0.35, 0.05], 
            k=1
        )[0]
        
        # Determine period and amount based on status
        if status in ["Paid", "Approved"]:
            period_start = datetime.now() - timedelta(days=random.randint(90, 365))
            period_end = period_start + timedelta(days=30)
            amount = contract["original_value"] * random.uniform(0.05, 0.15)
        else:
            period_start = datetime.now() - timedelta(days=random.randint(30, 90))
            period_end = period_start + timedelta(days=30)
            amount = contract["original_value"] * random.uniform(0.05, 0.15)
        
        payment_applications.append({
            "id": f"PA-{2025}-{i:03d}",
            "contract_id": contract_id,
            "contract_name": contract["name"],
            "period_start": period_start,
            "period_end": period_end,
            "submission_date": period_end + timedelta(days=random.randint(1, 10)),
            "status": status,
            "amount": amount,
            "retention_held": amount * contract["retention_rate"],
            "paid_amount": amount - (amount * contract["retention_rate"]) if status == "Paid" else 0,
            "payment_date": datetime.now() - timedelta(days=random.randint(1, 45)) if status == "Paid" else None,
        })
    
    # Calculate derived values for contracts
    for contract in contracts:
        # Calculate approved changes
        contract_change_orders = [co for co in change_orders if co["contract_id"] == contract["id"] and co["status"] == "Approved"]
        contract["approved_changes"] = sum(co["amount"] for co in contract_change_orders)
        
        # Calculate pending changes
        pending_change_orders = [co for co in change_orders if co["contract_id"] == contract["id"] and co["status"] in ["Draft", "Pending Approval"]]
        contract["pending_changes"] = sum(co["amount"] for co in pending_change_orders)
        
        # Calculate current contract value
        contract["current_value"] = contract["original_value"] + contract["approved_changes"]
        
        # Calculate paid to date
        contract_payments = [pa for pa in payment_applications if pa["contract_id"] == contract["id"] and pa["status"] == "Paid"]
        contract["paid_to_date"] = sum(pa["paid_amount"] for pa in contract_payments)
        
        # Calculate retention held
        contract["retention_held"] = sum(pa["retention_held"] for pa in contract_payments)
        
        # Calculate remaining balance
        contract["remaining_balance"] = contract["current_value"] - contract["paid_to_date"] - contract["retention_held"]
    
    # Filters for contracts
    col1, col2, col3 = st.columns(3)
    
    with col1:
        contract_type_filter = st.multiselect(
            "Contract Type",
            list(set(c["type"] for c in contracts)),
            default=list(set(c["type"] for c in contracts)),
            key="contract_type_filter"
        )
    
    with col2:
        contract_status_filter = st.multiselect(
            "Status",
            list(set(c["status"] for c in contracts)),
            default=list(set(c["status"] for c in contracts)),
            key="contract_status_filter"
        )
    
    with col3:
        vendor_filter = st.multiselect(
            "Vendor",
            list(set(c["vendor"] for c in contracts)),
            default=[],
            key="contract_vendor_filter"
        )
    
    # Apply filters
    filtered_contracts = [c for c in contracts 
                         if c["type"] in contract_type_filter 
                         and c["status"] in contract_status_filter]
    
    if vendor_filter:
        filtered_contracts = [c for c in filtered_contracts if c["vendor"] in vendor_filter]
    
    # Sort contracts by date (newest first)
    filtered_contracts.sort(key=lambda x: x["issue_date"], reverse=True)
    
    # Contract metrics
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        total_contracts = len(filtered_contracts)
        st.metric("Total Contracts", total_contracts)
    
    with metrics_col2:
        total_value = sum(c["current_value"] for c in filtered_contracts)
        st.metric("Total Value", f"${total_value:,.2f}")
    
    with metrics_col3:
        approved_changes = sum(c["approved_changes"] for c in filtered_contracts)
        st.metric("Approved Changes", f"${approved_changes:,.2f}")
    
    with metrics_col4:
        pending_changes = sum(c["pending_changes"] for c in filtered_contracts)
        st.metric("Pending Changes", f"${pending_changes:,.2f}")
    
    # Display contracts in a table
    st.subheader("Contract List")
    
    for contract in filtered_contracts:
        # Set status color
        if contract["status"] == "Draft":
            status_color = "#6c757d"  # Gray
        elif contract["status"] == "Issued":
            status_color = "#17a2b8"  # Info blue
        elif contract["status"] == "Executed":
            status_color = "#007bff"  # Primary blue
        elif contract["status"] == "In Progress":
            status_color = "#28a745"  # Green
        elif contract["status"] == "On Hold":
            status_color = "#ffc107"  # Warning yellow
        elif contract["status"] == "Completed":
            status_color = "#20c997"  # Teal
        else:  # Terminated
            status_color = "#dc3545"  # Danger red
        
        # Contract card
        with st.expander(f"{contract['name']} - {contract['vendor']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Contract ID:** {contract['id']}")
                st.markdown(f"**Type:** {contract['type']}")
                st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{contract['status']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Vendor:** {contract['vendor']}")
                st.markdown(f"**Issue Date:** {contract['issue_date'].strftime('%Y-%m-%d')}")
                
                if contract['execution_date']:
                    st.markdown(f"**Execution Date:** {contract['execution_date'].strftime('%Y-%m-%d')}")
                else:
                    st.markdown("**Execution Date:** Not yet executed")
                
                st.markdown(f"**Completion Date:** {contract['completion_date'].strftime('%Y-%m-%d')}")
            
            with col2:
                st.markdown(f"**Original Value:** ${contract['original_value']:,.2f}")
                st.markdown(f"**Approved Changes:** ${contract['approved_changes']:,.2f}")
                st.markdown(f"**Current Value:** ${contract['current_value']:,.2f}")
                st.markdown(f"**Paid to Date:** ${contract['paid_to_date']:,.2f}")
                st.markdown(f"**Retention Held:** ${contract['retention_held']:,.2f}")
                st.markdown(f"**Remaining Balance:** ${contract['remaining_balance']:,.2f}")
            
            st.markdown("### Scope")
            st.markdown(contract['scope'])
            
            st.markdown("### Contact Information")
            st.markdown(f"**Name:** {contract['contact_name']}")
            st.markdown(f"**Email:** {contract['contact_email']}")
            st.markdown(f"**Phone:** {contract['contact_phone']}")
            
            # Progress visualization
            st.markdown("### Contract Progress")
            
            # Calculate percentages
            paid_pct = (contract['paid_to_date'] / contract['current_value']) * 100 if contract['current_value'] > 0 else 0
            retention_pct = (contract['retention_held'] / contract['current_value']) * 100 if contract['current_value'] > 0 else 0
            remaining_pct = (contract['remaining_balance'] / contract['current_value']) * 100 if contract['current_value'] > 0 else 0
            
            # Create Stacked progress bar
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                y=['Progress'],
                x=[paid_pct],
                name='Paid to Date',
                orientation='h',
                marker=dict(color='#28a745'),
                text=f"${contract['paid_to_date']:,.2f}"
            ))
            
            fig.add_trace(go.Bar(
                y=['Progress'],
                x=[retention_pct],
                name='Retention',
                orientation='h',
                marker=dict(color='#ffc107'),
                text=f"${contract['retention_held']:,.2f}"
            ))
            
            fig.add_trace(go.Bar(
                y=['Progress'],
                x=[remaining_pct],
                name='Remaining',
                orientation='h',
                marker=dict(color='#17a2b8'),
                text=f"${contract['remaining_balance']:,.2f}"
            ))
            
            fig.update_layout(
                barmode='stack',
                height=150,
                margin=dict(l=0, r=0, t=0, b=0),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(ticksuffix="%")
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Action buttons
            buttons_col1, buttons_col2, buttons_col3, buttons_col4 = st.columns(4)
            
            with buttons_col1:
                st.button("Edit Contract", key=f"edit_{contract['id']}")
            
            with buttons_col2:
                st.button("Add Change Order", key=f"add_co_{contract['id']}")
            
            with buttons_col3:
                st.button("New Payment App", key=f"add_pa_{contract['id']}")
            
            with buttons_col4:
                st.button("View Documents", key=f"docs_{contract['id']}")
    
    # Add contract button
    st.divider()
    if st.button("Add New Contract", type="primary"):
        st.session_state.show_add_contract_form = True
    
    # Contract form
    if st.session_state.get("show_add_contract_form", False):
        with st.form("contract_form"):
            st.subheader("Add New Contract")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                contract_name = st.text_input("Contract Name", key="new_contract_name")
                contract_vendor = st.text_input("Vendor", key="new_contract_vendor")
                contract_type = st.selectbox(
                    "Contract Type",
                    ["Prime Contract", "Subcontract", "Purchase Order", "Services Agreement"],
                    key="new_contract_type"
                )
                contract_status = st.selectbox(
                    "Status",
                    ["Draft", "Issued", "Executed", "In Progress", "On Hold", "Completed", "Terminated"],
                    key="new_contract_status"
                )
                contract_value = st.number_input("Contract Value ($)", min_value=0.0, value=0.0, step=1000.0, key="new_contract_value")
                contract_retention = st.number_input("Retention Rate (%)", min_value=0.0, max_value=10.0, value=5.0, step=1.0, key="new_contract_retention")
            
            with form_col2:
                contract_issue_date = st.date_input("Issue Date", datetime.now(), key="new_contract_issue_date")
                contract_execution_date = st.date_input("Execution Date", datetime.now(), key="new_contract_execution_date")
                contract_completion_date = st.date_input("Completion Date", datetime.now() + timedelta(days=180), key="new_contract_completion_date")
                contract_contact_name = st.text_input("Contact Name", key="new_contract_contact_name")
                contract_contact_email = st.text_input("Contact Email", key="new_contract_contact_email")
                contract_contact_phone = st.text_input("Contact Phone", key="new_contract_contact_phone")
            
            contract_scope = st.text_area("Scope of Work", key="new_contract_scope")
            
            submitted = st.form_submit_button("Create Contract")
            
            if submitted:
                st.success("Contract created successfully!")
                st.session_state.show_add_contract_form = False
                st.rerun()

def render_change_orders():
    """Render the change orders management section"""
    
    st.header("Change Orders")
    
    # Sample data for contracts (simplified version - in reality you'd use the same from contract_list)
    contracts = [
        {"id": f"CT-{2025}-{i:03d}", "name": f"{random.choice(['Main Building', 'Site Work', 'Electrical', 'Plumbing', 'HVAC', 'Roofing', 'Landscaping', 'Structural', 'Concrete', 'Finishes'])} Contract"} 
        for i in range(1, 11)
    ]
    
    # Sample data for change orders
    change_orders = []
    for i in range(1, 41):
        contract = random.choice(contracts)
        
        # Generate change order with realistic status progression
        status = random.choices(
            ["Draft", "Pending Approval", "Approved", "Rejected"], 
            weights=[0.1, 0.2, 0.6, 0.1], 
            k=1
        )[0]
        
        # Generate amount (positive for additions, negative for deductions)
        amount = random.uniform(-50000, 200000)
        
        change_orders.append({
            "id": f"CO-{2025}-{i:03d}",
            "contract_id": contract["id"],
            "contract_name": contract["name"],
            "title": f"Change Order {i}",
            "description": random.choice([
                "Additional scope requested by owner",
                "Design changes requiring additional work",
                "Unforeseen field conditions requiring remediation",
                "Code compliance modifications",
                "Schedule acceleration costs",
                "Material substitution due to supply chain issues",
                "Reduced scope requested by owner",
                "Value engineering changes",
                "Weather-related delays and mitigation",
                "Site condition discoveries requiring design changes"
            ]),
            "status": status,
            "amount": amount,
            "submission_date": datetime.now() - timedelta(days=random.randint(1, 90)),
            "approval_date": datetime.now() - timedelta(days=random.randint(1, 30)) if status == "Approved" else None,
            "days_to_respond": random.randint(1, 30) if status != "Draft" else None,
            "time_extension": random.randint(0, 30) if random.random() > 0.7 else 0,
        })
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        contract_filter = st.selectbox(
            "Contract",
            ["All"] + [c["name"] for c in contracts],
            key="co_contract_filter"
        )
    
    with col2:
        status_filter = st.multiselect(
            "Status",
            ["Draft", "Pending Approval", "Approved", "Rejected"],
            default=["Draft", "Pending Approval", "Approved", "Rejected"],
            key="co_status_filter"
        )
    
    with col3:
        date_range = st.selectbox(
            "Date Range",
            ["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year", "All Time"],
            key="co_date_range"
        )
    
    # Apply filters
    filtered_cos = [co for co in change_orders if co["status"] in status_filter]
    
    if contract_filter != "All":
        filtered_cos = [co for co in filtered_cos if co["contract_name"] == contract_filter]
    
    # Apply date range filter
    today = datetime.now()
    if date_range == "Last 30 Days":
        filtered_cos = [co for co in filtered_cos if (today - co["submission_date"]).days <= 30]
    elif date_range == "Last 90 Days":
        filtered_cos = [co for co in filtered_cos if (today - co["submission_date"]).days <= 90]
    elif date_range == "Last 6 Months":
        filtered_cos = [co for co in filtered_cos if (today - co["submission_date"]).days <= 180]
    elif date_range == "Last Year":
        filtered_cos = [co for co in filtered_cos if (today - co["submission_date"]).days <= 365]
    
    # Change order metrics
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        total_cos = len(filtered_cos)
        st.metric("Total Change Orders", total_cos)
    
    with metrics_col2:
        approved_cos = len([co for co in filtered_cos if co["status"] == "Approved"])
        st.metric("Approved", approved_cos)
    
    with metrics_col3:
        total_amount = sum(co["amount"] for co in filtered_cos if co["status"] == "Approved")
        st.metric("Net Amount", f"${total_amount:,.2f}")
    
    with metrics_col4:
        avg_respond_time = sum(co["days_to_respond"] or 0 for co in filtered_cos) / len([co for co in filtered_cos if co["days_to_respond"] is not None]) if any(co["days_to_respond"] is not None for co in filtered_cos) else 0
        st.metric("Avg. Response Time", f"{avg_respond_time:.1f} days")
    
    # Charts
    st.subheader("Change Order Analysis")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Status distribution chart
        status_counts = pd.DataFrame([{"Status": co["status"]} for co in filtered_cos])
        
        if not status_counts.empty:
            status_fig = px.pie(
                status_counts, 
                names="Status",
                title="Change Orders by Status",
                color="Status",
                color_discrete_map={
                    "Draft": "#6c757d",
                    "Pending Approval": "#ffc107",
                    "Approved": "#28a745",
                    "Rejected": "#dc3545"
                }
            )
            
            st.plotly_chart(status_fig, use_container_width=True)
        else:
            st.info("No data available for status chart")
    
    with chart_col2:
        # Amount by status chart
        if filtered_cos:
            amount_data = []
            for co in filtered_cos:
                amount_data.append({
                    "Status": co["status"],
                    "Amount": abs(co["amount"]),
                    "Type": "Addition" if co["amount"] > 0 else "Deduction"
                })
            
            amount_df = pd.DataFrame(amount_data)
            
            amount_fig = px.bar(
                amount_df,
                x="Status",
                y="Amount",
                color="Type",
                title="Change Order Amounts by Status",
                color_discrete_map={
                    "Addition": "#28a745",
                    "Deduction": "#dc3545"
                }
            )
            
            st.plotly_chart(amount_fig, use_container_width=True)
        else:
            st.info("No data available for amount chart")
    
    # Change order list
    st.subheader("Change Order List")
    
    # Sort by submission date (newest first)
    filtered_cos.sort(key=lambda x: x["submission_date"], reverse=True)
    
    for co in filtered_cos:
        # Status color
        if co["status"] == "Draft":
            status_color = "#6c757d"  # Gray
        elif co["status"] == "Pending Approval":
            status_color = "#ffc107"  # Warning yellow
        elif co["status"] == "Approved":
            status_color = "#28a745"  # Green
        else:  # Rejected
            status_color = "#dc3545"  # Danger red
        
        # Amount color
        amount_color = "#28a745" if co["amount"] > 0 else "#dc3545"
        
        with st.expander(f"{co['id']} - {co['title']} ({co['contract_name']})", expanded=False):
            co_col1, co_col2 = st.columns(2)
            
            with co_col1:
                st.markdown(f"**Contract:** {co['contract_name']}")
                st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{co['status']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Submission Date:** {co['submission_date'].strftime('%Y-%m-%d')}")
                
                if co["approval_date"]:
                    st.markdown(f"**Approval Date:** {co['approval_date'].strftime('%Y-%m-%d')}")
                
                if co["days_to_respond"]:
                    st.markdown(f"**Response Time:** {co['days_to_respond']} days")
            
            with co_col2:
                st.markdown(f"**Amount:** <span style='color: {amount_color}; font-weight: bold;'>${co['amount']:,.2f}</span>", unsafe_allow_html=True)
                st.markdown(f"**Time Extension:** {co['time_extension']} days")
            
            st.markdown("### Description")
            st.markdown(co["description"])
            
            # Action buttons
            buttons_col1, buttons_col2, buttons_col3 = st.columns(3)
            
            with buttons_col1:
                st.button("Edit", key=f"edit_co_{co['id']}")
            
            with buttons_col2:
                if co["status"] in ["Draft", "Pending Approval"]:
                    st.button("Submit for Approval" if co["status"] == "Draft" else "Approve", key=f"approve_co_{co['id']}")
            
            with buttons_col3:
                st.button("View Details", key=f"details_co_{co['id']}")
    
    # Add new change order button
    st.divider()
    if st.button("Create New Change Order", type="primary", key="add_co_btn"):
        st.session_state.show_add_co_form = True
    
    # Change order form
    if st.session_state.get("show_add_co_form", False):
        with st.form("co_form"):
            st.subheader("Create New Change Order")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                co_contract = st.selectbox("Contract", [c["name"] for c in contracts], key="new_co_contract")
                co_title = st.text_input("Title", key="new_co_title")
                co_amount = st.number_input("Amount ($)", value=0.0, step=1000.0, key="new_co_amount")
                co_time_extension = st.number_input("Time Extension (days)", min_value=0, value=0, key="new_co_time")
            
            with form_col2:
                co_status = st.selectbox("Status", ["Draft", "Pending Approval"], key="new_co_status")
                co_submission_date = st.date_input("Submission Date", datetime.now(), key="new_co_date")
            
            co_description = st.text_area("Description", key="new_co_description")
            
            # File upload
            co_attachments = st.file_uploader("Attachments", accept_multiple_files=True, key="new_co_attachments")
            
            submitted = st.form_submit_button("Create Change Order")
            
            if submitted:
                st.success("Change order created successfully!")
                st.session_state.show_add_co_form = False
                st.rerun()

def render_payment_applications():
    """Render the payment applications management section"""
    
    st.header("Payment Applications")
    
    # Sample data for contracts (simplified version - in reality you'd use the same from contract_list)
    contracts = [
        {"id": f"CT-{2025}-{i:03d}", "name": f"{random.choice(['Main Building', 'Site Work', 'Electrical', 'Plumbing', 'HVAC', 'Roofing', 'Landscaping', 'Structural', 'Concrete', 'Finishes'])} Contract"} 
        for i in range(1, 11)
    ]
    
    # Sample data for payment applications
    payment_applications = []
    for i in range(1, 31):
        contract = random.choice(contracts)
        
        # Generate realistic payment application with proper status flow
        status = random.choices(
            ["Draft", "Submitted", "Under Review", "Approved", "Paid", "Rejected"], 
            weights=[0.05, 0.1, 0.2, 0.25, 0.35, 0.05], 
            k=1
        )[0]
        
        # Generate realistic period
        period_start = datetime.now() - timedelta(days=random.randint(30, 365))
        period_end = period_start + timedelta(days=30)
        
        # Generate amount based on randomized contract value
        contract_value = random.uniform(100000, 2000000)
        
        payment_applications.append({
            "id": f"PA-{2025}-{i:03d}",
            "contract_id": contract["id"],
            "contract_name": contract["name"],
            "period_start": period_start,
            "period_end": period_end,
            "submission_date": period_end + timedelta(days=random.randint(1, 10)),
            "period_number": random.randint(1, 12),
            "status": status,
            "amount": contract_value * random.uniform(0.05, 0.15),
            "retention_rate": random.choice([0.0, 0.05, 0.1]),
            "retention_held": 0,  # Will be calculated
            "paid_amount": 0,  # Will be calculated
            "payment_date": datetime.now() - timedelta(days=random.randint(1, 45)) if status == "Paid" else None,
            "description": random.choice([
                "Regular monthly progress payment",
                "Payment for completed foundations",
                "Payment for structural steel erection",
                "Payment for completed building envelope",
                "Payment for interior finishes",
                "Payment for MEP installation",
                "Payment for site work",
                "Payment for final completion",
                "Retainage release"
            ])
        })
    
    # Calculate derived values
    for pa in payment_applications:
        pa["retention_held"] = pa["amount"] * pa["retention_rate"]
        pa["paid_amount"] = pa["amount"] - pa["retention_held"] if pa["status"] == "Paid" else 0
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        contract_filter = st.selectbox(
            "Contract",
            ["All"] + [c["name"] for c in contracts],
            key="pa_contract_filter"
        )
    
    with col2:
        status_filter = st.multiselect(
            "Status",
            ["Draft", "Submitted", "Under Review", "Approved", "Paid", "Rejected"],
            default=["Draft", "Submitted", "Under Review", "Approved", "Paid", "Rejected"],
            key="pa_status_filter"
        )
    
    with col3:
        date_range = st.selectbox(
            "Date Range",
            ["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year", "All Time"],
            key="pa_date_range"
        )
    
    # Apply filters
    filtered_pas = [pa for pa in payment_applications if pa["status"] in status_filter]
    
    if contract_filter != "All":
        filtered_pas = [pa for pa in filtered_pas if pa["contract_name"] == contract_filter]
    
    # Apply date range filter
    today = datetime.now()
    if date_range == "Last 30 Days":
        filtered_pas = [pa for pa in filtered_pas if (today - pa["submission_date"]).days <= 30]
    elif date_range == "Last 90 Days":
        filtered_pas = [pa for pa in filtered_pas if (today - pa["submission_date"]).days <= 90]
    elif date_range == "Last 6 Months":
        filtered_pas = [pa for pa in filtered_pas if (today - pa["submission_date"]).days <= 180]
    elif date_range == "Last Year":
        filtered_pas = [pa for pa in filtered_pas if (today - pa["submission_date"]).days <= 365]
    
    # Payment application metrics
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        total_pas = len(filtered_pas)
        st.metric("Total Applications", total_pas)
    
    with metrics_col2:
        paid_pas = len([pa for pa in filtered_pas if pa["status"] == "Paid"])
        st.metric("Paid Applications", paid_pas)
    
    with metrics_col3:
        total_amount = sum(pa["amount"] for pa in filtered_pas if pa["status"] in ["Approved", "Paid"])
        st.metric("Approved Amount", f"${total_amount:,.2f}")
    
    with metrics_col4:
        retention_amount = sum(pa["retention_held"] for pa in filtered_pas if pa["status"] in ["Approved", "Paid"])
        st.metric("Retention Held", f"${retention_amount:,.2f}")
    
    # Charts
    st.subheader("Payment Application Analysis")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Status distribution chart
        status_counts = pd.DataFrame([{"Status": pa["status"]} for pa in filtered_pas])
        
        if not status_counts.empty:
            status_fig = px.pie(
                status_counts, 
                names="Status",
                title="Payment Applications by Status",
                color="Status",
                color_discrete_map={
                    "Draft": "#6c757d",
                    "Submitted": "#20c997",
                    "Under Review": "#ffc107",
                    "Approved": "#007bff",
                    "Paid": "#28a745",
                    "Rejected": "#dc3545"
                }
            )
            
            st.plotly_chart(status_fig, use_container_width=True)
        else:
            st.info("No data available for status chart")
    
    with chart_col2:
        # Payment timeline chart
        if filtered_pas:
            timeline_data = []
            for pa in filtered_pas:
                if pa["status"] == "Paid" and pa["payment_date"]:
                    timeline_data.append({
                        "Date": pa["payment_date"],
                        "Amount": pa["paid_amount"],
                        "Contract": pa["contract_name"]
                    })
            
            if timeline_data:
                timeline_df = pd.DataFrame(timeline_data)
                timeline_df = timeline_df.sort_values("Date")
                
                timeline_fig = px.line(
                    timeline_df,
                    x="Date",
                    y="Amount",
                    color="Contract",
                    title="Payment Timeline",
                    labels={"Amount": "Payment Amount ($)", "Date": "Payment Date"}
                )
                
                st.plotly_chart(timeline_fig, use_container_width=True)
            else:
                st.info("No payment data available for timeline chart")
        else:
            st.info("No data available for timeline chart")
    
    # Payment application list
    st.subheader("Payment Application List")
    
    # Sort by submission date (newest first)
    filtered_pas.sort(key=lambda x: x["submission_date"], reverse=True)
    
    for pa in filtered_pas:
        # Status color
        if pa["status"] == "Draft":
            status_color = "#6c757d"  # Gray
        elif pa["status"] == "Submitted":
            status_color = "#20c997"  # Teal
        elif pa["status"] == "Under Review":
            status_color = "#ffc107"  # Warning yellow
        elif pa["status"] == "Approved":
            status_color = "#007bff"  # Primary blue
        elif pa["status"] == "Paid":
            status_color = "#28a745"  # Green
        else:  # Rejected
            status_color = "#dc3545"  # Danger red
        
        with st.expander(f"{pa['id']} - {pa['contract_name']} - Period {pa['period_number']}", expanded=False):
            pa_col1, pa_col2 = st.columns(2)
            
            with pa_col1:
                st.markdown(f"**Contract:** {pa['contract_name']}")
                st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{pa['status']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Period:** {pa['period_start'].strftime('%Y-%m-%d')} to {pa['period_end'].strftime('%Y-%m-%d')}")
                st.markdown(f"**Submission Date:** {pa['submission_date'].strftime('%Y-%m-%d')}")
                
                if pa["payment_date"]:
                    st.markdown(f"**Payment Date:** {pa['payment_date'].strftime('%Y-%m-%d')}")
            
            with pa_col2:
                st.markdown(f"**Amount:** ${pa['amount']:,.2f}")
                st.markdown(f"**Retention Rate:** {pa['retention_rate'] * 100:.1f}%")
                st.markdown(f"**Retention Held:** ${pa['retention_held']:,.2f}")
                st.markdown(f"**Net Payment:** ${pa['paid_amount']:,.2f}")
            
            st.markdown("### Description")
            st.markdown(pa["description"])
            
            # Action buttons
            buttons_col1, buttons_col2, buttons_col3 = st.columns(3)
            
            with buttons_col1:
                st.button("Edit", key=f"edit_pa_{pa['id']}")
            
            with buttons_col2:
                action_text = ""
                if pa["status"] == "Draft":
                    action_text = "Submit for Approval"
                elif pa["status"] == "Submitted":
                    action_text = "Review"
                elif pa["status"] == "Under Review":
                    action_text = "Approve"
                elif pa["status"] == "Approved":
                    action_text = "Mark as Paid"
                
                if action_text:
                    st.button(action_text, key=f"action_pa_{pa['id']}")
            
            with buttons_col3:
                st.button("Print/Export", key=f"export_pa_{pa['id']}")
    
    # Add new payment application button
    st.divider()
    if st.button("Create New Payment Application", type="primary", key="add_pa_btn"):
        st.session_state.show_add_pa_form = True
    
    # Payment application form
    if st.session_state.get("show_add_pa_form", False):
        with st.form("pa_form"):
            st.subheader("Create New Payment Application")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                pa_contract = st.selectbox("Contract", [c["name"] for c in contracts], key="new_pa_contract")
                pa_period_start = st.date_input("Period Start Date", datetime.now() - timedelta(days=30), key="new_pa_start")
                pa_period_end = st.date_input("Period End Date", datetime.now(), key="new_pa_end")
                pa_period_number = st.number_input("Period Number", min_value=1, value=1, key="new_pa_period")
            
            with form_col2:
                pa_status = st.selectbox("Status", ["Draft", "Submitted"], key="new_pa_status")
                pa_amount = st.number_input("Amount ($)", min_value=0.0, value=0.0, step=1000.0, key="new_pa_amount")
                pa_retention_rate = st.number_input("Retention Rate (%)", min_value=0.0, max_value=10.0, value=5.0, step=1.0, key="new_pa_retention")
            
            pa_description = st.text_area("Description", "Regular monthly progress payment", key="new_pa_description")
            
            # File upload
            pa_attachments = st.file_uploader("Attachments", accept_multiple_files=True, key="new_pa_attachments")
            
            submitted = st.form_submit_button("Create Payment Application")
            
            if submitted:
                st.success("Payment application created successfully!")
                st.session_state.show_add_pa_form = False
                st.rerun()

def render_financial_summary():
    """Render the financial summary section"""
    
    st.header("Financial Summary")
    
    # Sample data for contracts
    contracts = [
        {
            "id": f"CT-{2025}-{i:03d}",
            "name": f"{random.choice(['Main Building', 'Site Work', 'Electrical', 'Plumbing', 'HVAC', 'Roofing', 'Landscaping', 'Structural', 'Concrete', 'Finishes'])} Contract",
            "vendor": random.choice([
                "Reliable Construction Inc.", "Elite Electrical Services", "Supreme Plumbing Co.", 
                "Advanced HVAC Systems", "Quality Roofing Ltd.", "Green Landscaping", 
                "Structural Masters", "Concrete Solutions", "Premium Finishes", "Global Services"
            ]),
            "type": random.choice(["Prime Contract", "Subcontract", "Purchase Order", "Services Agreement"]),
            "category": random.choice(["00-General", "02-Site Work", "03-Concrete", "05-Metals", "06-Wood & Plastics", "07-Thermal & Moisture", "08-Doors & Windows", "09-Finishes", "15-Mechanical", "16-Electrical"]),
            "original_value": round(random.uniform(50000, 2000000), 2),
            "approved_changes": round(random.uniform(-100000, 300000), 2),
            "paid_to_date": 0,  # Will be calculated
            "retention_held": 0,  # Will be calculated
        }
        for i in range(1, 21)
    ]
    
    # Calculate current contract values
    for contract in contracts:
        contract["current_value"] = contract["original_value"] + contract["approved_changes"]
        # Calculate random but realistic paid amount
        payment_progress = random.uniform(0.0, 1.0)
        contract["paid_to_date"] = contract["current_value"] * payment_progress
        # Calculate retention
        retention_rate = random.choice([0.0, 0.05, 0.1])
        contract["retention_held"] = contract["paid_to_date"] * retention_rate
        contract["paid_to_date"] -= contract["retention_held"]
        # Calculate remaining
        contract["remaining_balance"] = contract["current_value"] - contract["paid_to_date"] - contract["retention_held"]
    
    # Financial metrics
    total_contract_value = sum(c["current_value"] for c in contracts)
    total_paid = sum(c["paid_to_date"] for c in contracts)
    total_retention = sum(c["retention_held"] for c in contracts)
    total_remaining = sum(c["remaining_balance"] for c in contracts)
    
    # Calculate percentages for progress tracking
    paid_pct = (total_paid / total_contract_value) * 100 if total_contract_value > 0 else 0
    retention_pct = (total_retention / total_contract_value) * 100 if total_contract_value > 0 else 0
    remaining_pct = (total_remaining / total_contract_value) * 100 if total_contract_value > 0 else 0
    
    # Display financial overview
    st.subheader("Financial Overview")
    
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        st.metric("Total Contract Value", f"${total_contract_value:,.2f}")
    
    with metrics_col2:
        st.metric("Paid to Date", f"${total_paid:,.2f}")
    
    with metrics_col3:
        st.metric("Retention Held", f"${total_retention:,.2f}")
    
    with metrics_col4:
        st.metric("Remaining Balance", f"${total_remaining:,.2f}")
    
    # Progress bar
    st.subheader("Overall Payment Progress")
    
    # Create Stacked progress bar
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=['Progress'],
        x=[paid_pct],
        name='Paid to Date',
        orientation='h',
        marker=dict(color='#28a745'),
        text=f"${total_paid:,.2f}"
    ))
    
    fig.add_trace(go.Bar(
        y=['Progress'],
        x=[retention_pct],
        name='Retention',
        orientation='h',
        marker=dict(color='#ffc107'),
        text=f"${total_retention:,.2f}"
    ))
    
    fig.add_trace(go.Bar(
        y=['Progress'],
        x=[remaining_pct],
        name='Remaining',
        orientation='h',
        marker=dict(color='#17a2b8'),
        text=f"${total_remaining:,.2f}"
    ))
    
    fig.update_layout(
        barmode='stack',
        height=150,
        margin=dict(l=0, r=0, t=0, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(ticksuffix="%")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Charts
    st.subheader("Financial Analysis")
    
    chart_row1_col1, chart_row1_col2 = st.columns(2)
    
    with chart_row1_col1:
        # Contract Distribution by Type
        contract_types = pd.DataFrame([{"Type": c["type"], "Value": c["current_value"]} for c in contracts])
        type_grouped = contract_types.groupby("Type").sum().reset_index()
        
        type_fig = px.pie(
            type_grouped,
            values="Value",
            names="Type",
            title="Contract Value by Type",
            hole=0.4
        )
        
        st.plotly_chart(type_fig, use_container_width=True)
    
    with chart_row1_col2:
        # Contract Value by Category
        contract_categories = pd.DataFrame([{"Category": c["category"], "Value": c["current_value"]} for c in contracts])
        category_grouped = contract_categories.groupby("Category").sum().reset_index()
        
        category_fig = px.bar(
            category_grouped.sort_values("Value", ascending=False),
            x="Category",
            y="Value",
            title="Contract Value by Category",
            labels={"Value": "Contract Value ($)", "Category": "CSI Category"},
            color="Value",
            color_continuous_scale="Viridis"
        )
        
        category_fig.update_layout(xaxis_tickangle=-45)
        
        st.plotly_chart(category_fig, use_container_width=True)
    
    # Financial tables
    st.subheader("Contract Financial Summary")
    
    # Create DataFrame for better display
    contract_df = pd.DataFrame(contracts)
    
    # Format currency columns
    currency_cols = ["original_value", "approved_changes", "current_value", "paid_to_date", "retention_held", "remaining_balance"]
    for col in currency_cols:
        contract_df[col] = contract_df[col].apply(lambda x: f"${x:,.2f}")
    
    # Calculate progress percentage
    progress_data = []
    for contract in contracts:
        completed = (contract["paid_to_date"] + contract["retention_held"]) / contract["current_value"] if contract["current_value"] > 0 else 0
        progress_data.append(f"{completed * 100:.1f}%")
    
    contract_df["progress"] = progress_data
    
    # Select display columns and rename for better readability
    display_df = contract_df[["name", "vendor", "type", "original_value", "approved_changes", "current_value", "paid_to_date", "retention_held", "remaining_balance", "progress"]]
    display_df = display_df.rename(columns={
        "name": "Contract",
        "vendor": "Vendor",
        "type": "Type",
        "original_value": "Original Value",
        "approved_changes": "Changes",
        "current_value": "Current Value",
        "paid_to_date": "Paid to Date",
        "retention_held": "Retention",
        "remaining_balance": "Remaining",
        "progress": "Progress"
    })
    
    # Display as table
    st.dataframe(display_df, use_container_width=True)
    
    # Export options
    export_col1, export_col2, export_col3 = st.columns(3)
    
    with export_col1:
        st.button("Export to Excel", key="export_excel")
    
    with export_col2:
        st.button("Generate Financial Report", key="gen_report")
    
    with export_col3:
        st.button("Print Summary", key="print_summary")