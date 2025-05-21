"""
PWA Support Utils for gcPanel

This module provides utilities for enabling Progressive Web App (PWA)
features for gcPanel in production environments.
"""

import streamlit as st
import os

def setup_pwa():
    """
    Set up Progressive Web App (PWA) support.
    
    This function adds the required meta tags and manifest.json link to enable
    PWA features in supported browsers.
    """
    # Add PWA meta tags and manifest link
    st.markdown("""
    <head>
        <!-- PWA Meta Tags -->
        <meta name="application-name" content="gcPanel Construction Management">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="default">
        <meta name="apple-mobile-web-app-title" content="gcPanel">
        <meta name="description" content="Comprehensive construction management platform for project management and field operations.">
        <meta name="theme-color" content="#2E86C1">
        
        <!-- PWA Icons -->
        <link rel="apple-touch-icon" href="/static/icon-192x192.png">
        <link rel="manifest" href="/static/manifest.json">
        
        <!-- Register service worker for offline support -->
        <script>
            if ('serviceWorker' in navigator) {
                window.addEventListener('load', function() {
                    navigator.serviceWorker.register('/static/service-worker.js')
                        .then(function(registration) {
                            console.log('Service Worker registered with scope:', registration.scope);
                        })
                        .catch(function(error) {
                            console.log('Service Worker registration failed:', error);
                        });
                });
            }
        </script>
    </head>
    """, unsafe_allow_html=True)