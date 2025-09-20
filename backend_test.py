#!/usr/bin/env python3
"""
Backend Testing Suite for SoftGemZ Contact Form API
Tests the contact form submission and retrieval endpoints
"""

import requests
import json
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://techgems-digital.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class ContactFormTester:
    def __init__(self):
        self.api_base = API_BASE
        self.test_results = []
        self.submitted_ids = []
        
    def log_result(self, test_name, success, message, details=None):
        """Log test result"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details:
            print(f"   Details: {details}")
        print()

    def test_valid_contact_submission(self):
        """Test valid contact form submission with all fields"""
        test_data = {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "company": "Tech Solutions Inc",
            "phone": "+1-555-0123",
            "projectType": "AI Development",
            "message": "I'm interested in your AI automation services for our e-commerce platform."
        }
        
        try:
            response = requests.post(f"{self.api_base}/contact", json=test_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('id'):
                    self.submitted_ids.append(data['id'])
                    self.log_result(
                        "Valid Contact Submission (All Fields)",
                        True,
                        f"Successfully submitted contact form. ID: {data['id']}",
                        {'response_data': data, 'status_code': response.status_code}
                    )
                else:
                    self.log_result(
                        "Valid Contact Submission (All Fields)",
                        False,
                        f"API returned success=False: {data.get('message', 'Unknown error')}",
                        {'response_data': data, 'status_code': response.status_code}
                    )
            else:
                self.log_result(
                    "Valid Contact Submission (All Fields)",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Valid Contact Submission (All Fields)",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_required_fields_only(self):
        """Test contact submission with only required fields"""
        test_data = {
            "name": "Jane Doe",
            "email": "jane.doe@company.org",
            "message": "Looking for automation solutions for our manufacturing process."
        }
        
        try:
            response = requests.post(f"{self.api_base}/contact", json=test_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('id'):
                    self.submitted_ids.append(data['id'])
                    self.log_result(
                        "Required Fields Only Submission",
                        True,
                        f"Successfully submitted with required fields only. ID: {data['id']}",
                        {'response_data': data, 'status_code': response.status_code}
                    )
                else:
                    self.log_result(
                        "Required Fields Only Submission",
                        False,
                        f"API returned success=False: {data.get('message', 'Unknown error')}",
                        {'response_data': data, 'status_code': response.status_code}
                    )
            else:
                self.log_result(
                    "Required Fields Only Submission",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Required Fields Only Submission",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_missing_required_fields(self):
        """Test validation for missing required fields"""
        test_cases = [
            {"email": "test@example.com", "message": "Test message"},  # Missing name
            {"name": "Test User", "message": "Test message"},  # Missing email
            {"name": "Test User", "email": "test@example.com"},  # Missing message
            {}  # Missing all fields
        ]
        
        for i, test_data in enumerate(test_cases):
            missing_fields = []
            if 'name' not in test_data: missing_fields.append('name')
            if 'email' not in test_data: missing_fields.append('email')
            if 'message' not in test_data: missing_fields.append('message')
            
            try:
                response = requests.post(f"{self.api_base}/contact", json=test_data, timeout=10)
                
                # Should return validation error (422) or success=False
                if response.status_code == 422:
                    self.log_result(
                        f"Missing Required Fields Test {i+1} ({', '.join(missing_fields)})",
                        True,
                        "Correctly rejected submission with missing required fields",
                        {'status_code': response.status_code, 'missing_fields': missing_fields}
                    )
                elif response.status_code == 200:
                    data = response.json()
                    if not data.get('success'):
                        self.log_result(
                            f"Missing Required Fields Test {i+1} ({', '.join(missing_fields)})",
                            True,
                            f"Correctly rejected: {data.get('message')}",
                            {'response_data': data, 'missing_fields': missing_fields}
                        )
                    else:
                        self.log_result(
                            f"Missing Required Fields Test {i+1} ({', '.join(missing_fields)})",
                            False,
                            "API incorrectly accepted submission with missing required fields",
                            {'response_data': data, 'missing_fields': missing_fields}
                        )
                else:
                    self.log_result(
                        f"Missing Required Fields Test {i+1} ({', '.join(missing_fields)})",
                        False,
                        f"Unexpected HTTP {response.status_code}: {response.text}",
                        {'status_code': response.status_code, 'missing_fields': missing_fields}
                    )
            except Exception as e:
                self.log_result(
                    f"Missing Required Fields Test {i+1} ({', '.join(missing_fields)})",
                    False,
                    f"Request failed: {str(e)}",
                    {'error': str(e), 'missing_fields': missing_fields}
                )

    def test_invalid_email_formats(self):
        """Test email format validation"""
        invalid_emails = [
            "invalid-email",
            "test@",
            "@example.com",
            "test..test@example.com",
            "test@example",
            "test@.com",
            "",
            "test@example..com"
        ]
        
        for email in invalid_emails:
            test_data = {
                "name": "Test User",
                "email": email,
                "message": "Test message with invalid email"
            }
            
            try:
                response = requests.post(f"{self.api_base}/contact", json=test_data, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if not data.get('success'):
                        self.log_result(
                            f"Invalid Email Format Test ({email})",
                            True,
                            f"Correctly rejected invalid email: {data.get('message')}",
                            {'email': email, 'response_data': data}
                        )
                    else:
                        self.log_result(
                            f"Invalid Email Format Test ({email})",
                            False,
                            "API incorrectly accepted invalid email format",
                            {'email': email, 'response_data': data}
                        )
                elif response.status_code == 422:
                    self.log_result(
                        f"Invalid Email Format Test ({email})",
                        True,
                        "Correctly rejected invalid email with validation error",
                        {'email': email, 'status_code': response.status_code}
                    )
                else:
                    self.log_result(
                        f"Invalid Email Format Test ({email})",
                        False,
                        f"Unexpected HTTP {response.status_code}: {response.text}",
                        {'email': email, 'status_code': response.status_code}
                    )
            except Exception as e:
                self.log_result(
                    f"Invalid Email Format Test ({email})",
                    False,
                    f"Request failed: {str(e)}",
                    {'email': email, 'error': str(e)}
                )

    def test_field_length_limits(self):
        """Test field length validation"""
        test_cases = [
            {
                "name": "A" * 101,  # Exceeds 100 char limit
                "email": "test@example.com",
                "message": "Test message",
                "test_name": "Name Length Limit (101 chars)"
            },
            {
                "name": "Test User",
                "email": "test@" + "a" * 250 + ".com",  # Exceeds 255 char limit
                "message": "Test message",
                "test_name": "Email Length Limit (>255 chars)"
            },
            {
                "name": "Test User",
                "email": "test@example.com",
                "message": "A" * 2001,  # Exceeds 2000 char limit
                "test_name": "Message Length Limit (2001 chars)"
            },
            {
                "name": "Test User",
                "email": "test@example.com",
                "company": "B" * 101,  # Exceeds 100 char limit
                "message": "Test message",
                "test_name": "Company Length Limit (101 chars)"
            }
        ]
        
        for test_case in test_cases:
            test_name = test_case.pop('test_name')
            
            try:
                response = requests.post(f"{self.api_base}/contact", json=test_case, timeout=10)
                
                if response.status_code == 422:
                    self.log_result(
                        test_name,
                        True,
                        "Correctly rejected submission exceeding field length limits",
                        {'status_code': response.status_code}
                    )
                elif response.status_code == 200:
                    data = response.json()
                    if not data.get('success'):
                        self.log_result(
                            test_name,
                            True,
                            f"Correctly rejected: {data.get('message')}",
                            {'response_data': data}
                        )
                    else:
                        self.log_result(
                            test_name,
                            False,
                            "API incorrectly accepted submission exceeding field limits",
                            {'response_data': data}
                        )
                else:
                    self.log_result(
                        test_name,
                        False,
                        f"Unexpected HTTP {response.status_code}: {response.text}",
                        {'status_code': response.status_code}
                    )
            except Exception as e:
                self.log_result(
                    test_name,
                    False,
                    f"Request failed: {str(e)}",
                    {'error': str(e)}
                )

    def test_special_characters(self):
        """Test handling of special characters in inputs"""
        test_data = {
            "name": "José María O'Connor-Smith",
            "email": "jose.maria@example-company.co.uk",
            "company": "Müller & Associates (R&D)",
            "phone": "+49-123-456-7890",
            "projectType": "AI/ML & Data Analytics",
            "message": "We need AI solutions for our café's inventory management. Special chars: àáâãäåæçèéêë & symbols: @#$%^&*()"
        }
        
        try:
            response = requests.post(f"{self.api_base}/contact", json=test_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('id'):
                    self.submitted_ids.append(data['id'])
                    self.log_result(
                        "Special Characters Handling",
                        True,
                        f"Successfully handled special characters. ID: {data['id']}",
                        {'response_data': data}
                    )
                else:
                    self.log_result(
                        "Special Characters Handling",
                        False,
                        f"API returned success=False: {data.get('message', 'Unknown error')}",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Special Characters Handling",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Special Characters Handling",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_contact_retrieval(self):
        """Test GET /api/contact endpoint"""
        try:
            response = requests.get(f"{self.api_base}/contact", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result(
                        "Contact Submissions Retrieval",
                        True,
                        f"Successfully retrieved {len(data)} contact submissions",
                        {'count': len(data), 'status_code': response.status_code}
                    )
                    
                    # Verify data structure if we have submissions
                    if len(data) > 0:
                        first_submission = data[0]
                        required_fields = ['id', 'name', 'email', 'message', 'createdAt']
                        missing_fields = [field for field in required_fields if field not in first_submission]
                        
                        if not missing_fields:
                            self.log_result(
                                "Contact Data Structure Validation",
                                True,
                                "Contact submissions have correct data structure",
                                {'sample_fields': list(first_submission.keys())}
                            )
                        else:
                            self.log_result(
                                "Contact Data Structure Validation",
                                False,
                                f"Missing required fields: {missing_fields}",
                                {'missing_fields': missing_fields, 'available_fields': list(first_submission.keys())}
                            )
                else:
                    self.log_result(
                        "Contact Submissions Retrieval",
                        False,
                        f"Expected list, got {type(data)}",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Contact Submissions Retrieval",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Contact Submissions Retrieval",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_malformed_requests(self):
        """Test handling of malformed JSON requests"""
        test_cases = [
            ("Invalid JSON", "invalid json"),
            ("Empty Request", ""),
            ("Non-JSON Content", "This is not JSON"),
        ]
        
        for test_name, payload in test_cases:
            try:
                headers = {'Content-Type': 'application/json'}
                response = requests.post(f"{self.api_base}/contact", data=payload, headers=headers, timeout=10)
                
                if response.status_code in [400, 422]:
                    self.log_result(
                        f"Malformed Request Test ({test_name})",
                        True,
                        f"Correctly rejected malformed request with HTTP {response.status_code}",
                        {'status_code': response.status_code}
                    )
                else:
                    self.log_result(
                        f"Malformed Request Test ({test_name})",
                        False,
                        f"Unexpected response to malformed request: HTTP {response.status_code}",
                        {'status_code': response.status_code, 'response': response.text}
                    )
            except Exception as e:
                self.log_result(
                    f"Malformed Request Test ({test_name})",
                    False,
                    f"Request failed: {str(e)}",
                    {'error': str(e)}
                )

    def test_api_connectivity(self):
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{self.api_base}/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('message') == 'Hello World':
                    self.log_result(
                        "API Connectivity Test",
                        True,
                        "Successfully connected to API",
                        {'response_data': data, 'status_code': response.status_code}
                    )
                else:
                    self.log_result(
                        "API Connectivity Test",
                        False,
                        f"Unexpected response: {data}",
                        {'response_data': data, 'status_code': response.status_code}
                    )
            else:
                self.log_result(
                    "API Connectivity Test",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "API Connectivity Test",
                False,
                f"Connection failed: {str(e)}",
                {'error': str(e)}
            )

    def run_all_tests(self):
        """Run all backend tests"""
        print("=" * 80)
        print("SOFTGEMZ BACKEND TESTING SUITE")
        print("=" * 80)
        print(f"Testing API at: {self.api_base}")
        print(f"Started at: {datetime.now().isoformat()}")
        print("=" * 80)
        print()
        
        # Test API connectivity first
        self.test_api_connectivity()
        
        # Test contact form submission
        self.test_valid_contact_submission()
        self.test_required_fields_only()
        self.test_missing_required_fields()
        self.test_invalid_email_formats()
        self.test_field_length_limits()
        self.test_special_characters()
        self.test_malformed_requests()
        
        # Test contact retrieval
        self.test_contact_retrieval()
        
        # Summary
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result['success'])
        failed = len(self.test_results) - passed
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/len(self.test_results)*100):.1f}%")
        print()
        
        if failed > 0:
            print("FAILED TESTS:")
            print("-" * 40)
            for result in self.test_results:
                if not result['success']:
                    print(f"❌ {result['test']}: {result['message']}")
            print()
        
        print("PASSED TESTS:")
        print("-" * 40)
        for result in self.test_results:
            if result['success']:
                print(f"✅ {result['test']}")
        
        print()
        print(f"Test completed at: {datetime.now().isoformat()}")
        print("=" * 80)

if __name__ == "__main__":
    tester = ContactFormTester()
    tester.run_all_tests()