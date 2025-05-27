"""
Highland Tower Development - Transmittals Management Backend
Enterprise-grade transmittal tracking for document distribution and communication.
"""

import json
import uuid
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class TransmittalType(Enum):
    DRAWINGS = "Drawings"
    SPECIFICATIONS = "Specifications"
    SUBMITTALS = "Submittals"
    REPORTS = "Reports"
    CORRESPONDENCE = "Correspondence"
    SHOP_DRAWINGS = "Shop Drawings"
    PERMITS = "Permits"
    CERTIFICATES = "Certificates"

class TransmittalStatus(Enum):
    DRAFT = "Draft"
    SENT = "Sent"
    RECEIVED = "Received"
    ACKNOWLEDGED = "Acknowledged"
    REJECTED = "Rejected"

class DeliveryMethod(Enum):
    EMAIL = "Email"
    HAND_DELIVERY = "Hand Delivery"
    COURIER = "Courier"
    MAIL = "Mail"
    DIGITAL_PLATFORM = "Digital Platform"

@dataclass
class TransmittalDocument:
    """Document included in transmittal"""
    doc_id: str
    filename: str
    description: str
    drawing_number: Optional[str]
    revision: str
    date: str
    file_size: int
    file_type: str

@dataclass
class TransmittalRecipient:
    """Recipient of transmittal"""
    recipient_id: str
    name: str
    company: str
    email: str
    role: str
    copy_type: str  # "TO", "CC", "BCC"
    received_date: Optional[str]
    acknowledged_date: Optional[str]

@dataclass
class Transmittal:
    """Complete transmittal record"""
    transmittal_id: str
    transmittal_number: str
    subject: str
    description: str
    transmittal_type: TransmittalType
    status: TransmittalStatus
    
    # Project details
    project_name: str
    project_number: str
    
    # Sender info
    sender_name: str
    sender_company: str
    sender_email: str
    sender_phone: str
    
    # Recipients
    recipients: List[TransmittalRecipient]
    
    # Delivery
    delivery_method: DeliveryMethod
    sent_date: Optional[str]
    received_date: Optional[str]
    
    # Documents
    documents: List[TransmittalDocument]
    total_documents: int
    
    # Message
    message: str
    special_instructions: str
    reply_required: bool
    reply_by_date: Optional[str]
    
    # Tracking
    tracking_number: Optional[str]
    acknowledgment_required: bool
    
    # Metadata
    created_by: str
    created_at: str
    updated_at: str

