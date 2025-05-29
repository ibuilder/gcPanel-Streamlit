"""
Highland Tower Development - Mobile Companion Backend
Enterprise-grade mobile field operations with real-time sync and offline capabilities.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class DeviceType(Enum):
    SMARTPHONE = "Smartphone"
    TABLET = "Tablet"
    RUGGED_DEVICE = "Rugged Device"
    LAPTOP = "Laptop"

class SyncStatus(Enum):
    SYNCED = "Synced"
    PENDING = "Pending"
    FAILED = "Failed"
    OFFLINE = "Offline"

@dataclass
class MobileUser:
    """Mobile app user record"""
    user_id: str
    username: str
    full_name: str
    role: str
    department: str
    
    # Device information
    device_id: str
    device_type: DeviceType
    device_model: str
    app_version: str
    os_version: str
    
    # Access permissions
    modules_access: List[str]
    data_permissions: List[str]
    offline_enabled: bool
    
    # Location and status
    current_location: Optional[Dict[str, float]]  # lat, lng
    last_active: str
    online_status: bool
    
    # Settings
    notification_preferences: Dict[str, bool]
    sync_frequency: str
    data_usage_limit: int  # MB
    
    # Metrics
    login_count: int
    total_sync_data: int  # MB
    last_sync: str
    
    # Workflow tracking
    created_at: str
    updated_at: str

@dataclass
class FieldReport:
    """Mobile field report"""
    report_id: str
    report_type: str  # "Daily Progress", "Safety Incident", "Quality Issue", "Material Delivery"
    
    # Content
    title: str
    description: str
    location: str
    coordinates: Optional[Dict[str, float]]
    
    # Media attachments
    photos: List[str]
    videos: List[str]
    audio_notes: List[str]
    
    # Categorization
    trade: str
    priority: str
    status: str
    
    # Personnel
    reported_by: str
    assigned_to: Optional[str]
    witnesses: List[str]
    
    # Timestamps
    incident_time: Optional[str]
    reported_time: str
    
    # Sync information
    sync_status: SyncStatus
    offline_created: bool
    device_id: str
    
    # Follow-up
    follow_up_required: bool
    follow_up_date: Optional[str]
    resolution_notes: str
    
    # Workflow tracking
    created_at: str
    updated_at: str

@dataclass
class OfflineData:
    """Offline data cache"""
    cache_id: str
    user_id: str
    device_id: str
    
    # Cached content
    module_name: str
    data_type: str  # "forms", "reports", "schedules", "contacts"
    cached_data: Dict[str, Any]
    
    # Cache metadata
    cache_size: int  # bytes
    last_updated: str
    expires_at: str
    
    # Sync tracking
    sync_status: SyncStatus
    pending_changes: List[Dict[str, Any]]
    conflict_resolution: str  # "server_wins", "client_wins", "manual"
    
    # Workflow tracking
    created_at: str
    updated_at: str

class MobileCompanionManager:
    """Enterprise mobile companion management system"""
    
    def __init__(self):
        self.mobile_users: Dict[str, MobileUser] = {}
        self.field_reports: Dict[str, FieldReport] = {}
        self.offline_caches: Dict[str, OfflineData] = {}
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample mobile data"""
        
        # Sample Mobile Users
        sample_users = [
            MobileUser(
                user_id="mobile-001",
                username="jsmith_mobile",
                full_name="John Smith",
                role="Project Manager",
                department="Project Management",
                device_id="device-iphone-001",
                device_type=DeviceType.SMARTPHONE,
                device_model="iPhone 14 Pro",
                app_version="2.1.3",
                os_version="iOS 17.2",
                modules_access=["Dashboard", "Daily Reports", "RFIs", "Progress Photos", "Safety"],
                data_permissions=["read", "write", "approve"],
                offline_enabled=True,
                current_location={"lat": 40.7128, "lng": -74.0060},
                last_active="2025-05-28 16:30:00",
                online_status=True,
                notification_preferences={"push_enabled": True, "email_digest": True, "safety_alerts": True},
                sync_frequency="Real-time",
                data_usage_limit=500,
                login_count=127,
                total_sync_data=2840,
                last_sync="2025-05-28 16:25:00",
                created_at="2025-01-15 08:00:00",
                updated_at="2025-05-28 16:30:00"
            ),
            MobileUser(
                user_id="mobile-002",
                username="swilson_tablet",
                full_name="Sarah Wilson",
                role="Safety Manager",
                department="Safety",
                device_id="device-ipad-002",
                device_type=DeviceType.TABLET,
                device_model="iPad Pro 12.9",
                app_version="2.1.3",
                os_version="iPadOS 17.2",
                modules_access=["Safety", "Daily Reports", "Progress Photos", "Quality Control", "Inspections"],
                data_permissions=["read", "write", "safety_approve"],
                offline_enabled=True,
                current_location={"lat": 40.7130, "lng": -74.0058},
                last_active="2025-05-28 15:45:00",
                online_status=True,
                notification_preferences={"push_enabled": True, "email_digest": False, "safety_alerts": True},
                sync_frequency="Every 15 minutes",
                data_usage_limit=1000,
                login_count=89,
                total_sync_data=4320,
                last_sync="2025-05-28 15:45:00",
                created_at="2025-02-01 09:00:00",
                updated_at="2025-05-28 15:45:00"
            ),
            MobileUser(
                user_id="mobile-003",
                username="mbrown_rugged",
                full_name="Mike Brown",
                role="Site Supervisor",
                department="Field Operations",
                device_id="device-rugged-003",
                device_type=DeviceType.RUGGED_DEVICE,
                device_model="Panasonic Toughbook G2",
                app_version="2.1.2",
                os_version="Android 13",
                modules_access=["Daily Reports", "Progress Photos", "Material Management", "Equipment Tracking"],
                data_permissions=["read", "write"],
                offline_enabled=True,
                current_location={"lat": 40.7125, "lng": -74.0065},
                last_active="2025-05-28 17:00:00",
                online_status=False,
                notification_preferences={"push_enabled": True, "email_digest": True, "safety_alerts": True},
                sync_frequency="When connected",
                data_usage_limit=250,
                login_count=156,
                total_sync_data=1680,
                last_sync="2025-05-28 14:30:00",
                created_at="2025-01-20 10:00:00",
                updated_at="2025-05-28 17:00:00"
            )
        ]
        
        for user in sample_users:
            self.mobile_users[user.user_id] = user
        
        # Sample Field Reports
        sample_reports = [
            FieldReport(
                report_id="field-001",
                report_type="Safety Incident",
                title="Minor Cut Injury - Level 12",
                description="Worker sustained minor cut on hand while handling steel beam. First aid administered on site. No lost time incident.",
                location="Level 12 - Grid E4",
                coordinates={"lat": 40.7128, "lng": -74.0060},
                photos=["incident_001_01.jpg", "incident_001_02.jpg"],
                videos=["incident_001_walkthrough.mp4"],
                audio_notes=["incident_001_witness_statement.m4a"],
                trade="Steel Erection",
                priority="Medium",
                status="Reported",
                reported_by="Sarah Wilson - Safety Manager",
                assigned_to="Safety Team",
                witnesses=["Mike Rodriguez - Steel Foreman", "Tom Johnson - Worker"],
                incident_time="2025-05-28 10:30:00",
                reported_time="2025-05-28 10:35:00",
                sync_status=SyncStatus.SYNCED,
                offline_created=False,
                device_id="device-ipad-002",
                follow_up_required=True,
                follow_up_date="2025-05-29",
                resolution_notes="Worker cleared to return to work. Additional safety briefing scheduled.",
                created_at="2025-05-28 10:35:00",
                updated_at="2025-05-28 11:00:00"
            ),
            FieldReport(
                report_id="field-002",
                report_type="Quality Issue",
                title="Concrete Surface Defect - Level 8",
                description="Surface imperfection identified in concrete pour. Requires patch repair before proceeding with floor finishes.",
                location="Level 8 - Office Area",
                coordinates={"lat": 40.7129, "lng": -74.0059},
                photos=["quality_002_01.jpg", "quality_002_02.jpg", "quality_002_03.jpg"],
                videos=[],
                audio_notes=["quality_002_explanation.m4a"],
                trade="Concrete",
                priority="High",
                status="In Progress",
                reported_by="Mike Brown - Site Supervisor",
                assigned_to="Concrete Contractor",
                witnesses=["Quality Inspector"],
                incident_time="2025-05-28 08:15:00",
                reported_time="2025-05-28 08:20:00",
                sync_status=SyncStatus.PENDING,
                offline_created=True,
                device_id="device-rugged-003",
                follow_up_required=True,
                follow_up_date="2025-05-30",
                resolution_notes="Patch repair scheduled for tomorrow morning.",
                created_at="2025-05-28 08:20:00",
                updated_at="2025-05-28 14:30:00"
            ),
            FieldReport(
                report_id="field-003",
                report_type="Daily Progress",
                title="Steel Erection Progress - Level 13",
                description="Completed installation of 12 steel beams on Level 13. Sequence ahead of schedule. Ready for deck installation.",
                location="Level 13 - Full Floor",
                coordinates={"lat": 40.7127, "lng": -74.0061},
                photos=["progress_003_01.jpg", "progress_003_02.jpg"],
                videos=["progress_003_timelapse.mp4"],
                audio_notes=[],
                trade="Steel Erection",
                priority="Low",
                status="Complete",
                reported_by="John Smith - Project Manager",
                assigned_to=None,
                witnesses=["Steel Crew Foreman"],
                incident_time="2025-05-28 16:00:00",
                reported_time="2025-05-28 16:15:00",
                sync_status=SyncStatus.SYNCED,
                offline_created=False,
                device_id="device-iphone-001",
                follow_up_required=False,
                follow_up_date=None,
                resolution_notes="Progress documented for daily report.",
                created_at="2025-05-28 16:15:00",
                updated_at="2025-05-28 16:20:00"
            )
        ]
        
        for report in sample_reports:
            self.field_reports[report.report_id] = report
        
        # Sample Offline Cache
        sample_cache = OfflineData(
            cache_id="cache-001",
            user_id="mobile-003",
            device_id="device-rugged-003",
            module_name="Daily Reports",
            data_type="forms",
            cached_data={
                "forms": ["daily_report_template", "progress_photo_form"],
                "lookup_data": {"trades": ["Concrete", "Steel", "MEP"], "locations": ["Level 8", "Level 9", "Level 10"]},
                "recent_reports": [{"id": "DR-001", "date": "2025-05-27", "status": "Draft"}]
            },
            cache_size=2048000,  # 2 MB
            last_updated="2025-05-28 14:30:00",
            expires_at="2025-05-29 14:30:00",
            sync_status=SyncStatus.PENDING,
            pending_changes=[
                {"type": "new_report", "data": {"id": "field-002", "created_offline": True}},
                {"type": "photo_upload", "data": {"report_id": "field-002", "photos": ["quality_002_01.jpg"]}}
            ],
            conflict_resolution="server_wins",
            created_at="2025-05-28 08:00:00",
            updated_at="2025-05-28 14:30:00"
        )
        
        self.offline_caches[sample_cache.cache_id] = sample_cache
    
    def create_mobile_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new mobile user"""
        user_id = f"mobile-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        user_data.update({
            "user_id": user_id,
            "device_id": f"device-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}",
            "current_location": None,
            "last_active": datetime.now().isoformat(),
            "online_status": True,
            "login_count": 0,
            "total_sync_data": 0,
            "last_sync": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enum
        user_data["device_type"] = DeviceType(user_data["device_type"])
        
        user = MobileUser(**user_data)
        self.mobile_users[user_id] = user
        
        return user_id
    
    def create_field_report(self, report_data: Dict[str, Any]) -> str:
        """Create a new field report"""
        report_id = f"field-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        report_data.update({
            "report_id": report_id,
            "reported_time": datetime.now().isoformat(),
            "sync_status": SyncStatus.PENDING,
            "offline_created": report_data.get("offline_created", False),
            "follow_up_required": False,
            "follow_up_date": None,
            "resolution_notes": "",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        report = FieldReport(**report_data)
        self.field_reports[report_id] = report
        
        return report_id
    
    def get_all_mobile_users(self) -> List[MobileUser]:
        """Get all mobile users sorted by last active"""
        return sorted(self.mobile_users.values(), key=lambda u: u.last_active, reverse=True)
    
    def get_online_users(self) -> List[MobileUser]:
        """Get currently online users"""
        return [user for user in self.mobile_users.values() if user.online_status]
    
    def get_all_field_reports(self) -> List[FieldReport]:
        """Get all field reports sorted by report time"""
        return sorted(self.field_reports.values(), key=lambda r: r.reported_time, reverse=True)
    
    def get_pending_sync_reports(self) -> List[FieldReport]:
        """Get reports pending sync"""
        return [report for report in self.field_reports.values() if report.sync_status == SyncStatus.PENDING]
    
    def sync_field_report(self, report_id: str) -> bool:
        """Sync a field report to server"""
        report = self.field_reports.get(report_id)
        if not report:
            return False
        
        report.sync_status = SyncStatus.SYNCED
        report.updated_at = datetime.now().isoformat()
        
        return True
    
    def update_user_location(self, user_id: str, lat: float, lng: float) -> bool:
        """Update user location"""
        user = self.mobile_users.get(user_id)
        if not user:
            return False
        
        user.current_location = {"lat": lat, "lng": lng}
        user.last_active = datetime.now().isoformat()
        user.updated_at = datetime.now().isoformat()
        
        return True
    
    def generate_mobile_metrics(self) -> Dict[str, Any]:
        """Generate mobile companion system metrics"""
        users = list(self.mobile_users.values())
        reports = list(self.field_reports.values())
        caches = list(self.offline_caches.values())
        
        if not users and not reports:
            return {}
        
        # User metrics
        total_users = len(users)
        online_users = len([u for u in users if u.online_status])
        offline_enabled_users = len([u for u in users if u.offline_enabled])
        
        # Device breakdown
        device_types = {}
        for device_type in DeviceType:
            device_types[device_type.value] = len([u for u in users if u.device_type == device_type])
        
        # Report metrics
        total_reports = len(reports)
        pending_sync = len([r for r in reports if r.sync_status == SyncStatus.PENDING])
        offline_created = len([r for r in reports if r.offline_created])
        
        # Report type breakdown
        report_types = {}
        types = list(set(r.report_type for r in reports))
        for report_type in types:
            report_types[report_type] = len([r for r in reports if r.report_type == report_type])
        
        # Sync metrics
        total_sync_data = sum(u.total_sync_data for u in users)
        
        return {
            "total_users": total_users,
            "online_users": online_users,
            "offline_enabled_users": offline_enabled_users,
            "device_type_breakdown": device_types,
            "total_reports": total_reports,
            "pending_sync": pending_sync,
            "offline_created": offline_created,
            "report_type_breakdown": report_types,
            "total_sync_data_mb": total_sync_data,
            "sync_success_rate": round(((total_reports - pending_sync) / total_reports * 100) if total_reports > 0 else 0, 1),
            "offline_usage_rate": round((offline_created / total_reports * 100) if total_reports > 0 else 0, 1)
        }

# Global instance for use across the application
mobile_companion_manager = MobileCompanionManager()