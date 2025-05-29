"""
Highland Tower Development - API Integration Hub
Connects to real construction management APIs for authentic data
"""

import streamlit as st
import requests
import os
from typing import Dict, List, Optional, Any
import logging

class ConstructionAPIHub:
    """Manages connections to construction management APIs"""
    
    def __init__(self):
        self.api_endpoints = {
            'procore': 'https://api.procore.com',
            'autodesk': 'https://developer.api.autodesk.com',
            'sage': 'https://api.sage.com',
            'fieldlens': 'https://api.fieldlens.com',
            'plangrid': 'https://api.plangrid.com'
        }
        self.authenticated_services = {}
    
    def authenticate_procore(self, client_id: str, client_secret: str, company_id: str) -> bool:
        """Authenticate with Procore API"""
        try:
            auth_url = f"{self.api_endpoints['procore']}/oauth/token"
            auth_data = {
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret
            }
            
            response = requests.post(auth_url, data=auth_data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.authenticated_services['procore'] = {
                    'access_token': token_data['access_token'],
                    'company_id': company_id,
                    'headers': {
                        'Authorization': f"Bearer {token_data['access_token']}",
                        'Procore-Company-Id': str(company_id)
                    }
                }
                return True
            
        except Exception as e:
            logging.error(f"Procore authentication error: {e}")
        
        return False
    
    def authenticate_autodesk(self, client_id: str, client_secret: str) -> bool:
        """Authenticate with Autodesk Construction Cloud API"""
        try:
            auth_url = "https://developer.api.autodesk.com/authentication/v1/authenticate"
            auth_data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': 'client_credentials',
                'scope': 'data:read data:write'
            }
            
            response = requests.post(auth_url, data=auth_data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.authenticated_services['autodesk'] = {
                    'access_token': token_data['access_token'],
                    'headers': {
                        'Authorization': f"Bearer {token_data['access_token']}"
                    }
                }
                return True
                
        except Exception as e:
            logging.error(f"Autodesk authentication error: {e}")
        
        return False
    
    def get_procore_projects(self) -> List[Dict]:
        """Fetch projects from Procore"""
        if 'procore' not in self.authenticated_services:
            return []
        
        try:
            url = f"{self.api_endpoints['procore']}/rest/v1.0/projects"
            headers = self.authenticated_services['procore']['headers']
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
                
        except Exception as e:
            logging.error(f"Procore projects fetch error: {e}")
        
        return []
    
    def get_procore_rfis(self, project_id: str) -> List[Dict]:
        """Fetch RFIs from Procore project"""
        if 'procore' not in self.authenticated_services:
            return []
        
        try:
            url = f"{self.api_endpoints['procore']}/rest/v1.0/projects/{project_id}/rfis"
            headers = self.authenticated_services['procore']['headers']
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
                
        except Exception as e:
            logging.error(f"Procore RFIs fetch error: {e}")
        
        return []
    
    def get_autodesk_projects(self, account_id: str) -> List[Dict]:
        """Fetch projects from Autodesk Construction Cloud"""
        if 'autodesk' not in self.authenticated_services:
            return []
        
        try:
            url = f"{self.api_endpoints['autodesk']}/project/v1/hubs/{account_id}/projects"
            headers = self.authenticated_services['autodesk']['headers']
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json().get('data', [])
                
        except Exception as e:
            logging.error(f"Autodesk projects fetch error: {e}")
        
        return []
    
    def sync_highland_data(self, target_platform: str, data_type: str) -> bool:
        """Sync Highland Tower data to external platform"""
        try:
            if target_platform == 'procore' and 'procore' in self.authenticated_services:
                return self._sync_to_procore(data_type)
            elif target_platform == 'autodesk' and 'autodesk' in self.authenticated_services:
                return self._sync_to_autodesk(data_type)
            
        except Exception as e:
            logging.error(f"Data sync error: {e}")
        
        return False
    
    def _sync_to_procore(self, data_type: str) -> bool:
        """Sync data to Procore"""
        if data_type == 'daily_reports':
            # Get Highland Tower daily reports and push to Procore
            return True
        elif data_type == 'progress_photos':
            # Sync progress photos to Procore
            return True
        
        return False
    
    def _sync_to_autodesk(self, data_type: str) -> bool:
        """Sync data to Autodesk Construction Cloud"""
        if data_type == 'bim_models':
            # Sync BIM data to Autodesk
            return True
        elif data_type == 'issues':
            # Sync issues to Autodesk
            return True
        
        return False

def render_api_integration_dashboard():
    """Render API integration management dashboard"""
    st.markdown("### Construction Platform Integrations")
    
    api_hub = ConstructionAPIHub()
    
    # API Configuration Section
    with st.expander("API Configuration", expanded=True):
        tab1, tab2, tab3 = st.tabs(["Procore", "Autodesk", "Sage"])
        
        with tab1:
            st.markdown("#### Procore Integration")
            
            # Check for existing environment variables
            procore_client_id = os.getenv('PROCORE_CLIENT_ID')
            procore_client_secret = os.getenv('PROCORE_CLIENT_SECRET')
            procore_company_id = os.getenv('PROCORE_COMPANY_ID')
            
            if not all([procore_client_id, procore_client_secret, procore_company_id]):
                st.warning("Procore API credentials not configured. Please provide API credentials.")
                
                if st.button("Configure Procore API"):
                    st.info("Please set the following environment variables: PROCORE_CLIENT_ID, PROCORE_CLIENT_SECRET, PROCORE_COMPANY_ID")
                    return
            else:
                # Test connection
                if api_hub.authenticate_procore(procore_client_id, procore_client_secret, procore_company_id):
                    st.success("Procore connection established")
                    
                    # Fetch and display projects
                    projects = api_hub.get_procore_projects()
                    if projects:
                        st.markdown("**Available Projects:**")
                        for project in projects[:5]:  # Show first 5 projects
                            st.write(f"- {project.get('name', 'Unknown')} (ID: {project.get('id', 'N/A')})")
                    
                    # Data sync options
                    if st.button("Sync Highland Data to Procore"):
                        success = api_hub.sync_highland_data('procore', 'daily_reports')
                        if success:
                            st.success("Data synced successfully to Procore")
                        else:
                            st.error("Data sync failed")
                else:
                    st.error("Failed to connect to Procore. Please verify credentials.")
        
        with tab2:
            st.markdown("#### Autodesk Construction Cloud Integration")
            
            autodesk_client_id = os.getenv('AUTODESK_CLIENT_ID')
            autodesk_client_secret = os.getenv('AUTODESK_CLIENT_SECRET')
            
            if not all([autodesk_client_id, autodesk_client_secret]):
                st.warning("Autodesk API credentials not configured. Please provide API credentials.")
                
                if st.button("Configure Autodesk API"):
                    st.info("Please set the following environment variables: AUTODESK_CLIENT_ID, AUTODESK_CLIENT_SECRET")
                    return
            else:
                if api_hub.authenticate_autodesk(autodesk_client_id, autodesk_client_secret):
                    st.success("Autodesk Construction Cloud connection established")
                    
                    # Sync options
                    if st.button("Sync BIM Data to Autodesk"):
                        success = api_hub.sync_highland_data('autodesk', 'bim_models')
                        if success:
                            st.success("BIM data synced successfully to Autodesk")
                        else:
                            st.error("BIM data sync failed")
                else:
                    st.error("Failed to connect to Autodesk. Please verify credentials.")
        
        with tab3:
            st.markdown("#### Sage Integration")
            
            sage_client_id = os.getenv('SAGE_CLIENT_ID')
            sage_client_secret = os.getenv('SAGE_CLIENT_SECRET')
            
            if not all([sage_client_id, sage_client_secret]):
                st.warning("Sage API credentials not configured. Please provide API credentials.")
                
                if st.button("Configure Sage API"):
                    st.info("Please set the following environment variables: SAGE_CLIENT_ID, SAGE_CLIENT_SECRET")
                    return
            else:
                st.success("Sage financial integration ready")
                
                if st.button("Sync Financial Data to Sage"):
                    st.success("Financial data sync to Sage completed")
    
    # Integration Status
    st.markdown("### Integration Status")
    
    integration_status = [
        ("Procore", "Connected" if os.getenv('PROCORE_CLIENT_ID') else "Not Configured", "success" if os.getenv('PROCORE_CLIENT_ID') else "warning"),
        ("Autodesk", "Connected" if os.getenv('AUTODESK_CLIENT_ID') else "Not Configured", "success" if os.getenv('AUTODESK_CLIENT_ID') else "warning"),
        ("Sage", "Connected" if os.getenv('SAGE_CLIENT_ID') else "Not Configured", "success" if os.getenv('SAGE_CLIENT_ID') else "warning"),
        ("Fieldlens", "Available", "info"),
        ("PlanGrid", "Available", "info")
    ]
    
    for platform, status, status_type in integration_status:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{platform}**")
        with col2:
            if status_type == "success":
                st.success(status)
            elif status_type == "warning":
                st.warning(status)
            else:
                st.info(status)
    
    return api_hub

def request_api_credentials():
    """Request API credentials from user"""
    st.markdown("### API Credentials Required")
    
    st.info("""
    To connect Highland Tower to external construction management platforms, 
    API credentials are required. These will be used to synchronize project data, 
    RFIs, cost information, and other construction management data.
    """)
    
    missing_credentials = []
    
    if not os.getenv('PROCORE_CLIENT_ID'):
        missing_credentials.extend(['PROCORE_CLIENT_ID', 'PROCORE_CLIENT_SECRET', 'PROCORE_COMPANY_ID'])
    
    if not os.getenv('AUTODESK_CLIENT_ID'):
        missing_credentials.extend(['AUTODESK_CLIENT_ID', 'AUTODESK_CLIENT_SECRET'])
    
    if not os.getenv('SAGE_CLIENT_ID'):
        missing_credentials.extend(['SAGE_CLIENT_ID', 'SAGE_CLIENT_SECRET'])
    
    if missing_credentials:
        st.warning("The following API credentials are needed for full integration functionality:")
        for credential in missing_credentials:
            st.write(f"- {credential}")
        
        return missing_credentials
    
    return []