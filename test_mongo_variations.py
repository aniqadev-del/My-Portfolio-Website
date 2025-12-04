#!/usr/bin/env python3
"""
Test different MongoDB connection string variations to diagnose the issue
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from urllib.parse import quote_plus

async def test_connection_variations():
    # Original connection string from .env
    original_url = "mongodb+srv://aniqa_db_user:2yGZWqt4QYaPePAd@cluster0.flhyyxv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    # Test variations
    variations = [
        ("Original", original_url),
        ("With database name", original_url.replace("/?", "/softgemz_database?")),
        ("URL encoded password", original_url.replace("2yGZWqt4QYaPePAd", quote_plus("2yGZWqt4QYaPePAd"))),
        ("With authSource=admin", original_url + "&authSource=admin"),
        ("Different database in URL", original_url.replace("/?", "/test?")),
    ]
    
    for name, url in variations:
        print(f"\n🔍 Testing: {name}")
        print(f"URL: {url[:50]}...{url[-30:]}")
        
        try:
            client = AsyncIOMotorClient(url)
            db = client["softgemz_database"]
            
            # Test basic connection
            collections = await db.list_collection_names()
            print(f"✅ SUCCESS! Found collections: {collections}")
            client.close()
            break
            
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            if hasattr(e, 'code'):
                print(f"   Error code: {e.code}")
    
    # Test if it's a network/IP issue
    print(f"\n🌐 Testing basic connectivity to cluster...")
    try:
        import socket
        host = "cluster0.flhyyxv.mongodb.net"
        port = 27017
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Network connectivity to {host}:{port} is working")
        else:
            print(f"❌ Cannot connect to {host}:{port} - network issue")
    except Exception as e:
        print(f"❌ Network test failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_connection_variations())