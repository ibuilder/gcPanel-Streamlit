"""
Highland Tower Development - Authentic Project Data
$45.5M Mixed-Use Development Project Data for all Construction Modules
"""

# Safety Incidents Data
highland_safety_data = [
    {
        "incident_type": "Near Miss",
        "description": "Crane operator noticed loose rigging on structural steel beam during lift operation on Floor 23",
        "location": "Floor 23, Grid Line C-15",
        "date_occurred": "2024-12-14",
        "time_occurred": "14:30",
        "severity": "Medium",
        "status": "Under Investigation",
        "reported_by": "Jack Morrison, Crane Operator",
        "witnesses": "Site Foreman Mike Rodriguez, Rigger Tom Walsh",
        "immediate_action": "Halted all crane operations, inspected rigging equipment, retrained crew on proper procedures",
        "assigned_to": "Safety Manager Lisa Chen"
    },
    {
        "incident_type": "First Aid",
        "description": "Minor cut on hand from handling rebar during foundation work",
        "location": "Foundation Level, Section B",
        "date_occurred": "2024-12-10",
        "time_occurred": "10:15",
        "severity": "Low",
        "status": "Closed",
        "reported_by": "Carlos Mendez, Ironworker",
        "immediate_action": "First aid administered on site, worker returned to duty with proper PPE reminder",
        "corrective_action": "Enhanced safety briefing on proper rebar handling techniques"
    }
]

# Contracts Data
highland_contracts_data = [
    {
        "contract_number": "HT-2024-001",
        "contract_name": "Highland Tower Structural Steel Package",
        "contractor": "Morrison Construction LLC",
        "contract_type": "Subcontract",
        "contract_value": 8750000,
        "start_date": "2024-09-15",
        "end_date": "2025-06-30",
        "status": "Active",
        "scope_of_work": "Structural steel erection for floors 1-35, including connections, decking, and coordination with MEP trades",
        "payment_terms": "Net 30 days, 5% retention",
        "retention_percentage": 5,
        "contract_manager": "David Park"
    },
    {
        "contract_number": "HT-2024-002", 
        "contract_name": "HVAC Systems Installation",
        "contractor": "Advanced Building Systems Inc",
        "contract_type": "Subcontract",
        "contract_value": 6200000,
        "start_date": "2024-11-01",
        "end_date": "2025-08-15",
        "status": "Active",
        "scope_of_work": "Complete HVAC system design-build including chillers, air handlers, ductwork, and controls",
        "payment_terms": "Net 30 days, 10% retention",
        "retention_percentage": 10,
        "contract_manager": "Sarah Johnson"
    }
]

# Deliveries Data  
highland_deliveries_data = [
    {
        "delivery_date": "2024-12-15",
        "supplier": "Steel Dynamics Inc",
        "material_description": "W24x84 structural steel beams for Floor 24 framing",
        "quantity": 45,
        "unit": "pieces",
        "delivery_ticket_number": "SDI-2024-3847",
        "received_by": "Mike Rodriguez, Site Foreman",
        "location_stored": "Laydown Area C, North Side",
        "condition": "Good",
        "status": "Received",
        "notes": "All pieces inspected and match drawings S-301 Rev C"
    },
    {
        "delivery_date": "2024-12-14",
        "supplier": "Ready Mix Concrete Co",
        "material_description": "High-strength concrete, 5000 PSI for Floor 22 deck pour",
        "quantity": 180,
        "unit": "cubic yards",
        "delivery_ticket_number": "RMC-45821",
        "received_by": "Tony Garcia, Concrete Foreman",
        "location_stored": "Direct pour to Floor 22",
        "condition": "Good",
        "status": "Received",
        "notes": "Slump test passed at 6 inches, temperature 68°F"
    }
]

