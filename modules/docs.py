"""
Highland Tower Development - Documentation Module
Public documentation accessible without login
"""

import streamlit as st

def render():
    """Render the documentation module"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: 700;">
            📚 Highland Tower Development
        </h1>
        <p style="color: #e8f4fd; margin: 1rem 0 0 0; font-size: 1.2rem;">
            Construction Management Platform Documentation
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs for documentation
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏗️ Project Overview", "📖 User Guide", "🔧 Features", "❓ FAQ", "📞 Support"
    ])
    
    with tab1:
        render_project_overview()
    
    with tab2:
        render_user_guide()
    
    with tab3:
        render_features_guide()
    
    with tab4:
        render_faq()
    
    with tab5:
        render_support()

def render_project_overview():
    """Render Highland Tower project overview"""
    
    st.markdown("## 🏗️ Highland Tower Development Project")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Project Details
        
        **Highland Tower Development** is a $45.5M mixed-use construction project featuring:
        
        - **120 Residential Units** across 15 floors above ground
        - **8 Retail Spaces** at street level
        - **2 Below-ground levels** for parking and utilities
        - **168,500 total square feet** of construction
        - **24-month construction timeline**
        
        ### Project Status
        - ✅ **67.3% Complete** - ahead of schedule
        - 💰 **$2.1M Under Budget** - exceptional cost management
        - 🦺 **98.5% OSHA Compliance** - industry-leading safety
        - 📋 **23 Active RFIs** - managed through our system
        """)
    
    with col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #1e3c72;">
            <h4 style="color: #1e3c72; margin-top: 0;">Key Metrics</h4>
            <p><strong>Project Value:</strong> $45.5M</p>
            <p><strong>Completion:</strong> 67.3%</p>
            <p><strong>Schedule:</strong> 5 days ahead</p>
            <p><strong>Budget:</strong> $2.1M under</p>
            <p><strong>Safety Score:</strong> 98.5%</p>
            <p><strong>Quality Score:</strong> 96.2%</p>
        </div>
        """, unsafe_allow_html=True)

def render_user_guide():
    """Render user guide and getting started information"""
    
    st.markdown("## 📖 User Guide - Getting Started")
    
    st.markdown("### 🔐 Accessing the System")
    
    st.info("""
    **Login Required**: The Highland Tower Construction Management Platform requires authentication. 
    Contact your project manager for login credentials.
    """)
    
    st.markdown("### 🎯 Module Overview")
    
    modules_info = [
        {
            "category": "⚡ Core Tools",
            "modules": [
                ("📊 Dashboard", "Real-time project overview and key metrics"),
                ("📝 Daily Reports", "Submit and review daily field reports"),
                ("🚛 Deliveries", "Track material deliveries and shipments"),
                ("🦺 Safety", "Safety incident tracking and compliance")
            ]
        },
        {
            "category": "🎯 Project Management", 
            "modules": [
                ("🏗️ PreConstruction", "Planning, estimating, and design coordination"),
                ("⚙️ Engineering", "RFIs, technical documents, specifications"),
                ("👷 Field Operations", "Crew management and field coordination"),
                ("📋 Contracts", "Contract administration and change orders"),
                ("💰 Cost Management", "AIA billing, budget tracking, financials"),
                ("🏢 BIM", "3D model coordination and clash detection"),
                ("✅ Closeout", "Project completion and handover processes")
            ]
        },
        {
            "category": "🔧 Advanced Tools",
            "modules": [
                ("❓ RFIs", "Request for Information management"),
                ("📤 Submittals", "Submittal review and approval workflow"),
                ("📅 Scheduling", "Project timeline and milestone tracking"),
                ("🔍 Quality Control", "Inspection workflows and compliance"),
                ("📸 Progress Photos", "Site documentation with GPS tagging")
            ]
        }
    ]
    
    for category_info in modules_info:
        st.markdown(f"#### {category_info['category']}")
        for module_name, description in category_info['modules']:
            st.markdown(f"**{module_name}**: {description}")
        st.markdown("---")

def render_features_guide():
    """Render detailed features guide"""
    
    st.markdown("## 🔧 Platform Features")
    
    # Feature categories
    feature_sections = [
        {
            "title": "📊 Real-Time Analytics",
            "features": [
                "Live project dashboard with KPIs",
                "Cost variance tracking and forecasting", 
                "Schedule performance monitoring",
                "Safety compliance metrics",
                "Quality control analytics"
            ]
        },
        {
            "title": "📱 Mobile-Optimized",
            "features": [
                "Responsive design for field use",
                "GPS-enabled photo documentation",
                "Offline data entry capabilities",
                "Voice-to-text report submission",
                "Real-time synchronization"
            ]
        },
        {
            "title": "🔐 Security & Compliance",
            "features": [
                "Role-based access control",
                "Digital signature capabilities",
                "Audit trail for all actions",
                "OSHA compliance tracking",
                "Document version control"
            ]
        },
        {
            "title": "🤖 AI-Powered Features",
            "features": [
                "Smart tooltip guidance system",
                "Predictive cost analytics",
                "Automated quality checks",
                "Intelligent document search",
                "Performance snapshot generation"
            ]
        }
    ]
    
    for section in feature_sections:
        with st.expander(section["title"], expanded=True):
            for feature in section["features"]:
                st.markdown(f"• {feature}")

def render_faq():
    """Render frequently asked questions"""
    
    st.markdown("## ❓ Frequently Asked Questions")
    
    faqs = [
        {
            "question": "How do I get access to the Highland Tower platform?",
            "answer": "Contact your project manager or Highland Tower Development administration team for login credentials. Access is restricted to authorized project personnel only."
        },
        {
            "question": "Can I use this system on my mobile device?",
            "answer": "Yes! The platform is fully optimized for mobile use. Field personnel can submit reports, take progress photos, and access project information from any mobile device."
        },
        {
            "question": "How do I submit daily reports?",
            "answer": "Navigate to the Daily Reports module from the Core Tools section. Fill out the required fields including weather, crew count, work performed, and any safety notes."
        },
        {
            "question": "What is an RFI and how do I submit one?",
            "answer": "RFI stands for Request for Information. Use the Engineering module to submit RFIs when you need clarification on drawings, specifications, or construction details."
        },
        {
            "question": "How does digital signature work for owner bills?",
            "answer": "Authorized personnel can digitally sign AIA G702/G703 owner bills through the Cost Management module. Digital signatures are legally binding and secure."
        },
        {
            "question": "Can I access the system offline?",
            "answer": "Limited offline functionality is available for mobile users. Data will synchronize when connection is restored."
        }
    ]
    
    for faq in faqs:
        with st.expander(faq["question"]):
            st.write(faq["answer"])

def render_support():
    """Render support and contact information"""
    
    st.markdown("## 📞 Support & Contact Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏗️ Highland Tower Development Team
        
        **Project Manager**
        - Phone: (555) 123-4567
        - Email: pm@highlandtower.dev
        
        **Site Superintendent** 
        - Phone: (555) 123-4568
        - Email: super@highlandtower.dev
        
        **Safety Manager**
        - Phone: (555) 123-4569
        - Email: safety@highlandtower.dev
        """)
    
    with col2:
        st.markdown("""
        ### 💻 Technical Support
        
        **IT Help Desk**
        - Phone: (555) 123-4570
        - Email: support@highlandtower.dev
        - Hours: Monday-Friday, 7 AM - 6 PM
        
        **Emergency After Hours**
        - Phone: (555) 123-HELP
        - Available 24/7 for critical issues
        """)
    
    st.markdown("### 🆘 Emergency Contacts")
    
    st.warning("""
    **For Safety Emergencies**: Call 911 immediately, then contact the Safety Manager
    
    **For System Critical Issues**: Contact IT Help Desk or use emergency after-hours number
    """)
    
    st.markdown("### 📧 General Information")
    
    st.info("""
    **Project Website**: www.highlandtower.dev
    
    **Document Portal**: docs.highlandtower.dev
    
    **Training Resources**: Available through your project manager
    """)

if __name__ == "__main__":
    render()