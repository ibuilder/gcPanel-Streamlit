"""
Configuration models for application settings.

This module defines configuration models that store application-wide
settings and preferences.
"""

from sqlalchemy import Column, String, Text, Boolean
from core.models.base import BaseModel

class AppConfig(BaseModel):
    """
    Application configuration settings model.
    
    This model stores key-value pairs for application configuration
    with support for different data types.
    
    Attributes:
        key (str): Configuration key (unique identifier)
        value (str): Configuration value
        description (str): Optional description of what this setting does
        is_system (bool): Whether this is a system setting (not user-editable)
    """
    
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    is_system = Column(Boolean, default=False, nullable=False)
    
    @classmethod
    def get_value(cls, session, key, default=None):
        """
        Get configuration value by key.
        
        Args:
            session: Database session
            key (str): Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default if not found
        """
        config = session.query(cls).filter(cls.key == key).first()
        return config.value if config else default
    
    @classmethod
    def set_value(cls, session, key, value, description=None, is_system=False):
        """
        Set configuration value.
        
        Args:
            session: Database session
            key (str): Configuration key
            value: Value to set
            description: Optional description
            is_system: Whether this is a system setting
            
        Returns:
            AppConfig: Updated or created config object
        """
        config = session.query(cls).filter(cls.key == key).first()
        
        if config:
            # Update existing config
            config.value = value
            if description:
                config.description = description
        else:
            # Create new config
            config = cls(
                key=key,
                value=value,
                description=description,
                is_system=is_system
            )
            session.add(config)
            
        session.commit()
        return config