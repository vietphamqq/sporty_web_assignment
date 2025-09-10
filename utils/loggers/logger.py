"""
Logging utilities for the Sporty Web Assignment Testing Framework
"""

import logging
import os
from datetime import datetime
from typing import Optional

from config.settings import Settings


class Logger:
    """Centralized logging utility"""

    _loggers = {}
    _log_dir = None

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get or create a logger instance"""
        if name not in cls._loggers:
            cls._loggers[name] = cls._create_logger(name)
        return cls._loggers[name]

    @classmethod
    def _create_logger(cls, name: str) -> logging.Logger:
        """Create a new logger instance"""
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, Settings.REPORT.log_level.upper()))

        # Prevent duplicate handlers
        if logger.handlers:
            return logger

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler
        if cls._log_dir is None:
            cls._log_dir = os.path.join(Settings.REPORT.report_dir, "logs")
            os.makedirs(cls._log_dir, exist_ok=True)

        log_file = os.path.join(
            cls._log_dir, f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    @classmethod
    def setup_test_logger(cls, test_name: str) -> logging.Logger:
        """Setup logger for a specific test"""
        logger = cls.get_logger(f"test_{test_name}")
        logger.info(f"Starting test: {test_name}")
        return logger

    @classmethod
    def log_test_step(
        cls, logger: logging.Logger, step: str, details: Optional[dict] = None
    ):
        """Log a test step with optional details"""
        message = f"STEP: {step}"
        if details:
            message += f" - {details}"
        logger.info(message)

    @classmethod
    def log_assertion(
        cls,
        logger: logging.Logger,
        assertion: str,
        result: bool,
        details: Optional[str] = None,
    ):
        """Log an assertion result"""
        status = "PASS" if result else "FAIL"
        message = f"ASSERTION {status}: {assertion}"
        if details:
            message += f" - {details}"

        if result:
            logger.info(message)
        else:
            logger.error(message)

    @classmethod
    def log_error(cls, logger: logging.Logger, error: Exception, context: str = ""):
        """Log an error with context"""
        message = f"ERROR: {type(error).__name__}: {str(error)}"
        if context:
            message += f" - Context: {context}"
        logger.error(message, exc_info=True)