# Submittals Data
highland_submittals_data = [
    {
        "submittal_number": "SUB-2024-047",
        "title": "Curtain Wall System - South Facade",
        "trade": "Architectural",
        "specification_section": "08 44 13",
        "submittal_type": "Shop Drawings",
        "submitted_by": "Premier Glazing Systems",
        "date_submitted": "2024-12-08",
        "date_required": "2024-12-22",
        "status": "Under Review",
        "reviewer": "Highland Architectural Team",
        "revision_number": 2,
        "comments": "Previous submission required thermal performance calculations revision"
    },
    {
        "submittal_number": "SUB-2024-048",
        "title": "Fire Pump and Controller Package",
        "trade": "Mechanical",
        "specification_section": "21 13 13",
        "submittal_type": "Product Data",
        "submitted_by": "Fire Protection Systems LLC",
        "date_submitted": "2024-12-05",
        "status": "Approved",
        "reviewer": "Highland MEP Engineering",
        "review_date": "2024-12-12",
        "comments": "Approved as submitted, proceed with procurement"
    }
]

# Equipment Data
highland_equipment_data = [
    {
        "equipment_id": "CR-001",
        "equipment_name": "Tower Crane - Liebherr 280 EC-H",
        "equipment_type": "Heavy Machinery",
        "manufacturer": "Liebherr",
        "model": "280 EC-H 16 Litronic",
        "serial_number": "LBR-2019-4785",
        "status": "In Use",
        "location": "Tower Base - Grid C-12",
        "assigned_to": "Jack Morrison, Crane Operator",
        "last_maintenance": "2024-11-15",
        "next_maintenance": "2025-02-15",
        "purchase_cost": 485000,
        "hourly_rate": 285
    },
    {
        "equipment_id": "EX-003",
        "equipment_name": "Excavator - CAT 336",
        "equipment_type": "Heavy Machinery", 
        "manufacturer": "Caterpillar",
        "model": "336 Next Gen",
        "serial_number": "CAT336-2023-1247",
        "status": "Available",
        "location": "Equipment Yard",
        "last_maintenance": "2024-12-01",
        "next_maintenance": "2025-03-01",
        "purchase_cost": 425000,
        "hourly_rate": 165
    }
]

# Materials Data
highland_materials_data = [
    {
        "material_code": "STL-W24-84",
        "material_name": "W24x84 Structural Steel Beam",
        "category": "Steel",
        "unit_of_measure": "pieces",
        "unit_cost": 2850,
        "quantity_on_hand": 127,
        "minimum_quantity": 25,
        "supplier": "Steel Dynamics Inc",
        "storage_location": "Laydown Area C",
        "status": "In Stock"
    },
    {
        "material_code": "CON-5000-PSI",
        "material_name": "Ready Mix Concrete 5000 PSI",
        "category": "Concrete",
        "unit_of_measure": "cubic yards",
        "unit_cost": 145,
        "quantity_on_hand": 0,
        "minimum_quantity": 50,
        "supplier": "Ready Mix Concrete Co",
        "storage_location": "Direct Pour",
        "status": "On Order"
    }
]

# Inspections Data
highland_inspections_data = [
    {
        "inspection_type": "Structural",
        "inspection_date": "2024-12-13",
        "inspector": "City Building Inspector - Robert Kim",
        "location": "Floor 22 - Structural Steel Frame",
        "trade": "Structural",
        "result": "Pass",
        "status": "Completed",
        "permit_number": "STR-2024-4785",
        "notes": "All connections verified, welding quality acceptable, proceed with deck installation"
    },
    {
        "inspection_type": "Fire Safety",
        "inspection_date": "2024-12-10",
        "inspector": "Fire Marshal - Jennifer Adams",
        "location": "Floors 15-20 Egress Routes",
        "trade": "General",
        "result": "Conditional Pass",
        "deficiencies": "Emergency lighting requires battery backup verification on Floor 18",
        "corrective_actions": "Install UPS system for emergency lighting circuit",
        "due_date": "2024-12-20",
        "status": "Re-inspection Required"
    }
]

