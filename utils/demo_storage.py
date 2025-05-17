import streamlit as st
import pandas as pd
import json
import logging
from datetime import datetime
import uuid

class DemoStorage:
    """Class to handle data storage in demo mode using session state"""
    
    @staticmethod
    def initialize():
        """Initialize demo storage if it doesn't exist"""
        if 'demo_data' not in st.session_state:
            st.session_state.demo_data = {
                'projects': [],
                'sections': [
                    {'id': 1, 'name': 'preconstruction', 'display_name': 'Preconstruction', 'icon': 'building', 'sort_order': 1},
                    {'id': 2, 'name': 'engineering', 'display_name': 'Engineering', 'icon': 'clipboard', 'sort_order': 2},
                    {'id': 3, 'name': 'field', 'display_name': 'Field', 'icon': 'hard-hat', 'sort_order': 3},
                    {'id': 4, 'name': 'safety', 'display_name': 'Safety', 'icon': 'shield', 'sort_order': 4},
                    {'id': 5, 'name': 'contracts', 'display_name': 'Contracts', 'icon': 'file-text', 'sort_order': 5},
                    {'id': 6, 'name': 'cost', 'display_name': 'Cost', 'icon': 'dollar-sign', 'sort_order': 6},
                    {'id': 7, 'name': 'bim', 'display_name': 'BIM', 'icon': '3d-model', 'sort_order': 7},
                    {'id': 8, 'name': 'closeout', 'display_name': 'Closeout', 'icon': 'check-circle', 'sort_order': 8},
                    {'id': 9, 'name': 'resources', 'display_name': 'Resources', 'icon': 'database', 'sort_order': 9},
                    {'id': 10, 'name': 'settings', 'display_name': 'Settings', 'icon': 'settings', 'sort_order': 10},
                    {'id': 11, 'name': 'reports', 'display_name': 'Reports', 'icon': 'bar-chart-2', 'sort_order': 11}
                ],
                'modules': [],
                'users': [
                    {
                        'id': 1,
                        'username': 'admin',
                        'email': 'admin@example.com',
                        'role': 'administrator',
                        'created_at': datetime.now().isoformat()
                    }
                ],
                'bid_packages': [],
                'qualified_bidders': [],
                'daily_reports': [],
                'rfi': [],
                'prime_contracts': [],
                'budgets': [],
                'warranties': [],
                'observations': [],
                'locations': []
            }
            
            # Add some sample projects
            DemoStorage.insert('projects', {
                'name': 'Commercial Office Building',
                'description': 'Construction of a 10-story office building in downtown area',
                'start_date': '2025-01-01',
                'end_date': '2026-06-30',
                'status': 'In Progress'
            })
            
            DemoStorage.insert('projects', {
                'name': 'Residential Complex',
                'description': 'Development of a 50-unit luxury residential complex',
                'start_date': '2025-03-15',
                'end_date': '2026-09-30',
                'status': 'Planning'
            })
            
            # Add sample bid packages
            DemoStorage.insert('bid_packages', {
                'name': 'Excavation & Site Work',
                'description': 'Site preparation and excavation work',
                'issue_date': '2025-02-01',
                'due_date': '2025-02-15',
                'project_id': 1,
                'status': 'Awarded'
            })
            
            DemoStorage.insert('bid_packages', {
                'name': 'Structural Steel',
                'description': 'Structural steel supply and installation',
                'issue_date': '2025-02-10',
                'due_date': '2025-02-28',
                'project_id': 1,
                'status': 'In Review'
            })
            
            # Add sample qualified bidders
            DemoStorage.insert('qualified_bidders', {
                'company_name': 'ABC Excavation',
                'contact_name': 'John Smith',
                'email': 'john@abcexcavation.com',
                'phone': '555-123-4567',
                'specialty': 'Excavation',
                'qualification_status': 'Approved'
            })
            
            DemoStorage.insert('qualified_bidders', {
                'company_name': 'Steel Experts Inc',
                'contact_name': 'Maria Rodriguez',
                'email': 'maria@steelexperts.com',
                'phone': '555-987-6543',
                'specialty': 'Structural Steel',
                'qualification_status': 'Approved'
            })
            
            # Add sample daily reports
            DemoStorage.insert('daily_reports', {
                'date': '2025-01-15',
                'project_id': 1,
                'weather': 'Sunny, 72°F',
                'work_performed': 'Site clearing and initial excavation',
                'workers_present': 12,
                'equipment_used': 'Excavator, Bulldozer, Dump Trucks',
                'delays': 'None',
                'safety_incidents': 'None'
            })
            
            DemoStorage.insert('daily_reports', {
                'date': '2025-01-16',
                'project_id': 1,
                'weather': 'Partly Cloudy, 68°F',
                'work_performed': 'Continued excavation, began foundation layout',
                'workers_present': 15,
                'equipment_used': 'Excavator, Bulldozer, Dump Trucks, Transit Level',
                'delays': 'Minor delay due to utility marking',
                'safety_incidents': 'None'
            })
            
            # Add sample RFIs
            DemoStorage.insert('rfi', {
                'number': 'RFI-001',
                'project_id': 1,
                'subject': 'Foundation Depth Clarification',
                'date_submitted': '2025-01-20',
                'submitted_by': 'Construction Manager',
                'status': 'Answered',
                'response': 'Increase foundation depth by 12 inches per geotechnical report',
                'date_answered': '2025-01-22'
            })
            
            DemoStorage.insert('rfi', {
                'number': 'RFI-002',
                'project_id': 1,
                'subject': 'Electrical Conduit Routing',
                'date_submitted': '2025-01-25',
                'submitted_by': 'Electrical Contractor',
                'status': 'Open',
                'response': '',
                'date_answered': ''
            })
            
            # Add sample contracts
            DemoStorage.insert('prime_contracts', {
                'contract_number': 'PC-2025-001',
                'project_id': 1,
                'vendor': 'ABC General Contractors',
                'description': 'General Construction Services',
                'execution_date': '2024-12-15',
                'start_date': '2025-01-01',
                'completion_date': '2026-06-30',
                'contract_amount': 15000000.00,
                'status': 'Active'
            })
            
            # Add sample budgets
            DemoStorage.insert('budgets', {
                'project_id': 1,
                'category': 'Sitework',
                'description': 'Excavation, grading, and site preparation',
                'original_budget': 2500000.00,
                'current_budget': 2600000.00,
                'committed_costs': 2200000.00,
                'actual_costs': 1800000.00,
                'forecast_to_complete': 800000.00
            })
            
            DemoStorage.insert('budgets', {
                'project_id': 1,
                'category': 'Concrete',
                'description': 'Foundations and structural concrete',
                'original_budget': 3500000.00,
                'current_budget': 3500000.00,
                'committed_costs': 3300000.00,
                'actual_costs': 1200000.00,
                'forecast_to_complete': 2300000.00
            })
            
            # Add sample warranties
            DemoStorage.insert('warranties', {
                'project_id': 1,
                'system': 'Roofing',
                'provider': 'Superior Roofing Inc',
                'start_date': '2026-06-30',
                'end_date': '2046-06-30',
                'duration_years': 20,
                'description': 'Commercial roofing system warranty',
                'contact_info': 'warranty@superiorroofing.com'
            })
            
            # Add sample safety observations
            DemoStorage.insert('observations', {
                'project_id': 1,
                'date': '2025-01-18',
                'location': 'North excavation area',
                'type': 'Safety Concern',
                'description': 'Workers not wearing proper PPE near excavation edge',
                'severity': 'High',
                'reported_by': 'Safety Manager',
                'status': 'Addressed',
                'resolution': 'Toolbox talk conducted, proper PPE enforced',
                'resolution_date': '2025-01-18'
            })
            
            # Add sample locations
            DemoStorage.insert('locations', {
                'name': 'Level 1',
                'description': 'First floor of building',
                'project_id': 1,
                'parent_id': None
            })
            
            location_id = len(st.session_state.demo_data['locations'])
            
            DemoStorage.insert('locations', {
                'name': 'Level 1 - North Wing',
                'description': 'North section of first floor',
                'project_id': 1,
                'parent_id': location_id
            })
            
            DemoStorage.insert('locations', {
                'name': 'Level 1 - South Wing',
                'description': 'South section of first floor',
                'project_id': 1,
                'parent_id': location_id
            })
            
            logging.info("Demo storage initialized with sample data")
    
    @staticmethod
    def get_data(table_name):
        """Get all data from a specific table
        
        Args:
            table_name (str): Name of the table to get data from
            
        Returns:
            list: List of records from the table
        """
        DemoStorage.initialize()
        return st.session_state.demo_data.get(table_name, [])
    
    @staticmethod
    def get_df(table_name):
        """Get all data from a specific table as a pandas DataFrame
        
        Args:
            table_name (str): Name of the table to get data from
            
        Returns:
            DataFrame: Pandas DataFrame with the table data
        """
        data = DemoStorage.get_data(table_name)
        return pd.DataFrame(data)
    
    @staticmethod
    def get_record(table_name, record_id):
        """Get a specific record from a table
        
        Args:
            table_name (str): Name of the table
            record_id: ID of the record to get
            
        Returns:
            dict: The requested record or None if not found
        """
        data = DemoStorage.get_data(table_name)
        for record in data:
            if record.get('id') == record_id:
                return record
        return None
    
    @staticmethod
    def insert(table_name, record):
        """Insert a new record into a table
        
        Args:
            table_name (str): Name of the table
            record (dict): Record to insert
            
        Returns:
            int: ID of the newly inserted record
        """
        DemoStorage.initialize()
        
        # Add metadata fields
        if 'id' not in record:
            # Generate new ID as the next available number
            data = st.session_state.demo_data.get(table_name, [])
            next_id = len(data) + 1
            record['id'] = next_id
        
        if 'created_at' not in record:
            record['created_at'] = datetime.now().isoformat()
        
        if 'updated_at' not in record:
            record['updated_at'] = datetime.now().isoformat()
        
        # Ensure the table exists
        if table_name not in st.session_state.demo_data:
            st.session_state.demo_data[table_name] = []
        
        # Add the record
        st.session_state.demo_data[table_name].append(record)
        
        return record['id']
    
    @staticmethod
    def update(table_name, record_id, updates):
        """Update a specific record in a table
        
        Args:
            table_name (str): Name of the table
            record_id: ID of the record to update
            updates (dict): Fields and values to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        DemoStorage.initialize()
        
        # Add updated_at timestamp
        updates['updated_at'] = datetime.now().isoformat()
        
        # Find and update the record
        data = st.session_state.demo_data.get(table_name, [])
        for i, record in enumerate(data):
            if record.get('id') == record_id:
                # Update the record with new values
                data[i] = {**record, **updates}
                return True
        
        return False
    
    @staticmethod
    def delete(table_name, record_id):
        """Delete a specific record from a table
        
        Args:
            table_name (str): Name of the table
            record_id: ID of the record to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        DemoStorage.initialize()
        
        # Find and delete the record
        data = st.session_state.demo_data.get(table_name, [])
        for i, record in enumerate(data):
            if record.get('id') == record_id:
                del st.session_state.demo_data[table_name][i]
                return True
        
        return False
    
    @staticmethod
    def query(table_name, filters=None):
        """Query data from a table with optional filters
        
        Args:
            table_name (str): Name of the table
            filters (dict, optional): Key-value pairs for filtering records
            
        Returns:
            list: Filtered list of records
        """
        data = DemoStorage.get_data(table_name)
        
        if not filters:
            return data
        
        # Apply filters
        result = []
        for record in data:
            match = True
            for key, value in filters.items():
                if key in record and record[key] != value:
                    match = False
                    break
            if match:
                result.append(record)
        
        return result