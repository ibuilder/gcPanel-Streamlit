"""
Form helper components for Streamlit interface.

This module provides reusable form components with validation, state persistence,
and consistent styling across the application.
"""

import streamlit as st
from datetime import datetime
import re
from typing import Dict, List, Any, Callable, Optional, Union, Tuple

def validate_required(value, field_name):
    """Validate that a field is not empty"""
    if not value:
        return f"{field_name} is required"
    return None

def validate_email(value):
    """Validate email format"""
    if not value:
        return None
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, value):
        return "Please enter a valid email address"
    return None

def validate_number(value, field_name, min_val=None, max_val=None):
    """Validate that a field is a number within range"""
    if not value and value != 0:
        return None  # Empty is handled by required validator
    
    try:
        num_value = float(value)
        if min_val is not None and num_value < min_val:
            return f"{field_name} must be at least {min_val}"
        if max_val is not None and num_value > max_val:
            return f"{field_name} must be at most {max_val}"
    except (ValueError, TypeError):
        return f"{field_name} must be a number"
    
    return None

def form_input_field(
    label: str,
    key: str,
    field_type: str = "text",
    required: bool = False,
    default: Any = None,
    options: List[Any] = [],
    help_text: str = "",
    validators: List[Callable] = [],
    placeholder: str = "",
    min_value: Any = None,
    max_value: Any = None,
    **kwargs
) -> Tuple[Any, str]:
    """
    Render a form input field with validation and error handling
    
    Args:
        label: Field label
        key: Unique key for the field
        field_type: Type of field (text, number, date, select, multiselect, checkbox, textarea)
        required: Whether the field is required
        default: Default value for the field
        options: Options for select/multiselect fields
        help_text: Help text to display
        validators: List of validation functions
        placeholder: Placeholder text
        min_value: Minimum value for number/date fields
        max_value: Maximum value for number/date fields
        **kwargs: Additional arguments for the field
        
    Returns:
        Tuple of (field_value, error_message)
    """
    # Initialize error state for this field if not present
    if "form_errors" not in st.session_state:
        st.session_state.form_errors = {}
    
    # Get error state for this field
    error = st.session_state.form_errors.get(key, "")
    
    # Prepare field style based on error state
    field_style = {}
    if error:
        field_style = {"border": "1px solid #dc3545"}
    
    # Preserve field value in session state if submitted with error
    state_key = f"form_{key}_value"
    if state_key in st.session_state:
        default = st.session_state[state_key]
    
    # Add required indicator to label
    if required:
        label = f"{label} *"

    # Render the appropriate field type
    value = None
    if field_type == "text":
        value = st.text_input(
            label, 
            value=default,
            key=key,
            placeholder=placeholder,
            help=help_text,
            **kwargs
        )
    elif field_type == "number":
        value = st.number_input(
            label,
            value=default,
            key=key,
            min_value=min_value,
            max_value=max_value,
            help=help_text,
            **kwargs
        )
    elif field_type == "date":
        value = st.date_input(
            label,
            value=default or datetime.now(),
            key=key,
            min_value=min_value,
            max_value=max_value,
            help=help_text,
            **kwargs
        )
    elif field_type == "select":
        if options:
            index = 0
            if default and default in options:
                index = options.index(default)
            value = st.selectbox(
                label,
                options=options,
                index=index,
                key=key,
                help=help_text,
                **kwargs
            )
    elif field_type == "multiselect":
        if options:
            value = st.multiselect(
                label,
                options=options,
                default=default or [],
                key=key,
                help=help_text,
                **kwargs
            )
    elif field_type == "checkbox":
        value = st.checkbox(
            label,
            value=default or False,
            key=key,
            help=help_text,
            **kwargs
        )
    elif field_type == "textarea":
        value = st.text_area(
            label,
            value=default,
            key=key,
            placeholder=placeholder,
            help=help_text,
            **kwargs
        )
    
    # Store value in session state for persistence
    st.session_state[state_key] = value
    
    # Run validation
    error_message = ""
    
    # Add required validator if field is required
    if required and not validators:
        validators = [lambda v: validate_required(v, label)]
    elif required and validators:
        validators.insert(0, lambda v: validate_required(v, label))
    
    if validators:
        for validator in validators:
            result = validator(value)
            if result:
                error_message = result
                break
    
    # Display error message
    if error:
        st.markdown(f'<div style="color: #dc3545; font-size: 0.8rem; margin-top: -0.5rem;">{error}</div>', unsafe_allow_html=True)
    
    return value, error_message

def validate_form(form_data: Dict[str, Any]) -> bool:
    """
    Validate form data and return validity status
    
    Args:
        form_data: Dictionary of form field values with error messages
        
    Returns:
        Boolean indicating if form is valid
    """
    # Clear previous errors
    st.session_state.form_errors = {}
    
    # Update with new errors
    for key, error in form_data.items():
        if error:
            st.session_state.form_errors[key] = error
    
    # Return boolean indicating if form is valid
    return len(st.session_state.form_errors) == 0

def form_action_buttons(
    primary_label: str,
    secondary_label: Optional[str] = None,
    cancel_label: Optional[str] = None,
    primary_type: str = "primary",
    alignment: str = "right",
    spacing: List[int] = []):
    """
    Render form action buttons with consistent styling
    
    Args:
        primary_label: Label for primary button
        secondary_label: Label for secondary button (optional)
        cancel_label: Label for cancel button (optional)
        primary_type: Button type for primary button (primary, secondary)
        alignment: Button alignment (left, center, right)
        spacing: List of column widths for spacing
    """
    if not spacing:
        if secondary_label and cancel_label:
            spacing = [4, 3, 3, 2]  # Space, Primary, Secondary, Cancel
        elif secondary_label or cancel_label:
            spacing = [6, 3, 3]  # Space, Primary, Secondary/Cancel
        else:
            spacing = [9, 3]  # Space, Primary
    
    cols = st.columns(spacing)
    
    # Add buttons based on alignment
    button_index = 0
    if alignment == "right":
        button_index = 1
    elif alignment == "center":
        button_index = len(spacing) // 2
    
    # Add primary button
    with cols[button_index]:
        if primary_type == "primary":
            primary = st.form_submit_button(primary_label, type="primary", use_container_width=True)
        else:
            primary = st.form_submit_button(primary_label, type="secondary", use_container_width=True)
    
    # Add secondary button if provided
    secondary = False
    if secondary_label:
        button_index += 1
        if button_index < len(cols):
            with cols[button_index]:
                secondary = st.form_submit_button(secondary_label, use_container_width=True)
    
    # Add cancel button if provided
    cancel = False
    if cancel_label:
        button_index += 1
        if button_index < len(cols):
            with cols[button_index]:
                cancel = st.form_submit_button(cancel_label, use_container_width=True)
    
    return primary, secondary, cancel

def form_card(title: str, form_id: str, content_fn: Callable, on_submit: Callable, submit_label: str = "Submit"):
    """
    Create a form card with consistent styling and behavior
    
    Args:
        title: Card title
        form_id: Unique ID for the form
        content_fn: Function to render form content
        on_submit: Function to call when form is submitted
        submit_label: Label for submit button
    """
    with st.form(form_id):
        st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
        
        # Render form content
        content_fn()
        
        # Add submit button
        submitted = st.form_submit_button(submit_label, type="primary")
        
        if submitted:
            on_submit()