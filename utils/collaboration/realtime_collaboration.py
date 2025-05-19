"""
Realtime Collaboration Module for gcPanel.

This module provides WebSocket-based collaboration tools for real-time
interaction between team members, including chat, document editing,
comment threads, and @mentions.
"""

import streamlit as st
import json
import time
import uuid
from datetime import datetime

# ----- WebSocket Mock Implementation -----
# In a real application, this would use actual WebSockets
# For this demo, we'll simulate it with session state

class MockWebSocketManager:
    """Mock WebSocket Manager for demonstration purposes.
    
    In a real implementation, this would use actual WebSockets.
    """
    
    def __init__(self):
        """Initialize WebSocket manager."""
        # Initialize connection in session state if not present
        if "ws_connected" not in st.session_state:
            st.session_state.ws_connected = False
            
        if "ws_messages" not in st.session_state:
            st.session_state.ws_messages = []
            
        if "ws_users_online" not in st.session_state:
            st.session_state.ws_users_online = [
                {"id": "user1", "name": "John Smith", "role": "Project Manager", "status": "online"},
                {"id": "user2", "name": "Sarah Johnson", "role": "Field Engineer", "status": "online"},
                {"id": "user3", "name": "Mike Chen", "role": "Architect", "status": "away"},
                {"id": "user4", "name": "Lisa Rodriguez", "role": "Safety Manager", "status": "offline"}
            ]
    
    def connect(self):
        """Connect to WebSocket."""
        st.session_state.ws_connected = True
        return True
    
    def disconnect(self):
        """Disconnect from WebSocket."""
        st.session_state.ws_connected = False
        return True
    
    def is_connected(self):
        """Check if WebSocket is connected."""
        return st.session_state.ws_connected
    
    def send_message(self, channel, message_data):
        """Send a message through WebSocket.
        
        Args:
            channel (str): Channel/room to send message to
            message_data (dict): Message data to send
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_connected():
            return False
            
        # Add message metadata
        message = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "channel": channel,
            "data": message_data
        }
        
        # Add to session state message history
        st.session_state.ws_messages.append(message)
        
        return True
    
    def get_messages(self, channel=None, limit=50):
        """Get messages from WebSocket.
        
        Args:
            channel (str): Optional channel to filter messages
            limit (int): Maximum number of messages to return
            
        Returns:
            list: List of messages
        """
        if not self.is_connected():
            return []
            
        # Filter by channel if specified
        if channel:
            messages = [m for m in st.session_state.ws_messages if m["channel"] == channel]
        else:
            messages = st.session_state.ws_messages
            
        # Sort by timestamp and limit
        messages.sort(key=lambda m: m["timestamp"], reverse=True)
        return messages[:limit]
    
    def get_online_users(self):
        """Get list of online users.
        
        Returns:
            list: List of online users
        """
        if not self.is_connected():
            return []
            
        return st.session_state.ws_users_online


# ----- Document Collaboration -----

def get_document_comments(document_id):
    """Get comments for a document.
    
    Args:
        document_id (str): Document ID
        
    Returns:
        list: List of comments
    """
    # In a real app, this would fetch from a database
    # For this demo, we'll simulate with session state
    
    if "document_comments" not in st.session_state:
        st.session_state.document_comments = {}
        
    if document_id not in st.session_state.document_comments:
        # Generate some sample comments
        st.session_state.document_comments[document_id] = [
            {
                "id": "comment1",
                "user": {"id": "user1", "name": "John Smith", "avatar": "JS"},
                "timestamp": "2025-05-15T10:30:00",
                "text": "Please review section 3.2 of this document.",
                "mentions": [],
                "reactions": {"👍": 2, "👎": 0},
                "replies": [
                    {
                        "id": "reply1",
                        "user": {"id": "user2", "name": "Sarah Johnson", "avatar": "SJ"},
                        "timestamp": "2025-05-15T11:15:00",
                        "text": "I've made the requested changes.",
                        "mentions": ["user1"],
                        "reactions": {"👍": 1}
                    }
                ]
            },
            {
                "id": "comment2",
                "user": {"id": "user3", "name": "Mike Chen", "avatar": "MC"},
                "timestamp": "2025-05-16T09:45:00",
                "text": "The dimensions on page 5 need to be updated to match the revised plans.",
                "mentions": ["user2"],
                "reactions": {"👍": 0, "👎": 0},
                "replies": []
            }
        ]
    
    return st.session_state.document_comments[document_id]

def add_document_comment(document_id, user_data, comment_text, mentions=None, parent_id=None):
    """Add a comment to a document.
    
    Args:
        document_id (str): Document ID
        user_data (dict): User data of commenter
        comment_text (str): Comment text
        mentions (list): List of user IDs mentioned
        parent_id (str): Parent comment ID for replies
        
    Returns:
        dict: Newly created comment
    """
    # Initialize if needed
    if "document_comments" not in st.session_state:
        st.session_state.document_comments = {}
        
    if document_id not in st.session_state.document_comments:
        st.session_state.document_comments[document_id] = []
    
    # Create new comment
    comment = {
        "id": str(uuid.uuid4()),
        "user": user_data,
        "timestamp": datetime.now().isoformat(),
        "text": comment_text,
        "mentions": mentions or [],
        "reactions": {},
        "replies": []
    }
    
    # Add as reply or top-level comment
    if parent_id:
        # Find parent comment
        for existing_comment in st.session_state.document_comments[document_id]:
            if existing_comment["id"] == parent_id:
                existing_comment["replies"].append(comment)
                break
    else:
        # Add as top-level comment
        st.session_state.document_comments[document_id].append(comment)
    
    # Notify mentioned users (in real app, this would send notifications)
    if mentions:
        for user_id in mentions:
            # Mock notification that would be sent to the user
            notification = {
                "type": "mention",
                "sender": user_data,
                "document_id": document_id,
                "comment_id": comment["id"],
                "timestamp": comment["timestamp"]
            }
            # In a real app, this would send the notification to the user
    
    return comment

def add_reaction_to_comment(document_id, comment_id, reaction, user_id, is_reply=False, parent_id=None):
    """Add a reaction to a comment.
    
    Args:
        document_id (str): Document ID
        comment_id (str): Comment ID
        reaction (str): Reaction emoji
        user_id (str): User ID adding the reaction
        is_reply (bool): Whether the comment is a reply
        parent_id (str): Parent comment ID if is_reply is True
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Make sure document exists
    if "document_comments" not in st.session_state or document_id not in st.session_state.document_comments:
        return False
    
    # Find the comment
    if is_reply and parent_id:
        for comment in st.session_state.document_comments[document_id]:
            if comment["id"] == parent_id:
                for reply in comment["replies"]:
                    if reply["id"] == comment_id:
                        # Add reaction
                        if reaction not in reply["reactions"]:
                            reply["reactions"][reaction] = 0
                        reply["reactions"][reaction] += 1
                        return True
    else:
        for comment in st.session_state.document_comments[document_id]:
            if comment["id"] == comment_id:
                # Add reaction
                if reaction not in comment["reactions"]:
                    comment["reactions"][reaction] = 0
                comment["reactions"][reaction] += 1
                return True
    
    return False

