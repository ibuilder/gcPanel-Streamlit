"""
Pure Python API Layer for Highland Tower Development
FastAPI-based REST API that's completely independent of Streamlit

This creates a sustainable backend API that can serve any frontend framework
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date, datetime
import uvicorn

from .data_models import RFIStatus, Priority, Discipline
from .business_logic import highland_tower_manager
from .database_layer import db_manager

# FastAPI app instance
app = FastAPI(
    title="Highland Tower Development API",
    description="Pure Python REST API for Construction Management",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class RFICreate(BaseModel):
    subject: str = Field(..., min_length=1, max_length=500)
    description: str = Field(..., min_length=1)
    location: str
    discipline: str
    priority: str
    assigned_to: str
    cost_impact: Optional[str] = None
    schedule_impact: Optional[str] = None
    submitted_by: str = "Highland Tower Team"
    due_date: date

class RFIResponse(BaseModel):
    id: str
    number: str
    subject: str
    description: str
    location: str
    discipline: str
    priority: str
    status: str
    submitted_by: str
    assigned_to: str
    submitted_date: str
    due_date: str
    cost_impact: Optional[str]
    schedule_impact: Optional[str]
    days_open: int
    created_at: str

class ProjectHealth(BaseModel):
    overall_health_score: float
    progress_percent: float
    budget_remaining: float
    days_to_completion: int
    rfi_health: float
    active_rfis: int
    critical_issues: int

class SubcontractorResponse(BaseModel):
    id: str
    company_name: str
    contact_person: str
    email: str
    phone: str
    specialties: List[str]
    performance_rating: float
    active_projects: int
    total_contract_value: float

# API Routes
@app.get("/")
async def root():
    """API health check"""
    return {
        "message": "Highland Tower Development API",
        "status": "operational",
        "project": "45.5M Mixed-Use Development"
    }

@app.get("/api/project/health", response_model=ProjectHealth)
async def get_project_health():
    """Get comprehensive project health metrics"""
    try:
        health_data = highland_tower_manager.get_project_health_metrics()
        return ProjectHealth(**health_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rfis", response_model=List[RFIResponse])
async def get_rfis(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    discipline: Optional[str] = None
):
    """Get all RFIs with optional filtering"""
    try:
        # Use database layer for real data persistence
        rfis_data = db_manager.get_all_rfis("HTD-2024-001")
        
        # Apply filters
        if status:
            rfis_data = [rfi for rfi in rfis_data if rfi["status"] == status.lower()]
        if priority:
            rfis_data = [rfi for rfi in rfis_data if rfi["priority"] == priority.lower()]
        if discipline:
            rfis_data = [rfi for rfi in rfis_data if rfi["discipline"] == discipline.lower()]
        
        return [RFIResponse(**rfi) for rfi in rfis_data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rfis", response_model=Dict[str, str])
async def create_rfi(rfi_data: RFICreate):
    """Create new RFI"""
    try:
        # Validate enums
        try:
            discipline_enum = Discipline(rfi_data.discipline.lower().replace(" ", "_"))
            priority_enum = Priority(rfi_data.priority.lower())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid enum value: {str(e)}")
        
        # Prepare data for database
        db_data = {
            "subject": rfi_data.subject,
            "description": rfi_data.description,
            "location": rfi_data.location,
            "discipline": discipline_enum,
            "priority": priority_enum,
            "status": RFIStatus.OPEN,
            "assigned_to": rfi_data.assigned_to,
            "cost_impact": rfi_data.cost_impact,
            "schedule_impact": rfi_data.schedule_impact,
            "submitted_by": rfi_data.submitted_by,
            "submitted_date": date.today(),
            "due_date": rfi_data.due_date,
            "project_id": "HTD-2024-001"
        }
        
        result = db_manager.create_rfi(db_data)
        return {
            "message": "RFI created successfully",
            "rfi_id": result["id"],
            "rfi_number": result["number"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rfis/statistics")
async def get_rfi_statistics():
    """Get RFI statistics"""
    try:
        stats = highland_tower_manager.get_rfi_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/subcontractors", response_model=List[SubcontractorResponse])
async def get_subcontractors(specialty: Optional[str] = None):
    """Get all subcontractors with optional specialty filtering"""
    try:
        subcontractors = highland_tower_manager.get_subcontractors(specialty)
        return [
            SubcontractorResponse(
                id=sub.id,
                company_name=sub.company_name,
                contact_person=sub.contact_person,
                email=sub.email,
                phone=sub.phone,
                specialties=sub.specialties,
                performance_rating=sub.performance_rating,
                active_projects=sub.active_projects,
                total_contract_value=sub.total_contract_value
            )
            for sub in subcontractors
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/charts")
async def get_analytics_data():
    """Get analytics chart data"""
    try:
        from .ui_components import ui_components
        chart_data = ui_components.generate_analytics_charts_data()
        return chart_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/project/export")
async def export_project_data():
    """Export complete project data"""
    try:
        export_data = highland_tower_manager.export_project_data()
        return export_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize Highland Tower Development data"""
    try:
        db_manager.initialize_highland_tower_data()
        print("Highland Tower Development database initialized successfully")
    except Exception as e:
        print(f"Database initialization warning: {e}")

def run_api_server(host: str = "0.0.0.0", port: int = 8000):
    """Run the FastAPI server"""
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run_api_server()