"""
Notification Center Component for gcPanel Construction Management Dashboard.

This module provides UI components for displaying and managing notifications
within the application.
"""

import streamlit as st
import datetime
from utils.notifications import get_user_notifications, mark_notification_as_read

def notification_center():
    """
    Display a notification center in the UI
    
    This component allows users to view and manage their notifications.
    It supports filtering, marking as read, and taking action on notifications.
    """
    # Add custom styling for the notification center
    st.markdown("""
    <div class="notification-center-container">
        <div class="notification-center-header">
            <h2><i class="material-icons" style="vertical-align: middle; margin-right: 10px;">notifications</i> Notifications</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Get the current user ID from session state
    user_id = st.session_state.get("user_id", "current_user")
    
    # Notification filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        notification_type = st.selectbox(
            "Type",
            ["All", "Delivery", "General", "Task", "Schedule", "Document"],
            key="notification_type_filter"
        )
    
    with col2:
        time_filter = st.selectbox(
            "Time Frame",
            ["Today", "Last 7 Days", "Last 30 Days", "All"],
            key="notification_time_filter"
        )
    
    with col3:
        include_read = st.checkbox("Include Read", False, key="include_read_notifications")
    
    # Get user notifications
    notifications = get_user_notifications(user_id, limit=50, include_read=include_read)
    
    # Apply filters
    filtered_notifications = []
    for notification in notifications:
        # Apply type filter
        if notification_type != "All":
            notification_type_value = notification.get("type", "")
            if notification_type.lower() not in notification_type_value.lower():
                continue
        
        # Apply time filter
        if time_filter != "All":
            notification_time = notification.get("timestamp", "")
            if notification_time:
                try:
                    timestamp = datetime.datetime.fromisoformat(notification_time)
                    now = datetime.datetime.now()
                    
                    if time_filter == "Today" and timestamp.date() != now.date():
                        continue
                    elif time_filter == "Last 7 Days" and (now - timestamp).days > 7:
                        continue
                    elif time_filter == "Last 30 Days" and (now - timestamp).days > 30:
                        continue
                except ValueError:
                    # Skip this filter if timestamp is invalid
                    pass
        
        filtered_notifications.append(notification)
    
    # Display notifications
    if not filtered_notifications:
        st.markdown("""
        <div class="notification-empty">
            <i class="material-icons" style="font-size: 48px; color: #e0e0e0; display: block; margin-bottom: 10px;">notifications_none</i>
            <p>No notifications found matching your filters.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Option to mark all as read
        col_actions_1, col_actions_2 = st.columns([1, 4])
        
        with col_actions_1:
            if st.button("Mark All as Read", key="mark_all_read_btn"):
                for notification in filtered_notifications:
                    notification_id = notification.get("id", "")
                    if notification_id:
                        mark_notification_as_read(notification_id)
                st.success("All notifications marked as read.")
                st.rerun()
        
        # Display notifications
        st.markdown('<div class="notification-list">', unsafe_allow_html=True)
        for notification in filtered_notifications:
            render_notification(notification)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Close the notification center container
    st.markdown('</div>', unsafe_allow_html=True)

def render_notification(notification):
    """
    Render a single notification
    
    Args:
        notification (dict): The notification data to render
    """
    # Extract notification data
    subject = notification.get("subject", "Notification")
    message = notification.get("message", "")
    timestamp = notification.get("timestamp", "")
    priority = notification.get("priority", "normal")
    notification_type = notification.get("type", "general_announcement")
    read = notification.get("read", False)
    metadata = notification.get("metadata", {})
    
    # Format the timestamp
    formatted_time = ""
    if timestamp:
        try:
            dt = datetime.datetime.fromisoformat(timestamp)
            now = datetime.datetime.now()
            
            if dt.date() == now.date():
                formatted_time = f"Today at {dt.strftime('%I:%M %p')}"
            elif dt.date() == (now - datetime.timedelta(days=1)).date():
                formatted_time = f"Yesterday at {dt.strftime('%I:%M %p')}"
            else:
                formatted_time = dt.strftime("%b %d, %Y at %I:%M %p")
        except ValueError:
            formatted_time = timestamp
    
    # Set style based on priority and read status
    priority_class = "normal"
    
    if priority == "high":
        priority_class = "high"
    elif priority == "critical":
        priority_class = "critical"
    
    read_class = "" if read else "unread"
    
    # Get icon based on notification type
    icon_name = "notifications"  # Default bell icon
    
    if "delivery" in notification_type:
        icon_name = "local_shipping"
    elif "document" in notification_type:
        icon_name = "description"
    elif "task" in notification_type:
        icon_name = "task_alt"
    elif "schedule" in notification_type:
        icon_name = "event"
    
    # Render the notification with our new CSS classes
    st.markdown(f"""
        <div class="notification-item {read_class} priority-{priority_class}">
            <div class="notification-item-header">
                <div class="notification-item-title">
                    <i class="material-icons">{icon_name}</i> {subject}
                </div>
                <div class="notification-item-time">{formatted_time}</div>
            </div>
            <div class="notification-item-body">
                {message}
            </div>
            <div class="notification-item-footer">
                <div class="notification-item-type">{notification_type.replace('_', ' ').title()}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        if not read:
            if st.button("Mark as Read", key=f"read_{notification.get('id', id(notification))}"):
                mark_notification_as_read(notification.get("id", ""))
                st.success("Notification marked as read.")
                st.rerun()
    
    with col2:
        # Add relevant action button based on notification type
        if "delivery" in notification_type and metadata.get("id"):
            st.button("View Delivery", key=f"view_{notification.get('id', id(notification))}")

def notification_indicator():
    """
    Display a notification indicator in the header
    
    This component shows a badge with the number of unread notifications
    and provides a dropdown to view recent notifications.
    """
    # Get the current user ID from session state
    user_id = st.session_state.get("user_id", "current_user")
    
    # Get unread notifications count
    notifications = get_user_notifications(user_id, limit=10, include_read=False)
    unread_count = len(notifications)
    
    # Create the indicator
    if unread_count > 0:
        st.markdown(f"""
            <div style="position: relative; display: inline-block;">
                <button class="stButton notification-btn">
                    <span>🔔</span>
                    <span style="position: absolute; top: -5px; right: -5px; background-color: #dc3545; color: white; 
                    border-radius: 50%; width: 20px; height: 20px; font-size: 12px; display: flex; 
                    justify-content: center; align-items: center;">{unread_count}</span>
                </button>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="position: relative; display: inline-block;">
                <button class="stButton notification-btn">
                    <span>🔔</span>
                </button>
            </div>
        """, unsafe_allow_html=True)
    
    # Display mini notification dropdown
    with st.expander("", expanded=False):
        if unread_count > 0:
            for notification in notifications[:5]:  # Show up to 5 recent notifications
                subject = notification.get("subject", "Notification")
                timestamp = notification.get("timestamp", "")
                
                # Format the timestamp
                formatted_time = ""
                if timestamp:
                    try:
                        dt = datetime.datetime.fromisoformat(timestamp)
                        now = datetime.datetime.now()
                        
                        delta = now - dt
                        if delta.days == 0:
                            if delta.seconds < 60:
                                formatted_time = "Just now"
                            elif delta.seconds < 3600:
                                formatted_time = f"{delta.seconds // 60}m ago"
                            else:
                                formatted_time = f"{delta.seconds // 3600}h ago"
                        elif delta.days == 1:
                            formatted_time = "Yesterday"
                        else:
                            formatted_time = f"{delta.days}d ago"
                    except ValueError:
                        formatted_time = timestamp
                
                st.markdown(f"**{subject}** - {formatted_time}")
            
            if st.button("View All Notifications"):
                st.session_state.show_notification_center = True
        else:
            st.markdown("No new notifications")