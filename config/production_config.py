"""
Highland Tower Development - Production Configuration
Environment-specific settings, security hardening, and monitoring
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any
import secrets

class ProductionConfig:
    """Production environment configuration"""
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DATABASE_POOL_SIZE = int(os.environ.get('DATABASE_POOL_SIZE', '20'))
    DATABASE_MAX_OVERFLOW = int(os.environ.get('DATABASE_MAX_OVERFLOW', '30'))
    
    # Redis Configuration
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_CACHE_DEFAULT_TIMEOUT = int(os.environ.get('REDIS_CACHE_TIMEOUT', '3600'))
    
    # Celery Configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/1')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')
    
    # Security Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(32)
    SESSION_TIMEOUT = int(os.environ.get('SESSION_TIMEOUT', '3600'))  # 1 hour
    PASSWORD_MIN_LENGTH = int(os.environ.get('PASSWORD_MIN_LENGTH', '8'))
    MAX_LOGIN_ATTEMPTS = int(os.environ.get('MAX_LOGIN_ATTEMPTS', '5'))
    
    # Email Configuration
    SMTP_HOST = os.environ.get('SMTP_HOST')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
    SMTP_USER = os.environ.get('SMTP_USER')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    SMTP_USE_TLS = os.environ.get('SMTP_USE_TLS', 'true').lower() == 'true'
    
    # File Upload Configuration
    MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', '50')) * 1024 * 1024  # 50MB
    ALLOWED_FILE_EXTENSIONS = ['pdf', 'docx', 'xlsx', 'jpg', 'jpeg', 'png', 'dwg', 'ifc']
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/app/uploads')
    
    # API Rate Limiting
    API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT', '100/hour')
    API_BURST_LIMIT = int(os.environ.get('API_BURST_LIMIT', '10'))
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.environ.get('LOG_FILE', '/app/logs/highland_tower.log')
    
    # Monitoring Configuration
    HEALTH_CHECK_ENABLED = os.environ.get('HEALTH_CHECK_ENABLED', 'true').lower() == 'true'
    METRICS_ENABLED = os.environ.get('METRICS_ENABLED', 'true').lower() == 'true'
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    
    # Backup Configuration
    BACKUP_ENABLED = os.environ.get('BACKUP_ENABLED', 'true').lower() == 'true'
    BACKUP_SCHEDULE = os.environ.get('BACKUP_SCHEDULE', '0 2 * * *')  # Daily at 2 AM
    BACKUP_RETENTION_DAYS = int(os.environ.get('BACKUP_RETENTION_DAYS', '30'))

class DevelopmentConfig:
    """Development environment configuration"""
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost/highland_tower_dev')
    DATABASE_POOL_SIZE = 5
    DATABASE_MAX_OVERFLOW = 10
    
    # Redis Configuration
    REDIS_URL = 'redis://localhost:6379/0'
    REDIS_CACHE_DEFAULT_TIMEOUT = 300
    
    # Security Configuration (Less strict for development)
    SECRET_KEY = 'development-key-not-for-production'
    SESSION_TIMEOUT = 86400  # 24 hours
    PASSWORD_MIN_LENGTH = 6
    MAX_LOGIN_ATTEMPTS = 10
    
    # Logging Configuration
    LOG_LEVEL = 'DEBUG'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Development flags
    DEBUG = True
    TESTING = False

class SecurityManager:
    """Security hardening and monitoring"""
    
    def __init__(self, config):
        self.config = config
        self.failed_attempts = {}
        
    def setup_security_headers(self):
        """Configure security headers for web application"""
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self'; "
                "connect-src 'self';"
            )
        }
    
    def validate_file_upload(self, filename: str, file_size: int) -> tuple[bool, str]:
        """Validate file uploads for security"""
        # Check file size
        if file_size > self.config.MAX_FILE_SIZE:
            return False, f"File size exceeds maximum allowed size of {self.config.MAX_FILE_SIZE // (1024*1024)}MB"
        
        # Check file extension
        if '.' not in filename:
            return False, "File must have an extension"
        
        extension = filename.rsplit('.', 1)[1].lower()
        if extension not in self.config.ALLOWED_FILE_EXTENSIONS:
            return False, f"File type '{extension}' not allowed"
        
        # Check for malicious patterns
        dangerous_patterns = ['../', '.\\', '<script', 'javascript:', 'vbscript:']
        for pattern in dangerous_patterns:
            if pattern in filename.lower():
                return False, "Filename contains unsafe characters"
        
        return True, "File is valid"
    
    def check_rate_limit(self, user_id: str, action: str) -> bool:
        """Check if user has exceeded rate limits"""
        # Implement rate limiting logic
        key = f"{user_id}:{action}"
        # This would integrate with Redis in production
        return True
    
    def log_security_event(self, event_type: str, user_id: str = None, details: Dict = None):
        """Log security-related events"""
        security_log = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'details': details or {},
            'ip_address': self.get_client_ip()
        }
        
        # Log to security log file
        logging.getLogger('security').warning(f"Security Event: {security_log}")
    
    def get_client_ip(self) -> str:
        """Get client IP address for logging"""
        # This would be implemented based on your deployment setup
        return "unknown"

class MonitoringManager:
    """Application monitoring and health checks"""
    
    def __init__(self, config):
        self.config = config
        
    def setup_logging(self):
        """Configure production logging"""
        logging.basicConfig(
            level=getattr(logging, self.config.LOG_LEVEL),
            format=self.config.LOG_FORMAT,
            handlers=[
                logging.FileHandler(self.config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        
        # Security logger
        security_logger = logging.getLogger('security')
        security_handler = logging.FileHandler('/app/logs/security.log')
        security_handler.setFormatter(logging.Formatter(self.config.LOG_FORMAT))
        security_logger.addHandler(security_handler)
        
    def health_check(self) -> Dict[str, Any]:
        """Perform application health check"""
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy',
            'checks': {}
        }
        
        # Database check
        try:
            from database.models import db_manager
            session = db_manager.get_session()
            session.execute("SELECT 1")
            db_manager.close_session(session)
            health_status['checks']['database'] = 'healthy'
        except Exception as e:
            health_status['checks']['database'] = f'unhealthy: {str(e)}'
            health_status['status'] = 'unhealthy'
        
        # Redis check
        try:
            from modules.performance_optimization import cache
            if cache.available:
                health_status['checks']['redis'] = 'healthy'
            else:
                health_status['checks']['redis'] = 'unavailable'
        except Exception as e:
            health_status['checks']['redis'] = f'unhealthy: {str(e)}'
        
        # Disk space check
        try:
            import shutil
            total, used, free = shutil.disk_usage('/')
            free_percent = (free / total) * 100
            if free_percent > 10:
                health_status['checks']['disk_space'] = f'healthy ({free_percent:.1f}% free)'
            else:
                health_status['checks']['disk_space'] = f'warning ({free_percent:.1f}% free)'
                health_status['status'] = 'degraded'
        except Exception as e:
            health_status['checks']['disk_space'] = f'unhealthy: {str(e)}'
        
        return health_status
    
    def get_application_metrics(self) -> Dict[str, Any]:
        """Get application performance metrics"""
        from modules.performance_optimization import perf_monitor
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'performance': perf_monitor.get_performance_stats(),
            'system': self.get_system_metrics()
        }
        
        return metrics
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system-level metrics"""
        import psutil
        
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'network_io': psutil.net_io_counters()._asdict()
        }

