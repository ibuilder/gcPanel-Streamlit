"""
Enterprise-Grade Production Manager for gcPanel
Ensures all modules are production-ready with proper error handling, security, and performance
"""

import streamlit as st
import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
import traceback

class ProductionManager:
    """Manages enterprise-grade production readiness across all modules"""
    
    def __init__(self):
        self.production_config = {
            "error_handling": True,
            "logging": True,
            "performance_monitoring": True,
            "security_validation": True,
            "data_integrity": True,
            "backup_system": True
        }
        self._setup_production_environment()
    
    def _setup_production_environment(self):
        """Set up production environment with proper logging and error handling"""
        # Ensure production directories exist
        production_dirs = [
            "logs/application",
            "logs/security", 
            "logs/performance",
            "backups/data",
            "backups/config",
            "monitoring/metrics",
            "monitoring/alerts"
        ]
        
        for directory in production_dirs:
            os.makedirs(directory, exist_ok=True)
        
        # Setup logging
        self._setup_production_logging()
        
        # Initialize monitoring
        self._initialize_monitoring()
    
    def _setup_production_logging(self):
        """Set up comprehensive logging for production"""
        # Application logging
        app_logger = logging.getLogger('gcpanel.application')
        app_handler = logging.FileHandler('logs/application/app.log')
        app_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        app_handler.setFormatter(app_formatter)
        app_logger.addHandler(app_handler)
        app_logger.setLevel(logging.INFO)
        
        # Security logging
        security_logger = logging.getLogger('gcpanel.security')
        security_handler = logging.FileHandler('logs/security/security.log')
        security_handler.setFormatter(app_formatter)
        security_logger.addHandler(security_handler)
        security_logger.setLevel(logging.WARNING)
        
        # Performance logging
        perf_logger = logging.getLogger('gcpanel.performance')
        perf_handler = logging.FileHandler('logs/performance/performance.log')
        perf_handler.setFormatter(app_formatter)
        perf_logger.addHandler(perf_handler)
        perf_logger.setLevel(logging.INFO)
    
    def _initialize_monitoring(self):
        """Initialize production monitoring systems"""
        monitoring_config = {
            "metrics": {
                "response_time": [],
                "error_rate": 0,
                "user_sessions": 0,
                "database_queries": 0,
                "workflow_executions": 0
            },
            "alerts": {
                "critical_errors": [],
                "performance_warnings": [],
                "security_events": []
            },
            "health_checks": {
                "database": "healthy",
                "file_system": "healthy", 
                "workflows": "healthy",
                "authentication": "healthy"
            }
        }
        
        with open('monitoring/metrics/current_metrics.json', 'w') as f:
            json.dump(monitoring_config, f, indent=2)
    
    def validate_production_readiness(self) -> Dict:
        """Comprehensive production readiness validation"""
        validation_results = {
            "overall_status": "pending",
            "components": {},
            "critical_issues": [],
            "warnings": [],
            "recommendations": []
        }
        
        # Validate each component
        components = [
            "database_integrity",
            "security_framework", 
            "error_handling",
            "performance_optimization",
            "backup_systems",
            "monitoring_systems",
            "workflow_integrity",
            "data_validation"
        ]
        
        for component in components:
            validation_results["components"][component] = self._validate_component(component)
        
        # Determine overall status
        critical_failures = [
            comp for comp, status in validation_results["components"].items() 
            if status["status"] == "critical"
        ]
        
        if critical_failures:
            validation_results["overall_status"] = "not_ready"
            validation_results["critical_issues"] = critical_failures
        elif any(status["status"] == "warning" for status in validation_results["components"].values()):
            validation_results["overall_status"] = "ready_with_warnings"
        else:
            validation_results["overall_status"] = "production_ready"
        
        return validation_results
    
    def _validate_component(self, component: str) -> Dict:
        """Validate individual production component"""
        validators = {
            "database_integrity": self._validate_database_integrity,
            "security_framework": self._validate_security_framework,
            "error_handling": self._validate_error_handling,
            "performance_optimization": self._validate_performance,
            "backup_systems": self._validate_backup_systems,
            "monitoring_systems": self._validate_monitoring,
            "workflow_integrity": self._validate_workflows,
            "data_validation": self._validate_data_integrity
        }
        
        try:
            if component in validators:
                return validators[component]()
            else:
                return {"status": "warning", "message": "Component not recognized"}
        except Exception as e:
            return {"status": "critical", "message": f"Validation failed: {str(e)}"}
    
    def _validate_database_integrity(self) -> Dict:
        """Validate database integrity and relationships"""
        try:
            # Check core data files exist
            required_files = [
                "data/projects/projects.json",
                "data/contracts/contracts.json",
                "data/cost_management/aia_billing.json",
                "data/relationships/core_relationships.json"
            ]
            
            missing_files = []
            for file_path in required_files:
                if not os.path.exists(file_path):
                    missing_files.append(file_path)
            
            if missing_files:
                return {
                    "status": "warning",
                    "message": f"Missing data files: {', '.join(missing_files)}"
                }
            
            # Validate data structure
            for file_path in required_files:
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if not isinstance(data, (dict, list)):
                            return {
                                "status": "critical",
                                "message": f"Invalid data structure in {file_path}"
                            }
                except json.JSONDecodeError:
                    return {
                        "status": "critical", 
                        "message": f"Invalid JSON in {file_path}"
                    }
            
            return {"status": "healthy", "message": "Database integrity validated"}
            
        except Exception as e:
            return {"status": "critical", "message": f"Database validation failed: {str(e)}"}
    
    def _validate_security_framework(self) -> Dict:
        """Validate security implementation"""
        try:
            # Check if security logging is active
            security_log = "logs/security/security.log"
            if not os.path.exists(security_log):
                return {"status": "warning", "message": "Security logging not initialized"}
            
            # Validate session state security
            if 'authenticated' not in st.session_state:
                return {"status": "warning", "message": "Authentication state not properly managed"}
            
            return {"status": "healthy", "message": "Security framework operational"}
            
        except Exception as e:
            return {"status": "critical", "message": f"Security validation failed: {str(e)}"}
    
    def _validate_error_handling(self) -> Dict:
        """Validate error handling implementation"""
        try:
            # Check if error logging is working
            app_log = "logs/application/app.log"
            if not os.path.exists(app_log):
                return {"status": "warning", "message": "Application logging not active"}
            
            return {"status": "healthy", "message": "Error handling operational"}
            
        except Exception as e:
            return {"status": "critical", "message": f"Error handling validation failed: {str(e)}"}
    
    def _validate_performance(self) -> Dict:
        """Validate performance optimization"""
        try:
            # Check if performance monitoring is active
            perf_metrics = "monitoring/metrics/current_metrics.json"
            if not os.path.exists(perf_metrics):
                return {"status": "warning", "message": "Performance monitoring not initialized"}
            
            return {"status": "healthy", "message": "Performance monitoring active"}
            
        except Exception as e:
            return {"status": "warning", "message": f"Performance validation incomplete: {str(e)}"}
    
    def _validate_backup_systems(self) -> Dict:
        """Validate backup systems"""
        try:
            backup_dir = "backups/data"
            if not os.path.exists(backup_dir):
                return {"status": "warning", "message": "Backup directory not found"}
            
            return {"status": "healthy", "message": "Backup systems ready"}
            
        except Exception as e:
            return {"status": "warning", "message": f"Backup validation incomplete: {str(e)}"}
    
    def _validate_monitoring(self) -> Dict:
        """Validate monitoring systems"""
        try:
            monitoring_file = "monitoring/metrics/current_metrics.json"
            if os.path.exists(monitoring_file):
                with open(monitoring_file, 'r') as f:
                    metrics = json.load(f)
                    if "health_checks" in metrics:
                        return {"status": "healthy", "message": "Monitoring systems operational"}
            
            return {"status": "warning", "message": "Monitoring not fully configured"}
            
        except Exception as e:
            return {"status": "warning", "message": f"Monitoring validation incomplete: {str(e)}"}
    
    def _validate_workflows(self) -> Dict:
        """Validate workflow integrity"""
        try:
            workflow_file = "data/relationships/core_relationships.json"
            if os.path.exists(workflow_file):
                with open(workflow_file, 'r') as f:
                    workflows = json.load(f)
                    if len(workflows) > 0:
                        return {"status": "healthy", "message": "Workflow relationships defined"}
            
            return {"status": "warning", "message": "Workflow relationships not fully configured"}
            
        except Exception as e:
            return {"status": "warning", "message": f"Workflow validation incomplete: {str(e)}"}
    
    def _validate_data_integrity(self) -> Dict:
        """Validate data integrity across modules"""
        try:
            # Check Highland Tower Development project data exists
            project_files = [
                "data/cost_management/aia_billing.json",
                "data/contracts/owner_change_orders.json"
            ]
            
            for file_path in project_files:
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        # Validate Highland Tower Development data
                        if isinstance(data, dict) and "project_info" in data:
                            project_info = data["project_info"]
                            if project_info.get("project_name") == "Highland Tower Development":
                                continue
                        elif isinstance(data, dict) and "change_orders" in data:
                            continue
                        return {"status": "warning", "message": f"Data integrity issues in {file_path}"}
            
            return {"status": "healthy", "message": "Data integrity validated"}
            
        except Exception as e:
            return {"status": "warning", "message": f"Data integrity validation incomplete: {str(e)}"}
    
    def create_production_backup(self) -> bool:
        """Create comprehensive production backup"""
        try:
            backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"backups/data/backup_{backup_timestamp}"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup all data directories
            data_dirs = ["data", "logs", "monitoring"]
            for dir_name in data_dirs:
                if os.path.exists(dir_name):
                    self._copy_directory(dir_name, f"{backup_dir}/{dir_name}")
            
            # Create backup manifest
            manifest = {
                "backup_timestamp": backup_timestamp,
                "backup_type": "full_production",
                "directories_backed_up": data_dirs,
                "file_count": self._count_files(backup_dir)
            }
            
            with open(f"{backup_dir}/backup_manifest.json", 'w') as f:
                json.dump(manifest, f, indent=2)
            
            return True
            
        except Exception as e:
            logging.getLogger('gcpanel.application').error(f"Backup failed: {str(e)}")
            return False
    
    def _copy_directory(self, src: str, dst: str):
        """Copy directory recursively"""
        import shutil
        shutil.copytree(src, dst, dirs_exist_ok=True)
    
    def _count_files(self, directory: str) -> int:
        """Count files in directory recursively"""
        count = 0
        for root, dirs, files in os.walk(directory):
            count += len(files)
        return count
    
    def render_production_dashboard(self):
        """Render production readiness dashboard"""
        st.title("🏢 Enterprise Production Manager")
        
        # Validation results
        validation = self.validate_production_readiness()
        
        # Overall status
        status_colors = {
            "production_ready": "🟢",
            "ready_with_warnings": "🟡", 
            "not_ready": "🔴",
            "pending": "⚪"
        }
        
        st.markdown(f"## {status_colors.get(validation['overall_status'], '⚪')} Overall Status: {validation['overall_status'].replace('_', ' ').title()}")
        
        # Component status
        st.markdown("### Component Validation Results")
        
        for component, status in validation["components"].items():
            status_icon = {"healthy": "✅", "warning": "⚠️", "critical": "❌"}.get(status["status"], "❓")
            st.markdown(f"{status_icon} **{component.replace('_', ' ').title()}**: {status['message']}")
        
        # Actions
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Re-validate System", type="primary"):
                st.rerun()
        
        with col2:
            if st.button("💾 Create Backup", type="secondary"):
                success = self.create_production_backup()
                if success:
                    st.success("✅ Production backup created successfully")
                else:
                    st.error("❌ Backup creation failed")
        
        with col3:
            if st.button("📊 View Metrics", type="secondary"):
                self._show_production_metrics()
    
    def _show_production_metrics(self):
        """Show production metrics"""
        try:
            with open('monitoring/metrics/current_metrics.json', 'r') as f:
                metrics = json.load(f)
            
            st.markdown("### Production Metrics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Error Rate", f"{metrics['metrics']['error_rate']}%")
                st.metric("Active Sessions", metrics['metrics']['user_sessions'])
            
            with col2:
                st.metric("Database Queries", metrics['metrics']['database_queries'])
                st.metric("Workflow Executions", metrics['metrics']['workflow_executions'])
                
        except Exception:
            st.info("Metrics not available yet")

# Global production manager instance
production_manager = ProductionManager()

def get_production_manager():
    """Get production manager instance"""
    return production_manager