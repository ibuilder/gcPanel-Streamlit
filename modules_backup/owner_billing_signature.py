"""
Highland Tower Development - Owner Bill Digital Signature Module
Integrated with AIA G702/G703 billing system and PostgreSQL database
"""

import streamlit as st
import json
import base64
from datetime import datetime
from database.migrations import get_db_connection, save_owner_bill_signature
from components.smart_tooltips import render_signature_guidance, create_interactive_help

def render_owner_bill_signature(bill_data):
    """Render digital signature interface for Highland Tower owner bills"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h2 style="color: white; margin: 0; font-size: 2rem; font-weight: 700;">
            ✍️ Digital Signature Required
        </h2>
        <p style="color: #e8f4fd; margin: 1rem 0 0 0; font-size: 1.1rem;">
            Highland Tower Development - Owner Bill Authorization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show bill summary before signature
    display_bill_summary(bill_data)
    
    # Signature guidance
    render_signature_guidance()
    
    # Digital signature interface
    render_signature_interface(bill_data)

def display_bill_summary(bill_data):
    """Display bill summary for review before signing"""
    
    st.markdown("### 📋 Bill Summary - Review Before Signing")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Application Number", f"#{bill_data.get('application_number', 'HTD-001')}")
        st.metric("Contract Amount", f"${bill_data.get('total_contract_amount', 45500000):,.2f}")
    
    with col2:
        st.metric("Work Completed", f"${bill_data.get('work_completed_to_date', 28650000):,.2f}")
        st.metric("Retainage", f"${bill_data.get('less_retainage', 1432500):,.2f}")
    
    with col3:
        st.metric("Amount Due", f"${bill_data.get('amount_due', 27217500):,.2f}")
        st.metric("Period Ending", bill_data.get('period_ending', '2025-01-31'))
    
    # Warning for large amounts
    amount_due = bill_data.get('amount_due', 0)
    if amount_due > 1000000:
        st.warning(f"⚠️ **Large Payment Alert**: This bill requests ${amount_due:,.2f} - requires authorized signature")

def render_signature_interface(bill_data):
    """Render the actual signature interface"""
    
    st.markdown("### ✍️ Authorization Required")
    
    # Check user authorization
    user_role = st.session_state.get('user_role', '')
    username = st.session_state.get('username', '')
    
    if user_role not in ['admin', 'project_manager', 'owner']:
        st.error("🚫 **Access Denied**: Only authorized Highland Tower personnel can sign owner bills")
        st.info("Contact your project manager for signature authorization")
        return
    
    # Signature input
    st.markdown("#### Your Digital Signature")
    
    signature_type = st.radio(
        "Signature Method",
        ["Typed Signature", "Electronic Signature"],
        horizontal=True
    )
    
    if signature_type == "Typed Signature":
        typed_signature = st.text_input(
            "Type your full legal name",
            placeholder="Enter your full name as it appears on official documents",
            help="This will serve as your digital signature for Highland Tower Development"
        )
        
        if typed_signature:
            st.markdown(f"""
            <div style="border: 1px dashed #666; padding: 15px; margin: 10px 0; 
                       font-family: cursive; font-size: 18px; text-align: center;">
                {typed_signature}
            </div>
            """, unsafe_allow_html=True)
    
    # Confirmation checkboxes
    st.markdown("#### Authorization Confirmation")
    
    confirmations = []
    confirmations.append(st.checkbox("I have reviewed all line items and amounts in this Highland Tower owner bill"))
    confirmations.append(st.checkbox("I confirm that all work has been completed as specified"))
    confirmations.append(st.checkbox("I am authorized to approve payments for Highland Tower Development"))
    confirmations.append(st.checkbox("I understand this digital signature is legally binding"))
    
    all_confirmed = all(confirmations)
    
    # Signature button
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button(
            "🔐 Sign Owner Bill", 
            type="primary", 
            disabled=not (typed_signature and all_confirmed),
            use_container_width=True
        ):
            if process_signature(bill_data, typed_signature, username):
                st.success("✅ **Owner Bill Signed Successfully!**")
                st.balloons()
                
                # Show completed signature
                display_completed_signature(typed_signature, username)
    
    with col2:
        st.button("❌ Cancel", use_container_width=True)

def process_signature(bill_data, signature, signed_by):
    """Process and save the digital signature"""
    
    signature_data = {
        "signature_text": signature,
        "signed_by": signed_by,
        "timestamp": datetime.now().isoformat(),
        "ip_address": "Highland Tower Network",
        "bill_details": {
            "application_number": bill_data.get('application_number'),
            "amount_due": bill_data.get('amount_due'),
            "period_ending": bill_data.get('period_ending')
        }
    }
    
    # Convert to base64 for database storage
    signature_json = json.dumps(signature_data)
    signature_base64 = base64.b64encode(signature_json.encode()).decode()
    
    # Save to database
    bill_id = bill_data.get('id', 1)
    success = save_owner_bill_signature(bill_id, signature_base64, signed_by)
    
    if success:
        # Update session state
        st.session_state[f"bill_{bill_id}_signed"] = True
        st.session_state[f"bill_{bill_id}_signature"] = signature_data
        return True
    else:
        st.error("❌ Signature save failed - please try again")
        return False

def display_completed_signature(signature, signed_by):
    """Display the completed signature information"""
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    st.markdown(f"""
    <div style="border: 3px solid #28a745; padding: 20px; border-radius: 12px; 
               background: #f8fff8; margin: 20px 0;">
        <h4 style="color: #28a745; margin: 0 0 15px 0;">🔐 Digital Signature Complete</h4>
        
        <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <div style="font-family: cursive; font-size: 20px; text-align: center; 
                       border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 10px;">
                {signature}
            </div>
            <div style="text-align: center; font-size: 12px; color: #666;">
                Digitally signed by {signed_by}<br>
                Highland Tower Development<br>
                Date: {current_time}
            </div>
        </div>
        
        <div style="margin-top: 15px; padding: 10px; background: #e8f5e8; border-radius: 6px;">
            <p style="margin: 0; font-size: 13px; color: #2d5a2d;">
                ✅ This owner bill has been digitally signed and submitted for processing.<br>
                📧 Confirmation email will be sent to Highland Tower project team.<br>
                📋 This signature is legally binding and cannot be modified.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def check_signature_status(bill_id):
    """Check if a bill has been signed"""
    
    return st.session_state.get(f"bill_{bill_id}_signed", False)

