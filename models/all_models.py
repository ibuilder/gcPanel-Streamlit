"""
All Models for gcPanel Construction Management Platform
Comprehensive model definitions for all modules
"""

from models.base_model import BaseModel

class DeliveryModel(BaseModel):
    """Delivery tracking model"""
    def __init__(self):
        schema = {
            'id_prefix': 'DEL',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'date': {'type': 'date', 'required': True},
                'material_type': {'type': 'string', 'required': True},
                'supplier': {'type': 'string', 'required': True},
                'quantity': {'type': 'number', 'required': True},
                'unit': {'type': 'string', 'required': True},
                'status': {'type': 'string', 'required': True},
                'location': {'type': 'string'},
                'received_by': {'type': 'string'},
                'notes': {'type': 'string'}
            }
        }
        super().__init__('deliveries', schema)

class EngineeringModel(BaseModel):
    """Engineering documentation model"""
    def __init__(self):
        schema = {
            'id_prefix': 'ENG',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'title': {'type': 'string', 'required': True},
                'type': {'type': 'string', 'required': True},
                'discipline': {'type': 'string', 'required': True},
                'status': {'type': 'string', 'required': True},
                'engineer': {'type': 'string', 'required': True},
                'date_created': {'type': 'date', 'required': True},
                'revision': {'type': 'string'},
                'description': {'type': 'string'}
            }
        }
        super().__init__('engineering_items', schema)

class BIMModel(BaseModel):
    """BIM model management"""
    def __init__(self):
        schema = {
            'id_prefix': 'BIM',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'model_name': {'type': 'string', 'required': True},
                'discipline': {'type': 'string', 'required': True},
                'version': {'type': 'string', 'required': True},
                'last_updated': {'type': 'date', 'required': True},
                'file_size': {'type': 'string'},
                'status': {'type': 'string', 'required': True},
                'author': {'type': 'string'},
                'notes': {'type': 'string'}
            }
        }
        super().__init__('bim_models', schema)

class QualityControlModel(BaseModel):
    """Quality control inspections"""
    def __init__(self):
        schema = {
            'id_prefix': 'QC',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'inspection_type': {'type': 'string', 'required': True},
                'date': {'type': 'date', 'required': True},
                'location': {'type': 'string', 'required': True},
                'inspector': {'type': 'string', 'required': True},
                'result': {'type': 'string', 'required': True},
                'status': {'type': 'string', 'required': True},
                'notes': {'type': 'string'},
                'corrective_actions': {'type': 'string'}
            }
        }
        super().__init__('quality_items', schema)

class DocumentModel(BaseModel):
    """Document management"""
    def __init__(self):
        schema = {
            'id_prefix': 'DOC',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'title': {'type': 'string', 'required': True},
                'category': {'type': 'string', 'required': True},
                'status': {'type': 'string', 'required': True},
                'uploaded_by': {'type': 'string', 'required': True},
                'date_uploaded': {'type': 'date', 'required': True},
                'file_type': {'type': 'string'},
                'file_size': {'type': 'string'},
                'description': {'type': 'string'}
            }
        }
        super().__init__('documents', schema)

class MaterialModel(BaseModel):
    """Material inventory management"""
    def __init__(self):
        schema = {
            'id_prefix': 'MAT',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'material_name': {'type': 'string', 'required': True},
                'category': {'type': 'string', 'required': True},
                'quantity': {'type': 'number', 'required': True},
                'unit': {'type': 'string', 'required': True},
                'status': {'type': 'string', 'required': True},
                'supplier': {'type': 'string'},
                'cost_per_unit': {'type': 'number'},
                'location': {'type': 'string'}
            }
        }
        super().__init__('materials', schema)

class EquipmentModel(BaseModel):
    """Equipment tracking"""
    def __init__(self):
        schema = {
            'id_prefix': 'EQP',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'equipment_name': {'type': 'string', 'required': True},
                'type': {'type': 'string', 'required': True},
                'status': {'type': 'string', 'required': True},
                'location': {'type': 'string', 'required': True},
                'operator': {'type': 'string'},
                'maintenance_due': {'type': 'date'},
                'rental_cost': {'type': 'number'},
                'notes': {'type': 'string'}
            }
        }
        super().__init__('equipment', schema)

class InspectionModel(BaseModel):
    """Building inspections"""
    def __init__(self):
        schema = {
            'id_prefix': 'INS',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'inspection_type': {'type': 'string', 'required': True},
                'scheduled_date': {'type': 'date', 'required': True},
                'inspector': {'type': 'string', 'required': True},
                'status': {'type': 'string', 'required': True},
                'location': {'type': 'string', 'required': True},
                'result': {'type': 'string'},
                'notes': {'type': 'string'},
                'follow_up_required': {'type': 'boolean'}
            }
        }
        super().__init__('inspections', schema)

