"""
Contracts Service Module for gcPanel

This module provides the core business logic and data access for the contracts module.
It isolates the data operations from the UI components for better separation of concerns.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

# Constants for file paths
DATA_DIR = "data/contracts"
CHANGE_ORDERS_FILE = os.path.join(DATA_DIR, "change_orders.json")
SUBCONTRACTS_FILE = os.path.join(DATA_DIR, "subcontracts.json")
INVOICES_FILE = os.path.join(DATA_DIR, "invoices.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

class ContractsService:
    """
    Service class for contract-related data operations.
    
    This class handles all data operations for the contracts module,
    providing a clean interface for the UI components to use.
    """
    
    @staticmethod
    def initialize_data_files():
        """Initialize data files with sample data if they don't exist."""
        # Sample change orders data
        if not os.path.exists(CHANGE_ORDERS_FILE):
            sample_change_orders = [
                {
                    "id": "CO-2025-001",
                    "project": "Highland Tower Development",
                    "date": "2025-02-10",
                    "status": "Approved",
                    "description": "Added Roof Drains",
                    "reason": "Owner Request",
                    "original_amount": 45500000.00,
                    "previous_changes": 0.00,
                    "this_change": 28500.00,
                    "days_added": 2,
                    "signatures": ["Contractor: John Doe", "Owner: Jane Smith"],
                    "created_at": "2025-02-10",
                    "updated_at": "2025-02-15"
                },
                {
                    "id": "CO-2025-042",
                    "project": "Highland Tower Development",
                    "date": "2025-05-10",
                    "status": "Pending Approval",
                    "description": "Added Security Equipment",
                    "reason": "Owner Request",
                    "original_amount": 45500000.00,
                    "previous_changes": 124500.00,
                    "this_change": 36750.00,
                    "days_added": 3,
                    "signatures": ["Contractor: John Doe"],
                    "created_at": "2025-05-10",
                    "updated_at": "2025-05-10"
                }
            ]
            ContractsService._save_to_file(CHANGE_ORDERS_FILE, sample_change_orders)
        
        # Sample subcontracts data
        if not os.path.exists(SUBCONTRACTS_FILE):
            sample_subcontracts = [
                {
                    "id": "SC-2025-001",
                    "project": "Highland Tower Development",
                    "date": "2025-01-15",
                    "status": "Executed",
                    "company": "Deep Excavation Inc.",
                    "contact": "Mike Johnson",
                    "email": "mike@deepexcavation.com",
                    "scope": "Excavation",
                    "amount": 1250000.00,
                    "start_date": "2025-02-01",
                    "completion_date": "2025-04-15",
                    "signatures": ["Subcontractor: Mike Johnson", "General Contractor: John Doe"],
                    "created_at": "2025-01-10",
                    "updated_at": "2025-01-15"
                },
                {
                    "id": "SC-2025-038",
                    "project": "Highland Tower Development",
                    "date": "2025-03-22",
                    "status": "Executed",
                    "company": "Superior Concrete Solutions",
                    "contact": "Sarah Williams",
                    "email": "sarah@superiorconcrete.com",
                    "scope": "Concrete",
                    "amount": 3750000.00,
                    "start_date": "2025-04-01",
                    "completion_date": "2025-08-15",
                    "signatures": ["Subcontractor: Sarah Williams", "General Contractor: John Doe"],
                    "created_at": "2025-03-15",
                    "updated_at": "2025-03-22"
                }
            ]
            ContractsService._save_to_file(SUBCONTRACTS_FILE, sample_subcontracts)
        
        # Sample invoices data
        if not os.path.exists(INVOICES_FILE):
            sample_invoices = [
                {
                    "id": "INV-2025-087",
                    "project": "Highland Tower Development",
                    "date": "2025-04-15",
                    "status": "Paid",
                    "description": "March Progress",
                    "company": "Superior Concrete Solutions",
                    "contract_amount": 3750000.00,
                    "approved_changes": 0.00,
                    "previously_billed": 0.00,
                    "current_billed": 450000.00,
                    "retainage": 45000.00,
                    "amount_due": 405000.00,
                    "signatures": ["Contractor: Sarah Williams", "Owner/CM: Jane Smith"],
                    "created_at": "2025-04-15",
                    "updated_at": "2025-04-22"
                }
            ]
            ContractsService._save_to_file(INVOICES_FILE, sample_invoices)
    
    @staticmethod
    def _load_from_file(file_path: str) -> List[Dict[str, Any]]:
        """
        Load data from a JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            List of dictionaries containing the data
        """
        if not os.path.exists(file_path):
            return []
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading from {file_path}: {str(e)}")
            return []
    
    @staticmethod
    def _save_to_file(file_path: str, data: List[Dict[str, Any]]) -> bool:
        """
        Save data to a JSON file.
        
        Args:
            file_path: Path to the JSON file
            data: List of dictionaries to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving to {file_path}: {str(e)}")
            return False
    
    @staticmethod
    def get_change_orders() -> List[Dict[str, Any]]:
        """
        Get all change orders.
        
        Returns:
            List of change order dictionaries
        """
        return ContractsService._load_from_file(CHANGE_ORDERS_FILE)
    
    @staticmethod
    def get_change_order(change_order_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific change order by ID.
        
        Args:
            change_order_id: The ID of the change order to get
            
        Returns:
            The change order dictionary, or None if not found
        """
        change_orders = ContractsService.get_change_orders()
        return next((co for co in change_orders if co.get("id") == change_order_id), None)
    
    @staticmethod
    def create_change_order(change_order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new change order.
        
        Args:
            change_order_data: The change order data
            
        Returns:
            The created change order with assigned ID
        """
        change_orders = ContractsService.get_change_orders()
        
        # Generate a new ID if not provided
        if "id" not in change_order_data:
            # Find the highest existing ID number
            existing_ids = [co.get("id", "") for co in change_orders]
            existing_numbers = []
            
            for id_str in existing_ids:
                if id_str.startswith("CO-") and len(id_str) > 8:
                    try:
                        num = int(id_str.split("-")[-1])
                        existing_numbers.append(num)
                    except ValueError:
                        continue
            
            # Generate a new number
            new_number = 1
            if existing_numbers:
                new_number = max(existing_numbers) + 1
                
            # Create the new ID
            change_order_data["id"] = f"CO-2025-{new_number:03d}"
        
        # Add timestamps
        now = datetime.now().strftime("%Y-%m-%d")
        change_order_data["created_at"] = now
        change_order_data["updated_at"] = now
        
        # Add the new change order
        change_orders.append(change_order_data)
        ContractsService._save_to_file(CHANGE_ORDERS_FILE, change_orders)
        
        return change_order_data
    
    @staticmethod
    def update_change_order(change_order_id: str, change_order_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing change order.
        
        Args:
            change_order_id: The ID of the change order to update
            change_order_data: The new change order data
            
        Returns:
            The updated change order, or None if not found
        """
        change_orders = ContractsService.get_change_orders()
        
        # Find the change order to update
        for i, co in enumerate(change_orders):
            if co.get("id") == change_order_id:
                # Preserve the original ID
                change_order_data["id"] = change_order_id
                
                # Preserve creation timestamp
                change_order_data["created_at"] = co.get("created_at")
                
                # Update the timestamp
                change_order_data["updated_at"] = datetime.now().strftime("%Y-%m-%d")
                
                # Update the change order
                change_orders[i] = change_order_data
                ContractsService._save_to_file(CHANGE_ORDERS_FILE, change_orders)
                
                return change_order_data
        
        return None
    
    @staticmethod
    def delete_change_order(change_order_id: str) -> bool:
        """
        Delete a change order.
        
        Args:
            change_order_id: The ID of the change order to delete
            
        Returns:
            True if deleted, False if not found
        """
        change_orders = ContractsService.get_change_orders()
        
        # Find the change order to delete
        for i, co in enumerate(change_orders):
            if co.get("id") == change_order_id:
                # Remove the change order
                del change_orders[i]
                ContractsService._save_to_file(CHANGE_ORDERS_FILE, change_orders)
                return True
        
        return False
    
    @staticmethod
    def get_subcontracts() -> List[Dict[str, Any]]:
        """
        Get all subcontracts.
        
        Returns:
            List of subcontract dictionaries
        """
        return ContractsService._load_from_file(SUBCONTRACTS_FILE)
    
    @staticmethod
    def get_subcontract(subcontract_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific subcontract by ID.
        
        Args:
            subcontract_id: The ID of the subcontract to get
            
        Returns:
            The subcontract dictionary, or None if not found
        """
        subcontracts = ContractsService.get_subcontracts()
        return next((sc for sc in subcontracts if sc.get("id") == subcontract_id), None)
    
    @staticmethod
    def create_subcontract(subcontract_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new subcontract.
        
        Args:
            subcontract_data: The subcontract data
            
        Returns:
            The created subcontract with assigned ID
        """
        subcontracts = ContractsService.get_subcontracts()
        
        # Generate a new ID if not provided
        if "id" not in subcontract_data:
            # Find the highest existing ID number
            existing_ids = [sc.get("id", "") for sc in subcontracts]
            existing_numbers = []
            
            for id_str in existing_ids:
                if id_str.startswith("SC-") and len(id_str) > 8:
                    try:
                        num = int(id_str.split("-")[-1])
                        existing_numbers.append(num)
                    except ValueError:
                        continue
            
            # Generate a new number
            new_number = 1
            if existing_numbers:
                new_number = max(existing_numbers) + 1
                
            # Create the new ID
            subcontract_data["id"] = f"SC-2025-{new_number:03d}"
        
        # Add timestamps
        now = datetime.now().strftime("%Y-%m-%d")
        subcontract_data["created_at"] = now
        subcontract_data["updated_at"] = now
        
        # Add the new subcontract
        subcontracts.append(subcontract_data)
        ContractsService._save_to_file(SUBCONTRACTS_FILE, subcontracts)
        
        return subcontract_data
    
    @staticmethod
    def update_subcontract(subcontract_id: str, subcontract_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing subcontract.
        
        Args:
            subcontract_id: The ID of the subcontract to update
            subcontract_data: The new subcontract data
            
        Returns:
            The updated subcontract, or None if not found
        """
        subcontracts = ContractsService.get_subcontracts()
        
        # Find the subcontract to update
        for i, sc in enumerate(subcontracts):
            if sc.get("id") == subcontract_id:
                # Preserve the original ID
                subcontract_data["id"] = subcontract_id
                
                # Preserve creation timestamp
                subcontract_data["created_at"] = sc.get("created_at")
                
                # Update the timestamp
                subcontract_data["updated_at"] = datetime.now().strftime("%Y-%m-%d")
                
                # Update the subcontract
                subcontracts[i] = subcontract_data
                ContractsService._save_to_file(SUBCONTRACTS_FILE, subcontracts)
                
                return subcontract_data
        
        return None
    
    @staticmethod
    def delete_subcontract(subcontract_id: str) -> bool:
        """
        Delete a subcontract.
        
        Args:
            subcontract_id: The ID of the subcontract to delete
            
        Returns:
            True if deleted, False if not found
        """
        subcontracts = ContractsService.get_subcontracts()
        
        # Find the subcontract to delete
        for i, sc in enumerate(subcontracts):
            if sc.get("id") == subcontract_id:
                # Remove the subcontract
                del subcontracts[i]
                ContractsService._save_to_file(SUBCONTRACTS_FILE, subcontracts)
                return True
        
        return False
    
    @staticmethod
    def get_invoices() -> List[Dict[str, Any]]:
        """
        Get all invoices.
        
        Returns:
            List of invoice dictionaries
        """
        return ContractsService._load_from_file(INVOICES_FILE)
    
    @staticmethod
    def get_invoice(invoice_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific invoice by ID.
        
        Args:
            invoice_id: The ID of the invoice to get
            
        Returns:
            The invoice dictionary, or None if not found
        """
        invoices = ContractsService.get_invoices()
        return next((inv for inv in invoices if inv.get("id") == invoice_id), None)
    
    @staticmethod
    def create_invoice(invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new invoice.
        
        Args:
            invoice_data: The invoice data
            
        Returns:
            The created invoice with assigned ID
        """
        invoices = ContractsService.get_invoices()
        
        # Generate a new ID if not provided
        if "id" not in invoice_data:
            # Find the highest existing ID number
            existing_ids = [inv.get("id", "") for inv in invoices]
            existing_numbers = []
            
            for id_str in existing_ids:
                if id_str.startswith("INV-") and len(id_str) > 9:
                    try:
                        num = int(id_str.split("-")[-1])
                        existing_numbers.append(num)
                    except ValueError:
                        continue
            
            # Generate a new number
            new_number = 1
            if existing_numbers:
                new_number = max(existing_numbers) + 1
                
            # Create the new ID
            invoice_data["id"] = f"INV-2025-{new_number:03d}"
        
        # Add timestamps
        now = datetime.now().strftime("%Y-%m-%d")
        invoice_data["created_at"] = now
        invoice_data["updated_at"] = now
        
        # Add the new invoice
        invoices.append(invoice_data)
        ContractsService._save_to_file(INVOICES_FILE, invoices)
        
        return invoice_data
    
    @staticmethod
    def update_invoice(invoice_id: str, invoice_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing invoice.
        
        Args:
            invoice_id: The ID of the invoice to update
            invoice_data: The new invoice data
            
        Returns:
            The updated invoice, or None if not found
        """
        invoices = ContractsService.get_invoices()
        
        # Find the invoice to update
        for i, inv in enumerate(invoices):
            if inv.get("id") == invoice_id:
                # Preserve the original ID
                invoice_data["id"] = invoice_id
                
                # Preserve creation timestamp
                invoice_data["created_at"] = inv.get("created_at")
                
                # Update the timestamp
                invoice_data["updated_at"] = datetime.now().strftime("%Y-%m-%d")
                
                # Update the invoice
                invoices[i] = invoice_data
                ContractsService._save_to_file(INVOICES_FILE, invoices)
                
                return invoice_data
        
        return None
    
    @staticmethod
    def delete_invoice(invoice_id: str) -> bool:
        """
        Delete an invoice.
        
        Args:
            invoice_id: The ID of the invoice to delete
            
        Returns:
            True if deleted, False if not found
        """
        invoices = ContractsService.get_invoices()
        
        # Find the invoice to delete
        for i, inv in enumerate(invoices):
            if inv.get("id") == invoice_id:
                # Remove the invoice
                del invoices[i]
                ContractsService._save_to_file(INVOICES_FILE, invoices)
                return True
        
        return False

# Initialize data files when the module is imported
ContractsService.initialize_data_files()