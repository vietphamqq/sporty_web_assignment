# Sporty Web Assignment - Automation Testing Framework

[![CI/CD Pipeline](https://github.com/vietphamqq/sporty_web_assignment/actions/workflows/ci.yml/badge.svg)](https://github.com/vietphamqq/sporty_web_assignment/actions/workflows/ci.yml)

A demonstration of modern web automation testing capabilities built as part of a technical assignment. This framework showcases **parallel execution**, mobile emulation, comprehensive reporting, and CI/CD integration using Python and Selenium.

**Author**: William Pham

## 🚀 Technical Capabilities Demonstrated

- **🚀 Parallel Test Execution**: Showcases multi-threaded test running with worker isolation
- **📱 Mobile Testing**: Implements Chrome mobile emulation for responsive testing
- **🏗️ Clean Architecture**: Demonstrates Page Object Model (POM) and design patterns
- **🛡️ Error Handling**: Custom exception framework with 8 specialized exception types
- **📊 Test Reporting**: Allure reports with visual outputs and screenshots
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
├── reports/                      # Test reports and artifacts
│   ├── allure/                   # Allure reports
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

```bash
# Basic test execution
python -m pytest tests/ --headless

# With Allure reporting
python -m pytest tests/ --headless --allure-report --open-allure

# Available options:
--env ENV                    # Environment (production, prod)
--headless                   # Run in headless mode
--test-timeout TIMEOUT       # Test timeout in seconds
--allure-report              # Enable Allure report generation
--open-allure                # Auto-open Allure report
--screenshot-on-failure      # Take screenshot on failure
```

## 🚀 Parallel Execution

The framework supports parallel test execution with thread-safe driver management:

```bash
# Run tests in parallel (auto-detect CPU cores)
python -m pytest tests/ -n auto --headless

# Use specific number of workers
python -m pytest tests/ -n 4 --headless
```

**Features:**
- **Thread-Safe Design**: Per-worker WebDriver instances with complete test isolation
- **Automatic Cleanup**: Zero memory leaks with proper resource management
- **Worker Detection**: Automatic pytest-xdist integration

## 🔄 CI/CD Integration

### GitHub Actions Workflow

The framework includes a comprehensive CI/CD pipeline:

#### **CI/CD Pipeline** (`.github/workflows/ci.yml`)

**Features:**
- **Python 3.9 Testing**: Consistent testing environment
- **Automated Browser Setup**: Chrome installation and configuration
- **Comprehensive Reporting**: Allure reports, screenshots, and logs
- **Artifact Management**: 30-day retention for all test artifacts
- **GitHub Pages Deployment**: Automatic Allure report publishing

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual trigger via GitHub UI

#### **Allure Reports on GitHub Pages**
Test reports are automatically deployed to: `https://vietphamqq.github.io/sporty_web_assignment/{run_number}/`

### Setting Up CI/CD

1. **Enable GitHub Actions** in your repository settings
2. **Configure GitHub Pages** for Allure reports:
   - Go to **Repository Settings** → **Pages**
   - Under **Source**, select **GitHub Actions**
   - Go to **Settings** → **Actions** → **General**
   - Under **Workflow permissions**, select **Read and write permissions**
3. **Push to main branch** - Reports will be automatically deployed
   - Allure reports will be available at: `https://vietphamqq.github.io/sporty_web_assignment/{run_number}/`

**Optional:**
- **Repository Secrets**: No secrets required for basic functionality
- **Custom Domain**: Add CNAME record if you have a custom domain

### Viewing CI/CD Results

- **📊 Test Results**: Actions tab → Workflow run → Summary
- **📁 Artifacts**: Download reports, screenshots, logs from Actions
- **🌐 Live Allure Reports**: GitHub Pages URL (if configured)
- **📱 Status Badges**: README badges show current build status

## 🌍 Environment Configuration

The framework supports multiple environments with flexible configuration:

**Supported Environments:**
- **Production**: Live Twitch environment (default) - https://m.twitch.tv
- **Mobile Testing**: iPhone SE emulation for responsive testing

**Usage:**
```bash
# Production environment (default)
python -m pytest tests/ --env production

# Production with alias
python -m pytest tests/ --env prod
```

**Features:**
- **Environment Manager**: Centralized configuration management
- **Automatic URL Resolution**: Environment-based URL generation
- **Mobile Emulation**: iPhone SE with 375x667 resolution

## 📱 Mobile Testing

The framework is optimized for **iPhone SE** emulation:
- **Screen Resolution**: 375x667 pixels
- **User Agent**: iPhone SE mobile browser
- **Touch Events**: Mobile-optimized interactions
- **Performance**: Fast test execution

## 🛡️ Exception Handling

The framework includes specialized exception classes for better error handling:

- **`DriverException`**: WebDriver creation and management errors
- **`ElementNotFoundException`**: Element location failures with context
- **`PageNotFoundException`**: Page loading timeout errors
- **`TestDataException`**: Test data related errors
- **`ConfigurationException`**: Configuration and settings errors
- **`TimeoutException`**: Operation timeout errors
- **`UnsupportedDeviceException`**: Unsupported device errors

Each exception provides detailed context and actionable error messages.

## 📊 Reporting

**Allure Reports:**
- Professional UI with timeline view
- Screenshots, logs, and test attachments
- GitHub Pages integration for automatic deployment

**Logging:**
- Structured logs with step-by-step tracking
- Color-coded output for local development
- Rich error context and debugging information

## 🔧 Configuration

**Environment Variables:**
```bash
ENV=production                   # Environment to use
HEADLESS=true                    # Headless mode
EXPLICIT_WAIT=20                 # Element wait timeout
PAGE_LOAD_TIMEOUT=30             # Page load timeout
ALLURE_REPORT=true              # Allure report generation
```

**Configuration File:**
Edit `config/settings.py` for persistent configuration changes.

## 🧩 Architecture & Design Patterns

**Page Object Model (POM):**
- Clean separation of UI logic from test logic
- Maintainable and reusable page objects
- Natural, readable test code

**Abstract Factory Pattern:**
- Thread-safe WebDriver creation and management
- Extensible architecture for multiple browser types
- Proper resource management and cleanup

**Template Method Pattern:**
- Consistent test lifecycle management
- Reusable base classes with customizable behaviors


## 📚 Example

### Basic Test Example

```python
from core.base.test_base import BaseTest
from core.driver_manager import DriverManager
from pages.twitch_home_page import TwitchHomePage


class TestExample(BaseTest):
    """Basic test example using the framework"""

    def _prepare_test_data(self):
        """Setup test data"""
        self.search_term = "Starcraft II"
        self.test_data["search_term"] = self.search_term

    def test_homepage_navigation(self, driver):
        """Test: Verify homepage navigation works correctly"""
        # Initialize the home page
        self.home_page = TwitchHomePage(driver)
        
        self.log_test_step("Starting homepage navigation test")

        # Navigate to home page
        self.home_page.navigate_to_home()

        # Verify we're on the correct page
        current_url = driver.current_url
        assert "twitch.tv" in current_url, f"Expected twitch.tv in URL, got: {current_url}"

        self.log_test_step("Homepage navigation test completed successfully")
```

## 🆘 Troubleshooting

**Common Issues:**

```bash
# Update Chrome driver
pip install --upgrade webdriver-manager

# Force headless mode
python -m pytest tests/ --headless -v

# Install Allure CLI (macOS)
brew install allure

# Manual report generation
allure serve reports/allure/results
```

**Getting Help:**
- 📖 Documentation: This README and inline docstrings
- 🐛 Issues: GitHub Issues for bug reports

## 🙏 Technologies & Tools Utilized

- **Selenium WebDriver**: Core automation engine for browser interactions
- **Pytest Framework**: Testing framework with excellent plugin ecosystem
- **Allure Reporting**: Professional test reporting and visualization
- **GitHub Actions**: CI/CD pipeline automation and deployment

---

**Technical Assignment - Web Automation Testing Framework**
