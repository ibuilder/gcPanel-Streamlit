"""
PWA Support Utils for gcPanel

This module provides utilities for enabling Progressive Web App (PWA)
features for gcPanel in production environments.
"""

import streamlit as st
import os
import json

def check_offline_status():
    """
    Check if the application is currently running in offline mode.
    
    Returns:
        bool: True if app is in offline mode, False otherwise
    """
    # This is a simplified approach that would need to be implemented with JS
    return False

def cache_file_for_offline(file_path):
    """
    Register a file to be cached for offline use with the service worker.
    
    Args:
        file_path (str): Path to the file to cache
    """
    # In a real implementation, this would communicate with the service worker
    pass

def get_cached_files():
    """
    Get a list of files that are currently cached for offline use.
    
    Returns:
        list: List of cached file paths
    """
    # In a real implementation, this would communicate with the service worker
    return []

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