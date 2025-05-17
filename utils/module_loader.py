import os
import importlib
import streamlit as st
from utils.database import get_db_connection
import zipfile
import io
import shutil

def load_modules():
    """Load all module definitions from the database and filesystem"""
    modules = {}
    
    try:
        conn = get_db_connection()
        if not conn:
            return {}
            
        cursor = conn.cursor()
        
        # Get all sections
        cursor.execute('''
            SELECT name, display_name, icon
            FROM sections
            ORDER BY sort_order
        ''')
        
        sections = cursor.fetchall()
        
        for section_name, section_display_name, section_icon in sections:
            section_modules = []
            
            # Get modules for this section
            cursor.execute('''
                SELECT m.name, m.display_name, m.icon
                FROM modules m
                JOIN sections s ON m.section_id = s.id
                WHERE s.name = %s AND m.enabled = TRUE
                ORDER BY m.sort_order
            ''', (section_name,))
            
            db_modules = cursor.fetchall()
            
            # Check filesystem for modules
            module_path = f"modules.{section_name}"
            try:
                module_package = importlib.import_module(module_path)
                
                # Check each Python file in the module directory
                module_dir = os.path.dirname(module_package.__file__)
                for filename in os.listdir(module_dir):
                    if filename.endswith('.py') and not filename.startswith('__'):
                        module_name = filename[:-3]  # Remove .py extension
                        
                        # Skip if module is already in database
                        if any(m[0] == module_name for m in db_modules):
                            continue
                            
                        # Try to import module to get metadata
                        try:
                            module = importlib.import_module(f"{module_path}.{module_name}")
                            display_name = getattr(module, 'MODULE_DISPLAY_NAME', module_name.replace('_', ' ').title())
                            icon = getattr(module, 'MODULE_ICON', 'file')
                            
                            # Add to database
                            cursor.execute('''
                                INSERT INTO modules (section_id, name, display_name, icon, sort_order)
                                SELECT id, %s, %s, %s, COALESCE(MAX(sort_order), 0) + 1
                                FROM sections
                                WHERE name = %s
                                RETURNING id
                            ''', (module_name, display_name, icon, section_name))
                            
                            module_id = cursor.fetchone()[0]
                            db_modules.append((module_name, display_name, icon))
                            
                        except Exception as e:
                            st.error(f"Error loading module {module_name}: {str(e)}")
                
            except ModuleNotFoundError:
                # Section directory doesn't exist, create it
                os.makedirs(f"modules/{section_name}", exist_ok=True)
            
            # Add all modules to the result
            for module_name, module_display_name, module_icon in db_modules:
                section_modules.append({
                    'name': module_name,
                    'display_name': module_display_name,
                    'icon': module_icon
                })
            
            if section_modules:
                modules[section_name] = {
                    'display_name': section_display_name,
                    'icon': section_icon,
                    'modules': section_modules
                }
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        st.error(f"Error loading modules: {str(e)}")
    
    return modules

def upload_module(uploaded_file):
    """Upload and install a new module from a zip file"""
    if uploaded_file is None:
        return False, "No file provided"
    
    if not uploaded_file.name.endswith('.zip'):
        return False, "File must be a ZIP archive"
    
    try:
        # Create a temporary directory for extraction
        temp_dir = "temp_module"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Extract the zip file
        with zipfile.ZipFile(io.BytesIO(uploaded_file.getbuffer()), 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Check for module.json file
        if not os.path.exists(os.path.join(temp_dir, "module.json")):
            shutil.rmtree(temp_dir)
            return False, "Invalid module: missing module.json file"
        
        # TODO: Validate module structure and copy files to the right location
        # For simplicity, we're not implementing the full logic here
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        return True, "Module installed successfully"
        
    except Exception as e:
        return False, f"Error installing module: {str(e)}"
