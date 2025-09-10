"""
Configuration settings for Sporty Web Assignment Testing Framework
"""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from .constants import (
    TimeoutConstants,
    BrowserConstants,
    TestConstants,
    ReportConstants,
    FrameworkConstants,
)

# Load environment variables
load_dotenv()


@dataclass
class BrowserConfig:
    """Browser configuration settings"""

    name: str = BrowserConstants.DEFAULT_BROWSER
    headless: bool = BrowserConstants.DEFAULT_HEADLESS
    explicit_wait: int = TimeoutConstants.EXPLICIT_WAIT
    page_load_timeout: int = TimeoutConstants.PAGE_LOAD_TIMEOUT
    mobile_emulation: bool = BrowserConstants.MOBILE_EMULATION_ENABLED
    device: str = BrowserConstants.DEFAULT_DEVICE


@dataclass
class TestConfig:
    """Test execution configuration"""

    parallel_execution: bool = TestConstants.PARALLEL_EXECUTION_ENABLED
    max_workers: int = TestConstants.DEFAULT_MAX_WORKERS


@dataclass
class ReportConfig:
    """Reporting configuration"""

    allure_report: bool = ReportConstants.ALLURE_REPORT_ENABLED
    report_dir: str = ReportConstants.DEFAULT_REPORT_DIR
    log_level: str = ReportConstants.DEFAULT_LOG_LEVEL


class Settings:
    """Main configuration class for the Sporty Web Assignment Framework"""

    # Framework Information
    FRAMEWORK_NAME = FrameworkConstants.FRAMEWORK_NAME
    VERSION = FrameworkConstants.VERSION
    
    # Environment Configuration
    _environment_config: Optional[object] = None

    @classmethod
    def get_environment_config(cls):
        """Get current environment configuration"""
        if cls._environment_config is None:
            from .environment_manager import EnvironmentManager
            cls._environment_config = EnvironmentManager.get_environment()
        return cls._environment_config

    @classmethod
    def get_browser_config(cls) -> BrowserConfig:
        """Get browser configuration with environment overrides"""
        env_config = cls.get_environment_config()
        browser_options = env_config.get_browser_options()
        
        return BrowserConfig(
            name=os.getenv("BROWSER", "chrome"),
            headless=os.getenv("HEADLESS", str(browser_options.get("headless", "false"))).lower() == "true",
            explicit_wait=int(os.getenv("EXPLICIT_WAIT", str(browser_options.get("explicit_wait", 20)))),
            page_load_timeout=int(os.getenv("PAGE_LOAD_TIMEOUT", str(browser_options.get("page_load_timeout", 30)))),
            mobile_emulation=os.getenv("MOBILE_EMULATION", "true").lower() == "true",
            device=os.getenv("DEVICE", "iPhone SE"),
        )

    @classmethod
    def get_test_config(cls) -> TestConfig:
        """Get test configuration with environment overrides"""
        env_config = cls.get_environment_config()
        
        return TestConfig(
            parallel_execution=os.getenv("PARALLEL_EXECUTION", "true").lower() == "true",
            max_workers=int(os.getenv("MAX_WORKERS", "4")),
        )

    @classmethod
    def get_report_config(cls) -> ReportConfig:
        """Get report configuration with environment overrides"""
        return ReportConfig(
            allure_report=os.getenv("ALLURE_REPORT", "true").lower() == "true",
            report_dir=os.getenv("REPORT_DIR", "reports"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )

    # Legacy class properties for backward compatibility
    # These will be dynamically set to maintain compatibility
    BROWSER: BrowserConfig = None
    TEST: TestConfig = None 
    REPORT: ReportConfig = None
    
    @classmethod
    def _initialize_legacy_properties(cls):
        """Initialize legacy properties for backward compatibility"""
        cls.BROWSER = cls.get_browser_config()
        cls.TEST = cls.get_test_config()
        cls.REPORT = cls.get_report_config()
    
    @classmethod
    def get_base_url(cls) -> str:
        """Get base URL from current environment"""
        env_config = cls.get_environment_config()
        return env_config.base_url
    
    @classmethod
    def get_test_url(cls, url_key: str) -> str:
        """Get specific test URL from current environment
        
        Args:
            url_key: Key for the URL (e.g., 'home', 'search', 'login')
            
        Returns:
            str: URL for the specified key
        """
        from .environment_manager import EnvironmentManager
        return EnvironmentManager.get_test_url(url_key)
    
    @classmethod
    def get_environment_info(cls) -> dict:
        """Get current environment information"""
        from .environment_manager import EnvironmentManager
        return EnvironmentManager.get_environment_info()


# Initialize legacy properties for backward compatibility
Settings._initialize_legacy_properties()
