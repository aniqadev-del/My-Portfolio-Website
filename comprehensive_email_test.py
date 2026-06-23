#!/usr/bin/env python3
"""
Comprehensive Email Sending Test - Test with multiple contacts
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

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def get_admin_token():
    """Get admin JWT token"""
    login_data = {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    
    response = requests.post(f"{API_BASE}/admin/login", json=login_data, timeout=10)
    if response.status_code == 200:
        data = response.json()
        return data.get('access_token')
    return None

def get_contacts(token):
    """Get all contacts"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE}/admin/contacts", headers=headers, timeout=10)
    if response.status_code == 200:
        return response.json()
    return []

def send_admin_response(token, contact_id, admin_response, status="in-progress"):
    """Send admin response to a contact"""
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {
        "adminResponse": admin_response,
        "status": status
    }
    
    response = requests.put(
        f"{API_BASE}/admin/contacts/{contact_id}", 
        json=update_data, 
        headers=headers, 
        timeout=15
    )
    
    return response.status_code == 200, response

def check_recent_email_logs():
    """Check for recent email sending logs"""
    try:
        import subprocess
        result = subprocess.run(
            ['tail', '-n', '10', '/var/log/supervisor/backend.err.log'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        log_content = result.stdout
        return "Email sent successfully" in log_content
    except:
        return False

def main():
    print("=" * 80)
    print("COMPREHENSIVE EMAIL SENDING TEST")
    print("=" * 80)
    print()
    
    # Get admin token
    token = get_admin_token()
    if not token:
        print("❌ Failed to get admin token")
        return False
    
    print("✅ Admin authentication successful")
    
    # Get contacts
    contacts = get_contacts(token)
    if not contacts:
        print("❌ No contacts available for testing")
        return False
    
    print(f"✅ Retrieved {len(contacts)} contacts")
    
    # Find contacts that haven't been responded to yet or have minimal responses
    available_contacts = []
    for contact in contacts:
        if not contact.get('adminResponse') or len(contact.get('adminResponse', '')) < 50:
            available_contacts.append(contact)
    
    if not available_contacts:
        print("ℹ️  All contacts already have responses, using first contact for re-testing")
        available_contacts = contacts[:1]
    
    print(f"✅ Found {len(available_contacts)} contacts available for testing")
    print()
    
    # Test email sending with the first available contact
    test_contact = available_contacts[0]
    contact_id = test_contact.get('id')
    contact_email = test_contact.get('email')
    contact_name = test_contact.get('name')
    
    print(f"Testing email sending with:")
    print(f"  ID: {contact_id}")
    print(f"  Name: {contact_name}")
    print(f"  Email: {contact_email}")
    print()
    
    # Send admin response
    admin_response = "Thank you for contacting SoftGemZ! We have received your inquiry and our team will get back to you within 24 hours with more details about our AI automation solutions. Best regards, SoftGemZ Team"
    
    print("Sending admin response...")
    success, response = send_admin_response(token, contact_id, admin_response)
    
    if success:
        print("✅ Admin response API call successful")
        
        # Wait for email processing
        print("Waiting 3 seconds for email processing...")
        time.sleep(3)
        
        # Check logs
        if check_recent_email_logs():
            print("✅ Email sending confirmed in logs")
            
            # Verify database update
            updated_contacts = get_contacts(token)
            updated_contact = None
            for contact in updated_contacts:
                if contact.get('id') == contact_id:
                    updated_contact = contact
                    break
            
            if updated_contact and updated_contact.get('adminResponse'):
                print("✅ Admin response saved to database")
                print()
                print("=" * 80)
                print("EMAIL SENDING TEST RESULTS")
                print("=" * 80)
                print("✅ ALL TESTS PASSED")
                print("   1. Admin authentication: SUCCESS")
                print("   2. Contact retrieval: SUCCESS")
                print("   3. Admin response API: SUCCESS")
                print("   4. Email sending: SUCCESS")
                print("   5. Database update: SUCCESS")
                print()
                print("Email functionality is working correctly!")
                return True
            else:
                print("❌ Admin response not found in database")
        else:
            print("❌ No email sending confirmation found in logs")
    else:
        print(f"❌ Admin response API call failed: {response.status_code}")
    
    print()
    print("=" * 80)
    print("EMAIL SENDING TEST RESULTS")
    print("=" * 80)
    print("❌ SOME TESTS FAILED")
    print("   Check SMTP configuration and email credentials")
    return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)