"""
Base environment configuration class
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any

from ..constants import (
    TimeoutConstants,
    TestConstants,
    ReportConstants,
    URLConstants,
)


@dataclass
class BaseEnvironmentConfig(ABC):
    """Base configuration class for all environments"""
    
    # Environment identification
    name: str
    description: str
    
    # URLs and endpoints
    base_url: str
    
    # Timeouts (environment-specific adjustments)
    explicit_wait: int = TimeoutConstants.EXPLICIT_WAIT
    page_load_timeout: int = TimeoutConstants.PAGE_LOAD_TIMEOUT
    
    # Environment-specific test settings
    screenshot_on_failure: bool = ReportConstants.SCREENSHOT_ON_FAILURE
    
    # Environment-specific browser settings
    headless_mode: bool = False
    
    # Test data settings
    test_data_source: str = TestConstants.DEFAULT_TEST_DATA_SOURCE
    
    @abstractmethod
    def get_test_urls(self) -> Dict[str, str]:
        """Get environment-specific test URLs"""
        pass
    
    @abstractmethod
    def get_environment_variables(self) -> Dict[str, str]:
        """Get environment-specific variables to set"""
        pass
    
    def get_browser_options(self) -> Dict[str, Any]:
        """Get environment-specific browser options"""
        return {
            "headless": self.headless_mode,
            "explicit_wait": self.explicit_wait,
            "page_load_timeout": self.page_load_timeout
        }
    
    def validate_environment(self) -> bool:
        """Validate if environment is properly configured"""
        return bool(self.base_url and self.name)
