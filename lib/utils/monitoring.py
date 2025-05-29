"""
Monitoring and analytics for gcPanel.

This module provides monitoring capabilities to track application
performance, usage, and errors in production environments.
"""

import logging
import time
import os
import json
import traceback
from datetime import datetime
from functools import wraps
from threading import Thread, Lock
from queue import Queue

# Setup logging
logger = logging.getLogger(__name__)

# Global monitoring state
_monitoring_enabled = os.environ.get("ENABLE_MONITORING", "false").lower() == "true"
_metrics_queue = Queue(maxsize=1000)
_metrics_lock = Lock()
_metrics = {
    "requests": 0,
    "errors": 0,
    "response_times": [],
    "active_users": 0,
    "page_views": {},
    "start_time": datetime.utcnow().isoformat()
}

def enable_monitoring():
    """Enable application monitoring."""
    global _monitoring_enabled
    _monitoring_enabled = True
    logger.info("Application monitoring enabled")
    
    # Start metrics processing thread
    Thread(target=_process_metrics_queue, daemon=True).start()

def disable_monitoring():
    """Disable application monitoring."""
    global _monitoring_enabled
    _monitoring_enabled = False
    logger.info("Application monitoring disabled")

def is_monitoring_enabled():
    """Check if monitoring is enabled."""
    return _monitoring_enabled

def _process_metrics_queue():
    """Background thread to process metrics queue."""
    while True:
        try:
            # Get metric from queue
            metric = _metrics_queue.get(block=True, timeout=1.0)
            
            # Process metric
            with _metrics_lock:
                if metric["type"] == "request":
                    _metrics["requests"] += 1
                    _metrics["response_times"].append(metric["response_time"])
                    # Keep only last 1000 response times
                    if len(_metrics["response_times"]) > 1000:
                        _metrics["response_times"] = _metrics["response_times"][-1000:]
                
                elif metric["type"] == "error":
                    _metrics["errors"] += 1
                
                elif metric["type"] == "page_view":
                    page = metric["page"]
                    _metrics["page_views"][page] = _metrics["page_views"].get(page, 0) + 1
                
                elif metric["type"] == "user_activity":
                    _metrics["active_users"] = metric["count"]
            
            # Mark as done
            _metrics_queue.task_done()
        except Exception as e:
            # Just log and continue
            logger.error(f"Error processing metrics: {str(e)}")

def record_request(response_time):
    """
    Record a request and its response time.
    
    Args:
        response_time: Response time in milliseconds
    """
    if not _monitoring_enabled:
        return
    
    try:
        _metrics_queue.put({
            "type": "request",
            "timestamp": datetime.utcnow().isoformat(),
            "response_time": response_time
        }, block=False)
    except Exception:
        # Ignore if queue is full
        pass

def record_error(error_type, message):
    """
    Record an application error.
    
    Args:
        error_type: Type of error
        message: Error message
    """
    if not _monitoring_enabled:
        return
    
    try:
        _metrics_queue.put({
            "type": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": error_type,
            "message": message
        }, block=False)
    except Exception:
        # Ignore if queue is full
        pass

def record_page_view(page):
    """
    Record a page view.
    
    Args:
        page: Page name or path
    """
    if not _monitoring_enabled:
        return
    
    try:
        _metrics_queue.put({
            "type": "page_view",
            "timestamp": datetime.utcnow().isoformat(),
            "page": page
        }, block=False)
    except Exception:
        # Ignore if queue is full
        pass

def update_active_users(count):
    """
    Update active user count.
    
    Args:
        count: Number of active users
    """
    if not _monitoring_enabled:
        return
    
    try:
        _metrics_queue.put({
            "type": "user_activity",
            "timestamp": datetime.utcnow().isoformat(),
            "count": count
        }, block=False)
    except Exception:
        # Ignore if queue is full
        pass

