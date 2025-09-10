"""
HTML reporting utilities for test results
"""
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

from config.settings import Settings

class HTMLReporter:
    """HTML report generator for test results"""
    
    def __init__(self):
        self.report_dir = Settings.REPORT.report_dir
        self.html_dir = os.path.join(self.report_dir, "html")
        self.test_results = []
        self.start_time = None
        self.end_time = None
        
        # Ensure report directory exists
        os.makedirs(self.html_dir, exist_ok=True)
    
    def start_test_suite(self, suite_name: str = "Test Suite"):
        """Start a new test suite"""
        self.start_time = datetime.now()
        self.test_results = []
        self.suite_name = suite_name
    
    def add_test_result(self, test_name: str, status: str, duration: float, 
                       error_message: str = None, screenshot_path: str = None, 
                       details: Dict[str, Any] = None):
        """Add a test result"""
        result = {
            "test_name": test_name,
            "status": status,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "error_message": error_message,
            "screenshot_path": screenshot_path,
            "details": details or {}
        }
        self.test_results.append(result)
    
    def end_test_suite(self):
        """End the test suite and generate report"""
        self.end_time = datetime.now()
        self._generate_html_report()
    
    def _generate_html_report(self):
        """Generate HTML report"""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASSED"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAILED"])
        skipped_tests = len([r for r in self.test_results if r["status"] == "SKIPPED"])
        
        total_duration = (self.end_time - self.start_time).total_seconds()
        
        html_content = self._generate_html_template(
            total_tests, passed_tests, failed_tests, skipped_tests, total_duration
        )
        
        # Write HTML file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_report_{timestamp}.html"
        filepath = os.path.join(self.html_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML report generated: {filepath}")
        return filepath
    
    def _generate_html_template(self, total_tests: int, passed_tests: int, 
                               failed_tests: int, skipped_tests: int, total_duration: float) -> str:
        """Generate HTML template"""
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sporty Web Assignment Test Report</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Sporty Web Assignment Testing Framework</h1>
            <h2>Test Execution Report</h2>
        </header>
        
        <div class="summary">
            <h3>Test Summary</h3>
            <div class="summary-grid">
                <div class="summary-item total">
                    <span class="number">{total_tests}</span>
                    <span class="label">Total Tests</span>
                </div>
                <div class="summary-item passed">
                    <span class="number">{passed_tests}</span>
                    <span class="label">Passed</span>
                </div>
                <div class="summary-item failed">
                    <span class="number">{failed_tests}</span>
                    <span class="label">Failed</span>
                </div>
                <div class="summary-item skipped">
                    <span class="number">{skipped_tests}</span>
                    <span class="label">Skipped</span>
                </div>
                <div class="summary-item pass-rate">
                    <span class="number">{pass_rate:.1f}%</span>
                    <span class="label">Pass Rate</span>
                </div>
                <div class="summary-item duration">
                    <span class="number">{total_duration:.2f}s</span>
                    <span class="label">Duration</span>
                </div>
            </div>
        </div>
        
        <div class="test-results">
            <h3>Test Results</h3>
            <table>
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Status</th>
                        <th>Duration</th>
                        <th>Timestamp</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_test_rows()}
                </tbody>
            </table>
        </div>
        
        <footer>
            <p>Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
    
    <script>
        {self._get_javascript()}
    </script>
</body>
</html>
        """
    
    def _get_css_styles(self) -> str:
        """Get CSS styles for the report"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        
        header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #007acc;
        }
        
        header h1 {
            color: #007acc;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        header h2 {
            color: #666;
            font-size: 1.5em;
            font-weight: normal;
        }
        
        .summary {
            margin-bottom: 30px;
        }
        
        .summary h3 {
            margin-bottom: 15px;
            color: #333;
        }
        
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .summary-item {
            text-align: center;
            padding: 20px;
            border-radius: 8px;
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
        }
        
        .summary-item.total {
            background-color: #e3f2fd;
            border-color: #2196f3;
        }
        
        .summary-item.passed {
            background-color: #e8f5e8;
            border-color: #4caf50;
        }
        
        .summary-item.failed {
            background-color: #ffebee;
            border-color: #f44336;
        }
        
        .summary-item.skipped {
            background-color: #fff3e0;
            border-color: #ff9800;
        }
        
        .summary-item.pass-rate {
            background-color: #f3e5f5;
            border-color: #9c27b0;
        }
        
        .summary-item.duration {
            background-color: #e0f2f1;
            border-color: #009688;
        }
        
        .summary-item .number {
            display: block;
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .summary-item .label {
            font-size: 0.9em;
            color: #666;
        }
        
        .test-results {
            margin-bottom: 30px;
        }
        
        .test-results h3 {
            margin-bottom: 15px;
            color: #333;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }
        
        th {
            background-color: #007acc;
            color: white;
            font-weight: 600;
        }
        
        tr:hover {
            background-color: #f8f9fa;
        }
        
        .status {
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        .status.PASSED {
            background-color: #d4edda;
            color: #155724;
        }
        
        .status.FAILED {
            background-color: #f8d7da;
            color: #721c24;
        }
        
        .status.SKIPPED {
            background-color: #fff3cd;
            color: #856404;
        }
        
        .details {
            max-width: 200px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .details:hover {
            white-space: normal;
            overflow: visible;
        }
        
        .screenshot {
            max-width: 100px;
            max-height: 100px;
            border-radius: 4px;
            cursor: pointer;
        }
        
        .screenshot:hover {
            transform: scale(1.1);
        }
        
        footer {
            text-align: center;
            padding-top: 20px;
            border-top: 1px solid #dee2e6;
            color: #666;
        }
        
        .error-message {
            color: #dc3545;
            font-size: 0.9em;
            margin-top: 5px;
        }
        """
    
    def _generate_test_rows(self) -> str:
        """Generate HTML rows for test results"""
        rows = []
        for result in self.test_results:
            status_class = result["status"]
            error_html = ""
            if result["error_message"]:
                error_html = f'<div class="error-message">{result["error_message"]}</div>'
            
            screenshot_html = ""
            if result["screenshot_path"]:
                screenshot_html = f'<img src="{result["screenshot_path"]}" class="screenshot" onclick="openScreenshot(this.src)">'
            
            details_html = ""
            if result["details"]:
                details_html = f'<div class="details">{json.dumps(result["details"], indent=2)}</div>'
            
            row = f"""
            <tr>
                <td>{result["test_name"]}</td>
                <td><span class="status {status_class}">{result["status"]}</span></td>
                <td>{result["duration"]:.2f}s</td>
                <td>{result["timestamp"]}</td>
                <td>
                    {details_html}
                    {screenshot_html}
                    {error_html}
                </td>
            </tr>
            """
            rows.append(row)
        
        return "".join(rows)
    
    def _get_javascript(self) -> str:
        """Get JavaScript for the report"""
        return """
        function openScreenshot(src) {
            window.open(src, '_blank');
        }
        
        function filterTests(status) {
            const rows = document.querySelectorAll('tbody tr');
            rows.forEach(row => {
                const statusCell = row.querySelector('.status');
                if (status === 'ALL' || statusCell.textContent === status) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        }
        """
