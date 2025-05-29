"""
Highland Tower Development - Enhanced Collapsible Navigation
Collapsible and pinnable sidebar sections for improved user experience
"""

import streamlit as st
from typing import Dict, List

class NavigationManager:
    """Manages collapsible and pinnable navigation sections"""
    
    def __init__(self):
        self.initialize_navigation_state()
    
    def initialize_navigation_state(self):
        """Initialize navigation state in session"""
        if 'nav_collapsed_sections' not in st.session_state:
            st.session_state.nav_collapsed_sections = set()
        
        if 'nav_pinned_items' not in st.session_state:
            st.session_state.nav_pinned_items = []
        
        if 'nav_recent_items' not in st.session_state:
            st.session_state.nav_recent_items = []
    
    def toggle_section(self, section_name: str):
        """Toggle collapse state of a navigation section"""
        if section_name in st.session_state.nav_collapsed_sections:
            st.session_state.nav_collapsed_sections.remove(section_name)
        else:
            st.session_state.nav_collapsed_sections.add(section_name)
    
    def pin_item(self, item_name: str):
        """Pin a navigation item for quick access"""
        if item_name not in st.session_state.nav_pinned_items:
            st.session_state.nav_pinned_items.append(item_name)
    
    def unpin_item(self, item_name: str):
        """Unpin a navigation item"""
        if item_name in st.session_state.nav_pinned_items:
            st.session_state.nav_pinned_items.remove(item_name)
    
    def add_recent_item(self, item_name: str):
        """Add item to recent navigation"""
        if item_name in st.session_state.nav_recent_items:
            st.session_state.nav_recent_items.remove(item_name)
        
        st.session_state.nav_recent_items.insert(0, item_name)
        
        # Keep only last 5 recent items
        if len(st.session_state.nav_recent_items) > 5:
            st.session_state.nav_recent_items = st.session_state.nav_recent_items[:5]
    
    def is_section_collapsed(self, section_name: str) -> bool:
        """Check if section is collapsed"""
        return section_name in st.session_state.nav_collapsed_sections
    
    def is_item_pinned(self, item_name: str) -> bool:
        """Check if item is pinned"""
        return item_name in st.session_state.nav_pinned_items

