"""
Pure Python Configuration Manager for Highland Tower Development
Environment-independent configuration management using standard Python

This eliminates dependency on framework-specific configuration systems
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class Environment(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20


@dataclass
class APIConfig:
    """API configuration"""
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    cors_origins: list = None


@dataclass
class FileConfig:
    """File handling configuration"""
    upload_dir: str = "uploads"
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allowed_extensions: list = None


@dataclass
class SecurityConfig:
    """Security configuration"""
    secret_key: str
    jwt_expiry_hours: int = 24
    password_min_length: int = 8
    max_login_attempts: int = 5


@dataclass
class HighlandTowerConfig:
    """Highland Tower Development specific configuration"""
    project_id: str = "HTD-2024-001"
    project_name: str = "Highland Tower Development"
    project_value: float = 45500000.0
    residential_units: int = 120
    retail_units: int = 8
    floors_above: int = 15
    floors_below: int = 2
    completion_target: str = "2025-12-31"


@dataclass
class AppConfig:
    """Main application configuration"""
    environment: Environment
    debug: bool
    database: DatabaseConfig
    api: APIConfig
    files: FileConfig
    security: SecurityConfig
    highland_tower: HighlandTowerConfig


class ConfigManager:
    """Pure Python configuration management"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or self._get_default_config_file()
        self.config: Optional[AppConfig] = None
        self._load_config()
    
    def _get_default_config_file(self) -> str:
        """Get default configuration file path"""
        env = os.getenv("HIGHLAND_ENV", "development")
        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / f"{env}.json")
    
    def _load_config(self):
        """Load configuration from file or environment"""
        if Path(self.config_file).exists():
            self._load_from_file()
        else:
            self._load_from_environment()
            self._save_config()  # Save for future use
    
    def _load_from_file(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                config_data = json.load(f)
            
            self.config = AppConfig(
                environment=Environment(config_data.get("environment", "development")),
                debug=config_data.get("debug", True),
                database=DatabaseConfig(**config_data.get("database", {})),
                api=APIConfig(**config_data.get("api", {})),
                files=FileConfig(**config_data.get("files", {})),
                security=SecurityConfig(**config_data.get("security", {})),
                highland_tower=HighlandTowerConfig(**config_data.get("highland_tower", {}))
            )
        except Exception as e:
            print(f"Error loading config from file: {e}")
            self._load_from_environment()
    
    def _load_from_environment(self):
        """Load configuration from environment variables"""
        env_name = os.getenv("HIGHLAND_ENV", "development")
        environment = Environment(env_name)
        
        # Database configuration
        database_url = os.getenv("DATABASE_URL", "sqlite:///highland_tower.db")
        database = DatabaseConfig(
            url=database_url,
            echo=environment == Environment.DEVELOPMENT
        )
        
        # API configuration
        api = APIConfig(
            host=os.getenv("API_HOST", "0.0.0.0"),
            port=int(os.getenv("API_PORT", "8000")),
            debug=environment == Environment.DEVELOPMENT,
            cors_origins=["*"] if environment == Environment.DEVELOPMENT else []
        )
        
        # File configuration
        files = FileConfig(
            upload_dir=os.getenv("UPLOAD_DIR", "uploads"),
            max_file_size=int(os.getenv("MAX_FILE_SIZE", "52428800")),  # 50MB
            allowed_extensions=[".pdf", ".jpg", ".jpeg", ".png", ".dwg", ".xlsx", ".docx"]
        )
        
        # Security configuration
        security = SecurityConfig(
            secret_key=os.getenv("SECRET_KEY", "highland-tower-dev-key-change-in-prod"),
            jwt_expiry_hours=int(os.getenv("JWT_EXPIRY_HOURS", "24")),
            password_min_length=int(os.getenv("PASSWORD_MIN_LENGTH", "8")),
            max_login_attempts=int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
        )
        
        # Highland Tower specific configuration
        highland_tower = HighlandTowerConfig()
        
        self.config = AppConfig(
            environment=environment,
            debug=environment == Environment.DEVELOPMENT,
            database=database,
            api=api,
            files=files,
            security=security,
            highland_tower=highland_tower
        )
    
    def _save_config(self):
        """Save current configuration to file"""
        try:
            config_data = asdict(self.config)
            config_data["environment"] = self.config.environment.value
            
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Warning: Could not save config file: {e}")
    
    def get_config(self) -> AppConfig:
        """Get current configuration"""
        return self.config
    
    def update_config(self, updates: Dict[str, Any]):
        """Update configuration with new values"""
        config_dict = asdict(self.config)
        config_dict.update(updates)
        
        # Recreate config object
        self.config = AppConfig(
            environment=Environment(config_dict.get("environment", "development")),
            debug=config_dict.get("debug", True),
            database=DatabaseConfig(**config_dict.get("database", {})),
            api=APIConfig(**config_dict.get("api", {})),
            files=FileConfig(**config_dict.get("files", {})),
            security=SecurityConfig(**config_dict.get("security", {})),
            highland_tower=HighlandTowerConfig(**config_dict.get("highland_tower", {}))
        )
        
        self._save_config()
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate current configuration"""
        issues = []
        warnings = []
        
        # Validate database configuration
        if not self.config.database.url:
            issues.append("Database URL is required")
        
        # Validate security in production
        if self.config.environment == Environment.PRODUCTION:
            if "dev-key" in self.config.security.secret_key:
                issues.append("Production requires a secure secret key")
            
            if self.config.debug:
                warnings.append("Debug mode should be disabled in production")
        
        # Validate Highland Tower specific settings
        if self.config.highland_tower.project_value <= 0:
            issues.append("Project value must be positive")
        
        if self.config.highland_tower.residential_units <= 0:
            warnings.append("Residential units count seems low")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }
    
    def get_environment_info(self) -> Dict[str, Any]:
        """Get current environment information"""
        return {
            "environment": self.config.environment.value,
            "debug_mode": self.config.debug,
            "database_type": "postgresql" if "postgresql" in self.config.database.url else "sqlite",
            "api_endpoint": f"http://{self.config.api.host}:{self.config.api.port}",
            "upload_directory": self.config.files.upload_dir,
            "highland_tower_project": {
                "name": self.config.highland_tower.project_name,
                "value": f"${self.config.highland_tower.project_value:,.0f}",
                "units": f"{self.config.highland_tower.residential_units} residential + {self.config.highland_tower.retail_units} retail"
            }
        }


# Global configuration manager instance
config_manager = ConfigManager()


def get_config() -> AppConfig:
    """Get application configuration"""
    return config_manager.get_config()


def get_highland_tower_config() -> HighlandTowerConfig:
    """Get Highland Tower specific configuration"""
    return config_manager.get_config().highland_tower


def is_production() -> bool:
    """Check if running in production environment"""
    return config_manager.get_config().environment == Environment.PRODUCTION


def is_development() -> bool:
    """Check if running in development environment"""
    return config_manager.get_config().environment == Environment.DEVELOPMENT