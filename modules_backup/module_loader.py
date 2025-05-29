"""
Module Loader for gcPanel

This file acts as a centralized registry for all modules,
allowing modules to be independently developed and loaded.
It removes direct module dependencies from the main application.
"""

import streamlit as st
import importlib
import os
import sys
import json
from typing import Dict, Callable, List, Any

# Dictionary to store registered module handlers
_MODULE_REGISTRY = {}

# Dictionary to map module IDs to their friendly display names
_MODULE_DISPLAY_NAMES = {}

# Dictionary to store module metadata
_MODULE_METADATA = {}

# List to store module registration order for navigation purposes
_MODULE_ORDER = []

def register_module(module_id: str, display_name: str, render_function: Callable, 
                   position: int = None, category: str = "Main", 
                   requires_action_buttons: bool = False,
                   metadata: Dict[str, Any] = None):
    """
    Register a module with the application.
    
    Args:
        module_id: Unique identifier for the module
        display_name: Display name to show in navigation
        render_function: Function to call when rendering the module
        position: Optional position in the navigation menu (lower numbers appear first)
        category: Category for grouping in navigation
        requires_action_buttons: Whether this module requires action buttons
        metadata: Additional module metadata
    """
    if module_id in _MODULE_REGISTRY:
        # Module already registered, update its configuration
        _MODULE_REGISTRY[module_id] = render_function
        _MODULE_DISPLAY_NAMES[module_id] = display_name
        
        # Update metadata
        if not metadata:
            metadata = {}
        
        if module_id in _MODULE_METADATA:
            _MODULE_METADATA[module_id].update(metadata)
        else:
            _MODULE_METADATA[module_id] = metadata
            
        _MODULE_METADATA[module_id]["category"] = category
        _MODULE_METADATA[module_id]["requires_action_buttons"] = requires_action_buttons
    else:
        # New module registration
        _MODULE_REGISTRY[module_id] = render_function
        _MODULE_DISPLAY_NAMES[module_id] = display_name
        
        if not metadata:
            metadata = {}
            
        metadata["category"] = category
        metadata["requires_action_buttons"] = requires_action_buttons
        _MODULE_METADATA[module_id] = metadata
        
        # Add to ordered list
        if module_id not in _MODULE_ORDER:
            if position is not None:
                # Insert at specific position if provided
                if position < len(_MODULE_ORDER):
                    _MODULE_ORDER.insert(position, module_id)
                else:
                    _MODULE_ORDER.append(module_id)
            else:
                # Append to end if no position specified
                _MODULE_ORDER.append(module_id)

def get_module_renderer(module_id: str) -> Callable:
    """
    Get the render function for a specific module.
    
    Args:
        module_id: The module ID to get the renderer for
        
    Returns:
        The module's render function
    """
    if module_id in _MODULE_REGISTRY:
        return _MODULE_REGISTRY[module_id]
    return None

def get_all_modules() -> Dict[str, str]:
    """
    Get a dictionary of all registered modules.
    
    Returns:
        Dict mapping module IDs to display names
    """
    return _MODULE_DISPLAY_NAMES.copy()

def get_module_metadata(module_id: str) -> Dict[str, Any]:
    """
    Get metadata for a specific module.
    
    Args:
        module_id: The module ID to get metadata for
        
    Returns:
        Dictionary of module metadata
    """
    if module_id in _MODULE_METADATA:
        return _MODULE_METADATA[module_id].copy()
    return {}

def get_modules_by_category() -> Dict[str, List[Dict[str, str]]]:
    """
    Get modules organized by category.
    
    Returns:
        Dict mapping category names to lists of module info
    """
    categories = {}
    
    for module_id in _MODULE_ORDER:
        if module_id in _MODULE_METADATA:
            category = _MODULE_METADATA[module_id].get("category", "Main")
            
            if category not in categories:
                categories[category] = []
                
            categories[category].append({
                "id": module_id,
                "name": _MODULE_DISPLAY_NAMES.get(module_id, module_id)
            })
    
    return categories

def render_module(module_id: str):
    """
    Render a specific module by ID.
    
    Args:
        module_id: The module ID to render
    """
    renderer = get_module_renderer(module_id)
    if renderer:
        renderer()
    else:
        st.error(f"Module '{module_id}' not found. Please select a valid module.")

def get_modules_requiring_action_buttons() -> List[str]:
    """
    Get a list of modules that require action buttons.
    
    Returns:
        List of module IDs
    """
    modules = []
    for module_id, metadata in _MODULE_METADATA.items():
        if metadata.get("requires_action_buttons", False):
            modules.append(module_id)
    return modules

def initialize_modules():
    """
    Initialize all modules in the modules directory.
    This function dynamically loads modules from the filesystem.
    """
    try:
        # Get the modules directory
        modules_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Scan for module directories
        for item in os.listdir(modules_dir):
            item_path = os.path.join(modules_dir, item)
            
            # Skip this loader file and __pycache__ directories
            if (item == os.path.basename(__file__) or
                item == '__pycache__' or
                item.startswith('_') or
                not os.path.isdir(item_path)):
                continue
                
            # Check for module registration file
            registration_file = os.path.join(item_path, 'module_info.json')
            if os.path.exists(registration_file):
                try:
                    with open(registration_file, 'r') as f:
                        module_info = json.load(f)
                        
                    # Get module attributes from info file
                    module_id = module_info.get('id', item)
                    display_name = module_info.get('display_name', item.replace('_', ' ').title())
                    entry_point = module_info.get('entry_point', '__init__.py')
                    render_function = module_info.get('render_function', 'render')
                    position = module_info.get('position', None)
                    category = module_info.get('category', 'Main')
                    requires_action_buttons = module_info.get('requires_action_buttons', False)
                    metadata = module_info.get('metadata', {})
                    
                    # Import the module
                    module_path = f"modules.{item}"
                    if entry_point != '__init__.py':
                        # Remove .py extension if present
                        if entry_point.endswith('.py'):
                            entry_point = entry_point[:-3]
                        module_path = f"modules.{item}.{entry_point}"
                    
                    try:
                        module = importlib.import_module(module_path)
                        render_func = getattr(module, render_function)
                        
                        # Register the module
                        register_module(
                            module_id=module_id,
                            display_name=display_name,
                            render_function=render_func,
                            position=position,
                            category=category,
                            requires_action_buttons=requires_action_buttons,
                            metadata=metadata
                        )
                    except (ImportError, AttributeError) as e:
                        st.warning(f"Failed to load module {item}: {str(e)}")
                except (json.JSONDecodeError, IOError) as e:
                    st.warning(f"Failed to parse module info for {item}: {str(e)}")
            else:
                # If no registration file, try to use default behavior
                try:
                    module_path = f"modules.{item}"
                    module = importlib.import_module(module_path)
                    
                    # Check for render function
                    if hasattr(module, 'render'):
                        # Use directory name for module_id and a cleaned version for display
                        module_id = item
                        display_name = item.replace('_', ' ').title()
                        
                        # Register the module
                        register_module(
                            module_id=module_id,
                            display_name=display_name,
                            render_function=module.render,
                            category='Main'
                        )
                except ImportError:
                    # Skip modules that can't be imported
                    pass
    except Exception as e:
        st.error(f"Error initializing modules: {str(e)}")

# Initialize modules when this module is imported
initialize_modules()