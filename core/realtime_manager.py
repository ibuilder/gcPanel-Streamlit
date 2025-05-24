"""
Real-time Updates Manager for gcPanel Highland Tower Development

Implements WebSocket connections and live notifications for real-time
project updates and collaborative construction management.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Callable
import streamlit as st
from streamlit.runtime.caching import cache_data
import threading
import queue
import time

class RealtimeManager:
    """Enterprise real-time updates manager"""
    
    def __init__(self):
        self.subscribers = {}
        self.message_queue = queue.Queue()
        self.setup_logging()
        self.initialize_realtime_system()
    
    def setup_logging(self):
        """Setup real-time operation logging"""
        self.logger = logging.getLogger('RealtimeManager')
    
    def initialize_realtime_system(self):
        """Initialize real-time notification system"""
        if 'realtime_initialized' not in st.session_state:
            st.session_state.realtime_initialized = True
            st.session_state.notifications = []
            st.session_state.live_updates_enabled = True
    
    def subscribe_to_updates(self, channel: str, callback: Callable):
        """Subscribe to real-time updates for specific channel"""
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        self.subscribers[channel].append(callback)
        self.logger.info(f"Subscribed to channel: {channel}")
    
    def publish_update(self, channel: str, data: Dict):
        """Publish real-time update to subscribers"""
        update_message = {
            'timestamp': datetime.now().isoformat(),
            'channel': channel,
            'data': data,
            'project': 'highland_tower'
        }
        
        # Add to message queue
        self.message_queue.put(update_message)
        
        # Notify subscribers
        if channel in self.subscribers:
            for callback in self.subscribers[channel]:
                try:
                    callback(update_message)
                except Exception as e:
                    self.logger.error(f"Callback error: {e}")
    
    def add_notification(self, title: str, message: str, type: str = "info", 
                        action_url: str = None):
        """Add real-time notification"""
        notification = {
            'id': f"notif_{int(time.time())}",
            'title': title,
            'message': message,
            'type': type,
            'timestamp': datetime.now().isoformat(),
            'read': False,
            'action_url': action_url
        }
        
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
        
        st.session_state.notifications.insert(0, notification)
        
        # Limit to last 50 notifications
        st.session_state.notifications = st.session_state.notifications[:50]
        
        # Publish to real-time channel
        self.publish_update('notifications', notification)
    
    def get_unread_notifications(self) -> List[Dict]:
        """Get unread notifications"""
        if 'notifications' not in st.session_state:
            return []
        
        return [n for n in st.session_state.notifications if not n.get('read', False)]
    
    def mark_notification_read(self, notification_id: str):
        """Mark notification as read"""
        if 'notifications' not in st.session_state:
            return
        
        for notification in st.session_state.notifications:
            if notification['id'] == notification_id:
                notification['read'] = True
                break
    
    def render_live_notifications(self):
        """Render live notification center"""
        unread_count = len(self.get_unread_notifications())
        
        # Notification bell with count
        if unread_count > 0:
            st.markdown(f"""
            <div style="position: fixed; top: 20px; right: 20px; z-index: 1000;">
                <div style="background: #ff4444; color: white; border-radius: 50%; 
                           width: 30px; height: 30px; display: flex; align-items: center; 
                           justify-content: center; font-weight: bold; font-size: 12px;">
                    {unread_count}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Notification panel toggle
        if st.button("🔔 Notifications", key="notifications_toggle"):
            st.session_state.show_notifications = not st.session_state.get('show_notifications', False)
        
        # Show notifications panel
        if st.session_state.get('show_notifications', False):
            self.render_notification_panel()
    
    def render_notification_panel(self):
        """Render notification panel"""
        st.markdown("### 🔔 Live Notifications - Highland Tower Development")
        
        notifications = st.session_state.get('notifications', [])
        
        if not notifications:
            st.info("No notifications yet")
            return
        
        # Mark all as read button
        if st.button("✅ Mark All Read"):
            for notification in notifications:
                notification['read'] = True
            st.rerun()
        
        # Display notifications
        for notification in notifications[:10]:  # Show last 10
            self.render_notification_item(notification)
    
    def render_notification_item(self, notification: Dict):
        """Render individual notification item"""
        # Icon based on type
        type_icons = {
            'info': '💡',
            'success': '✅', 
            'warning': '⚠️',
            'error': '❌',
            'update': '🔄'
        }
        
        icon = type_icons.get(notification['type'], '📢')
        
        # Style based on read status
        bg_color = "#f0f0f0" if notification.get('read') else "#e8f4fd"
        
        st.markdown(f"""
        <div style="background: {bg_color}; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 4px solid #4CAF50;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{icon} {notification['title']}</strong><br>
                    <span style="color: #666;">{notification['message']}</span><br>
                    <small style="color: #999;">{notification['timestamp']}</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Mark as read when viewed
        if not notification.get('read'):
            self.mark_notification_read(notification['id'])

@st.cache_resource
def get_realtime_manager():
    """Get cached real-time manager instance"""
    return RealtimeManager()

class LiveDataUpdater:
    """Live data updates for Highland Tower Development metrics"""
    
    def __init__(self):
        self.realtime_manager = get_realtime_manager()
        self.update_intervals = {
            'project_metrics': 300,  # 5 minutes
            'active_rfis': 60,      # 1 minute
            'safety_alerts': 30,    # 30 seconds
            'quality_checks': 120   # 2 minutes
        }
    
    def start_live_updates(self):
        """Start live data update threads"""
        if 'live_updates_started' not in st.session_state:
            st.session_state.live_updates_started = True
            
            # Simulate live updates (in production, these would be real data sources)
            self.simulate_project_updates()
    
    def simulate_project_updates(self):
        """Simulate real-time project updates"""
        # RFI updates
        if st.session_state.get('live_updates_enabled'):
            self.realtime_manager.add_notification(
                "New RFI Submitted",
                "RFI-2025-045: Electrical outlet placement clarification - Floor 12",
                "info",
                "/rfis"
            )
        
        # Quality check updates
        if st.session_state.get('live_updates_enabled'):
            self.realtime_manager.add_notification(
                "Quality Check Completed",
                "Concrete pour inspection passed - Floor 14 East Wing",
                "success",
                "/quality-control"
            )
    
    def update_project_metrics(self):
        """Update live project metrics"""
        metrics_update = {
            'timestamp': datetime.now().isoformat(),
            'overall_progress': 72.3,
            'budget_utilization': 68.5,
            'safety_score': 98.2,
            'quality_score': 94.1
        }
        
        self.realtime_manager.publish_update('project_metrics', metrics_update)
    
    def update_active_rfis(self):
        """Update active RFIs count"""
        rfi_update = {
            'timestamp': datetime.now().isoformat(),
            'total_active': 12,
            'new_today': 3,
            'pending_response': 5
        }
        
        self.realtime_manager.publish_update('active_rfis', rfi_update)

def add_live_status_indicator():
    """Add live status indicator to show real-time connection"""
    st.markdown("""
    <div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
        <div style="background: #4CAF50; color: white; padding: 5px 10px; 
                   border-radius: 15px; font-size: 12px; display: flex; 
                   align-items: center;">
            <div style="width: 8px; height: 8px; background: #fff; 
                       border-radius: 50%; margin-right: 5px; 
                       animation: pulse 2s infinite;"></div>
            Live Updates Active
        </div>
    </div>
    
    <style>
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_live_updates():
    """Initialize live updates for Highland Tower Development"""
    realtime_manager = get_realtime_manager()
    live_updater = LiveDataUpdater()
    
    # Start live updates
    live_updater.start_live_updates()
    
    # Add status indicator
    add_live_status_indicator()
    
    # Enable auto-refresh for critical data
    if st.session_state.get('live_updates_enabled', True):
        time.sleep(0.1)  # Small delay to prevent overwhelming
        st.rerun()