"""
Micro-Interactions for Form Validation

This module provides enhanced form validation with real-time feedback,
visual indicators, and smooth micro-interactions for better user experience.
"""
import streamlit as st
import re
from datetime import datetime, date
from typing import Optional, Dict, Any, List, Tuple

def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email format with detailed feedback."""
    if not email:
        return False, ""
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email):
        return True, "✅ Valid email"
    else:
        return False, "❌ Invalid email format"

def validate_phone(phone: str) -> Tuple[bool, str]:
    """Validate phone number format."""
    if not phone:
        return False, ""
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    if len(digits_only) == 10:
        return True, "✅ Valid phone number"
    elif len(digits_only) == 11 and digits_only.startswith('1'):
        return True, "✅ Valid phone number"
    else:
        return False, "❌ Invalid phone format (use 10 digits)"

def validate_currency(amount: str) -> Tuple[bool, str, float]:
    """Validate currency amount."""
    if not amount:
        return False, "", 0.0
    
    try:
        # Remove currency symbols and commas
        clean_amount = re.sub(r'[$,]', '', amount)
        value = float(clean_amount)
        
        if value < 0:
            return False, "❌ Amount cannot be negative", 0.0
        elif value > 10000000:  # 10 million limit
            return False, "⚠️ Amount seems unusually high", value
        else:
            return True, f"✅ ${value:,.2f}", value
    except ValueError:
        return False, "❌ Invalid amount format", 0.0

def validate_date_range(start_date: date, end_date: date) -> Tuple[bool, str]:
    """Validate date range."""
    if not start_date or not end_date:
        return False, ""
    
    if start_date > end_date:
        return False, "❌ Start date must be before end date"
    elif (end_date - start_date).days > 3650:  # 10 years
        return False, "⚠️ Date range exceeds 10 years"
    else:
        days_diff = (end_date - start_date).days
        return True, f"✅ {days_diff} days duration"

def validate_required_field(value: Any, field_name: str) -> Tuple[bool, str]:
    """Validate required field."""
    if value is None or (isinstance(value, str) and not value.strip()):
        return False, f"❌ {field_name} is required"
    else:
        return True, f"✅ {field_name} provided"

def validate_text_length(text: str, min_length: int = 0, max_length: int = 1000) -> Tuple[bool, str]:
    """Validate text length with character counter."""
    if not text:
        length = 0
    else:
        length = len(text.strip())
    
    if length < min_length:
        return False, f"❌ Minimum {min_length} characters required ({length}/{min_length})"
    elif length > max_length:
        return False, f"❌ Maximum {max_length} characters allowed ({length}/{max_length})"
    else:
        if max_length > 100:
            return True, f"✅ {length}/{max_length} characters"
        else:
            return True, f"✅ {length} characters"

def enhanced_text_input(label: str, value: str = "", placeholder: str = "", 
                       required: bool = False, email_validation: bool = False,
                       phone_validation: bool = False, min_length: int = 0, 
                       max_length: int = 1000, key: str = None) -> str:
    """Enhanced text input with real-time validation."""
    
    # Create the input
    input_value = st.text_input(label, value=value, placeholder=placeholder, key=key)
    
    # Real-time validation feedback
    if input_value or required:
        validation_messages = []
        
        # Required field validation
        if required:
            is_valid, message = validate_required_field(input_value, label)
            if message:
                validation_messages.append((is_valid, message))
        
        # Length validation
        if input_value:
            is_valid, message = validate_text_length(input_value, min_length, max_length)
            if message:
                validation_messages.append((is_valid, message))
        
        # Email validation
        if email_validation and input_value:
            is_valid, message = validate_email(input_value)
            if message:
                validation_messages.append((is_valid, message))
        
        # Phone validation
        if phone_validation and input_value:
            is_valid, message = validate_phone(input_value)
            if message:
                validation_messages.append((is_valid, message))
        
        # Display validation messages
        for is_valid, message in validation_messages:
            if is_valid:
                st.success(message)
            else:
                st.error(message)
    
    return input_value

def enhanced_number_input(label: str, value: float = 0.0, min_value: float = None,
                         max_value: float = None, step: float = 1.0,
                         currency: bool = False, required: bool = False,
                         key: str = None) -> float:
    """Enhanced number input with validation."""
    
    if currency:
        # For currency, use text input with validation
        display_value = f"${value:,.2f}" if value > 0 else ""
        text_value = st.text_input(label, value=display_value, 
                                  placeholder="$0.00", key=key)
        
        if text_value:
            is_valid, message, parsed_value = validate_currency(text_value)
            if message:
                if is_valid:
                    st.success(message)
                else:
                    st.error(message)
            return parsed_value
        else:
            if required:
                st.error("❌ Amount is required")
            return 0.0
    else:
        # Regular number input
        input_value = st.number_input(label, value=value, min_value=min_value,
                                     max_value=max_value, step=step, key=key)
        
        # Validation feedback
        if required and input_value == 0:
            st.error(f"❌ {label} is required")
        elif min_value is not None and input_value < min_value:
            st.error(f"❌ Minimum value is {min_value}")
        elif max_value is not None and input_value > max_value:
            st.error(f"❌ Maximum value is {max_value}")
        else:
            if input_value > 0:
                st.success(f"✅ {input_value}")
        
        return input_value

def enhanced_date_input(label: str, value: date = None, min_value: date = None,
                       max_value: date = None, required: bool = False,
                       key: str = None) -> date:
    """Enhanced date input with validation."""
    
    default_value = value if value else date.today()
    input_value = st.date_input(label, value=default_value, min_value=min_value,
                               max_value=max_value, key=key)
    
    # Validation feedback
    if required and not input_value:
        st.error(f"❌ {label} is required")
    elif min_value and input_value < min_value:
        st.error(f"❌ Date must be after {min_value}")
    elif max_value and input_value > max_value:
        st.error(f"❌ Date must be before {max_value}")
    else:
        if input_value:
            st.success(f"✅ {input_value.strftime('%B %d, %Y')}")
    
    return input_value

def enhanced_selectbox(label: str, options: List[str], index: int = 0,
                      required: bool = False, key: str = None) -> str:
    """Enhanced selectbox with validation."""
    
    # Add placeholder option if required
    display_options = options.copy()
    if required and not display_options[0].startswith("Select"):
        display_options.insert(0, f"Select {label.lower()}...")
        index = index + 1 if index >= 0 else 0
    
    selected = st.selectbox(label, display_options, index=index, key=key)
    
    # Validation feedback
    if required and (selected.startswith("Select") or not selected):
        st.error(f"❌ Please select {label.lower()}")
        return ""
    else:
        if selected and not selected.startswith("Select"):
            st.success(f"✅ {selected}")
        return selected

def enhanced_text_area(label: str, value: str = "", height: int = 100,
                      max_length: int = 2000, required: bool = False,
                      key: str = None) -> str:
    """Enhanced text area with character counter."""
    
    input_value = st.text_area(label, value=value, height=height, key=key)
    
    # Character counter and validation
    char_count = len(input_value) if input_value else 0
    
    if required and not input_value.strip():
        st.error(f"❌ {label} is required")
    elif char_count > max_length:
        st.error(f"❌ Maximum {max_length} characters allowed ({char_count}/{max_length})")
    else:
        if char_count > 0:
            # Color code based on usage
            if char_count < max_length * 0.5:
                st.success(f"✅ {char_count}/{max_length} characters")
            elif char_count < max_length * 0.8:
                st.info(f"ℹ️ {char_count}/{max_length} characters")
            else:
                st.warning(f"⚠️ {char_count}/{max_length} characters")
    
    return input_value

def form_validation_summary(validation_results: Dict[str, bool], 
                           field_labels: Dict[str, str] = None) -> bool:
    """Display a summary of form validation results."""
    
    if not validation_results:
        return True
    
    valid_fields = [k for k, v in validation_results.items() if v]
    invalid_fields = [k for k, v in validation_results.items() if not v]
    
    if not invalid_fields:
        st.success(f"✅ All {len(valid_fields)} fields are valid")
        return True
    else:
        with st.expander("❌ Form Validation Issues", expanded=True):
            st.error(f"Please fix {len(invalid_fields)} field(s):")
            for field in invalid_fields:
                display_name = field_labels.get(field, field) if field_labels else field
                st.write(f"• {display_name}")
        return False

def apply_form_validation_styles():
    """Apply CSS styles for enhanced form validation micro-interactions."""
    
    st.markdown("""
    <style>
    /* Form validation styles */
    .validation-success {
        color: #28a745;
        font-size: 0.875rem;
        margin-top: -10px;
        margin-bottom: 10px;
        animation: fadeInSuccess 0.3s ease-in;
    }
    
    .validation-error {
        color: #dc3545;
        font-size: 0.875rem;
        margin-top: -10px;
        margin-bottom: 10px;
        animation: shakeError 0.5s ease-in-out;
    }
    
    .validation-warning {
        color: #ffc107;
        font-size: 0.875rem;
        margin-top: -10px;
        margin-bottom: 10px;
        animation: fadeInWarning 0.3s ease-in;
    }
    
    /* Input field enhancements */
    .stTextInput > div > div > input:focus {
        border-color: #007bff;
        box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
        transition: all 0.15s ease-in-out;
    }
    
    .stTextInput > div > div > input.error {
        border-color: #dc3545;
        box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
    }
    
    .stTextInput > div > div > input.success {
        border-color: #28a745;
        box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25);
    }
    
    /* Animations */
    @keyframes fadeInSuccess {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInWarning {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes shakeError {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-2px); }
        20%, 40%, 60%, 80% { transform: translateX(2px); }
    }
    
    /* Character counter styling */
    .char-counter {
        font-size: 0.75rem;
        color: #6c757d;
        text-align: right;
        margin-top: -5px;
        margin-bottom: 10px;
    }
    
    .char-counter.warning {
        color: #ffc107;
    }
    
    .char-counter.error {
        color: #dc3545;
    }
    
    /* Form section styling */
    .form-section {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #007bff;
    }
    
    .form-section.error {
        border-left-color: #dc3545;
        background: #fdf2f2;
    }
    
    .form-section.success {
        border-left-color: #28a745;
        background: #f0f8f0;
    }
    
    /* Button hover effects */
    .stButton > button {
        transition: all 0.2s ease-in-out;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Progress indicators */
    .form-progress {
        width: 100%;
        height: 4px;
        background: #e9ecef;
        border-radius: 2px;
        overflow: hidden;
        margin-bottom: 20px;
    }
    
    .form-progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #007bff, #28a745);
        transition: width 0.3s ease-in-out;
    }
    </style>
    """, unsafe_allow_html=True)