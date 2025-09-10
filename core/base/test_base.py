"""
Base test class for all test types
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional

from config.settings import Settings
from utils.loggers.logger import Logger
from utils.reporters.allure_reporter import AllureReporter


class BaseTest(ABC):
    """Base class for all tests providing common setup, teardown, logging, and reporting"""

    def setup_method(self):
        """Setup method called before each test"""
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.start_time = datetime.now()
        self.test_data = {}
        self._setup_reporters()

        self.logger.info(f"Starting test: {self.__class__.__name__}")

        # Setup test data
        self._setup_test_data()

        # Setup test environment
        self._setup_test_environment()

    def _setup_reporters(self):
        """Setup reporting systems"""
        self.allure_reporter = (
            AllureReporter() if Settings.REPORT.allure_report else None
        )

    def teardown_method(self):
        """Teardown method called after each test"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()

        self.logger.info(
            f"Test completed: {self.__class__.__name__} in {duration:.2f}s"
        )

        # Cleanup test environment
        self._cleanup_test_environment()

    @abstractmethod
    def _setup_test_data(self):
        """Setup test-specific data - to be implemented by subclasses"""
        pass

    def _setup_test_environment(self):
        """Setup test-specific environment - can be overridden by subclasses"""
        # Default implementation - subclasses can override if needed
        pass

    def _cleanup_test_environment(self):
        """Cleanup test-specific environment - can be overridden by subclasses"""
        # Default implementation - subclasses can override if needed
        pass

    def add_test_data(self, key: str, value: Any):
        """Add data to test context"""
        self.test_data[key] = value
        self.logger.debug(f"Added test data: {key} = {value}")

    def get_test_data(self, key: str, default: Any = None) -> Any:
        """Get data from test context"""
        return self.test_data.get(key, default)

    def log_test_step(self, step: str, details: Optional[Dict] = None):
        """Log a test step with optional details"""
        message = f"Test Step: {step}"
        if details:
            message += f" - Details: {details}"
        self.logger.info(message)

    def assert_condition(self, condition: bool, message: str):
        """Assert a condition with custom message"""
        if not condition:
            self.logger.error(f"Assertion failed: {message}")
            raise AssertionError(message)
        self.logger.debug(f"Assertion passed: {message}")

    def soft_assert(self, condition: bool, message: str) -> bool:
        """Soft assertion that doesn't stop test execution"""
        if not condition:
            self.logger.warning(f"Soft assertion failed: {message}")
            return False
        self.logger.debug(f"Soft assertion passed: {message}")
        return True
