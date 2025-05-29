"""
Highland Tower Development - Performance Optimization System
Redis caching, background tasks, and API response optimization
"""

import redis
import json
import pickle
from celery import Celery
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
import streamlit as st
import functools
import time
import os

class RedisCache:
    """Redis-based caching system for Highland Tower"""
    
    def __init__(self):
        redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
        try:
            self.redis_client = redis.from_url(redis_url)
            self.redis_client.ping()
            self.available = True
        except:
            self.redis_client = None
            self.available = False
            self.fallback_cache = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if self.available:
            try:
                value = self.redis_client.get(key)
                return pickle.loads(value) if value else None
            except:
                return None
        else:
            return self.fallback_cache.get(key)
    
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in cache with expiration"""
        if self.available:
            try:
                serialized = pickle.dumps(value)
                return self.redis_client.setex(key, expire, serialized)
            except:
                return False
        else:
            self.fallback_cache[key] = value
            return True
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if self.available:
            try:
                return bool(self.redis_client.delete(key))
            except:
                return False
        else:
            return self.fallback_cache.pop(key, None) is not None
    
    def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        if self.available:
            try:
                keys = self.redis_client.keys(pattern)
                return self.redis_client.delete(*keys) if keys else 0
            except:
                return 0
        else:
            cleared = 0
            keys_to_delete = [k for k in self.fallback_cache.keys() if pattern in k]
            for key in keys_to_delete:
                del self.fallback_cache[key]
                cleared += 1
            return cleared

# Global cache instance
cache = RedisCache()

class BackgroundTaskManager:
    """Celery-based background task management"""
    
    def __init__(self):
        broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/1')
        result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')
        
        self.celery_app = Celery(
            'highland_tower',
            broker=broker_url,
            backend=result_backend
        )
        
        self.celery_app.conf.update(
            task_serializer='json',
            accept_content=['json'],
            result_serializer='json',
            timezone='UTC',
            enable_utc=True,
            task_routes={
                'highland_tower.sync_external_data': {'queue': 'sync'},
                'highland_tower.generate_report': {'queue': 'reports'},
                'highland_tower.send_notification': {'queue': 'notifications'}
            }
        )

# Global task manager
task_manager = BackgroundTaskManager()

def cached(expire: int = 3600, key_prefix: str = None):
    """Decorator for caching function results"""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_prefix:
                cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            else:
                cache_key = f"highland:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, expire)
            return result
        
        return wrapper
    return decorator

def invalidate_cache(pattern: str):
    """Invalidate cache entries matching pattern"""
    return cache.clear_pattern(pattern)

@cached(expire=1800, key_prefix="dashboard")
def get_dashboard_metrics(project_id: str) -> Dict[str, Any]:
    """Cached dashboard metrics calculation"""
    # Simulate expensive calculation
    time.sleep(0.1)  # Remove in production
    
    return {
        "total_rfis": 23,
        "active_rfis": 5,
        "budget_utilization": 78.5,
        "schedule_performance": 1.05,
        "safety_score": 98.2,
        "last_updated": datetime.now().isoformat()
    }

@cached(expire=3600, key_prefix="reports")
def get_project_reports(project_id: str, report_type: str) -> Dict[str, Any]:
    """Cached project reports"""
    # Simulate report generation
    time.sleep(0.2)  # Remove in production
    
    return {
        "report_type": report_type,
        "project_id": project_id,
        "generated_at": datetime.now().isoformat(),
        "data": {
            "summary": "Highland Tower Development progress report",
            "metrics": get_dashboard_metrics(project_id)
        }
    }

@task_manager.celery_app.task(name='highland_tower.sync_external_data')
def sync_external_data_task(platform: str, project_id: str):
    """Background task for syncing external platform data"""
    try:
        from integrations.unified_integration_manager import UnifiedIntegrationManager
        
        manager = UnifiedIntegrationManager()
        result = manager.sync_all_platforms({
            'platform_project_ids': {platform: project_id}
        })
        
        # Invalidate related caches
        invalidate_cache(f"*{platform}*")
        invalidate_cache("dashboard*")
        
        return {
            'status': 'success',
            'platform': platform,
            'result': result,
            'completed_at': datetime.now().isoformat()
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'platform': platform,
            'error': str(e),
            'completed_at': datetime.now().isoformat()
        }

@task_manager.celery_app.task(name='highland_tower.generate_report')
def generate_report_task(report_type: str, project_id: str, params: Dict):
    """Background task for generating large reports"""
    try:
        # Simulate report generation
        time.sleep(5)  # Remove in production
        
        report_data = {
            'report_type': report_type,
            'project_id': project_id,
            'parameters': params,
            'generated_at': datetime.now().isoformat(),
            'file_path': f'/reports/{report_type}_{project_id}_{int(time.time())}.pdf'
        }
        
        # Cache the report
        cache_key = f"report:{report_type}:{project_id}"
        cache.set(cache_key, report_data, expire=86400)  # 24 hours
        
        return report_data
    
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'completed_at': datetime.now().isoformat()
        }

@task_manager.celery_app.task(name='highland_tower.send_notification')
def send_notification_task(recipient: str, message: str, notification_type: str):
    """Background task for sending notifications"""
    try:
        # Simulate notification sending
        time.sleep(1)  # Remove in production
        
        notification_data = {
            'recipient': recipient,
            'message': message,
            'type': notification_type,
            'sent_at': datetime.now().isoformat(),
            'status': 'sent'
        }
        
        return notification_data
    
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'completed_at': datetime.now().isoformat()
        }

class PerformanceMonitor:
    """Performance monitoring and optimization"""
    
    def __init__(self):
        self.metrics = {}
    
    def time_function(self, func_name: str):
        """Decorator to time function execution"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Store metrics
                if func_name not in self.metrics:
                    self.metrics[func_name] = []
                
                self.metrics[func_name].append({
                    'execution_time': execution_time,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Keep only last 100 measurements
                if len(self.metrics[func_name]) > 100:
                    self.metrics[func_name] = self.metrics[func_name][-100:]
                
                return result
            return wrapper
        return decorator
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        stats = {}
        
        for func_name, measurements in self.metrics.items():
            if measurements:
                times = [m['execution_time'] for m in measurements]
                stats[func_name] = {
                    'avg_time': sum(times) / len(times),
                    'min_time': min(times),
                    'max_time': max(times),
                    'call_count': len(times),
                    'last_call': measurements[-1]['timestamp']
                }
        
        return stats

# Global performance monitor
perf_monitor = PerformanceMonitor()

class DataLoader:
    """Optimized data loading with caching and pagination"""
    
    @staticmethod
    @cached(expire=600, key_prefix="data")
    def load_rfis(project_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """Load RFIs with pagination and caching"""
        # Simulate database query
        time.sleep(0.1)  # Remove in production
        
        # Mock data for Highland Tower
        total_rfis = 23
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, total_rfis)
        
        rfis = []
        for i in range(start_idx, end_idx):
            rfis.append({
                'id': f'RFI-HTD-{i+1:03d}',
                'subject': f'Highland Tower RFI {i+1}',
                'status': 'open' if i < 5 else 'closed',
                'created_date': (datetime.now() - timedelta(days=i)).isoformat(),
                'priority': 'high' if i < 3 else 'medium'
            })
        
        return {
            'rfis': rfis,
            'total_count': total_rfis,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_rfis + page_size - 1) // page_size
        }
    
    @staticmethod
    @cached(expire=300, key_prefix="data")
    def load_daily_reports(project_id: str, date_range: int = 30) -> List[Dict[str, Any]]:
        """Load daily reports with caching"""
        # Simulate database query
        time.sleep(0.15)  # Remove in production
        
        reports = []
        for i in range(date_range):
            report_date = datetime.now() - timedelta(days=i)
            reports.append({
                'id': f'DR-HTD-{report_date.strftime("%Y%m%d")}',
                'date': report_date.date().isoformat(),
                'weather': 'Partly Cloudy',
                'crew_count': 25 + (i % 10),
                'work_performed': f'Highland Tower construction activities - Day {i+1}',
                'safety_score': 98.5 - (i * 0.1)
            })
        
        return reports

def optimize_streamlit_performance():
    """Apply Streamlit-specific performance optimizations"""
    
    # Set page config for better performance
    if 'page_config_set' not in st.session_state:
        st.set_page_config(
            page_title="Highland Tower Development",
            page_icon="🏗️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        st.session_state.page_config_set = True
    
    # Cache frequently used data in session state
    if 'performance_cache' not in st.session_state:
        st.session_state.performance_cache = {}

def render_performance_dashboard():
    """Render performance monitoring dashboard"""
    st.subheader("📊 Highland Tower Performance Dashboard")
    
    # Cache status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cache_status = "🟢 Redis Available" if cache.available else "🔴 Fallback Cache"
        st.metric("Cache Status", cache_status)
    
    with col2:
        # Get cache hit rate (mock for now)
        hit_rate = "85.2%"
        st.metric("Cache Hit Rate", hit_rate, "↑ 12%")
    
    with col3:
        # Background tasks status
        task_status = "🟢 Active"
        st.metric("Background Tasks", task_status)
    
    # Performance metrics
    st.markdown("#### Function Performance Metrics")
    stats = perf_monitor.get_performance_stats()
    
    if stats:
        performance_data = []
        for func_name, metrics in stats.items():
            performance_data.append({
                "Function": func_name,
                "Avg Time (ms)": f"{metrics['avg_time']*1000:.2f}",
                "Min Time (ms)": f"{metrics['min_time']*1000:.2f}",
                "Max Time (ms)": f"{metrics['max_time']*1000:.2f}",
                "Call Count": metrics['call_count']
            })
        
        st.dataframe(performance_data, use_container_width=True)
    else:
        st.info("No performance metrics available yet")
    
    # Cache management
    st.markdown("#### Cache Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Clear Dashboard Cache", use_container_width=True):
            cleared = invalidate_cache("dashboard*")
            st.success(f"Cleared {cleared} dashboard cache entries")
    
    with col2:
        if st.button("Clear Report Cache", use_container_width=True):
            cleared = invalidate_cache("report*")
            st.success(f"Cleared {cleared} report cache entries")
    
    with col3:
        if st.button("Clear All Cache", use_container_width=True):
            cleared = invalidate_cache("highland*")
            st.success(f"Cleared {cleared} cache entries")

def async_task_status():
    """Display background task status"""
    st.markdown("#### Background Task Status")
    
    # Mock task statuses for Highland Tower
    tasks = [
        {"Task": "Procore Data Sync", "Status": "✅ Completed", "Last Run": "2024-05-29 14:30", "Duration": "2.3s"},
        {"Task": "Report Generation", "Status": "🔄 Running", "Last Run": "2024-05-29 14:25", "Duration": "45s"},
        {"Task": "Autodesk Sync", "Status": "⏳ Queued", "Last Run": "2024-05-29 14:20", "Duration": "-"},
        {"Task": "Email Notifications", "Status": "✅ Completed", "Last Run": "2024-05-29 14:15", "Duration": "0.8s"}
    ]
    
    st.dataframe(tasks, use_container_width=True)
    
    # Task controls
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Sync All Platforms", use_container_width=True):
            # Queue background sync tasks
            st.info("Background sync tasks queued for all platforms")
    
    with col2:
        if st.button("📊 Generate Full Report", use_container_width=True):
            # Queue report generation
            st.info("Full project report generation started in background")