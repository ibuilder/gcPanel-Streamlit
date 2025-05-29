"""
Real-time Collaboration Manager for Highland Tower Development

Enables live collaboration features including:
- User presence tracking
- Real-time updates
- Live cursors and editing
- Team communication
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

class CollaborationManager:
    """Manages real-time collaboration features for the Highland Tower Development dashboard."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.active_users = {}
        self.collaboration_events = []
        
    def initialize(self):
        """Initialize collaboration system."""
        if "collaboration_active" not in st.session_state:
            st.session_state.collaboration_active = True
        
        if "live_users" not in st.session_state:
            st.session_state.live_users = {}
        
        if "user_presence" not in st.session_state:
            st.session_state.user_presence = {
                "status": "online",
                "last_seen": datetime.now().isoformat(),
                "current_module": "Dashboard"
            }
    
    def update_user_presence(self, user_id: str, module: str = None):
        """Update user presence information."""
        if user_id not in st.session_state.live_users:
            st.session_state.live_users[user_id] = {}
        
        st.session_state.live_users[user_id].update({
            "status": "online",
            "last_seen": datetime.now().isoformat(),
            "current_module": module or st.session_state.get("current_module", "Dashboard"),
            "session_id": st.session_state.get("session_id", "unknown")
        })
    
    def get_active_users(self) -> Dict[str, Any]:
        """Get list of currently active users."""
        current_time = datetime.now()
        active_users = {}
        
        for user_id, presence in st.session_state.get("live_users", {}).items():
            last_seen = datetime.fromisoformat(presence["last_seen"])
            if (current_time - last_seen).total_seconds() < 300:  # 5 minutes
                active_users[user_id] = presence
        
        return active_users
    
    def broadcast_update(self, update_type: str, data: Dict[str, Any]):
        """Broadcast update to all active users."""
        update = {
            "type": update_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "user_id": st.session_state.get("current_user", {}).get("id", "unknown")
        }
        
        # Store in collaboration events (in production, this would use WebSockets)
        if "collaboration_events" not in st.session_state:
            st.session_state.collaboration_events = []
        
        st.session_state.collaboration_events.append(update)
        
        # Keep only recent events
        cutoff_time = datetime.now() - timedelta(minutes=30)
        st.session_state.collaboration_events = [
            event for event in st.session_state.collaboration_events
            if datetime.fromisoformat(event["timestamp"]) > cutoff_time
        ]
    
    def get_updates(self) -> List[Dict[str, Any]]:
        """Get recent collaboration updates."""
        current_user_id = st.session_state.get("current_user", {}).get("id", "unknown")
        events = st.session_state.get("collaboration_events", [])
        
        # Return events from other users
        return [event for event in events if event["user_id"] != current_user_id]
    
    def notify_data_change(self, module: str, item_id: str, action: str):
        """Notify other users of data changes."""
        self.broadcast_update("data_change", {
            "module": module,
            "item_id": item_id,
            "action": action
        })
    
    def start_collaborative_editing(self, module: str, item_id: str):
        """Start collaborative editing session."""
        user_id = st.session_state.get("current_user", {}).get("id", "unknown")
        
        editing_session = {
            "module": module,
            "item_id": item_id,
            "user_id": user_id,
            "started": datetime.now().isoformat()
        }
        
        if "active_editing_sessions" not in st.session_state:
            st.session_state.active_editing_sessions = {}
        
        session_key = f"{module}_{item_id}"
        st.session_state.active_editing_sessions[session_key] = editing_session
        
        self.broadcast_update("editing_started", editing_session)
    
    def end_collaborative_editing(self, module: str, item_id: str):
        """End collaborative editing session."""
        session_key = f"{module}_{item_id}"
        
        if "active_editing_sessions" in st.session_state:
            if session_key in st.session_state.active_editing_sessions:
                session = st.session_state.active_editing_sessions.pop(session_key)
                self.broadcast_update("editing_ended", session)
    
    def get_editing_conflicts(self, module: str, item_id: str) -> List[Dict[str, Any]]:
        """Check for editing conflicts."""
        session_key = f"{module}_{item_id}"
        current_user_id = st.session_state.get("current_user", {}).get("id", "unknown")
        
        active_sessions = st.session_state.get("active_editing_sessions", {})
        
        conflicts = []
        if session_key in active_sessions:
            session = active_sessions[session_key]
            if session["user_id"] != current_user_id:
                conflicts.append(session)
        
        return conflicts