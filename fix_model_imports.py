"""
Script to fix model import paths after reorganization
"""

import os
import glob

def fix_model_imports():
    """Fix import paths in all model files"""
    
    # Fix imports in model files
    for model_file in glob.glob('lib/models/*.py'):
        if model_file.endswith('__init__.py') or model_file.endswith('base_model.py'):
            continue
            
        with open(model_file, 'r') as f:
            content = f.read()
        
        # Fix base model import
        content = content.replace(
            'from models.base_model import BaseModel',
            'from lib.models.base_model import BaseModel'
        )
        
        # Fix data import
        content = content.replace(
            'from data.highland_tower_data import',
            'from lib.data.highland_tower_data import'
        )
        
        with open(model_file, 'w') as f:
            f.write(content)
        
        print(f"Fixed imports in {model_file}")

def fix_base_model_import():
    """Fix highland tower data import in base model"""
    base_model_path = 'lib/models/base_model.py'
    
    with open(base_model_path, 'r') as f:
        content = f.read()
    
    # Fix highland tower data import
    content = content.replace(
        'from data.highland_tower_data import HIGHLAND_TOWER_DATA',
        'from lib.data.highland_tower_data import HIGHLAND_TOWER_DATA'
    )
    
    with open(base_model_path, 'w') as f:
        f.write(content)
    
    print(f"Fixed highland tower data import in {base_model_path}")

def main():
    """Fix all model imports"""
    fix_model_imports()
    fix_base_model_import()
    print("All model imports fixed!")

if __name__ == "__main__":
    main()