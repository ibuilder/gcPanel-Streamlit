"""
Mobile application layout component for gcPanel.

This module provides layout components optimized for mobile devices,
allowing users to access the construction management system on smartphones and tablets.
"""

import streamlit as st
from datetime import datetime

def check_mobile_device():
    """
    Check if the user is on a mobile device based on viewport width.
    
    Returns:
        bool: True if user is on a mobile device, False otherwise
    """
    # Using custom JavaScript to detect viewport width
    mobile_detector = """
    <script>
        const updateViewportWidth = () => {
            const viewportWidth = window.innerWidth;
            localStorage.setItem('viewportWidth', viewportWidth);
        };
        
        // Update on load
        updateViewportWidth();
        
        // Update on resize
        window.addEventListener('resize', updateViewportWidth);
    </script>
    """
    
    st.markdown(mobile_detector, unsafe_allow_html=True)
    
    # We'll set the mobile threshold at 768px
    # Since we can't directly access localStorage from Python,
    # we'll make best-effort adjustments based on expected device types
    return True  # For now, we'll always show mobile optimized view in the mobile section

def render_mobile_header():
    """
    Render a mobile-optimized header for the app.
    """
    # Current date
    current_date = datetime.now().strftime("%b %d, %Y")
    
    # Mobile header with logo, project selector and menu button
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; 
                padding: 10px 0; border-bottom: 1px solid #DADCE0;">
        <div style="display: flex; align-items: center;">
            <img src="gcpanel.png" style="height: 30px; margin-right: 10px;">
            <div>
                <div style="font-weight: 600; color: #3367D6;">gcPanel</div>
                <div style="font-size: 12px; color: #5F6368;">{}</div>
            </div>
        </div>
        <div>
            <button id="mobile-menu-btn" style="background: none; border: none; cursor: pointer;">
                <span class="material-icons" style="font-size: 24px; color: #3367D6;">menu</span>
            </button>
        </div>
    </div>
    """.format(current_date), unsafe_allow_html=True)

def render_mobile_bottom_nav():
    """
    Render a mobile-optimized bottom navigation bar.
    """
    # Get current page to highlight active item
    current_page = st.session_state.get("mobile_page", "dashboard")
    
    # Bottom navigation with icons for main sections
    st.markdown("""
    <style>
        .mobile-bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: white;
            display: flex;
            justify-content: space-around;
            padding: 10px 0;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
            z-index: 1000;
        }
        
        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-decoration: none;
            color: #5F6368;
            font-size: 12px;
        }
        
        .nav-item.active {
            color: #3367D6;
        }
        
        .nav-item .material-icons {
            font-size: 20px;
            margin-bottom: 2px;
        }
    </style>
    
    <div class="mobile-bottom-nav">
        <a href="#" class="nav-item {}" id="nav-dashboard" onclick="setActivePage('dashboard')">
            <span class="material-icons">dashboard</span>
            <span>Dashboard</span>
        </a>
        <a href="#" class="nav-item {}" id="nav-tasks" onclick="setActivePage('tasks')">
            <span class="material-icons">assignment</span>
            <span>Tasks</span>
        </a>
        <a href="#" class="nav-item {}" id="nav-photos" onclick="setActivePage('photos')">
            <span class="material-icons">photo_camera</span>
            <span>Photos</span>
        </a>
        <a href="#" class="nav-item {}" id="nav-docs" onclick="setActivePage('docs')">
            <span class="material-icons">description</span>
            <span>Documents</span>
        </a>
        <a href="#" class="nav-item {}" id="nav-more" onclick="setActivePage('more')">
            <span class="material-icons">more_horiz</span>
            <span>More</span>
        </a>
    </div>
    
    <script>
        function setActivePage(page) {
            // Update active class visually
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            document.getElementById('nav-' + page).classList.add('active');
            
            // Store in session state via form submission
            const formData = new FormData();
            formData.append('mobile_page', page);
            
            fetch(window.location.href, {
                method: 'POST',
                body: formData
            }).then(() => {
                window.location.reload();
            });
        }
        
        // Set initial active state
        document.getElementById('nav-{}').classList.add('active');
    </script>
    """.format(
        "active" if current_page == "dashboard" else "",
        "active" if current_page == "tasks" else "",
        "active" if current_page == "photos" else "",
        "active" if current_page == "docs" else "",
        "active" if current_page == "more" else "",
        current_page
    ), unsafe_allow_html=True)

def mobile_dashboard():
    """
    Render a mobile-optimized dashboard with key metrics and activity.
    """
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
        
        <!-- Weather Card -->
        <div style="background-color: white; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                    padding: 15px; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 14px; color: #5F6368;">Current Weather</div>
                    <div style="font-size: 24px; font-weight: 600;">72°F</div>
                    <div style="font-size: 14px; color: #5F6368;">Sunny</div>
                </div>
                <span class="material-icons" style="font-size: 40px; color: #F9AB00;">wb_sunny</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def mobile_tasks():
    """
    Render a mobile-optimized tasks list.
    """
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
            <div style="padding: 15px; border-bottom: 1px solid #F1F3F4; display: flex; align-items: flex-start;">
                <div style="margin-right: 10px; padding-top: 2px;">
                    <span class="material-icons" style="color: #4285F4; font-size: 20px;">arrow_right</span>
                </div>
                <div style="flex-grow: 1;">
                    <div style="font-weight: 500; margin-bottom: 5px;">Coordinate MEP rough-in schedule</div>
                    <div style="font-size: 12px; display: flex; color: #5F6368; margin-bottom: 8px;">
                        <span style="margin-right: 10px;">Due: May 25, 2025</span>
                        <span>Assigned to you</span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 12px; background-color: #E8F0FE; color: #4285F4; 
                                    padding: 2px 8px; border-radius: 10px; margin-right: 8px;">Medium Priority</span>
                        <span style="font-size: 12px; background-color: #E8F0FE; color: #3367D6; 
                                    padding: 2px 8px; border-radius: 10px;">Coordination</span>
                    </div>
                </div>
            </div>
            
            <!-- Task 4 -->
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

def mobile_photos():
    """
    Render a mobile-optimized photo gallery for site documentation.
    """
    st.markdown("""
    <div style="padding: 0 10px 60px 10px;">
        <h2 style="font-size: 20px; margin: 15px 0;">Site Photos</h2>
        
        <!-- Filter options -->
        <div style="display: flex; margin-bottom: 15px; overflow-x: auto; padding-bottom: 5px;">
            <button style="background-color: #3367D6; color: white; border: none; 
                          border-radius: 20px; padding: 8px 16px; font-size: 14px; 
                          margin-right: 8px; white-space: nowrap;">All Photos</button>
            <button style="background: none; border: 1px solid #DADCE0; color: #5F6368; 
                          border-radius: 20px; padding: 8px 16px; font-size: 14px; 
                          margin-right: 8px; white-space: nowrap;">Foundation</button>
            <button style="background: none; border: 1px solid #DADCE0; color: #5F6368; 
                          border-radius: 20px; padding: 8px 16px; font-size: 14px; 
                          margin-right: 8px; white-space: nowrap;">Structure</button>
            <button style="background: none; border: 1px solid #DADCE0; color: #5F6368; 
                          border-radius: 20px; padding: 8px 16px; font-size: 14px; 
                          margin-right: 8px; white-space: nowrap;">MEP</button>
        </div>
        
        <!-- Photo Gallery - Using local sample images -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
            <!-- Sample photos with placeholder images -->
            <div style="position: relative;">
                <div style="width: 100%; border-radius: 8px; aspect-ratio: 1/1; 
                          background-color: #E8F0FE; display: flex; align-items: center; 
                          justify-content: center;">
                    <span class="material-icons" style="font-size: 40px; color: #3367D6;">image</span>
                </div>
                <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.7)); 
                            border-radius: 0 0 8px 8px; padding: 8px;">
                    <div style="font-size: 12px; color: white;">Foundation work</div>
                    <div style="font-size: 10px; color: rgba(255,255,255,0.8);">May 10, 2025</div>
                </div>
            </div>
            <div style="position: relative;">
                <div style="width: 100%; border-radius: 8px; aspect-ratio: 1/1; 
                          background-color: #E8F0FE; display: flex; align-items: center; 
                          justify-content: center;">
                    <span class="material-icons" style="font-size: 40px; color: #3367D6;">image</span>
                </div>
                <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.7)); 
                            border-radius: 0 0 8px 8px; padding: 8px;">
                    <div style="font-size: 12px; color: white;">Steel structure</div>
                    <div style="font-size: 10px; color: rgba(255,255,255,0.8);">May 8, 2025</div>
                </div>
            </div>
            <div style="position: relative;">
                <div style="width: 100%; border-radius: 8px; aspect-ratio: 1/1; 
                          background-color: #E8F0FE; display: flex; align-items: center; 
                          justify-content: center;">
                    <span class="material-icons" style="font-size: 40px; color: #3367D6;">image</span>
                </div>
                <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.7)); 
                            border-radius: 0 0 8px 8px; padding: 8px;">
                    <div style="font-size: 12px; color: white;">Elevator shaft</div>
                    <div style="font-size: 10px; color: rgba(255,255,255,0.8);">May 5, 2025</div>
                </div>
            </div>
            <div style="position: relative;">
                <div style="width: 100%; border-radius: 8px; aspect-ratio: 1/1; 
                          background-color: #E8F0FE; display: flex; align-items: center; 
                          justify-content: center;">
                    <span class="material-icons" style="font-size: 40px; color: #3367D6;">image</span>
                </div>
                <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.7)); 
                            border-radius: 0 0 8px 8px; padding: 8px;">
                    <div style="font-size: 12px; color: white;">MEP coordination</div>
                    <div style="font-size: 10px; color: rgba(255,255,255,0.8);">May 3, 2025</div>
                </div>
            </div>
        </div>
        
        <!-- Floating Action Button -->
        <div style="position: fixed; bottom: 70px; right: 20px; z-index: 1001;">
            <button style="width: 56px; height: 56px; border-radius: 28px; background-color: #3367D6; 
                         border: none; box-shadow: 0 2px 10px rgba(0,0,0,0.2); display: flex; 
                         align-items: center; justify-content: center;">
                <span class="material-icons" style="color: white; font-size: 24px;">photo_camera</span>
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)

