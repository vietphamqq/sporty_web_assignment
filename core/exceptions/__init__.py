"""
Custom exceptions for the Sporty Web Assignment Testing Framework
"""

from .framework_exceptions import (
    SportyFrameworkException,
    DriverException,
    ElementNotFoundException,
    PageNotFoundException,
    TestDataException,
    ConfigurationException,
    TimeoutException as SportyTimeoutException
)

__all__ = [
    'SportyFrameworkException',
    'DriverException',
    'ElementNotFoundException',
    'PageNotFoundException',
    'TestDataException',
    'ConfigurationException',
    'SportyTimeoutException'
]
