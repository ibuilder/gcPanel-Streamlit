"""
Backup and recovery utilities for gcPanel.

This module provides functions for database backups,
automated backup verification, and point-in-time recovery.
"""

import os
import subprocess
import logging
import tempfile
import datetime
import json
import shutil
import gzip
from pathlib import Path

# Setup logging
logger = logging.getLogger(__name__)

# Constants
BACKUP_DIR = os.environ.get("BACKUP_DIR", "backups")
RETENTION_DAYS = int(os.environ.get("BACKUP_RETENTION_DAYS", "30"))

def ensure_backup_dir():
    """Ensure backup directory exists."""
    os.makedirs(BACKUP_DIR, exist_ok=True)

def generate_backup_filename(prefix="backup", include_timestamp=True):
    """
    Generate a filename for a backup.
    
    Args:
        prefix: Prefix for the filename
        include_timestamp: Whether to include a timestamp
        
    Returns:
        str: Backup filename
    """
    if include_timestamp:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.sql.gz"
    return f"{prefix}.sql.gz"

def get_connection_string():
    """
    Get database connection string for backup/restore.
    
    Returns:
        str: Connection options for PostgreSQL
    """
    # Check if using PostgreSQL
    database_url = os.environ.get("DATABASE_URL", "")
    
    if database_url and database_url.startswith("postgresql"):
        # Parse components from DATABASE_URL
        import urllib.parse
        parsed_url = urllib.parse.urlparse(database_url)
        
        # Extract connection parameters
        user = parsed_url.username
        password = parsed_url.password
        host = parsed_url.hostname
        port = parsed_url.port or 5432
        dbname = parsed_url.path.lstrip('/')
        
        return f"-h {host} -p {port} -U {user} -d {dbname}"
    
    # Using SQLite
    db_path = os.environ.get("DB_PATH", "data/gcpanel.db")
    return db_path

