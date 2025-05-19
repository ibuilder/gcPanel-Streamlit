"""
Mobile UI components for gcPanel.

This module provides reusable UI components for mobile interface elements,
separating the HTML from Python code for better maintainability.
"""

import streamlit as st

def render_mobile_header(title, subtitle=None):
    """
    Render a mobile-friendly header.
    
    Args:
        title (str): The title to display
        subtitle (str, optional): Optional subtitle
    """
    header_html = f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="font-size: 1.8rem; margin-bottom: 5px;">{title}</h1>
        {f'<p style="color: #666; margin: 0;">{subtitle}</p>' if subtitle else ''}
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def render_quick_action_button(icon, label, action_key):
    """
    Render a mobile-friendly quick action button.
    
    Args:
        icon (str): The emoji icon to display
        label (str): The button label
        action_key (str): The unique key for the button
        
    Returns:
        bool: True if the button was clicked, False otherwise
    """
    button_html = f"""
    <div style="text-align: center;">
        <div style="font-size: 1.8rem; margin-bottom: 5px;">{icon}</div>
        <div style="font-size: 0.8rem;">{label}</div>
    </div>
    """
    
    clicked = st.button(
        label, 
        key=action_key,
        help=f"{label} action",
        use_container_width=True
    )
    
    if clicked:
        return True
    
    return False

def render_card_with_icon(icon, title, content, badge=None):
    """
    Render a mobile-friendly card with an icon.
    
    Args:
        icon (str): The emoji icon to display
        title (str): The card title
        content (str): The card content
        badge (dict, optional): Optional badge with text and color
    """
    # Badge HTML if provided
    badge_html = ""
    if badge:
        text = badge.get("text", "")
        color = badge.get("color", "#4CAF50")
        background = badge.get("background", "#E8F5E9")
        badge_html = f"""
        <span style="background-color: {background}; color: {color}; 
                    padding: 2px 6px; border-radius: 10px; font-size: 0.7rem;">
            {text}
        </span>
        """
    
    card_html = f"""
    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 15px;">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <div style="font-size: 1.5rem; margin-right: 10px;">{icon}</div>
            <div style="flex-grow: 1;">
                <div style="font-weight: 500; font-size: 1.1rem;">{title}</div>
            </div>
            {badge_html}
        </div>
        <div>{content}</div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def render_list_item(title, subtitle=None, meta=None, icon=None, is_clickable=False, key=None):
    """
    Render a mobile-friendly list item.
    
    Args:
        title (str): The item title
        subtitle (str, optional): Optional item subtitle
        meta (str, optional): Optional meta information (right-aligned)
        icon (str, optional): Optional emoji icon
        is_clickable (bool): Whether the item is clickable
        key (str, optional): Optional unique key for the item
    
    Returns:
        bool: True if the item was clicked, False otherwise
    """
    # Icon HTML if provided
    icon_html = f'<div style="font-size: 1.5rem; margin-right: 10px;">{icon}</div>' if icon else ''
    
    # Subtitle HTML if provided
    subtitle_html = f'<div style="color: #666; font-size: 0.9rem;">{subtitle}</div>' if subtitle else ''
    
    # Meta HTML if provided
    meta_html = f'<div style="text-align: right; color: #999;">{meta}</div>' if meta else ''
    
    # Clickable style
    clickable_style = 'cursor: pointer; background-color: #f5f5f5;' if is_clickable else ''
    
    item_html = f"""
    <div style="border-bottom: 1px solid #eee; padding: 10px 0; {clickable_style}">
        <div style="display: flex; align-items: center;">
            {icon_html}
            <div style="flex-grow: 1;">
                <div style="font-weight: 500;">{title}</div>
                {subtitle_html}
            </div>
            {meta_html}
        </div>
    </div>
    """
    
    st.markdown(item_html, unsafe_allow_html=True)
    
    # If clickable, add a button below it
    if is_clickable and key:
        clicked = st.button("Select", key=key, help=f"Select {title}")
        return clicked
    
    return False

def render_weather_card(temperature, conditions, forecast, location):
    """
    Render a mobile-friendly weather card.
    
    Args:
        temperature (str): Current temperature
        conditions (str): Current weather conditions
        forecast (str): Weather forecast
        location (str): Location name
    """
    # Emoji based on conditions
    condition_emojis = {
        "sunny": "☀️",
        "partly cloudy": "⛅",
        "cloudy": "☁️",
        "rain": "🌧️",
        "snow": "❄️",
        "storm": "⛈️"
    }
    
    # Get appropriate emoji or default
    condition_lower = conditions.lower()
    emoji = next((v for k, v in condition_emojis.items() if k in condition_lower), "🌤️")
    
    weather_html = f"""
    <div style="background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%); color: white; 
                border-radius: 10px; padding: 20px; margin-bottom: 15px;">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="font-size: 3rem; margin-right: 20px;">{emoji}</div>
            <div>
                <div style="font-size: 2rem; font-weight: 500;">{temperature}</div>
                <div>{conditions}</div>
            </div>
        </div>
        <div style="margin-bottom: 10px;">{location}</div>
        <div style="font-size: 0.9rem;">{forecast}</div>
    </div>
    """
    
    st.markdown(weather_html, unsafe_allow_html=True)

def render_progress_circle(percentage, label=None, size=120):
    """
    Render a mobile-friendly circular progress indicator.
    
    Args:
        percentage (int): Progress percentage (0-100)
        label (str, optional): Optional label
        size (int): Size of the circle in pixels
    """
    # Ensure percentage is within bounds
    percentage = max(0, min(100, percentage))
    
    # Calculate parameters
    radius = size / 2
    stroke_width = size / 10
    stroke_radius = radius - (stroke_width / 2)
    circumference = 2 * 3.14159 * stroke_radius
    stroke_dasharray = circumference
    stroke_dashoffset = circumference * (1 - percentage / 100)
    
    # Generate label HTML if provided
    label_html = f'<div style="text-align: center; margin-top: 5px;">{label}</div>' if label else ''
    
    progress_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; margin: 10px 0;">
        <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
            <circle cx="{radius}" cy="{radius}" r="{stroke_radius}" 
                    stroke="#e0e0e0" stroke-width="{stroke_width}" fill="none" />
            <circle cx="{radius}" cy="{radius}" r="{stroke_radius}" 
                    stroke="#4CAF50" stroke-width="{stroke_width}" fill="none" 
                    stroke-dasharray="{stroke_dasharray}" stroke-dashoffset="{stroke_dashoffset}" 
                    transform="rotate(-90 {radius} {radius})" />
            <text x="{radius}" y="{radius}" text-anchor="middle" dominant-baseline="middle" 
                  font-size="{size/5}px" font-weight="bold">
                {percentage}%
            </text>
        </svg>
        {label_html}
    </div>
    """
    
    st.markdown(progress_html, unsafe_allow_html=True)

