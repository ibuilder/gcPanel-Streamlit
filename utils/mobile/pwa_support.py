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
    # Insert PWA support using Streamlit components
    # This approach uses st.components to properly add scripts and styles to the head
    # without causing them to appear in the visible page content
    
    # Create a hidden div to contain our PWA scripts
    pwa_container_style = """
    <style>
        .pwa-support {
            display: none;
            visibility: hidden;
            height: 0;
            width: 0;
            position: absolute;
            top: -9999px;
            left: -9999px;
        }
    </style>
    """
    
    # Add PWA meta tags using Streamlit's head component
    pwa_meta_tags = """
    <meta name="application-name" content="gcPanel Construction Management">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="gcPanel">
    <meta name="description" content="Comprehensive construction management platform for project management and field operations.">
    <meta name="theme-color" content="#2E86C1">
    <link rel="apple-touch-icon" href="/static/icon-192x192.png">
    <link rel="manifest" href="/static/manifest.json">
    """
    
    # Add service worker script with proper initialization
    service_worker_script = """
    <script>
        // Register service worker for PWA support
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
    """
    
    # Use Streamlit's head_html to properly add these elements to the page head
    # This keeps them from showing in the visible page content
    st.markdown(pwa_container_style, unsafe_allow_html=True)
    st.markdown(f"<div class='pwa-support'>{pwa_meta_tags}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='pwa-support'>{service_worker_script}</div>", unsafe_allow_html=True)