def parse_mentions(text):
    """Parse @mentions in text.
    
    Args:
        text (str): Text to parse
        
    Returns:
        list: List of mentioned user IDs
    """
    # In a real application, this would match user handles and IDs
    # For this demo, we'll do a simple parsing
    
    # Mock user mapping for demonstration
    user_handles = {
        "@john": "user1",
        "@sarah": "user2",
        "@mike": "user3",
        "@lisa": "user4"
    }
    
    mentioned_users = []
    
    # Check for each handle
    for handle, user_id in user_handles.items():
        if handle in text:
            mentioned_users.append(user_id)
    
    return mentioned_users


# ----- Collaboration UI Components -----

def render_comment_thread(document_id, current_user):
    """Render a comment thread for a document.
    
    Args:
        document_id (str): Document ID
        current_user (dict): Current user data
        
    Returns:
        None
    """
    # Get comments for the document
    comments = get_document_comments(document_id)
    
    # Render comments UI
    st.markdown("### Comments")
    
    if not comments:
        st.info("No comments yet. Be the first to comment!")
    
    # Render each comment
    for comment in comments:
        render_comment(comment, document_id, current_user)
    
    # Add new comment
    st.markdown("### Add Comment")
    new_comment = st.text_area("Write a comment (use @username to mention someone)", key=f"new_comment_{document_id}")
    
    if st.button("Post Comment", key=f"post_comment_{document_id}"):
        if new_comment:
            # Parse mentions
            mentions = parse_mentions(new_comment)
            
            # Add comment
            add_document_comment(document_id, current_user, new_comment, mentions)
            
            # Clear input and show success
            st.success("Comment posted!")
            st.session_state[f"new_comment_{document_id}"] = ""
            st.rerun()