def get_signature_data(bill_id):
    """Get signature data for a signed bill"""
    
    return st.session_state.get(f"bill_{bill_id}_signature", None)

def render_signature_history():
    """Render signature history for Highland Tower bills"""
    
    st.markdown("### 📋 Signature History - Highland Tower Development")
    
    # Sample signature history
    signatures = [
        {"date": "2025-01-24", "bill": "HTD-APP-003", "amount": "$2,850,000", "signed_by": "John Smith"},
        {"date": "2025-01-20", "bill": "HTD-APP-002", "amount": "$2,650,000", "signed_by": "Jane Doe"},
        {"date": "2025-01-15", "bill": "HTD-APP-001", "amount": "$2,450,000", "signed_by": "Mike Johnson"}
    ]
    
    for sig in signatures:
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
        
        with col1:
            st.write(sig["date"])
        with col2:
            st.write(sig["bill"])
        with col3:
            st.write(sig["amount"])
        with col4:
            st.write(sig["signed_by"])
        with col5:
            st.button("📄", key=f"view_{sig['bill']}", help="View signed document")

if __name__ == "__main__":
    # Sample bill data for testing
    sample_bill = {
        "id": 1,
        "application_number": "HTD-APP-004",
        "total_contract_amount": 45500000,
        "work_completed_to_date": 28650000,
        "less_retainage": 1432500,
        "amount_due": 27217500,
        "period_ending": "2025-01-31"
    }
    
    render_owner_bill_signature(sample_bill)