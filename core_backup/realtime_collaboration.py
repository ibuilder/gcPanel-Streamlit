"""
Real-time Collaboration System for Highland Tower Development
Live notifications, team messaging, and activity feeds
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import uuid
import json

def initialize_collaboration_system():
    """Initialize real-time collaboration features"""
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    
    if 'team_messages' not in st.session_state:
        st.session_state.team_messages = []
    
    if 'activity_feed' not in st.session_state:
        st.session_state.activity_feed = []
    
    if 'online_users' not in st.session_state:
        st.session_state.online_users = [
            {"name": "Jennifer Walsh", "role": "Project Manager", "status": "online", "last_seen": "now"},
            {"name": "Sarah Chen, PE", "role": "Structural Engineer", "status": "online", "last_seen": "2 min ago"},
            {"name": "Mike Rodriguez", "role": "Site Supervisor", "status": "away", "last_seen": "15 min ago"},
            {"name": "David Kim", "role": "MEP Engineer", "status": "online", "last_seen": "now"},
            {"name": "Lisa Wong", "role": "Safety Manager", "status": "online", "last_seen": "5 min ago"}
        ]

def render_notification_center():
    """Render real-time notification center"""
    st.markdown("### 🔔 Live Notifications")
    
    # Notification summary
    notifications = st.session_state.get('notifications', [])
    unread_count = len([n for n in notifications if not n.get('read', False)])
    
    if unread_count > 0:
        st.error(f"🔴 {unread_count} unread notifications")
    else:
        st.success("✅ All notifications read")
    
    # Add sample real-time notifications
    if st.button("🔄 Refresh Notifications"):
        add_sample_notifications()
        st.rerun()
    
    # Display notifications
    if notifications:
        for notification in notifications[-10:]:  # Show last 10
            render_notification_item(notification)
    else:
        st.info("No notifications yet")

def render_notification_item(notification):
    """Render individual notification item"""
    priority_colors = {
        'critical': '🔴',
        'high': '🟠', 
        'medium': '🟡',
        'low': '🟢'
    }
    
    priority_icon = priority_colors.get(notification.get('priority', 'medium'), '🟡')
    read_status = "✓" if notification.get('read') else "●"
    
    with st.expander(f"{priority_icon} {read_status} {notification.get('title', 'Notification')} - {notification.get('time', 'now')}"):
        st.markdown(f"**From:** {notification.get('from', 'System')}")
        st.markdown(f"**Type:** {notification.get('type', 'Update')}")
        st.markdown(f"**Message:** {notification.get('message', '')}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓ Mark Read", key=f"read_{notification.get('id')}"):
                notification['read'] = True
                st.rerun()
        
        with col2:
            if st.button("↗️ View Details", key=f"details_{notification.get('id')}"):
                st.info("Opening detailed view...")

def render_team_chat():
    """Render integrated team messaging"""
    st.markdown("### 💬 Highland Tower Team Chat")
    
    # Online team members
    st.markdown("#### 👥 Online Team Members")
    online_users = st.session_state.get('online_users', [])
    
    cols = st.columns(len(online_users))
    for i, user in enumerate(online_users):
        with cols[i]:
            status_icon = "🟢" if user['status'] == 'online' else "🟡" if user['status'] == 'away' else "⚫"
            st.markdown(f"{status_icon} **{user['name']}**")
            st.caption(f"{user['role']}")
            st.caption(f"Last seen: {user['last_seen']}")
    
    # Message input
    st.markdown("#### 📝 Send Message")
    
    with st.form("team_message"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            message_text = st.text_area("Message", placeholder="Type your message to the Highland Tower team...", height=100)
        
        with col2:
            message_type = st.selectbox("Type", ["General", "Urgent", "Question", "Update"])
            mention_user = st.selectbox("@Mention", ["None"] + [user['name'] for user in online_users])
            attach_file = st.file_uploader("Attach", type=['pdf', 'jpg', 'png', 'docx'])
        
        if st.form_submit_button("📤 Send Message", type="primary"):
            if message_text.strip():
                send_team_message(message_text, message_type, mention_user, attach_file)
                st.success("✅ Message sent to Highland Tower team!")
                st.rerun()
            else:
                st.error("Please enter a message")
    
    # Recent messages
    st.markdown("#### 💬 Recent Team Messages")
    
    messages = st.session_state.get('team_messages', [])
    if messages:
        for message in messages[-5:]:  # Show last 5 messages
            render_message_item(message)
    else:
        st.info("No messages yet - start the conversation!")

def render_message_item(message):
    """Render individual chat message"""
    timestamp = message.get('timestamp', datetime.now())
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)
    
    time_str = timestamp.strftime("%H:%M")
    
    with st.container():
        st.markdown(f"""
        <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; margin: 8px 0; background: white;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <strong>{message.get('from', 'Unknown')}</strong>
                <small style="color: #6b7280;">{time_str}</small>
            </div>
            <div style="margin-bottom: 8px;">
                <span style="background: #eff6ff; color: #1e40af; padding: 2px 8px; border-radius: 12px; font-size: 12px;">
                    {message.get('type', 'General')}
                </span>
            </div>
            <div>{message.get('text', '')}</div>
        </div>
        """, unsafe_allow_html=True)

def render_activity_feed():
    """Render real-time activity feed"""
    st.markdown("### 📊 Live Activity Feed")
    st.caption("Real-time updates from across Highland Tower Development")
    
    # Activity feed controls
    col1, col2 = st.columns(2)
    with col1:
        auto_refresh = st.checkbox("🔄 Auto-refresh", value=True)
    with col2:
        if st.button("↻ Refresh Now"):
            add_sample_activities()
            st.rerun()
    
    # Filter options
    activity_filter = st.selectbox("Filter Activities", [
        "All Activities", "RFI Updates", "Document Changes", "Safety Reports", 
        "Progress Updates", "Team Actions"
    ])
    
    # Activity feed
    activities = st.session_state.get('activity_feed', [])
    
    if activities:
        for activity in activities[-15:]:  # Show last 15 activities
            render_activity_item(activity)
    else:
        st.info("No recent activities")

def render_activity_item(activity):
    """Render individual activity item"""
    activity_icons = {
        'rfi': '📝',
        'document': '📄',
        'safety': '🚨',
        'progress': '📊',
        'team': '👥',
        'system': '⚙️'
    }
    
    icon = activity_icons.get(activity.get('type', 'system'), '📋')
    timestamp = activity.get('timestamp', datetime.now())
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)
    
    time_ago = get_time_ago(timestamp)
    
    st.markdown(f"""
    <div style="border-left: 3px solid #3b82f6; padding: 8px 12px; margin: 4px 0; background: #f8fafc;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 16px;">{icon}</span>
            <strong>{activity.get('user', 'System')}</strong>
            <span>{activity.get('action', 'performed an action')}</span>
            <small style="color: #6b7280; margin-left: auto;">{time_ago}</small>
        </div>
        <div style="margin-top: 4px; color: #4b5563;">
            {activity.get('description', '')}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_document_collaboration():
    """Render real-time document collaboration tools"""
    st.markdown("### 📄 Document Collaboration")
    
    # Active document sessions
    st.markdown("#### 👥 Active Document Sessions")
    
    active_sessions = [
        {
            "document": "Foundation_Plan_Rev3.dwg",
            "users": ["Sarah Chen, PE", "Jennifer Walsh"],
            "status": "🟢 Live editing",
            "last_update": "2 minutes ago"
        },
        {
            "document": "Steel_Connection_Details.pdf", 
            "users": ["David Kim"],
            "status": "🟡 Viewing",
            "last_update": "5 minutes ago"
        }
    ]
    
    for session in active_sessions:
        with st.expander(f"📄 {session['document']} - {session['status']}"):
            st.markdown(f"**Active Users:** {', '.join(session['users'])}")
            st.markdown(f"**Status:** {session['status']}")
            st.markdown(f"**Last Update:** {session['last_update']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔗 Join Session", key=f"join_{session['document']}"):
                    st.success("Joining collaborative session...")
            with col2:
                if st.button("💬 Chat", key=f"chat_{session['document']}"):
                    st.info("Opening document chat...")

