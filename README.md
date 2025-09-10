# Sporty Web Assignment - Automation Testing Framework

[![CI/CD Pipeline](https://github.com/vietphamqq/sporty_web_assignment/actions/workflows/ci.yml/badge.svg)](https://github.com/vietphamqq/sporty_web_assignment/actions/workflows/ci.yml)

A demonstration of modern web automation testing capabilities built as part of a technical assignment. This framework showcases **parallel execution**, mobile emulation, comprehensive reporting, and CI/CD integration using Python and Selenium.

**Author**: William Pham

## 🚀 Technical Capabilities Demonstrated

- **🚀 Parallel Test Execution**: Showcases multi-threaded test running with worker isolation
- **📱 Mobile Testing**: Implements Chrome mobile emulation for responsive testing
- **🏗️ Clean Architecture**: Demonstrates Page Object Model (POM) and design patterns
- **🛡️ Error Handling**: Custom exception framework with 8 specialized exception types
- **📊 Test Reporting**: Multiple report formats (HTML & Allure) with visual outputs
- **🔄 CI/CD Integration**: Complete GitHub Actions pipeline implementation
- **⚡ Thread-Safe Design**: Proper resource management and test isolation
- **🧪 Cross-Environment Support**: Headless and GUI modes for different environments
- **📝 Structured Logging**: Comprehensive logging with test step tracking
- **🔧 Configuration Management**: Flexible CLI options and environment-based settings

## 📁 Project Structure

```
sporty_web_assignment/
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI/CD pipeline
├── core/
│   ├── base/
│   │   ├── base_page.py          # Base page class with flexible locators
│   │   └── test_base.py          # Base test class with lifecycle management
│   ├── exceptions/
│   │   └── framework_exceptions.py # Custom exception classes
│   └── driver_manager.py         # Thread-safe WebDriver factory
├── pages/                        # Page Object Model classes
│   ├── twitch_home_page.py       # Twitch home page
│   ├── twitch_search_page.py     # Twitch search page
│   └── twitch_streamer_page.py   # Twitch streamer page
├── config/
│   ├── constants.py              # Centralized framework constants
│   ├── environment_manager.py    # Environment management logic
│   ├── environments/
│   │   ├── base.py              # Base environment configuration
│   │   └── production.py        # Production environment settings
│   └── settings.py              # Main framework configuration
├── tests/                        # Test suites
│   └── test_twitch.py            # Twitch end-to-end test
├── utils/                        # Utility functions
│   ├── loggers/
│   │   └── logger.py             # Logging configuration
│   └── reporters/
│       ├── allure_reporter.py    # Allure reporting utilities
│       └── html_reporter.py      # HTML reporting utilities
├── reports/                      # Test reports and artifacts
│   ├── allure/                   # Allure reports
│   ├── html/                     # HTML reports
│   ├── logs/                     # Test logs
│   └── screenshots/              # Test screenshots
├── conftest.py                   # Pytest configuration and CLI options
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🛠️ Installation

### Prerequisites

- **Python 3.8 or higher**
- **Chrome browser** (automatically managed in CI/CD)
- **Git** (for repository operations)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sporty_web_assignment
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -m pytest --version
   ```

### Optional: Allure CLI (for local report viewing)

```bash
# macOS
brew install allure

# npm (cross-platform)
npm install -g allure-commandline

# Verify installation
allure --version
```

## 🧪 Running Tests

### Test Execution Demo

![Test Run Demo](twitch.gif)

*Live demonstration of the test framework running locally*

### Basic Test Execution

```bash
# Run all tests (iPhone SE emulation, production environment)
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run in headless mode
python -m pytest tests/ --headless

# Run against production environment (default)
python -m pytest tests/ --env production
```

### Command Line Options

The framework provides comprehensive CLI options for flexible test execution:

#### **Environment Options**
```bash
--env ENV                    # Environment to run tests against
                             # Choices: production, prod (default: production)
```

#### **Browser Options**
```bash
--headless                   # Run tests in headless mode (default: false)
```

#### **Timing Options**
```bash
--test-timeout TIMEOUT       # Test timeout in seconds (default: 30)
```

#### **Reporting Options**
```bash
--html-report                # Enable HTML report generation
--allure-report              # Enable Allure report generation
--open-allure                # Automatically open Allure report in browser
                             # (requires --allure-report and Allure CLI)
--screenshot-on-failure      # Take screenshot on test failure (default: true)
```

#### **Advanced Usage Examples**

```bash
# Complete test run with all options
python -m pytest tests/ \
  --env production \
  --headless \
  --test-timeout 60 \
  --html-report \
  --allure-report \
  --open-allure \
  --screenshot-on-failure

# Minimal test run
python -m pytest tests/ --headless

# Debug mode with verbose output
python -m pytest tests/ -v -s --test-timeout 120
```

### With Reporting

```bash
# HTML report only
python -m pytest tests/ --html-report --html reports/html/test_report.html --self-contained-html

# Allure report only
python -m pytest tests/ --allure-report --alluredir reports/allure/results

# Both reports with auto-open Allure
python -m pytest tests/ --html-report --allure-report --open-allure

# Complete test run with all features
python -m pytest tests/ --headless --html-report --allure-report --open-allure -v

# Production environment with all features
python -m pytest tests/ --env production --headless --allure-report --open-allure
```

### Advanced Options

```bash
# Specific test method
python -m pytest tests/test_twitch.py::TestTwitch::test_twitch_search_and_navigate_to_streamer -v

# With custom Allure directory
python -m pytest tests/ --allure-report --alluredir custom/allure/path

# Timeout configuration
python -m pytest tests/ --timeout=60
```

## 🚀 Parallel Execution Implementation

This assignment demonstrates **parallel test execution** capabilities with complete test isolation and thread-safe driver management.

### Quick Start with Parallel Execution

```bash
# Auto-detect CPU cores and run tests in parallel
python -m pytest tests/ -n auto --headless

# Use specific number of workers
python -m pytest tests/ -n 4 --headless

# Parallel execution with Allure reporting
python -m pytest tests/ -n auto --headless --allure-report --open-allure
```

### Distribution Strategies

```bash
# Load balancing (default) - distributes tests evenly
python -m pytest tests/ -n 4 --dist load

# Work stealing - workers steal work from others when idle (recommended)
python -m pytest tests/ -n 4 --dist worksteal

# Each test runs on all workers - for cross-environment testing
python -m pytest tests/ -n 4 --dist each
```

### Thread-Safe Architecture Implementation

This implementation showcases a custom `DriverManager` design with:

- **Per-worker WebDriver instances** - Complete test isolation
- **Thread-safe resource management** - No race conditions
- **Automatic cleanup** - Zero memory leaks
- **Worker detection** - Automatic pytest-xdist integration

```python
# Thread-safe driver management
class DriverManager:
    _drivers: Dict[str, webdriver.Chrome] = {}  # Worker-specific drivers
    _lock = threading.Lock()                    # Thread synchronization
    
    @classmethod
    def get_mobile_driver(cls, worker_id: Optional[str] = None):
        # Automatically detects worker and provides isolated driver
```

### Environment Variables for Parallel Execution

```bash
# Enable parallel execution optimizations
export HEADLESS=true                    # Faster execution
export PARALLEL_EXECUTION=true          # Framework awareness
export MAX_WORKERS=4                    # Worker limit

# Run tests
python -m pytest tests/ -n auto
```

## 🔄 CI/CD Integration

### GitHub Actions Workflow

The framework includes a comprehensive CI/CD pipeline:

#### **CI/CD Pipeline** (`.github/workflows/ci.yml`)

**Features:**
- **Python 3.9 Testing**: Consistent testing environment
- **Automated Browser Setup**: Chrome installation and configuration
- **Comprehensive Reporting**: HTML, Allure, screenshots, and logs
- **Artifact Management**: 30-day retention for all test artifacts
- **GitHub Pages Deployment**: Automatic Allure report publishing

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual trigger via GitHub UI

#### **Allure Reports on GitHub Pages**
Test reports are automatically deployed to: `https://vietphamqq.github.io/sporty_web_assignment/{run_number}/index.html`

### Setting Up CI/CD

1. **Enable GitHub Actions** in your repository settings
2. **Configure GitHub Pages** for Allure reports:
   - Go to **Repository Settings** → **Pages**
   - Under **Source**, select **GitHub Actions**
   - Go to **Settings** → **Actions** → **General**
   - Under **Workflow permissions**, select **Read and write permissions**
3. **Push to main branch** - Reports will be automatically deployed
   - Allure reports will be available at: `https://vietphamqq.github.io/sporty_web_assignment/{run_number}/index.html`

**Optional:**
- **Repository Secrets**: No secrets required for basic functionality
- **Custom Domain**: Add CNAME record if you have a custom domain

### Viewing CI/CD Results

- **📊 Test Results**: Actions tab → Workflow run → Summary
- **📁 Artifacts**: Download reports, screenshots, logs from Actions
- **🌐 Live Allure Reports**: GitHub Pages URL (if configured)
- **📱 Status Badges**: README badges show current build status

## 🌍 Environment Configuration

### Environment Configuration System

The framework features a comprehensive **environment management system** that supports multiple environments with inheritance and flexible configuration:

#### **Supported Environments**
- **Production**: Live Twitch production environment (default)
- **Base URL**: https://m.twitch.tv
- **Mobile Testing**: iPhone SE emulation for responsive testing

#### **Environment Manager Architecture**

The framework uses an **Environment Manager** pattern with:
- **Base Environment Class**: Abstract base for all environments
- **Environment-Specific Configurations**: Production, staging, development
- **Centralized Management**: Single point of control for environment switching
- **Automatic URL Resolution**: Environment-based URL generation

#### **Usage Examples**

```bash
# Production environment (default)
python -m pytest tests/ --env production

# Production with alias
python -m pytest tests/ --env prod

# Production with all features
python -m pytest tests/ --env production --headless --allure-report --open-allure
```

#### **Environment Configuration Structure**

```
config/
├── constants.py              # Centralized constants for all environments
├── environments/
│   ├── base.py              # Abstract base environment configuration
│   └── production.py        # Production-specific settings
├── environment_manager.py    # Environment management and switching logic
└── settings.py              # Main configuration with environment integration
```

#### **Production Environment Features**

- **Base URL**: https://m.twitch.tv
- **Explicit Wait**: 20 seconds
- **Page Load Timeout**: 30 seconds
- **Test Data Source**: Local
- **Mobile Emulation**: iPhone SE
- **Screenshot on Failure**: Enabled

#### **Environment Variables**

The production environment automatically sets these variables:

```python
# Production Environment Configuration
{
    "ENV": "production",
    "BASE_URL": "https://m.twitch.tv",
    "EXPLICIT_WAIT": "20",
    "PAGE_LOAD_TIMEOUT": "30",
    "SCREENSHOT_ON_FAILURE": "true",
    "TEST_DATA_SOURCE": "local"
}
```

#### **Adding New Environments**

To add a new environment (e.g., staging):

1. **Create Environment Class**:
```python
# config/environments/staging.py
from .base import BaseEnvironmentConfig

class StagingConfig(BaseEnvironmentConfig):
    def __init__(self):
        super().__init__(
            name="staging",
            description="Staging environment for testing",
            base_url="https://staging.twitch.tv",
            explicit_wait=15,  # Different timeout for staging
        )
```

2. **Register Environment**:
```python
# config/environment_manager.py
_environments: Dict[str, Type[BaseEnvironmentConfig]] = {
    "production": ProductionConfig,
    "staging": StagingConfig,  # Add new environment
    "prod": ProductionConfig,  # Alias
}
```

3. **Use New Environment**:
```bash
python -m pytest tests/ --env staging
```

## 📱 Mobile Testing

### Current Configuration

The framework is optimized for **iPhone SE** emulation, providing:
- **Screen Resolution**: 375x667 pixels
- **User Agent**: iPhone SE mobile browser
- **Touch Events**: Mobile-optimized interactions
- **Viewport**: Mobile-responsive testing

### Why iPhone SE?

- **Widely Used**: Represents a significant portion of mobile users
- **Compact Size**: Tests responsiveness on smaller screens
- **Consistent**: Reliable testing environment
- **Performance**: Fast test execution

## 🛡️ Exception Handling

### Custom Exception Classes

The framework includes 8 specialized exception classes:

- **`MobileDriverException`**: WebDriver creation and management errors
- **`ElementNotFoundException`**: Element location failures with context
- **`PageLoadException`**: Page loading timeout errors
- **`NavigationException`**: Navigation and URL errors
- **`ScreenshotException`**: Screenshot capture failures
- **`ConfigurationException`**: Configuration and settings errors
- **`TestDataException`**: Test data validation errors
- **`ReportGenerationException`**: Reporting system errors

Each exception provides:
- **Detailed Context**: Specific error information
- **Actionable Messages**: Clear guidance for resolution
- **Stack Traces**: Full debugging information

## 📊 Reporting

### HTML Reports

- **Self-Contained**: Single file with embedded CSS/JS
- **Rich Content**: Screenshots, logs, metadata
- **Interactive**: Expandable sections, filtering
- **CI/CD Ready**: Artifact upload and download

### Allure Reports

- **Professional UI**: Modern, interactive interface
- **Timeline View**: Test execution timeline
- **Attachments**: Screenshots, logs, videos
- **History**: Trend analysis across builds
- **GitHub Pages**: Automatic deployment

### Logging

- **Structured Logs**: JSON-compatible format
- **Color Coding**: Local development visualization
- **Test Steps**: Detailed step-by-step tracking
- **Error Context**: Rich error information

## 🔧 Configuration

### Environment Variables

```bash
# Environment Configuration
ENV=production                   # Environment to use

# Browser Configuration
BROWSER=chrome                    # Browser type (default: chrome)
HEADLESS=true                    # Headless mode (default: false)
EXPLICIT_WAIT=20                 # Element wait timeout (default: 20)
PAGE_LOAD_TIMEOUT=30             # Page load timeout (default: 30)

# Test Configuration
PARALLEL_EXECUTION=true          # Parallel test execution (default: true)
MAX_WORKERS=4                    # Number of parallel workers (default: 4)

# Reporting Configuration
HTML_REPORT=true                 # HTML report generation (default: true)
ALLURE_REPORT=true              # Allure report generation (default: true)
REPORT_DIR=reports              # Report directory (default: reports)
LOG_LEVEL=INFO                  # Logging level (default: INFO)
```

### Configuration File

Edit `config/settings.py` for persistent configuration changes:

```python
class Settings:
    # Framework Information
    FRAMEWORK_NAME = "Sporty Web Assignment Testing Framework"
    VERSION = "1.0.0"
    
    # Browser Configuration
    BROWSER = BrowserConfig(
        name="chrome",
        headless=False,
        explicit_wait=20,
        page_load_timeout=30
    )
    
    # Additional configurations...
```

## 🧩 Architecture & Design Patterns

This assignment demonstrates several key software engineering patterns:

### Design Patterns Implemented

#### **Page Object Model (POM)**
- **Separation of Concerns**: Demonstrates clean separation of UI logic from test logic
- **Maintainability**: Shows how page changes don't affect other components
- **Reusability**: Page objects designed for cross-test reuse
- **Readability**: Tests written in natural, readable language

#### **Abstract Factory Pattern**
- **Multi-Browser Support**: Extensible architecture for different browser types
- **Driver Management**: Thread-safe WebDriver creation and management
- **Configuration**: Consistent setup across environments and browsers
- **Resource Management**: Proper cleanup and lifecycle management
- **Future Extensibility**: Easy addition of Firefox, Safari, Edge support

#### **Template Method Pattern**
- **Test Lifecycle**: Demonstrates consistent setup/teardown methodology
- **Customization**: Shows how subclasses can override specific behaviors
- **Code Reuse**: Implements common functionality in base classes

### Multi-Browser Architecture

The framework uses an **Abstract Factory Pattern** for browser extensibility:

```python
# Current implementation (Chrome only for assignment)
driver = DriverManager.get_mobile_driver()  # Returns Chrome by default

# Future multi-browser support (ready for extension)
chrome_driver = DriverManager.get_mobile_driver(browser=BrowserType.CHROME)
firefox_driver = DriverManager.get_mobile_driver(browser=BrowserType.FIREFOX)  # Future
safari_driver = DriverManager.get_mobile_driver(browser=BrowserType.SAFARI)    # Future
```

**Benefits:**
- **Zero Breaking Changes**: Current tests work unchanged
- **Clean Extension**: Add new browsers without modifying existing code  
- **Thread-Safe**: Maintains parallel execution capabilities
- **Configuration-Driven**: Browser selection through environment variables


## 📚 Examples

### Basic Test Example

```python
from core.base.test_base import TestBase
from core.driver_manager import DriverManager
from core.exceptions.framework_exceptions import DriverException
from pages.twitch_home_page import TwitchHomePage
from config.constants import TimeoutConstants


class TestExample(TestBase):
    """Basic test example using the framework"""

    def _setup_test_data(self):
        """Setup test data"""
        self.search_term = "Starcraft II"
        self.expected_url = "twitch.tv"

    def _setup_test_environment(self):
        """Setup WebDriver and page objects using DriverManager"""
        try:
            # Get thread-safe mobile driver instance
            self.driver = DriverManager.get_mobile_driver()

            # Initialize page objects
            self.home_page = TwitchHomePage(self.driver)

        except DriverException as e:
            self.logger.error(f"Failed to setup test environment: {e}")
            raise

    def _cleanup_test_environment(self):
        """Cleanup WebDriver instance"""
        # DriverManager handles thread-safe cleanup
        DriverManager.quit_driver()

    def test_homepage_navigation(self):
        """Test: Verify homepage navigation works correctly"""
        self.log_test_step("Starting homepage navigation test")

        # Navigate to home page using environment-configured URL
        self.home_page.navigate_to_home()

        # Verify navigation
        current_url = self.driver.current_url
        assert self.expected_url in current_url, \
            f"Expected '{self.expected_url}' in URL, got: {current_url}"

        # Verify page loaded correctly
        page_loaded = self.home_page.is_page_loaded_correctly()
        assert page_loaded, "Home page did not load correctly"

        self.log_test_step("Homepage navigation test completed successfully")
```

### Page Object with Environment Integration

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from core.base.base_page import BasePage
from core.exceptions.framework_exceptions import ElementNotFoundException
from config.constants import TimeoutConstants, URLConstants


class CustomPage(BasePage):
    """Custom page object with environment-aware URL configuration"""

    # Robust locators with multiple strategies
    SEARCH_BUTTON = [
        ("css", "[data-test-selector='search-button']"),
        ("xpath", "//button[contains(text(), 'Search')]"),
        ("id", "search-btn")
    ]

    SEARCH_INPUT = [
        ("css", "input[type='search']"),
        ("xpath", "//input[@type='search']"),
        ("name", "search")
    ]

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        # Get URL from environment configuration
        from config.settings import Settings
        self.url = Settings.get_test_url(URLConstants.SEARCH_URL_KEY)

    def navigate_to_page(self) -> None:
        """Navigate to page using environment-configured URL"""
        self.navigate_to(self.url)
        self.wait_for_page_load()

    def perform_search(self, search_term: str) -> bool:
        """Perform search with robust error handling"""
        try:
            self.log_test_step(f"Searching for: {search_term}")

            # Enter search term
            search_input_success = self.enter_text(
                self.SEARCH_INPUT,
                search_term,
                timeout=TimeoutConstants.EXPLICIT_WAIT
            )

            if not search_input_success:
                self.logger.error("Failed to enter search term")
                return False

            # Click search button with fallback to Enter key
            button_clicked = self.click_element(
                self.SEARCH_BUTTON,
                timeout=TimeoutConstants.EXPLICIT_WAIT
            )

            if not button_clicked:
                # Fallback: press Enter key
                from selenium.webdriver.common.keys import Keys
                self.send_keys_to_element(
                    self.SEARCH_INPUT,
                    Keys.RETURN,
                    timeout=TimeoutConstants.QUICK_WAIT
                )

            return True

        except ElementNotFoundException as e:
            self.logger.error(f"Search failed: {e}")
            return False

    def is_page_loaded_correctly(self) -> bool:
        """Verify page loaded correctly"""
        try:
            return (
                self.is_element_present(self.SEARCH_INPUT, timeout=TimeoutConstants.QUICK_WAIT) and
                self.is_element_present(self.SEARCH_BUTTON, timeout=TimeoutConstants.QUICK_WAIT)
            )
        except Exception:
            return False
```

### Environment-Aware Test Example

```python
from core.base.test_base import TestBase
from core.driver_manager import DriverManager
from core.exceptions.framework_exceptions import DriverException
from pages.twitch_home_page import TwitchHomePage
from config.constants import TimeoutConstants


class TestEnvironmentAware(TestBase):
    """Test example demonstrating environment configuration usage"""

    def _setup_test_data(self):
        """Setup test data"""
        # Get environment-specific configuration
        from config.settings import Settings
        env_info = Settings.get_environment_info()

        self.base_url = env_info['base_url']
        self.explicit_wait = int(env_info['explicit_wait'])
        self.test_search_term = "gaming"

    def _setup_test_environment(self):
        """Setup with environment-aware configuration"""
        try:
            # DriverManager automatically uses environment settings
            self.driver = DriverManager.get_mobile_driver()
            self.home_page = TwitchHomePage(self.driver)

        except DriverException as e:
            self.logger.error(f"Environment setup failed: {e}")
            raise

    def _cleanup_test_environment(self):
        """Cleanup"""
        DriverManager.quit_driver()

    def test_environment_integration(self):
        """Test: Verify environment configuration is properly integrated"""
        self.log_test_step("Testing environment integration")

        # Navigate using environment URL
        self.home_page.navigate_to_home()

        # Verify environment URL is used
        current_url = self.driver.current_url
        assert self.base_url in current_url, \
            f"Expected environment URL '{self.base_url}' in current URL: {current_url}"

        # Test respects environment timeouts
        # (The framework automatically uses environment-specific timeouts)
        page_loaded = self.home_page.is_page_loaded_correctly()
        assert page_loaded, "Page should load within environment timeout"

        self.log_test_step("Environment integration test passed")
```

## 🧪 Creating New Tests

### Basic Test Structure

Create test files in the `tests/` directory following this pattern:

```python
# tests/test_example.py
"""
Example Test - Template for new test classes
"""

from core.base.test_base import TestBase
from core.driver_manager import DriverManager
from core.exceptions.framework_exceptions import DriverException
from pages.twitch_home_page import TwitchHomePage


class TestExample(TestBase):
    """Test class for Example page functionality"""

    def _setup_test_data(self):
        """Setup test data for the example test"""
        self.search_term = "Starcraft II"

    def _setup_test_environment(self):
        """Setup WebDriver and page objects"""
        try:
            # Setup WebDriver using DriverManager
            self.driver = DriverManager.get_mobile_driver()

            # Initialize page objects
            self.home_page = TwitchHomePage(self.driver)

        except DriverException as e:
            self.logger.error(f"Failed to setup test environment: {e}")
            raise

    def _cleanup_test_environment(self):
        """Cleanup WebDriver instance"""
        DriverManager.quit_driver()

    def test_homepage_navigation(self):
        """Test: Verify homepage navigation works correctly"""
        self.log_test_step("Starting homepage navigation test")

        # Navigate to home page
        self.home_page.navigate_to_home()

        # Verify we're on the correct page
        current_url = self.driver.current_url
        assert "twitch.tv" in current_url, f"Expected twitch.tv in URL, got: {current_url}"

        self.log_test_step("Homepage navigation test completed successfully")
```

## 🆘 Troubleshooting

### Common Issues

#### **Chrome Driver Issues**
```bash
# Update Chrome driver
pip install --upgrade webdriver-manager

# Manual Chrome installation (CI/CD)
apt-get update && apt-get install -y google-chrome-stable
```

#### **Headless Mode Not Working**
```bash
# Verify environment variable
echo $HEADLESS

# Force headless mode
python -m pytest tests/ --headless -v
```

#### **Allure Reports Not Opening**
```bash
# Install Allure CLI
brew install allure  # macOS
npm install -g allure-commandline  # npm

# Manual report generation
allure serve reports/allure/results
```

#### **Permission Issues**
```bash
# Fix permissions
chmod +x venv/bin/activate
chmod -R 755 reports/
```

### Getting Help

- **📖 Documentation**: This README and inline docstrings
- **🐛 Issues**: GitHub Issues for bug reports
- **💬 Discussions**: GitHub Discussions for questions

## 🙏 Technologies & Tools Utilized

- **Selenium WebDriver**: Core automation engine for browser interactions
- **Pytest Framework**: Testing framework with excellent plugin ecosystem
- **Allure Reporting**: Professional test reporting and visualization
- **GitHub Actions**: CI/CD pipeline automation and deployment

---

**Technical Assignment - Web Automation Testing Framework**
