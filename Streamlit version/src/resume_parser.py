import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import time

from config import Config
from data_preprocessing import ResumeTextExtractor, DataValidator
from skill_extractor import analyze_resume_phase1
from gap_analyzer import analyze_gaps_phase2, calculate_match_score
from recommendation_engine import generate_recommendations_phase3

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeParser:
    """Main resume parsing orchestrator for all phases"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.text_extractor = ResumeTextExtractor(config)
        self.validator = DataValidator()
    
    def parse_resume_file(self, file_path: Path, phase: int = 1, 
                         job_context: Optional[Dict[str, Any]] = None,
                         user_prefs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Parse a resume file and return results based on phase"""
        
        start_time = time.time()
        
        try:
            # Extract text based on file type
            if file_path.suffix.lower() == '.pdf':
                text = self.text_extractor.extract_from_pdf(file_path)
            elif file_path.suffix.lower() == '.docx':
                text = self.text_extractor.extract_from_docx(file_path)
            elif file_path.suffix.lower() == '.txt':
                text = self.text_extractor.extract_from_txt(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
            if not text:
                raise ValueError("Could not extract text from resume")
            
            # Validate extracted text
            validation = self.validator.validate_resume_text(text)
            if not validation['valid']:
                logger.warning(f"Resume validation failed: {validation['reason']}")
            
            # Parse based on phase
            return self.parse_resume_text(text, phase, job_context, user_prefs)
        
        except Exception as e:
            logger.error(f"Error parsing resume file {file_path}: {e}")
            return self._create_error_response(str(e), time.time() - start_time)
    
    def parse_resume_text(self, resume_text: str, phase: int = 1,
                         job_context: Optional[Dict[str, Any]] = None,
                         user_prefs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Parse resume text and return results based on phase"""
        
        start_time = time.time()
        
        try:
            # Phase 1: Extract skills only
            phase1_result = analyze_resume_phase1(resume_text)
            
            if phase == 1:
                phase1_result["meta"] = {
                    "model": "resume-analyzer-phase1",
                    "latencyMs": int((time.time() - start_time) * 1000),
                    "phase": 1
                }
                return phase1_result
            
            # Phase 2: Add gap analysis
            if phase >= 2:
                if not job_context or 'roleId' not in job_context:
                    raise ValueError("Job context with roleId required for Phase 2+")
                
                target_role_id = job_context['roleId']
                gaps = analyze_gaps_phase2(phase1_result['skills'], target_role_id)
                match_score = calculate_match_score(phase1_result['skills'], target_role_id)
                
                phase2_result = phase1_result.copy()
                phase2_result.update({
                    "gaps": gaps,
                    "matchScore": match_score
                })
                
                if phase == 2:
                    phase2_result["meta"] = {
                        "model": "resume-analyzer-phase2",
                        "latencyMs": int((time.time() - start_time) * 1000),
                        "phase": 2,
                        "targetRole": job_context.get('title', target_role_id)
                    }
                    return phase2_result
            
            # Phase 3: Add recommendations and learning path
            if phase >= 3:
                recommendations_result = generate_recommendations_phase3(gaps, user_prefs)
                
                phase3_result = phase2_result.copy()
                phase3_result.update({
                    "recommendations": recommendations_result["recommendations"],
                    "learningPath": recommendations_result["learningPath"]
                })
                
                # Generate summary
                summary = self._generate_summary(phase3_result)
                phase3_result["summary"] = summary
                
                phase3_result["meta"] = {
                    "model": "resume-analyzer-phase3",
                    "latencyMs": int((time.time() - start_time) * 1000),
                    "phase": 3,
                    "targetRole": job_context.get('title', target_role_id),
                    "totalRecommendations": len(recommendations_result["recommendations"])
                }
                
                return phase3_result
            
        except Exception as e:
            logger.error(f"Error in parse_resume_text: {e}")
            return self._create_error_response(str(e), time.time() - start_time)
    
    def _generate_summary(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of analysis results"""
        
        skills = analysis_result.get('skills', [])
        gaps = analysis_result.get('gaps', [])
        match_score = analysis_result.get('matchScore', {})
        learning_path = analysis_result.get('learningPath', {})
        
        # Identify strengths (high-scoring skills)
        strengths = []
        for skill in skills:
            if skill.get('score', 0) >= 80:
                strengths.append(skill['name'])
        
        # Identify improvement areas (critical gaps)
        improvements = []
        for gap in gaps:
            if gap.get('priority', 5) <= 2:  # High priority gaps
                improvements.append(gap.get('skillName', ''))
        
        # Generate profile summary
        total_skills = len(skills)
        high_level_skills = len([s for s in skills if s.get('level') in ['Advanced', 'Expert']])
        overall_score = match_score.get('overall_score', 0)
        
        if overall_score >= 80:
            profile_level = "Highly qualified"
        elif overall_score >= 65:
            profile_level = "Well qualified"  
        elif overall_score >= 50:
            profile_level = "Moderately qualified"
        else:
            profile_level = "Developing"
        
        profile_summary = f"{profile_level} candidate with {total_skills} identified skills, "
        profile_summary += f"{high_level_skills} at advanced level. "
        profile_summary += f"Match score of {overall_score}% for target role."
        
        return {
            "strengths": strengths[:5],  # Top 5 strengths
            "improvements": improvements[:5],  # Top 5 areas for improvement
            "profileSummary": profile_summary,
            "totalSkills": total_skills,
            "advancedSkills": high_level_skills,
            "matchScore": overall_score,
            "learningTimeEstimate": f"{learning_path.get('estimatedWeeks', 0)} weeks"
        }
    
    def _create_error_response(self, error_message: str, elapsed_time: float) -> Dict[str, Any]:
        """Create standardized error response"""
        return {
            "version": self.config.API_VERSION,
            "skills": [],
            "gaps": [],
            "recommendations": [],
            "learningPath": {
                "totalHours": 0,
                "estimatedWeeks": 0,
                "steps": []
            },
            "summary": {
                "strengths": [],
                "improvements": [],
                "profileSummary": "Analysis failed due to error",
                "error": error_message
            },
            "meta": {
                "model": "resume-analyzer-error",
                "latencyMs": int(elapsed_time * 1000),
                "error": error_message
            }
        }
    
    def batch_process_resumes(self, resume_folder: Path, output_folder: Path,
                            phase: int = 1, job_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process multiple resumes in batch"""
        
        resume_folder = Path(resume_folder)
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)
        
        results = {
            "processed": 0,
            "failed": 0,
            "results": []
        }
        
        # Process each resume file
        for resume_file in resume_folder.iterdir():
            if resume_file.suffix.lower() in ['.pdf', '.docx', '.txt']:
                logger.info(f"Processing: {resume_file.name}")
                
                try:
                    # Parse resume
                    result = self.parse_resume_file(resume_file, phase, job_context)
                    
                    # Save result
                    output_file = output_folder / f"{resume_file.stem}_analysis.json"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(result, f, indent=2)
                    
                    results["processed"] += 1
                    results["results"].append({
                        "filename": resume_file.name,
                        "output_file": output_file.name,
                        "status": "success",
                        "skills_count": len(result.get('skills', [])),
                        "match_score": result.get('matchScore', {}).get('overall_score', 0)
                    })
                    
                    logger.info(f"Successfully processed: {resume_file.name}")
                    
                except Exception as e:
                    results["failed"] += 1
                    results["results"].append({
                        "filename": resume_file.name,
                        "status": "failed",
                        "error": str(e)
                    })
                    logger.error(f"Failed to process {resume_file.name}: {e}")
        
        return results

# Utility functions for direct API use
def parse_resume_phase1(resume_text: str) -> Dict[str, Any]:
    """Direct Phase 1 parsing"""
    parser = ResumeParser()
    return parser.parse_resume_text(resume_text, phase=1)

def parse_resume_phase2(resume_text: str, job_context: Dict[str, Any]) -> Dict[str, Any]:
    """Direct Phase 2 parsing"""
    parser = ResumeParser()
    return parser.parse_resume_text(resume_text, phase=2, job_context=job_context)

def parse_resume_phase3(resume_text: str, job_context: Dict[str, Any], 
                       user_prefs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Direct Phase 3 parsing"""
    parser = ResumeParser()
    return parser.parse_resume_text(resume_text, phase=3, job_context=job_context, user_prefs=user_prefs)

if __name__ == "__main__":
    # Test the complete resume parser
    Config.create_directories()
    
    sample_resume = """
    John Doe
    Senior Software Engineer
    john.doe@email.com | (555) 123-4567
    
    TECHNICAL SKILLS:
    • Programming Languages: Python, Java, JavaScript, TypeScript
    • Web Technologies: React, Node.js, Django, Flask
    • Databases: PostgreSQL, MongoDB, Redis
    • Cloud Platforms: AWS, Docker, Kubernetes
    • Tools: Git, Jenkins, JIRA
    
    EXPERIENCE:
    Senior Python Developer at Tech Corp (2020-2023)
    • Developed scalable web applications using Django and React
    • Implemented machine learning models using scikit-learn and TensorFlow  
    • Managed PostgreSQL databases and optimized query performance
    • Deployed applications on AWS using Docker containers
    • Led a team of 5 developers using Agile methodologies
    
    PROJECTS:
    • E-commerce Platform: Built using React, Node.js, and MongoDB
    • ML Recommendation System: Developed using Python and TensorFlow
    • Microservices Architecture: Deployed on AWS with Kubernetes
    """
    
    parser = ResumeParser()
    
    # Test Phase 1
    print("=== PHASE 1 TEST ===")
    phase1_result = parser.parse_resume_text(sample_resume, phase=1)
    print(f"Skills found: {len(phase1_result['skills'])}")
    
    # Test Phase 2  
    print("\n=== PHASE 2 TEST ===")
    job_context = {"roleId": "software_engineer", "title": "Software Engineer"}
    phase2_result = parser.parse_resume_text(sample_resume, phase=2, job_context=job_context)
    print(f"Gaps found: {len(phase2_result['gaps'])}")
    print(f"Match score: {phase2_result['matchScore']['overall_score']}%")
    
    # Test Phase 3
    print("\n=== PHASE 3 TEST ===") 
    user_prefs = {"learningStyle": "video", "budgetLimit": 500, "hoursPerWeek": 10}
    phase3_result = parser.parse_resume_text(sample_resume, phase=3, job_context=job_context, user_prefs=user_prefs)
    print(f"Recommendations: {len(phase3_result['recommendations'])}")
    print(f"Learning path steps: {len(phase3_result['learningPath']['steps'])}")
    print(f"Estimated weeks: {phase3_result['learningPath']['estimatedWeeks']}")
