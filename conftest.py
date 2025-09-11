"""
Pytest configuration file with parallel execution support

This module provides:
- Custom command line options for test configuration
- Fixtures for driver management and test setup
- Hooks for reporting, screenshots, and cleanup
- Parallel execution support with worker management
"""

import os
import subprocess
import threading
import time
from pathlib import Path

import pytest

def pytest_addoption(parser):
    """Add custom command line options to pytest"""

    # Environment options
    parser.addoption(
        "--env",
        action="store",
        default="production",
        help="Environment to run tests against",
        choices=["production", "prod"]
    )

    # Framework options
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode",
    )

    parser.addoption(
        "--test-timeout",
        action="store",
        type=int,
        default=30,
        help="Test timeout in seconds (default: 30)",
    )


    # Reporting options

    parser.addoption(
        "--allure-report",
        action="store_true",
        default=False,
        help="Enable Allure report generation",
    )

    parser.addoption(
        "--open-allure",
        action="store_true",
        default=False,
        help="Automatically open Allure report in browser (requires --allure-report, uses default path if --alluredir not specified)",
    )

    parser.addoption(
        "--screenshot-on-failure",
        action="store_true",
        default=True,
        help="Take screenshot on test failure",
    )


@pytest.fixture(scope="session")
def test_config(request) -> dict:
    """Fixture to get test configuration from command line

    Returns:
        dict: Test configuration dictionary
    """
    return {
        "environment": request.config.getoption("--env"),
        "headless": request.config.getoption("--headless"),
        "timeout": request.config.getoption("--test-timeout"),
        "allure_report": request.config.getoption("--allure-report"),
        "open_allure": request.config.getoption("--open-allure"),
        "screenshot_on_failure": request.config.getoption("--screenshot-on-failure"),
    }


@pytest.fixture(scope="session", autouse=True)
def parallel_session_setup(request):
    """Automatic session-level setup for parallel execution"""
    
    # Set environment from CLI option
    environment = request.config.getoption("--env")
    os.environ["ENV"] = environment
    
    # Initialize environment configuration
    try:
        from config.environment_manager import EnvironmentManager
        env_info = EnvironmentManager.get_environment_info()
        print(f"\n🌍 Environment: {env_info['name']} ({env_info['description']})")
        print(f"🔗 Base URL: {env_info['base_url']}")
    except Exception as e:
        print(f"\n⚠️  Warning: Failed to initialize environment '{environment}': {e}")
        print("   Falling back to default configuration")

    # Check if running in parallel mode
    worker_id = getattr(request.config, "workerinput", {}).get("workerid")
    if worker_id:
        print(f"\n🚀 Worker {worker_id} starting...")
        # Set environment variable for worker identification
        os.environ["PYTEST_XDIST_WORKER"] = worker_id
    else:
        print(f"\n🚀 Single-worker execution starting...")

    yield

    # Cleanup after session
    if worker_id:
        print(f"\n✅ Worker {worker_id} finished")


@pytest.fixture(scope="function")
def driver():
    """Provides a WebDriver instance with selenium-wire for network monitoring

    This fixture ensures complete test isolation in parallel execution
    and handles automatic cleanup. Uses selenium-wire for GraphQL request monitoring.
    """
    from core.driver_manager import DriverManager

    # Get worker-specific driver with selenium-wire support for GraphQL monitoring
    driver = DriverManager.get_mobile_wire_driver()
    print("\n🧪 New WebDriver instance created for test (with selenium-wire for GraphQL monitoring)")

    yield driver

    # Cleanup is handled automatically by DriverManager per worker
    DriverManager.quit_driver()


