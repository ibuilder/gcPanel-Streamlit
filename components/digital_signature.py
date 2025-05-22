"""
Digital Signature Component for gcPanel.

This component provides digital signature functionality for forms requiring
approval and authentication including T&M tickets, change orders, invoices,
and daily reports.
"""

import streamlit as st
from datetime import datetime
import base64
import hashlib

def render_digital_signature_section(form_type="document", required_signatures=None):
    """
    Render digital signature section for forms.
    
    Args:
        form_type (str): Type of form (tm_ticket, change_order, invoice, daily_report, etc.)
        required_signatures (list): List of required signature roles
    """
    if required_signatures is None:
        required_signatures = ["Supervisor", "Project Manager"]
    
    st.markdown("---")
    st.markdown("### ✍️ Digital Signatures")
    st.markdown("*Required signatures for approval and authentication*")
    
    # Initialize session state for signatures
    signature_key = f"{form_type}_signatures"
    if signature_key not in st.session_state:
        st.session_state[signature_key] = {}
    
    signatures = st.session_state[signature_key]
    
    # Create signature fields for each required role
    for i, role in enumerate(required_signatures):
        with st.container():
            st.markdown(f"#### {role} Signature")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Signature name input
                signature_name = st.text_input(
                    f"{role} Name",
                    key=f"{form_type}_sig_name_{i}",
                    placeholder=f"Enter {role.lower()} name",
                    value=signatures.get(role, {}).get('name', '')
                )
                
                # Signature date/time (auto-populated when signed)
                signature_datetime = signatures.get(role, {}).get('datetime', '')
                if signature_datetime:
                    st.text_input(
                        f"Signed Date/Time",
                        value=signature_datetime,
                        disabled=True,
                        key=f"{form_type}_sig_datetime_{i}"
                    )
            
            with col2:
                # Digital signature button
                if role not in signatures or not signatures[role].get('signed', False):
                    if st.button(f"🖊️ Sign as {role}", key=f"{form_type}_sign_{i}"):
                        if signature_name.strip():
                            # Create digital signature
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            signature_data = {
                                'name': signature_name,
                                'role': role,
                                'datetime': timestamp,
                                'signed': True,
                                'signature_hash': generate_signature_hash(signature_name, role, timestamp)
                            }
                            
                            signatures[role] = signature_data
                            st.session_state[signature_key] = signatures
                            st.success(f"Document signed by {signature_name} as {role}")
                            st.rerun()
                        else:
                            st.error(f"Please enter {role.lower()} name before signing")
                else:
                    # Show signed status
                    st.success("✅ Signed")
                    if st.button(f"Clear", key=f"{form_type}_clear_{i}"):
                        del signatures[role]
                        st.session_state[signature_key] = signatures
                        st.rerun()
            
            # Show signature details if signed
            if role in signatures and signatures[role].get('signed', False):
                sig_data = signatures[role]
                st.markdown(f"""
                <div style="background-color: #f0f9ff; border-left: 4px solid #0284c7; padding: 12px; margin-top: 8px;">
                    <strong>Digitally Signed by:</strong> {sig_data['name']}<br>
                    <strong>Role:</strong> {sig_data['role']}<br>
                    <strong>Date/Time:</strong> {sig_data['datetime']}<br>
                    <strong>Signature ID:</strong> {sig_data['signature_hash'][:12]}...
                </div>
                """, unsafe_allow_html=True)
    
    # Signature validation status
    st.markdown("---")
    render_signature_validation_status(signatures, required_signatures)
    
    return signatures

def render_signature_validation_status(signatures, required_signatures):
    """Render the overall signature validation status."""
    signed_count = sum(1 for role in required_signatures if role in signatures and signatures[role].get('signed', False))
    total_required = len(required_signatures)
    
    if signed_count == total_required:
        st.success(f"✅ All required signatures obtained ({signed_count}/{total_required})")
        st.markdown("*This document is fully authorized and approved.*")
    elif signed_count > 0:
        st.warning(f"⏳ Partial signatures obtained ({signed_count}/{total_required})")
        missing_roles = [role for role in required_signatures if role not in signatures or not signatures[role].get('signed', False)]
        st.markdown(f"*Missing signatures from: {', '.join(missing_roles)}*")
    else:
        st.error(f"❌ No signatures obtained (0/{total_required})")
        st.markdown("*This document requires digital signatures before submission.*")

def generate_signature_hash(name, role, timestamp):
    """Generate a unique hash for the digital signature."""
    signature_string = f"{name}_{role}_{timestamp}_{st.session_state.get('user_email', 'unknown')}"
    return hashlib.sha256(signature_string.encode()).hexdigest()

def get_signature_summary(signatures):
    """Get a summary of signatures for saving to data."""
    summary = {}
    for role, sig_data in signatures.items():
        if sig_data.get('signed', False):
            summary[role] = {
                'name': sig_data['name'],
                'datetime': sig_data['datetime'],
                'signature_hash': sig_data['signature_hash']
            }
    return summary

def validate_required_signatures(signatures, required_signatures):
    """Validate that all required signatures are present."""
    for role in required_signatures:
        if role not in signatures or not signatures[role].get('signed', False):
            return False, f"Missing signature from {role}"
    return True, "All required signatures present"

def render_signature_verification(signature_data):
    """Render signature verification information for viewing saved documents."""
    if not signature_data:
        st.info("No digital signatures on file for this document.")
        return
    
    st.markdown("### 🔐 Digital Signature Verification")
    
    for role, sig_info in signature_data.items():
        st.markdown(f"""
        <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px; margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="color: #1e40af;">{role}</strong><br>
                    <span style="color: #475569;">Signed by: {sig_info.get('name', 'Unknown')}</span><br>
                    <small style="color: #64748b;">Date: {sig_info.get('datetime', 'Unknown')}</small>
                </div>
                <div style="color: #059669; font-size: 24px;">✓</div>
            </div>
            <div style="margin-top: 8px;">
                <small style="color: #64748b; font-family: monospace;">
                    Signature ID: {sig_info.get('signature_hash', 'Unknown')[:16]}...
                </small>
            </div>
        </div>
        """, unsafe_allow_html=True)