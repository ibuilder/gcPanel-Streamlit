"""
Animated Progress Visualization Component for gcPanel

This component provides animated progress visualizations for document processing
operations including uploads, analysis, and conversions.
"""

import streamlit as st
import time
import json
from datetime import datetime

def render_document_progress_animation(process_type="upload", current_step=0, total_steps=5, message="Processing...", details=None):
    """
    Render animated progress visualization for document processing
    
    Args:
        process_type (str): Type of process ('upload', 'analysis', 'conversion', 'validation')
        current_step (int): Current step in the process (0-based)
        total_steps (int): Total number of steps
        message (str): Current process message
        details (dict): Additional details to display
    """
    
    # Calculate progress percentage
    progress = min(current_step / max(total_steps, 1), 1.0)
    progress_percent = int(progress * 100)
    
    # Process type configurations
    process_configs = {
        "upload": {
            "icon": "📤",
            "title": "Document Upload",
            "color": "#4CAF50",
            "steps": ["Preparing", "Uploading", "Validating", "Processing", "Complete"]
        },
        "analysis": {
            "icon": "🔍",
            "title": "Document Analysis", 
            "color": "#2196F3",
            "steps": ["Reading", "Parsing", "Analyzing", "Extracting", "Complete"]
        },
        "conversion": {
            "icon": "🔄",
            "title": "Document Conversion",
            "color": "#FF9800",
            "steps": ["Loading", "Converting", "Optimizing", "Finalizing", "Complete"]
        },
        "validation": {
            "icon": "✅",
            "title": "Document Validation",
            "color": "#9C27B0",
            "steps": ["Checking", "Verifying", "Validating", "Confirming", "Complete"]
        }
    }
    
    config = process_configs.get(process_type, process_configs["upload"])
    
    # Create animated progress container
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    ">
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="
                font-size: 3em;
                margin-bottom: 10px;
                animation: pulse 2s infinite;
            ">{config['icon']}</div>
            <h3 style="
                color: #333;
                margin: 0;
                font-weight: 600;
            ">{config['title']}</h3>
            <p style="
                color: #666;
                margin: 5px 0 0 0;
                font-size: 0.9em;
            ">{message}</p>
        </div>
        
        <!-- Animated Progress Bar -->
        <div style="
            background-color: #f0f0f0;
            border-radius: 25px;
            height: 8px;
            margin: 20px 0;
            overflow: hidden;
            position: relative;
        ">
            <div style="
                background: linear-gradient(90deg, {config['color']}, {config['color']}aa);
                height: 100%;
                width: {progress_percent}%;
                border-radius: 25px;
                transition: width 0.3s ease;
                position: relative;
                overflow: hidden;
            ">
                <div style="
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
                    animation: shimmer 2s infinite;
                "></div>
            </div>
        </div>
        
        <!-- Progress Percentage -->
        <div style="text-align: center; margin: 15px 0;">
            <span style="
                font-size: 1.2em;
                font-weight: bold;
                color: {config['color']};
            ">{progress_percent}%</span>
        </div>
        
        <!-- Step Indicators -->
        <div style="
            display: flex;
            justify-content: space-between;
            margin: 20px 0;
            padding: 0 10px;
        ">
    """, unsafe_allow_html=True)
    
    # Render step indicators
    for i, step in enumerate(config['steps']):
        is_current = i == current_step
        is_completed = i < current_step
        
        if is_completed:
            step_color = config['color']
            step_icon = "✓"
            text_color = config['color']
        elif is_current:
            step_color = config['color']
            step_icon = "●"
            text_color = config['color']
        else:
            step_color = "#ddd"
            step_icon = "○"
            text_color = "#999"
        
        animation = "animation: bounce 1s infinite;" if is_current else ""
        
        st.markdown(f"""
            <div style="
                text-align: center;
                flex: 1;
                margin: 0 5px;
            ">
                <div style="
                    width: 24px;
                    height: 24px;
                    border-radius: 50%;
                    background-color: {step_color};
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto 8px auto;
                    font-size: 0.8em;
                    font-weight: bold;
                    {animation}
                ">{step_icon}</div>
                <div style="
                    font-size: 0.7em;
                    color: {text_color};
                    font-weight: {'bold' if is_current else 'normal'};
                ">{step}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display additional details if provided
    if details:
        st.markdown(f"""
        <div style="
            background-color: rgba(255,255,255,0.7);
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
        ">
            <h4 style="margin: 0 0 10px 0; color: #333; font-size: 0.9em;">Process Details:</h4>
        """, unsafe_allow_html=True)
        
        for key, value in details.items():
            st.markdown(f"""
            <div style="
                display: flex;
                justify-content: space-between;
                margin: 5px 0;
                font-size: 0.8em;
            ">
                <span style="color: #666;">{key}:</span>
                <span style="color: #333; font-weight: 500;">{value}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add CSS animations
    st.markdown("""
    <style>
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-3px); }
        60% { transform: translateY(-2px); }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translate3d(0, 20px, 0);
        }
        to {
            opacity: 1;
            transform: translate3d(0, 0, 0);
        }
    }
    </style>
    """, unsafe_allow_html=True)

def render_batch_progress_visualization(files_progress):
    """
    Render progress visualization for batch document processing
    
    Args:
        files_progress (list): List of dictionaries with file progress information
            [{"name": "file1.pdf", "progress": 0.8, "status": "processing", "message": "Analyzing..."}]
    """
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        color: white;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
    ">
        <h3 style="
            color: white;
            margin: 0 0 20px 0;
            text-align: center;
            font-weight: 600;
        ">📄 Batch Document Processing</h3>
        
        <div style="
            text-align: center;
            margin-bottom: 20px;
        ">
            <span style="font-size: 1.1em;">
                Processing {len([f for f in files_progress if f.get('status') != 'complete'])} of {len(files_progress)} files
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render individual file progress
    for i, file_info in enumerate(files_progress):
        progress = file_info.get('progress', 0)
        status = file_info.get('status', 'pending')
        message = file_info.get('message', 'Waiting...')
        file_name = file_info.get('name', f'File {i+1}')
        
        # Status colors
        status_colors = {
            'pending': '#ffc107',
            'processing': '#2196F3', 
            'complete': '#4CAF50',
            'error': '#f44336'
        }
        
        status_icons = {
            'pending': '⏳',
            'processing': '🔄',
            'complete': '✅',
            'error': '❌'
        }
        
        color = status_colors.get(status, '#2196F3')
        icon = status_icons.get(status, '📄')
        progress_percent = int(progress * 100)
        
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        ">
            <div style="
                display: flex;
                align-items: center;
                margin-bottom: 10px;
            ">
                <div style="
                    font-size: 1.2em;
                    margin-right: 10px;
                ">{icon}</div>
                <div style="flex: 1;">
                    <div style="
                        font-weight: 600;
                        color: #333;
                        margin-bottom: 2px;
                    ">{file_name}</div>
                    <div style="
                        font-size: 0.8em;
                        color: #666;
                    ">{message}</div>
                </div>
                <div style="
                    font-weight: bold;
                    color: {color};
                ">{progress_percent}%</div>
            </div>
            
            <div style="
                background-color: #f0f0f0;
                border-radius: 10px;
                height: 6px;
                overflow: hidden;
            ">
                <div style="
                    background-color: {color};
                    height: 100%;
                    width: {progress_percent}%;
                    border-radius: 10px;
                    transition: width 0.3s ease;
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_real_time_processing_stats(stats):
    """
    Render real-time processing statistics
    
    Args:
        stats (dict): Processing statistics
            {"processed": 15, "total": 20, "rate": "2.3 files/sec", "eta": "00:02:15"}
    """
    
    processed = stats.get('processed', 0)
    total = stats.get('total', 0)
    rate = stats.get('rate', '0 files/sec')
    eta = stats.get('eta', '--:--:--')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Processed",
            value=f"{processed}/{total}",
            delta=f"{processed} completed"
        )
    
    with col2:
        st.metric(
            label="⚡ Processing Rate",
            value=rate,
            delta="Real-time"
        )
    
    with col3:
        st.metric(
            label="⏱️ ETA",
            value=eta,
            delta="Estimated"
        )
    
    with col4:
        completion_rate = (processed / max(total, 1)) * 100
        st.metric(
            label="✅ Completion",
            value=f"{completion_rate:.1f}%",
            delta=f"{total - processed} remaining"
        )

def simulate_document_processing(document_name, process_type="analysis"):
    """
    Simulate document processing with animated progress
    This function demonstrates the progress visualization in action
    """
    
    placeholder = st.empty()
    
    # Define processing steps
    steps = {
        "upload": [
            ("Preparing upload...", {"File Size": "2.4 MB", "Type": "PDF"}),
            ("Uploading document...", {"Progress": "Uploading", "Speed": "1.2 MB/s"}),
            ("Validating file...", {"Status": "Checking format", "Validation": "PDF/A compliance"}),
            ("Processing metadata...", {"Extracting": "Properties", "Pages": "24"}),
            ("Upload complete!", {"Status": "Success", "Duration": "3.2 seconds"})
        ],
        "analysis": [
            ("Reading document structure...", {"Pages": "24", "Format": "PDF"}),
            ("Parsing content...", {"Text Blocks": "156", "Images": "8"}),
            ("Analyzing specifications...", {"CSI Divisions": "12", "References": "45"}),
            ("Extracting key data...", {"Tables": "6", "Schedules": "3"}),
            ("Analysis complete!", {"Confidence": "94.7%", "Items": "89"})
        ]
    }
    
    process_steps = steps.get(process_type, steps["analysis"])
    
    for i, (message, details) in enumerate(process_steps):
        with placeholder.container():
            render_document_progress_animation(
                process_type=process_type,
                current_step=i,
                total_steps=len(process_steps) - 1,
                message=message,
                details=details
            )
        
        # Simulate processing time
        if i < len(process_steps) - 1:
            time.sleep(1.5)
    
    return True