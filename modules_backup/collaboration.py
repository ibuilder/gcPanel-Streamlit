"""
Real-time Collaboration Module for gcPanel.

This module provides real-time collaboration features including:
- Team chat functionality
- Document collaboration with comments
- Activity feed
- Task assignment and tracking
- Notification system for updates
"""

import streamlit as st
import time
from datetime import datetime, timedelta
import json
import uuid
import pandas as pd
import random

# Sample data for demonstration purposes
# In production, this would be replaced with database calls
def get_sample_users():
    """Get sample user data for demonstration."""
    return [
        {"id": "user_1", "name": "John Smith", "role": "Project Manager", "avatar": "👷‍♂️", "company": "GC Prime Contractors"},
        {"id": "user_2", "name": "Sarah Johnson", "role": "Architect", "avatar": "👩‍💼", "company": "Design Partners"},
        {"id": "user_3", "name": "Michael Chen", "role": "Structural Engineer", "avatar": "👨‍💻", "company": "Structure Solutions"},
        {"id": "user_4", "name": "Lisa Rodriguez", "role": "Foreman", "avatar": "👷‍♀️", "company": "GC Prime Contractors"},
        {"id": "user_5", "name": "Robert Williams", "role": "Electrical Contractor", "avatar": "👨‍🔧", "company": "Power Systems Inc."},
        {"id": "user_6", "name": "Jessica Taylor", "role": "Owner Representative", "avatar": "👩‍💼", "company": "Highland Development LLC"},
    ]

