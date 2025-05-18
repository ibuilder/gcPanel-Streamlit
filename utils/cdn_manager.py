"""
CDN and asset management utilities for gcPanel.

This module provides functions for managing static assets,
implementing versioning for cache invalidation, and integrating
with Content Delivery Networks.
"""

import os
import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path

import streamlit as st

# Setup logging
logger = logging.getLogger(__name__)

# Constants
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
DIST_DIR = os.path.join(STATIC_DIR, "dist")
MANIFEST_FILE = os.path.join(DIST_DIR, "asset-manifest.json")

# CDN configuration (can be overridden with environment variables)
CDN_ENABLED = os.environ.get("CDN_ENABLED", "false").lower() == "true"
CDN_URL = os.environ.get("CDN_URL", "")  # e.g., "https://cdn.example.com/gcpanel"
CDN_ENV = os.environ.get("CDN_ENV", "production")

def ensure_dirs_exist():
    """Ensure all required static asset directories exist."""
    os.makedirs(os.path.join(DIST_DIR, "css"), exist_ok=True)
    os.makedirs(os.path.join(DIST_DIR, "js"), exist_ok=True)
    os.makedirs(os.path.join(DIST_DIR, "img"), exist_ok=True)

def hash_file(filepath):
    """
    Generate a hash for a file for versioning.
    
    Args:
        filepath: Path to the file
        
    Returns:
        str: File hash (first 8 characters)
    """
    if not os.path.exists(filepath):
        return None
        
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    
    return hasher.hexdigest()[:8]

def build_asset_manifest():
    """
    Build an asset manifest with file hashes for versioning.
    
    The manifest is a JSON file that maps original filenames to
    versioned filenames with hashes.
    
    Returns:
        dict: Asset manifest
    """
    ensure_dirs_exist()
    
    manifest = {
        "version": datetime.utcnow().strftime("%Y%m%d%H%M%S"),
        "assets": {}
    }
    
    # Process all static asset directories
    for subdir in ["css", "js", "img"]:
        dir_path = os.path.join(DIST_DIR, subdir)
        if not os.path.exists(dir_path):
            continue
            
        for filename in os.listdir(dir_path):
            if filename.startswith(".") or filename.endswith(".map"):
                continue
                
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path):
                file_hash = hash_file(file_path)
                
                if file_hash:
                    # Generate versioned filename
                    name, ext = os.path.splitext(filename)
                    versioned_name = f"{name}.{file_hash}{ext}"
                    versioned_path = os.path.join(dir_path, versioned_name)
                    
                    # Copy/rename if needed
                    if not os.path.exists(versioned_path):
                        import shutil
                        shutil.copy2(file_path, versioned_path)
                    
                    # Add to manifest
                    asset_path = f"{subdir}/{filename}"
                    versioned_path = f"{subdir}/{versioned_name}"
                    manifest["assets"][asset_path] = versioned_path
    
    # Write manifest to file
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    logger.info(f"Built asset manifest with {len(manifest['assets'])} assets")
    return manifest

def get_asset_url(path):
    """
    Get the URL for an asset, including versioning and CDN if enabled.
    
    Args:
        path: Asset path relative to static directory (e.g. 'css/style.css')
        
    Returns:
        str: Complete URL for the asset
    """
    # Ensure path is correctly formatted
    if path.startswith('/'):
        path = path[1:]
    
    manifest = {}
    
    # Load manifest if exists
    if os.path.exists(MANIFEST_FILE):
        try:
            with open(MANIFEST_FILE, 'r') as f:
                manifest = json.load(f)
        except Exception as e:
            logger.error(f"Error loading asset manifest: {str(e)}")
    
    # Check if we have a versioned path in the manifest
    versioned_path = manifest.get("assets", {}).get(path, path)
    
    # Determine base URL
    if CDN_ENABLED and CDN_URL:
        base_url = f"{CDN_URL.rstrip('/')}/{CDN_ENV}"
    else:
        base_url = "/static/dist"
    
    # Return complete URL
    return f"{base_url}/{versioned_path}"

def apply_cdn_resources():
    """Apply CDN resources to Streamlit page."""
    # Inject a small script to load resources from CDN
    if CDN_ENABLED and CDN_URL:
        js = f"""
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                // Override streamlit resource loading to use CDN
                const cdnBase = "{CDN_URL.rstrip('/')}/{CDN_ENV}";
                
                // Function to replace resource URLs
                function replaceSrcWithCDN() {{
                    const resources = document.querySelectorAll('link[rel="stylesheet"], script[src]');
                    resources.forEach(el => {{
                        let src = el.getAttribute(el.tagName === 'LINK' ? 'href' : 'src');
                        if (src && src.startsWith('/static/')) {{
                            const cdnPath = src.replace('/static/', '/');
                            el.setAttribute(el.tagName === 'LINK' ? 'href' : 'src', cdnBase + cdnPath);
                        }}
                    }});
                }}
                
                // Initial replacement
                replaceSrcWithCDN();
                
                // Set up observer for dynamically added elements
                const observer = new MutationObserver(function(mutations) {{
                    mutations.forEach(function(mutation) {{
                        if (mutation.addedNodes.length) {{
                            replaceSrcWithCDN();
                        }}
                    }});
                }});
                
                observer.observe(document.documentElement, {{
                    childList: true,
                    subtree: true
                }});
            }});
        </script>
        """
        
        st.markdown(js, unsafe_allow_html=True)

def include_versioned_css(css_file):
    """
    Include a CSS file with versioning.
    
    Args:
        css_file: CSS filename (e.g., 'main.css')
    """
    css_path = f"css/{css_file}"
    css_url = get_asset_url(css_path)
    
    # Include as a stylesheet link
    st.markdown(f'<link rel="stylesheet" href="{css_url}">', unsafe_allow_html=True)

def include_versioned_js(js_file):
    """
    Include a JavaScript file with versioning.
    
    Args:
        js_file: JS filename (e.g., 'main.js')
    """
    js_path = f"js/{js_file}"
    js_url = get_asset_url(js_path)
    
    # Include as a script tag
    st.markdown(f'<script src="{js_url}"></script>', unsafe_allow_html=True)

def get_versioned_image_url(img_file):
    """
    Get a versioned URL for an image file.
    
    Args:
        img_file: Image filename (e.g., 'logo.png')
        
    Returns:
        str: Versioned image URL
    """
    img_path = f"img/{img_file}"
    return get_asset_url(img_path)

def initialize_cdn():
    """Initialize CDN and asset versioning system."""
    # Ensure directories exist
    ensure_dirs_exist()
    
    # Build asset manifest if needed
    if not os.path.exists(MANIFEST_FILE) or os.environ.get("REBUILD_ASSETS", "false").lower() == "true":
        build_asset_manifest()
    
    # Apply CDN resources if enabled
    if CDN_ENABLED:
        apply_cdn_resources()
        logger.info(f"CDN initialized with base URL: {CDN_URL}")
    else:
        logger.info("CDN is disabled, using local static files")