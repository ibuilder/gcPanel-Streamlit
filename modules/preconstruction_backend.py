"""
Highland Tower Development - Preconstruction Backend
Enterprise-grade preconstruction planning, estimating, and procurement management.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class EstimateStatus(Enum):
    DRAFT = "Draft"
    IN_REVIEW = "In Review"
    APPROVED = "Approved"
    FINAL = "Final"
    SUPERSEDED = "Superseded"

class BidStatus(Enum):
    PREPARING = "Preparing"
    OPEN = "Open"
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    AWARDED = "Awarded"
    DECLINED = "Declined"

@dataclass
class CostEstimate:
    """Project cost estimate record"""
    estimate_id: str
    estimate_code: str
    estimate_name: str
    
    # Project information
    project_phase: str
    trade: str
    scope_description: str
    
    # Estimate details
    base_cost: float
    contingency_percentage: float
    contingency_amount: float
    overhead_percentage: float
    overhead_amount: float
    profit_percentage: float
    profit_amount: float
    total_estimate: float
    
    # Status and workflow
    status: EstimateStatus
    accuracy_level: str  # "Order of Magnitude", "Budget", "Definitive"
    confidence_level: int  # 1-100%
    
    # Responsibility
    estimator: str
    reviewed_by: Optional[str]
    approved_by: Optional[str]
    
    # Dates
    estimate_date: str
    review_date: Optional[str]
    approval_date: Optional[str]
    
    # Cost breakdown
    labor_cost: float
    material_cost: float
    equipment_cost: float
    subcontractor_cost: float
    other_costs: float
    
    # Market conditions
    escalation_percentage: float
    market_conditions: str
    risk_factors: List[str]
    
    # Notes and assumptions
    assumptions: List[str]
    exclusions: List[str]
    notes: str
    
    # Workflow tracking
    created_at: str
    updated_at: str

@dataclass
class BidPackage:
    """Bid package for subcontractor procurement"""
    package_id: str
    package_code: str
    package_name: str
    
    # Scope and requirements
    trade: str
    scope_description: str
    technical_requirements: List[str]
    performance_requirements: List[str]
    
    # Bidding process
    status: BidStatus
    bid_due_date: str
    pre_bid_meeting_date: Optional[str]
    site_visit_required: bool
    
    # Financial details
    estimated_value: float
    budget_range_low: float
    budget_range_high: float
    
    # Invited bidders
    invited_contractors: List[str]
    submitted_bids: List[Dict[str, Any]]
    
    # Documents and requirements
    required_documents: List[str]
    specifications: List[str]
    drawings_included: List[str]
    
    # Evaluation criteria
    evaluation_criteria: Dict[str, int]  # criteria: weight percentage
    technical_score_weight: int
    price_score_weight: int
    
    # Award information
    awarded_contractor: Optional[str]
    awarded_amount: Optional[float]
    award_date: Optional[str]
    
    # Timeline
    mobilization_date: Optional[str]
    substantial_completion_date: Optional[str]
    
    # Contact and workflow
    procurement_manager: str
    created_by: str
    
    # Notes
    bid_notes: str
    award_justification: str
    
    # Workflow tracking
    created_at: str
    updated_at: str

@dataclass
class VendorProfile:
    """Vendor/subcontractor profile"""
    vendor_id: str
    company_name: str
    
    # Contact information
    primary_contact: str
    phone: str
    email: str
    address: str
    
    # Business information
    business_type: str  # "Corporation", "LLC", "Partnership", "Sole Proprietorship"
    years_in_business: int
    annual_revenue: float
    employee_count: int
    
    # Certifications and qualifications
    licenses: List[str]
    certifications: List[str]
    insurance_coverage: Dict[str, float]
    bonding_capacity: float
    
    # Trade specializations
    primary_trades: List[str]
    secondary_trades: List[str]
    geographic_coverage: List[str]
    
    # Performance history
    projects_completed: int
    safety_rating: float
    quality_rating: float
    schedule_performance: float
    
    # Financial information
    credit_rating: str
    payment_terms: str
    preferred_project_size_min: float
    preferred_project_size_max: float
    
    # Prequalification status
    prequalified: bool
    prequalification_date: Optional[str]
    prequalification_expiry: Optional[str]
    
    # Notes and tracking
    vendor_notes: str
    relationship_manager: str
    
    # Workflow tracking
    created_at: str
    updated_at: str

class PreconstructionManager:
    """Enterprise preconstruction management system"""
    
    def __init__(self):
        self.estimates: Dict[str, CostEstimate] = {}
        self.bid_packages: Dict[str, BidPackage] = {}
        self.vendors: Dict[str, VendorProfile] = {}
        self.next_estimate_code = 1
        self.next_package_code = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample preconstruction data"""
        
        # Sample Cost Estimates
        sample_estimates = [
            CostEstimate(
                estimate_id="est-001",
                estimate_code="HTD-EST-001",
                estimate_name="Highland Tower - Structural Steel Estimate",
                project_phase="Design Development",
                trade="Structural Steel",
                scope_description="Complete structural steel frame for 15-story mixed-use building",
                base_cost=2850000.0,
                contingency_percentage=8.0,
                contingency_amount=228000.0,
                overhead_percentage=12.0,
                overhead_amount=369360.0,
                profit_percentage=6.0,
                profit_amount=207921.6,
                total_estimate=3655281.6,
                status=EstimateStatus.APPROVED,
                accuracy_level="Definitive",
                confidence_level=92,
                estimator="Mike Rodriguez - Chief Estimator",
                reviewed_by="Tom Brown - Project Manager",
                approved_by="John Smith - VP Construction",
                estimate_date="2025-04-15",
                review_date="2025-04-18",
                approval_date="2025-04-20",
                labor_cost=1425000.0,
                material_cost=1140000.0,
                equipment_cost=142500.0,
                subcontractor_cost=0.0,
                other_costs=142500.0,
                escalation_percentage=3.5,
                market_conditions="Steel prices stable, labor market tight",
                risk_factors=["Weather delays", "Material delivery schedules", "Crane availability"],
                assumptions=["Standard 40-hour work week", "No overtime premium", "Material delivered to site"],
                exclusions=["Site preparation", "Concrete foundations", "Architectural connections"],
                notes="Estimate based on 75% complete design documents. Final quantities subject to design completion.",
                created_at="2025-04-15 09:00:00",
                updated_at="2025-04-20 16:30:00"
            ),
            CostEstimate(
                estimate_id="est-002",
                estimate_code="HTD-EST-002",
                estimate_name="Highland Tower - HVAC Systems Estimate",
                project_phase="Construction Documents",
                trade="HVAC",
                scope_description="Complete HVAC systems including chillers, boilers, and VAV distribution",
                base_cost=1850000.0,
                contingency_percentage=10.0,
                contingency_amount=185000.0,
                overhead_percentage=15.0,
                overhead_amount=305250.0,
                profit_percentage=8.0,
                profit_amount=187220.0,
                total_estimate=2527470.0,
                status=EstimateStatus.IN_REVIEW,
                accuracy_level="Budget",
                confidence_level=85,
                estimator="Lisa Park - MEP Estimator",
                reviewed_by="Tom Brown - Project Manager",
                approved_by=None,
                estimate_date="2025-05-10",
                review_date="2025-05-15",
                approval_date=None,
                labor_cost=740000.0,
                material_cost=925000.0,
                equipment_cost=111000.0,
                subcontractor_cost=37000.0,
                other_costs=37000.0,
                escalation_percentage=4.2,
                market_conditions="HVAC equipment lead times extended, energy efficiency incentives available",
                risk_factors=["Equipment delivery delays", "Complexity of controls integration", "Energy code compliance"],
                assumptions=["Union labor rates", "Equipment delivered and rigged", "Standard warranty terms"],
                exclusions=["Electrical connections", "Structural supports", "Architectural finishes"],
                notes="Estimate includes high-efficiency systems for LEED certification requirements.",
                created_at="2025-05-10 10:30:00",
                updated_at="2025-05-15 14:15:00"
            )
        ]
        
        for estimate in sample_estimates:
            self.estimates[estimate.estimate_id] = estimate
        
        # Sample Bid Packages
        sample_packages = [
            BidPackage(
                package_id="pkg-001",
                package_code="HTD-PKG-001",
                package_name="Highland Tower - Electrical Systems",
                trade="Electrical",
                scope_description="Complete electrical systems including service, distribution, lighting, and power",
                technical_requirements=["NEC compliance", "Energy efficient lighting", "Smart building integration"],
                performance_requirements=["99.9% uptime", "LEED Gold compliance", "25-year equipment life"],
                status=BidStatus.AWARDED,
                bid_due_date="2025-04-30",
                pre_bid_meeting_date="2025-04-15",
                site_visit_required=True,
                estimated_value=1650000.0,
                budget_range_low=1500000.0,
                budget_range_high=1800000.0,
                invited_contractors=["Power Systems Inc.", "Electrical Solutions LLC", "Metro Electric Co."],
                submitted_bids=[
                    {"contractor": "Power Systems Inc.", "amount": 1625000.0, "submitted_date": "2025-04-30"},
                    {"contractor": "Electrical Solutions LLC", "amount": 1685000.0, "submitted_date": "2025-04-29"},
                    {"contractor": "Metro Electric Co.", "amount": 1710000.0, "submitted_date": "2025-04-30"}
                ],
                required_documents=["Electrical drawings", "Specifications", "Equipment cut sheets"],
                specifications=["Division 26 - Electrical", "Smart building controls spec"],
                drawings_included=["E1.0-E8.5", "Lighting plans", "Power distribution"],
                evaluation_criteria={"Technical Approach": 40, "Experience": 25, "Schedule": 15, "Price": 20},
                technical_score_weight=80,
                price_score_weight=20,
                awarded_contractor="Power Systems Inc.",
                awarded_amount=1625000.0,
                award_date="2025-05-05",
                mobilization_date="2025-06-01",
                substantial_completion_date="2025-11-15",
                procurement_manager="Tom Brown - Project Manager",
                created_by="Highland Construction Team",
                bid_notes="Strong competition with good pricing. All bidders qualified.",
                award_justification="Power Systems provided best value with superior technical approach and competitive pricing.",
                created_at="2025-04-01 08:00:00",
                updated_at="2025-05-05 16:45:00"
            ),
            BidPackage(
                package_id="pkg-002",
                package_code="HTD-PKG-002",
                package_name="Highland Tower - Exterior Envelope",
                trade="Curtain Wall",
                scope_description="Design-build curtain wall system with high-performance glazing",
                technical_requirements=["Thermal performance", "Wind load resistance", "Seismic compliance"],
                performance_requirements=["U-factor 0.25", "Air infiltration < 0.06 cfm/sf", "50-year life"],
                status=BidStatus.UNDER_REVIEW,
                bid_due_date="2025-06-15",
                pre_bid_meeting_date="2025-05-30",
                site_visit_required=True,
                estimated_value=3200000.0,
                budget_range_low=2800000.0,
                budget_range_high=3600000.0,
                invited_contractors=["Glass Systems Corp.", "Envelope Solutions Inc.", "Curtain Wall Specialists"],
                submitted_bids=[
                    {"contractor": "Glass Systems Corp.", "amount": 3150000.0, "submitted_date": "2025-06-14"},
                    {"contractor": "Envelope Solutions Inc.", "amount": 3280000.0, "submitted_date": "2025-06-15"}
                ],
                required_documents=["Design calculations", "Mock-up requirements", "Performance test data"],
                specifications=["Division 08 - Openings", "Curtain wall performance spec"],
                drawings_included=["A4.0-A4.8", "Curtain wall details", "Glazing schedule"],
                evaluation_criteria={"Design Approach": 35, "Performance": 30, "Experience": 20, "Price": 15},
                technical_score_weight=85,
                price_score_weight=15,
                awarded_contractor=None,
                awarded_amount=None,
                award_date=None,
                mobilization_date="2025-08-01",
                substantial_completion_date="2025-12-31",
                procurement_manager="Sarah Wilson - Procurement",
                created_by="Highland Construction Team",
                bid_notes="High-performance envelope critical for energy efficiency goals.",
                award_justification="",
                created_at="2025-05-01 09:30:00",
                updated_at="2025-06-15 17:00:00"
            )
        ]
        
        for package in sample_packages:
            self.bid_packages[package.package_id] = package
        
        # Sample Vendor Profiles
        sample_vendors = [
            VendorProfile(
                vendor_id="vendor-001",
                company_name="Steel Fabricators Inc.",
                primary_contact="Robert Martinez - Project Manager",
                phone="(555) 234-5678",
                email="rmartinez@steelfab.com",
                address="1234 Industrial Blvd, Construction City, CC 12345",
                business_type="Corporation",
                years_in_business=28,
                annual_revenue=45000000.0,
                employee_count=185,
                licenses=["General Contractor Class A", "Structural Steel Fabricator"],
                certifications=["AISC Certified Fabricator", "AWS D1.1 Certified"],
                insurance_coverage={"General Liability": 5000000.0, "Professional": 2000000.0, "Workers Comp": 1000000.0},
                bonding_capacity=25000000.0,
                primary_trades=["Structural Steel", "Miscellaneous Metals"],
                secondary_trades=["Metal Decking", "Steel Stairs"],
                geographic_coverage=["Metro Area", "State Region", "Regional Multi-State"],
                projects_completed=347,
                safety_rating=4.8,
                quality_rating=4.6,
                schedule_performance=4.7,
                credit_rating="A-",
                payment_terms="Net 30",
                preferred_project_size_min=500000.0,
                preferred_project_size_max=15000000.0,
                prequalified=True,
                prequalification_date="2024-12-15",
                prequalification_expiry="2025-12-15",
                vendor_notes="Excellent structural steel contractor with strong safety record. Preferred vendor for complex projects.",
                relationship_manager="Tom Brown - Project Manager",
                created_at="2024-12-15 10:00:00",
                updated_at="2025-05-20 14:30:00"
            ),
            VendorProfile(
                vendor_id="vendor-002",
                company_name="Power Systems Inc.",
                primary_contact="Jennifer Chen - Business Development",
                phone="(555) 345-6789",
                email="jchen@powersystems.com",
                address="5678 Electric Ave, Power City, PC 23456",
                business_type="LLC",
                years_in_business=22,
                annual_revenue=28000000.0,
                employee_count=125,
                licenses=["Electrical Contractor C-10", "Low Voltage Systems"],
                certifications=["NECA Member", "IBEW Signatory", "Smart Building Certified"],
                insurance_coverage={"General Liability": 3000000.0, "Professional": 1000000.0, "Workers Comp": 1000000.0},
                bonding_capacity=15000000.0,
                primary_trades=["Electrical Systems", "Low Voltage", "Smart Building Controls"],
                secondary_trades=["Fire Alarm", "Security Systems"],
                geographic_coverage=["Metro Area", "Regional"],
                projects_completed=298,
                safety_rating=4.9,
                quality_rating=4.8,
                schedule_performance=4.6,
                credit_rating="A",
                payment_terms="Net 30",
                preferred_project_size_min=250000.0,
                preferred_project_size_max=8000000.0,
                prequalified=True,
                prequalification_date="2024-11-20",
                prequalification_expiry="2025-11-20",
                vendor_notes="Top-tier electrical contractor with expertise in smart building systems. Strong performance history.",
                relationship_manager="Sarah Wilson - Procurement",
                created_at="2024-11-20 11:15:00",
                updated_at="2025-05-28 09:45:00"
            )
        ]
        
        for vendor in sample_vendors:
            self.vendors[vendor.vendor_id] = vendor
        
        self.next_estimate_code = 3
        self.next_package_code = 3
    
    def create_cost_estimate(self, estimate_data: Dict[str, Any]) -> str:
        """Create a new cost estimate"""
        estimate_id = f"est-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        estimate_code = f"HTD-EST-{self.next_estimate_code:03d}"
        
        # Calculate derived values
        base_cost = estimate_data["base_cost"]
        contingency_amount = base_cost * (estimate_data["contingency_percentage"] / 100)
        subtotal_with_contingency = base_cost + contingency_amount
        overhead_amount = subtotal_with_contingency * (estimate_data["overhead_percentage"] / 100)
        subtotal_with_overhead = subtotal_with_contingency + overhead_amount
        profit_amount = subtotal_with_overhead * (estimate_data["profit_percentage"] / 100)
        total_estimate = subtotal_with_overhead + profit_amount
        
        estimate_data.update({
            "estimate_id": estimate_id,
            "estimate_code": estimate_code,
            "contingency_amount": contingency_amount,
            "overhead_amount": overhead_amount,
            "profit_amount": profit_amount,
            "total_estimate": total_estimate,
            "estimate_date": datetime.now().strftime('%Y-%m-%d'),
            "review_date": None,
            "approval_date": None,
            "reviewed_by": None,
            "approved_by": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enum
        estimate_data["status"] = EstimateStatus(estimate_data["status"])
        
        estimate = CostEstimate(**estimate_data)
        self.estimates[estimate_id] = estimate
        self.next_estimate_code += 1
        
        return estimate_id
    
    def create_bid_package(self, package_data: Dict[str, Any]) -> str:
        """Create a new bid package"""
        package_id = f"pkg-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        package_code = f"HTD-PKG-{self.next_package_code:03d}"
        
        package_data.update({
            "package_id": package_id,
            "package_code": package_code,
            "submitted_bids": [],
            "awarded_contractor": None,
            "awarded_amount": None,
            "award_date": None,
            "award_justification": "",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enum
        package_data["status"] = BidStatus(package_data["status"])
        
        package = BidPackage(**package_data)
        self.bid_packages[package_id] = package
        self.next_package_code += 1
        
        return package_id
    
    def create_vendor_profile(self, vendor_data: Dict[str, Any]) -> str:
        """Create a new vendor profile"""
        vendor_id = f"vendor-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        vendor_data.update({
            "vendor_id": vendor_id,
            "prequalified": False,
            "prequalification_date": None,
            "prequalification_expiry": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        vendor = VendorProfile(**vendor_data)
        self.vendors[vendor_id] = vendor
        
        return vendor_id
    
    def get_all_estimates(self) -> List[CostEstimate]:
        """Get all cost estimates sorted by estimate date"""
        return sorted(self.estimates.values(), key=lambda e: e.estimate_date, reverse=True)
    
    def get_estimates_by_status(self, status: EstimateStatus) -> List[CostEstimate]:
        """Get estimates by status"""
        return [est for est in self.estimates.values() if est.status == status]
    
    def get_all_bid_packages(self) -> List[BidPackage]:
        """Get all bid packages sorted by due date"""
        return sorted(self.bid_packages.values(), key=lambda p: p.bid_due_date)
    
    def get_packages_by_status(self, status: BidStatus) -> List[BidPackage]:
        """Get bid packages by status"""
        return [pkg for pkg in self.bid_packages.values() if pkg.status == status]
    
    def get_all_vendors(self) -> List[VendorProfile]:
        """Get all vendor profiles sorted by company name"""
        return sorted(self.vendors.values(), key=lambda v: v.company_name)
    
    def get_prequalified_vendors(self) -> List[VendorProfile]:
        """Get prequalified vendors"""
        return [vendor for vendor in self.vendors.values() if vendor.prequalified]
    
    def approve_estimate(self, estimate_id: str, approved_by: str) -> bool:
        """Approve a cost estimate"""
        estimate = self.estimates.get(estimate_id)
        if not estimate:
            return False
        
        estimate.status = EstimateStatus.APPROVED
        estimate.approved_by = approved_by
        estimate.approval_date = datetime.now().strftime('%Y-%m-%d')
        estimate.updated_at = datetime.now().isoformat()
        
        return True
    
    def award_bid_package(self, package_id: str, contractor: str, amount: float, justification: str) -> bool:
        """Award a bid package to a contractor"""
        package = self.bid_packages.get(package_id)
        if not package:
            return False
        
        package.status = BidStatus.AWARDED
        package.awarded_contractor = contractor
        package.awarded_amount = amount
        package.award_date = datetime.now().strftime('%Y-%m-%d')
        package.award_justification = justification
        package.updated_at = datetime.now().isoformat()
        
        return True
    
    def generate_preconstruction_metrics(self) -> Dict[str, Any]:
        """Generate preconstruction system metrics"""
        estimates = list(self.estimates.values())
        packages = list(self.bid_packages.values())
        vendors = list(self.vendors.values())
        
        if not estimates and not packages and not vendors:
            return {}
        
        # Estimate metrics
        total_estimates = len(estimates)
        approved_estimates = len([e for e in estimates if e.status == EstimateStatus.APPROVED])
        total_estimated_value = sum(e.total_estimate for e in estimates if e.status in [EstimateStatus.APPROVED, EstimateStatus.FINAL])
        
        # Package metrics
        total_packages = len(packages)
        awarded_packages = len([p for p in packages if p.status == BidStatus.AWARDED])
        total_awarded_value = sum(p.awarded_amount for p in packages if p.awarded_amount is not None)
        
        # Vendor metrics
        total_vendors = len(vendors)
        prequalified_vendors = len([v for v in vendors if v.prequalified])
        
        return {
            "total_estimates": total_estimates,
            "approved_estimates": approved_estimates,
            "total_estimated_value": total_estimated_value,
            "total_packages": total_packages,
            "awarded_packages": awarded_packages,
            "total_awarded_value": total_awarded_value,
            "total_vendors": total_vendors,
            "prequalified_vendors": prequalified_vendors,
            "estimate_approval_rate": round((approved_estimates / total_estimates * 100) if total_estimates > 0 else 0, 1),
            "package_award_rate": round((awarded_packages / total_packages * 100) if total_packages > 0 else 0, 1),
            "vendor_prequalification_rate": round((prequalified_vendors / total_vendors * 100) if total_vendors > 0 else 0, 1)
        }

# Global instance for use across the application
preconstruction_manager = PreconstructionManager()