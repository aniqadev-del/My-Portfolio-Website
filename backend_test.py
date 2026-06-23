#!/usr/bin/env python3
"""
Comprehensive Backend Testing Suite for SoftGemZ Admin Control System
Tests all backend APIs including contact form, admin authentication, and admin management endpoints
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
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://admin-suite-71.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

# Admin credentials for testing
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

class AdminSystemTester:
    def __init__(self):
        self.api_base = API_BASE
        self.test_results = []
        self.submitted_ids = []
        self.admin_token = None
        self.created_portfolio_ids = []
        self.created_service_ids = []
        
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
                if data.get('message') == 'API is alive!':
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

    # ==========================================
    # ADMIN AUTHENTICATION TESTS
    # ==========================================
    
    def test_admin_login_valid_credentials(self):
        """Test admin login with correct credentials"""
        login_data = {
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        }
        
        try:
            response = requests.post(f"{self.api_base}/admin/login", json=login_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('access_token') and data.get('token_type') == 'bearer':
                    self.admin_token = data['access_token']
                    self.log_result(
                        "Admin Login - Valid Credentials",
                        True,
                        f"Successfully logged in as {data.get('username')}",
                        {'token_received': True, 'username': data.get('username')}
                    )
                else:
                    self.log_result(
                        "Admin Login - Valid Credentials",
                        False,
                        "Login response missing token or incorrect format",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Admin Login - Valid Credentials",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Login - Valid Credentials",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_login_invalid_username(self):
        """Test admin login with incorrect username"""
        login_data = {
            "username": "wronguser",
            "password": ADMIN_PASSWORD
        }
        
        try:
            response = requests.post(f"{self.api_base}/admin/login", json=login_data, timeout=10)
            
            if response.status_code == 401:
                self.log_result(
                    "Admin Login - Invalid Username",
                    True,
                    "Correctly rejected invalid username",
                    {'status_code': response.status_code}
                )
            else:
                self.log_result(
                    "Admin Login - Invalid Username",
                    False,
                    f"Expected 401, got HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Login - Invalid Username",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_login_invalid_password(self):
        """Test admin login with incorrect password"""
        login_data = {
            "username": ADMIN_USERNAME,
            "password": "wrongpassword"
        }
        
        try:
            response = requests.post(f"{self.api_base}/admin/login", json=login_data, timeout=10)
            
            if response.status_code == 401:
                self.log_result(
                    "Admin Login - Invalid Password",
                    True,
                    "Correctly rejected invalid password",
                    {'status_code': response.status_code}
                )
            else:
                self.log_result(
                    "Admin Login - Invalid Password",
                    False,
                    f"Expected 401, got HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Login - Invalid Password",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_login_missing_fields(self):
        """Test admin login with missing fields"""
        test_cases = [
            {"username": ADMIN_USERNAME},  # Missing password
            {"password": ADMIN_PASSWORD},  # Missing username
            {}  # Missing both
        ]
        
        for i, login_data in enumerate(test_cases):
            try:
                response = requests.post(f"{self.api_base}/admin/login", json=login_data, timeout=10)
                
                if response.status_code == 422:
                    self.log_result(
                        f"Admin Login - Missing Fields Test {i+1}",
                        True,
                        "Correctly rejected login with missing fields",
                        {'status_code': response.status_code, 'test_data': login_data}
                    )
                else:
                    self.log_result(
                        f"Admin Login - Missing Fields Test {i+1}",
                        False,
                        f"Expected 422, got HTTP {response.status_code}: {response.text}",
                        {'status_code': response.status_code, 'test_data': login_data}
                    )
            except Exception as e:
                self.log_result(
                    f"Admin Login - Missing Fields Test {i+1}",
                    False,
                    f"Request failed: {str(e)}",
                    {'error': str(e), 'test_data': login_data}
                )

    # ==========================================
    # ADMIN CONTACTS MANAGEMENT TESTS
    # ==========================================
    
    def test_admin_contacts_get_all(self):
        """Test GET /api/admin/contacts - retrieve all contacts"""
        if not self.admin_token:
            self.log_result(
                "Admin Contacts - Get All",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{self.api_base}/admin/contacts", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result(
                        "Admin Contacts - Get All",
                        True,
                        f"Successfully retrieved {len(data)} contacts",
                        {'count': len(data), 'status_code': response.status_code}
                    )
                else:
                    self.log_result(
                        "Admin Contacts - Get All",
                        False,
                        f"Expected list, got {type(data)}",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Admin Contacts - Get All",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Contacts - Get All",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_contacts_filter_by_status(self):
        """Test GET /api/admin/contacts?status=new - filter by status"""
        if not self.admin_token:
            self.log_result(
                "Admin Contacts - Filter by Status",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{self.api_base}/admin/contacts?status=new", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result(
                        "Admin Contacts - Filter by Status",
                        True,
                        f"Successfully filtered contacts by status 'new': {len(data)} results",
                        {'count': len(data), 'status_code': response.status_code}
                    )
                else:
                    self.log_result(
                        "Admin Contacts - Filter by Status",
                        False,
                        f"Expected list, got {type(data)}",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Admin Contacts - Filter by Status",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Contacts - Filter by Status",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_contacts_search(self):
        """Test GET /api/admin/contacts?search=test - search functionality"""
        if not self.admin_token:
            self.log_result(
                "Admin Contacts - Search",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{self.api_base}/admin/contacts?search=test", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result(
                        "Admin Contacts - Search",
                        True,
                        f"Successfully searched contacts for 'test': {len(data)} results",
                        {'count': len(data), 'status_code': response.status_code}
                    )
                else:
                    self.log_result(
                        "Admin Contacts - Search",
                        False,
                        f"Expected list, got {type(data)}",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Admin Contacts - Search",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Contacts - Search",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_contacts_update_status(self):
        """Test PUT /api/admin/contacts/{contact_id} - update contact status"""
        if not self.admin_token:
            self.log_result(
                "Admin Contacts - Update Status",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        # First get a contact to update
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Get contacts first
            response = requests.get(f"{self.api_base}/admin/contacts", headers=headers, timeout=10)
            
            if response.status_code == 200:
                contacts = response.json()
                if len(contacts) > 0:
                    contact_id = contacts[0]['id']
                    
                    # Update the contact status
                    update_data = {"status": "in-progress"}
                    response = requests.put(
                        f"{self.api_base}/admin/contacts/{contact_id}", 
                        json=update_data, 
                        headers=headers, 
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('status') == 'in-progress':
                            self.log_result(
                                "Admin Contacts - Update Status",
                                True,
                                f"Successfully updated contact {contact_id} status to 'in-progress'",
                                {'contact_id': contact_id, 'new_status': data.get('status')}
                            )
                        else:
                            self.log_result(
                                "Admin Contacts - Update Status",
                                False,
                                f"Status not updated correctly: {data.get('status')}",
                                {'response_data': data}
                            )
                    else:
                        self.log_result(
                            "Admin Contacts - Update Status",
                            False,
                            f"HTTP {response.status_code}: {response.text}",
                            {'status_code': response.status_code}
                        )
                else:
                    self.log_result(
                        "Admin Contacts - Update Status",
                        False,
                        "No contacts available to update",
                        {'contacts_count': 0}
                    )
            else:
                self.log_result(
                    "Admin Contacts - Update Status",
                    False,
                    f"Failed to get contacts: HTTP {response.status_code}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Contacts - Update Status",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_contacts_add_response(self):
        """Test PUT /api/admin/contacts/{contact_id} - add admin response"""
        if not self.admin_token:
            self.log_result(
                "Admin Contacts - Add Response",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Get contacts first
            response = requests.get(f"{self.api_base}/admin/contacts", headers=headers, timeout=10)
            
            if response.status_code == 200:
                contacts = response.json()
                if len(contacts) > 0:
                    contact_id = contacts[0]['id']
                    
                    # Add admin response
                    update_data = {
                        "adminResponse": "Thank you for your inquiry. We will review your requirements and get back to you within 2 business days."
                    }
                    response = requests.put(
                        f"{self.api_base}/admin/contacts/{contact_id}", 
                        json=update_data, 
                        headers=headers, 
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('adminResponse') and data.get('respondedBy'):
                            self.log_result(
                                "Admin Contacts - Add Response",
                                True,
                                f"Successfully added admin response to contact {contact_id}",
                                {'contact_id': contact_id, 'responded_by': data.get('respondedBy')}
                            )
                        else:
                            self.log_result(
                                "Admin Contacts - Add Response",
                                False,
                                "Admin response not saved correctly",
                                {'response_data': data}
                            )
                    else:
                        self.log_result(
                            "Admin Contacts - Add Response",
                            False,
                            f"HTTP {response.status_code}: {response.text}",
                            {'status_code': response.status_code}
                        )
                else:
                    self.log_result(
                        "Admin Contacts - Add Response",
                        False,
                        "No contacts available to respond to",
                        {'contacts_count': 0}
                    )
            else:
                self.log_result(
                    "Admin Contacts - Add Response",
                    False,
                    f"Failed to get contacts: HTTP {response.status_code}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Contacts - Add Response",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_contacts_export_csv(self):
        """Test GET /api/admin/contacts/export - export contacts to CSV"""
        if not self.admin_token:
            self.log_result(
                "Admin Contacts - Export CSV",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{self.api_base}/admin/contacts/export", headers=headers, timeout=10)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'text/csv' in content_type:
                    csv_content = response.text
                    lines = csv_content.split('\n')
                    self.log_result(
                        "Admin Contacts - Export CSV",
                        True,
                        f"Successfully exported contacts to CSV ({len(lines)} lines)",
                        {'content_type': content_type, 'lines_count': len(lines)}
                    )
                else:
                    self.log_result(
                        "Admin Contacts - Export CSV",
                        False,
                        f"Expected CSV content, got {content_type}",
                        {'content_type': content_type}
                    )
            else:
                self.log_result(
                    "Admin Contacts - Export CSV",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Contacts - Export CSV",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_contacts_without_auth(self):
        """Test admin contacts endpoints without authentication token"""
        try:
            response = requests.get(f"{self.api_base}/admin/contacts", timeout=10)
            
            if response.status_code == 401:
                self.log_result(
                    "Admin Contacts - No Auth Token",
                    True,
                    "Correctly rejected request without authentication",
                    {'status_code': response.status_code}
                )
            else:
                self.log_result(
                    "Admin Contacts - No Auth Token",
                    False,
                    f"Expected 401, got HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Contacts - No Auth Token",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    # ==========================================
    # ADMIN DASHBOARD STATS TESTS
    # ==========================================
    
    def test_admin_dashboard_stats(self):
        """Test GET /api/admin/stats - dashboard statistics"""
        if not self.admin_token:
            self.log_result(
                "Admin Dashboard Stats",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{self.api_base}/admin/stats", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = [
                    'totalContacts', 'newContacts', 'inProgressContacts', 
                    'completedContacts', 'totalPortfolioProjects', 'totalServices', 'recentContacts'
                ]
                
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    self.log_result(
                        "Admin Dashboard Stats",
                        True,
                        f"Successfully retrieved dashboard statistics",
                        {
                            'total_contacts': data.get('totalContacts'),
                            'new_contacts': data.get('newContacts'),
                            'portfolio_projects': data.get('totalPortfolioProjects'),
                            'services': data.get('totalServices'),
                            'recent_contacts_count': len(data.get('recentContacts', []))
                        }
                    )
                else:
                    self.log_result(
                        "Admin Dashboard Stats",
                        False,
                        f"Missing required fields: {missing_fields}",
                        {'missing_fields': missing_fields, 'response_data': data}
                    )
            else:
                self.log_result(
                    "Admin Dashboard Stats",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Dashboard Stats",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    # ==========================================
    # ADMIN PORTFOLIO MANAGEMENT TESTS
    # ==========================================
    
    def test_admin_portfolio_get_all(self):
        """Test GET /api/admin/portfolio - get all projects"""
        if not self.admin_token:
            self.log_result(
                "Admin Portfolio - Get All",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{self.api_base}/admin/portfolio", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result(
                        "Admin Portfolio - Get All",
                        True,
                        f"Successfully retrieved {len(data)} portfolio projects",
                        {'count': len(data), 'status_code': response.status_code}
                    )
                else:
                    self.log_result(
                        "Admin Portfolio - Get All",
                        False,
                        f"Expected list, got {type(data)}",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Admin Portfolio - Get All",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Portfolio - Get All",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_portfolio_create(self):
        """Test POST /api/admin/portfolio - create new project"""
        if not self.admin_token:
            self.log_result(
                "Admin Portfolio - Create Project",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        project_data = {
            "title": "AI-Powered Customer Service Bot",
            "description": "Intelligent chatbot system that handles customer inquiries with natural language processing",
            "category": "AI Development",
            "image": "https://example.com/chatbot-image.jpg",
            "technologies": ["Python", "TensorFlow", "FastAPI", "React"],
            "challenge": "Client needed 24/7 customer support without increasing staff costs",
            "solution": "Developed an AI chatbot that handles 80% of customer inquiries automatically",
            "results": "Reduced response time by 90% and customer service costs by 60%"
        }
        
        try:
            response = requests.post(f"{self.api_base}/admin/portfolio", json=project_data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('id') and data.get('title') == project_data['title']:
                    self.created_portfolio_ids.append(data['id'])
                    self.log_result(
                        "Admin Portfolio - Create Project",
                        True,
                        f"Successfully created portfolio project: {data['title']}",
                        {'project_id': data['id'], 'title': data['title']}
                    )
                else:
                    self.log_result(
                        "Admin Portfolio - Create Project",
                        False,
                        "Project creation response missing required fields",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Admin Portfolio - Create Project",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Portfolio - Create Project",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_portfolio_update(self):
        """Test PUT /api/admin/portfolio/{project_id} - update project"""
        if not self.admin_token:
            self.log_result(
                "Admin Portfolio - Update Project",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        if not self.created_portfolio_ids:
            self.log_result(
                "Admin Portfolio - Update Project",
                False,
                "No portfolio projects available to update",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        project_id = self.created_portfolio_ids[0]
        
        update_data = {
            "title": "Advanced AI Customer Service Bot",
            "description": "Enhanced intelligent chatbot system with multilingual support",
            "category": "AI Development",
            "image": "https://example.com/enhanced-chatbot.jpg",
            "technologies": ["Python", "TensorFlow", "FastAPI", "React", "MongoDB"],
            "challenge": "Client needed multilingual 24/7 customer support",
            "solution": "Developed an enhanced AI chatbot with multilingual capabilities",
            "results": "Reduced response time by 95% and expanded to 5 languages"
        }
        
        try:
            response = requests.put(f"{self.api_base}/admin/portfolio/{project_id}", json=update_data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('title') == update_data['title']:
                    self.log_result(
                        "Admin Portfolio - Update Project",
                        True,
                        f"Successfully updated portfolio project: {data['title']}",
                        {'project_id': project_id, 'new_title': data['title']}
                    )
                else:
                    self.log_result(
                        "Admin Portfolio - Update Project",
                        False,
                        "Project update did not reflect changes",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Admin Portfolio - Update Project",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Portfolio - Update Project",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_portfolio_delete(self):
        """Test DELETE /api/admin/portfolio/{project_id} - delete project"""
        if not self.admin_token:
            self.log_result(
                "Admin Portfolio - Delete Project",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        if not self.created_portfolio_ids:
            self.log_result(
                "Admin Portfolio - Delete Project",
                False,
                "No portfolio projects available to delete",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        project_id = self.created_portfolio_ids[0]
        
        try:
            response = requests.delete(f"{self.api_base}/admin/portfolio/{project_id}", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_result(
                        "Admin Portfolio - Delete Project",
                        True,
                        f"Successfully deleted portfolio project: {project_id}",
                        {'project_id': project_id, 'message': data.get('message')}
                    )
                    self.created_portfolio_ids.remove(project_id)
                else:
                    self.log_result(
                        "Admin Portfolio - Delete Project",
                        False,
                        "Delete response indicates failure",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Admin Portfolio - Delete Project",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Portfolio - Delete Project",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_portfolio_validation(self):
        """Test portfolio creation with missing required fields"""
        if not self.admin_token:
            self.log_result(
                "Admin Portfolio - Validation",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test with missing required fields
        invalid_data = {
            "description": "Test description"
            # Missing title, category
        }
        
        try:
            response = requests.post(f"{self.api_base}/admin/portfolio", json=invalid_data, headers=headers, timeout=10)
            
            if response.status_code == 422:
                self.log_result(
                    "Admin Portfolio - Validation",
                    True,
                    "Correctly rejected portfolio creation with missing required fields",
                    {'status_code': response.status_code}
                )
            else:
                self.log_result(
                    "Admin Portfolio - Validation",
                    False,
                    f"Expected 422, got HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Portfolio - Validation",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    # ==========================================
    # ADMIN SERVICES MANAGEMENT TESTS
    # ==========================================
    
    def test_admin_services_get_all(self):
        """Test GET /api/admin/services - get all services"""
        if not self.admin_token:
            self.log_result(
                "Admin Services - Get All",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{self.api_base}/admin/services", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result(
                        "Admin Services - Get All",
                        True,
                        f"Successfully retrieved {len(data)} services",
                        {'count': len(data), 'status_code': response.status_code}
                    )
                else:
                    self.log_result(
                        "Admin Services - Get All",
                        False,
                        f"Expected list, got {type(data)}",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Admin Services - Get All",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Services - Get All",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_services_create(self):
        """Test POST /api/admin/services - create new service"""
        if not self.admin_token:
            self.log_result(
                "Admin Services - Create Service",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        service_data = {
            "title": "AI-Powered Data Analytics",
            "description": "Transform your raw data into actionable insights with our advanced AI analytics platform",
            "icon": "📊",
            "features": [
                "Real-time data processing",
                "Predictive analytics",
                "Custom dashboard creation",
                "Automated reporting",
                "Machine learning insights"
            ]
        }
        
        try:
            response = requests.post(f"{self.api_base}/admin/services", json=service_data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('id') and data.get('title') == service_data['title']:
                    self.created_service_ids.append(data['id'])
                    self.log_result(
                        "Admin Services - Create Service",
                        True,
                        f"Successfully created service: {data['title']}",
                        {'service_id': data['id'], 'title': data['title']}
                    )
                else:
                    self.log_result(
                        "Admin Services - Create Service",
                        False,
                        "Service creation response missing required fields",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Admin Services - Create Service",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Services - Create Service",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_services_update(self):
        """Test PUT /api/admin/services/{service_id} - update service"""
        if not self.admin_token:
            self.log_result(
                "Admin Services - Update Service",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        if not self.created_service_ids:
            self.log_result(
                "Admin Services - Update Service",
                False,
                "No services available to update",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        service_id = self.created_service_ids[0]
        
        update_data = {
            "title": "Advanced AI Data Analytics & Insights",
            "description": "Enhanced AI analytics platform with real-time processing and advanced machine learning capabilities",
            "icon": "🤖",
            "features": [
                "Real-time data processing",
                "Advanced predictive analytics",
                "Custom dashboard creation",
                "Automated reporting",
                "Deep learning insights",
                "Natural language queries"
            ]
        }
        
        try:
            response = requests.put(f"{self.api_base}/admin/services/{service_id}", json=update_data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('title') == update_data['title']:
                    self.log_result(
                        "Admin Services - Update Service",
                        True,
                        f"Successfully updated service: {data['title']}",
                        {'service_id': service_id, 'new_title': data['title']}
                    )
                else:
                    self.log_result(
                        "Admin Services - Update Service",
                        False,
                        "Service update did not reflect changes",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Admin Services - Update Service",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Services - Update Service",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_services_delete(self):
        """Test DELETE /api/admin/services/{service_id} - delete service"""
        if not self.admin_token:
            self.log_result(
                "Admin Services - Delete Service",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        if not self.created_service_ids:
            self.log_result(
                "Admin Services - Delete Service",
                False,
                "No services available to delete",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        service_id = self.created_service_ids[0]
        
        try:
            response = requests.delete(f"{self.api_base}/admin/services/{service_id}", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_result(
                        "Admin Services - Delete Service",
                        True,
                        f"Successfully deleted service: {service_id}",
                        {'service_id': service_id, 'message': data.get('message')}
                    )
                    self.created_service_ids.remove(service_id)
                else:
                    self.log_result(
                        "Admin Services - Delete Service",
                        False,
                        "Delete response indicates failure",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Admin Services - Delete Service",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Services - Delete Service",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_admin_services_validation(self):
        """Test service creation with missing required fields"""
        if not self.admin_token:
            self.log_result(
                "Admin Services - Validation",
                False,
                "No admin token available for authentication",
                {}
            )
            return
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test with missing required fields
        invalid_data = {
            "icon": "🔧"
            # Missing title, description
        }
        
        try:
            response = requests.post(f"{self.api_base}/admin/services", json=invalid_data, headers=headers, timeout=10)
            
            if response.status_code == 422:
                self.log_result(
                    "Admin Services - Validation",
                    True,
                    "Correctly rejected service creation with missing required fields",
                    {'status_code': response.status_code}
                )
            else:
                self.log_result(
                    "Admin Services - Validation",
                    False,
                    f"Expected 422, got HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Admin Services - Validation",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    # ==========================================
    # PUBLIC ENDPOINTS TESTS
    # ==========================================
    
    def test_public_portfolio_endpoint(self):
        """Test GET /api/portfolio - public portfolio endpoint"""
        try:
            response = requests.get(f"{self.api_base}/portfolio", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result(
                        "Public Portfolio Endpoint",
                        True,
                        f"Successfully retrieved {len(data)} portfolio projects from public endpoint",
                        {'count': len(data), 'status_code': response.status_code}
                    )
                else:
                    self.log_result(
                        "Public Portfolio Endpoint",
                        False,
                        f"Expected list, got {type(data)}",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Public Portfolio Endpoint",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Public Portfolio Endpoint",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def test_public_services_endpoint(self):
        """Test GET /api/services - public services endpoint"""
        try:
            response = requests.get(f"{self.api_base}/services", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result(
                        "Public Services Endpoint",
                        True,
                        f"Successfully retrieved {len(data)} services from public endpoint",
                        {'count': len(data), 'status_code': response.status_code}
                    )
                else:
                    self.log_result(
                        "Public Services Endpoint",
                        False,
                        f"Expected list, got {type(data)}",
                        {'response_data': data}
                    )
            else:
                self.log_result(
                    "Public Services Endpoint",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
        except Exception as e:
            self.log_result(
                "Public Services Endpoint",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )

    def run_all_tests(self):
        """Run all backend tests"""
        print("=" * 80)
        print("SOFTGEMZ COMPREHENSIVE BACKEND TESTING SUITE")
        print("=" * 80)
        print(f"Testing API at: {self.api_base}")
        print(f"Started at: {datetime.now().isoformat()}")
        print("=" * 80)
        print()
        
        # Test API connectivity first
        self.test_api_connectivity()
        
        # Test admin authentication
        print("\n🔐 TESTING ADMIN AUTHENTICATION...")
        self.test_admin_login_valid_credentials()
        self.test_admin_login_invalid_username()
        self.test_admin_login_invalid_password()
        self.test_admin_login_missing_fields()
        
        # Test admin contacts management
        print("\n📧 TESTING ADMIN CONTACTS MANAGEMENT...")
        self.test_admin_contacts_get_all()
        self.test_admin_contacts_filter_by_status()
        self.test_admin_contacts_search()
        self.test_admin_contacts_update_status()
        self.test_admin_contacts_add_response()
        self.test_admin_contacts_export_csv()
        self.test_admin_contacts_without_auth()
        
        # Test admin dashboard stats
        print("\n📊 TESTING ADMIN DASHBOARD STATS...")
        self.test_admin_dashboard_stats()
        
        # Test admin portfolio management
        print("\n💼 TESTING ADMIN PORTFOLIO MANAGEMENT...")
        self.test_admin_portfolio_get_all()
        self.test_admin_portfolio_create()
        self.test_admin_portfolio_update()
        self.test_admin_portfolio_validation()
        self.test_admin_portfolio_delete()
        
        # Test admin services management
        print("\n🛠️ TESTING ADMIN SERVICES MANAGEMENT...")
        self.test_admin_services_get_all()
        self.test_admin_services_create()
        self.test_admin_services_update()
        self.test_admin_services_validation()
        self.test_admin_services_delete()
        
        # Test public endpoints
        print("\n🌐 TESTING PUBLIC ENDPOINTS...")
        self.test_public_portfolio_endpoint()
        self.test_public_services_endpoint()
        
        # Test contact form (existing functionality)
        print("\n📝 TESTING CONTACT FORM (EXISTING FUNCTIONALITY)...")
        self.test_valid_contact_submission()
        self.test_required_fields_only()
        self.test_missing_required_fields()
        self.test_invalid_email_formats()
        self.test_field_length_limits()
        self.test_special_characters()
        self.test_malformed_requests()
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
    tester = AdminSystemTester()
    tester.run_all_tests()