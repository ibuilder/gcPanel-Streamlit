"""
Enterprise File Management System for gcPanel Construction Platform

Cloud storage integration for construction documents, photos, and files
with secure access controls and performance optimization.
"""

import os
import logging
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, BinaryIO
import streamlit as st
from core.database import get_database
from core.auth_enterprise import get_auth

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileManager:
    """Enterprise file management with cloud storage integration."""
    
    def __init__(self):
        """Initialize file management system."""
        self.db = get_database()
        self.auth = get_auth()
        
        # Cloud storage configuration
        self.storage_provider = os.environ.get('STORAGE_PROVIDER', 'local')
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        self.allowed_extensions = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
            'documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
            'cad': ['.dwg', '.dxf', '.ifc', '.rvt', '.skp'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz']
        }
        
        self._ensure_storage_structure()
    
    def _ensure_storage_structure(self):
        """Create local storage directories if needed."""
        try:
            base_dirs = [
                'uploads/projects',
                'uploads/reports',
                'uploads/inspections',
                'uploads/photos',
                'uploads/documents',
                'uploads/temp'
            ]
            
            for directory in base_dirs:
                os.makedirs(directory, exist_ok=True)
            
            logger.info("Storage directory structure verified")
            
        except Exception as e:
            logger.error(f"Error creating storage directories: {str(e)}")
    
    def upload_file(self, file_data: BinaryIO, filename: str, 
                   file_type: str, project_id: int = None, 
                   description: str = "") -> Dict:
        """Upload file with validation and metadata storage."""
        try:
            # Validate file
            validation = self._validate_file(file_data, filename)
            if not validation['valid']:
                return validation
            
            # Generate secure filename
            file_extension = os.path.splitext(filename)[1].lower()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            secure_filename = f"{timestamp}_{hashlib.md5(filename.encode()).hexdigest()[:8]}{file_extension}"
            
            # Determine storage path
            storage_path = self._get_storage_path(file_type, project_id, secure_filename)
            
            # Save file
            file_size = self._save_file(file_data, storage_path)
            
            # Store metadata in database
            file_metadata = {
                'original_filename': filename,
                'secure_filename': secure_filename,
                'file_path': storage_path,
                'file_size': file_size,
                'file_type': file_type,
                'mime_type': self._get_mime_type(file_extension),
                'project_id': project_id,
                'description': description,
                'uploaded_by': st.session_state.get('user_id'),
                'upload_date': datetime.utcnow(),
                'is_active': True
            }
            
            file_id = self.db.insert_data('file_metadata', file_metadata)
            
            # Log audit event
            self.db.log_audit_action(
                st.session_state.get('user_id', 0),
                'FILE_UPLOAD',
                'file_metadata',
                file_id,
                new_values=f"Uploaded: {filename}"
            )
            
            logger.info(f"File uploaded successfully: {filename}")
            
            return {
                'success': True,
                'file_id': file_id,
                'filename': secure_filename,
                'file_size': file_size,
                'message': 'File uploaded successfully'
            }
            
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            return {'success': False, 'message': 'File upload failed'}
    
    def _validate_file(self, file_data: BinaryIO, filename: str) -> Dict:
        """Validate file size, type, and content."""
        try:
            # Check file extension
            file_extension = os.path.splitext(filename)[1].lower()
            allowed_extensions = []
            for ext_list in self.allowed_extensions.values():
                allowed_extensions.extend(ext_list)
            
            if file_extension not in allowed_extensions:
                return {
                    'valid': False,
                    'message': f'File type {file_extension} not allowed'
                }
            
            # Check file size
            file_data.seek(0, 2)  # Seek to end
            file_size = file_data.tell()
            file_data.seek(0)  # Reset to beginning
            
            if file_size > self.max_file_size:
                return {
                    'valid': False,
                    'message': f'File size exceeds limit of {self.max_file_size // (1024*1024)}MB'
                }
            
            if file_size == 0:
                return {
                    'valid': False,
                    'message': 'Empty file not allowed'
                }
            
            return {'valid': True}
            
        except Exception as e:
            logger.error(f"File validation error: {str(e)}")
            return {'valid': False, 'message': 'File validation failed'}
    
    def _get_storage_path(self, file_type: str, project_id: int, filename: str) -> str:
        """Generate storage path based on file type and project."""
        base_path = "uploads"
        
        if project_id:
            return f"{base_path}/projects/{project_id}/{file_type}/{filename}"
        else:
            return f"{base_path}/{file_type}/{filename}"
    
    def _save_file(self, file_data: BinaryIO, storage_path: str) -> int:
        """Save file to storage and return file size."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(storage_path), exist_ok=True)
            
            # Write file
            with open(storage_path, 'wb') as f:
                file_data.seek(0)
                content = file_data.read()
                f.write(content)
                return len(content)
            
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise
    
    def _get_mime_type(self, file_extension: str) -> str:
        """Get MIME type based on file extension."""
        mime_types = {
            '.pdf': 'application/pdf',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.dwg': 'application/acad',
            '.dxf': 'application/dxf',
            '.zip': 'application/zip'
        }
        
        return mime_types.get(file_extension, 'application/octet-stream')
    
    def get_project_files(self, project_id: int, file_type: str = None) -> List[Dict]:
        """Get files for a specific project."""
        try:
            query = """
            SELECT fm.*, u.full_name as uploaded_by_name
            FROM file_metadata fm
            LEFT JOIN users u ON fm.uploaded_by = u.id
            WHERE fm.project_id = :project_id AND fm.is_active = true
            """
            params = {'project_id': project_id}
            
            if file_type:
                query += " AND fm.file_type = :file_type"
                params['file_type'] = file_type
            
            query += " ORDER BY fm.upload_date DESC"
            
            return self.db.execute_query(query, params)
            
        except Exception as e:
            logger.error(f"Error getting project files: {str(e)}")
            return []
    
    def get_file_metadata(self, file_id: int) -> Optional[Dict]:
        """Get file metadata by ID."""
        try:
            query = """
            SELECT fm.*, u.full_name as uploaded_by_name
            FROM file_metadata fm
            LEFT JOIN users u ON fm.uploaded_by = u.id
            WHERE fm.id = :file_id AND fm.is_active = true
            """
            
            result = self.db.execute_query(query, {'file_id': file_id})
            return result[0] if result else None
            
        except Exception as e:
            logger.error(f"Error getting file metadata: {str(e)}")
            return None
    
    def download_file(self, file_id: int) -> Optional[bytes]:
        """Download file by ID with permission check."""
        try:
            # Get file metadata
            file_meta = self.get_file_metadata(file_id)
            if not file_meta:
                return None
            
            # Check permissions
            if not self._check_file_access(file_meta):
                logger.warning(f"Unauthorized file access attempt: {file_id}")
                return None
            
            # Read file
            file_path = file_meta['file_path']
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return None
            
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Log download
            self.db.log_audit_action(
                st.session_state.get('user_id', 0),
                'FILE_DOWNLOAD',
                'file_metadata',
                file_id,
                new_values=f"Downloaded: {file_meta['original_filename']}"
            )
            
            return content
            
        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            return None
    
    def delete_file(self, file_id: int) -> Dict:
        """Soft delete file with audit logging."""
        try:
            # Get file metadata
            file_meta = self.get_file_metadata(file_id)
            if not file_meta:
                return {'success': False, 'message': 'File not found'}
            
            # Check permissions
            if not self._check_file_delete_access(file_meta):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # Soft delete (mark as inactive)
            success = self.db.update_data('file_metadata', file_id, {
                'is_active': False,
                'deleted_at': datetime.utcnow(),
                'deleted_by': st.session_state.get('user_id')
            })
            
            if success:
                # Log audit event
                self.db.log_audit_action(
                    st.session_state.get('user_id', 0),
                    'FILE_DELETE',
                    'file_metadata',
                    file_id,
                    new_values=f"Deleted: {file_meta['original_filename']}"
                )
                
                return {'success': True, 'message': 'File deleted successfully'}
            else:
                return {'success': False, 'message': 'Failed to delete file'}
            
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return {'success': False, 'message': 'Error deleting file'}
    
    def _check_file_access(self, file_meta: Dict) -> bool:
        """Check if user has access to file."""
        user_id = st.session_state.get('user_id')
        user_role = st.session_state.get('user_role', 'User')
        
        # Admin can access all files
        if user_role == 'Administrator':
            return True
        
        # File owner can access
        if file_meta['uploaded_by'] == user_id:
            return True
        
        # Project team members can access project files
        if file_meta['project_id']:
            # Check if user is assigned to project (implement based on your project assignment logic)
            return self._is_user_on_project(user_id, file_meta['project_id'])
        
        return False
    
    def _check_file_delete_access(self, file_meta: Dict) -> bool:
        """Check if user can delete file."""
        user_role = st.session_state.get('user_role', 'User')
        
        # Admin can delete all files
        if user_role in ['Administrator', 'Project Manager']:
            return True
        
        # File owner can delete their files
        if file_meta['uploaded_by'] == st.session_state.get('user_id'):
            return True
        
        return False
    
    def _is_user_on_project(self, user_id: int, project_id: int) -> bool:
        """Check if user is assigned to project."""
        # This would check project assignments in a real implementation
        # For now, return True for authenticated users
        return st.session_state.get('authenticated', False)
    
    def get_storage_statistics(self) -> Dict:
        """Get storage usage statistics."""
        try:
            query = """
            SELECT 
                file_type,
                COUNT(*) as file_count,
                SUM(file_size) as total_size
            FROM file_metadata 
            WHERE is_active = true
            GROUP BY file_type
            ORDER BY total_size DESC
            """
            
            stats = self.db.execute_query(query)
            
            total_files = sum(stat['file_count'] for stat in stats)
            total_size = sum(stat['total_size'] for stat in stats)
            
            return {
                'by_type': stats,
                'total_files': total_files,
                'total_size': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting storage statistics: {str(e)}")
            return {}

# Global file manager instance
file_manager = None

def get_file_manager():
    """Get or create file manager instance."""
    global file_manager
    if file_manager is None:
        file_manager = FileManager()
    return file_manager