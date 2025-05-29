"""
Highland Tower Development - Settings Backend
Enterprise-grade system configuration and user preference management.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class UserRole(Enum):
    ADMIN = "Administrator"
    PROJECT_MANAGER = "Project Manager"
    CONSTRUCTION_MANAGER = "Construction Manager"
    SAFETY_MANAGER = "Safety Manager"
    COST_MANAGER = "Cost Manager"
    FIELD_SUPERVISOR = "Field Supervisor"
    QUALITY_INSPECTOR = "Quality Inspector"
    VIEWER = "Viewer"

class NotificationMethod(Enum):
    EMAIL = "Email"
    SMS = "SMS"
    PUSH = "Push Notification"
    IN_APP = "In-App Notification"

@dataclass
class UserPreference:
    """User preference settings"""
    preference_id: str
    user_id: str
    user_name: str
    user_role: UserRole
    
    # Interface preferences
    theme: str  # "Light", "Dark", "Auto"
    language: str
    timezone: str
    date_format: str
    currency_format: str
    
    # Notification preferences
    email_notifications: Dict[str, bool]
    sms_notifications: Dict[str, bool]
    push_notifications: Dict[str, bool]
    notification_frequency: str  # "Immediate", "Hourly", "Daily", "Weekly"
    
    # Dashboard preferences
    default_dashboard: str
    dashboard_layout: Dict[str, Any]
    favorite_modules: List[str]
    quick_access_items: List[str]
    
    # Report preferences
    default_report_format: str  # "PDF", "Excel", "CSV"
    auto_generate_reports: bool
    report_distribution_list: List[str]
    
    # Mobile preferences
    mobile_sync_frequency: str
    offline_mode_enabled: bool
    mobile_photo_quality: str  # "High", "Medium", "Low"
    
    # Privacy and security
    two_factor_enabled: bool
    session_timeout_minutes: int
    data_sharing_consent: bool
    
    # Workflow tracking
    created_at: str
    updated_at: str

@dataclass
class SystemConfiguration:
    """System-wide configuration settings"""
    config_id: str
    config_category: str  # "Security", "Integration", "Performance", "Backup"
    config_name: str
    
    # Configuration details
    setting_key: str
    setting_value: str
    setting_type: str  # "String", "Integer", "Boolean", "JSON"
    description: str
    
    # Constraints and validation
    is_required: bool
    default_value: str
    valid_values: Optional[List[str]]
    validation_rules: Dict[str, Any]
    
    # Access control
    requires_admin: bool
    requires_restart: bool
    environment: str  # "Development", "Staging", "Production"
    
    # Change tracking
    last_modified_by: str
    change_reason: str
    backup_value: Optional[str]
    
    # Workflow tracking
    created_at: str
    updated_at: str

@dataclass
class IntegrationSetting:
    """Third-party integration settings"""
    integration_id: str
    service_name: str
    service_type: str  # "API", "Database", "File System", "Cloud Service"
    
    # Connection details
    endpoint_url: str
    authentication_method: str  # "API Key", "OAuth", "Basic Auth", "Certificate"
    api_key: Optional[str]
    username: Optional[str]
    connection_timeout: int
    
    # Configuration
    is_enabled: bool
    sync_frequency: str
    data_mapping: Dict[str, str]
    sync_direction: str  # "Import", "Export", "Bidirectional"
    
    # Status and monitoring
    last_sync: Optional[str]
    sync_status: str  # "Success", "Failed", "In Progress", "Disabled"
    error_count: int
    last_error: Optional[str]
    
    # Performance metrics
    avg_response_time: float
    success_rate: float
    data_volume_mb: float
    
    # Workflow tracking
    created_at: str
    updated_at: str

class SettingsManager:
    """Enterprise settings management system"""
    
    def __init__(self):
        self.user_preferences: Dict[str, UserPreference] = {}
        self.system_configurations: Dict[str, SystemConfiguration] = {}
        self.integration_settings: Dict[str, IntegrationSetting] = {}
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample settings data"""
        
        # Sample User Preferences
        sample_preferences = [
            UserPreference(
                preference_id="pref-001",
                user_id="user-001",
                user_name="John Smith",
                user_role=UserRole.PROJECT_MANAGER,
                theme="Dark",
                language="English",
                timezone="America/New_York",
                date_format="MM/DD/YYYY",
                currency_format="USD",
                email_notifications={
                    "daily_reports": True,
                    "safety_alerts": True,
                    "cost_overruns": True,
                    "schedule_delays": True,
                    "rfi_updates": True
                },
                sms_notifications={
                    "emergency_alerts": True,
                    "critical_issues": True,
                    "safety_incidents": True
                },
                push_notifications={
                    "task_assignments": True,
                    "meeting_reminders": True,
                    "deadline_alerts": True
                },
                notification_frequency="Immediate",
                default_dashboard="Executive Dashboard",
                dashboard_layout={
                    "layout": "grid",
                    "widgets": ["project_progress", "cost_summary", "safety_metrics", "recent_rfis"],
                    "refresh_interval": 300
                },
                favorite_modules=["Dashboard", "Cost Management", "RFIs", "Daily Reports", "Analytics"],
                quick_access_items=["Create RFI", "Daily Report", "Safety Incident", "Cost Entry"],
                default_report_format="PDF",
                auto_generate_reports=True,
                report_distribution_list=["stakeholders@highland.com", "owner@highland.com"],
                mobile_sync_frequency="Real-time",
                offline_mode_enabled=True,
                mobile_photo_quality="High",
                two_factor_enabled=True,
                session_timeout_minutes=480,
                data_sharing_consent=True,
                created_at="2025-01-15 08:00:00",
                updated_at="2025-05-28 16:45:00"
            ),
            UserPreference(
                preference_id="pref-002",
                user_id="user-002",
                user_name="Sarah Wilson",
                user_role=UserRole.SAFETY_MANAGER,
                theme="Light",
                language="English",
                timezone="America/New_York",
                date_format="DD/MM/YYYY",
                currency_format="USD",
                email_notifications={
                    "safety_alerts": True,
                    "incident_reports": True,
                    "inspection_due": True,
                    "training_reminders": True,
                    "compliance_updates": True
                },
                sms_notifications={
                    "emergency_alerts": True,
                    "safety_incidents": True,
                    "evacuation_alerts": True
                },
                push_notifications={
                    "inspection_schedules": True,
                    "safety_meetings": True,
                    "incident_updates": True
                },
                notification_frequency="Immediate",
                default_dashboard="Safety Dashboard",
                dashboard_layout={
                    "layout": "safety_focused",
                    "widgets": ["safety_metrics", "incident_tracker", "inspection_status", "training_progress"],
                    "refresh_interval": 60
                },
                favorite_modules=["Safety", "Inspections", "Quality Control", "Daily Reports"],
                quick_access_items=["Safety Incident", "Inspection", "Safety Meeting", "Training Record"],
                default_report_format="Excel",
                auto_generate_reports=True,
                report_distribution_list=["safety@highland.com", "osha@highland.com"],
                mobile_sync_frequency="Every 5 minutes",
                offline_mode_enabled=True,
                mobile_photo_quality="High",
                two_factor_enabled=True,
                session_timeout_minutes=240,
                data_sharing_consent=True,
                created_at="2025-02-01 09:00:00",
                updated_at="2025-05-28 15:30:00"
            )
        ]
        
        for preference in sample_preferences:
            self.user_preferences[preference.preference_id] = preference
        
        # Sample System Configurations
        sample_configs = [
            SystemConfiguration(
                config_id="config-001",
                config_category="Security",
                config_name="Password Policy",
                setting_key="password_policy.min_length",
                setting_value="12",
                setting_type="Integer",
                description="Minimum password length for user accounts",
                is_required=True,
                default_value="8",
                valid_values=None,
                validation_rules={"min": 8, "max": 128},
                requires_admin=True,
                requires_restart=False,
                environment="Production",
                last_modified_by="System Administrator",
                change_reason="Enhanced security requirements",
                backup_value="8",
                created_at="2025-01-10 10:00:00",
                updated_at="2025-03-15 14:30:00"
            ),
            SystemConfiguration(
                config_id="config-002",
                config_category="Performance",
                config_name="Database Connection Pool",
                setting_key="database.connection_pool.max_size",
                setting_value="50",
                setting_type="Integer",
                description="Maximum number of database connections in the pool",
                is_required=True,
                default_value="20",
                valid_values=None,
                validation_rules={"min": 10, "max": 100},
                requires_admin=True,
                requires_restart=True,
                environment="Production",
                last_modified_by="Database Administrator",
                change_reason="Performance optimization for Highland Tower load",
                backup_value="20",
                created_at="2025-01-10 10:00:00",
                updated_at="2025-04-20 16:00:00"
            ),
            SystemConfiguration(
                config_id="config-003",
                config_category="Integration",
                config_name="API Rate Limiting",
                setting_key="api.rate_limit.requests_per_hour",
                setting_value="10000",
                setting_type="Integer",
                description="Maximum API requests per hour per client",
                is_required=True,
                default_value="1000",
                valid_values=None,
                validation_rules={"min": 100, "max": 100000},
                requires_admin=True,
                requires_restart=False,
                environment="Production",
                last_modified_by="API Administrator",
                change_reason="Increased limit for Highland Tower mobile apps",
                backup_value="5000",
                created_at="2025-02-01 12:00:00",
                updated_at="2025-05-15 10:30:00"
            )
        ]
        
        for config in sample_configs:
            self.system_configurations[config.config_id] = config
        
        # Sample Integration Settings
        sample_integrations = [
            IntegrationSetting(
                integration_id="int-001",
                service_name="Weather API",
                service_type="API",
                endpoint_url="https://api.weather.com/v1/current",
                authentication_method="API Key",
                api_key="weather_api_key_hidden",
                username=None,
                connection_timeout=30,
                is_enabled=True,
                sync_frequency="Every hour",
                data_mapping={"temperature": "site_temperature", "conditions": "weather_conditions"},
                sync_direction="Import",
                last_sync="2025-05-28 16:00:00",
                sync_status="Success",
                error_count=0,
                last_error=None,
                avg_response_time=1.2,
                success_rate=99.8,
                data_volume_mb=0.05,
                created_at="2025-01-20 11:00:00",
                updated_at="2025-05-28 16:00:00"
            ),
            IntegrationSetting(
                integration_id="int-002",
                service_name="Document Storage",
                service_type="Cloud Service",
                endpoint_url="https://storage.highland.com/api/v2",
                authentication_method="OAuth",
                api_key=None,
                username="highland_service",
                connection_timeout=60,
                is_enabled=True,
                sync_frequency="Real-time",
                data_mapping={"documents": "project_documents", "photos": "progress_photos"},
                sync_direction="Bidirectional",
                last_sync="2025-05-28 16:45:00",
                sync_status="Success",
                error_count=2,
                last_error="Temporary network timeout on 2025-05-27",
                avg_response_time=3.8,
                success_rate=97.5,
                data_volume_mb=1250.0,
                created_at="2025-01-15 09:00:00",
                updated_at="2025-05-28 16:45:00"
            ),
            IntegrationSetting(
                integration_id="int-003",
                service_name="Email Service",
                service_type="API",
                endpoint_url="https://api.sendgrid.com/v3/mail/send",
                authentication_method="API Key",
                api_key="sendgrid_api_key_hidden",
                username=None,
                connection_timeout=30,
                is_enabled=True,
                sync_frequency="Real-time",
                data_mapping={"notifications": "email_notifications", "reports": "email_reports"},
                sync_direction="Export",
                last_sync="2025-05-28 16:50:00",
                sync_status="Success",
                error_count=1,
                last_error="Rate limit exceeded on 2025-05-26",
                avg_response_time=2.1,
                success_rate=99.2,
                data_volume_mb=15.8,
                created_at="2025-01-10 08:00:00",
                updated_at="2025-05-28 16:50:00"
            )
        ]
        
        for integration in sample_integrations:
            self.integration_settings[integration.integration_id] = integration
    
    def create_user_preference(self, preference_data: Dict[str, Any]) -> str:
        """Create new user preference settings"""
        preference_id = f"pref-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        preference_data.update({
            "preference_id": preference_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enum
        preference_data["user_role"] = UserRole(preference_data["user_role"])
        
        preference = UserPreference(**preference_data)
        self.user_preferences[preference_id] = preference
        
        return preference_id
    
    def create_system_configuration(self, config_data: Dict[str, Any]) -> str:
        """Create new system configuration"""
        config_id = f"config-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        config_data.update({
            "config_id": config_id,
            "last_modified_by": config_data.get("last_modified_by", "System Administrator"),
            "change_reason": config_data.get("change_reason", "Configuration update"),
            "backup_value": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        config = SystemConfiguration(**config_data)
        self.system_configurations[config_id] = config
        
        return config_id
    
    def create_integration_setting(self, integration_data: Dict[str, Any]) -> str:
        """Create new integration setting"""
        integration_id = f"int-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        integration_data.update({
            "integration_id": integration_id,
            "last_sync": None,
            "sync_status": "Configured",
            "error_count": 0,
            "last_error": None,
            "avg_response_time": 0.0,
            "success_rate": 0.0,
            "data_volume_mb": 0.0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        integration = IntegrationSetting(**integration_data)
        self.integration_settings[integration_id] = integration
        
        return integration_id
    
    def get_all_user_preferences(self) -> List[UserPreference]:
        """Get all user preferences"""
        return list(self.user_preferences.values())
    
    def get_user_preferences_by_role(self, role: UserRole) -> List[UserPreference]:
        """Get user preferences filtered by role"""
        return [pref for pref in self.user_preferences.values() if pref.user_role == role]
    
    def get_all_system_configurations(self) -> List[SystemConfiguration]:
        """Get all system configurations grouped by category"""
        return sorted(self.system_configurations.values(), key=lambda c: (c.config_category, c.config_name))
    
    def get_configurations_by_category(self, category: str) -> List[SystemConfiguration]:
        """Get system configurations by category"""
        return [config for config in self.system_configurations.values() if config.config_category == category]
    
    def get_all_integration_settings(self) -> List[IntegrationSetting]:
        """Get all integration settings"""
        return sorted(self.integration_settings.values(), key=lambda i: i.service_name)
    
    def get_active_integrations(self) -> List[IntegrationSetting]:
        """Get only active integrations"""
        return [integration for integration in self.integration_settings.values() if integration.is_enabled]
    
    def update_integration_status(self, integration_id: str, status: str, error_message: Optional[str] = None) -> bool:
        """Update integration sync status"""
        integration = self.integration_settings.get(integration_id)
        if not integration:
            return False
        
        integration.sync_status = status
        integration.last_sync = datetime.now().isoformat()
        integration.updated_at = datetime.now().isoformat()
        
        if error_message:
            integration.error_count += 1
            integration.last_error = error_message
        
        return True
    
    def generate_settings_metrics(self) -> Dict[str, Any]:
        """Generate settings and configuration metrics"""
        preferences = list(self.user_preferences.values())
        configs = list(self.system_configurations.values())
        integrations = list(self.integration_settings.values())
        
        if not preferences and not configs and not integrations:
            return {}
        
        # User preference metrics
        total_users = len(preferences)
        
        # Theme preferences
        theme_breakdown = {}
        themes = ["Light", "Dark", "Auto"]
        for theme in themes:
            theme_breakdown[theme] = len([p for p in preferences if p.theme == theme])
        
        # Role distribution
        role_breakdown = {}
        for role in UserRole:
            role_breakdown[role.value] = len([p for p in preferences if p.user_role == role])
        
        # System configuration metrics
        total_configs = len(configs)
        config_categories = {}
        categories = list(set(c.config_category for c in configs))
        for category in categories:
            config_categories[category] = len([c for c in configs if c.config_category == category])
        
        # Integration metrics
        total_integrations = len(integrations)
        active_integrations = len([i for i in integrations if i.is_enabled])
        successful_syncs = len([i for i in integrations if i.sync_status == "Success"])
        
        # Integration types
        integration_types = {}
        types = list(set(i.service_type for i in integrations))
        for int_type in types:
            integration_types[int_type] = len([i for i in integrations if i.service_type == int_type])
        
        return {
            "total_users": total_users,
            "theme_preferences": theme_breakdown,
            "role_distribution": role_breakdown,
            "total_configurations": total_configs,
            "config_categories": config_categories,
            "total_integrations": total_integrations,
            "active_integrations": active_integrations,
            "integration_success_rate": round((successful_syncs / total_integrations * 100) if total_integrations > 0 else 0, 1),
            "integration_types": integration_types,
            "two_factor_adoption": round((len([p for p in preferences if p.two_factor_enabled]) / total_users * 100) if total_users > 0 else 0, 1)
        }

# Global instance for use across the application
settings_manager = SettingsManager()