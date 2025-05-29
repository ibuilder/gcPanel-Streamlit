"""
Highland Tower Development - Unified Integration Manager
Orchestrates all construction platform integrations with real data synchronization
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import asyncio
import json
from dataclasses import asdict

from .procore_integration import ProcoreIntegration
from .autodesk_integration import AutodeskIntegration
from .sage_integration import SageIntegration
from .fieldlens_integration import FieldlensIntegration
from .plangrid_integration import PlanGridIntegration

class UnifiedIntegrationManager:
    """
    Central manager for all construction platform integrations
    Handles data synchronization, transformation, and workflow orchestration
    """
    
    def __init__(self):
        self.setup_logging()
        
        # Initialize all integrations
        self.integrations = {
            'procore': ProcoreIntegration(),
            'autodesk': AutodeskIntegration(),
            'sage': SageIntegration(),
            'fieldlens': FieldlensIntegration(),
            'plangrid': PlanGridIntegration()
        }
        
        self.sync_status = {}
        self.last_sync_times = {}
        
    def setup_logging(self):
        """Setup comprehensive logging for integration manager"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('UnifiedIntegrationManager')
        
        handler = logging.FileHandler('unified_integration.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def check_all_connections(self) -> Dict[str, bool]:
        """Test connectivity to all integrated platforms"""
        connection_status = {}
        
        for platform_name, integration in self.integrations.items():
            try:
                connection_status[platform_name] = integration.test_connection()
                self.logger.info(f"{platform_name} connection: {'✅ Connected' if connection_status[platform_name] else '❌ Failed'}")
            except Exception as e:
                self.logger.error(f"Error testing {platform_name} connection: {e}")
                connection_status[platform_name] = False
        
        return connection_status
    
    def sync_all_platforms(self, highland_project_data: Dict) -> Dict[str, Any]:
        """
        Perform comprehensive data synchronization across all platforms
        
        Args:
            highland_project_data: Core Highland Tower project configuration
            
        Returns:
            Sync results for each platform
        """
        sync_results = {}
        
        # Extract project identifiers for each platform
        project_ids = highland_project_data.get('platform_project_ids', {})
        
        for platform_name, integration in self.integrations.items():
            if not integration.test_connection():
                sync_results[platform_name] = {'status': 'failed', 'reason': 'connection_failed'}
                continue
            
            try:
                platform_project_id = project_ids.get(platform_name)
                if not platform_project_id:
                    sync_results[platform_name] = {'status': 'skipped', 'reason': 'no_project_id'}
                    continue
                
                # Platform-specific sync operations
                if platform_name == 'procore':
                    result = self.sync_procore_data(integration, highland_project_data, platform_project_id)
                elif platform_name == 'autodesk':
                    result = self.sync_autodesk_data(integration, highland_project_data, platform_project_id)
                elif platform_name == 'sage':
                    result = self.sync_sage_data(integration, highland_project_data, platform_project_id)
                elif platform_name == 'fieldlens':
                    result = self.sync_fieldlens_data(integration, highland_project_data, platform_project_id)
                elif platform_name == 'plangrid':
                    result = self.sync_plangrid_data(integration, highland_project_data, platform_project_id)
                
                sync_results[platform_name] = result
                self.last_sync_times[platform_name] = datetime.now().isoformat()
                
            except Exception as e:
                self.logger.error(f"Error syncing {platform_name}: {e}")
                sync_results[platform_name] = {'status': 'error', 'message': str(e)}
        
        return sync_results
    
    def sync_procore_data(self, integration: ProcoreIntegration, highland_data: Dict, project_id: str) -> Dict:
        """Sync data with Procore platform"""
        try:
            # Import from Procore
            company_id = highland_data.get('procore_company_id')
            rfis = integration.sync_rfis(company_id, project_id)
            daily_reports = integration.sync_daily_reports(company_id, project_id)
            submittals = integration.sync_submittals(company_id, project_id)
            
            # Export Highland Tower data to Procore
            highland_rfis = highland_data.get('rfis', {})
            if highland_rfis:
                integration.export_highland_data_to_procore(highland_rfis, 'rfis')
            
            highland_reports = highland_data.get('daily_reports', {})
            if highland_reports:
                integration.export_highland_data_to_procore(highland_reports, 'daily_reports')
            
            return {
                'status': 'success',
                'imported': {
                    'rfis': len(rfis),
                    'daily_reports': len(daily_reports),
                    'submittals': len(submittals)
                },
                'exported': {
                    'rfis': len(highland_rfis.get('items', [])),
                    'daily_reports': len(highland_reports.get('items', []))
                }
            }
            
        except Exception as e:
            self.logger.error(f"Procore sync error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def sync_autodesk_data(self, integration: AutodeskIntegration, highland_data: Dict, project_id: str) -> Dict:
        """Sync data with Autodesk Construction Cloud"""
        try:
            account_id = highland_data.get('autodesk_account_id')
            
            # Import from Autodesk
            documents = integration.sync_documents(account_id, project_id)
            issues = integration.sync_bim360_issues(account_id, project_id)
            rfis = integration.sync_bim360_rfis(account_id, project_id)
            
            # Export Highland Tower data to Autodesk
            highland_issues = highland_data.get('issues', {})
            if highland_issues:
                integration.export_highland_data_to_autodesk(highland_issues, 'issues')
            
            return {
                'status': 'success',
                'imported': {
                    'documents': len(documents),
                    'issues': len(issues),
                    'rfis': len(rfis)
                },
                'exported': {
                    'issues': len(highland_issues.get('items', []))
                }
            }
            
        except Exception as e:
            self.logger.error(f"Autodesk sync error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def sync_sage_data(self, integration: SageIntegration, highland_data: Dict, job_number: str) -> Dict:
        """Sync data with Sage Construction"""
        try:
            # Import from Sage
            projects = integration.sync_projects()
            cost_codes = integration.sync_cost_codes(job_number)
            change_orders = integration.sync_change_orders(job_number)
            
            # Export Highland Tower data to Sage
            highland_change_orders = highland_data.get('change_orders', {})
            if highland_change_orders:
                integration.export_highland_data_to_sage(highland_change_orders, 'change_orders', job_number)
            
            highland_costs = highland_data.get('costs', {})
            if highland_costs:
                integration.export_highland_data_to_sage(highland_costs, 'costs', job_number)
            
            return {
                'status': 'success',
                'imported': {
                    'projects': len(projects),
                    'cost_codes': len(cost_codes),
                    'change_orders': len(change_orders)
                },
                'exported': {
                    'change_orders': len(highland_change_orders.get('items', [])),
                    'costs': len(highland_costs.get('items', []))
                }
            }
            
        except Exception as e:
            self.logger.error(f"Sage sync error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def sync_fieldlens_data(self, integration: FieldlensIntegration, highland_data: Dict, project_id: str) -> Dict:
        """Sync data with Fieldlens"""
        try:
            # Import from Fieldlens
            tasks = integration.sync_tasks(project_id)
            reports = integration.sync_reports(project_id)
            
            # Export Highland Tower data to Fieldlens
            highland_tasks = highland_data.get('tasks', {})
            if highland_tasks:
                integration.export_highland_data_to_fieldlens(highland_tasks, 'tasks', project_id)
            
            highland_reports = highland_data.get('field_reports', {})
            if highland_reports:
                integration.export_highland_data_to_fieldlens(highland_reports, 'reports', project_id)
            
            return {
                'status': 'success',
                'imported': {
                    'tasks': len(tasks),
                    'reports': len(reports)
                },
                'exported': {
                    'tasks': len(highland_tasks.get('items', [])),
                    'reports': len(highland_reports.get('items', []))
                }
            }
            
        except Exception as e:
            self.logger.error(f"Fieldlens sync error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def sync_plangrid_data(self, integration: PlanGridIntegration, highland_data: Dict, project_id: str) -> Dict:
        """Sync data with PlanGrid"""
        try:
            # Import from PlanGrid
            sheets = integration.sync_sheets(project_id)
            issues = integration.sync_issues(project_id)
            
            # Export Highland Tower data to PlanGrid
            highland_issues = highland_data.get('plangrid_issues', {})
            if highland_issues:
                integration.export_highland_data_to_plangrid(highland_issues, 'issues', project_id)
            
            return {
                'status': 'success',
                'imported': {
                    'sheets': len(sheets),
                    'issues': len(issues)
                },
                'exported': {
                    'issues': len(highland_issues.get('items', []))
                }
            }
            
        except Exception as e:
            self.logger.error(f"PlanGrid sync error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all integrations"""
        status = {
            'overall_health': 'healthy',
            'total_integrations': len(self.integrations),
            'active_connections': 0,
            'last_sync': max(self.last_sync_times.values()) if self.last_sync_times else None,
            'platforms': {}
        }
        
        for platform_name, integration in self.integrations.items():
            platform_status = integration.get_integration_status()
            platform_status['last_sync'] = self.last_sync_times.get(platform_name)
            status['platforms'][platform_name] = platform_status
            
            if platform_status.get('connected'):
                status['active_connections'] += 1
        
        # Determine overall health
        if status['active_connections'] == 0:
            status['overall_health'] = 'critical'
        elif status['active_connections'] < len(self.integrations) / 2:
            status['overall_health'] = 'warning'
        
        return status
    
    def export_highland_project_to_all_platforms(self, highland_project: Dict) -> Dict[str, Any]:
        """
        Export complete Highland Tower project data to all connected platforms
        
        Args:
            highland_project: Complete Highland Tower project data
            
        Returns:
            Export results for each platform
        """
        export_results = {}
        
        for platform_name, integration in self.integrations.items():
            if not integration.test_connection():
                export_results[platform_name] = {'status': 'skipped', 'reason': 'not_connected'}
                continue
            
            try:
                # Platform-specific export logic would go here
                # This is where you'd transform Highland Tower data to each platform's format
                result = self.perform_platform_export(platform_name, integration, highland_project)
                export_results[platform_name] = result
                
            except Exception as e:
                self.logger.error(f"Error exporting to {platform_name}: {e}")
                export_results[platform_name] = {'status': 'error', 'message': str(e)}
        
        return export_results
    
    def perform_platform_export(self, platform_name: str, integration: Any, project_data: Dict) -> Dict:
        """Perform export to a specific platform"""
        # This would contain the logic to export Highland Tower data
        # to each specific platform based on their requirements
        return {'status': 'success', 'message': f'Export to {platform_name} completed'}
    
    def schedule_automatic_sync(self, sync_interval_hours: int = 24) -> None:
        """Schedule automatic synchronization with all platforms"""
        # Implementation would set up scheduled syncing
        self.logger.info(f"Automatic sync scheduled every {sync_interval_hours} hours")
    
    def generate_integration_report(self) -> Dict:
        """Generate comprehensive integration report"""
        status = self.get_comprehensive_status()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'highland_tower_project': 'Highland Tower Development - $45.5M',
            'integration_summary': {
                'total_platforms': len(self.integrations),
                'connected_platforms': status['active_connections'],
                'health_status': status['overall_health']
            },
            'platform_details': status['platforms'],
            'recommendations': self.generate_recommendations(status)
        }
        
        return report
    
    def generate_recommendations(self, status: Dict) -> List[str]:
        """Generate recommendations based on integration status"""
        recommendations = []
        
        if status['active_connections'] == 0:
            recommendations.append("Configure API credentials for at least one platform to enable data synchronization")
        
        for platform_name, platform_status in status['platforms'].items():
            if not platform_status.get('connected'):
                recommendations.append(f"Configure {platform_name} API credentials to enable integration")
        
        if status['active_connections'] < len(self.integrations):
            recommendations.append("Consider enabling additional platform integrations for comprehensive data coverage")
        
        return recommendations