"""
Integration Manager for gcPanel Highland Tower Development

Handles connections to external construction management APIs, BIM software,
accounting systems, and communication platforms for seamless data flow.
"""

import requests
import logging
from typing import Dict, List, Any, Optional
import streamlit as st
from datetime import datetime
import json
import os
from abc import ABC, abstractmethod

class BaseIntegration(ABC):
    """Base class for all external integrations"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f'Integration_{name}')
        self.is_connected = False
    
    @abstractmethod
    def authenticate(self, credentials: Dict) -> bool:
        """Authenticate with the external service"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """Test the connection to external service"""
        pass
    
    @abstractmethod
    def sync_data(self, data_type: str) -> Dict:
        """Sync data with external service"""
        pass

class ProcoreIntegration(BaseIntegration):
    """Integration with Procore construction management platform"""
    
    def __init__(self):
        super().__init__("Procore")
        self.api_base = "https://api.procore.com/rest/v1.0"
        self.client_id = os.environ.get('PROCORE_CLIENT_ID')
        self.client_secret = os.environ.get('PROCORE_CLIENT_SECRET')
        self.access_token = None
    
    def authenticate(self, credentials: Dict = None) -> bool:
        """Authenticate with Procore API"""
        if not self.client_id or not self.client_secret:
            self.logger.warning("Procore credentials not found in environment")
            return False
        
        try:
            auth_url = "https://api.procore.com/oauth/token"
            auth_data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            
            response = requests.post(auth_url, data=auth_data)
            if response.status_code == 200:
                self.access_token = response.json().get('access_token')
                self.is_connected = True
                self.logger.info("Successfully authenticated with Procore")
                return True
            else:
                self.logger.error(f"Procore authentication failed: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Procore authentication error: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test Procore API connection"""
        if not self.access_token:
            return self.authenticate()
        
        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            response = requests.get(f"{self.api_base}/companies", headers=headers)
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Procore connection test failed: {e}")
            return False
    
    def sync_data(self, data_type: str) -> Dict:
        """Sync data from Procore"""
        if not self.test_connection():
            return {"error": "Not connected to Procore"}
        
        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            
            if data_type == 'rfis':
                response = requests.get(f"{self.api_base}/rfis", headers=headers)
            elif data_type == 'daily_reports':
                response = requests.get(f"{self.api_base}/daily_logs", headers=headers)
            elif data_type == 'submittals':
                response = requests.get(f"{self.api_base}/submittals", headers=headers)
            else:
                return {"error": f"Unsupported data type: {data_type}"}
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            self.logger.error(f"Procore sync error: {e}")
            return {"error": str(e)}

