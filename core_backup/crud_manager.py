"""
CRUD Manager for Highland Tower Development
Enterprise-grade data operations with real database integration
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import hashlib
import uuid

# Import database connection
try:
    from database.connection import db_manager
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class CRUDManager:
    """Centralized CRUD operations for Highland Tower Development"""
    
    def __init__(self):
        self.db_available = DATABASE_AVAILABLE
    
    # ============= RFI CRUD OPERATIONS =============
    
    def create_rfi(self, data: Dict) -> Dict:
        """Create new RFI with full workflow"""
        rfi_data = {
            'id': str(uuid.uuid4()),
            'rfi_number': f"HTD-RFI-{datetime.now().strftime('%Y%m%d')}-{self._generate_sequence()}",
            'project_id': 1,  # Highland Tower Development
            'subject': data.get('subject'),
            'description': data.get('description'),
            'location': data.get('location'),
            'priority': data.get('priority', 'medium'),
            'discipline': data.get('discipline'),
            'submitted_by': data.get('submitted_by'),
            'assigned_to': data.get('assigned_to'),
            'status': 'open',
            'due_date': data.get('due_date'),
            'created_at': datetime.now(),
            'cost_impact': data.get('cost_impact'),
            'attachments': data.get('attachments', [])
        }
        
        if self.db_available:
            # Insert into database
            query = """
            INSERT INTO rfis (rfi_number, subject, description, location, priority, 
                            submitted_by, assigned_to, due_date, project_id, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """
            params = (
                rfi_data['rfi_number'], rfi_data['subject'], rfi_data['description'],
                rfi_data['location'], rfi_data['priority'], rfi_data['submitted_by'],
                rfi_data['assigned_to'], rfi_data['due_date'], rfi_data['project_id'],
                rfi_data['created_at']
            )
            result = db_manager.execute_query(query, params)
            if result:
                rfi_data['db_id'] = result[0]['id']
        
        # Store in session state as fallback
        if 'rfis' not in st.session_state:
            st.session_state.rfis = []
        st.session_state.rfis.append(rfi_data)
        
        # Create audit log entry
        self._create_audit_log('CREATE', 'rfis', rfi_data['id'], None, rfi_data)
        
        return rfi_data
    
    def get_rfis(self, filters: Dict = None) -> List[Dict]:
        """Get RFIs with filtering options"""
        if self.db_available:
            query = """
            SELECT r.*, u1.full_name as submitted_by_name, u2.full_name as assigned_to_name
            FROM rfis r
            LEFT JOIN users u1 ON r.submitted_by = u1.id
            LEFT JOIN users u2 ON r.assigned_to = u2.id
            WHERE r.project_id = 1
            ORDER BY r.created_at DESC
            """
            result = db_manager.execute_query(query)
            if result:
                return result
        
        # Fallback to session state
        rfis = st.session_state.get('rfis', [])
        
        # Apply filters
        if filters:
            if filters.get('status'):
                rfis = [r for r in rfis if r['status'] == filters['status']]
            if filters.get('priority'):
                rfis = [r for r in rfis if r['priority'] == filters['priority']]
            if filters.get('discipline'):
                rfis = [r for r in rfis if r['discipline'] == filters['discipline']]
        
        return rfis
    
    def update_rfi(self, rfi_id: str, updates: Dict) -> bool:
        """Update RFI with change tracking"""
        if self.db_available:
            # Get current RFI
            current_rfi = self.get_rfi_by_id(rfi_id)
            
            # Build update query
            set_clauses = []
            params = []
            for key, value in updates.items():
                if key in ['subject', 'description', 'status', 'priority', 'assigned_to', 'response_text']:
                    set_clauses.append(f"{key} = %s")
                    params.append(value)
            
            if set_clauses:
                params.append(datetime.now())  # updated_at
                params.append(rfi_id)
                
                query = f"""
                UPDATE rfis 
                SET {', '.join(set_clauses)}, updated_at = %s
                WHERE id = %s
                """
                result = db_manager.execute_query(query, tuple(params))
                
                if result:
                    self._create_audit_log('UPDATE', 'rfis', rfi_id, current_rfi, updates)
                    return True
        
        # Fallback to session state
        rfis = st.session_state.get('rfis', [])
        for rfi in rfis:
            if rfi['id'] == rfi_id:
                old_data = rfi.copy()
                rfi.update(updates)
                rfi['updated_at'] = datetime.now()
                self._create_audit_log('UPDATE', 'rfis', rfi_id, old_data, rfi)
                return True
        
        return False
    
    def delete_rfi(self, rfi_id: str) -> bool:
        """Soft delete RFI (mark as deleted)"""
        return self.update_rfi(rfi_id, {'status': 'deleted', 'deleted_at': datetime.now()})
    
    # ============= DAILY REPORTS CRUD OPERATIONS =============
    
    def create_daily_report(self, data: Dict) -> Dict:
        """Create new daily report"""
        report_data = {
            'id': str(uuid.uuid4()),
            'project_id': 1,
            'report_date': data.get('report_date', datetime.now().date()),
            'weather_conditions': data.get('weather_conditions'),
            'temperature_high': data.get('temperature_high'),
            'temperature_low': data.get('temperature_low'),
            'work_performed': data.get('work_performed'),
            'delays_issues': data.get('delays_issues'),
            'safety_notes': data.get('safety_notes'),
            'crew_count': data.get('crew_count'),
            'equipment_on_site': data.get('equipment_on_site'),
            'materials_delivered': data.get('materials_delivered'),
            'created_by': data.get('created_by'),
            'created_at': datetime.now(),
            'photos': data.get('photos', [])
        }
        
        if self.db_available:
            query = """
            INSERT INTO daily_reports (project_id, report_date, weather_conditions, 
                                     temperature_high, temperature_low, work_performed, 
                                     delays_issues, safety_notes, crew_count, 
                                     equipment_on_site, materials_delivered, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """
            params = (
                report_data['project_id'], report_data['report_date'], 
                report_data['weather_conditions'], report_data['temperature_high'],
                report_data['temperature_low'], report_data['work_performed'],
                report_data['delays_issues'], report_data['safety_notes'],
                report_data['crew_count'], report_data['equipment_on_site'],
                report_data['materials_delivered'], report_data['created_by']
            )
            result = db_manager.execute_query(query, params)
            if result:
                report_data['db_id'] = result[0]['id']
        
        # Store in session state
        if 'daily_reports' not in st.session_state:
            st.session_state.daily_reports = []
        st.session_state.daily_reports.append(report_data)
        
        self._create_audit_log('CREATE', 'daily_reports', report_data['id'], None, report_data)
        return report_data
    
    def get_daily_reports(self, date_range: tuple = None) -> List[Dict]:
        """Get daily reports with optional date filtering"""
        if self.db_available:
            query = """
            SELECT dr.*, u.full_name as created_by_name
            FROM daily_reports dr
            LEFT JOIN users u ON dr.created_by = u.id
            WHERE dr.project_id = 1
            ORDER BY dr.report_date DESC
            LIMIT 50
            """
            result = db_manager.execute_query(query)
            if result:
                return result
        
        # Fallback to session state
        reports = st.session_state.get('daily_reports', [])
        
        # Apply date filtering
        if date_range:
            start_date, end_date = date_range
            reports = [r for r in reports if start_date <= r['report_date'] <= end_date]
        
        return sorted(reports, key=lambda x: x['report_date'], reverse=True)
    
    # ============= USER MANAGEMENT CRUD OPERATIONS =============
    
    def create_user(self, data: Dict) -> Dict:
        """Create new user with role assignment"""
        user_data = {
            'id': str(uuid.uuid4()),
            'username': data.get('username'),
            'email': data.get('email'),
            'full_name': data.get('full_name'),
            'role': data.get('role', 'user'),
            'department': data.get('department'),
            'phone': data.get('phone'),
            'password_hash': self._hash_password(data.get('password', 'TempPassword123!')),
            'is_active': True,
            'created_at': datetime.now(),
            'permissions': data.get('permissions', {})
        }
        
        if self.db_available:
            query = """
            INSERT INTO users (username, email, full_name, role, phone, password_hash, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """
            params = (
                user_data['username'], user_data['email'], user_data['full_name'],
                user_data['role'], user_data['phone'], user_data['password_hash'],
                user_data['is_active']
            )
            result = db_manager.execute_query(query, params)
            if result:
                user_data['db_id'] = result[0]['id']
        
        # Store in session state
        if 'users' not in st.session_state:
            st.session_state.users = []
        st.session_state.users.append(user_data)
        
        self._create_audit_log('CREATE', 'users', user_data['id'], None, user_data)
        return user_data
    
    def get_users(self, active_only: bool = True) -> List[Dict]:
        """Get all users with filtering"""
        if self.db_available:
            query = """
            SELECT id, username, email, full_name, role, phone, is_active, created_at
            FROM users
            WHERE is_active = %s OR %s = FALSE
            ORDER BY full_name
            """
            result = db_manager.execute_query(query, (True, active_only))
            if result:
                return result
        
        # Fallback to session state
        users = st.session_state.get('users', [])
        if active_only:
            users = [u for u in users if u.get('is_active', True)]
        
        return users
    
    def update_user(self, user_id: str, updates: Dict) -> bool:
        """Update user information"""
        if 'password' in updates:
            updates['password_hash'] = self._hash_password(updates.pop('password'))
        
        if self.db_available:
            set_clauses = []
            params = []
            for key, value in updates.items():
                if key in ['username', 'email', 'full_name', 'role', 'phone', 'password_hash', 'is_active']:
                    set_clauses.append(f"{key} = %s")
                    params.append(value)
            
            if set_clauses:
                params.append(datetime.now())
                params.append(user_id)
                
                query = f"""
                UPDATE users 
                SET {', '.join(set_clauses)}, updated_at = %s
                WHERE id = %s
                """
                result = db_manager.execute_query(query, tuple(params))
                return result is not None
        
        # Fallback to session state
        users = st.session_state.get('users', [])
        for user in users:
            if user['id'] == user_id:
                user.update(updates)
                user['updated_at'] = datetime.now()
                return True
        
        return False
    
    # ============= SEARCH AND FILTER OPERATIONS =============
    
    def global_search(self, search_term: str, modules: List[str] = None) -> Dict:
        """Global search across all project data"""
        results = {
            'rfis': [],
            'daily_reports': [],
            'users': [],
            'submittals': []
        }
        
        if not modules:
            modules = ['rfis', 'daily_reports', 'users']
        
        search_term = search_term.lower()
        
        # Search RFIs
        if 'rfis' in modules:
            rfis = self.get_rfis()
            for rfi in rfis:
                if (search_term in rfi.get('subject', '').lower() or 
                    search_term in rfi.get('description', '').lower() or
                    search_term in rfi.get('rfi_number', '').lower()):
                    results['rfis'].append(rfi)
        
        # Search Daily Reports
        if 'daily_reports' in modules:
            reports = self.get_daily_reports()
            for report in reports:
                if (search_term in str(report.get('work_performed', '')).lower() or
                    search_term in str(report.get('delays_issues', '')).lower()):
                    results['daily_reports'].append(report)
        
        # Search Users
        if 'users' in modules:
            users = self.get_users()
            for user in users:
                if (search_term in user.get('full_name', '').lower() or
                    search_term in user.get('email', '').lower() or
                    search_term in user.get('role', '').lower()):
                    results['users'].append(user)
        
        return results
    
    # ============= HELPER METHODS =============
    
    def _generate_sequence(self) -> str:
        """Generate sequence number for documents"""
        return f"{datetime.now().microsecond:06d}"[-3:]
    
    def _hash_password(self, password: str) -> str:
        """Hash password for secure storage"""
        return hashlib.sha256(f"highland_tower_{password}".encode()).hexdigest()
    
    def _create_audit_log(self, action: str, table_name: str, record_id: str, 
                         old_values: Dict, new_values: Dict):
        """Create audit log entry"""
        audit_data = {
            'id': str(uuid.uuid4()),
            'action': action,
            'table_name': table_name,
            'record_id': record_id,
            'old_values': old_values,
            'new_values': new_values,
            'user_id': st.session_state.get('user_id', 'system'),
            'timestamp': datetime.now(),
            'ip_address': st.session_state.get('client_ip', 'unknown')
        }
        
        if self.db_available:
            query = """
            INSERT INTO audit_log (action, table_name, record_id, old_values, new_values, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                audit_data['action'], audit_data['table_name'], audit_data['record_id'],
                str(audit_data['old_values']), str(audit_data['new_values']), audit_data['user_id']
            )
            db_manager.execute_query(query, params)
        
        # Store in session state
        if 'audit_logs' not in st.session_state:
            st.session_state.audit_logs = []
        st.session_state.audit_logs.append(audit_data)
    
    def get_rfi_by_id(self, rfi_id: str) -> Optional[Dict]:
        """Get single RFI by ID"""
        rfis = self.get_rfis()
        for rfi in rfis:
            if rfi['id'] == rfi_id:
                return rfi
        return None

# Global CRUD manager instance
crud_manager = CRUDManager()