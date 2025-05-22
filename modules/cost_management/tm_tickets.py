"""
Time and Material (T&M) Tickets Module for gcPanel

This module provides CRUD functionality for managing T&M tickets including:
- T&M ticket creation with detailed line items for labor, materials and equipment
- Unit pricing integration for accurate cost tracking
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
    end_crud_detail_container,
    render_crud_detail_container
)
from app_config import PROJECT_COMPANIES

class TMTicketsModule(CrudModule):
    def __init__(self):
        """Initialize the T&M Tickets module with configuration."""
        super().__init__(
            module_name="T&M Tickets",
            data_file_path="data/cost_management/tm_tickets.json",
            id_field="ticket_id",
            list_columns=["ticket_id", "description", "company_name", "work_date", "total_amount", "status"],
            default_sort_field="work_date",
            default_sort_direction="desc",
            status_field="status",
            filter_options=["Open", "Reviewed", "Approved", "Rejected", "Invoiced"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        statuses = ["Open", "Reviewed", "Approved", "Rejected", "Invoiced"]
        work_types = ["Emergency Repair", "Requested Additional Work", "Unforeseen Condition", "Site Condition"]
        locations = ["Level 1", "Level 2", "Level 3", "Basement", "Exterior", "Roof", "Mechanical Room"]
        
        # Load unit price data for line items
        labor_rates = self._load_demo_unit_prices("labor")
        material_rates = self._load_demo_unit_prices("material")
        equipment_rates = self._load_demo_unit_prices("equipment")
        
        demo_items = []
        
        # Create several sample T&M tickets
        for i in range(1, 20):
            # Generate sample data
            company = random.choice(PROJECT_COMPANIES)
            work_type = random.choice(work_types)
            status = random.choice(statuses)
            location = random.choice(locations)
            
            # Dates
            days_ago = random.randint(1, 90)
            work_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            submission_date = (datetime.now() - timedelta(days=max(0, days_ago - random.randint(1, 3)))).strftime("%Y-%m-%d")
            
            # Create line items
            line_items = []
            total_amount = 0
            
            # Add labor items
            for _ in range(random.randint(1, 3)):
                if not labor_rates:
                    continue
                labor = random.choice(labor_rates)
                hours = random.uniform(1, 8)
                hours = round(hours * 2) / 2  # Round to nearest half hour
                rate = labor["rate"]
                amount = hours * rate
                total_amount += amount
                
                line_items.append({
                    "item_id": f"L-{uuid.uuid4().hex[:6]}",
                    "description": f"{labor['trade']} - {labor['classification']}",
                    "quantity": hours,
                    "unit": "Hour",
                    "rate": rate,
                    "amount": amount,
                    "type": "Labor",
                    "reference_id": labor["rate_id"]
                })
            
            # Add material items
            for _ in range(random.randint(0, 2)):
                if not material_rates:
                    continue
                material = random.choice(material_rates)
                quantity = random.randint(1, 10)
                rate = material["price"]
                amount = quantity * rate
                total_amount += amount
                
                line_items.append({
                    "item_id": f"M-{uuid.uuid4().hex[:6]}",
                    "description": material["material"],
                    "quantity": quantity,
                    "unit": material["unit"],
                    "rate": rate,
                    "amount": amount,
                    "type": "Material",
                    "reference_id": material["rate_id"]
                })
            
            # Add equipment items if needed
            if random.random() < 0.4:  # 40% chance to add equipment
                if equipment_rates:
                    equipment = random.choice(equipment_rates)
                    quantity = random.randint(1, 4)
                    rate = equipment["rate"]
                    amount = quantity * rate
                    total_amount += amount
                    
                    line_items.append({
                        "item_id": f"E-{uuid.uuid4().hex[:6]}",
                        "description": f"{equipment['equipment']} ({equipment['rate_type']})",
                        "quantity": quantity,
                        "unit": equipment["rate_type"],
                        "rate": rate,
                        "amount": amount,
                        "type": "Equipment",
                        "reference_id": equipment["rate_id"]
                    })
            
            # Add markup (only for certain statuses)
            if status in ["Approved", "Invoiced"]:
                markup_percent = 0.15  # 15% standard markup
                markup_amount = round(total_amount * markup_percent, 2)
                total_amount += markup_amount
                
                line_items.append({
                    "item_id": f"MU-{uuid.uuid4().hex[:6]}",
                    "description": f"Markup (15%)",
                    "quantity": 1,
                    "unit": "LS",
                    "rate": markup_amount,
                    "amount": markup_amount,
                    "type": "Markup",
                    "reference_id": None
                })
            
            # Create T&M ticket object
            ticket = {
                "ticket_id": f"TM-{i:03d}",
                "description": f"{work_type} at {location}",
                "company_id": company["id"],
                "company_name": company["name"],
                "work_type": work_type,
                "location": location,
                "work_date": work_date,
                "submission_date": submission_date,
                "worker_name": f"Worker {random.randint(1, 10)}",
                "supervisor_name": f"Supervisor {random.randint(1, 5)}",
                "detailed_description": f"Time and material work performed for {work_type.lower()} at {location}. Work included necessary repairs and adjustments to restore proper function.",
                "line_items": line_items,
                "total_amount": round(total_amount, 2),
                "status": status,
                "linked_change_order_id": f"CO-{i:03d}" if status in ["Approved", "Invoiced"] else None,
                "notes": f"Sample T&M ticket for {work_type}"
            }
            
            demo_items.append(ticket)
        
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
        """Render the detail view for creating or editing a T&M ticket."""
        # Apply consistent CRUD styling
        apply_crud_styles()
        
        is_new = item_id is None
        title = "Add New T&M Ticket" if is_new else "Edit T&M Ticket"
        
        # Get the current item if editing
        current_item = None
        if not is_new:
            current_item = self._get_item_by_id(item_id)
            if not current_item:
                st.error(f"T&M Ticket with ID {item_id} not found.")
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
        with st.form("tm_ticket_form"):
            # Basic information section
            with st.container():
                st.subheader("Basic Information")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Company selection
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
                    
                    # Work Type
                    work_type_options = [
                        "Emergency Repair", 
                        "Requested Additional Work", 
                        "Unforeseen Condition", 
                        "Site Condition"
                    ]
                    work_type = st.selectbox(
                        "Work Type",
                        options=work_type_options,
                        index=0 if is_new else (
                            work_type_options.index(current_item["work_type"])
                            if current_item.get("work_type") in work_type_options else 0
                        )
                    )
                    
                    # Location
                    location_options = [
                        "Level 1", "Level 2", "Level 3", "Basement", 
                        "Exterior", "Roof", "Mechanical Room", "Other"
                    ]
                    location = st.selectbox(
                        "Location",
                        options=location_options,
                        index=0 if is_new else (
                            location_options.index(current_item["location"])
                            if current_item.get("location") in location_options else 0
                        )
                    )
                
                with col2:
                    # Work Date
                    work_date = st.date_input(
                        "Work Date",
                        value=datetime.now() if is_new else (
                            datetime.strptime(current_item["work_date"], "%Y-%m-%d") 
                            if "work_date" in current_item else datetime.now()
                        )
                    )
                    
                    # Status
                    status_options = ["Open", "Reviewed", "Approved", "Rejected", "Invoiced"]
                    status = st.selectbox(
                        "Status",
                        options=status_options,
                        index=0 if is_new else status_options.index(current_item["status"])
                    )
                    
                    # Short Description
                    short_description = st.text_input(
                        "Short Description",
                        value="" if is_new else current_item.get("description", "")
                    )
            
            # Work Details Section
            with st.container():
                st.subheader("Work Details")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Worker Name
                    worker_name = st.text_input(
                        "Worker Name",
                        value="" if is_new else current_item.get("worker_name", "")
                    )
                
                with col2:
                    # Supervisor Name
                    supervisor_name = st.text_input(
                        "Supervisor Name",
                        value="" if is_new else current_item.get("supervisor_name", "")
                    )
            
            # Detailed Description
            detailed_description = st.text_area(
                "Detailed Work Description",
                value="" if is_new else current_item.get("detailed_description", "")
            )
            
            # Line Items Section
            st.subheader("Line Items")
            
            # Add placeholder for line items management
            st.info("In a production version, this would be a dynamic line item editor with unit price integration")
            
            # Simplified line items view for demo purposes
            if not is_new and "line_items" in current_item:
                line_items_df = pd.DataFrame(current_item["line_items"])
                if not line_items_df.empty:
                    st.table(line_items_df[["description", "quantity", "unit", "rate", "amount", "type"]])
                    st.markdown(f"**Total Amount: ${current_item['total_amount']:,.2f}**")
            
            # Change Order Linkage
            if status in ["Approved", "Invoiced"]:
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
                if not short_description or not selected_company:
                    st.error("Description and Company are required fields.")
                else:
                    # For demo purposes, we'll create a simple T&M ticket with some default line items
                    if is_new:
                        # Create a new ticket ID
                        ticket_id = f"TM-{uuid.uuid4().hex[:6]}"
                        
                        # Create demo line items
                        line_items = [
                            {
                                "item_id": f"L-{uuid.uuid4().hex[:6]}",
                                "description": "Carpenter - Journeyman",
                                "quantity": 4.5,
                                "unit": "Hour",
                                "rate": 65.00,
                                "amount": 292.50,
                                "type": "Labor",
                                "reference_id": None
                            },
                            {
                                "item_id": f"M-{uuid.uuid4().hex[:6]}",
                                "description": "Lumber and Fasteners",
                                "quantity": 1,
                                "unit": "LS",
                                "rate": 125.00,
                                "amount": 125.00,
                                "type": "Material",
                                "reference_id": None
                            },
                            {
                                "item_id": f"MU-{uuid.uuid4().hex[:6]}",
                                "description": "Markup (15%)",
                                "quantity": 1,
                                "unit": "LS",
                                "rate": 62.63,
                                "amount": 62.63,
                                "type": "Markup",
                                "reference_id": None
                            }
                        ]
                        
                        total_amount = sum(item["amount"] for item in line_items)
                    else:
                        # Use existing values for demo
                        ticket_id = current_item["ticket_id"]
                        line_items = current_item.get("line_items", [])
                        total_amount = current_item.get("total_amount", 0)
                    
                    # Create the T&M ticket object
                    ticket = {
                        "ticket_id": ticket_id,
                        "description": short_description,
                        "company_id": company_id_map[selected_company],
                        "company_name": selected_company,
                        "work_type": work_type,
                        "location": location,
                        "work_date": work_date.strftime("%Y-%m-%d"),
                        "submission_date": datetime.now().strftime("%Y-%m-%d"),
                        "worker_name": worker_name,
                        "supervisor_name": supervisor_name,
                        "detailed_description": detailed_description,
                        "line_items": line_items,
                        "total_amount": total_amount,
                        "status": status,
                        "linked_change_order_id": linked_co if linked_co else None,
                        "notes": notes
                    }
                    
                    # Save the ticket
                    self._save_item(ticket)
                    
                    # Show success message and return to list
                    st.success(f"T&M Ticket {ticket_id} saved successfully!")
                    self._return_to_list_view()
            
            if cancel_button:
                self._return_to_list_view()
        
        # Close the detail container
        end_crud_detail_container()


def render_tm_tickets():
    """Render the T&M tickets module."""
    tm_tickets_module = TMTicketsModule()
    
    # Get the view state
    base_key = tm_tickets_module._get_state_key_prefix()
    current_view = st.session_state.get(f"{base_key}_view", "list")
    item_id = st.session_state.get(f"{base_key}_item_id", None)
    
    # Render the appropriate view
    if current_view == "list":
        tm_tickets_module.render_list_view()
    elif current_view == "detail":
        tm_tickets_module.render_detail_view(item_id)
    elif current_view == "new":
        tm_tickets_module.render_detail_view()