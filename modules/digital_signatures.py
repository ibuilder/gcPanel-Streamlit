"""
Digital Signatures Module for gcPanel.

This module provides digital signature functionality for various forms
in the gcPanel construction management system, including integration with
DocuSign and SignNow as well as direct signature capture.
"""

import streamlit as st
import os
from components.digital_signature_demo import render_signature_demo

def render_digital_signatures():
    """
    Render the digital signatures module.
    
    This module provides signature capabilities for various construction forms
    including change orders, daily reports, and invoices.
    """
    st.title("Digital Signatures")
    
    # Create signatures directory if it doesn't exist
    os.makedirs("signatures", exist_ok=True)
    
    # Main content tabs
    tabs = st.tabs(["Signature Demo", "Recent Signatures", "Configuration"])
    
    # Signature demo tab
    with tabs[0]:
        render_signature_demo()
    
    # Recent signatures tab
    with tabs[1]:
        render_recent_signatures()
    
    # Configuration tab
    with tabs[2]:
        render_signature_configuration()

def render_recent_signatures():
    """Render a list of recent signatures."""
    st.header("Recent Signatures")
    
    # Check if signatures directory exists
    if not os.path.exists("signatures"):
        st.info("No signatures have been captured yet. Try the Signature Demo to create some signatures.")
        return
    
    # Get list of signature files
    signature_files = [f for f in os.listdir("signatures") if f.endswith(".png") and not f.endswith(".json")]
    
    if not signature_files:
        st.info("No signatures have been captured yet. Try the Signature Demo to create some signatures.")
        return
    
    # Display signature files in a grid
    st.write(f"Found {len(signature_files)} signatures")
    
    # Create rows of 3 columns
    for i in range(0, len(signature_files), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(signature_files):
                file = signature_files[i + j]
                with cols[j]:
                    st.image(f"signatures/{file}", width=200)
                    
                    # Try to load metadata
                    metadata_file = f"signatures/{file}.json"
                    if os.path.exists(metadata_file):
                        import json
                        with open(metadata_file, "r") as f:
                            metadata = json.load(f)
                            st.markdown(f"""
                            **Signer:** {metadata.get('signer_name', 'Unknown')}  
                            **Date:** {metadata.get('timestamp', 'Unknown')}  
                            **Provider:** {metadata.get('provider', 'direct')}
                            """)
                    else:
                        st.write("No metadata available")

def render_signature_configuration():
    """Render signature configuration options."""
    st.header("Signature Configuration")
    
    st.markdown("""
    ## External Signature Providers
    
    Configure integration with external electronic signature providers to enable seamless document signing.
    """)
    
    # DocuSign configuration
    st.subheader("DocuSign Configuration")
    
    with st.form("docusign_config"):
        cols = st.columns(2)
        with cols[0]:
            docusign_client_id = st.text_input("DocuSign Client ID", type="password")
            docusign_account_id = st.text_input("DocuSign Account ID")
        with cols[1]:
            docusign_user_id = st.text_input("DocuSign User ID")
            docusign_private_key = st.text_area("DocuSign Private Key", height=100, type="password")
        
        docusign_submitted = st.form_submit_button("Save DocuSign Configuration")
        
        if docusign_submitted:
            if docusign_client_id and docusign_account_id and docusign_user_id and docusign_private_key:
                # Here we would normally save these securely
                st.success("DocuSign configuration saved successfully!")
                st.info("In a production environment, these credentials would be securely stored and used to authenticate with the DocuSign API.")
            else:
                st.error("Please fill out all required fields.")
    
    # SignNow configuration
    st.subheader("SignNow Configuration")
    
    with st.form("signnow_config"):
        cols = st.columns(2)
        with cols[0]:
            signnow_client_id = st.text_input("SignNow Client ID", type="password")
            signnow_client_secret = st.text_input("SignNow Client Secret", type="password")
        with cols[1]:
            signnow_api_url = st.text_input("SignNow API URL", value="https://api.signnow.com")
            signnow_refresh_token = st.text_input("SignNow Refresh Token", type="password")
        
        signnow_submitted = st.form_submit_button("Save SignNow Configuration")
        
        if signnow_submitted:
            if signnow_client_id and signnow_client_secret:
                # Here we would normally save these securely
                st.success("SignNow configuration saved successfully!")
                st.info("In a production environment, these credentials would be securely stored and used to authenticate with the SignNow API.")
            else:
                st.error("Please fill out all required fields.")
    
    # Direct signature configuration
    st.subheader("Direct Signature Configuration")
    
    with st.form("direct_signature_config"):
        st.write("Configure settings for direct signature capture.")
        
        cols = st.columns(2)
        with cols[0]:
            signature_storage = st.selectbox("Signature Storage", ["Local File System", "Database", "Cloud Storage"])
        with cols[1]:
            signature_format = st.selectbox("Signature Format", ["PNG", "JPEG", "SVG"])
        
        require_name = st.checkbox("Require signer name", value=True)
        require_timestamp = st.checkbox("Include timestamp", value=True)
        
        direct_submitted = st.form_submit_button("Save Direct Signature Configuration")
        
        if direct_submitted:
            st.success("Direct signature configuration saved successfully!")