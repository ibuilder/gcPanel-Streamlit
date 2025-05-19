"""
PWA Support Module for gcPanel.

This module provides Progressive Web App (PWA) support for gcPanel,
enabling offline capabilities, home screen installation, and more.
"""

import streamlit as st
import json
import os

def setup_pwa():
    """
    Set up Progressive Web App support.
    
    This function adds the necessary manifest and service worker
    to enable PWA functionality.
    """
    # Add PWA meta tags
    st.markdown("""
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="theme-color" content="#3B82F6">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="gcPanel">
        <link rel="apple-touch-icon" href="static/images/gcpanel-icon-192.png">
    </head>
    """, unsafe_allow_html=True)
    
    # Add PWA install prompt handler
    st.markdown("""
    <script>
    // PWA installation
    let deferredPrompt;
    
    window.addEventListener('beforeinstallprompt', (e) => {
        // Prevent Chrome 67 and earlier from automatically showing the prompt
        e.preventDefault();
        // Stash the event so it can be triggered later
        deferredPrompt = e;
        
        // Show the install button
        const installButton = document.createElement('div');
        installButton.id = 'pwa-install-button';
        installButton.innerHTML = `
            <div style="position: fixed; bottom: 20px; right: 20px; background-color: #3B82F6; color: white; padding: 10px 15px; border-radius: 50px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); z-index: 9999; display: flex; align-items: center; cursor: pointer;">
                <span style="margin-right: 8px;">📱</span>
                <span>Install App</span>
            </div>
        `;
        
        document.body.appendChild(installButton);
        
        installButton.addEventListener('click', (e) => {
            // Hide the install button
            installButton.style.display = 'none';
            
            // Show the prompt
            deferredPrompt.prompt();
            
            // Wait for the user to respond to the prompt
            deferredPrompt.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('User accepted the install prompt');
                } else {
                    console.log('User dismissed the install prompt');
                }
                deferredPrompt = null;
            });
        });
    });
    
    // Check if app is in standalone mode (installed)
    if (window.matchMedia('(display-mode: standalone)').matches) {
        console.log('App is running in standalone mode');
        
        // Add a class to the body for PWA-specific styling
        document.body.classList.add('pwa-mode');
    }
    
    // Handle online/offline status
    function updateOnlineStatus() {
        const statusIndicator = document.createElement('div');
        statusIndicator.id = 'online-status-indicator';
        
        if (navigator.onLine) {
            // Online - remove offline message if it exists
            const existingIndicator = document.getElementById('online-status-indicator');
            if (existingIndicator) {
                existingIndicator.remove();
            }
        } else {
            // Offline - show message
            statusIndicator.innerHTML = `
                <div style="position: fixed; top: 60px; left: 0; right: 0; background-color: #fff3cd; color: #856404; text-align: center; padding: 8px; z-index: 9999;">
                    You are offline. Some features may be limited.
                </div>
            `;
            
            // Add to body if not already present
            if (!document.getElementById('online-status-indicator')) {
                document.body.appendChild(statusIndicator);
            }
        }
    }
    
    // Check status on load
    window.addEventListener('load', updateOnlineStatus);
    
    // Listen for changes
    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);
    </script>
    """, unsafe_allow_html=True)

def create_service_worker():
    """
    Create a service worker file for offline support.
    
    In a real implementation, this would write the service worker
    file to the static directory. For this demo, we'll just display
    the code that would be used.
    """
    service_worker_code = """
    // Service Worker for gcPanel PWA
    
    const CACHE_NAME = 'gcpanel-cache-v1';
    const urlsToCache = [
        '/',
        '/static/css/main.css',
        '/static/js/main.js',
        '/static/images/logo.png',
        '/static/images/icons/icon-192x192.png',
        '/static/images/icons/icon-512x512.png'
    ];
    
    // Install event - cache assets
    self.addEventListener('install', event => {
        event.waitUntil(
            caches.open(CACHE_NAME)
                .then(cache => {
                    console.log('Opened cache');
                    return cache.addAll(urlsToCache);
                })
        );
    });
    
    // Fetch event - serve from cache if available
    self.addEventListener('fetch', event => {
        event.respondWith(
            caches.match(event.request)
                .then(response => {
                    // Cache hit - return response
                    if (response) {
                        return response;
                    }
                    
                    // Clone the request
                    const fetchRequest = event.request.clone();
                    
                    return fetch(fetchRequest)
                        .then(response => {
                            // Check if valid response
                            if (!response || response.status !== 200 || response.type !== 'basic') {
                                return response;
                            }
                            
                            // Clone the response
                            const responseToCache = response.clone();
                            
                            // Cache the response
                            caches.open(CACHE_NAME)
                                .then(cache => {
                                    cache.put(event.request, responseToCache);
                                });
                                
                            return response;
                        })
                        .catch(() => {
                            // Network failed, try to serve from cache for HTML pages
                            if (event.request.url.indexOf('.html') > -1 || 
                                event.request.url.endsWith('/')) {
                                return caches.match('/offline.html');
                            }
                        });
                })
        );
    });
    
    // Activate event - clean up old caches
    self.addEventListener('activate', event => {
        const cacheWhitelist = [CACHE_NAME];
        
        event.waitUntil(
            caches.keys().then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => {
                        if (cacheWhitelist.indexOf(cacheName) === -1) {
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
        );
    });
    """
    
    return service_worker_code

def create_manifest():
    """
    Create a web app manifest for PWA support.
    
    In a real implementation, this would write the manifest
    file to the static directory. For this demo, we'll just display
    the manifest that would be used.
    """
    manifest = {
        "name": "gcPanel Construction Management",
        "short_name": "gcPanel",
        "description": "Construction management dashboard for the Highland Tower Development",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#3B82F6",
        "icons": [
            {
                "src": "static/images/gcpanel-icon-192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "static/images/gcpanel-icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }
    
    return json.dumps(manifest, indent=2)

def show_pwa_details():
    """Display PWA implementation details for development purposes."""
    with st.expander("PWA Implementation Details"):
        st.markdown("""
        ### PWA Implementation
        
        To implement PWA capabilities, three key components are required:
        
        1. **Web App Manifest**: JSON file that provides information about the app
        2. **Service Worker**: JavaScript file that enables offline functionality
        3. **HTTPS**: PWAs require secure connections
        
        Below are the implementations for this project:
        """)
        
        # Show manifest.json
        st.markdown("#### Web App Manifest (manifest.json)")
        st.code(create_manifest(), language="json")
        
        # Show service-worker.js
        st.markdown("#### Service Worker (service-worker.js)")
        st.code(create_service_worker(), language="javascript")
        
        # Show registration code
        st.markdown("#### Service Worker Registration (in main.js)")
        registration_code = """
        // Register service worker
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/service-worker.js')
                    .then(registration => {
                        console.log('ServiceWorker registration successful');
                    })
                    .catch(error => {
                        console.log('ServiceWorker registration failed:', error);
                    });
            });
        }
        """
        st.code(registration_code, language="javascript")