def send_team_message(text, msg_type, mention_user, attach_file):
    """Send message to team chat"""
    message = {
        'id': str(uuid.uuid4()),
        'from': st.session_state.get('username', 'Current User'),
        'text': text,
        'type': msg_type,
        'mention': mention_user if mention_user != "None" else None,
        'attachment': attach_file.name if attach_file else None,
        'timestamp': datetime.now().isoformat()
    }
    
    st.session_state.team_messages.append(message)
    
    # Create notification for mentioned user
    if mention_user and mention_user != "None":
        create_notification(
            title=f"You were mentioned in team chat",
            message=f"{message['from']} mentioned you: {text[:50]}...",
            type='mention',
            priority='medium',
            from_user=message['from']
        )

def create_notification(title, message, type='info', priority='medium', from_user='System'):
    """Create new notification"""
    notification = {
        'id': str(uuid.uuid4()),
        'title': title,
        'message': message,
        'type': type,
        'priority': priority,
        'from': from_user,
        'time': datetime.now().strftime('%H:%M'),
        'timestamp': datetime.now().isoformat(),
        'read': False
    }
    
    st.session_state.notifications.append(notification)

def add_sample_notifications():
    """Add sample real-time notifications"""
    sample_notifications = [
        {
            'title': 'RFI Response Received',
            'message': 'HTD-RFI-001 (Foundation reinforcement) has been answered by Sarah Chen, PE',
            'type': 'rfi_response',
            'priority': 'high',
            'from': 'Sarah Chen, PE'
        },
        {
            'title': 'Safety Alert',
            'message': 'Weather advisory: High winds expected this afternoon, secure loose materials',
            'type': 'safety',
            'priority': 'critical',
            'from': 'Lisa Wong'
        },
        {
            'title': 'Document Updated',
            'message': 'Foundation_Plan_Rev3.dwg has been updated with latest revisions',
            'type': 'document',
            'priority': 'medium',
            'from': 'Highland Structural'
        }
    ]
    
    for notif in sample_notifications:
        create_notification(**notif)

