"""
Driver Manager - Thread-safe implementation for parallel execution with multi-browser support
"""

import os
import threading
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Union

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from core.exceptions.framework_exceptions import DriverException
from config.constants import (
    BrowserConstants,
    TimeoutConstants,
    ChromeOptionsConstants,
)


class BrowserType(Enum):
    """Supported browser types for future extensibility"""
    CHROME = "chrome"
    # FIREFOX = "firefox"    # Future support
    # SAFARI = "safari"      # Future support  
    # EDGE = "edge"          # Future support


class BrowserFactory(ABC):
    """Abstract factory for creating browser-specific WebDriver instances"""
    
    @abstractmethod
    def create_mobile_driver(self, device: str) -> webdriver.Remote:
        """Create a mobile WebDriver instance for the specific browser"""
        pass
    
    @abstractmethod
    def create_desktop_driver(self) -> webdriver.Remote:
        """Create a desktop WebDriver instance for the specific browser"""
        pass


class ChromeDriverFactory(BrowserFactory):
    """Factory for creating Chrome WebDriver instances"""
    
    def create_mobile_driver(self, device: str) -> webdriver.Chrome:
        """Create a Chrome mobile WebDriver instance with device emulation"""
        return self._create_chrome_mobile_driver(device)
    
    def create_desktop_driver(self) -> webdriver.Chrome:
        """Create a Chrome desktop WebDriver instance"""
        # Future implementation for desktop Chrome
        raise NotImplementedError("Desktop Chrome driver not implemented yet")
    
    def _create_chrome_mobile_driver(self, device_name: str) -> webdriver.Chrome:
        """Create Chrome mobile driver with device emulation - existing implementation"""
        try:
            chrome_options = ChromeOptions()

            # Use Chrome's built-in device emulation
            mobile_emulation = {"deviceName": device_name}
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

            # Check for headless mode from pytest configuration
            if os.getenv("HEADLESS", "false").lower() == "true":
                chrome_options.add_argument("--headless")

            # Add Chrome arguments from constants
            for arg in ChromeOptionsConstants.CHROME_ARGS:
                chrome_options.add_argument(arg)
            
            for arg in ChromeOptionsConstants.MOBILE_EMULATION_ARGS:
                chrome_options.add_argument(arg)

            # Mobile-specific preferences from constants
            chrome_options.add_experimental_option("prefs", ChromeOptionsConstants.CHROME_PREFS)

            # Create driver with Chrome mobile emulation
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # Configure timeouts for mobile from constants
            driver.implicitly_wait(BrowserConstants.CHROME_IMPLICIT_WAIT)
            driver.set_page_load_timeout(BrowserConstants.CHROME_PAGE_LOAD_TIMEOUT)
            driver.set_script_timeout(BrowserConstants.CHROME_SCRIPT_TIMEOUT)

            return driver

        except Exception as e:
            raise DriverException(
                f"Failed to create mobile WebDriver for device '{device_name}'",
                {"device": device_name, "error": str(e)},
            )


# Future browser factories
# class FirefoxDriverFactory(BrowserFactory):
#     """Factory for creating Firefox WebDriver instances"""
#     
#     def create_mobile_driver(self, device: str) -> webdriver.Firefox:
#         """Create Firefox mobile driver with responsive design testing"""
#         # Future implementation:
#         # - Use Firefox's responsive design mode
#         # - Configure user agent for mobile
#         # - Set viewport dimensions
#         pass
#     
#     def create_desktop_driver(self) -> webdriver.Firefox:
#         """Create Firefox desktop driver"""
#         pass

# class SafariDriverFactory(BrowserFactory):
#     """Factory for creating Safari WebDriver instances"""
#     
#     def create_mobile_driver(self, device: str) -> webdriver.Safari:
#         """Create Safari mobile driver (iOS Simulator)"""
#         # Future implementation:
#         # - Integrate with iOS Simulator
#         # - Configure mobile Safari settings
#         pass
#     
#     def create_desktop_driver(self) -> webdriver.Safari:
#         """Create Safari desktop driver"""
#         pass


