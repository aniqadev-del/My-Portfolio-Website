from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timedelta
import re
import threading
import time
import requests
import jwt
from passlib.context import CryptContext
import csv
import io
from fastapi.responses import StreamingResponse

# ---------------------
# Load environment variables
# ---------------------
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# ---------------------
# FastAPI app & router
# ---------------------
app = FastAPI()
api_router = APIRouter(prefix="/api")
@app.get("/")
async def root():
    return {"message": "Backend is alive!"}

# ---------------------
# Logging
# ---------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ---------------------
# Models
# ---------------------
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class ContactSubmission(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    company: str = ""
    phone: str = ""
    projectType: str = ""
    message: str
    status: str = "new"
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class ContactSubmissionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Full name is required")
    email: str = Field(..., min_length=1, max_length=255, description="Valid email is required")
    company: str = Field("", max_length=100, description="Company name (optional)")
    phone: str = Field("", max_length=20, description="Phone number (optional)")
    projectType: str = Field("", max_length=50, description="Project type (optional)")
    message: str = Field(..., min_length=1, max_length=2000, description="Message is required")

class ContactResponse(BaseModel):
    success: bool
    message: str
    id: str = None

# ---------------------
# API Routes
# ---------------------
@api_router.get("/")
async def api_root():
    return {"message": "API is alive!"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_obj = StatusCheck(**input.dict())
    await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**sc) for sc in status_checks]

@api_router.post("/contact", response_model=ContactResponse)
async def submit_contact_form(contact_data: ContactSubmissionCreate):
    try:
        # Validate email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, contact_data.email):
            return ContactResponse(success=False, message="Please provide a valid email address")
        
        submission = ContactSubmission(
            name=contact_data.name.strip(),
            email=contact_data.email.strip().lower(),
            company=contact_data.company.strip(),
            phone=contact_data.phone.strip(),
            projectType=contact_data.projectType,
            message=contact_data.message.strip()
        )
        
        result = await db.contact_submissions.insert_one(submission.dict())
        if result.inserted_id:
            logger.info(f"New contact submission from {submission.email}")
            return ContactResponse(success=True, message="Thank you! We'll get back to you within 24 hours.", id=submission.id)
        else:
            logger.error("Failed to insert contact submission")
            return ContactResponse(success=False, message="Failed to submit form. Please try again.")
    except Exception as e:
        logger.error(f"Error submitting contact form: {str(e)}")
        return ContactResponse(success=False, message="An error occurred. Please try again later.")

@api_router.get("/contact", response_model=List[ContactSubmission])
async def get_contact_submissions():
    try:
        submissions = await db.contact_submissions.find().sort("createdAt", -1).to_list(1000)
        return [ContactSubmission(**s) for s in submissions]
    except Exception as e:
        logger.error(f"Error fetching contact submissions: {str(e)}")
        return []

# Include router
app.include_router(api_router)

# ---------------------
# CORS middleware (restricted via environment variable)
# ---------------------
cors_origins = os.environ.get('CORS_ORIGINS', '').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,      # e.g., ["https://softgemz.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------
# Keep backend awake thread
# ---------------------
def keep_backend_awake():
    backend_url = os.environ.get("BACKEND_URL")  # just the root now
    while True:
        try:
            response = requests.get(backend_url)
            logger.info(f"[Ping] {backend_url} - Status: {response.status_code} at {datetime.utcnow().isoformat()}")
        except Exception as e:
            logger.error(f"[Ping] Failed to ping backend: {e}")
        time.sleep(14 * 60)  # 14 minutes



threading.Thread(target=keep_backend_awake, daemon=True).start()

# ---------------------
# Shutdown event
# ---------------------
@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
