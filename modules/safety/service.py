"""
Safety Service Module for gcPanel

This module provides the core business logic and data access for the safety module.
It isolates the data operations from the UI components for better separation of concerns.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

# Constants for file paths
DATA_DIR = "data/safety"
INCIDENTS_FILE = os.path.join(DATA_DIR, "incidents.json")
INSPECTIONS_FILE = os.path.join(DATA_DIR, "inspections.json")
TOOLBOX_TALKS_FILE = os.path.join(DATA_DIR, "toolbox_talks.json")
HAZARDS_FILE = os.path.join(DATA_DIR, "hazards.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

class SafetyService:
    """
    Service class for safety-related data operations.
    
    This class handles all data operations for the safety module,
    providing a clean interface for the UI components to use.
    """
    
    @staticmethod
    def initialize_data_files():
        """Initialize data files with sample data if they don't exist."""
        # Sample incidents data
        if not os.path.exists(INCIDENTS_FILE):
            sample_incidents = [
                {
                    "id": "INC-2025-001",
                    "date": "2025-02-10",
                    "status": "Closed",
                    "type": "Near Miss",
                    "location": "Floor 5, East Wing",
                    "description": "Worker nearly slipped on wet floor",
                    "reported_by": "John Smith",
                    "severity": "Low",
                    "corrective_action": "Area was cordoned off and dried",
                    "photos": [],
                    "witnesses": ["Jane Doe"],
                    "created_at": "2025-02-10",
                    "updated_at": "2025-02-12"
                },
                {
                    "id": "INC-2025-002",
                    "date": "2025-03-15",
                    "status": "Open",
                    "type": "Injury",
                    "location": "Basement Level, Electrical Room",
                    "description": "Minor electrical shock when connecting temporary power",
                    "reported_by": "Robert Johnson",
                    "severity": "Medium",
                    "corrective_action": "Investigation in progress",
                    "photos": [],
                    "witnesses": ["Maria Garcia", "David Wilson"],
                    "created_at": "2025-03-15",
                    "updated_at": "2025-03-15"
                }
            ]
            SafetyService._save_to_file(INCIDENTS_FILE, sample_incidents)
        
        # Sample inspections data
        if not os.path.exists(INSPECTIONS_FILE):
            sample_inspections = [
                {
                    "id": "INS-2025-001",
                    "date": "2025-01-15",
                    "status": "Completed",
                    "type": "Weekly Site Inspection",
                    "location": "Entire Site",
                    "inspector": "Safety Manager",
                    "findings": [
                        {"item": "Fall protection", "status": "Compliant", "notes": "All workers properly using harnesses"},
                        {"item": "Fire extinguishers", "status": "Non-compliant", "notes": "Two extinguishers missing monthly inspection tags"},
                        {"item": "Housekeeping", "status": "Partially compliant", "notes": "Some debris in stairwells"}
                    ],
                    "score": 85,
                    "created_at": "2025-01-15",
                    "updated_at": "2025-01-15"
                },
                {
                    "id": "INS-2025-002",
                    "date": "2025-02-01",
                    "status": "Completed",
                    "type": "Monthly Equipment Inspection",
                    "location": "Equipment Yard",
                    "inspector": "Maintenance Supervisor",
                    "findings": [
                        {"item": "Crane inspection", "status": "Compliant", "notes": "All certifications current"},
                        {"item": "Forklift maintenance", "status": "Compliant", "notes": "Regular maintenance up to date"},
                        {"item": "Scaffolding components", "status": "Non-compliant", "notes": "Some damaged components identified"}
                    ],
                    "score": 90,
                    "created_at": "2025-02-01",
                    "updated_at": "2025-02-01"
                }
            ]
            SafetyService._save_to_file(INSPECTIONS_FILE, sample_inspections)
        
        # Sample toolbox talks data
        if not os.path.exists(TOOLBOX_TALKS_FILE):
            sample_toolbox_talks = [
                {
                    "id": "TBT-2025-001",
                    "date": "2025-01-10",
                    "topic": "Fall Protection",
                    "presenter": "Safety Manager",
                    "duration": 30,
                    "attendees": [
                        {"name": "John Smith", "company": "GC Construction", "signature": True},
                        {"name": "Jane Doe", "company": "GC Construction", "signature": True},
                        {"name": "Robert Johnson", "company": "Electrical Subcontractor", "signature": True}
                    ],
                    "notes": "Discussed proper use of harnesses and anchor points",
                    "created_at": "2025-01-10",
                    "updated_at": "2025-01-10"
                },
                {
                    "id": "TBT-2025-002",
                    "date": "2025-01-17",
                    "topic": "Hazard Communication",
                    "presenter": "Project Manager",
                    "duration": 20,
                    "attendees": [
                        {"name": "John Smith", "company": "GC Construction", "signature": True},
                        {"name": "Jane Doe", "company": "GC Construction", "signature": True},
                        {"name": "Maria Garcia", "company": "Concrete Subcontractor", "signature": True}
                    ],
                    "notes": "Reviewed SDS for new epoxy product being used",
                    "created_at": "2025-01-17",
                    "updated_at": "2025-01-17"
                }
            ]
            SafetyService._save_to_file(TOOLBOX_TALKS_FILE, sample_toolbox_talks)
        
        # Sample hazards data
        if not os.path.exists(HAZARDS_FILE):
            sample_hazards = [
                {
                    "id": "HAZ-2025-001",
                    "date_identified": "2025-01-05",
                    "status": "Mitigated",
                    "type": "Physical",
                    "location": "Floor 2, North Wing",
                    "description": "Floor opening without proper covering",
                    "severity": "High",
                    "mitigation": "Installed OSHA-compliant cover and warning signs",
                    "identified_by": "Safety Inspector",
                    "due_date": "2025-01-06",
                    "completed_date": "2025-01-06",
                    "created_at": "2025-01-05",
                    "updated_at": "2025-01-06"
                },
                {
                    "id": "HAZ-2025-002",
                    "date_identified": "2025-02-20",
                    "status": "Open",
                    "type": "Chemical",
                    "location": "Basement Level, Storage Room",
                    "description": "Improper storage of incompatible chemicals",
                    "severity": "Medium",
                    "mitigation": "Scheduled reorganization of storage area",
                    "identified_by": "Subcontractor Foreman",
                    "due_date": "2025-02-25",
                    "completed_date": None,
                    "created_at": "2025-02-20",
                    "updated_at": "2025-02-20"
                }
            ]
            SafetyService._save_to_file(HAZARDS_FILE, sample_hazards)
    
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
    
    # Incident-related methods
    @staticmethod
    def get_incidents() -> List[Dict[str, Any]]:
        """
        Get all safety incidents.
        
        Returns:
            List of incident dictionaries
        """
        return SafetyService._load_from_file(INCIDENTS_FILE)
    
    @staticmethod
    def get_incident(incident_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific safety incident by ID.
        
        Args:
            incident_id: The ID of the incident to get
            
        Returns:
            The incident dictionary, or None if not found
        """
        incidents = SafetyService.get_incidents()
        return next((inc for inc in incidents if inc.get("id") == incident_id), None)
    
    @staticmethod
    def create_incident(incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new safety incident.
        
        Args:
            incident_data: The incident data
            
        Returns:
            The created incident with assigned ID
        """
        incidents = SafetyService.get_incidents()
        
        # Generate a new ID if not provided
        if "id" not in incident_data:
            # Find the highest existing ID number
            existing_ids = [inc.get("id", "") for inc in incidents]
            existing_numbers = []
            
            for id_str in existing_ids:
                if id_str.startswith("INC-") and len(id_str) > 9:
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
            incident_data["id"] = f"INC-2025-{new_number:03d}"
        
        # Add timestamps
        now = datetime.now().strftime("%Y-%m-%d")
        incident_data["created_at"] = now
        incident_data["updated_at"] = now
        
        # Add the new incident
        incidents.append(incident_data)
        SafetyService._save_to_file(INCIDENTS_FILE, incidents)
        
        return incident_data
    
    @staticmethod
    def update_incident(incident_id: str, incident_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing safety incident.
        
        Args:
            incident_id: The ID of the incident to update
            incident_data: The new incident data
            
        Returns:
            The updated incident, or None if not found
        """
        incidents = SafetyService.get_incidents()
        
        # Find the incident to update
        for i, inc in enumerate(incidents):
            if inc.get("id") == incident_id:
                # Preserve the original ID
                incident_data["id"] = incident_id
                
                # Preserve creation timestamp
                incident_data["created_at"] = inc.get("created_at")
                
                # Update the timestamp
                incident_data["updated_at"] = datetime.now().strftime("%Y-%m-%d")
                
                # Update the incident
                incidents[i] = incident_data
                SafetyService._save_to_file(INCIDENTS_FILE, incidents)
                
                return incident_data
        
        return None
    
    @staticmethod
    def delete_incident(incident_id: str) -> bool:
        """
        Delete a safety incident.
        
        Args:
            incident_id: The ID of the incident to delete
            
        Returns:
            True if deleted, False if not found
        """
        incidents = SafetyService.get_incidents()
        
        # Find the incident to delete
        for i, inc in enumerate(incidents):
            if inc.get("id") == incident_id:
                # Remove the incident
                del incidents[i]
                SafetyService._save_to_file(INCIDENTS_FILE, incidents)
                return True
        
        return False
    
    # Inspection-related methods
    @staticmethod
    def get_inspections() -> List[Dict[str, Any]]:
        """
        Get all safety inspections.
        
        Returns:
            List of inspection dictionaries
        """
        return SafetyService._load_from_file(INSPECTIONS_FILE)
    
    @staticmethod
    def get_inspection(inspection_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific safety inspection by ID.
        
        Args:
            inspection_id: The ID of the inspection to get
            
        Returns:
            The inspection dictionary, or None if not found
        """
        inspections = SafetyService.get_inspections()
        return next((insp for insp in inspections if insp.get("id") == inspection_id), None)
    
    @staticmethod
    def create_inspection(inspection_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new safety inspection.
        
        Args:
            inspection_data: The inspection data
            
        Returns:
            The created inspection with assigned ID
        """
        inspections = SafetyService.get_inspections()
        
        # Generate a new ID if not provided
        if "id" not in inspection_data:
            # Find the highest existing ID number
            existing_ids = [insp.get("id", "") for insp in inspections]
            existing_numbers = []
            
            for id_str in existing_ids:
                if id_str.startswith("INS-") and len(id_str) > 9:
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
            inspection_data["id"] = f"INS-2025-{new_number:03d}"
        
        # Add timestamps
        now = datetime.now().strftime("%Y-%m-%d")
        inspection_data["created_at"] = now
        inspection_data["updated_at"] = now
        
        # Add the new inspection
        inspections.append(inspection_data)
        SafetyService._save_to_file(INSPECTIONS_FILE, inspections)
        
        return inspection_data
    
    # Similar methods for toolbox talks and hazards...

# Initialize data files when the module is imported
SafetyService.initialize_data_files()