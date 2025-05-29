"""
Script to update all page imports to use the new lib structure
"""

import os
import re

def update_page_imports(file_path):
    """Update imports in a page file to use lib structure"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Update sys.path.append to add lib to path
    content = re.sub(
        r'sys\.path\.append\(os\.path\.dirname\(os\.path\.dirname\(os\.path\.abspath\(__file__\)\)\)\)',
        'sys.path.append(os.path.dirname(os.path.abspath(__file__)))',
        content
    )
    
    # Update import statements
    import_mappings = {
        'from utils.helpers import': 'from lib.utils.helpers import',
        'from models.all_models import': 'from lib.models.all_models import',
        'from models.': 'from lib.models.',
        'from controllers.crud_controller import': 'from lib.controllers.crud_controller import',
        'from helpers.ui_helpers import': 'from lib.helpers.ui_helpers import',
        'from data.highland_tower_data import': 'from lib.data.highland_tower_data import'
    }
    
    for old_import, new_import in import_mappings.items():
        content = content.replace(old_import, new_import)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Updated imports in {file_path}")

def update_app_imports():
    """Update imports in app.py"""
    if os.path.exists('app.py'):
        with open('app.py', 'r') as f:
            content = f.read()
        
        # Update import statements
        import_mappings = {
            'from utils.helpers import': 'from lib.utils.helpers import',
            'from database.connection import': 'from lib.database.connection import',
            'from helpers.ui_helpers import': 'from lib.helpers.ui_helpers import'
        }
        
        for old_import, new_import in import_mappings.items():
            content = content.replace(old_import, new_import)
        
        with open('app.py', 'w') as f:
            f.write(content)
        
        print("Updated imports in app.py")

def main():
    """Update all page imports"""
    # Update all pages
    for filename in os.listdir('pages'):
        if filename.endswith('.py'):
            file_path = os.path.join('pages', filename)
            update_page_imports(file_path)
    
    # Update app.py
    update_app_imports()
    
    print("All imports updated to use lib structure!")

if __name__ == "__main__":
    main()