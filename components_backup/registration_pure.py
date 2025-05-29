"""
Pure Python Registration Component for gcPanel

This module provides a clean registration interface using only Streamlit's
native Python components, avoiding HTML/CSS/JS dependencies.
"""
import streamlit as st

def render_registration_request():
    """Render a pure Python registration request form using Streamlit components."""
    
    # Main header
    st.header("Request Project Access")
    
    # Information notice
    st.info("**Note:** Registration for Highland Tower Development is managed by your project administrator.")
    
    # Instructions
    st.write("To request access, please contact your project manager with the following information:")
    
    # Required information section using columns for better layout
    st.subheader("Required Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**👤 Personal Information**")
        st.write("• Full Name & Professional Credentials")
        st.write("• Corporate Email Address")
        
    with col2:
        st.markdown("**🏢 Company Information**")
        st.write("• Company Name & Address")
        st.write("• Project Role & Responsibilities")
    
    # Contact form section
    st.subheader("Contact Information")
    
    # Create expandable section for contact details
    with st.expander("📧 Project Manager Contact Details", expanded=True):
        st.write("**Primary Contact:** John Smith, Project Manager")
        st.write("**Email:** j.smith@highlandtower.com")
        st.write("**Phone:** (555) 123-4567")
        st.write("**Office Hours:** Monday - Friday, 8:00 AM - 6:00 PM EST")
    
    # Process information
    st.subheader("Access Process")
    
    # Use Streamlit's native success box for process steps
    st.success("📝 **Step 1:** Submit your information to the project manager")
    st.info("🔍 **Step 2:** Your credentials and role will be verified")
    st.warning("⏳ **Step 3:** Account setup typically takes 1-2 business days")
    st.success("📧 **Step 4:** You'll receive login credentials via email once approved")
    
    # Quick contact form (optional)
    st.subheader("Quick Contact Form")
    st.write("Alternatively, you can submit a quick request here:")
    
    with st.form("registration_request"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *")
            company = st.text_input("Company Name *")
            
        with col2:
            email = st.text_input("Email Address *")
            role = st.selectbox("Project Role *", 
                               ["Select Role", "General Contractor", "Subcontractor", 
                                "Architect", "Engineer", "Owner Representative", "Consultant"])
        
        message = st.text_area("Additional Information", 
                              placeholder="Please provide any additional details about your role or access requirements...")
        
        # Submit button
        submitted = st.form_submit_button("Submit Access Request", type="primary")
        
        if submitted:
            if full_name and company and email and role != "Select Role":
                st.success("✅ Your access request has been submitted successfully!")
                st.info("You will receive a confirmation email shortly, and the project manager will contact you within 24 hours.")
                
                # Display submitted information for confirmation
                with st.expander("📋 Request Summary", expanded=True):
                    st.write(f"**Name:** {full_name}")
                    st.write(f"**Company:** {company}")
                    st.write(f"**Email:** {email}")
                    st.write(f"**Role:** {role}")
                    if message:
                        st.write(f"**Additional Info:** {message}")
            else:
                st.error("❌ Please fill in all required fields marked with *")
    
    # Additional resources
    st.subheader("Additional Resources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📖 Project Documentation**")
        st.write("Access project specs and drawings after approval")
        
    with col2:
        st.markdown("**🔧 System Requirements**")
        st.write("Modern web browser with JavaScript enabled")
        
    with col3:
        st.markdown("**💬 Support**")
        st.write("Technical support available during business hours")
    
    # Footer information
    st.markdown("---")
    st.markdown("**Highland Tower Development** - Construction Management Platform")
    st.caption("For technical issues or questions, contact support@gcpanel.co")

def render_demo_accounts_pure():
    """Render demo accounts section using pure Python components."""
    
    st.subheader("🎯 Demo Accounts")
    st.write("Try the platform with these pre-configured demo accounts:")
    
    # Demo accounts data
    demo_accounts = [
        {
            "role": "Project Manager",
            "username": "demo_pm",
            "password": "demo123",
            "access": "Full access to all modules and project data",
            "color": "blue"
        },
        {
            "role": "Site Supervisor",
            "username": "demo_super",
            "password": "demo123", 
            "access": "Field operations, safety, and daily reporting",
            "color": "green"
        },
        {
            "role": "Subcontractor",
            "username": "demo_sub",
            "password": "demo123",
            "access": "Limited access to relevant contracts and documents",
            "color": "orange"
        }
    ]
    
    # Display each demo account
    for i, account in enumerate(demo_accounts):
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"**{account['role']}**")
                st.write(f"👤 Username: `{account['username']}`")
                st.write(f"🔑 Password: `{account['password']}`")
                
            with col2:
                st.write(f"**Access Level:**")
                st.write(account['access'])
                
            with col3:
                if st.button(f"Login as {account['role']}", 
                           key=f"demo_login_{i}", 
                           type="secondary"):
                    # Store demo login in session state
                    st.session_state.login_username = account['username']
                    st.session_state.login_password = account['password'] 
                    st.session_state.login_form_submitted = True
                    st.success(f"Logging in as {account['role']}...")
                    st.rerun()
            
            # Add separator except for last item
            if i < len(demo_accounts) - 1:
                st.markdown("---")
    
    # Information about demo accounts
    st.info("💡 **Note:** Demo accounts are reset daily and contain sample project data for evaluation purposes.")

if __name__ == "__main__":
    # For testing purposes
    st.title("gcPanel Registration - Pure Python Version")
    
    tab1, tab2 = st.tabs(["Registration Request", "Demo Accounts"])
    
    with tab1:
        render_registration_request()
        
    with tab2:
        render_demo_accounts_pure()