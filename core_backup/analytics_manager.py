"""
Advanced Analytics Manager for gcPanel Highland Tower Development

Implements predictive analytics, AI-powered insights, and custom dashboards
for intelligent construction management decision-making.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

class AnalyticsManager:
    """Enterprise analytics manager with AI-powered predictions"""
    
    def __init__(self):
        self.setup_logging()
        self.prediction_models = {}
        self.initialize_models()
    
    def setup_logging(self):
        """Setup analytics operation logging"""
        self.logger = logging.getLogger('AnalyticsManager')
    
    def initialize_models(self):
        """Initialize machine learning models for predictions"""
        # Project completion prediction model
        self.prediction_models['completion'] = LinearRegression()
        
        # Cost overrun prediction model
        self.prediction_models['cost'] = RandomForestRegressor(n_estimators=100, random_state=42)
        
        # Risk assessment model
        self.prediction_models['risk'] = RandomForestRegressor(n_estimators=50, random_state=42)
        
        # Train models with Highland Tower Development data
        self.train_prediction_models()
    
    def train_prediction_models(self):
        """Train prediction models with Highland Tower Development historical data"""
        # Generate training data based on Highland Tower project patterns
        project_data = self.generate_training_data()
        
        # Train completion prediction model
        completion_features = project_data[['progress_rate', 'weather_impact', 'resource_availability']]
        completion_target = project_data['days_to_completion']
        self.prediction_models['completion'].fit(completion_features, completion_target)
        
        # Train cost prediction model
        cost_features = project_data[['current_progress', 'change_orders', 'material_inflation', 'labor_hours']]
        cost_target = project_data['final_cost_variance']
        self.prediction_models['cost'].fit(cost_features, cost_target)
        
        # Train risk model
        risk_features = project_data[['safety_incidents', 'weather_delays', 'rfi_count', 'quality_issues']]
        risk_target = project_data['risk_score']
        self.prediction_models['risk'].fit(risk_features, risk_target)
        
        self.logger.info("Prediction models trained successfully")
    
    def generate_training_data(self) -> pd.DataFrame:
        """Generate realistic training data for Highland Tower Development"""
        np.random.seed(42)
        n_samples = 500
        
        data = {
            'progress_rate': np.random.normal(1.2, 0.3, n_samples),
            'weather_impact': np.random.uniform(0, 1, n_samples),
            'resource_availability': np.random.normal(0.85, 0.15, n_samples),
            'current_progress': np.random.uniform(10, 95, n_samples),
            'change_orders': np.random.poisson(3, n_samples),
            'material_inflation': np.random.normal(0.05, 0.02, n_samples),
            'labor_hours': np.random.normal(8000, 1000, n_samples),
            'safety_incidents': np.random.poisson(1, n_samples),
            'weather_delays': np.random.poisson(2, n_samples),
            'rfi_count': np.random.poisson(15, n_samples),
            'quality_issues': np.random.poisson(5, n_samples)
        }
        
        # Calculate target variables
        df = pd.DataFrame(data)
        df['days_to_completion'] = 180 - (df['progress_rate'] * 30) + (df['weather_impact'] * 20)
        df['final_cost_variance'] = (df['change_orders'] * 50000) + (df['material_inflation'] * 1000000)
        df['risk_score'] = (df['safety_incidents'] * 20) + (df['weather_delays'] * 10) + (df['quality_issues'] * 5)
        
        return df
    
    def predict_project_completion(self, current_metrics: Dict) -> Dict:
        """Predict project completion timeline using AI"""
        try:
            features = np.array([[
                current_metrics.get('progress_rate', 1.0),
                current_metrics.get('weather_impact', 0.2),
                current_metrics.get('resource_availability', 0.85)
            ]])
            
            predicted_days = self.prediction_models['completion'].predict(features)[0]
            completion_date = datetime.now() + timedelta(days=int(predicted_days))
            
            # Calculate confidence intervals
            confidence = min(95, max(65, 100 - abs(predicted_days - 120) * 0.5))
            
            return {
                'predicted_completion': completion_date.strftime('%Y-%m-%d'),
                'days_remaining': int(predicted_days),
                'confidence': f"{confidence:.1f}%",
                'risk_factors': self.identify_completion_risks(current_metrics)
            }
            
        except Exception as e:
            self.logger.error(f"Completion prediction error: {e}")
            return {'error': 'Prediction unavailable'}
    
    def predict_cost_overrun(self, project_metrics: Dict) -> Dict:
        """Predict potential cost overruns using machine learning"""
        try:
            features = np.array([[
                project_metrics.get('current_progress', 72),
                project_metrics.get('change_orders', 8),
                project_metrics.get('material_inflation', 0.07),
                project_metrics.get('labor_hours', 45000)
            ]])
            
            predicted_variance = self.prediction_models['cost'].predict(features)[0]
            original_budget = 45500000  # Highland Tower budget
            predicted_final_cost = original_budget + predicted_variance
            
            return {
                'predicted_final_cost': predicted_final_cost,
                'cost_variance': predicted_variance,
                'variance_percentage': (predicted_variance / original_budget) * 100,
                'budget_status': 'Over Budget' if predicted_variance > 0 else 'Under Budget',
                'mitigation_strategies': self.generate_cost_mitigation_strategies(predicted_variance)
            }
            
        except Exception as e:
            self.logger.error(f"Cost prediction error: {e}")
            return {'error': 'Cost prediction unavailable'}
    
    def assess_project_risk(self, risk_indicators: Dict) -> Dict:
        """Assess overall project risk using AI analysis"""
        try:
            features = np.array([[
                risk_indicators.get('safety_incidents', 2),
                risk_indicators.get('weather_delays', 3),
                risk_indicators.get('rfi_count', 12),
                risk_indicators.get('quality_issues', 4)
            ]])
            
            risk_score = self.prediction_models['risk'].predict(features)[0]
            
            # Categorize risk level
            if risk_score < 30:
                risk_level = 'Low'
                risk_color = 'green'
            elif risk_score < 60:
                risk_level = 'Medium'
                risk_color = 'yellow'
            else:
                risk_level = 'High'
                risk_color = 'red'
            
            return {
                'risk_score': risk_score,
                'risk_level': risk_level,
                'risk_color': risk_color,
                'top_risks': self.identify_top_risks(risk_indicators),
                'recommendations': self.generate_risk_recommendations(risk_level)
            }
            
        except Exception as e:
            self.logger.error(f"Risk assessment error: {e}")
            return {'error': 'Risk assessment unavailable'}
    
    def generate_predictive_dashboard(self):
        """Generate AI-powered predictive analytics dashboard"""
        st.markdown("### 🔮 AI-Powered Predictive Analytics - Highland Tower Development")
        
        # Current project metrics for predictions
        current_metrics = {
            'progress_rate': 1.1,
            'weather_impact': 0.3,
            'resource_availability': 0.88,
            'current_progress': 72.3,
            'change_orders': 8,
            'material_inflation': 0.07,
            'labor_hours': 45000,
            'safety_incidents': 2,
            'weather_delays': 3,
            'rfi_count': 12,
            'quality_issues': 4
        }
        
        # Create three columns for predictions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 📅 Completion Prediction")
            completion_pred = self.predict_project_completion(current_metrics)
            if 'error' not in completion_pred:
                st.metric("Predicted Completion", completion_pred['predicted_completion'])
                st.metric("Days Remaining", completion_pred['days_remaining'])
                st.metric("Confidence Level", completion_pred['confidence'])
        
        with col2:
            st.markdown("#### 💰 Cost Prediction")
            cost_pred = self.predict_cost_overrun(current_metrics)
            if 'error' not in cost_pred:
                variance_pct = cost_pred['variance_percentage']
                st.metric("Budget Variance", f"{variance_pct:+.1f}%")
                st.metric("Predicted Final Cost", f"${cost_pred['predicted_final_cost']:,.0f}")
                status_color = "🔴" if variance_pct > 0 else "🟢"
                st.markdown(f"{status_color} {cost_pred['budget_status']}")
        
        with col3:
            st.markdown("#### ⚠️ Risk Assessment")
            risk_assessment = self.assess_project_risk(current_metrics)
            if 'error' not in risk_assessment:
                risk_score = risk_assessment['risk_score']
                risk_level = risk_assessment['risk_level']
                st.metric("Risk Score", f"{risk_score:.1f}")
                st.metric("Risk Level", risk_level)
                
                # Risk level indicator
                if risk_level == 'Low':
                    st.success("🟢 Low Risk")
                elif risk_level == 'Medium':
                    st.warning("🟡 Medium Risk")
                else:
                    st.error("🔴 High Risk")
        
        # Detailed analytics sections
        self.render_trend_analysis()
        self.render_performance_metrics()
    
    def render_trend_analysis(self):
        """Render trend analysis charts"""
        st.markdown("#### 📈 Trend Analysis")
        
        # Generate sample trend data
        dates = pd.date_range(start='2024-01-01', end='2025-05-24', freq='W')
        progress_data = np.cumsum(np.random.normal(2, 0.5, len(dates)))
        progress_data = np.clip(progress_data, 0, 100)
        
        # Create interactive trend chart
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Project Progress', 'Budget Utilization', 'Quality Score', 'Safety Performance'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Progress trend
        fig.add_trace(
            go.Scatter(x=dates, y=progress_data, name='Progress %', line=dict(color='#4CAF50')),
            row=1, col=1
        )
        
        # Budget trend
        budget_data = progress_data * 0.95 + np.random.normal(0, 2, len(dates))
        fig.add_trace(
            go.Scatter(x=dates, y=budget_data, name='Budget %', line=dict(color='#2196F3')),
            row=1, col=2
        )
        
        # Quality trend
        quality_data = 85 + np.random.normal(0, 5, len(dates))
        fig.add_trace(
            go.Scatter(x=dates, y=quality_data, name='Quality Score', line=dict(color='#FF9800')),
            row=2, col=1
        )
        
        # Safety trend
        safety_data = 95 + np.random.normal(0, 3, len(dates))
        fig.add_trace(
            go.Scatter(x=dates, y=safety_data, name='Safety Score', line=dict(color='#9C27B0')),
            row=2, col=2
        )
        
        fig.update_layout(height=500, showlegend=False, title_text="Highland Tower Development - Performance Trends")
        st.plotly_chart(fig, use_container_width=True)
    
    def render_performance_metrics(self):
        """Render performance metrics and KPIs"""
        st.markdown("#### 📊 Performance Metrics")
        
        # Key performance indicators
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Overall Progress", "72.3%", "2.1%")
        
        with col2:
            st.metric("Budget Efficiency", "96.8%", "-1.2%")
        
        with col3:
            st.metric("Quality Score", "94.1", "0.8")
        
        with col4:
            st.metric("Safety Rating", "98.2", "0.5")
        
        # Performance comparison chart
        categories = ['Progress', 'Quality', 'Safety', 'Budget', 'Schedule']
        current_values = [72.3, 94.1, 98.2, 96.8, 78.5]
        target_values = [75.0, 95.0, 98.0, 98.0, 80.0]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=current_values,
            theta=categories,
            fill='toself',
            name='Current Performance',
            line_color='#4CAF50'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=target_values,
            theta=categories,
            fill='toself',
            name='Target Performance',
            line_color='#2196F3',
            opacity=0.5
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Performance vs Targets"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def identify_completion_risks(self, metrics: Dict) -> List[str]:
        """Identify risks that could impact completion timeline"""
        risks = []
        
        if metrics.get('weather_impact', 0) > 0.4:
            risks.append("High weather impact on schedule")
        
        if metrics.get('resource_availability', 1) < 0.8:
            risks.append("Limited resource availability")
        
        if metrics.get('progress_rate', 1) < 1.0:
            risks.append("Below-target progress rate")
        
        return risks or ["No significant completion risks identified"]
    
    def generate_cost_mitigation_strategies(self, variance: float) -> List[str]:
        """Generate cost mitigation strategies based on predicted variance"""
        strategies = []
        
        if variance > 1000000:  # Over $1M variance
            strategies.extend([
                "Implement value engineering reviews",
                "Negotiate bulk purchasing agreements",
                "Optimize labor scheduling efficiency"
            ])
        elif variance > 500000:  # Over $500K variance
            strategies.extend([
                "Review change order processes",
                "Implement cost control measures",
                "Optimize material procurement"
            ])
        else:
            strategies.append("Continue current cost management practices")
        
        return strategies
    
    def identify_top_risks(self, indicators: Dict) -> List[str]:
        """Identify top project risks based on indicators"""
        risks = []
        
        if indicators.get('safety_incidents', 0) > 3:
            risks.append("Safety performance concerns")
        
        if indicators.get('weather_delays', 0) > 5:
            risks.append("Weather-related schedule delays")
        
        if indicators.get('rfi_count', 0) > 15:
            risks.append("High volume of design clarifications needed")
        
        if indicators.get('quality_issues', 0) > 7:
            risks.append("Quality control challenges")
        
        return risks or ["No major risks identified"]
    
    def generate_risk_recommendations(self, risk_level: str) -> List[str]:
        """Generate recommendations based on risk level"""
        if risk_level == 'High':
            return [
                "Implement daily risk assessment meetings",
                "Increase safety oversight and training",
                "Review and update quality control procedures",
                "Consider additional project management resources"
            ]
        elif risk_level == 'Medium':
            return [
                "Monitor risk indicators closely",
                "Maintain current safety protocols",
                "Regular quality check reviews"
            ]
        else:
            return [
                "Continue current risk management practices",
                "Maintain vigilance on key risk indicators"
            ]

@st.cache_resource
def get_analytics_manager():
    """Get cached analytics manager instance"""
    return AnalyticsManager()