"""
Playful Security Loading Animations

This module provides engaging security-themed loading animations
to make authentication processes more delightful and reassuring.
"""
import streamlit as st
import time
from typing import List, Optional

def security_loading_animation(steps: List[str], duration: float = 3.0) -> None:
    """Display a playful security loading animation with steps."""
    
    st.markdown("""
    <style>
    .security-loader {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin: 20px 0;
        color: white;
        animation: pulse 2s infinite;
    }
    
    .security-shield {
        font-size: 48px;
        margin-bottom: 20px;
        animation: shield-bounce 1.5s ease-in-out infinite;
    }
    
    .security-steps {
        font-size: 16px;
        margin: 10px 0;
        opacity: 0;
        animation: step-fade-in 0.5s ease-in forwards;
    }
    
    .security-progress {
        width: 200px;
        height: 6px;
        background: rgba(255,255,255,0.3);
        border-radius: 3px;
        margin: 20px 0;
        overflow: hidden;
    }
    
    .security-progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #00ff88, #00cc6a);
        border-radius: 3px;
        animation: progress-fill var(--duration) ease-out forwards;
        width: 0%;
    }
    
    .lock-animation {
        display: inline-block;
        animation: lock-unlock 2s ease-in-out infinite;
    }
    
    @keyframes shield-bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    @keyframes step-fade-in {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes progress-fill {
        from { width: 0%; }
        to { width: 100%; }
    }
    
    @keyframes lock-unlock {
        0% { transform: rotate(0deg); }
        25% { transform: rotate(-5deg); }
        75% { transform: rotate(5deg); }
        100% { transform: rotate(0deg); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255, 255, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create placeholder for dynamic content
    container = st.empty()
    
    step_duration = duration / len(steps)
    
    for i, step in enumerate(steps):
        progress_percent = ((i + 1) / len(steps)) * 100
        
        container.markdown(f"""
        <div class="security-loader">
            <div class="security-shield">🛡️</div>
            <div class="security-steps" style="animation-delay: {i * 0.2}s;">
                <span class="lock-animation">🔐</span> {step}
            </div>
            <div class="security-progress">
                <div class="security-progress-bar" style="--duration: {step_duration}s; width: {progress_percent}%;"></div>
            </div>
            <small>Securing your session... {progress_percent:.0f}%</small>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(step_duration)
    
    # Final success animation
    container.markdown("""
    <div class="security-loader" style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);">
        <div style="font-size: 48px; animation: bounce 0.6s;">✅</div>
        <div style="font-size: 18px; font-weight: bold;">Security Verified!</div>
        <small>Welcome to gcPanel</small>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(1)
    container.empty()

def quick_security_check() -> None:
    """Quick security check animation for faster interactions."""
    
    container = st.empty()
    
    container.markdown("""
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 32px; animation: spin 1s linear infinite;">🔒</div>
        <div style="margin-top: 10px; color: #666;">Verifying security...</div>
    </div>
    <style>
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    time.sleep(1.5)
    container.empty()

def authentication_success_animation() -> None:
    """Celebration animation for successful authentication."""
    
    st.markdown("""
    <div class="success-celebration">
        <div class="celebration-emoji">🎉</div>
        <div class="success-text">Login Successful!</div>
        <div class="welcome-text">Welcome to gcPanel</div>
    </div>
    
    <style>
    .success-celebration {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, #4CAF50, #45a049);
        border-radius: 15px;
        color: white;
        margin: 20px 0;
        animation: celebration-bounce 0.6s ease-out;
    }
    
    .celebration-emoji {
        font-size: 64px;
        animation: emoji-bounce 0.8s ease-out;
    }
    
    .success-text {
        font-size: 24px;
        font-weight: bold;
        margin: 15px 0 5px 0;
    }
    
    .welcome-text {
        font-size: 16px;
        opacity: 0.9;
    }
    
    @keyframes celebration-bounce {
        0% { transform: scale(0.3) rotate(-180deg); opacity: 0; }
        50% { transform: scale(1.1) rotate(-10deg); }
        100% { transform: scale(1) rotate(0deg); opacity: 1; }
    }
    
    @keyframes emoji-bounce {
        0%, 20%, 60%, 100% { transform: translateY(0); }
        40% { transform: translateY(-20px); }
        80% { transform: translateY(-10px); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    time.sleep(2)

def security_breach_animation() -> None:
    """Security alert animation for failed attempts."""
    
    st.markdown("""
    <div class="security-alert">
        <div class="alert-emoji">🚨</div>
        <div class="alert-text">Security Alert</div>
        <div class="alert-message">Invalid credentials detected</div>
    </div>
    
    <style>
    .security-alert {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, #ff4757, #ff3838);
        border-radius: 15px;
        color: white;
        margin: 20px 0;
        animation: alert-shake 0.6s ease-out;
    }
    
    .alert-emoji {
        font-size: 48px;
        animation: alert-flash 1s infinite;
    }
    
    .alert-text {
        font-size: 20px;
        font-weight: bold;
        margin: 10px 0 5px 0;
    }
    
    .alert-message {
        font-size: 14px;
        opacity: 0.9;
    }
    
    @keyframes alert-shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    @keyframes alert-flash {
        0%, 50%, 100% { opacity: 1; }
        25%, 75% { opacity: 0.5; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    time.sleep(2)

def loading_dots_animation(text: str = "Processing") -> None:
    """Simple loading dots animation."""
    
    container = st.empty()
    
    for i in range(6):
        dots = "." * ((i % 3) + 1)
        container.markdown(f"""
        <div style="text-align: center; padding: 20px; font-size: 18px; color: #666;">
            {text}{dots}
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.5)
    
    container.empty()

def role_transition_animation(from_role: str, to_role: str) -> None:
    """Animation for role transitions."""
    
    st.markdown(f"""
    <div class="role-transition">
        <div class="transition-text">Switching from</div>
        <div class="role-badge from-role">{from_role}</div>
        <div class="transition-arrow">→</div>
        <div class="role-badge to-role">{to_role}</div>
    </div>
    
    <style>
    .role-transition {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 10px;
        margin: 15px 0;
        animation: slide-in 0.5s ease-out;
    }}
    
    .role-badge {{
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        color: white;
        animation: badge-pop 0.4s ease-out;
    }}
    
    .from-role {{
        background: #6c757d;
        animation-delay: 0.1s;
    }}
    
    .to-role {{
        background: #28a745;
        animation-delay: 0.3s;
    }}
    
    .transition-arrow {{
        font-size: 24px;
        color: #007bff;
        animation: arrow-bounce 1s ease-in-out infinite;
    }}
    
    .transition-text {{
        color: #666;
        font-size: 14px;
    }}
    
    @keyframes slide-in {{
        from {{ transform: translateY(-20px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    
    @keyframes badge-pop {{
        0% {{ transform: scale(0); }}
        80% {{ transform: scale(1.1); }}
        100% {{ transform: scale(1); }}
    }}
    
    @keyframes arrow-bounce {{
        0%, 20%, 50%, 80%, 100% {{ transform: translateX(0); }}
        40% {{ transform: translateX(5px); }}
        60% {{ transform: translateX(3px); }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    time.sleep(1.5)