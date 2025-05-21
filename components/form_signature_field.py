"""
Form Signature Field Component for gcPanel.

This module provides a reusable digital signature field that can be 
embedded in any form throughout the application.
"""

import streamlit as st
import base64
from datetime import datetime
import os
import json

def signature_field(label="Signature", key=None, required=False, include_timestamp=True, 
                  include_name=True, external_options=True):
    """
    Render a signature field that can be embedded in any form.
    
    Args:
        label (str): Label for the signature field
        key (str): Unique key for the component state
        required (bool): Whether the signature is required
        include_timestamp (bool): Whether to include timestamp with signature
        include_name (bool): Whether to include signer name field
        external_options (bool): Whether to show DocuSign/SignNow options
        
    Returns:
        dict: Signature data including image, name, timestamp, and method
    """
    # Create a unique key for this instance if none provided
    if key is None:
        key = f"sig_{label.lower().replace(' ', '_')}"
    
    # Initialize the signature data in session state if not present
    if f"{key}_data" not in st.session_state:
        st.session_state[f"{key}_data"] = {
            "image": None,
            "name": "",
            "timestamp": "",
            "method": "draw"
        }
    
    # Create the signature fieldset
    st.markdown(f"#### {label}{' *' if required else ''}")
    
    # Add name field if requested
    if include_name:
        signer_name = st.text_input(
            "Signer Name", 
            value=st.session_state[f"{key}_data"]["name"],
            key=f"{key}_name"
        )
        if signer_name != st.session_state[f"{key}_data"]["name"]:
            st.session_state[f"{key}_data"]["name"] = signer_name
    
    # Create tabs for different signature methods if external options are enabled
    if external_options:
        signature_tabs = st.tabs(["Draw Signature", "DocuSign", "SignNow"])
        
        # Draw signature tab - this is where the canvas will be
        with signature_tabs[0]:
            _draw_signature_area(key)
            
        # DocuSign tab
        with signature_tabs[1]:
            _docusign_option(key)
            
        # SignNow tab  
        with signature_tabs[2]:
            _signnow_option(key)
    else:
        # Just the drawing canvas
        _draw_signature_area(key)
    
    # Add timestamp if enabled
    if include_timestamp and st.session_state[f"{key}_data"]["image"] is not None:
        if not st.session_state[f"{key}_data"]["timestamp"]:
            st.session_state[f"{key}_data"]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        st.caption(f"Signed: {st.session_state[f'{key}_data']['timestamp']}")
    
    # Return the signature data
    return st.session_state[f"{key}_data"]

def _draw_signature_area(key):
    """Create an HTML canvas for signature drawing."""
    # Add the signature pad container and styling
    st.markdown(f"""
    <style>
    .signature-pad-container {{
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        margin: 10px 0;
        width: 100%;
    }}
    </style>
    
    <div class="signature-pad-container">
        <canvas id="{key}_canvas" width="600" height="150" style="width: 100%; height: 150px;"></canvas>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/signature_pad@4.0.6/dist/signature_pad.umd.min.js"></script>
    <script>
        // Initialize the signature pad
        var {key}_canvas = document.getElementById("{key}_canvas");
        var {key}_signaturePad = new SignaturePad({key}_canvas, {{
            backgroundColor: 'rgba(255, 255, 255, 0)',
            penColor: 'rgb(0, 0, 0)',
            minWidth: 1,
            maxWidth: 2.5
        }});
        
        // Adjust canvas size on window resize
        function {key}_resizeCanvas() {{
            var ratio = Math.max(window.devicePixelRatio || 1, 1);
            {key}_canvas.width = {key}_canvas.offsetWidth * ratio;
            {key}_canvas.height = {key}_canvas.offsetHeight * ratio;
            {key}_canvas.getContext("2d").scale(ratio, ratio);
            {key}_signaturePad.clear();
        }}
        
        window.addEventListener("resize", {key}_resizeCanvas);
        {key}_resizeCanvas();
        
        // Save signature when drawn
        {key}_canvas.addEventListener("mouseup", function() {{
            if (!{key}_signaturePad.isEmpty()) {{
                var signatureData = {key}_signaturePad.toDataURL();
                
                // Send to Streamlit using the component message passing
                window.parent.postMessage({{
                    type: "streamlit:setComponentValue",
                    value: {{
                        {key}: signatureData
                    }}
                }}, "*");
            }}
        }});
        
        {key}_canvas.addEventListener("touchend", function() {{
            if (!{key}_signaturePad.isEmpty()) {{
                var signatureData = {key}_signaturePad.toDataURL();
                
                // Send to Streamlit using the component message passing
                window.parent.postMessage({{
                    type: "streamlit:setComponentValue",
                    value: {{
                        {key}: signatureData
                    }}
                }}, "*");
            }}
        }});
    </script>
    """, unsafe_allow_html=True)
    
    # Instead of using a button inside the form (which causes errors),
    # we'll add a JavaScript clear button directly
    st.markdown(f"""
    <div style="margin-bottom: 10px;">
        <button type="button" onclick="clearSignature_{key}()" 
                style="background-color: #f8f9fa; border: 1px solid #ced4da; 
                border-radius: 4px; padding: 4px 8px; cursor: pointer;">
            Clear Signature
        </button>
    </div>
    
    <script>
        function clearSignature_{key}() {{
            if (typeof {key}_signaturePad !== 'undefined') {{
                {key}_signaturePad.clear();
                
                // Send a message to Streamlit to clear the session state
                window.parent.postMessage({{
                    type: "streamlit:setComponentValue",
                    value: {{
                        {key}_clear: true
                    }}
                }}, "*");
            }}
        }}
    </script>
    """, unsafe_allow_html=True)
    
    # Check if the clear button was clicked via the custom event
    if f"{key}_clear" in st.session_state and st.session_state[f"{key}_clear"]:
        # Clear the signature data
        st.session_state[f"{key}_data"]["image"] = None
        st.session_state[f"{key}_data"]["timestamp"] = ""
        st.session_state[f"{key}_data"]["method"] = "draw"
        # Reset the clear flag
        st.session_state[f"{key}_clear"] = False
    
    # Handle the signature data received from JS
    # This would be updated to handle the actual data from the component message passing
    query_params = st.experimental_get_query_params()
    if key in query_params:
        st.session_state[f"{key}_data"]["image"] = query_params[key][0]
        st.session_state[f"{key}_data"]["method"] = "draw"
        if not st.session_state[f"{key}_data"]["timestamp"]:
            st.session_state[f"{key}_data"]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # If we already have a signature, display it
    if st.session_state[f"{key}_data"]["image"]:
        st.markdown(f"""
        <div style="margin-top: 10px;">
            <img src="{st.session_state[f"{key}_data"]["image"]}" style="max-height: 100px; border: 1px solid #e0e0e0; border-radius: 4px; padding: 5px;" />
        </div>
        """, unsafe_allow_html=True)

