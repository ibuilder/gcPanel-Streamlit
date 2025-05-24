"""
Help Page for Highland Tower Development - gcPanel

Comprehensive FAQ and support information for the construction management platform.
"""

import streamlit as st

def render_help_page():
    """Render the help page with FAQ and support information."""
    
    st.title("❓ Help & Support - Highland Tower Development")
    
    st.markdown("""
    Welcome to the Highland Tower Development help center. Find answers to common questions 
    and learn how to make the most of your construction management platform.
    """)
    
    # Quick navigation
    st.markdown("### Quick Navigation")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏗️ Getting Started", use_container_width=True, key="help_start"):
            st.session_state["help_section"] = "getting_started"
    with col2:
        if st.button("❓ FAQ", use_container_width=True, key="help_faq"):
            st.session_state["help_section"] = "faq"
    with col3:
        if st.button("🌐 Community Support", use_container_width=True, key="help_community"):
            st.session_state["help_section"] = "community"
    
    st.divider()
    
    # Get current section
    current_section = st.session_state.get("help_section", "getting_started")
    
    if current_section == "getting_started":
        render_getting_started()
    elif current_section == "faq":
        render_faq()
    elif current_section == "community":
        render_community_support()

def render_getting_started():
    """Render getting started section."""
    st.markdown("## 🏗️ Getting Started with Highland Tower Development")
    
    st.markdown("""
    ### About gcPanel Construction Management Platform
    
    gcPanel is a comprehensive construction management platform designed specifically for 
    projects like Highland Tower Development. This $45.5M mixed-use project showcases 
    the full capabilities of modern construction management technology.
    
    **Project Overview:**
    - **Value:** $45.5M Mixed-Use Development
    - **Scale:** 120 Residential + 8 Retail Units
    - **Size:** 168,500 sq ft
    - **Structure:** 15 Stories Above + 2 Below Ground
    
    ### Key Features:
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **📊 Dashboard & Analytics**
        - Real-time project metrics
        - Progress tracking
        - Budget monitoring
        - Safety performance
        
        **📋 Project Management**
        - Preconstruction planning
        - Engineering documentation
        - Field operations tracking
        """)
    
    with col2:
        st.markdown("""
        **🦺 Safety & Compliance**
        - Safety incident tracking
        - Compliance monitoring
        - Risk assessment tools
        
        **💰 Financial Management**
        - Cost tracking and analysis
        - Budget variance reporting
        - Contract management
        """)
    
    st.markdown("""
    ### Navigation Guide:
    - Use the sidebar navigation to switch between modules
    - Each module has specific tools for different aspects of construction management
    - Access your user profile and project information in the sidebar
    """)

def render_faq():
    """Render FAQ section."""
    st.markdown("## ❓ Frequently Asked Questions")
    
    # FAQ data
    faqs = [
        {
            "question": "How do I navigate between different modules?",
            "answer": "Use the dropdown navigation menu in the sidebar. Each module (Dashboard, Analytics, Safety, etc.) has specific tools for different aspects of construction management."
        },
        {
            "question": "What project information is available in gcPanel?",
            "answer": "You can view comprehensive project details including budget status, schedule progress, safety metrics, and team information. The Highland Tower Development project data is displayed throughout the platform."
        },
        {
            "question": "How do I track project progress?",
            "answer": "The Dashboard module provides real-time metrics showing overall progress, budget status, schedule adherence, and safety performance. Use the Analytics module for detailed reporting."
        },
        {
            "question": "What safety features are available?",
            "answer": "The Safety module includes incident tracking, compliance monitoring, safety score tracking, and risk assessment tools. All safety data is integrated into the main dashboard."
        },
        {
            "question": "How do I manage project documents?",
            "answer": "The Documents module provides centralized storage and management for all project files including drawings, specifications, contracts, and reports."
        },
        {
            "question": "Can I view BIM models in gcPanel?",
            "answer": "Yes, the BIM module provides 3D model viewing capabilities and integration with Building Information Modeling workflows for the Highland Tower Development."
        },
        {
            "question": "How do I track costs and budgets?",
            "answer": "Use the Cost Management module to monitor budget performance, track expenses, analyze cost variances, and manage financial aspects of the project."
        },
        {
            "question": "What user roles are available?",
            "answer": "gcPanel supports various user roles including Project Manager, Site Supervisor, Safety Officer, and other construction team roles with appropriate access permissions."
        },
        {
            "question": "How do I access field operations data?",
            "answer": "The Field Operations module provides tools for daily activity tracking, progress reporting, resource management, and on-site coordination."
        },
        {
            "question": "Is there mobile support?",
            "answer": "Yes, gcPanel is optimized for mobile devices, allowing field teams to access project information and update data from construction sites."
        }
    ]
    
    # Display FAQs
    for i, faq in enumerate(faqs):
        with st.expander(f"**{faq['question']}**"):
            st.markdown(faq['answer'])

def render_community_support():
    """Render community support section."""
    st.markdown("## 🌐 Community Support")
    
    st.markdown("""
    ### Get Help from the gcPanel Community
    
    Join thousands of construction professionals using gcPanel for project management 
    and collaboration. Our community is here to help you succeed.
    """)
    
    # Community support options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🌐 Visit Our Website
        
        For comprehensive support, documentation, and community resources:
        
        **[www.gcpanel.co](https://www.gcpanel.co)**
        
        - Complete user guides
        - Video tutorials
        - Best practices
        - Feature updates
        - Community forums
        """)
    
    with col2:
        st.markdown("""
        ### 💬 Community Features
        
        - **Discussion Forums:** Connect with other users
        - **Knowledge Base:** Searchable help articles  
        - **Video Library:** Step-by-step tutorials
        - **Best Practices:** Industry expert insights
        - **Feature Requests:** Suggest improvements
        """)
    
    st.divider()
    
    st.markdown("""
    ### 📞 Additional Support Options
    
    - **Documentation:** Comprehensive guides available at www.gcpanel.co
    - **Community Forums:** Ask questions and share experiences
    - **Knowledge Base:** Search for specific topics and solutions
    - **Video Tutorials:** Visual guides for all major features
    """)
    
    # Call to action
    st.info("💡 **Tip:** Visit www.gcpanel.co to access the latest documentation, connect with other construction professionals, and stay updated on new features!")
    
    if st.button("🌐 Visit www.gcpanel.co", use_container_width=True, key="visit_website"):
        st.success("Opening www.gcpanel.co in a new tab...")
        st.markdown("**[Click here to visit www.gcpanel.co](https://www.gcpanel.co)**")

def render_help_login():
    """Render help page for login/authentication issues."""
    st.title("🔐 Login Help")
    
    st.markdown("""
    ### Having trouble logging in?
    
    **Demo Accounts Available:**
    - Use the demo account options on the login page
    - No registration required for demonstration
    
    **For Production Access:**
    - Contact your project administrator
    - Visit www.gcpanel.co for account setup
    
    **Technical Issues:**
    - Clear your browser cache
    - Try a different browser
    - Check www.gcpanel.co for system status
    """)
    
    if st.button("🔙 Back to Login", use_container_width=True):
        st.session_state["show_help"] = False
        st.rerun()