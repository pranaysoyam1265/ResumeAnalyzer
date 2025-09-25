import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from collections import defaultdict
import random

from config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CourseDatabase:
    """Manage course database and recommendations"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.courses = self.load_courses()
        self.skill_course_mapping = self._build_skill_course_mapping()
    
    def load_courses(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load course data from various sources"""
        courses = {}
        
        # Load from different course files
        course_files = [
            "udemy_courses.json",
            "coursera_courses.json", 
            "youtube_tutorials.json"
        ]
        
        for course_file in course_files:
            file_path = self.config.COURSES_DIR / course_file
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    courses[course_file] = json.load(f)
            else:
                # Create sample data
                courses[course_file] = self._create_sample_courses(course_file)
        
        return courses
    
    def _create_sample_courses(self, course_type: str) -> List[Dict[str, Any]]:
        """Create sample course data"""
        
        if "udemy" in course_type:
            return [
                {
                    "id": "udemy_python_1",
                    "title": "Complete Python Bootcamp From Zero to Hero",
                    "provider": "Udemy",
                    "instructor": "Jose Portilla",
                    "difficulty": "Beginner",
                    "duration_hours": 22,
                    "rating": 4.6,
                    "price": 84.99,
                    "url": "https://www.udemy.com/course/complete-python-bootcamp/",
                    "skills": ["Python", "Programming", "Object-Oriented Programming"],
                    "description": "Learn Python like a Professional Start from the basics and go all the way to creating your own applications and games",
                    "type": "course"
                },
                {
                    "id": "udemy_react_1",
                    "title": "React - The Complete Guide",
                    "provider": "Udemy",
                    "instructor": "Maximilian Schwarzmüller",
                    "difficulty": "Intermediate",
                    "duration_hours": 48,
                    "rating": 4.6,
                    "price": 89.99,
                    "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
                    "skills": ["React", "JavaScript", "Redux", "Hooks"],
                    "description": "Dive in and learn React.js from scratch! Learn Reactjs, Hooks, Redux, React Routing, Animations, Next.js and way more!",
                    "type": "course"
                },
                {
                    "id": "udemy_ml_1",
                    "title": "Machine Learning A-Z: Hands-On Python & R In Data Science",
                    "provider": "Udemy",
                    "instructor": "Kirill Eremenko",
                    "difficulty": "Intermediate",
                    "duration_hours": 44,
                    "rating": 4.5,
                    "price": 94.99,
                    "url": "https://www.udemy.com/course/machinelearning/",
                    "skills": ["Machine Learning", "Python", "R", "Data Science"],
                    "description": "Learn to create Machine Learning Algorithms in Python and R from two Data Science experts",
                    "type": "course"
                },
                {
                    "id": "udemy_aws_1",
                    "title": "Ultimate AWS Certified Solutions Architect Associate",
                    "provider": "Udemy",
                    "instructor": "Stephane Maarek",
                    "difficulty": "Intermediate",
                    "duration_hours": 27,
                    "rating": 4.7,
                    "price": 79.99,
                    "url": "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/",
                    "skills": ["AWS", "Cloud Computing", "Solutions Architecture"],
                    "description": "Full Practice Exam | Learn Cloud Computing | Pass the AWS Certified Solutions Architect Associate Certification SAA-C03!",
                    "type": "course"
                }
            ]
        
        elif "coursera" in course_type:
            return [
                {
                    "id": "coursera_python_1",
                    "title": "Python for Everybody Specialization",
                    "provider": "Coursera",
                    "instructor": "University of Michigan",
                    "difficulty": "Beginner",
                    "duration_hours": 32,
                    "rating": 4.8,
                    "price": 49.0,
                    "url": "https://www.coursera.org/specializations/python",
                    "skills": ["Python", "Programming", "Data Structures", "Web Scraping"],
                    "description": "Learn to Program and Analyze Data with Python. Develop programs to gather, clean, analyze, and visualize data.",
                    "type": "specialization"
                },
                {
                    "id": "coursera_ml_1",
                    "title": "Machine Learning Course",
                    "provider": "Coursera",
                    "instructor": "Stanford University",
                    "difficulty": "Intermediate",
                    "duration_hours": 60,
                    "rating": 4.9,
                    "price": 79.0,
                    "url": "https://www.coursera.org/learn/machine-learning",
                    "skills": ["Machine Learning", "MATLAB", "Octave"],
                    "description": "Machine Learning course by Andrew Ng. Learn about supervised and unsupervised learning algorithms.",
                    "type": "course"
                },
                {
                    "id": "coursera_react_1",
                    "title": "Front-End Web Development with React",
                    "provider": "Coursera",
                    "instructor": "The Hong Kong University of Science and Technology",
                    "difficulty": "Intermediate",
                    "duration_hours": 40,
                    "rating": 4.6,
                    "price": 59.0,
                    "url": "https://www.coursera.org/specializations/full-stack-react",
                    "skills": ["React", "Redux", "React Native", "MongoDB"],
                    "description": "A complete course on developing full stack web and hybrid mobile solutions",
                    "type": "specialization"
                }
            ]
        
        else:  # YouTube tutorials
            return [
                {
                    "id": "youtube_python_1",
                    "title": "Python Tutorial for Beginners",
                    "provider": "YouTube",
                    "instructor": "Programming with Mosh",
                    "difficulty": "Beginner",
                    "duration_hours": 6,
                    "rating": 4.8,
                    "price": 0.0,
                    "url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
                    "skills": ["Python", "Programming"],
                    "description": "Python tutorial for beginners. Learn Python programming from scratch.",
                    "type": "tutorial"
                },
                {
                    "id": "youtube_react_1",
                    "title": "React JS Crash Course",
                    "provider": "YouTube",
                    "instructor": "Traversy Media",
                    "difficulty": "Intermediate",
                    "duration_hours": 2,
                    "rating": 4.7,
                    "price": 0.0,
                    "url": "https://www.youtube.com/watch?v=sBws8MSXN7A",
                    "skills": ["React", "JavaScript", "JSX"],
                    "description": "Learn React JS in this crash course. Build a task tracker app.",
                    "type": "tutorial"
                },
                {
                    "id": "youtube_git_1",
                    "title": "Git and GitHub for Beginners - Crash Course",
                    "provider": "YouTube",
                    "instructor": "freeCodeCamp",
                    "difficulty": "Beginner",
                    "duration_hours": 1.2,
                    "rating": 4.9,
                    "price": 0.0,
                    "url": "https://www.youtube.com/watch?v=RGOj5yH7evk",
                    "skills": ["Git", "GitHub", "Version Control"],
                    "description": "Learn Git and GitHub in this tutorial. Commands and workflows explained.",
                    "type": "tutorial"
                }
            ]
    
    def _build_skill_course_mapping(self) -> Dict[str, List[Dict[str, Any]]]:
        """Build mapping from skills to courses"""
        skill_mapping = defaultdict(list)
        
        for source, course_list in self.courses.items():
            for course in course_list:
                for skill in course.get('skills', []):
                    skill_mapping[skill.lower()].append(course)
        
        return dict(skill_mapping)
    
    def find_courses_for_skill(self, skill: str, difficulty: str = None, 
                              max_results: int = 5) -> List[Dict[str, Any]]:
        """Find courses for a specific skill"""
        courses = self.skill_course_mapping.get(skill.lower(), [])
        
        if difficulty:
            courses = [c for c in courses if c.get('difficulty', '').lower() == difficulty.lower()]
        
        # Sort by rating and relevance
        courses.sort(key=lambda x: (-x.get('rating', 0), x.get('price', float('inf'))))
        
        return courses[:max_results]

