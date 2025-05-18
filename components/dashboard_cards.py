"""
Enhanced dashboard card components for the gcPanel application.

This module provides visually appealing and functional card components
for displaying dashboard metrics and information.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def metric_card(title, value, change=None, is_percent=False, icon=None, color="#3367D6"):
    """
    Render a metric card with value and optional trend indicator.
    
    Args:
        title: Card title
        value: Metric value to display
        change: Percentage change (positive or negative)
        is_percent: Whether the value itself is a percentage
        icon: Optional icon name (using Material icons)
        color: Card accent color
    """
    # Format the value
    if isinstance(value, (int, float)):
        if is_percent:
            value_formatted = f"{value}%"
        else:
            value_formatted = f"{value:,}"
    else:
        value_formatted = value
        
    # Create HTML for the card
    html = f"""
    <div class="dashboard-metric" style="border-left: 4px solid {color};">
        <div class="dashboard-metric-value">{value_formatted}</div>
        <div class="dashboard-metric-label">{title}</div>
    """
    
    # Add trend indicator if provided
    if change is not None:
        if change > 0:
            trend_color = "#0F9D58"
            trend_icon = "arrow_upward"
            trend_text = f"+{change}%"
        elif change < 0:
            trend_color = "#DB4437"
            trend_icon = "arrow_downward"
            trend_text = f"{change}%"
        else:
            trend_color = "#5F6368"
            trend_icon = "remove"
            trend_text = "No change"
            
        html += f"""
        <div style="display: flex; align-items: center; margin-top: 5px;">
            <span class="material-icons" style="font-size: 16px; color: {trend_color}; margin-right: 4px;">{trend_icon}</span>
            <span style="font-size: 14px; color: {trend_color};">{trend_text}</span>
        </div>
        """
    
    html += "</div>"
    
    # Display the card
    st.markdown(html, unsafe_allow_html=True)

def info_card(title, content, icon=None, color="#3367D6"):
    """
    Render an information card with title and content.
    
    Args:
        title: Card title
        content: Card content (HTML/markdown)
        icon: Optional icon name (using Material icons)
        color: Card accent color
    """
    html = f"""
    <div class="section-card" style="border-left: 4px solid {color};">
        <div class="section-card-header">
            <h3 class="section-card-title" style="color: {color};">{title}</h3>
            {f'<span class="material-icons" style="color: {color};">{icon}</span>' if icon else ''}
        </div>
        <div class="section-card-content">
            {content}
        </div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)

def activity_item(title, time, icon, color="#3367D6"):
    """
    Render a single activity feed item.
    
    Args:
        title: Activity title
        time: Time string (e.g., "2 hours ago")
        icon: Material icon name
        color: Icon color
    """
    html = f"""
    <div class="activity-item">
        <div class="activity-icon">
            <span class="material-icons" style="color: {color};">{icon}</span>
        </div>
        <div class="activity-content">
            <div class="activity-title">{title}</div>
            <div class="activity-meta">{time}</div>
        </div>
    </div>
    """
    
    return html

def activity_feed(items, max_items=5, title="Recent Activity"):
    """
    Render an activity feed with multiple items.
    
    Args:
        items: List of dictionaries with keys 'title', 'time', 'icon', and 'color'
        max_items: Maximum number of items to display
        title: Feed title
    """
    with st.container():
        st.subheader(title)
        
        feed_html = '<div class="section-card">'
        
        for item in items[:max_items]:
            feed_html += activity_item(
                title=item['title'],
                time=item['time'],
                icon=item['icon'],
                color=item.get('color', "#3367D6")
            )
            
        feed_html += '</div>'
        
        st.markdown(feed_html, unsafe_allow_html=True)

