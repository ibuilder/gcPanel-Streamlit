"""
Mobile-responsive layout utilities for gcPanel.

This module provides utilities for creating responsive layouts for different screen sizes.
"""

import streamlit as st

def add_mobile_styles():
    """Add mobile-specific CSS styles to the application."""
    # Add custom CSS for mobile optimization
    st.markdown("""
    <style>
    /* General Mobile Optimizations */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        h2 {
            font-size: 1.3rem !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
        }
        
        p, li, .stTextInput > div[data-baseweb="input"] > div, 
        .stTextArea textarea, .stButton button, .stSelectbox div {
            font-size: 0.9rem !important;
        }
        
        /* Increase touch targets */
        .stButton button {
            min-height: 44px;
            margin-bottom: 0.5rem;
        }
        
        .stSelectbox div[role="listbox"] span {
            min-height: 44px;
            display: flex;
            align-items: center;
        }
        
        /* Reduce table font size */
        .dataframe {
            font-size: 0.7rem !important;
        }
        
        /* Optimize chart size */
        .stPlotlyChart {
            height: 250px !important;
        }
    }
    
    /* Offline indicator styling */
    .offline-indicator {
        background-color: #fff3cd;
        color: #856404;
        padding: 8px 16px;
        border-radius: 4px;
        margin-bottom: 16px;
        display: none; /* Hidden by default, shown via JavaScript when offline */
    }
    
    /* Responsive card styling */
    .responsive-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
    }
    
    .responsive-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .responsive-card-title {
        font-weight: bold;
        margin-bottom: 8px;
        font-size: 1.1rem;
    }
    
    .responsive-card-content {
        color: #555;
    }
    
    /* Add offline detection JavaScript */
    </style>
    <script>
    // Check for online/offline status
    function updateOfflineStatus() {
        var offlineIndicator = document.querySelector('.offline-indicator');
        if (offlineIndicator) {
            if (navigator.onLine) {
                offlineIndicator.style.display = 'none';
            } else {
                offlineIndicator.style.display = 'block';
            }
        }
    }
    
    // Initial check
    document.addEventListener('DOMContentLoaded', function() {
        updateOfflineStatus();
    });
    
    // Listen for online/offline events
    window.addEventListener('online', updateOfflineStatus);
    window.addEventListener('offline', updateOfflineStatus);
    </script>
    """, unsafe_allow_html=True)

def create_responsive_card(title, content, on_click=None):
    """
    Create a responsive card component.
    
    Args:
        title (str): Title of the card
        content (str): Content text of the card
        on_click (function, optional): Function to execute when card is clicked
        
    Returns:
        bool: True if card was clicked, False otherwise
    """
    # Create card HTML
    card_html = f"""
    <div class="responsive-card" id="card_{hash(title)}">
        <div class="responsive-card-title">{title}</div>
        <div class="responsive-card-content">{content}</div>
    </div>
    """
    
    # Add click handler if provided
    if on_click:
        card_html += f"""
        <script>
        document.getElementById("card_{hash(title)}").addEventListener("click", function() {{
            // Set a value in localStorage that will be detected
            localStorage.setItem("cardClicked_{hash(title)}", "true");
            window.location.reload();
        }});
        
        // Check if this card was clicked
        document.addEventListener("DOMContentLoaded", function() {{
            if (localStorage.getItem("cardClicked_{hash(title)}")) {{
                // Clear the flag
                localStorage.removeItem("cardClicked_{hash(title)}");
                // Execute callback
                window.streamlitIsReady.then(() => {{
                    Streamlit.setComponentValue(true);
                }});
            }}
        }});
        </script>
        """
    
    # Render the card
    clicked = st.markdown(card_html, unsafe_allow_html=True)
    
    return clicked