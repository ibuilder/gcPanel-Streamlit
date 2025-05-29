"""
Pure Python Preconstruction Management for Highland Tower Development
Advanced bidding, prequalification, and preconstruction services

Integrated from gcDeliver preconstruction and bidding capabilities
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from enum import Enum
import json

from .data_models import HIGHLAND_TOWER_PROJECT


class CompanyType(Enum):
    GENERAL_CONTRACTOR = "general_contractor"
    SUBCONTRACTOR = "subcontractor" 
    SUPPLIER = "supplier"
    CONSULTANT = "consultant"
    ARCHITECT = "architect"
    ENGINEER = "engineer"


class PrequalificationStatus(Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class BidStatus(Enum):
    INVITED = "invited"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    AWARDED = "awarded"
    DECLINED = "declined"


class InsuranceType(Enum):
    GENERAL_LIABILITY = "general_liability"
    WORKERS_COMP = "workers_compensation"
    AUTO_LIABILITY = "auto_liability"
    PROFESSIONAL_LIABILITY = "professional_liability"
    UMBRELLA = "umbrella"


@dataclass
class Company:
    """Company/Contractor database entry"""
    id: str
    name: str
    company_type: CompanyType
    contact_person: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip_code: str
    license_number: Optional[str]
    specialty_trades: List[str]
    years_in_business: int
    annual_revenue: float
    bonding_capacity: float
    emod_rate: float  # Experience Modification Rate
    safety_record_rating: float  # 1-5 scale
    references: List[Dict[str, str]]
    certifications: List[str]
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class InsuranceCertificate:
    """Insurance certificate tracking"""
    id: str
    company_id: str
    insurance_type: InsuranceType
    carrier_name: str
    policy_number: str
    coverage_amount: float
    effective_date: date
    expiration_date: date
    certificate_holder: str
    file_path: Optional[str]
    is_valid: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    @property
    def days_until_expiration(self) -> int:
        """Calculate days until expiration"""
        return (self.expiration_date - date.today()).days
    
    @property
    def is_expired(self) -> bool:
        """Check if certificate is expired"""
        return date.today() > self.expiration_date


@dataclass
class PrequalificationChecklist:
    """Prequalification checklist item"""
    id: str
    company_id: str
    category: str
    requirement: str
    description: str
    is_completed: bool = False
    completion_date: Optional[date] = None
    notes: str = ""
    file_attachments: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class BidPackage:
    """Bid package for Highland Tower trades"""
    id: str
    project_id: str
    package_name: str
    trade_category: str
    description: str
    scope_of_work: str
    estimated_value: float
    bid_due_date: date
    project_start_date: date
    project_completion_date: date
    bonding_required: bool
    insurance_requirements: List[InsuranceType]
    prequalification_required: bool
    status: BidStatus = BidStatus.INVITED
    invited_contractors: List[str] = field(default_factory=list)
    documents: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class BidSubmission:
    """Contractor bid submission"""
    id: str
    bid_package_id: str
    company_id: str
    base_bid_amount: float
    schedule_duration: int  # days
    warranty_period: int  # months
    alternate_bids: Dict[str, float] = field(default_factory=dict)
    unit_prices: Dict[str, float] = field(default_factory=dict)
    escalation_factors: Dict[str, float] = field(default_factory=dict)
    exclusions: List[str] = field(default_factory=list)
    clarifications: str = ""
    submitted_date: datetime = field(default_factory=datetime.now)
    status: BidStatus = BidStatus.SUBMITTED
    evaluation_score: float = 0.0
    ranking: int = 0
    awarded: bool = False


@dataclass
class BudgetLineItem:
    """Highland Tower budget line item tracking"""
    id: str
    project_id: str
    csi_division: str
    trade_category: str
    description: str
    quantity: float
    unit: str
    unit_cost: float
    total_estimated_cost: float
    actual_cost: float = 0.0
    committed_cost: float = 0.0
    variance: float = 0.0
    status: str = "planning"  # planning, bidding, awarded, complete
    awarded_contractor: Optional[str] = None
    contract_amount: Optional[float] = None
    notes: str = ""
    last_updated: datetime = field(default_factory=datetime.now)
    
    @property
    def remaining_budget(self) -> float:
        """Calculate remaining budget"""
        return self.total_estimated_cost - self.committed_cost - self.actual_cost
    
    @property
    def budget_variance_percentage(self) -> float:
        """Calculate budget variance percentage"""
        if self.total_estimated_cost > 0:
            return ((self.actual_cost + self.committed_cost - self.total_estimated_cost) / 
                   self.total_estimated_cost) * 100
        return 0.0


# Highland Tower Development Companies Database
HIGHLAND_TOWER_COMPANIES = [
    Company(
        id="HTD-COMP-001",
        name="Highland Steel Fabricators",
        company_type=CompanyType.SUBCONTRACTOR,
        contact_person="Robert Martinez",
        email="r.martinez@highland-steel.com",
        phone="(555) 234-5678",
        address="2500 Industrial Boulevard",
        city="San Francisco",
        state="CA",
        zip_code="94124",
        license_number="CA-B-789456",
        specialty_trades=["Structural Steel", "Metal Decking", "Miscellaneous Metals"],
        years_in_business=15,
        annual_revenue=12500000.0,
        bonding_capacity=25000000.0,
        emod_rate=0.85,
        safety_record_rating=4.5,
        references=[
            {"project": "Bay Tower Complex", "contact": "John Smith", "phone": "(555) 111-2222"},
            {"project": "Metro Office Building", "contact": "Sarah Lee", "phone": "(555) 333-4444"}
        ],
        certifications=["AISC Certified", "AWS D1.1 Certified", "OSHA 30"]
    ),
    Company(
        id="HTD-COMP-002",
        name="Elite Electrical Systems",
        company_type=CompanyType.SUBCONTRACTOR,
        contact_person="Jennifer Chen",
        email="j.chen@elite-electrical.com",
        phone="(555) 345-6789",
        address="1800 Electric Avenue",
        city="San Francisco",
        state="CA",
        zip_code="94107",
        license_number="CA-C10-654321",
        specialty_trades=["Electrical", "Low Voltage", "Fire Alarm", "Security Systems"],
        years_in_business=22,
        annual_revenue=8750000.0,
        bonding_capacity=15000000.0,
        emod_rate=0.92,
        safety_record_rating=4.8,
        references=[
            {"project": "Financial District Tower", "contact": "Mike Johnson", "phone": "(555) 555-6666"},
            {"project": "Mission Bay Development", "contact": "Lisa Wong", "phone": "(555) 777-8888"}
        ],
        certifications=["NECA Member", "IBEW Signatory", "NICET Certified"]
    ),
    Company(
        id="HTD-COMP-003",
        name="Premium Concrete Solutions",
        company_type=CompanyType.SUBCONTRACTOR,
        contact_person="David Thompson",
        email="d.thompson@premium-concrete.com", 
        phone="(555) 456-7890",
        address="3200 Concrete Way",
        city="San Francisco",
        state="CA",
        zip_code="94134",
        license_number="CA-A-987654",
        specialty_trades=["Concrete", "Formwork", "Post-Tensioning", "Concrete Repair"],
        years_in_business=18,
        annual_revenue=15200000.0,
        bonding_capacity=30000000.0,
        emod_rate=0.78,
        safety_record_rating=4.2,
        references=[
            {"project": "Residential High-Rise", "contact": "Amy Davis", "phone": "(555) 999-0000"},
            {"project": "Commercial Plaza", "contact": "Tom Wilson", "phone": "(555) 111-3333"}
        ],
        certifications=["ACI Certified", "PCI Certified", "Tilt-Up Certified"]
    )
]

# Highland Tower Insurance Certificates
HIGHLAND_TOWER_INSURANCE_CERTIFICATES = [
    InsuranceCertificate(
        id="HTD-INS-001",
        company_id="HTD-COMP-001",
        insurance_type=InsuranceType.GENERAL_LIABILITY,
        carrier_name="Zurich Insurance",
        policy_number="ZUR-GL-2024-5678",
        coverage_amount=2000000.0,
        effective_date=date(2024, 1, 1),
        expiration_date=date(2025, 1, 1),
        certificate_holder="Highland Tower Development",
        file_path="certificates/zurich_gl_2024.pdf"
    ),
    InsuranceCertificate(
        id="HTD-INS-002",
        company_id="HTD-COMP-001",
        insurance_type=InsuranceType.WORKERS_COMP,
        carrier_name="State Fund Insurance",
        policy_number="SF-WC-2024-9012",
        coverage_amount=1000000.0,
        effective_date=date(2024, 1, 1),
        expiration_date=date(2025, 1, 1),
        certificate_holder="Highland Tower Development",
        file_path="certificates/state_fund_wc_2024.pdf"
    ),
    InsuranceCertificate(
        id="HTD-INS-003",
        company_id="HTD-COMP-002",
        insurance_type=InsuranceType.GENERAL_LIABILITY,
        carrier_name="Liberty Mutual",
        policy_number="LM-GL-2024-3456",
        coverage_amount=2000000.0,
        effective_date=date(2024, 2, 1),
        expiration_date=date(2025, 2, 1),
        certificate_holder="Highland Tower Development",
        file_path="certificates/liberty_gl_2024.pdf"
    )
]

# Highland Tower Bid Packages
HIGHLAND_TOWER_BID_PACKAGES = [
    BidPackage(
        id="HTD-BID-001",
        project_id="HTD-2024-001",
        package_name="Structural Steel Package",
        trade_category="Structural Steel",
        description="Complete structural steel framework for Highland Tower",
        scope_of_work="Furnish and install all structural steel, metal decking, and connections",
        estimated_value=4200000.0,
        bid_due_date=date(2024, 3, 15),
        project_start_date=date(2024, 4, 1),
        project_completion_date=date(2024, 8, 31),
        bonding_required=True,
        insurance_requirements=[InsuranceType.GENERAL_LIABILITY, InsuranceType.WORKERS_COMP],
        prequalification_required=True,
        invited_contractors=["HTD-COMP-001"],
        documents=["structural_drawings.pdf", "specifications.pdf", "bid_form.pdf"]
    ),
    BidPackage(
        id="HTD-BID-002",
        project_id="HTD-2024-001",
        package_name="Electrical Systems Package",
        trade_category="Electrical",
        description="Complete electrical systems for Highland Tower",
        scope_of_work="Power distribution, lighting, fire alarm, and low voltage systems",
        estimated_value=2100000.0,
        bid_due_date=date(2024, 3, 20),
        project_start_date=date(2024, 5, 1),
        project_completion_date=date(2024, 10, 15),
        bonding_required=True,
        insurance_requirements=[InsuranceType.GENERAL_LIABILITY, InsuranceType.WORKERS_COMP],
        prequalification_required=True,
        invited_contractors=["HTD-COMP-002"],
        documents=["electrical_drawings.pdf", "specifications.pdf", "equipment_schedules.pdf"]
    )
]

# Highland Tower Budget Line Items
HIGHLAND_TOWER_BUDGET_ITEMS = [
    BudgetLineItem(
        id="HTD-BUDGET-001",
        project_id="HTD-2024-001",
        csi_division="05 - Metals",
        trade_category="Structural Steel",
        description="Structural steel framework",
        quantity=485.0,
        unit="Tons",
        unit_cost=8500.0,
        total_estimated_cost=4122500.0,
        committed_cost=4200000.0,
        status="awarded",
        awarded_contractor="Highland Steel Fabricators",
        contract_amount=4200000.0,
        notes="Contract awarded after competitive bidding process"
    ),
    BudgetLineItem(
        id="HTD-BUDGET-002",
        project_id="HTD-2024-001",
        csi_division="26 - Electrical",
        trade_category="Electrical Systems",
        description="Complete electrical package",
        quantity=1.0,
        unit="LS",
        unit_cost=2100000.0,
        total_estimated_cost=2100000.0,
        committed_cost=2050000.0,
        status="awarded",
        awarded_contractor="Elite Electrical Systems",
        contract_amount=2050000.0,
        notes="Value engineered to reduce costs by $50,000"
    ),
    BudgetLineItem(
        id="HTD-BUDGET-003",
        project_id="HTD-2024-001",
        csi_division="03 - Concrete",
        trade_category="Cast-in-Place Concrete",
        description="Structural concrete and formwork",
        quantity=2850.0,
        unit="CY",
        unit_cost=950.0,
        total_estimated_cost=2707500.0,
        actual_cost=1950000.0,
        committed_cost=750000.0,
        status="in_progress",
        awarded_contractor="Premium Concrete Solutions",
        contract_amount=2700000.0,
        notes="70% complete, on schedule and budget"
    )
]

# Highland Tower Prequalification Checklists
HIGHLAND_TOWER_PREQUALIFICATION_CHECKLISTS = [
    PrequalificationChecklist(
        id="HTD-PREQ-001",
        company_id="HTD-COMP-001",
        category="Financial",
        requirement="Audited Financial Statements",
        description="Provide last 3 years of audited financial statements",
        is_completed=True,
        completion_date=date(2024, 1, 15),
        notes="CPA firm: Johnson & Associates",
        file_attachments=["highland_steel_financials_2021-2023.pdf"]
    ),
    PrequalificationChecklist(
        id="HTD-PREQ-002",
        company_id="HTD-COMP-001",
        category="Bonding",
        requirement="Bonding Capacity Letter",
        description="Letter from surety confirming bonding capacity",
        is_completed=True,
        completion_date=date(2024, 1, 20),
        notes="Surety: Travelers Casualty and Surety Company",
        file_attachments=["bonding_capacity_letter.pdf"]
    ),
    PrequalificationChecklist(
        id="HTD-PREQ-003",
        company_id="HTD-COMP-001",
        category="Safety",
        requirement="Safety Program Documentation",
        description="Comprehensive safety program and OSHA 300 logs",
        is_completed=True,
        completion_date=date(2024, 1, 25),
        notes="Excellent safety record with 0.85 EMOD rate",
        file_attachments=["safety_program.pdf", "osha_300_logs.pdf"]
    )
]