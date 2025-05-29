"""
Footer component for the gcPanel application.

This component renders a footer with copyright information
and additional links or information as needed.
"""

import streamlit as st

def render_footer():
    """
    Render the application footer with copyright information.
    """
    # Footer container
    with st.container():
        # Add some space before the footer
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Apply footer styling
        st.markdown("""
        <style>
        .footer-container {
            border-top: 1px solid #DADCE0;
            padding: 20px 0;
            margin-top: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: #5F6368;
            font-size: 14px;
        }
        
        .footer-links a {
            color: #3367D6;
            text-decoration: none;
            margin-left: 20px;
        }
        
        .footer-links a:hover {
            text-decoration: underline;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create the footer HTML
        footer_html = """
        <div class="footer-container">
            <div class="footer-copyright">
                © 2025 gcPanel Construction Management. All rights reserved.
            </div>
            <div class="footer-links">
                <a href="#">Terms</a>
                <a href="#">Privacy</a>
                <a href="#">Help</a>
            </div>
        </div>
        """
        
        # Render the footer
        st.markdown(footer_html, unsafe_allow_html=True)