def render_comment(comment, document_id, current_user, is_reply=False):
    """Render a single comment.
    
    Args:
        comment (dict): Comment data
        document_id (str): Document ID
        current_user (dict): Current user data
        is_reply (bool): Whether the comment is a reply
        
    Returns:
        None
    """
    # Comment container
    indent = "40px" if is_reply else "0px"
    
    st.markdown(f"""
    <div style="margin-left: {indent}; margin-bottom: 15px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;">
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <div style="width: 30px; height: 30px; border-radius: 50%; background-color: #3B82F6; color: white; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                {comment["user"]["avatar"]}
            </div>
            <div>
                <div style="font-weight: bold;">{comment["user"]["name"]}</div>
                <div style="font-size: 0.8em; color: #666;">{format_timestamp(comment["timestamp"])}</div>
            </div>
        </div>
        <div style="margin-bottom: 10px;">{format_comment_text(comment["text"])}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Reactions
    reaction_col1, reaction_col2, reaction_col3 = st.columns([1, 1, 10])
    
    with reaction_col1:
        thumbs_up_count = comment["reactions"].get("👍", 0)
        if st.button(f"👍 {thumbs_up_count}", key=f"thumbs_up_{comment['id']}"):
            add_reaction_to_comment(document_id, comment["id"], "👍", current_user["id"], is_reply)
            st.rerun()
    
    with reaction_col2:
        thumbs_down_count = comment["reactions"].get("👎", 0)
        if st.button(f"👎 {thumbs_down_count}", key=f"thumbs_down_{comment['id']}"):
            add_reaction_to_comment(document_id, comment["id"], "👎", current_user["id"], is_reply)
            st.rerun()
    
    # Show replies if any
    if not is_reply and comment["replies"]:
        with st.expander(f"View {len(comment['replies'])} replies", expanded=True):
            for reply in comment["replies"]:
                render_comment(reply, document_id, current_user, is_reply=True)
    
    # Reply input (only for top-level comments)
    if not is_reply:
        reply_text = st.text_input("Reply to this comment", key=f"reply_{comment['id']}")
        
        if st.button("Reply", key=f"post_reply_{comment['id']}"):
            if reply_text:
                # Parse mentions
                mentions = parse_mentions(reply_text)
                
                # Always mention the original commenter
                if comment["user"]["id"] not in mentions:
                    mentions.append(comment["user"]["id"])
                
                # Add reply
                add_document_comment(document_id, current_user, reply_text, mentions, comment["id"])
                
                # Clear input and show success
                st.success("Reply posted!")
                st.session_state[f"reply_{comment['id']}"] = ""
                st.rerun()

def format_timestamp(timestamp_str):
    """Format timestamp for display.
    
    Args:
        timestamp_str (str): ISO format timestamp string
        
    Returns:
        str: Formatted timestamp
    """
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
        now = datetime.now()
        
        # Calculate the time difference
        diff = now - timestamp
        
        # Format based on difference
        if diff.days == 0:
            # Today - show time
            return timestamp.strftime("Today at %I:%M %p")
        elif diff.days == 1:
            # Yesterday
            return "Yesterday"
        elif diff.days < 7:
            # This week
            return timestamp.strftime("%A")  # Day name
        else:
            # Older
            return timestamp.strftime("%b %d, %Y")
    
    except Exception:
        # Fallback for any parsing issues
        return timestamp_str

def format_comment_text(text):
    """Format comment text with mentions, links, etc.
    
    Args:
        text (str): Comment text
        
    Returns:
        str: Formatted comment text
    """
    # Mock user mapping for demonstration
    user_handles = {
        "@john": '<span style="color: #3B82F6; font-weight: bold;">@john</span>',
        "@sarah": '<span style="color: #3B82F6; font-weight: bold;">@sarah</span>',
        "@mike": '<span style="color: #3B82F6; font-weight: bold;">@mike</span>',
        "@lisa": '<span style="color: #3B82F6; font-weight: bold;">@lisa</span>'
    }
    
    # Replace mentions with styled versions
    for handle, styled in user_handles.items():
        text = text.replace(handle, styled)
    
    return text

def render_collaboration_chat(channel="general", height=400):
    """Render a collaboration chat interface.
    
    Args:
        channel (str): Chat channel to display
        height (int): Height of the chat window
        
    Returns:
        None
    """
    # Initialize WebSocket connection
    ws_manager = MockWebSocketManager()
    ws_manager.connect()
    
    # Mock current user
    if "current_user" not in st.session_state:
        st.session_state.current_user = {
            "id": "current_user",
            "name": "You",
            "avatar": "YO",
            "role": "Project Engineer"
        }
    
    current_user = st.session_state.current_user
    
    # Get online users
    online_users = ws_manager.get_online_users()
    
    # Display the chat window
    st.markdown(f"""
    <div style="border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px;">
        <div style="background-color: #f0f0f0; padding: 8px 15px; border-bottom: 1px solid #ddd; font-weight: bold;">
            {channel.capitalize()} Chat
        </div>
        <div id="chat-messages" style="height: {height-50}px; overflow-y: auto; padding: 10px; background-color: #fff;">
    """, unsafe_allow_html=True)
    
    # Get messages for the channel
    messages = ws_manager.get_messages(channel)
    
    # If no messages, show a placeholder
    if not messages:
        st.markdown("No messages yet. Start the conversation!")
    
    # Otherwise, display the messages
    for message in messages:
        data = message["data"]
        timestamp = format_timestamp(message["timestamp"])
        
        # Message container
        message_html = f"""
        <div style="margin-bottom: 10px; {'text-align: right;' if data['user']['id'] == current_user['id'] else ''}">
            <div style="display: inline-block; max-width: 80%; background-color: {'#e2f0fd' if data['user']['id'] == current_user['id'] else '#f1f1f1'}; border-radius: 10px; padding: 8px 12px;">
                <div style="font-size: 0.8em; color: #666; margin-bottom: 3px;">
                    {data['user']['name'] if data['user']['id'] != current_user['id'] else 'You'} • {timestamp}
                </div>
                <div>{format_comment_text(data['text'])}</div>
            </div>
        </div>
        """
        
        st.markdown(message_html, unsafe_allow_html=True)
    
    # Close the chat window div
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Message input area
    message_text = st.text_input("Type a message (use @username to mention)", key=f"chat_input_{channel}")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Show typing indicator (simulated)
        if "typing_users" not in st.session_state:
            st.session_state.typing_users = []
            
        if st.session_state.typing_users:
            typing_text = ", ".join([u["name"] for u in st.session_state.typing_users])
            st.caption(f"{typing_text} {'is' if len(st.session_state.typing_users) == 1 else 'are'} typing...")
    
    with col2:
        # Send button
        if st.button("Send", key=f"send_button_{channel}"):
            if message_text:
                # Parse mentions
                mentions = parse_mentions(message_text)
                
                # Send message
                ws_manager.send_message(channel, {
                    "user": current_user,
                    "text": message_text,
                    "mentions": mentions
                })
                
                # Clear input
                st.session_state[f"chat_input_{channel}"] = ""
                st.rerun()
    
    # Online users sidebar
    with st.sidebar:
        st.subheader("Online Users")
        
        for user in online_users:
            status_color = "green" if user["status"] == "online" else "orange" if user["status"] == "away" else "gray"
            
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="width: 10px; height: 10px; border-radius: 50%; background-color: {status_color}; margin-right: 10px;"></div>
                <div>{user["name"]} <span style="font-size: 0.8em; color: #666;">({user["role"]})</span></div>
            </div>
            """, unsafe_allow_html=True)


