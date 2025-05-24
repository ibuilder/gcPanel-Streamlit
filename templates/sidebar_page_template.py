"""
Sidebar Page Template for Highland Tower Development

Standard template for all module pages to match the clean sidebar layout.
"""

import streamlit as st

def render_page_header(title, icon="🏗️"):
    """Render standardized page header for sidebar layout."""
    st.title(f"{icon} {title}")

def render_page_metrics(metrics_data):
    """Render standardized metrics section."""
    if not metrics_data:
        return
        
    cols = st.columns(len(metrics_data))
    for i, metric in enumerate(metrics_data):
        with cols[i]:
            st.metric(
                metric.get("label", "Metric"),
                metric.get("value", "N/A"),
                metric.get("delta", None)
            )

def render_page_content(sections):
    """Render standardized page content sections."""
    for section in sections:
        if section.get("type") == "header":
            st.markdown(f"### {section.get('title', 'Section')}")
        elif section.get("type") == "info":
            st.info(section.get("content", ""))
        elif section.get("type") == "text":
            st.markdown(section.get("content", ""))
        elif section.get("type") == "divider":
            st.divider()

def sidebar_page_template(title, icon="🏗️", metrics=None, sections=None):
    """
    Standard template for Highland Tower Development pages.
    
    Args:
        title (str): Page title
        icon (str): Page icon
        metrics (list): List of metric dictionaries
        sections (list): List of content sections
    """
    render_page_header(title, icon)
    
    if metrics:
        render_page_metrics(metrics)
        st.divider()
    
    if sections:
        render_page_content(sections)