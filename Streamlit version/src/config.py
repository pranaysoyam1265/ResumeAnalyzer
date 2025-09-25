import os
from pathlib import Path
from typing import List, Dict, Any

class Config:
    """Configuration settings for the resume analyzer"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    MODELS_DIR = BASE_DIR / "models"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Data directories
    RESUMES_DIR = DATA_DIR / "resumes"
    COURSES_DIR = DATA_DIR / "courses"
    SKILLS_DIR = DATA_DIR / "skills"
    JOB_ROLES_DIR = DATA_DIR / "job_roles"
    
    # Model paths
    NER_MODEL_PATH = MODELS_DIR / "ner_model"
    SKILL_CLASSIFIER_PATH = MODELS_DIR / "skill_classifier"
    
    # API settings
    API_VERSION = "1.0.0"
    API_TITLE = "Resume Analyzer API"
    API_DESCRIPTION = "AI-powered resume analysis and skill extraction system"
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.txt']
    
    # Skill extraction settings
    MIN_SKILL_CONFIDENCE = 0.6
    MAX_SKILLS_PER_RESUME = 50
    MIN_SKILL_LENGTH = 2
    MAX_SKILL_LENGTH = 50
    
    # Model settings
    SPACY_MODEL = "en_core_web_sm"
    
    # Database settings (for future use)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///resume_analyzer.db")
    
    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Skills categorization
    SKILL_CATEGORIES = {
        "technical": ["programming", "frameworks", "databases", "tools", "cloud"],
        "soft": ["communication", "leadership", "analytical"],
        "certifications": ["professional", "technical", "cloud"]
    }
    
    # Experience levels
    EXPERIENCE_LEVELS = ["Beginner", "Familiar", "Intermediate", "Advanced", "Expert"]
    
    # Priority levels for gap analysis
    PRIORITY_LEVELS = {
        1: "Critical",
        2: "High", 
        3: "Medium",
        4: "Low",
        5: "Optional"
    }
    
    @classmethod
    def create_directories(cls):
        """Create all necessary directories"""
        dirs = [
            cls.RESUMES_DIR / "raw",
            cls.RESUMES_DIR / "processed", 
            cls.RESUMES_DIR / "annotations",
            cls.COURSES_DIR,
            cls.SKILLS_DIR,
            cls.JOB_ROLES_DIR,
            cls.MODELS_DIR / "ner_model",
            cls.MODELS_DIR / "skill_classifier",
            cls.LOGS_DIR
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {dir_path}")
    
    @classmethod
    def get_skill_taxonomy_path(cls) -> Path:
        """Get path to skill taxonomy file"""
        return cls.SKILLS_DIR / "skill_taxonomy.json"
    
    @classmethod
    def get_skill_synonyms_path(cls) -> Path:
        """Get path to skill synonyms file"""
        return cls.SKILLS_DIR / "skill_synonyms.json"
    
    @classmethod
    def get_job_roles_path(cls) -> Path:
        """Get path to job roles file"""
        return cls.JOB_ROLES_DIR / "role_requirements.json"

# Environment-specific configurations
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    LOG_LEVEL = "WARNING"

class TestingConfig(Config):
    TESTING = True
    MIN_SKILL_CONFIDENCE = 0.5  # Lower threshold for testing

# Configuration factory
def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()
