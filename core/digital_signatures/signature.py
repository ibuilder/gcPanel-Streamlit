"""
Digital signature module for the gcPanel Construction Management Dashboard.

This module provides functionality for creating, verifying, and managing
digital signatures on construction documents.
"""

import streamlit as st
import base64
import json
import hashlib
import uuid
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
import time

class DigitalSignature:
    """Class for managing digital signatures."""
    
    @staticmethod
    def generate_signature_id() -> str:
        """Generate a unique signature ID."""
        return str(uuid.uuid4())
    
    @staticmethod
    def create_signature_pad(
        key: str, 
        height: int = 200, 
        clear_on_submit: bool = True,
        line_color: str = "#000000",
        background_color: str = "#ffffff",
        border_color: str = "#cccccc",
        title: Optional[str] = None
    ) -> Optional[str]:
        """
        Create a signature pad for capturing digital signatures.
        
        Args:
            key: Unique key for the component
            height: Height of the signature pad in pixels
            clear_on_submit: Whether to clear the signature pad after submission
            line_color: Color of the signature line
            background_color: Background color of the signature pad
            border_color: Border color of the signature pad
            title: Optional title for the signature pad
            
        Returns:
            Base64 encoded signature image data or None if not signed
        """
        # Set up signature container
        if title:
            st.markdown(f"### {title}")
        
        # Initialize session state for signature data
        if f"{key}_signature_data" not in st.session_state:
            st.session_state[f"{key}_signature_data"] = None
        
        # Create signature pad HTML
        signature_pad_html = f"""
        <div style="margin-bottom: 10px;">
            <div id="{key}_signature_pad" style="border: 1px solid {border_color}; border-radius: 5px; 
                      background-color: {background_color}; width: 100%; height: {height}px;">
                <canvas id="{key}_signature_canvas" style="width: 100%; height: 100%;"></canvas>
            </div>
            <div style="margin-top: 10px; display: flex; justify-content: space-between;">
                <button id="{key}_clear_btn" style="padding: 5px 10px; border: none; background-color: #f8f9fa; border-radius: 5px; cursor: pointer;">
                    Clear
                </button>
                <button id="{key}_save_btn" style="padding: 5px 10px; border: none; background-color: #3e79f7; color: white; border-radius: 5px; cursor: pointer;">
                    Save Signature
                </button>
            </div>
        </div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/signature_pad/4.0.0/signature_pad.min.js"></script>
        <script>
            // Initialize signature pad
            var canvas = document.getElementById("{key}_signature_canvas");
            var signaturePad = new SignaturePad(canvas, {{
                backgroundColor: "{background_color}",
                penColor: "{line_color}"
            }});
            
            // Resize function to maintain aspect ratio
            function resizeCanvas() {{
                var ratio = Math.max(window.devicePixelRatio || 1, 1);
                canvas.width = canvas.offsetWidth * ratio;
                canvas.height = canvas.offsetHeight * ratio;
                canvas.getContext("2d").scale(ratio, ratio);
                signaturePad.clear();
            }}
            
            // Call resize on window resize
            window.addEventListener("resize", resizeCanvas);
            
            // Initial resize
            resizeCanvas();
            
            // Clear button handler
            document.getElementById("{key}_clear_btn").addEventListener("click", function() {{
                signaturePad.clear();
            }});
            
            // Save button handler
            document.getElementById("{key}_save_btn").addEventListener("click", function() {{
                if (!signaturePad.isEmpty()) {{
                    var signatureData = signaturePad.toDataURL();
                    
                    // Send to Streamlit
                    const data = {{
                        signature: signatureData,
                        key: "{key}_signature_data"
                    }};
                    window.parent.postMessage({{
                        type: "streamlit:setComponentValue",
                        value: data
                    }}, "*");
                    
                    {f"signaturePad.clear();" if clear_on_submit else ""}
                }}
            }});
        </script>
        """
        
        # Display signature pad
        st.components.v1.html(signature_pad_html, height=height+80)
        
        # Return signature data if available
        return st.session_state.get(f"{key}_signature_data")
    
    @staticmethod
    def create_signature_object(
        signer_name: str,
        signer_title: str,
        signer_email: str,
        document_id: str,
        signature_image: str,
        document_hash: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a digital signature object with metadata.
        
        Args:
            signer_name: Name of the signer
            signer_title: Title/role of the signer
            signer_email: Email of the signer
            document_id: ID of the document being signed
            signature_image: Base64 encoded signature image
            document_hash: Optional hash of the document content
            metadata: Optional additional metadata
            
        Returns:
            Digital signature object
        """
        # Generate timestamp
        timestamp = datetime.now().isoformat()
        
        # Create signature object
        signature = {
            "signature_id": DigitalSignature.generate_signature_id(),
            "signer": {
                "name": signer_name,
                "title": signer_title,
                "email": signer_email
            },
            "document": {
                "document_id": document_id,
                "hash": document_hash or "N/A"
            },
            "signature_image": signature_image,
            "timestamp": timestamp,
            "ip_address": "127.0.0.1",  # In a real app, you would capture the actual IP
            "metadata": metadata or {}
        }
        
        return signature
    
    @staticmethod
    def verify_signature(
        signature: Dict[str, Any],
        document_hash: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Verify a digital signature.
        
        Args:
            signature: The signature object to verify
            document_hash: Optional current hash of the document to verify against
            
        Returns:
            Tuple of (is_valid, message)
        """
        # In a real implementation, this would perform cryptographic verification
        # For this demo, we just check basic integrity
        
        # Check if signature has all required fields
        required_fields = ["signature_id", "signer", "document", "signature_image", "timestamp"]
        for field in required_fields:
            if field not in signature:
                return False, f"Signature missing required field: {field}"
        
        # Check signer fields
        signer_fields = ["name", "email"]
        for field in signer_fields:
            if field not in signature["signer"]:
                return False, f"Signer information missing required field: {field}"
        
        # Check document fields
        if "document_id" not in signature["document"]:
            return False, "Document information missing document_id"
        
        # If document hash is provided, verify it matches
        if document_hash and "hash" in signature["document"]:
            if signature["document"]["hash"] != document_hash and signature["document"]["hash"] != "N/A":
                return False, "Document has been modified since signing"
        
        return True, "Signature is valid"
    
    @staticmethod
    def render_signature_info(signature: Dict[str, Any], show_image: bool = True) -> None:
        """
        Render signature information in the Streamlit UI.
        
        Args:
            signature: The signature object to display
            show_image: Whether to show the signature image
        """
        st.markdown("### Digital Signature Information")
        
        # Create columns for layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Signer Details")
            st.markdown(f"**Name:** {signature['signer']['name']}")
            st.markdown(f"**Title:** {signature['signer'].get('title', 'N/A')}")
            st.markdown(f"**Email:** {signature['signer']['email']}")
        
        with col2:
            st.markdown("#### Signature Details")
            st.markdown(f"**Date:** {datetime.fromisoformat(signature['timestamp']).strftime('%B %d, %Y %I:%M %p')}")
            st.markdown(f"**Signature ID:** {signature['signature_id']}")
            
            # Verify the signature
            is_valid, message = DigitalSignature.verify_signature(signature)
            
            if is_valid:
                st.markdown(f"**Status:** <span style='color: #38d39f;'>✓ Valid</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"**Status:** <span style='color: #ff5b5b;'>✗ Invalid - {message}</span>", unsafe_allow_html=True)
        
        # Display signature image if requested
        if show_image and "signature_image" in signature:
            st.markdown("#### Signature")
            st.markdown(f"<img src='{signature['signature_image']}' style='max-height: 100px; border: 1px solid #eee; padding: 5px;'>", unsafe_allow_html=True)
        
        # Display additional metadata if available
        if "metadata" in signature and signature["metadata"]:
            st.markdown("#### Additional Information")
            for key, value in signature["metadata"].items():
                st.markdown(f"**{key}:** {value}")
    
    @staticmethod
    def collect_signature_form(
        document_id: str,
        document_title: str,
        document_hash: Optional[str] = None,
        key: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Collect a complete signature including form data and signature image.
        
        Args:
            document_id: ID of the document being signed
            document_title: Title of the document
            document_hash: Optional hash of the document content
            key: Optional unique key for the form
            
        Returns:
            Complete signature object or None if not submitted
        """
        if key is None:
            key = f"sig_form_{document_id}"
        
        st.markdown(f"## Sign Document: {document_title}")
        
        # Create form for signature information
        with st.form(key=f"{key}_form"):
            # Signer information
            st.markdown("### Signer Information")
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name", key=f"{key}_name")
                email = st.text_input("Email", key=f"{key}_email")
            
            with col2:
                title = st.text_input("Title/Role", key=f"{key}_title")
                company = st.text_input("Company", key=f"{key}_company")
            
            # Certification statement
            st.markdown("### Certification")
            st.markdown("""
            By signing this document electronically, I certify that:
            
            1. I am the person identified above
            2. I have read and understand the document
            3. My electronic signature is legally binding equivalent to my handwritten signature
            """)
            
            agree = st.checkbox("I agree to the terms above", key=f"{key}_agree")
            
            # Signature pad
            st.markdown("### Signature")
            signature_data = DigitalSignature.create_signature_pad(
                key=f"{key}_pad",
                height=150,
                title="Draw your signature below"
            )
            
            # Submit button
            submitted = st.form_submit_button("Sign Document")
            
            if submitted:
                if not name or not email or not title:
                    st.error("Please fill in all required fields.")
                    return None
                
                if not agree:
                    st.error("You must agree to the terms before signing.")
                    return None
                
                if not signature_data:
                    st.error("Please draw your signature before submitting.")
                    return None
                
                # Create complete signature object
                signature = DigitalSignature.create_signature_object(
                    signer_name=name,
                    signer_title=title,
                    signer_email=email,
                    document_id=document_id,
                    signature_image=signature_data,
                    document_hash=document_hash,
                    metadata={
                        "company": company,
                        "device_info": "Web Browser",
                        "agreement_version": "1.0"
                    }
                )
                
                return signature
        
        return None