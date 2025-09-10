"""
Configuration settings for Sporty Web Assignment Testing Framework
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class BrowserConfig:
    """Browser configuration settings"""
    name: str = "chrome"
    headless: bool = False
    explicit_wait: int = 20
    page_load_timeout: int = 30

@dataclass
class TestConfig:
    """Test execution configuration"""
    parallel_execution: bool = True
    max_workers: int = 4

@dataclass
class ReportConfig:
    """Reporting configuration"""
    html_report: bool = True
    allure_report: bool = True
    report_dir: str = "reports"
    log_level: str = "INFO"

class Settings:
    """Main configuration class for the Sporty Web Assignment Framework"""
    
    # Framework Information
    FRAMEWORK_NAME = "Sporty Web Assignment Testing Framework"
    VERSION = "1.0.0"
    
    # Browser Configuration
    BROWSER = BrowserConfig(
        name=os.getenv("BROWSER", "chrome"),
        headless=os.getenv("HEADLESS", "false").lower() == "true",
        explicit_wait=int(os.getenv("EXPLICIT_WAIT", "20")),
        page_load_timeout=int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    )
    
    # Test Configuration
    TEST = TestConfig(
        parallel_execution=os.getenv("PARALLEL_EXECUTION", "true").lower() == "true",
        max_workers=int(os.getenv("MAX_WORKERS", "4"))
    )
    
    # Reporting Configuration
    REPORT = ReportConfig(
        html_report=os.getenv("HTML_REPORT", "true").lower() == "true",
        allure_report=os.getenv("ALLURE_REPORT", "true").lower() == "true",
        report_dir=os.getenv("REPORT_DIR", "reports"),
        log_level=os.getenv("LOG_LEVEL", "INFO")
    )
    
