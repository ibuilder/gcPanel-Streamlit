"""
All Model Classes for gcPanel Construction Management Platform
Complete model definitions for every construction module
"""

from lib.models.base_model import BaseModel
from typing import Dict, Any

# RFI Model
class RFIModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'title': {'type': 'text', 'required': True},
                'description': {'type': 'textarea', 'required': True},
                'trade': {'type': 'select', 'required': True, 'options': ['Architectural', 'Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Civil', 'Vertical Transportation']},
                'priority': {'type': 'select', 'required': True, 'options': ['Low', 'Medium', 'High', 'Critical']},
                'submitted_by': {'type': 'text', 'required': True},
                'date_submitted': {'type': 'date', 'required': True},
                'status': {'type': 'select', 'required': True, 'options': ['Under Review', 'Responded', 'Pending Response', 'Closed']},
                'assignee': {'type': 'text', 'required': False},
                'due_date': {'type': 'date', 'required': False},
                'location': {'type': 'text', 'required': False},
                'drawing_reference': {'type': 'text', 'required': False},
                'response': {'type': 'textarea', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('rfis', schema)

# Daily Reports Model  
class DailyReportModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'date': {'type': 'date', 'required': True},
                'weather': {'type': 'text', 'required': False},
                'temperature': {'type': 'number', 'required': False},
                'crew_count': {'type': 'number', 'required': True, 'min_value': 1},
                'hours_worked': {'type': 'number', 'required': True, 'min_value': 0},
                'activities': {'type': 'textarea', 'required': True},
                'progress': {'type': 'textarea', 'required': False},
                'issues': {'type': 'textarea', 'required': False},
                'safety_incidents': {'type': 'number', 'required': False, 'min_value': 0},
                'materials_delivered': {'type': 'textarea', 'required': False},
                'equipment_used': {'type': 'textarea', 'required': False},
                'created_by': {'type': 'text', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('daily_reports', schema)

# Cost Management Model
class CostModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'category': {'type': 'select', 'required': True, 'options': ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'Other']},
                'description': {'type': 'textarea', 'required': True},
                'budget': {'type': 'currency', 'required': True, 'min_value': 0},
                'actual': {'type': 'currency', 'required': False, 'min_value': 0},
                'committed': {'type': 'currency', 'required': False, 'min_value': 0},
                'variance': {'type': 'currency', 'required': False},
                'status': {'type': 'select', 'required': True, 'options': ['On Budget', 'Over Budget', 'Under Budget', 'Pending']},
                'cost_code': {'type': 'text', 'required': False},
                'vendor': {'type': 'text', 'required': False},
                'invoice_number': {'type': 'text', 'required': False},
                'date_incurred': {'type': 'date', 'required': False},
                'approval_status': {'type': 'select', 'required': False, 'options': ['Pending', 'Approved', 'Rejected']},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('cost_management', schema)

# Safety Model
class SafetyModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'incident_type': {'type': 'select', 'required': True, 'options': ['Near Miss', 'First Aid', 'Medical Treatment', 'Lost Time', 'Property Damage', 'Environmental']},
                'description': {'type': 'textarea', 'required': True},
                'location': {'type': 'text', 'required': True},
                'date_occurred': {'type': 'date', 'required': True},
                'time_occurred': {'type': 'text', 'required': False},
                'severity': {'type': 'select', 'required': True, 'options': ['Low', 'Medium', 'High', 'Critical']},
                'status': {'type': 'select', 'required': True, 'options': ['Open', 'Under Investigation', 'Closed', 'Pending Action']},
                'reported_by': {'type': 'text', 'required': True},
                'injured_person': {'type': 'text', 'required': False},
                'witnesses': {'type': 'text', 'required': False},
                'immediate_action': {'type': 'textarea', 'required': False},
                'root_cause': {'type': 'textarea', 'required': False},
                'corrective_action': {'type': 'textarea', 'required': False},
                'assigned_to': {'type': 'text', 'required': False},
                'due_date': {'type': 'date', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('safety_incidents', schema)

# Contracts Model
class ContractModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'contract_number': {'type': 'text', 'required': True},
                'contract_name': {'type': 'text', 'required': True},
                'contractor': {'type': 'text', 'required': True},
                'contract_type': {'type': 'select', 'required': True, 'options': ['Prime Contract', 'Subcontract', 'Purchase Order', 'Service Agreement']},
                'contract_value': {'type': 'currency', 'required': True, 'min_value': 0},
                'start_date': {'type': 'date', 'required': True},
                'end_date': {'type': 'date', 'required': True},
                'status': {'type': 'select', 'required': True, 'options': ['Draft', 'Under Review', 'Approved', 'Active', 'Completed', 'Terminated']},
                'scope_of_work': {'type': 'textarea', 'required': True},
                'payment_terms': {'type': 'text', 'required': False},
                'retention_percentage': {'type': 'number', 'required': False, 'min_value': 0, 'max_value': 100},
                'contract_manager': {'type': 'text', 'required': False},
                'executed_date': {'type': 'date', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('contracts', schema)

# Deliveries Model
class DeliveryModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'delivery_date': {'type': 'date', 'required': True},
                'supplier': {'type': 'text', 'required': True},
                'material_description': {'type': 'textarea', 'required': True},
                'quantity': {'type': 'number', 'required': True, 'min_value': 0},
                'unit': {'type': 'text', 'required': False},
                'delivery_ticket_number': {'type': 'text', 'required': False},
                'received_by': {'type': 'text', 'required': True},
                'location_stored': {'type': 'text', 'required': False},
                'condition': {'type': 'select', 'required': True, 'options': ['Good', 'Damaged', 'Partial', 'Rejected']},
                'notes': {'type': 'textarea', 'required': False},
                'status': {'type': 'select', 'required': True, 'options': ['Scheduled', 'Delivered', 'Received', 'Rejected']},
                'invoice_number': {'type': 'text', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('deliveries', schema)

# Submittals Model
class SubmittalModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'submittal_number': {'type': 'text', 'required': True},
                'title': {'type': 'text', 'required': True},
                'trade': {'type': 'select', 'required': True, 'options': ['Architectural', 'Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Civil']},
                'specification_section': {'type': 'text', 'required': False},
                'submittal_type': {'type': 'select', 'required': True, 'options': ['Shop Drawings', 'Product Data', 'Samples', 'Design Mix', 'Test Reports']},
                'submitted_by': {'type': 'text', 'required': True},
                'date_submitted': {'type': 'date', 'required': True},
                'date_required': {'type': 'date', 'required': False},
                'status': {'type': 'select', 'required': True, 'options': ['Submitted', 'Under Review', 'Approved', 'Approved as Noted', 'Revise and Resubmit', 'Rejected']},
                'reviewer': {'type': 'text', 'required': False},
                'review_date': {'type': 'date', 'required': False},
                'comments': {'type': 'textarea', 'required': False},
                'revision_number': {'type': 'number', 'required': False, 'min_value': 0},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('submittals', schema)

# Equipment Tracking Model
class EquipmentModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'equipment_id': {'type': 'text', 'required': True},
                'equipment_name': {'type': 'text', 'required': True},
                'equipment_type': {'type': 'select', 'required': True, 'options': ['Heavy Machinery', 'Hand Tools', 'Safety Equipment', 'Surveying', 'Testing', 'Lifting']},
                'manufacturer': {'type': 'text', 'required': False},
                'model': {'type': 'text', 'required': False},
                'serial_number': {'type': 'text', 'required': False},
                'status': {'type': 'select', 'required': True, 'options': ['Available', 'In Use', 'Maintenance', 'Out of Service', 'Retired']},
                'location': {'type': 'text', 'required': False},
                'assigned_to': {'type': 'text', 'required': False},
                'last_maintenance': {'type': 'date', 'required': False},
                'next_maintenance': {'type': 'date', 'required': False},
                'purchase_date': {'type': 'date', 'required': False},
                'purchase_cost': {'type': 'currency', 'required': False, 'min_value': 0},
                'hourly_rate': {'type': 'currency', 'required': False, 'min_value': 0},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('equipment', schema)

# Material Management Model
class MaterialModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'material_code': {'type': 'text', 'required': True},
                'material_name': {'type': 'text', 'required': True},
                'category': {'type': 'select', 'required': True, 'options': ['Concrete', 'Steel', 'Lumber', 'Electrical', 'Plumbing', 'Insulation', 'Finishes', 'Hardware']},
                'unit_of_measure': {'type': 'text', 'required': True},
                'unit_cost': {'type': 'currency', 'required': False, 'min_value': 0},
                'quantity_on_hand': {'type': 'number', 'required': False, 'min_value': 0},
                'minimum_quantity': {'type': 'number', 'required': False, 'min_value': 0},
                'supplier': {'type': 'text', 'required': False},
                'storage_location': {'type': 'text', 'required': False},
                'status': {'type': 'select', 'required': True, 'options': ['In Stock', 'Low Stock', 'Out of Stock', 'On Order', 'Discontinued']},
                'last_updated': {'type': 'date', 'required': False},
                'notes': {'type': 'textarea', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('materials', schema)

# Inspections Model
class InspectionModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'inspection_type': {'type': 'select', 'required': True, 'options': ['Building', 'Electrical', 'Plumbing', 'Mechanical', 'Fire Safety', 'Structural', 'Quality Control']},
                'inspection_date': {'type': 'date', 'required': True},
                'inspector': {'type': 'text', 'required': True},
                'location': {'type': 'text', 'required': True},
                'trade': {'type': 'select', 'required': False, 'options': ['General', 'Architectural', 'Structural', 'Mechanical', 'Electrical', 'Plumbing']},
                'result': {'type': 'select', 'required': True, 'options': ['Pass', 'Fail', 'Conditional Pass', 'Pending']},
                'deficiencies': {'type': 'textarea', 'required': False},
                'corrective_actions': {'type': 'textarea', 'required': False},
                'due_date': {'type': 'date', 'required': False},
                'status': {'type': 'select', 'required': True, 'options': ['Scheduled', 'Completed', 'Failed', 'Re-inspection Required']},
                'permit_number': {'type': 'text', 'required': False},
                'notes': {'type': 'textarea', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('inspections', schema)

# Documents Model
class DocumentModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'document_name': {'type': 'text', 'required': True},
                'document_type': {'type': 'select', 'required': True, 'options': ['Drawings', 'Specifications', 'Contracts', 'Reports', 'Photos', 'Correspondence', 'Permits', 'Warranties']},
                'category': {'type': 'select', 'required': False, 'options': ['Architectural', 'Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Civil', 'Administrative']},
                'revision': {'type': 'text', 'required': False},
                'date_created': {'type': 'date', 'required': True},
                'created_by': {'type': 'text', 'required': True},
                'file_size': {'type': 'text', 'required': False},
                'file_format': {'type': 'select', 'required': False, 'options': ['PDF', 'DWG', 'XLS', 'DOC', 'JPG', 'PNG', 'ZIP']},
                'status': {'type': 'select', 'required': True, 'options': ['Current', 'Superseded', 'Under Review', 'Archived']},
                'access_level': {'type': 'select', 'required': True, 'options': ['Public', 'Internal', 'Confidential', 'Restricted']},
                'tags': {'type': 'text', 'required': False},
                'description': {'type': 'textarea', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('documents', schema)

# Scheduling Model
class ScheduleModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'task_name': {'type': 'text', 'required': True},
                'task_description': {'type': 'textarea', 'required': False},
                'trade': {'type': 'select', 'required': True, 'options': ['General', 'Architectural', 'Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Civil']},
                'start_date': {'type': 'date', 'required': True},
                'end_date': {'type': 'date', 'required': True},
                'duration': {'type': 'number', 'required': False, 'min_value': 1},
                'percent_complete': {'type': 'number', 'required': False, 'min_value': 0, 'max_value': 100},
                'status': {'type': 'select', 'required': True, 'options': ['Not Started', 'In Progress', 'Completed', 'On Hold', 'Cancelled']},
                'assigned_to': {'type': 'text', 'required': False},
                'predecessor_tasks': {'type': 'text', 'required': False},
                'priority': {'type': 'select', 'required': False, 'options': ['Low', 'Normal', 'High', 'Critical']},
                'milestone': {'type': 'checkbox', 'required': False},
                'notes': {'type': 'textarea', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('schedule_tasks', schema)

# Issues and Risks Model
class IssueRiskModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'type': {'type': 'select', 'required': True, 'options': ['Issue', 'Risk']},
                'title': {'type': 'text', 'required': True},
                'description': {'type': 'textarea', 'required': True},
                'category': {'type': 'select', 'required': True, 'options': ['Technical', 'Schedule', 'Cost', 'Quality', 'Safety', 'Environmental', 'Regulatory']},
                'probability': {'type': 'select', 'required': False, 'options': ['Very Low', 'Low', 'Medium', 'High', 'Very High']},
                'impact': {'type': 'select', 'required': True, 'options': ['Very Low', 'Low', 'Medium', 'High', 'Very High']},
                'status': {'type': 'select', 'required': True, 'options': ['Open', 'In Progress', 'Resolved', 'Closed', 'Escalated']},
                'priority': {'type': 'select', 'required': True, 'options': ['Low', 'Medium', 'High', 'Critical']},
                'assigned_to': {'type': 'text', 'required': False},
                'reported_by': {'type': 'text', 'required': True},
                'date_identified': {'type': 'date', 'required': True},
                'target_resolution': {'type': 'date', 'required': False},
                'mitigation_plan': {'type': 'textarea', 'required': False},
                'resolution': {'type': 'textarea', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('issues_risks', schema)

# Progress Photos Model
class ProgressPhotoModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'photo_date': {'type': 'date', 'required': True},
                'location': {'type': 'text', 'required': True},
                'description': {'type': 'textarea', 'required': True},
                'photographer': {'type': 'text', 'required': True},
                'trade': {'type': 'select', 'required': False, 'options': ['General', 'Architectural', 'Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Civil']},
                'weather_conditions': {'type': 'text', 'required': False},
                'direction_facing': {'type': 'select', 'required': False, 'options': ['North', 'South', 'East', 'West', 'Northeast', 'Northwest', 'Southeast', 'Southwest']},
                'photo_type': {'type': 'select', 'required': True, 'options': ['Overall Progress', 'Detail Work', 'Safety Compliance', 'Quality Control', 'Before/After', 'Problem Documentation']},
                'file_name': {'type': 'text', 'required': False},
                'file_size': {'type': 'text', 'required': False},
                'tags': {'type': 'text', 'required': False},
                'notes': {'type': 'textarea', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('progress_photos', schema)

# Subcontractor Management Model
class SubcontractorModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'company_name': {'type': 'text', 'required': True},
                'trade': {'type': 'select', 'required': True, 'options': ['General', 'Electrical', 'Plumbing', 'HVAC', 'Roofing', 'Concrete', 'Steel', 'Drywall', 'Flooring', 'Painting']},
                'contact_person': {'type': 'text', 'required': True},
                'phone': {'type': 'phone', 'required': True},
                'email': {'type': 'email', 'required': False},
                'address': {'type': 'textarea', 'required': False},
                'license_number': {'type': 'text', 'required': False},
                'insurance_status': {'type': 'select', 'required': True, 'options': ['Current', 'Expired', 'Pending', 'Not Required']},
                'insurance_expiry': {'type': 'date', 'required': False},
                'status': {'type': 'select', 'required': True, 'options': ['Active', 'Inactive', 'Prequalified', 'Blacklisted']},
                'performance_rating': {'type': 'select', 'required': False, 'options': ['Excellent', 'Good', 'Satisfactory', 'Needs Improvement', 'Poor']},
                'contract_value': {'type': 'currency', 'required': False, 'min_value': 0},
                'start_date': {'type': 'date', 'required': False},
                'completion_date': {'type': 'date', 'required': False},
                'notes': {'type': 'textarea', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('subcontractors', schema)

# Quality Control Model
class QualityControlModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'inspection_type': {'type': 'select', 'required': True, 'options': ['Material Testing', 'Workmanship Review', 'Code Compliance', 'Safety Check', 'Quality Audit']},
                'inspection_date': {'type': 'date', 'required': True},
                'inspector': {'type': 'text', 'required': True},
                'location': {'type': 'text', 'required': True},
                'trade': {'type': 'select', 'required': True, 'options': ['General', 'Architectural', 'Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Civil']},
                'specification_reference': {'type': 'text', 'required': False},
                'result': {'type': 'select', 'required': True, 'options': ['Pass', 'Fail', 'Conditional', 'Retest Required']},
                'deficiencies_found': {'type': 'textarea', 'required': False},
                'corrective_actions': {'type': 'textarea', 'required': False},
                'retest_date': {'type': 'date', 'required': False},
                'status': {'type': 'select', 'required': True, 'options': ['Open', 'Closed', 'Pending Correction', 'Reinspection Scheduled']},
                'photos_taken': {'type': 'checkbox', 'required': False},
                'test_results': {'type': 'textarea', 'required': False},
                'notes': {'type': 'textarea', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('quality_control', schema)

# Engineering Model
class EngineeringModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'document_type': {'type': 'select', 'required': True, 'options': ['Structural Calculations', 'MEP Design', 'Site Plans', 'Detail Drawings', 'Engineering Reports', 'Change Orders']},
                'document_number': {'type': 'text', 'required': True},
                'title': {'type': 'text', 'required': True},
                'discipline': {'type': 'select', 'required': True, 'options': ['Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Civil', 'Environmental']},
                'revision': {'type': 'text', 'required': False},
                'date_created': {'type': 'date', 'required': True},
                'engineer': {'type': 'text', 'required': True},
                'status': {'type': 'select', 'required': True, 'options': ['Draft', 'Under Review', 'Approved', 'Issued for Construction', 'Superseded']},
                'reviewer': {'type': 'text', 'required': False},
                'review_date': {'type': 'date', 'required': False},
                'description': {'type': 'textarea', 'required': True},
                'comments': {'type': 'textarea', 'required': False},
                'related_drawings': {'type': 'text', 'required': False},
                'project_phase': {'type': 'select', 'required': False, 'options': ['Design Development', 'Construction Documents', 'Construction Administration', 'Closeout']},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('engineering', schema)

# Preconstruction Model
class PreconstructionModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'activity_type': {'type': 'select', 'required': True, 'options': ['Permits', 'Site Survey', 'Soil Testing', 'Utility Coordination', 'Design Review', 'Value Engineering', 'Bidding']},
                'description': {'type': 'textarea', 'required': True},
                'responsible_party': {'type': 'text', 'required': True},
                'start_date': {'type': 'date', 'required': True},
                'target_completion': {'type': 'date', 'required': True},
                'actual_completion': {'type': 'date', 'required': False},
                'status': {'type': 'select', 'required': True, 'options': ['Not Started', 'In Progress', 'Completed', 'On Hold', 'Cancelled']},
                'priority': {'type': 'select', 'required': True, 'options': ['Low', 'Medium', 'High', 'Critical']},
                'estimated_cost': {'type': 'currency', 'required': False, 'min_value': 0},
                'actual_cost': {'type': 'currency', 'required': False, 'min_value': 0},
                'deliverables': {'type': 'textarea', 'required': False},
                'dependencies': {'type': 'text', 'required': False},
                'risks': {'type': 'textarea', 'required': False},
                'notes': {'type': 'textarea', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('preconstruction', schema)

# Closeout Model
class CloseoutModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'closeout_item': {'type': 'text', 'required': True},
                'category': {'type': 'select', 'required': True, 'options': ['Documentation', 'Testing', 'Training', 'Warranties', 'As-Built Drawings', 'O&M Manuals', 'Permits']},
                'trade': {'type': 'select', 'required': False, 'options': ['General', 'Architectural', 'Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Civil']},
                'responsible_party': {'type': 'text', 'required': True},
                'due_date': {'type': 'date', 'required': True},
                'completion_date': {'type': 'date', 'required': False},
                'status': {'type': 'select', 'required': True, 'options': ['Not Started', 'In Progress', 'Submitted', 'Under Review', 'Approved', 'Rejected']},
                'priority': {'type': 'select', 'required': True, 'options': ['Low', 'Medium', 'High', 'Critical']},
                'description': {'type': 'textarea', 'required': True},
                'submittal_requirements': {'type': 'textarea', 'required': False},
                'review_comments': {'type': 'textarea', 'required': False},
                'final_approval_date': {'type': 'date', 'required': False},
                'notes': {'type': 'textarea', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('closeout', schema)

# Field Operations Model
class FieldOperationModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'operation_type': {'type': 'select', 'required': True, 'options': ['Site Setup', 'Excavation', 'Foundation', 'Framing', 'MEP Installation', 'Finishes', 'Cleanup']},
                'description': {'type': 'textarea', 'required': True},
                'location': {'type': 'text', 'required': True},
                'crew_lead': {'type': 'text', 'required': True},
                'crew_size': {'type': 'number', 'required': True, 'min_value': 1},
                'start_date': {'type': 'date', 'required': True},
                'end_date': {'type': 'date', 'required': False},
                'estimated_hours': {'type': 'number', 'required': False, 'min_value': 0},
                'actual_hours': {'type': 'number', 'required': False, 'min_value': 0},
                'status': {'type': 'select', 'required': True, 'options': ['Planned', 'In Progress', 'Completed', 'On Hold', 'Cancelled']},
                'weather_impact': {'type': 'select', 'required': False, 'options': ['None', 'Minor Delay', 'Major Delay', 'Work Stopped']},
                'equipment_used': {'type': 'text', 'required': False},
                'materials_consumed': {'type': 'textarea', 'required': False},
                'productivity_notes': {'type': 'textarea', 'required': False},
                'safety_issues': {'type': 'textarea', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('field_operations', schema)

# BIM Model
class BIMModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'model_name': {'type': 'text', 'required': True},
                'model_type': {'type': 'select', 'required': True, 'options': ['Architectural', 'Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Coordination', 'Federated']},
                'discipline': {'type': 'select', 'required': True, 'options': ['Architecture', 'Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Civil', 'Landscape']},
                'version': {'type': 'text', 'required': True},
                'date_created': {'type': 'date', 'required': True},
                'created_by': {'type': 'text', 'required': True},
                'file_size': {'type': 'text', 'required': False},
                'software_used': {'type': 'select', 'required': False, 'options': ['Revit', 'AutoCAD', 'Navisworks', 'Tekla', 'ArchiCAD', 'SketchUp', 'Other']},
                'status': {'type': 'select', 'required': True, 'options': ['In Development', 'Under Review', 'Approved', 'Current', 'Superseded', 'Archived']},
                'clash_detection_run': {'type': 'checkbox', 'required': False},
                'clashes_found': {'type': 'number', 'required': False, 'min_value': 0},
                'clashes_resolved': {'type': 'number', 'required': False, 'min_value': 0},
                'level_of_detail': {'type': 'select', 'required': False, 'options': ['LOD 100', 'LOD 200', 'LOD 300', 'LOD 400', 'LOD 500']},
                'notes': {'type': 'textarea', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('bim_models', schema)

# Transmittals Model
class TransmittalModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'transmittal_number': {'type': 'text', 'required': True},
                'date_sent': {'type': 'date', 'required': True},
                'sent_to': {'type': 'text', 'required': True},
                'sent_by': {'type': 'text', 'required': True},
                'project_phase': {'type': 'select', 'required': False, 'options': ['Design', 'Preconstruction', 'Construction', 'Closeout']},
                'transmittal_type': {'type': 'select', 'required': True, 'options': ['For Review', 'For Approval', 'For Information', 'For Construction', 'Final']},
                'description': {'type': 'textarea', 'required': True},
                'documents_included': {'type': 'textarea', 'required': True},
                'delivery_method': {'type': 'select', 'required': True, 'options': ['Email', 'Hand Delivery', 'Mail', 'FTP', 'Project Portal']},
                'response_required': {'type': 'checkbox', 'required': False},
                'response_due_date': {'type': 'date', 'required': False},
                'status': {'type': 'select', 'required': True, 'options': ['Sent', 'Acknowledged', 'Reviewed', 'Approved', 'Rejected', 'Superseded']},
                'response_received': {'type': 'date', 'required': False},
                'comments': {'type': 'textarea', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('transmittals', schema)

# Unit Prices Model
class UnitPriceModel(BaseModel):
    def __init__(self):
        schema = {
            'fields': {
                'id': {'type': 'text', 'required': False},
                'item_code': {'type': 'text', 'required': True},
                'description': {'type': 'textarea', 'required': True},
                'category': {'type': 'select', 'required': True, 'options': ['Labor', 'Materials', 'Equipment', 'Subcontractor', 'General Conditions']},
                'trade': {'type': 'select', 'required': True, 'options': ['General', 'Sitework', 'Concrete', 'Masonry', 'Steel', 'Carpentry', 'Thermal', 'Roofing', 'MEP', 'Finishes']},
                'unit_of_measure': {'type': 'text', 'required': True},
                'unit_price': {'type': 'currency', 'required': True, 'min_value': 0},
                'labor_hours': {'type': 'number', 'required': False, 'min_value': 0},
                'material_cost': {'type': 'currency', 'required': False, 'min_value': 0},
                'equipment_cost': {'type': 'currency', 'required': False, 'min_value': 0},
                'overhead_percentage': {'type': 'number', 'required': False, 'min_value': 0, 'max_value': 100},
                'profit_percentage': {'type': 'number', 'required': False, 'min_value': 0, 'max_value': 100},
                'effective_date': {'type': 'date', 'required': True},
                'expiry_date': {'type': 'date', 'required': False},
                'status': {'type': 'select', 'required': True, 'options': ['Active', 'Inactive', 'Pending Approval', 'Expired']},
                'notes': {'type': 'textarea', 'required': False},
                'created_at': {'type': 'datetime', 'required': False},
                'updated_at': {'type': 'datetime', 'required': False}
            }
        }
        super().__init__('unit_prices', schema)