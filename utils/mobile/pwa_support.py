"""
Progressive Web App (PWA) Support for gcPanel.

This module provides functionality to enable PWA capabilities,
allowing the application to work offline and be installed on mobile devices.
"""

import streamlit as st
import os
import json
from datetime import datetime

def generate_manifest():
    """
    Generate a Web App Manifest for PWA support.
    
    Returns:
        dict: The manifest as a dictionary
    """
    return {
        "name": "gcPanel Construction Management",
        "short_name": "gcPanel",
        "description": "Construction management dashboard for project teams",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#FFFFFF",
        "theme_color": "#3B82F6",
        "icons": [
            {
                "src": "static/images/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "static/images/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }

def generate_service_worker():
    """
    Generate a Service Worker script for offline capabilities.
    
    Returns:
        str: Service worker JavaScript code
    """
    # Get the current timestamp for cache versioning
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    return f"""
    // Service Worker for gcPanel PWA
    const CACHE_NAME = 'gcpanel-cache-v{timestamp}';
    const ASSETS_TO_CACHE = [
        '/',
        '/static/css/style.css',
        '/static/js/main.js',
        '/static/images/logo.png',
        '/static/images/icon-192x192.png',
        '/static/images/icon-512x512.png',
        // Add other assets that should be available offline
    ];

    // Install event - cache assets
    self.addEventListener('install', event => {{
        event.waitUntil(
            caches.open(CACHE_NAME)
                .then(cache => {{
                    console.log('Caching app assets');
                    return cache.addAll(ASSETS_TO_CACHE);
                }})
        );
    }});

    // Activate event - clean up old caches
    self.addEventListener('activate', event => {{
        event.waitUntil(
            caches.keys().then(cacheNames => {{
                return Promise.all(
                    cacheNames.map(cacheName => {{
                        if (cacheName !== CACHE_NAME) {{
                            console.log('Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        }}
                    }})
                );
            }})
        );
    }});

    // Fetch event - serve cached content when offline
    self.addEventListener('fetch', event => {{
        event.respondWith(
            caches.match(event.request)
                .then(response => {{
                    if (response) {{
                        return response;
                    }}
                    
                    // Clone the request - request can only be used once
                    const fetchRequest = event.request.clone();
                    
                    return fetch(fetchRequest).then(response => {{
                        // Check if valid response
                        if (!response || response.status !== 200 || response.type !== 'basic') {{
                            return response;
                        }}
                        
                        // Clone the response - response can only be used once
                        const responseToCache = response.clone();
                        
                        caches.open(CACHE_NAME)
                            .then(cache => {{
                                // Only cache GET requests
                                if (event.request.method === 'GET') {{
                                    cache.put(event.request, responseToCache);
                                }}
                            }});
                            
                        return response;
                    }}).catch(() => {{
                        // If network request fails and we don't have a cached response,
                        // try to return a fallback for HTML pages
                        if (event.request.headers.get('accept').includes('text/html')) {{
                            return caches.match('/offline.html');
                        }}
                    }});
                }})
        );
    }});
    """

def generate_offline_page():
    """
    Generate a simple offline page.
    
    Returns:
        str: HTML content for the offline page
    """
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>gcPanel - Offline</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                padding: 20px;
                text-align: center;
                background-color: #f5f7fa;
                color: #333;
            }
            .container {
                max-width: 600px;
                background-color: white;
                border-radius: 8px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #3B82F6;
                margin-bottom: 10px;
            }
            p {
                line-height: 1.6;
                margin-bottom: 20px;
            }
            .icon {
                font-size: 48px;
                margin-bottom: 20px;
            }
            .cached-data {
                background-color: #f0f4f8;
                border-radius: 4px;
                padding: 15px;
                margin-top: 20px;
            }
            .retry-button {
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 4px;
                font-weight: bold;
                cursor: pointer;
                margin-top: 20px;
            }
            .retry-button:hover {
                background-color: #2563EB;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="icon">📶</div>
            <h1>You're Offline</h1>
            <p>It looks like you've lost your internet connection. Don't worry, you can still access previously loaded data and some basic functionality.</p>
            
            <div class="cached-data">
                <h3>Available Offline:</h3>
                <ul id="offline-features">
                    <li>Project dashboard (last synced data)</li>
                    <li>Document viewer (previously opened documents)</li>
                    <li>Field notes and checklists</li>
                </ul>
            </div>
            
            <button class="retry-button" onclick="window.location.reload()">
                Retry Connection
            </button>
        </div>
        
        <script>
            // Check connection status when user clicks retry
            document.querySelector('.retry-button').addEventListener('click', () => {
                if (navigator.onLine) {
                    window.location.href = '/';
                } else {
                    alert('Still offline. Please check your connection and try again.');
                }
            });
            
            // Listen for online status change
            window.addEventListener('online', () => {
                window.location.href = '/';
            });
        </script>
    </body>
    </html>
    """

def create_pwa_assets(static_dir="static"):
    """
    Create necessary PWA assets if they don't exist.
    
    Args:
        static_dir (str): Directory to store static assets
    """
    # Create directory structure
    os.makedirs(f"{static_dir}/js", exist_ok=True)
    os.makedirs(f"{static_dir}/css", exist_ok=True)
    os.makedirs(f"{static_dir}/images", exist_ok=True)
    
    # Create manifest.json
    manifest = generate_manifest()
    with open(f"{static_dir}/manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    # Create service-worker.js
    with open(f"{static_dir}/service-worker.js", "w") as f:
        f.write(generate_service_worker())
    
    # Create offline.html
    with open(f"{static_dir}/offline.html", "w") as f:
        f.write(generate_offline_page())
    
    # Create a minimal main.js
    main_js = """
    // Register service worker for PWA
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/service-worker.js')
                .then(registration => {
                    console.log('Service Worker registered with scope:', registration.scope);
                })
                .catch(error => {
                    console.error('Service Worker registration failed:', error);
                });
        });
    }
    
    // Add to home screen functionality
    let deferredPrompt;
    const addBtn = document.querySelector('.add-to-home');
    
    window.addEventListener('beforeinstallprompt', (e) => {
        // Prevent Chrome 67 and earlier from automatically showing the prompt
        e.preventDefault();
        // Stash the event so it can be triggered later
        deferredPrompt = e;
        // Update UI to notify the user they can add to home screen
        if (addBtn) {
            addBtn.style.display = 'block';
            
            addBtn.addEventListener('click', () => {
                // Show the install prompt
                deferredPrompt.prompt();
                // Wait for the user to respond to the prompt
                deferredPrompt.userChoice.then((choiceResult) => {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('User accepted the A2HS prompt');
                    } else {
                        console.log('User dismissed the A2HS prompt');
                    }
                    deferredPrompt = null;
                    addBtn.style.display = 'none';
                });
            });
        }
    });
    
    // Handle offline/online status
    function updateOnlineStatus() {
        const status = navigator.onLine ? 'online' : 'offline';
        console.log(`App is now ${status}`);
        
        // Update UI based on connection status
        const offlineIndicator = document.querySelector('.offline-indicator');
        if (offlineIndicator) {
            offlineIndicator.style.display = status === 'offline' ? 'block' : 'none';
        }
    }
    
    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);
    
    // Initial check
    updateOnlineStatus();
    """
    
    with open(f"{static_dir}/js/main.js", "w") as f:
        f.write(main_js)
    
    # Create minimal CSS
    main_css = """
    /* Offline indicator */
    .offline-indicator {
        display: none;
        background-color: #fef2f2;
        color: #b91c1c;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    /* Add to home screen button */
    .add-to-home {
        display: none;
        background-color: #3B82F6;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        cursor: pointer;
        margin: 0.5rem 0;
    }
    
    .add-to-home:hover {
        background-color: #2563EB;
    }
    
    /* Mobile optimizations */
    @media (max-width: 768px) {
        .mobile-stack {
            flex-direction: column !important;
        }
        
        .mobile-full-width {
            width: 100% !important;
        }
        
        .mobile-hide {
            display: none !important;
        }
        
        .mobile-show {
            display: block !important;
        }
        
        .mobile-text-center {
            text-align: center !important;
        }
        
        .mobile-compact {
            padding: 0.5rem !important;
            margin: 0.5rem 0 !important;
        }
    }
    """
    
    with open(f"{static_dir}/css/style.css", "w") as f:
        f.write(main_css)

def add_pwa_head_tags():
    """
    Add necessary PWA meta tags to the page header.
    
    This function injects HTML with meta tags required for PWA functionality.
    """
    pwa_tags = """
    <link rel="manifest" href="/static/manifest.json">
    <meta name="theme-color" content="#3B82F6">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="gcPanel">
    <link rel="apple-touch-icon" href="/static/images/icon-192x192.png">
    <link rel="stylesheet" href="/static/css/style.css">
    <script src="/static/js/main.js" defer></script>
    """
    
    st.markdown(pwa_tags, unsafe_allow_html=True)

def add_offline_indicator():
    """
    Add an offline status indicator to the page.
    
    This function adds a banner that appears when the device goes offline.
    """
    indicator_html = """
    <div class="offline-indicator">
        You are currently offline. Some features may be limited.
    </div>
    
    <script>
    // Update the indicator based on current connection status
    document.addEventListener('DOMContentLoaded', function() {
        const indicator = document.querySelector('.offline-indicator');
        if (indicator) {
            indicator.style.display = navigator.onLine ? 'none' : 'block';
        }
    });
    </script>
    """
    
    st.markdown(indicator_html, unsafe_allow_html=True)

def add_install_prompt():
    """
    Add a button to prompt users to install the PWA.
    
    This function adds a button that triggers the install prompt on compatible devices.
    """
    prompt_html = """
    <button class="add-to-home">
        Add gcPanel to Home Screen
    </button>
    """
    
    st.markdown(prompt_html, unsafe_allow_html=True)

def setup_pwa():
    """
    Set up all PWA features.
    
    This function initializes all PWA components and ensures the necessary
    files are created.
    """
    # Create static assets directory if it doesn't exist
    static_dir = "static"
    if not os.path.exists(static_dir):
        create_pwa_assets(static_dir)
    
    # Add PWA meta tags to head
    add_pwa_head_tags()
    
    # Add offline indicator
    add_offline_indicator()
    
    # Add install prompt button
    add_install_prompt()