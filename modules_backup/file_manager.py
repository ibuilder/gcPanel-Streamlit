"""
File Upload and Document Management for gcPanel
Handles file uploads, storage, and document management with proper validation
"""

import os
import streamlit as st
import hashlib
from datetime import datetime
from typing import Optional, List, Dict
import mimetypes
from pathlib import Path

class FileManager:
    def __init__(self):
        self.upload_dir = "uploads"
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        self.allowed_extensions = {
            'documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
            'cad': ['.dwg', '.dxf', '.ifc', '.rvt'],
            'archive': ['.zip', '.rar', '.7z', '.tar', '.gz']
        }
        
        # Create upload directory if it doesn't exist
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def get_file_hash(self, file_content: bytes) -> str:
        """Generate MD5 hash for file content"""
        return hashlib.md5(file_content).hexdigest()
    
    def get_file_category(self, filename: str) -> str:
        """Determine file category based on extension"""
        ext = Path(filename).suffix.lower()
        
        for category, extensions in self.allowed_extensions.items():
            if ext in extensions:
                return category
        return 'other'
    
    def validate_file(self, uploaded_file) -> Dict[str, any]:
        """Validate uploaded file and return validation results"""
        if not uploaded_file:
            return {'valid': False, 'error': 'No file uploaded'}
        
        # Check file size
        if uploaded_file.size > self.max_file_size:
            return {
                'valid': False, 
                'error': f'File size ({uploaded_file.size / 1024 / 1024:.1f}MB) exceeds maximum allowed size (50MB)'
            }
        
        # Check file extension
        ext = Path(uploaded_file.name).suffix.lower()
        all_allowed = []
        for extensions in self.allowed_extensions.values():
            all_allowed.extend(extensions)
        
        if ext not in all_allowed:
            return {
                'valid': False, 
                'error': f'File type {ext} not allowed. Allowed types: {", ".join(all_allowed)}'
            }
        
        return {
            'valid': True, 
            'category': self.get_file_category(uploaded_file.name),
            'mime_type': mimetypes.guess_type(uploaded_file.name)[0] or 'application/octet-stream'
        }
    
    def save_file(self, uploaded_file, project_id: int = 1) -> Optional[Dict]:
        """Save uploaded file and return file information"""
        validation = self.validate_file(uploaded_file)
        
        if not validation['valid']:
            st.error(validation['error'])
            return None
        
        try:
            # Read file content
            file_content = uploaded_file.read()
            file_hash = self.get_file_hash(file_content)
            
            # Create unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = "".join(c for c in uploaded_file.name if c.isalnum() or c in "._-")
            unique_filename = f"{timestamp}_{file_hash[:8]}_{safe_filename}"
            
            # Create project-specific directory
            project_dir = os.path.join(self.upload_dir, f"project_{project_id}")
            os.makedirs(project_dir, exist_ok=True)
            
            # Save file
            file_path = os.path.join(project_dir, unique_filename)
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # Return file information
            return {
                'original_name': uploaded_file.name,
                'file_name': unique_filename,
                'file_path': file_path,
                'file_size': len(file_content),
                'file_hash': file_hash,
                'mime_type': validation['mime_type'],
                'category': validation['category'],
                'upload_date': datetime.now()
            }
            
        except Exception as e:
            st.error(f"Error saving file: {str(e)}")
            return None
    
    def delete_file(self, file_path: str) -> bool:
        """Delete file from storage"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            st.error(f"Error deleting file: {str(e)}")
            return False
    
    def get_file_size_str(self, size_bytes: int) -> str:
        """Convert file size to human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    
    def render_file_uploader(self, document_type: str = "Document", accept_multiple: bool = False) -> Optional[List[Dict]]:
        """Render file uploader component and handle uploads"""
        st.subheader(f"Upload {document_type}")
        
        # File uploader
        uploaded_files = st.file_uploader(
            f"Choose {document_type.lower()} files",
            accept_multiple_files=accept_multiple,
            help=f"Maximum file size: 50MB. Supported formats: PDF, DOC, DOCX, XLS, XLSX, Images, CAD files"
        )
        
        if uploaded_files:
            if not isinstance(uploaded_files, list):
                uploaded_files = [uploaded_files]
            
            saved_files = []
            for uploaded_file in uploaded_files:
                with st.spinner(f"Uploading {uploaded_file.name}..."):
                    file_info = self.save_file(uploaded_file)
                    if file_info:
                        saved_files.append(file_info)
                        st.success(f"Successfully uploaded {uploaded_file.name}")
            
            return saved_files if saved_files else None
        
        return None

# Global file manager instance
@st.cache_resource
def get_file_manager():
    """Get cached file manager instance"""
    return FileManager()

def render_document_upload_section():
    """Render document upload section for any module"""
    file_manager = get_file_manager()
    
    with st.expander("📎 Upload Documents", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            document_type = st.selectbox(
                "Document Type",
                ["General Document", "Drawing", "Specification", "Photo", "Report", "Contract", "Other"]
            )
        
        with col2:
            description = st.text_input("Description (optional)")
        
        uploaded_files = file_manager.render_file_uploader(document_type, accept_multiple=True)
        
        if uploaded_files:
            st.write("**Uploaded Files:**")
            for file_info in uploaded_files:
                st.write(f"- {file_info['original_name']} ({file_manager.get_file_size_str(file_info['file_size'])})")
            
            return uploaded_files
        
        return None

def render_progress_photo_upload():
    """Render progress photo upload specifically for progress photos"""
    file_manager = get_file_manager()
    
    st.subheader("📸 Upload Progress Photos")
    
    col1, col2 = st.columns(2)
    with col1:
        photo_location = st.text_input("Photo Location", placeholder="e.g., Level 3 East Wing")
    with col2:
        weather_conditions = st.selectbox("Weather Conditions", 
                                        ["Clear", "Cloudy", "Rainy", "Sunny", "Overcast"])
    
    # File uploader specifically for images
    uploaded_files = st.file_uploader(
        "Choose photo files",
        type=['jpg', 'jpeg', 'png', 'gif'],
        accept_multiple_files=True,
        help="Upload progress photos (JPG, PNG, GIF). Maximum 50MB per file."
    )
    
    if uploaded_files:
        saved_files = []
        for uploaded_file in uploaded_files:
            with st.spinner(f"Uploading {uploaded_file.name}..."):
                file_info = file_manager.save_file(uploaded_file)
                if file_info:
                    file_info['location'] = photo_location
                    file_info['weather_conditions'] = weather_conditions
                    saved_files.append(file_info)
                    
                    # Display uploaded image
                    st.image(uploaded_file, caption=f"{uploaded_file.name} - {photo_location}", width=300)
                    st.success(f"Successfully uploaded {uploaded_file.name}")
        
        return saved_files if saved_files else None
    
    return None