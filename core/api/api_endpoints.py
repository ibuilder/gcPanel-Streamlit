"""
API endpoints for the gcPanel Construction Management Dashboard.

This module provides RESTful API endpoints for the application, allowing external
systems to interact with gcPanel data and services.
"""

import json
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Union

class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder that handles datetime and date objects."""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

class APIEndpoint:
    """Base class for all API endpoints."""
    
    @staticmethod
    def to_json(data: Any) -> str:
        """Convert data to JSON string with proper encoding."""
        return json.dumps(data, cls=DateTimeEncoder)
    
    @staticmethod
    def from_json(json_str: str) -> Any:
        """Convert JSON string to Python object."""
        return json.loads(json_str)
    
    @staticmethod
    def success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
        """Create a standardized success response."""
        return {
            "status": "success",
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def error_response(message: str, error_code: int = 400) -> Dict[str, Any]:
        """Create a standardized error response."""
        return {
            "status": "error",
            "error_code": error_code,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }

class ProjectAPI(APIEndpoint):
    """Project-related API endpoints."""
    
    @staticmethod
    def get_projects(filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get projects, optionally filtered.
        
        Args:
            filters: Dictionary of filter criteria
            
        Returns:
            API response with projects data
        """
        # In a real implementation, this would query the database
        # Here we return sample data
        projects = [
            {
                "id": 1,
                "code": "HTD-2025-001",
                "name": "Highland Tower Development",
                "client": "Highland Properties LLC",
                "status": "Active",
                "start_date": date(2025, 1, 5),
                "end_date": date(2025, 12, 15)
            },
            {
                "id": 2,
                "code": "RVP-2025-002",
                "name": "Riverfront Plaza",
                "client": "Metro Development Corp",
                "status": "Planning",
                "start_date": date(2025, 3, 10),
                "end_date": date(2026, 6, 30)
            }
        ]
        
        # Apply filters if provided
        if filters:
            for key, value in filters.items():
                projects = [p for p in projects if str(p.get(key, "")).lower() == str(value).lower()]
        
        return ProjectAPI.success_response(projects, "Projects retrieved successfully")
    
    @staticmethod
    def get_project(project_id: int) -> Dict[str, Any]:
        """
        Get a specific project by ID.
        
        Args:
            project_id: The project ID
            
        Returns:
            API response with project data
        """
        # In a real implementation, this would query the database
        # Here we return sample data
        if project_id == 1:
            project = {
                "id": 1,
                "code": "HTD-2025-001",
                "name": "Highland Tower Development",
                "client": "Highland Properties LLC",
                "type": "Commercial",
                "address": "1250 Highland Avenue",
                "location": "Metro City, State",
                "start_date": date(2025, 1, 5),
                "end_date": date(2025, 12, 15),
                "duration": 345,
                "base_budget": 6800000,
                "contingency_percent": 10.0,
                "contingency_amount": 680000,
                "total_budget": 7480000,
                "contract_type": "Guaranteed Maximum Price",
                "payment_terms": "Monthly",
                "status": "Active"
            }
            return ProjectAPI.success_response(project, "Project retrieved successfully")
        else:
            return ProjectAPI.error_response("Project not found", 404)
    
    @staticmethod
    def create_project(project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new project.
        
        Args:
            project_data: Dictionary of project data
            
        Returns:
            API response with created project data
        """
        # In a real implementation, this would insert to the database
        # Here we just return the data with an ID added
        required_fields = ["name", "code", "client", "start_date", "end_date"]
        
        # Validate required fields
        missing_fields = [field for field in required_fields if field not in project_data]
        if missing_fields:
            return ProjectAPI.error_response(f"Missing required fields: {', '.join(missing_fields)}", 400)
        
        # Create project (simulate database insert)
        project_data["id"] = 3  # Next available ID
        project_data["created_at"] = datetime.now()
        
        return ProjectAPI.success_response(project_data, "Project created successfully")
    
    @staticmethod
    def update_project(project_id: int, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing project.
        
        Args:
            project_id: The project ID to update
            project_data: Dictionary of project data to update
            
        Returns:
            API response with updated project data
        """
        # In a real implementation, this would update the database
        # Here we just return the data
        if project_id not in [1, 2]:
            return ProjectAPI.error_response("Project not found", 404)
        
        # Update project (simulate database update)
        project_data["id"] = project_id
        project_data["updated_at"] = datetime.now()
        
        return ProjectAPI.success_response(project_data, "Project updated successfully")
    
    @staticmethod
    def delete_project(project_id: int) -> Dict[str, Any]:
        """
        Delete a project.
        
        Args:
            project_id: The project ID to delete
            
        Returns:
            API response confirming deletion
        """
        # In a real implementation, this would delete from the database
        if project_id not in [1, 2]:
            return ProjectAPI.error_response("Project not found", 404)
        
        # Delete project (simulate database delete)
        return ProjectAPI.success_response(None, "Project deleted successfully")

class EngineeringAPI(APIEndpoint):
    """Engineering-related API endpoints."""
    
    @staticmethod
    def get_rfis(project_id: int, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get RFIs for a project, optionally filtered.
        
        Args:
            project_id: The project ID
            filters: Dictionary of filter criteria
            
        Returns:
            API response with RFIs data
        """
        # In a real implementation, this would query the database
        # Here we return sample data
        rfis = [
            {
                "id": 1,
                "project_id": project_id,
                "number": "RFI-001",
                "subject": "Foundation Detail Clarification",
                "date_submitted": date(2025, 3, 10),
                "date_required": date(2025, 3, 17),
                "status": "Answered",
                "assignee": "Jennifer Wilson"
            },
            {
                "id": 2,
                "project_id": project_id,
                "number": "RFI-002",
                "subject": "Steel Connection Details",
                "date_submitted": date(2025, 4, 5),
                "date_required": date(2025, 4, 12),
                "status": "Answered",
                "assignee": "Steven Thompson"
            },
            {
                "id": 3,
                "project_id": project_id,
                "number": "RFI-003",
                "subject": "MEP Coordination",
                "date_submitted": date(2025, 4, 20),
                "date_required": date(2025, 4, 27),
                "status": "Open",
                "assignee": "Karen Davis"
            }
        ]
        
        # Apply filters if provided
        if filters:
            for key, value in filters.items():
                rfis = [r for r in rfis if str(r.get(key, "")).lower() == str(value).lower()]
        
        return EngineeringAPI.success_response(rfis, "RFIs retrieved successfully")
    
    @staticmethod
    def get_submittals(project_id: int, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get submittals for a project, optionally filtered.
        
        Args:
            project_id: The project ID
            filters: Dictionary of filter criteria
            
        Returns:
            API response with submittals data
        """
        # In a real implementation, this would query the database
        # Here we return sample data
        submittals = [
            {
                "id": 1,
                "project_id": project_id,
                "number": "SUB-001",
                "description": "Concrete Mix Design",
                "date_submitted": date(2025, 3, 1),
                "date_required": date(2025, 3, 15),
                "status": "Approved",
                "assignee": "Jennifer Wilson"
            },
            {
                "id": 2,
                "project_id": project_id,
                "number": "SUB-002",
                "description": "Rebar Shop Drawings",
                "date_submitted": date(2025, 3, 5),
                "date_required": date(2025, 3, 19),
                "status": "Approved with Comments",
                "assignee": "Steven Thompson"
            },
            {
                "id": 3,
                "project_id": project_id,
                "number": "SUB-003",
                "description": "Structural Steel Shop Drawings",
                "date_submitted": date(2025, 3, 15),
                "date_required": date(2025, 3, 29),
                "status": "Pending Review",
                "assignee": "Steven Thompson"
            },
            {
                "id": 4,
                "project_id": project_id,
                "number": "SUB-004",
                "description": "Glazing Samples",
                "date_submitted": date(2025, 3, 20),
                "date_required": date(2025, 4, 3),
                "status": "Pending Review",
                "assignee": "Jennifer Wilson"
            }
        ]
        
        # Apply filters if provided
        if filters:
            for key, value in filters.items():
                submittals = [s for s in submittals if str(s.get(key, "")).lower() == str(value).lower()]
        
        return EngineeringAPI.success_response(submittals, "Submittals retrieved successfully")

class WeatherAPI(APIEndpoint):
    """Weather-related API endpoints."""
    
    @staticmethod
    def get_weather(project_id: int, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get weather data for a project location.
        
        Args:
            project_id: The project ID
            date: Optional date string in ISO format (YYYY-MM-DD)
            
        Returns:
            API response with weather data
        """
        # In a real implementation, this would query a weather service API
        # Here we return sample data
        
        # If date is not provided, use current date
        if not date:
            current_date = datetime.now().date()
        else:
            try:
                current_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                return WeatherAPI.error_response("Invalid date format. Use YYYY-MM-DD", 400)
        
        # Sample weather data
        weather_data = {
            "project_id": project_id,
            "date": current_date,
            "location": "Metro City, State",
            "temperature": {
                "current": 72,
                "min": 65,
                "max": 78,
                "unit": "F"
            },
            "conditions": "Sunny",
            "humidity": 45,
            "wind": {
                "speed": 8,
                "direction": "NW",
                "unit": "mph"
            },
            "precipitation": {
                "probability": 10,
                "amount": 0,
                "unit": "in"
            },
            "forecast": [
                {
                    "date": (current_date.replace(day=current_date.day+1)).isoformat(),
                    "conditions": "Partly Cloudy",
                    "temperature": {"min": 68, "max": 75}
                },
                {
                    "date": (current_date.replace(day=current_date.day+2)).isoformat(),
                    "conditions": "Sunny",
                    "temperature": {"min": 70, "max": 78}
                },
                {
                    "date": (current_date.replace(day=current_date.day+3)).isoformat(),
                    "conditions": "Rainy",
                    "temperature": {"min": 65, "max": 68}
                },
                {
                    "date": (current_date.replace(day=current_date.day+4)).isoformat(),
                    "conditions": "Thunderstorm",
                    "temperature": {"min": 62, "max": 65}
                }
            ]
        }
        
        return WeatherAPI.success_response(weather_data, "Weather data retrieved successfully")

# Define API routes mapping
API_ROUTES = {
    # Project routes
    "GET /api/projects": ProjectAPI.get_projects,
    "GET /api/projects/{id}": ProjectAPI.get_project,
    "POST /api/projects": ProjectAPI.create_project,
    "PUT /api/projects/{id}": ProjectAPI.update_project,
    "DELETE /api/projects/{id}": ProjectAPI.delete_project,
    
    # Engineering routes
    "GET /api/projects/{id}/rfis": EngineeringAPI.get_rfis,
    "GET /api/projects/{id}/submittals": EngineeringAPI.get_submittals,
    
    # Weather routes
    "GET /api/projects/{id}/weather": WeatherAPI.get_weather
}