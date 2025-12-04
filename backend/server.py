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
# Security Configuration
# ---------------------
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Predefined admin credentials - Change these in production
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")  # Hash this in production
ADMIN_PASSWORD_HASH = pwd_context.hash(ADMIN_PASSWORD)

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
    status: str = "new"  # new, in-progress, completed
    adminResponse: str = ""
    respondedAt: Optional[datetime] = None
    respondedBy: str = ""
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

# Admin Models
class AdminLogin(BaseModel):
    username: str
    password: str

class AdminToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str

class AdminContactUpdate(BaseModel):
    status: Optional[str] = None
    adminResponse: Optional[str] = None

class Portfolio(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    category: str
    image: str
    technologies: List[str] = []
    challenge: str = ""
    solution: str = ""
    results: str = ""
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class PortfolioCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    category: str = Field(..., min_length=1, max_length=100)
    image: str = ""
    technologies: List[str] = []
    challenge: str = Field("", max_length=1000)
    solution: str = Field("", max_length=1000)
    results: str = Field("", max_length=500)

class Service(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    icon: str = ""
    features: List[str] = []
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class ServiceCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    icon: str = ""
    features: List[str] = []

class DashboardStats(BaseModel):
    totalContacts: int
    newContacts: int
    inProgressContacts: int
    completedContacts: int
    totalPortfolioProjects: int
    totalServices: int
    recentContacts: List[ContactSubmission]

# ---------------------
# Authentication Helpers
# ---------------------
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

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

# ---------------------
# Admin Authentication Routes
# ---------------------
@api_router.post("/admin/login", response_model=AdminToken)
async def admin_login(credentials: AdminLogin):
    try:
        if credentials.username != ADMIN_USERNAME:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        if not verify_password(credentials.password, ADMIN_PASSWORD_HASH):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        access_token = create_access_token(data={"sub": credentials.username})
        logger.info(f"Admin {credentials.username} logged in successfully")
        
        return AdminToken(
            access_token=access_token,
            token_type="bearer",
            username=credentials.username
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error during admin login: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# ---------------------
# Admin Contact Management Routes
# ---------------------
@api_router.get("/admin/contacts", response_model=List[ContactSubmission])
async def admin_get_contacts(
    status: Optional[str] = None,
    search: Optional[str] = None,
    current_admin: str = Depends(get_current_admin)
):
    try:
        query = {}
        if status and status != "all":
            query["status"] = status
        
        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}},
                {"company": {"$regex": search, "$options": "i"}},
                {"message": {"$regex": search, "$options": "i"}}
            ]
        
        contacts = await db.contact_submissions.find(query).sort("createdAt", -1).to_list(1000)
        return [ContactSubmission(**c) for c in contacts]
    except Exception as e:
        logger.error(f"Error fetching contacts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch contacts")

@api_router.put("/admin/contacts/{contact_id}")
async def admin_update_contact(
    contact_id: str,
    update_data: AdminContactUpdate,
    current_admin: str = Depends(get_current_admin)
):
    try:
        contact = await db.contact_submissions.find_one({"id": contact_id})
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        update_fields = {"updatedAt": datetime.utcnow()}
        
        if update_data.status:
            update_fields["status"] = update_data.status
        
        if update_data.adminResponse:
            update_fields["adminResponse"] = update_data.adminResponse
            update_fields["respondedAt"] = datetime.utcnow()
            update_fields["respondedBy"] = current_admin
        
        result = await db.contact_submissions.update_one(
            {"id": contact_id},
            {"$set": update_fields}
        )
        
        if result.modified_count > 0:
            updated_contact = await db.contact_submissions.find_one({"id": contact_id})
            logger.info(f"Admin {current_admin} updated contact {contact_id}")
            return ContactSubmission(**updated_contact)
        else:
            raise HTTPException(status_code=500, detail="Failed to update contact")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error updating contact: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.get("/admin/contacts/export")
async def admin_export_contacts(current_admin: str = Depends(get_current_admin)):
    try:
        contacts = await db.contact_submissions.find().sort("createdAt", -1).to_list(10000)
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            "ID", "Name", "Email", "Company", "Phone", "Project Type", 
            "Message", "Status", "Admin Response", "Created At", 
            "Responded At", "Responded By"
        ])
        
        # Write data
        for contact in contacts:
            writer.writerow([
                contact.get("id", ""),
                contact.get("name", ""),
                contact.get("email", ""),
                contact.get("company", ""),
                contact.get("phone", ""),
                contact.get("projectType", ""),
                contact.get("message", ""),
                contact.get("status", ""),
                contact.get("adminResponse", ""),
                contact.get("createdAt", ""),
                contact.get("respondedAt", ""),
                contact.get("respondedBy", "")
            ])
        
        output.seek(0)
        logger.info(f"Admin {current_admin} exported {len(contacts)} contacts")
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=contacts_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
    except Exception as e:
        logger.error(f"Error exporting contacts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to export contacts")

# ---------------------
# Admin Dashboard Stats Route
# ---------------------
@api_router.get("/admin/stats", response_model=DashboardStats)
async def admin_get_stats(current_admin: str = Depends(get_current_admin)):
    try:
        all_contacts = await db.contact_submissions.find().to_list(10000)
        total_contacts = len(all_contacts)
        new_contacts = len([c for c in all_contacts if c.get("status") == "new"])
        in_progress = len([c for c in all_contacts if c.get("status") == "in-progress"])
        completed = len([c for c in all_contacts if c.get("status") == "completed"])
        
        portfolio_count = await db.portfolio_projects.count_documents({})
        services_count = await db.services.count_documents({})
        
        recent_contacts = await db.contact_submissions.find().sort("createdAt", -1).limit(5).to_list(5)
        
        return DashboardStats(
            totalContacts=total_contacts,
            newContacts=new_contacts,
            inProgressContacts=in_progress,
            completedContacts=completed,
            totalPortfolioProjects=portfolio_count,
            totalServices=services_count,
            recentContacts=[ContactSubmission(**c) for c in recent_contacts]
        )
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch statistics")

