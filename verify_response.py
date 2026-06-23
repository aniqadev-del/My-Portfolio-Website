#!/usr/bin/env python3
"""
Verify that the admin response was saved to database
"""

import requests
import json
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

def verify_contact_response():
    """Verify the contact response was saved"""
    token = get_admin_token()
    if not token:
        print("❌ Failed to get admin token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get all contacts
    response = requests.get(f"{API_BASE}/admin/contacts", headers=headers, timeout=10)
    if response.status_code == 200:
        contacts = response.json()
        
        # Find the contact we just responded to
        target_contact = None
        for contact in contacts:
            if contact.get('email') == 'jose.maria@example-company.co.uk':
                target_contact = contact
                break
        
        if target_contact:
            print("✅ Contact found in database:")
            print(f"   Name: {target_contact.get('name')}")
            print(f"   Email: {target_contact.get('email')}")
            print(f"   Status: {target_contact.get('status')}")
            print(f"   Admin Response: {target_contact.get('adminResponse')[:100]}...")
            print(f"   Responded By: {target_contact.get('respondedBy')}")
            print(f"   Responded At: {target_contact.get('respondedAt')}")
            
            # Verify the response contains our expected text
            expected_text = "Thank you for contacting SoftGemZ!"
            if expected_text in target_contact.get('adminResponse', ''):
                print("✅ Admin response correctly saved to database")
            else:
                print("❌ Admin response not found or incorrect")
        else:
            print("❌ Target contact not found in database")
    else:
        print(f"❌ Failed to get contacts: HTTP {response.status_code}")

if __name__ == "__main__":
    verify_contact_response()