# ----- Document Collaboration UI -----

def render_document_collaboration(document_id, document_title, document_content, current_user=None):
    """Render a collaborative document editor.
    
    Args:
        document_id (str): Document ID
        document_title (str): Document title
        document_content (str): Document content (can be HTML)
        current_user (dict): Current user, defaults to session
        
    Returns:
        None
    """
    # Use the provided user or session user
    if current_user is None:
        if "current_user" not in st.session_state:
            st.session_state.current_user = {
                "id": "current_user",
                "name": "You",
                "avatar": "YO",
                "role": "Project Engineer"
            }
        current_user = st.session_state.current_user
    
    # Document header
    st.title(document_title)
    
    # Status indicators
    col1, col2, col3 = st.columns([1, 1, 5])
    
    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center;">
            <div style="width: 10px; height: 10px; border-radius: 50%; background-color: green; margin-right: 5px;"></div>
            <div style="font-size: 0.9em;">3 viewers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="display: flex; align-items: center;">
            <div style="width: 10px; height: 10px; border-radius: 50%; background-color: orange; margin-right: 5px;"></div>
            <div style="font-size: 0.9em;">Last edit: 5m ago</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Document tabs (Document, Comments, History)
    tabs = st.tabs(["Document", "Comments", "History"])
    
    # Document tab
    with tabs[0]:
        # Document content (HTML)
        st.markdown(document_content, unsafe_allow_html=True)
        
        # Edit button
        if st.button("Edit Document"):
            st.info("Document editing would be implemented here. In a real application, this would use WebSockets for real-time collaboration.")
    
    # Comments tab
    with tabs[1]:
        render_comment_thread(document_id, current_user)
    
    # History tab
    with tabs[2]:
        st.markdown("### Document History")
        
        # Mock history data
        history = [
            {"user": "Sarah Johnson", "action": "Updated section 3.2", "timestamp": "2025-05-16T15:30:00"},
            {"user": "John Smith", "action": "Added new diagrams", "timestamp": "2025-05-14T11:20:00"},
            {"user": "Mike Chen", "action": "Initial document creation", "timestamp": "2025-05-10T09:45:00"}
        ]
        
        for entry in history:
            st.markdown(f"""
            <div style="margin-bottom: 10px; padding: 8px; border-left: 2px solid #3B82F6;">
                <div style="font-weight: bold;">{entry['action']}</div>
                <div style="font-size: 0.8em; color: #666;">{entry['user']} • {format_timestamp(entry['timestamp'])}</div>
            </div>
            """, unsafe_allow_html=True)