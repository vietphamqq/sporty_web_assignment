"""
Allure reporting utilities for test results
"""
import os
import json
import shutil
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

from config.settings import Settings

class AllureReporter:
    """Allure report generator for test results"""
    
    def __init__(self):
        self.report_dir = Settings.REPORT.report_dir
        self.allure_dir = os.path.join(self.report_dir, "allure")
        self.results_dir = os.path.join(self.allure_dir, "results")
        
        # Ensure directories exist
        os.makedirs(self.results_dir, exist_ok=True)
    
    def start_test_suite(self, suite_name: str = "Test Suite"):
        """Start a new test suite"""
        self.suite_name = suite_name
        self.suite_start_time = datetime.now()
    
    def add_test_result(self, test_name: str, status: str, duration: float,
                       error_message: str = None, screenshot_path: str = None,
                       steps: List[Dict[str, Any]] = None, attachments: List[str] = None,
                       labels: List[Dict[str, str]] = None, parameters: List[Dict[str, str]] = None):
        """Add a test result to Allure report"""
        
        # Generate unique test UUID
        test_uuid = str(uuid.uuid4())
        
        # Create Allure result structure
        allure_result = {
            "uuid": test_uuid,
            "name": test_name,
            "status": self._map_status_to_allure(status),
            "stage": "finished",
            "start": int(self.suite_start_time.timestamp() * 1000),
            "stop": int((self.suite_start_time.timestamp() + duration) * 1000),
            "fullName": f"{self.suite_name}.{test_name}",
            "labels": self._create_labels(test_name, labels),
            "parameters": parameters or [],
            "steps": self._create_steps(steps or []),
            "attachments": self._create_attachments(attachments or [], screenshot_path),
            "statusDetails": self._create_status_details(status, error_message)
        }
        
        # Write result to file
        result_file = os.path.join(self.results_dir, f"{test_uuid}-result.json")
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(allure_result, f, indent=2)
    
    def _map_status_to_allure(self, status: str) -> str:
        """Map test status to Allure status"""
        status_mapping = {
            "PASSED": "passed",
            "FAILED": "failed",
            "SKIPPED": "skipped",
            "BROKEN": "broken"
        }
        return status_mapping.get(status.upper(), "unknown")
    
    def _create_labels(self, test_name: str, custom_labels: List[Dict[str, str]] = None) -> List[Dict[str, str]]:
        """Create Allure labels"""
        labels = [
            {"name": "suite", "value": self.suite_name},
            {"name": "testClass", "value": test_name},
            {"name": "framework", "value": "Sporty Web Assignment Testing Framework"},
            {"name": "language", "value": "python"},
            {"name": "package", "value": "sporty_web_assignment"}
        ]
        
        if custom_labels:
            labels.extend(custom_labels)
        
        return labels
    
    def _create_steps(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create Allure test steps"""
        allure_steps = []
        
        for i, step in enumerate(steps):
            allure_step = {
                "name": step.get("name", f"Step {i+1}"),
                "status": self._map_status_to_allure(step.get("status", "PASSED")),
                "stage": "finished",
                "start": int(step.get("start_time", 0) * 1000),
                "stop": int(step.get("end_time", 0) * 1000),
                "attachments": step.get("attachments", [])
            }
            allure_steps.append(allure_step)
        
        return allure_steps
    
    def _create_attachments(self, attachments: List[str], screenshot_path: str = None) -> List[Dict[str, str]]:
        """Create Allure attachments"""
        allure_attachments = []
        
        # Add screenshot if provided
        if screenshot_path and os.path.exists(screenshot_path):
            attachment_name = os.path.basename(screenshot_path)
            allure_attachments.append({
                "name": attachment_name,
                "source": attachment_name,
                "type": "image/png"
            })
        
        # Add other attachments
        for attachment in attachments:
            if os.path.exists(attachment):
                attachment_name = os.path.basename(attachment)
                file_extension = os.path.splitext(attachment)[1].lower()
                mime_type = self._get_mime_type(file_extension)
                
                allure_attachments.append({
                    "name": attachment_name,
                    "source": attachment_name,
                    "type": mime_type
                })
        
        return allure_attachments
    
    def _get_mime_type(self, file_extension: str) -> str:
        """Get MIME type for file extension"""
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.txt': 'text/plain',
            '.json': 'application/json',
            '.xml': 'application/xml',
            '.html': 'text/html',
            '.csv': 'text/csv'
        }
        return mime_types.get(file_extension, 'application/octet-stream')
    
    def _create_status_details(self, status: str, error_message: str = None) -> Dict[str, Any]:
        """Create Allure status details"""
        if status.upper() == "FAILED" and error_message:
            return {
                "message": error_message,
                "trace": error_message
            }
        elif status.upper() == "SKIPPED":
            return {
                "message": "Test was skipped",
                "trace": None
            }
        else:
            return {}
    
    def copy_attachments(self, attachments: List[str], screenshot_path: str = None):
        """Copy attachment files to Allure results directory"""
        for attachment in attachments:
            if os.path.exists(attachment):
                filename = os.path.basename(attachment)
                dest_path = os.path.join(self.results_dir, filename)
                
                shutil.copy2(attachment, dest_path)
        
        # Copy screenshot if provided
        if screenshot_path and os.path.exists(screenshot_path):
            filename = os.path.basename(screenshot_path)
            dest_path = os.path.join(self.results_dir, filename)
            
            shutil.copy2(screenshot_path, dest_path)
    
    def generate_environment_properties(self, properties: Dict[str, str] = None):
        """Generate environment.properties file for Allure"""
        default_properties = {
            "Framework": "Sporty Web Assignment Testing Framework",
            "Version": "1.0.0",
            "Python": "3.8+",
            "Browser": Settings.BROWSER.name,
            "Headless": str(Settings.BROWSER.headless),
            "Parallel": str(Settings.TEST.parallel_execution),
            "Max Workers": str(Settings.TEST.max_workers)
        }
        
        if properties:
            default_properties.update(properties)
        
        env_file = os.path.join(self.results_dir, "environment.properties")
        with open(env_file, 'w', encoding='utf-8') as f:
            for key, value in default_properties.items():
                f.write(f"{key}={value}\n")
    
    def generate_categories(self, categories: List[Dict[str, Any]] = None):
        """Generate categories.json file for Allure"""
        default_categories = [
            {
                "name": "Test defects",
                "matchedStatuses": ["failed"],
                "messageRegex": ".*AssertionError.*"
            },
            {
                "name": "Product defects",
                "matchedStatuses": ["failed"],
                "messageRegex": ".*ElementNotFoundException.*"
            },
            {
                "name": "Test infrastructure",
                "matchedStatuses": ["broken", "failed"],
                "messageRegex": ".*DriverException.*"
            }
        ]
        
        if categories:
            default_categories.extend(categories)
        
        categories_file = os.path.join(self.results_dir, "categories.json")
        with open(categories_file, 'w', encoding='utf-8') as f:
            json.dump(default_categories, f, indent=2)
    
    def generate_executor_info(self, executor_info: Dict[str, Any] = None):
        """Generate executor.json file for Allure"""
        default_executor = {
            "name": "Sporty Web Assignment Test Runner",
            "type": "local",
            "url": "local",
            "buildOrder": 1,
            "buildName": f"Build {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "buildUrl": "local",
            "reportUrl": "local",
            "reportName": "Sporty Web Assignment Test Report"
        }
        
        if executor_info:
            default_executor.update(executor_info)
        
        executor_file = os.path.join(self.results_dir, "executor.json")
        with open(executor_file, 'w', encoding='utf-8') as f:
            json.dump(default_executor, f, indent=2)
    
    def finalize_report(self):
        """Finalize Allure report generation"""
        # Generate additional Allure files
        self.generate_environment_properties()
        self.generate_categories()
        self.generate_executor_info()
        
        print(f"Allure results generated in: {self.results_dir}")
        print("To generate Allure report, run: allure generate allure-results --clean -o allure-report")
        print("To open Allure report, run: allure open allure-report")
