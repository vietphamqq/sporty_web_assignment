"""
Base test class for all test types
"""

from datetime import datetime
from re import S
from typing import Optional, Dict

from utils.loggers.logger import Logger


class BaseTest:
    """Base class for all tests providing common setup, teardown, and logging"""

    def setup_method(self):
        """Setup method called before each test"""
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.start_time = datetime.now()
        self.test_data = {}

        self.logger.info(f"Starting test: {self.__class__.__name__}")
        # Setup test data
        self.logger.info("Preparing test data")
        self._prepare_test_data()

    def _prepare_test_data(self):
        """Prepare test data"""
        pass

    def teardown_method(self):
        """Teardown method called after each test"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()

        self.logger.info(
            f"Test completed: {self.__class__.__name__} in {duration:.2f}s"
        )

    def log_test_step(self, step: str, details: Optional[Dict] = None):
        """Log a test step with optional details"""
        message = f"Test Step: {step}"
        if details:
            message += f" - Details: {details}"
        self.logger.info(message)
