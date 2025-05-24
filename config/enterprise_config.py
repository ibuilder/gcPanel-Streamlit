"""
Enterprise Configuration for Highland Tower Development Dashboard

Centralized configuration management with production-ready settings.
"""

from datetime import datetime
from typing import Dict, List, Any

class EnterpriseConfig:
    """Centralized configuration for Highland Tower Development enterprise features."""
    
    # Project Information
    PROJECT_INFO = {
        "name": "Highland Tower Development",
        "value": "$45.5M",
        "type": "Mixed-Use Development",
        "units": "120 Residential + 8 Retail",
        "area": "168,500 sq ft",
        "floors": "15 above ground, 2 below",
        "status": "Under Construction",
        "start_date": "2024-01-15",
        "target_completion": "2026-03-30"
    }
    
    # Enhanced Navigation with Categories
    NAVIGATION_STRUCTURE = {
        "Project Management": {
            "📊 Dashboard": "Dashboard",
            "📋 Project Information": "Project Information", 
            "📅 Schedule": "Schedule",
            "🤝 Meeting Management": "Meeting Management"
        },
        "Field Operations": {
            "📝 Daily Reports": "Daily Reports",
            "❓ RFIs": "RFIs", 
            "📦 Submittals": "Submittals",
            "📤 Transmittals": "Transmittals",
            "🚧 Field Operations": "Field Operations"
        },
        "Safety & Compliance": {
            "⚠️ Safety": "Safety",
            "📄 Documents": "Documents",
            "✅ Closeout": "Closeout"
        },
        "Technology & Analytics": {
            "🏢 BIM": "BIM",
            "📈 Analytics": "Analytics",
            "🤖 AI Assistant": "AI Assistant",
            "📱 Mobile Companion": "Mobile Companion"
        },
        "Business Management": {
            "📝 Contracts": "Contracts",
            "💰 Cost Management": "Cost Management",
            "🏗️ PreConstruction": "PreConstruction"
        },
        "Collaboration & Admin": {
            "👥 Collaboration": "Collaboration",
            "🔄 Integrations": "Integrations",
            "⚙️ Settings": "Settings",
            "👨‍💻 Admin": "Admin"
        }
    }
    
    # Real-time Features Configuration
    REAL_TIME_CONFIG = {
        "collaboration_enabled": True,
        "live_updates": True,
        "user_presence_tracking": True,
        "real_time_notifications": True,
        "websocket_enabled": True,
        "update_interval": 5000  # milliseconds
    }
    
    # Search & Filtering Configuration
    SEARCH_CONFIG = {
        "global_search_enabled": True,
        "fuzzy_search": True,
        "search_suggestions": True,
        "search_history_limit": 50,
        "index_refresh_interval": 300,  # seconds
        "searchable_fields": [
            "id", "title", "description", "status", 
            "created_by", "date", "priority", "tags"
        ]
    }
    
    # Mobile Optimization Settings
    MOBILE_CONFIG = {
        "responsive_design": True,
        "mobile_navigation": True,
        "touch_optimized": True,
        "offline_capabilities": True,
        "field_shortcuts": True,
        "photo_capture": True,
        "voice_notes": True
    }
    
    # Performance & Caching Configuration
    PERFORMANCE_CONFIG = {
        "caching_enabled": True,
        "lazy_loading": True,
        "connection_pooling": True,
        "query_optimization": True,
        "compression": True,
        "cdn_enabled": False,  # Enable in production
        "cache_ttl": 3600  # seconds
    }
    
    # Security & Audit Configuration
    SECURITY_CONFIG = {
        "audit_logging": True,
        "security_monitoring": True,
        "session_timeout": 3600,  # seconds
        "password_complexity": True,
        "two_factor_auth": False,  # Enable in production
        "ip_whitelisting": False,
        "encryption_at_rest": True
    }
    
    # Notification Configuration
    NOTIFICATION_CONFIG = {
        "email_notifications": True,
        "sms_notifications": False,  # Requires Twilio setup
        "browser_notifications": True,
        "slack_integration": False,  # Optional
        "teams_integration": False,  # Optional
        "notification_retention": 30  # days
    }
    
    # Module-specific Configurations
    MODULE_CONFIGS = {
        "daily_reports": {
            "auto_save": True,
            "weather_integration": False,  # Requires weather API
            "photo_attachments": True,
            "signature_capture": True,
            "offline_mode": True
        },
        "rfis": {
            "auto_numbering": True,
            "approval_workflow": True,
            "due_date_alerts": True,
            "photo_markup": True,
            "email_notifications": True
        },
        "submittals": {
            "version_control": True,
            "approval_matrix": True,
            "automated_routing": True,
            "compliance_checking": True,
            "integration_with_specs": True
        },
        "safety": {
            "incident_reporting": True,
            "hazard_tracking": True,
            "training_records": True,
            "inspection_checklists": True,
            "emergency_contacts": True
        }
    }
    
    # Integration Settings
    INTEGRATION_CONFIG = {
        "procore_sync": False,
        "autodesk_construction_cloud": False,
        "microsoft_project": False,
        "quickbooks": False,
        "docusign": False,
        "dropbox": False,
        "sharepoint": False
    }
    
    # Dashboard Metrics Configuration
    DASHBOARD_METRICS = [
        {
            "name": "Project Progress",
            "type": "percentage",
            "source": "schedule",
            "update_frequency": "daily"
        },
        {
            "name": "Budget Status", 
            "type": "currency",
            "source": "cost_management",
            "update_frequency": "weekly"
        },
        {
            "name": "Safety Record",
            "type": "counter",
            "source": "safety",
            "update_frequency": "daily"
        },
        {
            "name": "Active RFIs",
            "type": "counter", 
            "source": "rfis",
            "update_frequency": "real_time"
        }
    ]
    
    # User Roles and Permissions
    USER_ROLES = {
        "admin": {
            "permissions": ["all"],
            "modules": ["all"]
        },
        "project_manager": {
            "permissions": ["view", "create", "edit", "approve"],
            "modules": ["all"]
        },
        "superintendent": {
            "permissions": ["view", "create", "edit"],
            "modules": ["daily_reports", "rfis", "safety", "field_operations"]
        },
        "foreman": {
            "permissions": ["view", "create"],
            "modules": ["daily_reports", "safety"]
        },
        "viewer": {
            "permissions": ["view"],
            "modules": ["dashboard", "schedule", "documents"]
        }
    }
    
    # Production Environment Settings
    PRODUCTION_CONFIG = {
        "debug_mode": False,
        "ssl_required": True,
        "database_backup": True,
        "monitoring_enabled": True,
        "error_reporting": True,
        "performance_tracking": True,
        "security_scanning": True,
        "load_balancing": True
    }