def pytest_configure(config):
    """Configure pytest with custom settings"""

    # Configure custom markers
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")

    # Set environment from CLI option
    if hasattr(config.option, "env"):
        environment = config.getoption("--env")
        os.environ["ENV"] = environment
        print(f"🌍 Setting environment to: {environment}")

    # Set environment variables based on CLI options - use getattr to safely check if option exists
    if hasattr(config.option, "headless") and config.getoption("--headless"):
        os.environ["HEADLESS"] = "true"

    if hasattr(config.option, "allure_report") and config.getoption("--allure-report"):
        os.environ["ALLURE_REPORT"] = "true"

    if hasattr(config.option, "open_allure") and config.getoption("--open-allure"):
        os.environ["OPEN_ALLURE"] = "true"

        # If --alluredir is not specified, set default
        try:
            allure_dir = config.getoption("--alluredir")
        except ValueError:
            # Set default alluredir when using --open-allure
            default_allure_dir = "reports/allure/results"
            # We can't modify the config option after parsing, but we can ensure the directory exists
            os.makedirs(default_allure_dir, exist_ok=True)

        # Early validation: Check if Allure CLI is available
        try:
            subprocess.run(["allure", "--version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("\n" + "=" * 60)
            print("⚠️  WARNING: Allure CLI not found!")
            print("=" * 60)
            print("You used --open-allure but Allure CLI is not installed.")
            print("The report will be generated, but won't open automatically.")
            print("")
            print("To install Allure CLI:")
            print("  • macOS: brew install allure")
            print("  • npm:   npm install -g allure-commandline")
            print("  • Manual: https://docs.qameta.io/allure/")
            print("")
            print("Or view results manually after tests complete:")
            print("  allure serve reports/allure/results")
            print("=" * 60)
            print("")
        except Exception:
            # If any other error occurs, just continue silently
            pass

    if hasattr(config.option, "screenshot_on_failure") and config.getoption(
        "--screenshot-on-failure"
    ):
        os.environ["SCREENSHOT_ON_FAILURE"] = "true"

    # Set test timeout
    timeout = config.getoption("--test-timeout")
    os.environ["TEST_TIMEOUT"] = str(timeout)


def pytest_report_header(config):
    """Add custom header to pytest report"""
    environment = config.getoption("--env")
    headless = "Yes" if config.getoption("--headless") else "No"
    timeout = config.getoption("--test-timeout")

    # Get environment info if available
    try:
        from config.environment_manager import EnvironmentManager
        env_info = EnvironmentManager.get_environment_info()
        base_url = env_info.get('base_url', 'Unknown')
    except:
        base_url = 'Unknown'

    return [
        f"Environment: {environment}",
        f"Base URL: {base_url}",
        f"Headless Mode: {headless}",
        f"Test Timeout: {timeout}s",
        f"Framework: Sporty Web Assignment Testing Framework",
    ]


def pytest_runtest_makereport(item, call):
    """Hook to capture screenshots on test failure"""
    if call.when == "call" and call.excinfo is not None:
        # Test failed, try to capture screenshot
        try:
            from core.driver_manager import DriverManager

            worker_key = DriverManager._get_worker_key()

            if worker_key in DriverManager._drivers:
                driver = DriverManager._drivers[worker_key]

                # Create screenshots directory
                import os

                screenshot_dir = os.path.join("reports", "screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)

                # Generate screenshot filename
                test_name = item.name.replace("::", "_").replace("/", "_")
                timestamp = str(int(call.start * 1000))  # Use call start time
                screenshot_path = os.path.join(
                    screenshot_dir, f"FAILURE_{test_name}_{timestamp}.png"
                )

                # Take screenshot
                driver.save_screenshot(screenshot_path)
                print(f"\n📸 Screenshot captured on failure: {screenshot_path}")

                # Attach to Allure if available
                try:
                    import allure

                    with open(screenshot_path, "rb") as image_file:
                        allure.attach(
                            image_file.read(),
                            name="Failure Screenshot",
                            attachment_type=allure.attachment_type.PNG,
                        )
                except ImportError:
                    pass  # Allure not available, skip attachment

        except Exception as e:
            print(f"\n⚠️  Failed to capture screenshot on failure: {e}")


def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished, right before returning the exit status to the system"""

    # Clean up all driver instances when session ends
    try:
        from core.driver_manager import DriverManager

        DriverManager.quit_all_drivers()
        print("\n✅ All WebDriver instances cleaned up successfully")
    except Exception as e:
        print(f"\n⚠️  Warning: Error during driver cleanup: {e}")

    config = session.config

    # Check if both --allure-report and --open-allure flags are set
    if (
        hasattr(config.option, "allure_report")
        and config.getoption("--allure-report")
        and hasattr(config.option, "open_allure")
        and config.getoption("--open-allure")
    ):


        # Get the allure results directory
        allure_dir = None
        try:
            allure_dir = config.getoption("--alluredir")
        except ValueError:
            # --alluredir option not available or not set
            pass

        # If no alluredir specified, use default path
        if not allure_dir:
            allure_dir = "reports/allure/results"
            print(f"\n💡 No --alluredir specified, using default: {allure_dir}")

        if allure_dir and Path(allure_dir).exists():
            print(f"🚀 Opening Allure report from: {allure_dir}")

            try:
                # Try to use allure serve command to open the report
                def open_allure_report():
                    try:
                        # Start allure serve in background
                        process = subprocess.Popen(
                            [
                                "allure",
                                "serve",
                                allure_dir,
                                "--port",
                                "0",
                            ],  # port 0 = auto-assign
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                        )

                        # Wait a bit for server to start
                        time.sleep(3)

                        # The allure serve command automatically opens browser
                        print("✅ Allure report opened in browser")

                    except FileNotFoundError:
                        print(
                            "⚠️  Allure CLI not found. The allure-pytest Python package is installed,"
                        )
                        print("   but the Allure CLI tool is missing. Install it with:")
                        print("   • macOS: brew install allure")
                        print("   • npm:   npm install -g allure-commandline")
                        print(f"   Then view results: allure serve {allure_dir}")
                    except Exception as e:
                        print(f"⚠️  Could not open Allure report: {e}")
                        print(f"   View results manually: allure serve {allure_dir}")

                # Run in background thread so it doesn't block test completion
                thread = threading.Thread(target=open_allure_report, daemon=True)
                thread.start()

            except Exception as e:
                print(f"⚠️  Error opening Allure report: {e}")
                print(f"   View results manually: allure serve {allure_dir}")

        else:
            print(f"⚠️  Allure results directory not found: {allure_dir}")
            print("   Make sure tests with --allure-report have been run first")
