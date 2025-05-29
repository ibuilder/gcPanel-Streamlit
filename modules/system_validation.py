"""
Highland Tower Development - System Validation and Testing
Comprehensive testing framework for production readiness
"""

import streamlit as st
import pandas as pd
import requests
import psycopg2
import os
from datetime import datetime
from typing import Dict, List, Tuple, Any
import logging

class SystemValidator:
    """Validates Highland Tower system components for production readiness"""
    
    def __init__(self):
        self.test_results = []
        self.database_connection = None
    
    def validate_database_connection(self) -> Tuple[bool, str]:
        """Validate PostgreSQL database connection"""
        try:
            database_url = os.getenv('DATABASE_URL')
            if not database_url:
                return False, "DATABASE_URL environment variable not set"
            
            self.database_connection = psycopg2.connect(database_url)
            cursor = self.database_connection.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            cursor.close()
            
            return True, f"Connected to PostgreSQL: {version[0][:50]}..."
            
        except Exception as e:
            return False, f"Database connection failed: {str(e)}"
    
    def validate_core_tables(self) -> Tuple[bool, str]:
        """Validate existence of core Highland Tower tables"""
        if not self.database_connection:
            return False, "No database connection available"
        
        required_tables = [
            'highland_progress',
            'highland_costs', 
            'highland_rfis',
            'highland_daily_reports'
        ]
        
        try:
            cursor = self.database_connection.cursor()
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name LIKE 'highland_%'
            """)
            existing_tables = [row[0] for row in cursor.fetchall()]
            cursor.close()
            
            missing_tables = [table for table in required_tables if table not in existing_tables]
            
            if missing_tables:
                return False, f"Missing tables: {', '.join(missing_tables)}"
            
            return True, f"All core tables present: {len(existing_tables)} tables found"
            
        except Exception as e:
            return False, f"Table validation failed: {str(e)}"
    
    def validate_data_integrity(self) -> Tuple[bool, str]:
        """Validate data integrity in Highland Tower tables"""
        if not self.database_connection:
            return False, "No database connection available"
        
        try:
            cursor = self.database_connection.cursor()
            
            # Check progress data consistency
            cursor.execute("""
                SELECT COUNT(*) FROM highland_progress 
                WHERE planned_progress BETWEEN 0 AND 100 
                AND actual_progress BETWEEN 0 AND 100
            """)
            valid_progress_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM highland_progress")
            total_progress_count = cursor.fetchone()[0]
            
            # Check cost data consistency
            cursor.execute("""
                SELECT COUNT(*) FROM highland_costs 
                WHERE budgeted_amount > 0 AND spent_amount >= 0
            """)
            valid_cost_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM highland_costs")
            total_cost_count = cursor.fetchone()[0]
            
            cursor.close()
            
            if valid_progress_count != total_progress_count:
                return False, f"Progress data integrity issues: {total_progress_count - valid_progress_count} invalid records"
            
            if valid_cost_count != total_cost_count:
                return False, f"Cost data integrity issues: {total_cost_count - valid_cost_count} invalid records"
            
            return True, f"Data integrity verified: {total_progress_count} progress records, {total_cost_count} cost records"
            
        except Exception as e:
            return False, f"Data integrity validation failed: {str(e)}"
    
    def validate_api_integrations(self) -> Dict[str, Tuple[bool, str]]:
        """Validate external API integrations"""
        integration_results = {}
        
        # Procore validation
        procore_credentials = {
            'client_id': os.getenv('PROCORE_CLIENT_ID'),
            'client_secret': os.getenv('PROCORE_CLIENT_SECRET'),
            'company_id': os.getenv('PROCORE_COMPANY_ID')
        }
        
        if all(procore_credentials.values()):
            try:
                # Test Procore API connectivity
                auth_url = "https://api.procore.com/oauth/token"
                response = requests.post(auth_url, data={
                    'grant_type': 'client_credentials',
                    'client_id': procore_credentials['client_id'],
                    'client_secret': procore_credentials['client_secret']
                }, timeout=10)
                
                if response.status_code == 200:
                    integration_results['procore'] = (True, "Procore API connection successful")
                else:
                    integration_results['procore'] = (False, f"Procore API error: {response.status_code}")
                    
            except Exception as e:
                integration_results['procore'] = (False, f"Procore connection failed: {str(e)}")
        else:
            integration_results['procore'] = (False, "Procore credentials not configured")
        
        # Autodesk validation
        autodesk_credentials = {
            'client_id': os.getenv('AUTODESK_CLIENT_ID'),
            'client_secret': os.getenv('AUTODESK_CLIENT_SECRET')
        }
        
        if all(autodesk_credentials.values()):
            try:
                auth_url = "https://developer.api.autodesk.com/authentication/v1/authenticate"
                response = requests.post(auth_url, data={
                    'client_id': autodesk_credentials['client_id'],
                    'client_secret': autodesk_credentials['client_secret'],
                    'grant_type': 'client_credentials',
                    'scope': 'data:read'
                }, timeout=10)
                
                if response.status_code == 200:
                    integration_results['autodesk'] = (True, "Autodesk API connection successful")
                else:
                    integration_results['autodesk'] = (False, f"Autodesk API error: {response.status_code}")
                    
            except Exception as e:
                integration_results['autodesk'] = (False, f"Autodesk connection failed: {str(e)}")
        else:
            integration_results['autodesk'] = (False, "Autodesk credentials not configured")
        
        return integration_results
    
    def validate_security_configuration(self) -> Tuple[bool, str]:
        """Validate security configuration"""
        security_issues = []
        
        # JWT secret validation
        jwt_secret = os.getenv('JWT_SECRET_KEY')
        if not jwt_secret:
            security_issues.append("JWT_SECRET_KEY not configured")
        elif len(jwt_secret) < 32:
            security_issues.append("JWT_SECRET_KEY too short (minimum 32 characters)")
        
        # Session configuration
        session_timeout = os.getenv('SESSION_TIMEOUT', '3600')
        try:
            timeout_int = int(session_timeout)
            if timeout_int < 300:  # 5 minutes minimum
                security_issues.append("SESSION_TIMEOUT too short (minimum 300 seconds)")
        except ValueError:
            security_issues.append("SESSION_TIMEOUT must be a valid integer")
        
        # Environment validation
        environment = os.getenv('ENVIRONMENT', 'development')
        if environment == 'production':
            # Additional production security checks
            if not os.getenv('HTTPS_ONLY'):
                security_issues.append("HTTPS_ONLY not enforced in production")
        
        if security_issues:
            return False, f"Security issues: {'; '.join(security_issues)}"
        
        return True, "Security configuration validated"
    
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run all validation tests"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'tests': {},
            'overall_status': 'pending'
        }
        
        # Database tests
        db_success, db_message = self.validate_database_connection()
        results['tests']['database_connection'] = {'success': db_success, 'message': db_message}
        
        if db_success:
            tables_success, tables_message = self.validate_core_tables()
            results['tests']['core_tables'] = {'success': tables_success, 'message': tables_message}
            
            integrity_success, integrity_message = self.validate_data_integrity()
            results['tests']['data_integrity'] = {'success': integrity_success, 'message': integrity_message}
        
        # API integration tests
        api_results = self.validate_api_integrations()
        for api_name, (success, message) in api_results.items():
            results['tests'][f'{api_name}_integration'] = {'success': success, 'message': message}
        
        # Security tests
        security_success, security_message = self.validate_security_configuration()
        results['tests']['security_config'] = {'success': security_success, 'message': security_message}
        
        # Calculate overall status
        total_tests = len(results['tests'])
        passed_tests = sum(1 for test in results['tests'].values() if test['success'])
        
        results['overall_status'] = 'passed' if passed_tests == total_tests else 'failed'
        results['success_rate'] = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        return results

def render_validation_dashboard():
    """Render system validation dashboard"""
    st.markdown("### System Validation & Testing")
    
    validator = SystemValidator()
    
    if st.button("Run Comprehensive System Validation", type="primary"):
        with st.spinner("Running validation tests..."):
            results = validator.run_comprehensive_validation()
        
        st.session_state.validation_results = results
    
    if 'validation_results' in st.session_state:
        results = st.session_state.validation_results
        
        # Overall status
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if results['overall_status'] == 'passed':
                st.success(f"**System Status: PASSED**")
            else:
                st.error(f"**System Status: FAILED**")
        
        with col2:
            st.metric("Success Rate", f"{results['success_rate']:.1f}%")
        
        with col3:
            st.metric("Tests Run", len(results['tests']))
        
        # Detailed test results
        st.markdown("### Test Results")
        
        for test_name, test_result in results['tests'].items():
            with st.expander(f"{test_name.replace('_', ' ').title()}", expanded=not test_result['success']):
                if test_result['success']:
                    st.success(test_result['message'])
                else:
                    st.error(test_result['message'])
        
        # Recommendations
        failed_tests = [name for name, result in results['tests'].items() if not result['success']]
        
        if failed_tests:
            st.markdown("### Recommendations")
            
            for test_name in failed_tests:
                if 'database' in test_name:
                    st.info("Configure DATABASE_URL environment variable with valid PostgreSQL connection string")
                elif 'integration' in test_name:
                    st.info(f"Configure {test_name.split('_')[0].upper()} API credentials for external integrations")
                elif 'security' in test_name:
                    st.info("Review and configure security settings including JWT_SECRET_KEY")
        else:
            st.success("All validation tests passed! System is ready for production deployment.")

def validate_environment_variables() -> List[Tuple[str, bool, str]]:
    """Validate required environment variables"""
    required_vars = [
        ('DATABASE_URL', 'PostgreSQL database connection string'),
        ('JWT_SECRET_KEY', 'JWT token signing secret'),
        ('ENVIRONMENT', 'Application environment (development/production)')
    ]
    
    optional_vars = [
        ('PROCORE_CLIENT_ID', 'Procore API client ID'),
        ('PROCORE_CLIENT_SECRET', 'Procore API client secret'),
        ('PROCORE_COMPANY_ID', 'Procore company ID'),
        ('AUTODESK_CLIENT_ID', 'Autodesk API client ID'),
        ('AUTODESK_CLIENT_SECRET', 'Autodesk API client secret'),
        ('SAGE_CLIENT_ID', 'Sage API client ID'),
        ('SAGE_CLIENT_SECRET', 'Sage API client secret')
    ]
    
    results = []
    
    for var_name, description in required_vars:
        value = os.getenv(var_name)
        results.append((var_name, bool(value), description))
    
    for var_name, description in optional_vars:
        value = os.getenv(var_name)
        results.append((var_name, bool(value), f"{description} (optional)"))
    
    return results

def render_environment_status():
    """Render environment configuration status"""
    st.markdown("### Environment Configuration")
    
    env_vars = validate_environment_variables()
    
    for var_name, is_set, description in env_vars:
        col1, col2, col3 = st.columns([2, 1, 3])
        
        with col1:
            st.write(f"**{var_name}**")
        
        with col2:
            if is_set:
                st.success("✓ Set")
            else:
                if "(optional)" in description:
                    st.warning("Not set")
                else:
                    st.error("✗ Missing")
        
        with col3:
            st.write(description)

def check_system_health():
    """Quick system health check"""
    health_status = {
        'database': bool(os.getenv('DATABASE_URL')),
        'security': bool(os.getenv('JWT_SECRET_KEY')),
        'integrations': any([
            os.getenv('PROCORE_CLIENT_ID'),
            os.getenv('AUTODESK_CLIENT_ID'),
            os.getenv('SAGE_CLIENT_ID')
        ])
    }
    
    healthy_components = sum(health_status.values())
    total_components = len(health_status)
    
    return healthy_components, total_components, health_status