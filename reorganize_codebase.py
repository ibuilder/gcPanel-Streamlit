"""
Script to reorganize codebase into proper Streamlit structure
"""

import os
import shutil
import glob

def create_streamlit_structure():
    """Create proper Streamlit directory structure"""
    
    # Create .streamlit directory for configuration
    os.makedirs('.streamlit', exist_ok=True)
    
    # Create lib directory for shared modules
    os.makedirs('lib', exist_ok=True)
    os.makedirs('lib/models', exist_ok=True)
    os.makedirs('lib/controllers', exist_ok=True)
    os.makedirs('lib/helpers', exist_ok=True)
    os.makedirs('lib/utils', exist_ok=True)
    os.makedirs('lib/data', exist_ok=True)
    os.makedirs('lib/database', exist_ok=True)
    
    # Create assets directory
    os.makedirs('assets', exist_ok=True)
    
    print("Created Streamlit directory structure")

def move_core_files():
    """Move core files to lib directory"""
    
    # Move models
    if os.path.exists('models'):
        for file in glob.glob('models/*.py'):
            if os.path.basename(file) != '__init__.py':
                shutil.copy2(file, f'lib/models/')
    
    # Move controllers
    if os.path.exists('controllers'):
        for file in glob.glob('controllers/*.py'):
            if os.path.basename(file) != '__init__.py':
                shutil.copy2(file, f'lib/controllers/')
    
    # Move helpers
    if os.path.exists('helpers'):
        for file in glob.glob('helpers/*.py'):
            if os.path.basename(file) != '__init__.py':
                shutil.copy2(file, f'lib/helpers/')
    
    # Move utils
    if os.path.exists('utils'):
        for file in glob.glob('utils/*.py'):
            if os.path.basename(file) != '__init__.py':
                shutil.copy2(file, f'lib/utils/')
    
    # Move database files
    if os.path.exists('database'):
        for file in glob.glob('database/*.py'):
            if os.path.basename(file) != '__init__.py':
                shutil.copy2(file, f'lib/database/')
    
    # Move data files
    if os.path.exists('data/highland_tower_data.py'):
        shutil.copy2('data/highland_tower_data.py', 'lib/data/')
    
    print("Moved core files to lib directory")

def create_streamlit_config():
    """Create Streamlit configuration file"""
    
    config_content = """[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[browser]
gatherUsageStats = false
"""
    
    with open('.streamlit/config.toml', 'w') as f:
        f.write(config_content)
    
    print("Created Streamlit configuration")

def update_import_references():
    """Update import references in pages to use lib structure"""
    
    import_updates = {
        'from models.': 'from lib.models.',
        'from controllers.': 'from lib.controllers.',
        'from helpers.': 'from lib.helpers.',
        'from utils.': 'from lib.utils.',
        'from database.': 'from lib.database.',
        'from data.highland_tower_data': 'from lib.data.highland_tower_data'
    }
    
    # Update pages
    for page_file in glob.glob('pages/*.py'):
        with open(page_file, 'r') as f:
            content = f.read()
        
        # Update imports
        for old_import, new_import in import_updates.items():
            content = content.replace(old_import, new_import)
        
        with open(page_file, 'w') as f:
            f.write(content)
    
    # Update app.py
    if os.path.exists('app.py'):
        with open('app.py', 'r') as f:
            content = f.read()
        
        for old_import, new_import in import_updates.items():
            content = content.replace(old_import, new_import)
        
        with open('app.py', 'w') as f:
            f.write(content)
    
    print("Updated import references")

def create_lib_init_files():
    """Create __init__.py files for lib modules"""
    
    init_dirs = [
        'lib',
        'lib/models',
        'lib/controllers', 
        'lib/helpers',
        'lib/utils',
        'lib/data',
        'lib/database'
    ]
    
    for dir_path in init_dirs:
        init_file = os.path.join(dir_path, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('"""Streamlit gcPanel library module"""\n')
    
    print("Created __init__.py files")

def clean_redundant_directories():
    """Remove old directory structure after copying"""
    
    # Remove duplicate directories (keep originals as backup for now)
    dirs_to_clean = ['components', 'core', 'modules', 'integrations']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            # Move to backup instead of deleting
            backup_name = f"{dir_name}_backup"
            if os.path.exists(backup_name):
                shutil.rmtree(backup_name)
            os.rename(dir_name, backup_name)
            print(f"Moved {dir_name} to {backup_name}")

def move_assets():
    """Move assets to proper location"""
    
    if os.path.exists('attached_assets'):
        # Move specific assets we need
        asset_files = [
            'gcpanel.png',
            'gcpanel-streamlit2.png',
            'margins-layout-gcpanel1.png'
        ]
        
        for asset in asset_files:
            src = f'attached_assets/{asset}'
            if os.path.exists(src):
                shutil.copy2(src, f'assets/{asset}')
    
    # Move root assets
    if os.path.exists('gcpanel.png'):
        shutil.copy2('gcpanel.png', 'assets/')
    
    print("Moved assets")

def main():
    """Main reorganization function"""
    print("Starting codebase reorganization...")
    
    create_streamlit_structure()
    move_core_files()
    create_streamlit_config()
    create_lib_init_files()
    update_import_references()
    move_assets()
    clean_redundant_directories()
    
    print("Codebase reorganization complete!")
    print("\nNew structure:")
    print("├── app.py                 # Main Streamlit app")
    print("├── pages/                 # Streamlit pages")
    print("├── lib/                   # Shared library modules")
    print("│   ├── models/           # Data models")
    print("│   ├── controllers/      # Business logic")
    print("│   ├── helpers/          # UI helpers")
    print("│   ├── utils/            # Utilities")
    print("│   ├── data/             # Data files")
    print("│   └── database/         # Database modules")
    print("├── assets/               # Static assets")
    print("└── .streamlit/           # Streamlit configuration")

if __name__ == "__main__":
    main()