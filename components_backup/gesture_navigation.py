"""
Intuitive Gesture-Based Navigation

This module provides touch-friendly navigation with swipe gestures,
keyboard shortcuts, and intuitive navigation patterns for enhanced UX.
"""
import streamlit as st
from typing import List, Dict, Optional, Callable

def apply_gesture_navigation_styles() -> None:
    """Apply CSS and JavaScript for gesture-based navigation."""
    
    st.markdown("""
    <style>
    /* Gesture-friendly navigation styles */
    .gesture-nav-container {
        position: relative;
        touch-action: pan-x;
        overflow-x: hidden;
    }
    
    .swipe-indicator {
        position: fixed;
        top: 50%;
        transform: translateY(-50%);
        background: rgba(0,0,0,0.7);
        color: white;
        padding: 10px;
        border-radius: 20px;
        font-size: 24px;
        z-index: 1000;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .swipe-left {
        right: 20px;
        animation: swipe-hint-left 1s ease-in-out;
    }
    
    .swipe-right {
        left: 20px;
        animation: swipe-hint-right 1s ease-in-out;
    }
    
    /* Navigation breadcrumbs */
    .nav-breadcrumbs {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 0;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    
    .breadcrumb-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 6px 12px;
        background: #f8f9fa;
        border-radius: 20px;
        font-size: 14px;
        color: #666;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .breadcrumb-item:hover {
        background: #e9ecef;
        color: #333;
        transform: translateY(-1px);
    }
    
    .breadcrumb-item.active {
        background: #007bff;
        color: white;
    }
    
    .breadcrumb-separator {
        color: #ccc;
        font-size: 12px;
    }
    
    /* Quick action buttons */
    .quick-actions {
        position: fixed;
        bottom: 20px;
        right: 20px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        z-index: 999;
    }
    
    .quick-action-btn {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: #007bff;
        color: white;
        border: none;
        font-size: 20px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,123,255,0.3);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .quick-action-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0,123,255,0.4);
    }
    
    .quick-action-btn.primary {
        background: #28a745;
        width: 64px;
        height: 64px;
        font-size: 24px;
    }
    
    /* Keyboard shortcuts hint */
    .keyboard-hints {
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-size: 12px;
        max-width: 200px;
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.3s ease;
        z-index: 998;
    }
    
    .keyboard-hints.show {
        opacity: 1;
        transform: translateY(0);
    }
    
    .shortcut-item {
        display: flex;
        justify-content: space-between;
        margin: 5px 0;
    }
    
    .shortcut-key {
        background: #333;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: monospace;
    }
    
    /* Mobile-friendly navigation */
    @media (max-width: 768px) {
        .nav-breadcrumbs {
            overflow-x: auto;
            scrollbar-width: none;
            -ms-overflow-style: none;
        }
        
        .nav-breadcrumbs::-webkit-scrollbar {
            display: none;
        }
        
        .quick-actions {
            bottom: 80px;
        }
    }
    
    /* Animations */
    @keyframes swipe-hint-left {
        0%, 100% { opacity: 0; transform: translateY(-50%) translateX(0); }
        50% { opacity: 1; transform: translateY(-50%) translateX(-10px); }
    }
    
    @keyframes swipe-hint-right {
        0%, 100% { opacity: 0; transform: translateY(-50%) translateX(0); }
        50% { opacity: 1; transform: translateY(-50%) translateX(10px); }
    }
    
    /* Page transition effects */
    .page-transition {
        animation: page-slide-in 0.3s ease-out;
    }
    
    @keyframes page-slide-in {
        from { transform: translateX(20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    </style>
    
    <script>
    // Gesture navigation JavaScript
    function initGestureNavigation() {
        let startX = 0;
        let startY = 0;
        let isScrolling = false;
        
        document.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
            isScrolling = undefined;
        }, {passive: true});
        
        document.addEventListener('touchmove', function(e) {
            if (e.touches.length > 1) return;
            
            let currentX = e.touches[0].clientX;
            let currentY = e.touches[0].clientY;
            
            if (isScrolling === undefined) {
                isScrolling = Math.abs(currentY - startY) > Math.abs(currentX - startX);
            }
            
            if (!isScrolling) {
                e.preventDefault();
                
                let diffX = currentX - startX;
                
                if (Math.abs(diffX) > 30) {
                    if (diffX > 0) {
                        showSwipeIndicator('right');
                    } else {
                        showSwipeIndicator('left');
                    }
                }
            }
        }, {passive: false});
        
        document.addEventListener('touchend', function(e) {
            if (isScrolling) return;
            
            let endX = e.changedTouches[0].clientX;
            let diffX = endX - startX;
            
            if (Math.abs(diffX) > 100) {
                if (diffX > 0) {
                    navigateDirection('previous');
                } else {
                    navigateDirection('next');
                }
            }
            
            hideSwipeIndicators();
        }, {passive: true});
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.altKey) {
                switch(e.key) {
                    case 'ArrowLeft':
                        e.preventDefault();
                        navigateDirection('previous');
                        break;
                    case 'ArrowRight':
                        e.preventDefault();
                        navigateDirection('next');
                        break;
                    case 'h':
                        e.preventDefault();
                        navigateToPage('Dashboard');
                        break;
                    case 's':
                        e.preventDefault();
                        navigateToPage('Safety');
                        break;
                    case 'c':
                        e.preventDefault();
                        navigateToPage('Cost Management');
                        break;
                }
            }
            
            if (e.key === '?') {
                toggleKeyboardHints();
            }
        });
    }
    
    function showSwipeIndicator(direction) {
        const indicator = document.createElement('div');
        indicator.className = `swipe-indicator swipe-${direction}`;
        indicator.innerHTML = direction === 'left' ? '→' : '←';
        document.body.appendChild(indicator);
        
        setTimeout(() => {
            indicator.style.opacity = '1';
        }, 10);
    }
    
    function hideSwipeIndicators() {
        const indicators = document.querySelectorAll('.swipe-indicator');
        indicators.forEach(indicator => {
            indicator.style.opacity = '0';
            setTimeout(() => {
                if (indicator.parentNode) {
                    indicator.parentNode.removeChild(indicator);
                }
            }, 300);
        });
    }
    
    function navigateDirection(direction) {
        // This would integrate with Streamlit's navigation system
        console.log(`Navigate ${direction}`);
        
        // Trigger page transition effect
        const mainContent = document.querySelector('.main');
        if (mainContent) {
            mainContent.classList.add('page-transition');
            setTimeout(() => {
                mainContent.classList.remove('page-transition');
            }, 300);
        }
    }
    
    function navigateToPage(page) {
        console.log(`Navigate to ${page}`);
        // This would integrate with Streamlit's session state
    }
    
    function toggleKeyboardHints() {
        let hints = document.querySelector('.keyboard-hints');
        if (!hints) {
            createKeyboardHints();
            hints = document.querySelector('.keyboard-hints');
        }
        
        hints.classList.toggle('show');
        
        setTimeout(() => {
            if (hints.classList.contains('show')) {
                hints.classList.remove('show');
            }
        }, 5000);
    }
    
    function createKeyboardHints() {
        const hints = document.createElement('div');
        hints.className = 'keyboard-hints';
        hints.innerHTML = `
            <div style="font-weight: bold; margin-bottom: 10px;">Keyboard Shortcuts</div>
            <div class="shortcut-item">
                <span>Previous/Next</span>
                <span class="shortcut-key">Alt + ←/→</span>
            </div>
            <div class="shortcut-item">
                <span>Dashboard</span>
                <span class="shortcut-key">Alt + H</span>
            </div>
            <div class="shortcut-item">
                <span>Safety</span>
                <span class="shortcut-key">Alt + S</span>
            </div>
            <div class="shortcut-item">
                <span>Cost Mgmt</span>
                <span class="shortcut-key">Alt + C</span>
            </div>
            <div class="shortcut-item">
                <span>Show Shortcuts</span>
                <span class="shortcut-key">?</span>
            </div>
        `;
        document.body.appendChild(hints);
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initGestureNavigation);
    } else {
        initGestureNavigation();
    }
    </script>
    """, unsafe_allow_html=True)

