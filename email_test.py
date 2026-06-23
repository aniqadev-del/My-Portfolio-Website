#!/usr/bin/env python3
"""
Email Sending Test for Admin Response Functionality
Tests the email sending functionality when admin responds to contacts
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

class EmailTester:
    def __init__(self):
        self.api_base = API_BASE
        self.admin_token = None
        
    def log_result(self, test_name, success, message, details=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details:
            print(f"   Details: {details}")
        print()

    def admin_login(self):
        """Login as admin to get JWT token"""
        login_data = {
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        }
        
        try:
            response = requests.post(f"{self.api_base}/admin/login", json=login_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('access_token'):
                    self.admin_token = data['access_token']
                    self.log_result(
                        "Admin Login",
                        True,
                        f"Successfully logged in as {data.get('username')}",
                        {'token_received': True}
                    )
                    return True
                else:
                    self.log_result(
                        "Admin Login",
                        False,
                        "Login response missing token",
                        {'response_data': data}
                    )
                    return False
            else:
                self.log_result(
                    "Admin Login",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
                return False
        except Exception as e:
            self.log_result(
                "Admin Login",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )
            return False

    def get_existing_contacts(self):
        """Get existing contacts from the database"""
        if not self.admin_token:
            self.log_result(
                "Get Existing Contacts",
                False,
                "No admin token available",
                {}
            )
            return []
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{self.api_base}/admin/contacts", headers=headers, timeout=10)
            
            if response.status_code == 200:
                contacts = response.json()
                self.log_result(
                    "Get Existing Contacts",
                    True,
                    f"Successfully retrieved {len(contacts)} contacts",
                    {'count': len(contacts)}
                )
                return contacts
            else:
                self.log_result(
                    "Get Existing Contacts",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
                return []
        except Exception as e:
            self.log_result(
                "Get Existing Contacts",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )
            return []

    def test_admin_response_with_email(self, contact_id, contact_email, contact_name):
        """Test admin response with email sending"""
        if not self.admin_token:
            self.log_result(
                "Admin Response with Email",
                False,
                "No admin token available",
                {}
            )
            return False
            
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Admin response as specified in the request
        admin_response = "Thank you for contacting SoftGemZ! We have received your inquiry and our team will get back to you within 24 hours with more details about our AI automation solutions. Best regards, SoftGemZ Team"
        
        update_data = {
            "adminResponse": admin_response,
            "status": "in-progress"
        }
        
        try:
            print(f"Sending admin response to contact {contact_id} ({contact_email})...")
            response = requests.put(
                f"{self.api_base}/admin/contacts/{contact_id}", 
                json=update_data, 
                headers=headers, 
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('adminResponse') and data.get('status') == 'in-progress':
                    self.log_result(
                        "Admin Response with Email - API Success",
                        True,
                        f"Successfully updated contact {contact_id} with admin response",
                        {
                            'contact_id': contact_id,
                            'contact_email': contact_email,
                            'status': data.get('status'),
                            'responded_by': data.get('respondedBy'),
                            'responded_at': data.get('respondedAt')
                        }
                    )
                    return True
                else:
                    self.log_result(
                        "Admin Response with Email - API Success",
                        False,
                        "Response not saved correctly to database",
                        {'response_data': data}
                    )
                    return False
            else:
                self.log_result(
                    "Admin Response with Email - API Success",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {'status_code': response.status_code}
                )
                return False
        except Exception as e:
            self.log_result(
                "Admin Response with Email - API Success",
                False,
                f"Request failed: {str(e)}",
                {'error': str(e)}
            )
            return False

    def check_email_logs(self):
        """Check backend logs for email sending confirmation"""
        try:
            # Check recent backend logs for email sending messages
            import subprocess
            result = subprocess.run(
                ['tail', '-n', '50', '/var/log/supervisor/backend.err.log'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            log_content = result.stdout
            
            # Look for email success messages
            email_success_found = False
            email_error_found = False
            
            if "Email sent successfully" in log_content:
                email_success_found = True
            
            if "Failed to send email" in log_content or "Email sending error" in log_content:
                email_error_found = True
            
            if email_success_found:
                self.log_result(
                    "Email Sending Verification",
                    True,
                    "Found 'Email sent successfully' message in backend logs",
                    {'log_check': 'success_message_found'}
                )
                return True
            elif email_error_found:
                self.log_result(
                    "Email Sending Verification",
                    False,
                    "Found email sending error messages in backend logs",
                    {'log_check': 'error_message_found'}
                )
                return False
            else:
                self.log_result(
                    "Email Sending Verification",
                    False,
                    "No email sending messages found in recent backend logs",
                    {'log_check': 'no_email_messages'}
                )
                return False
                
        except Exception as e:
            self.log_result(
                "Email Sending Verification",
                False,
                f"Failed to check logs: {str(e)}",
                {'error': str(e)}
            )
            return False

    def run_email_test(self):
        """Run the complete email sending test"""
        print("=" * 80)
        print("EMAIL SENDING FUNCTIONALITY TEST")
        print("=" * 80)
        print()
        
        # Step 1: Admin Login
        if not self.admin_login():
            print("❌ Cannot proceed without admin authentication")
            return False
        
        # Step 2: Get existing contacts
        contacts = self.get_existing_contacts()
        if not contacts:
            print("❌ No contacts available to test email sending")
            return False
        
        # Step 3: Pick the first contact
        first_contact = contacts[0]
        contact_id = first_contact.get('id')
        contact_email = first_contact.get('email')
        contact_name = first_contact.get('name')
        
        print(f"Selected contact for testing:")
        print(f"  ID: {contact_id}")
        print(f"  Name: {contact_name}")
        print(f"  Email: {contact_email}")
        print()
        
        # Step 4: Send admin response with email
        if not self.test_admin_response_with_email(contact_id, contact_email, contact_name):
            print("❌ Failed to send admin response")
            return False
        
        # Step 5: Wait a moment for email processing
        print("Waiting 3 seconds for email processing...")
        time.sleep(3)
        
        # Step 6: Check logs for email confirmation
        email_sent = self.check_email_logs()
        
        # Final summary
        print("=" * 80)
        print("EMAIL TEST SUMMARY")
        print("=" * 80)
        
        if email_sent:
            print("✅ EMAIL SENDING TEST PASSED")
            print("   - Admin response saved to database")
            print("   - Email sent successfully to contact")
            print("   - Email confirmation found in logs")
        else:
            print("❌ EMAIL SENDING TEST FAILED")
            print("   - Admin response may have been saved to database")
            print("   - Email sending failed or no confirmation in logs")
            print("   - Check SMTP configuration and credentials")
        
        return email_sent

if __name__ == "__main__":
    tester = EmailTester()
    success = tester.run_email_test()
    exit(0 if success else 1)