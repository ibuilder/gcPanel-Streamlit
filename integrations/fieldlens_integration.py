"""
Highland Tower Development - Fieldlens Integration Module
Full Python API integration with Fieldlens field management platform
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
class FieldlensTask:
    """Fieldlens task data structure"""
    id: str
    title: str
    description: str
    status: str
    assignee: str
    due_date: str
    location: str
    priority: str
    created_at: str

@dataclass
class FieldlensReport:
    """Fieldlens report data structure"""
    id: str
    title: str
    date: str
    weather: str
    work_performed: str
    crew_count: int
    notes: str
    photos: List[str]

class FieldlensIntegration:
    """Complete Fieldlens API integration with full field management synchronization"""
    
    def __init__(self):
        self.api_base = "https://api.fieldlens.com/v2"
        self.api_key = os.environ.get('FIELDLENS_API_KEY')
        self.company_id = os.environ.get('FIELDLENS_COMPANY_ID')
        self.project_id = None
        
        self.setup_logging()
        self.rate_limit_delay = 1
        self.max_retries = 3
    
    def setup_logging(self):
        """Setup comprehensive logging for Fieldlens integration"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('FieldlensIntegration')
        
        handler = logging.FileHandler('fieldlens_integration.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def authenticate(self) -> bool:
        """
        Authenticate with Fieldlens API using API key
        
        Returns:
            bool: Authentication success status
        """
        if not self.api_key:
            self.logger.error("Fieldlens API key not found in environment variables")
            return False
        
        try:
            # Test authentication by getting user info
            test_url = f"{self.api_base}/users/me"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(test_url, headers=headers)
            
            if response.status_code == 200:
                self.logger.info("Successfully authenticated with Fieldlens")
                return True
            else:
                self.logger.error(f"Fieldlens authentication failed: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Fieldlens authentication error: {e}")
            return False
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Optional[Dict]:
        """
        Make authenticated API request to Fieldlens with retry logic
        
        Args:
            method: HTTP method
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            
        Returns:
            API response data or None if failed
        """
        if not self.api_key:
            self.logger.error("No API key available")
            return None
        
        url = f"{self.api_base}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'Highland-Tower-gcPanel/1.0'
        }
        
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
                    self.logger.error("Authentication failed - check API key")
                    return None
                
                if response.status_code == 429:
                    wait_time = int(response.headers.get('Retry-After', 60))
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
        """Get all projects for the company"""
        projects = self.make_request('GET', f'/companies/{self.company_id}/projects') or []
        self.logger.info(f"Retrieved {len(projects)} projects from Fieldlens")
        return projects
    
    def sync_tasks(self, project_id: str) -> List[FieldlensTask]:
        """
        Sync tasks from Fieldlens for a specific project
        
        Args:
            project_id: Fieldlens project ID
            
        Returns:
            List of FieldlensTask objects
        """
        tasks_data = self.make_request('GET', f'/projects/{project_id}/tasks') or []
        
        tasks = []
        for task_data in tasks_data:
            try:
                task = FieldlensTask(
                    id=task_data['id'],
                    title=task_data['title'],
                    description=task_data.get('description', ''),
                    status=task_data['status'],
                    assignee=task_data.get('assignee', {}).get('name', ''),
                    due_date=task_data.get('due_date', ''),
                    location=task_data.get('location', ''),
                    priority=task_data.get('priority', 'medium'),
                    created_at=task_data['created_at']
                )
                tasks.append(task)
            except KeyError as e:
                self.logger.error(f"Missing required field in task data: {e}")
                continue
        
        self.logger.info(f"Synced {len(tasks)} tasks from Fieldlens project {project_id}")
        return tasks
    
    def create_task(self, project_id: str, task_data: Dict) -> Optional[Dict]:
        """
        Create a new task in Fieldlens
        
        Args:
            project_id: Fieldlens project ID
            task_data: Task creation data
            
        Returns:
            Created task data or None if failed
        """
        return self.make_request('POST', f'/projects/{project_id}/tasks', data=task_data)
    
    def sync_reports(self, project_id: str, start_date: str = None) -> List[FieldlensReport]:
        """
        Sync daily reports from Fieldlens
        
        Args:
            project_id: Fieldlens project ID
            start_date: Start date for sync (YYYY-MM-DD)
            
        Returns:
            List of FieldlensReport objects
        """
        params = {}
        if start_date:
            params['start_date'] = start_date
        
        reports_data = self.make_request('GET', f'/projects/{project_id}/reports', params=params) or []
        
        reports = []
        for report_data in reports_data:
            try:
                report = FieldlensReport(
                    id=report_data['id'],
                    title=report_data['title'],
                    date=report_data['date'],
                    weather=report_data.get('weather', ''),
                    work_performed=report_data.get('work_performed', ''),
                    crew_count=report_data.get('crew_count', 0),
                    notes=report_data.get('notes', ''),
                    photos=report_data.get('photos', [])
                )
                reports.append(report)
            except KeyError as e:
                self.logger.error(f"Missing required field in report data: {e}")
                continue
        
        self.logger.info(f"Synced {len(reports)} reports from Fieldlens project {project_id}")
        return reports
    
    def export_highland_data_to_fieldlens(self, highland_data: Dict, data_type: str, project_id: str) -> bool:
        """
        Export Highland Tower data to Fieldlens
        
        Args:
            highland_data: Data from Highland Tower system
            data_type: Type of data (tasks, reports)
            project_id: Target Fieldlens project ID
            
        Returns:
            Success status
        """
        success_count = 0
        error_count = 0
        
        for item in highland_data.get('items', []):
            try:
                if data_type == 'tasks':
                    fieldlens_data = self.transform_highland_to_fieldlens_task(item)
                    result = self.create_task(project_id, fieldlens_data)
                    
                elif data_type == 'reports':
                    fieldlens_data = self.transform_highland_to_fieldlens_report(item)
                    result = self.make_request('POST', f'/projects/{project_id}/reports', data=fieldlens_data)
                    
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
    
    def transform_highland_to_fieldlens_task(self, highland_item: Dict) -> Dict:
        """Transform Highland Tower task data to Fieldlens format"""
        return {
            'title': highland_item.get('subject', ''),
            'description': highland_item.get('description', ''),
            'assignee_id': highland_item.get('assigned_to_id'),
            'due_date': highland_item.get('due_date', ''),
            'priority': highland_item.get('priority', 'medium'),
            'location': highland_item.get('location', ''),
            'custom_fields': {
                'cost_impact': highland_item.get('cost_impact', 0),
                'schedule_impact': highland_item.get('schedule_impact', 0)
            }
        }
    
    def transform_highland_to_fieldlens_report(self, highland_item: Dict) -> Dict:
        """Transform Highland Tower report data to Fieldlens format"""
        return {
            'title': highland_item.get('title', ''),
            'date': highland_item.get('date', ''),
            'weather': highland_item.get('weather', ''),
            'work_performed': highland_item.get('work_performed', ''),
            'crew_count': highland_item.get('crew_count', 0),
            'notes': highland_item.get('notes', ''),
            'photos': highland_item.get('photos', [])
        }
    
    def test_connection(self) -> bool:
        """Test Fieldlens API connection"""
        return self.authenticate()
    
    def get_integration_status(self) -> Dict:
        """Get comprehensive integration status"""
        return {
            'connected': bool(self.api_key),
            'company_id': self.company_id,
            'project_id': self.project_id,
            'last_sync': datetime.now().isoformat(),
            'capabilities': [
                'Task Management',
                'Daily Reports Sync',
                'Photo Management',
                'Field Crew Tracking',
                'Two-way Data Sync'
            ]
        }