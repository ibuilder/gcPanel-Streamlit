"""
Proposals Module for gcPanel

This module provides CRUD functionality for managing project proposals including:
- Proposal creation with detailed line items
- Unit pricing integration for labor, materials, and equipment
- Change order linkage capabilities
- Approval workflow and status tracking
"""

import streamlit as st
import os
import json
import random
from datetime import datetime, timedelta
import pandas as pd
import uuid

from modules.crud_template import CrudModule
from assets.crud_styler import (
    apply_crud_styles, 
    render_form_actions, 
    render_crud_fieldset,
    end_crud_detail_container
)
from app_config import PROJECT_COMPANIES

class ProposalsModule(CrudModule):
    def __init__(self):
        """Initialize the Proposals module with configuration."""
        super().__init__(
            module_name="Proposals",
            data_file_path="data/cost_management/proposals.json",
            id_field="proposal_id",
            list_columns=["proposal_id", "title", "company_name", "total_amount", "submission_date", "status"],
            default_sort_field="submission_date",
            default_sort_direction="desc",
            status_field="status",
            filter_options=["Draft", "Submitted", "In Review", "Approved", "Rejected"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        statuses = ["Draft", "Submitted", "In Review", "Approved", "Rejected"]
        proposal_types = ["Additional Work", "Scope Change", "Unforeseen Condition", "Value Engineering"]
        
        # Load unit price data for line items
        labor_rates = self._load_demo_unit_prices("labor")
        material_rates = self._load_demo_unit_prices("material")
        equipment_rates = self._load_demo_unit_prices("equipment")
        
        demo_items = []
        
        # Create several sample proposals
        for i in range(1, 16):
            # Generate sample data
            company = random.choice(PROJECT_COMPANIES)
            proposal_type = random.choice(proposal_types)
            status = random.choice(statuses)
            
            # Dates - ensure submission is before review
            days_ago = random.randint(10, 180)
            submission_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            review_date = (datetime.now() - timedelta(days=max(0, days_ago - random.randint(3, 10)))).strftime("%Y-%m-%d") if status in ["In Review", "Approved", "Rejected"] else None
            
            # Create line items
            line_items = []
            total_amount = 0
            
            # Add some labor items
            for _ in range(random.randint(1, 4)):
                if not labor_rates:
                    continue
                labor = random.choice(labor_rates)
                quantity = random.randint(8, 80)
                unit_price = labor["rate"]
                amount = quantity * unit_price
                total_amount += amount
                
                line_items.append({
                    "item_id": f"L-{uuid.uuid4().hex[:6]}",
                    "description": f"{labor['trade']} - {labor['classification']}",
                    "quantity": quantity,
                    "unit": labor["unit"],
                    "unit_price": unit_price,
                    "amount": amount,
                    "type": "Labor",
                    "reference_id": labor["rate_id"]
                })
            
            # Add some material items
            for _ in range(random.randint(1, 3)):
                if not material_rates:
                    continue
                material = random.choice(material_rates)
                quantity = random.randint(10, 100)
                unit_price = material["price"]
                amount = quantity * unit_price
                total_amount += amount
                
                line_items.append({
                    "item_id": f"M-{uuid.uuid4().hex[:6]}",
                    "description": material["material"],
                    "quantity": quantity,
                    "unit": material["unit"],
                    "unit_price": unit_price,
                    "amount": amount,
                    "type": "Material",
                    "reference_id": material["rate_id"]
                })
            
            # Add some equipment items
            for _ in range(random.randint(0, 2)):
                if not equipment_rates:
                    continue
                equipment = random.choice(equipment_rates)
                quantity = random.randint(1, 10)
                unit_price = equipment["rate"]
                amount = quantity * unit_price
                total_amount += amount
                
                line_items.append({
                    "item_id": f"E-{uuid.uuid4().hex[:6]}",
                    "description": f"{equipment['equipment']} ({equipment['rate_type']})",
                    "quantity": quantity,
                    "unit": equipment["rate_type"],
                    "unit_price": unit_price,
                    "amount": amount,
                    "type": "Equipment",
                    "reference_id": equipment["rate_id"]
                })
            
            # Add markup
            markup_percent = random.uniform(0.1, 0.2)  # 10-20% markup
            markup_amount = total_amount * markup_percent
            total_amount += markup_amount
            
            line_items.append({
                "item_id": f"MU-{uuid.uuid4().hex[:6]}",
                "description": f"Markup ({markup_percent:.1%})",
                "quantity": 1,
                "unit": "LS",
                "unit_price": markup_amount,
                "amount": markup_amount,
                "type": "Markup",
                "reference_id": None
            })
            
            # Create proposal object
            proposal = {
                "proposal_id": f"P-{i:03d}",
                "title": f"Proposal for {proposal_type} - {company['name']}",
                "company_id": company["id"],
                "company_name": company["name"],
                "proposal_type": proposal_type,
                "description": f"Proposal for additional work related to {proposal_type.lower()} requested by {company['name']}.",
                "scope_of_work": f"This proposal includes all labor, materials, and equipment required to complete the {proposal_type.lower()} as detailed in the attached drawings and specifications.",
                "submission_date": submission_date,
                "review_date": review_date,
                "expiration_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "line_items": line_items,
                "total_amount": round(total_amount, 2),
                "status": status,
                "linked_change_order_id": f"CO-{i:03d}" if status == "Approved" else None,
                "notes": f"Sample proposal for {proposal_type}"
            }
            
            demo_items.append(proposal)
        
        # Save the demo data
        self._save_items(demo_items)
    
    def _load_demo_unit_prices(self, price_type):
        """Load unit price data for demo purposes."""
        file_path = f"data/unit_prices/{price_type}_rates.json"
        
        if not os.path.exists(file_path):
            return []
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def render_detail_view(self, item_id=None):
        """Render the detail view for creating or editing a proposal."""
        # Apply consistent CRUD styling
        apply_crud_styles()
        
        is_new = item_id is None
        title = "Add New Proposal" if is_new else "Edit Proposal"
        
        # Get the current item if editing
        current_item = None
        if not is_new:
            current_item = self._get_item_by_id(item_id)
            if not current_item:
                st.error(f"Proposal with ID {item_id} not found.")
                return
        
        # Render the detail container
        actions = render_crud_detail_container(
            title=title,
            is_new=is_new,
            back_button=True
        )
        
        # Handle the back button
        if actions['back_clicked']:
            self._return_to_list_view()
            return
        
        # Create the form
        with st.form("proposal_form"):
            # Proposal Information Section
            with st.container():
                st.subheader("Proposal Information")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Proposal Title
                    title_value = st.text_input(
                        "Title",
                        value="" if is_new else current_item["title"]
                    )
                    
                    # Company
                    company_options = [company["name"] for company in PROJECT_COMPANIES]
                    company_id_map = {company["name"]: company["id"] for company in PROJECT_COMPANIES}
                    
                    selected_company = st.selectbox(
                        "Company",
                        options=company_options,
                        index=0 if is_new else (
                            company_options.index(current_item["company_name"]) 
                            if current_item["company_name"] in company_options else 0
                        )
                    )
                    
                    # Proposal Type
                    proposal_type_options = [
                        "Additional Work", 
                        "Scope Change", 
                        "Unforeseen Condition", 
                        "Value Engineering"
                    ]
                    proposal_type = st.selectbox(
                        "Proposal Type",
                        options=proposal_type_options,
                        index=0 if is_new else (
                            proposal_type_options.index(current_item["proposal_type"])
                            if current_item.get("proposal_type") in proposal_type_options else 0
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
                    
                    # Expiration Date
                    expiration_date = st.date_input(
                        "Expiration Date",
                        value=(datetime.now() + timedelta(days=30)) if is_new else (
                            datetime.strptime(current_item["expiration_date"], "%Y-%m-%d")
                            if "expiration_date" in current_item else (datetime.now() + timedelta(days=30))
                        )
                    )
                    
                    # Status
                    status_options = ["Draft", "Submitted", "In Review", "Approved", "Rejected"]
                    status = st.selectbox(
                        "Status",
                        options=status_options,
                        index=0 if is_new else status_options.index(current_item["status"])
                    )
            
            # Description and Scope
            st.subheader("Description and Scope")
            
            # Description
            description = st.text_area(
                "Description",
                value="" if is_new else current_item.get("description", "")
            )
            
            # Scope of Work
            scope_of_work = st.text_area(
                "Scope of Work",
                value="" if is_new else current_item.get("scope_of_work", "")
            )
            
            # Line Items Section
            st.subheader("Line Items")
            
            # Add placeholder for line items management
            st.info("In a production version, this would be a dynamic line item editor with unit price integration")
            
            # Simplified line items view for demo purposes
            if not is_new and "line_items" in current_item:
                line_items_df = pd.DataFrame(current_item["line_items"])
                if not line_items_df.empty:
                    st.table(line_items_df[["description", "quantity", "unit", "unit_price", "amount", "type"]])
                    st.markdown(f"**Total Amount: ${current_item['total_amount']:,.2f}**")
            
            # Change Order Linkage
            if status == "Approved":
                st.subheader("Change Order Linkage")
                
                linked_co = st.text_input(
                    "Linked Change Order ID",
                    value="" if is_new else current_item.get("linked_change_order_id", "")
                )
            else:
                linked_co = None
            
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
                if not title_value or not selected_company:
                    st.error("Title and Company are required fields.")
                else:
                    # For demo purposes, we'll create a simple proposal with some default line items
                    if is_new:
                        # Create a new proposal ID
                        proposal_id = f"P-{uuid.uuid4().hex[:6]}"
                        
                        # Create demo line items
                        line_items = [
                            {
                                "item_id": f"L-{uuid.uuid4().hex[:6]}",
                                "description": "Labor - General",
                                "quantity": 40,
                                "unit": "Hour",
                                "unit_price": 75.00,
                                "amount": 3000.00,
                                "type": "Labor",
                                "reference_id": None
                            },
                            {
                                "item_id": f"M-{uuid.uuid4().hex[:6]}",
                                "description": "Materials - General",
                                "quantity": 1,
                                "unit": "LS",
                                "unit_price": 2500.00,
                                "amount": 2500.00,
                                "type": "Material",
                                "reference_id": None
                            },
                            {
                                "item_id": f"MU-{uuid.uuid4().hex[:6]}",
                                "description": "Markup (15%)",
                                "quantity": 1,
                                "unit": "LS",
                                "unit_price": 825.00,
                                "amount": 825.00,
                                "type": "Markup",
                                "reference_id": None
                            }
                        ]
                        
                        total_amount = sum(item["amount"] for item in line_items)
                    else:
                        # Use existing values for demo
                        proposal_id = current_item["proposal_id"]
                        line_items = current_item.get("line_items", [])
                        total_amount = current_item.get("total_amount", 0)
                    
                    # Create the proposal object
                    proposal = {
                        "proposal_id": proposal_id,
                        "title": title_value,
                        "company_id": company_id_map[selected_company],
                        "company_name": selected_company,
                        "proposal_type": proposal_type,
                        "description": description,
                        "scope_of_work": scope_of_work,
                        "submission_date": submission_date.strftime("%Y-%m-%d"),
                        "expiration_date": expiration_date.strftime("%Y-%m-%d"),
                        "line_items": line_items,
                        "total_amount": total_amount,
                        "status": status,
                        "linked_change_order_id": linked_co if linked_co else None,
                        "notes": notes
                    }
                    
                    # Save the proposal
                    self._save_item(proposal)
                    
                    # Show success message and return to list
                    st.success(f"Proposal {proposal_id} saved successfully!")
                    self._return_to_list_view()
            
            if cancel_button:
                self._return_to_list_view()
        
        # Close the detail container
        end_crud_detail_container()


def render_proposals():
    """Render the proposals module."""
    proposals_module = ProposalsModule()
    
    # Get the view state
    base_key = proposals_module._get_state_key_prefix()
    current_view = st.session_state.get(f"{base_key}_view", "list")
    item_id = st.session_state.get(f"{base_key}_item_id", None)
    
    # Render the appropriate view
    if current_view == "list":
        proposals_module.render_list_view()
    elif current_view == "detail":
        proposals_module.render_detail_view(item_id)
    elif current_view == "new":
        proposals_module.render_detail_view()