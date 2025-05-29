"""
Highland Tower Development - Integration Settings Manager
User-friendly interface for managing all construction platform API credentials
"""

import streamlit as st
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

class IntegrationSettingsManager:
    """Manages API credentials and integration configurations through the UI"""
    
    def __init__(self):
        self.credentials_file = "integration_credentials.json"
        self.load_saved_credentials()
    
    def load_saved_credentials(self):
        """Load saved credentials from secure storage"""
        if os.path.exists(self.credentials_file):
            try:
                with open(self.credentials_file, 'r') as f:
                    self.credentials = json.load(f)
            except:
                self.credentials = {}
        else:
            self.credentials = {}
    
    def save_credentials(self):
        """Save credentials to secure storage"""
        try:
            with open(self.credentials_file, 'w') as f:
                json.dump(self.credentials, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Error saving credentials: {e}")
            return False
    
    def render_procore_settings(self):
        """Render Procore integration settings"""
        st.subheader("🏗️ Procore Integration")
        
        with st.expander("Configure Procore API Access", expanded=False):
            st.markdown("""
            **To get Procore API credentials:**
            1. Log into your Procore account
            2. Go to Company Settings → App Management
            3. Create a new App or select existing
            4. Copy Client ID and Client Secret
            5. Note your Company ID from account settings
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                client_id = st.text_input(
                    "Procore Client ID",
                    value=self.credentials.get('procore', {}).get('client_id', ''),
                    type="password"
                )
                company_id = st.text_input(
                    "Procore Company ID",
                    value=self.credentials.get('procore', {}).get('company_id', '')
                )
            
            with col2:
                client_secret = st.text_input(
                    "Procore Client Secret",
                    value=self.credentials.get('procore', {}).get('client_secret', ''),
                    type="password"
                )
                redirect_uri = st.text_input(
                    "Redirect URI (optional)",
                    value=self.credentials.get('procore', {}).get('redirect_uri', 'urn:ietf:wg:oauth:2.0:oob')
                )
            
            if st.button("Save Procore Settings", key="save_procore"):
                if client_id and client_secret and company_id:
                    self.credentials['procore'] = {
                        'client_id': client_id,
                        'client_secret': client_secret,
                        'company_id': company_id,
                        'redirect_uri': redirect_uri,
                        'updated_at': datetime.now().isoformat()
                    }
                    if self.save_credentials():
                        st.success("✅ Procore credentials saved successfully!")
                else:
                    st.error("Please fill in all required fields")
    
    def render_autodesk_settings(self):
        """Render Autodesk Construction Cloud settings"""
        st.subheader("🏢 Autodesk Construction Cloud")
        
        with st.expander("Configure Autodesk Forge API Access", expanded=False):
            st.markdown("""
            **To get Autodesk API credentials:**
            1. Visit Forge Developer Portal (developer.autodesk.com)
            2. Create a new App or select existing
            3. Copy Client ID and Client Secret
            4. Set callback URL for your domain
            5. Enable required scopes (data:read, data:write, account:read)
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                client_id = st.text_input(
                    "Autodesk Client ID",
                    value=self.credentials.get('autodesk', {}).get('client_id', ''),
                    type="password"
                )
            
            with col2:
                client_secret = st.text_input(
                    "Autodesk Client Secret",
                    value=self.credentials.get('autodesk', {}).get('client_secret', ''),
                    type="password"
                )
            
            callback_url = st.text_input(
                "Callback URL",
                value=self.credentials.get('autodesk', {}).get('callback_url', 'http://localhost:3000/callback')
            )
            
            if st.button("Save Autodesk Settings", key="save_autodesk"):
                if client_id and client_secret:
                    self.credentials['autodesk'] = {
                        'client_id': client_id,
                        'client_secret': client_secret,
                        'callback_url': callback_url,
                        'updated_at': datetime.now().isoformat()
                    }
                    if self.save_credentials():
                        st.success("✅ Autodesk credentials saved successfully!")
                else:
                    st.error("Please fill in Client ID and Client Secret")
    
    def render_sage_settings(self):
        """Render Sage Construction settings"""
        st.subheader("📊 Sage Construction")
        
        with st.expander("Configure Sage API Access", expanded=False):
            st.markdown("""
            **To get Sage API credentials:**
            1. Contact your Sage administrator
            2. Request API access for your user account
            3. Get Client ID and Secret from Sage developer portal
            4. Note your company database identifier
            5. Ensure your user has appropriate permissions
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                client_id = st.text_input(
                    "Sage Client ID",
                    value=self.credentials.get('sage', {}).get('client_id', ''),
                    type="password"
                )
                username = st.text_input(
                    "Sage Username",
                    value=self.credentials.get('sage', {}).get('username', '')
                )
                company_db = st.text_input(
                    "Company Database",
                    value=self.credentials.get('sage', {}).get('company_db', '')
                )
            
            with col2:
                client_secret = st.text_input(
                    "Sage Client Secret",
                    value=self.credentials.get('sage', {}).get('client_secret', ''),
                    type="password"
                )
                password = st.text_input(
                    "Sage Password",
                    value=self.credentials.get('sage', {}).get('password', ''),
                    type="password"
                )
                api_base = st.text_input(
                    "API Base URL",
                    value=self.credentials.get('sage', {}).get('api_base', 'https://api.sage.com')
                )
            
            if st.button("Save Sage Settings", key="save_sage"):
                if all([client_id, client_secret, username, password, company_db]):
                    self.credentials['sage'] = {
                        'client_id': client_id,
                        'client_secret': client_secret,
                        'username': username,
                        'password': password,
                        'company_db': company_db,
                        'api_base': api_base,
                        'updated_at': datetime.now().isoformat()
                    }
                    if self.save_credentials():
                        st.success("✅ Sage credentials saved successfully!")
                else:
                    st.error("Please fill in all required fields")
    
    def render_fieldlens_settings(self):
        """Render Fieldlens settings"""
        st.subheader("📱 Fieldlens")
        
        with st.expander("Configure Fieldlens API Access", expanded=False):
            st.markdown("""
            **To get Fieldlens API credentials:**
            1. Log into your Fieldlens account
            2. Go to Account Settings → API Access
            3. Generate or copy your API Key
            4. Note your Company ID from account info
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                api_key = st.text_input(
                    "Fieldlens API Key",
                    value=self.credentials.get('fieldlens', {}).get('api_key', ''),
                    type="password"
                )
            
            with col2:
                company_id = st.text_input(
                    "Fieldlens Company ID",
                    value=self.credentials.get('fieldlens', {}).get('company_id', '')
                )
            
            if st.button("Save Fieldlens Settings", key="save_fieldlens"):
                if api_key and company_id:
                    self.credentials['fieldlens'] = {
                        'api_key': api_key,
                        'company_id': company_id,
                        'updated_at': datetime.now().isoformat()
                    }
                    if self.save_credentials():
                        st.success("✅ Fieldlens credentials saved successfully!")
                else:
                    st.error("Please fill in API Key and Company ID")
    
    def render_plangrid_settings(self):
        """Render PlanGrid settings"""
        st.subheader("📐 PlanGrid")
        
        with st.expander("Configure PlanGrid API Access", expanded=False):
            st.markdown("""
            **To get PlanGrid API credentials:**
            1. Log into your PlanGrid account
            2. Go to Account Settings → Developer Settings
            3. Generate or copy your API Key
            4. Alternative: Use OAuth Access Token
            """)
            
            auth_method = st.radio(
                "Authentication Method",
                ["API Key", "Access Token"],
                key="plangrid_auth_method"
            )
            
            if auth_method == "API Key":
                api_key = st.text_input(
                    "PlanGrid API Key",
                    value=self.credentials.get('plangrid', {}).get('api_key', ''),
                    type="password"
                )
                access_token = ""
            else:
                api_key = ""
                access_token = st.text_input(
                    "PlanGrid Access Token",
                    value=self.credentials.get('plangrid', {}).get('access_token', ''),
                    type="password"
                )
            
            if st.button("Save PlanGrid Settings", key="save_plangrid"):
                if api_key or access_token:
                    self.credentials['plangrid'] = {
                        'api_key': api_key,
                        'access_token': access_token,
                        'auth_method': auth_method.lower().replace(' ', '_'),
                        'updated_at': datetime.now().isoformat()
                    }
                    if self.save_credentials():
                        st.success("✅ PlanGrid credentials saved successfully!")
                else:
                    st.error("Please provide either API Key or Access Token")
    
    def render_integration_status(self):
        """Render integration connection status"""
        st.subheader("🔗 Integration Status")
        
        platforms = ['procore', 'autodesk', 'sage', 'fieldlens', 'plangrid']
        
        for platform in platforms:
            platform_data = self.credentials.get(platform, {})
            
            if platform_data:
                last_updated = platform_data.get('updated_at', 'Never')
                if last_updated != 'Never':
                    last_updated = datetime.fromisoformat(last_updated).strftime('%Y-%m-%d %H:%M')
                
                status_color = "🟢"
                status_text = "Configured"
            else:
                last_updated = "Not configured"
                status_color = "🔴"
                status_text = "Not configured"
            
            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                st.write(f"{status_color} **{platform.title()}**")
            with col2:
                st.write(status_text)
            with col3:
                st.write(f"Updated: {last_updated}")
    
    def test_all_connections(self):
        """Test connections to all configured platforms"""
        st.subheader("🧪 Test Connections")
        
        if st.button("Test All Configured Integrations", key="test_all"):
            with st.spinner("Testing connections..."):
                results = {}
                
                # Import integration classes
                try:
                    from integrations.unified_integration_manager import UnifiedIntegrationManager
                    
                    # Update environment variables with saved credentials
                    self.update_environment_variables()
                    
                    # Initialize and test
                    manager = UnifiedIntegrationManager()
                    results = manager.check_all_connections()
                    
                    # Display results
                    for platform, connected in results.items():
                        if connected:
                            st.success(f"✅ {platform.title()}: Connected successfully")
                        else:
                            st.error(f"❌ {platform.title()}: Connection failed")
                
                except ImportError as e:
                    st.error(f"Integration modules not found: {e}")
                except Exception as e:
                    st.error(f"Error testing connections: {e}")
    
    def update_environment_variables(self):
        """Update environment variables with saved credentials"""
        for platform, creds in self.credentials.items():
            if platform == 'procore':
                os.environ['PROCORE_CLIENT_ID'] = creds.get('client_id', '')
                os.environ['PROCORE_CLIENT_SECRET'] = creds.get('client_secret', '')
                os.environ['PROCORE_COMPANY_ID'] = creds.get('company_id', '')
                os.environ['PROCORE_REDIRECT_URI'] = creds.get('redirect_uri', '')
            
            elif platform == 'autodesk':
                os.environ['AUTODESK_CLIENT_ID'] = creds.get('client_id', '')
                os.environ['AUTODESK_CLIENT_SECRET'] = creds.get('client_secret', '')
                os.environ['AUTODESK_CALLBACK_URL'] = creds.get('callback_url', '')
            
            elif platform == 'sage':
                os.environ['SAGE_CLIENT_ID'] = creds.get('client_id', '')
                os.environ['SAGE_CLIENT_SECRET'] = creds.get('client_secret', '')
                os.environ['SAGE_USERNAME'] = creds.get('username', '')
                os.environ['SAGE_PASSWORD'] = creds.get('password', '')
                os.environ['SAGE_COMPANY_DB'] = creds.get('company_db', '')
                os.environ['SAGE_API_BASE'] = creds.get('api_base', '')
            
            elif platform == 'fieldlens':
                os.environ['FIELDLENS_API_KEY'] = creds.get('api_key', '')
                os.environ['FIELDLENS_COMPANY_ID'] = creds.get('company_id', '')
            
            elif platform == 'plangrid':
                os.environ['PLANGRID_API_KEY'] = creds.get('api_key', '')
                os.environ['PLANGRID_ACCESS_TOKEN'] = creds.get('access_token', '')
    
    def get_saved_credentials(self, platform: str) -> Dict:
        """Get saved credentials for a specific platform"""
        return self.credentials.get(platform, {})
    
    def is_platform_configured(self, platform: str) -> bool:
        """Check if a platform is properly configured"""
        creds = self.credentials.get(platform, {})
        
        required_fields = {
            'procore': ['client_id', 'client_secret', 'company_id'],
            'autodesk': ['client_id', 'client_secret'],
            'sage': ['client_id', 'client_secret', 'username', 'password', 'company_db'],
            'fieldlens': ['api_key', 'company_id'],
            'plangrid': ['api_key']  # OR access_token
        }
        
        required = required_fields.get(platform, [])
        
        if platform == 'plangrid':
            return bool(creds.get('api_key') or creds.get('access_token'))
        
        return all(creds.get(field) for field in required)

def render_integration_settings():
    """Main function to render integration settings interface"""
    manager = IntegrationSettingsManager()
    
    st.markdown("""
    <div class="module-header">
        <h1>🔗 Integration Settings</h1>
        <p>Configure API credentials for construction platform integrations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Integration status overview
    manager.render_integration_status()
    
    st.markdown("---")
    
    # Platform configuration sections
    manager.render_procore_settings()
    manager.render_autodesk_settings() 
    manager.render_sage_settings()
    manager.render_fieldlens_settings()
    manager.render_plangrid_settings()
    
    st.markdown("---")
    
    # Connection testing
    manager.test_all_connections()
    
    # Clear all credentials option
    if st.button("🗑️ Clear All Credentials", key="clear_all"):
        if st.confirm("Are you sure you want to clear all saved credentials?"):
            manager.credentials = {}
            manager.save_credentials()
            st.success("All credentials cleared successfully!")
            st.rerun()