"""
Smart Tooltip Guidance System
Highland Tower Development - Enterprise Construction Management

Provides contextual help and guidance throughout the application
"""

import streamlit as st

def apply_smart_tooltips():
    """Apply smart tooltip system with contextual guidance"""
    
    st.markdown("""
    <style>
    /* Smart Tooltip Styling */
    .tooltip-container {
        position: relative;
        display: inline-block;
    }
    
    .tooltip-help {
        background: #1e3c72;
        color: white;
        border: none;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        font-size: 12px;
        cursor: help;
        margin-left: 5px;
        position: relative;
    }
    
    .tooltip-content {
        visibility: hidden;
        background-color: #333;
        color: #fff;
        text-align: left;
        border-radius: 8px;
        padding: 10px;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        margin-left: -120px;
        width: 240px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 13px;
        line-height: 1.4;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .tooltip-content::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #333 transparent transparent transparent;
    }
    
    .tooltip-container:hover .tooltip-content {
        visibility: visible;
        opacity: 1;
    }
    
    .smart-guidance {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        color: white;
        border-left: 4px solid #ffd700;
    }
    
    .guidance-step {
        background: #f8f9fa;
        border-left: 4px solid #28a745;
        padding: 12px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
    }
    
    .warning-tooltip {
        background: #dc3545;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        margin: 5px 0;
        font-size: 13px;
    }
    
    .success-tooltip {
        background: #28a745;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        margin: 5px 0;
        font-size: 13px;
    }
    
    .info-tooltip {
        background: #17a2b8;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        margin: 5px 0;
        font-size: 13px;
    }
    </style>
    """, unsafe_allow_html=True)