# ---------------------
# Admin Portfolio Management Routes
# ---------------------
@api_router.get("/admin/portfolio", response_model=List[Portfolio])
async def admin_get_portfolio(current_admin: str = Depends(get_current_admin)):
    try:
        projects = await db.portfolio_projects.find().sort("createdAt", -1).to_list(1000)
        return [Portfolio(**p) for p in projects]
    except Exception as e:
        logger.error(f"Error fetching portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch portfolio projects")

@api_router.post("/admin/portfolio", response_model=Portfolio)
async def admin_create_portfolio(
    project_data: PortfolioCreate,
    current_admin: str = Depends(get_current_admin)
):
    try:
        project = Portfolio(**project_data.dict())
        result = await db.portfolio_projects.insert_one(project.dict())
        if result.inserted_id:
            logger.info(f"Admin {current_admin} created portfolio project {project.id}")
            return project
        else:
            raise HTTPException(status_code=500, detail="Failed to create project")
    except Exception as e:
        logger.error(f"Error creating portfolio project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.put("/admin/portfolio/{project_id}", response_model=Portfolio)
async def admin_update_portfolio(
    project_id: str,
    project_data: PortfolioCreate,
    current_admin: str = Depends(get_current_admin)
):
    try:
        project = await db.portfolio_projects.find_one({"id": project_id})
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        update_fields = project_data.dict()
        update_fields["updatedAt"] = datetime.utcnow()
        
        result = await db.portfolio_projects.update_one(
            {"id": project_id},
            {"$set": update_fields}
        )
        
        if result.modified_count > 0:
            updated_project = await db.portfolio_projects.find_one({"id": project_id})
            logger.info(f"Admin {current_admin} updated portfolio project {project_id}")
            return Portfolio(**updated_project)
        else:
            raise HTTPException(status_code=500, detail="Failed to update project")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error updating portfolio project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.delete("/admin/portfolio/{project_id}")
async def admin_delete_portfolio(
    project_id: str,
    current_admin: str = Depends(get_current_admin)
):
    try:
        result = await db.portfolio_projects.delete_one({"id": project_id})
        if result.deleted_count > 0:
            logger.info(f"Admin {current_admin} deleted portfolio project {project_id}")
            return {"success": True, "message": "Project deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Project not found")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error deleting portfolio project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# ---------------------
# Admin Services Management Routes
# ---------------------
@api_router.get("/admin/services", response_model=List[Service])
async def admin_get_services(current_admin: str = Depends(get_current_admin)):
    try:
        services = await db.services.find().sort("createdAt", -1).to_list(1000)
        return [Service(**s) for s in services]
    except Exception as e:
        logger.error(f"Error fetching services: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch services")

@api_router.post("/admin/services", response_model=Service)
async def admin_create_service(
    service_data: ServiceCreate,
    current_admin: str = Depends(get_current_admin)
):
    try:
        service = Service(**service_data.dict())
        result = await db.services.insert_one(service.dict())
        if result.inserted_id:
            logger.info(f"Admin {current_admin} created service {service.id}")
            return service
        else:
            raise HTTPException(status_code=500, detail="Failed to create service")
    except Exception as e:
        logger.error(f"Error creating service: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.put("/admin/services/{service_id}", response_model=Service)
async def admin_update_service(
    service_id: str,
    service_data: ServiceCreate,
    current_admin: str = Depends(get_current_admin)
):
    try:
        service = await db.services.find_one({"id": service_id})
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        update_fields = service_data.dict()
        update_fields["updatedAt"] = datetime.utcnow()
        
        result = await db.services.update_one(
            {"id": service_id},
            {"$set": update_fields}
        )
        
        if result.modified_count > 0:
            updated_service = await db.services.find_one({"id": service_id})
            logger.info(f"Admin {current_admin} updated service {service_id}")
            return Service(**updated_service)
        else:
            raise HTTPException(status_code=500, detail="Failed to update service")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error updating service: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.delete("/admin/services/{service_id}")
async def admin_delete_service(
    service_id: str,
    current_admin: str = Depends(get_current_admin)
):
    try:
        result = await db.services.delete_one({"id": service_id})
        if result.deleted_count > 0:
            logger.info(f"Admin {current_admin} deleted service {service_id}")
            return {"success": True, "message": "Service deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Service not found")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error deleting service: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# ---------------------
# Public Portfolio Route (for frontend to fetch)
# ---------------------
@api_router.get("/portfolio", response_model=List[Portfolio])
async def get_portfolio():
    try:
        projects = await db.portfolio_projects.find().sort("createdAt", -1).to_list(1000)
        return [Portfolio(**p) for p in projects]
    except Exception as e:
        logger.error(f"Error fetching portfolio: {str(e)}")
        return []

# ---------------------
# Public Services Route (for frontend to fetch)
# ---------------------
@api_router.get("/services", response_model=List[Service])
async def get_services():
    try:
        services = await db.services.find().sort("createdAt", -1).to_list(1000)
        return [Service(**s) for s in services]
    except Exception as e:
        logger.error(f"Error fetching services: {str(e)}")
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
