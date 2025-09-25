import json
import logging
from typing import List, Dict, Any, Optional, Set
from pathlib import Path
from collections import defaultdict

from config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobRoleManager:
    """Manage job role requirements and skill mappings"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.job_roles = self.load_job_roles()
    
    def load_job_roles(self) -> Dict[str, Any]:
        """Load job role requirements"""
        roles_path = self.config.get_job_roles_path()
        
        if roles_path.exists():
            with open(roles_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Create comprehensive job roles database
        default_roles = {
            "software_engineer": {
                "title": "Software Engineer",
                "level": "mid",
                "required_skills": [
                    {"skill": "Python", "level": "Intermediate", "priority": 1},
                    {"skill": "JavaScript", "level": "Intermediate", "priority": 1},
                    {"skill": "Git", "level": "Intermediate", "priority": 1},
                    {"skill": "SQL", "level": "Beginner", "priority": 2},
                    {"skill": "React", "level": "Beginner", "priority": 2},
                    {"skill": "Problem Solving", "level": "Advanced", "priority": 1}
                ],
                "preferred_skills": [
                    {"skill": "Docker", "level": "Beginner", "priority": 3},
                    {"skill": "AWS", "level": "Beginner", "priority": 3},
                    {"skill": "Node.js", "level": "Beginner", "priority": 3}
                ],
                "categories": ["technical_skills.programming", "technical_skills.web_development"]
            },
            "senior_software_engineer": {
                "title": "Senior Software Engineer",
                "level": "senior",
                "required_skills": [
                    {"skill": "Python", "level": "Advanced", "priority": 1},
                    {"skill": "JavaScript", "level": "Advanced", "priority": 1},
                    {"skill": "System Design", "level": "Intermediate", "priority": 1},
                    {"skill": "Leadership", "level": "Intermediate", "priority": 1},
                    {"skill": "Mentoring", "level": "Intermediate", "priority": 2},
                    {"skill": "Architecture", "level": "Intermediate", "priority": 2}
                ],
                "preferred_skills": [
                    {"skill": "Microservices", "level": "Intermediate", "priority": 2},
                    {"skill": "Kubernetes", "level": "Intermediate", "priority": 3},
                    {"skill": "Team Management", "level": "Beginner", "priority": 3}
                ]
            },
            "data_scientist": {
                "title": "Data Scientist",
                "level": "mid",
                "required_skills": [
                    {"skill": "Python", "level": "Advanced", "priority": 1},
                    {"skill": "Machine Learning", "level": "Advanced", "priority": 1},
                    {"skill": "Statistics", "level": "Advanced", "priority": 1},
                    {"skill": "Pandas", "level": "Advanced", "priority": 1},
                    {"skill": "NumPy", "level": "Intermediate", "priority": 2},
                    {"skill": "Data Analysis", "level": "Advanced", "priority": 1}
                ],
                "preferred_skills": [
                    {"skill": "TensorFlow", "level": "Intermediate", "priority": 2},
                    {"skill": "PyTorch", "level": "Intermediate", "priority": 2},
                    {"skill": "Deep Learning", "level": "Intermediate", "priority": 3},
                    {"skill": "SQL", "level": "Intermediate", "priority": 2}
                ]
            },
            "frontend_developer": {
                "title": "Frontend Developer",
                "level": "mid",
                "required_skills": [
                    {"skill": "JavaScript", "level": "Advanced", "priority": 1},
                    {"skill": "HTML", "level": "Advanced", "priority": 1},
                    {"skill": "CSS", "level": "Advanced", "priority": 1},
                    {"skill": "React", "level": "Intermediate", "priority": 1},
                    {"skill": "Responsive Design", "level": "Intermediate", "priority": 2}
                ],
                "preferred_skills": [
                    {"skill": "TypeScript", "level": "Intermediate", "priority": 2},
                    {"skill": "Vue.js", "level": "Beginner", "priority": 3},
                    {"skill": "Angular", "level": "Beginner", "priority": 3},
                    {"skill": "SASS", "level": "Beginner", "priority": 3}
                ]
            },
            "backend_developer": {
                "title": "Backend Developer",
                "level": "mid",
                "required_skills": [
                    {"skill": "Python", "level": "Advanced", "priority": 1},
                    {"skill": "API Development", "level": "Advanced", "priority": 1},
                    {"skill": "Database Design", "level": "Intermediate", "priority": 1},
                    {"skill": "SQL", "level": "Advanced", "priority": 1},
                    {"skill": "Django", "level": "Intermediate", "priority": 2}
                ],
                "preferred_skills": [
                    {"skill": "PostgreSQL", "level": "Intermediate", "priority": 2},
                    {"skill": "Redis", "level": "Beginner", "priority": 3},
                    {"skill": "Docker", "level": "Intermediate", "priority": 2},
                    {"skill": "AWS", "level": "Beginner", "priority": 3}
                ]
            },
            "devops_engineer": {
                "title": "DevOps Engineer",
                "level": "mid",
                "required_skills": [
                    {"skill": "Docker", "level": "Advanced", "priority": 1},
                    {"skill": "Kubernetes", "level": "Intermediate", "priority": 1},
                    {"skill": "AWS", "level": "Advanced", "priority": 1},
                    {"skill": "CI/CD", "level": "Advanced", "priority": 1},
                    {"skill": "Jenkins", "level": "Intermediate", "priority": 2},
                    {"skill": "Terraform", "level": "Intermediate", "priority": 2}
                ],
                "preferred_skills": [
                    {"skill": "Ansible", "level": "Intermediate", "priority": 2},
                    {"skill": "Monitoring", "level": "Intermediate", "priority": 3},
                    {"skill": "Shell Scripting", "level": "Intermediate", "priority": 2}
                ]
            },
            "product_manager": {
                "title": "Product Manager",
                "level": "mid",
                "required_skills": [
                    {"skill": "Product Management", "level": "Advanced", "priority": 1},
                    {"skill": "Strategic Planning", "level": "Advanced", "priority": 1},
                    {"skill": "Market Research", "level": "Intermediate", "priority": 2},
                    {"skill": "User Research", "level": "Intermediate", "priority": 2},
                    {"skill": "Data Analysis", "level": "Intermediate", "priority": 2},
                    {"skill": "Communication", "level": "Advanced", "priority": 1}
                ],
                "preferred_skills": [
                    {"skill": "Agile", "level": "Intermediate", "priority": 2},
                    {"skill": "Scrum", "level": "Intermediate", "priority": 3},
                    {"skill": "SQL", "level": "Beginner", "priority": 3},
                    {"skill": "A/B Testing", "level": "Beginner", "priority": 3}
                ]
            }
        }
        
        # Save default roles
        roles_path.parent.mkdir(parents=True, exist_ok=True)
        with open(roles_path, 'w', encoding='utf-8') as f:
            json.dump(default_roles, f, indent=2)
        
        return default_roles
    
    def get_role_requirements(self, role_id: str) -> Optional[Dict[str, Any]]:
        """Get requirements for a specific role"""
        return self.job_roles.get(role_id)
    
    def list_available_roles(self) -> List[Dict[str, str]]:
        """List all available job roles"""
        return [
            {"id": role_id, "title": role_data["title"], "level": role_data["level"]}
            for role_id, role_data in self.job_roles.items()
        ]

class SkillGapAnalyzer:
    """Analyze skill gaps between resume and job requirements"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.job_manager = JobRoleManager(config)
        
        # Skill level hierarchy for comparison
        self.level_hierarchy = {
            "Beginner": 1,
            "Familiar": 2,
            "Intermediate": 3,
            "Advanced": 4,
            "Expert": 5
        }
    
    def analyze_gaps(self, extracted_skills: List[Dict[str, Any]], 
                    target_role_id: str) -> List[Dict[str, Any]]:
        """Analyze skill gaps for a target role"""
        
        # Get role requirements
        role_requirements = self.job_manager.get_role_requirements(target_role_id)
        if not role_requirements:
            logger.error(f"Role {target_role_id} not found")
            return []
        
        # Create skill lookup for extracted skills
        skill_lookup = {
            skill['name'].lower(): skill for skill in extracted_skills
        }
        
        gaps = []
        
        # Analyze required skills
        for req_skill in role_requirements.get('required_skills', []):
            gap = self._analyze_skill_gap(req_skill, skill_lookup, 'required')
            if gap:
                gaps.append(gap)
        
        # Analyze preferred skills
        for pref_skill in role_requirements.get('preferred_skills', []):
            gap = self._analyze_skill_gap(pref_skill, skill_lookup, 'preferred')
            if gap:
                gaps.append(gap)
        
        # Sort gaps by priority
        gaps.sort(key=lambda x: (x['priority'], -x.get('level_gap', 0)))
        
        return gaps
    
    def _analyze_skill_gap(self, required_skill: Dict[str, Any], 
                          skill_lookup: Dict[str, Dict[str, Any]], 
                          skill_type: str) -> Optional[Dict[str, Any]]:
        """Analyze gap for a single skill"""
        
        skill_name = required_skill['skill']
        required_level = required_skill['level']
        priority = required_skill['priority']
        
        # Check if skill exists in resume
        current_skill = skill_lookup.get(skill_name.lower())
        
        if not current_skill:
            # Complete gap - skill missing
            return {
                "skillId": f"gap_{skill_name.lower().replace(' ', '_')}",
                "skillName": skill_name,
                "targetLevel": required_level,
                "currentLevel": "None",
                "priority": priority,
                "gapType": "missing",
                "skillType": skill_type,
                "rationale": f"{skill_name} is {skill_type} for this role but not found in resume",
                "level_gap": self.level_hierarchy.get(required_level, 3)
            }
        
        # Check level gap
        current_level = current_skill.get('level', 'Beginner')
        current_level_num = self.level_hierarchy.get(current_level, 1)
        required_level_num = self.level_hierarchy.get(required_level, 3)
        
        if current_level_num < required_level_num:
            # Level gap - skill exists but level insufficient
            return {
                "skillId": current_skill.get('id', f"gap_{skill_name.lower().replace(' ', '_')}"),
                "skillName": skill_name,
                "targetLevel": required_level,
                "currentLevel": current_level,
                "priority": priority,
                "gapType": "level",
                "skillType": skill_type,
                "rationale": f"{skill_name} level needs improvement from {current_level} to {required_level}",
                "level_gap": required_level_num - current_level_num
            }
        
        # No gap
        return None
    
    def get_gap_summary(self, gaps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get summary statistics of skill gaps"""
        if not gaps:
            return {
                "total_gaps": 0,
                "critical_gaps": 0,
                "missing_skills": 0,
                "level_gaps": 0,
                "readiness_score": 100
            }
        
        critical_gaps = len([g for g in gaps if g['priority'] <= 2])
        missing_skills = len([g for g in gaps if g['gapType'] == 'missing'])
        level_gaps = len([g for g in gaps if g['gapType'] == 'level'])
        
        # Calculate readiness score (0-100)
        total_weight = sum(6 - g['priority'] for g in gaps)  # Higher priority = higher weight
        max_possible_weight = len(gaps) * 5  # Max weight if all were priority 1
        
        if max_possible_weight > 0:
            gap_impact = (total_weight / max_possible_weight) * 100
            readiness_score = max(0, 100 - gap_impact)
        else:
            readiness_score = 100
        
        return {
            "total_gaps": len(gaps),
            "critical_gaps": critical_gaps,
            "missing_skills": missing_skills,
            "level_gaps": level_gaps,
            "readiness_score": int(readiness_score),
            "priority_breakdown": {
                f"priority_{i}": len([g for g in gaps if g['priority'] == i])
                for i in range(1, 6)
            }
        }

class SkillMatcher:
    """Match and score candidates against job requirements"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.gap_analyzer = SkillGapAnalyzer(config)
        self.job_manager = JobRoleManager(config)
    
    def calculate_match_score(self, extracted_skills: List[Dict[str, Any]], 
                            target_role_id: str) -> Dict[str, Any]:
        """Calculate overall match score for a role"""
        
        role_requirements = self.job_manager.get_role_requirements(target_role_id)
        if not role_requirements:
            return {"error": f"Role {target_role_id} not found"}
        
        # Get gaps
        gaps = self.gap_analyzer.analyze_gaps(extracted_skills, target_role_id)
        gap_summary = self.gap_analyzer.get_gap_summary(gaps)
        
        # Calculate detailed scores
        required_skills = role_requirements.get('required_skills', [])
        preferred_skills = role_requirements.get('preferred_skills', [])
        
        skill_lookup = {skill['name'].lower(): skill for skill in extracted_skills}
        
        # Required skills score (60% weight)
        required_score = self._calculate_skill_group_score(required_skills, skill_lookup)
        
        # Preferred skills score (40% weight)
        preferred_score = self._calculate_skill_group_score(preferred_skills, skill_lookup)
        
        # Overall score
        overall_score = (required_score * 0.6) + (preferred_score * 0.4)
        
        return {
            "overall_score": int(overall_score),
            "required_skills_score": int(required_score),
            "preferred_skills_score": int(preferred_score),
            "readiness_score": gap_summary["readiness_score"],
            "total_gaps": gap_summary["total_gaps"],
            "critical_gaps": gap_summary["critical_gaps"],
            "match_level": self._get_match_level(overall_score),
            "recommendation": self._get_recommendation(overall_score, gap_summary)
        }
    
    def _calculate_skill_group_score(self, skill_requirements: List[Dict[str, Any]], 
                                   skill_lookup: Dict[str, Dict[str, Any]]) -> float:
        """Calculate score for a group of skills"""
        if not skill_requirements:
            return 100.0
        
        total_score = 0
        total_weight = 0
        
        level_hierarchy = {
            "Beginner": 1, "Familiar": 2, "Intermediate": 3, "Advanced": 4, "Expert": 5
        }
        
        for req_skill in skill_requirements:
            skill_name = req_skill['skill']
            required_level = req_skill['level']
            priority = req_skill['priority']
            
            # Weight based on priority (higher priority = more weight)
            weight = 6 - priority  # Priority 1 = weight 5, Priority 5 = weight 1
            
            current_skill = skill_lookup.get(skill_name.lower())
            
            if current_skill:
                current_level = current_skill.get('level', 'Beginner')
                current_level_num = level_hierarchy.get(current_level, 1)
                required_level_num = level_hierarchy.get(required_level, 3)
                
                # Calculate skill score (0-100)
                if current_level_num >= required_level_num:
                    skill_score = 100  # Meets or exceeds requirement
                else:
                    # Partial credit based on how close they are
                    skill_score = (current_level_num / required_level_num) * 100
            else:
                skill_score = 0  # Skill missing
            
            total_score += skill_score * weight
            total_weight += weight
        
        return (total_score / total_weight) if total_weight > 0 else 0
    
    def _get_match_level(self, score: float) -> str:
        """Get match level description"""
        if score >= 90:
            return "Excellent Match"
        elif score >= 75:
            return "Good Match"
        elif score >= 60:
            return "Moderate Match"
        elif score >= 40:
            return "Partial Match"
        else:
            return "Poor Match"
    
    def _get_recommendation(self, score: float, gap_summary: Dict[str, Any]) -> str:
        """Get recommendation based on match score"""
        critical_gaps = gap_summary["critical_gaps"]
        total_gaps = gap_summary["total_gaps"]
        
        if score >= 90 and critical_gaps == 0:
            return "Strong candidate, ready to proceed"
        elif score >= 75:
            if critical_gaps <= 1:
                return "Good candidate, minor skill development needed"
            else:
                return "Good potential, focus on critical skills first"
        elif score >= 60:
            return f"Moderate fit, {critical_gaps} critical skills need development"
        elif score >= 40:
            return f"Requires significant skill development in {total_gaps} areas"
        else:
            return "Not recommended for this role without extensive training"

# Main functions for Phase 2
def analyze_gaps_phase2(extracted_skills: List[Dict[str, Any]], 
                       target_role_id: str) -> List[Dict[str, Any]]:
    """Phase 2: Analyze skill gaps"""
    try:
        analyzer = SkillGapAnalyzer()
        gaps = analyzer.analyze_gaps(extracted_skills, target_role_id)
        
        # Format gaps for API response
        formatted_gaps = []
        for gap in gaps:
            formatted_gaps.append({
                "skillId": gap["skillId"],
                "skillName": gap["skillName"],
                "targetLevel": gap["targetLevel"],
                "currentLevel": gap.get("currentLevel", "None"),
                "priority": gap["priority"],
                "rationale": gap["rationale"]
            })
        
        return formatted_gaps
    
    except Exception as e:
        logger.error(f"Error in analyze_gaps_phase2: {e}")
        return []

def calculate_match_score(extracted_skills: List[Dict[str, Any]], 
                        target_role_id: str) -> Dict[str, Any]:
    """Calculate match score for a role"""
    try:
        matcher = SkillMatcher()
        return matcher.calculate_match_score(extracted_skills, target_role_id)
    
    except Exception as e:
        logger.error(f"Error in calculate_match_score: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Test gap analysis
    Config.create_directories()
    
    # Sample extracted skills
    sample_skills = [
        {"id": "skill_0", "name": "Python", "level": "Intermediate", "score": 85},
        {"id": "skill_1", "name": "JavaScript", "level": "Beginner", "score": 70},
        {"id": "skill_2", "name": "Git", "level": "Intermediate", "score": 80},
        {"id": "skill_3", "name": "React", "level": "Beginner", "score": 65}
    ]
    
    # Test gap analysis
    gaps = analyze_gaps_phase2(sample_skills, "software_engineer")
    print("=== GAP ANALYSIS TEST ===")
    print(json.dumps(gaps, indent=2))
    
    # Test match scoring
    match_score = calculate_match_score(sample_skills, "software_engineer")
    print("\n=== MATCH SCORE TEST ===")
    print(json.dumps(match_score, indent=2))