def initialize_collaboration_state():
    """Initialize session state for collaboration features."""
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"id": "msg_1", "user_id": "user_2", "timestamp": (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"), 
             "content": "I've updated the lobby design with the new material selections. Please review when you get a chance.", "channel": "general"},
            {"id": "msg_2", "user_id": "user_4", "timestamp": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"), 
             "content": "Foundation inspection is scheduled for tomorrow at 9 AM. We need to have all site prep completed by end of day.", "channel": "general"},
            {"id": "msg_3", "user_id": "user_3", "timestamp": (datetime.now() - timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M"), 
             "content": "Updated structural calculations for the cantilevered section have been uploaded to the documents section.", "channel": "general"},
            {"id": "msg_4", "user_id": "user_5", "timestamp": (datetime.now() - timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M"), 
             "content": "Need clarification on the electrical panel location in the east wing. Can someone from design team confirm?", "channel": "general"},
        ]
    
    if "document_comments" not in st.session_state:
        st.session_state.document_comments = [
            {"id": "comment_1", "document_id": "doc_101", "user_id": "user_2", "timestamp": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
             "content": "Please note the change in ceiling height from 10' to 9'6\" on level 3.", "page": 4, "position": {"x": 120, "y": 350}},
            {"id": "comment_2", "document_id": "doc_101", "user_id": "user_3", "timestamp": (datetime.now() - timedelta(hours=8)).strftime("%Y-%m-%d %H:%M"),
             "content": "The support column dimensions need to be updated to match structural calculations.", "page": 2, "position": {"x": 250, "y": 180}},
            {"id": "comment_3", "document_id": "doc_102", "user_id": "user_5", "timestamp": (datetime.now() - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M"),
             "content": "Electrical conduit routing needs to be adjusted to avoid conflict with HVAC.", "page": 7, "position": {"x": 300, "y": 210}},
        ]
    
    if "activity_feed" not in st.session_state:
        st.session_state.activity_feed = [
            {"id": "act_1", "user_id": "user_1", "timestamp": (datetime.now() - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M"),
             "action": "updated", "item_type": "RFI", "item_id": "RFI-042", "item_name": "Column Foundation Detail"},
            {"id": "act_2", "user_id": "user_2", "timestamp": (datetime.now() - timedelta(hours=3, minutes=30)).strftime("%Y-%m-%d %H:%M"),
             "action": "uploaded", "item_type": "document", "item_id": "doc_103", "item_name": "Revised Lobby Elevations"},
            {"id": "act_3", "user_id": "user_4", "timestamp": (datetime.now() - timedelta(hours=2, minutes=15)).strftime("%Y-%m-%d %H:%M"),
             "action": "completed", "item_type": "task", "item_id": "task_85", "item_name": "Site Preparation for Foundation"},
            {"id": "act_4", "user_id": "user_3", "timestamp": (datetime.now() - timedelta(hours=1, minutes=10)).strftime("%Y-%m-%d %H:%M"),
             "action": "commented on", "item_type": "submittal", "item_id": "SUB-028", "item_name": "Structural Steel Specifications"},
            {"id": "act_5", "user_id": "user_5", "timestamp": (datetime.now() - timedelta(minutes=25)).strftime("%Y-%m-%d %H:%M"),
             "action": "created", "item_type": "issue", "item_id": "ISS-017", "item_name": "Electrical Conduit Routing Conflict"},
        ]
    
    if "tasks" not in st.session_state:
        st.session_state.tasks = [
            {"id": "task_84", "title": "Prepare Site for Foundation Work", "description": "Clear debris and mark layout for foundation pouring",
             "assigned_to": "user_4", "due_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"), "status": "In Progress", 
             "priority": "High", "project_area": "Site Work"},
            {"id": "task_85", "title": "Review Updated Lobby Design", "description": "Review and approve latest lobby design changes",
             "assigned_to": "user_1", "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"), "status": "Not Started", 
             "priority": "Medium", "project_area": "Design"},
            {"id": "task_86", "title": "Resolve Electrical-HVAC Conflict", "description": "Coordinate with teams to resolve routing conflict",
             "assigned_to": "user_5", "due_date": (datetime.now() + timedelta(hours=36)).strftime("%Y-%m-%d"), "status": "Not Started", 
             "priority": "High", "project_area": "MEP"},
            {"id": "task_87", "title": "Update Structural Calculations", "description": "Review and update calculations for cantilevered section",
             "assigned_to": "user_3", "due_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"), "status": "Complete", 
             "priority": "Medium", "project_area": "Structural"},
            {"id": "task_88", "title": "Schedule Final Design Review", "description": "Set up meeting with design team and owner for final review",
             "assigned_to": "user_2", "due_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"), "status": "Not Started", 
             "priority": "Low", "project_area": "Coordination"},
        ]
    
    if "notifications" not in st.session_state:
        st.session_state.notifications = [
            {"id": "notif_1", "user_id": "user_1", "timestamp": (datetime.now() - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M"),
             "content": "Sarah Johnson mentioned you in a comment", "read": False, "link": "doc_101"},
            {"id": "notif_2", "user_id": "user_1", "timestamp": (datetime.now() - timedelta(hours=1, minutes=15)).strftime("%Y-%m-%d %H:%M"),
             "content": "New RFI assigned to you: Window Detail Clarification", "read": False, "link": "rfi_043"},
            {"id": "notif_3", "user_id": "user_1", "timestamp": (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
             "content": "Task deadline approaching: Review Updated Lobby Design", "read": True, "link": "task_85"},
        ]
    
    if "active_users" not in st.session_state:
        st.session_state.active_users = ["user_1", "user_2", "user_4", "user_5"]
    
    if "chat_channels" not in st.session_state:
        st.session_state.chat_channels = [
            {"id": "general", "name": "General", "description": "Project-wide announcements and discussions"},
            {"id": "design", "name": "Design Team", "description": "Design coordination and issues"},
            {"id": "field", "name": "Field Operations", "description": "On-site construction activities"},
            {"id": "mep", "name": "MEP Coordination", "description": "Mechanical, electrical, and plumbing coordination"}
        ]

def render_collaboration_hub():
    """Render the main collaboration hub interface."""
    st.title("Team Collaboration Hub")
    
    # Initialize collaboration state
    initialize_collaboration_state()
    
    # Get user data
    users = get_sample_users()
    user_map = {user["id"]: user for user in users}
    
    # Set up the tab structure
    tabs = st.tabs(["Activity Feed", "Team Chat", "Task Board", "Document Collaboration"])
    
    # ACTIVITY FEED TAB
    with tabs[0]:
        render_activity_feed(user_map)
    
    # TEAM CHAT TAB
    with tabs[1]:
        render_team_chat(user_map)
    
    # TASK BOARD TAB
    with tabs[2]:
        render_task_board(user_map)
    
    # DOCUMENT COLLABORATION TAB
    with tabs[3]:
        render_document_collaboration(user_map)

def render_activity_feed(user_map):
    """Render activity feed showing recent project activities."""
    st.subheader("Project Activity Feed")
    
    # Activity filters
    col1, col2 = st.columns([2, 1])
    with col1:
        filter_type = st.multiselect("Filter by type:", 
                                    ["All", "Document", "RFI", "Submittal", "Task", "Issue"], 
                                    default=["All"])
    with col2:
        time_filter = st.selectbox("Time period:", 
                                ["Last 24 hours", "Last 7 days", "Last 30 days", "All time"])
    
    # Get filtered activities
    activities = st.session_state.activity_feed
    
    # Apply filters
    if "All" not in filter_type:
        activities = [act for act in activities if act["item_type"].lower() in [t.lower() for t in filter_type]]
    
    # Render activity feed entries
    st.markdown("---")
    for activity in activities:
        user = user_map.get(activity["user_id"], {"name": "Unknown User", "avatar": "👤"})
        
        # Format the activity message
        activity_msg = f"{user['avatar']} **{user['name']}** {activity['action']} {activity['item_type']} " \
                      f"[{activity['item_name']}]({activity['item_id']}) - {activity['timestamp']}"
        
        st.markdown(activity_msg)
        st.markdown("---")
    
    # Add "Load More" button at the bottom
    if st.button("Load More Activities"):
        st.info("Loading additional activities would fetch older entries from database in production.")

def render_team_chat(user_map):
    """Render team chat interface."""
    st.subheader("Team Chat")
    
    # Chat interface layout
    col1, col2 = st.columns([1, 3])
    
    # Channel list in sidebar
    with col1:
        st.markdown("### Channels")
        
        # Display channels
        selected_channel = None
        for channel in st.session_state.chat_channels:
            if st.button(f"# {channel['name']}", key=f"channel_{channel['id']}"):
                st.session_state.selected_channel = channel["id"]
                selected_channel = channel["id"]
        
        # Show active users
        st.markdown("### Active Now")
        for user_id in st.session_state.active_users:
            user = user_map.get(user_id, {"name": "Unknown", "avatar": "👤"})
            st.markdown(f"{user['avatar']} {user['name']} 🟢")
    
    # Get the currently selected channel
    if "selected_channel" not in st.session_state:
        st.session_state.selected_channel = "general"
    
    selected_channel = st.session_state.selected_channel
    
    # Find the channel info
    channel_info = next((c for c in st.session_state.chat_channels if c["id"] == selected_channel), None)
    
    # Chat window
    with col2:
        if channel_info:
            st.markdown(f"### #{channel_info['name']}")
            st.caption(channel_info['description'])
            
            # Show messages for this channel
            chat_messages = [msg for msg in st.session_state.chat_messages if msg["channel"] == selected_channel]
            
            # Create a bordered chat container with fixed height
            st.markdown("""
            <style>
            .chat-container {
                border: 1px solid #ddd;
                border-radius: 8px;
                height: 400px;
                overflow-y: auto;
                padding: 1rem;
                background-color: #f9f9f9;
                margin-bottom: 1rem;
            }
            .message {
                margin-bottom: 1rem;
                padding: 0.5rem;
                border-radius: 8px;
            }
            .message-mine {
                background-color: #e3f2fd;
                margin-left: 2rem;
                margin-right: 0;
            }
            .message-other {
                background-color: #f0f0f0;
                margin-left: 0;
                margin-right: 2rem;
            }
            </style>
            <div class="chat-container">
            """, unsafe_allow_html=True)
            
            # Display chat messages
            for msg in chat_messages:
                user = user_map.get(msg["user_id"], {"name": "Unknown User", "avatar": "👤"})
                
                # Check if this is the current user's message
                is_mine = msg["user_id"] == "user_1"  # Assuming current user is user_1
                message_class = "message-mine" if is_mine else "message-other"
                
                st.markdown(f"""
                <div class="message {message_class}">
                    <strong>{user['avatar']} {user['name']}</strong> <small>{msg['timestamp']}</small><br>
                    {msg['content']}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Message input
            with st.form(key="message_form"):
                new_message = st.text_area("Message", placeholder="Type your message here...")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text("")  # Empty space
                with col2:
                    send_btn = st.form_submit_button("Send Message", use_container_width=True)
                
                if send_btn and new_message:
                    # Add the new message
                    new_msg = {
                        "id": f"msg_{uuid.uuid4().hex[:8]}",
                        "user_id": "user_1",  # Current user
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "content": new_message,
                        "channel": selected_channel
                    }
                    st.session_state.chat_messages.append(new_msg)
                    st.rerun()

def render_task_board(user_map):
    """Render task board with drag-and-drop functionality."""
    st.subheader("Task Board")
    
    # Task filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.multiselect("Status:", 
                                     ["Not Started", "In Progress", "Complete"], 
                                     default=["Not Started", "In Progress"])
    
    with col2:
        priority_filter = st.multiselect("Priority:", 
                                       ["Low", "Medium", "High"], 
                                       default=["Medium", "High"])
    
    with col3:
        assignee_filter = st.selectbox("Assigned to:", 
                                     ["All"] + [user["name"] for user in user_map.values()],
                                     index=0)
    
    # Create a grid layout for task columns
    col1, col2, col3 = st.columns(3)
    
    # Filter tasks
    tasks = st.session_state.tasks
    
    if status_filter:
        tasks = [task for task in tasks if task["status"] in status_filter]
    
    if priority_filter:
        tasks = [task for task in tasks if task["priority"] in priority_filter]
    
    if assignee_filter != "All":
        tasks = [task for task in tasks if user_map.get(task["assigned_to"], {"name": ""})["name"] == assignee_filter]
    
    # Group tasks by status
    not_started = [task for task in tasks if task["status"] == "Not Started"]
    in_progress = [task for task in tasks if task["status"] == "In Progress"]
    completed = [task for task in tasks if task["status"] == "Complete"]
    
    # Define common card style for tasks
    card_style = """
    <style>
    .task-card {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
        background-color: white;
    }
    .task-card-high {
        border-left: 5px solid #f44336;
    }
    .task-card-medium {
        border-left: 5px solid #ff9800;
    }
    .task-card-low {
        border-left: 5px solid #4caf50;
    }
    .task-card h4 {
        margin: 0 0 5px 0;
    }
    .task-status {
        display: inline-block;
        padding: 3px 6px;
        border-radius: 3px;
        font-size: 12px;
        font-weight: bold;
    }
    .status-not-started {
        background-color: #e0e0e0;
        color: #616161;
    }
    .status-in-progress {
        background-color: #bbdefb;
        color: #1976d2;
    }
    .status-complete {
        background-color: #c8e6c9;
        color: #388e3c;
    }
    </style>
    """
    
    st.markdown(card_style, unsafe_allow_html=True)
    
    # Not Started column
    with col1:
        st.markdown("### To Do")
        for task in not_started:
            with st.container():
                user = user_map.get(task["assigned_to"], {"name": "Unassigned", "avatar": "❓"})
                priority_class = f"task-card-{task['priority'].lower()}"
                
                task_html = f"""
                <div class="task-card {priority_class}">
                    <h4>{task['title']}</h4>
                    <p>{task['description']}</p>
                    <div>Assigned to: {user['avatar']} {user['name']}</div>
                    <div>Due: {task['due_date']}</div>
                    <div>Area: {task['project_area']}</div>
                    <div><span class="task-status status-not-started">Not Started</span></div>
                </div>
                """
                st.markdown(task_html, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Start", key=f"start_{task['id']}"):
                        # Update task status
                        for t in st.session_state.tasks:
                            if t["id"] == task["id"]:
                                t["status"] = "In Progress"
                        st.rerun()
                with col2:
                    if st.button("Edit", key=f"edit_{task['id']}"):
                        st.session_state.editing_task = task["id"]
    
    # In Progress column
    with col2:
        st.markdown("### In Progress")
        for task in in_progress:
            with st.container():
                user = user_map.get(task["assigned_to"], {"name": "Unassigned", "avatar": "❓"})
                priority_class = f"task-card-{task['priority'].lower()}"
                
                task_html = f"""
                <div class="task-card {priority_class}">
                    <h4>{task['title']}</h4>
                    <p>{task['description']}</p>
                    <div>Assigned to: {user['avatar']} {user['name']}</div>
                    <div>Due: {task['due_date']}</div>
                    <div>Area: {task['project_area']}</div>
                    <div><span class="task-status status-in-progress">In Progress</span></div>
                </div>
                """
                st.markdown(task_html, unsafe_allow_html=True)
                
                # Use containers instead of nested columns
                with st.container():
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("Complete", key=f"complete_{task['id']}"):
                            # Update task status
                            for t in st.session_state.tasks:
                                if t["id"] == task["id"]:
                                    t["status"] = "Complete"
                            st.rerun()
                    with btn_col2:
                        if st.button("Edit", key=f"edit_ip_{task['id']}"):
                            st.session_state.editing_task = task["id"]
    
    # Completed column
    with col3:
        st.markdown("### Completed")
        for task in completed:
            with st.container():
                user = user_map.get(task["assigned_to"], {"name": "Unassigned", "avatar": "❓"})
                priority_class = f"task-card-{task['priority'].lower()}"
                
                task_html = f"""
                <div class="task-card {priority_class}">
                    <h4>{task['title']}</h4>
                    <p>{task['description']}</p>
                    <div>Assigned to: {user['avatar']} {user['name']}</div>
                    <div>Due: {task['due_date']}</div>
                    <div>Area: {task['project_area']}</div>
                    <div><span class="task-status status-complete">Complete</span></div>
                </div>
                """
                st.markdown(task_html, unsafe_allow_html=True)
                
                if st.button("Reopen", key=f"reopen_{task['id']}"):
                    # Update task status
                    for t in st.session_state.tasks:
                        if t["id"] == task["id"]:
                            t["status"] = "In Progress"
                    st.rerun()
    
    # Create New Task button
    if st.button("➕ Create New Task", type="primary"):
        st.session_state.creating_new_task = True
    
    # Task edit modal
    if "editing_task" in st.session_state and st.session_state.editing_task:
        task_id = st.session_state.editing_task
        task = next((t for t in st.session_state.tasks if t["id"] == task_id), None)
        
        if task:
            st.markdown("### Edit Task")
            with st.form(key="edit_task_form"):
                title = st.text_input("Title", value=task["title"])
                description = st.text_area("Description", value=task["description"])
                col1, col2 = st.columns(2)
                with col1:
                    assigned_to = st.selectbox("Assigned To", 
                                            [user["name"] for user in user_map.values()],
                                            index=list(user_map.keys()).index(task["assigned_to"]))
                    priority = st.selectbox("Priority", ["Low", "Medium", "High"], 
                                          index=["Low", "Medium", "High"].index(task["priority"]))
                with col2:
                    status = st.selectbox("Status", ["Not Started", "In Progress", "Complete"],
                                        index=["Not Started", "In Progress", "Complete"].index(task["status"]))
                    due_date = st.date_input("Due Date", datetime.strptime(task["due_date"], "%Y-%m-%d"))
                
                project_area = st.text_input("Project Area", value=task["project_area"])
                
                col1, col2 = st.columns(2)
                with col1:
                    cancel = st.form_submit_button("Cancel")
                with col2:
                    update = st.form_submit_button("Update Task")
                
                if cancel:
                    st.session_state.editing_task = None
                    st.rerun()
                
                if update:
                    # Find user ID from name
                    assigned_user_id = next((u_id for u_id, u in user_map.items() if u["name"] == assigned_to), task["assigned_to"])
                    
                    # Update task
                    for t in st.session_state.tasks:
                        if t["id"] == task_id:
                            t["title"] = title
                            t["description"] = description
                            t["assigned_to"] = assigned_user_id
                            t["priority"] = priority
                            t["status"] = status
                            t["due_date"] = due_date.strftime("%Y-%m-%d")
                            t["project_area"] = project_area
                    
                    st.session_state.editing_task = None
                    st.success("Task updated!")
                    st.rerun()
    
    # New task creation modal
    if "creating_new_task" in st.session_state and st.session_state.creating_new_task:
        st.markdown("### Create New Task")
        with st.form(key="new_task_form"):
            title = st.text_input("Title", placeholder="Enter task title")
            description = st.text_area("Description", placeholder="Enter task description")
            col1, col2 = st.columns(2)
            with col1:
                assigned_to = st.selectbox("Assigned To", [user["name"] for user in user_map.values()])
                priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)  # Default to Medium
            with col2:
                status = st.selectbox("Status", ["Not Started", "In Progress", "Complete"], index=0)  # Default to Not Started
                due_date = st.date_input("Due Date", datetime.now() + timedelta(days=7))  # Default to 1 week from now
            
            project_area = st.text_input("Project Area", placeholder="e.g., Design, Structural, MEP")
            
            col1, col2 = st.columns(2)
            with col1:
                cancel = st.form_submit_button("Cancel")
            with col2:
                create = st.form_submit_button("Create Task")
            
            if cancel:
                st.session_state.creating_new_task = False
                st.rerun()
            
            if create:
                if not title:
                    st.error("Title is required")
                else:
                    # Find user ID from name
                    assigned_user_id = next((u_id for u_id, u in user_map.items() if u["name"] == assigned_to), "user_1")
                    
                    # Create new task
                    new_task = {
                        "id": f"task_{uuid.uuid4().hex[:3]}",
                        "title": title,
                        "description": description,
                        "assigned_to": assigned_user_id,
                        "priority": priority,
                        "status": status,
                        "due_date": due_date.strftime("%Y-%m-%d"),
                        "project_area": project_area
                    }
                    
                    st.session_state.tasks.append(new_task)
                    st.session_state.creating_new_task = False
                    st.success("Task created!")
                    st.rerun()

def render_document_collaboration(user_map):
    """Render document collaboration interface with annotation support."""
    st.subheader("Document Collaboration")
    
    # Document list and viewer
    col1, col2 = st.columns([1, 3])
    
    # Document list
    with col1:
        st.markdown("### Project Documents")
        
        # Create tabs for document categories
        doc_tabs = st.tabs(["Drawings", "Specs", "Submittals"])
        
        with doc_tabs[0]:
            if st.button("Floor Plans (A2.1)", key="doc_101"):
                st.session_state.selected_document = "doc_101"
            if st.button("Elevations (A3.1)", key="doc_102"):
                st.session_state.selected_document = "doc_102"
            if st.button("Structural Details (S2.3)", key="doc_103"):
                st.session_state.selected_document = "doc_103"
            
        with doc_tabs[1]:
            if st.button("Division 03 - Concrete", key="spec_01"):
                st.session_state.selected_document = "spec_01"
            if st.button("Division 08 - Openings", key="spec_02"):
                st.session_state.selected_document = "spec_02"
            
        with doc_tabs[2]:
            if st.button("Structural Steel", key="sub_01"):
                st.session_state.selected_document = "sub_01"
            if st.button("Curtain Wall System", key="sub_02"):
                st.session_state.selected_document = "sub_02"
    
    # Document viewer
    with col2:
        # Check if a document is selected
        if "selected_document" not in st.session_state:
            st.session_state.selected_document = "doc_101"  # Default
        
        # Get the document ID
        doc_id = st.session_state.selected_document
        
        # Get comments for this document
        doc_comments = [c for c in st.session_state.document_comments if c["document_id"] == doc_id]
        
        # Define document titles based on ID
        doc_titles = {
            "doc_101": "Floor Plans (A2.1)",
            "doc_102": "Elevations (A3.1)",
            "doc_103": "Structural Details (S2.3)",
            "spec_01": "Division 03 - Concrete",
            "spec_02": "Division 08 - Openings",
            "sub_01": "Structural Steel",
            "sub_02": "Curtain Wall System"
        }
        
        # Get the document title
        doc_title = doc_titles.get(doc_id, "Unknown Document")
        
        # Render document viewer
        st.markdown(f"### {doc_title}")
        
        # Document toolbar
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("🔍 Zoom In")
        with col2:
            st.button("🔍 Zoom Out")
        with col3:
            st.button("📝 Add Comment")
        with col4:
            st.button("📥 Download")
        
        # Document display (placeholder)
        if doc_id.startswith("doc_"):
            # For drawings, show a mock drawing area
            st.markdown("""
            <style>
            .document-viewer {
                border: 1px solid #ddd;
                background-color: #f5f5f5;
                height: 500px;
                position: relative;
                overflow: hidden;
            }
            .drawing-placeholder {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
                color: #999;
                flex-direction: column;
            }
            .comment-marker {
                position: absolute;
                width: 24px;
                height: 24px;
                background-color: #f9a01b;
                color: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 12px;
                cursor: pointer;
            }
            </style>
            
            <div class="document-viewer">
                <div class="drawing-placeholder">
                    <div style="font-size: 48px;">📋</div>
                    <div>Document Viewer - Drawing {doc_id}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Add comment markers
            for i, comment in enumerate(doc_comments):
                # Position is specified in the comment
                left = comment["position"]["x"]
                top = comment["position"]["y"]
                
                st.markdown(f"""
                <div class="comment-marker" style="left: {left}px; top: {top}px;">{i+1}</div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        elif doc_id.startswith("spec_"):
            # For specifications, show a text document placeholder
            st.text_area("Document Content", 
                       value="This is a placeholder for specification document content.\n" +
                       "In a production environment, this would display the actual document content\n" +
                       "with support for inline comments and collaborative editing.",
                       height=500, disabled=True)
        else:
            # For submittals, show another type of viewer
            st.markdown("""
            <style>
            .submittal-viewer {
                border: 1px solid #ddd;
                background-color: white;
                height: 500px;
                padding: 1rem;
                overflow-y: auto;
            }
            </style>
            
            <div class="submittal-viewer">
                <h3>Submittal Document</h3>
                <p>Product Data Sheet for: {doc_title}</p>
                <p>Submitted by: Supplier Company</p>
                <p>Date Submitted: 2025-04-15</p>
                <hr>
                <p>This placeholder represents the content of a submittal document.
                In the production version, this would display the actual submittal content
                with support for comments, approval workflows, and revision tracking.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Comment section
        st.markdown("### Comments")
        
        # Display comments
        if doc_comments:
            for comment in doc_comments:
                user = user_map.get(comment["user_id"], {"name": "Unknown User", "avatar": "👤"})
                
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"""
                        <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                            <p><strong>{user['avatar']} {user['name']}</strong> <small>{comment['timestamp']} | Page {comment['page']}</small></p>
                            <p>{comment['content']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.button("Reply", key=f"reply_{comment['id']}")
        else:
            st.info("No comments on this document yet.")
        
        # New comment form
        with st.form(key="new_comment_form"):
            comment_text = st.text_area("Add a comment", placeholder="Type your comment here...")
            col1, col2 = st.columns([3, 1])
            with col2:
                submit_comment = st.form_submit_button("Post Comment")
            
            if submit_comment and comment_text:
                # Add new comment
                new_comment = {
                    "id": f"comment_{uuid.uuid4().hex[:8]}",
                    "document_id": doc_id,
                    "user_id": "user_1",  # Current user
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "content": comment_text,
                    "page": 1,  # Default to page 1
                    "position": {"x": random.randint(50, 350), "y": random.randint(50, 450)}  # Random position
                }
                
                st.session_state.document_comments.append(new_comment)
                st.success("Comment added!")
                st.rerun()

def render_notifications_panel():
    """Render a notifications panel showing project notifications."""
    # Get notifications for the current user
    if "notifications" in st.session_state:
        user_notifications = [n for n in st.session_state.notifications if n["user_id"] == "user_1"]
    else:
        user_notifications = []
    
    unread_count = len([n for n in user_notifications if not n["read"]])
    
    # Notification bell with count
    notification_icon = "🔔"
    if unread_count > 0:
        notification_text = f"{notification_icon} ({unread_count})"
    else:
        notification_text = notification_icon
    
    if st.button(notification_text, key="notification_toggle"):
        st.session_state.show_notifications = not st.session_state.get("show_notifications", False)
    
    # Display notifications panel if toggled
    if st.session_state.get("show_notifications", False):
        with st.container():
            st.markdown("""
            <style>
            .notification-panel {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 1rem;
                background-color: white;
                max-height: 300px;
                overflow-y: auto;
            }
            .notification-item {
                padding: 0.75rem;
                border-bottom: 1px solid #eee;
                cursor: pointer;
            }
            .notification-item:hover {
                background-color: #f5f5f5;
            }
            .notification-unread {
                background-color: #e3f2fd;
            }
            </style>
            
            <div class="notification-panel">
                <h3>Notifications</h3>
            """, unsafe_allow_html=True)
            
            if user_notifications:
                for notif in user_notifications:
                    # Determine if this notification is unread
                    read_class = "" if notif["read"] else "notification-unread"
                    
                    st.markdown(f"""
                    <div class="notification-item {read_class}">
                        <div><strong>{notif['content']}</strong></div>
                        <div><small>{notif['timestamp']}</small></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Mark as read button
                    if not notif["read"]:
                        if st.button("Mark as read", key=f"read_{notif['id']}"):
                            # Mark notification as read
                            for n in st.session_state.notifications:
                                if n["id"] == notif["id"]:
                                    n["read"] = True
                            st.rerun()
            else:
                st.info("No notifications")
            
            st.markdown("</div>", unsafe_allow_html=True)