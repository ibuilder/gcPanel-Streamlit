"""
Mobile companion module for the gcPanel application.

This module provides the mobile companion interface showing how the
construction management dashboard can be accessed on mobile devices.
"""

import streamlit as st
from components.mobile_app.layout import render_mobile_header, render_mobile_bottom_nav, render_mobile_frame

def mobile_dashboard():
    """
    Render a mobile-optimized dashboard with key metrics and activity.
    """
    # Render the header
    render_mobile_header()
    
    st.markdown("""
    <div style="padding: 0 10px 60px 10px;">  <!-- Add padding at bottom for the nav bar -->
        <h2 style="font-size: 20px; margin: 15px 0;">Highland Tower Development</h2>
        
        <!-- Project Progress Card -->
        <div style="background-color: white; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                    padding: 15px; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div style="font-size: 14px; color: #5F6368;">Overall Progress</div>
                    <div style="font-size: 24px; font-weight: 600; color: #3367D6;">72%</div>
                </div>
                <div style="background-color: #E8F0FE; border-radius: 50%; width: 40px; height: 40px; 
                            display: flex; align-items: center; justify-content: center;">
                    <span class="material-icons" style="color: #3367D6;">trending_up</span>
                </div>
            </div>
            <div style="height: 8px; background-color: #E8F0FE; border-radius: 4px; margin: 10px 0;">
                <div style="height: 8px; width: 72%; background-color: #3367D6; border-radius: 4px;"></div>
            </div>
            <div style="font-size: 12px; color: #5F6368;">Updated today at 9:30 AM</div>
        </div>
        
        <!-- Quick Stats -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
            <div style="background-color: white; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); padding: 15px;">
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <span class="material-icons" style="color: #FF5252; margin-right: 5px;">flag</span>
                    <div style="font-size: 14px; color: #5F6368;">Tasks Due</div>
                </div>
                <div style="font-size: 24px; font-weight: 600; color: #FF5252;">8</div>
            </div>
            <div style="background-color: white; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); padding: 15px;">
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <span class="material-icons" style="color: #4285F4; margin-right: 5px;">question_answer</span>
                    <div style="font-size: 14px; color: #5F6368;">Open RFIs</div>
                </div>
                <div style="font-size: 24px; font-weight: 600; color: #4285F4;">12</div>
            </div>
        </div>
        
        <!-- Today's Schedule -->
        <h3 style="font-size: 16px; margin: 15px 0;">Today's Schedule</h3>
        <div style="background-color: white; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                    padding: 15px; margin-bottom: 15px;">
            <div style="border-left: 3px solid #4285F4; padding-left: 10px; margin-bottom: 10px;">
                <div style="font-weight: 500; font-size: 14px;">9:00 AM - Site Inspection</div>
                <div style="font-size: 12px; color: #5F6368;">East Wing, Floor 3</div>
            </div>
            <div style="border-left: 3px solid #0F9D58; padding-left: 10px; margin-bottom: 10px;">
                <div style="font-weight: 500; font-size: 14px;">11:30 AM - Team Meeting</div>
                <div style="font-size: 12px; color: #5F6368;">Project Office</div>
            </div>
            <div style="border-left: 3px solid #DB4437; padding-left: 10px;">
                <div style="font-weight: 500; font-size: 14px;">2:00 PM - Concrete Pour</div>
                <div style="font-size: 12px; color: #5F6368;">West Foundation</div>
            </div>
        </div>
        
        <!-- Recent Activity -->
        <h3 style="font-size: 16px; margin: 15px 0;">Recent Activity</h3>
        <div style="background-color: white; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                    padding: 15px; margin-bottom: 15px;">
            <div style="display: flex; margin-bottom: 12px;">
                <span class="material-icons" style="color: #4285F4; margin-right: 10px;">question_answer</span>
                <div>
                    <div style="font-weight: 500; font-size: 14px;">RFI #123 was answered</div>
                    <div style="font-size: 12px; color: #5F6368;">2 hours ago</div>
                </div>
            </div>
            <div style="display: flex; margin-bottom: 12px;">
                <span class="material-icons" style="color: #0F9D58; margin-right: 10px;">check_circle</span>
                <div>
                    <div style="font-weight: 500; font-size: 14px;">Submittal #45 was approved</div>
                    <div style="font-size: 12px; color: #5F6368;">Yesterday</div>
                </div>
            </div>
            <div style="display: flex;">
                <span class="material-icons" style="color: #DB4437; margin-right: 10px;">warning</span>
                <div>
                    <div style="font-weight: 500; font-size: 14px;">Issue reported on Floor 5</div>
                    <div style="font-size: 12px; color: #5F6368;">Yesterday</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render the bottom navigation
    render_mobile_bottom_nav()

def mobile_tasks():
    """
    Render a mobile-optimized tasks list.
    """
    # Render the header
    render_mobile_header()
    
    st.markdown("""
    <div style="padding: 0 10px 60px 10px;">
        <h2 style="font-size: 20px; margin: 15px 0;">Tasks</h2>
        
        <!-- Filter options -->
        <div style="display: flex; margin-bottom: 15px; background-color: #F8F9FA; border-radius: 20px; padding: 5px;">
            <button style="flex: 1; background-color: #3367D6; color: white; border: none; 
                          border-radius: 20px; padding: 8px; font-size: 14px; font-weight: 500;">My Tasks</button>
            <button style="flex: 1; background: none; border: none; color: #5F6368; 
                          border-radius: 20px; padding: 8px; font-size: 14px;">All Tasks</button>
        </div>
        
        <!-- Tasks list -->
        <div style="background-color: white; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                    margin-bottom: 15px;">
            <!-- Task 1 -->
            <div style="padding: 15px; border-bottom: 1px solid #F1F3F4; display: flex; align-items: flex-start;">
                <div style="margin-right: 10px; padding-top: 2px;">
                    <span class="material-icons" style="color: #FF5252; font-size: 20px;">priority_high</span>
                </div>
                <div style="flex-grow: 1;">
                    <div style="font-weight: 500; margin-bottom: 5px;">Submit foundation inspection request</div>
                    <div style="font-size: 12px; display: flex; color: #5F6368; margin-bottom: 8px;">
                        <span style="margin-right: 10px;">Due: May 22, 2025</span>
                        <span>Assigned to you</span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 12px; background-color: #FFEBEE; color: #FF5252; 
                                    padding: 2px 8px; border-radius: 10px; margin-right: 8px;">High Priority</span>
                        <span style="font-size: 12px; background-color: #E8F0FE; color: #3367D6; 
                                    padding: 2px 8px; border-radius: 10px;">Permit</span>
                    </div>
                </div>
            </div>
            
            <!-- Task 2 -->
            <div style="padding: 15px; border-bottom: 1px solid #F1F3F4; display: flex; align-items: flex-start;">
                <div style="margin-right: 10px; padding-top: 2px;">
                    <span class="material-icons" style="color: #4285F4; font-size: 20px;">arrow_right</span>
                </div>
                <div style="flex-grow: 1;">
                    <div style="font-weight: 500; margin-bottom: 5px;">Review structural steel shop drawings</div>
                    <div style="font-size: 12px; display: flex; color: #5F6368; margin-bottom: 8px;">
                        <span style="margin-right: 10px;">Due: May 24, 2025</span>
                        <span>Assigned to you</span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 12px; background-color: #E8F0FE; color: #4285F4; 
                                    padding: 2px 8px; border-radius: 10px; margin-right: 8px;">Medium Priority</span>
                        <span style="font-size: 12px; background-color: #E8F0FE; color: #3367D6; 
                                    padding: 2px 8px; border-radius: 10px;">Submittal</span>
                    </div>
                </div>
            </div>
            
            <!-- Task 3 -->
            <div style="padding: 15px; display: flex; align-items: flex-start;">
                <div style="margin-right: 10px; padding-top: 2px;">
                    <span class="material-icons" style="color: #5F6368; font-size: 20px;">arrow_right</span>
                </div>
                <div style="flex-grow: 1;">
                    <div style="font-weight: 500; margin-bottom: 5px;">Finalize interior finish selections</div>
                    <div style="font-size: 12px; display: flex; color: #5F6368; margin-bottom: 8px;">
                        <span style="margin-right: 10px;">Due: May 30, 2025</span>
                        <span>Assigned to you</span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 12px; background-color: #F1F3F4; color: #5F6368; 
                                    padding: 2px 8px; border-radius: 10px; margin-right: 8px;">Low Priority</span>
                        <span style="font-size: 12px; background-color: #E8F0FE; color: #3367D6; 
                                    padding: 2px 8px; border-radius: 10px;">Design</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Floating Action Button -->
        <div style="position: fixed; bottom: 70px; right: 20px; z-index: 1001;">
            <button style="width: 56px; height: 56px; border-radius: 28px; background-color: #3367D6; 
                         border: none; box-shadow: 0 2px 10px rgba(0,0,0,0.2); display: flex; 
                         align-items: center; justify-content: center;">
                <span class="material-icons" style="color: white; font-size: 24px;">add</span>
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render the bottom navigation
    render_mobile_bottom_nav()

def render_mobile_screen():
    """
    Display the mobile app based on the selected screen.
    """
    # Get current page from session state
    current_page = st.session_state.get("mobile_page", "dashboard")
    
    # Render the appropriate page
    if current_page == "dashboard":
        mobile_dashboard()
    elif current_page == "tasks":
        mobile_tasks()
    else:
        # Placeholder for other screens
        render_mobile_header()
        st.markdown(f"""
        <div style="padding: 20px; text-align: center; margin-top: 40px;">
            <span class="material-icons" style="font-size: 48px; color: #3367D6;">{
                "photo_camera" if current_page == "photos" else
                "description" if current_page == "docs" else
                "more_horiz"
            }</span>
            <h2 style="margin-top: 20px; font-size: 20px;">Coming Soon</h2>
            <p style="color: #5F6368; margin-top: 10px;">
                The {
                    "Photos" if current_page == "photos" else
                    "Documents" if current_page == "docs" else
                    "More Options"
                } section is under development.
            </p>
        </div>
        """, unsafe_allow_html=True)
        render_mobile_bottom_nav()

def mobile_companion_page():
    """
    Display the mobile companion page.
    
    This page shows a demonstration of the mobile app interface for the gcPanel application.
    """
    # Initialize session state for mobile page if not set
    if "mobile_page" not in st.session_state:
        st.session_state.mobile_page = "dashboard"
    
    # Page header with Add/Edit buttons
    st.title("📱 Mobile Companion App")
    
    # Import and use our action buttons component
    from components.action_buttons import render_action_buttons
    
    # Display action buttons (Add, Edit) at the top of the page
    actions = render_action_buttons("Feature", show_delete=False)
    
    # Show description of the mobile companion
    st.markdown("""
    The gcPanel Mobile Companion allows field teams to access critical project information 
    on-the-go. The interface is optimized for smartphones and tablets, with easy navigation 
    and quick access to key features.
    """)
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Mobile Preview", "Features", "Getting Started"])
    
    with tab1:
        # Show mobile app preview in a phone frame
        def show_mobile_content():
            render_mobile_screen()
        
        # Use our mobile frame component to display the app
        render_mobile_frame(show_mobile_content)
        
        # Add a note about interactivity
        st.info("Note: This is a demonstration of the mobile interface. Some features may have limited functionality in this preview.")
    
    with tab2:
        # Show features of the mobile app
        st.subheader("Key Features")
        
        # Feature cards in a 3-column layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); height: 100%;">
                <div style="text-align: center; margin-bottom: 10px;">
                    <span class="material-icons" style="font-size: 36px; color: #3367D6;">dashboard</span>
                </div>
                <h4 style="text-align: center; margin-bottom: 10px;">Project Dashboard</h4>
                <p style="font-size: 14px; color: #5F6368; text-align: center;">
                    Real-time project metrics and KPIs for quick decisions on the go.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); height: 100%;">
                <div style="text-align: center; margin-bottom: 10px;">
                    <span class="material-icons" style="font-size: 36px; color: #DB4437;">assignment</span>
                </div>
                <h4 style="text-align: center; margin-bottom: 10px;">Task Management</h4>
                <p style="font-size: 14px; color: #5F6368; text-align: center;">
                    Create, assign, and update tasks directly from your mobile device.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); height: 100%;">
                <div style="text-align: center; margin-bottom: 10px;">
                    <span class="material-icons" style="font-size: 36px; color: #0F9D58;">photo_camera</span>
                </div>
                <h4 style="text-align: center; margin-bottom: 10px;">Site Photos</h4>
                <p style="font-size: 14px; color: #5F6368; text-align: center;">
                    Capture, tag, and organize site photos with location metadata.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Second row of features
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); height: 100%;">
                <div style="text-align: center; margin-bottom: 10px;">
                    <span class="material-icons" style="font-size: 36px; color: #4285F4;">description</span>
                </div>
                <h4 style="text-align: center; margin-bottom: 10px;">Document Access</h4>
                <p style="font-size: 14px; color: #5F6368; text-align: center;">
                    View and share project documents from anywhere in the field.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); height: 100%;">
                <div style="text-align: center; margin-bottom: 10px;">
                    <span class="material-icons" style="font-size: 36px; color: #F9AB00;">notifications</span>
                </div>
                <h4 style="text-align: center; margin-bottom: 10px;">Push Notifications</h4>
                <p style="font-size: 14px; color: #5F6368; text-align: center;">
                    Receive real-time alerts for important project updates.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); height: 100%;">
                <div style="text-align: center; margin-bottom: 10px;">
                    <span class="material-icons" style="font-size: 36px; color: #3367D6;">sync</span>
                </div>
                <h4 style="text-align: center; margin-bottom: 10px;">Offline Mode</h4>
                <p style="font-size: 14px; color: #5F6368; text-align: center;">
                    Work without internet connectivity and sync when back online.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        # Getting started guide
        st.subheader("Getting Started")
        
        # Create expandable sections
        with st.expander("Download the App", expanded=True):
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
        
        with st.expander("Login and Setup", expanded=False):
            st.markdown("""
            ### Setting Up Your Account
            
            1. **Download and Install**: Get the app from your device's app store.
            2. **Login**: Use your existing gcPanel credentials to sign in.
            3. **Project Selection**: Select your active project(s) for mobile access.
            4. **Notification Preferences**: Configure which alerts you want to receive.
            5. **Offline Access**: Select documents for offline availability.
            """)
            
            st.image("static/img/gcpanel.png", width=150, caption="Login with your existing gcPanel credentials")
        
        with st.expander("Security Features", expanded=False):
            st.markdown("""
            ### Security Information
            
            The gcPanel Mobile Companion includes several security features:
            
            * **Biometric Authentication**: Enable fingerprint or face recognition for quick secure access.
            * **Auto Timeout**: Sessions automatically timeout after 30 minutes of inactivity.
            * **Remote Wipe**: Administrators can remotely wipe app data if a device is lost or stolen.
            * **Encrypted Storage**: All local data is encrypted on your device.
            * **Secure Connections**: All data transfers use encrypted HTTPS connections.
            """)
    
    # Add a "Learn More" section at the bottom
    st.markdown("""
    ---
    
    ### Want to Learn More?
    
    Contact your system administrator to get access to the mobile companion app for your project.
    """)
    
    # Track button clicks for Add/Edit
    if actions['add_clicked']:
        st.session_state.show_add_form = True
        st.rerun()
    elif actions['edit_clicked']:
        st.session_state.show_edit_form = True
        st.rerun()
    
    # Display forms if buttons were clicked
    if st.session_state.get("show_add_form", False):
        st.subheader("Add New Mobile Feature")
        with st.form("add_feature_form"):
            feature_name = st.text_input("Feature Name")
            feature_description = st.text_area("Feature Description")
            feature_icon = st.selectbox("Feature Icon", ["dashboard", "assignment", "photo_camera", "description", "notifications"])
            st.form_submit_button("Save Feature", type="primary")
        
        # Add a cancel button
        if st.button("Cancel"):
            st.session_state.show_add_form = False
            st.rerun()
    
    if st.session_state.get("show_edit_form", False):
        st.subheader("Edit Mobile Features")
        with st.form("edit_features_form"):
            st.multiselect("Select Features to Edit", ["Dashboard", "Task Management", "Site Photos", "Document Access", "Push Notifications", "Offline Mode"])
            st.form_submit_button("Save Changes", type="primary")
        
        # Add a cancel button
        if st.button("Cancel"):
            st.session_state.show_edit_form = False
            st.rerun()