def render_mobile_alerts(alerts):
    """
    Render a list of mobile-friendly alerts.
    
    Args:
        alerts (list): List of alert dictionaries with keys:
                      - text: Alert text
                      - type: One of "info", "warning", "error", "success"
                      - icon: Optional emoji icon
    """
    if not alerts:
        return
    
    # Define alert styles based on type
    alert_styles = {
        "info": {"bg": "#E3F2FD", "color": "#0D47A1", "icon": "ℹ️"},
        "success": {"bg": "#E8F5E9", "color": "#1B5E20", "icon": "✅"},
        "warning": {"bg": "#FFF3E0", "color": "#E65100", "icon": "⚠️"},
        "error": {"bg": "#FFEBEE", "color": "#B71C1C", "icon": "❌"}
    }
    
    for alert in alerts:
        alert_type = alert.get("type", "info")
        style = alert_styles.get(alert_type, alert_styles["info"])
        
        icon = alert.get("icon", style["icon"])
        text = alert.get("text", "")
        
        alert_html = f"""
        <div style="background-color: {style['bg']}; color: {style['color']}; 
                    padding: 12px; border-radius: 8px; margin-bottom: 10px; 
                    display: flex; align-items: flex-start;">
            <div style="margin-right: 10px; font-size: 1.2rem;">{icon}</div>
            <div style="flex-grow: 1;">{text}</div>
        </div>
        """
        
        st.markdown(alert_html, unsafe_allow_html=True)

def render_mobile_tag(text, color="#4CAF50", background="#E8F5E9"):
    """
    Render a mobile-friendly tag.
    
    Args:
        text (str): The tag text
        color (str): The text color
        background (str): The background color
    """
    tag_html = f"""
    <span style="background-color: {background}; color: {color}; 
                padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; 
                display: inline-block; margin-right: 5px; margin-bottom: 5px;">
        {text}
    </span>
    """
    
    return tag_html