class IssueRiskModel(BaseModel):
    """Issues and risks management"""
    def __init__(self):
        schema = {
            'id_prefix': 'ISS',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'title': {'type': 'string', 'required': True},
                'type': {'type': 'string', 'required': True},
                'priority': {'type': 'string', 'required': True},
                'status': {'type': 'string', 'required': True},
                'reported_by': {'type': 'string', 'required': True},
                'date_reported': {'type': 'date', 'required': True},
                'description': {'type': 'string'},
                'mitigation_plan': {'type': 'string'},
                'assigned_to': {'type': 'string'}
            }
        }
        super().__init__('issues_risks', schema)

class UnitPriceModel(BaseModel):
    """Unit pricing database"""
    def __init__(self):
        schema = {
            'id_prefix': 'UP',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'item_description': {'type': 'string', 'required': True},
                'category': {'type': 'string', 'required': True},
                'unit': {'type': 'string', 'required': True},
                'price': {'type': 'number', 'required': True},
                'supplier': {'type': 'string'},
                'last_updated': {'type': 'date', 'required': True},
                'notes': {'type': 'string'}
            }
        }
        super().__init__('unit_prices', schema)

class SubcontractorModel(BaseModel):
    """Subcontractor management"""
    def __init__(self):
        schema = {
            'id_prefix': 'SUB',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'company_name': {'type': 'string', 'required': True},
                'trade': {'type': 'string', 'required': True},
                'status': {'type': 'string', 'required': True},
                'contact_person': {'type': 'string', 'required': True},
                'phone': {'type': 'string'},
                'email': {'type': 'string'},
                'rating': {'type': 'number'},
                'notes': {'type': 'string'}
            }
        }
        super().__init__('subcontractors', schema)

class TransmittalModel(BaseModel):
    """Document transmittals"""
    def __init__(self):
        schema = {
            'id_prefix': 'TXM',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'title': {'type': 'string', 'required': True},
                'recipient': {'type': 'string', 'required': True},
                'sender': {'type': 'string', 'required': True},
                'date_sent': {'type': 'date', 'required': True},
                'status': {'type': 'string', 'required': True},
                'purpose': {'type': 'string'},
                'document_count': {'type': 'number'},
                'notes': {'type': 'string'}
            }
        }
        super().__init__('transmittals', schema)

class ProgressPhotoModel(BaseModel):
    """Progress photography"""
    def __init__(self):
        schema = {
            'id_prefix': 'PHO',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'date_taken': {'type': 'date', 'required': True},
                'location': {'type': 'string', 'required': True},
                'photographer': {'type': 'string', 'required': True},
                'description': {'type': 'string'},
                'phase': {'type': 'string'},
                'weather': {'type': 'string'},
                'file_name': {'type': 'string'}
            }
        }
        super().__init__('progress_photos', schema)

class CloseoutModel(BaseModel):
    """Project closeout management"""
    def __init__(self):
        schema = {
            'id_prefix': 'CLO',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'item_name': {'type': 'string', 'required': True},
                'category': {'type': 'string', 'required': True},
                'status': {'type': 'string', 'required': True},
                'responsible_party': {'type': 'string', 'required': True},
                'due_date': {'type': 'date', 'required': True},
                'completion_date': {'type': 'date'},
                'notes': {'type': 'string'}
            }
        }
        super().__init__('closeout_items', schema)

class FieldOperationsModel(BaseModel):
    """Field operations logging"""
    def __init__(self):
        schema = {
            'id_prefix': 'FOP',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'date': {'type': 'date', 'required': True},
                'activity_type': {'type': 'string', 'required': True},
                'crew': {'type': 'string', 'required': True},
                'location': {'type': 'string', 'required': True},
                'hours_worked': {'type': 'number'},
                'progress': {'type': 'number'},
                'weather': {'type': 'string'},
                'notes': {'type': 'string'}
            }
        }
        super().__init__('field_activities', schema)

class PreconstructionModel(BaseModel):
    """Preconstruction planning"""
    def __init__(self):
        schema = {
            'id_prefix': 'PRE',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'task_name': {'type': 'string', 'required': True},
                'category': {'type': 'string', 'required': True},
                'status': {'type': 'string', 'required': True},
                'assigned_to': {'type': 'string', 'required': True},
                'due_date': {'type': 'date', 'required': True},
                'completion_date': {'type': 'date'},
                'priority': {'type': 'string'},
                'notes': {'type': 'string'}
            }
        }
        super().__init__('preconstruction_tasks', schema)