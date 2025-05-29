"""
Highland Tower Development - Performance Snapshot Backend
Executive-grade performance monitoring with real-time project health indicators.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class HealthStatus(Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    WARNING = "Warning"
    CRITICAL = "Critical"

class TrendDirection(Enum):
    IMPROVING = "Improving"
    STABLE = "Stable"
    DECLINING = "Declining"

@dataclass
class PerformanceMetric:
    """Executive performance metric"""
    metric_id: str
    metric_name: str
    current_value: float
    target_value: float
    unit: str
    status: HealthStatus
    trend: TrendDirection
    variance_percentage: float
    last_updated: str
    category: str
    description: str

@dataclass
class ProjectAlert:
    """Critical project alert"""
    alert_id: str
    alert_type: str  # "Budget", "Schedule", "Safety", "Quality", "Resource"
    severity: str  # "Low", "Medium", "High", "Critical"
    title: str
    description: str
    impact: str
    recommended_action: str
    responsible_party: str
    due_date: str
    status: str  # "Open", "In Progress", "Resolved"
    created_date: str
    resolved_date: Optional[str]

@dataclass
class ExecutiveSummary:
    """Executive project summary"""
    summary_id: str
    report_date: str
    project_phase: str
    overall_health: HealthStatus
    
    # Key metrics
    schedule_performance: float
    cost_performance: float
    quality_score: float
    safety_rating: float
    
    # Financial summary
    total_budget: float
    spent_to_date: float
    remaining_budget: float
    projected_final_cost: float
    
    # Schedule summary
    percent_complete: float
    days_ahead_behind: int
    critical_path_status: str
    
    # Key accomplishments
    accomplishments: List[str]
    upcoming_milestones: List[Dict[str, str]]
    
    # Issues and risks
    open_issues: int
    high_priority_risks: int
    
    # Resource status
    current_workforce: int
    equipment_utilization: float
    
    # Notes
    executive_notes: str
    created_by: str
    created_at: str

class PerformanceSnapshotManager:
    """Executive performance monitoring system"""
    
    def __init__(self):
        self.metrics: Dict[str, PerformanceMetric] = {}
        self.alerts: Dict[str, ProjectAlert] = {}
        self.summaries: Dict[str, ExecutiveSummary] = {}
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample performance data"""
        
        # Sample Performance Metrics
        sample_metrics = [
            PerformanceMetric(
                metric_id="pm-001",
                metric_name="Schedule Performance Index",
                current_value=1.05,
                target_value=1.00,
                unit="SPI",
                status=HealthStatus.EXCELLENT,
                trend=TrendDirection.IMPROVING,
                variance_percentage=5.0,
                last_updated="2025-05-28",
                category="Schedule",
                description="Schedule efficiency ratio - currently ahead of schedule"
            ),
            PerformanceMetric(
                metric_id="pm-002",
                metric_name="Cost Performance Index",
                current_value=1.02,
                target_value=1.00,
                unit="CPI",
                status=HealthStatus.GOOD,
                trend=TrendDirection.STABLE,
                variance_percentage=2.0,
                last_updated="2025-05-28",
                category="Cost",
                description="Cost efficiency ratio - slightly under budget"
            ),
            PerformanceMetric(
                metric_id="pm-003",
                metric_name="Overall Project Progress",
                current_value=78.5,
                target_value=75.0,
                unit="%",
                status=HealthStatus.EXCELLENT,
                trend=TrendDirection.IMPROVING,
                variance_percentage=4.7,
                last_updated="2025-05-28",
                category="Progress",
                description="Total project completion percentage"
            ),
            PerformanceMetric(
                metric_id="pm-004",
                metric_name="Safety Performance Rating",
                current_value=97.2,
                target_value=95.0,
                unit="%",
                status=HealthStatus.EXCELLENT,
                trend=TrendDirection.IMPROVING,
                variance_percentage=2.3,
                last_updated="2025-05-27",
                category="Safety",
                description="Composite safety score including incidents and compliance"
            ),
            PerformanceMetric(
                metric_id="pm-005",
                metric_name="Quality Control Score",
                current_value=94.2,
                target_value=90.0,
                unit="%",
                status=HealthStatus.EXCELLENT,
                trend=TrendDirection.STABLE,
                variance_percentage=4.7,
                last_updated="2025-05-28",
                category="Quality",
                description="Overall quality inspection pass rate"
            ),
            PerformanceMetric(
                metric_id="pm-006",
                metric_name="Budget Utilization",
                current_value=68.2,
                target_value=75.0,
                unit="%",
                status=HealthStatus.GOOD,
                trend=TrendDirection.STABLE,
                variance_percentage=-9.1,
                last_updated="2025-05-28",
                category="Financial",
                description="Percentage of total budget utilized to date"
            )
        ]
        
        for metric in sample_metrics:
            self.metrics[metric.metric_id] = metric
        
        # Sample Project Alerts
        sample_alerts = [
            ProjectAlert(
                alert_id="alert-001",
                alert_type="Schedule",
                severity="Medium",
                title="MEP Coordination Delay Risk",
                description="HVAC rough-in schedule may conflict with electrical installation on Level 12-13",
                impact="Potential 3-5 day delay if not resolved by June 1st",
                recommended_action="Coordinate MEP schedule meeting with all trades by May 30th",
                responsible_party="Tom Brown - MEP Manager",
                due_date="2025-05-30",
                status="In Progress",
                created_date="2025-05-25",
                resolved_date=None
            ),
            ProjectAlert(
                alert_id="alert-002",
                alert_type="Budget",
                severity="Low",
                title="Steel Material Cost Variance",
                description="Structural steel costs trending 2% above budgeted amounts",
                impact="Potential $57K over budget if trend continues",
                recommended_action="Review steel procurement strategy and negotiate bulk pricing",
                responsible_party="Cost Management Team",
                due_date="2025-06-15",
                status="Open",
                created_date="2025-05-22",
                resolved_date=None
            ),
            ProjectAlert(
                alert_id="alert-003",
                alert_type="Safety",
                severity="High",
                title="Fall Protection Equipment Expiration",
                description="12 fall protection harnesses expire next month, affecting high-rise work",
                impact="Work stoppage risk if not replaced by June 15th",
                recommended_action="Order replacement equipment immediately and schedule recertification",
                responsible_party="Sarah Wilson - Safety Manager",
                due_date="2025-06-10",
                status="In Progress",
                created_date="2025-05-20",
                resolved_date=None
            )
        ]
        
        for alert in sample_alerts:
            self.alerts[alert.alert_id] = alert
        
        # Sample Executive Summary
        sample_summary = ExecutiveSummary(
            summary_id="exec-001",
            report_date="2025-05-28",
            project_phase="Core & Shell Construction",
            overall_health=HealthStatus.EXCELLENT,
            schedule_performance=1.05,
            cost_performance=1.02,
            quality_score=94.2,
            safety_rating=97.2,
            total_budget=45500000.0,
            spent_to_date=31025000.0,
            remaining_budget=14475000.0,
            projected_final_cost=44800000.0,
            percent_complete=78.5,
            days_ahead_behind=8,  # 8 days ahead
            critical_path_status="On Track",
            accomplishments=[
                "Level 15 structural steel installation completed ahead of schedule",
                "Penthouse architectural plans approved by city planning",
                "Zero safety incidents recorded this month",
                "Quality control scores exceed 90% target consistently"
            ],
            upcoming_milestones=[
                {"milestone": "MEP Rough-in Levels 12-15", "date": "2025-06-15", "status": "On Track"},
                {"milestone": "Elevator Installation Begin", "date": "2025-07-01", "status": "On Track"},
                {"milestone": "Exterior Envelope 50% Complete", "date": "2025-07-30", "status": "Ahead"},
                {"milestone": "Interior Finishes Begin", "date": "2025-08-15", "status": "On Track"}
            ],
            open_issues=8,
            high_priority_risks=2,
            current_workforce=127,
            equipment_utilization=89.3,
            executive_notes="Project continues to exceed expectations with strong performance across all metrics. Steel installation ahead of schedule creating opportunities for accelerated MEP installation. Budget performance remains excellent with $700K projected savings.",
            created_by="John Smith - Project Manager",
            created_at="2025-05-28 16:00:00"
        )
        
        self.summaries[sample_summary.summary_id] = sample_summary
    
    def create_performance_metric(self, metric_data: Dict[str, Any]) -> str:
        """Create a new performance metric"""
        metric_id = f"pm-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        # Calculate variance percentage
        if metric_data["target_value"] != 0:
            variance = ((metric_data["current_value"] - metric_data["target_value"]) / metric_data["target_value"]) * 100
        else:
            variance = 0.0
        
        metric_data.update({
            "metric_id": metric_id,
            "variance_percentage": variance,
            "last_updated": datetime.now().strftime('%Y-%m-%d')
        })
        
        # Convert enums
        metric_data["status"] = HealthStatus(metric_data["status"])
        metric_data["trend"] = TrendDirection(metric_data["trend"])
        
        metric = PerformanceMetric(**metric_data)
        self.metrics[metric_id] = metric
        
        return metric_id
    
    def create_alert(self, alert_data: Dict[str, Any]) -> str:
        """Create a new project alert"""
        alert_id = f"alert-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        alert_data.update({
            "alert_id": alert_id,
            "status": "Open",
            "created_date": datetime.now().strftime('%Y-%m-%d'),
            "resolved_date": None
        })
        
        alert = ProjectAlert(**alert_data)
        self.alerts[alert_id] = alert
        
        return alert_id
    
    def create_executive_summary(self, summary_data: Dict[str, Any]) -> str:
        """Create a new executive summary"""
        summary_id = f"exec-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        summary_data.update({
            "summary_id": summary_id,
            "report_date": datetime.now().strftime('%Y-%m-%d'),
            "created_at": datetime.now().isoformat()
        })
        
        # Convert enum
        summary_data["overall_health"] = HealthStatus(summary_data["overall_health"])
        
        summary = ExecutiveSummary(**summary_data)
        self.summaries[summary_id] = summary
        
        return summary_id
    
    def get_performance_metrics(self) -> List[PerformanceMetric]:
        """Get all performance metrics"""
        return list(self.metrics.values())
    
    def get_metrics_by_category(self, category: str) -> List[PerformanceMetric]:
        """Get metrics by category"""
        return [metric for metric in self.metrics.values() if metric.category == category]
    
    def get_critical_metrics(self) -> List[PerformanceMetric]:
        """Get metrics with critical status"""
        return [metric for metric in self.metrics.values() if metric.status == HealthStatus.CRITICAL]
    
    def get_active_alerts(self) -> List[ProjectAlert]:
        """Get all active (non-resolved) alerts"""
        return [alert for alert in self.alerts.values() if alert.status != "Resolved"]
    
    def get_high_priority_alerts(self) -> List[ProjectAlert]:
        """Get high priority alerts"""
        return [alert for alert in self.alerts.values() 
                if alert.severity in ["High", "Critical"] and alert.status != "Resolved"]
    
    def get_latest_summary(self) -> Optional[ExecutiveSummary]:
        """Get the most recent executive summary"""
        if not self.summaries:
            return None
        return max(self.summaries.values(), key=lambda s: s.report_date)
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Mark an alert as resolved"""
        alert = self.alerts.get(alert_id)
        if not alert:
            return False
        
        alert.status = "Resolved"
        alert.resolved_date = datetime.now().strftime('%Y-%m-%d')
        return True
    
    def update_metric_value(self, metric_id: str, new_value: float) -> bool:
        """Update a performance metric value"""
        metric = self.metrics.get(metric_id)
        if not metric:
            return False
        
        old_value = metric.current_value
        metric.current_value = new_value
        metric.last_updated = datetime.now().strftime('%Y-%m-%d')
        
        # Recalculate variance
        if metric.target_value != 0:
            metric.variance_percentage = ((new_value - metric.target_value) / metric.target_value) * 100
        
        # Update trend
        if new_value > old_value:
            metric.trend = TrendDirection.IMPROVING
        elif new_value < old_value:
            metric.trend = TrendDirection.DECLINING
        else:
            metric.trend = TrendDirection.STABLE
        
        # Update status based on variance
        abs_variance = abs(metric.variance_percentage)
        if abs_variance <= 5:
            metric.status = HealthStatus.EXCELLENT if new_value >= metric.target_value else HealthStatus.GOOD
        elif abs_variance <= 15:
            metric.status = HealthStatus.WARNING
        else:
            metric.status = HealthStatus.CRITICAL
        
        return True
    
    def calculate_overall_project_health(self) -> HealthStatus:
        """Calculate overall project health based on all metrics"""
        if not self.metrics:
            return HealthStatus.GOOD
        
        metrics = list(self.metrics.values())
        critical_count = len([m for m in metrics if m.status == HealthStatus.CRITICAL])
        warning_count = len([m for m in metrics if m.status == HealthStatus.WARNING])
        excellent_count = len([m for m in metrics if m.status == HealthStatus.EXCELLENT])
        
        total_metrics = len(metrics)
        
        if critical_count > 0:
            return HealthStatus.CRITICAL
        elif warning_count > total_metrics * 0.3:  # More than 30% in warning
            return HealthStatus.WARNING
        elif excellent_count >= total_metrics * 0.7:  # 70% or more excellent
            return HealthStatus.EXCELLENT
        else:
            return HealthStatus.GOOD
    
    def generate_performance_metrics(self) -> Dict[str, Any]:
        """Generate performance dashboard metrics"""
        metrics = list(self.metrics.values())
        alerts = list(self.alerts.values())
        active_alerts = self.get_active_alerts()
        
        if not metrics and not alerts:
            return {}
        
        # Metric status counts
        status_counts = {}
        for status in HealthStatus:
            status_counts[status.value] = len([m for m in metrics if m.status == status])
        
        # Category performance
        categories = list(set(m.category for m in metrics))
        category_performance = {}
        for category in categories:
            cat_metrics = self.get_metrics_by_category(category)
            if cat_metrics:
                avg_performance = sum(m.current_value for m in cat_metrics) / len(cat_metrics)
                category_performance[category] = round(avg_performance, 1)
        
        # Alert analysis
        alert_severity_counts = {}
        severities = ["Low", "Medium", "High", "Critical"]
        for severity in severities:
            alert_severity_counts[severity] = len([a for a in active_alerts if a.severity == severity])
        
        # Trend analysis
        improving_metrics = len([m for m in metrics if m.trend == TrendDirection.IMPROVING])
        declining_metrics = len([m for m in metrics if m.trend == TrendDirection.DECLINING])
        
        return {
            "total_metrics": len(metrics),
            "total_alerts": len(alerts),
            "active_alerts": len(active_alerts),
            "metric_status_breakdown": status_counts,
            "category_performance": category_performance,
            "alert_severity_breakdown": alert_severity_counts,
            "overall_health": self.calculate_overall_project_health().value,
            "improving_metrics": improving_metrics,
            "declining_metrics": declining_metrics,
            "critical_metrics": status_counts.get("Critical", 0),
            "high_priority_alerts": len(self.get_high_priority_alerts())
        }

# Global instance for use across the application
performance_manager = PerformanceSnapshotManager()