# Documents Data
highland_documents_data = [
    {
        "document_name": "Highland Tower - Structural Drawings Package",
        "document_type": "Drawings",
        "category": "Structural",
        "revision": "Rev D",
        "date_created": "2024-12-01",
        "created_by": "Highland Structural Engineering",
        "file_format": "DWG",
        "status": "Current",
        "access_level": "Internal",
        "description": "Complete structural drawing set for floors 20-25 including connection details"
    },
    {
        "document_name": "MEP Coordination Report - December 2024",
        "document_type": "Reports",
        "category": "Mechanical",
        "revision": "Final",
        "date_created": "2024-12-08",
        "created_by": "Highland MEP Engineering",
        "file_format": "PDF",
        "status": "Current",
        "access_level": "Internal",
        "description": "Monthly coordination report addressing HVAC/electrical/plumbing conflicts and resolutions"
    }
]

# Scheduling Data
highland_scheduling_data = [
    {
        "task_name": "Floor 24 Structural Steel Erection",
        "task_description": "Erect structural steel frame including beams, columns, and bracing for Floor 24",
        "trade": "Structural",
        "start_date": "2024-12-16",
        "end_date": "2024-12-28",
        "duration": 10,
        "percent_complete": 15,
        "status": "In Progress",
        "assigned_to": "Morrison Construction LLC",
        "priority": "High",
        "milestone": False,
        "notes": "Weather delays possible due to forecasted snow mid-week"
    },
    {
        "task_name": "Floor 22 Concrete Deck Pour", 
        "task_description": "Pour concrete deck and cure for 28-day strength",
        "trade": "General",
        "start_date": "2024-12-14",
        "end_date": "2024-12-14",
        "duration": 1,
        "percent_complete": 100,
        "status": "Completed",
        "assigned_to": "Concrete Specialists Inc",
        "priority": "Normal",
        "milestone": True,
        "notes": "Pour completed successfully, curing on schedule"
    }
]

# Issues and Risks Data
highland_issues_risks_data = [
    {
        "type": "Issue",
        "title": "HVAC Duct Conflict with Structural Steel",
        "description": "HVAC main supply duct conflicts with structural steel beam W24x84 at grid intersection C-15 on Floor 18",
        "category": "Technical",
        "impact": "Medium",
        "status": "In Progress",
        "priority": "High",
        "assigned_to": "Highland MEP Engineering",
        "reported_by": "Site Foreman Mike Rodriguez",
        "date_identified": "2024-12-08",
        "target_resolution": "2024-12-18",
        "mitigation_plan": "Coordinate with structural engineer to relocate beam or reroute ductwork through alternate path"
    },
    {
        "type": "Risk",
        "title": "Weather Impact on Steel Erection Schedule",
        "description": "Forecasted winter weather conditions may impact crane operations for upper floor steel erection",
        "category": "Schedule",
        "probability": "High",
        "impact": "Medium",
        "status": "Open",
        "priority": "Medium",
        "assigned_to": "Project Manager Sarah Johnson",
        "reported_by": "Jack Morrison, Crane Operator",
        "date_identified": "2024-12-01",
        "mitigation_plan": "Pre-position materials, coordinate with weather service for accurate forecasts, have contingency indoor work ready"
    }
]

# Progress Photos Data
highland_progress_photos_data = [
    {
        "photo_date": "2024-12-15",
        "location": "Floor 24 - Overall Progress",
        "description": "Structural steel erection progress showing completed grid lines A-H, columns and beams in place",
        "photographer": "Site Foreman Mike Rodriguez",
        "trade": "Structural",
        "weather_conditions": "Clear, 42°F",
        "direction_facing": "Northeast",
        "photo_type": "Overall Progress",
        "file_name": "HT_Floor24_Progress_20241215.jpg",
        "tags": "steel, erection, floor24, structural"
    },
    {
        "photo_date": "2024-12-12",
        "location": "Floor 22 - Concrete Pour",
        "description": "Concrete deck pour in progress, showing pump truck and finishing crew",
        "photographer": "Quality Control Inspector",
        "trade": "General",
        "weather_conditions": "Overcast, 55°F",
        "direction_facing": "South",
        "photo_type": "Detail Work",
        "file_name": "HT_Floor22_ConcretePour_20241212.jpg",
        "tags": "concrete, pour, floor22, deck"
    }
]

