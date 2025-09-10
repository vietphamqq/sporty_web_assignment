"""
Production environment configuration
"""

from typing import Dict
from .base import BaseEnvironmentConfig
from ..constants import (
    TimeoutConstants,
    TestConstants,
    URLConstants,
)


class ProductionConfig(BaseEnvironmentConfig):
    """Production environment configuration for Twitch testing"""
    
    def __init__(self):
        super().__init__(
            name="production",
            description="Production Twitch environment for assignment testing",
            base_url=URLConstants.PRODUCTION_BASE_URL,
            explicit_wait=TimeoutConstants.EXPLICIT_WAIT,
            page_load_timeout=TimeoutConstants.PAGE_LOAD_TIMEOUT,
            screenshot_on_failure=True,
            headless_mode=False,
            test_data_source=TestConstants.DEFAULT_TEST_DATA_SOURCE
        )
    
    def get_test_urls(self) -> Dict[str, str]:
        """Get production-specific test URLs"""
        return {
            URLConstants.HOME_URL_KEY: f"{self.base_url}/",
            URLConstants.SEARCH_URL_KEY: f"{self.base_url}/search",
            URLConstants.BROWSE_URL_KEY: f"{self.base_url}/directory",
            URLConstants.LOGIN_URL_KEY: f"{self.base_url}/login",
            # Add more URLs as needed for your tests
        }
    
    def get_environment_variables(self) -> Dict[str, str]:
        """Get production-specific environment variables"""
        return {
            "ENV": "production",
            "BASE_URL": self.base_url,
            "EXPLICIT_WAIT": str(self.explicit_wait),
            "PAGE_LOAD_TIMEOUT": str(self.page_load_timeout),
            "SCREENSHOT_ON_FAILURE": str(self.screenshot_on_failure).lower(),
            "TEST_DATA_SOURCE": self.test_data_source
        }