def get_metrics():
    """
    Get current metrics.
    
    Returns:
        dict: Current metrics
    """
    with _metrics_lock:
        # Create a copy
        metrics_copy = dict(_metrics)
        
        # Add calculated metrics
        metrics_copy["avg_response_time"] = sum(metrics_copy["response_times"]) / len(metrics_copy["response_times"]) if metrics_copy["response_times"] else 0
        metrics_copy["response_times"] = len(metrics_copy["response_times"])  # Just return count
        
        # Add timestamp
        metrics_copy["timestamp"] = datetime.utcnow().isoformat()
        
        return metrics_copy

def export_metrics(format="json"):
    """
    Export metrics in specified format.
    
    Args:
        format: Export format (json, csv)
        
    Returns:
        str: Formatted metrics
    """
    metrics = get_metrics()
    
    if format.lower() == "json":
        return json.dumps(metrics, indent=2)
    
    elif format.lower() == "csv":
        csv_lines = ["metric,value"]
        
        for key, value in metrics.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    csv_lines.append(f"{key}.{subkey},{subvalue}")
            else:
                csv_lines.append(f"{key},{value}")
        
        return "\n".join(csv_lines)
    
    else:
        raise ValueError(f"Unsupported format: {format}")

def monitor_response_time(func):
    """
    Decorator to monitor function response time.
    
    Args:
        func: Function to monitor
        
    Returns:
        Function with monitoring
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Skip if monitoring disabled
        if not _monitoring_enabled:
            return func(*args, **kwargs)
        
        # Record start time
        start_time = time.time()
        
        try:
            # Call function
            result = func(*args, **kwargs)
            
            # Record response time
            response_time = (time.time() - start_time) * 1000  # ms
            record_request(response_time)
            
            return result
        except Exception as e:
            # Record error
            error_type = type(e).__name__
            record_error(error_type, str(e))
            
            # Re-raise
            raise
    
    return wrapper

def render_metrics_dashboard():
    """
    Render a metrics dashboard in Streamlit.
    
    This should only be available to admin users.
    """
    import streamlit as st
    
    st.title("Application Metrics")
    
    if not _monitoring_enabled:
        st.warning("Monitoring is currently disabled. Enable it in the application settings.")
        
        if st.button("Enable Monitoring"):
            enable_monitoring()
            st.success("Monitoring enabled!")
            st.rerun()
        
        return
    
    # Get current metrics
    metrics = get_metrics()
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Requests", metrics["requests"])
    
    with col2:
        st.metric("Errors", metrics["errors"])
    
    with col3:
        st.metric("Avg Response Time", f"{metrics['avg_response_time']:.2f} ms")
    
    with col4:
        st.metric("Active Users", metrics["active_users"])
    
    # Page views
    st.subheader("Page Views")
    
    if metrics["page_views"]:
        import pandas as pd
        
        # Convert to DataFrame
        page_views_df = pd.DataFrame({
            "Page": list(metrics["page_views"].keys()),
            "Views": list(metrics["page_views"].values())
        }).sort_values("Views", ascending=False)
        
        st.bar_chart(page_views_df.set_index("Page"))
    else:
        st.info("No page views recorded yet.")
    
    # Export options
    st.subheader("Export Metrics")
    
    export_format = st.selectbox("Export Format", ["JSON", "CSV"])
    
    if st.button("Export"):
        exported = export_metrics(export_format.lower())
        st.download_button(
            label=f"Download {export_format}",
            data=exported,
            file_name=f"metrics_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{export_format.lower()}",
            mime="text/plain"
        )
    
    # Admin controls
    st.subheader("Admin Controls")
    
    if st.button("Reset Metrics"):
        with _metrics_lock:
            _metrics["requests"] = 0
            _metrics["errors"] = 0
            _metrics["response_times"] = []
            _metrics["page_views"] = {}
            _metrics["start_time"] = datetime.utcnow().isoformat()
        
        st.success("Metrics reset successfully!")
    
    if st.button("Disable Monitoring"):
        disable_monitoring()
        st.warning("Monitoring disabled!")
        st.rerun()