"""
Mobile application companion module for gcPanel.

This module provides functionality for accessing key project features
via mobile devices, optimized for smartphone and tablet screens.
"""

import streamlit as st
from components.mobile.mobile_app_layout import (
    render_mobile_app, 
    mobile_dashboard, 
    mobile_tasks, 
    mobile_photos, 
    mobile_documents, 
    mobile_more_menu
)

def mobile_app_main():
    """
    Main entry point for the mobile companion app.
    
    This function renders a mobile-optimized interface for the gcPanel
    construction management dashboard.
    """
    # Set up the mobile companion app page
    st.title("gcPanel Mobile Companion")
    
    # Add a description of the mobile companion
    st.markdown("""
    ### Mobile Access to Your Construction Projects
    
    This mobile companion provides easy access to your construction project data on the go.
    The interface is optimized for smartphones and tablets, allowing you to:
    
    * View project dashboards and key metrics
    * Manage and update tasks
    * Capture and review site photos
    * Access important documents
    * Receive real-time notifications
    """)
    
    # Add a preview of the mobile app
    st.subheader("Preview Mobile App")
    
    # Introduce tabs to switch between different views
    tab1, tab2 = st.tabs(["Mobile Preview", "QR Code"])
    
    with tab1:
        # Phone frame container to simulate mobile device
        st.markdown("""
        <div style="max-width: 375px; margin: 0 auto; border: 12px solid #333; 
                    border-radius: 36px; padding: 8px; background-color: #333; 
                    box-shadow: 0px 10px 20px rgba(0,0,0,0.2);">
            <div style="position: relative; width: 100%; height: 48px; background-color: #333; 
                        border-radius: 24px 24px 0 0; margin-bottom: 1px;">
                <div style="position: absolute; width: 150px; height: 28px; background-color: #111; 
                            border-radius: 14px; top: 10px; left: 50%; transform: translateX(-50%);">
                </div>
            </div>
            <div style="width: 100%; height: 600px; overflow-y: auto; border-radius: 2px; background-color: white;">
                <div id="mobile-app-container" style="height: 100%;">
        """, unsafe_allow_html=True)
        
        # Render the mobile app UI inside the phone frame
        render_mobile_app()
        
        st.markdown("""
                </div>
            </div>
            <div style="position: relative; width: 100%; height: 48px; background-color: #333; 
                        border-radius: 0 0 24px 24px; margin-top: 1px;">
                <div style="position: absolute; width: 120px; height: 5px; background-color: #999; 
                            border-radius: 5px; bottom: 12px; left: 50%; transform: translateX(-50%);">
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        # Display QR code for mobile access
        st.markdown("""
        <div style="text-align: center; padding: 20px; border: 1px solid #e6e6e6; 
                    border-radius: 8px; background-color: white; max-width: 350px; margin: 0 auto;">
            <h3 style="margin-bottom: 20px;">Scan to Access on Your Device</h3>
            <div style="background-color: white; padding: 20px; width: 200px; height: 200px; 
                        margin: 0 auto; border: 1px solid #e6e6e6;">
                <!-- QR code placeholder - would be dynamically generated in production -->
                <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMDAgMjAwIj4KICA8c3R5bGU+CiAgICByZWN0IHsKICAgICAgZmlsbDogYmxhY2s7CiAgICAgIHdpZHRoOiA4cHg7CiAgICAgIGhlaWdodDogOHB4OwogICAgfQogIDwvc3R5bGU+CiAgPGcgZmlsbD0ibm9uZSI+CiAgICA8IS0tIFFSIGNvZGUgcG9zaXRpb24gbWFya2VycyAtLT4KICAgIDxnPgogICAgICA8IS0tIFRvcCBsZWZ0IC0tPgogICAgICA8cmVjdCB4PSIxNiIgeT0iMTYiIHdpZHRoPSI0MCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIxNiIgeT0iMjQiIHdpZHRoPSI4IiBoZWlnaHQ9IjMyIiAvPgogICAgICA8cmVjdCB4PSI0OCIgeT0iMjQiIHdpZHRoPSI4IiBoZWlnaHQ9IjMyIiAvPgogICAgICA8cmVjdCB4PSIxNiIgeT0iNTYiIHdpZHRoPSI0MCIgaGVpZ2h0PSI4IiAvPgogICAgICA8IS0tIFRvcCByaWdodCAtLT4KICAgICAgPHJlY3QgeD0iMTM2IiB5PSIxNiIgd2lkdGg9IjQwIiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjEzNiIgeT0iMjQiIHdpZHRoPSI4IiBoZWlnaHQ9IjMyIiAvPgogICAgICA8cmVjdCB4PSIxNjgiIHk9IjI0IiB3aWR0aD0iOCIgaGVpZ2h0PSIzMiIgLz4KICAgICAgPHJlY3QgeD0iMTM2IiB5PSI1NiIgd2lkdGg9IjQwIiBoZWlnaHQ9IjgiIC8+CiAgICAgIDwhLS0gQm90dG9tIGxlZnQgLS0+CiAgICAgIDxyZWN0IHg9IjE2IiB5PSIxMzYiIHdpZHRoPSI0MCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIxNiIgeT0iMTQ0IiB3aWR0aD0iOCIgaGVpZ2h0PSIzMiIgLz4KICAgICAgPHJlY3QgeD0iNDgiIHk9IjE0NCIgd2lkdGg9IjgiIGhlaWdodD0iMzIiIC8+CiAgICAgIDxyZWN0IHg9IjE2IiB5PSIxNzYiIHdpZHRoPSI0MCIgaGVpZ2h0PSI4IiAvPgogICAgPC9nPgogICAgPCEtLSBRUiBjb2RlIGRhdGEgc2VjdGlvbiAtLT4KICAgIDxnPgogICAgICA8cmVjdCB4PSI4MCIgeT0iMjQiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjEwNCIgeT0iMjQiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjExMiIgeT0iMjQiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjgwIiB5PSIzMiIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iOTYiIHk9IjMyIiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIxMTIiIHk9IjMyIiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSI4OCIgeT0iNDAiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9Ijk2IiB5PSI0MCIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iMTA0IiB5PSI0MCIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iODAiIHk9IjQ4IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSI5NiIgeT0iNDgiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjExMiIgeT0iNDgiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjgwIiB5PSI1NiIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iODgiIHk9IjU2IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSI5NiIgeT0iNTYiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjEwNCIgeT0iNTYiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDwhLS0gTW9yZSBRUiBkYXRhIHBvaW50cyAtLT4KICAgICAgPHJlY3QgeD0iMjQiIHk9IjgwIiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSI0MCIgeT0iODAiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjU2IiB5PSI4MCIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iNzIiIHk9IjgwIiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSI4OCIgeT0iODAiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjEyMCIgeT0iODAiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjEzNiIgeT0iODAiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjE1MiIgeT0iODAiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjE2OCIgeT0iODAiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjMyIiB5PSI4OCIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iNDgiIHk9Ijg4IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSI2NCIgeT0iODgiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9Ijk2IiB5PSI4OCIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iMTEyIiB5PSI4OCIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iMTI4IiB5PSI4OCIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iMTYwIiB5PSI4OCIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iMjQiIHk9Ijk2IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSI1NiIgeT0iOTYiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjcyIiB5PSI5NiIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iODgiIHk9Ijk2IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIxMDQiIHk9Ijk2IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIxMzYiIHk9Ijk2IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIxNTIiIHk9Ijk2IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIxNjgiIHk9Ijk2IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIzMiIgeT0iMTA0IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSI0OCIgeT0iMTA0IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSI2NCIgeT0iMTA0IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSI4MCIgeT0iMTA0IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIxMTIiIHk9IjEwNCIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iMTQ0IiB5PSIxMDQiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjE2MCIgeT0iMTA0IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIyNCIgeT0iMTEyIiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSI0MCIgeT0iMTEyIiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSI1NiIgeT0iMTEyIiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSI4OCIgeT0iMTEyIiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIxMjAiIHk9IjExMiIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iMTM2IiB5PSIxMTIiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjE1MiIgeT0iMTEyIiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIxNjgiIHk9IjExMiIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iODAiIHk9IjEyMCIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iOTYiIHk9IjEyMCIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iMTA0IiB5PSIxMjAiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjExMiIgeT0iMTIwIiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSI4MCIgeT0iMTI4IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSI4OCIgeT0iMTI4IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIxMDQiIHk9IjEyOCIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iODAiIHk9IjEzNiIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iOTYiIHk9IjEzNiIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iMTEyIiB5PSIxMzYiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjgwIiB5PSIxNDQiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9Ijk2IiB5PSIxNDQiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjEwNCIgeT0iMTQ0IiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIxMTIiIHk9IjE0NCIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iODAiIHk9IjE1MiIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iODgiIHk9IjE1MiIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iOTYiIHk9IjE1MiIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iMTA0IiB5PSIxNTIiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjExMiIgeT0iMTUyIiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIxMjAiIHk9IjE1MiIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iMTI4IiB5PSIxNTIiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjEzNiIgeT0iMTUyIiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIxNDQiIHk9IjE1MiIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iMTUyIiB5PSIxNTIiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICAgIDxyZWN0IHg9IjE2MCIgeT0iMTUyIiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiAvPgogICAgICA8cmVjdCB4PSIxNjgiIHk9IjE1MiIgd2lkdGg9IjgiIGhlaWdodD0iOCIgLz4KICAgICAgPHJlY3QgeD0iMTc2IiB5PSIxNTIiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIC8+CiAgICA8L2c+CiAgPC9nPgo8L3N2Zz4=" 
                    width="160" height="160" alt="QR Code for mobile app access">
            </div>
            <p style="margin-top: 15px; font-size: 14px; color: #5F6368;">
                Use your device's camera to scan this QR code and access the mobile companion app.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add app features section
    st.subheader("Mobile Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 8px; 
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1); height: 100%;">
            <div style="text-align: center; margin-bottom: 10px;">
                <span class="material-icons" style="font-size: 36px; color: #3367D6;">devices</span>
            </div>
            <h4 style="text-align: center; margin-bottom: 10px;">Responsive Design</h4>
            <p style="font-size: 14px; color: #5F6368; text-align: center;">
                Optimized for all devices from smartphones to tablets.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 8px; 
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1); height: 100%;">
            <div style="text-align: center; margin-bottom: 10px;">
                <span class="material-icons" style="font-size: 36px; color: #0F9D58;">sync</span>
            </div>
            <h4 style="text-align: center; margin-bottom: 10px;">Real-time Sync</h4>
            <p style="font-size: 14px; color: #5F6368; text-align: center;">
                Data syncs instantly between mobile and desktop.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 8px; 
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1); height: 100%;">
            <div style="text-align: center; margin-bottom: 10px;">
                <span class="material-icons" style="font-size: 36px; color: #DB4437;">notifications</span>
            </div>
            <h4 style="text-align: center; margin-bottom: 10px;">Push Notifications</h4>
            <p style="font-size: 14px; color: #5F6368; text-align: center;">
                Stay updated with important project alerts.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add download buttons section
    st.subheader("Get the Mobile App")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <a href="#" style="display: inline-block; background-color: black; color: white; 
                              text-decoration: none; padding: 8px 16px; border-radius: 8px; 
                              margin: 10px; text-align: center; min-width: 200px;">
                <div style="display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 24px; margin-right: 8px;">
                        <svg viewBox="0 0 24 24" width="24" height="24" fill="white">
                            <path d="M17.6,9.48l-1.91-3.3c-0.14-0.24-0.44-0.32-0.68-0.18L12,8.5V2H5C3.9,2,3,2.9,3,4v16c0,1.1,0.9,2,2,2h14c1.1,0,2-0.9,2-2
                            V8C21,8,17.6,9.48,17.6,9.48z M10.25,9.75H7.5v1.5h2.75v1.5H7.5v1.5h2.75V18h-4V6h4V9.75z M16.5,18h-1.5v-6h-1.5V18h-1.5V9
                            h4.5V18z"/>
                        </svg>
                    </span>
                    <div>
                        <div style="font-size: 10px; text-align: left;">GET IT ON</div>
                        <div style="font-size: 16px; font-weight: 500; text-align: left;">Google Play</div>
                    </div>
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <a href="#" style="display: inline-block; background-color: black; color: white; 
                              text-decoration: none; padding: 8px 16px; border-radius: 8px; 
                              margin: 10px; text-align: center; min-width: 200px;">
                <div style="display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 24px; margin-right: 8px;">
                        <svg viewBox="0 0 24 24" width="24" height="24" fill="white">
                            <path d="M17.05,12.04C17.03,9.82,18.81,8.04,20.98,8c0.01,2.23-1.78,4.01-3.93,4.04
                            M6.95,8C9.13,8.05,10.92,9.81,10.98,12.04c-2.17,0-3.97-1.79-4.03-4.04
                            M15.05,22h-6.1c-1.6,0-2.89-1.29-2.89-2.89V8.75C6.06,6.12,8.29,4,10.96,4H13c2.67,0,4.9,2.12,4.9,4.75
                            v10.36c0,1.6-1.29,2.89-2.89,2.89"/>
                        </svg>
                    </span>
                    <div>
                        <div style="font-size: 10px; text-align: left;">Download on the</div>
                        <div style="font-size: 16px; font-weight: 500; text-align: left;">App Store</div>
                    </div>
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    # Add PWA information
    st.markdown("""
    <div style="background-color: #F8F9FA; padding: 15px; border-radius: 8px; margin-top: 20px;">
        <h4>📱 Progressive Web App</h4>
        <p>
            For instant access, you can also use gcPanel as a Progressive Web App (PWA)
            by visiting the site on your mobile device and adding it to your home screen.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add instructions for using the mobile companion
    st.subheader("How to Use")
    
    with st.expander("Setup Instructions", expanded=False):
        st.markdown("""
        ### Setting Up the Mobile Companion
        
        1. **Download the App**: Use the download links above or scan the QR code.
        2. **Login**: Use the same credentials as your desktop gcPanel account.
        3. **Project Access**: Your projects will automatically sync to your mobile device.
        4. **Offline Mode**: The app supports offline mode for field use with limited connectivity.
        5. **Notifications**: Enable push notifications for real-time updates.
        """)
    
    with st.expander("Security Features", expanded=False):
        st.markdown("""
        ### Security Features
        
        The gcPanel mobile companion includes several security features:
        
        * **Biometric Authentication**: Use fingerprint or face recognition for quick access.
        * **Automatic Timeout**: Sessions automatically timeout after 30 minutes of inactivity.
        * **Remote Wipe**: Administrators can remotely wipe data if a device is lost or stolen.
        * **Encrypted Storage**: All local data is encrypted on your device.
        * **Secure Connections**: All data is transmitted over encrypted HTTPS connections.
        """)