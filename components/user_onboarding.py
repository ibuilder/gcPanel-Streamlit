"""
Contextual User Role Onboarding Tooltips

This module provides intelligent, role-based onboarding tooltips
that guide users through their specific workflow and permissions.
"""
import streamlit as st
from typing import Dict, List, Optional, Tuple

# Role-specific onboarding content
ROLE_ONBOARDING = {
    "Project Manager": {
        "welcome": "Welcome, Project Manager! You have comprehensive access to oversee all project aspects.",
        "key_features": [
            "Dashboard: Monitor overall project health and KPIs",
            "Cost Management: Track budgets, change orders, and financial reports",
            "Scheduling: Manage project timelines and milestones",
            "Contracts: Oversee all project contracts and subcontractors",
            "Reports: Generate executive reports and analytics"
        ],
        "first_steps": [
            "Check the Dashboard for project overview",
            "Review active change orders in Cost Management",
            "Verify schedule progress in Field Operations"
        ],
        "permissions": "Full access to all modules with administrative privileges"
    },
    "Field Supervisor": {
        "welcome": "Welcome, Field Supervisor! Focus on daily operations and field management.",
        "key_features": [
            "Field Operations: Daily reports, equipment tracking, crew management",
            "Safety: Incident reporting, safety meetings, compliance tracking",
            "Quality Control: Inspections, punch lists, defect tracking",
            "Document Management: Access plans, specs, and field drawings",
            "Time & Materials: Submit T&M tickets and labor reports"
        ],
        "first_steps": [
            "Submit today's daily report in Field Operations",
            "Check safety compliance status",
            "Review active punch list items"
        ],
        "permissions": "Field operations focus with read access to related modules"
    },
    "Safety Officer": {
        "welcome": "Welcome, Safety Officer! Ensure project safety and compliance.",
        "key_features": [
            "Safety Module: Incident management, training records, compliance",
            "Field Operations: Safety observations and hazard identification",
            "Document Management: Safety plans, MSDS, and regulations",
            "Reports: Safety analytics and compliance reporting"
        ],
        "first_steps": [
            "Review recent safety incidents",
            "Check training compliance status",
            "Update safety meeting records"
        ],
        "permissions": "Full safety module access with read access to field operations"
    },
    "Cost Manager": {
        "welcome": "Welcome, Cost Manager! Control project finances and budgets.",
        "key_features": [
            "Cost Management: Budget tracking, change orders, invoicing",
            "Contracts: Contract values and payment schedules",
            "AIA Billing: Progress billing and payment applications",
            "Reports: Financial analytics and cost forecasting"
        ],
        "first_steps": [
            "Review budget variance reports",
            "Process pending change orders",
            "Check invoice approval queue"
        ],
        "permissions": "Full financial module access with contract read access"
    },
    "Document Controller": {
        "welcome": "Welcome, Document Controller! Manage all project documentation.",
        "key_features": [
            "Document Management: File organization, version control, sharing",
            "BIM Integration: Model management and coordination",
            "Communications: RFI management and submittal tracking",
            "Quality: Document review and approval workflows"
        ],
        "first_steps": [
            "Organize latest drawing revisions",
            "Process pending RFIs",
            "Update document distribution lists"
        ],
        "permissions": "Full document access with workflow management capabilities"
    },
    "Subcontractor": {
        "welcome": "Welcome, Subcontractor! Access your work areas and submit reports.",
        "key_features": [
            "Field Operations: Submit daily reports and progress updates",
            "Safety: Access safety requirements and submit observations",
            "Document Management: View relevant plans and specifications",
            "Time & Materials: Submit work tickets and material requests"
        ],
        "first_steps": [
            "Submit today's work progress",
            "Check safety requirements for your trade",
            "Review latest drawings for your scope"
        ],
        "permissions": "Limited access to assigned work areas and reporting functions"
    }
}

def show_role_welcome_tooltip(role: str) -> None:
    """Display welcome tooltip for user role."""
    
    if role not in ROLE_ONBOARDING:
        return
    
    role_info = ROLE_ONBOARDING[role]
    
    st.markdown(f"""
    <div class="welcome-tooltip">
        <div class="tooltip-header">
            <span class="welcome-icon">👋</span>
            <span class="welcome-title">{role_info['welcome']}</span>
        </div>
        <div class="tooltip-content">
            <div class="permissions-info">
                <strong>Your Access Level:</strong> {role_info['permissions']}
            </div>
        </div>
    </div>
    
    <style>
    .welcome-tooltip {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        animation: tooltip-slide-in 0.5s ease-out;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    
    .tooltip-header {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 15px;
    }}
    
    .welcome-icon {{
        font-size: 24px;
        animation: wave 2s ease-in-out infinite;
    }}
    
    .welcome-title {{
        font-size: 16px;
        font-weight: 600;
        line-height: 1.4;
    }}
    
    .permissions-info {{
        background: rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 6px;
        font-size: 14px;
    }}
    
    @keyframes tooltip-slide-in {{
        from {{ transform: translateY(-20px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    
    @keyframes wave {{
        0%, 100% {{ transform: rotate(0deg); }}
        25% {{ transform: rotate(20deg); }}
        75% {{ transform: rotate(-20deg); }}
    }}
    </style>
    """, unsafe_allow_html=True)