# Subcontractors Data
highland_subcontractors_data = [
    {
        "company_name": "Morrison Construction LLC",
        "trade": "Steel",
        "contact_person": "David Morrison",
        "phone": "(555) 234-5678",
        "email": "david@morrisonconstruction.com",
        "license_number": "CONT-2024-4785",
        "insurance_status": "Current",
        "insurance_expiry": "2025-08-15",
        "status": "Active",
        "performance_rating": "Excellent",
        "contract_value": 8750000,
        "start_date": "2024-09-15",
        "completion_date": "2025-06-30",
        "notes": "Consistently ahead of schedule, excellent quality work"
    },
    {
        "company_name": "Advanced Building Systems Inc",
        "trade": "HVAC",
        "contact_person": "Jennifer Martinez",
        "phone": "(555) 345-6789",
        "email": "jennifer@advancedbuildingsystems.com",
        "license_number": "HVAC-2024-3621",
        "insurance_status": "Current", 
        "insurance_expiry": "2025-05-30",
        "status": "Active",
        "performance_rating": "Good",
        "contract_value": 6200000,
        "start_date": "2024-11-01",
        "completion_date": "2025-08-15",
        "notes": "Working closely with structural trades for coordination"
    }
]

# Quality Control Data
highland_quality_control_data = [
    {
        "inspection_type": "Material Testing",
        "inspection_date": "2024-12-14",
        "inspector": "QC Manager Tom Walsh",
        "location": "Floor 22 Concrete Deck",
        "trade": "General",
        "specification_reference": "ACI 318-19",
        "result": "Pass",
        "status": "Closed",
        "test_results": "Compressive strength: 5,250 PSI at 7 days, exceeds 5,000 PSI requirement",
        "photos_taken": True,
        "notes": "Samples sent to lab for 28-day strength verification"
    },
    {
        "inspection_type": "Workmanship Review",
        "inspection_date": "2024-12-12",
        "inspector": "QC Inspector Lisa Chen",
        "location": "Floor 23 Structural Steel Connections",
        "trade": "Structural",
        "specification_reference": "AISC 360-16",
        "result": "Conditional",
        "deficiencies_found": "Three bolted connections require additional tightening to specified torque",
        "corrective_actions": "Re-torque connections per specification, verify with calibrated torque wrench",
        "retest_date": "2024-12-16",
        "status": "Pending Correction",
        "notes": "Issued NCR-2024-047 for tracking"
    }
]

# Engineering Data
highland_engineering_data = [
    {
        "document_type": "Structural Calculations",
        "document_number": "CALC-STR-2024-15",
        "title": "Floor 24 Beam Design Calculations",
        "discipline": "Structural",
        "revision": "Rev B",
        "date_created": "2024-12-05",
        "engineer": "P.E. Robert Chen",
        "status": "Approved",
        "reviewer": "Senior Engineer Maria Santos",
        "review_date": "2024-12-10",
        "description": "Design calculations for W24x84 beams supporting mechanical equipment loads on Floor 24",
        "comments": "Calculations verified, proceed with installation per drawings S-301 Rev D"
    },
    {
        "document_type": "Change Orders",
        "document_number": "ENG-CO-2024-08",
        "title": "HVAC Duct Rerouting - Floor 18",
        "discipline": "Mechanical",
        "revision": "Final",
        "date_created": "2024-12-08",
        "engineer": "P.E. Jennifer Liu",
        "status": "Issued for Construction",
        "description": "Engineering solution for HVAC duct conflict with structural steel, alternate routing through service corridor",
        "comments": "Coordination complete with structural and electrical trades"
    }
]

# All data collections
HIGHLAND_TOWER_DATA = {
    'safety_incidents': highland_safety_data,
    'contracts': highland_contracts_data,
    'deliveries': highland_deliveries_data,
    'submittals': highland_submittals_data,
    'equipment': highland_equipment_data,
    'materials': highland_materials_data,
    'inspections': highland_inspections_data,
    'documents': highland_documents_data,
    'schedule_tasks': highland_scheduling_data,
    'issues_risks': highland_issues_risks_data,
    'progress_photos': highland_progress_photos_data,
    'subcontractors': highland_subcontractors_data,
    'quality_control': highland_quality_control_data,
    'engineering': highland_engineering_data
}