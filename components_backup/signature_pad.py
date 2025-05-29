"""
Signature Pad Component for gcPanel.

This module provides a digital signature pad component that can be embedded in forms
throughout the application. It supports both direct on-screen signatures and
integration with external signature providers like DocuSign and SignNow.
"""

import streamlit as st
import base64
from io import BytesIO
from datetime import datetime
import json
import os

def render_signature_pad(key="signature_pad", label="Signature", height=150, clear_button=True, 
                        save_button=True, external_providers=True):
    """
    Render a signature pad component with options for direct signatures and external providers.
    
    Args:
        key (str): Unique key for the component
        label (str): Label text for the signature field
        height (int): Height of the signature pad in pixels
        clear_button (bool): Whether to show a clear button
        save_button (bool): Whether to show a save button
        external_providers (bool): Whether to show external signature provider options
        
    Returns:
        dict: Dictionary containing signature data and metadata
    """
    # Signature data container
    if f"{key}_data" not in st.session_state:
        st.session_state[f"{key}_data"] = {
            "signature": None,
            "timestamp": None,
            "provider": "local",
            "signer_name": "",
            "signer_email": "",
            "status": "unsigned"
        }
    
    # Display label
    st.markdown(f"### {label}")
    
    # Provider selection tabs
    if external_providers:
        provider_tabs = st.tabs(["Draw Signature", "DocuSign", "SignNow"])
        
        # Direct signature pad tab
        with provider_tabs[0]:
            _render_direct_signature_pad(key, height, clear_button, save_button)
        
        # DocuSign tab
        with provider_tabs[1]:
            _render_docusign_integration(key)
        
        # SignNow tab
        with provider_tabs[2]:
            _render_signnow_integration(key)
    else:
        # Only show direct signature pad
        _render_direct_signature_pad(key, height, clear_button, save_button)
    
    # Display current signature status
    if st.session_state[f"{key}_data"]["signature"]:
        status_color = "green" if st.session_state[f"{key}_data"]["status"] == "signed" else "orange"
        st.markdown(f"""
        <div style="margin-top: 10px; color: {status_color};">
            <p>✓ Signature captured via {st.session_state[f"{key}_data"]["provider"]}</p>
            <p>Signed by: {st.session_state[f"{key}_data"]["signer_name"]}</p>
            <p>Timestamp: {st.session_state[f"{key}_data"]["timestamp"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    return st.session_state[f"{key}_data"]

def _render_direct_signature_pad(key, height, clear_button, save_button):
    """
    Render a HTML canvas-based signature pad for direct signatures.
    """
    # Add the signature pad HTML/JS
    st.markdown(f"""
    <div class="signature-pad-container" style="border: 1px solid #e0e0e0; border-radius: 4px; overflow: hidden;">
        <canvas id="{key}" width="600" height="{height}" style="width: 100%; height: {height}px;"></canvas>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/signature_pad/4.0.0/signature_pad.min.js"></script>
    <script>
        const canvas = document.getElementById("{key}");
        const signaturePad = new SignaturePad(canvas, {{
            backgroundColor: 'rgba(255, 255, 255, 0)',
            penColor: 'rgb(0, 0, 0)',
            minWidth: 1,
            maxWidth: 2.5
        }});
        
        // Adjust canvas size when window is resized
        function resizeCanvas() {{
            const ratio = Math.max(window.devicePixelRatio || 1, 1);
            canvas.width = canvas.offsetWidth * ratio;
            canvas.height = canvas.offsetHeight * ratio;
            canvas.getContext("2d").scale(ratio, ratio);
            signaturePad.clear();
        }}
        
        window.onresize = resizeCanvas;
        resizeCanvas();
        
        // Function to save signature data
        function saveSignature() {{
            if (!signaturePad.isEmpty()) {{
                // Get signature as base64 image
                const signatureData = signaturePad.toDataURL();
                
                // Send data to Streamlit
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: {{
                        key: "{key}",
                        data: signatureData
                    }}
                }}, '*');
            }}
        }}
        
        // Save signature when canvas is touched/clicked
        canvas.addEventListener("touchend", saveSignature);
        canvas.addEventListener("mouseup", saveSignature);
    </script>
    """, unsafe_allow_html=True)
    
    # Add component message handler
    if "component_message_handler" not in st.session_state:
        st.session_state.component_message_handler = True
        st.markdown("""
        <script>
        // Listen for messages from component
        window.addEventListener('message', function(event) {
            if (event.data.type === 'streamlit:componentOutput') {
                const data = event.data;
                // Forward to Streamlit
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: data.value
                }, '*');
            }
        });
        </script>
        """, unsafe_allow_html=True)
    
    # Add buttons for clear and save
    cols = st.columns(2)
    if clear_button:
        if cols[0].button("Clear Signature", key=f"clear_{key}"):
            st.markdown(f"""
            <script>
                signaturePad.clear();
            </script>
            """, unsafe_allow_html=True)
            st.session_state[f"{key}_data"]["signature"] = None
            st.session_state[f"{key}_data"]["timestamp"] = None
            st.session_state[f"{key}_data"]["status"] = "unsigned"
            st.rerun()
    
    if save_button:
        if cols[1].button("Save Signature", key=f"save_{key}"):
            # This is handled by JS, but we also need to get signer info
            st.session_state[f"{key}_data"]["provider"] = "direct"
            st.session_state[f"{key}_data"]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state[f"{key}_data"]["status"] = "signed"
            
            if not st.session_state[f"{key}_data"]["signer_name"]:
                # Prompt for signer name if not already provided
                signer_name = st.text_input("Enter your name:", key=f"{key}_signer_name")
                if signer_name:
                    st.session_state[f"{key}_data"]["signer_name"] = signer_name
    
    # Handle incoming signature data from JS
    if st.experimental_get_query_params().get(key):
        data = st.experimental_get_query_params()[key][0]
        st.session_state[f"{key}_data"]["signature"] = data
        st.session_state[f"{key}_data"]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state[f"{key}_data"]["status"] = "signed"

def _render_docusign_integration(key):
    """
    Render DocuSign integration form.
    """
    st.markdown("""
    ### DocuSign Integration
    
    Send this document for electronic signature via DocuSign.
    """)
    
    with st.form(f"docusign_form_{key}"):
        signer_name = st.text_input("Signer Name")
        signer_email = st.text_input("Signer Email")
        document_name = st.text_input("Document Name", value="gcPanel Document")
        
        submitted = st.form_submit_button("Send for Signature")
        if submitted:
            if signer_name and signer_email:
                # In a real implementation, this would make API calls to DocuSign
                st.session_state[f"{key}_data"]["signer_name"] = signer_name
                st.session_state[f"{key}_data"]["signer_email"] = signer_email
                st.session_state[f"{key}_data"]["provider"] = "DocuSign"
                st.session_state[f"{key}_data"]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state[f"{key}_data"]["status"] = "pending"
                
                st.success(f"Document sent to {signer_email} via DocuSign for signature.")
                
                # Note: Actual implementation would use DocuSign API
                st.info("Note: This is a placeholder for DocuSign API integration. In a production environment, this would connect to the DocuSign API to create and send an envelope.")
            else:
                st.error("Please provide both signer name and email.")
    
    # Display DocuSign configuration
    with st.expander("DocuSign Configuration"):
        st.markdown("""
        To configure DocuSign integration, you'll need:
        
        1. A DocuSign developer account
        2. Integration key (Client ID)
        3. API username/password or JWT authentication
        
        For production use, the actual integration would use the [DocuSign eSignature API](https://developers.docusign.com/docs/esign-rest-api/reference/) to:
        
        1. Create an envelope with the document
        2. Add recipients and routing
        3. Send for signature
        4. Receive webhook callbacks when signed
        """)

def _render_signnow_integration(key):
    """
    Render SignNow integration form.
    """
    st.markdown("""
    ### SignNow Integration
    
    Send this document for electronic signature via SignNow.
    """)
    
    with st.form(f"signnow_form_{key}"):
        signer_name = st.text_input("Signer Name")
        signer_email = st.text_input("Signer Email")
        document_name = st.text_input("Document Name", value="gcPanel Document")
        
        submitted = st.form_submit_button("Send for Signature")
        if submitted:
            if signer_name and signer_email:
                # In a real implementation, this would make API calls to SignNow
                st.session_state[f"{key}_data"]["signer_name"] = signer_name
                st.session_state[f"{key}_data"]["signer_email"] = signer_email
                st.session_state[f"{key}_data"]["provider"] = "SignNow"
                st.session_state[f"{key}_data"]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state[f"{key}_data"]["status"] = "pending"
                
                st.success(f"Document sent to {signer_email} via SignNow for signature.")
                
                # Note: Actual implementation would use SignNow API
                st.info("Note: This is a placeholder for SignNow API integration. In a production environment, this would connect to the SignNow API to create and send a signature request.")
            else:
                st.error("Please provide both signer name and email.")
    
    # Display SignNow configuration
    with st.expander("SignNow Configuration"):
        st.markdown("""
        To configure SignNow integration, you'll need:
        
        1. A SignNow developer account
        2. API Client ID and Client Secret
        3. OAuth2 token for API authentication
        
        For production use, the actual integration would use the [SignNow API](https://docs.signnow.com/api/) to:
        
        1. Upload the document
        2. Add fields and signature requirements
        3. Invite signers
        4. Monitor signature status
        """)

def save_signature_to_file(signature_data, filename=None):
    """
    Save signature data to a file.
    
    Args:
        signature_data (dict): Signature data from the render_signature_pad function
        filename (str, optional): Filename to save to. If None, a timestamped filename is used.
    
    Returns:
        str: Path to the saved signature file
    """
    if not signature_data or not signature_data.get("signature"):
        return None
    
    # Create signatures directory if it doesn't exist
    os.makedirs("signatures", exist_ok=True)
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        signer = signature_data.get("signer_name", "unnamed").lower().replace(" ", "-")
        filename = f"signatures/signature-{signer}-{timestamp}.png"
    
    # Save signature image
    if signature_data["signature"].startswith("data:image"):
        # Extract base64 data
        img_data = signature_data["signature"].split(",")[1]
        with open(filename, "wb") as f:
            f.write(base64.b64decode(img_data))
    
    # Save metadata
    metadata = {
        "signer_name": signature_data.get("signer_name", ""),
        "signer_email": signature_data.get("signer_email", ""),
        "provider": signature_data.get("provider", "direct"),
        "timestamp": signature_data.get("timestamp", ""),
        "status": signature_data.get("status", "signed")
    }
    
    metadata_filename = f"{filename}.json"
    with open(metadata_filename, "w") as f:
        json.dump(metadata, f, indent=2)
    
    return filename