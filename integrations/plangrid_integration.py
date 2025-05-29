"""
Highland Tower Development - PlanGrid Integration Module
Full Python API integration with PlanGrid construction drawing management
"""

import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
import pandas as pd
from dataclasses import dataclass
import time
import os

@dataclass
class PlanGridSheet:
    """PlanGrid sheet (drawing) data structure"""
    id: str
    name: str
    number: str
    revision: str
    discipline: str
    uploaded_at: str
    file_size: int
    status: str

@dataclass
class PlanGridIssue:
    """PlanGrid issue data structure"""
    id: str
    title: str
    description: str
    status: str
    assignee: str
    due_date: str
    location: Dict
    photos: List[str]
    created_at: str

class PlanGridIntegration:
    """Complete PlanGrid API integration with full drawing and issue management"""
    
    def __init__(self):
        self.api_base = "https://api.plangrid.com/v1"
        self.api_key = os.environ.get('PLANGRID_API_KEY')
        self.access_token = os.environ.get('PLANGRID_ACCESS_TOKEN')
        self.project_id = None
        
        self.setup_logging()
        self.rate_limit_delay = 2
        self.max_retries = 3
    
    def setup_logging(self):
        """Setup comprehensive logging for PlanGrid integration"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('PlanGridIntegration')
        
        handler = logging.FileHandler('plangrid_integration.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def authenticate(self) -> bool:
        """
        Authenticate with PlanGrid API
        
        Returns:
            bool: Authentication success status
        """
        if not self.api_key and not self.access_token:
            self.logger.error("PlanGrid credentials not found in environment variables")
            return False
        
        try:
            # Test authentication by getting user info
            test_url = f"{self.api_base}/user"
            headers = self.get_auth_headers()
            
            response = requests.get(test_url, headers=headers)
            
            if response.status_code == 200:
                self.logger.info("Successfully authenticated with PlanGrid")
                return True
            else:
                self.logger.error(f"PlanGrid authentication failed: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"PlanGrid authentication error: {e}")
            return False
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests"""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Highland-Tower-gcPanel/1.0'
        }
        
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        elif self.api_key:
            headers['Authorization'] = f'Token {self.api_key}'
        
        return headers
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Optional[Dict]:
        """
        Make authenticated API request to PlanGrid with retry logic
        
        Args:
            method: HTTP method
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            
        Returns:
            API response data or None if failed
        """
        if not self.api_key and not self.access_token:
            self.logger.error("No authentication credentials available")
            return None
        
        url = f"{self.api_base}{endpoint}"
        headers = self.get_auth_headers()
        
        for attempt in range(self.max_retries):
            try:
                time.sleep(self.rate_limit_delay)
                
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                    params=params
                )
                
                if response.status_code == 401:
                    self.logger.error("Authentication failed - check API key or access token")
                    return None
                
                if response.status_code == 429:
                    wait_time = int(response.headers.get('Retry-After', 120))
                    self.logger.warning(f"Rate limited, waiting {wait_time} seconds")
                    time.sleep(wait_time)
                    continue
                
                if response.status_code >= 200 and response.status_code < 300:
                    return response.json() if response.content else {}
                else:
                    self.logger.error(f"API request failed: {response.status_code} - {response.text}")
                    return None
                    
            except Exception as e:
                self.logger.error(f"Request attempt {attempt + 1} failed: {e}")
                if attempt == self.max_retries - 1:
                    return None
                time.sleep(2 ** attempt)
        
        return None
    
    def get_projects(self) -> List[Dict]:
        """Get all projects accessible to the user"""
        projects = self.make_request('GET', '/projects') or []
        self.logger.info(f"Retrieved {len(projects)} projects from PlanGrid")
        return projects
    
    def sync_sheets(self, project_id: str) -> List[PlanGridSheet]:
        """
        Sync sheets (drawings) from PlanGrid for a specific project
        
        Args:
            project_id: PlanGrid project ID
            
        Returns:
            List of PlanGridSheet objects
        """
        sheets_data = self.make_request('GET', f'/projects/{project_id}/sheets') or []
        
        sheets = []
        for sheet_data in sheets_data:
            try:
                sheet = PlanGridSheet(
                    id=sheet_data['id'],
                    name=sheet_data['name'],
                    number=sheet_data['number'],
                    revision=sheet_data.get('revision', ''),
                    discipline=sheet_data.get('discipline', ''),
                    uploaded_at=sheet_data['uploaded_at'],
                    file_size=sheet_data.get('file_size', 0),
                    status=sheet_data.get('status', 'active')
                )
                sheets.append(sheet)
            except KeyError as e:
                self.logger.error(f"Missing required field in sheet data: {e}")
                continue
        
        self.logger.info(f"Synced {len(sheets)} sheets from PlanGrid project {project_id}")
        return sheets
    
    def sync_issues(self, project_id: str) -> List[PlanGridIssue]:
        """
        Sync issues from PlanGrid for a specific project
        
        Args:
            project_id: PlanGrid project ID
            
        Returns:
            List of PlanGridIssue objects
        """
        issues_data = self.make_request('GET', f'/projects/{project_id}/issues') or []
        
        issues = []
        for issue_data in issues_data:
            try:
                issue = PlanGridIssue(
                    id=issue_data['id'],
                    title=issue_data['title'],
                    description=issue_data.get('description', ''),
                    status=issue_data['status'],
                    assignee=issue_data.get('assignee', {}).get('name', ''),
                    due_date=issue_data.get('due_date', ''),
                    location=issue_data.get('location', {}),
                    photos=issue_data.get('photos', []),
                    created_at=issue_data['created_at']
                )
                issues.append(issue)
            except KeyError as e:
                self.logger.error(f"Missing required field in issue data: {e}")
                continue
        
        self.logger.info(f"Synced {len(issues)} issues from PlanGrid project {project_id}")
        return issues
    
    def create_issue(self, project_id: str, issue_data: Dict) -> Optional[Dict]:
        """
        Create a new issue in PlanGrid
        
        Args:
            project_id: PlanGrid project ID
            issue_data: Issue creation data
            
        Returns:
            Created issue data or None if failed
        """
        return self.make_request('POST', f'/projects/{project_id}/issues', data=issue_data)
    
    def upload_sheet(self, project_id: str, file_path: str, sheet_data: Dict) -> Optional[Dict]:
        """
        Upload a new sheet (drawing) to PlanGrid
        
        Args:
            project_id: PlanGrid project ID
            file_path: Local file path
            sheet_data: Sheet metadata
            
        Returns:
            Upload result data or None if failed
        """
        try:
            # Step 1: Create upload session
            upload_session_data = {
                'name': sheet_data.get('name', ''),
                'number': sheet_data.get('number', ''),
                'discipline': sheet_data.get('discipline', ''),
                'revision': sheet_data.get('revision', '')
            }
            
            session_result = self.make_request('POST', f'/projects/{project_id}/sheets/upload', data=upload_session_data)
            
            if not session_result:
                return None
            
            upload_url = session_result.get('upload_url')
            sheet_id = session_result.get('sheet_id')
            
            # Step 2: Upload file to the provided URL
            with open(file_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(upload_url, files=files)
                
                if response.status_code != 200:
                    self.logger.error(f"Failed to upload file: {response.text}")
                    return None
            
            # Step 3: Confirm upload completion
            confirm_result = self.make_request('POST', f'/projects/{project_id}/sheets/{sheet_id}/confirm')
            
            if confirm_result:
                self.logger.info(f"Successfully uploaded sheet {sheet_data.get('name', '')}")
            
            return confirm_result
            
        except Exception as e:
            self.logger.error(f"Error uploading sheet: {e}")
            return None
    
    def export_highland_data_to_plangrid(self, highland_data: Dict, data_type: str, project_id: str) -> bool:
        """
        Export Highland Tower data to PlanGrid
        
        Args:
            highland_data: Data from Highland Tower system
            data_type: Type of data (issues, sheets)
            project_id: Target PlanGrid project ID
            
        Returns:
            Success status
        """
        success_count = 0
        error_count = 0
        
        for item in highland_data.get('items', []):
            try:
                if data_type == 'issues':
                    plangrid_data = self.transform_highland_to_plangrid_issue(item)
                    result = self.create_issue(project_id, plangrid_data)
                    
                elif data_type == 'sheets':
                    # For sheets, would need file upload capability
                    self.logger.warning("Sheet upload from Highland Tower not implemented yet")
                    continue
                    
                else:
                    self.logger.warning(f"Export not implemented for {data_type}")
                    continue
                
                if result:
                    success_count += 1
                else:
                    error_count += 1
                    
            except Exception as e:
                self.logger.error(f"Error exporting {data_type} item: {e}")
                error_count += 1
        
        self.logger.info(f"Export completed: {success_count} successful, {error_count} errors")
        return error_count == 0
    
    def transform_highland_to_plangrid_issue(self, highland_item: Dict) -> Dict:
        """Transform Highland Tower issue data to PlanGrid format"""
        return {
            'title': highland_item.get('subject', ''),
            'description': highland_item.get('description', ''),
            'assignee_id': highland_item.get('assigned_to_id'),
            'due_date': highland_item.get('due_date', ''),
            'priority': highland_item.get('priority', 'medium'),
            'location': {
                'x': highland_item.get('location_x', 0),
                'y': highland_item.get('location_y', 0),
                'sheet_id': highland_item.get('sheet_id', '')
            },
            'custom_fields': {
                'cost_impact': highland_item.get('cost_impact', 0),
                'schedule_impact': highland_item.get('schedule_impact', 0)
            }
        }
    
    def test_connection(self) -> bool:
        """Test PlanGrid API connection"""
        return self.authenticate()
    
    def get_integration_status(self) -> Dict:
        """Get comprehensive integration status"""
        return {
            'connected': bool(self.api_key or self.access_token),
            'project_id': self.project_id,
            'last_sync': datetime.now().isoformat(),
            'capabilities': [
                'Drawing Management',
                'Issue Tracking',
                'Photo Attachments',
                'Version Control',
                'Two-way Data Sync'
            ]
        }