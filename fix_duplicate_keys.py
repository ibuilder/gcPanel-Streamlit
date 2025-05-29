#!/usr/bin/env python3
"""
Script to fix duplicate element ID errors by adding unique keys to search inputs
"""

import os
import re

# Define the pages and their unique search keys
pages_config = {
    "pages/02_📋_Daily_Reports.py": "daily_reports",
    "pages/03_📄_RFIs.py": "rfis", 
    "pages/04_📨_Submittals.py": "submittals",
    "pages/05_📑_Contracts.py": "contracts",
    "pages/06_🦺_Safety.py": "safety",
    "pages/07_🚚_Deliveries.py": "deliveries",
    "pages/08_🏗️_Preconstruction.py": "preconstruction",
    "pages/09_⚙️_Engineering.py": "engineering",
    "pages/10_🏭_Field_Operations.py": "field_operations",
    "pages/11_💰_Cost_Management.py": "cost_management",
    "pages/12_🏗️_BIM.py": "bim",
    "pages/13_🏁_Closeout.py": "closeout",
    "pages/14_📺_Transmittals.py": "transmittals",
    "pages/15_📅_Scheduling.py": "scheduling",
    "pages/16_🔍_Quality_Control.py": "quality_control",
    "pages/17_📸_Progress_Photos.py": "progress_photos",
    "pages/18_👷_Subcontractor_Management.py": "subcontractor_management",
    "pages/19_🔧_Inspections.py": "inspections",
    "pages/20_⚠️_Issues_Risks.py": "issues_risks",
    "pages/21_📁_Documents.py": "documents",
    "pages/22_💲_Unit_Prices.py": "unit_prices",
    "pages/23_📦_Material_Management.py": "material_management",
    "pages/24_🚜_Equipment_Tracking.py": "equipment_tracking",
}

def fix_search_inputs():
    for file_path, key_prefix in pages_config.items():
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Find all text_input with search pattern and add unique keys
            pattern = r'st\.text_input\("🔍 Search[^"]*"[^)]*\)'
            matches = re.findall(pattern, content)
            
            counter = 1
            for match in matches:
                # Only add key if it doesn't already have one
                if 'key=' not in match:
                    new_match = match[:-1] + f', key="{key_prefix}_search_{counter}")'
                    content = content.replace(match, new_match, 1)
                    counter += 1
            
            with open(file_path, 'w') as f:
                f.write(content)
            
            print(f"Fixed {file_path}")

if __name__ == "__main__":
    fix_search_inputs()
    print("All search input duplicate keys have been fixed!")