"""
Project Budget Prediction for gcPanel.

This module provides predictive analytics for project budgets,
forecasting final costs and identifying potential budget risks.
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

# Utility functions for budget prediction
def get_project_budget_data():
    """
    Get project budget data for prediction.
    
    In a production environment, this would fetch real data from the database.
    """
    # Generate dates for last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    
    # Generate budget data
    total_budget = 45500000  # $45.5M total budget
    planned_budget = np.linspace(0, total_budget * 0.85, len(dates))  # Project is 85% complete financially
    
    # Add some randomness to actual costs
    noise = np.cumsum(np.random.normal(0, 100000, len(dates)))
    actual_costs = planned_budget + noise
    
    # Generate category data
    categories = [
        "Labor", 
        "Materials", 
        "Equipment", 
        "Subcontractors", 
        "Overhead", 
        "Permits",
        "Contingency"
    ]
    
    category_allocations = {
        "Labor": 0.35,
        "Materials": 0.25,
        "Equipment": 0.15,
        "Subcontractors": 0.10,
        "Overhead": 0.05,
        "Permits": 0.02,
        "Contingency": 0.08
    }
    
    # Generate category actuals
    category_data = {}
    
    for category, allocation in category_allocations.items():
        # Planned spending for category
        planned = planned_budget * allocation
        
        # Actual spending for category (with different variance per category)
        if category == "Labor":
            variance = 0.10  # Labor costs tend to vary more
        elif category == "Materials":
            variance = 0.15  # Material costs vary a lot
        elif category == "Contingency":
            variance = -0.30  # Contingency often underused
        else:
            variance = 0.05  # Other categories more stable
        
        noise = np.cumsum(np.random.normal(0, allocation * 50000, len(dates)))
        actual = planned * (1 + variance) + noise
        
        category_data[f"{category}_planned"] = planned
        category_data[f"{category}_actual"] = actual
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'planned_total': planned_budget,
        'actual_total': actual_costs,
        **category_data
    })
    
    return df, categories, total_budget

def predict_final_cost(df, total_budget):
    """
    Predict final project cost using regression.
    
    Args:
        df: DataFrame with cost data
        total_budget: Total project budget
        
    Returns:
        tuple: (predicted_cost, confidence_interval)
    """
    # Calculate current project completion percentage
    current_planned = df['planned_total'].iloc[-1]
    current_planned_pct = current_planned / total_budget
    
    # If project is nearly complete, use actual trends only
    if current_planned_pct > 0.9:
        # Simple extrapolation based on actual/planned ratio
        ratio = df['actual_total'].iloc[-1] / df['planned_total'].iloc[-1]
        predicted_cost = total_budget * ratio
        
        # Calculate simple confidence interval
        std_dev = np.std(df['actual_total'] / df['planned_total']) * total_budget
        confidence = (std_dev, std_dev)
        
        return predicted_cost, confidence
    
    # Convert to percentage of completion for better modeling
    df = df.copy()
    df['planned_pct'] = df['planned_total'] / total_budget
    df['actual_ratio'] = df['actual_total'] / df['planned_total']
    
    # Use last 6 months of data for prediction if available
    min_rows = min(6, len(df))
    recent_df = df.iloc[-min_rows:]
    
    # Create linear regression model
    model = LinearRegression()
    X = recent_df['planned_pct'].values.reshape(-1, 1)
    y = recent_df['actual_ratio'].values
    
    # Fit model
    model.fit(X, y)
    
    # Predict final ratio at 100% completion
    final_ratio = model.predict([[1.0]])[0]
    
    # Calculate final cost
    predicted_cost = total_budget * final_ratio
    
    # Calculate confidence interval
    residuals = y - model.predict(X)
    std_error = np.std(residuals) * total_budget
    confidence = (std_error, std_error)
    
    return predicted_cost, confidence

def predict_category_costs(df, categories, total_budget):
    """
    Predict final costs by category.
    
    Args:
        df: DataFrame with cost data
        categories: List of cost categories
        total_budget: Total project budget
        
    Returns:
        dict: Dictionary of predicted category costs
    """
    # Calculate current project completion percentage
    current_planned = df['planned_total'].iloc[-1]
    current_planned_pct = current_planned / total_budget
    
    # Initialize results
    predictions = {}
    
    for category in categories:
        planned_col = f"{category}_planned"
        actual_col = f"{category}_actual"
        
        # Calculate current values
        current_planned_cat = df[planned_col].iloc[-1]
        current_actual_cat = df[actual_col].iloc[-1]
        
        # Calculate ratio of actual to planned
        ratio = current_actual_cat / current_planned_cat if current_planned_cat > 0 else 1.0
        
        # Simple extrapolation for category
        cat_allocation = current_planned_cat / current_planned
        cat_budget = total_budget * cat_allocation
        predicted_cost = cat_budget * ratio
        
        # Calculate risk level
        if ratio > 1.15:
            risk = "High"
        elif ratio > 1.05:
            risk = "Medium"
        else:
            risk = "Low"
        
        # Store results
        predictions[category] = {
            "planned_budget": cat_budget,
            "predicted_cost": predicted_cost,
            "variance_pct": (ratio - 1) * 100,
            "risk_level": risk
        }
    
    return predictions

def create_cost_forecast_chart(df, total_budget, predicted_cost, confidence_interval):
    """
    Create cost forecast chart with prediction.
    
    Args:
        df: DataFrame with cost data
        total_budget: Total project budget
        predicted_cost: Predicted final cost
        confidence_interval: Confidence interval
        
    Returns:
        plotly.graph_objects.Figure: Forecast chart
    """
    # Create figure
    fig = go.Figure()
    
    # Add traces for historical data
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['planned_total'],
            name="Planned Expenditure",
            line=dict(color='blue', dash='dash')
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['actual_total'],
            name="Actual Expenditure",
            line=dict(color='green')
        )
    )
    
    # Add projection to complete
    # Calculate current project completion percentage
    current_planned = df['planned_total'].iloc[-1]
    current_planned_pct = current_planned / total_budget
    current_actual = df['actual_total'].iloc[-1]
    
    # Create forecast dates based on expected completion timeline
    remaining_pct = 1.0 - current_planned_pct
    months_remaining = int(remaining_pct * 12) + 2  # Assume project completion within a year plus buffer
    forecast_dates = pd.date_range(
        start=df['date'].iloc[-1] + pd.DateOffset(months=1),
        periods=months_remaining,
        freq='M'
    )
    
    # Create planned projection
    planned_projection = np.linspace(
        current_planned,
        total_budget,
        months_remaining
    )
    
    # Create actual projection
    actual_projection = np.linspace(
        current_actual,
        predicted_cost,
        months_remaining
    )
    
    # Add total budget reference line
    fig.add_trace(
        go.Scatter(
            x=[df['date'].min(), forecast_dates[-1]],
            y=[total_budget, total_budget],
            name="Total Budget",
            line=dict(color='red', dash='dash')
        )
    )
    
    # Add planned projection
    fig.add_trace(
        go.Scatter(
            x=forecast_dates,
            y=planned_projection,
            name="Planned Projection",
            line=dict(color='blue', dash='dot')
        )
    )
    
    # Add actual projection
    fig.add_trace(
        go.Scatter(
            x=forecast_dates,
            y=actual_projection,
            name="Cost Projection",
            line=dict(color='orange', dash='dot')
        )
    )
    
    # Add confidence interval
    upper_bound = predicted_cost + confidence_interval[1]
    lower_bound = predicted_cost - confidence_interval[0]
    
    fig.add_trace(
        go.Scatter(
            x=[forecast_dates[-1], forecast_dates[-1]],
            y=[lower_bound, upper_bound],
            name="Confidence Interval",
            mode="lines",
            line=dict(color='gray', width=8),
            showlegend=False
        )
    )
    
    # Add markers for final predicted cost
    fig.add_trace(
        go.Scatter(
            x=[forecast_dates[-1]],
            y=[predicted_cost],
            name="Predicted Final Cost",
            mode="markers",
            marker=dict(color="red", size=12, symbol="star")
        )
    )
    
    # Update layout
    fig.update_layout(
        title="Cost Forecast",
        xaxis_title="Date",
        yaxis_title="Cumulative Cost ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        hovermode="x unified",
        height=500
    )
    
    # Format y-axis as currency
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    
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

def create_category_forecast_chart(category_predictions, categories, total_budget):
    """
    Create category forecast chart.
    
    Args:
        category_predictions: Dictionary of category predictions
        categories: List of cost categories
        total_budget: Total project budget
        
    Returns:
        plotly.graph_objects.Figure: Category forecast chart
    """
    # Prepare data
    cat_names = []
    planned_values = []
    predicted_values = []
    colors = []
    
    for category in categories:
        pred = category_predictions[category]
        cat_names.append(category)
        planned_values.append(pred["planned_budget"])
        predicted_values.append(pred["predicted_cost"])
        
        # Set color based on risk level
        if pred["risk_level"] == "High":
            colors.append("red")
        elif pred["risk_level"] == "Medium":
            colors.append("orange")
        else:
            colors.append("green")
    
    # Create figure
    fig = go.Figure()
    
    # Add bars for planned budget
    fig.add_trace(
        go.Bar(
            y=cat_names,
            x=planned_values,
            name="Planned Budget",
            orientation='h',
            marker_color='blue'
        )
    )
    
    # Add bars for predicted costs
    fig.add_trace(
        go.Bar(
            y=cat_names,
            x=predicted_values,
            name="Predicted Cost",
            orientation='h',
            marker=dict(color=colors)
        )
    )
    
    # Update layout
    fig.update_layout(
        title="Cost Forecast by Category",
        xaxis_title="Cost ($)",
        yaxis_title="Category",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        barmode='group',
        height=400
    )
    
    # Format x-axis as currency
    fig.update_xaxes(tickprefix="$", tickformat=",.0f")
    
    return fig

def create_cost_variance_chart(df, categories):
    """
    Create chart showing cost variance trends by category.
    
    Args:
        df: DataFrame with cost data
        categories: List of cost categories
        
    Returns:
        plotly.graph_objects.Figure: Variance chart
    """
    # Create figure
    fig = go.Figure()
    
    # Calculate variance for each category over time
    for category in categories:
        planned_col = f"{category}_planned"
        actual_col = f"{category}_actual"
        
        # Calculate variance percentage
        variance_pct = ((df[actual_col] - df[planned_col]) / df[planned_col]) * 100
        
        # Add line for this category
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=variance_pct,
                name=category,
                mode='lines+markers'
            )
        )
    
    # Update layout
    fig.update_layout(
        title="Cost Variance Trends by Category",
        xaxis_title="Date",
        yaxis_title="Variance (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        hovermode="x unified",
        height=400
    )
    
    # Add zero line
    fig.add_hline(
        y=0,
        line_width=1,
        line_dash="dash",
        line_color="black"
    )
    
    return fig

def render_budget_prediction():
    """Render the budget prediction interface."""
    st.header("Project Budget Prediction")
    
    # Get project data
    df, categories, total_budget = get_project_budget_data()
    
    # Project selector (in a real app, this would load different project data)
    project = st.selectbox(
        "Select Project",
        ["Highland Tower Development", "Project B", "Project C"],
        index=0
    )
    
    # Get current budget status
    current_planned = df['planned_total'].iloc[-1]
    current_actual = df['actual_total'].iloc[-1]
    
    # Calculate current variance
    current_variance = ((current_actual - current_planned) / current_planned) * 100
    
    # Display current status
    st.info(f"Current Budget Status: ${current_actual:,.0f} spent of ${current_planned:,.0f} planned ({current_variance:.1f}% variance)")
    
    # Predict final cost
    predicted_cost, confidence_interval = predict_final_cost(df, total_budget)
    
    # Calculate budget variance
    budget_variance = ((predicted_cost - total_budget) / total_budget) * 100
    
    # Display prediction
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Budget",
            value=f"${total_budget:,.0f}"
        )
    
    with col2:
        variance_text = f"{budget_variance:.1f}%"
        delta_color = "inverse" if budget_variance > 0 else "normal"
        
        st.metric(
            label="Predicted Final Cost",
            value=f"${predicted_cost:,.0f}",
            delta=variance_text,
            delta_color=delta_color
        )
    
    with col3:
        lower_bound = predicted_cost - confidence_interval[0]
        upper_bound = predicted_cost + confidence_interval[1]
        
        st.metric(
            label="Confidence Range",
            value=f"${lower_bound:,.0f} - ${upper_bound:,.0f}"
        )
    
    # Show forecast chart
    st.plotly_chart(
        create_cost_forecast_chart(df, total_budget, predicted_cost, confidence_interval),
        use_container_width=True
    )
    
    # Predict category costs
    category_predictions = predict_category_costs(df, categories, total_budget)
    
    # Show category forecast chart
    st.subheader("Category Analysis")
    st.plotly_chart(
        create_category_forecast_chart(category_predictions, categories, total_budget),
        use_container_width=True
    )
    
    # Show variance trends
    st.plotly_chart(
        create_cost_variance_chart(df, categories),
        use_container_width=True
    )
    
    # Show category breakdown table
    st.subheader("Category Predictions")
    
    # Prepare data for table
    cat_data = []
    for category in categories:
        pred = category_predictions[category]
        cat_data.append({
            "Category": category,
            "Planned Budget": f"${pred['planned_budget']:,.0f}",
            "Predicted Cost": f"${pred['predicted_cost']:,.0f}",
            "Variance": f"{pred['variance_pct']:.1f}%",
            "Risk Level": pred['risk_level']
        })
    
    st.dataframe(pd.DataFrame(cat_data))
    
    # Add risk mitigation recommendations
    st.subheader("Budget Risk Analysis")
    
    # Identify high-risk categories
    high_risk = [c for c in categories if category_predictions[c]["risk_level"] == "High"]
    medium_risk = [c for c in categories if category_predictions[c]["risk_level"] == "Medium"]
    
    if high_risk:
        st.error(f"High Risk Categories: {', '.join(high_risk)}")
        
        for category in high_risk:
            st.markdown(f"**{category} Risk Mitigation:**")
            
            # Generate recommendations based on category
            if category == "Labor":
                st.markdown("- Review staffing plans and overtime policies")
                st.markdown("- Consider subcontracting options for remaining work")
                st.markdown("- Implement productivity improvement measures")
            elif category == "Materials":
                st.markdown("- Audit material usage and waste factors")
                st.markdown("- Explore alternative suppliers or materials")
                st.markdown("- Lock in prices for remaining materials")
            elif category == "Equipment":
                st.markdown("- Optimize equipment utilization schedules")
                st.markdown("- Evaluate rental vs. purchase decisions")
                st.markdown("- Consider equipment sharing with other projects")
            else:
                st.markdown("- Review budget allocation and spending patterns")
                st.markdown("- Implement additional approval levels for expenditures")
                st.markdown("- Identify cost reduction opportunities")
    
    if medium_risk:
        st.warning(f"Medium Risk Categories: {', '.join(medium_risk)}")
        
    if not high_risk and not medium_risk:
        st.success("All categories are currently low risk.")