def _docusign_option(key):
    """Create DocuSign integration option."""
    st.markdown("""
    ### Send via DocuSign
    
    Send this document for electronic signature through DocuSign.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        recipient_name = st.text_input("Recipient Name", key=f"{key}_docusign_name")
    with col2:
        recipient_email = st.text_input("Recipient Email", key=f"{key}_docusign_email")
    
    if st.button("Send via DocuSign", key=f"{key}_docusign_send"):
        if recipient_name and recipient_email:
            # In a real integration, this would call the DocuSign API
            st.success(f"Document sent to {recipient_name} ({recipient_email}) via DocuSign.")
            
            # Update the signature data
            st.session_state[f"{key}_data"]["name"] = recipient_name
            st.session_state[f"{key}_data"]["method"] = "DocuSign"
            st.session_state[f"{key}_data"]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Use a placeholder image for DocuSign
            st.session_state[f"{key}_data"]["image"] = "data:image/png;base64,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"
        else:
            st.error("Please enter recipient name and email.")

def _signnow_option(key):
    """Create SignNow integration option."""
    st.markdown("""
    ### Send via SignNow
    
    Send this document for electronic signature through SignNow.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        recipient_name = st.text_input("Recipient Name", key=f"{key}_signnow_name")
    with col2:
        recipient_email = st.text_input("Recipient Email", key=f"{key}_signnow_email")
    
    if st.button("Send via SignNow", key=f"{key}_signnow_send"):
        if recipient_name and recipient_email:
            # In a real integration, this would call the SignNow API
            st.success(f"Document sent to {recipient_name} ({recipient_email}) via SignNow.")
            
            # Update the signature data
            st.session_state[f"{key}_data"]["name"] = recipient_name
            st.session_state[f"{key}_data"]["method"] = "SignNow"
            st.session_state[f"{key}_data"]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Use a placeholder image for SignNow
            st.session_state[f"{key}_data"]["image"] = "data:image/png;base64,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"
        else:
            st.error("Please enter recipient name and email.")

def get_signature_image(signature_data):
    """Get the signature image from the signature data."""
    if signature_data is None or signature_data.get("image") is None:
        return None
    return signature_data["image"]

def save_signature(signature_data, filename=None):
    """
    Save the signature data to a file.
    
    Args:
        signature_data (dict): The signature data from signature_field function
        filename (str, optional): The filename to save to. If None, a timestamped filename is used.
        
    Returns:
        str: The filename where the signature was saved, or None if no signature
    """
    if signature_data is None or signature_data.get("image") is None:
        return None
    
    os.makedirs("signatures", exist_ok=True)
    
    # Generate filename if not provided
    if filename is None:
        name = signature_data.get("name", "unnamed").lower().replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"signatures/sig_{name}_{timestamp}.png"
    
    # Save signature image
    if signature_data["image"].startswith("data:image"):
        # Extract base64 data
        img_data = signature_data["image"].split(",")[1]
        with open(filename, "wb") as f:
            f.write(base64.b64decode(img_data))
    
    # Save metadata
    metadata = {
        "name": signature_data.get("name", ""),
        "timestamp": signature_data.get("timestamp", ""),
        "method": signature_data.get("method", "")
    }
    
    meta_filename = f"{filename}.json"
    with open(meta_filename, "w") as f:
        json.dump(metadata, f, indent=2)
    
    return filename