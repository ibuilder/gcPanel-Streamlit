"""
Database migrations module.

This module handles database schema migrations to ensure
smooth upgrades between different application versions.
"""

import os
import logging
import alembic.config
from alembic import command
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext

# Setup logging
logger = logging.getLogger(__name__)

def init_migrations():
    """
    Initialize the migrations directory structure if it doesn't exist.
    
    This should be called once during application setup.
    """
    try:
        # Create migrations directory if it doesn't exist
        os.makedirs("migrations/versions", exist_ok=True)
        
        # Create alembic.ini if it doesn't exist
        if not os.path.exists("alembic.ini"):
            with open("alembic.ini", "w") as f:
                f.write("""[alembic]
script_location = migrations
prepend_sys_path = .
version_path_separator = os

sqlalchemy.url = 

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = INFO
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
""")
        
        # Create migrations directory structure
        if not os.path.exists("migrations/env.py"):
            os.makedirs("migrations", exist_ok=True)
            
            # Create env.py
            with open("migrations/env.py", "w") as f:
                f.write("""from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import logging
import os

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Add model's MetaData object here for autogenerate support
from core.models.base import Base
target_metadata = Base.metadata

# Get the database URL from the environment
from core.database.config import DATABASE_URL, DB_PATH
url = DATABASE_URL or f"sqlite:///{DB_PATH}"
config.set_main_option('sqlalchemy.url', url)

def run_migrations_offline():
    \"\"\"Run migrations in 'offline' mode.\"\"\"
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    \"\"\"Run migrations in 'online' mode.\"\"\"
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
""")
            
            # Create README
            with open("migrations/README", "w") as f:
                f.write("# Database Migrations\n\nThis directory contains database migrations managed by Alembic.\n")
            
            # Create script.py.mako
            with open("migrations/script.py.mako", "w") as f:
                f.write("""\"\"\"${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

\"\"\"
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}
""")
        
        logger.info("Migration system initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing migrations: {str(e)}")
        return False

def create_migration(message="schema update"):
    """
    Create a new migration file.
    
    Args:
        message: Migration description
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Initialize alembic config
        alembic_cfg = alembic.config.Config("alembic.ini")
        
        # Create a new migration
        command.revision(alembic_cfg, message=message, autogenerate=True)
        logger.info(f"Migration created: {message}")
        return True
    except Exception as e:
        logger.error(f"Error creating migration: {str(e)}")
        return False

def run_migrations():
    """
    Run all pending migrations.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Initialize alembic config
        alembic_cfg = alembic.config.Config("alembic.ini")
        
        # Run migrations
        command.upgrade(alembic_cfg, "head")
        logger.info("Migrations applied successfully")
        return True
    except Exception as e:
        logger.error(f"Error applying migrations: {str(e)}")
        return False

def get_migration_status():
    """
    Get the current migration status.
    
    Returns:
        dict: Migration status information
    """
    try:
        # Initialize alembic config
        alembic_cfg = alembic.config.Config("alembic.ini")
        
        # Get migration information
        script = ScriptDirectory.from_config(alembic_cfg)
        heads = script.get_heads()
        
        # Get current revision (requires custom implementation)
        current = None
        try:
            from core.database.config import get_db_session
            with get_db_session() as session:
                result = session.execute("SELECT version_num FROM alembic_version").fetchone()
                if result:
                    current = result[0]
        except Exception:
            current = None
            
        return {
            "current_revision": current,
            "latest_revision": heads[0] if heads else None,
            "is_current": current in heads if current and heads else False,
            "total_migrations": len(script.get_revisions())
        }
    except Exception as e:
        logger.error(f"Error getting migration status: {str(e)}")
        return {
            "error": str(e),
            "current_revision": None,
            "latest_revision": None,
            "is_current": False,
            "total_migrations": 0
        }