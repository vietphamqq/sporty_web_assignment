"""
Driver Manager - Thread-safe implementation for parallel execution
"""

import os
import threading
from typing import Dict, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from core.exceptions.framework_exceptions import DriverException


class DriverManager:
    """Thread-safe manager for creating WebDriver instances using Chrome's built-in device emulation"""

    # Thread-safe storage for multiple driver instances
    _drivers: Dict[str, webdriver.Chrome] = {}
    _devices: Dict[str, str] = {}
    _lock = threading.Lock()

    # Class-level configuration
    _default_device = "iPhone SE"

    @classmethod
    def get_mobile_driver(
        cls, worker_id: Optional[str] = None, device: Optional[str] = None
    ) -> webdriver.Chrome:
        """Get or create a thread-safe mobile WebDriver instance

        Args:
            worker_id: Optional worker ID for parallel execution (auto-detected if None)
            device: Device to emulate (defaults to iPhone SE)

        Returns:
            webdriver.Chrome: Chrome WebDriver instance with mobile emulation

        Raises:
            DriverException: If driver creation fails
        """
        # Generate unique identifier for this worker/thread
        worker_key = cls._get_worker_key(worker_id)
        device_name = device or cls._default_device

        with cls._lock:
            try:
                # Check if driver already exists for this worker
                if worker_key not in cls._drivers:
                    cls._devices[worker_key] = device_name
                    cls._drivers[worker_key] = cls._create_mobile_driver(device_name)

                return cls._drivers[worker_key]

            except Exception as e:
                # Clean up failed driver creation
                cls._cleanup_worker(worker_key)
                raise DriverException(
                    f"Failed to create mobile driver for worker '{worker_key}': {str(e)}",
                    {"worker_id": worker_key, "device": device_name, "error": str(e)},
                )

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
    def _create_mobile_driver(cls, device_name: str) -> webdriver.Chrome:
        """Create a new mobile WebDriver instance with Chrome mobile emulation

        Args:
            device_name: Name of the device to emulate

        Returns:
            webdriver.Chrome: Configured Chrome WebDriver instance

        Raises:
            DriverException: If driver creation fails
        """
        try:
            chrome_options = ChromeOptions()

            # Use Chrome's built-in device emulation
            mobile_emulation = {"deviceName": device_name}
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

            # Check for headless mode from pytest configuration
            if os.getenv("HEADLESS", "false").lower() == "true":
                chrome_options.add_argument("--headless")
                # chrome_options.add_argument("--window-size=1920,1080")  # Set window size for headless

            # Chrome-specific mobile emulation options
            chrome_options.add_argument("--enable-mobile-emulation")
            chrome_options.add_argument("--touch-events=enabled")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")

            # Performance and stability options for parallel execution
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-logging")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-features=TranslateUI")
            chrome_options.add_argument("--disable-ipc-flooding-protection")

            # Additional parallel execution optimizations
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument(
                "--remote-debugging-port=0"
            )  # Auto-assign debug port
            chrome_options.add_argument(
                "--user-data-dir=/tmp/chrome_dev_test"
            )  # Separate user data

            # Reduce overlays and consent prompts
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-default-apps")

            # Mobile-specific preferences
            prefs = {
                "profile.default_content_setting_values": {
                    "notifications": 2,  # Block notifications
                    "geolocation": 2,  # Block geolocation
                    "camera": 2,  # Block camera
                    "microphone": 2,  # Block microphone
                },
                "profile.managed_default_content_settings": {
                    "images": 1,  # Allow images
                    "plugins": 1,  # Allow plugins
                    "popups": 2,  # Block popups
                },
            }
            chrome_options.add_experimental_option("prefs", prefs)

            # Create driver with Chrome mobile emulation
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # Configure timeouts for mobile
            driver.implicitly_wait(10)
            driver.set_page_load_timeout(30)
            driver.set_script_timeout(30)

            return driver

        except Exception as e:
            raise DriverException(
                f"Failed to create mobile WebDriver for device '{device_name}'",
                {"device": device_name, "error": str(e)},
            )

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
                    f"Warning: Error quitting mobile driver for worker '{worker_key}': {e}"
                )
            finally:
                cls._drivers.pop(worker_key, None)
                cls._devices.pop(worker_key, None)

    @classmethod
    def get_current_device(cls, worker_id: Optional[str] = None) -> Optional[str]:
        """Get the current device for a specific worker

        Args:
            worker_id: Optional worker ID (auto-detected if None)

        Returns:
            str: Device name or None if no driver exists
        """
        worker_key = cls._get_worker_key(worker_id)
        return cls._devices.get(worker_key)

    @classmethod
    def get_active_workers(cls) -> Dict[str, str]:
        """Get all active workers and their devices

        Returns:
            Dict[str, str]: Mapping of worker_key to device_name
        """
        with cls._lock:
            return cls._devices.copy()
