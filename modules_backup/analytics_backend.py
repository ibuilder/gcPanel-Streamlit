"""
Highland Tower Development - Analytics Backend
Enterprise-grade analytics and reporting with executive dashboards and KPI tracking.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class ReportType(Enum):
    EXECUTIVE_SUMMARY = "Executive Summary"
    PROJECT_PERFORMANCE = "Project Performance"
    COST_ANALYSIS = "Cost Analysis"
    SAFETY_METRICS = "Safety Metrics"
    SCHEDULE_ANALYSIS = "Schedule Analysis"
    QUALITY_REPORT = "Quality Report"
    FINANCIAL_DASHBOARD = "Financial Dashboard"
    CUSTOM_REPORT = "Custom Report"

class ReportFrequency(Enum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"
    ANNUAL = "Annual"
    ON_DEMAND = "On Demand"

class MetricStatus(Enum):
    ON_TARGET = "On Target"
    AT_RISK = "At Risk"
    CRITICAL = "Critical"
    EXCEEDING = "Exceeding"

@dataclass
class KPIMetric:
    """Key Performance Indicator metric"""
    metric_id: str
    metric_name: str
    category: str
    current_value: float
    target_value: float
    unit: str
    status: MetricStatus
    trend: str  # "Improving", "Declining", "Stable"
    last_updated: str
    description: str

@dataclass
class Report:
    """Analytics report record"""
    report_id: str
    report_code: str
    title: str
    description: str
    report_type: ReportType
    frequency: ReportFrequency
    
    # Content and data
    data_sources: List[str]
    metrics_included: List[str]
    charts_included: List[str]
    
    # Generation details
    generated_date: str
    report_period_start: str
    report_period_end: str
    
    # Access and distribution
    created_by: str
    distribution_list: List[str]
    access_level: str
    
    # File information
    file_path: Optional[str]
    file_format: str  # "PDF", "Excel", "PowerBI", "Dashboard"
    file_size: int
    
    # Status and workflow
    status: str  # "Generated", "Scheduled", "Failed", "In Progress"
    automated: bool
    next_generation: Optional[str]
    
    # Notes and tracking
    notes: str
    parameters: Dict[str, Any]
    
    # Workflow
    created_at: str
    updated_at: str

@dataclass
class Dashboard:
    """Executive dashboard configuration"""
    dashboard_id: str
    dashboard_name: str
    description: str
    dashboard_type: str  # "Executive", "Project Manager", "Field Operations", "Financial"
    
    # Layout and widgets
    widgets: List[Dict[str, Any]]
    layout_config: Dict[str, Any]
    
    # Data refresh
    refresh_frequency: str
    last_refreshed: str
    auto_refresh: bool
    
    # Access control
    created_by: str
    shared_with: List[str]
    public_access: bool
    
    # Customization
    theme: str
    filters: Dict[str, Any]
    
    # Workflow
    created_at: str
    updated_at: str

class AnalyticsManager:
    """Enterprise analytics and reporting system"""
    
    def __init__(self):
        self.reports: Dict[str, Report] = {}
        self.dashboards: Dict[str, Dashboard] = {}
        self.kpi_metrics: Dict[str, KPIMetric] = {}
        self.next_report_code = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample analytics data"""
        
        # Sample KPI Metrics
        sample_kpis = [
            KPIMetric(
                metric_id="kpi-001",
                metric_name="Project Progress",
                category="Schedule",
                current_value=78.5,
                target_value=75.0,
                unit="%",
                status=MetricStatus.EXCEEDING,
                trend="Improving",
                last_updated="2025-05-28",
                description="Overall project completion percentage"
            ),
            KPIMetric(
                metric_id="kpi-002",
                metric_name="Cost Performance Index",
                category="Cost",
                current_value=1.02,
                target_value=1.00,
                unit="CPI",
                status=MetricStatus.ON_TARGET,
                trend="Stable",
                last_updated="2025-05-28",
                description="Cost efficiency ratio (earned value / actual cost)"
            ),
            KPIMetric(
                metric_id="kpi-003",
                metric_name="Safety Incident Rate",
                category="Safety",
                current_value=0.8,
                target_value=1.0,
                unit="incidents/month",
                status=MetricStatus.EXCEEDING,
                trend="Improving",
                last_updated="2025-05-27",
                description="Monthly safety incident rate per 100 workers"
            ),
            KPIMetric(
                metric_id="kpi-004",
                metric_name="Quality Score",
                category="Quality",
                current_value=94.2,
                target_value=90.0,
                unit="%",
                status=MetricStatus.EXCEEDING,
                trend="Improving",
                last_updated="2025-05-28",
                description="Overall quality inspection pass rate"
            ),
            KPIMetric(
                metric_id="kpi-005",
                metric_name="RFI Response Time",
                category="Communication",
                current_value=2.1,
                target_value=3.0,
                unit="days",
                status=MetricStatus.EXCEEDING,
                trend="Improving",
                last_updated="2025-05-28",
                description="Average time to respond to RFIs"
            )
        ]
        
        for kpi in sample_kpis:
            self.kpi_metrics[kpi.metric_id] = kpi
        
        # Sample Report 1 - Executive Summary
        sample_report_1 = Report(
            report_id="rpt-001",
            report_code="HTD-RPT-001",
            title="Highland Tower Development - Executive Summary May 2025",
            description="Monthly executive summary including project progress, financials, and key metrics",
            report_type=ReportType.EXECUTIVE_SUMMARY,
            frequency=ReportFrequency.MONTHLY,
            data_sources=["Project Schedule", "Cost Management", "Safety Records", "Quality Control"],
            metrics_included=["Project Progress", "Cost Performance", "Safety Metrics", "Quality Scores"],
            charts_included=["Progress Timeline", "Cost Curve", "Safety Trends", "Quality Dashboard"],
            generated_date="2025-05-28",
            report_period_start="2025-05-01",
            report_period_end="2025-05-31",
            created_by="John Smith - Project Manager",
            distribution_list=["Highland Properties LLC", "Executive Team", "Stakeholders"],
            access_level="Executive",
            file_path="/reports/executive/HTD-Executive-May-2025.pdf",
            file_format="PDF",
            file_size=8450000,  # 8.45 MB
            status="Generated",
            automated=True,
            next_generation="2025-06-28",
            notes="Excellent progress this month, project ahead of schedule",
            parameters={"include_photos": True, "detail_level": "summary", "charts": True},
            created_at="2025-05-28 09:00:00",
            updated_at="2025-05-28 09:15:00"
        )
        
        # Sample Report 2 - Cost Analysis
        sample_report_2 = Report(
            report_id="rpt-002",
            report_code="HTD-RPT-002",
            title="Highland Tower Cost Performance Analysis Q2 2025",
            description="Detailed cost analysis including budget variance, cost projections, and financial KPIs",
            report_type=ReportType.COST_ANALYSIS,
            frequency=ReportFrequency.QUARTERLY,
            data_sources=["Cost Management", "Change Orders", "Material Costs", "Labor Hours"],
            metrics_included=["Budget Variance", "Cost Performance Index", "Earned Value", "Forecast"],
            charts_included=["S-Curve", "Cost Breakdown", "Variance Analysis", "Cash Flow"],
            generated_date="2025-05-25",
            report_period_start="2025-04-01",
            report_period_end="2025-06-30",
            created_by="Tom Brown - Cost Manager",
            distribution_list=["Finance Team", "Project Management", "Highland Properties LLC"],
            access_level="Management",
            file_path="/reports/cost/HTD-Cost-Analysis-Q2-2025.xlsx",
            file_format="Excel",
            file_size=12800000,  # 12.8 MB
            status="Generated",
            automated=False,
            next_generation="2025-08-25",
            notes="Project under budget by $285K, excellent cost control",
            parameters={"include_forecasting": True, "breakdown_by_phase": True, "variance_threshold": 5.0},
            created_at="2025-05-25 14:00:00",
            updated_at="2025-05-25 16:30:00"
        )
        
        # Sample Report 3 - Safety Metrics (Scheduled)
        sample_report_3 = Report(
            report_id="rpt-003",
            report_code="HTD-RPT-003",
            title="Highland Tower Safety Performance Dashboard",
            description="Weekly safety metrics including incident rates, near misses, and compliance tracking",
            report_type=ReportType.SAFETY_METRICS,
            frequency=ReportFrequency.WEEKLY,
            data_sources=["Safety Records", "Incident Reports", "Training Records", "Compliance Audits"],
            metrics_included=["Incident Rate", "Near Miss Reports", "Training Compliance", "Safety Score"],
            charts_included=["Safety Trends", "Incident Categories", "Training Status", "Compliance Dashboard"],
            generated_date="2025-05-27",
            report_period_start="2025-05-20",
            report_period_end="2025-05-27",
            created_by="Sarah Wilson - Safety Manager",
            distribution_list=["Safety Team", "Project Management", "Site Supervisors"],
            access_level="Project Team",
            file_path="/reports/safety/HTD-Safety-Week-21-2025.pdf",
            file_format="PDF",
            file_size=3200000,  # 3.2 MB
            status="Generated",
            automated=True,
            next_generation="2025-06-03",
            notes="Zero incidents this week, safety training 100% complete",
            parameters={"include_photos": True, "incident_details": True, "recommendations": True},
            created_at="2025-05-27 17:00:00",
            updated_at="2025-05-27 17:15:00"
        )
        
        self.reports[sample_report_1.report_id] = sample_report_1
        self.reports[sample_report_2.report_id] = sample_report_2
        self.reports[sample_report_3.report_id] = sample_report_3
        
        # Sample Dashboard 1 - Executive Dashboard
        sample_dashboard_1 = Dashboard(
            dashboard_id="dash-001",
            dashboard_name="Highland Tower Executive Dashboard",
            description="Real-time executive overview of project performance and key metrics",
            dashboard_type="Executive",
            widgets=[
                {"type": "kpi_card", "metric": "Project Progress", "position": {"x": 0, "y": 0, "w": 3, "h": 2}},
                {"type": "kpi_card", "metric": "Cost Performance", "position": {"x": 3, "y": 0, "w": 3, "h": 2}},
                {"type": "chart", "chart_type": "line", "data": "progress_timeline", "position": {"x": 0, "y": 2, "w": 6, "h": 4}},
                {"type": "chart", "chart_type": "gauge", "data": "safety_score", "position": {"x": 6, "y": 0, "w": 3, "h": 3}},
                {"type": "table", "data": "active_rfis", "position": {"x": 6, "y": 3, "w": 3, "h": 3}}
            ],
            layout_config={"columns": 12, "row_height": 50, "margin": [10, 10]},
            refresh_frequency="hourly",
            last_refreshed="2025-05-28 14:30:00",
            auto_refresh=True,
            created_by="John Smith - Project Manager",
            shared_with=["Highland Properties LLC", "Executive Team"],
            public_access=False,
            theme="professional",
            filters={"date_range": "last_30_days", "include_forecasts": True},
            created_at="2025-03-01 10:00:00",
            updated_at="2025-05-28 14:30:00"
        )
        
        self.dashboards[sample_dashboard_1.dashboard_id] = sample_dashboard_1
        self.next_report_code = 4
    
    def create_report(self, report_data: Dict[str, Any]) -> str:
        """Create a new analytics report"""
        report_id = f"rpt-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        report_code = f"HTD-RPT-{self.next_report_code:03d}"
        
        report_data.update({
            "report_id": report_id,
            "report_code": report_code,
            "generated_date": datetime.now().strftime('%Y-%m-%d'),
            "status": "In Progress",
            "file_size": 0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        report_data["report_type"] = ReportType(report_data["report_type"])
        report_data["frequency"] = ReportFrequency(report_data["frequency"])
        
        report = Report(**report_data)
        self.reports[report_id] = report
        self.next_report_code += 1
        
        return report_id
    
    def create_kpi_metric(self, kpi_data: Dict[str, Any]) -> str:
        """Create a new KPI metric"""
        metric_id = f"kpi-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        kpi_data.update({
            "metric_id": metric_id,
            "last_updated": datetime.now().strftime('%Y-%m-%d')
        })
        
        # Convert enum
        kpi_data["status"] = MetricStatus(kpi_data["status"])
        
        kpi = KPIMetric(**kpi_data)
        self.kpi_metrics[metric_id] = kpi
        
        return metric_id
    
    def get_report(self, report_id: str) -> Optional[Report]:
        """Get a specific report"""
        return self.reports.get(report_id)
    
    def get_all_reports(self) -> List[Report]:
        """Get all reports sorted by generated date (newest first)"""
        return sorted(self.reports.values(),
                     key=lambda r: r.generated_date, reverse=True)
    
    def get_reports_by_type(self, report_type: ReportType) -> List[Report]:
        """Get reports by type"""
        return [report for report in self.reports.values() if report.report_type == report_type]
    
    def get_kpi_metrics(self) -> List[KPIMetric]:
        """Get all KPI metrics"""
        return list(self.kpi_metrics.values())
    
    def get_kpis_by_category(self, category: str) -> List[KPIMetric]:
        """Get KPIs by category"""
        return [kpi for kpi in self.kpi_metrics.values() if kpi.category == category]
    
    def get_critical_kpis(self) -> List[KPIMetric]:
        """Get KPIs with critical status"""
        return [kpi for kpi in self.kpi_metrics.values() if kpi.status == MetricStatus.CRITICAL]
    
    def update_kpi_value(self, metric_id: str, new_value: float) -> bool:
        """Update KPI metric value"""
        kpi = self.kpi_metrics.get(metric_id)
        if not kpi:
            return False
        
        old_value = kpi.current_value
        kpi.current_value = new_value
        kpi.last_updated = datetime.now().strftime('%Y-%m-%d')
        
        # Determine trend
        if new_value > old_value:
            kpi.trend = "Improving"
        elif new_value < old_value:
            kpi.trend = "Declining"
        else:
            kpi.trend = "Stable"
        
        # Update status based on target
        variance = abs(new_value - kpi.target_value) / kpi.target_value * 100
        
        if variance <= 5:
            kpi.status = MetricStatus.ON_TARGET
        elif variance <= 15:
            kpi.status = MetricStatus.AT_RISK
        else:
            kpi.status = MetricStatus.CRITICAL
        
        # Special case for metrics where higher is better
        if kpi.metric_name in ["Project Progress", "Quality Score"] and new_value > kpi.target_value:
            kpi.status = MetricStatus.EXCEEDING
        
        return True
    
    def generate_analytics_metrics(self) -> Dict[str, Any]:
        """Generate analytics system metrics"""
        reports = list(self.reports.values())
        kpis = list(self.kpi_metrics.values())
        
        if not reports and not kpis:
            return {}
        
        # Report metrics
        total_reports = len(reports)
        
        # Report type counts
        type_counts = {}
        for report_type in ReportType:
            type_counts[report_type.value] = len([r for r in reports if r.report_type == report_type])
        
        # Report frequency counts
        frequency_counts = {}
        for frequency in ReportFrequency:
            frequency_counts[frequency.value] = len([r for r in reports if r.frequency == frequency])
        
        # KPI metrics
        total_kpis = len(kpis)
        
        # KPI status counts
        status_counts = {}
        for status in MetricStatus:
            status_counts[status.value] = len([k for k in kpis if k.status == status])
        
        # Category performance
        categories = list(set(kpi.category for kpi in kpis))
        category_performance = {}
        for category in categories:
            category_kpis = [k for k in kpis if k.category == category]
            avg_performance = sum(
                (k.current_value / k.target_value * 100) if k.target_value > 0 else 100 
                for k in category_kpis
            ) / len(category_kpis) if category_kpis else 0
            category_performance[category] = round(avg_performance, 1)
        
        # File size metrics
        total_file_size = sum(r.file_size for r in reports if r.file_size > 0)
        
        return {
            "total_reports": total_reports,
            "total_kpis": total_kpis,
            "report_type_breakdown": type_counts,
            "report_frequency_breakdown": frequency_counts,
            "kpi_status_breakdown": status_counts,
            "category_performance": category_performance,
            "total_storage_mb": round(total_file_size / 1024 / 1024, 1),
            "automated_reports": len([r for r in reports if r.automated]),
            "critical_kpis": status_counts.get("Critical", 0),
            "exceeding_kpis": status_counts.get("Exceeding", 0)
        }

# Global instance for use across the application
analytics_manager = AnalyticsManager()