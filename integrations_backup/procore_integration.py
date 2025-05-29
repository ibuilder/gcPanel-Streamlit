"""
Highland Tower Development - Procore Integration Module
Full Python API integration with real data synchronization, import/export workflows
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
class ProcoreProject:
    """Procore project data structure"""
    id: int
    name: str
    company_id: int
    address: str
    city: str
    state: str
    zip_code: str
    project_number: str
    start_date: str
    completion_date: str
    active: bool

@dataclass
class ProcoreRFI:
    """Procore RFI data structure"""
    id: int
    number: str
    subject: str
    question: str
    status: str
    created_by: Dict
    assigned_to: Dict
    created_at: str
    due_date: str
    project_id: int

class ProcoreIntegration:
    """Complete Procore API integration with full CRUD operations"""
    
    def __init__(self):
        self.api_base = "https://app.procore.com/rest/v1.0"
        self.client_id = os.environ.get('PROCORE_CLIENT_ID')
        self.client_secret = os.environ.get('PROCORE_CLIENT_SECRET') 
        self.redirect_uri = os.environ.get('PROCORE_REDIRECT_URI', 'urn:ietf:wg:oauth:2.0:oob')
        self.access_token = None
        self.refresh_token = None
        self.company_id = None
        self.project_id = None
        self.setup_logging()
        self.rate_limit_delay = 1  # seconds between requests
        self.max_retries = 3
    
    def setup_logging(self):
        """Setup comprehensive logging"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('ProcoreIntegration')
        
        # Create file handler for integration logs
        handler = logging.FileHandler('procore_integration.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def authenticate(self, authorization_code: str = None) -> bool:
        """
        Complete OAuth 2.0 authentication with Procore
        
        Args:
            authorization_code: OAuth authorization code from user consent
            
        Returns:
            bool: Authentication success status
        """
        if not self.client_id or not self.client_secret:
            self.logger.error("Procore credentials not found in environment variables")
            return False
        
        try:
            # Step 1: Get authorization URL (manual step for user)
            if not authorization_code:
                auth_url = (
                    f"https://app.procore.com/oauth/authorize"
                    f"?client_id={self.client_id}"
                    f"&response_type=code"
                    f"&redirect_uri={self.redirect_uri}"
                    f"&state=highland_tower_integration"
                )
                self.logger.info(f"Authorization URL: {auth_url}")
                return False
            
            # Step 2: Exchange code for access token
            token_url = "https://app.procore.com/oauth/token"
            token_data = {
                'grant_type': 'authorization_code',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': authorization_code,
                'redirect_uri': self.redirect_uri
            }
            
            response = requests.post(token_url, data=token_data)
            if response.status_code == 200:
                token_info = response.json()
                self.access_token = token_info.get('access_token')
                self.refresh_token = token_info.get('refresh_token')
                self.logger.info("Successfully authenticated with Procore")
                return True
            else:
                self.logger.error(f"Procore authentication failed: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Procore authentication error: {e}")
            return False
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Optional[Dict]:
        """
        Make authenticated API request with retry logic and rate limiting
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            
        Returns:
            API response data or None if failed
        """
        if not self.access_token:
            self.logger.error("No access token available")
            return None
        
        url = f"{self.api_base}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Highland-Tower-gcPanel/1.0'
        }
        
        for attempt in range(self.max_retries):
            try:
                # Rate limiting
                time.sleep(self.rate_limit_delay)
                
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                    params=params
                )
                
                if response.status_code == 401:
                    # Token expired, try to refresh
                    if self.refresh_access_token():
                        headers['Authorization'] = f'Bearer {self.access_token}'
                        continue
                    else:
                        self.logger.error("Authentication failed - need to re-authenticate")
                        return None
                
                if response.status_code == 429:
                    # Rate limited, wait and retry
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
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return None
    
    def sync_rfis(self, company_id: int, project_id: int) -> List[ProcoreRFI]:
        """
        Sync RFIs from Procore to Highland Tower system
        
        Args:
            company_id: Procore company ID
            project_id: Procore project ID
            
        Returns:
            List of ProcoreRFI objects
        """
        params = {
            'company_id': company_id,
            'project_id': project_id
        }
        
        rfis_data = self.make_request('GET', '/rfis', params=params) or []
        
        rfis = []
        for rfi_data in rfis_data:
            try:
                rfi = ProcoreRFI(
                    id=rfi_data['id'],
                    number=rfi_data['number'],
                    subject=rfi_data['subject'],
                    question=rfi_data['question'],
                    status=rfi_data['status'],
                    created_by=rfi_data['created_by'],
                    assigned_to=rfi_data.get('assigned_to', {}),
                    created_at=rfi_data['created_at'],
                    due_date=rfi_data.get('due_date', ''),
                    project_id=project_id
                )
                rfis.append(rfi)
            except KeyError as e:
                self.logger.error(f"Missing required field in RFI data: {e}")
                continue
        
        self.logger.info(f"Synced {len(rfis)} RFIs from Procore project {project_id}")
        return rfis
    
    def export_highland_data_to_procore(self, highland_data: Dict, data_type: str) -> bool:
        """
        Export Highland Tower data to Procore
        
        Args:
            highland_data: Data from Highland Tower system
            data_type: Type of data (rfis, daily_reports, submittals)
            
        Returns:
            Success status
        """
        if not self.company_id or not self.project_id:
            self.logger.error("Company ID and Project ID must be set for export")
            return False
        
        success_count = 0
        error_count = 0
        
        for item in highland_data.get('items', []):
            try:
                # Transform Highland Tower data to Procore format
                procore_data = self.transform_highland_to_procore(item, data_type)
                
                if data_type == 'rfis':
                    result = self.make_request('POST', '/rfis', data=procore_data, 
                                             params={'company_id': self.company_id, 'project_id': self.project_id})
                elif data_type == 'daily_reports':
                    result = self.make_request('POST', '/daily_logs', data=procore_data, 
                                             params={'company_id': self.company_id, 'project_id': self.project_id})
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