def create_backup(backup_file=None):
    """
    Create a backup of the database.
    
    Args:
        backup_file: Optional filename for the backup
        
    Returns:
        tuple: (success, backup_file)
    """
    ensure_backup_dir()
    
    if not backup_file:
        backup_file = os.path.join(BACKUP_DIR, generate_backup_filename())
    
    try:
        # Check if we're using PostgreSQL
        database_url = os.environ.get("DATABASE_URL", "")
        
        if database_url and database_url.startswith("postgresql"):
            # Use pg_dump for PostgreSQL
            conn_string = get_connection_string()
            
            # Run pg_dump and pipe to gzip
            cmd = f"PGPASSWORD='{os.environ.get('POSTGRES_PASSWORD')}' pg_dump {conn_string} | gzip > {backup_file}"
            subprocess.run(cmd, shell=True, check=True)
            
            logger.info(f"PostgreSQL backup created: {backup_file}")
            
        else:
            # SQLite backup
            db_path = os.environ.get("DB_PATH", "data/gcpanel.db")
            
            # Check if database exists
            if not os.path.exists(db_path):
                logger.error(f"SQLite database not found: {db_path}")
                return False, None
            
            # Create backup using sqlite3 dump
            with tempfile.NamedTemporaryFile(mode='w') as temp_sql:
                cmd = f"sqlite3 {db_path} .dump"
                subprocess.run(cmd, shell=True, check=True, stdout=temp_sql)
                
                # Compress with gzip
                with open(temp_sql.name, 'rb') as f_in:
                    with gzip.open(backup_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            
            logger.info(f"SQLite backup created: {backup_file}")
        
        # Add backup metadata
        add_backup_metadata(backup_file)
        
        return True, backup_file
        
    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")
        return False, None

def restore_backup(backup_file):
    """
    Restore a database from a backup.
    
    Args:
        backup_file: Path to the backup file
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not os.path.exists(backup_file):
        logger.error(f"Backup file not found: {backup_file}")
        return False
    
    try:
        # Check if we're using PostgreSQL
        database_url = os.environ.get("DATABASE_URL", "")
        
        if database_url and database_url.startswith("postgresql"):
            # Use pg_restore for PostgreSQL
            conn_string = get_connection_string()
            
            # Run gunzip and pipe to psql
            cmd = f"gunzip -c {backup_file} | PGPASSWORD='{os.environ.get('POSTGRES_PASSWORD')}' psql {conn_string}"
            subprocess.run(cmd, shell=True, check=True)
            
            logger.info(f"PostgreSQL backup restored: {backup_file}")
            
        else:
            # SQLite restore
            db_path = os.environ.get("DB_PATH", "data/gcpanel.db")
            
            # Create a backup of the current database first
            current_backup = os.path.join(BACKUP_DIR, "pre_restore_" + generate_backup_filename())
            create_backup(current_backup)
            
            # Extract SQL from gzip
            with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_sql:
                with gzip.open(backup_file, 'rb') as f_in:
                    shutil.copyfileobj(f_in, temp_sql)
            
            try:
                # Delete existing database
                if os.path.exists(db_path):
                    os.remove(db_path)
                
                # Restore using sqlite3
                cmd = f"sqlite3 {db_path} < {temp_sql.name}"
                subprocess.run(cmd, shell=True, check=True)
                
                logger.info(f"SQLite backup restored: {backup_file}")
            finally:
                # Clean up temp file
                os.unlink(temp_sql.name)
        
        return True
        
    except Exception as e:
        logger.error(f"Restore failed: {str(e)}")
        return False

def verify_backup(backup_file):
    """
    Verify a backup file is valid and can be restored.
    
    Args:
        backup_file: Path to the backup file
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not os.path.exists(backup_file):
        logger.error(f"Backup file not found: {backup_file}")
        return False
    
    try:
        # Create a temporary directory for verification
        with tempfile.TemporaryDirectory() as temp_dir:
            # Check if we're using PostgreSQL
            database_url = os.environ.get("DATABASE_URL", "")
            
            if database_url and database_url.startswith("postgresql"):
                # Create a temporary database for verification
                temp_db = "verify_backup"
                
                # Create the test database
                conn_string = get_connection_string().replace(f"-d {temp_db}", "")
                create_cmd = f"PGPASSWORD='{os.environ.get('POSTGRES_PASSWORD')}' createdb {conn_string} {temp_db}"
                subprocess.run(create_cmd, shell=True, check=True)
                
                try:
                    # Restore to the test database
                    restore_cmd = f"gunzip -c {backup_file} | PGPASSWORD='{os.environ.get('POSTGRES_PASSWORD')}' psql {conn_string} -d {temp_db}"
                    subprocess.run(restore_cmd, shell=True, check=True)
                    
                    # Check if we can query the test database
                    test_cmd = f"PGPASSWORD='{os.environ.get('POSTGRES_PASSWORD')}' psql {conn_string} -d {temp_db} -c 'SELECT 1'"
                    result = subprocess.run(test_cmd, shell=True, check=True, capture_output=True)
                    
                    return "1" in result.stdout.decode()
                    
                finally:
                    # Drop the test database
                    drop_cmd = f"PGPASSWORD='{os.environ.get('POSTGRES_PASSWORD')}' dropdb {conn_string} {temp_db}"
                    subprocess.run(drop_cmd, shell=True, check=True)
            
            else:
                # SQLite verification
                temp_db = os.path.join(temp_dir, "verify.db")
                
                # Extract SQL from gzip
                with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_sql:
                    with gzip.open(backup_file, 'rb') as f_in:
                        shutil.copyfileobj(f_in, temp_sql)
                
                try:
                    # Restore to temporary database
                    cmd = f"sqlite3 {temp_db} < {temp_sql.name}"
                    subprocess.run(cmd, shell=True, check=True)
                    
                    # Check if we can query the database
                    test_cmd = f"sqlite3 {temp_db} 'SELECT 1'"
                    result = subprocess.run(test_cmd, shell=True, check=True, capture_output=True)
                    
                    return "1" in result.stdout.decode()
                
                finally:
                    # Clean up temp file
                    os.unlink(temp_sql.name)
    
    except Exception as e:
        logger.error(f"Backup verification failed: {str(e)}")
        return False

def add_backup_metadata(backup_file):
    """
    Add metadata to a backup file.
    
    Args:
        backup_file: Path to the backup file
    """
    metadata = {
        "filename": os.path.basename(backup_file),
        "created_at": datetime.datetime.now().isoformat(),
        "database_type": "postgresql" if os.environ.get("DATABASE_URL", "").startswith("postgresql") else "sqlite",
        "size_bytes": os.path.getsize(backup_file),
        "application_version": os.environ.get("APP_VERSION", "unknown")
    }
    
    # Create metadata file
    metadata_file = backup_file + ".meta"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

def get_backup_metadata(backup_file):
    """
    Get metadata for a backup file.
    
    Args:
        backup_file: Path to the backup file
        
    Returns:
        dict: Backup metadata
    """
    metadata_file = backup_file + ".meta"
    
    if not os.path.exists(metadata_file):
        # Generate basic metadata if file doesn't exist
        return {
            "filename": os.path.basename(backup_file),
            "created_at": datetime.datetime.fromtimestamp(os.path.getctime(backup_file)).isoformat(),
            "size_bytes": os.path.getsize(backup_file)
        }
    
    with open(metadata_file, 'r') as f:
        return json.load(f)

def list_backups():
    """
    List all backups with metadata.
    
    Returns:
        list: List of backup info dictionaries
    """
    ensure_backup_dir()
    
    backups = []
    
    for file in os.listdir(BACKUP_DIR):
        if file.endswith(".sql.gz"):
            backup_file = os.path.join(BACKUP_DIR, file)
            metadata = get_backup_metadata(backup_file)
            backups.append(metadata)
    
    # Sort by creation time (newest first)
    backups.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    return backups

def cleanup_old_backups():
    """
    Clean up old backups beyond retention period.
    
    Returns:
        int: Number of backups removed
    """
    ensure_backup_dir()
    
    retention_date = datetime.datetime.now() - datetime.timedelta(days=RETENTION_DAYS)
    count = 0
    
    for file in os.listdir(BACKUP_DIR):
        if file.endswith(".sql.gz"):
            backup_file = os.path.join(BACKUP_DIR, file)
            metadata_file = backup_file + ".meta"
            
            # Get creation time
            try:
                if os.path.exists(metadata_file):
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                        created_at = datetime.datetime.fromisoformat(metadata.get("created_at", ""))
                else:
                    created_at = datetime.datetime.fromtimestamp(os.path.getctime(backup_file))
                
                # Remove if older than retention period
                if created_at < retention_date:
                    os.remove(backup_file)
                    if os.path.exists(metadata_file):
                        os.remove(metadata_file)
                    count += 1
                    logger.info(f"Removed old backup: {file}")
            
            except Exception as e:
                logger.error(f"Error processing backup for cleanup: {file}, {str(e)}")
    
    return count

def scheduled_backup():
    """Perform a scheduled backup with verification."""
    logger.info("Starting scheduled backup")
    
    success, backup_file = create_backup()
    
    if success and backup_file:
        # Verify backup
        if verify_backup(backup_file):
            logger.info(f"Backup verified successfully: {backup_file}")
            
            # Clean up old backups
            removed = cleanup_old_backups()
            logger.info(f"Cleaned up {removed} old backups")
            
            return True, backup_file
        else:
            logger.error(f"Backup verification failed: {backup_file}")
            return False, backup_file
    
    return False, None

def point_in_time_recovery(timestamp):
    """
    Restore database to a specific point in time.
    
    Args:
        timestamp: ISO format timestamp or backup filename
        
    Returns:
        bool: True if successful, False otherwise
    """
    # List all backups
    backups = list_backups()
    
    if not backups:
        logger.error("No backups available for point-in-time recovery")
        return False
    
    # Find the backup closest to the requested timestamp
    target_backup = None
    
    if timestamp.endswith(".sql.gz"):
        # Direct filename provided
        backup_path = os.path.join(BACKUP_DIR, timestamp)
        if os.path.exists(backup_path):
            target_backup = backup_path
    else:
        # Timestamp provided, find closest backup
        try:
            target_time = datetime.datetime.fromisoformat(timestamp)
            
            closest_backup = None
            smallest_diff = None
            
            for backup in backups:
                backup_time = datetime.datetime.fromisoformat(backup.get("created_at", ""))
                
                # Only consider backups before the target time
                if backup_time <= target_time:
                    diff = (target_time - backup_time).total_seconds()
                    
                    if smallest_diff is None or diff < smallest_diff:
                        smallest_diff = diff
                        closest_backup = backup
            
            if closest_backup:
                target_backup = os.path.join(BACKUP_DIR, closest_backup.get("filename"))
        
        except ValueError:
            logger.error(f"Invalid timestamp format: {timestamp}")
            return False
    
    # Restore the target backup
    if target_backup and os.path.exists(target_backup):
        logger.info(f"Restoring backup for point-in-time recovery: {target_backup}")
        return restore_backup(target_backup)
    
    logger.error(f"No suitable backup found for point-in-time recovery: {timestamp}")
    return False