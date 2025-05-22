"""
Transmittals Module for gcPanel

This module implements the Transmittals functionality for the Engineering section,
using the standardized CRUD template for consistent styling and behavior.
"""

import streamlit as st
import os
import json
from datetime import datetime, timedelta
import random
import pandas as pd

from modules.crud_template import CrudModule
from assets.crud_styler import (
    apply_crud_styles, 
    render_form_actions, 
    render_crud_fieldset
)

class TransmittalModule(CrudModule):
    def __init__(self):
        """Initialize the Transmittals module with configuration."""
        super().__init__(
            module_name="Transmittals",
            data_file_path="data/engineering/transmittals.json",
            id_field="transmittal_id",
            list_columns=["transmittal_id", "date_sent", "recipient", "subject", "status"],
            default_sort_field="date_sent",
            default_sort_direction="desc",
            status_field="status",
            filter_options=["Draft", "Sent", "Delivered", "Acknowledged", "Returned"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        recipients = [
            "Architect - Modern Architects Group", 
            "Owner - Highland Properties LLC", 
            "Structural Engineer - Smith Engineering",
            "MEP Engineer - MEP Solutions Inc.", 
            "General Contractor - GC Construction",
            "Electrical Subcontractor - Electrical Solutions",
            "Plumbing Subcontractor - Plumbing Specialists",
            "HVAC Subcontractor - HVAC Contractors",
            "Building Department - City of Highland",
            "Fire Marshal - Highland Fire Department"
        ]
        
        subjects = [
            "Submittal Package for Concrete Mix Design", 
            "RFI Response for Foundation Details", 
            "Updated Construction Schedule",
            "Revised Mechanical Drawings", 
            "Electrical Load Calculations", 
            "Plumbing Fixture Submittals",
            "Steel Shop Drawings", 
            "Building Permit Application", 
            "Window Shop Drawings",
            "Fire Alarm Design"
        ]
        
        statuses = ["Draft", "Sent", "Delivered", "Acknowledged", "Returned"]
        
        demo_items = []
        
        # Create sample transmittals
        for i in range(1, 21):
            # Set dates
            date_sent = datetime.now() - timedelta(days=random.randint(1, 90))
            
            # Determine status and set related dates accordingly
            status = random.choice(statuses)
            date_delivered = None
            date_acknowledged = None
            date_returned = None
            
            if status in ["Delivered", "Acknowledged", "Returned"]:
                date_delivered = date_sent + timedelta(days=random.randint(1, 5))
                
                if status in ["Acknowledged", "Returned"]:
                    date_acknowledged = date_delivered + timedelta(days=random.randint(1, 7))
                    
                    if status == "Returned":
                        date_returned = date_acknowledged + timedelta(days=random.randint(1, 10))
            
            # Randomly select recipient and subject
            recipient = random.choice(recipients)
            subject = random.choice(subjects)
            
            # Create attachments
            num_attachments = random.randint(1, 5)
            attachments = []
            
            for j in range(num_attachments):
                attachments.append({
                    'title': f"Attachment {j+1}",
                    'description': f"Description for attachment {j+1}",
                    'file_type': random.choice(["PDF", "DWG", "DOC", "XLS", "IMG"]),
                    'file_name': f"attachment_{j+1}.pdf"  # Demo mode only
                })
            
            # Create the transmittal
            item = {
                'transmittal_id': f'TRN-{i:03d}',
                'date_sent': date_sent.strftime('%Y-%m-%d'),
                'recipient': recipient,
                'recipient_company': recipient.split(' - ')[1] if ' - ' in recipient else "",
                'recipient_email': f"contact@{recipient.split(' - ')[1].lower().replace(' ', '')}.com" if ' - ' in recipient else "",
                'sender': "John Smith",
                'sender_company': "GC Construction",
                'sender_email': "john.smith@gcconstruction.com",
                'subject': subject,
                'description': f"Transmittal for {subject} to {recipient}",
                'delivery_method': random.choice(["Email", "Courier", "Mail", "FedEx", "Hand Delivery"]),
                'status': status,
                'date_delivered': date_delivered.strftime('%Y-%m-%d') if date_delivered else None,
                'date_acknowledged': date_acknowledged.strftime('%Y-%m-%d') if date_acknowledged else None,
                'date_returned': date_returned.strftime('%Y-%m-%d') if date_returned else None,
                'comments': "" if random.random() < 0.7 else "Please review and respond at your earliest convenience.",
                'attachments': attachments
            }
            
            demo_items.append(item)
        
        # Save demo data
        self._save_items(demo_items)
    
    def _create_new_item_template(self):
        """Create a template for a new transmittal with default values."""
        transmittal_id = self._generate_new_id()
        
        # Set default dates
        today = datetime.now()
        
        return {
            'transmittal_id': f'TRN-{int(transmittal_id):03d}',
            'date_sent': today.strftime('%Y-%m-%d'),
            'recipient': '',
            'recipient_company': '',
            'recipient_email': '',
            'sender': 'Current User',
            'sender_company': 'GC Construction',
            'sender_email': '',
            'subject': '',
            'description': '',
            'delivery_method': 'Email',
            'status': 'Draft',
            'date_delivered': None,
            'date_acknowledged': None,
            'date_returned': None,
            'comments': '',
            'attachments': []
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for transmittals."""
        items = self._get_items()
        
        # If no items exist yet, start with ID 1
        if not items:
            return "1"
        
        # Find the highest numerical ID and increment
        max_id = 0
        for item in items:
            transmittal_id = item.get('transmittal_id', '')
            if transmittal_id.startswith('TRN-'):
                try:
                    num = int(transmittal_id.split('-')[1])
                    max_id = max(max_id, num)
                except:
                    pass
        
        return str(max_id + 1)
    
    def _get_status_class(self, status):
        """Get the status class for a given status value."""
        status_classes = {
            'Draft': 'secondary',
            'Sent': 'info',
            'Delivered': 'primary',
            'Acknowledged': 'success',
            'Returned': 'warning'
        }
        return status_classes.get(status, 'secondary')
    
    def render_detail_view(self):
        """Render the detail view for creating, viewing, or editing a transmittal."""
        # Apply CRUD styles
        apply_crud_styles()
        
        base_key = self._get_state_key_prefix()
        
        # Get view mode
        is_new = st.session_state.get(f'{base_key}_view') == 'new'
        is_edit_mode = st.session_state.get(f'{base_key}_edit_mode', False)
        
        # Get item data
        if is_new:
            item = self._create_new_item_template()
            detail_title = "New Transmittal"
        else:
            item_id = st.session_state.get(f'{base_key}_selected_id')
            item = self._get_item_by_id(item_id)
            if not item:
                st.error(f"Transmittal with ID {item_id} not found")
                return
            detail_title = f"{item.get('subject', item.get('transmittal_id', 'Transmittal'))}"
        
        # Render the detail container
        from assets.crud_styler import render_crud_detail_container, end_crud_detail_container
        
        mode_prefix = "New" if is_new else "Edit" if is_edit_mode else "View"
        container_title = f"{mode_prefix}: {detail_title}"
        
        detail_actions = render_crud_detail_container(
            title=container_title,
            is_new=is_new,
            back_button=True
        )
        
        # Check if back button was clicked
        if detail_actions['back_clicked']:
            st.session_state[f'{base_key}_view'] = 'list'
            st.rerun()
        
        # Display top action buttons for view mode
        if not is_new and not is_edit_mode:
            col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
            with col1:
                if st.button("✏️ Edit", type="primary", key=f"edit_{base_key}_action"):
                    st.session_state[f'{base_key}_edit_mode'] = True
                    st.rerun()
            with col2:
                if st.button("📄 PDF", type="secondary", key=f"pdf_{base_key}_action"):
                    st.info("This would generate a PDF version of the transmittal in a production environment.")
            with col3:
                if st.button("🗑️ Delete", type="secondary", key=f"delete_{base_key}_action"):
                    st.warning("Are you sure you want to delete this transmittal?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key=f"confirm_delete_{base_key}"):
                            self._delete_item(item['transmittal_id'])
                            st.success("Transmittal deleted successfully")
                            st.session_state[f'{base_key}_view'] = 'list'
                            st.rerun()
                    with confirm_col2:
                        if st.button("Cancel", key=f"cancel_delete_{base_key}"):
                            st.rerun()
        
        # Create form for editing or read-only view for viewing
        if is_edit_mode or is_new:
            with st.form(f"{base_key}_form"):
                # Basic Information Section
                def render_basic_info():
                    col1, col2 = st.columns(2)
                    with col1:
                        transmittal_id = st.text_input("Transmittal ID", value=item['transmittal_id'], disabled=not is_new)
                    with col2:
                        date_sent = st.date_input(
                            "Date Sent", 
                            value=datetime.strptime(item['date_sent'], '%Y-%m-%d') if item['date_sent'] else datetime.now()
                        )
                    
                    subject = st.text_input("Subject", value=item['subject'])
                    
                    delivery_method = st.selectbox("Delivery Method", options=[
                        'Email', 'Courier', 'Mail', 'FedEx', 'Hand Delivery'
                    ], index=['Email', 'Courier', 'Mail', 'FedEx', 'Hand Delivery'].index(
                        item['delivery_method'] if item['delivery_method'] in ['Email', 'Courier', 'Mail', 'FedEx', 'Hand Delivery'] 
                        else 'Email')
                    )
                    
                    description = st.text_area("Description", value=item['description'], height=100)
                    
                    status = st.selectbox("Status", options=[
                        'Draft', 'Sent', 'Delivered', 'Acknowledged', 'Returned'
                    ], index=['Draft', 'Sent', 'Delivered', 'Acknowledged', 'Returned'].index(
                        item['status'] if item['status'] in ['Draft', 'Sent', 'Delivered', 'Acknowledged', 'Returned'] 
                        else 'Draft')
                    )
                    
                    return transmittal_id, date_sent, subject, delivery_method, description, status
                
                transmittal_id, date_sent, subject, delivery_method, description, status = render_crud_fieldset("Basic Information", render_basic_info)
                
                # Recipient Information Section
                def render_recipient_info():
                    recipient = st.text_input("Recipient", value=item['recipient'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        recipient_company = st.text_input("Recipient Company", value=item['recipient_company'])
                    with col2:
                        recipient_email = st.text_input("Recipient Email", value=item['recipient_email'])
                    
                    return recipient, recipient_company, recipient_email
                
                recipient, recipient_company, recipient_email = render_crud_fieldset("Recipient Information", render_recipient_info)
                
                # Sender Information Section
                def render_sender_info():
                    sender = st.text_input("Sender", value=item['sender'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        sender_company = st.text_input("Sender Company", value=item['sender_company'])
                    with col2:
                        sender_email = st.text_input("Sender Email", value=item['sender_email'])
                    
                    return sender, sender_company, sender_email
                
                sender, sender_company, sender_email = render_crud_fieldset("Sender Information", render_sender_info)
                
                # Status Tracking Section
                def render_status_tracking():
                    show_delivered = status in ['Delivered', 'Acknowledged', 'Returned']
                    show_acknowledged = status in ['Acknowledged', 'Returned']
                    show_returned = status in ['Returned']
                    
                    if show_delivered:
                        date_delivered = st.date_input(
                            "Date Delivered", 
                            value=datetime.strptime(item['date_delivered'], '%Y-%m-%d') if item.get('date_delivered') else datetime.now()
                        )
                    else:
                        date_delivered = None
                    
                    if show_acknowledged:
                        date_acknowledged = st.date_input(
                            "Date Acknowledged", 
                            value=datetime.strptime(item['date_acknowledged'], '%Y-%m-%d') if item.get('date_acknowledged') else datetime.now()
                        )
                    else:
                        date_acknowledged = None
                    
                    if show_returned:
                        date_returned = st.date_input(
                            "Date Returned", 
                            value=datetime.strptime(item['date_returned'], '%Y-%m-%d') if item.get('date_returned') else datetime.now()
                        )
                    else:
                        date_returned = None
                    
                    comments = st.text_area("Comments", value=item['comments'], height=100)
                    
                    return date_delivered, date_acknowledged, date_returned, comments, show_delivered, show_acknowledged, show_returned
                
                date_delivered, date_acknowledged, date_returned, comments, show_delivered, show_acknowledged, show_returned = render_crud_fieldset("Status Tracking", render_status_tracking)
                
                # Form Actions
                form_actions = render_form_actions(
                    save_label="Save Transmittal",
                    cancel_label="Cancel",
                    delete_label="Delete Transmittal",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    # Update item with form values
                    updated_item = {
                        'transmittal_id': transmittal_id,
                        'date_sent': date_sent.strftime('%Y-%m-%d'),
                        'recipient': recipient,
                        'recipient_company': recipient_company,
                        'recipient_email': recipient_email,
                        'sender': sender,
                        'sender_company': sender_company,
                        'sender_email': sender_email,
                        'subject': subject,
                        'description': description,
                        'delivery_method': delivery_method,
                        'status': status,
                        'date_delivered': date_delivered.strftime('%Y-%m-%d') if date_delivered and show_delivered else None,
                        'date_acknowledged': date_acknowledged.strftime('%Y-%m-%d') if date_acknowledged and show_acknowledged else None,
                        'date_returned': date_returned.strftime('%Y-%m-%d') if date_returned and show_returned else None,
                        'comments': comments,
                        'attachments': item.get('attachments', [])
                    }
                    
                    # Save the updated item
                    self._save_item(updated_item)
                    
                    # Show success message and return to list view
                    st.success("Transmittal saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked'] and not is_new:
                    self._delete_item(item['transmittal_id'])
                    st.success("Transmittal deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view
            # Basic Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Basic Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Transmittal ID:** {item['transmittal_id']}")
            with col2:
                st.markdown(f"**Date Sent:** {item['date_sent']}")
            
            st.markdown(f"**Subject:** {item['subject']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Delivery Method:** {item['delivery_method']}")
            with col2:
                status_html = f"""
                <div style="display: flex; align-items: center; background: transparent;">
                    <span class='crud-status crud-status-{self._get_status_class(item['status'])}' style="outline: none; box-shadow: none; border: none;">{item['status']}</span>
                </div>
                """
                st.markdown("**Status:**")
                st.markdown(status_html, unsafe_allow_html=True)
            
            if item.get('description'):
                st.markdown(f"**Description:**")
                st.markdown(f"```{item['description']}```")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Recipient Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Recipient Information")
            
            st.markdown(f"**Recipient:** {item['recipient']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Recipient Company:** {item['recipient_company']}")
            with col2:
                st.markdown(f"**Recipient Email:** {item['recipient_email']}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Sender Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Sender Information")
            
            st.markdown(f"**Sender:** {item['sender']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Sender Company:** {item['sender_company']}")
            with col2:
                st.markdown(f"**Sender Email:** {item['sender_email']}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Status Tracking Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Status Tracking")
            
            # Create a status timeline
            timeline_data = [
                {"date": item['date_sent'], "event": "Sent", "done": True}
            ]
            
            if item.get('date_delivered'):
                timeline_data.append({"date": item['date_delivered'], "event": "Delivered", "done": True})
            elif item['status'] in ['Delivered', 'Acknowledged', 'Returned']:
                timeline_data.append({"date": "Pending", "event": "Delivered", "done": False})
            
            if item.get('date_acknowledged'):
                timeline_data.append({"date": item['date_acknowledged'], "event": "Acknowledged", "done": True})
            elif item['status'] in ['Acknowledged', 'Returned']:
                timeline_data.append({"date": "Pending", "event": "Acknowledged", "done": False})
            
            if item.get('date_returned'):
                timeline_data.append({"date": item['date_returned'], "event": "Returned", "done": True})
            elif item['status'] in ['Returned']:
                timeline_data.append({"date": "Pending", "event": "Returned", "done": False})
            
            # Display timeline
            st.markdown('<div style="display: flex; align-items: center; margin-bottom: 20px;">', unsafe_allow_html=True)
            
            for i, step in enumerate(timeline_data):
                # Determine status color
                if step['done']:
                    color = "green"
                    date = step['date']
                else:
                    color = "gray"
                    date = "Pending"
                
                # Display status circle
                st.markdown(f"""
                <div style="display: flex; flex-direction: column; align-items: center; flex: 1;">
                    <div style="width: 30px; height: 30px; border-radius: 15px; background-color: {color}; 
                         display: flex; justify-content: center; align-items: center; color: white; margin-bottom: 5px;">
                        {i+1}
                    </div>
                    <div style="text-align: center; font-weight: bold;">{step['event']}</div>
                    <div style="text-align: center; font-size: 0.8em;">{date}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Add connector line if not the last item
                if i < len(timeline_data) - 1:
                    st.markdown(f"""
                    <div style="flex: 0.5; height: 2px; background-color: {color}; margin-top: -20px;"></div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if item.get('comments'):
                st.markdown(f"**Comments:**")
                st.markdown(f"```{item['comments']}```")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Attachments Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Attachments")
            
            if not item.get('attachments'):
                st.info("No attachments with this transmittal.")
                
                # Add attachment button
                if st.button("➕ Add Attachment", key=f"add_attachment_{base_key}"):
                    st.session_state[f'{base_key}_add_attachment'] = True
                    
                if st.session_state.get(f'{base_key}_add_attachment', False):
                    with st.form(f"attachment_form_{base_key}"):
                        file_title = st.text_input("Title")
                        file_description = st.text_input("Description")
                        file_type = st.selectbox("File Type", options=["PDF", "DWG", "DOC", "XLS", "IMG"])
                        
                        attachment_actions = st.columns([1, 1])
                        with attachment_actions[0]:
                            save_attachment = st.form_submit_button("Save Attachment")
                        with attachment_actions[1]:
                            cancel_attachment = st.form_submit_button("Cancel")
                        
                        if save_attachment and file_title:
                            # Add attachment to the item
                            new_attachment = {
                                'title': file_title,
                                'description': file_description,
                                'file_type': file_type,
                                'file_name': f"{file_title.lower().replace(' ', '_')}.{file_type.lower()}"  # Demo mode only
                            }
                            
                            attachments = item.get('attachments', [])
                            attachments.append(new_attachment)
                            
                            # Update item with new attachment
                            item['attachments'] = attachments
                            self._save_item(item)
                            
                            st.success("Attachment added successfully")
                            st.session_state[f'{base_key}_add_attachment'] = False
                            st.rerun()
                        
                        if cancel_attachment:
                            st.session_state[f'{base_key}_add_attachment'] = False
                            st.rerun()
            else:
                # Display attachments in a table
                attachments = item.get('attachments', [])
                
                # Create columns for headers
                cols = st.columns([3, 2, 1, 2])
                cols[0].markdown("**Title**")
                cols[1].markdown("**Type**")
                cols[2].markdown("**Action**")
                
                # Display horizontal line
                st.markdown("---")
                
                # Display each attachment
                for i, attachment in enumerate(attachments):
                    cols = st.columns([3, 2, 1, 2])
                    
                    # Display attachment details
                    cols[0].markdown(f"{attachment['title']}")
                    cols[1].markdown(f"{attachment['file_type']}")
                    
                    # Action button
                    with cols[2]:
                        if st.button("📄 View", key=f"view_attachment_{i}_{base_key}"):
                            st.info(f"Viewing {attachment['title']} (Demo Mode)")
                    
                    # Display description if present
                    if attachment.get('description'):
                        st.markdown(f"_{attachment['description']}_")
                    
                    # Add separator between attachments
                    if i < len(attachments) - 1:
                        st.markdown("---")
                
                # Add attachment button
                if st.button("➕ Add Attachment", key=f"add_attachment_{base_key}"):
                    st.session_state[f'{base_key}_add_attachment'] = True
                    
                if st.session_state.get(f'{base_key}_add_attachment', False):
                    with st.form(f"attachment_form_{base_key}"):
                        file_title = st.text_input("Title")
                        file_description = st.text_input("Description")
                        file_type = st.selectbox("File Type", options=["PDF", "DWG", "DOC", "XLS", "IMG"])
                        
                        attachment_actions = st.columns([1, 1])
                        with attachment_actions[0]:
                            save_attachment = st.form_submit_button("Save Attachment")
                        with attachment_actions[1]:
                            cancel_attachment = st.form_submit_button("Cancel")
                        
                        if save_attachment and file_title:
                            # Add attachment to the item
                            new_attachment = {
                                'title': file_title,
                                'description': file_description,
                                'file_type': file_type,
                                'file_name': f"{file_title.lower().replace(' ', '_')}.{file_type.lower()}"  # Demo mode only
                            }
                            
                            attachments = item.get('attachments', [])
                            attachments.append(new_attachment)
                            
                            # Update item with new attachment
                            item['attachments'] = attachments
                            self._save_item(item)
                            
                            st.success("Attachment added successfully")
                            st.session_state[f'{base_key}_add_attachment'] = False
                            st.rerun()
                        
                        if cancel_attachment:
                            st.session_state[f'{base_key}_add_attachment'] = False
                            st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        end_crud_detail_container()

def render():
    """Render the Transmittals module."""
    st.title("Transmittals")
    
    # Create and render the Transmittals module
    transmittals = TransmittalModule()
    transmittals.render()