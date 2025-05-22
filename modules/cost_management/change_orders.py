"""
Change Orders Module for gcPanel

This module provides CRUD functionality for managing change orders including:
- Change order creation with detailed line items
- Integration with Proposals and T&M tickets
- Approval workflow and status tracking
- Financial impact analysis
"""

import streamlit as st
import os
import json
import random
from datetime import datetime, timedelta
import pandas as pd
import uuid

from modules.crud_template import CrudModule
from components.digital_signature import render_digital_signature_section, get_signature_summary, validate_required_signatures
from assets.crud_styler import (
    apply_crud_styles, 
    render_form_actions, 
    render_crud_fieldset,
    end_crud_detail_container,
    render_crud_detail_container
)
from app_config import PROJECT_COMPANIES

class ChangeOrdersModule(CrudModule):
    def __init__(self):
        """Initialize the Change Orders module with configuration."""
        super().__init__(
            module_name="Change Orders",
            data_file_path="data/cost_management/change_orders.json",
            id_field="co_id",
            list_columns=["co_id", "title", "company_name", "total_amount", "submission_date", "status"],
            default_sort_field="submission_date",
            default_sort_direction="desc",
            status_field="status",
            filter_options=["Draft", "Pending Approval", "Approved", "Rejected"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        statuses = ["Draft", "Pending Approval", "Approved", "Rejected"]
        co_types = ["Additional Work", "Scope Change", "Unforeseen Condition", "Client Request"]
        
        # Load proposals and T&M tickets to link them
        proposals = self._load_proposal_data()
        tm_tickets = self._load_tm_ticket_data()
        
        demo_items = []
        
        # Create sample change orders
        for i in range(1, 16):
            # Generate sample data
            company = random.choice(PROJECT_COMPANIES)
            co_type = random.choice(co_types)
            status = random.choice(statuses)
            
            # Dates
            days_ago = random.randint(10, 150)
            submission_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            approval_date = (datetime.now() - timedelta(days=max(0, days_ago - random.randint(3, 10)))).strftime("%Y-%m-%d") if status == "Approved" else None
            
            # Linked items
            linked_proposals = []
            linked_tm_tickets = []
            
            # Link some proposals (if available)
            if proposals and random.random() < 0.7:  # 70% chance to link proposals
                num_proposals = random.randint(1, min(3, len(proposals)))
                selected_proposals = random.sample(proposals, num_proposals)
                for proposal in selected_proposals:
                    linked_proposals.append({
                        "proposal_id": proposal["proposal_id"],
                        "title": proposal["title"],
                        "amount": proposal["total_amount"]
                    })
            
            # Link some T&M tickets (if available)
            if tm_tickets and random.random() < 0.6:  # 60% chance to link T&M tickets
                num_tickets = random.randint(1, min(2, len(tm_tickets)))
                selected_tickets = random.sample(tm_tickets, num_tickets)
                for ticket in selected_tickets:
                    linked_tm_tickets.append({
                        "ticket_id": ticket["ticket_id"],
                        "description": ticket["description"],
                        "amount": ticket["total_amount"]
                    })
            
            # Calculate total amount from linked items
            linked_items_total = (
                sum(item["amount"] for item in linked_proposals) +
                sum(item["amount"] for item in linked_tm_tickets)
            )
            
            # Add some markup for some change orders
            markup_percent = 0
            markup_amount = 0
            if random.random() < 0.4:  # 40% chance to add markup
                markup_percent = random.uniform(0.05, 0.15)  # 5-15% markup
                markup_amount = linked_items_total * markup_percent
            
            total_amount = linked_items_total + markup_amount
            
            # Create change order object
            change_order = {
                "co_id": f"CO-{i:03d}",
                "title": f"Change Order for {co_type} - {company['name']}",
                "company_id": company["id"],
                "company_name": company["name"],
                "co_type": co_type,
                "description": f"Change order for {co_type.lower()} with {company['name']}",
                "justification": f"This change order is required due to {co_type.lower()} that occurred during construction.",
                "submission_date": submission_date,
                "approval_date": approval_date,
                "linked_proposals": linked_proposals,
                "linked_tm_tickets": linked_tm_tickets,
                "markup_percent": markup_percent * 100,  # Store as actual percentage
                "markup_amount": markup_amount,
                "items_total": linked_items_total,
                "total_amount": total_amount,
                "status": status,
                "approver": "Project Manager" if status in ["Approved", "Rejected"] else None,
                "notes": f"Sample change order for {co_type}"
            }
            
            demo_items.append(change_order)
        
        # Save the demo data
        self._save_items(demo_items)
    
    def _load_proposal_data(self):
        """Load proposal data for linking with change orders."""
        file_path = "data/cost_management/proposals.json"
        
        if not os.path.exists(file_path):
            return []
        
        try:
            with open(file_path, 'r') as f:
                proposals = json.load(f)
                # Only use approved proposals for linking
                return [p for p in proposals if p.get("status") == "Approved"]
        except:
            return []
    
    def _load_tm_ticket_data(self):
        """Load T&M ticket data for linking with change orders."""
        file_path = "data/cost_management/tm_tickets.json"
        
        if not os.path.exists(file_path):
            return []
        
        try:
            with open(file_path, 'r') as f:
                tickets = json.load(f)
                # Only use approved tickets for linking
                return [t for t in tickets if t.get("status") in ["Approved", "Invoiced"]]
        except:
            return []
    
    def render_detail_view(self, item_id=None):
        """Render the detail view for creating or editing a change order."""
        # Apply consistent CRUD styling
        apply_crud_styles()
        
        is_new = item_id is None
        title = "Add New Change Order" if is_new else "Edit Change Order"
        
        # Get the current item if editing
        current_item = None
        if not is_new:
            current_item = self._get_item_by_id(item_id)
            if not current_item:
                st.error(f"Change Order with ID {item_id} not found.")
                return
        
        # Render the detail container
        actions = render_crud_detail_container(
            title=title,
            is_new=is_new,
            back_button=True
        )
        
        # Handle the back button
        if actions['back_clicked']:
            self.return_to_list_view()
            return
        
        # Create the form
        with st.form("change_order_form"):
            # Basic Information Section
            with st.container():
                st.subheader("Basic Information")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Change Order Title
                    co_title = st.text_input(
                        "Title",
                        value="" if is_new else current_item.get("title", "")
                    )
                    
                    # Company
                    company_options = [company["name"] for company in PROJECT_COMPANIES]
                    company_id_map = {company["name"]: company["id"] for company in PROJECT_COMPANIES}
                    
                    selected_company = st.selectbox(
                        "Company",
                        options=company_options,
                        index=0 if is_new else (
                            company_options.index(current_item["company_name"]) 
                            if current_item.get("company_name") in company_options else 0
                        )
                    )
                    
                    # Change Order Type
                    co_type_options = [
                        "Additional Work", 
                        "Scope Change", 
                        "Unforeseen Condition", 
                        "Client Request"
                    ]
                    co_type = st.selectbox(
                        "Change Order Type",
                        options=co_type_options,
                        index=0 if is_new else (
                            co_type_options.index(current_item["co_type"])
                            if current_item.get("co_type") in co_type_options else 0
                        )
                    )
                
                with col2:
                    # Submission Date
                    submission_date = st.date_input(
                        "Submission Date",
                        value=datetime.now() if is_new else (
                            datetime.strptime(current_item["submission_date"], "%Y-%m-%d") 
                            if "submission_date" in current_item else datetime.now()
                        )
                    )
                    
                    # Status
                    status_options = ["Draft", "Pending Approval", "Approved", "Rejected"]
                    status = st.selectbox(
                        "Status",
                        options=status_options,
                        index=0 if is_new else status_options.index(current_item.get("status", "Draft"))
                    )
                    
                    # Approval Date (if approved)
                    if status == "Approved":
                        approval_date = st.date_input(
                            "Approval Date",
                            value=datetime.now() if is_new else (
                                datetime.strptime(current_item.get("approval_date", submission_date.strftime("%Y-%m-%d")), "%Y-%m-%d")
                            )
                        )
                    else:
                        approval_date = None
            
            # Description and Justification
            st.subheader("Description and Justification")
            
            # Description
            description = st.text_area(
                "Description",
                value="" if is_new else current_item.get("description", "")
            )
            
            # Justification
            justification = st.text_area(
                "Justification",
                value="" if is_new else current_item.get("justification", "")
            )
            
            # Linked Items Section
            st.subheader("Linked Items")
            
            # For demonstration purposes, just show a placeholder for linking items
            if is_new:
                st.info("In a production version, you would be able to select proposals and T&M tickets to link to this change order")
                
                # Simple mock linked items for demo
                linked_proposals_df = pd.DataFrame([
                    {"proposal_id": "P-001", "title": "Additional HVAC Work", "amount": 12500.00},
                    {"proposal_id": "P-003", "title": "Electrical System Upgrade", "amount": 8750.00}
                ])
                linked_tm_tickets_df = pd.DataFrame([
                    {"ticket_id": "TM-002", "description": "Emergency Repair at Level 2", "amount": 1850.00}
                ])
                
                total_linked = linked_proposals_df["amount"].sum() + linked_tm_tickets_df["amount"].sum()
                
                st.subheader("Linked Proposals")
                st.dataframe(linked_proposals_df, hide_index=True)
                
                st.subheader("Linked T&M Tickets")
                st.dataframe(linked_tm_tickets_df, hide_index=True)
                
                markup_percent = st.slider("Markup Percentage", min_value=0.0, max_value=20.0, value=10.0, step=0.5)
                markup_amount = total_linked * (markup_percent / 100)
                
                st.subheader("Change Order Total")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Items Total", f"${total_linked:,.2f}")
                with col2:
                    st.metric("Markup", f"${markup_amount:,.2f}")
                with col3:
                    st.metric("Total Amount", f"${(total_linked + markup_amount):,.2f}")
                
            else:
                # Show linked proposals if any
                if current_item.get("linked_proposals"):
                    st.subheader("Linked Proposals")
                    linked_proposals_df = pd.DataFrame(current_item["linked_proposals"])
                    st.dataframe(linked_proposals_df[["proposal_id", "title", "amount"]], hide_index=True)
                
                # Show linked T&M tickets if any
                if current_item.get("linked_tm_tickets"):
                    st.subheader("Linked T&M Tickets")
                    linked_tm_tickets_df = pd.DataFrame(current_item["linked_tm_tickets"])
                    st.dataframe(linked_tm_tickets_df[["ticket_id", "description", "amount"]], hide_index=True)
                
                # Show the totals
                st.subheader("Change Order Total")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Items Total", f"${current_item.get('items_total', 0):,.2f}")
                with col2:
                    st.metric("Markup", f"${current_item.get('markup_amount', 0):,.2f}")
                with col3:
                    st.metric("Total Amount", f"${current_item.get('total_amount', 0):,.2f}")
            
            # Additional Information
            st.subheader("Additional Information")
            
            # Approver (if applicable)
            if status in ["Approved", "Rejected"]:
                approver = st.text_input(
                    "Approver",
                    value="" if is_new else current_item.get("approver", "")
                )
            else:
                approver = None
            
            # Notes
            notes = st.text_area(
                "Notes",
                value="" if is_new else current_item.get("notes", "")
            )
            
            # Form actions
            col1, col2 = st.columns(2)
            with col1:
                submit_button = st.form_submit_button("Save", type="primary")
            with col2:
                cancel_button = st.form_submit_button("Cancel")
            
            # Handle form submission
            if submit_button:
                if not co_title or not selected_company:
                    st.error("Title and Company are required fields.")
                else:
                    # For demo purposes, we'll create a simple change order with some defaults
                    if is_new:
                        # Create a new change order ID
                        co_id = f"CO-{uuid.uuid4().hex[:6]}"
                        
                        # Use the mocked linked items from above
                        linked_proposals = [
                            {"proposal_id": "P-001", "title": "Additional HVAC Work", "amount": 12500.00},
                            {"proposal_id": "P-003", "title": "Electrical System Upgrade", "amount": 8750.00}
                        ]
                        linked_tm_tickets = [
                            {"ticket_id": "TM-002", "description": "Emergency Repair at Level 2", "amount": 1850.00}
                        ]
                        
                        items_total = 23100.00  # Sum of linked items
                        markup_percent_value = 10.0
                        markup_amount_value = 2310.00
                        total_amount = 25410.00
                    else:
                        # Use existing values
                        co_id = current_item["co_id"]
                        linked_proposals = current_item.get("linked_proposals", [])
                        linked_tm_tickets = current_item.get("linked_tm_tickets", [])
                        items_total = current_item.get("items_total", 0)
                        markup_percent_value = current_item.get("markup_percent", 0)
                        markup_amount_value = current_item.get("markup_amount", 0)
                        total_amount = current_item.get("total_amount", 0)
                    
                    # Create the change order object
                    change_order = {
                        "co_id": co_id,
                        "title": co_title,
                        "company_id": company_id_map[selected_company],
                        "company_name": selected_company,
                        "co_type": co_type,
                        "description": description,
                        "justification": justification,
                        "submission_date": submission_date.strftime("%Y-%m-%d"),
                        "approval_date": approval_date.strftime("%Y-%m-%d") if approval_date else None,
                        "linked_proposals": linked_proposals,
                        "linked_tm_tickets": linked_tm_tickets,
                        "markup_percent": markup_percent_value,
                        "markup_amount": markup_amount_value,
                        "items_total": items_total,
                        "total_amount": total_amount,
                        "status": status,
                        "approver": approver,
                        "notes": notes
                    }
                    
                    # Add digital signatures section
                    signatures = render_digital_signature_section("change_order", ["Project Manager", "Owner Representative"])
                    
                    # Validate signatures before saving
                    is_valid, message = validate_required_signatures(signatures, ["Project Manager", "Owner Representative"])
                    if is_valid:
                        # Add signature data to change order
                        change_order["signatures"] = get_signature_summary(signatures)
                        
                        # Save the change order
                        self._save_item(change_order)
                        
                        # Show success message and return to list
                        st.success(f"Change Order {co_id} saved successfully with digital signatures!")
                        self._return_to_list_view()
                    else:
                        st.error(f"Cannot save change order: {message}")
            
            if cancel_button:
                self._return_to_list_view()
        
        # Close the detail container
        end_crud_detail_container()


def render_change_orders():
    """Render the change orders module."""
    change_orders_module = ChangeOrdersModule()
    
    # Get the view state
    base_key = change_orders_module._get_state_key_prefix()
    current_view = st.session_state.get(f"{base_key}_view", "list")
    item_id = st.session_state.get(f"{base_key}_item_id", None)
    
    # Render the appropriate view
    if current_view == "list":
        change_orders_module.render_list_view()
    elif current_view == "detail":
        change_orders_module.render_detail_view(item_id)
    elif current_view == "new":
        change_orders_module.render_detail_view()