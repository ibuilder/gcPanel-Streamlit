"""
Project Timeline Prediction for gcPanel.

This module provides predictive analytics for project timelines,
forecasting completion dates and identifying potential schedule risks.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Import scikit-learn for prediction
try:
    from sklearn.linear_model import LinearRegression
except ImportError:
    # Create a simple fallback if sklearn is not available
    class LinearRegression:
        def __init__(self):
            pass
        
        def fit(self, X, y):
            # Simple linear regression implementation
            self.X = X
            self.y = y
            n = len(X)
            self.coef_ = [np.cov(X.flatten(), y)[0, 1] / np.var(X.flatten())]
            self.intercept_ = np.mean(y) - self.coef_[0] * np.mean(X.flatten())
            return self
        
        def predict(self, X):
            return self.intercept_ + self.coef_[0] * X.flatten()

# Utility functions for timeline prediction
def get_project_schedule_data():
    """
    Get project schedule data for prediction.
    
    In a production environment, this would fetch real data from the database.
    """
    # Generate dates for last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date, freq='W')
    
    # Generate schedule data (% complete)
    planned_progress = np.linspace(0, 85, len(dates))  # Project is 85% complete
    
    # Add some randomness to actual progress
    noise = np.cumsum(np.random.normal(0, 0.5, len(dates)))
    actual_progress = planned_progress + noise
    actual_progress = np.clip(actual_progress, 0, 100)
    
    # Add milestone data
    milestones = [
        {"name": "Project Start", "date": start_date, "completion": 0},
        {"name": "Foundation Complete", "date": start_date + timedelta(days=60), "completion": 15},
        {"name": "Structure Complete", "date": start_date + timedelta(days=150), "completion": 40},
        {"name": "Envelope Complete", "date": start_date + timedelta(days=240), "completion": 60},
        {"name": "Interior Complete", "date": start_date + timedelta(days=330), "completion": 80},
        {"name": "Project Completion", "date": start_date + timedelta(days=450), "completion": 100}
    ]
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'planned_progress': planned_progress,
        'actual_progress': actual_progress
    })
    
    return df, milestones

def predict_project_completion(df, target_completion=100):
    """
    Predict project completion date using linear regression.
    
    Args:
        df: DataFrame with progress data
        target_completion: Target completion percentage
        
    Returns:
        tuple: (predicted_date, confidence_interval)
    """
    # Convert dates to numeric for regression
    df = df.copy()
    df['date_numeric'] = (df['date'] - df['date'].min()).dt.days
    
    # Create linear regression model
    model = LinearRegression()
    X = df['date_numeric'].values.reshape(-1, 1)
    y = df['actual_progress'].values
    
    # Fit model
    model.fit(X, y)
    
    # Predict days needed to reach target completion
    current_progress = df['actual_progress'].iloc[-1]
    if current_progress >= target_completion:
        return df['date'].iloc[-1], (0, 0)
    
    progress_per_day = model.coef_[0]
    days_needed = (target_completion - current_progress) / progress_per_day
    
    # Calculate prediction date
    last_date = df['date'].iloc[-1]
    predicted_date = last_date + timedelta(days=days_needed)
    
    # Calculate confidence interval (simplified)
    residuals = y - model.predict(X)
    std_error = np.std(residuals)
    confidence_days = int(1.96 * std_error / progress_per_day)
    
    return predicted_date, (confidence_days, confidence_days)

def predict_milestone_dates(df, milestones):
    """
    Predict milestone dates based on current progress.
    
    Args:
        df: DataFrame with progress data
        milestones: List of milestone dictionaries
        
    Returns:
        list: Updated milestones with predicted dates
    """
    updated_milestones = []
    
    for milestone in milestones:
        # Skip milestones that are already completed
        if df['actual_progress'].iloc[-1] >= milestone['completion']:
            milestone['status'] = "Completed"
            milestone['predicted_date'] = milestone['date']
            milestone['delay'] = 0
        else:
            # Predict date for this milestone
            predicted_date, confidence = predict_project_completion(df, milestone['completion'])
            
            # Calculate delay
            delay = (predicted_date - milestone['date']).days
            
            milestone['status'] = "Pending"
            milestone['predicted_date'] = predicted_date
            milestone['delay'] = delay
            milestone['confidence'] = confidence
        
        updated_milestones.append(milestone)
    
    return updated_milestones

def create_schedule_forecast_chart(df, predicted_date, confidence_interval):
    """
    Create schedule forecast chart with prediction.
    
    Args:
        df: DataFrame with progress data
        predicted_date: Predicted completion date
        confidence_interval: Confidence interval in days
        
    Returns:
        plotly.graph_objects.Figure: Forecast chart
    """
    # Create figure
    fig = go.Figure()
    
    # Add traces for historical data
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['planned_progress'],
            name="Planned Progress",
            line=dict(color='blue', dash='dash')
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['actual_progress'],
            name="Actual Progress",
            line=dict(color='green')
        )
    )
    
    # Add forecast
    last_date = df['date'].iloc[-1]
    last_progress = df['actual_progress'].iloc[-1]
    
    # Create forecast dates
    forecast_dates = pd.date_range(
        start=last_date,
        end=predicted_date + timedelta(days=30),
        freq='W'
    )
    
    # Create linear forecast
    days_to_completion = (predicted_date - last_date).days
    if days_to_completion > 0:
        progress_per_day = (100 - last_progress) / days_to_completion
        forecast_progress = [
            min(100, last_progress + progress_per_day * (date - last_date).days)
            for date in forecast_dates
        ]
    else:
        forecast_progress = [100] * len(forecast_dates)
    
    # Add forecast trace
    fig.add_trace(
        go.Scatter(
            x=forecast_dates,
            y=forecast_progress,
            name="Forecast",
            line=dict(color='red', dash='dot')
        )
    )
    
    # Add confidence interval
    lower_dates = [predicted_date - timedelta(days=confidence_interval[0])]
    upper_dates = [predicted_date + timedelta(days=confidence_interval[1])]
    
    fig.add_trace(
        go.Scatter(
            x=[predicted_date],
            y=[100],
            name="Predicted Completion",
            mode="markers",
            marker=dict(color="red", size=12, symbol="star")
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=lower_dates + upper_dates,
            y=[100, 100],
            name="Confidence Interval",
            mode="markers",
            marker=dict(color="orange", size=10, symbol="diamond")
        )
    )
    
    # Update layout
    fig.update_layout(
        title="Schedule Forecast",
        xaxis_title="Date",
        yaxis_title="Completion (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        hovermode="x unified",
        height=500
    )
    
    # Add current date line
    fig.add_vline(
        x=datetime.now(),
        line_width=2,
        line_dash="dash",
        line_color="green",
        annotation_text="Today",
        annotation_position="top right"
    )
    
    return fig

def create_milestone_gantt_chart(milestones):
    """
    Create Gantt chart for milestones.
    
    Args:
        milestones: List of milestone dictionaries
        
    Returns:
        plotly.graph_objects.Figure: Gantt chart
    """
    # Prepare data for Gantt chart
    tasks = []
    for i, milestone in enumerate(milestones):
        # Original planned milestone
        tasks.append({
            "Task": milestone["name"],
            "Start": milestone["date"] - timedelta(days=5),
            "Finish": milestone["date"] + timedelta(days=5),
            "Type": "Planned",
            "Status": milestone["status"],
            "Index": i
        })
        
        # Add predicted milestone if it's pending
        if milestone["status"] == "Pending":
            tasks.append({
                "Task": milestone["name"],
                "Start": milestone["predicted_date"] - timedelta(days=5),
                "Finish": milestone["predicted_date"] + timedelta(days=5),
                "Type": "Predicted",
                "Status": milestone["status"],
                "Index": i
            })
    
    # Convert to DataFrame
    df = pd.DataFrame(tasks)
    
    # Create color mapping
    color_map = {
        "Planned-Completed": "green",
        "Planned-Pending": "blue",
        "Predicted-Pending": "red"
    }
    
    # Add combined column for coloring
    df["Color"] = df["Type"] + "-" + df["Status"]
    
    # Create Gantt chart
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Color",
        color_discrete_map=color_map,
        category_orders={"Task": [m["name"] for m in milestones]}
    )
    
    # Update layout
    fig.update_layout(
        title="Milestone Timeline",
        xaxis_title="Date",
        yaxis_title="Milestone",
        legend_title="Type",
        height=400
    )
    
    # Add today line
    fig.add_vline(
        x=datetime.now(),
        line_width=2,
        line_dash="dash",
        line_color="green",
        annotation_text="Today",
        annotation_position="top right"
    )
    
    return fig

def create_progress_comparison_chart(df):
    """
    Create chart comparing actual vs planned progress rate.
    
    Args:
        df: DataFrame with progress data
        
    Returns:
        plotly.graph_objects.Figure: Progress rate chart
    """
    # Calculate progress rates
    df = df.copy()
    df['planned_rate'] = df['planned_progress'].diff().fillna(0)
    df['actual_rate'] = df['actual_progress'].diff().fillna(0)
    
    # Calculate moving averages for smoothing
    window = 4  # 4-week moving average
    df['planned_rate_ma'] = df['planned_rate'].rolling(window=window).mean().fillna(df['planned_rate'])
    df['actual_rate_ma'] = df['actual_rate'].rolling(window=window).mean().fillna(df['actual_rate'])
    
    # Create figure
    fig = go.Figure()
    
    # Add traces
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['planned_rate_ma'],
            name="Planned Progress Rate",
            line=dict(color='blue', dash='dash')
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['actual_rate_ma'],
            name="Actual Progress Rate",
            line=dict(color='green')
        )
    )
    
    # Add reference line for average rate needed
    current_date = datetime.now()
    current_progress = df.loc[df['date'] <= current_date, 'actual_progress'].iloc[-1]
    avg_rate_needed = (100 - current_progress) / ((df['date'].max() - current_date).days / 7)
    
    fig.add_trace(
        go.Scatter(
            x=[df['date'].min(), df['date'].max()],
            y=[avg_rate_needed, avg_rate_needed],
            name="Required Average Rate",
            line=dict(color='red', dash='dot')
        )
    )
    
    # Update layout
    fig.update_layout(
        title="Progress Rate Comparison (% per week)",
        xaxis_title="Date",
        yaxis_title="Progress Rate (% per week)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        hovermode="x unified",
        height=400
    )
    
    return fig

def render_timeline_prediction():
    """Render the timeline prediction interface."""
    st.header("Project Timeline Prediction")
    
    # Get project data
    df, milestones = get_project_schedule_data()
    
    # Project selector (in a real app, this would load different project data)
    project = st.selectbox(
        "Select Project",
        ["Highland Tower Development", "Project B", "Project C"],
        index=0
    )
    
    # Get current project completion
    current_completion = df['actual_progress'].iloc[-1]
    
    # Display current status
    st.info(f"Current Project Completion: {current_completion:.1f}%")
    
    # Input for target completion
    target_completion = st.slider(
        "Target Completion Percentage",
        min_value=float(current_completion),
        max_value=100.0,
        value=100.0,
        step=5.0
    )
    
    # Predict completion date
    predicted_date, confidence_interval = predict_project_completion(df, target_completion)
    
    # Display prediction
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Predicted Completion Date",
            value=predicted_date.strftime("%Y-%m-%d")
        )
    
    with col2:
        # Calculate if ahead or behind schedule
        planned_date = milestones[-1]["date"]
        days_diff = (predicted_date - planned_date).days
        
        status = "On Schedule"
        delta_color = "off"
        
        if days_diff > 0:
            status = f"{days_diff} days behind"
            delta_color = "inverse"
        elif days_diff < 0:
            status = f"{abs(days_diff)} days ahead"
            delta_color = "normal"
        
        st.metric(
            label="Schedule Status",
            value=status,
            delta=status,
            delta_color=delta_color
        )
    
    with col3:
        st.metric(
            label="Confidence Interval",
            value=f"±{confidence_interval[0]} days"
        )
    
    # Show forecast chart
    st.plotly_chart(
        create_schedule_forecast_chart(df, predicted_date, confidence_interval),
        use_container_width=True
    )
    
    # Calculate milestone predictions
    predicted_milestones = predict_milestone_dates(df, milestones)
    
    # Show milestone Gantt chart
    st.subheader("Milestone Timeline")
    st.plotly_chart(
        create_milestone_gantt_chart(predicted_milestones),
        use_container_width=True
    )
    
    # Show progress rate comparison
    st.subheader("Progress Rate Analysis")
    st.plotly_chart(
        create_progress_comparison_chart(df),
        use_container_width=True
    )
    
    # Show detailed milestone table
    st.subheader("Milestone Prediction Details")
    
    milestone_data = []
    for m in predicted_milestones:
        milestone_data.append({
            "Milestone": m["name"],
            "Planned Date": m["date"].strftime("%Y-%m-%d"),
            "Predicted Date": m["predicted_date"].strftime("%Y-%m-%d"),
            "Status": m["status"],
            "Delay (days)": m["delay"] if "delay" in m else 0
        })
    
    st.dataframe(pd.DataFrame(milestone_data))