def render_navigation_breadcrumbs(pages: List[str], current_page: str, 
                                 on_navigate: Optional[Callable] = None) -> None:
    """Render interactive navigation breadcrumbs."""
    
    current_index = pages.index(current_page) if current_page in pages else 0
    
    breadcrumb_html = '<div class="nav-breadcrumbs">'
    
    for i, page in enumerate(pages):
        is_active = (i == current_index)
        is_clickable = (i <= current_index)
        
        if i > 0:
            breadcrumb_html += '<span class="breadcrumb-separator">›</span>'
        
        css_class = "breadcrumb-item"
        if is_active:
            css_class += " active"
        
        icon = get_page_icon(page)
        
        breadcrumb_html += f'''
        <div class="{css_class}" onclick="{'navigateToPage(\\''+page+'\\')' if is_clickable else ''}">
            <span>{icon}</span>
            <span>{page}</span>
        </div>
        '''
    
    breadcrumb_html += '</div>'
    
    st.markdown(breadcrumb_html, unsafe_allow_html=True)

def render_quick_actions(actions: List[Dict[str, str]]) -> None:
    """Render floating quick action buttons."""
    
    actions_html = '<div class="quick-actions">'
    
    for i, action in enumerate(actions):
        css_class = "quick-action-btn"
        if i == 0:  # Primary action
            css_class += " primary"
        
        actions_html += f'''
        <button class="{css_class}" 
                onclick="quickAction('{action['key']}')" 
                title="{action['label']}">
            {action['icon']}
        </button>
        '''
    
    actions_html += '</div>'
    
    st.markdown(actions_html, unsafe_allow_html=True)