def render_enhanced_sidebar():
    """Render enhanced sidebar with collapsible sections"""
    nav_manager = NavigationManager()
    
    st.markdown("""
    <style>
    .nav-section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 12px;
        background: rgba(255,255,255,0.05);
        border-radius: 6px;
        margin: 4px 0;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .nav-section-header:hover {
        background: rgba(255,255,255,0.1);
    }
    
    .nav-item {
        padding: 6px 16px;
        margin: 2px 0;
        border-radius: 4px;
        transition: all 0.2s ease;
        position: relative;
    }
    
    .nav-item:hover {
        background: rgba(255,255,255,0.08);
    }
    
    .nav-item.pinned::before {
        content: "📌";
        position: absolute;
        right: 8px;
        font-size: 12px;
    }
    
    .nav-pinned-section {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 16px;
    }
    
    .nav-recent-section {
        background: rgba(16, 185, 129, 0.1);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 16px;
        border-left: 4px solid #10b981;
    }
    
    .collapse-icon {
        transition: transform 0.2s ease;
    }
    
    .collapse-icon.collapsed {
        transform: rotate(-90deg);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Highland Tower Header
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; border-bottom: 2px solid #3b82f6;">
        <h2 style="color: #3b82f6; margin: 0;">Highland Tower</h2>
        <p style="color: #64748b; margin: 5px 0 0 0; font-size: 14px;">$45.5M Development</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pinned Items Section
    if st.session_state.nav_pinned_items:
        st.markdown('<div class="nav-pinned-section">', unsafe_allow_html=True)
        st.markdown("**📌 Pinned**")
        
        for item in st.session_state.nav_pinned_items:
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(item, key=f"pinned_{item}", use_container_width=True):
                    st.session_state.current_menu = item
                    nav_manager.add_recent_item(item)
                    st.rerun()
            with col2:
                if st.button("📌", key=f"unpin_{item}", help="Unpin"):
                    nav_manager.unpin_item(item)
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Items Section
    if st.session_state.nav_recent_items:
        st.markdown('<div class="nav-recent-section">', unsafe_allow_html=True)
        st.markdown("**🕒 Recent**")
        
        for item in st.session_state.nav_recent_items[:3]:  # Show top 3 recent
            if st.button(f"↪ {item}", key=f"recent_{item}", use_container_width=True):
                st.session_state.current_menu = item
                nav_manager.add_recent_item(item)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main Navigation Sections
    navigation_sections = {
        "🏗️ Project Management": [
            "Dashboard", "Daily Reports", "Progress Photos", 
            "Scheduling", "Field Operations"
        ],
        "📋 Documentation": [
            "RFIs", "Submittals", "Transmittals", 
            "Documents", "Engineering"
        ],
        "💰 Financial": [
            "Cost Management", "AIA Billing", "Prime Contract", 
            "Change Orders", "Procurement"
        ],
        "🔧 Operations": [
            "Safety", "Quality Control", "Material Management", 
            "Equipment Tracking", "Inspections"
        ],
        "📊 Analytics": [
            "Analytics", "Performance Snapshot", 
            "BIM", "AI Assistant"
        ],
        "⚙️ Resources": [
            "Contracts", "Subcontractor Management", 
            "Integrations", "Settings"
        ]
    }
    
    for section_name, items in navigation_sections.items():
        # Section Header
        col1, col2 = st.columns([5, 1])
        
        with col1:
            if st.button(
                section_name, 
                key=f"section_{section_name}",
                use_container_width=True
            ):
                nav_manager.toggle_section(section_name)
                st.rerun()
        
        with col2:
            is_collapsed = nav_manager.is_section_collapsed(section_name)
            icon = "▼" if not is_collapsed else "▶"
            st.markdown(f"<div style='text-align: center; padding: 8px;'>{icon}</div>", 
                       unsafe_allow_html=True)
        
        # Section Items (if not collapsed)
        if not nav_manager.is_section_collapsed(section_name):
            for item in items:
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    # Highlight current menu
                    button_type = "primary" if st.session_state.get('current_menu') == item else "secondary"
                    
                    if st.button(
                        item, 
                        key=f"nav_{item}",
                        type=button_type,
                        use_container_width=True
                    ):
                        st.session_state.current_menu = item
                        nav_manager.add_recent_item(item)
                        st.rerun()
                
                with col2:
                    # Pin/Unpin button
                    if nav_manager.is_item_pinned(item):
                        if st.button("📌", key=f"pin_toggle_{item}", help="Unpin"):
                            nav_manager.unpin_item(item)
                            st.rerun()
                    else:
                        if st.button("📍", key=f"pin_toggle_{item}", help="Pin"):
                            nav_manager.pin_item(item)
                            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation Controls
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset Navigation", use_container_width=True):
            st.session_state.nav_collapsed_sections = set()
            st.session_state.nav_pinned_items = []
            st.session_state.nav_recent_items = []
            st.rerun()
    
    with col2:
        if st.button("📋 Collapse All", use_container_width=True):
            st.session_state.nav_collapsed_sections = set(navigation_sections.keys())
            st.rerun()
    
    return st.session_state.get('current_menu', 'Dashboard')

def get_navigation_analytics():
    """Get navigation usage analytics"""
    analytics = {
        'pinned_count': len(st.session_state.get('nav_pinned_items', [])),
        'recent_count': len(st.session_state.get('nav_recent_items', [])),
        'collapsed_sections': len(st.session_state.get('nav_collapsed_sections', set())),
        'most_used': st.session_state.get('nav_recent_items', [])[:3]
    }
    return analytics