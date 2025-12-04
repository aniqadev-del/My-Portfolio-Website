#!/usr/bin/env python3
"""
Test MongoDB Atlas connection to diagnose authentication issues
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

async def test_mongo_connection():
    mongo_url = os.environ['MONGO_URL']
    db_name = os.environ['DB_NAME']
    
    print(f"Testing MongoDB connection...")
    print(f"Database name: {db_name}")
    print(f"Connection URL (masked): {mongo_url[:20]}...{mongo_url[-20:]}")
    
    try:
        # Create client
        client = AsyncIOMotorClient(mongo_url)
        
        # Get database
        db = client[db_name]
        
        # Test connection by listing collections
        print("Attempting to list collections...")
        collections = await db.list_collection_names()
        print(f"✅ Successfully connected! Found {len(collections)} collections: {collections}")
        
        # Test a simple operation
        print("Testing a simple count operation...")
        contact_count = await db.contact_submissions.count_documents({})
        print(f"✅ Contact submissions count: {contact_count}")
        
        # Test admin stats operation
        print("Testing admin stats operations...")
        all_contacts = await db.contact_submissions.find().to_list(10000)
        portfolio_count = await db.portfolio_projects.count_documents({})
        services_count = await db.services.count_documents({})
        
        print(f"✅ All contacts: {len(all_contacts)}")
        print(f"✅ Portfolio projects: {portfolio_count}")
        print(f"✅ Services: {services_count}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        
        # Try with authSource=admin
        try:
            print("\nTrying with authSource=admin...")
            mongo_url_with_auth = mongo_url
            if "authSource" not in mongo_url_with_auth:
                separator = "&" if "?" in mongo_url_with_auth else "?"
                mongo_url_with_auth += f"{separator}authSource=admin"
            
            client = AsyncIOMotorClient(mongo_url_with_auth)
            db = client[db_name]
            collections = await db.list_collection_names()
            print(f"✅ Success with authSource=admin! Collections: {collections}")
            client.close()
            
        except Exception as e2:
            print(f"❌ Still failed with authSource=admin: {str(e2)}")

if __name__ == "__main__":
    asyncio.run(test_mongo_connection())