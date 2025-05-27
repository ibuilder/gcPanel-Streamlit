"""
Pure Python Project Management Models for Highland Tower Development
Advanced project information, cost codes, and general conditions management

Integrated comprehensive project management features with Highland Tower data
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from enum import Enum

from .data_models import HIGHLAND_TOWER_PROJECT


class CSIDivision(Enum):
    """CSI MasterFormat Divisions"""
    DIVISION_00 = "00 - Procurement and Contracting Requirements"
    DIVISION_01 = "01 - General Requirements"
    DIVISION_02 = "02 - Existing Conditions"
    DIVISION_03 = "03 - Concrete"
    DIVISION_04 = "04 - Masonry"
    DIVISION_05 = "05 - Metals"
    DIVISION_06 = "06 - Wood, Plastics, and Composites"
    DIVISION_07 = "07 - Thermal and Moisture Protection"
    DIVISION_08 = "08 - Openings"
    DIVISION_09 = "09 - Finishes"
    DIVISION_10 = "10 - Specialties"
    DIVISION_11 = "11 - Equipment"
    DIVISION_12 = "12 - Furnishings"
    DIVISION_13 = "13 - Special Construction"
    DIVISION_14 = "14 - Conveying Equipment"
    DIVISION_21 = "21 - Fire Suppression"
    DIVISION_22 = "22 - Plumbing"
    DIVISION_23 = "23 - HVAC"
    DIVISION_26 = "26 - Electrical"
    DIVISION_27 = "27 - Communications"
    DIVISION_28 = "28 - Electronic Safety and Security"
    DIVISION_31 = "31 - Earthwork"
    DIVISION_32 = "32 - Exterior Improvements"
    DIVISION_33 = "33 - Utilities"


@dataclass
class ProjectInformation:
    """Highland Tower Development project information"""
    project_id: str
    project_name: str
    project_number: str
    client_name: str
    client_contact: str
    client_email: str
    client_phone: str
    project_address: str
    city: str
    state: str
    zip_code: str
    contract_amount: float
    contract_date: date
    start_date: date
    substantial_completion_date: date
    final_completion_date: date
    architect: str
    engineer: str
    general_contractor: str
    project_manager: str
    superintendent: str
    project_description: str
    building_type: str
    gross_square_footage: int
    stories_above_grade: int
    stories_below_grade: int
    parking_spaces: int
    occupancy_type: str
    construction_type: str
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class CostCode:
    """CSI Division-based cost code"""
    id: str
    code: str
    division: CSIDivision
    title: str
    description: str
    unit_of_measure: str
    estimated_cost: float
    actual_cost: float = 0.0
    committed_cost: float = 0.0
    budget_variance: float = 0.0
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    @property
    def remaining_budget(self) -> float:
        """Calculate remaining budget"""
        return self.estimated_cost - self.committed_cost - self.actual_cost
    
    @property
    def percent_complete(self) -> float:
        """Calculate percent complete based on actual costs"""
        if self.estimated_cost > 0:
            return (self.actual_cost / self.estimated_cost) * 100
        return 0.0


@dataclass
class GeneralCondition:
    """General conditions category"""
    id: str
    category: str
    title: str
    description: str
    monthly_cost: float
    total_months: int
    total_budgeted: float
    actual_cost: float = 0.0
    is_active: bool = True
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    @property
    def remaining_budget(self) -> float:
        """Calculate remaining budget for general condition"""
        return self.total_budgeted - self.actual_cost


@dataclass
class ScheduleOfValuesItem:
    """Schedule of Values line item"""
    id: str
    item_number: str
    description: str
    scheduled_value: float
    work_completed_from_previous: float = 0.0
    work_completed_this_period: float = 0.0
    materials_presently_stored: float = 0.0
    total_completed_and_stored: float = 0.0
    percent_complete: float = 0.0
    balance_to_finish: float = 0.0
    retainage: float = 0.0
    cost_code_id: Optional[str] = None
    
    def calculate_totals(self):
        """Calculate SOV totals"""
        self.total_completed_and_stored = (
            self.work_completed_from_previous + 
            self.work_completed_this_period + 
            self.materials_presently_stored
        )
        self.percent_complete = (
            (self.total_completed_and_stored / self.scheduled_value) * 100 
            if self.scheduled_value > 0 else 0
        )
        self.balance_to_finish = self.scheduled_value - self.total_completed_and_stored


@dataclass
class UserProfile:
    """User profile information"""
    user_id: str
    username: str
    email: str
    first_name: str
    last_name: str
    title: str
    department: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    notification_preferences: Dict[str, bool] = field(default_factory=dict)
    last_login: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def display_name(self) -> str:
        """Get display name for UI"""
        return self.full_name if self.first_name and self.last_name else self.username


# Highland Tower Development Project Information
HIGHLAND_TOWER_PROJECT_INFO = ProjectInformation(
    project_id="HTD-2024-001",
    project_name="Highland Tower Development",
    project_number="HTD-2024-001",
    client_name="Highland Development Group",
    client_contact="James Morrison",
    client_email="j.morrison@highland-dev.com",
    client_phone="(555) 123-4567",
    project_address="1500 Highland Avenue",
    city="San Francisco",
    state="CA",
    zip_code="94102",
    contract_amount=45500000.0,
    contract_date=date(2024, 1, 10),
    start_date=date(2024, 1, 15),
    substantial_completion_date=date(2025, 10, 15),
    final_completion_date=date(2025, 12, 31),
    architect="Highland Architecture Associates",
    engineer="Structural Engineering Partners",
    general_contractor="Highland Construction Corp",
    project_manager="Sarah Johnson",
    superintendent="Mike Chen",
    project_description="Mixed-use development featuring 120 residential units and 8 retail spaces across 17 stories",
    building_type="Mixed-Use Residential/Retail",
    gross_square_footage=485000,
    stories_above_grade=15,
    stories_below_grade=2,
    parking_spaces=140,
    occupancy_type="R-2 Residential, M Mercantile",
    construction_type="Type I Fire-Resistive"
)

# Highland Tower Cost Codes
HIGHLAND_TOWER_COST_CODES = [
    CostCode(
        id="HTD-CC-01",
        code="01-500",
        division=CSIDivision.DIVISION_01,
        title="Temporary Facilities and Controls",
        description="Site office, utilities, and temporary facilities",
        unit_of_measure="LS",
        estimated_cost=485000.0,
        actual_cost=312000.0,
        committed_cost=150000.0
    ),
    CostCode(
        id="HTD-CC-03",
        code="03-300",
        division=CSIDivision.DIVISION_03,
        title="Cast-in-Place Concrete",
        description="Structural concrete for foundations, columns, and slabs",
        unit_of_measure="CY",
        estimated_cost=2850000.0,
        actual_cost=1950000.0,
        committed_cost=780000.0
    ),
    CostCode(
        id="HTD-CC-05",
        code="05-120",
        division=CSIDivision.DIVISION_05,
        title="Structural Steel",
        description="Steel frame, beams, columns, and connections",
        unit_of_measure="TON",
        estimated_cost=4200000.0,
        actual_cost=2890000.0,
        committed_cost=1200000.0
    ),
    CostCode(
        id="HTD-CC-07",
        code="07-200",
        division=CSIDivision.DIVISION_07,
        title="Thermal Protection",
        description="Building insulation and vapor barriers",
        unit_of_measure="SF",
        estimated_cost=650000.0,
        actual_cost=285000.0,
        committed_cost=320000.0
    ),
    CostCode(
        id="HTD-CC-08",
        code="08-100",
        division=CSIDivision.DIVISION_08,
        title="Metal Doors and Frames",
        description="Interior and exterior doors and frames",
        unit_of_measure="EA",
        estimated_cost=420000.0,
        actual_cost=180000.0,
        committed_cost=200000.0
    ),
    CostCode(
        id="HTD-CC-09",
        code="09-250",
        division=CSIDivision.DIVISION_09,
        title="Gypsum Board",
        description="Interior partition walls and ceilings",
        unit_of_measure="SF",
        estimated_cost=890000.0,
        actual_cost=320000.0,
        committed_cost=480000.0
    ),
    CostCode(
        id="HTD-CC-23",
        code="23-050",
        division=CSIDivision.DIVISION_23,
        title="HVAC Systems",
        description="Heating, ventilation, and air conditioning systems",
        unit_of_measure="LS",
        estimated_cost=3200000.0,
        actual_cost=1450000.0,
        committed_cost=1600000.0
    ),
    CostCode(
        id="HTD-CC-26",
        code="26-050",
        division=CSIDivision.DIVISION_26,
        title="Electrical Systems",
        description="Power distribution, lighting, and low voltage systems",
        unit_of_measure="LS",
        estimated_cost=2100000.0,
        actual_cost=980000.0,
        committed_cost=950000.0
    )
]

# Highland Tower General Conditions
HIGHLAND_TOWER_GENERAL_CONDITIONS = [
    GeneralCondition(
        id="HTD-GC-01",
        category="Project Management",
        title="Project Management Team",
        description="Project manager, assistant PM, and administrative support",
        monthly_cost=32000.0,
        total_months=24,
        total_budgeted=768000.0,
        actual_cost=520000.0,
        notes="Includes project manager, assistant PM, and project coordinator"
    ),
    GeneralCondition(
        id="HTD-GC-02",
        category="Site Operations",
        title="Site Supervision",
        description="Superintendent and field supervision",
        monthly_cost=28000.0,
        total_months=24,
        total_budgeted=672000.0,
        actual_cost=448000.0,
        notes="Site superintendent and assistant superintendent"
    ),
    GeneralCondition(
        id="HTD-GC-03",
        category="Temporary Facilities",
        title="Site Office and Facilities",
        description="Temporary offices, utilities, and storage",
        monthly_cost=15000.0,
        total_months=24,
        total_budgeted=360000.0,
        actual_cost=240000.0,
        notes="Site office trailers, utilities, internet, and storage containers"
    ),
    GeneralCondition(
        id="HTD-GC-04",
        category="Safety",
        title="Safety Program",
        description="Safety officer, training, and equipment",
        monthly_cost=12000.0,
        total_months=24,
        total_budgeted=288000.0,
        actual_cost=192000.0,
        notes="Full-time safety officer and safety program implementation"
    ),
    GeneralCondition(
        id="HTD-GC-05",
        category="Quality Control",
        title="Quality Assurance",
        description="Quality control manager and testing",
        monthly_cost=8000.0,
        total_months=24,
        total_budgeted=192000.0,
        actual_cost=128000.0,
        notes="Quality control inspections and materials testing"
    )
]

# Highland Tower Schedule of Values
HIGHLAND_TOWER_SCHEDULE_OF_VALUES = [
    ScheduleOfValuesItem(
        id="HTD-SOV-01",
        item_number="001",
        description="General Requirements",
        scheduled_value=2280000.0,
        work_completed_from_previous=1950000.0,
        work_completed_this_period=150000.0,
        materials_presently_stored=0.0,
        cost_code_id="HTD-CC-01"
    ),
    ScheduleOfValuesItem(
        id="HTD-SOV-02",
        item_number="002",
        description="Concrete Work",
        scheduled_value=2850000.0,
        work_completed_from_previous=2100000.0,
        work_completed_this_period=320000.0,
        materials_presently_stored=85000.0,
        cost_code_id="HTD-CC-03"
    ),
    ScheduleOfValuesItem(
        id="HTD-SOV-03",
        item_number="003",
        description="Structural Steel",
        scheduled_value=4200000.0,
        work_completed_from_previous=2890000.0,
        work_completed_this_period=180000.0,
        materials_presently_stored=120000.0,
        cost_code_id="HTD-CC-05"
    )
]

# Calculate SOV totals
for sov_item in HIGHLAND_TOWER_SCHEDULE_OF_VALUES:
    sov_item.calculate_totals()

# Highland Tower User Profiles
HIGHLAND_TOWER_USER_PROFILES = [
    UserProfile(
        user_id="HTD-USER-001",
        username="s.johnson",
        email="s.johnson@highland-construction.com",
        first_name="Sarah",
        last_name="Johnson",
        title="Project Manager",
        department="Project Management",
        phone="(555) 234-5678",
        notification_preferences={
            "email_rfi_notifications": True,
            "email_clash_alerts": True,
            "email_progress_reports": True,
            "email_safety_incidents": True,
            "sms_critical_alerts": True
        }
    ),
    UserProfile(
        user_id="HTD-USER-002",
        username="m.chen",
        email="m.chen@highland-construction.com",
        first_name="Mike",
        last_name="Chen",
        title="Site Superintendent",
        department="Field Operations",
        phone="(555) 345-6789",
        notification_preferences={
            "email_rfi_notifications": True,
            "email_daily_reports": True,
            "email_safety_incidents": True,
            "sms_critical_alerts": True,
            "sms_weather_alerts": True
        }
    ),
    UserProfile(
        user_id="HTD-USER-003",
        username="admin",
        email="admin@highland-construction.com",
        first_name="Highland",
        last_name="Administrator",
        title="System Administrator",
        department="IT",
        notification_preferences={
            "email_system_alerts": True,
            "email_user_activity": False,
            "email_backup_reports": True
        }
    )
]