"""
Progressive Web App support for mobile applications.

This module provides functionality to make the Streamlit app work as a
Progressive Web App (PWA) with offline capabilities.
"""

import streamlit as st

def setup_pwa():
    """
    Configure the application to function as a Progressive Web App (PWA).
    
    This adds the necessary manifest and service worker for PWA support,
    enabling offline functionality and add-to-home-screen capability.
    """
    # Add PWA meta tags and manifest link
    pwa_meta = """
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <meta name="theme-color" content="#3b82f6">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="gcPanel Field">
    <link rel="manifest" href="./static/manifest.json">
    <link rel="apple-touch-icon" href="./static/icon-192x192.png">
    """
    
    # Add service worker registration script
    service_worker = """
    <script>
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('./static/service-worker.js')
                .then(function(registration) {
                    console.log('PWA: ServiceWorker registration successful with scope: ', registration.scope);
                })
                .catch(function(error) {
                    console.log('PWA: ServiceWorker registration failed: ', error);
                });
        });
    }
    </script>
    """
    
    # Add PWA installation prompt
    pwa_install_prompt = """
    <script>
    // Store the install prompt event
    let deferredPrompt;
    
    window.addEventListener('beforeinstallprompt', (e) => {
        // Prevent Chrome 67 and earlier from automatically showing the prompt
        e.preventDefault();
        // Store the event for later use
        deferredPrompt = e;
        
        // Show your custom install prompt
        document.getElementById('installPWA').style.display = 'block';
    });
    
    function showInstallPrompt() {
        // Hide the install button
        document.getElementById('installPWA').style.display = 'none';
        
        // Show the native install prompt
        if (deferredPrompt) {
            deferredPrompt.prompt();
            
            deferredPrompt.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('User accepted the PWA installation');
                } else {
                    console.log('User dismissed the PWA installation');
                }
                deferredPrompt = null;
            });
        }
    }
    </script>
    
    <div id="installPWA" style="display: none; position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background-color: #3b82f6; color: white; padding: 10px 20px; border-radius: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); z-index: 1000; font-size: 14px; text-align: center;">
        <div style="margin-bottom: 8px;">Add to Home Screen for offline access</div>
        <button onclick="showInstallPrompt()" style="background-color: white; color: #3b82f6; border: none; padding: 5px 15px; border-radius: 16px; font-weight: 500; cursor: pointer;">Install</button>
    </div>
    """
    
    # Combine all PWA components and inject into the page
    st.markdown(pwa_meta + service_worker + pwa_install_prompt, unsafe_allow_html=True)

def check_offline_status():
    """
    Check if the application is currently running in offline mode.
    
    Returns:
        bool: True if app is in offline mode, False otherwise
    """
    # Add offline status detection script
    offline_check_script = """
    <script>
    // Function to check online status
    function updateOnlineStatus() {
        if (navigator.onLine) {
            // Online - remove offline indicator
            document.getElementById('offlineIndicator').style.display = 'none';
            // Set a session storage value
            sessionStorage.setItem('isOffline', 'false');
        } else {
            // Offline - show offline indicator
            document.getElementById('offlineIndicator').style.display = 'block';
            // Set a session storage value
            sessionStorage.setItem('isOffline', 'true');
        }
    }
    
    // Add event listeners for online/offline events
    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);
    
    // Initial check
    updateOnlineStatus();
    </script>
    
    <div id="offlineIndicator" style="display: none; position: fixed; top: 10px; right: 10px; background-color: #f9c851; color: #333; padding: 5px 10px; border-radius: 12px; font-size: 12px; z-index: 1000;">
        Offline Mode
    </div>
    """
    
    # Add the offline detection script
    st.markdown(offline_check_script, unsafe_allow_html=True)
    
    # Return placeholder - in a real app, this would check session storage
    # Since Streamlit can't directly access JavaScript variables, we'd need
    # a more complex solution for a real app
    return False

def cache_file_for_offline(file_path, file_type):
    """
    Mark a file to be cached for offline use by the service worker.
    
    Args:
        file_path (str): Path to the file to cache
        file_type (str): Type of file (document, image, etc.)
        
    Returns:
        bool: True if successful, False otherwise
    """
    # In a real application, this would update a list of files to be cached
    # by the service worker. For this demo, we'll just return success.
    
    # Simulate successful caching
    return True

def get_cached_files(file_type=None):
    """
    Get a list of files that are cached for offline use.
    
    Args:
        file_type (str, optional): Filter by file type
        
    Returns:
        list: List of cached file paths
    """
    # In a real application, this would return files from the cache storage
    # For this demo, we'll return a static list
    
    all_cached_files = {
        "document": [
            "/documents/foundation_plan.pdf",
            "/documents/concrete_specs.pdf",
            "/documents/safety_plan.pdf"
        ],
        "image": [
            "/images/site_photo_1.jpg",
            "/images/site_photo_2.jpg"
        ],
        "data": [
            "/data/project_schedule.json",
            "/data/project_contacts.json"
        ]
    }
    
    if file_type and file_type in all_cached_files:
        return all_cached_files[file_type]
    
    # Return flattened list of all cached files
    return [file for files in all_cached_files.values() for file in files]