def progress_card(title, current, total, color="#3367D6"):
    """
    Render a progress card with percentage bar.
    
    Args:
        title: Card title
        current: Current value
        total: Total/target value
        color: Progress bar color
    """
    percentage = min(100, round((current / total) * 100))
    
    with st.container():
        st.markdown(f"""
        <div class="dashboard-metric">
            <div class="dashboard-metric-label">{title}</div>
            <div class="dashboard-metric-value">{percentage}%</div>
            <div style="background-color: #E8EAED; height: 8px; border-radius: 4px; margin: 10px 0;">
                <div style="background-color: {color}; width: {percentage}%; height: 8px; border-radius: 4px;"></div>
            </div>
            <div style="font-size: 14px; color: #5F6368; text-align: right;">{current:,} / {total:,}</div>
        </div>
        """, unsafe_allow_html=True)

def plotly_chart_card(title, fig, height=300):
    """
    Render a Plotly chart within a styled card.
    
    Args:
        title: Card title
        fig: Plotly figure object
        height: Chart height
    """
    # Update the figure layout
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", size=12),
        showlegend=True,
        legend=dict(orientation="h", y=-0.2),
        xaxis=dict(gridcolor='#DADCE0', gridwidth=0.5),
        yaxis=dict(gridcolor='#DADCE0', gridwidth=0.5)
    )
    
    # Create the card
    with st.container():
        st.subheader(title)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def create_sample_progress_chart():
    """Create a sample task progress chart for demonstration"""
    categories = ['Design', 'Foundations', 'Structure', 'MEP', 'Finishes']
    completed = [90, 75, 60, 30, 10]
    remaining = [10, 25, 40, 70, 90]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=categories,
        x=completed,
        name='Completed',
        orientation='h',
        marker=dict(color='#3367D6')
    ))
    
    fig.add_trace(go.Bar(
        y=categories,
        x=remaining,
        name='Remaining',
        orientation='h',
        marker=dict(color='#DADCE0')
    ))
    
    fig.update_layout(
        barmode='stack',
        title_text='Project Progress by Category',
        xaxis=dict(title='Percentage (%)', range=[0, 100]),
        legend=dict(orientation="h", y=1.1)
    )
    
    return fig

def create_sample_cost_chart():
    """Create a sample cost tracking chart for demonstration"""
    categories = ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'Other']
    actual = [520000, 780000, 340000, 920000, 95000]
    budget = [500000, 750000, 300000, 900000, 100000]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories,
        y=actual,
        name='Actual',
        marker=dict(color='#4285F4')
    ))
    
    fig.add_trace(go.Bar(
        x=categories,
        y=budget,
        name='Budget',
        marker=dict(color='#5F6368')
    ))
    
    fig.update_layout(
        title_text='Cost Tracking',
        yaxis=dict(title='Amount ($)')
    )
    
    return fig

def create_sample_schedule_chart():
    """Create a sample schedule tracking chart for demonstration"""
    # Create date range
    today = datetime.now()
    date_range = [today + timedelta(days=i) for i in range(-30, 60, 10)]
    date_strings = [d.strftime('%b %d') for d in date_range]
    
    # Create sample data
    planned = [0, 10, 25, 40, 55, 70, 85, 95, 100]
    actual = [0, 12, 28, 38, 52, 60, None, None, None]  # None for future dates
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=date_strings,
        y=planned,
        mode='lines+markers',
        name='Planned',
        line=dict(color='#5F6368', dash='dash'),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=date_strings[:6],  # Only include dates up to today
        y=actual[:6],       # Only include data up to today
        mode='lines+markers',
        name='Actual',
        line=dict(color='#3367D6'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title_text='Schedule Performance',
        yaxis=dict(title='Completion (%)', range=[0, 100])
    )
    
    # Add vertical line for today
    fig.add_shape(
        type="line",
        x0=date_strings[3], x1=date_strings[3],
        y0=0, y1=100,
        line=dict(color="#DB4437", width=2, dash="dash"),
    )
    
    # Add "Today" annotation
    fig.add_annotation(
        x=date_strings[3], y=100,
        text="Today",
        showarrow=False,
        yshift=10,
        font=dict(color="#DB4437")
    )
    
    return fig