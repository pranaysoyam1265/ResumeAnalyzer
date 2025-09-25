from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import tempfile
from pathlib import Path
import time
import logging

from config import Config
from resume_parser import ResumeParser
from gap_analyzer import JobRoleManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize
config = Config()
app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
parser = ResumeParser(config)
job_manager = JobRoleManager(config)

# Pydantic models for request/response validation
class JobContext(BaseModel):
    roleId: str = Field(..., description="Target job role ID")
    title: Optional[str] = Field(None, description="Job title")

class UserPreferences(BaseModel):
    targetRoleId: Optional[str] = Field(None, description="Target role ID")
    learningStyle: Optional[str] = Field("mixed", description="Learning style preference")
    budgetLimit: Optional[float] = Field(1000, description="Budget limit for courses")
    timeLimit: Optional[int] = Field(100, description="Time limit per month (hours)")
    hoursPerWeek: Optional[int] = Field(10, description="Available hours per week")

class ResumeAnalysisRequest(BaseModel):
    resumeText: str = Field(..., description="Resume text content")
    jobContext: Optional[JobContext] = Field(None, description="Job context for analysis")
    userPrefs: Optional[UserPreferences] = Field(None, description="User preferences")
    phase: Optional[int] = Field(1, description="Analysis phase (1-3)", ge=1, le=3)

class SkillItem(BaseModel):
    id: str
    name: str
    category: str
    score: int
    level: str
    confidence: float
    evidence: List[Dict[str, Any]]

class GapItem(BaseModel):
    skillId: str
    skillName: str
    targetLevel: str
    currentLevel: str
    priority: int
    rationale: str

class RecommendationItem(BaseModel):
    id: str
    title: str
    provider: str
    type: str
    difficulty: str
    estimatedHours: float
    rating: float
    price: float
    link: str
    reason: str

class LearningPath(BaseModel):
    totalHours: float
    estimatedWeeks: int
    steps: List[Dict[str, Any]]

class Summary(BaseModel):
    strengths: List[str]
    improvements: List[str]
    profileSummary: str

class ResumeAnalysisResponse(BaseModel):
    version: str
    skills: List[SkillItem]
    gaps: Optional[List[GapItem]] = None
    recommendations: Optional[List[RecommendationItem]] = None
    learningPath: Optional[LearningPath] = None
    summary: Optional[Summary] = None
    matchScore: Optional[Dict[str, Any]] = None
    meta: Dict[str, Any]

# API Endpoints

@app.get("/", summary="Root endpoint")
async def root():
    """Welcome message and API information"""
    return {
        "message": "Resume Analyzer API",
        "version": config.API_VERSION,
        "description": config.API_DESCRIPTION,
        "endpoints": {
            "analyze_text": "/api/v1/analyze-resume",
            "analyze_file": "/api/v1/analyze-resume-file", 
            "job_roles": "/api/v1/job-roles",
            "health": "/api/v1/health"
        }
    }

@app.get("/api/v1/health", summary="Health check")
async def health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "version": config.API_VERSION,
        "timestamp": int(time.time())
    }

@app.get("/api/v1/job-roles", summary="Get available job roles")
async def get_job_roles():
    """Get list of available job roles for analysis"""
    try:
        roles = job_manager.list_available_roles()
        return {
            "roles": roles,
            "total": len(roles)
        }
    except Exception as e:
        logger.error(f"Error getting job roles: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze-resume", 
          response_model=Dict[str, Any],
          summary="Analyze resume from text")