class TransmittalsManager:
    """Enterprise transmittals management system"""
    
    def __init__(self):
        self.transmittals: Dict[str, Transmittal] = {}
        self.next_transmittal_number = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample transmittal data"""
        
        # Sample transmittal 1 - Drawings
        sample_transmittal_1 = Transmittal(
            transmittal_id="trans-001",
            transmittal_number="TRANS-2025-001",
            subject="Structural Drawings - Level 15 Revisions",
            description="Revised structural drawings for Level 15 incorporating latest design changes",
            transmittal_type=TransmittalType.DRAWINGS,
            status=TransmittalStatus.ACKNOWLEDGED,
            project_name="Highland Tower Development",
            project_number="HTD-2024-001",
            sender_name="John Smith",
            sender_company="Highland Construction Co.",
            sender_email="jsmith@highland.com",
            sender_phone="(555) 123-4567",
            recipients=[
                TransmittalRecipient(
                    recipient_id="rec-001",
                    name="Sarah Wilson",
                    company="Structural Design Partners",
                    email="swilson@structuraldesign.com",
                    role="Structural Engineer",
                    copy_type="TO",
                    received_date="2025-05-20",
                    acknowledged_date="2025-05-20"
                ),
                TransmittalRecipient(
                    recipient_id="rec-002",
                    name="Mike Johnson",
                    company="Highland Construction Co.",
                    email="mjohnson@highland.com",
                    role="Project Manager",
                    copy_type="CC",
                    received_date="2025-05-20",
                    acknowledged_date="2025-05-20"
                )
            ],
            delivery_method=DeliveryMethod.EMAIL,
            sent_date="2025-05-20",
            received_date="2025-05-20",
            documents=[
                TransmittalDocument(
                    doc_id="doc-001",
                    filename="S-301_Rev2.pdf",
                    description="Level 15 Structural Plan",
                    drawing_number="S-301",
                    revision="2",
                    date="2025-05-19",
                    file_size=8421504,
                    file_type="PDF"
                ),
                TransmittalDocument(
                    doc_id="doc-002",
                    filename="S-302_Rev2.pdf",
                    description="Level 15 Connection Details",
                    drawing_number="S-302",
                    revision="2",
                    date="2025-05-19",
                    file_size=5242880,
                    file_type="PDF"
                )
            ],
            total_documents=2,
            message="Please review the revised structural drawings for Level 15. Key changes include updated connection details and member sizing.",
            special_instructions="Coordinate with MEP team for any conflicts",
            reply_required=True,
            reply_by_date="2025-05-25",
            tracking_number="EMAIL-20250520-001",
            acknowledgment_required=True,
            created_by="John Smith",
            created_at="2025-05-20 09:00:00",
            updated_at="2025-05-20 14:30:00"
        )
        
        # Sample transmittal 2 - Submittals
        sample_transmittal_2 = Transmittal(
            transmittal_id="trans-002",
            transmittal_number="TRANS-2025-002",
            subject="HVAC Equipment Submittals",
            description="Product data and shop drawings for rooftop HVAC units",
            transmittal_type=TransmittalType.SUBMITTALS,
            status=TransmittalStatus.SENT,
            project_name="Highland Tower Development",
            project_number="HTD-2024-001",
            sender_name="Tom Brown",
            sender_company="Highland MEP Contractors",
            sender_email="tbrown@highlandmep.com",
            sender_phone="(555) 234-5678",
            recipients=[
                TransmittalRecipient(
                    recipient_id="rec-003",
                    name="Lisa Chen",
                    company="MEP Engineering Group",
                    email="lchen@mepeng.com",
                    role="MEP Engineer",
                    copy_type="TO",
                    received_date=None,
                    acknowledged_date=None
                ),
                TransmittalRecipient(
                    recipient_id="rec-004",
                    name="John Smith",
                    company="Highland Construction Co.",
                    email="jsmith@highland.com",
                    role="Project Manager",
                    copy_type="CC",
                    received_date=None,
                    acknowledged_date=None
                )
            ],
            delivery_method=DeliveryMethod.DIGITAL_PLATFORM,
            sent_date="2025-05-25",
            received_date=None,
            documents=[
                TransmittalDocument(
                    doc_id="doc-003",
                    filename="HVAC_Product_Data.pdf",
                    description="Rooftop Unit Product Data Sheets",
                    drawing_number=None,
                    revision="1",
                    date="2025-05-24",
                    file_size=12582912,
                    file_type="PDF"
                ),
                TransmittalDocument(
                    doc_id="doc-004",
                    filename="HVAC_Shop_Drawings.pdf",
                    description="HVAC Installation Details",
                    drawing_number="MEP-401",
                    revision="1",
                    date="2025-05-24",
                    file_size=15728640,
                    file_type="PDF"
                )
            ],
            total_documents=2,
            message="Please review the HVAC equipment submittals for the rooftop units. All equipment meets specified performance criteria.",
            special_instructions="Review for energy code compliance",
            reply_required=True,
            reply_by_date="2025-06-08",
            tracking_number="DIG-20250525-002",
            acknowledgment_required=True,
            created_by="Tom Brown",
            created_at="2025-05-25 11:00:00",
            updated_at="2025-05-25 11:00:00"
        )
        
        # Sample transmittal 3 - Reports
        sample_transmittal_3 = Transmittal(
            transmittal_id="trans-003",
            transmittal_number="TRANS-2025-003",
            subject="Weekly Progress Report - Week 21",
            description="Weekly construction progress report and schedule update",
            transmittal_type=TransmittalType.REPORTS,
            status=TransmittalStatus.RECEIVED,
            project_name="Highland Tower Development",
            project_number="HTD-2024-001",
            sender_name="John Smith",
            sender_company="Highland Construction Co.",
            sender_email="jsmith@highland.com",
            sender_phone="(555) 123-4567",
            recipients=[
                TransmittalRecipient(
                    recipient_id="rec-005",
                    name="David Miller",
                    company="Highland Development LLC",
                    email="dmiller@highland-dev.com",
                    role="Owner Representative",
                    copy_type="TO",
                    received_date="2025-05-27",
                    acknowledged_date=None
                ),
                TransmittalRecipient(
                    recipient_id="rec-006",
                    name="Anna Rodriguez",
                    company="Project Management Consultants",
                    email="arodriguez@pmconsult.com",
                    role="Project Consultant",
                    copy_type="CC",
                    received_date="2025-05-27",
                    acknowledged_date=None
                )
            ],
            delivery_method=DeliveryMethod.EMAIL,
            sent_date="2025-05-27",
            received_date="2025-05-27",
            documents=[
                TransmittalDocument(
                    doc_id="doc-005",
                    filename="Progress_Report_Week21.pdf",
                    description="Weekly Progress Report",
                    drawing_number=None,
                    revision="1",
                    date="2025-05-27",
                    file_size=3145728,
                    file_type="PDF"
                ),
                TransmittalDocument(
                    doc_id="doc-006",
                    filename="Schedule_Update_Week21.pdf",
                    description="Updated Project Schedule",
                    drawing_number=None,
                    revision="1",
                    date="2025-05-27",
                    file_size=2097152,
                    file_type="PDF"
                )
            ],
            total_documents=2,
            message="Please find attached the weekly progress report and updated schedule for Week 21.",
            special_instructions="Schedule shows 2-day acceleration on structural work",
            reply_required=False,
            reply_by_date=None,
            tracking_number="EMAIL-20250527-003",
            acknowledgment_required=False,
            created_by="John Smith",
            created_at="2025-05-27 16:00:00",
            updated_at="2025-05-27 16:00:00"
        )
        
        self.transmittals[sample_transmittal_1.transmittal_id] = sample_transmittal_1
        self.transmittals[sample_transmittal_2.transmittal_id] = sample_transmittal_2
        self.transmittals[sample_transmittal_3.transmittal_id] = sample_transmittal_3
        self.next_transmittal_number = 4
    
    def create_transmittal(self, transmittal_data: Dict[str, Any]) -> str:
        """Create a new transmittal"""
        transmittal_id = f"trans-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        transmittal_number = f"TRANS-2025-{self.next_transmittal_number:03d}"
        
        transmittal_data.update({
            "transmittal_id": transmittal_id,
            "transmittal_number": transmittal_number,
            "status": TransmittalStatus.DRAFT,
            "recipients": transmittal_data.get("recipients", []),
            "documents": transmittal_data.get("documents", []),
            "total_documents": len(transmittal_data.get("documents", [])),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        transmittal_data["transmittal_type"] = TransmittalType(transmittal_data["transmittal_type"])
        transmittal_data["status"] = TransmittalStatus(transmittal_data["status"])
        transmittal_data["delivery_method"] = DeliveryMethod(transmittal_data["delivery_method"])
        
        transmittal = Transmittal(**transmittal_data)
        self.transmittals[transmittal_id] = transmittal
        self.next_transmittal_number += 1
        
        return transmittal_id
    
    def get_transmittal(self, transmittal_id: str) -> Optional[Transmittal]:
        """Get a specific transmittal"""
        return self.transmittals.get(transmittal_id)
    
    def get_all_transmittals(self) -> List[Transmittal]:
        """Get all transmittals sorted by date (newest first)"""
        return sorted(self.transmittals.values(),
                     key=lambda t: t.created_at,
                     reverse=True)
    
    def update_transmittal(self, transmittal_id: str, updates: Dict[str, Any]) -> bool:
        """Update a transmittal"""
        if transmittal_id not in self.transmittals:
            return False
        
        transmittal = self.transmittals[transmittal_id]
        
        for key, value in updates.items():
            if hasattr(transmittal, key):
                setattr(transmittal, key, value)
        
        transmittal.updated_at = datetime.now().isoformat()
        return True
    
    def send_transmittal(self, transmittal_id: str) -> bool:
        """Send a transmittal"""
        transmittal = self.transmittals.get(transmittal_id)
        if not transmittal:
            return False
        
        transmittal.status = TransmittalStatus.SENT
        transmittal.sent_date = datetime.now().strftime('%Y-%m-%d')
        transmittal.tracking_number = f"{transmittal.delivery_method.value.upper()[:3]}-{datetime.now().strftime('%Y%m%d')}-{transmittal.transmittal_number[-3:]}"
        transmittal.updated_at = datetime.now().isoformat()
        
        return True
    
    def acknowledge_transmittal(self, transmittal_id: str, recipient_id: str) -> bool:
        """Mark transmittal as acknowledged by recipient"""
        transmittal = self.transmittals.get(transmittal_id)
        if not transmittal:
            return False
        
        # Find and update recipient
        for recipient in transmittal.recipients:
            if recipient.recipient_id == recipient_id:
                recipient.acknowledged_date = datetime.now().strftime('%Y-%m-%d')
                break
        
        # Check if all recipients have acknowledged
        all_acknowledged = all(r.acknowledged_date is not None for r in transmittal.recipients if r.copy_type == "TO")
        if all_acknowledged:
            transmittal.status = TransmittalStatus.ACKNOWLEDGED
        
        transmittal.updated_at = datetime.now().isoformat()
        return True
    
    def get_transmittals_by_status(self, status: TransmittalStatus) -> List[Transmittal]:
        """Get transmittals by status"""
        return [t for t in self.transmittals.values() if t.status == status]
    
    def get_transmittals_by_type(self, transmittal_type: TransmittalType) -> List[Transmittal]:
        """Get transmittals by type"""
        return [t for t in self.transmittals.values() if t.transmittal_type == transmittal_type]
    
    def get_pending_acknowledgments(self) -> List[Transmittal]:
        """Get transmittals pending acknowledgment"""
        pending = []
        for transmittal in self.transmittals.values():
            if transmittal.acknowledgment_required and transmittal.status == TransmittalStatus.SENT:
                pending.append(transmittal)
        return pending
    
    def generate_transmittal_metrics(self) -> Dict[str, Any]:
        """Generate transmittal performance metrics"""
        transmittals = list(self.transmittals.values())
        
        if not transmittals:
            return {}
        
        total_transmittals = len(transmittals)
        
        # Status counts
        status_counts = {}
        for status in TransmittalStatus:
            status_counts[status.value] = len([t for t in transmittals if t.status == status])
        
        # Type counts
        type_counts = {}
        for trans_type in TransmittalType:
            type_counts[trans_type.value] = len([t for t in transmittals if t.transmittal_type == trans_type])
        
        # Delivery method counts
        delivery_counts = {}
        for method in DeliveryMethod:
            delivery_counts[method.value] = len([t for t in transmittals if t.delivery_method == method])
        
        # Acknowledgment metrics
        pending_ack = len(self.get_pending_acknowledgments())
        acknowledged = len([t for t in transmittals if t.status == TransmittalStatus.ACKNOWLEDGED])
        ack_rate = (acknowledged / total_transmittals * 100) if total_transmittals > 0 else 0
        
        # Document metrics
        total_documents = sum(t.total_documents for t in transmittals)
        avg_docs_per_transmittal = total_documents / total_transmittals if total_transmittals > 0 else 0
        
        return {
            "total_transmittals": total_transmittals,
            "status_breakdown": status_counts,
            "type_breakdown": type_counts,
            "delivery_methods": delivery_counts,
            "pending_acknowledgments": pending_ack,
            "acknowledgment_rate": round(ack_rate, 1),
            "total_documents": total_documents,
            "avg_documents_per_transmittal": round(avg_docs_per_transmittal, 1)
        }
    
    def validate_transmittal_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate transmittal data"""
        errors = []
        
        required_fields = ["subject", "transmittal_type", "delivery_method", 
                          "sender_name", "sender_company", "created_by"]
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Required field '{field}' is missing")
        
        if not data.get("recipients"):
            errors.append("At least one recipient is required")
        
        if not data.get("documents"):
            errors.append("At least one document is required")
        
        return errors

# Global instance for use across the application
transmittals_manager = TransmittalsManager()