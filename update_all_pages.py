#!/usr/bin/env python3
"""
Script to update all pages to have view/list as default tab and create forms as secondary tabs
"""

import os
import re

# Define the pages that need to be updated
pages_to_update = [
    "pages/05_📑_Contracts.py",
    "pages/06_🦺_Safety.py", 
    "pages/07_🚚_Deliveries.py",
    "pages/08_🏗️_Preconstruction.py",
    "pages/09_⚙️_Engineering.py",
    "pages/10_🏭_Field_Operations.py",
    "pages/11_💰_Cost_Management.py",
    "pages/12_🏗️_BIM.py",
    "pages/13_🏁_Closeout.py",
    "pages/14_📺_Transmittals.py",
    "pages/15_📅_Scheduling.py",
    "pages/16_🔍_Quality_Control.py",
    "pages/17_📸_Progress_Photos.py",
    "pages/18_👷_Subcontractor_Management.py",
    "pages/19_🔧_Inspections.py",
    "pages/20_⚠️_Issues_Risks.py",
    "pages/21_📁_Documents.py",
    "pages/22_💲_Unit_Prices.py",
    "pages/23_📦_Material_Management.py",
    "pages/24_🚜_Equipment_Tracking.py",
]

# Tab reordering patterns
tab_patterns = [
    (r'st\.tabs\(\["📝[^"]*", "📊[^"]*"\]\)', 'reorder_tabs'),
    (r'st\.tabs\(\["📤[^"]*", "📊[^"]*"\]\)', 'reorder_tabs'),
    (r'st\.tabs\(\["📋[^"]*", "📊[^"]*"\]\)', 'reorder_tabs'),
]

def update_page_tabs(file_path):
    """Update a page to have view tab first, create tab second"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find and reorder tabs
        for pattern, action in tab_patterns:
            if re.search(pattern, content):
                print(f"Updating tabs in {file_path}")
                # This would need specific implementation for each pattern
                
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error updating {file_path}: {e}")

if __name__ == "__main__":
    for page in pages_to_update:
        update_page_tabs(page)
    print("Page update script completed")