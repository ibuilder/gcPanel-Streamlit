"""
Highland Tower Development - Real-time Data Synchronization
Handles live updates and data consistency across all construction management modules
"""

import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
import logging

class RealTimeDataSync:
    """Manages real-time data synchronization for Highland Tower project"""
    
    def __init__(self):
        self.connection = None
        self.initialize_connection()
    
    def initialize_connection(self):
        """Initialize database connection"""
        try:
            database_url = os.getenv('DATABASE_URL')
            if database_url:
                self.connection = psycopg2.connect(
                    database_url,
                    cursor_factory=RealDictCursor
                )
                self.setup_real_time_tables()
            else:
                logging.warning("Database connection not available")
        except Exception as e:
            logging.error(f"Database connection error: {e}")
    
    def setup_real_time_tables(self):
        """Setup tables for real-time data tracking"""
        try:
            with self.connection.cursor() as cursor:
                # Activity log for real-time updates
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS highland_activity_log (
                        id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        module VARCHAR(50) NOT NULL,
                        action VARCHAR(50) NOT NULL,
                        user_id VARCHAR(100),
                        details JSONB,
                        project_id VARCHAR(50) DEFAULT 'highland_tower'
                    )
                """)
                
                # Real-time metrics
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS highland_real_time_metrics (
                        id SERIAL PRIMARY KEY,
                        metric_name VARCHAR(100) NOT NULL,
                        metric_value DECIMAL(15,2),
                        metric_unit VARCHAR(20),
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        category VARCHAR(50)
                    )
                """)
                
                # Live notifications
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS highland_notifications (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(200) NOT NULL,
                        message TEXT,
                        notification_type VARCHAR(50) DEFAULT 'info',
                        target_user VARCHAR(100),
                        is_read BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP
                    )
                """)
                
                self.connection.commit()
                
        except Exception as e:
            logging.error(f"Real-time table setup error: {e}")
    
    def log_activity(self, module: str, action: str, user_id: str = "system", details: Dict = None):
        """Log activity for real-time tracking"""
        try:
            if self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO highland_activity_log (module, action, user_id, details)
                        VALUES (%s, %s, %s, %s)
                    """, (module, action, user_id, json.dumps(details or {})))
                    self.connection.commit()
        except Exception as e:
            logging.error(f"Activity logging error: {e}")
    
    def update_metric(self, metric_name: str, value: float, unit: str = "", category: str = "general"):
        """Update real-time metric"""
        try:
            if self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO highland_real_time_metrics (metric_name, metric_value, metric_unit, category)
                        VALUES (%s, %s, %s, %s)
                    """, (metric_name, value, unit, category))
                    self.connection.commit()
        except Exception as e:
            logging.error(f"Metric update error: {e}")
    
    def get_recent_activities(self, limit: int = 20) -> List[Dict]:
        """Get recent project activities"""
        try:
            if self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT module, action, user_id, details, timestamp
                        FROM highland_activity_log
                        ORDER BY timestamp DESC
                        LIMIT %s
                    """, (limit,))
                    return cursor.fetchall()
            return []
        except Exception as e:
            logging.error(f"Recent activities retrieval error: {e}")
            return []
    
    def get_live_metrics(self) -> Dict[str, Any]:
        """Get current live project metrics"""
        try:
            metrics = {}
            if self.connection:
                with self.connection.cursor() as cursor:
                    # Get latest metrics by category
                    cursor.execute("""
                        SELECT DISTINCT ON (metric_name) 
                               metric_name, metric_value, metric_unit, category, timestamp
                        FROM highland_real_time_metrics
                        ORDER BY metric_name, timestamp DESC
                    """)
                    
                    for row in cursor.fetchall():
                        metrics[row['metric_name']] = {
                            'value': float(row['metric_value']),
                            'unit': row['metric_unit'],
                            'category': row['category'],
                            'timestamp': row['timestamp']
                        }
            
            return metrics
        except Exception as e:
            logging.error(f"Live metrics retrieval error: {e}")
            return {}
    
    def create_notification(self, title: str, message: str, notification_type: str = "info", 
                          target_user: str = None, expires_hours: int = 24):
        """Create real-time notification"""
        try:
            if self.connection:
                with self.connection.cursor() as cursor:
                    expires_at = datetime.now() + timedelta(hours=expires_hours)
                    cursor.execute("""
                        INSERT INTO highland_notifications 
                        (title, message, notification_type, target_user, expires_at)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (title, message, notification_type, target_user, expires_at))
                    self.connection.commit()
        except Exception as e:
            logging.error(f"Notification creation error: {e}")
    
    def get_active_notifications(self, user_id: str = None) -> List[Dict]:
        """Get active notifications for user"""
        try:
            if self.connection:
                with self.connection.cursor() as cursor:
                    if user_id:
                        cursor.execute("""
                            SELECT title, message, notification_type, created_at
                            FROM highland_notifications
                            WHERE (target_user = %s OR target_user IS NULL)
                            AND NOT is_read
                            AND (expires_at IS NULL OR expires_at > NOW())
                            ORDER BY created_at DESC
                        """, (user_id,))
                    else:
                        cursor.execute("""
                            SELECT title, message, notification_type, created_at
                            FROM highland_notifications
                            WHERE target_user IS NULL
                            AND NOT is_read
                            AND (expires_at IS NULL OR expires_at > NOW())
                            ORDER BY created_at DESC
                        """)
                    
                    return cursor.fetchall()
            return []
        except Exception as e:
            logging.error(f"Notifications retrieval error: {e}")
            return []

def initialize_highland_real_time_data():
    """Initialize Highland Tower with sample real-time data"""
    sync = RealTimeDataSync()
    
    # Sample activities
    activities = [
        ("RFIs", "created", "john.smith", {"rfi_id": "RFI-2024-045", "priority": "High"}),
        ("Cost Management", "updated", "sarah.johnson", {"phase": "Structure", "amount": 125000}),
        ("Safety", "inspection", "mike.wilson", {"area": "Foundation", "score": 98}),
        ("Daily Reports", "submitted", "carlos.rodriguez", {"crew_count": 24, "hours": 192}),
        ("Progress Photos", "uploaded", "lisa.chen", {"location": "Floor 3", "count": 15})
    ]
    
    for module, action, user, details in activities:
        sync.log_activity(module, action, user, details)
    
    # Sample metrics
    metrics = [
        ("project_progress", 72.5, "%", "progress"),
        ("budget_utilization", 68.2, "%", "financial"),
        ("safety_score", 97.8, "points", "safety"),
        ("crew_productivity", 105.3, "%", "operations"),
        ("rfi_response_time", 2.4, "days", "documentation")
    ]
    
    for name, value, unit, category in metrics:
        sync.update_metric(name, value, unit, category)
    
    # Sample notifications
    notifications = [
        ("RFI Response Overdue", "RFI-2024-043 response is 2 days overdue", "warning"),
        ("Safety Milestone", "Achieved 100 days without incidents", "success"),
        ("Budget Alert", "Structure phase approaching 90% budget utilization", "info"),
        ("Weather Alert", "Heavy rain forecasted for tomorrow - review outdoor activities", "warning")
    ]
    
    for title, message, notification_type in notifications:
        sync.create_notification(title, message, notification_type)
    
    return sync

@st.cache_resource
def get_real_time_sync():
    """Get or create real-time sync instance"""
    return initialize_highland_real_time_data()

def render_live_activity_feed():
    """Render live activity feed widget"""
    sync = get_real_time_sync()
    
    st.markdown("### 🔄 Live Activity Feed")
    
    activities = sync.get_recent_activities(10)
    
    if activities:
        for activity in activities:
            timestamp = activity['timestamp'].strftime("%H:%M")
            details = activity.get('details', {})
            
            with st.container():
                col1, col2, col3 = st.columns([2, 6, 2])
                
                with col1:
                    st.caption(timestamp)
                
                with col2:
                    st.write(f"**{activity['module']}** - {activity['action']} by {activity['user_id']}")
                    if details:
                        st.caption(f"Details: {json.dumps(details, indent=2)}")
                
                with col3:
                    if activity['module'] == "Safety":
                        st.success("🛡️")
                    elif activity['module'] == "RFIs":
                        st.info("📋")
                    elif activity['module'] == "Cost Management":
                        st.warning("💰")
                    else:
                        st.info("📊")
    else:
        st.info("No recent activities")

def render_live_metrics_dashboard():
    """Render live metrics dashboard"""
    sync = get_real_time_sync()
    
    st.markdown("### 📊 Live Metrics")
    
    metrics = sync.get_live_metrics()
    
    if metrics:
        col1, col2, col3, col4 = st.columns(4)
        
        metric_items = list(metrics.items())
        
        for i, (name, data) in enumerate(metric_items[:4]):
            with [col1, col2, col3, col4][i]:
                st.metric(
                    label=name.replace('_', ' ').title(),
                    value=f"{data['value']:.1f}{data['unit']}",
                    delta=f"Updated: {data['timestamp'].strftime('%H:%M')}"
                )
    else:
        st.info("No live metrics available")

def render_notifications_panel():
    """Render notifications panel"""
    sync = get_real_time_sync()
    
    notifications = sync.get_active_notifications()
    
    if notifications:
        st.markdown("### 🔔 Active Notifications")
        
        for notification in notifications:
            notification_type = notification['notification_type']
            
            if notification_type == "warning":
                st.warning(f"**{notification['title']}** - {notification['message']}")
            elif notification_type == "success":
                st.success(f"**{notification['title']}** - {notification['message']}")
            elif notification_type == "error":
                st.error(f"**{notification['title']}** - {notification['message']}")
            else:
                st.info(f"**{notification['title']}** - {notification['message']}")
    
    return len(notifications) if notifications else 0