class BackupManager:
    """Database backup and recovery"""
    
    def __init__(self, config):
        self.config = config
        
    def create_backup(self) -> Dict[str, Any]:
        """Create database backup"""
        if not self.config.BACKUP_ENABLED:
            return {'status': 'disabled', 'message': 'Backups are disabled'}
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"highland_tower_backup_{timestamp}.sql"
        backup_path = f"/app/backups/{backup_filename}"
        
        try:
            # PostgreSQL backup command
            import subprocess
            cmd = [
                'pg_dump',
                self.config.DATABASE_URL,
                '-f', backup_path,
                '--no-owner',
                '--no-privileges'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    'status': 'success',
                    'backup_file': backup_filename,
                    'backup_path': backup_path,
                    'timestamp': timestamp
                }
            else:
                return {
                    'status': 'error',
                    'message': result.stderr
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def cleanup_old_backups(self):
        """Remove old backup files"""
        import os
        import glob
        from datetime import timedelta
        
        backup_dir = "/app/backups"
        cutoff_date = datetime.now() - timedelta(days=self.config.BACKUP_RETENTION_DAYS)
        
        for backup_file in glob.glob(f"{backup_dir}/highland_tower_backup_*.sql"):
            file_stat = os.stat(backup_file)
            file_date = datetime.fromtimestamp(file_stat.st_mtime)
            
            if file_date < cutoff_date:
                os.remove(backup_file)
                logging.info(f"Removed old backup: {backup_file}")

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('HIGHLAND_ENV', 'development')
    
    if env == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig()

def setup_production_environment():
    """Initialize production environment"""
    config = get_config()
    
    # Setup security
    security_manager = SecurityManager(config)
    
    # Setup monitoring
    monitoring_manager = MonitoringManager(config)
    monitoring_manager.setup_logging()
    
    # Setup backup manager
    backup_manager = BackupManager(config)
    
    # Create necessary directories
    os.makedirs('/app/logs', exist_ok=True)
    os.makedirs('/app/backups', exist_ok=True)
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    
    return {
        'config': config,
        'security': security_manager,
        'monitoring': monitoring_manager,
        'backup': backup_manager
    }

def render_system_status():
    """Render system status dashboard"""
    import streamlit as st
    
    st.subheader("🏗️ Highland Tower System Status")
    
    # Get system components
    components = setup_production_environment()
    monitoring = components['monitoring']
    
    # Health check
    health = monitoring.health_check()
    
    # Status overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_color = "🟢" if health['status'] == 'healthy' else "🔴"
        st.metric("System Status", f"{status_color} {health['status'].title()}")
    
    with col2:
        check_count = len([c for c in health['checks'].values() if 'healthy' in c])
        total_checks = len(health['checks'])
        st.metric("Health Checks", f"{check_count}/{total_checks}")
    
    with col3:
        st.metric("Last Check", health['timestamp'].split('T')[1][:8])
    
    # Detailed health checks
    st.markdown("#### Component Health")
    for component, status in health['checks'].items():
        status_icon = "🟢" if 'healthy' in status else "🔴" if 'unhealthy' in status else "🟡"
        st.write(f"{status_icon} **{component.title()}**: {status}")
    
    # System metrics
    try:
        metrics = monitoring.get_application_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("CPU Usage", f"{metrics['system']['cpu_percent']:.1f}%")
        
        with col2:
            st.metric("Memory Usage", f"{metrics['system']['memory_percent']:.1f}%")
        
        with col3:
            st.metric("Disk Usage", f"{metrics['system']['disk_percent']:.1f}%")
        
        with col4:
            network_sent = metrics['system']['network_io']['bytes_sent'] / (1024*1024)
            st.metric("Network Sent", f"{network_sent:.1f} MB")
    
    except Exception as e:
        st.warning(f"Could not load system metrics: {e}")
    
    # Backup status
    if st.button("🗂️ Create Database Backup"):
        backup_manager = components['backup']
        result = backup_manager.create_backup()
        
        if result['status'] == 'success':
            st.success(f"Backup created: {result['backup_file']}")
        else:
            st.error(f"Backup failed: {result['message']}")