"""
Highland Tower Development - Scroll Fix
Fixes page scrolling issues and layout problems
"""

import streamlit as st

def apply_scroll_fix():
    """Apply CSS fixes for page scrolling issues"""
    st.markdown("""
    <style>
    /* Fix main scrolling container */
    .main .block-container {
        max-height: none !important;
        overflow: visible !important;
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
    }
    
    /* Ensure body and html allow scrolling */
    html, body {
        overflow: auto !important;
        height: auto !important;
        scroll-behavior: smooth !important;
    }
    
    /* Fix Streamlit app container */
    .stApp {
        overflow: auto !important;
        height: auto !important;
        min-height: 100vh !important;
    }
    
    /* Remove fixed positioning that blocks scrolling */
    .stApp > header {
        position: relative !important;
    }
    
    /* Fix sidebar scrolling */
    section[data-testid="stSidebar"] > div {
        overflow-y: auto !important;
        height: 100vh !important;
    }
    
    /* Ensure content doesn't overflow */
    .element-container {
        overflow: visible !important;
    }
    
    /* Fix chart containers */
    .js-plotly-plot {
        overflow: visible !important;
    }
    
    /* Remove any problematic height constraints */
    .stVerticalBlock {
        height: auto !important;
    }
    
    /* Fix data frame scrolling */
    .stDataFrame {
        overflow: auto !important;
        max-height: 400px !important;
    }
    
    /* Ensure proper spacing for scrolling */
    .main > div {
        padding-bottom: 2rem !important;
    }
    
    /* Fix any sticky elements that might interfere */
    .sticky {
        position: relative !important;
    }
    
    /* Mobile scroll fixes */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem !important;
            max-width: 100% !important;
        }
        
        body {
            -webkit-overflow-scrolling: touch !important;
        }
    }
    
    /* Remove any transform3d that might cause issues */
    * {
        -webkit-transform: none !important;
        transform: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_scroll_fix():
    """Initialize scroll fix on page load"""
    if 'scroll_fix_applied' not in st.session_state:
        st.session_state.scroll_fix_applied = True
        apply_scroll_fix()
        
        # Add JavaScript to ensure scrolling works
        st.markdown("""
        <script>
        // Ensure page can scroll
        document.documentElement.style.overflow = 'auto';
        document.body.style.overflow = 'auto';
        
        // Remove any scroll blocking
        window.addEventListener('load', function() {
            document.body.style.height = 'auto';
            document.documentElement.style.height = 'auto';
        });
        </script>
        """, unsafe_allow_html=True)