async def analyze_resume_text(request: ResumeAnalysisRequest):
    """
    Analyze resume from text input
    
    - **Phase 1**: Extract skills only
    - **Phase 2**: Extract skills + gap analysis (requires jobContext)
    - **Phase 3**: Complete analysis with recommendations (requires jobContext)
    """
    try:
        start_time = time.time()
        
        # Validate phase requirements
        if request.phase >= 2 and not request.jobContext:
            raise HTTPException(
                status_code=400, 
                detail="jobContext required for Phase 2+ analysis"
            )
        
        # Convert Pydantic models to dicts
        job_context = request.jobContext.dict() if request.jobContext else None
        user_prefs = request.userPrefs.dict() if request.userPrefs else None
        
        # Parse resume
        result = parser.parse_resume_text(
            request.resumeText,
            phase=request.phase,
            job_context=job_context,
            user_prefs=user_prefs
        )
        
        # Wrap in request/response structure
        response = {
            "request": {
                "phase": request.phase,
                "jobContext": job_context,
                "userPrefs": user_prefs,
                "textLength": len(request.resumeText)
            },
            "response": result
        }
        
        logger.info(f"Successfully analyzed resume (Phase {request.phase})")
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analyze_resume_text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze-resume-file", summary="Analyze resume from file")
async def analyze_resume_file(
    file: UploadFile = File(..., description="Resume file (PDF, DOCX, TXT)"),
    phase: int = Query(1, description="Analysis phase (1-3)", ge=1, le=3),
    job_role_id: Optional[str] = Query(None, description="Target job role ID"),
    job_title: Optional[str] = Query(None, description="Job title"),
    learning_style: Optional[str] = Query("mixed", description="Learning style"),
    budget_limit: Optional[float] = Query(1000, description="Budget limit"),
    hours_per_week: Optional[int] = Query(10, description="Hours per week")
):
    """
    Analyze resume from uploaded file
    
    Supports PDF, DOCX, and TXT files up to 10MB
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded")
            
        if file.size and file.size > config.MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail=f"File too large. Max size: {config.MAX_FILE_SIZE/1024/1024}MB")
        
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in config.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format. Allowed: {config.ALLOWED_EXTENSIONS}"
            )
        
        # Validate phase requirements
        if phase >= 2 and not job_role_id:
            raise HTTPException(
                status_code=400,
                detail="job_role_id required for Phase 2+ analysis"
            )
        
        start_time = time.time()
        
        # Save temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = Path(tmp_file.name)
        
        try:
            # Prepare context and preferences
            job_context = None
            if job_role_id:
                job_context = {"roleId": job_role_id, "title": job_title}
            
            user_prefs = {
                "learningStyle": learning_style,
                "budgetLimit": budget_limit,
                "hoursPerWeek": hours_per_week
            }
            
            # Parse resume
            result = parser.parse_resume_file(
                tmp_file_path,
                phase=phase,
                job_context=job_context,
                user_prefs=user_prefs
            )
            
            # Add file metadata
            result["meta"]["filename"] = file.filename
            result["meta"]["fileSize"] = file.size
            result["meta"]["fileType"] = file_ext
            
            response = {
                "request": {
                    "filename": file.filename,
                    "phase": phase,
                    "jobContext": job_context,
                    "userPrefs": user_prefs
                },
                "response": result
            }
            
            logger.info(f"Successfully analyzed file: {file.filename} (Phase {phase})")
            return response
        
        finally:
            # Clean up temp file
            tmp_file_path.unlink(missing_ok=True)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analyze_resume_file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/job-roles/{role_id}", summary="Get job role details")
async def get_job_role_details(role_id: str):
    """Get detailed requirements for a specific job role"""
    try:
        role_details = job_manager.get_role_requirements(role_id)
        if not role_details:
            raise HTTPException(status_code=404, detail=f"Job role '{role_id}' not found")
        
        return {
            "roleId": role_id,
            "details": role_details
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job role details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/batch-analyze", summary="Batch analyze multiple resumes")
async def batch_analyze_resumes(
    files: List[UploadFile] = File(..., description="Multiple resume files"),
    phase: int = Query(1, description="Analysis phase (1-3)", ge=1, le=3),
    job_role_id: Optional[str] = Query(None, description="Target job role ID")
):
    """
    Analyze multiple resume files in batch
    
    Limited to 10 files per request for performance
    """
    try:
        if len(files) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 files per batch")
        
        results = []
        
        for file in files:
            try:
                # Validate file
                file_ext = Path(file.filename).suffix.lower()
                if file_ext not in config.ALLOWED_EXTENSIONS:
                    results.append({
                        "filename": file.filename,
                        "status": "error",
                        "error": f"Unsupported file format: {file_ext}"
                    })
                    continue
                
                # Process file (simplified for batch)
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                    content = await file.read()
                    tmp_file.write(content)
                    tmp_file_path = Path(tmp_file.name)
                
                try:
                    job_context = {"roleId": job_role_id} if job_role_id else None
                    result = parser.parse_resume_file(tmp_file_path, phase=phase, job_context=job_context)
                    
                    results.append({
                        "filename": file.filename,
                        "status": "success",
                        "skillsCount": len(result.get('skills', [])),
                        "matchScore": result.get('matchScore', {}).get('overall_score', 0) if phase >= 2 else None,
                        "analysis": result
                    })
                
                finally:
                    tmp_file_path.unlink(missing_ok=True)
                    
            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "status": "error", 
                    "error": str(e)
                })
        
        return {
            "totalFiles": len(files),
            "successful": len([r for r in results if r["status"] == "success"]),
            "failed": len([r for r in results if r["status"] == "error"]),
            "results": results
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in batch analyze: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Not Found",
        "message": "The requested resource was not found",
        "status_code": 404
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "status_code": 500
    }

if __name__ == "__main__":
    import uvicorn
    
    # Create necessary directories
    Config.create_directories()
    
    # Run the API
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
