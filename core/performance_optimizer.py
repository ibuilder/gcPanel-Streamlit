"""
Pure Python Performance Optimizer for Highland Tower Development
CPU and memory optimization using standard Python libraries

This provides sustainable performance monitoring and optimization
"""

import time
import psutil
import threading
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime, timedelta
from functools import wraps
from dataclasses import dataclass
import gc

from .caching_layer import highland_cache


@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    timestamp: datetime
    cpu_percent: float
    memory_usage_mb: float
    active_threads: int
    cache_hit_rate: float
    response_time_ms: float
    operation_name: str


class PerformanceMonitor:
    """Pure Python performance monitoring"""
    
    def __init__(self):
        self.metrics: List[PerformanceMetrics] = []
        self.operation_times: Dict[str, List[float]] = {}
        self._lock = threading.Lock()
        self.start_time = time.time()
    
    def record_operation(self, operation_name: str, execution_time: float):
        """Record operation performance"""
        with self._lock:
            if operation_name not in self.operation_times:
                self.operation_times[operation_name] = []
            
            self.operation_times[operation_name].append(execution_time)
            
            # Keep only last 100 measurements per operation
            if len(self.operation_times[operation_name]) > 100:
                self.operation_times[operation_name] = self.operation_times[operation_name][-100:]
            
            # Record full metrics
            metrics = PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_percent=psutil.cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                active_threads=threading.active_count(),
                cache_hit_rate=self._calculate_cache_hit_rate(),
                response_time_ms=execution_time * 1000,
                operation_name=operation_name
            )
            
            self.metrics.append(metrics)
            
            # Keep only last 1000 metrics
            if len(self.metrics) > 1000:
                self.metrics = self.metrics[-1000:]
    
    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        try:
            cache_stats = highland_cache.get_cache_summary()
            hits = cache_stats.get('cache_hits', 0)
            total = cache_stats.get('total_cached_items', 0)
            return (hits / max(total, 1)) * 100
        except:
            return 0.0
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        with self._lock:
            if not self.metrics:
                return {"status": "no_data"}
            
            recent_metrics = self.metrics[-50:]  # Last 50 operations
            
            avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
            avg_memory = sum(m.memory_usage_mb for m in recent_metrics) / len(recent_metrics)
            avg_response = sum(m.response_time_ms for m in recent_metrics) / len(recent_metrics)
            
            # Operation performance breakdown
            operation_stats = {}
            for op_name, times in self.operation_times.items():
                if times:
                    operation_stats[op_name] = {
                        "avg_time_ms": (sum(times) / len(times)) * 1000,
                        "min_time_ms": min(times) * 1000,
                        "max_time_ms": max(times) * 1000,
                        "total_calls": len(times)
                    }
            
            return {
                "highland_tower_performance": {
                    "uptime_seconds": time.time() - self.start_time,
                    "average_cpu_percent": round(avg_cpu, 2),
                    "average_memory_mb": round(avg_memory, 2),
                    "average_response_time_ms": round(avg_response, 2),
                    "active_threads": threading.active_count(),
                    "cache_hit_rate": round(self._calculate_cache_hit_rate(), 2)
                },
                "operation_performance": operation_stats,
                "system_health": self._get_system_health()
            }
    
    def _get_system_health(self) -> Dict[str, Any]:
        """Get system health indicators"""
        try:
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "memory_available_mb": memory.available / 1024 / 1024,
                "memory_percent_used": memory.percent,
                "disk_free_gb": disk.free / 1024 / 1024 / 1024,
                "disk_percent_used": (disk.used / disk.total) * 100,
                "cpu_count": psutil.cpu_count()
            }
        except:
            return {"status": "unavailable"}


def performance_monitor(operation_name: str):
    """Decorator for monitoring operation performance"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                execution_time = time.time() - start_time
                performance_tracker.record_operation(operation_name, execution_time)
        return wrapper
    return decorator


class MemoryOptimizer:
    """Pure Python memory optimization"""
    
    @staticmethod
    def cleanup_memory():
        """Force garbage collection and cleanup"""
        collected = gc.collect()
        return {
            "objects_collected": collected,
            "memory_freed": "garbage_collection_completed"
        }
    
    @staticmethod
    def get_memory_usage() -> Dict[str, Any]:
        """Get detailed memory usage"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            
            return {
                "rss_mb": memory_info.rss / 1024 / 1024,
                "vms_mb": memory_info.vms / 1024 / 1024,
                "percent": process.memory_percent(),
                "available_mb": psutil.virtual_memory().available / 1024 / 1024
            }
        except:
            return {"status": "unavailable"}


class HighlandTowerOptimizer:
    """Highland Tower Development specific optimizations"""
    
    def __init__(self):
        self.performance_monitor = PerformanceMonitor()
        self.memory_optimizer = MemoryOptimizer()
    
    def optimize_rfi_operations(self):
        """Optimize RFI data operations"""
        # Clear expired cache entries
        highland_cache.cache.cleanup_expired()
        
        # Force garbage collection
        self.memory_optimizer.cleanup_memory()
        
        return {
            "rfi_cache_cleaned": True,
            "memory_optimized": True,
            "optimization_timestamp": datetime.now().isoformat()
        }
    
    def get_highland_tower_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive Highland Tower performance report"""
        performance_summary = self.performance_monitor.get_performance_summary()
        memory_usage = self.memory_optimizer.get_memory_usage()
        cache_summary = highland_cache.get_cache_summary()
        
        return {
            "highland_tower_performance_report": {
                "generated_at": datetime.now().isoformat(),
                "project": "Highland Tower Development - $45.5M",
                "performance_metrics": performance_summary,
                "memory_optimization": memory_usage,
                "cache_efficiency": cache_summary,
                "recommendations": self._generate_recommendations(performance_summary, memory_usage)
            }
        }
    
    def _generate_recommendations(self, performance: Dict[str, Any], memory: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        highland_perf = performance.get("highland_tower_performance", {})
        
        # CPU recommendations
        if highland_perf.get("average_cpu_percent", 0) > 80:
            recommendations.append("Consider optimizing CPU-intensive operations")
        
        # Memory recommendations
        if memory.get("percent", 0) > 85:
            recommendations.append("Memory usage is high - consider cleanup operations")
        
        # Cache recommendations
        if highland_perf.get("cache_hit_rate", 0) < 50:
            recommendations.append("Cache hit rate is low - review caching strategy")
        
        # Response time recommendations
        if highland_perf.get("average_response_time_ms", 0) > 1000:
            recommendations.append("Response times are slow - investigate bottlenecks")
        
        if not recommendations:
            recommendations.append("Highland Tower system performance is optimal")
        
        return recommendations


# Global instances
performance_tracker = PerformanceMonitor()
highland_optimizer = HighlandTowerOptimizer()


# Performance monitoring decorators for Highland Tower operations
def monitor_rfi_performance(func):
    """Monitor RFI operation performance"""
    return performance_monitor("highland_rfi_operation")(func)


def monitor_dashboard_performance(func):
    """Monitor dashboard operation performance"""
    return performance_monitor("highland_dashboard_operation")(func)


def monitor_analytics_performance(func):
    """Monitor analytics operation performance"""
    return performance_monitor("highland_analytics_operation")(func)