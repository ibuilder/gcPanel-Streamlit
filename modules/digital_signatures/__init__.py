"""
Digital Signatures Module for gcPanel

This module provides digital signature capabilities with multiple options:
1. Direct on-screen signature drawing
2. DocuSign integration
3. SignNow integration

The module can be used standalone or integrated into other modules' forms.
"""

import streamlit as st
import os
import json
from datetime import datetime
import base64
from components.form_signature_field import signature_field, save_signature, get_signature_image

def render_digital_signatures():
    """Main entry point for the Digital Signatures module."""
    st.title("Digital Signatures")
    
    # Create tabs for the different signature options
    tabs = st.tabs(["Create Signature", "Signature Gallery", "Integration Options"])
    
    # Create Signature tab
    with tabs[0]:
        render_signature_creator()
    
    # Signature Gallery tab
    with tabs[1]:
        render_signature_gallery()
    
    # Integration Options tab
    with tabs[2]:
        render_integration_options()

def render_signature_creator():
    """Render the signature creation interface."""
    st.header("Create New Signature")
    
    with st.form("signature_creator_form"):
        # Basic information
        st.text_input("Full Name", key="signature_name")
        st.text_input("Title/Position", key="signature_title")
        
        # Create the signature field
        signature_data = signature_field(
            label="Signature",
            key="new_signature",
            required=True,
            include_timestamp=True,
            include_name=False  # We already collect name above
        )
        
        # Submit button
        submitted = st.form_submit_button("Save Signature")
        
        if submitted:
            # Validate required fields
            if not st.session_state.signature_name:
                st.error("Please enter your full name.")
                return
                
            if not signature_data.get("image"):
                st.error("Please provide a signature.")
                return
            
            # Save the signature
            name = st.session_state.signature_name
            title = st.session_state.signature_title
            
            # Create a more descriptive filename
            safe_name = name.lower().replace(" ", "_")
            filename = f"signatures/signature_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            # Save signature with additional metadata
            save_path = save_signature(signature_data, filename)
            
            # Also save additional metadata
            metadata = {
                "name": name,
                "title": title,
                "timestamp": signature_data.get("timestamp", ""),
                "method": signature_data.get("method", "draw"),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            meta_filename = f"{filename}.json"
            os.makedirs(os.path.dirname(meta_filename), exist_ok=True)
            
            with open(meta_filename, "w") as f:
                json.dump(metadata, f, indent=2)
            
            st.success(f"Signature saved successfully for {name}.")

def render_signature_gallery():
    """Render a gallery of saved signatures."""
    st.header("Signature Gallery")
    
    # Create the signatures directory if it doesn't exist
    os.makedirs("signatures", exist_ok=True)
    
    # Find all signature files
    signature_files = []
    for file in os.listdir("signatures"):
        if file.endswith(".png") and not file.endswith(".json"):
            # Find the corresponding metadata file
            meta_file = f"{file}.json"
            meta_path = os.path.join("signatures", meta_file)
            
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, "r") as f:
                        metadata = json.load(f)
                    
                    signature_files.append({
                        "file_path": os.path.join("signatures", file),
                        "metadata": metadata
                    })
                except Exception as e:
                    st.warning(f"Failed to load metadata for {file}: {str(e)}")
    
    if not signature_files:
        st.info("No signatures have been saved yet. Create a signature in the 'Create Signature' tab.")
        return
    
    # Display the signatures in a grid
    num_cols = 3
    signature_groups = [signature_files[i:i+num_cols] for i in range(0, len(signature_files), num_cols)]
    
    for group in signature_groups:
        cols = st.columns(num_cols)
        
        for i, signature in enumerate(group):
            if i < len(cols):
                with cols[i]:
                    metadata = signature.get("metadata", {})
                    name = metadata.get("name", "Unknown")
                    title = metadata.get("title", "")
                    timestamp = metadata.get("timestamp", "Unknown date")
                    method = metadata.get("method", "draw")
                    
                    # Display signature card
                    st.markdown(f"**{name}**")
                    if title:
                        st.markdown(f"*{title}*")
                    
                    # Display the signature image
                    try:
                        with open(signature["file_path"], "rb") as f:
                            image_data = base64.b64encode(f.read()).decode("utf-8")
                            
                        st.markdown(f"""
                        <div style="border: 1px solid #e0e0e0; padding: 10px; border-radius: 4px; margin-bottom: 10px;">
                            <img src="data:image/png;base64,{image_data}" alt="{name}'s signature" style="max-width: 100%; max-height: 100px;"/>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Failed to load signature image: {str(e)}")
                    
                    st.caption(f"Signed: {timestamp}")
                    st.caption(f"Method: {method}")
                    
                    # Delete button
                    if st.button("Delete", key=f"delete_{signature['file_path']}"):
                        try:
                            os.remove(signature["file_path"])
                            meta_path = f"{signature['file_path']}.json"
                            if os.path.exists(meta_path):
                                os.remove(meta_path)
                            st.success(f"Signature for {name} deleted successfully.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to delete signature: {str(e)}")

def render_integration_options():
    """Render information about how to integrate signatures into other modules."""
    st.header("Integration Options")
    
    st.markdown("""
    ## Using Digital Signatures in Forms

    Digital signatures can be easily integrated into any form within gcPanel.
    Here's how to integrate signatures into your custom forms:
    
    ### 1. Using the Form Signature Field Component
    
    Import the component:
    ```python
    from components.form_signature_field import signature_field, save_signature
    ```
    
    Add a signature field to your form:
    ```python
    signature_data = signature_field(
        label="Signature",
        key="unique_key",
        required=True,
        include_timestamp=True,
        include_name=True
    )
    ```
    
    Save the signature when submitted:
    ```python
    if form_submitted:
        signature_file = save_signature(signature_data, "path/to/save/signature.png")
    ```
    
    ### 2. Available Integration Options
    
    The signature component supports three methods:
    
    - **Draw Signature**: Direct on-screen signature drawing
    - **DocuSign**: Integration with DocuSign for official electronic signatures
    - **SignNow**: Integration with SignNow platform
    
    ### 3. Example Usage in Contracts Module
    
    The Contracts module demonstrates a complete implementation with signatures
    embedded in Change Orders, Subcontracts, and Invoices forms.
    """)
    
    # Add a DocuSign configuration section
    st.subheader("DocuSign Configuration")
    
    with st.expander("Configure DocuSign Integration"):
        st.text_input("DocuSign Integration Key", type="password")
        st.text_input("DocuSign Account ID")
        st.text_area("DocuSign Private Key", height=100, type="password")
        
        st.button("Save DocuSign Configuration")
        
    # Add a SignNow configuration section
    st.subheader("SignNow Configuration")
    
    with st.expander("Configure SignNow Integration"):
        st.text_input("SignNow API Key", type="password")
        st.text_input("SignNow Client ID")
        st.text_input("SignNow Client Secret", type="password")
        
        st.button("Save SignNow Configuration")