"""
Highland Tower Development - Subcontractor Management Backend
Enterprise-grade subcontractor tracking with performance monitoring and contract management.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class SubcontractorStatus(Enum):
    ACTIVE = "Active"
    PREQUALIFIED = "Prequalified"
    BIDDING = "Bidding"
    AWARDED = "Awarded"
    MOBILIZING = "Mobilizing"
    ON_SITE = "On Site"
    DEMOBILIZING = "Demobilizing"
    COMPLETED = "Completed"
    TERMINATED = "Terminated"

class TradeCategory(Enum):
    CONCRETE = "Concrete & Masonry"
    STEEL = "Structural Steel"
    ROOFING = "Roofing & Waterproofing"
    ELECTRICAL = "Electrical"
    PLUMBING = "Plumbing"
    HVAC = "HVAC"
    DRYWALL = "Drywall & Finishes"
    FLOORING = "Flooring"
    GLAZING = "Glass & Glazing"
    ELEVATORS = "Elevators"
    LANDSCAPING = "Landscaping"
    SPECIALTY = "Specialty Trades"

class PerformanceRating(Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    SATISFACTORY = "Satisfactory"
    NEEDS_IMPROVEMENT = "Needs Improvement"
    UNSATISFACTORY = "Unsatisfactory"

@dataclass
class Insurance:
    """Insurance information"""
    policy_type: str
    carrier: str
    policy_number: str
    coverage_amount: float
    expiry_date: str
    certificate_received: bool

@dataclass
class SafetyRecord:
    """Safety performance record"""
    record_id: str
    date: str
    incident_type: str
    description: str
    severity: str
    corrective_action: str
    resolved: bool

@dataclass
class PerformanceReview:
    """Performance review record"""
    review_id: str
    review_date: str
    reviewer: str
    quality_rating: PerformanceRating
    schedule_rating: PerformanceRating
    safety_rating: PerformanceRating
    communication_rating: PerformanceRating
    overall_rating: PerformanceRating
    comments: str
    recommendations: str

@dataclass
class PaymentRecord:
    """Payment history record"""
    payment_id: str
    invoice_number: str
    invoice_date: str
    amount: float
    payment_date: Optional[str]
    status: str  # "Pending", "Approved", "Paid", "Disputed"
    notes: str

@dataclass
class Subcontractor:
    """Complete subcontractor record"""
    subcontractor_id: str
    company_code: str
    company_name: str
    trade_category: TradeCategory
    status: SubcontractorStatus
    
    # Contact information
    primary_contact: str
    contact_email: str
    contact_phone: str
    office_address: str
    
    # Business information
    business_license: str
    tax_id: str
    duns_number: Optional[str]
    website: Optional[str]
    years_in_business: int
    
    # Contract details
    contract_value: float
    contract_start_date: str
    contract_end_date: str
    scope_of_work: str
    
    # Project assignment
    project_name: str
    work_areas: List[str]
    current_phase: str
    
    # Performance metrics
    quality_score: float
    schedule_performance: float
    safety_score: float
    overall_rating: PerformanceRating
    
    # Financial
    total_invoiced: float
    total_paid: float
    amount_pending: float
    retention_held: float
    
    # Insurance and bonding
    insurance_policies: List[Insurance]
    bond_amount: float
    bond_expiry: Optional[str]
    
    # Safety and compliance
    safety_records: List[SafetyRecord]
    safety_orientation_complete: bool
    certifications: List[str]
    
    # Performance tracking
    performance_reviews: List[PerformanceReview]
    payment_history: List[PaymentRecord]
    
    # Key personnel
    project_manager: str
    superintendent: str
    safety_officer: Optional[str]
    
    # Equipment and resources
    equipment_on_site: List[str]
    crew_size: int
    
    # Notes and tracking
    prequalification_notes: str
    performance_notes: str
    contract_notes: str
    
    # Workflow
    prequalified_by: str
    awarded_by: Optional[str]
    created_by: str
    last_updated_by: str
    created_at: str
    updated_at: str
    
    def calculate_payment_percentage(self) -> float:
        """Calculate percentage of contract paid"""
        if self.contract_value > 0:
            return (self.total_paid / self.contract_value) * 100
        return 0.0
    
    def is_insurance_current(self) -> bool:
        """Check if all insurance policies are current"""
        today = date.today()
        for insurance in self.insurance_policies:
            expiry = datetime.strptime(insurance.expiry_date, '%Y-%m-%d').date()
            if expiry <= today:
                return False
        return True
    
    def needs_performance_review(self) -> bool:
        """Check if subcontractor needs performance review"""
        if not self.performance_reviews:
            return True
        
        last_review = max(self.performance_reviews, key=lambda r: r.review_date)
        last_review_date = datetime.strptime(last_review.review_date, '%Y-%m-%d').date()
        return (date.today() - last_review_date).days > 90  # Review every 90 days

class SubcontractorManager:
    """Enterprise subcontractor management system"""
    
    def __init__(self):
        self.subcontractors: Dict[str, Subcontractor] = {}
        self.next_company_code = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample subcontractor data"""
        
        # Sample subcontractor 1 - Steel Fabricator
        sample_sub_1 = Subcontractor(
            subcontractor_id="sub-001",
            company_code="HTD-SUB-001",
            company_name="Steel Fabricators Inc.",
            trade_category=TradeCategory.STEEL,
            status=SubcontractorStatus.ON_SITE,
            primary_contact="Lisa Chen",
            contact_email="lchen@steelfab.com",
            contact_phone="555-234-5678",
            office_address="1500 Industrial Blvd, Highland, CA 92346",
            business_license="BL-2023-5678",
            tax_id="12-3456789",
            duns_number="123456789",
            website="www.steelfabricators.com",
            years_in_business=15,
            contract_value=2850000.0,
            contract_start_date="2024-09-01",
            contract_end_date="2025-12-31",
            scope_of_work="Structural steel fabrication and installation for levels 1-15",
            project_name="Highland Tower Development",
            work_areas=["Levels 1-15", "Core Structure", "Perimeter Frame"],
            current_phase="Steel Installation - Levels 11-15",
            quality_score=92.5,
            schedule_performance=88.0,
            safety_score=95.0,
            overall_rating=PerformanceRating.EXCELLENT,
            total_invoiced=2280000.0,
            total_paid=1995000.0,
            amount_pending=285000.0,
            retention_held=142500.0,
            insurance_policies=[
                Insurance(
                    policy_type="General Liability",
                    carrier="Construction Insurance Co.",
                    policy_number="GL-2024-SF-001",
                    coverage_amount=2000000.0,
                    expiry_date="2025-12-31",
                    certificate_received=True
                ),
                Insurance(
                    policy_type="Workers Compensation",
                    carrier="Workers Comp LLC",
                    policy_number="WC-2024-SF-001",
                    coverage_amount=1000000.0,
                    expiry_date="2025-12-31",
                    certificate_received=True
                )
            ],
            bond_amount=285000.0,
            bond_expiry="2025-12-31",
            safety_records=[
                SafetyRecord(
                    record_id="sr-001",
                    date="2025-04-15",
                    incident_type="Near Miss",
                    description="Load almost dropped during crane operation",
                    severity="Low",
                    corrective_action="Additional rigging training provided",
                    resolved=True
                )
            ],
            safety_orientation_complete=True,
            certifications=["AWS Certified Welders", "AISC Certified Fabricator", "OSHA 30-Hour"],
            performance_reviews=[
                PerformanceReview(
                    review_id="pr-001",
                    review_date="2025-03-31",
                    reviewer="John Smith - Project Manager",
                    quality_rating=PerformanceRating.EXCELLENT,
                    schedule_rating=PerformanceRating.GOOD,
                    safety_rating=PerformanceRating.EXCELLENT,
                    communication_rating=PerformanceRating.EXCELLENT,
                    overall_rating=PerformanceRating.EXCELLENT,
                    comments="Outstanding work quality, minor schedule delays due to weather",
                    recommendations="Continue current practices, improve weather contingency planning"
                )
            ],
            payment_history=[
                PaymentRecord(
                    payment_id="pay-001",
                    invoice_number="SF-INV-2025-015",
                    invoice_date="2025-05-01",
                    amount=285000.0,
                    payment_date=None,
                    status="Approved",
                    notes="Level 11-12 completion payment"
                )
            ],
            project_manager="Robert Williams",
            superintendent="Mike Rodriguez",
            safety_officer="Sarah Johnson",
            equipment_on_site=["Tower Crane", "Welding Equipment", "Material Hoists"],
            crew_size=24,
            prequalification_notes="Excellent references, strong financial position, experienced crew",
            performance_notes="Consistently exceeds quality standards, good communication",
            contract_notes="Standard terms, 5% retention, monthly progress payments",
            prequalified_by="Tom Brown - Procurement Manager",
            awarded_by="John Smith - Project Manager",
            created_by="Tom Brown - Procurement Manager",
            last_updated_by="John Smith - Project Manager",
            created_at="2024-06-15 10:00:00",
            updated_at="2025-05-27 14:30:00"
        )
        
        # Sample subcontractor 2 - HVAC Contractor
        sample_sub_2 = Subcontractor(
            subcontractor_id="sub-002",
            company_code="HTD-SUB-002",
            company_name="HVAC Systems LLC",
            trade_category=TradeCategory.HVAC,
            status=SubcontractorStatus.AWARDED,
            primary_contact="Robert Martinez",
            contact_email="rmartinez@hvacsystems.com",
            contact_phone="555-345-6789",
            office_address="2200 Climate Way, Highland, CA 92346",
            business_license="BL-2023-7890",
            tax_id="23-4567890",
            duns_number="234567890",
            website="www.hvacsystems.com",
            years_in_business=12,
            contract_value=1850000.0,
            contract_start_date="2025-06-01",
            contract_end_date="2026-04-30",
            scope_of_work="Complete HVAC system installation including rooftop units, ductwork, and controls",
            project_name="Highland Tower Development",
            work_areas=["All Levels", "Rooftop", "Mechanical Rooms"],
            current_phase="Pre-Construction Planning",
            quality_score=87.0,
            schedule_performance=91.0,
            safety_score=89.0,
            overall_rating=PerformanceRating.GOOD,
            total_invoiced=0.0,
            total_paid=0.0,
            amount_pending=0.0,
            retention_held=0.0,
            insurance_policies=[
                Insurance(
                    policy_type="General Liability",
                    carrier="Mechanical Contractors Insurance",
                    policy_number="GL-2025-HVAC-001",
                    coverage_amount=1500000.0,
                    expiry_date="2026-05-31",
                    certificate_received=True
                ),
                Insurance(
                    policy_type="Workers Compensation",
                    carrier="Trade Specific Insurance",
                    policy_number="WC-2025-HVAC-001",
                    coverage_amount=1000000.0,
                    expiry_date="2026-05-31",
                    certificate_received=True
                )
            ],
            bond_amount=185000.0,
            bond_expiry="2026-04-30",
            safety_records=[],
            safety_orientation_complete=False,
            certifications=["EPA Section 608", "NATE Certified", "OSHA 10-Hour"],
            performance_reviews=[
                PerformanceReview(
                    review_id="pr-002",
                    review_date="2025-05-15",
                    reviewer="Tom Brown - MEP Manager",
                    quality_rating=PerformanceRating.GOOD,
                    schedule_rating=PerformanceRating.EXCELLENT,
                    safety_rating=PerformanceRating.GOOD,
                    communication_rating=PerformanceRating.GOOD,
                    overall_rating=PerformanceRating.GOOD,
                    comments="Good performance on previous projects, reliable schedule adherence",
                    recommendations="Ensure safety training is up to date before mobilization"
                )
            ],
            payment_history=[],
            project_manager="Carlos Mendez",
            superintendent="David Kim",
            safety_officer=None,
            equipment_on_site=[],
            crew_size=0,
            prequalification_notes="Strong mechanical background, good references from similar projects",
            performance_notes="Reliable contractor with good track record",
            contract_notes="Net 30 payment terms, 10% retention, performance bonuses available",
            prequalified_by="Tom Brown - MEP Manager",
            awarded_by="John Smith - Project Manager",
            created_by="Tom Brown - MEP Manager",
            last_updated_by="Tom Brown - MEP Manager",
            created_at="2025-04-01 09:00:00",
            updated_at="2025-05-15 11:15:00"
        )
        
        # Sample subcontractor 3 - Electrical Contractor (Bidding)
        sample_sub_3 = Subcontractor(
            subcontractor_id="sub-003",
            company_code="HTD-SUB-003",
            company_name="Power Systems Inc.",
            trade_category=TradeCategory.ELECTRICAL,
            status=SubcontractorStatus.BIDDING,
            primary_contact="Jennifer Adams",
            contact_email="jadams@powersystems.com",
            contact_phone="555-456-7890",
            office_address="3300 Electric Ave, Highland, CA 92346",
            business_license="BL-2023-9012",
            tax_id="34-5678901",
            duns_number="345678901",
            website="www.powersystemsinc.com",
            years_in_business=20,
            contract_value=0.0,  # Still bidding
            contract_start_date="2025-07-01",
            contract_end_date="2026-06-30",
            scope_of_work="Complete electrical system installation including panels, wiring, lighting, and emergency systems",
            project_name="Highland Tower Development",
            work_areas=["All Levels", "Electrical Rooms", "Emergency Systems"],
            current_phase="Bid Preparation",
            quality_score=94.0,
            schedule_performance=86.0,
            safety_score=92.0,
            overall_rating=PerformanceRating.EXCELLENT,
            total_invoiced=0.0,
            total_paid=0.0,
            amount_pending=0.0,
            retention_held=0.0,
            insurance_policies=[
                Insurance(
                    policy_type="General Liability",
                    carrier="Electrical Contractors Mutual",
                    policy_number="GL-2025-ELEC-001",
                    coverage_amount=2000000.0,
                    expiry_date="2026-07-31",
                    certificate_received=True
                )
            ],
            bond_amount=0.0,  # Will be required upon award
            bond_expiry=None,
            safety_records=[],
            safety_orientation_complete=False,
            certifications=["Master Electrician License", "IBEW Local 640", "NECA Member"],
            performance_reviews=[
                PerformanceReview(
                    review_id="pr-003",
                    review_date="2025-05-20",
                    reviewer="Mike Johnson - Electrical Engineer",
                    quality_rating=PerformanceRating.EXCELLENT,
                    schedule_rating=PerformanceRating.GOOD,
                    safety_rating=PerformanceRating.EXCELLENT,
                    communication_rating=PerformanceRating.EXCELLENT,
                    overall_rating=PerformanceRating.EXCELLENT,
                    comments="Top-tier electrical contractor with excellent technical capabilities",
                    recommendations="Preferred bidder based on qualifications and past performance"
                )
            ],
            payment_history=[],
            project_manager="Mark Thompson",
            superintendent="Steve Wilson",
            safety_officer="Linda Garcia",
            equipment_on_site=[],
            crew_size=0,
            prequalification_notes="Premier electrical contractor, extensive high-rise experience",
            performance_notes="Consistently delivers high-quality work on schedule",
            contract_notes="Bidding on electrical package, decision pending",
            prequalified_by="Mike Johnson - Electrical Engineer",
            awarded_by=None,
            created_by="Mike Johnson - Electrical Engineer",
            last_updated_by="Mike Johnson - Electrical Engineer",
            created_at="2025-03-01 14:00:00",
            updated_at="2025-05-20 09:45:00"
        )
        
        self.subcontractors[sample_sub_1.subcontractor_id] = sample_sub_1
        self.subcontractors[sample_sub_2.subcontractor_id] = sample_sub_2
        self.subcontractors[sample_sub_3.subcontractor_id] = sample_sub_3
        self.next_company_code = 4
    
    def create_subcontractor(self, subcontractor_data: Dict[str, Any]) -> str:
        """Create a new subcontractor record"""
        subcontractor_id = f"sub-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        company_code = f"HTD-SUB-{self.next_company_code:03d}"
        
        subcontractor_data.update({
            "subcontractor_id": subcontractor_id,
            "company_code": company_code,
            "status": SubcontractorStatus.PREQUALIFIED,
            "total_invoiced": 0.0,
            "total_paid": 0.0,
            "amount_pending": 0.0,
            "retention_held": 0.0,
            "insurance_policies": [],
            "safety_records": [],
            "performance_reviews": [],
            "payment_history": [],
            "equipment_on_site": [],
            "crew_size": 0,
            "safety_orientation_complete": False,
            "awarded_by": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        subcontractor_data["trade_category"] = TradeCategory(subcontractor_data["trade_category"])
        subcontractor_data["status"] = SubcontractorStatus(subcontractor_data["status"])
        subcontractor_data["overall_rating"] = PerformanceRating(subcontractor_data.get("overall_rating", "Satisfactory"))
        
        subcontractor = Subcontractor(**subcontractor_data)
        self.subcontractors[subcontractor_id] = subcontractor
        self.next_company_code += 1
        
        return subcontractor_id
    
    def get_subcontractor(self, subcontractor_id: str) -> Optional[Subcontractor]:
        """Get a specific subcontractor"""
        return self.subcontractors.get(subcontractor_id)
    
    def get_all_subcontractors(self) -> List[Subcontractor]:
        """Get all subcontractors sorted by company name"""
        return sorted(self.subcontractors.values(),
                     key=lambda s: s.company_name)
    
    def get_subcontractors_by_status(self, status: SubcontractorStatus) -> List[Subcontractor]:
        """Get subcontractors by status"""
        return [sub for sub in self.subcontractors.values() if sub.status == status]
    
    def get_subcontractors_by_trade(self, trade: TradeCategory) -> List[Subcontractor]:
        """Get subcontractors by trade category"""
        return [sub for sub in self.subcontractors.values() if sub.trade_category == trade]
    
    def get_subcontractors_needing_review(self) -> List[Subcontractor]:
        """Get subcontractors that need performance review"""
        return [sub for sub in self.subcontractors.values() if sub.needs_performance_review()]
    
    def get_insurance_expiring_soon(self) -> List[Subcontractor]:
        """Get subcontractors with insurance expiring within 30 days"""
        expiring_soon = []
        thirty_days = date.today() + timedelta(days=30)
        
        for sub in self.subcontractors.values():
            for insurance in sub.insurance_policies:
                expiry = datetime.strptime(insurance.expiry_date, '%Y-%m-%d').date()
                if expiry <= thirty_days:
                    expiring_soon.append(sub)
                    break
        
        return expiring_soon
    
    def add_performance_review(self, subcontractor_id: str, review_data: Dict[str, Any]) -> bool:
        """Add a performance review to subcontractor"""
        subcontractor = self.subcontractors.get(subcontractor_id)
        if not subcontractor:
            return False
        
        review_id = f"pr-{len(subcontractor.performance_reviews) + 1:03d}"
        review_data.update({"review_id": review_id})
        
        # Convert enum ratings
        for rating_field in ['quality_rating', 'schedule_rating', 'safety_rating', 'communication_rating', 'overall_rating']:
            if rating_field in review_data:
                review_data[rating_field] = PerformanceRating(review_data[rating_field])
        
        review = PerformanceReview(**review_data)
        subcontractor.performance_reviews.append(review)
        
        # Update overall rating
        subcontractor.overall_rating = review.overall_rating
        subcontractor.updated_at = datetime.now().isoformat()
        
        return True
    
    def add_payment_record(self, subcontractor_id: str, payment_data: Dict[str, Any]) -> bool:
        """Add a payment record to subcontractor"""
        subcontractor = self.subcontractors.get(subcontractor_id)
        if not subcontractor:
            return False
        
        payment_id = f"pay-{len(subcontractor.payment_history) + 1:03d}"
        payment_data.update({"payment_id": payment_id})
        
        payment = PaymentRecord(**payment_data)
        subcontractor.payment_history.append(payment)
        
        # Update financial totals
        subcontractor.total_invoiced += payment.amount
        if payment.status == "Paid":
            subcontractor.total_paid += payment.amount
        else:
            subcontractor.amount_pending += payment.amount
        
        subcontractor.updated_at = datetime.now().isoformat()
        return True
    
    def generate_subcontractor_metrics(self) -> Dict[str, Any]:
        """Generate subcontractor management metrics"""
        subcontractors = list(self.subcontractors.values())
        
        if not subcontractors:
            return {}
        
        total_subcontractors = len(subcontractors)
        
        # Status counts
        status_counts = {}
        for status in SubcontractorStatus:
            status_counts[status.value] = len([s for s in subcontractors if s.status == status])
        
        # Trade counts
        trade_counts = {}
        for trade in TradeCategory:
            trade_counts[trade.value] = len([s for s in subcontractors if s.trade_category == trade])
        
        # Performance metrics
        active_subs = [s for s in subcontractors if s.status in [SubcontractorStatus.ACTIVE, SubcontractorStatus.ON_SITE]]
        avg_quality = sum(s.quality_score for s in active_subs) / len(active_subs) if active_subs else 0
        avg_schedule = sum(s.schedule_performance for s in active_subs) / len(active_subs) if active_subs else 0
        avg_safety = sum(s.safety_score for s in active_subs) / len(active_subs) if active_subs else 0
        
        # Financial metrics
        total_contract_value = sum(s.contract_value for s in subcontractors if s.contract_value > 0)
        total_paid = sum(s.total_paid for s in subcontractors)
        total_pending = sum(s.amount_pending for s in subcontractors)
        
        # Issues needing attention
        needing_review = len(self.get_subcontractors_needing_review())
        insurance_expiring = len(self.get_insurance_expiring_soon())
        
        return {
            "total_subcontractors": total_subcontractors,
            "status_breakdown": status_counts,
            "trade_breakdown": trade_counts,
            "average_quality_score": round(avg_quality, 1),
            "average_schedule_performance": round(avg_schedule, 1),
            "average_safety_score": round(avg_safety, 1),
            "total_contract_value": total_contract_value,
            "total_paid": total_paid,
            "total_pending": total_pending,
            "needing_performance_review": needing_review,
            "insurance_expiring_soon": insurance_expiring,
            "active_subcontractors": status_counts.get("On Site", 0) + status_counts.get("Active", 0),
            "awarded_contracts": status_counts.get("Awarded", 0)
        }

# Global instance for use across the application
subcontractor_manager = SubcontractorManager()