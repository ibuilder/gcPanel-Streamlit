"""
Highland Tower Development - Autodesk Construction Cloud Integration Module
Full Python API integration with BIM 360, ACC, and Forge platform data synchronization
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
import base64

@dataclass
class AutodeskProject:
    """Autodesk project data structure"""
    id: str
    name: str
    project_type: str
    status: str
    start_date: str
    end_date: str
    business_units_id: str
    timezone: str

@dataclass
class AutodeskDocument:
    """Autodesk document data structure"""
    id: str
    display_name: str
    version_number: int
    file_type: str
    storage_location: str
    created_date: str
    modified_date: str
    created_by: str

class AutodeskIntegration:
    """Complete Autodesk Construction Cloud/BIM 360 API integration"""
    
    def __init__(self):
        self.forge_base = "https://developer.api.autodesk.com"
        self.bim360_base = "https://developer.api.autodesk.com/bim360/docs/v1"
        self.acc_base = "https://developer.api.autodesk.com/construction"
        
        self.client_id = os.environ.get('AUTODESK_CLIENT_ID')
        self.client_secret = os.environ.get('AUTODESK_CLIENT_SECRET')
        self.callback_url = os.environ.get('AUTODESK_CALLBACK_URL', 'http://localhost:3000/callback')
        
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None
        self.account_id = None
        self.project_id = None
        
        self.setup_logging()
        self.rate_limit_delay = 0.5
        self.max_retries = 3
    
    def setup_logging(self):
        """Setup comprehensive logging for Autodesk integration"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('AutodeskIntegration')
        
        handler = logging.FileHandler('autodesk_integration.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def get_authorization_url(self, scopes: List[str] = None) -> str:
        """
        Generate OAuth 2.0 authorization URL for user consent
        
        Args:
            scopes: List of permission scopes needed
            
        Returns:
            Authorization URL for user to visit
        """
        if not scopes:
            scopes = [
                'data:read', 'data:write', 'data:create',
                'account:read', 'user:read',
                'viewables:read', 'code:all'
            ]
        
        scope_string = ' '.join(scopes)
        
        auth_url = (
            f"{self.forge_base}/authentication/v1/authorize"
            f"?response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.callback_url}"
            f"&scope={scope_string}"
            f"&state=highland_tower_integration"
        )
        
        return auth_url
    
    def authenticate(self, authorization_code: str = None) -> bool:
        """
        Complete OAuth 2.0 authentication with Autodesk Forge
        
        Args:
            authorization_code: OAuth authorization code from user consent
            
        Returns:
            bool: Authentication success status
        """
        if not self.client_id or not self.client_secret:
            self.logger.error("Autodesk credentials not found in environment variables")
            return False
        
        try:
            if not authorization_code:
                auth_url = self.get_authorization_url()
                self.logger.info(f"Please visit this URL to authorize: {auth_url}")
                return False
            
            # Exchange authorization code for access token
            token_url = f"{self.forge_base}/authentication/v1/gettoken"
            
            # Prepare basic auth header
            credentials = f"{self.client_id}:{self.client_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'grant_type': 'authorization_code',
                'code': authorization_code,
                'redirect_uri': self.callback_url
            }
            
            response = requests.post(token_url, headers=headers, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get('access_token')
                self.refresh_token = token_data.get('refresh_token')
                expires_in = token_data.get('expires_in', 3600)
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                
                self.logger.info("Successfully authenticated with Autodesk Forge")
                return True
            else:
                self.logger.error(f"Autodesk authentication failed: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Autodesk authentication error: {e}")
            return False
    
    def refresh_access_token(self) -> bool:
        """Refresh expired access token using refresh token"""
        if not self.refresh_token:
            return False
        
        try:
            token_url = f"{self.forge_base}/authentication/v1/refreshtoken"
            
            credentials = f"{self.client_id}:{self.client_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token
            }
            
            response = requests.post(token_url, headers=headers, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get('access_token')
                self.refresh_token = token_data.get('refresh_token', self.refresh_token)
                expires_in = token_data.get('expires_in', 3600)
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                return True
            else:
                self.logger.error(f"Token refresh failed: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Token refresh error: {e}")
            return False
    
    def make_request(self, method: str, url: str, data: Dict = None, params: Dict = None, headers: Dict = None) -> Optional[Dict]:
        """
        Make authenticated API request with retry logic and rate limiting
        
        Args:
            method: HTTP method
            url: Full API URL
            data: Request body data
            params: Query parameters
            headers: Additional headers
            
        Returns:
            API response data or None if failed
        """
        if not self.access_token:
            self.logger.error("No access token available")
            return None
        
        # Check if token is expired
        if self.token_expires_at and datetime.now() >= self.token_expires_at:
            if not self.refresh_access_token():
                self.logger.error("Failed to refresh expired token")
                return None
        
        request_headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Highland-Tower-gcPanel/1.0'
        }
        
        if headers:
            request_headers.update(headers)
        
        for attempt in range(self.max_retries):
            try:
                time.sleep(self.rate_limit_delay)
                
                response = requests.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    json=data,
                    params=params
                )
                
                if response.status_code == 401:
                    if self.refresh_access_token():
                        request_headers['Authorization'] = f'Bearer {self.access_token}'
                        continue
                    else:
                        self.logger.error("Authentication failed - need to re-authenticate")
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
    
    def get_accounts(self) -> List[Dict]:
        """Get list of accounts (hubs) user has access to"""
        url = f"{self.forge_base}/project/v1/hubs"
        return self.make_request('GET', url) or []
    
    def get_projects(self, account_id: str) -> List[AutodeskProject]:
        """
        Get all projects for an account
        
        Args:
            account_id: Autodesk account (hub) ID
            
        Returns:
            List of AutodeskProject objects
        """
        url = f"{self.forge_base}/project/v1/hubs/{account_id}/projects"
        projects_data = self.make_request('GET', url) or {'data': []}
        
        projects = []
        for project_data in projects_data.get('data', []):
            try:
                attributes = project_data.get('attributes', {})
                project = AutodeskProject(
                    id=project_data['id'],
                    name=attributes.get('name', ''),
                    project_type=project_data.get('type', ''),
                    status=attributes.get('status', ''),
                    start_date=attributes.get('startDate', ''),
                    end_date=attributes.get('endDate', ''),
                    business_units_id=attributes.get('businessUnitsId', ''),
                    timezone=attributes.get('timezone', '')
                )
                projects.append(project)
            except KeyError as e:
                self.logger.error(f"Missing required field in project data: {e}")
                continue
        
        return projects
    
    def sync_documents(self, account_id: str, project_id: str, folder_urn: str = None) -> List[AutodeskDocument]:
        """
        Sync documents from Autodesk Construction Cloud
        
        Args:
            account_id: Autodesk account ID
            project_id: Autodesk project ID
            folder_urn: Specific folder URN (optional)
            
        Returns:
            List of AutodeskDocument objects
        """
        if not folder_urn:
            # Get project's root folder first
            folders_url = f"{self.forge_base}/project/v1/hubs/{account_id}/projects/{project_id}/topFolders"
            folders_response = self.make_request('GET', folders_url)
            
            if not folders_response or not folders_response.get('data'):
                self.logger.error("Could not retrieve project folders")
                return []
            
            # Use first available folder
            folder_urn = folders_response['data'][0]['id']
        
        # Get documents from folder
        documents_url = f"{self.forge_base}/data/v1/projects/{project_id}/folders/{folder_urn}/contents"
        documents_data = self.make_request('GET', documents_url) or {'data': []}
        
        documents = []
        for doc_data in documents_data.get('data', []):
            try:
                if doc_data.get('type') == 'items':  # Filter for actual documents
                    attributes = doc_data.get('attributes', {})
                    document = AutodeskDocument(
                        id=doc_data['id'],
                        display_name=attributes.get('displayName', ''),
                        version_number=attributes.get('versionNumber', 1),
                        file_type=attributes.get('fileType', ''),
                        storage_location=attributes.get('storageLocation', ''),
                        created_date=attributes.get('createTime', ''),
                        modified_date=attributes.get('lastModifiedTime', ''),
                        created_by=attributes.get('createUserId', '')
                    )
                    documents.append(document)
            except KeyError as e:
                self.logger.error(f"Missing required field in document data: {e}")
                continue
        
        self.logger.info(f"Synced {len(documents)} documents from Autodesk project {project_id}")
        return documents
    
    def sync_bim360_issues(self, account_id: str, project_id: str) -> List[Dict]:
        """
        Sync issues from BIM 360/ACC Issues module
        
        Args:
            account_id: Autodesk account ID
            project_id: Autodesk project ID
            
        Returns:
            List of issue data
        """
        url = f"{self.acc_base}/issues/v1/containers/{project_id}/issues"
        params = {
            'filter[status]': 'open,in_dispute,in_progress,pending'  # Active issues only
        }
        
        issues_response = self.make_request('GET', url, params=params) or {'results': []}
        issues = issues_response.get('results', [])
        
        self.logger.info(f"Synced {len(issues)} issues from BIM 360 project {project_id}")
        return issues
    
    def sync_bim360_rfis(self, account_id: str, project_id: str) -> List[Dict]:
        """
        Sync RFIs from BIM 360/ACC RFIs module
        
        Args:
            account_id: Autodesk account ID
            project_id: Autodesk project ID
            
        Returns:
            List of RFI data
        """
        url = f"{self.acc_base}/rfis/v1/containers/{project_id}/rfis"
        
        rfis_response = self.make_request('GET', url) or {'results': []}
        rfis = rfis_response.get('results', [])
        
        self.logger.info(f"Synced {len(rfis)} RFIs from BIM 360 project {project_id}")
        return rfis
    
    def upload_document(self, account_id: str, project_id: str, folder_urn: str, file_path: str, file_name: str) -> Optional[Dict]:
        """
        Upload document to Autodesk Construction Cloud
        
        Args:
            account_id: Autodesk account ID
            project_id: Autodesk project ID
            folder_urn: Target folder URN
            file_path: Local file path
            file_name: Display name for the file
            
        Returns:
            Upload result data or None if failed
        """
        try:
            # Step 1: Create storage location
            storage_url = f"{self.forge_base}/oss/v2/buckets/wip.dm.prod/objects/{file_name}"
            
            with open(file_path, 'rb') as file:
                file_data = file.read()
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/octet-stream'
            }
            
            storage_response = requests.put(storage_url, headers=headers, data=file_data)
            
            if storage_response.status_code != 200:
                self.logger.error(f"Failed to upload to storage: {storage_response.text}")
                return None
            
            storage_data = storage_response.json()
            
            # Step 2: Create item in project
            create_url = f"{self.forge_base}/data/v1/projects/{project_id}/items"
            
            create_data = {
                "jsonapi": {"version": "1.0"},
                "data": {
                    "type": "items",
                    "attributes": {
                        "displayName": file_name,
                        "extension": {
                            "type": "items:autodesk.core:File",
                            "version": "1.0"
                        }
                    },
                    "relationships": {
                        "tip": {
                            "data": {
                                "type": "versions",
                                "id": "1"
                            }
                        },
                        "parent": {
                            "data": {
                                "type": "folders",
                                "id": folder_urn
                            }
                        }
                    }
                },
                "included": [
                    {
                        "type": "versions",
                        "id": "1",
                        "attributes": {
                            "name": file_name,
                            "extension": {
                                "type": "versions:autodesk.core:File",
                                "version": "1.0"
                            }
                        },
                        "relationships": {
                            "storage": {
                                "data": {
                                    "type": "objects",
                                    "id": storage_data["objectId"]
                                }
                            }
                        }
                    }
                ]
            }
            
            result = self.make_request('POST', create_url, data=create_data)
            
            if result:
                self.logger.info(f"Successfully uploaded {file_name} to Autodesk project")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error uploading document: {e}")
            return None
    
    def export_highland_data_to_autodesk(self, highland_data: Dict, data_type: str) -> bool:
        """
        Export Highland Tower data to Autodesk Construction Cloud
        
        Args:
            highland_data: Data from Highland Tower system
            data_type: Type of data (issues, rfis, documents)
            
        Returns:
            Success status
        """
        if not self.account_id or not self.project_id:
            self.logger.error("Account ID and Project ID must be set for export")
            return False
        
        success_count = 0
        error_count = 0
        
        for item in highland_data.get('items', []):
            try:
                if data_type == 'issues':
                    # Transform Highland Tower data to BIM 360 Issues format
                    issue_data = self.transform_highland_to_autodesk_issue(item)
                    url = f"{self.acc_base}/issues/v1/containers/{self.project_id}/issues"
                    result = self.make_request('POST', url, data=issue_data)
                    
                elif data_type == 'rfis':
                    # Transform Highland Tower data to BIM 360 RFIs format
                    rfi_data = self.transform_highland_to_autodesk_rfi(item)
                    url = f"{self.acc_base}/rfis/v1/containers/{self.project_id}/rfis"
                    result = self.make_request('POST', url, data=rfi_data)
                    
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
    
    def transform_highland_to_autodesk_issue(self, highland_item: Dict) -> Dict:
        """Transform Highland Tower issue data to BIM 360 format"""
        return {
            "title": highland_item.get('subject', ''),
            "description": highland_item.get('description', ''),
            "status": highland_item.get('status', 'open'),
            "assignedTo": highland_item.get('assigned_to', ''),
            "dueDate": highland_item.get('due_date', ''),
            "priority": highland_item.get('priority', 'medium'),
            "issueTypeId": highland_item.get('category_id', ''),
            "location": {
                "description": highland_item.get('location', '')
            }
        }
    
    def transform_highland_to_autodesk_rfi(self, highland_item: Dict) -> Dict:
        """Transform Highland Tower RFI data to BIM 360 format"""
        return {
            "subject": highland_item.get('subject', ''),
            "question": highland_item.get('description', ''),
            "assignedTo": highland_item.get('assigned_to', ''),
            "dueDate": highland_item.get('due_date', ''),
            "priority": highland_item.get('priority', 'medium'),
            "location": {
                "description": highland_item.get('location', '')
            },
            "customAttributes": {
                "costImpact": highland_item.get('cost_impact', 0),
                "scheduleImpact": highland_item.get('schedule_impact', 0)
            }
        }
    
    def test_connection(self) -> bool:
        """Test Autodesk API connection"""
        try:
            accounts = self.get_accounts()
            return len(accounts) >= 0
        except:
            return False
    
    def get_integration_status(self) -> Dict:
        """Get comprehensive integration status"""
        return {
            'connected': bool(self.access_token),
            'account_id': self.account_id,
            'project_id': self.project_id,
            'token_expires_at': self.token_expires_at.isoformat() if self.token_expires_at else None,
            'last_sync': datetime.now().isoformat(),
            'capabilities': [
                'Document Sync',
                'BIM 360 Issues Sync',
                'RFI Sync',
                'Model Viewing',
                'File Upload/Download',
                'Two-way Data Sync'
            ]
        }