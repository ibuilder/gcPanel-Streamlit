"""
Script to standardize all MVC pages with sortable tables and view/edit functionality
Updates all construction module pages to use the Highland Tower data structure
"""

import os
import re

# Define key fields for each module based on Highland Tower data
MODULE_CONFIGS = {
    '03_📄_RFIs.py': {
        'key_fields': ['id', 'title', 'trade', 'status', 'date_submitted'],
        'search_fields': ['title', 'description', 'trade', 'submitted_by'],
        'primary_filter': 'status',
        'secondary_filter': 'trade'
    },
    '04_📨_Submittals.py': {
        'key_fields': ['submittal_number', 'title', 'trade', 'status', 'date_submitted'],
        'search_fields': ['title', 'trade', 'submitted_by', 'submittal_number'],
        'primary_filter': 'status',
        'secondary_filter': 'trade'
    },
    '05_📑_Contracts.py': {
        'key_fields': ['contract_number', 'contract_name', 'contractor', 'contract_value', 'status'],
        'search_fields': ['contract_name', 'contractor', 'contract_number', 'contract_type'],
        'primary_filter': 'status',
        'secondary_filter': 'contract_type'
    },
    '07_🚚_Deliveries.py': {
        'key_fields': ['delivery_date', 'supplier', 'material_description', 'quantity', 'status'],
        'search_fields': ['supplier', 'material_description', 'delivery_ticket_number'],
        'primary_filter': 'status',
        'secondary_filter': 'condition'
    },
    '08_🏗️_Preconstruction.py': {
        'key_fields': ['id', 'activity_name', 'phase', 'status', 'completion_date'],
        'search_fields': ['activity_name', 'phase', 'responsible_party'],
        'primary_filter': 'status',
        'secondary_filter': 'phase'
    },
    '09_⚙️_Engineering.py': {
        'key_fields': ['document_number', 'title', 'discipline', 'status', 'date_created'],
        'search_fields': ['title', 'discipline', 'engineer', 'document_type'],
        'primary_filter': 'status',
        'secondary_filter': 'discipline'
    },
    '10_🏭_Field_Operations.py': {
        'key_fields': ['date', 'activity_type', 'location', 'status', 'crew_size'],
        'search_fields': ['activity_description', 'location', 'foreman'],
        'primary_filter': 'status',
        'secondary_filter': 'activity_type'
    },
    '12_🏗️_BIM.py': {
        'key_fields': ['model_name', 'model_type', 'discipline', 'status', 'last_updated'],
        'search_fields': ['model_name', 'discipline', 'created_by'],
        'primary_filter': 'status',
        'secondary_filter': 'discipline'
    },
    '13_🏁_Closeout.py': {
        'key_fields': ['item_name', 'category', 'status', 'due_date', 'completion_date'],
        'search_fields': ['item_name', 'category', 'responsible_party'],
        'primary_filter': 'status',
        'secondary_filter': 'category'
    },
    '14_📺_Transmittals.py': {
        'key_fields': ['transmittal_number', 'title', 'recipient', 'status', 'date_sent'],
        'search_fields': ['title', 'recipient', 'transmittal_number', 'sent_by'],
        'primary_filter': 'status',
        'secondary_filter': 'transmittal_type'
    },
    '15_📅_Scheduling.py': {
        'key_fields': ['task_name', 'trade', 'start_date', 'end_date', 'status'],
        'search_fields': ['task_name', 'task_description', 'assigned_to'],
        'primary_filter': 'status',
        'secondary_filter': 'trade'
    },
    '16_🔍_Quality_Control.py': {
        'key_fields': ['inspection_type', 'inspection_date', 'location', 'result', 'status'],
        'search_fields': ['location', 'inspector', 'inspection_type'],
        'primary_filter': 'result',
        'secondary_filter': 'status'
    },
    '17_📸_Progress_Photos.py': {
        'key_fields': ['photo_date', 'location', 'trade', 'photo_type', 'photographer'],
        'search_fields': ['location', 'description', 'photographer', 'tags'],
        'primary_filter': 'trade',
        'secondary_filter': 'photo_type'
    },
    '18_👷_Subcontractor_Management.py': {
        'key_fields': ['company_name', 'trade', 'status', 'performance_rating', 'contract_value'],
        'search_fields': ['company_name', 'trade', 'contact_person'],
        'primary_filter': 'status',
        'secondary_filter': 'trade'
    },
    '19_🔧_Inspections.py': {
        'key_fields': ['inspection_type', 'inspection_date', 'inspector', 'result', 'status'],
        'search_fields': ['location', 'inspector', 'inspection_type'],
        'primary_filter': 'result',
        'secondary_filter': 'status'
    },
    '20_⚠️_Issues_Risks.py': {
        'key_fields': ['type', 'title', 'category', 'priority', 'status'],
        'search_fields': ['title', 'description', 'assigned_to', 'reported_by'],
        'primary_filter': 'status',
        'secondary_filter': 'priority'
    },
    '21_📁_Documents.py': {
        'key_fields': ['document_name', 'document_type', 'category', 'status', 'date_created'],
        'search_fields': ['document_name', 'category', 'created_by'],
        'primary_filter': 'status',
        'secondary_filter': 'category'
    },
    '22_💲_Unit_Prices.py': {
        'key_fields': ['item_code', 'description', 'unit', 'unit_price', 'category'],
        'search_fields': ['description', 'item_code', 'category'],
        'primary_filter': 'category',
        'secondary_filter': 'unit'
    },
    '23_📦_Material_Management.py': {
        'key_fields': ['material_code', 'material_name', 'category', 'quantity_on_hand', 'status'],
        'search_fields': ['material_name', 'material_code', 'supplier'],
        'primary_filter': 'status',
        'secondary_filter': 'category'
    },
    '24_🚜_Equipment_Tracking.py': {
        'key_fields': ['equipment_id', 'equipment_name', 'equipment_type', 'status', 'location'],
        'search_fields': ['equipment_name', 'equipment_id', 'assigned_to'],
        'primary_filter': 'status',
        'secondary_filter': 'equipment_type'
    }
}

def update_display_config(file_path, config):
    """Update the display_config in a page file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Build new key_fields string
    key_fields_str = str(config['key_fields'])
    search_fields_str = str(config['search_fields'])
    
    # Replace key_fields pattern
    content = re.sub(
        r"'key_fields': \[.*?\]",
        f"'key_fields': {key_fields_str}",
        content,
        flags=re.DOTALL
    )
    
    # Replace search_fields pattern
    content = re.sub(
        r"'search_fields': \[.*?\]",
        f"'search_fields': {search_fields_str}",
        content,
        flags=re.DOTALL
    )
    
    # Update primary filter
    content = re.sub(
        r"'field': '[^']*'",
        f"'field': '{config['primary_filter']}'",
        content
    )
    
    with open(file_path, 'w') as f:
        f.write(content)

def main():
    """Update all module pages"""
    pages_dir = 'pages'
    
    for filename, config in MODULE_CONFIGS.items():
        file_path = os.path.join(pages_dir, filename)
        if os.path.exists(file_path):
            print(f"Updating {filename}...")
            update_display_config(file_path, config)
        else:
            print(f"File not found: {file_path}")
    
    print("All pages updated with standardized configurations!")

if __name__ == "__main__":
    main()