"""
Environment Manager for handling different environment configurations
"""

import os
from typing import Dict, Type, Optional

from .environments.base import BaseEnvironmentConfig
from .environments.production import ProductionConfig


class EnvironmentManager:
    """Manager class for handling environment configurations"""
    
    # Registry of available environments
    _environments: Dict[str, Type[BaseEnvironmentConfig]] = {
        "production": ProductionConfig,
        "prod": ProductionConfig,  # Alias
    }
    
    _current_environment: Optional[BaseEnvironmentConfig] = None
    _default_environment = "production"
    
    @classmethod
    def get_environment(cls, env_name: str = None) -> BaseEnvironmentConfig:
        """Get environment configuration
        
        Args:
            env_name: Name of the environment (production, staging, development)
                     If None, uses ENV environment variable or default
        
        Returns:
            BaseEnvironmentConfig: Environment configuration instance
            
        Raises:
            ValueError: If environment name is not supported
        """
        if env_name is None:
            env_name = os.getenv("ENV", cls._default_environment)
        
        env_name = env_name.lower().strip()
        
        if env_name not in cls._environments:
            available_envs = list(cls._environments.keys())
            raise ValueError(
                f"Unsupported environment: '{env_name}'. "
                f"Available environments: {available_envs}"
            )
        
        # Create and cache environment configuration
        if cls._current_environment is None or cls._current_environment.name != env_name:
            env_class = cls._environments[env_name]
            cls._current_environment = env_class()
            
            # Set environment variables
            cls._set_environment_variables(cls._current_environment)
        
        return cls._current_environment
    
    @classmethod
    def _set_environment_variables(cls, env_config: BaseEnvironmentConfig) -> None:
        """Set environment variables from configuration
        
        Args:
            env_config: Environment configuration instance
        """
        env_vars = env_config.get_environment_variables()
        for key, value in env_vars.items():
            os.environ[key] = value
    
    @classmethod
    def get_current_environment(cls) -> Optional[BaseEnvironmentConfig]:
        """Get the current active environment configuration
        
        Returns:
            BaseEnvironmentConfig: Current environment configuration or None
        """
        return cls._current_environment
    
    @classmethod
    def list_available_environments(cls) -> list:
        """List all available environment names
        
        Returns:
            list: List of available environment names
        """
        return list(cls._environments.keys())
    
    @classmethod
    def register_environment(cls, name: str, env_class: Type[BaseEnvironmentConfig]) -> None:
        """Register a new environment configuration
        
        Args:
            name: Environment name
            env_class: Environment configuration class
        """
        cls._environments[name.lower()] = env_class
    
    @classmethod
    def validate_environment(cls, env_name: str = None) -> bool:
        """Validate if environment configuration is valid
        
        Args:
            env_name: Environment name to validate
            
        Returns:
            bool: True if environment is valid, False otherwise
        """
        try:
            env_config = cls.get_environment(env_name)
            return env_config.validate_environment()
        except (ValueError, Exception):
            return False
    
    @classmethod
    def get_test_url(cls, url_key: str, env_name: str = None) -> str:
        """Get a specific test URL from current environment
        
        Args:
            url_key: Key for the URL (e.g., 'home', 'search', 'login')
            env_name: Environment name (optional)
            
        Returns:
            str: URL for the specified key
            
        Raises:
            KeyError: If URL key is not found in environment configuration
        """
        env_config = cls.get_environment(env_name)
        test_urls = env_config.get_test_urls()
        
        if url_key not in test_urls:
            available_keys = list(test_urls.keys())
            raise KeyError(
                f"URL key '{url_key}' not found in {env_config.name} environment. "
                f"Available keys: {available_keys}"
            )
        
        return test_urls[url_key]
    
    @classmethod
    def reset(cls) -> None:
        """Reset environment manager state"""
        cls._current_environment = None
    
    @classmethod
    def get_environment_info(cls, env_name: str = None) -> Dict[str, str]:
        """Get environment information for logging/reporting
        
        Args:
            env_name: Environment name (optional)
            
        Returns:
            Dict[str, str]: Environment information
        """
        env_config = cls.get_environment(env_name)
        return {
            "name": env_config.name,
            "description": env_config.description,
            "base_url": env_config.base_url,
            "explicit_wait": str(env_config.explicit_wait),
            "page_load_timeout": str(env_config.page_load_timeout),
            "test_data_source": env_config.test_data_source
        }