def get_page_icon(page: str) -> str:
    """Get icon for page based on name."""
    
    icons = {
        "Dashboard": "📊",
        "Pre-Construction": "📋",
        "Engineering": "⚙️",
        "Field Operations": "🏗️",
        "Safety": "🦺",
        "Contracts": "📄",
        "Cost Management": "💰",
        "BIM": "🏢",
        "Document Management": "📁",
        "Closeout": "✅",
        "Resource Management": "👥",
        "Admin": "⚙️",
        "Collaboration": "💬"
    }
    
    return icons.get(page, "📄")

def enable_touch_gestures(navigation_callback: Optional[Callable] = None) -> None:
    """Enable touch gesture recognition for navigation."""
    
    if 'gesture_enabled' not in st.session_state:
        st.session_state.gesture_enabled = True
        
        # Add gesture detection JavaScript
        st.markdown("""
        <script>
        window.gestureCallback = function(direction) {
            // This would communicate back to Streamlit
            console.log('Gesture detected:', direction);
        };
        </script>
        """, unsafe_allow_html=True)

def render_navigation_helper() -> None:
    """Render navigation helper tooltip."""
    
    st.markdown("""
    <div class="nav-helper" style="
        position: fixed; 
        top: 20px; 
        right: 20px; 
        background: rgba(0,0,0,0.8); 
        color: white; 
        padding: 10px; 
        border-radius: 6px; 
        font-size: 12px;
        z-index: 1000;
        opacity: 0.7;
    ">
        💡 Swipe left/right to navigate<br>
        Press ? for shortcuts
    </div>
    """, unsafe_allow_html=True)

def create_gesture_navigation_for_module(module_name: str, pages: List[str]) -> None:
    """Create complete gesture navigation setup for a module."""
    
    # Apply styles
    apply_gesture_navigation_styles()
    
    # Current page from session state
    current_page = st.session_state.get('current_menu', pages[0])
    
    # Render breadcrumbs
    render_navigation_breadcrumbs(pages, current_page)
    
    # Quick actions based on module
    quick_actions = get_module_quick_actions(module_name)
    if quick_actions:
        render_quick_actions(quick_actions)
    
    # Enable gestures
    enable_touch_gestures()
    
    # Show helper on first visit
    if f'nav_helper_shown_{module_name}' not in st.session_state:
        render_navigation_helper()
        st.session_state[f'nav_helper_shown_{module_name}'] = True

def get_module_quick_actions(module_name: str) -> List[Dict[str, str]]:
    """Get quick actions for specific modules."""
    
    actions_map = {
        "Safety": [
            {"key": "new_incident", "icon": "🚨", "label": "Report Incident"},
            {"key": "safety_meeting", "icon": "👥", "label": "Safety Meeting"},
            {"key": "inspection", "icon": "🔍", "label": "Inspection"}
        ],
        "Field Operations": [
            {"key": "daily_report", "icon": "📝", "label": "Daily Report"},
            {"key": "timesheet", "icon": "⏰", "label": "Timesheet"},
            {"key": "photo", "icon": "📷", "label": "Take Photo"}
        ],
        "Cost Management": [
            {"key": "new_change_order", "icon": "💰", "label": "Change Order"},
            {"key": "invoice", "icon": "🧾", "label": "New Invoice"},
            {"key": "budget_check", "icon": "📊", "label": "Budget Check"}
        ]
    }
    
    return actions_map.get(module_name, [])