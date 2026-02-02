#!/usr/bin/env python3
"""
Automated API Testing Script
===========================

This script tests all API endpoints with various scenarios
and generates a test report.

Usage:
    python test_api.py [server_url]
    
Example:
    python test_api.py http://localhost:8000
"""

import requests
import json
import sys
import time
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class APITester:
    """
    Automated tester for Transaction API
    """
    
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url.rstrip('/')
        self.username = 'admin'
        self.password = 'password123'
        self.auth = (self.username, self.password)
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def print_header(self, text):
        """Print formatted section header"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")
    
    def log_test(self, test_name, passed, details=""):
        """Log test result"""
        status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
        print(f"{status} - {test_name}")
        if details:
            print(f"      {details}")
        
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'details': details
        })
        
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def test_get_all_transactions(self):
        """Test GET /transactions endpoint"""
        self.print_header("TEST 1: GET All Transactions")
        
        # Test with authentication
        try:
            response = requests.get(
                f"{self.base_url}/transactions",
                auth=self.auth
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "GET /transactions with auth",
                    True,
                    f"Retrieved {data.get('count', 0)} transactions"
                )
            else:
                self.log_test(
                    "GET /transactions with auth",
                    False,
                    f"Expected 200, got {response.status_code}"
                )
        except Exception as e:
            self.log_test("GET /transactions with auth", False, str(e))
    
    def test_get_without_auth(self):
        """Test unauthorized access"""
        self.print_header("TEST 2: Unauthorized Access")
        
        try:
            response = requests.get(f"{self.base_url}/transactions")
            
            if response.status_code == 401:
                self.log_test(
                    "GET /transactions without auth",
                    True,
                    "Correctly returned 401 Unauthorized"
                )
            else:
                self.log_test(
                    "GET /transactions without auth",
                    False,
                    f"Expected 401, got {response.status_code}"
                )
        except Exception as e:
            self.log_test("GET /transactions without auth", False, str(e))
    
    def test_get_specific_transaction(self):
        """Test GET /transactions/{id}"""
        self.print_header("TEST 3: GET Specific Transaction")
        
        # Test valid ID
        try:
            response = requests.get(
                f"{self.base_url}/transactions/1",
                auth=self.auth
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('transaction', {}).get('id') == 1:
                    self.log_test(
                        "GET /transactions/1",
                        True,
                        "Retrieved correct transaction"
                    )
                else:
                    self.log_test(
                        "GET /transactions/1",
                        False,
                        "Transaction ID mismatch"
                    )
            else:
                self.log_test(
                    "GET /transactions/1",
                    False,
                    f"Expected 200, got {response.status_code}"
                )
        except Exception as e:
            self.log_test("GET /transactions/1", False, str(e))
        
        # Test invalid ID
        try:
            response = requests.get(
                f"{self.base_url}/transactions/99999",
                auth=self.auth
            )
            
            if response.status_code == 404:
                self.log_test(
                    "GET /transactions/99999 (invalid)",
                    True,
                    "Correctly returned 404 Not Found"
                )
            else:
                self.log_test(
                    "GET /transactions/99999 (invalid)",
                    False,
                    f"Expected 404, got {response.status_code}"
                )
        except Exception as e:
            self.log_test("GET /transactions/99999 (invalid)", False, str(e))
    
    def test_post_transaction(self):
        """Test POST /transactions"""
        self.print_header("TEST 4: POST Create Transaction")
        
        new_transaction = {
            "type": "payment",
            "amount": 5000,
            "recipient": "Test User",
            "fee": 100,
            "new_balance": 45000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/transactions",
                auth=self.auth,
                json=new_transaction
            )
            
            if response.status_code == 201:
                data = response.json()
                created = data.get('transaction', {})
                if created.get('type') == 'payment' and created.get('amount') == 5000:
                    self.log_test(
                        "POST /transactions",
                        True,
                        f"Created transaction with ID {created.get('id')}"
                    )
                    # Save ID for later tests
                    self.created_id = created.get('id')
                else:
                    self.log_test(
                        "POST /transactions",
                        False,
                        "Created but data mismatch"
                    )
            else:
                self.log_test(
                    "POST /transactions",
                    False,
                    f"Expected 201, got {response.status_code}"
                )
        except Exception as e:
            self.log_test("POST /transactions", False, str(e))
            self.created_id = None
    
    def test_post_invalid_data(self):
        """Test POST with invalid data"""
        self.print_header("TEST 5: POST Invalid Data")
        
        # Missing required field
        try:
            response = requests.post(
                f"{self.base_url}/transactions",
                auth=self.auth,
                json={"amount": 1000}  # Missing 'type'
            )
            
            if response.status_code == 400:
                self.log_test(
                    "POST with missing required field",
                    True,
                    "Correctly returned 400 Bad Request"
                )
            else:
                self.log_test(
                    "POST with missing required field",
                    False,
                    f"Expected 400, got {response.status_code}"
                )
        except Exception as e:
            self.log_test("POST with missing required field", False, str(e))
    
    def test_put_transaction(self):
        """Test PUT /transactions/{id}"""
        self.print_header("TEST 6: PUT Update Transaction")
        
        if not hasattr(self, 'created_id') or self.created_id is None:
            self.log_test("PUT /transactions/{id}", False, "No transaction ID from POST test")
            return
        
        update_data = {
            "amount": 7500,
            "fee": 150
        }
        
        try:
            response = requests.put(
                f"{self.base_url}/transactions/{self.created_id}",
                auth=self.auth,
                json=update_data
            )
            
            if response.status_code == 200:
                data = response.json()
                updated = data.get('transaction', {})
                if updated.get('amount') == 7500 and updated.get('fee') == 150:
                    self.log_test(
                        f"PUT /transactions/{self.created_id}",
                        True,
                        "Transaction updated successfully"
                    )
                else:
                    self.log_test(
                        f"PUT /transactions/{self.created_id}",
                        False,
                        "Updated but data mismatch"
                    )
            else:
                self.log_test(
                    f"PUT /transactions/{self.created_id}",
                    False,
                    f"Expected 200, got {response.status_code}"
                )
        except Exception as e:
            self.log_test(f"PUT /transactions/{self.created_id}", False, str(e))
    
    def test_delete_transaction(self):
        """Test DELETE /transactions/{id}"""
        self.print_header("TEST 7: DELETE Transaction")
        
        if not hasattr(self, 'created_id') or self.created_id is None:
            self.log_test("DELETE /transactions/{id}", False, "No transaction ID from POST test")
            return
        
        try:
            response = requests.delete(
                f"{self.base_url}/transactions/{self.created_id}",
                auth=self.auth
            )
            
            if response.status_code == 200:
                self.log_test(
                    f"DELETE /transactions/{self.created_id}",
                    True,
                    "Transaction deleted successfully"
                )
                
                # Verify deletion
                verify = requests.get(
                    f"{self.base_url}/transactions/{self.created_id}",
                    auth=self.auth
                )
                
                if verify.status_code == 404:
                    self.log_test(
                        "Verify deletion",
                        True,
                        "Transaction no longer exists"
                    )
                else:
                    self.log_test(
                        "Verify deletion",
                        False,
                        "Transaction still exists after deletion"
                    )
            else:
                self.log_test(
                    f"DELETE /transactions/{self.created_id}",
                    False,
                    f"Expected 200, got {response.status_code}"
                )
        except Exception as e:
            self.log_test(f"DELETE /transactions/{self.created_id}", False, str(e))
    
    def test_filters(self):
        """Test query parameter filtering"""
        self.print_header("TEST 8: Query Filters")
        
        # Test type filter
        try:
            response = requests.get(
                f"{self.base_url}/transactions?type=payment",
                auth=self.auth
            )
            
            if response.status_code == 200:
                data = response.json()
                transactions = data.get('transactions', [])
                
                if all(t.get('type') == 'payment' for t in transactions):
                    self.log_test(
                        "Filter by type=payment",
                        True,
                        f"Retrieved {len(transactions)} payment transactions"
                    )
                else:
                    self.log_test(
                        "Filter by type=payment",
                        False,
                        "Filter returned wrong transaction types"
                    )
            else:
                self.log_test(
                    "Filter by type=payment",
                    False,
                    f"Expected 200, got {response.status_code}"
                )
        except Exception as e:
            self.log_test("Filter by type=payment", False, str(e))
    
    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{'TEST SUMMARY':^70}{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")
        
        print(f"Total Tests:    {total}")
        print(f"{Colors.GREEN}Passed:         {self.passed}{Colors.RESET}")
        print(f"{Colors.RED}Failed:         {self.failed}{Colors.RESET}")
        print(f"Pass Rate:      {pass_rate:.1f}%")
        
        if self.failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED!{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}⚠ Some tests failed. Review details above.{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}\n")
    
    def save_report(self, filename='test_report.json'):
        """Save test results to JSON file"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'base_url': self.base_url,
            'total_tests': self.passed + self.failed,
            'passed': self.passed,
            'failed': self.failed,
            'pass_rate': (self.passed / (self.passed + self.failed) * 100) if (self.passed + self.failed) > 0 else 0,
            'results': self.test_results
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Test report saved to: {filename}")
    
    def run_all_tests(self):
        """Run all test suites"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}Starting API Tests...{Colors.RESET}")
        print(f"Base URL: {self.base_url}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Check if server is running
        try:
            response = requests.get(self.base_url, timeout=2)
        except requests.exceptions.RequestException:
            print(f"{Colors.RED}ERROR: Cannot connect to {self.base_url}{Colors.RESET}")
            print("Make sure the API server is running!")
            sys.exit(1)
        
        # Run all tests
        self.test_get_all_transactions()
        self.test_get_without_auth()
        self.test_get_specific_transaction()
        self.test_post_transaction()
        self.test_post_invalid_data()
        self.test_put_transaction()
        self.test_delete_transaction()
        self.test_filters()
        
        # Print summary
        self.print_summary()
        
        # Save report
        self.save_report()


if __name__ == '__main__':
    # Get base URL from command line or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8000'
    
    # Create tester and run
    tester = APITester(base_url)
    tester.run_all_tests()
