import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.database import get_db_connection
from utils.auth import check_permission

# Module metadata
MODULE_DISPLAY_NAME = "File Explorer"
MODULE_ICON = "folder"

def init_database():
    """Initialize the database tables"""
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        cursor = conn.cursor()
        
        # Create folders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_folders (
                id SERIAL PRIMARY KEY,
                parent_id INTEGER REFERENCES file_folders(id),
                name VARCHAR(255) NOT NULL,
                path VARCHAR(255) NOT NULL,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_items (
                id SERIAL PRIMARY KEY,
                folder_id INTEGER REFERENCES file_folders(id),
                name VARCHAR(255) NOT NULL,
                file_type VARCHAR(50),
                file_size INTEGER,
                storage_path VARCHAR(255),
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Check for root folder, create if not exists
        cursor.execute("SELECT COUNT(*) FROM file_folders WHERE parent_id IS NULL")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO file_folders (name, path, created_by) VALUES ('Root', '/', %s)",
                (st.session_state.get('user_id'),)
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        st.error(f"Error initializing file explorer database: {str(e)}")

def get_folder_contents(folder_id):
    """Get the contents of a folder"""
    try:
        conn = get_db_connection()
        if not conn:
            return [], []
            
        cursor = conn.cursor()
        
        # Get subfolders
        cursor.execute(
            "SELECT id, name FROM file_folders WHERE parent_id = %s ORDER BY name",
            (folder_id,)
        )
        folders = cursor.fetchall()
        
        # Get files
        cursor.execute(
            "SELECT id, name, file_type, file_size, created_at FROM file_items WHERE folder_id = %s ORDER BY name",
            (folder_id,)
        )
        files = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return folders, files
        
    except Exception as e:
        st.error(f"Error loading folder contents: {str(e)}")
        return [], []

def get_folder_path(folder_id):
    """Get the path to a folder"""
    if not folder_id:
        return [('Root', None)]
        
    try:
        conn = get_db_connection()
        if not conn:
            return [('Root', None)]
            
        cursor = conn.cursor()
        
        path = []
        current_id = folder_id
        
        while current_id is not None:
            cursor.execute(
                "SELECT id, name, parent_id FROM file_folders WHERE id = %s",
                (current_id,)
            )
            folder = cursor.fetchone()
            
            if folder:
                path.insert(0, (folder[1], folder[0]))
                current_id = folder[2]
            else:
                break
        
        cursor.close()
        conn.close()
        
        if not path:
            return [('Root', None)]
            
        return path
        
    except Exception as e:
        st.error(f"Error getting folder path: {str(e)}")
        return [('Root', None)]

def render_list():
    """Render the file explorer list view"""
    st.title("File Explorer")
    
    # Initialize database
    init_database()
    
    # Check permission
    if not check_permission('read'):
        st.error("You don't have permission to view files")
        return
    
    # Initialize session state
    if 'current_folder_id' not in st.session_state:
        # Get the root folder ID
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM file_folders WHERE parent_id IS NULL LIMIT 1")
            root_id = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            st.session_state.current_folder_id = root_id
        except Exception:
            st.session_state.current_folder_id = None
    
    # Get the current folder path
    folder_path = get_folder_path(st.session_state.current_folder_id)
    
    # Render breadcrumbs
    st.write("Location:")
    breadcrumbs = " / ".join([f"[{name}]" if i == len(folder_path) - 1 else f"[{name}](javascript:void(0))" 
                             for i, (name, _) in enumerate(folder_path)])
    st.markdown(breadcrumbs, unsafe_allow_html=True)
    
    # Create columns for the path navigation
    path_cols = st.columns(len(folder_path))
    for i, ((name, folder_id), col) in enumerate(zip(folder_path, path_cols)):
        if i < len(folder_path) - 1 and col.button(name, key=f"path_{i}"):
            st.session_state.current_folder_id = folder_id
            st.rerun()
    
    # Divider
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    # New folder button
    if check_permission('create') and col1.button("New Folder"):
        st.session_state.file_explorer_action = "new_folder"
        st.rerun()
    
    # Upload file button
    if check_permission('create') and col2.button("Upload File"):
        st.session_state.file_explorer_action = "upload_file"
        st.rerun()
    
    # Refresh button
    if col3.button("Refresh"):
        st.rerun()
    
    # Divider
    st.markdown("---")
    
    # Handle folder actions
    if st.session_state.get('file_explorer_action') == "new_folder":
        with st.form("new_folder_form"):
            folder_name = st.text_input("Folder Name")
            
            col1, col2 = st.columns(2)
            if col1.form_submit_button("Create"):
                if folder_name:
                    try:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        
                        # Get parent path
                        cursor.execute(
                            "SELECT path FROM file_folders WHERE id = %s",
                            (st.session_state.current_folder_id,)
                        )
                        parent_path = cursor.fetchone()[0]
                        
                        # Create new path
                        new_path = os.path.join(parent_path, folder_name)
                        
                        # Insert new folder
                        cursor.execute(
                            "INSERT INTO file_folders (parent_id, name, path, created_by) VALUES (%s, %s, %s, %s)",
                            (st.session_state.current_folder_id, folder_name, new_path, st.session_state.get('user_id'))
                        )
                        
                        conn.commit()
                        cursor.close()
                        conn.close()
                        
                        st.success(f"Folder '{folder_name}' created successfully")
                        st.session_state.file_explorer_action = None
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating folder: {str(e)}")
                else:
                    st.error("Folder name cannot be empty")
            
            if col2.form_submit_button("Cancel"):
                st.session_state.file_explorer_action = None
                st.rerun()
    
    elif st.session_state.get('file_explorer_action') == "upload_file":
        with st.form("upload_file_form"):
            uploaded_file = st.file_uploader("Choose a file")
            
            col1, col2 = st.columns(2)
            if col1.form_submit_button("Upload"):
                if uploaded_file is not None:
                    try:
                        # Get file details
                        file_name = uploaded_file.name
                        file_type = file_name.split('.')[-1] if '.' in file_name else 'unknown'
                        file_size = len(uploaded_file.getvalue())
                        
                        # In a real app, you would save the file to a storage service
                        # For this example, we'll just store metadata
                        
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        
                        # Insert file record
                        cursor.execute(
                            """
                            INSERT INTO file_items 
                            (folder_id, name, file_type, file_size, storage_path, created_by) 
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """,
                            (st.session_state.current_folder_id, file_name, file_type, file_size, 
                             f"/storage/{st.session_state.current_folder_id}/{file_name}", 
                             st.session_state.get('user_id'))
                        )
                        
                        conn.commit()
                        cursor.close()
                        conn.close()
                        
                        st.success(f"File '{file_name}' uploaded successfully")
                        st.session_state.file_explorer_action = None
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error uploading file: {str(e)}")
                else:
                    st.error("No file selected")
            
            if col2.form_submit_button("Cancel"):
                st.session_state.file_explorer_action = None
                st.rerun()
    
    # Get folder contents
    folders, files = get_folder_contents(st.session_state.current_folder_id)
    
    # Display folders
    if folders:
        st.subheader("Folders")
        
        folder_cols = st.columns(4)
        for i, (folder_id, folder_name) in enumerate(folders):
            col_idx = i % 4
            with folder_cols[col_idx]:
                if st.button(f"📁 {folder_name}", key=f"folder_{folder_id}"):
                    st.session_state.current_folder_id = folder_id
                    st.rerun()
    
    # Display files
    if files:
        st.subheader("Files")
        
        # Create DataFrame for display
        file_data = {
            "Name": [f[1] for f in files],
            "Type": [f[2].upper() for f in files],
            "Size": [f"{f[3] / 1024:.2f} KB" for f in files],
            "Date": [f[4].strftime("%Y-%m-%d %H:%M:%S") for f in files]
        }
        
        file_df = pd.DataFrame(file_data)
        st.dataframe(file_df)
    
    if not folders and not files:
        st.info("This folder is empty")

def render_view():
    """Render the file viewer"""
    st.title("File Viewer")
    st.info("Select a file from the File Explorer to view its details")
    
    # In a real application, we would implement file viewing/previewing functionality
    # For simplicity, we'll just show a placeholder

def render_form():
    """Render the file upload form"""
    st.title("File Upload")
    
    # For simplicity, we'll redirect to the list view
    st.session_state.file_explorer_action = "upload_file"
    st.rerun()