def render_tooltip(text, tooltip_content, tooltip_type="info"):
    """Render a smart tooltip with contextual help"""
    
    color_map = {
        "info": "#17a2b8",
        "warning": "#ffc107", 
        "success": "#28a745",
        "error": "#dc3545"
    }
    
    color = color_map.get(tooltip_type, "#17a2b8")
    
    st.markdown(f"""
    <div class="tooltip-container">
        {text}
        <button class="tooltip-help" style="background: {color};">?</button>
        <div class="tooltip-content">
            {tooltip_content}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_smart_guidance(title, steps, context="general"):
    """Render contextual step-by-step guidance"""
    
    st.markdown(f"""
    <div class="smart-guidance">
        <h4 style="margin: 0 0 10px 0; color: #ffd700;">💡 {title}</h4>
        <p style="margin: 0; font-size: 14px;">Highland Tower Development guidance for this section:</p>
    </div>
    """, unsafe_allow_html=True)
    
    for i, step in enumerate(steps, 1):
        st.markdown(f"""
        <div class="guidance-step">
            <strong>Step {i}:</strong> {step}
        </div>
        """, unsafe_allow_html=True)

def get_context_help(module_name):
    """Get contextual help based on current module"""
    
    help_content = {
        "Dashboard": {
            "title": "Dashboard Navigation Guide",
            "steps": [
                "Review key metrics in the top cards for project health",
                "Check recent activities for urgent items requiring attention", 
                "Use quick access buttons to jump to specific modules",
                "Monitor Highland Tower's 67.3% completion status"
            ]
        },
        "Daily Reports": {
            "title": "Daily Reports Best Practices",
            "steps": [
                "Submit reports before 6 PM each day for Highland Tower",
                "Include weather conditions and crew count",
                "Document any safety incidents or near misses",
                "Upload progress photos with GPS location data"
            ]
        },
        "Cost Management": {
            "title": "AIA Billing Process",
            "steps": [
                "Review Schedule of Values before creating owner bills",
                "Ensure all work is properly documented with photos",
                "Get digital signatures from authorized personnel only",
                "Submit bills by the 25th of each month for Highland Tower"
            ]
        },
        "Engineering": {
            "title": "RFI Management Process", 
            "steps": [
                "Submit RFIs with clear drawings and specifications",
                "Include Highland Tower project number in all submissions",
                "Follow up on overdue RFIs after 5 business days",
                "Currently tracking 23 active RFIs for this project"
            ]
        },
        "Safety": {
            "title": "OSHA Compliance Guidelines",
            "steps": [
                "Conduct daily safety briefings at 7 AM",
                "Report all incidents within 24 hours",
                "Maintain 98.5% compliance rate for Highland Tower",
                "Complete weekly safety inspections every Friday"
            ]
        }
    }
    
    return help_content.get(module_name, {
        "title": "General Usage Guide",
        "steps": [
            "Use the sidebar navigation to access different modules",
            "All data is automatically saved as you work",
            "Contact support for Highland Tower specific questions",
            "Export reports using the action buttons"
        ]
    })

def render_field_guidance():
    """Render field-specific guidance for mobile users"""
    
    st.markdown("""
    <div class="info-tooltip">
        📱 <strong>Field Mode Active:</strong> Optimized for mobile use on Highland Tower site
    </div>
    """, unsafe_allow_html=True)
    
    guidance_tips = [
        "Take photos in landscape mode for better documentation",
        "Use GPS tagging for accurate location tracking", 
        "Submit reports even with poor connectivity - they'll sync later",
        "Voice-to-text available for faster data entry"
    ]
    
    for tip in guidance_tips:
        st.markdown(f"""
        <div class="guidance-step">
            • {tip}
        </div>
        """, unsafe_allow_html=True)

def render_signature_guidance():
    """Render guidance for digital signatures"""
    
    st.markdown("""
    <div class="warning-tooltip">
        ⚠️ <strong>Digital Signature Required:</strong> Owner bills require authorized signatures
    </div>
    """, unsafe_allow_html=True)
    
    signature_steps = [
        "Verify all line items and amounts before signing",
        "Ensure supporting documentation is attached",
        "Only authorized Highland Tower personnel can sign owner bills",
        "Signed documents are legally binding and cannot be modified"
    ]
    
    for step in signature_steps:
        st.markdown(f"""
        <div class="guidance-step">
            🔐 {step}
        </div>
        """, unsafe_allow_html=True)

def show_module_help(module_name):
    """Show contextual help for specific module"""
    
    if st.button("💡 Show Guidance", key=f"help_{module_name}"):
        help_content = get_context_help(module_name)
        render_smart_guidance(help_content["title"], help_content["steps"], module_name.lower())
    
def render_onboarding_tooltips():
    """Render onboarding tooltips for new users"""
    
    if "show_onboarding" not in st.session_state:
        st.session_state.show_onboarding = True
    
    if st.session_state.show_onboarding:
        st.markdown("""
        <div class="smart-guidance">
            <h4 style="margin: 0 0 10px 0; color: #ffd700;">👋 Welcome to Highland Tower Development</h4>
            <p style="margin: 0; font-size: 14px;">Your $45.5M project management platform is ready!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("Got it!", key="dismiss_onboarding"):
                st.session_state.show_onboarding = False
                st.rerun()

def create_interactive_help(content_type="general"):
    """Create interactive help based on context"""
    
    help_data = {
        "billing": {
            "title": "AIA G702/G703 Billing Help",
            "content": "Highland Tower Development uses standard AIA billing forms. Ensure all work is documented before submitting owner bills.",
            "action": "Review the Schedule of Values first"
        },
        "signature": {
            "title": "Digital Signature Process", 
            "content": "Digital signatures are legally binding. Only authorized Highland Tower project managers can sign owner bills.",
            "action": "Verify your authorization level"
        },
        "rfis": {
            "title": "RFI Submission Guidelines",
            "content": "Submit RFIs with clear drawings and detailed questions. Include Highland Tower project number HTD-2024-001.",
            "action": "Check RFI template requirements"
        }
    }
    
    if content_type in help_data:
        data = help_data[content_type]
        
        with st.expander(f"❓ {data['title']}", expanded=False):
            st.info(data['content'])
            st.button(data['action'], key=f"help_action_{content_type}")

if __name__ == "__main__":
    apply_smart_tooltips()