class DriverManager:
    """Thread-safe manager for creating WebDriver instances with multi-browser support"""

    # Thread-safe storage for multiple driver instances (now supports any WebDriver type)
    _drivers: Dict[str, webdriver.Remote] = {}
    _browser_configs: Dict[str, Dict] = {}
    _lock = threading.Lock()

    # Browser factory registry
    _browser_factories = {
        BrowserType.CHROME: ChromeDriverFactory(),
        # BrowserType.FIREFOX: FirefoxDriverFactory(),  # Future support
        # BrowserType.SAFARI: SafariDriverFactory(),    # Future support
        # BrowserType.EDGE: EdgeDriverFactory(),        # Future support
    }

    # Default configuration
    _default_browser = BrowserType.CHROME
    _default_device = BrowserConstants.DEFAULT_DEVICE

    @classmethod
    def get_mobile_driver(
        cls, 
        worker_id: Optional[str] = None, 
        device: Optional[str] = None,
        browser: BrowserType = None
    ) -> webdriver.Remote:
        """Get or create a thread-safe mobile WebDriver instance

        Args:
            worker_id: Optional worker ID for parallel execution (auto-detected if None)
            device: Device to emulate (defaults to iPhone SE)
            browser: Browser type to use (defaults to Chrome)

        Returns:
            webdriver.Remote: WebDriver instance with mobile emulation

        Raises:
            DriverException: If driver creation fails
        """
        # Use default browser (Chrome) 
        browser_type = browser or cls._default_browser
        device_name = device or cls._default_device
        worker_key = cls._get_worker_key(worker_id)

        with cls._lock:
            try:
                # Check if driver already exists for this worker
                if worker_key not in cls._drivers:
                    # Store configuration for this worker
                    cls._browser_configs[worker_key] = {
                        "browser": browser_type,
                        "device": device_name,
                        "mobile": True
                    }
                    
                    # Create driver using appropriate factory
                    factory = cls._get_browser_factory(browser_type)
                    cls._drivers[worker_key] = factory.create_mobile_driver(device_name)

                return cls._drivers[worker_key]

            except Exception as e:
                # Clean up failed driver creation
                cls._cleanup_worker(worker_key)
                raise DriverException(
                    f"Failed to create mobile driver for worker '{worker_key}': {str(e)}",
                    {"worker_id": worker_key, "browser": browser_type.value, "device": device_name, "error": str(e)},
                )

    @classmethod
    def get_desktop_driver(
        cls,
        worker_id: Optional[str] = None,
        browser: BrowserType = None
    ) -> webdriver.Remote:
        """Get or create a thread-safe desktop WebDriver instance
        
        Args:
            worker_id: Optional worker ID for parallel execution (auto-detected if None)
            browser: Browser type to use (defaults to Chrome)
            
        Returns:
            webdriver.Remote: Desktop WebDriver instance
            
        Raises:
            DriverException: If driver creation fails
        """
        # Future implementation - placeholder for assignment
        browser_type = browser or cls._default_browser
        worker_key = cls._get_worker_key(worker_id)
        
        # For assignment: only Chrome mobile is implemented
        raise NotImplementedError(
            f"Desktop {browser_type.value} driver not implemented yet. "
            "Assignment focuses on mobile Chrome testing."
        )

    @classmethod
    def _get_browser_factory(cls, browser_type: BrowserType) -> BrowserFactory:
        """Get the appropriate factory for the browser type
        
        Args:
            browser_type: Type of browser to get factory for
            
        Returns:
            BrowserFactory: Factory instance for the browser
            
        Raises:
            DriverException: If browser type is not supported
        """
        if browser_type not in cls._browser_factories:
            supported_browsers = [bt.value for bt in cls._browser_factories.keys()]
            raise DriverException(
                f"Unsupported browser type: {browser_type.value}",
                {
                    "requested_browser": browser_type.value,
                    "supported_browsers": supported_browsers
                }
            )
        
        return cls._browser_factories[browser_type]

    @classmethod
    def _get_worker_key(cls, worker_id: Optional[str] = None) -> str:
        """Generate unique worker key for thread-safe driver management

        Args:
            worker_id: Optional explicit worker ID

        Returns:
            str: Unique worker identifier
        """
        if worker_id:
            return f"worker_{worker_id}"

        # Use thread ID for local parallel execution
        thread_id = threading.current_thread().ident

        # Check if running under pytest-xdist
        try:
            import os

            if "PYTEST_XDIST_WORKER" in os.environ:
                return f"xdist_{os.environ['PYTEST_XDIST_WORKER']}"
        except:
            pass

        return f"thread_{thread_id}"


    @classmethod
    def quit_driver(cls, worker_id: Optional[str] = None) -> None:
        """Quit a specific worker's mobile WebDriver instance

        Args:
            worker_id: Optional worker ID (auto-detected if None)
        """
        worker_key = cls._get_worker_key(worker_id)
        cls._cleanup_worker(worker_key)

    @classmethod
    def quit_all_drivers(cls) -> None:
        """Quit all mobile WebDriver instances (cleanup for test session end)"""
        with cls._lock:
            worker_keys = list(cls._drivers.keys())
            for worker_key in worker_keys:
                cls._cleanup_worker(worker_key)

    @classmethod
    def _cleanup_worker(cls, worker_key: str) -> None:
        """Internal method to cleanup a specific worker's resources

        Args:
            worker_key: Worker identifier to cleanup
        """
        if worker_key in cls._drivers:
            try:
                cls._drivers[worker_key].quit()
            except Exception as e:
                # Log warning but don't raise exception during cleanup
                print(
                    f"Warning: Error quitting driver for worker '{worker_key}': {e}"
                )
            finally:
                cls._drivers.pop(worker_key, None)
                cls._browser_configs.pop(worker_key, None)

    @classmethod
    def get_current_device(cls, worker_id: Optional[str] = None) -> Optional[str]:
        """Get the current device for a specific worker

        Args:
            worker_id: Optional worker ID (auto-detected if None)

        Returns:
            str: Device name or None if no driver exists
        """
        worker_key = cls._get_worker_key(worker_id)
        config = cls._browser_configs.get(worker_key, {})
        return config.get("device")

    @classmethod
    def get_current_browser(cls, worker_id: Optional[str] = None) -> Optional[BrowserType]:
        """Get the current browser type for a specific worker

        Args:
            worker_id: Optional worker ID (auto-detected if None)

        Returns:
            BrowserType: Browser type or None if no driver exists
        """
        worker_key = cls._get_worker_key(worker_id)
        config = cls._browser_configs.get(worker_key, {})
        return config.get("browser")

    @classmethod
    def get_active_workers(cls) -> Dict[str, Dict]:
        """Get all active workers and their configurations

        Returns:
            Dict[str, Dict]: Mapping of worker_key to worker configuration
        """
        with cls._lock:
            return cls._browser_configs.copy()

    @classmethod
    def add_browser_support(cls, browser_type: BrowserType, factory: BrowserFactory) -> None:
        """Add support for a new browser type (future extensibility)
        
        Args:
            browser_type: Type of browser to add support for
            factory: Factory instance for creating the browser drivers
        """
        cls._browser_factories[browser_type] = factory

    @classmethod
    def get_supported_browsers(cls) -> List[str]:
        """Get list of currently supported browser types
        
        Returns:
            List[str]: List of supported browser names
        """
        return [browser.value for browser in cls._browser_factories.keys()]
