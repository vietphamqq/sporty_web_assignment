"""
Custom exceptions for the Sporty Web Assignment Testing Framework
"""

class SportyFrameworkException(Exception):
    """Base exception for all framework-related errors"""
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            return f"{self.message} - Details: {self.details}"
        return self.message


class DriverException(SportyFrameworkException):
    """Exception raised when there are issues with WebDriver operations"""
    pass


class ElementNotFoundException(SportyFrameworkException):
    """Exception raised when an element cannot be found on the page"""
    def __init__(self, locator, message: str = None, timeout: int = None):
        self.locator = locator
        self.timeout = timeout
        
        if message is None:
            if isinstance(locator, list):
                locator_str = f"Multiple locators: {locator}"
            else:
                locator_str = f"Single locator: {locator}"
            
            timeout_str = f" within {timeout}s" if timeout else ""
            message = f"Element not found with {locator_str}{timeout_str}"
        
        details = {
            "locator": locator,
            "timeout": timeout
        }
        super().__init__(message, details)


class PageNotFoundException(SportyFrameworkException):
    """Exception raised when a page cannot be loaded or found"""
    def __init__(self, url: str, message: str = None, status_code: int = None):
        self.url = url
        self.status_code = status_code
        
        if message is None:
            status_str = f" (Status: {status_code})" if status_code else ""
            message = f"Page not found or failed to load: {url}{status_str}"
        
        details = {
            "url": url,
            "status_code": status_code
        }
        super().__init__(message, details)


class TestDataException(SportyFrameworkException):
    """Exception raised when there are issues with test data"""
    pass


class ConfigurationException(SportyFrameworkException):
    """Exception raised when there are configuration-related issues"""
    pass


class TimeoutException(SportyFrameworkException):
    """Exception raised when operations timeout"""
    def __init__(self, operation: str, timeout: int, message: str = None):
        self.operation = operation
        self.timeout = timeout
        
        if message is None:
            message = f"Operation '{operation}' timed out after {timeout}s"
        
        details = {
            "operation": operation,
            "timeout": timeout
        }
        super().__init__(message, details)


class UnsupportedDeviceException(DriverException):
    """Exception raised when an unsupported mobile device is requested"""
    def __init__(self, device_name: str, supported_devices: list = None):
        self.device_name = device_name
        self.supported_devices = supported_devices or []
        
        if self.supported_devices:
            message = f"Unsupported device '{device_name}'. Supported devices: {', '.join(self.supported_devices)}"
        else:
            message = f"Unsupported device '{device_name}'"
        
        details = {
            "requested_device": device_name,
            "supported_devices": self.supported_devices
        }
        super().__init__(message, details)