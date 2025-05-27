"""
Pure Python UI Component Generator for Highland Tower Development
Streamlit-agnostic components that can be easily adapted to any UI framework

This approach ensures longevity by separating business logic from UI rendering
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import date, datetime
from .data_models import RFI, Subcontractor, Project, Priority, RFIStatus, Discipline
from .business_logic import highland_tower_manager


class ComponentGenerator:
    """Generate UI component data structures that can be rendered by any framework"""
    
    @staticmethod
    def generate_rfi_list_data() -> Dict[str, Any]:
        """Generate data structure for RFI list component"""
        rfis = highland_tower_manager.get_rfis()
        stats = highland_tower_manager.get_rfi_statistics()
        
        # Convert RFIs to display-ready format
        rfi_display_data = []
        for rfi in rfis:
            priority_icon = {
                Priority.CRITICAL: "🔴",
                Priority.HIGH: "🟠", 
                Priority.MEDIUM: "🟡",
                Priority.LOW: "🟢"
            }.get(rfi.priority, "⚪")
            
            status_icon = {
                RFIStatus.OPEN: "🔴",
                RFIStatus.IN_REVIEW: "🟡",
                RFIStatus.ANSWERED: "🟢",
                RFIStatus.CLOSED: "✅"
            }.get(rfi.status, "⚪")
            
            rfi_display_data.append({
                "id": rfi.id,
                "number": rfi.number,
                "subject": rfi.subject,
                "priority": rfi.priority.value.title(),
                "priority_icon": priority_icon,
                "status": rfi.status.value.title().replace("_", " "),
                "status_icon": status_icon,
                "discipline": rfi.discipline.value.title(),
                "location": rfi.location,
                "submitted_by": rfi.submitted_by,
                "due_date": rfi.due_date.strftime("%Y-%m-%d"),
                "days_open": rfi.days_open,
                "cost_impact": rfi.cost_impact,
                "schedule_impact": rfi.schedule_impact,
                "description": rfi.description,
                "is_overdue": rfi.is_overdue
            })
        
        return {
            "rfis": rfi_display_data,
            "statistics": {
                "total": stats["total"],
                "open": stats["open"],
                "critical": stats["critical"],
                "overdue": stats["overdue"],
                "avg_days_open": stats["avg_days_open"]
            },
            "action_buttons": [
                {"label": "➕ Create RFI", "action": "create", "primary": True},
                {"label": "🔍 Search RFIs", "action": "search", "primary": False},
                {"label": "📊 Analytics", "action": "analytics", "primary": False},
                {"label": "📋 Reports", "action": "reports", "primary": False}
            ]
        }
    
    @staticmethod
    def generate_rfi_form_data() -> Dict[str, Any]:
        """Generate RFI creation form structure"""
        return {
            "title": "Create New RFI - Highland Tower Development",
            "fields": [
                {
                    "name": "subject",
                    "label": "RFI Subject*",
                    "type": "text",
                    "placeholder": "Brief description of the question or issue",
                    "required": True
                },
                {
                    "name": "location",
                    "label": "Location",
                    "type": "select",
                    "options": [
                        "Level B2 - Parking",
                        "Level B1 - Storage", 
                        "Ground Floor - Retail",
                        "Level 2-5 - Residential",
                        "Level 6-10 - Residential",
                        "Level 11-15 - Residential",
                        "Mechanical Penthouse",
                        "Roof Level",
                        "Site Overall"
                    ],
                    "required": True
                },
                {
                    "name": "discipline",
                    "label": "Engineering Discipline",
                    "type": "select",
                    "options": [d.value.title().replace("_", " ") for d in Discipline],
                    "required": True
                },
                {
                    "name": "priority",
                    "label": "Priority Level",
                    "type": "select",
                    "options": [p.value.title() for p in Priority],
                    "required": True
                },
                {
                    "name": "assigned_to",
                    "label": "Assign To",
                    "type": "select",
                    "options": [
                        "Highland Structural Engineering",
                        "Highland MEP Consultants",
                        "Highland Architecture Group", 
                        "Highland Electrical Consultants",
                        "Fire Safety Consultants Inc",
                        "Project Engineering Team"
                    ],
                    "required": True
                },
                {
                    "name": "description",
                    "label": "Detailed Description*",
                    "type": "textarea",
                    "placeholder": "Provide detailed description of the question, issue, or clarification needed...",
                    "required": True
                },
                {
                    "name": "cost_impact",
                    "label": "Estimated Cost Impact",
                    "type": "select",
                    "options": [
                        "No Impact",
                        "$0 - $2,000",
                        "$2,000 - $5,000", 
                        "$5,000 - $15,000",
                        "$15,000 - $25,000",
                        "$25,000+"
                    ]
                },
                {
                    "name": "schedule_impact",
                    "label": "Schedule Impact", 
                    "type": "select",
                    "options": [
                        "No Impact",
                        "1 day",
                        "2-3 days",
                        "4-7 days",
                        "1-2 weeks",
                        "2+ weeks"
                    ]
                }
            ]
        }
    
    @staticmethod
    def generate_subcontractor_data() -> Dict[str, Any]:
        """Generate subcontractor management component data"""
        subcontractors = highland_tower_manager.get_subcontractors()
        performance_stats = highland_tower_manager.get_subcontractor_performance_summary()
        
        sub_display_data = []
        for sub in subcontractors:
            # Calculate performance indicators
            rating_color = "green" if sub.performance_rating >= 4.5 else "orange" if sub.performance_rating >= 4.0 else "red"
            insurance_status = "valid" if sub.insurance_expiry > date.today() else "expired"
            
            sub_display_data.append({
                "id": sub.id,
                "company_name": sub.company_name,
                "contact_person": sub.contact_person,
                "email": sub.email,
                "phone": sub.phone,
                "specialties": ", ".join(sub.specialties),
                "performance_rating": sub.performance_rating,
                "rating_color": rating_color,
                "active_projects": sub.active_projects,
                "contract_value_formatted": f"${sub.total_contract_value:,.0f}",
                "insurance_status": insurance_status,
                "insurance_expiry": sub.insurance_expiry.strftime("%Y-%m-%d")
            })
        
        return {
            "subcontractors": sub_display_data,
            "statistics": performance_stats,
            "summary_cards": [
                {
                    "title": "Total Subcontractors",
                    "value": performance_stats.get("total_subcontractors", 0),
                    "icon": "👥"
                },
                {
                    "title": "Average Rating",
                    "value": f"{performance_stats.get('average_rating', 0)}/5.0",
                    "icon": "⭐"
                },
                {
                    "title": "Total Contract Value",
                    "value": f"${performance_stats.get('total_contract_value', 0):,.0f}",
                    "icon": "💰"
                },
                {
                    "title": "Active Projects",
                    "value": performance_stats.get("active_projects", 0),
                    "icon": "🚧"
                }
            ]
        }
    
    @staticmethod
    def generate_dashboard_data() -> Dict[str, Any]:
        """Generate dashboard component data"""
        health_metrics = highland_tower_manager.get_project_health_metrics()
        rfi_stats = highland_tower_manager.get_rfi_statistics()
        
        return {
            "project_info": {
                "name": "Highland Tower Development",
                "value": "$45.5M",
                "progress": f"{health_metrics['progress_percent']}%",
                "status": "Active Development",
                "days_remaining": health_metrics["days_to_completion"]
            },
            "key_metrics": [
                {
                    "title": "Project Health",
                    "value": f"{health_metrics['overall_health_score']}%",
                    "trend": "↗️" if health_metrics['overall_health_score'] > 80 else "→",
                    "color": "green" if health_metrics['overall_health_score'] > 80 else "orange"
                },
                {
                    "title": "Active RFIs",
                    "value": rfi_stats["open"],
                    "trend": "↗️" if rfi_stats["open"] < 10 else "↘️",
                    "color": "green" if rfi_stats["open"] < 10 else "red"
                },
                {
                    "title": "Budget Remaining",
                    "value": f"${health_metrics['budget_remaining']:,.0f}",
                    "trend": "→",
                    "color": "blue"
                },
                {
                    "title": "Critical Issues",
                    "value": rfi_stats["critical"],
                    "trend": "↘️" if rfi_stats["critical"] < 3 else "↗️",
                    "color": "green" if rfi_stats["critical"] < 3 else "red"
                }
            ],
            "recent_activities": [
                f"RFI {rfi.number} created: {rfi.subject[:50]}..." 
                for rfi in highland_tower_manager.rfis[-5:]
            ]
        }
    
    @staticmethod
    def generate_analytics_charts_data() -> Dict[str, Any]:
        """Generate chart data for analytics dashboards"""
        rfis = highland_tower_manager.get_rfis()
        
        # RFI by priority breakdown
        priority_counts = {}
        for rfi in rfis:
            priority = rfi.priority.value.title()
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # RFI by discipline breakdown
        discipline_counts = {}
        for rfi in rfis:
            discipline = rfi.discipline.value.title().replace("_", " ")
            discipline_counts[discipline] = discipline_counts.get(discipline, 0) + 1
        
        # RFI status breakdown
        status_counts = {}
        for rfi in rfis:
            status = rfi.status.value.title().replace("_", " ")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "priority_chart": {
                "type": "pie",
                "title": "RFIs by Priority Level",
                "data": priority_counts
            },
            "discipline_chart": {
                "type": "bar",
                "title": "RFIs by Engineering Discipline", 
                "data": discipline_counts
            },
            "status_chart": {
                "type": "donut",
                "title": "RFI Status Distribution",
                "data": status_counts
            },
            "timeline_data": {
                "title": "RFI Submission Timeline",
                "data": [
                    {
                        "date": rfi.submitted_date.strftime("%Y-%m-%d"),
                        "count": 1,
                        "priority": rfi.priority.value
                    }
                    for rfi in rfis
                ]
            }
        }


class DataProcessor:
    """Pure Python data processing utilities"""
    
    @staticmethod
    def filter_rfis(rfis: List[RFI], filters: Dict[str, Any]) -> List[RFI]:
        """Filter RFIs based on criteria"""
        filtered = rfis.copy()
        
        if filters.get("status"):
            status = RFIStatus(filters["status"].lower())
            filtered = [rfi for rfi in filtered if rfi.status == status]
        
        if filters.get("priority"):
            priority = Priority(filters["priority"].lower())
            filtered = [rfi for rfi in filtered if rfi.priority == priority]
        
        if filters.get("discipline"):
            discipline = Discipline(filters["discipline"].lower().replace(" ", "_"))
            filtered = [rfi for rfi in filtered if rfi.discipline == discipline]
        
        if filters.get("search_text"):
            search_text = filters["search_text"].lower()
            filtered = [
                rfi for rfi in filtered 
                if search_text in rfi.subject.lower() or search_text in rfi.description.lower()
            ]
        
        return filtered
    
    @staticmethod
    def sort_rfis(rfis: List[RFI], sort_by: str = "submitted_date", reverse: bool = True) -> List[RFI]:
        """Sort RFIs by specified field"""
        if sort_by == "priority":
            priority_order = {Priority.CRITICAL: 4, Priority.HIGH: 3, Priority.MEDIUM: 2, Priority.LOW: 1}
            return sorted(rfis, key=lambda x: priority_order[x.priority], reverse=reverse)
        elif sort_by == "days_open":
            return sorted(rfis, key=lambda x: x.days_open, reverse=reverse)
        elif sort_by == "due_date":
            return sorted(rfis, key=lambda x: x.due_date, reverse=reverse)
        else:
            return sorted(rfis, key=lambda x: getattr(x, sort_by), reverse=reverse)


# Export main component generator instance
ui_components = ComponentGenerator()
data_processor = DataProcessor()