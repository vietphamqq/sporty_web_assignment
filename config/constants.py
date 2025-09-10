"""
Centralized constants for the Sporty Web Assignment Testing Framework

This module contains all framework constants to eliminate duplication
and provide a single source of truth for configuration values.
"""


class TimeoutConstants:
    """Timeout-related constants"""
    
    # Default timeouts (in seconds)
    EXPLICIT_WAIT = 20
    PAGE_LOAD_TIMEOUT = 30
    SCRIPT_TIMEOUT = 30
    
    # Short timeouts for quick checks
    QUICK_WAIT = 5
    ELEMENT_CHECK_TIMEOUT = 3
    
    # Long timeouts for slow operations
    LONG_WAIT = 60
    STREAMER_PAGE_LOAD_TIMEOUT = 15


class BrowserConstants:
    """Browser-related constants"""
    
    # Default browser settings
    DEFAULT_BROWSER = "chrome"
    DEFAULT_DEVICE = "iPhone SE"
    DEFAULT_HEADLESS = False
    
    # Mobile emulation settings
    MOBILE_EMULATION_ENABLED = True
    
    # Chrome-specific settings
    CHROME_IMPLICIT_WAIT = 10
    CHROME_PAGE_LOAD_TIMEOUT = 30
    CHROME_SCRIPT_TIMEOUT = 30


class TestConstants:
    """Test execution constants"""
    
    # Parallel execution
    DEFAULT_MAX_WORKERS = 4
    PARALLEL_EXECUTION_ENABLED = True
    
    # Test data
    DEFAULT_TEST_DATA_SOURCE = "local"


class ReportConstants:
    """Reporting-related constants"""
    
    # Default report settings
    DEFAULT_REPORT_DIR = "reports"
    DEFAULT_LOG_LEVEL = "INFO"
    
    # Report subdirectories
    HTML_REPORT_DIR = "html"
    ALLURE_REPORT_DIR = "allure"
    ALLURE_RESULTS_DIR = "results"
    SCREENSHOTS_DIR = "screenshots"
    LOGS_DIR = "logs"
    
    # Report generation
    HTML_REPORT_ENABLED = True
    ALLURE_REPORT_ENABLED = True
    SCREENSHOT_ON_FAILURE = True


class EnvironmentConstants:
    """Environment-related constants"""
    
    # Environment names
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"
    
    # Environment aliases
    PROD_ALIAS = "prod"
    DEV_ALIAS = "dev"
    
    # Default environment
    DEFAULT_ENVIRONMENT = PRODUCTION


class URLConstants:
    """URL-related constants"""
    
    # Production URLs
    PRODUCTION_BASE_URL = "https://m.twitch.tv"
    
    
    # URL keys for environment configuration
    HOME_URL_KEY = "home"
    SEARCH_URL_KEY = "search"
    BROWSE_URL_KEY = "browse"
    LOGIN_URL_KEY = "login"


class FrameworkConstants:
    """Framework metadata constants"""
    
    # Framework information
    FRAMEWORK_NAME = "Sporty Web Assignment Testing Framework"
    VERSION = "1.0.0"
    AUTHOR = "William Pham"
    
    # Python requirements
    MIN_PYTHON_VERSION = "3.8"
    RECOMMENDED_PYTHON_VERSION = "3.9"
    
    # Dependencies
    REQUIRED_SELENIUM_VERSION = "4.8.0"
    REQUIRED_PYTEST_VERSION = "7.0.0"


class ChromeOptionsConstants:
    """Chrome-specific options constants"""
    
    # Performance and stability options
    CHROME_ARGS = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--disable-extensions",
        "--disable-logging",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding",
        "--disable-features=TranslateUI",
        "--disable-ipc-flooding-protection",
        "--disable-web-security",
        "--disable-features=VizDisplayCompositor",
        "--remote-debugging-port=0",
        "--user-data-dir=/tmp/chrome_dev_test",
        "--disable-infobars",
        "--disable-notifications",
        "--disable-popup-blocking",
        "--disable-default-apps",
    ]
    
    # Mobile emulation options
    MOBILE_EMULATION_ARGS = [
        "--enable-mobile-emulation",
        "--touch-events=enabled",
        "--disable-features=VizDisplayCompositor",
    ]
    
    # Chrome preferences
    CHROME_PREFS = {
        "profile.default_content_setting_values": {
            "notifications": 2,  # Block notifications
            "geolocation": 2,    # Block geolocation
            "camera": 2,         # Block camera
            "microphone": 2,     # Block microphone
        },
        "profile.managed_default_content_settings": {
            "images": 1,         # Allow images
            "plugins": 1,        # Allow plugins
            "popups": 2,         # Block popups
        },
    }


class AllureConstants:
    """Allure reporting constants"""
    
    # Default categories for test classification
    DEFAULT_CATEGORIES = [
        {
            "name": "Test defects",
            "matchedStatuses": ["failed"],
            "messageRegex": ".*AssertionError.*",
        },
        {
            "name": "Product defects", 
            "matchedStatuses": ["failed"],
            "messageRegex": ".*ElementNotFoundException.*",
        },
        {
            "name": "Test infrastructure",
            "matchedStatuses": ["broken", "failed"],
            "messageRegex": ".*DriverException.*",
        },
    ]
    
    # Default labels
    DEFAULT_LABELS = [
        {"name": "framework", "value": FrameworkConstants.FRAMEWORK_NAME},
        {"name": "language", "value": "python"},
        {"name": "package", "value": "sporty_web_assignment"},
    ]


class LoggingConstants:
    """Logging-related constants"""
    
    # Log levels
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    
    # Default log level
    DEFAULT_LOG_LEVEL = INFO
    
    # Log format
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # Log file naming
    LOG_FILE_PATTERN = "{name}_{date}.log"
    LOG_DATE_PATTERN = "%Y%m%d"
