"""
Audit Manager for Highland Tower Development

Comprehensive audit logging and security monitoring for all user actions.
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
import json

class AuditManager:
    """Manages audit logging and security monitoring for the Highland Tower Development dashboard."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def initialize(self):
        """Initialize audit system."""
        if "audit_log" not in st.session_state:
            st.session_state.audit_log = []
    
    def log_action(self, user_id: str, action: str, module: str, details: Dict[str, Any] = None):
        """Log user action for audit trail."""
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "action": action,
            "module": module,
            "details": details or {},
            "session_id": st.session_state.get("session_id", "unknown"),
            "ip_address": "127.0.0.1"  # In production, get real IP
        }
        
        st.session_state.audit_log.append(audit_entry)
        
        # Keep only recent entries in session
        if len(st.session_state.audit_log) > 1000:
            st.session_state.audit_log = st.session_state.audit_log[-500:]
        
        self.logger.info(f"Audit: {user_id} - {action} in {module}")
    
    def get_audit_log(self, module: str = None, user_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get audit log entries with optional filtering."""
        entries = st.session_state.get("audit_log", [])
        
        # Apply filters
        if module:
            entries = [e for e in entries if e["module"] == module]
        
        if user_id:
            entries = [e for e in entries if e["user_id"] == user_id]
        
        # Sort by timestamp (newest first)
        entries.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return entries[:limit]
    
    def get_security_events(self) -> List[Dict[str, Any]]:
        """Get security-related audit events."""
        security_actions = ["login", "logout", "failed_login", "permission_denied", "data_export"]
        
        entries = st.session_state.get("audit_log", [])
        security_events = [e for e in entries if e["action"] in security_actions]
        
        return security_events
    
    def generate_audit_report(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Generate comprehensive audit report."""
        entries = st.session_state.get("audit_log", [])
        
        # Filter by date if provided
        if start_date or end_date:
            filtered_entries = []
            for entry in entries:
                entry_date = datetime.fromisoformat(entry["timestamp"]).date()
                
                if start_date and entry_date < datetime.fromisoformat(start_date).date():
                    continue
                if end_date and entry_date > datetime.fromisoformat(end_date).date():
                    continue
                
                filtered_entries.append(entry)
            
            entries = filtered_entries
        
        # Generate statistics
        total_actions = len(entries)
        unique_users = len(set(e["user_id"] for e in entries))
        modules_accessed = len(set(e["module"] for e in entries))
        
        # Action breakdown
        action_counts = {}
        module_counts = {}
        user_counts = {}
        
        for entry in entries:
            action_counts[entry["action"]] = action_counts.get(entry["action"], 0) + 1
            module_counts[entry["module"]] = module_counts.get(entry["module"], 0) + 1
            user_counts[entry["user_id"]] = user_counts.get(entry["user_id"], 0) + 1
        
        return {
            "total_actions": total_actions,
            "unique_users": unique_users,
            "modules_accessed": modules_accessed,
            "top_actions": sorted(action_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            "top_modules": sorted(module_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            "top_users": sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            "date_range": {
                "start": entries[-1]["timestamp"] if entries else None,
                "end": entries[0]["timestamp"] if entries else None
            }
        }