class RecommendationEngine:
    """Generate personalized learning recommendations"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.course_db = CourseDatabase(config)
        
        # Difficulty progression mapping
        self.difficulty_progression = {
            "None": "Beginner",
            "Beginner": "Beginner", 
            "Familiar": "Beginner",
            "Intermediate": "Intermediate",
            "Advanced": "Advanced",
            "Expert": "Advanced"
        }
    
    def generate_recommendations(self, gaps: List[Dict[str, Any]], 
                               user_prefs: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Generate course recommendations based on skill gaps"""
        
        if not gaps:
            return []
        
        user_prefs = user_prefs or {}
        learning_style = user_prefs.get("learningStyle", "mixed")
        budget_limit = user_prefs.get("budgetLimit", 1000)
        time_limit = user_prefs.get("timeLimit", 100)  # hours per month
        
        recommendations = []
        total_time = 0
        total_cost = 0
        
        # Sort gaps by priority
        sorted_gaps = sorted(gaps, key=lambda x: (x.get('priority', 5), x.get('gapType') == 'missing'))
        
        for gap in sorted_gaps:
            if total_time >= time_limit:
                break
                
            skill_name = gap.get('skillName', '')
            target_level = gap.get('targetLevel', 'Intermediate')
            current_level = gap.get('currentLevel', 'None')
            
            # Determine appropriate difficulty
            recommended_difficulty = self._get_recommended_difficulty(current_level, target_level)
            
            # Find courses
            courses = self.course_db.find_courses_for_skill(skill_name, recommended_difficulty)
            
            if courses:
                # Select best course based on preferences
                best_course = self._select_best_course(courses, learning_style, budget_limit - total_cost)
                
                if best_course and total_cost + best_course.get('price', 0) <= budget_limit:
                    recommendation = self._create_recommendation(best_course, gap, recommended_difficulty)
                    recommendations.append(recommendation)
                    
                    total_time += best_course.get('duration_hours', 0)
                    total_cost += best_course.get('price', 0)
        
        return recommendations
    
    def _get_recommended_difficulty(self, current_level: str, target_level: str) -> str:
        """Determine recommended course difficulty"""
        if current_level == "None":
            return "Beginner"
        
        # Map levels to numbers for comparison
        level_map = {"None": 0, "Beginner": 1, "Familiar": 1, "Intermediate": 2, "Advanced": 3, "Expert": 4}
        
        current_num = level_map.get(current_level, 0)
        target_num = level_map.get(target_level, 2)
        
        if target_num <= 1:
            return "Beginner"
        elif target_num <= 2:
            return "Intermediate" if current_num > 0 else "Beginner"
        else:
            return "Advanced" if current_num >= 2 else "Intermediate"
    
    def _select_best_course(self, courses: List[Dict[str, Any]], learning_style: str, 
                           remaining_budget: float) -> Optional[Dict[str, Any]]:
        """Select the best course based on preferences"""
        
        # Filter by budget
        affordable_courses = [c for c in courses if c.get('price', 0) <= remaining_budget]
        
        if not affordable_courses:
            return None
        
        # Score courses based on learning style
        scored_courses = []
        for course in affordable_courses:
            score = self._calculate_course_score(course, learning_style)
            scored_courses.append((score, course))
        
        # Sort by score (descending)
        scored_courses.sort(key=lambda x: x[0], reverse=True)
        
        return scored_courses[0][1] if scored_courses else None
    
    def _calculate_course_score(self, course: Dict[str, Any], learning_style: str) -> float:
        """Calculate course score based on learning preferences"""
        score = 0.0
        
        # Base score from rating
        score += course.get('rating', 0) * 20
        
        # Learning style preferences
        course_type = course.get('type', 'course')
        provider = course.get('provider', '').lower()
        
        if learning_style == "video" and provider in ['youtube', 'udemy']:
            score += 10
        elif learning_style == "structured" and provider in ['coursera']:
            score += 10
        elif learning_style == "hands-on" and 'project' in course.get('title', '').lower():
            score += 15
        
        # Price preference (lower is better, but free isn't always best)
        price = course.get('price', 0)
        if price == 0:
            score += 5  # Free courses get some bonus
        else:
            # Normalize price score (assume max reasonable price is 200)
            price_score = max(0, 10 - (price / 20))
            score += price_score
        
        # Duration preference (moderate length preferred)
        duration = course.get('duration_hours', 10)
        if 10 <= duration <= 30:
            score += 5
        elif duration < 5:
            score -= 2  # Too short might not be comprehensive
        elif duration > 50:
            score -= 3  # Too long might be overwhelming
        
        return score
    
    def _create_recommendation(self, course: Dict[str, Any], gap: Dict[str, Any], 
                             difficulty: str) -> Dict[str, Any]:
        """Create a formatted recommendation"""
        
        # Generate contextual reason
        skill_name = gap.get('skillName', '')
        gap_type = gap.get('gapType', 'missing')
        priority = gap.get('priority', 3)
        
        if gap_type == 'missing':
            reason = f"Learn {skill_name} fundamentals - currently missing from your skillset"
        else:
            current_level = gap.get('currentLevel', 'Beginner')
            target_level = gap.get('targetLevel', 'Intermediate')
            reason = f"Advance {skill_name} skills from {current_level} to {target_level}"
        
        # Add priority context
        priority_text = {1: "Critical", 2: "High", 3: "Medium", 4: "Low", 5: "Optional"}
        priority_label = priority_text.get(priority, "Medium")
        reason += f" - {priority_label} priority for target role"
        
        return {
            "id": course.get('id', f"rec_{skill_name.lower().replace(' ', '_')}"),
            "title": course.get('title', ''),
            "provider": course.get('provider', ''),
            "instructor": course.get('instructor', ''),
            "type": course.get('type', 'course'),
            "difficulty": difficulty,
            "estimatedHours": course.get('duration_hours', 0),
            "rating": course.get('rating', 0),
            "price": course.get('price', 0),
            "link": course.get('url', ''),
            "skills": course.get('skills', []),
            "reason": reason,
            "priority": priority,
            "skillName": skill_name,
            "description": course.get('description', '')
        }
    
    def create_learning_path(self, recommendations: List[Dict[str, Any]], 
                           user_prefs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a structured learning path"""
        
        if not recommendations:
            return {
                "totalHours": 0,
                "totalCost": 0,
                "estimatedWeeks": 0,
                "steps": []
            }
        
        user_prefs = user_prefs or {}
        hours_per_week = user_prefs.get("hoursPerWeek", 10)
        
        # Group recommendations by priority and create logical steps
        priority_groups = defaultdict(list)
        for rec in recommendations:
            priority = rec.get('priority', 3)
            priority_groups[priority].append(rec)
        
        steps = []
        step_id = 1
        total_hours = 0
        total_cost = 0
        
        # Process by priority (1 = highest)
        for priority in sorted(priority_groups.keys()):
            group_recs = priority_groups[priority]
            
            # Create steps for this priority group
            for rec in group_recs:
                step = {
                    "id": f"step_{step_id}",
                    "title": f"Master {rec.get('skillName', 'Skill')}",
                    "description": rec.get('reason', ''),
                    "estimatedHours": rec.get('estimatedHours', 0),
                    "priority": priority,
                    "resources": [rec]
                }
                
                steps.append(step)
                total_hours += rec.get('estimatedHours', 0)
                total_cost += rec.get('price', 0)
                step_id += 1
        
        # Calculate timeline
        estimated_weeks = max(1, int(total_hours / hours_per_week)) if hours_per_week > 0 else 0
        
        return {
            "totalHours": total_hours,
            "totalCost": total_cost,
            "estimatedWeeks": estimated_weeks,
            "hoursPerWeek": hours_per_week,
            "steps": steps
        }

# Main function for Phase 3
def generate_recommendations_phase3(gaps: List[Dict[str, Any]], 
                                  user_prefs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Phase 3: Generate complete recommendations and learning path"""
    try:
        engine = RecommendationEngine()
        
        # Generate recommendations
        recommendations = engine.generate_recommendations(gaps, user_prefs)
        
        # Create learning path
        learning_path = engine.create_learning_path(recommendations, user_prefs)
        
        return {
            "recommendations": recommendations,
            "learningPath": learning_path
        }
    
    except Exception as e:
        logger.error(f"Error in generate_recommendations_phase3: {e}")
        return {
            "recommendations": [],
            "learningPath": {
                "totalHours": 0,
                "estimatedWeeks": 0,
                "steps": []
            },
            "error": str(e)
        }

if __name__ == "__main__":
    # Test recommendation engine
    Config.create_directories()
    
    # Sample gaps
    sample_gaps = [
        {
            "skillName": "Python",
            "targetLevel": "Advanced",
            "currentLevel": "Beginner", 
            "priority": 1,
            "gapType": "level"
        },
        {
            "skillName": "Machine Learning",
            "targetLevel": "Intermediate",
            "currentLevel": "None",
            "priority": 2,
            "gapType": "missing"
        }
    ]
    
    # Test recommendations
    result = generate_recommendations_phase3(sample_gaps, {
        "learningStyle": "video",
        "budgetLimit": 200,
        "hoursPerWeek": 10
    })
    
    print("=== RECOMMENDATION ENGINE TEST ===")
    print(json.dumps(result, indent=2))