def add_sample_activities():
    """Add sample activity feed entries"""
    sample_activities = [
        {
            'user': 'Sarah Chen, PE',
            'action': 'responded to RFI',
            'description': 'HTD-RFI-001: Foundation reinforcement details - Level B2',
            'type': 'rfi',
            'timestamp': datetime.now() - timedelta(minutes=5)
        },
        {
            'user': 'Mike Rodriguez',
            'action': 'uploaded progress photos',
            'description': 'Level 8 structural progress - 12 photos uploaded',
            'type': 'progress',
            'timestamp': datetime.now() - timedelta(minutes=12)
        },
        {
            'user': 'David Kim',
            'action': 'updated drawing',
            'description': 'MEP_Plan_Level8.dwg - Revised ductwork routing',
            'type': 'document',
            'timestamp': datetime.now() - timedelta(minutes=18)
        },
        {
            'user': 'Lisa Wong',
            'action': 'completed safety inspection',
            'description': 'Weekly safety walkthrough - All areas passed',
            'type': 'safety',
            'timestamp': datetime.now() - timedelta(minutes=25)
        }
    ]
    
    for activity in sample_activities:
        st.session_state.activity_feed.append(activity)

def get_time_ago(timestamp):
    """Get human-readable time ago string"""
    now = datetime.now()
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)
    
    diff = now - timestamp
    
    if diff.seconds < 60:
        return "just now"
    elif diff.seconds < 3600:
        minutes = diff.seconds // 60
        return f"{minutes} min ago"
    elif diff.seconds < 86400:
        hours = diff.seconds // 3600
        return f"{hours}h ago"
    else:
        days = diff.days
        return f"{days}d ago"

def render_mentions_and_alerts():
    """Render @mentions and urgent alerts system"""
    st.markdown("### 📢 Mentions & Alerts")
    
    # Urgent alerts
    urgent_alerts = [
        {
            'type': 'weather',
            'message': 'High wind warning - Secure all materials and equipment',
            'priority': 'critical',
            'time': '10 minutes ago'
        },
        {
            'type': 'safety',
            'message': 'Safety inspection required - Level 9 before concrete pour',
            'priority': 'high', 
            'time': '25 minutes ago'
        }
    ]
    
    if urgent_alerts:
        st.error("🚨 Urgent Alerts")
        for alert in urgent_alerts:
            st.markdown(f"⚠️ **{alert['message']}** ({alert['time']})")
    
    # @Mentions
    mentions = [
        {
            'from': 'Jennifer Walsh',
            'message': '@current_user Please review the structural calculations for Level 9',
            'context': 'RFI HTD-RFI-003',
            'time': '15 minutes ago'
        }
    ]
    
    if mentions:
        st.warning("📣 You were mentioned")
        for mention in mentions:
            with st.expander(f"💬 {mention['from']} mentioned you - {mention['time']}"):
                st.markdown(f"**Message:** {mention['message']}")
                st.markdown(f"**Context:** {mention['context']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💬 Reply", key=f"reply_{mention['time']}"):
                        st.info("Opening reply interface...")
                with col2:
                    if st.button("✓ Mark Read", key=f"mark_read_{mention['time']}"):
                        st.success("Mention marked as read")

if __name__ == "__main__":
    initialize_collaboration_system()
    render_notification_center()