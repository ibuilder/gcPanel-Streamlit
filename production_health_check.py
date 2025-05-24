"""
Highland Tower Development - Production Health Check

Run this script to validate production readiness and fix critical issues.
"""

import os
import sys
import traceback
from datetime import datetime

def run_production_health_check():
    """Run comprehensive health check for Highland Tower Development dashboard."""
    
    print("🏗️ Highland Tower Development - Production Health Check")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    issues_found = []
    warnings = []
    success_count = 0
    
    # Check 1: Environment Variables
    print("🔧 Checking Environment Variables...")
    required_vars = ['DATABASE_URL', 'JWT_SECRET_KEY', 'SECRET_KEY']
    
    for var in required_vars:
        if os.environ.get(var):
            print(f"  ✅ {var} - Configured")
            success_count += 1
        else:
            print(f"  ❌ {var} - Missing")
            issues_found.append(f"Environment variable {var} not set")
    
    # Check 2: Core Imports
    print("\n📦 Checking Core Module Imports...")
    core_modules = [
        'streamlit',
        'pandas', 
        'datetime',
        'logging'
    ]
    
    for module in core_modules:
        try:
            __import__(module)
            print(f"  ✅ {module} - Available")
            success_count += 1
        except ImportError:
            print(f"  ❌ {module} - Missing")
            issues_found.append(f"Required module {module} not available")
    
    # Check 3: Highland Tower Modules
    print("\n🏗️ Checking Highland Tower Modules...")
    highland_modules = [
        'app',
        'app_config',
        'app_manager',
        'login_form'
    ]
    
    for module in highland_modules:
        try:
            if os.path.exists(f"{module}.py"):
                print(f"  ✅ {module}.py - Found")
                success_count += 1
            else:
                print(f"  ⚠️ {module}.py - Not found")
                warnings.append(f"Module file {module}.py missing")
        except Exception as e:
            print(f"  ❌ {module} - Error: {str(e)}")
            issues_found.append(f"Module {module} has issues")
    
    # Check 4: Database Connection
    print("\n🗄️ Checking Database Configuration...")
    database_url = os.environ.get('DATABASE_URL', '')
    
    if database_url:
        if 'localhost' in database_url or '127.0.0.1' in database_url:
            print("  ⚠️ Database - Using localhost (not production-ready)")
            warnings.append("Database using localhost - configure production database")
        else:
            print("  ✅ Database - Production URL configured")
            success_count += 1
    else:
        print("  ❌ Database - No URL configured")
        issues_found.append("DATABASE_URL not configured")
    
    # Check 5: Asset Files
    print("\n🎨 Checking Asset Files...")
    asset_files = [
        'assets/dark_theme_styles.py',
        'assets/construction_dashboard_js.py'
    ]
    
    for asset in asset_files:
        if os.path.exists(asset):
            print(f"  ✅ {asset} - Found")
            success_count += 1
        else:
            print(f"  ⚠️ {asset} - Not found")
            warnings.append(f"Asset file {asset} missing")
    
    # Check 6: Logs Directory
    print("\n📝 Checking Logging Setup...")
    if not os.path.exists('logs'):
        try:
            os.makedirs('logs')
            print("  ✅ Logs directory created")
            success_count += 1
        except Exception as e:
            print(f"  ❌ Failed to create logs directory: {str(e)}")
            issues_found.append("Cannot create logs directory")
    else:
        print("  ✅ Logs directory exists")
        success_count += 1
    
    # Generate Report
    print("\n" + "=" * 60)
    print("📊 HIGHLAND TOWER DEVELOPMENT - HEALTH CHECK RESULTS")
    print("=" * 60)
    
    total_checks = success_count + len(issues_found) + len(warnings)
    health_score = (success_count / total_checks * 100) if total_checks > 0 else 0
    
    print(f"Health Score: {health_score:.1f}%")
    print(f"Successful Checks: {success_count}")
    print(f"Critical Issues: {len(issues_found)}")
    print(f"Warnings: {len(warnings)}")
    
    if issues_found:
        print("\n🔴 CRITICAL ISSUES TO FIX:")
        for i, issue in enumerate(issues_found, 1):
            print(f"  {i}. {issue}")
    
    if warnings:
        print("\n⚠️ WARNINGS:")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")
    
    # Deployment Recommendation
    print("\n🚀 DEPLOYMENT RECOMMENDATION:")
    if health_score >= 90:
        print("✅ READY FOR PRODUCTION - Highland Tower dashboard is enterprise-ready!")
    elif health_score >= 75:
        print("⚠️ MINOR FIXES NEEDED - Address warnings before deployment")
    elif health_score >= 50:
        print("🔧 FIXES REQUIRED - Resolve critical issues before production")
    else:
        print("🚨 MAJOR ISSUES - Significant work needed before deployment")
    
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return health_score >= 75

if __name__ == "__main__":
    try:
        is_ready = run_production_health_check()
        sys.exit(0 if is_ready else 1)
    except Exception as e:
        print(f"\n❌ Health check failed: {str(e)}")
        print(traceback.format_exc())
        sys.exit(1)