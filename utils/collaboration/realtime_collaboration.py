"""
Real-time collaboration utilities for document editing and commenting.

This module provides functionality for real-time collaboration on documents,
including collaborative editing, commenting, and version control.
"""

import streamlit as st
from datetime import datetime
import random

def render_document_collaboration(document_id, editable=True):
    """
    Render collaborative document editing interface.
    
    Args:
        document_id (str): Identifier for the document
        editable (bool): Whether the document is editable by the current user
    """
    # Get document content (in a real app, this would come from a database)
    document_content = get_document_content(document_id)
    
    # Show collaborative editing interface
    if editable:
        edited_content = st.text_area(
            "Document Content", 
            value=document_content, 
            height=400,
            key=f"doc_editor_{document_id}"
        )
        
        # Show active collaborators
        active_users = get_active_collaborators(document_id)
        
        if active_users:
            st.markdown("### Active Collaborators")
            
            cols = st.columns(len(active_users))
            for i, user in enumerate(active_users):
                with cols[i]:
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="width: 40px; height: 40px; border-radius: 20px; background-color: {user['color']}; 
                                 color: white; display: flex; align-items: center; justify-content: center; 
                                 margin: 0 auto;">
                            {user['name'][0]}
                        </div>
                        <div style="margin-top: 5px; font-size: 12px;">{user['name']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Save and version control buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Save Changes", key=f"save_doc_{document_id}"):
                # In a real app, save to database
                st.success("Document saved successfully!")
                
                # Track the edit in revision history
                add_revision_history_entry(
                    document_id=document_id,
                    user_name="Current User",
                    action="Edited document",
                    details="Updated document content"
                )
                
        with col2:
            if st.button("Create New Version", key=f"version_doc_{document_id}"):
                # In a real app, create a new version in the database
                st.success("New version created successfully!")
                
                # Track the version creation
                add_revision_history_entry(
                    document_id=document_id,
                    user_name="Current User",
                    action="Created new version",
                    details="Created version 2.1"
                )
        
        with col3:
            if st.button("Discard Changes", key=f"discard_doc_{document_id}"):
                # Reload original content
                st.session_state[f"doc_editor_{document_id}"] = document_content
                st.rerun()
    else:
        # Read-only view
        # Use a different approach to avoid backslash issues in f-strings
        # First we'll replace newlines with <br> tags
        formatted_content = document_content.replace("\n", "<br>")
        
        # Then construct the HTML without f-string escape sequences
        content_html = f"""
        <div style="border: 1px solid #e6e6e6; border-radius: 5px; padding: 15px; 
                  background-color: #f9f9f9;">
            {formatted_content}
        </div>
        """
        st.markdown(content_html, unsafe_allow_html=True)
        
        st.warning("You don't have permission to edit this document.")

def render_collaboration_chat(document_id, current_user="Current User"):
    """
    Render real-time collaboration chat interface.
    
    Args:
        document_id (str): Identifier for the document
        current_user (str): Name of the current user
    """
    # Implementation of real-time chat
    st.subheader("Collaboration Chat")
    
    # Initialize chat history if not present
    if f"chat_history_{document_id}" not in st.session_state:
        st.session_state[f"chat_history_{document_id}"] = [
            {"user": "System", "message": "Chat started for this document", "time": datetime.now().strftime("%H:%M")}
        ]
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for chat in st.session_state[f"chat_history_{document_id}"]:
            user_color = generate_user_color(chat["user"])
            st.markdown(
                f"""
                <div style="margin-bottom: 10px;">
                    <span style="font-weight: bold; color: {user_color};">{chat["user"]}</span>
                    <span style="font-size: 0.8em; color: gray;"> ({chat["time"]})</span><br>
                    <span style="margin-left: 10px;">{chat["message"]}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Add new message
    with st.form(f"chat_form_{document_id}", clear_on_submit=True):
        message = st.text_area("Message", height=50, key=f"chat_message_{document_id}")
        submitted = st.form_submit_button("Send")
        
        if submitted and message:
            new_chat = {
                "user": current_user,
                "message": message,
                "time": datetime.now().strftime("%H:%M")
            }
            st.session_state[f"chat_history_{document_id}"].append(new_chat)
            st.rerun()

def render_comment_thread(document_id, current_user="Current User"):
    """
    Render comments thread for collaborative discussion on a document.
    
    Args:
        document_id (str): Identifier for the document
        current_user (str): Name of the current user
    """
    # Get existing comments (in a real app, this would come from a database)
    comments = get_document_comments(document_id)
    
    # Display comments
    if not comments:
        st.info("No comments on this document yet. Be the first to comment!")
    else:
        for comment in comments:
            # Determine if comment has replies
            has_replies = 'replies' in comment and comment['replies']
            
            # User avatar color based on name
            user_color = generate_user_color(comment['user'])
            
            # Main comment box
            with st.container():
                # Avatar and username
                col1, col2 = st.columns([1, 9])
                
                with col1:
                    st.markdown(f"""
                    <div style="width: 40px; height: 40px; border-radius: 20px; background-color: {user_color}; 
                             color: white; display: flex; align-items: center; justify-content: center; margin-top: 10px;">
                        {comment['user'][0]}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Comment header
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="font-weight: 500;">{comment['user']}</span>
                        <span style="color: #666; font-size: 12px;">{comment['time']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Comment type badge if applicable
                    if 'type' in comment and comment['type']:
                        badge_color = {
                            'question': '#3b82f6',
                            'issue': '#ef4444',
                            'suggestion': '#8b5cf6',
                            'general': '#6b7280'
                        }.get(comment['type'].lower(), '#6b7280')
                        
                        st.markdown(f"""
                        <div style="display: inline-block; background-color: {badge_color}; color: white; 
                                 border-radius: 12px; padding: 1px 8px; font-size: 12px; margin-bottom: 8px;">
                            {comment['type']}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Comment text
                    st.markdown(f"<div style='margin-bottom: 5px;'>{comment['text']}</div>", unsafe_allow_html=True)
                    
                    # Comment actions
                    action_col1, action_col2, action_col3 = st.columns([1, 1, 5])
                    
                    with action_col1:
                        reply_button = st.button("Reply", key=f"reply_{comment['id']}")
                        if reply_button:
                            st.session_state[f"replying_to_{comment['id']}"] = True
                    
                    with action_col2:
                        resolve_button = st.button("Resolve", key=f"resolve_{comment['id']}")
                        if resolve_button:
                            st.success(f"Comment resolved by {current_user}")
                            
                            # Track resolution in comment history
                            add_comment_history_entry(
                                comment_id=comment['id'],
                                user_name=current_user,
                                action="resolved",
                            )
            
            # Show replies if any
            if has_replies:
                for reply in comment['replies']:
                    reply_color = generate_user_color(reply['user'])
                    
                    # Indented reply
                    with st.container():
                        # Add indentation
                        rep_col1, rep_col2, rep_col3 = st.columns([1, 1, 8])
                        
                        with rep_col2:
                            st.markdown(f"""
                            <div style="width: 30px; height: 30px; border-radius: 15px; background-color: {reply_color}; 
                                     color: white; display: flex; align-items: center; justify-content: center; margin-top: 10px;">
                                {reply['user'][0]}
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with rep_col3:
                            # Reply header
                            st.markdown(f"""
                            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                <span style="font-weight: 500;">{reply['user']}</span>
                                <span style="color: #666; font-size: 12px;">{reply['time']}</span>
                            </div>
                            <div style='margin-bottom: 5px;'>{reply['text']}</div>
                            """, unsafe_allow_html=True)
            
            # Show reply form if active
            if st.session_state.get(f"replying_to_{comment['id']}", False):
                with st.container():
                    # Add indentation
                    rep_col1, rep_col2 = st.columns([2, 8])
                    
                    with rep_col2:
                        reply_text = st.text_area(
                            "Your reply", 
                            key=f"reply_text_{comment['id']}",
                            height=100
                        )
                        
                        reply_col1, reply_col2 = st.columns([1, 1])
                        
                        with reply_col1:
                            if st.button("Post Reply", key=f"post_reply_{comment['id']}"):
                                if reply_text.strip():
                                    st.success("Reply posted!")
                                    
                                    # In a real app, save to database
                                    # Here we just clear the form
                                    st.session_state[f"replying_to_{comment['id']}"] = False
                                    st.session_state[f"reply_text_{comment['id']}"] = ""
                                    
                                    # Track in comment history
                                    add_comment_history_entry(
                                        comment_id=comment['id'],
                                        user_name=current_user,
                                        action="replied",
                                        details=reply_text
                                    )
                                    
                                    st.rerun()
                                else:
                                    st.error("Reply cannot be empty")
                        
                        with reply_col2:
                            if st.button("Cancel", key=f"cancel_reply_{comment['id']}"):
                                st.session_state[f"replying_to_{comment['id']}"] = False
                                st.rerun()
            
            # Add separator between comments
            st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)

# Helper functions for real-time collaboration features

def get_document_content(document_id):
    """
    Get the content of a document by ID.
    
    Args:
        document_id (str): Identifier for the document
        
    Returns:
        str: Document content text
    """
    # In a real app, this would fetch from a database
    # Here we return sample content for demonstration
    
    if document_id == "DOC-001":
        return """# Foundation Specifications

## 1. General Requirements

The foundation system shall be designed to support all applied loads, including both dead and live loads, as well as lateral loads such as wind and seismic forces. All work shall comply with ACI 318 and local building codes.

## 2. Materials

### 2.1 Concrete
- Compressive Strength: 4,000 psi at 28 days
- Water-Cement Ratio: Maximum 0.45
- Air Content: 5-7%

### 2.2 Reinforcement
- Deformed Bars: ASTM A615, Grade 60
- Welded Wire Fabric: ASTM A1064
"""
    elif document_id == "DOC-002":
        return """# Electrical Specifications

## 1. General Requirements

All electrical work shall comply with the National Electrical Code (NEC) and local building codes. All materials shall be UL listed and labeled.

## 2. Materials

### 2.1 Conductors
- Building Wire: THHN/THWN, copper, 600V
- Cable: Type MC, copper, 600V

### 2.2 Raceways
- Conduit: Rigid galvanized steel (RGS)
- EMT: Electro-galvanized steel
"""
    else:
        return f"# Document {document_id}\n\nContent for this document is not available."

def get_active_collaborators(document_id):
    """
    Get list of users currently collaborating on a document.
    
    Args:
        document_id (str): Identifier for the document
        
    Returns:
        list: List of active collaborator information
    """
    # In a real app, this would track active users in real-time
    # For demo, return some sample users
    return [
        {"name": "John Smith", "color": "#3b82f6"},
        {"name": "Sarah Johnson", "color": "#8b5cf6"},
        {"name": "Mike Chen", "color": "#10b981"},
    ]

def get_document_comments(document_id):
    """
    Get comments for a document.
    
    Args:
        document_id (str): Identifier for the document
        
    Returns:
        list: List of comment objects
    """
    # In a real app, this would fetch from a database
    # Here we return sample comments for demonstration
    
    if document_id == "DOC-001":
        return [
            {
                "id": "comment1",
                "user": "Sarah Johnson",
                "time": "Yesterday at 3:45 PM",
                "type": "Question",
                "text": "Should we specify a minimum thickness for the foundation slab?",
                "replies": [
                    {
                        "id": "reply1",
                        "user": "John Smith",
                        "time": "Yesterday at 4:15 PM",
                        "text": "Yes, I'll add a minimum of 12 inches for the main foundation."
                    }
                ]
            },
            {
                "id": "comment2",
                "user": "Mike Chen",
                "time": "2 days ago",
                "type": "Issue",
                "text": "The reinforcement spacing doesn't match the structural engineer's latest calculations. We need to update this.",
                "replies": []
            }
        ]
    elif document_id == "DOC-002":
        return [
            {
                "id": "comment3",
                "user": "Lisa Rodriguez",
                "time": "Today at 9:30 AM",
                "type": "Suggestion",
                "text": "We should add specifications for LED lighting fixtures throughout the building.",
                "replies": []
            }
        ]
    else:
        return []

def add_revision_history_entry(document_id, user_name, action, details=None):
    """
    Add an entry to document revision history.
    
    Args:
        document_id (str): Identifier for the document
        user_name (str): Name of the user making the change
        action (str): Type of action performed
        details (str, optional): Additional details about the action
    """
    # In a real app, this would save to a database
    # Here we just print a message to simulate this
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    details_str = f": {details}" if details else ""
    
    st.write(f"Added to history: {timestamp} - {user_name} {action}{details_str}")

def add_comment_history_entry(comment_id, user_name, action, details=None):
    """
    Add an entry to comment history.
    
    Args:
        comment_id (str): Identifier for the comment
        user_name (str): Name of the user performing the action
        action (str): Type of action performed
        details (str, optional): Additional details about the action
    """
    # In a real app, this would save to a database
    # Here we just print a message to simulate this
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    details_str = f": {details}" if details else ""
    
    st.write(f"Comment {comment_id}: {timestamp} - {user_name} {action}{details_str}")

def generate_user_color(username):
    """
    Generate a consistent color for a user based on their username.
    
    Args:
        username (str): The username
        
    Returns:
        str: A hex color code
    """
    # Simple hash function to generate a color based on username
    colors = [
        "#3b82f6",  # Blue
        "#10b981",  # Green
        "#8b5cf6",  # Purple
        "#ef4444",  # Red
        "#f59e0b",  # Orange
        "#6366f1",  # Indigo
        "#ec4899",  # Pink
        "#14b8a6",  # Teal
    ]
    
    # Use a hash of the username to pick a consistent color
    color_index = sum(ord(c) for c in username) % len(colors)
    return colors[color_index]