class AutodeskIntegration(BaseIntegration):
    """Integration with Autodesk Construction Cloud"""
    
    def __init__(self):
        super().__init__("Autodesk")
        self.api_base = "https://developer.api.autodesk.com"
        self.client_id = os.environ.get('AUTODESK_CLIENT_ID')
        self.client_secret = os.environ.get('AUTODESK_CLIENT_SECRET')
        self.access_token = None
    
    def authenticate(self, credentials: Dict = None) -> bool:
        """Authenticate with Autodesk Forge API"""
        if not self.client_id or not self.client_secret:
            self.logger.warning("Autodesk credentials not found in environment")
            return False
        
        try:
            auth_url = f"{self.api_base}/authentication/v1/authenticate"
            auth_data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials',
                'scope': 'data:read data:write'
            }
            
            response = requests.post(auth_url, data=auth_data)
            if response.status_code == 200:
                self.access_token = response.json().get('access_token')
                self.is_connected = True
                self.logger.info("Successfully authenticated with Autodesk")
                return True
            else:
                self.logger.error(f"Autodesk authentication failed: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Autodesk authentication error: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test Autodesk API connection"""
        if not self.access_token:
            return self.authenticate()
        
        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            response = requests.get(f"{self.api_base}/project/v1/hubs", headers=headers)
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Autodesk connection test failed: {e}")
            return False
    
    def sync_data(self, data_type: str) -> Dict:
        """Sync BIM data from Autodesk"""
        if not self.test_connection():
            return {"error": "Not connected to Autodesk"}
        
        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            
            if data_type == 'models':
                response = requests.get(f"{self.api_base}/project/v1/projects", headers=headers)
            elif data_type == 'issues':
                response = requests.get(f"{self.api_base}/issues/v1/containers", headers=headers)
            else:
                return {"error": f"Unsupported data type: {data_type}"}
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            self.logger.error(f"Autodesk sync error: {e}")
            return {"error": str(e)}

class QuickBooksIntegration(BaseIntegration):
    """Integration with QuickBooks accounting system"""
    
    def __init__(self):
        super().__init__("QuickBooks")
        self.api_base = "https://sandbox-quickbooks.api.intuit.com"
        self.client_id = os.environ.get('QUICKBOOKS_CLIENT_ID')
        self.client_secret = os.environ.get('QUICKBOOKS_CLIENT_SECRET')
        self.access_token = None
        self.company_id = None
    
    def authenticate(self, credentials: Dict = None) -> bool:
        """Authenticate with QuickBooks API"""
        if not self.client_id or not self.client_secret:
            self.logger.warning("QuickBooks credentials not found in environment")
            return False
        
        # QuickBooks uses OAuth 2.0 flow - would need user authorization
        # For now, check if tokens are available
        self.access_token = os.environ.get('QUICKBOOKS_ACCESS_TOKEN')
        self.company_id = os.environ.get('QUICKBOOKS_COMPANY_ID')
        
        if self.access_token and self.company_id:
            self.is_connected = True
            return True
        
        return False
    
    def test_connection(self) -> bool:
        """Test QuickBooks API connection"""
        if not self.access_token or not self.company_id:
            return self.authenticate()
        
        try:
            headers = {'Authorization': f'Bearer {self.access_token}',
                      'Accept': 'application/json'}
            url = f"{self.api_base}/v3/company/{self.company_id}/companyinfo/{self.company_id}"
            response = requests.get(url, headers=headers)
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"QuickBooks connection test failed: {e}")
            return False
    
    def sync_data(self, data_type: str) -> Dict:
        """Sync financial data from QuickBooks"""
        if not self.test_connection():
            return {"error": "Not connected to QuickBooks"}
        
        try:
            headers = {'Authorization': f'Bearer {self.access_token}',
                      'Accept': 'application/json'}
            
            if data_type == 'vendors':
                url = f"{self.api_base}/v3/company/{self.company_id}/vendors"
            elif data_type == 'invoices':
                url = f"{self.api_base}/v3/company/{self.company_id}/invoices"
            elif data_type == 'expenses':
                url = f"{self.api_base}/v3/company/{self.company_id}/purchases"
            else:
                return {"error": f"Unsupported data type: {data_type}"}
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            self.logger.error(f"QuickBooks sync error: {e}")
            return {"error": str(e)}

class SlackIntegration(BaseIntegration):
    """Integration with Slack for team notifications"""
    
    def __init__(self):
        super().__init__("Slack")
        self.webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
        self.bot_token = os.environ.get('SLACK_BOT_TOKEN')
    
    def authenticate(self, credentials: Dict = None) -> bool:
        """Authenticate with Slack"""
        if self.webhook_url or self.bot_token:
            self.is_connected = True
            return True
        
        self.logger.warning("Slack credentials not found in environment")
        return False
    
    def test_connection(self) -> bool:
        """Test Slack connection"""
        if not self.authenticate():
            return False
        
        try:
            if self.webhook_url:
                test_message = {"text": "gcPanel Highland Tower Development - Connection Test"}
                response = requests.post(self.webhook_url, json=test_message)
                return response.status_code == 200
            return True
        except Exception as e:
            self.logger.error(f"Slack connection test failed: {e}")
            return False
    
    def sync_data(self, data_type: str) -> Dict:
        """Send notifications to Slack"""
        if not self.test_connection():
            return {"error": "Not connected to Slack"}
        
        # This is for sending data TO Slack, not syncing FROM it
        return {"success": True, "message": "Slack is for outbound notifications"}
    
    def send_notification(self, message: str, channel: str = None) -> bool:
        """Send notification to Slack channel"""
        if not self.webhook_url:
            return False
        
        try:
            payload = {
                "text": f"🏗️ Highland Tower Development: {message}",
                "username": "gcPanel Bot"
            }
            
            if channel:
                payload["channel"] = channel
            
            response = requests.post(self.webhook_url, json=payload)
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"Slack notification error: {e}")
            return False

