"""
Pure Python File Operations for Highland Tower Development
Framework-independent file handling, document management, and data export

This eliminates dependency on Streamlit's file upload/download and provides
sustainable file operations using standard Python libraries
"""

import os
import json
import csv
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, BinaryIO
from datetime import datetime
import hashlib
import mimetypes

from .data_models import Document
from .business_logic import highland_tower_manager


class FileManager:
    """Pure Python file operations manager"""
    
    def __init__(self, base_upload_dir: str = "uploads"):
        self.base_dir = Path(base_upload_dir)
        self.base_dir.mkdir(exist_ok=True)
        
        # Create project-specific directories
        self.highland_dir = self.base_dir / "highland_tower"
        self.highland_dir.mkdir(exist_ok=True)
        
        # Document categories
        self.doc_categories = {
            "rfis": self.highland_dir / "rfis",
            "contracts": self.highland_dir / "contracts", 
            "drawings": self.highland_dir / "drawings",
            "photos": self.highland_dir / "photos",
            "reports": self.highland_dir / "reports"
        }
        
        for category_path in self.doc_categories.values():
            category_path.mkdir(exist_ok=True)
    
    def save_file(self, file_content: bytes, filename: str, category: str = "general") -> Dict[str, Any]:
        """Save file to appropriate directory"""
        try:
            # Generate safe filename
            safe_filename = self._generate_safe_filename(filename)
            
            # Determine save path
            if category in self.doc_categories:
                save_path = self.doc_categories[category] / safe_filename
            else:
                save_path = self.highland_dir / safe_filename
            
            # Write file
            with open(save_path, 'wb') as f:
                f.write(file_content)
            
            # Generate file metadata
            file_hash = self._calculate_file_hash(file_content)
            file_size = len(file_content)
            mime_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            
            document_record = {
                "id": f"DOC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "title": filename,
                "filename": safe_filename,
                "file_path": str(save_path),
                "category": category,
                "file_size": file_size,
                "mime_type": mime_type,
                "file_hash": file_hash,
                "upload_date": datetime.now().isoformat(),
                "project_id": "HTD-2024-001"
            }
            
            return {
                "success": True,
                "document": document_record,
                "message": f"File saved successfully: {safe_filename}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to save file: {filename}"
            }
    
    def get_file(self, file_path: str) -> Optional[bytes]:
        """Retrieve file content"""
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                with open(path, 'rb') as f:
                    return f.read()
            return None
        except Exception:
            return None
    
    def delete_file(self, file_path: str) -> bool:
        """Delete file safely"""
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                # Ensure file is within our managed directories
                if str(path).startswith(str(self.base_dir)):
                    path.unlink()
                    return True
            return False
        except Exception:
            return False
    
    def list_files(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List files in category or all files"""
        files = []
        
        try:
            if category and category in self.doc_categories:
                search_path = self.doc_categories[category]
            else:
                search_path = self.highland_dir
            
            for file_path in search_path.rglob('*'):
                if file_path.is_file():
                    stat = file_path.stat()
                    files.append({
                        "filename": file_path.name,
                        "path": str(file_path),
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "category": category or "general"
                    })
            
            return files
            
        except Exception:
            return []
    
    def _generate_safe_filename(self, filename: str) -> str:
        """Generate safe filename with timestamp"""
        # Remove unsafe characters
        safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_"
        safe_name = ''.join(c if c in safe_chars else '_' for c in filename)
        
        # Add timestamp to prevent conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(safe_name)
        
        return f"{name}_{timestamp}{ext}"
    
    def _calculate_file_hash(self, content: bytes) -> str:
        """Calculate SHA-256 hash of file content"""
        return hashlib.sha256(content).hexdigest()


class DataExporter:
    """Pure Python data export functionality"""
    
    @staticmethod
    def export_rfis_to_csv() -> str:
        """Export RFI data to CSV format"""
        rfis = highland_tower_manager.get_rfis()
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        
        try:
            writer = csv.writer(temp_file)
            
            # Write headers
            headers = [
                'RFI Number', 'Subject', 'Description', 'Location', 'Discipline',
                'Priority', 'Status', 'Submitted By', 'Assigned To', 'Submitted Date',
                'Due Date', 'Days Open', 'Cost Impact', 'Schedule Impact'
            ]
            writer.writerow(headers)
            
            # Write RFI data
            for rfi in rfis:
                writer.writerow([
                    rfi.number, rfi.subject, rfi.description, rfi.location,
                    rfi.discipline.value.title(), rfi.priority.value.title(),
                    rfi.status.value.title(), rfi.submitted_by, rfi.assigned_to,
                    rfi.submitted_date.isoformat(), rfi.due_date.isoformat(),
                    rfi.days_open, rfi.cost_impact, rfi.schedule_impact
                ])
            
            temp_file.close()
            return temp_file.name
            
        except Exception as e:
            temp_file.close()
            os.unlink(temp_file.name)
            raise e
    
    @staticmethod
    def export_project_data_to_json() -> str:
        """Export complete project data to JSON"""
        project_data = highland_tower_manager.export_project_data()
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        
        try:
            json.dump(project_data, temp_file, indent=2, default=str)
            temp_file.close()
            return temp_file.name
            
        except Exception as e:
            temp_file.close()
            os.unlink(temp_file.name)
            raise e
    
    @staticmethod
    def export_subcontractors_to_csv() -> str:
        """Export subcontractor data to CSV"""
        subcontractors = highland_tower_manager.get_subcontractors()
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        
        try:
            writer = csv.writer(temp_file)
            
            headers = [
                'Company Name', 'Contact Person', 'Email', 'Phone', 'License Number',
                'Insurance Expiry', 'Specialties', 'Performance Rating', 'Active Projects',
                'Total Contract Value'
            ]
            writer.writerow(headers)
            
            for sub in subcontractors:
                writer.writerow([
                    sub.company_name, sub.contact_person, sub.email, sub.phone,
                    sub.license_number, sub.insurance_expiry.isoformat(),
                    ', '.join(sub.specialties), sub.performance_rating,
                    sub.active_projects, sub.total_contract_value
                ])
            
            temp_file.close()
            return temp_file.name
            
        except Exception as e:
            temp_file.close()
            os.unlink(temp_file.name)
            raise e


class ReportGenerator:
    """Pure Python report generation"""
    
    @staticmethod
    def generate_project_summary_report() -> Dict[str, Any]:
        """Generate comprehensive project summary report"""
        health_metrics = highland_tower_manager.get_project_health_metrics()
        rfi_stats = highland_tower_manager.get_rfi_statistics()
        sub_stats = highland_tower_manager.get_subcontractor_performance_summary()
        
        report = {
            "report_title": "Highland Tower Development - Project Summary",
            "generated_date": datetime.now().isoformat(),
            "project_overview": {
                "name": "Highland Tower Development",
                "value": "$45.5M",
                "type": "Mixed-Use Development",
                "residential_units": 120,
                "retail_units": 8,
                "floors": "15 above ground, 2 below",
                "status": "Active Development"
            },
            "health_metrics": health_metrics,
            "rfi_summary": rfi_stats,
            "subcontractor_summary": sub_stats,
            "key_highlights": [
                f"Project is {health_metrics['progress_percent']}% complete",
                f"{rfi_stats['open']} active RFIs requiring attention",
                f"${health_metrics['budget_remaining']:,.0f} budget remaining",
                f"{sub_stats.get('total_subcontractors', 0)} active subcontractors"
            ],
            "action_items": []
        }
        
        # Add action items based on data
        if rfi_stats['critical'] > 0:
            report["action_items"].append(f"Address {rfi_stats['critical']} critical RFIs immediately")
        
        if rfi_stats['overdue'] > 0:
            report["action_items"].append(f"Follow up on {rfi_stats['overdue']} overdue RFIs")
        
        if health_metrics['overall_health_score'] < 80:
            report["action_items"].append("Review project health - score below optimal range")
        
        return report
    
    @staticmethod
    def generate_rfi_status_report() -> Dict[str, Any]:
        """Generate detailed RFI status report"""
        rfis = highland_tower_manager.get_rfis()
        stats = highland_tower_manager.get_rfi_statistics()
        
        # Group RFIs by status
        rfi_by_status = {}
        for rfi in rfis:
            status = rfi.status.value
            if status not in rfi_by_status:
                rfi_by_status[status] = []
            rfi_by_status[status].append({
                "number": rfi.number,
                "subject": rfi.subject,
                "priority": rfi.priority.value,
                "days_open": rfi.days_open,
                "assigned_to": rfi.assigned_to
            })
        
        return {
            "report_title": "Highland Tower Development - RFI Status Report",
            "generated_date": datetime.now().isoformat(),
            "summary_statistics": stats,
            "rfis_by_status": rfi_by_status,
            "priority_breakdown": {
                priority.value: len([rfi for rfi in rfis if rfi.priority == priority])
                for priority in {rfi.priority for rfi in rfis}
            },
            "discipline_breakdown": {
                discipline.value: len([rfi for rfi in rfis if rfi.discipline == discipline])
                for discipline in {rfi.discipline for rfi in rfis}
            }
        }


# Global instances
file_manager = FileManager()
data_exporter = DataExporter()
report_generator = ReportGenerator()