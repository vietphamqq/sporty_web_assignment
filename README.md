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
│   └── settings.py               # Framework configuration
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
# Run all tests (iPhone SE emulation)
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run in headless mode
python -m pytest tests/ --headless
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

### Performance Comparison

| Execution Mode | Time (1 test) | Time (4 tests) | Efficiency |
|----------------|---------------|----------------|------------|
| **Sequential** | 9.6s | ~38.4s | 1x |
| **Parallel (n=2)** | 9.6s | ~19.2s | 2x |
| **Parallel (n=4)** | 9.6s | ~9.6s | 4x |
| **Parallel (n=auto)** | 9.6s | ~9.6s | N-core scaling |

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
- **Code Quality Checks**: Black, isort, flake8, mypy
- **Security Scanning**: Safety and Bandit security analysis
- **Smart Notifications**: Success/failure notifications

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

#### **Factory Pattern**
- **Driver Management**: Showcases centralized WebDriver creation and management
- **Configuration**: Demonstrates consistent setup across environments
- **Resource Management**: Implements proper cleanup and lifecycle management
- **Extensibility**: Architecture allows easy addition of new browser types

#### **Template Method Pattern**
- **Test Lifecycle**: Demonstrates consistent setup/teardown methodology
- **Customization**: Shows how subclasses can override specific behaviors
- **Code Reuse**: Implements common functionality in base classes


## 📚 Examples

### Basic Test Example

```python
from core.base.test_base import TestBase
from core.mobile_driver_manager import DriverManager
from pages.twitch_home_page import TwitchHomePage

class TestExample(TestBase):
    def _setup_test_data(self):
        self.search_term = "Starcraft II"
    
    def _setup_test_environment(self):
        self.driver = DriverManager.get_mobile_driver()
        self.home_page = TwitchHomePage(self.driver)
    
    def _cleanup_test_environment(self):
        DriverManager.quit_driver()
    
    def test_homepage_navigation(self):
        self.home_page.navigate_to_home()
        assert "twitch.tv" in self.driver.current_url
```

### Custom Page Object Example

```python
from core.base.base_page import BasePage
from core.exceptions.framework_exceptions import ElementNotFoundException

class CustomPage(BasePage):
    # Locators with fallbacks
    SEARCH_BUTTON = [
        ("css", "[data-test-selector='search-button']"),
        ("xpath", "//button[contains(text(), 'Search')]"),
        ("id", "search-btn")
    ]
    
    def click_search_button(self):
        try:
            element = self.find_element(self.SEARCH_BUTTON)
            element.click()
            return True
        except ElementNotFoundException:
            self.logger.error("Search button not found")
            return False
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
