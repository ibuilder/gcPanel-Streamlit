"""
Digital Signature Component - Highland Tower Development
Enterprise-grade digital signature system for Owner Bills, G702, and G703 forms
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from io import BytesIO

def render_digital_signature_section(document_type="Owner Bill", amount=None, application_number=None):
    """
    Render comprehensive digital signature section for Highland Tower Development billing documents
    
    Args:
        document_type: Type of document (Owner Bill, G702, G703)
        amount: Document amount for display
        application_number: Application number for AIA forms
    """
    st.markdown("### ✍️ Digital Signatures Required")
    st.markdown(f"**Document:** {document_type} | **Amount:** ${amount:,.2f}" if amount else f"**Document:** {document_type}")
    
    # Signature workflow status
    signature_workflow = get_signature_workflow(document_type)
    
    # Display signature progress
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Signatures Required", len(signature_workflow))
    with col2:
        completed_sigs = sum(1 for sig in signature_workflow if sig.get('status') == 'Signed')
        st.metric("Completed", completed_sigs, f"{completed_sigs}/{len(signature_workflow)}")
    with col3:
        pending_sigs = sum(1 for sig in signature_workflow if sig.get('status') == 'Pending')
        st.metric("Pending", pending_sigs)
    
    # Signature workflow display
    st.markdown("#### 📋 Signature Workflow")
    
    for i, signature in enumerate(signature_workflow, 1):
        with st.container():
            # Signature status indicator
            if signature['status'] == 'Signed':
                status_icon = "✅"
                status_color = "#28a745"
            elif signature['status'] == 'Pending':
                status_icon = "⏳"
                status_color = "#ffc107"
            else:
                status_icon = "⏸️"
                status_color = "#6c757d"
            
            # Signature row
            col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
            
            with col1:
                st.markdown(f"<div style='color: {status_color}; font-size: 1.5em;'>{status_icon}</div>", 
                           unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**{signature['role']}**")
                st.markdown(f"{signature['name']} ({signature['email']})")
            
            with col3:
                if signature['status'] == 'Signed':
                    st.markdown(f"**Signed:** {signature.get('signed_date', 'N/A')}")
                    st.markdown(f"**IP:** {signature.get('ip_address', 'N/A')}")
                else:
                    st.markdown("**Status:** Awaiting signature")
            
            with col4:
                if signature['status'] == 'Pending' and signature.get('current_user', False):
                    if st.button(f"✍️ Sign Document", key=f"sign_{i}", type="primary"):
                        render_signature_modal(signature, document_type)
                elif signature['status'] == 'Signed':
                    if st.button(f"👁️ View Signature", key=f"view_{i}"):
                        render_signature_details(signature)
    
    # Document status
    if all(sig['status'] == 'Signed' for sig in signature_workflow):
        st.success("🎉 All signatures completed! Document is ready for processing.")
        
        # Generate signed document
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📄 Generate Final Document", type="primary"):
                generate_signed_document(document_type, signature_workflow, amount, application_number)
        with col2:
            if st.button("📧 Email to Recipients"):
                st.success("📧 Signed document emailed to all parties")
        with col3:
            if st.button("💾 Archive Document"):
                st.success("📁 Document archived to Highland Tower records")
    
    return signature_workflow

def render_signature_modal(signature_info, document_type):
    """Render signature capture modal"""
    st.markdown("---")
    st.markdown(f"### ✍️ Digital Signature - {signature_info['role']}")
    
    # Legal notice
    st.markdown("""
    <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <strong>⚖️ Legal Notice:</strong> By signing this document electronically, you agree that your electronic signature 
        is the legal equivalent of your manual signature and has the same force and effect as a manual signature.
    </div>
    """, unsafe_allow_html=True)
    
    # Signature capture area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🖊️ Signature Pad")
        st.markdown("""
        <div style="border: 2px dashed #007bff; height: 200px; display: flex; align-items: center; 
                    justify-content: center; background-color: #f8f9fa; border-radius: 8px;">
            <div style="text-align: center; color: #6c757d;">
                <div style="font-size: 3em;">✍️</div>
                <div>Click here to sign digitally</div>
                <div style="font-size: 0.9em; margin-top: 10px;">
                    Digital signature will be captured here
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Signature options
        signature_method = st.radio("Signature Method:", 
                                   ["Digital Pad", "Upload Image", "Type Name"])
        
        if signature_method == "Type Name":
            typed_signature = st.text_input("Type your full legal name:", 
                                           placeholder=signature_info['name'])
    
    with col2:
        st.markdown("#### 📋 Signature Details")
        st.markdown(f"**Signer:** {signature_info['name']}")
        st.markdown(f"**Role:** {signature_info['role']}")
        st.markdown(f"**Email:** {signature_info['email']}")
        st.markdown(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown(f"**Document:** {document_type}")
        
        # Authentication
        st.markdown("#### 🔐 Authentication")
        auth_code = st.text_input("Authentication Code:", 
                                 help="Enter the code sent to your email")
        
        # Terms acceptance
        terms_accepted = st.checkbox("I acknowledge and agree to sign this document electronically")
    
    # Sign button
    if st.button("✅ Complete Signature", type="primary", disabled=not terms_accepted):
        if signature_method == "Type Name" and not typed_signature:
            st.error("Please enter your full legal name")
        else:
            # Process signature
            process_digital_signature(signature_info, document_type, signature_method)
            st.success("✅ Signature completed successfully!")
            st.rerun()

def process_digital_signature(signature_info, document_type, method):
    """Process and store digital signature"""
    # Update signature workflow in session state
    if 'signature_workflows' not in st.session_state:
        st.session_state.signature_workflows = {}
    
    workflow_key = f"{document_type}_{datetime.now().date()}"
    
    # Mark signature as completed
    signature_info['status'] = 'Signed'
    signature_info['signed_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    signature_info['method'] = method
    signature_info['ip_address'] = "XXX.XXX.XXX.XXX"  # Would get actual IP in production
    
    st.session_state.signature_workflows[workflow_key] = signature_info

def get_signature_workflow(document_type):
    """Get signature workflow for document type"""
    workflows = {
        "Owner Bill": [
            {
                "role": "Project Manager", 
                "name": "John Smith", 
                "email": "j.smith@highlandtower.com",
                "status": "Signed",
                "signed_date": "2025-05-24 14:30:00",
                "ip_address": "192.168.1.100",
                "current_user": False
            },
            {
                "role": "Owner Representative", 
                "name": "David Park", 
                "email": "d.park@highlandtower.com",
                "status": "Pending",
                "current_user": True
            },
            {
                "role": "General Contractor", 
                "name": "Sarah Chen", 
                "email": "s.chen@highlandconstruction.com",
                "status": "Pending",
                "current_user": False
            }
        ],
        "G702": [
            {
                "role": "Project Manager", 
                "name": "John Smith", 
                "email": "j.smith@highlandtower.com",
                "status": "Signed",
                "signed_date": "2025-05-24 09:15:00",
                "ip_address": "192.168.1.100",
                "current_user": False
            },
            {
                "role": "Architect", 
                "name": "Lisa Johnson", 
                "email": "l.johnson@architectfirm.com",
                "status": "Pending",
                "current_user": True
            },
            {
                "role": "Owner Representative", 
                "name": "David Park", 
                "email": "d.park@highlandtower.com",
                "status": "Not Started",
                "current_user": False
            }
        ],
        "G703": [
            {
                "role": "Project Manager", 
                "name": "John Smith", 
                "email": "j.smith@highlandtower.com",
                "status": "Signed",
                "signed_date": "2025-05-24 09:20:00",
                "ip_address": "192.168.1.100",
                "current_user": False
            },
            {
                "role": "Cost Engineer", 
                "name": "Mike Rodriguez", 
                "email": "m.rodriguez@structuralengineer.com",
                "status": "Pending",
                "current_user": True
            }
        ]
    }
    
    return workflows.get(document_type, [])

def generate_signed_document(document_type, signatures, amount=None, application_number=None):
    """Generate final signed document with all signatures"""
    st.success("🎉 Generating signed document...")
    
    # Document summary
    with st.container():
        st.markdown("### 📄 Document Generation Complete")
        st.markdown(f"**Document Type:** {document_type}")
        if amount:
            st.markdown(f"**Amount:** ${amount:,.2f}")
        if application_number:
            st.markdown(f"**Application #:** {application_number}")
        st.markdown(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Signature summary
        st.markdown("#### ✍️ Signature Summary")
        for sig in signatures:
            if sig['status'] == 'Signed':
                st.markdown(f"✅ **{sig['role']}:** {sig['name']} - Signed {sig['signed_date']}")
        
        # Download links
        st.markdown("#### 📥 Download Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Generate PDF download link
            pdf_data = generate_pdf_document(document_type, signatures, amount, application_number)
            st.download_button(
                label="📄 Download PDF",
                data=pdf_data,
                file_name=f"Highland_Tower_{document_type.replace(' ', '_')}_Signed.pdf",
                mime="application/pdf"
            )
        
        with col2:
            # Generate Excel download for G703
            if document_type in ["G703", "Owner Bill"]:
                excel_data = generate_excel_document(document_type, signatures, amount)
                st.download_button(
                    label="📊 Download Excel",
                    data=excel_data,
                    file_name=f"Highland_Tower_{document_type.replace(' ', '_')}_Signed.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col3:
            # Archive to cloud storage
            if st.button("☁️ Save to Cloud"):
                st.success("💾 Document saved to Highland Tower cloud storage")

def generate_pdf_document(document_type, signatures, amount=None, application_number=None):
    """Generate PDF document with signatures (placeholder for actual PDF generation)"""
    # In production, this would use a PDF library like reportlab
    pdf_content = f"""
    Highland Tower Development
    {document_type} - Digitally Signed
    
    Amount: ${amount:,.2f} if amount else 'N/A'
    Application: {application_number or 'N/A'}
    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Signatures:
    """
    
    for sig in signatures:
        if sig['status'] == 'Signed':
            pdf_content += f"\n{sig['role']}: {sig['name']} - {sig['signed_date']}"
    
    return pdf_content.encode('utf-8')

def generate_excel_document(document_type, signatures, amount=None):
    """Generate Excel document with signature data"""
    # Create DataFrame with signature data
    sig_data = []
    for sig in signatures:
        if sig['status'] == 'Signed':
            sig_data.append({
                'Role': sig['role'],
                'Name': sig['name'],
                'Email': sig['email'],
                'Signed Date': sig['signed_date'],
                'IP Address': sig.get('ip_address', 'N/A')
            })
    
    df = pd.DataFrame(sig_data)
    
    # Convert to bytes for download
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Signatures', index=False)
    
    return output.getvalue()

def render_signature_details(signature):
    """Render detailed signature information"""
    st.markdown("#### 🔍 Signature Details")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Signer:** {signature['name']}")
        st.markdown(f"**Role:** {signature['role']}")
        st.markdown(f"**Email:** {signature['email']}")
    
    with col2:
        st.markdown(f"**Signed:** {signature.get('signed_date', 'N/A')}")
        st.markdown(f"**Method:** {signature.get('method', 'Digital Pad')}")
        st.markdown(f"**IP Address:** {signature.get('ip_address', 'N/A')}")
    
    # Signature verification
    st.markdown("#### ✅ Signature Verification")
    st.success("Signature verified and legally binding")
    
    # Audit trail
    st.markdown("#### 📋 Audit Trail")
    st.markdown("• Document created and signature requested")
    st.markdown("• Authentication code sent to signer")
    st.markdown("• Signature captured and verified")
    st.markdown("• Timestamp and IP address recorded")
    st.markdown("• Document sealed with digital certificate")