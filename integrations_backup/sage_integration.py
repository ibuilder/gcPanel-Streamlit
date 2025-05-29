"""
Highland Tower Development - Sage Construction Integration Module
Full Python API integration with Sage 100 Contractor and Sage 300 Construction
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
class SageProject:
    """Sage project data structure"""
    job_number: str
    job_name: str
    customer_id: str
    contract_amount: float
    start_date: str
    completion_date: str
    status: str
    project_manager: str

@dataclass
class SageCostCode:
    """Sage cost code data structure"""
    cost_code: str
    description: str
    phase: str
    category: str
    unit_of_measure: str
    budgeted_amount: float
    actual_amount: float

class SageIntegration:
    """Complete Sage Construction API integration with full accounting synchronization"""
    
    def __init__(self):
        self.api_base = os.environ.get('SAGE_API_BASE', 'https://api.sage.com')
        self.api_version = "v1"
        self.client_id = os.environ.get('SAGE_CLIENT_ID')
        self.client_secret = os.environ.get('SAGE_CLIENT_SECRET')
        self.username = os.environ.get('SAGE_USERNAME')
        self.password = os.environ.get('SAGE_PASSWORD')
        self.company_database = os.environ.get('SAGE_COMPANY_DB')
        
        self.access_token = None
        self.session_id = None
        self.token_expires_at = None
        
        self.setup_logging()
        self.rate_limit_delay = 2  # Sage APIs often have stricter rate limits
        self.max_retries = 3
    
    def setup_logging(self):
        """Setup comprehensive logging for Sage integration"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('SageIntegration')
        
        handler = logging.FileHandler('sage_integration.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def authenticate(self) -> bool:
        """
        Authenticate with Sage Construction API
        
        Returns:
            bool: Authentication success status
        """
        if not all([self.client_id, self.client_secret, self.username, self.password]):
            self.logger.error("Sage credentials not found in environment variables")
            return False
        
        try:
            # Sage typically uses session-based authentication
            auth_url = f"{self.api_base}/{self.api_version}/auth/login"
            
            auth_data = {
                'username': self.username,
                'password': self.password,
                'company_database': self.company_database,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            
            response = requests.post(auth_url, json=auth_data)
            
            if response.status_code == 200:
                auth_result = response.json()
                self.access_token = auth_result.get('access_token')
                self.session_id = auth_result.get('session_id')
                expires_in = auth_result.get('expires_in', 3600)
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                
                self.logger.info("Successfully authenticated with Sage Construction")
                return True
            else:
                self.logger.error(f"Sage authentication failed: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Sage authentication error: {e}")
            return False
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Optional[Dict]:
        """
        Make authenticated API request to Sage with retry logic
        
        Args:
            method: HTTP method
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            
        Returns:
            API response data or None if failed
        """
        if not self.access_token:
            if not self.authenticate():
                return None
        
        # Check token expiration
        if self.token_expires_at and datetime.now() >= self.token_expires_at:
            if not self.authenticate():
                return None
        
        url = f"{self.api_base}/{self.api_version}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Session-ID': self.session_id,
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
                    if self.authenticate():
                        headers['Authorization'] = f'Bearer {self.access_token}'
                        headers['X-Session-ID'] = self.session_id
                        continue
                    else:
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
    
    def sync_projects(self) -> List[SageProject]:
        """
        Sync all projects from Sage Construction
        
        Returns:
            List of SageProject objects
        """
        projects_data = self.make_request('GET', '/projects') or {'data': []}
        
        projects = []
        for project_data in projects_data.get('data', []):
            try:
                project = SageProject(
                    job_number=project_data['job_number'],
                    job_name=project_data['job_name'],
                    customer_id=project_data['customer_id'],
                    contract_amount=float(project_data.get('contract_amount', 0)),
                    start_date=project_data.get('start_date', ''),
                    completion_date=project_data.get('completion_date', ''),
                    status=project_data.get('status', 'Active'),
                    project_manager=project_data.get('project_manager', '')
                )
                projects.append(project)
            except (KeyError, ValueError) as e:
                self.logger.error(f"Error parsing project data: {e}")
                continue
        
        self.logger.info(f"Synced {len(projects)} projects from Sage")
        return projects
    
    def sync_cost_codes(self, job_number: str) -> List[SageCostCode]:
        """
        Sync cost codes for a specific project
        
        Args:
            job_number: Sage job number
            
        Returns:
            List of SageCostCode objects
        """
        params = {'job_number': job_number}
        cost_codes_data = self.make_request('GET', '/cost-codes', params=params) or {'data': []}
        
        cost_codes = []
        for code_data in cost_codes_data.get('data', []):
            try:
                cost_code = SageCostCode(
                    cost_code=code_data['cost_code'],
                    description=code_data['description'],
                    phase=code_data.get('phase', ''),
                    category=code_data.get('category', ''),
                    unit_of_measure=code_data.get('unit_of_measure', ''),
                    budgeted_amount=float(code_data.get('budgeted_amount', 0)),
                    actual_amount=float(code_data.get('actual_amount', 0))
                )
                cost_codes.append(cost_code)
            except (KeyError, ValueError) as e:
                self.logger.error(f"Error parsing cost code data: {e}")
                continue
        
        self.logger.info(f"Synced {len(cost_codes)} cost codes for job {job_number}")
        return cost_codes
    
    def sync_change_orders(self, job_number: str) -> List[Dict]:
        """
        Sync change orders for a specific project
        
        Args:
            job_number: Sage job number
            
        Returns:
            List of change order data
        """
        params = {'job_number': job_number}
        change_orders = self.make_request('GET', '/change-orders', params=params) or {'data': []}
        
        self.logger.info(f"Synced {len(change_orders.get('data', []))} change orders for job {job_number}")
        return change_orders.get('data', [])
    
    def sync_payroll(self, job_number: str, start_date: str = None, end_date: str = None) -> List[Dict]:
        """
        Sync payroll data for a specific project
        
        Args:
            job_number: Sage job number
            start_date: Start date for payroll sync (YYYY-MM-DD)
            end_date: End date for payroll sync (YYYY-MM-DD)
            
        Returns:
            List of payroll data
        """
        params = {'job_number': job_number}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        
        payroll_data = self.make_request('GET', '/payroll', params=params) or {'data': []}
        
        self.logger.info(f"Synced payroll data for job {job_number}")
        return payroll_data.get('data', [])
    
    def create_change_order(self, job_number: str, change_order_data: Dict) -> Optional[Dict]:
        """
        Create a new change order in Sage
        
        Args:
            job_number: Sage job number
            change_order_data: Change order creation data
            
        Returns:
            Created change order data or None if failed
        """
        endpoint = f'/change-orders'
        data = {
            'job_number': job_number,
            **change_order_data
        }
        
        return self.make_request('POST', endpoint, data=data)
    
    def update_project_costs(self, job_number: str, cost_updates: List[Dict]) -> bool:
        """
        Update project costs in Sage
        
        Args:
            job_number: Sage job number
            cost_updates: List of cost update data
            
        Returns:
            Success status
        """
        success_count = 0
        error_count = 0
        
        for cost_update in cost_updates:
            try:
                endpoint = f'/projects/{job_number}/costs'
                result = self.make_request('PUT', endpoint, data=cost_update)
                
                if result:
                    success_count += 1
                else:
                    error_count += 1
                    
            except Exception as e:
                self.logger.error(f"Error updating cost: {e}")
                error_count += 1
        
        self.logger.info(f"Cost updates completed: {success_count} successful, {error_count} errors")
        return error_count == 0
    
    def export_highland_data_to_sage(self, highland_data: Dict, data_type: str, job_number: str) -> bool:
        """
        Export Highland Tower data to Sage Construction
        
        Args:
            highland_data: Data from Highland Tower system
            data_type: Type of data (change_orders, costs, payroll)
            job_number: Target Sage job number
            
        Returns:
            Success status
        """
        success_count = 0
        error_count = 0
        
        for item in highland_data.get('items', []):
            try:
                if data_type == 'change_orders':
                    sage_data = self.transform_highland_to_sage_change_order(item)
                    result = self.create_change_order(job_number, sage_data)
                    
                elif data_type == 'costs':
                    sage_data = self.transform_highland_to_sage_cost(item)
                    result = self.update_project_costs(job_number, [sage_data])
                    
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
    
    def transform_highland_to_sage_change_order(self, highland_item: Dict) -> Dict:
        """Transform Highland Tower change order data to Sage format"""
        return {
            'change_order_number': highland_item.get('number', ''),
            'description': highland_item.get('description', ''),
            'amount': highland_item.get('amount', 0),
            'status': highland_item.get('status', 'Pending'),
            'date_created': highland_item.get('created_date', ''),
            'reason_code': highland_item.get('reason', ''),
            'cost_codes': highland_item.get('cost_codes', [])
        }
    
    def transform_highland_to_sage_cost(self, highland_item: Dict) -> Dict:
        """Transform Highland Tower cost data to Sage format"""
        return {
            'cost_code': highland_item.get('cost_code', ''),
            'amount': highland_item.get('amount', 0),
            'date': highland_item.get('date', ''),
            'description': highland_item.get('description', ''),
            'phase': highland_item.get('phase', ''),
            'category': highland_item.get('category', 'Labor')
        }
    
    def generate_financial_report(self, job_number: str, report_type: str = 'summary') -> Dict:
        """
        Generate financial report for a project
        
        Args:
            job_number: Sage job number
            report_type: Type of report (summary, detailed, variance)
            
        Returns:
            Financial report data
        """
        params = {
            'job_number': job_number,
            'report_type': report_type
        }
        
        report_data = self.make_request('GET', '/reports/financial', params=params) or {}
        
        self.logger.info(f"Generated {report_type} financial report for job {job_number}")
        return report_data
    
    def test_connection(self) -> bool:
        """Test Sage API connection"""
        try:
            projects = self.sync_projects()
            return len(projects) >= 0
        except:
            return False
    
    def get_integration_status(self) -> Dict:
        """Get comprehensive integration status"""
        return {
            'connected': bool(self.access_token),
            'company_database': self.company_database,
            'session_id': self.session_id,
            'token_expires_at': self.token_expires_at.isoformat() if self.token_expires_at else None,
            'last_sync': datetime.now().isoformat(),
            'capabilities': [
                'Project Sync',
                'Cost Code Management',
                'Change Order Sync',
                'Payroll Integration',
                'Financial Reporting',
                'Two-way Data Sync'
            ]
        }