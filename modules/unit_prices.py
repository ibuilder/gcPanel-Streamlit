"""
Unit Prices Module for gcPanel

This module provides CRUD functionality for managing unit prices including:
- Labor rates by trade and company
- Material rates by type and supplier
- Equipment rates by type and company

All pricing information is stored with company relationships for proper tracking and analysis.
"""

import streamlit as st
import os
import json
from datetime import datetime, timedelta
import pandas as pd
import uuid

from modules.crud_template import CrudModule
from assets.crud_styler import (
    apply_crud_styles, 
    render_form_actions, 
    render_crud_fieldset
)
from app_config import PROJECT_COMPANIES

class LaborRatesModule(CrudModule):
    def __init__(self):
        """Initialize the Labor Rates module with configuration."""
        super().__init__(
            module_name="Labor Rates",
            data_file_path="data/unit_prices/labor_rates.json",
            id_field="rate_id",
            list_columns=["trade", "company_name", "classification", "rate", "unit", "effective_date", "status"],
            default_sort_field="trade",
            default_sort_direction="asc",
            status_field="status",
            filter_options=["Active", "Archive", "Pending"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        trades = [
            "Carpenter", "Electrician", "Plumber", "HVAC Technician", 
            "Ironworker", "Mason", "Painter", "Laborer",
            "Operator", "Roofer", "Glazier", "Concrete Finisher"
        ]
        
        classifications = [
            "Journeyman", "Apprentice", "Foreman", "General Foreman",
            "Helper", "Master", "Supervisor"
        ]
        
        units = ["Hour", "Day", "Week"]
        
        demo_items = []
        
        # Create several sample labor rates for different companies
        for i, company in enumerate(PROJECT_COMPANIES):
            # Each company gets some trades
            company_trades = random.sample(trades, min(5, len(trades)))
            
            for j, trade in enumerate(company_trades):
                # For each trade, add a few classifications
                trade_classifications = random.sample(classifications, min(3, len(classifications)))
                
                for k, classification in enumerate(trade_classifications):
                    # Base rate varies by trade and classification
                    base_rate = 30 + (trades.index(trade) * 2) + (classifications.index(classification) * 5)
                    
                    # Add some randomness to the rate
                    rate = base_rate + random.uniform(-5, 5)
                    
                    # Create a unique ID
                    rate_id = f"LR-{i+1:03d}-{j+1:02d}-{k+1:02d}"
                    
                    # Effective date (random date in the past year)
                    days_ago = random.randint(0, 365)
                    effective_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
                    
                    # Sample item
                    demo_items.append({
                        "rate_id": rate_id,
                        "company_id": company["id"],
                        "company_name": company["name"],
                        "trade": trade,
                        "classification": classification,
                        "rate": round(rate, 2),
                        "unit": "Hour",  # Most labor rates are per hour
                        "overtime_multiplier": 1.5,
                        "double_time_multiplier": 2.0,
                        "effective_date": effective_date,
                        "expiration_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                        "notes": f"Standard {classification} rate for {trade}",
                        "status": "Active"
                    })
        
        # Save the demo data
        self._save_items(demo_items)
    
    def render_detail_view(self, item_id=None):
        """Render the detail view for creating or editing a labor rate."""
        # Apply consistent CRUD styling
        apply_crud_styles()
        
        is_new = item_id is None
        title = "Add New Labor Rate" if is_new else "Edit Labor Rate"
        
        # Get the current item if editing
        current_item = None
        if not is_new:
            current_item = self._get_item_by_id(item_id)
            if not current_item:
                st.error(f"Labor Rate with ID {item_id} not found.")
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
        with st.form("labor_rate_form"):
            # Basic information fieldset
            with st.container():
                st.subheader("Basic Information")
                
                # Two columns for the form
                col1, col2 = st.columns(2)
                
                with col1:
                    # Company selection (from project companies)
                    company_options = [company["name"] for company in PROJECT_COMPANIES]
                    company_id_map = {company["name"]: company["id"] for company in PROJECT_COMPANIES}
                    
                    selected_company = st.selectbox(
                        "Company",
                        options=company_options,
                        index=0 if is_new else company_options.index(current_item["company_name"])
                    )
                    
                    # Trade input
                    trade = st.text_input(
                        "Trade",
                        value="" if is_new else current_item["trade"]
                    )
                    
                    # Classification input
                    classification = st.text_input(
                        "Classification",
                        value="" if is_new else current_item["classification"]
                    )
                
                with col2:
                    # Rate input
                    rate = st.number_input(
                        "Rate ($)",
                        min_value=0.0,
                        max_value=1000.0,
                        value=0.0 if is_new else current_item["rate"],
                        step=0.01,
                        format="%.2f"
                    )
                    
                    # Unit selection
                    unit_options = ["Hour", "Day", "Week"]
                    unit = st.selectbox(
                        "Unit",
                        options=unit_options,
                        index=0 if is_new else unit_options.index(current_item["unit"])
                    )
                    
                    # Status selection
                    status_options = ["Active", "Archive", "Pending"]
                    status = st.selectbox(
                        "Status",
                        options=status_options,
                        index=0 if is_new else status_options.index(current_item["status"])
                    )
            
            # Additional details fieldset
            with st.container():
                st.subheader("Rate Details")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Overtime multiplier
                    overtime_multiplier = st.number_input(
                        "Overtime Multiplier",
                        min_value=1.0,
                        max_value=3.0,
                        value=1.5 if is_new else current_item.get("overtime_multiplier", 1.5),
                        step=0.1,
                        format="%.1f"
                    )
                    
                    # Double time multiplier
                    double_time_multiplier = st.number_input(
                        "Double Time Multiplier",
                        min_value=1.0,
                        max_value=4.0,
                        value=2.0 if is_new else current_item.get("double_time_multiplier", 2.0),
                        step=0.1,
                        format="%.1f"
                    )
                
                with col2:
                    # Effective date
                    effective_date = st.date_input(
                        "Effective Date",
                        value=datetime.now() if is_new else datetime.strptime(current_item["effective_date"], "%Y-%m-%d")
                    )
                    
                    # Expiration date (optional)
                    expiration_date = st.date_input(
                        "Expiration Date (Optional)",
                        value=(datetime.now() + timedelta(days=365)) if is_new else (
                            datetime.strptime(current_item["expiration_date"], "%Y-%m-%d") 
                            if "expiration_date" in current_item else (datetime.now() + timedelta(days=365))
                        )
                    )
            
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
                if not trade or not selected_company:
                    st.error("Trade and Company are required fields.")
                else:
                    # Create or update the item
                    item = {
                        "rate_id": str(uuid.uuid4())[:8] if is_new else current_item["rate_id"],
                        "company_id": company_id_map[selected_company],
                        "company_name": selected_company,
                        "trade": trade,
                        "classification": classification,
                        "rate": float(rate),
                        "unit": unit,
                        "overtime_multiplier": float(overtime_multiplier),
                        "double_time_multiplier": float(double_time_multiplier),
                        "effective_date": effective_date.strftime("%Y-%m-%d"),
                        "expiration_date": expiration_date.strftime("%Y-%m-%d"),
                        "notes": notes,
                        "status": status
                    }
                    
                    # Save the item
                    self._save_item(item)
                    
                    # Show success message and return to list
                    st.success(f"Labor rate for {trade} ({classification}) saved successfully!")
                    self._return_to_list_view()
            
            if cancel_button:
                self._return_to_list_view()
        
        # Close the detail container
        end_crud_detail_container()


class MaterialRatesModule(CrudModule):
    def __init__(self):
        """Initialize the Material Rates module with configuration."""
        super().__init__(
            module_name="Material Rates",
            data_file_path="data/unit_prices/material_rates.json",
            id_field="rate_id",
            list_columns=["material", "category", "supplier", "price", "unit", "effective_date", "status"],
            default_sort_field="material",
            default_sort_direction="asc",
            status_field="status",
            filter_options=["Active", "Archive", "Pending"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        materials = [
            "Concrete (4000 PSI)", "Steel Rebar (#4)", "Framing Lumber (2x4)", 
            "Drywall (5/8\")", "Copper Pipe (1\")", "Electrical Wire (12 AWG)",
            "Paint (Interior Latex)", "Insulation (R-19)", "Plywood (3/4\")",
            "Carpet (Commercial)", "Ceramic Tile", "Brick (Standard)"
        ]
        
        categories = [
            "Concrete", "Steel", "Lumber", "Finishes", "Plumbing", "Electrical",
            "Thermal", "Flooring", "Masonry"
        ]
        
        units = ["CY", "LF", "SF", "EA", "GAL", "TON", "SQFT"]
        
        suppliers = [
            "ABC Supply Co.", "Builder's First Source", "Construction Materials Inc.",
            "Highland Materials", "City Electric Supply", "Modern Plumbing Supply"
        ]
        
        material_category_map = {
            "Concrete (4000 PSI)": "Concrete",
            "Steel Rebar (#4)": "Steel",
            "Framing Lumber (2x4)": "Lumber",
            "Drywall (5/8\")": "Finishes",
            "Copper Pipe (1\")": "Plumbing",
            "Electrical Wire (12 AWG)": "Electrical",
            "Paint (Interior Latex)": "Finishes",
            "Insulation (R-19)": "Thermal",
            "Plywood (3/4\")": "Lumber",
            "Carpet (Commercial)": "Flooring",
            "Ceramic Tile": "Flooring",
            "Brick (Standard)": "Masonry"
        }
        
        material_unit_map = {
            "Concrete (4000 PSI)": "CY",
            "Steel Rebar (#4)": "LF",
            "Framing Lumber (2x4)": "LF",
            "Drywall (5/8\")": "SF",
            "Copper Pipe (1\")": "LF",
            "Electrical Wire (12 AWG)": "LF",
            "Paint (Interior Latex)": "GAL",
            "Insulation (R-19)": "SF",
            "Plywood (3/4\")": "SF",
            "Carpet (Commercial)": "SQFT",
            "Ceramic Tile": "SF",
            "Brick (Standard)": "EA"
        }
        
        demo_items = []
        
        # Create several sample material rates
        for i, material in enumerate(materials):
            # Each material gets prices from multiple suppliers
            material_suppliers = random.sample(suppliers, min(3, len(suppliers)))
            
            for j, supplier in enumerate(material_suppliers):
                # Base price varies by material
                if material in ["Concrete (4000 PSI)", "Steel Rebar (#4)"]:
                    base_price = 100 + random.uniform(-20, 20)
                elif material in ["Framing Lumber (2x4)", "Copper Pipe (1\")", "Electrical Wire (12 AWG)"]:
                    base_price = 30 + random.uniform(-5, 5)
                else:
                    base_price = 10 + random.uniform(-2, 2)
                
                # Create a unique ID
                rate_id = f"MR-{i+1:03d}-{j+1:02d}"
                
                # Effective date (random date in the past year)
                days_ago = random.randint(0, 365)
                effective_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
                
                # Sample item
                demo_items.append({
                    "rate_id": rate_id,
                    "material": material,
                    "category": material_category_map.get(material, "Miscellaneous"),
                    "supplier": supplier,
                    "price": round(base_price, 2),
                    "unit": material_unit_map.get(material, "EA"),
                    "minimum_order": 1,
                    "lead_time_days": random.randint(1, 14),
                    "effective_date": effective_date,
                    "expiration_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                    "notes": f"Standard pricing for {material}",
                    "status": "Active"
                })
        
        # Save the demo data
        self._save_items(demo_items)
    
    def render_detail_view(self, item_id=None):
        """Render the detail view for creating or editing a material rate."""
        # Apply consistent CRUD styling
        apply_crud_styles()
        
        is_new = item_id is None
        title = "Add New Material Rate" if is_new else "Edit Material Rate"
        
        # Get the current item if editing
        current_item = None
        if not is_new:
            current_item = self._get_item_by_id(item_id)
            if not current_item:
                st.error(f"Material Rate with ID {item_id} not found.")
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
        with st.form("material_rate_form"):
            # Basic information fieldset
            with st.container():
                st.subheader("Basic Information")
                
                # Two columns for the form
                col1, col2 = st.columns(2)
                
                with col1:
                    # Material name input
                    material = st.text_input(
                        "Material",
                        value="" if is_new else current_item["material"]
                    )
                    
                    # Category selection
                    category_options = [
                        "Concrete", "Steel", "Lumber", "Finishes", "Plumbing", "Electrical",
                        "Thermal", "Flooring", "Masonry", "Miscellaneous"
                    ]
                    category = st.selectbox(
                        "Category",
                        options=category_options,
                        index=0 if is_new else (
                            category_options.index(current_item["category"]) 
                            if current_item.get("category") in category_options else 0
                        )
                    )
                    
                    # Supplier input
                    supplier = st.text_input(
                        "Supplier",
                        value="" if is_new else current_item["supplier"]
                    )
                
                with col2:
                    # Price input
                    price = st.number_input(
                        "Price ($)",
                        min_value=0.0,
                        max_value=10000.0,
                        value=0.0 if is_new else current_item["price"],
                        step=0.01,
                        format="%.2f"
                    )
                    
                    # Unit selection
                    unit_options = ["CY", "LF", "SF", "EA", "GAL", "TON", "SQFT", "LS"]
                    unit = st.selectbox(
                        "Unit",
                        options=unit_options,
                        index=0 if is_new else (
                            unit_options.index(current_item["unit"]) 
                            if current_item.get("unit") in unit_options else 0
                        )
                    )
                    
                    # Status selection
                    status_options = ["Active", "Archive", "Pending"]
                    status = st.selectbox(
                        "Status",
                        options=status_options,
                        index=0 if is_new else status_options.index(current_item["status"])
                    )
            
            # Additional details fieldset
            with st.container():
                st.subheader("Order Details")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Minimum order
                    minimum_order = st.number_input(
                        "Minimum Order",
                        min_value=1,
                        value=1 if is_new else current_item.get("minimum_order", 1)
                    )
                    
                    # Lead time
                    lead_time_days = st.number_input(
                        "Lead Time (days)",
                        min_value=0,
                        value=1 if is_new else current_item.get("lead_time_days", 1)
                    )
                
                with col2:
                    # Effective date
                    effective_date = st.date_input(
                        "Effective Date",
                        value=datetime.now() if is_new else datetime.strptime(current_item["effective_date"], "%Y-%m-%d")
                    )
                    
                    # Expiration date (optional)
                    expiration_date = st.date_input(
                        "Expiration Date (Optional)",
                        value=(datetime.now() + timedelta(days=365)) if is_new else (
                            datetime.strptime(current_item["expiration_date"], "%Y-%m-%d") 
                            if "expiration_date" in current_item else (datetime.now() + timedelta(days=365))
                        )
                    )
            
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
                if not material or not supplier:
                    st.error("Material and Supplier are required fields.")
                else:
                    # Create or update the item
                    item = {
                        "rate_id": str(uuid.uuid4())[:8] if is_new else current_item["rate_id"],
                        "material": material,
                        "category": category,
                        "supplier": supplier,
                        "price": float(price),
                        "unit": unit,
                        "minimum_order": int(minimum_order),
                        "lead_time_days": int(lead_time_days),
                        "effective_date": effective_date.strftime("%Y-%m-%d"),
                        "expiration_date": expiration_date.strftime("%Y-%m-%d"),
                        "notes": notes,
                        "status": status
                    }
                    
                    # Save the item
                    self._save_item(item)
                    
                    # Show success message and return to list
                    st.success(f"Material rate for {material} saved successfully!")
                    self._return_to_list_view()
            
            if cancel_button:
                self._return_to_list_view()
        
        # Close the detail container
        end_crud_detail_container()


class EquipmentRatesModule(CrudModule):
    def __init__(self):
        """Initialize the Equipment Rates module with configuration."""
        super().__init__(
            module_name="Equipment Rates",
            data_file_path="data/unit_prices/equipment_rates.json",
            id_field="rate_id",
            list_columns=["equipment", "type", "company_name", "rate", "rate_type", "effective_date", "status"],
            default_sort_field="equipment",
            default_sort_direction="asc",
            status_field="status",
            filter_options=["Active", "Archive", "Pending"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        equipment_list = [
            "Excavator (Medium)", "Bulldozer (D6)", "Crane (50-ton)", 
            "Concrete Pump", "Skid Steer", "Backhoe",
            "Forklift (10K lb)", "Scissor Lift", "Boom Lift",
            "Generator (100kW)", "Compressor (185 CFM)", "Dump Truck (12 CY)"
        ]
        
        equipment_types = [
            "Earthmoving", "Lifting", "Concrete", "Material Handling", "Power", "Transportation"
        ]
        
        rate_types = ["Hour", "Day", "Week", "Month"]
        
        equipment_type_map = {
            "Excavator (Medium)": "Earthmoving",
            "Bulldozer (D6)": "Earthmoving",
            "Crane (50-ton)": "Lifting",
            "Concrete Pump": "Concrete",
            "Skid Steer": "Earthmoving",
            "Backhoe": "Earthmoving",
            "Forklift (10K lb)": "Material Handling",
            "Scissor Lift": "Lifting",
            "Boom Lift": "Lifting",
            "Generator (100kW)": "Power",
            "Compressor (185 CFM)": "Power",
            "Dump Truck (12 CY)": "Transportation"
        }
        
        demo_items = []
        
        # Create several sample equipment rates for different companies
        for i, company in enumerate(PROJECT_COMPANIES):
            # Each company offers some equipment
            company_equipment = random.sample(equipment_list, min(5, len(equipment_list)))
            
            for j, equipment in enumerate(company_equipment):
                # Create rate for multiple time periods
                for k, rate_type in enumerate(rate_types):
                    # Base hourly rate varies by equipment
                    if equipment in ["Crane (50-ton)", "Concrete Pump"]:
                        base_hourly_rate = 150 + random.uniform(-20, 20)
                    elif equipment in ["Excavator (Medium)", "Bulldozer (D6)"]:
                        base_hourly_rate = 100 + random.uniform(-10, 10)
                    else:
                        base_hourly_rate = 50 + random.uniform(-5, 5)
                    
                    # Adjust rate based on rental period
                    if rate_type == "Hour":
                        rate = base_hourly_rate
                    elif rate_type == "Day":
                        rate = base_hourly_rate * 8 * 0.8  # 8 hours with 20% discount
                    elif rate_type == "Week":
                        rate = base_hourly_rate * 40 * 0.6  # 40 hours with 40% discount
                    else:  # Month
                        rate = base_hourly_rate * 160 * 0.4  # 160 hours with 60% discount
                    
                    # Create a unique ID
                    rate_id = f"ER-{i+1:03d}-{j+1:02d}-{k+1:02d}"
                    
                    # Effective date (random date in the past year)
                    days_ago = random.randint(0, 365)
                    effective_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
                    
                    # Sample item
                    demo_items.append({
                        "rate_id": rate_id,
                        "company_id": company["id"],
                        "company_name": company["name"],
                        "equipment": equipment,
                        "type": equipment_type_map.get(equipment, "Miscellaneous"),
                        "rate": round(rate, 2),
                        "rate_type": rate_type,
                        "minimum_rental": 1,
                        "includes_operator": random.choice([True, False]),
                        "includes_fuel": random.choice([True, False]),
                        "effective_date": effective_date,
                        "expiration_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                        "notes": f"Standard {rate_type} rate for {equipment}",
                        "status": "Active"
                    })
        
        # Save the demo data
        self._save_items(demo_items)
    
    def render_detail_view(self, item_id=None):
        """Render the detail view for creating or editing an equipment rate."""
        # Apply consistent CRUD styling
        apply_crud_styles()
        
        is_new = item_id is None
        title = "Add New Equipment Rate" if is_new else "Edit Equipment Rate"
        
        # Get the current item if editing
        current_item = None
        if not is_new:
            current_item = self._get_item_by_id(item_id)
            if not current_item:
                st.error(f"Equipment Rate with ID {item_id} not found.")
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
        with st.form("equipment_rate_form"):
            # Basic information fieldset
            with st.container():
                st.subheader("Basic Information")
                
                # Two columns for the form
                col1, col2 = st.columns(2)
                
                with col1:
                    # Company selection (from project companies)
                    company_options = [company["name"] for company in PROJECT_COMPANIES]
                    company_id_map = {company["name"]: company["id"] for company in PROJECT_COMPANIES}
                    
                    selected_company = st.selectbox(
                        "Company",
                        options=company_options,
                        index=0 if is_new else company_options.index(current_item["company_name"])
                    )
                    
                    # Equipment input
                    equipment = st.text_input(
                        "Equipment",
                        value="" if is_new else current_item["equipment"]
                    )
                    
                    # Equipment type selection
                    type_options = [
                        "Earthmoving", "Lifting", "Concrete", "Material Handling", 
                        "Power", "Transportation", "Miscellaneous"
                    ]
                    equipment_type = st.selectbox(
                        "Type",
                        options=type_options,
                        index=0 if is_new else (
                            type_options.index(current_item["type"]) 
                            if current_item.get("type") in type_options else 0
                        )
                    )
                
                with col2:
                    # Rate input
                    rate = st.number_input(
                        "Rate ($)",
                        min_value=0.0,
                        max_value=10000.0,
                        value=0.0 if is_new else current_item["rate"],
                        step=0.01,
                        format="%.2f"
                    )
                    
                    # Rate type selection
                    rate_type_options = ["Hour", "Day", "Week", "Month"]
                    rate_type = st.selectbox(
                        "Rate Type",
                        options=rate_type_options,
                        index=0 if is_new else rate_type_options.index(current_item["rate_type"])
                    )
                    
                    # Status selection
                    status_options = ["Active", "Archive", "Pending"]
                    status = st.selectbox(
                        "Status",
                        options=status_options,
                        index=0 if is_new else status_options.index(current_item["status"])
                    )
            
            # Additional details fieldset
            with st.container():
                st.subheader("Rental Details")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Minimum rental
                    minimum_rental = st.number_input(
                        f"Minimum Rental ({rate_type}s)",
                        min_value=1,
                        value=1 if is_new else current_item.get("minimum_rental", 1)
                    )
                    
                    # Includes operator
                    includes_operator = st.checkbox(
                        "Includes Operator",
                        value=False if is_new else current_item.get("includes_operator", False)
                    )
                    
                    # Includes fuel
                    includes_fuel = st.checkbox(
                        "Includes Fuel",
                        value=False if is_new else current_item.get("includes_fuel", False)
                    )
                
                with col2:
                    # Effective date
                    effective_date = st.date_input(
                        "Effective Date",
                        value=datetime.now() if is_new else datetime.strptime(current_item["effective_date"], "%Y-%m-%d")
                    )
                    
                    # Expiration date (optional)
                    expiration_date = st.date_input(
                        "Expiration Date (Optional)",
                        value=(datetime.now() + timedelta(days=365)) if is_new else (
                            datetime.strptime(current_item["expiration_date"], "%Y-%m-%d") 
                            if "expiration_date" in current_item else (datetime.now() + timedelta(days=365))
                        )
                    )
            
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
                if not equipment or not selected_company:
                    st.error("Equipment and Company are required fields.")
                else:
                    # Create or update the item
                    item = {
                        "rate_id": str(uuid.uuid4())[:8] if is_new else current_item["rate_id"],
                        "company_id": company_id_map[selected_company],
                        "company_name": selected_company,
                        "equipment": equipment,
                        "type": equipment_type,
                        "rate": float(rate),
                        "rate_type": rate_type,
                        "minimum_rental": int(minimum_rental),
                        "includes_operator": includes_operator,
                        "includes_fuel": includes_fuel,
                        "effective_date": effective_date.strftime("%Y-%m-%d"),
                        "expiration_date": expiration_date.strftime("%Y-%m-%d"),
                        "notes": notes,
                        "status": status
                    }
                    
                    # Save the item
                    self._save_item(item)
                    
                    # Show success message and return to list
                    st.success(f"Equipment rate for {equipment} saved successfully!")
                    self._return_to_list_view()
            
            if cancel_button:
                self._return_to_list_view()
        
        # Close the detail container
        end_crud_detail_container()


def render_unit_prices():
    """Render the unit prices interface with tabs for different rate categories."""
    st.title("Unit Prices")
    
    # Create tabs for different rate types
    tabs = st.tabs(["Labor Rates", "Material Rates", "Equipment Rates"])
    
    with tabs[0]:
        labor_module = LaborRatesModule()
        render_labor_rates(labor_module)
    
    with tabs[1]:
        material_module = MaterialRatesModule()
        render_material_rates(material_module)
    
    with tabs[2]:
        equipment_module = EquipmentRatesModule()
        render_equipment_rates(equipment_module)


def render_labor_rates(module):
    """Render labor rates module."""
    # Get the view state
    base_key = module._get_state_key_prefix()
    current_view = st.session_state.get(f"{base_key}_view", "list")
    item_id = st.session_state.get(f"{base_key}_item_id", None)
    
    # Render the appropriate view
    if current_view == "list":
        module.render_list_view()
    elif current_view == "detail":
        module.render_detail_view(item_id)
    elif current_view == "new":
        module.render_detail_view()


def render_material_rates(module):
    """Render material rates module."""
    # Get the view state
    base_key = module._get_state_key_prefix()
    current_view = st.session_state.get(f"{base_key}_view", "list")
    item_id = st.session_state.get(f"{base_key}_item_id", None)
    
    # Render the appropriate view
    if current_view == "list":
        module.render_list_view()
    elif current_view == "detail":
        module.render_detail_view(item_id)
    elif current_view == "new":
        module.render_detail_view()


def render_equipment_rates(module):
    """Render equipment rates module."""
    # Get the view state
    base_key = module._get_state_key_prefix()
    current_view = st.session_state.get(f"{base_key}_view", "list")
    item_id = st.session_state.get(f"{base_key}_item_id", None)
    
    # Render the appropriate view
    if current_view == "list":
        module.render_list_view()
    elif current_view == "detail":
        module.render_detail_view(item_id)
    elif current_view == "new":
        module.render_detail_view()


if __name__ == "__main__":
    render_unit_prices()