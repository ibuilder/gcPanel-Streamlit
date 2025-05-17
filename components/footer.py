import streamlit as st

def render_footer():
    """Render the application footer"""
    st.markdown("<hr>", unsafe_allow_html=True)
    
    with st.container():
        cols = st.columns([3, 3, 3, 1])
        
        with cols[0]:
            st.markdown("### gcPanel")
            st.markdown("Construction Management Dashboard")
        
        with cols[1]:
            st.markdown("### Quick Links")
            st.markdown("[Documentation](#)")
            st.markdown("[Support](#)")
            st.markdown("[Report Issue](#)")
        
        with cols[2]:
            st.markdown("### Contact")
            st.markdown("Email: support@gcpanel.com")
            st.markdown("Phone: (555) 123-4567")
        
        with cols[3]:
            st.markdown("### Follow")
            st.markdown("[LinkedIn](#)")
            st.markdown("[Twitter](#)")
    
    st.markdown("<p style='text-align: center; margin-top: 20px;'>© 2023 gcPanel. All rights reserved.</p>", unsafe_allow_html=True)