def show_feature_discovery_tooltip(role: str, current_page: str) -> None:
    """Show contextual feature discovery based on current page."""
    
    if role not in ROLE_ONBOARDING:
        return
    
    role_info = ROLE_ONBOARDING[role]
    
    # Find relevant features for current page
    relevant_features = [f for f in role_info['key_features'] if current_page.lower() in f.lower()]
    
    if relevant_features:
        st.info(f"💡 **{role} Tip:** {relevant_features[0]}")

def show_next_steps_guide(role: str) -> None:
    """Display suggested next steps for the user role."""
    
    if role not in ROLE_ONBOARDING:
        return
    
    role_info = ROLE_ONBOARDING[role]
    
    with st.expander("🚀 Suggested Next Steps", expanded=False):
        st.markdown("**Recommended actions to get started:**")
        for i, step in enumerate(role_info['first_steps'], 1):
            st.markdown(f"{i}. {step}")

def show_interactive_feature_tour(role: str) -> None:
    """Interactive feature tour for new users."""
    
    if role not in ROLE_ONBOARDING:
        return
    
    if f"tour_completed_{role}" not in st.session_state:
        st.session_state[f"tour_completed_{role}"] = False
    
    if not st.session_state[f"tour_completed_{role}"]:
        role_info = ROLE_ONBOARDING[role]
        
        st.markdown("""
        <div class="feature-tour">
            <div class="tour-header">
                <span class="tour-icon">🎯</span>
                <span class="tour-title">Take a Quick Tour</span>
            </div>
            <p>Let's explore the key features available to you!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🚀 Start Tour", use_container_width=True):
                st.session_state.show_tour = True
        
        with col2:
            if st.button("⏭️ Skip Tour", use_container_width=True):
                st.session_state[f"tour_completed_{role}"] = True
                st.rerun()
        
        if st.session_state.get('show_tour', False):
            show_feature_highlights(role)

def show_feature_highlights(role: str) -> None:
    """Show feature highlights during tour."""
    
    role_info = ROLE_ONBOARDING[role]
    
    st.markdown("### 🌟 Your Key Features")
    
    for i, feature in enumerate(role_info['key_features']):
        with st.container():
            feature_name, description = feature.split(': ', 1)
            
            st.markdown(f"""
            <div class="feature-highlight">
                <div class="feature-number">{i+1}</div>
                <div class="feature-content">
                    <div class="feature-name">{feature_name}</div>
                    <div class="feature-description">{description}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    if st.button("✅ Complete Tour", use_container_width=True):
        st.session_state[f"tour_completed_{role}"] = True
        st.session_state.show_tour = False
        st.success("🎉 Tour completed! You're ready to get started.")
        st.rerun()

def show_contextual_help(page: str, role: str) -> None:
    """Show contextual help based on current page and user role."""
    
    help_content = {
        "Dashboard": {
            "Project Manager": "Monitor KPIs, project health, and team performance metrics.",
            "Field Supervisor": "View field-specific metrics and crew productivity.",
            "Safety Officer": "Track safety statistics and incident trends."
        },
        "Cost Management": {
            "Project Manager": "Oversee budget performance and approve major expenditures.",
            "Cost Manager": "Manage detailed budgets, change orders, and financial forecasting.",
            "Field Supervisor": "Submit cost-related field observations and material usage."
        },
        "Safety": {
            "Safety Officer": "Manage all safety protocols, incidents, and training records.",
            "Field Supervisor": "Report safety observations and conduct toolbox talks.",
            "Project Manager": "Review safety performance and compliance status."
        }
    }
    
    if page in help_content and role in help_content[page]:
        with st.sidebar:
            st.markdown("### 💡 Quick Help")
            st.info(help_content[page][role])

def apply_onboarding_styles() -> None:
    """Apply CSS styles for onboarding components."""
    
    st.markdown("""
    <style>
    .feature-tour {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        color: #333;
        animation: tour-pulse 2s ease-in-out infinite;
    }
    
    .tour-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }
    
    .tour-icon {
        font-size: 24px;
    }
    
    .tour-title {
        font-size: 18px;
        font-weight: bold;
    }
    
    .feature-highlight {
        display: flex;
        align-items: flex-start;
        gap: 15px;
        padding: 15px;
        background: #f8f9fa;
        border-radius: 8px;
        margin: 10px 0;
        animation: feature-slide-in 0.5s ease-out;
        border-left: 4px solid #007bff;
    }
    
    .feature-number {
        background: #007bff;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        flex-shrink: 0;
    }
    
    .feature-name {
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
    }
    
    .feature-description {
        color: #666;
        font-size: 14px;
        line-height: 1.4;
    }
    
    @keyframes tour-pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(255, 154, 158, 0.4); }
        50% { box-shadow: 0 0 0 10px rgba(255, 154, 158, 0); }
    }
    
    @keyframes feature-slide-in {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)