def mobile_documents():
    """
    Render a mobile-optimized document browser.
    """
    st.markdown("""
    <div style="padding: 0 10px 60px 10px;">
        <h2 style="font-size: 20px; margin: 15px 0;">Documents</h2>
        
        <!-- Search bar -->
        <div style="position: relative; margin-bottom: 15px;">
            <input type="text" placeholder="Search documents..." 
                   style="width: 100%; padding: 10px 15px 10px 40px; border-radius: 8px; 
                          border: 1px solid #DADCE0; font-size: 14px; box-sizing: border-box;">
            <span class="material-icons" style="position: absolute; left: 12px; top: 50%; transform: translateY(-50%); 
                                               color: #5F6368; font-size: 20px;">search</span>
        </div>
        
        <!-- Recent Documents -->
        <h3 style="font-size: 16px; margin: 15px 0;">Recent Documents</h3>
        <div style="background-color: white; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                    margin-bottom: 15px;">
            <!-- Document 1 -->
            <div style="padding: 15px; border-bottom: 1px solid #F1F3F4; display: flex; align-items: center;">
                <span class="material-icons" style="color: #DB4437; font-size: 24px; margin-right: 15px;">picture_as_pdf</span>
                <div style="flex-grow: 1;">
                    <div style="font-weight: 500; font-size: 14px;">Construction Drawings v2.3.pdf</div>
                    <div style="font-size: 12px; color: #5F6368;">12.5 MB • Updated 2 days ago</div>
                </div>
                <span class="material-icons" style="color: #5F6368; font-size: 20px;">more_vert</span>
            </div>
            
            <!-- Document 2 -->
            <div style="padding: 15px; border-bottom: 1px solid #F1F3F4; display: flex; align-items: center;">
                <span class="material-icons" style="color: #4285F4; font-size: 24px; margin-right: 15px;">description</span>
                <div style="flex-grow: 1;">
                    <div style="font-weight: 500; font-size: 14px;">Meeting Minutes - May 15.docx</div>
                    <div style="font-size: 12px; color: #5F6368;">245 KB • Updated 3 days ago</div>
                </div>
                <span class="material-icons" style="color: #5F6368; font-size: 20px;">more_vert</span>
            </div>
            
            <!-- Document 3 -->
            <div style="padding: 15px; border-bottom: 1px solid #F1F3F4; display: flex; align-items: center;">
                <span class="material-icons" style="color: #0F9D58; font-size: 24px; margin-right: 15px;">table_chart</span>
                <div style="flex-grow: 1;">
                    <div style="font-weight: 500; font-size: 14px;">Budget Tracking Q2.xlsx</div>
                    <div style="font-size: 12px; color: #5F6368;">1.8 MB • Updated 5 days ago</div>
                </div>
                <span class="material-icons" style="color: #5F6368; font-size: 20px;">more_vert</span>
            </div>
            
            <!-- Document 4 -->
            <div style="padding: 15px; display: flex; align-items: center;">
                <span class="material-icons" style="color: #DB4437; font-size: 24px; margin-right: 15px;">picture_as_pdf</span>
                <div style="flex-grow: 1;">
                    <div style="font-weight: 500; font-size: 14px;">Structural Calculations.pdf</div>
                    <div style="font-size: 12px; color: #5F6368;">8.3 MB • Updated 1 week ago</div>
                </div>
                <span class="material-icons" style="color: #5F6368; font-size: 20px;">more_vert</span>
            </div>
        </div>
        
        <!-- Document Folders -->
        <h3 style="font-size: 16px; margin: 15px 0;">Folders</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
            <div style="background-color: white; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                        padding: 15px; display: flex; align-items: center;">
                <span class="material-icons" style="color: #4285F4; font-size: 28px; margin-right: 10px;">folder</span>
                <div>
                    <div style="font-weight: 500; font-size: 14px;">Drawings</div>
                    <div style="font-size: 12px; color: #5F6368;">32 files</div>
                </div>
            </div>
            <div style="background-color: white; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                        padding: 15px; display: flex; align-items: center;">
                <span class="material-icons" style="color: #4285F4; font-size: 28px; margin-right: 10px;">folder</span>
                <div>
                    <div style="font-weight: 500; font-size: 14px;">Specifications</div>
                    <div style="font-size: 12px; color: #5F6368;">17 files</div>
                </div>
            </div>
            <div style="background-color: white; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                        padding: 15px; display: flex; align-items: center;">
                <span class="material-icons" style="color: #4285F4; font-size: 28px; margin-right: 10px;">folder</span>
                <div>
                    <div style="font-weight: 500; font-size: 14px;">Photos</div>
                    <div style="font-size: 12px; color: #5F6368;">156 files</div>
                </div>
            </div>
            <div style="background-color: white; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                        padding: 15px; display: flex; align-items: center;">
                <span class="material-icons" style="color: #4285F4; font-size: 28px; margin-right: 10px;">folder</span>
                <div>
                    <div style="font-weight: 500; font-size: 14px;">Contracts</div>
                    <div style="font-size: 12px; color: #5F6368;">8 files</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def mobile_more_menu():
    """
    Render a mobile-optimized more menu with additional options.
    """
    st.markdown("""
    <div style="padding: 0 10px 60px 10px;">
        <h2 style="font-size: 20px; margin: 15px 0;">More Options</h2>
        
        <!-- User profile section -->
        <div style="background-color: white; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                    padding: 15px; margin-bottom: 15px; display: flex; align-items: center;">
            <div style="width: 50px; height: 50px; border-radius: 25px; background-color: #3367D6; 
                       display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                <span style="color: white; font-size: 20px; font-weight: 500;">JS</span>
            </div>
            <div>
                <div style="font-weight: 500; font-size: 16px;">John Smith</div>
                <div style="font-size: 14px; color: #5F6368;">Project Manager</div>
            </div>
        </div>
        
        <!-- Menu items -->
        <div style="background-color: white; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                    margin-bottom: 15px;">
            <!-- Menu item 1 -->
            <div style="padding: 15px; border-bottom: 1px solid #F1F3F4; display: flex; align-items: center;">
                <span class="material-icons" style="color: #4285F4; font-size: 24px; margin-right: 15px;">view_in_ar</span>
                <div style="flex-grow: 1; font-size: 16px;">BIM Viewer</div>
                <span class="material-icons" style="color: #5F6368; font-size: 20px;">chevron_right</span>
            </div>
            
            <!-- Menu item 2 -->
            <div style="padding: 15px; border-bottom: 1px solid #F1F3F4; display: flex; align-items: center;">
                <span class="material-icons" style="color: #DB4437; font-size: 24px; margin-right: 15px;">notifications</span>
                <div style="flex-grow: 1; font-size: 16px;">Notifications</div>
                <span class="material-icons" style="color: #5F6368; font-size: 20px;">chevron_right</span>
            </div>
            
            <!-- Menu item 3 -->
            <div style="padding: 15px; border-bottom: 1px solid #F1F3F4; display: flex; align-items: center;">
                <span class="material-icons" style="color: #0F9D58; font-size: 24px; margin-right: 15px;">people</span>
                <div style="flex-grow: 1; font-size: 16px;">Team</div>
                <span class="material-icons" style="color: #5F6368; font-size: 20px;">chevron_right</span>
            </div>
            
            <!-- Menu item 4 -->
            <div style="padding: 15px; border-bottom: 1px solid #F1F3F4; display: flex; align-items: center;">
                <span class="material-icons" style="color: #F9AB00; font-size: 24px; margin-right: 15px;">bar_chart</span>
                <div style="flex-grow: 1; font-size: 16px;">Reports</div>
                <span class="material-icons" style="color: #5F6368; font-size: 20px;">chevron_right</span>
            </div>
            
            <!-- Menu item 5 -->
            <div style="padding: 15px; display: flex; align-items: center;">
                <span class="material-icons" style="color: #5F6368; font-size: 24px; margin-right: 15px;">settings</span>
                <div style="flex-grow: 1; font-size: 16px;">Settings</div>
                <span class="material-icons" style="color: #5F6368; font-size: 20px;">chevron_right</span>
            </div>
        </div>
        
        <!-- App version -->
        <div style="text-align: center; margin-top: 30px; color: #5F6368; font-size: 12px;">
            <div>gcPanel Mobile App</div>
            <div>Version 1.0.0</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_mobile_app():
    """
    Main function to render the mobile application interface.
    
    This simulates how the app would appear on a mobile device.
    """
    # First check if we're on a mobile device
    is_mobile = check_mobile_device()
    
    # Apply mobile-specific styling
    st.markdown("""
    <style>
        /* Mobile-specific styling */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 0 !important;
                max-width: 100% !important;
            }
        }
        
        /* Hide Streamlit footer and header for app-like experience */
        footer {
            visibility: hidden;
        }
        
        /* Handle safe areas for modern mobile browsers */
        @supports(padding: max(0px)) {
            .mobile-body {
                padding-left: max(12px, env(safe-area-inset-left));
                padding-right: max(12px, env(safe-area-inset-right));
                padding-bottom: max(12px, env(safe-area-inset-bottom));
            }
        }
    </style>
    
    <!-- Ensure mobile viewport is configured properly -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
    <!-- Fix for iOS safe areas -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    """, unsafe_allow_html=True)
    
    # Render the mobile header (always included)
    render_mobile_header()
    
    # Get the current mobile page from session state (default to dashboard)
    current_page = st.session_state.get("mobile_page", "dashboard")
    
    # Render the appropriate page content
    if current_page == "dashboard":
        mobile_dashboard()
    elif current_page == "tasks":
        mobile_tasks()
    elif current_page == "photos":
        mobile_photos()
    elif current_page == "docs":
        mobile_documents()
    elif current_page == "more":
        mobile_more_menu()
    
    # Render the mobile bottom navigation (always included)
    render_mobile_bottom_nav()
    
    # Add a hidden form element to capture page navigation from the bottom nav
    if st.session_state.get("mobile_page") != st.session_state.get("prev_mobile_page"):
        st.session_state.prev_mobile_page = st.session_state.get("mobile_page")