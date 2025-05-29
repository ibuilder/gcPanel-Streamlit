"""
Highland Tower Development - Mobile Optimization
Mobile-responsive design and field operations interface
"""

import streamlit as st
from typing import Dict, List

def apply_mobile_responsive_styles():
    """Apply mobile-responsive CSS for Highland Tower platform"""
    st.markdown("""
    <style>
    /* Mobile-first responsive design */
    @media (max-width: 768px) {
        .block-container {
            padding: 16px !important;
            margin: 8px !important;
        }
        
        .module-header h1 {
            font-size: 24px !important;
        }
        
        .stColumns > div {
            margin-bottom: 16px;
        }
        
        .metric-card {
            padding: 12px;
            margin: 8px 0;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #3b82f6;
        }
        
        .mobile-nav-button {
            width: 100%;
            padding: 12px;
            margin: 4px 0;
            border: none;
            border-radius: 6px;
            background: #f8fafc;
            color: #374151;
            font-size: 16px;
            text-align: left;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .mobile-nav-button:hover {
            background: #e2e8f0;
            transform: translateX(4px);
        }
        
        .mobile-nav-button.active {
            background: #3b82f6;
            color: white;
        }
        
        .field-data-entry {
            background: #f0f9ff;
            border: 1px solid #bae6fd;
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
        }
        
        .safety-alert {
            background: #fef2f2;
            border: 1px solid #fecaca;
            border-radius: 8px;
            padding: 12px;
            margin: 8px 0;
            border-left: 4px solid #ef4444;
        }
        
        .progress-indicator {
            width: 100%;
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            overflow: hidden;
            margin: 8px 0;
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #10b981, #059669);
            transition: width 0.3s ease;
        }
    }
    
    /* Touch-friendly interactions */
    .stButton > button {
        min-height: 44px !important;
        font-size: 16px !important;
    }
    
    .stSelectbox > div > div {
        min-height: 44px !important;
    }
    
    .stTextInput > div > div > input {
        min-height: 44px !important;
        font-size: 16px !important;
    }
    
    /* Quick action buttons for field use */
    .quick-action-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 12px;
        margin: 16px 0;
    }
    
    .quick-action-btn {
        padding: 16px;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        border: none;
        border-radius: 8px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 14px;
        font-weight: 600;
    }
    
    .quick-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Offline indicator */
    .offline-indicator {
        position: fixed;
        top: 10px;
        right: 10px;
        background: #ef4444;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        z-index: 1000;
        display: none;
    }
    
    .online-indicator {
        position: fixed;
        top: 10px;
        right: 10px;
        background: #10b981;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

def render_mobile_quick_actions():
    """Render quick action buttons for field operations"""
    st.markdown("### Quick Field Actions")
    
    actions = [
        ("📋", "Daily Report", "daily_report"),
        ("📸", "Photo Upload", "photo_upload"),
        ("⚠️", "Safety Report", "safety_report"),
        ("🔧", "Equipment Issue", "equipment_issue"),
        ("📞", "Call Support", "call_support"),
        ("📍", "Location Check", "location_check")
    ]
    
    cols = st.columns(3)
    
    for i, (icon, label, action_key) in enumerate(actions):
        with cols[i % 3]:
            if st.button(f"{icon}\n{label}", key=action_key, use_container_width=True):
                return action_key
    
    return None

def render_field_data_entry():
    """Render mobile-optimized data entry form"""
    st.markdown('<div class="field-data-entry">', unsafe_allow_html=True)
    st.markdown("### Field Data Entry")
    
    with st.form("field_data_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            crew_count = st.number_input("Crew Count", min_value=0, max_value=100, value=24)
            weather = st.selectbox("Weather", ["Sunny", "Cloudy", "Rainy", "Windy"])
        
        with col2:
            temperature = st.number_input("Temperature (°F)", min_value=-20, max_value=120, value=72)
            safety_score = st.slider("Safety Score", 0, 100, 95)
        
        work_completed = st.text_area("Work Completed Today", height=100)
        issues = st.text_area("Issues/Concerns", height=80)
        
        submitted = st.form_submit_button("Submit Report", use_container_width=True)
        
        if submitted:
            st.success("Field report submitted successfully!")
            return {
                "crew_count": crew_count,
                "weather": weather,
                "temperature": temperature,
                "safety_score": safety_score,
                "work_completed": work_completed,
                "issues": issues
            }
    
    st.markdown('</div>', unsafe_allow_html=True)
    return None

def render_mobile_metrics():
    """Render mobile-optimized metrics display"""
    metrics_data = [
        ("Project Progress", "72.5%", "+3.2%", "green"),
        ("Budget Used", "$31.2M", "68% of total", "blue"),
        ("Safety Score", "97.8", "Excellent", "green"),
        ("Crew Efficiency", "105%", "+5% target", "green")
    ]
    
    for metric, value, delta, color in metrics_data:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 14px; color: #6b7280; margin-bottom: 4px;">{metric}</div>
            <div style="font-size: 24px; font-weight: bold; color: #111827; margin-bottom: 4px;">{value}</div>
            <div style="font-size: 12px; color: {'#10b981' if color == 'green' else '#3b82f6'};">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

def render_mobile_safety_alerts():
    """Render mobile safety alerts"""
    alerts = [
        ("High Wind Alert", "Wind speeds 25+ mph expected this afternoon", "warning"),
        ("Equipment Inspection Due", "Crane #2 inspection due tomorrow", "info"),
        ("Safety Training", "Fall protection training scheduled Friday", "success")
    ]
    
    st.markdown("### Safety Alerts")
    
    for title, message, alert_type in alerts:
        color = "#ef4444" if alert_type == "warning" else "#3b82f6" if alert_type == "info" else "#10b981"
        
        st.markdown(f"""
        <div class="safety-alert" style="border-left-color: {color};">
            <div style="font-weight: bold; color: {color};">{title}</div>
            <div style="font-size: 14px; color: #374151; margin-top: 4px;">{message}</div>
        </div>
        """, unsafe_allow_html=True)

def render_mobile_progress_indicators():
    """Render mobile progress indicators"""
    phases = [
        ("Foundation", 100, "#10b981"),
        ("Structure", 85, "#3b82f6"),
        ("MEP Systems", 65, "#f59e0b"),
        ("Finishes", 30, "#ef4444"),
        ("Final Inspections", 0, "#6b7280")
    ]
    
    st.markdown("### Phase Progress")
    
    for phase, progress, color in phases:
        st.markdown(f"""
        <div style="margin: 12px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 500;">{phase}</span>
                <span style="color: {color}; font-weight: bold;">{progress}%</span>
            </div>
            <div class="progress-indicator">
                <div class="progress-bar" style="width: {progress}%; background: {color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_mobile_navigation():
    """Render mobile-optimized navigation"""
    nav_items = [
        ("🏠", "Dashboard"),
        ("📋", "Daily Reports"),
        ("📸", "Photos"),
        ("💰", "Costs"),
        ("⚠️", "Safety"),
        ("📊", "Analytics")
    ]
    
    selected_item = st.session_state.get('current_menu', 'Dashboard')
    
    cols = st.columns(len(nav_items))
    
    for i, (icon, label) in enumerate(nav_items):
        with cols[i]:
            is_active = selected_item == label
            button_class = "mobile-nav-button active" if is_active else "mobile-nav-button"
            
            if st.button(f"{icon}\n{label}", key=f"mobile_nav_{label}"):
                st.session_state.current_menu = label
                st.rerun()

def check_mobile_device():
    """Check if user is on mobile device"""
    # This would typically use JavaScript to detect mobile, 
    # but for Streamlit we'll use a simple approach
    return st.session_state.get('mobile_mode', False)

def toggle_mobile_mode():
    """Toggle mobile optimization mode"""
    if st.button("📱 Toggle Mobile Mode"):
        st.session_state.mobile_mode = not st.session_state.get('mobile_mode', False)
        st.rerun()

def render_mobile_dashboard():
    """Render complete mobile-optimized dashboard"""
    apply_mobile_responsive_styles()
    
    # Mobile header
    st.markdown("""
    <div style="text-align: center; padding: 16px 0; background: linear-gradient(135deg, #1e3a8a, #3b82f6); 
                border-radius: 8px; margin-bottom: 16px; color: white;">
        <h2 style="margin: 0; font-size: 20px;">Highland Tower Mobile</h2>
        <p style="margin: 4px 0 0 0; font-size: 14px; opacity: 0.9;">Field Operations Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Connection status indicator
    st.markdown("""
    <div class="online-indicator">
        🟢 Online
    </div>
    """, unsafe_allow_html=True)
    
    # Quick actions
    action = render_mobile_quick_actions()
    
    if action:
        st.success(f"Action triggered: {action}")
    
    # Mobile metrics
    render_mobile_metrics()
    
    # Progress indicators
    render_mobile_progress_indicators()
    
    # Safety alerts
    render_mobile_safety_alerts()
    
    # Field data entry
    field_data = render_field_data_entry()
    
    if field_data:
        st.success("Field data captured successfully!")
    
    return True