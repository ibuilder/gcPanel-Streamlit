"""
Highland Tower Development - Charts & Analytics Backend
Enterprise-grade chart generation with proper data handling and visualization.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional

class HighlandChartsManager:
    """Professional chart generation for Highland Tower Development"""
    
    def __init__(self):
        self.highland_theme = {
            'primary_blue': '#1e3c72',
            'highland_blue': '#2a5298', 
            'success_green': '#059669',
            'warning_orange': '#d97706',
            'danger_red': '#dc2626',
            'neutral_gray': '#64748b'
        }
    
    def create_cost_progress_chart(self) -> go.Figure:
        """Create Highland Tower cost vs progress chart"""
        # Highland Tower Development actual data
        data = {
            'Phase': ['Foundation', 'Structure', 'MEP Systems', 'Facade', 'Interiors'],
            'Budget_M': [8.5, 18.2, 12.8, 4.7, 1.3],
            'Spent_M': [8.5, 17.1, 9.8, 2.1, 0.2],
            'Progress_Pct': [100, 94, 76, 45, 15]
        }
        
        df = pd.DataFrame(data)
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Budget vs Spent ($M)', 'Phase Progress (%)'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Budget vs Spent
        fig.add_trace(
            go.Bar(x=df['Phase'], y=df['Budget_M'], name='Budget', 
                  marker_color=self.highland_theme['highland_blue']),
            row=1, col=1
        )
        fig.add_trace(
            go.Bar(x=df['Phase'], y=df['Spent_M'], name='Spent',
                  marker_color=self.highland_theme['success_green']),
            row=1, col=1
        )
        
        # Progress
        fig.add_trace(
            go.Bar(x=df['Phase'], y=df['Progress_Pct'], name='Progress',
                  marker_color=self.highland_theme['primary_blue']),
            row=1, col=2
        )
        
        fig.update_layout(
            title="Highland Tower Development - Cost & Progress Analysis",
            height=500,
            showlegend=True,
            plot_bgcolor='white'
        )
        
        return fig
    
    def create_schedule_gantt(self) -> go.Figure:
        """Create Highland Tower project schedule Gantt chart"""
        # Highland Tower Development schedule data
        tasks = [
            {'Task': 'Site Preparation', 'Start': '2024-01-15', 'End': '2024-03-01', 'Phase': 'Foundation', 'Progress': 100},
            {'Task': 'Foundation Work', 'Start': '2024-02-15', 'End': '2024-05-15', 'Phase': 'Foundation', 'Progress': 100},
            {'Task': 'Structural Frame L1-5', 'Start': '2024-04-01', 'End': '2024-07-15', 'Phase': 'Structure', 'Progress': 100},
            {'Task': 'Structural Frame L6-10', 'Start': '2024-06-01', 'End': '2024-09-15', 'Phase': 'Structure', 'Progress': 100},
            {'Task': 'Structural Frame L11-15', 'Start': '2024-08-01', 'End': '2024-11-15', 'Phase': 'Structure', 'Progress': 95},
            {'Task': 'MEP Rough-in L1-8', 'Start': '2024-09-01', 'End': '2024-12-15', 'Phase': 'MEP', 'Progress': 85},
            {'Task': 'MEP Rough-in L9-15', 'Start': '2024-11-01', 'End': '2025-02-15', 'Phase': 'MEP', 'Progress': 60},
            {'Task': 'Facade Installation', 'Start': '2024-12-01', 'End': '2025-04-15', 'Phase': 'Facade', 'Progress': 40},
            {'Task': 'Interior Finishes', 'Start': '2025-02-01', 'End': '2025-07-15', 'Phase': 'Interiors', 'Progress': 15}
        ]
        
        df = pd.DataFrame(tasks)
        df['Start'] = pd.to_datetime(df['Start'])
        df['End'] = pd.to_datetime(df['End'])
        
        # Color mapping for phases
        color_map = {
            'Foundation': self.highland_theme['neutral_gray'],
            'Structure': self.highland_theme['primary_blue'],
            'MEP': self.highland_theme['highland_blue'],
            'Facade': self.highland_theme['success_green'],
            'Interiors': self.highland_theme['warning_orange']
        }
        
        fig = px.timeline(
            df, x_start="Start", x_end="End", y="Task", 
            color="Phase", 
            title="Highland Tower Development - Master Schedule",
            color_discrete_map=color_map
        )
        
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(
            height=600,
            xaxis_title="Timeline",
            yaxis_title="Project Tasks"
        )
        
        return fig
    
    def create_safety_dashboard(self) -> go.Figure:
        """Create Highland Tower safety metrics dashboard"""
        # Highland Tower safety data
        safety_metrics = {
            'days_without_incident': 45,
            'total_incidents_ytd': 2,
            'safety_score': 4.8,
            'inspections_passed': 28,
            'inspections_total': 30
        }
        
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=('Days Without Incident', 'Safety Score', 'Inspection Pass Rate',
                          'YTD Incidents', 'Safety Training', 'PPE Compliance'),
            specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "bar"}, {"type": "pie"}, {"type": "bar"}]]
        )
        
        # Days without incident
        fig.add_trace(go.Indicator(
            mode="number",
            value=safety_metrics['days_without_incident'],
            title={"text": "Days"},
            number={'font': {'size': 40, 'color': self.highland_theme['success_green']}},
        ), row=1, col=1)
        
        # Safety score
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=safety_metrics['safety_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "out of 5.0"},
            gauge={
                'axis': {'range': [None, 5]},
                'bar': {'color': self.highland_theme['success_green']},
                'steps': [
                    {'range': [0, 2.5], 'color': "lightgray"},
                    {'range': [2.5, 4], 'color': "gray"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 4.5}
            }
        ), row=1, col=2)
        
        # Inspection pass rate
        pass_rate = (safety_metrics['inspections_passed'] / safety_metrics['inspections_total']) * 100
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=pass_rate,
            number={'suffix': "%"},
            delta={'reference': 95, 'relative': True},
            title={"text": "Pass Rate"},
        ), row=1, col=3)
        
        fig.update_layout(
            title="Highland Tower Development - Safety Dashboard",
            height=700
        )
        
        return fig
    
    def create_rfi_analytics(self, rfi_data: List[Dict]) -> go.Figure:
        """Create RFI analytics charts"""
        if not rfi_data:
            # Highland Tower sample data
            rfi_data = [
                {'status': 'Open', 'count': 8},
                {'status': 'Under Review', 'count': 12},
                {'status': 'Closed', 'count': 23},
                {'status': 'Pending', 'count': 3}
            ]
        
        df = pd.DataFrame(rfi_data)
        
        # Create pie chart for RFI status distribution
        fig = go.Figure(data=[go.Pie(
            labels=df['status'],
            values=df['count'],
            hole=0.4,
            marker_colors=[
                self.highland_theme['danger_red'],     # Open
                self.highland_theme['warning_orange'], # Under Review
                self.highland_theme['success_green'],  # Closed
                self.highland_theme['highland_blue']   # Pending
            ]
        )])
        
        fig.update_layout(
            title="Highland Tower Development - RFI Status Distribution",
            annotations=[dict(text='46 Total<br>RFIs', x=0.5, y=0.5, font_size=16, showarrow=False)]
        )
        
        return fig
    
    def create_cost_breakdown_pie(self, cost_data: Optional[Dict] = None) -> go.Figure:
        """Create Highland Tower cost breakdown pie chart"""
        if not cost_data:
            # Highland Tower actual cost breakdown
            cost_data = {
                'Labor': 18.2,
                'Materials': 15.4,
                'Equipment': 7.8,
                'Subcontractors': 4.1
            }
        
        fig = go.Figure(data=[go.Pie(
            labels=list(cost_data.keys()),
            values=list(cost_data.values()),
            hole=0.3,
            marker_colors=[
                self.highland_theme['primary_blue'],
                self.highland_theme['highland_blue'],
                self.highland_theme['success_green'],
                self.highland_theme['warning_orange']
            ]
        )])
        
        total_cost = sum(cost_data.values())
        fig.update_layout(
            title="Highland Tower Development - Cost Breakdown",
            annotations=[dict(text=f'${total_cost:.1f}M<br>Total', x=0.5, y=0.5, font_size=16, showarrow=False)]
        )
        
        return fig
    
    def create_progress_timeline(self) -> go.Figure:
        """Create Highland Tower progress timeline"""
        # Highland Tower monthly progress data
        months = ['Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024', 'May 2024', 
                 'Jun 2024', 'Jul 2024', 'Aug 2024', 'Sep 2024', 'Oct 2024',
                 'Nov 2024', 'Dec 2024', 'Jan 2025', 'Feb 2025', 'Mar 2025',
                 'Apr 2025', 'May 2025']
        
        planned_progress = [5, 12, 18, 25, 32, 40, 48, 55, 62, 68, 74, 79, 83, 87, 90, 93, 95]
        actual_progress = [4, 11, 17, 24, 31, 39, 47, 54, 61, 67, 73, 78, 82, 86, 89, 91, 92]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=months, y=planned_progress,
            mode='lines+markers',
            name='Planned Progress',
            line=dict(color=self.highland_theme['highland_blue'], width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=months, y=actual_progress,
            mode='lines+markers',
            name='Actual Progress',
            line=dict(color=self.highland_theme['success_green'], width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Highland Tower Development - Progress Timeline",
            xaxis_title="Timeline",
            yaxis_title="Progress (%)",
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    def create_quality_metrics(self) -> go.Figure:
        """Create Highland Tower quality metrics dashboard"""
        # Highland Tower quality data
        quality_data = {
            'Inspections Passed': 28,
            'Defects Found': 12,
            'Defects Resolved': 9,
            'Quality Score': 4.7
        }
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=list(quality_data.keys()),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # Add indicators
        fig.add_trace(go.Indicator(
            mode="number",
            value=quality_data['Inspections Passed'],
            title={"text": "This Month"},
            number={'font': {'color': self.highland_theme['success_green']}}
        ), row=1, col=1)
        
        fig.add_trace(go.Indicator(
            mode="number",
            value=quality_data['Defects Found'],
            title={"text": "Total Open"},
            number={'font': {'color': self.highland_theme['warning_orange']}}
        ), row=1, col=2)
        
        fig.add_trace(go.Indicator(
            mode="number",
            value=quality_data['Defects Resolved'],
            title={"text": "Resolved"},
            number={'font': {'color': self.highland_theme['success_green']}}
        ), row=2, col=1)
        
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=quality_data['Quality Score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "out of 5.0"},
            gauge={'axis': {'range': [None, 5]},
                   'bar': {'color': self.highland_theme['success_green']}}
        ), row=2, col=2)
        
        fig.update_layout(
            title="Highland Tower Development - Quality Metrics",
            height=600
        )
        
        return fig

# Global instance
highland_charts = HighlandChartsManager()