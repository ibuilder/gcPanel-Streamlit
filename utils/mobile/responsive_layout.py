"""
Responsive Layout Utils for gcPanel

This module provides utilities for making the application responsive and mobile-friendly.
"""

import streamlit as st

def add_mobile_styles():
    """
    Add responsive mobile styles to improve the application on mobile devices.
    
    This includes adjustments for:
    - Touch targets (larger buttons, inputs)
    - Responsive layout adjustments
    - Better readability on small screens
    """
    # Mobile optimization CSS
    st.markdown("""
    <style>
        /* Base mobile optimizations */
        @media (max-width: 768px) {
            /* Make buttons and inputs larger for touch */
            button, input, select, textarea, .stButton button {
                min-height: 44px !important;
                font-size: 16px !important;
            }
            
            /* Improve readability on small screens */
            body, p, div {
                font-size: 16px !important;
            }
            
            h1 {
                font-size: 1.8rem !important;
            }
            
            h2 {
                font-size: 1.5rem !important;
            }
            
            h3 {
                font-size: 1.3rem !important;
            }
            
            /* Adjust column layout for mobile */
            div.row-widget.stHorizontal {
                flex-direction: column;
            }
            
            /* Make sure tables don't overflow */
            table {
                display: block;
                overflow-x: auto;
                white-space: nowrap;
            }
            
            /* Adjust sidebar for mobile */
            section[data-testid="stSidebar"] {
                width: 100% !important;
                min-width: 100% !important;
                max-width: 100% !important;
            }
            
            /* Improve cards on mobile */
            .card {
                margin: 0.5rem 0 !important;
                padding: 0.8rem !important;
            }
            
            /* Better spacing for form elements */
            .element-container {
                margin-bottom: 1rem !important;
            }
            
            /* Make notification content scrollable on small screens */
            .notification-content {
                max-height: 60vh;
                overflow-y: auto;
            }
        }
        
        /* Add viewport meta tag for proper mobile rendering */
        @media screen {
            body:before {
                content: '';
                display: block;
            }
        }
        
        /* Handle notches on iPhone X and newer */
        @supports (padding: max(0px)) {
            .main .block-container {
                padding-left: max(1rem, env(safe-area-inset-left));
                padding-right: max(1rem, env(safe-area-inset-right));
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Add viewport meta tag
    st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    """, unsafe_allow_html=True)