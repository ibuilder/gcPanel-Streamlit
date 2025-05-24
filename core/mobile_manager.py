"""
Mobile Optimization Manager for gcPanel Highland Tower Development

Implements responsive design, mobile-first layouts, and field-optimized
interfaces for construction management on tablets and mobile devices.
"""

import streamlit as st
from typing import Dict, List
import logging

class MobileManager:
    """Enterprise mobile optimization manager"""
    
    def __init__(self):
        self.setup_logging()
        self.device_breakpoints = {
            'mobile': 768,
            'tablet': 1024,
            'desktop': 1200
        }
    
    def setup_logging(self):
        """Setup mobile optimization logging"""
        self.logger = logging.getLogger('MobileManager')
    
    def detect_device_type(self) -> str:
        """Detect device type for responsive layout"""
        # In production, this would use actual device detection
        # For now, check session state or default to mobile-first
        return st.session_state.get('device_type', 'mobile')
    
    def apply_mobile_styles(self):
        """Apply mobile-optimized CSS styles"""
        mobile_css = """
        <style>
        /* Mobile-first responsive design for Highland Tower Development */
        @media screen and (max-width: 768px) {
            .main .block-container {
                padding: 1rem 0.5rem !important;
                max-width: 100% !important;
            }
            
            /* Mobile-optimized buttons */
            .stButton > button {
                width: 100% !important;
                padding: 12px 16px !important;
                font-size: 16px !important;
                margin: 4px 0 !important;
                min-height: 44px !important; /* Touch-friendly */
            }
            
            /* Mobile-optimized form inputs */
            .stTextInput > div > div > input,
            .stSelectbox > div > div,
            .stTextArea > div > div > textarea {
                font-size: 16px !important; /* Prevents zoom on iOS */
                padding: 12px !important;
                min-height: 44px !important;
            }
            
            /* Mobile-optimized metrics */
            [data-testid="metric-container"] {
                padding: 8px !important;
                margin: 4px 0 !important;
            }
            
            /* Hide desktop-only elements on mobile */
            .desktop-only {
                display: none !important;
            }
            
            /* Mobile navigation */
            .mobile-nav {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: #1e2228;
                padding: 8px;
                z-index: 1000;
                display: flex;
                justify-content: space-around;
            }
            
            .mobile-nav-item {
                flex: 1;
                text-align: center;
                padding: 8px 4px;
                color: #fafafa;
                text-decoration: none;
                font-size: 12px;
            }
            
            /* Mobile tables */
            .stDataFrame {
                font-size: 14px !important;
            }
            
            /* Mobile sidebar adjustments */
            .css-1d391kg {
                width: 100% !important;
                position: relative !important;
            }
        }
        
        @media screen and (max-width: 480px) {
            /* Extra small mobile devices */
            .main .block-container {
                padding: 0.5rem 0.25rem !important;
            }
            
            h1, h2, h3 {
                font-size: 1.2rem !important;
                line-height: 1.3 !important;
            }
            
            /* Stack columns on very small screens */
            .row-widget.stHorizontal > div {
                flex-direction: column !important;
            }
        }
        
        /* Tablet optimizations */
        @media screen and (min-width: 769px) and (max-width: 1024px) {
            .main .block-container {
                padding: 1rem !important;
            }
            
            /* Show more content on tablets */
            .tablet-show {
                display: block !important;
            }
        }
        
        /* Touch-friendly improvements */
        .touch-friendly {
            min-height: 44px;
            min-width: 44px;
            padding: 8px;
        }
        
        /* Loading indicators for mobile */
        .mobile-loading {
            text-align: center;
            padding: 20px;
            font-size: 14px;
            color: #666;
        }
        </style>
        """
        
        st.markdown(mobile_css, unsafe_allow_html=True)
    
    def render_mobile_navigation(self):
        """Render mobile-optimized bottom navigation"""
        nav_items = [
            {"icon": "🏗️", "label": "Dashboard", "key": "dashboard"},
            {"icon": "❓", "label": "RFIs", "key": "rfis"},
            {"icon": "📝", "label": "Reports", "key": "reports"},
            {"icon": "🔍", "label": "QC", "key": "quality"},
            {"icon": "⚙️", "label": "More", "key": "more"}
        ]
        
        st.markdown("""
        <div class="mobile-nav">
        """, unsafe_allow_html=True)
        
        cols = st.columns(len(nav_items))
        for i, item in enumerate(nav_items):
            with cols[i]:
                if st.button(f"{item['icon']}\n{item['label']}", 
                           key=f"mobile_nav_{item['key']}",
                           use_container_width=True):
                    st.session_state.current_menu = item['label']
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def render_mobile_quick_actions(self):
        """Render mobile-optimized quick action buttons"""
        st.markdown("#### Quick Actions")
        
        quick_actions = [
            {"icon": "📝", "label": "New Daily Report", "action": "daily_report"},
            {"icon": "❓", "label": "Submit RFI", "action": "new_rfi"},
            {"icon": "📸", "label": "Photo Log", "action": "photo_log"},
            {"icon": "⚠️", "label": "Safety Issue", "action": "safety_issue"}
        ]
        
        # Create 2x2 grid for mobile
        cols = st.columns(2)
        for i, action in enumerate(quick_actions):
            with cols[i % 2]:
                if st.button(f"{action['icon']} {action['label']}", 
                           key=f"quick_action_{action['action']}",
                           use_container_width=True):
                    st.success(f"Opening {action['label']} form...")
    
    def render_mobile_metrics(self, metrics: List[Dict]):
        """Render mobile-optimized metrics display"""
        # Single column layout for mobile
        for metric in metrics:
            st.metric(
                label=metric['label'],
                value=metric['value'],
                delta=metric.get('delta'),
                delta_color=metric.get('delta_color', 'normal')
            )
    
    def render_mobile_table(self, data: List[Dict], max_rows: int = 5):
        """Render mobile-optimized table view"""
        st.markdown("#### Recent Items")
        
        for i, item in enumerate(data[:max_rows]):
            with st.expander(f"{item.get('title', item.get('id', f'Item {i+1}'))}"):
                # Display key fields in mobile-friendly format
                for key, value in item.items():
                    if key not in ['id', 'title']:
                        st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
        
        if len(data) > max_rows:
            if st.button(f"View All ({len(data)} items)", use_container_width=True):
                st.session_state.show_all_items = True
                st.rerun()
    
    def get_mobile_layout_config(self) -> Dict:
        """Get mobile-optimized layout configuration"""
        device_type = self.detect_device_type()
        
        if device_type == 'mobile':
            return {
                'columns': 1,
                'sidebar_collapsed': True,
                'show_navigation': False,
                'use_bottom_nav': True,
                'max_table_rows': 3,
                'card_layout': True
            }
        elif device_type == 'tablet':
            return {
                'columns': 2,
                'sidebar_collapsed': False,
                'show_navigation': True,
                'use_bottom_nav': False,
                'max_table_rows': 5,
                'card_layout': True
            }
        else:  # desktop
            return {
                'columns': 4,
                'sidebar_collapsed': False,
                'show_navigation': True,
                'use_bottom_nav': False,
                'max_table_rows': 10,
                'card_layout': False
            }
    
    def optimize_for_field_use(self):
        """Apply field-specific optimizations"""
        field_css = """
        <style>
        /* Field operations optimizations */
        .field-form input, .field-form textarea, .field-form select {
            font-size: 18px !important;
            padding: 15px !important;
            border: 2px solid #4CAF50 !important;
        }
        
        .field-button {
            background: #ff6b35 !important;
            color: white !important;
            font-size: 18px !important;
            padding: 15px 20px !important;
            border-radius: 8px !important;
            margin: 10px 0 !important;
        }
        
        .field-alert {
            background: #fff3cd !important;
            border: 2px solid #ffc107 !important;
            padding: 15px !important;
            border-radius: 8px !important;
            margin: 10px 0 !important;
            font-size: 16px !important;
        }
        
        /* High contrast for outdoor use */
        .outdoor-mode {
            filter: contrast(120%) brightness(110%);
        }
        
        /* Large touch targets */
        .field-touch-target {
            min-height: 60px !important;
            min-width: 60px !important;
            padding: 15px !important;
        }
        </style>
        """
        
        st.markdown(field_css, unsafe_allow_html=True)
    
    def add_mobile_pwa_support(self):
        """Add Progressive Web App support for mobile installation"""
        pwa_html = """
        <script>
        // Progressive Web App support
        let deferredPrompt;
        
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            showInstallBanner();
        });
        
        function showInstallBanner() {
            const banner = document.createElement('div');
            banner.innerHTML = `
                <div style="position: fixed; top: 0; left: 0; right: 0; background: #4CAF50; color: white; padding: 10px; text-align: center; z-index: 10000;">
                    <span>Install gcPanel for Highland Tower Development</span>
                    <button onclick="installApp()" style="margin-left: 10px; background: white; color: #4CAF50; border: none; padding: 5px 10px; border-radius: 3px;">Install</button>
                    <button onclick="dismissBanner()" style="margin-left: 5px; background: transparent; color: white; border: 1px solid white; padding: 5px 10px; border-radius: 3px;">Later</button>
                </div>
            `;
            document.body.appendChild(banner);
        }
        
        function installApp() {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {
                    deferredPrompt = null;
                    dismissBanner();
                });
            }
        }
        
        function dismissBanner() {
            const banner = document.querySelector('[style*="position: fixed; top: 0"]');
            if (banner) banner.remove();
        }
        </script>
        """
        
        st.markdown(pwa_html, unsafe_allow_html=True)

@st.cache_resource
def get_mobile_manager():
    """Get cached mobile manager instance"""
    return MobileManager()

def apply_responsive_layout():
    """Apply responsive layout optimizations"""
    mobile_manager = get_mobile_manager()
    
    # Apply mobile styles
    mobile_manager.apply_mobile_styles()
    
    # Add PWA support
    mobile_manager.add_mobile_pwa_support()
    
    # Field optimizations if in field mode
    if st.session_state.get('field_mode', False):
        mobile_manager.optimize_for_field_use()
    
    return mobile_manager.get_mobile_layout_config()

def render_responsive_content(content_func, mobile_func=None):
    """Render content responsively based on device type"""
    mobile_manager = get_mobile_manager()
    device_type = mobile_manager.detect_device_type()
    
    if device_type == 'mobile' and mobile_func:
        mobile_func()
    else:
        content_func()