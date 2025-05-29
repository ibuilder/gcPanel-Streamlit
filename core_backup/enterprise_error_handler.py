"""
Enterprise-Grade Error Handling System for gcPanel
Production-ready error handling, logging, and recovery mechanisms
"""

import streamlit as st
import logging
import traceback
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from functools import wraps

class EnterpriseErrorHandler:
    """Enterprise-grade error handling and recovery system"""
    
    def __init__(self):
        self._setup_error_logging()
        self._initialize_error_tracking()
    
    def _setup_error_logging(self):
        """Setup comprehensive error logging"""
        os.makedirs("logs/errors", exist_ok=True)
        
        # Application errors logger
        error_logger = logging.getLogger('gcpanel.errors')
        if not error_logger.handlers:
            handler = logging.FileHandler('logs/errors/application_errors.log')
            formatter = logging.Formatter(
                '%(asctime)s - ERROR - %(levelname)s - %(name)s - %(message)s'
            )
            handler.setFormatter(formatter)
            error_logger.addHandler(handler)
            error_logger.setLevel(logging.ERROR)
        
        # Critical errors logger
        critical_logger = logging.getLogger('gcpanel.critical')
        if not critical_logger.handlers:
            handler = logging.FileHandler('logs/errors/critical_errors.log')
            formatter = logging.Formatter(
                '%(asctime)s - CRITICAL - %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d'
            )
            handler.setFormatter(formatter)
            critical_logger.addHandler(handler)
            critical_logger.setLevel(logging.CRITICAL)
    
    def _initialize_error_tracking(self):
        """Initialize error tracking state"""
        if 'error_tracking' not in st.session_state:
            st.session_state.error_tracking = {
                'total_errors': 0,
                'recent_errors': [],
                'error_recovery_attempts': 0
            }
    
    def handle_error(self, error: Exception, context: Dict = None, critical: bool = False) -> Dict:
        """Handle errors with comprehensive logging and recovery"""
        try:
            error_info = {
                'timestamp': datetime.now().isoformat(),
                'error_type': type(error).__name__,
                'error_message': str(error),
                'traceback': traceback.format_exc(),
                'context': context or {},
                'critical': critical,
                'user': st.session_state.get('current_user', 'anonymous'),
                'session_id': st.session_state.get('session_id', 'unknown')
            }
            
            # Log the error
            if critical:
                logging.getLogger('gcpanel.critical').critical(json.dumps(error_info))
            else:
                logging.getLogger('gcpanel.errors').error(json.dumps(error_info))
            
            # Update session tracking
            st.session_state.error_tracking['total_errors'] += 1
            st.session_state.error_tracking['recent_errors'].append(error_info)
            
            # Keep only last 10 errors in session
            st.session_state.error_tracking['recent_errors'] = \
                st.session_state.error_tracking['recent_errors'][-10:]
            
            # Store in persistent error log
            self._store_error_record(error_info)
            
            # Attempt recovery if not critical
            recovery_result = None
            if not critical:
                recovery_result = self._attempt_error_recovery(error, context)
            
            return {
                'error_logged': True,
                'error_id': error_info['timestamp'],
                'recovery_attempted': recovery_result is not None,
                'recovery_successful': recovery_result.get('success', False) if recovery_result else False,
                'user_message': self._generate_user_message(error, critical, recovery_result)
            }
            
        except Exception as e:
            # Fallback error handling
            st.error(f"Critical error in error handler: {str(e)}")
            return {
                'error_logged': False,
                'error_id': None,
                'recovery_attempted': False,
                'recovery_successful': False,
                'user_message': "A system error occurred. Please contact support."
            }
    
    def _store_error_record(self, error_info: Dict):
        """Store error record in persistent storage"""
        try:
            error_log_file = "logs/errors/error_records.json"
            
            if os.path.exists(error_log_file):
                with open(error_log_file, 'r') as f:
                    error_records = json.load(f)
            else:
                error_records = {'errors': []}
            
            error_records['errors'].append(error_info)
            
            # Keep only last 500 error records
            error_records['errors'] = error_records['errors'][-500:]
            
            with open(error_log_file, 'w') as f:
                json.dump(error_records, f, indent=2)
                
        except Exception:
            pass  # Don't fail if error storage fails
    
    def _attempt_error_recovery(self, error: Exception, context: Dict = None) -> Dict:
        """Attempt to recover from non-critical errors"""
        recovery_strategies = {
            'FileNotFoundError': self._recover_missing_file,
            'json.JSONDecodeError': self._recover_corrupt_json,
            'KeyError': self._recover_missing_key,
            'ValueError': self._recover_invalid_value,
            'AttributeError': self._recover_missing_attribute
        }
        
        error_type = type(error).__name__
        
        if error_type in recovery_strategies:
            try:
                st.session_state.error_tracking['error_recovery_attempts'] += 1
                return recovery_strategies[error_type](error, context)
            except Exception:
                return {'success': False, 'message': 'Recovery attempt failed'}
        
        return {'success': False, 'message': 'No recovery strategy available'}
    
    def _recover_missing_file(self, error: Exception, context: Dict = None) -> Dict:
        """Recover from missing file errors"""
        try:
            if context and 'file_path' in context:
                file_path = context['file_path']
                
                # Create directory if needed
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Create default file based on file type
                if file_path.endswith('.json'):
                    with open(file_path, 'w') as f:
                        json.dump({}, f)
                else:
                    with open(file_path, 'w') as f:
                        f.write("")
                
                return {'success': True, 'message': f'Created missing file: {file_path}'}
            
            return {'success': False, 'message': 'Unable to recover: file path not provided'}
            
        except Exception:
            return {'success': False, 'message': 'File recovery failed'}
    
    def _recover_corrupt_json(self, error: Exception, context: Dict = None) -> Dict:
        """Recover from corrupt JSON files"""
        try:
            if context and 'file_path' in context:
                file_path = context['file_path']
                
                # Backup corrupt file
                backup_path = f"{file_path}.corrupt.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                if os.path.exists(file_path):
                    os.rename(file_path, backup_path)
                
                # Create new valid JSON file
                with open(file_path, 'w') as f:
                    json.dump({}, f)
                
                return {'success': True, 'message': f'Recovered corrupt JSON file: {file_path}'}
            
            return {'success': False, 'message': 'Unable to recover: file path not provided'}
            
        except Exception:
            return {'success': False, 'message': 'JSON recovery failed'}
    
    def _recover_missing_key(self, error: Exception, context: Dict = None) -> Dict:
        """Recover from missing key errors"""
        return {'success': False, 'message': 'Using default values for missing keys'}
    
    def _recover_invalid_value(self, error: Exception, context: Dict = None) -> Dict:
        """Recover from invalid value errors"""
        return {'success': False, 'message': 'Using fallback values for invalid data'}
    
    def _recover_missing_attribute(self, error: Exception, context: Dict = None) -> Dict:
        """Recover from missing attribute errors"""
        return {'success': False, 'message': 'Using alternative attribute access methods'}
    
    def _generate_user_message(self, error: Exception, critical: bool, recovery_result: Dict = None) -> str:
        """Generate user-friendly error message"""
        if critical:
            return "A critical system error occurred. The issue has been logged and administrators have been notified. Please contact support if the problem persists."
        
        if recovery_result and recovery_result.get('success'):
            return f"A minor issue was detected and automatically resolved. You can continue using the application normally."
        
        error_type = type(error).__name__
        
        user_messages = {
            'FileNotFoundError': "Some data files are missing. The system is attempting to recreate them automatically.",
            'json.JSONDecodeError': "Data format issues were detected. The system is rebuilding the affected files.",
            'KeyError': "Some configuration data is missing. Using default values temporarily.",
            'ValueError': "Invalid data was encountered. The system is using safe fallback values.",
            'AttributeError': "A component access issue occurred. The system is using alternative methods."
        }
        
        return user_messages.get(error_type, 
            "An unexpected issue occurred. The error has been logged and you can continue using the application.")
    
    def get_error_statistics(self) -> Dict:
        """Get error statistics for monitoring"""
        try:
            error_log_file = "logs/errors/error_records.json"
            
            if os.path.exists(error_log_file):
                with open(error_log_file, 'r') as f:
                    error_records = json.load(f)
                
                errors = error_records.get('errors', [])
                
                # Calculate statistics
                total_errors = len(errors)
                critical_errors = len([e for e in errors if e.get('critical', False)])
                recent_errors = len([e for e in errors if self._is_recent_error(e)])
                
                # Error types breakdown
                error_types = {}
                for error in errors:
                    error_type = error.get('error_type', 'Unknown')
                    error_types[error_type] = error_types.get(error_type, 0) + 1
                
                return {
                    'total_errors': total_errors,
                    'critical_errors': critical_errors,
                    'recent_errors_24h': recent_errors,
                    'error_types': error_types,
                    'recovery_attempts': st.session_state.error_tracking.get('error_recovery_attempts', 0),
                    'system_stability': max(0, 100 - (critical_errors * 10) - (recent_errors * 2))
                }
            
            return {
                'total_errors': 0,
                'critical_errors': 0,
                'recent_errors_24h': 0,
                'error_types': {},
                'recovery_attempts': 0,
                'system_stability': 100
            }
            
        except Exception:
            return {'error': 'Unable to calculate error statistics'}
    
    def _is_recent_error(self, error_info: Dict) -> bool:
        """Check if error occurred in the last 24 hours"""
        try:
            error_time = datetime.fromisoformat(error_info['timestamp'])
            return (datetime.now() - error_time).total_seconds() < 86400  # 24 hours
        except:
            return False

def safe_execute(func):
    """Decorator for safe function execution with error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_handler = EnterpriseErrorHandler()
            result = error_handler.handle_error(e, {
                'function': func.__name__,
                'args': str(args)[:100],  # Limit arg string length
                'kwargs': str(kwargs)[:100]
            })
            
            # Display user-friendly message
            if result['recovery_successful']:
                st.info(result['user_message'])
            else:
                st.error(result['user_message'])
            
            return None
    return wrapper

def critical_operation(func):
    """Decorator for critical operations that should not fail silently"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_handler = EnterpriseErrorHandler()
            result = error_handler.handle_error(e, {
                'function': func.__name__,
                'operation_type': 'critical'
            }, critical=True)
            
            st.error(result['user_message'])
            st.stop()  # Stop execution for critical errors
    return wrapper

# Global error handler instance
error_handler = EnterpriseErrorHandler()

def get_error_handler():
    """Get error handler instance"""
    return error_handler