class IntegrationManager:
    """Manages all external integrations for Highland Tower Development"""
    
    def __init__(self):
        self.integrations = {
            'procore': ProcoreIntegration(),
            'autodesk': AutodeskIntegration(),
            'quickbooks': QuickBooksIntegration(),
            'slack': SlackIntegration()
        }
        self.setup_logging()
    
    def setup_logging(self):
        """Setup integration logging"""
        self.logger = logging.getLogger('IntegrationManager')
    
    def check_all_connections(self) -> Dict[str, bool]:
        """Check connection status for all integrations"""
        status = {}
        for name, integration in self.integrations.items():
            try:
                status[name] = integration.test_connection()
            except Exception as e:
                self.logger.error(f"Error checking {name}: {e}")
                status[name] = False
        
        return status
    
    def sync_all_data(self) -> Dict[str, Any]:
        """Sync data from all connected integrations"""
        results = {}
        
        for name, integration in self.integrations.items():
            if integration.is_connected:
                try:
                    if name == 'procore':
                        results[name] = {
                            'rfis': integration.sync_data('rfis'),
                            'daily_reports': integration.sync_data('daily_reports')
                        }
                    elif name == 'autodesk':
                        results[name] = {
                            'models': integration.sync_data('models'),
                            'issues': integration.sync_data('issues')
                        }
                    elif name == 'quickbooks':
                        results[name] = {
                            'vendors': integration.sync_data('vendors'),
                            'expenses': integration.sync_data('expenses')
                        }
                except Exception as e:
                    results[name] = {"error": str(e)}
            else:
                results[name] = {"status": "not_connected"}
        
        return results
    
    def render_integration_status(self):
        """Render integration status dashboard"""
        st.markdown("### 🔗 External Integrations - Highland Tower Development")
        
        status = self.check_all_connections()
        
        for name, connected in status.items():
            integration = self.integrations[name]
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                status_icon = "🟢" if connected else "🔴"
                st.markdown(f"{status_icon} **{name.title()}** - {integration.name}")
            
            with col2:
                status_text = "Connected" if connected else "Disconnected"
                st.markdown(f"Status: {status_text}")
            
            with col3:
                if st.button(f"Test {name}", key=f"test_{name}"):
                    if integration.test_connection():
                        st.success(f"{name.title()} connection successful!")
                    else:
                        st.error(f"{name.title()} connection failed!")
        
        # Sync all data button
        if st.button("🔄 Sync All Data", type="primary"):
            with st.spinner("Syncing data from all integrations..."):
                results = self.sync_all_data()
                
                for integration, result in results.items():
                    if isinstance(result, dict) and result.get('error'):
                        st.error(f"{integration.title()}: {result['error']}")
                    elif isinstance(result, dict) and result.get('status') == 'not_connected':
                        st.warning(f"{integration.title()}: Not connected")
                    else:
                        st.success(f"{integration.title()}: Data synced successfully")
    
    def send_team_notification(self, message: str) -> bool:
        """Send notification to team via Slack"""
        slack = self.integrations.get('slack')
        if slack and slack.is_connected:
            return slack.send_notification(message)
        return False

@st.cache_resource
def get_integration_manager():
    """Get cached integration manager instance"""
    return IntegrationManager()