#!/usr/bin/env python3
"""
Migrate mock data from frontend to database
This script will populate the database with initial portfolio and services data
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime
import uuid

# Load environment variables
load_dotenv('/app/backend/.env')

mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

# Mock data
services_data = [
    {
        "id": str(uuid.uuid4()),
        "title": "Process Automation",
        "description": "Streamline repetitive tasks with intelligent workflow automation using Power Automate and custom solutions.",
        "icon": "Zap",
        "features": [
            "Document processing automation",
            "Email & notification workflows", 
            "Data entry elimination",
            "Compliance management"
        ],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "AI-Powered Analytics",
        "description": "Transform your data into actionable insights with custom AI models and predictive analytics.",
        "icon": "Brain",
        "features": [
            "Business intelligence dashboards",
            "Predictive modeling",
            "Anomaly detection",
            "Real-time reporting"
        ],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Document Intelligence",
        "description": "Extract and process information from unstructured documents using advanced AI techniques.",
        "icon": "FileText",
        "features": [
            "Automated data extraction",
            "Document classification",
            "Template standardization",
            "Quality assurance workflows"
        ],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Custom Software Development",
        "description": "Build tailored software solutions that integrate seamlessly with your existing systems.",
        "icon": "Code",
        "features": [
            "Web applications",
            "API integrations",
            "Database optimization",
            "System modernization"
        ],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
]

portfolio_data = [
    {
        "id": str(uuid.uuid4()),
        "title": "Calibration Certificate Automation",
        "category": "Process Automation",
        "description": "Eliminated repetitive manual work in calibration management by building a Power Automate workflow that generated 25+ calibration certificates monthly.",
        "challenge": "Manual data entry for calibration certificates was time-consuming and error-prone",
        "solution": "Built a Power Automate workflow that pulled data directly from a master sheet (instrument ID, model, manufacturer, reference values) and prefilled templates automatically.",
        "results": "Reduced manual data entry by 90%, ensured compliance, and saved technicians hours every month.",
        "technologies": ["Power Automate", "Microsoft 365", "Data Integration"],
        "image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&h=400&fit=crop",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Weekly Calibration Expiry Alerts",
        "category": "Compliance Management",
        "description": "Ensured timely calibration compliance across hundreds of instruments with automated alert system.",
        "challenge": "Risk of missed calibrations due to lack of proactive monitoring",
        "solution": "Created a Power Automate solution that scanned the calibration master sheet weekly, identified upcoming expiry dates, and sent proactive email alerts.",
        "results": "Improved audit readiness, reduced missed calibrations, and strengthened operational reliability.",
        "technologies": ["Power Automate", "Email Integration", "Data Analytics"],
        "image": "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=600&h=400&fit=crop",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Document Formatting Automation",
        "category": "AI-Assisted Processing",
        "description": "Standardized unstructured lab reports into consistent templates using AI-driven document processing.",
        "challenge": "Lab reports came in various formats, requiring manual standardization",
        "solution": "Designed an AI-driven document processing workflow that extracted key values from raw lab documents and reformatted them into ready-to-use certificate templates.",
        "results": "Eliminated manual copy-pasting, improved consistency, and accelerated reporting turnaround.",
        "technologies": ["AI Document Processing", "Template Engine", "Data Extraction"],
        "image": "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=600&h=400&fit=crop",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Automated Invoicing & Reminders",
        "category": "Business Process Automation",
        "description": "Simplified client billing and follow-ups with intelligent invoicing workflows.",
        "challenge": "Manual invoice generation and follow-ups were consuming admin resources",
        "solution": "Implemented a workflow where invoices were automatically generated from client bookings and sent via email, with payment reminders and cancellation rules if overdue.",
        "results": "Reduced admin workload, improved payment timelines, and created a seamless client experience.",
        "technologies": ["Workflow Automation", "Email Marketing", "Payment Integration"],
        "image": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=600&h=400&fit=crop",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Business Intelligence Dashboard",
        "category": "AI-Powered Analytics",
        "description": "Provided management with real-time visibility into operations using AI-powered insights.",
        "challenge": "Management lacked real-time visibility into operational performance",
        "solution": "Developed a Power BI dashboard integrated with Microsoft 365 and Power Automate, providing predictive insights and highlighting anomalies using AI models.",
        "results": "Enabled smarter decision-making with real-time analytics and reduced reliance on manual reporting.",
        "technologies": ["Power BI", "AI Models", "Microsoft 365", "Predictive Analytics"],
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=400&fit=crop",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
]

async def migrate_data():
    print("=" * 80)
    print("MIGRATING MOCK DATA TO DATABASE")
    print("=" * 80)
    print()
    
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        
        print("✅ Connected to MongoDB")
        
        # Check existing data
        existing_services = await db.services.count_documents({})
        existing_portfolio = await db.portfolio_projects.count_documents({})
        
        print(f"ℹ️  Existing services: {existing_services}")
        print(f"ℹ️  Existing portfolio projects: {existing_portfolio}")
        print()
        
        # Migrate Services
        if existing_services == 0:
            print("📤 Migrating services...")
            result = await db.services.insert_many(services_data)
            print(f"✅ Inserted {len(result.inserted_ids)} services")
        else:
            print("ℹ️  Services already exist, skipping migration")
        
        print()
        
        # Migrate Portfolio
        if existing_portfolio == 0:
            print("📤 Migrating portfolio projects...")
            result = await db.portfolio_projects.insert_many(portfolio_data)
            print(f"✅ Inserted {len(result.inserted_ids)} portfolio projects")
        else:
            print("ℹ️  Portfolio projects already exist, skipping migration")
        
        print()
        
        # Verify data
        final_services = await db.services.count_documents({})
        final_portfolio = await db.portfolio_projects.count_documents({})
        
        print("=" * 80)
        print("MIGRATION COMPLETE")
        print("=" * 80)
        print(f"Total services in database: {final_services}")
        print(f"Total portfolio projects in database: {final_portfolio}")
        print()
        print("✅ Frontend can now fetch data from backend APIs!")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(migrate_data())
    exit(0 if success else 1)
