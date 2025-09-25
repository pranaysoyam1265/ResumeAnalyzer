# app.py - Enhanced AI Skill Gap Analyzer with Advanced Features
import streamlit as st
import pandas as pd
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import logging
import requests
from dataclasses import dataclass
import time

# Core ML/NLP imports with error handling
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# File processing imports
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# Configure page
st.set_page_config(
    page_title="AI Skill Gap Analyzer Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# NEW MODULE: Analytics Engine (Phase 1)
# =============================================================================
class AnalyticsEngine:
    """Advanced analytics without affecting skill extraction"""
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.skill_trends = self._load_skill_trends()
        self.salary_data = self._load_salary_data()
        self.market_demand = self._load_market_demand()
    
    def _load_skill_trends(self):
        """Load skill popularity trends over time"""
        return {
            "python": {"2023": 85, "2024": 90, "2025": 92},
            "machine learning": {"2023": 78, "2024": 85, "2025": 88},
            "aws": {"2023": 75, "2024": 82, "2025": 85},
            "react": {"2023": 80, "2024": 83, "2025": 84},
            "docker": {"2023": 70, "2024": 78, "2025": 82},
            "kubernetes": {"2023": 65, "2024": 75, "2025": 80},
            "tensorflow": {"2023": 72, "2024": 76, "2025": 78},
            "pytorch": {"2023": 68, "2024": 74, "2025": 79},
            "sql": {"2023": 88, "2024": 89, "2025": 90},
            "javascript": {"2023": 87, "2024": 88, "2025": 87}
        }
    
    def _load_salary_data(self):
        """Load salary impact data for skills"""
        return {
            "python": {"base": 95000, "premium": 25000},
            "machine learning": {"base": 110000, "premium": 35000},
            "aws": {"base": 105000, "premium": 30000},
            "react": {"base": 98000, "premium": 22000},
            "docker": {"base": 102000, "premium": 27000},
            "kubernetes": {"base": 115000, "premium": 40000},
            "tensorflow": {"base": 108000, "premium": 33000},
            "pytorch": {"base": 112000, "premium": 37000},
            "sql": {"base": 92000, "premium": 18000},
            "javascript": {"base": 96000, "premium": 24000}
        }
    
    def _load_market_demand(self):
        """Load real-time market demand metrics"""
        return {
            "python": 95,
            "machine learning": 88,
            "aws": 92,
            "react": 85,
            "docker": 87,
            "kubernetes": 90,
            "sql": 83,
            "javascript": 86,
            "azure": 78,
            "gcp": 76,
            "node.js": 82,
            "angular": 75
        }
    
    def get_skill_trend_analysis(self, skills: List[str]) -> Dict:
        """Analyze skill trends for given skills"""
        trend_data = {}
        for skill in skills:
            skill_lower = skill.lower()
            if skill_lower in self.skill_trends:
                trend_data[skill] = {
                    "trends": self.skill_trends[skill_lower],
                    "growth_rate": self._calculate_growth_rate(self.skill_trends[skill_lower]),
                    "future_outlook": self._predict_future_outlook(skill_lower)
                }
        return trend_data
    
    def _calculate_growth_rate(self, trends: Dict) -> float:
        """Calculate annual growth rate"""
        years = sorted(trends.keys())
        if len(years) < 2:
            return 0.0
        start = trends[years[0]]
        end = trends[years[-1]]
        return ((end - start) / start) * 100
    
    def _predict_future_outlook(self, skill: str) -> str:
        """Predict future outlook for a skill"""
        outlooks = {
            "python": "Very Strong - Continued dominance in AI/ML and web development",
            "machine learning": "Excellent - High demand across industries",
            "aws": "Strong - Cloud adoption continues to grow",
            "react": "Stable - Widely adopted in frontend development",
            "docker": "Growing - Containerization becoming standard",
            "kubernetes": "Rapid Growth - Orchestration demand increasing"
        }
        return outlooks.get(skill, "Stable - Moderate market demand")
    
    def get_salary_impact_analysis(self, skills: List[Dict]) -> Dict:
        """Calculate potential salary impact of skills"""
        total_base = 0
        total_premium = 0
        skill_impacts = {}
        
        for skill_data in skills:
            skill = skill_data["skill"].lower()
            if skill in self.salary_data:
                level_multiplier = self._get_level_multiplier(skill_data["proficiency_level"])
                base = self.salary_data[skill]["base"] * level_multiplier
                premium = self.salary_data[skill]["premium"] * level_multiplier
                
                skill_impacts[skill] = {
                    "base_salary": base,
                    "premium": premium,
                    "total_value": base + premium,
                    "level_multiplier": level_multiplier
                }
                
                total_base += base
                total_premium += premium
        
        return {
            "total_estimated_salary": total_base + total_premium,
            "skill_premium_value": total_premium,
            "skill_breakdown": skill_impacts,
            "average_skill_value": total_premium / max(1, len(skills))
        }
    
    def _get_level_multiplier(self, level: str) -> float:
        """Get multiplier based on proficiency level"""
        multipliers = {
            "Beginner": 0.5,
            "Intermediate": 1.0,
            "Advanced": 1.5,
            "Expert": 2.0
        }
        return multipliers.get(level, 1.0)
    
    def get_market_demand_scores(self, skills: List[str]) -> Dict:
        """Get market demand scores for skills"""
        demand_scores = {}
        for skill in skills:
            skill_lower = skill.lower()
            demand_scores[skill] = {
                "demand_score": self.market_demand.get(skill_lower, 50),
                "market_trend": self._get_market_trend(skill_lower),
                "recommendation": self._get_demand_recommendation(skill_lower)
            }
        return demand_scores
    
    def _get_market_trend(self, skill: str) -> str:
        """Get market trend for skill"""
        trends = {
            "python": "Rising",
            "machine learning": "Rapidly Rising",
            "aws": "Rising",
            "kubernetes": "Rapidly Rising",
            "docker": "Rising",
            "react": "Stable",
            "javascript": "Stable"
        }
        return trends.get(skill, "Stable")
    
    def _get_demand_recommendation(self, skill: str) -> str:
        """Get recommendation based on market demand"""
        demand = self.market_demand.get(skill, 50)
        if demand >= 85:
            return "High Priority - Strong market demand"
        elif demand >= 70:
            return "Good Investment - Growing demand"
        else:
            return "Consider alternatives - Moderate demand"

# =============================================================================
# NEW MODULE: Report Generator (Phase 1)
# =============================================================================
class ReportGenerator:
    """Generate comprehensive analysis reports"""
    
    def __init__(self, analyzer, analytics_engine):
        self.analyzer = analyzer
        self.analytics = analytics_engine
    
    def generate_comprehensive_report(self, skills_data: List[Dict], gaps_data: Dict) -> Dict:
        """Generate comprehensive analysis report"""
        try:
            report = {
                "executive_summary": self._generate_executive_summary(skills_data, gaps_data),
                "skill_analysis": self._generate_skill_analysis(skills_data),
                "gap_analysis": self._generate_gap_analysis(gaps_data),
                "market_insights": self._generate_market_insights(skills_data),
                "recommendations": self._generate_recommendations(skills_data, gaps_data),
                "learning_strategy": self._generate_learning_strategy(gaps_data),
                "timestamp": datetime.now().isoformat()
            }
            return report
        except Exception as e:
            logging.warning(f"Report generation failed: {e}")
            return self._generate_fallback_report(skills_data, gaps_data)
    
    def _generate_executive_summary(self, skills_data: List[Dict], gaps_data: Dict) -> Dict:
        """Generate executive summary"""
        total_skills = len(skills_data)
        expert_skills = len([s for s in skills_data if s["proficiency_level"] == "Expert"])
        
        if "error" not in gaps_data:
            match_score = gaps_data["summary"]["overall_match_score"]
            critical_gaps = gaps_data["summary"]["missing_critical_skills"]
        else:
            match_score = 0
            critical_gaps = 0
        
        return {
            "total_skills": total_skills,
            "expert_skills": expert_skills,
            "match_score": match_score,
            "critical_gaps": critical_gaps,
            "overall_assessment": self._get_overall_assessment(match_score, critical_gaps)
        }
    
    def _get_overall_assessment(self, match_score: float, critical_gaps: int) -> str:
        """Get overall assessment"""
        if match_score >= 80 and critical_gaps == 0:
            return "Excellent - Well positioned for target role"
        elif match_score >= 60:
            return "Good - Minor improvements needed"
        elif match_score >= 40:
            return "Moderate - Significant development required"
        else:
            return "Needs Work - Consider alternative roles or major upskilling"
    
    def _generate_skill_analysis(self, skills_data: List[Dict]) -> Dict:
        """Generate detailed skill analysis"""
        # Salary impact analysis
        salary_impact = self.analytics.get_salary_impact_analysis(skills_data)
        
        # Market demand analysis
        skill_names = [s["skill"] for s in skills_data]
        market_demand = self.analytics.get_market_demand_scores(skill_names)
        
        return {
            "salary_impact": salary_impact,
            "market_demand": market_demand,
            "skill_distribution": self._analyze_skill_distribution(skills_data)
        }
    
    def _analyze_skill_distribution(self, skills_data: List[Dict]) -> Dict:
        """Analyze skill distribution across categories"""
        distribution = {}
        for skill in skills_data:
            category = skill.get("category", "Other")
            if category not in distribution:
                distribution[category] = []
            distribution[category].append(skill)
        return distribution
    
    def _generate_gap_analysis(self, gaps_data: Dict) -> Dict:
        """Generate gap analysis section"""
        if "error" in gaps_data:
            return {"error": gaps_data["error"]}
        
        return {
            "critical_gaps": gaps_data["missing_critical"],
            "level_gaps": gaps_data["level_gaps"],
            "strengths": gaps_data["strengths"],
            "summary": gaps_data["summary"]
        }
    
    def _generate_market_insights(self, skills_data: List[Dict]) -> Dict:
        """Generate market insights section"""
        skill_names = [s["skill"] for s in skills_data]
        trend_analysis = self.analytics.get_skill_trend_analysis(skill_names)
        
        return {
            "trend_analysis": trend_analysis,
            "industry_benchmarks": self._get_industry_benchmarks(),
            "emerging_skills": self._get_emerging_skills()
        }
    
    def _get_industry_benchmarks(self) -> Dict:
        """Get industry benchmarks"""
        return {
            "tech_industry": {"avg_skills": 15, "expert_skills": 3},
            "finance_industry": {"avg_skills": 12, "expert_skills": 2},
            "healthcare_industry": {"avg_skills": 10, "expert_skills": 2}
        }
    
    def _get_emerging_skills(self) -> List[str]:
        """Get list of emerging skills"""
        return [
            "Generative AI",
            "Quantum Computing",
            "Edge Computing",
            "Cybersecurity AI",
            "Sustainable Tech"
        ]
    
    def _generate_recommendations(self, skills_data: List[Dict], gaps_data: Dict) -> Dict:
        """Generate personalized recommendations"""
        recommendations = {
            "immediate_actions": [],
            "short_term_goals": [],
            "long_term_strategy": []
        }
        
        # Immediate actions based on critical gaps
        if "error" not in gaps_data:
            for gap in gaps_data["missing_critical"][:3]:
                recommendations["immediate_actions"].append(
                    f"Learn {gap['skill']} (Priority {gap['priority']})"
                )
        
        # Short-term goals based on level gaps
        if "error" not in gaps_data:
            for gap in gaps_data["level_gaps"][:2]:
                recommendations["short_term_goals"].append(
                    f"Improve {gap['skill']} from {gap['current_level']} to {gap['required_level']}"
                )
        
        # Long-term strategy
        recommendations["long_term_strategy"].extend([
            "Develop 2-3 expert-level specialization skills",
            "Build portfolio projects demonstrating key skills",
            "Network with professionals in target industry",
            "Consider relevant certifications for career advancement"
        ])
        
        return recommendations
    
    def _generate_learning_strategy(self, gaps_data: Dict) -> Dict:
        """Generate learning strategy"""
        if "error" in gaps_data:
            return {"error": "No gap data available"}
        
        return {
            "timeline": self._generate_learning_timeline(gaps_data),
            "resource_allocation": self._generate_resource_allocation(gaps_data),
            "success_metrics": self._generate_success_metrics()
        }
    
    def _generate_learning_timeline(self, gaps_data: Dict) -> Dict:
        """Generate learning timeline"""
        timeline = {}
        critical_gaps = gaps_data["missing_critical"]
        level_gaps = gaps_data["level_gaps"]
        
        if critical_gaps:
            timeline["weeks_1_4"] = [f"Learn {gap['skill']}" for gap in critical_gaps[:2]]
        if level_gaps:
            timeline["weeks_5_8"] = [f"Improve {gap['skill']}" for gap in level_gaps[:3]]
        
        timeline["months_3_6"] = ["Advanced specialization", "Portfolio development"]
        
        return timeline
    
    def _generate_resource_allocation(self, gaps_data: Dict) -> Dict:
        """Generate resource allocation plan"""
        return {
            "time_commitment": "10-15 hours per week",
            "budget_range": "$500-1000 for courses/certifications",
            "learning_resources": ["Online courses", "Practice projects", "Mentorship"],
            "success_factors": ["Consistent practice", "Real-world application", "Community engagement"]
        }
    
    def _generate_success_metrics(self) -> Dict:
        """Generate success metrics"""
        return {
            "skill_acquisition": "2-3 new skills per quarter",
            "proficiency_improvement": "One level up in 2 key skills every 6 months",
            "career_impact": "Salary increase or promotion within 12-18 months"
        }
    
    def _generate_fallback_report(self, skills_data: List[Dict], gaps_data: Dict) -> Dict:
        """Generate fallback report if main generation fails"""
        return {
            "executive_summary": {
                "total_skills": len(skills_data),
                "expert_skills": len([s for s in skills_data if s["proficiency_level"] == "Expert"]),
                "match_score": gaps_data.get("summary", {}).get("overall_match_score", 0) if "error" not in gaps_data else 0,
                "critical_gaps": gaps_data.get("summary", {}).get("missing_critical_skills", 0) if "error" not in gaps_data else 0,
                "overall_assessment": "Analysis incomplete"
            },
            "timestamp": datetime.now().isoformat()
        }

# =============================================================================
# NEW MODULE: Learning Path Optimizer (Phase 3)
# =============================================================================
class LearningPathOptimizer:
    """AI-powered learning path optimization"""
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.learning_modules = self._load_learning_modules()
    
    def _load_learning_modules(self):
        """Load micro-learning modules"""
        return {
            "python": [
                {"module": "Python Basics", "duration": 10, "difficulty": "Beginner"},
                {"module": "OOP in Python", "duration": 15, "difficulty": "Intermediate"},
                {"module": "Advanced Python", "duration": 20, "difficulty": "Advanced"}
            ],
            "machine learning": [
                {"module": "ML Fundamentals", "duration": 25, "difficulty": "Intermediate"},
                {"module": "Deep Learning", "duration": 30, "difficulty": "Advanced"},
                {"module": "ML Projects", "duration": 20, "difficulty": "Advanced"}
            ],
            # Add more skills as needed
        }
    
    def optimize_learning_path(self, gap_skills: List[str], constraints: Dict) -> Dict:
        """Optimize learning path based on constraints"""
        try:
            path = []
            total_duration = 0
            weekly_hours = constraints.get("weekly_hours", 10)
            
            for skill in gap_skills:
                if skill.lower() in self.learning_modules:
                    modules = self.learning_modules[skill.lower()]
                    for module in modules:
                        path.append({
                            "skill": skill,
                            "module": module["module"],
                            "duration_hours": module["duration"],
                            "duration_weeks": module["duration"] / weekly_hours,
                            "difficulty": module["difficulty"]
                        })
                        total_duration += module["duration"]
            
            # Apply spaced repetition scheduling
            optimized_path = self._apply_spaced_repetition(path, weekly_hours)
            
            return {
                "optimized_path": optimized_path,
                "total_duration_hours": total_duration,
                "estimated_completion_weeks": total_duration / weekly_hours,
                "weekly_commitment": weekly_hours
            }
        except Exception as e:
            logging.warning(f"Learning path optimization failed: {e}")
            return self._generate_fallback_path(gap_skills, constraints)
    
    def _apply_spaced_repetition(self, path: List[Dict], weekly_hours: int) -> List[Dict]:
        """Apply spaced repetition scheduling"""
        scheduled_path = []
        current_week = 1
        
        for item in path:
            weeks_needed = max(1, round(item["duration_hours"] / weekly_hours))
            
            scheduled_path.append({
                **item,
                "start_week": current_week,
                "end_week": current_week + weeks_needed - 1,
                "review_weeks": [current_week + weeks_needed + 2, current_week + weeks_needed + 4]
            })
            
            current_week += weeks_needed
        
        return scheduled_path
    
    def _generate_fallback_path(self, gap_skills: List[str], constraints: Dict) -> Dict:
        """Generate fallback learning path"""
        weekly_hours = constraints.get("weekly_hours", 10)
        path = []
        
        for i, skill in enumerate(gap_skills):
            path.append({
                "skill": skill,
                "module": f"Learn {skill}",
                "duration_hours": 20,
                "duration_weeks": 2,
                "difficulty": "Intermediate",
                "start_week": i * 2 + 1,
                "end_week": i * 2 + 2
            })
        
        return {
            "optimized_path": path,
            "total_duration_hours": len(gap_skills) * 20,
            "estimated_completion_weeks": len(gap_skills) * 2,
            "weekly_commitment": weekly_hours
        }

# =============================================================================
# NEW MODULE: AI Career Advisor (Phase 3)
# =============================================================================
class AICareerAdvisor:
    """AI-powered career guidance and recommendations"""
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.career_paths = self._load_career_paths()
    
    def _load_career_paths(self):
        """Load career progression paths"""
        return {
            "Data Scientist": {
                "entry": ["Python", "SQL", "Statistics"],
                "mid": ["Machine Learning", "Data Visualization", "Big Data"],
                "senior": ["Deep Learning", "MLOps", "Leadership"],
                "expert": ["AI Research", "Architecture", "Strategy"]
            },
            "Full Stack Developer": {
                "entry": ["JavaScript", "HTML/CSS", "React"],
                "mid": ["Node.js", "Databases", "APIs"],
                "senior": ["System Design", "DevOps", "Mentoring"],
                "expert": ["Architecture", "Technical Leadership", "Innovation"]
            }
        }
    
    def get_career_recommendations(self, skills: List[Dict], experience: str) -> Dict:
        """Get AI-powered career recommendations"""
        try:
            skill_names = [s["skill"].lower() for s in skills]
            expert_skills = [s["skill"] for s in skills if s["proficiency_level"] == "Expert"]
            
            # Match against career paths
            matched_paths = []
            for path_name, path_data in self.career_paths.items():
                match_score = self._calculate_career_match(skill_names, path_data)
                matched_paths.append({
                    "career_path": path_name,
                    "match_score": match_score,
                    "next_steps": self._get_next_steps(skill_names, path_data, experience),
                    "growth_potential": self._assess_growth_potential(path_name)
                })
            
            # Sort by match score
            matched_paths.sort(key=lambda x: x["match_score"], reverse=True)
            
            return {
                "recommended_paths": matched_paths[:3],
                "strengths_alignment": self._analyze_strengths_alignment(skills, matched_paths),
                "growth_opportunities": self._identify_growth_opportunities(skills)
            }
        except Exception as e:
            logging.warning(f"Career recommendations failed: {e}")
            return self._get_fallback_recommendations()
    
    def _calculate_career_match(self, user_skills: List[str], career_path: Dict) -> float:
        """Calculate match score between user skills and career path"""
        all_required = set()
        for level_skills in career_path.values():
            all_required.update([s.lower() for s in level_skills])
        
        if not all_required:
            return 0.0
        
        matched_skills = set(user_skills) & all_required
        return len(matched_skills) / len(all_required) * 100
    
    def _get_next_steps(self, user_skills: List[str], career_path: Dict, experience: str) -> List[str]:
        """Get next steps for career progression"""
        next_steps = []
        
        # Determine current level based on experience
        level_map = {"entry": "entry", "mid": "mid", "senior": "senior", "expert": "expert"}
        current_level = level_map.get(experience.lower(), "entry")
        
        # Get skills for next level
        levels = ["entry", "mid", "senior", "expert"]
        current_index = levels.index(current_level)
        
        if current_index < len(levels) - 1:
            next_level = levels[current_index + 1]
            required_skills = career_path.get(next_level, [])
            missing_skills = [s for s in required_skills if s.lower() not in user_skills]
            next_steps.extend([f"Learn {skill}" for skill in missing_skills[:3]])
        
        return next_steps
    
    def _assess_growth_potential(self, career_path: str) -> str:
        """Assess growth potential for career path"""
        potentials = {
            "Data Scientist": "Very High - Growing demand across industries",
            "Full Stack Developer": "High - Continuous need for web development",
            "DevOps Engineer": "High - Critical for modern infrastructure",
            "Product Manager": "High - Essential for product development"
        }
        return potentials.get(career_path, "Moderate - Stable market demand")
    
    def _analyze_strengths_alignment(self, skills: List[Dict], career_paths: List[Dict]) -> Dict:
        """Analyze how strengths align with career paths"""
        expert_skills = [s["skill"] for s in skills if s["proficiency_level"] == "Expert"]
        
        alignment = {}
        for path in career_paths:
            path_name = path["career_path"]
            # Simple alignment calculation (can be enhanced)
            alignment[path_name] = {
                "expert_skills_count": len(expert_skills),
                "alignment_score": path["match_score"],
                "leverage_points": expert_skills[:3]  # Top 3 expert skills
            }
        
        return alignment
    
    def _identify_growth_opportunities(self, skills: List[Dict]) -> List[str]:
        """Identify growth opportunities based on skill trends"""
        opportunities = []
        
        # Analyze current skills and suggest complementary ones
        skill_categories = {}
        for skill in skills:
            category = skill.get("category", "Other")
            if category not in skill_categories:
                skill_categories[category] = []
            skill_categories[category].append(skill["skill"])
        
        # Suggest opportunities based on categories
        if "Programming Languages" in skill_categories:
            opportunities.append("Learn a complementary framework (e.g., Django, Spring)")
        if "Databases" in skill_categories:
            opportunities.append("Explore cloud database technologies")
        
        return opportunities[:3]
    
    def _get_fallback_recommendations(self) -> Dict:
        """Get fallback career recommendations"""
        return {
            "recommended_paths": [
                {
                    "career_path": "Software Developer",
                    "match_score": 75.0,
                    "next_steps": ["Continue building full-stack projects", "Learn system design"],
                    "growth_potential": "High - Strong market demand"
                }
            ],
            "strengths_alignment": {},
            "growth_opportunities": ["Focus on building portfolio projects", "Network with industry professionals"]
        }

# =============================================================================
# PRESERVED: Original Skill Gap Analyzer (UNCHANGED)
# =============================================================================
class AdvancedSkillGapAnalyzer:
    def __init__(self):
        self.non_skill_terms = self._build_non_skill_terms()
        self.skill_categories = self._build_skill_categories()
        self.master_skills = self._build_master_skills_set()
        self.skill_synonyms = self._build_skill_synonyms()
        self.job_roles = self._build_job_roles()
        self.courses_df = self._build_courses_database()
        self.evidence_cache = {}
        self.level_hierarchy = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Expert": 4}
        
        # Initialize NLP model
        self.nlp, self.model_type = self._initialize_nlp()
        
    def _initialize_nlp(self):
        """Initialize NLP model with fallback"""
        if not SPACY_AVAILABLE:
            return None, "none"
        try:
            nlp = spacy.load("en_core_web_sm")
            return nlp, "pretrained"
        except OSError:
            try:
                nlp = spacy.blank("en")
                return nlp, "blank"
            except:
                return None, "none"
    
    def _build_non_skill_terms(self):
        """Build comprehensive list of non-skill terms"""
        return {
            'years', 'months', 'experience', 'work', 'job', 'role', 'position',
            'company', 'team', 'project', 'client', 'business', 'industry',
            'software', 'application', 'system', 'data', 'information', 'technology',
            'solutions', 'services', 'management', 'development', 'design', 'analysis',
            'testing', 'support', 'training', 'certification', 'degree', 'education',
            'professional', 'summary', 'strong', 'excellent', 'good', 'solid',
            'extensive', 'comprehensive', 'deep', 'advanced', 'intermediate', 'expert'
        }
    
    def _build_skill_categories(self):
        """Define proper skill categories"""
        return {
            "Programming Languages": {
                "keywords": {"python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", 
                           "swift", "kotlin", "php", "ruby", "scala", "r", "matlab", "perl", "shell",
                           "html", "css", "sql", "nosql", "graphql"},
                "icon": "💻"
            },
            "Web Technologies": {
                "keywords": {"react", "angular", "vue", "node.js", "express", "django", "flask", 
                           "spring", "laravel", "rails", "asp.net", "rest", "soap", "websocket"},
                "icon": "🌐"
            },
            "Databases": {
                "keywords": {"mysql", "postgresql", "mongodb", "redis", "oracle", "sql server", 
                           "cassandra", "dynamodb", "sqlite", "firebase", "elasticsearch", "bigquery"},
                "icon": "🗄️"
            },
            "Cloud & DevOps": {
                "keywords": {"aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins", 
                           "ansible", "puppet", "chef", "gitlab", "github", "ci/cd", "devops", "iac"},
                "icon": "☁️"
            },
            "Data Science & AI": {
                "keywords": {"machine learning", "deep learning", "data science", "ai", "tensorflow", 
                           "pytorch", "keras", "pandas", "numpy", "spark", "hadoop", "kafka", "tableau"},
                "icon": "🤖"
            },
            "Testing & QA": {
                "keywords": {"selenium", "cypress", "jest", "mocha", "junit", "testng", "soapui", 
                           "postman", "jmeter", "appium", "quality center", "alm", "automation"},
                "icon": "🧪"
            },
            "Project Management": {
                "keywords": {"agile", "scrum", "kanban", "waterfall", "jira", "confluence", "trello", 
                           "asana", "ms project", "rally", "safe", "pm", "project management"},
                "icon": "📊"
            },
            "Soft Skills": {
                "keywords": {"leadership", "communication", "problem solving", "critical thinking", 
                           "teamwork", "collaboration", "mentoring", "presentation", "negotiation",
                           "time management", "analytical thinking", "creativity", "adaptability"},
                "icon": "💬"
            }
        }
    
    def _build_master_skills_set(self):
        """Build comprehensive skills database"""
        skills = set()
        for category in self.skill_categories.values():
            skills.update(category["keywords"])
        return skills
    
    def _build_skill_synonyms(self):
        """Build skill synonyms mapping"""
        return {
            "javascript": ["js", "ecmascript"],
            "python": ["python3", "py"],
            "machine learning": ["ml", "machinelearning"],
            "artificial intelligence": ["ai"],
            "react": ["reactjs", "react.js"],
            "node.js": ["nodejs", "node"],
            "sql": ["structured query language"],
            "aws": ["amazon web services"],
            "azure": ["microsoft azure"],
            "gcp": ["google cloud platform"],
            "scrum": ["agile scrum"],
            "java": ["java programming"],
            "docker": ["containerization"],
            "kubernetes": ["k8s", "container orchestration"],
            "terraform": ["infrastructure as code", "iac"]
        }
    
    def _build_job_roles(self):
        """Build comprehensive job roles database"""
        return {
            "fullstack_developer": {
                "title": "Full Stack Developer",
                "category": "Engineering",
                "level": "Mid-Senior",
                "required_skills": [
                    {"skill": "JavaScript", "level": "Advanced", "priority": 1},
                    {"skill": "React", "level": "Intermediate", "priority": 1},
                    {"skill": "Node.js", "level": "Intermediate", "priority": 1},
                    {"skill": "SQL", "level": "Intermediate", "priority": 2},
                    {"skill": "HTML/CSS", "level": "Advanced", "priority": 1},
                    {"skill": "Git", "level": "Intermediate", "priority": 2}
                ]
            },
            "data_scientist": {
                "title": "Data Scientist",
                "category": "Data & Analytics",
                "level": "Senior",
                "required_skills": [
                    {"skill": "Python", "level": "Advanced", "priority": 1},
                    {"skill": "Machine Learning", "level": "Advanced", "priority": 1},
                    {"skill": "SQL", "level": "Advanced", "priority": 1},
                    {"skill": "Statistics", "level": "Intermediate", "priority": 2},
                    {"skill": "Data Analysis", "level": "Advanced", "priority": 1},
                    {"skill": "Pandas", "level": "Intermediate", "priority": 2}
                ]
            },
            "devops_engineer": {
                "title": "DevOps Engineer",
                "category": "Infrastructure",
                "level": "Mid-Senior",
                "required_skills": [
                    {"skill": "AWS", "level": "Intermediate", "priority": 1},
                    {"skill": "Docker", "level": "Intermediate", "priority": 1},
                    {"skill": "Kubernetes", "level": "Intermediate", "priority": 2},
                    {"skill": "Jenkins", "level": "Intermediate", "priority": 2},
                    {"skill": "Linux", "level": "Intermediate", "priority": 1},
                    {"skill": "Terraform", "level": "Intermediate", "priority": 2}
                ]
            },
            "cloud_architect": {
                "title": "Cloud Architect",
                "category": "Infrastructure",
                "level": "Senior",
                "required_skills": [
                    {"skill": "AWS", "level": "Expert", "priority": 1},
                    {"skill": "Azure", "level": "Advanced", "priority": 1},
                    {"skill": "Cloud Security", "level": "Advanced", "priority": 1},
                    {"skill": "Microservices", "level": "Intermediate", "priority": 2},
                    {"skill": "DevOps", "level": "Advanced", "priority": 1}
                ]
            },
            "qa_automation": {
                "title": "QA Automation Engineer",
                "category": "Quality Assurance",
                "level": "Mid-Level",
                "required_skills": [
                    {"skill": "Selenium", "level": "Advanced", "priority": 1},
                    {"skill": "Java", "level": "Intermediate", "priority": 1},
                    {"skill": "TestNG", "level": "Intermediate", "priority": 2},
                    {"skill": "API Testing", "level": "Intermediate", "priority": 2},
                    {"skill": "Jenkins", "level": "Beginner", "priority": 3}
                ]
            },
            "product_manager": {
                "title": "Product Manager",
                "category": "Product",
                "level": "Senior",
                "required_skills": [
                    {"skill": "Product Strategy", "level": "Advanced", "priority": 1},
                    {"skill": "Agile", "level": "Intermediate", "priority": 1},
                    {"skill": "Data Analysis", "level": "Intermediate", "priority": 2},
                    {"skill": "Stakeholder Management", "level": "Advanced", "priority": 1},
                    {"skill": "User Research", "level": "Intermediate", "priority": 2}
                ]
            },
            "ux_designer": {
                "title": "UX Designer",
                "category": "Design",
                "level": "Mid-Level",
                "required_skills": [
                    {"skill": "Figma", "level": "Advanced", "priority": 1},
                    {"skill": "User Research", "level": "Intermediate", "priority": 1},
                    {"skill": "Prototyping", "level": "Intermediate", "priority": 2},
                    {"skill": "UI/UX Design", "level": "Advanced", "priority": 1},
                    {"skill": "Design Systems", "level": "Intermediate", "priority": 2}
                ]
            },
            "cybersecurity_analyst": {
                "title": "Cybersecurity Analyst",
                "category": "Security",
                "level": "Mid-Senior",
                "required_skills": [
                    {"skill": "Network Security", "level": "Advanced", "priority": 1},
                    {"skill": "SIEM", "level": "Intermediate", "priority": 2},
                    {"skill": "Incident Response", "level": "Intermediate", "priority": 1},
                    {"skill": "Python", "level": "Intermediate", "priority": 2},
                    {"skill": "Cloud Security", "level": "Intermediate", "priority": 2}
                ]
            }
        }
    
    def _build_courses_database(self):
        """Build comprehensive courses database"""
        courses = [
            # Programming Languages
            {
                "title": "Python Programming Masterclass",
                "provider": "Udemy",
                "difficulty": "Beginner",
                "duration": 40,
                "price": 49.99,
                "skills": ["Python", "Programming", "OOP", "Algorithms"],
                "url": "https://www.udemy.com/python-programming/",
                "category": "Programming Languages",
                "rating": 4.7
            },
            {
                "title": "JavaScript: The Advanced Concepts",
                "provider": "Zero To Mastery",
                "difficulty": "Advanced",
                "duration": 25,
                "price": 39.99,
                "skills": ["JavaScript", "ES6", "React", "Node.js"],
                "url": "https://zerotomastery.io/courses/javascript-advanced/",
                "category": "Programming Languages",
                "rating": 4.8
            },
            
            # Web Technologies
            {
                "title": "React - The Complete Guide",
                "provider": "Udemy",
                "difficulty": "Intermediate",
                "duration": 48,
                "price": 59.99,
                "skills": ["React", "JavaScript", "Frontend", "Web Development"],
                "url": "https://www.udemy.com/react-the-complete-guide/",
                "category": "Web Technologies",
                "rating": 4.6
            },
            {
                "title": "Node.js Developer Course",
                "provider": "Coursera",
                "difficulty": "Intermediate",
                "duration": 35,
                "price": 79.99,
                "skills": ["Node.js", "JavaScript", "Backend", "API"],
                "url": "https://www.coursera.org/nodejs",
                "category": "Web Technologies",
                "rating": 4.5
            },
            
            # Data Science & AI
            {
                "title": "Machine Learning A-Z",
                "provider": "Udemy",
                "difficulty": "Intermediate",
                "duration": 44,
                "price": 69.99,
                "skills": ["Machine Learning", "Python", "Data Science", "AI"],
                "url": "https://www.udemy.com/machinelearning/",
                "category": "Data Science & AI",
                "rating": 4.7
            },
            {
                "title": "Data Science Specialization",
                "provider": "Coursera",
                "difficulty": "Intermediate",
                "duration": 60,
                "price": 99.99,
                "skills": ["Data Science", "Python", "Statistics", "Machine Learning"],
                "url": "https://www.coursera.org/specializations/data-science",
                "category": "Data Science & AI",
                "rating": 4.8
            },
            
            # Cloud & DevOps
            {
                "title": "AWS Certified Solutions Architect",
                "provider": "AWS Training",
                "difficulty": "Advanced",
                "duration": 45,
                "price": 99.99,
                "skills": ["AWS", "Cloud", "Architecture", "DevOps"],
                "url": "https://aws.amazon.com/training/",
                "category": "Cloud & DevOps",
                "rating": 4.7
            },
            {
                "title": "Docker and Kubernetes: The Complete Guide",
                "provider": "Udemy",
                "difficulty": "Intermediate",
                "duration": 23,
                "price": 49.99,
                "skills": ["Docker", "Kubernetes", "DevOps", "Containers"],
                "url": "https://www.udemy.com/docker-kubernetes/",
                "category": "Cloud & DevOps",
                "rating": 4.6
            },
            
            # Additional courses
            {
                "title": "Complete SQL Bootcamp",
                "provider": "Udemy",
                "difficulty": "Beginner",
                "duration": 20,
                "price": 29.99,
                "skills": ["SQL", "Database", "PostgreSQL", "MySQL"],
                "url": "https://www.udemy.com/sql-bootcamp/",
                "category": "Databases",
                "rating": 4.7
            },
            {
                "title": "Selenium WebDriver with Java",
                "provider": "Udemy",
                "difficulty": "Intermediate",
                "duration": 28,
                "price": 39.99,
                "skills": ["Selenium", "Java", "Automation", "Testing"],
                "url": "https://www.udemy.com/selenium-webdriver/",
                "category": "Testing & QA",
                "rating": 4.5
            },
            {
                "title": "Agile Crash Course",
                "provider": "Coursera",
                "difficulty": "Beginner",
                "duration": 15,
                "price": 19.99,
                "skills": ["Agile", "Scrum", "Project Management"],
                "url": "https://www.coursera.org/agile",
                "category": "Project Management",
                "rating": 4.4
            },
            {
                "title": "Leadership and Management",
                "provider": "edX",
                "difficulty": "Intermediate",
                "duration": 30,
                "price": 49.99,
                "skills": ["Leadership", "Management", "Soft Skills"],
                "url": "https://www.edx.org/leadership",
                "category": "Soft Skills",
                "rating": 4.6
            }
        ]
        return pd.DataFrame(courses)
    
    def _is_valid_skill(self, skill_candidate: str, context: str = "") -> bool:
        """Enhanced skill validation"""
        if not skill_candidate or len(skill_candidate) < 2:
            return False
        
        skill_lower = skill_candidate.lower().strip()
        
        # Check against non-skill terms
        if skill_lower in self.non_skill_terms:
            return False
        
        # Check length
        if len(skill_lower) < 2 or len(skill_lower) > 50:
            return False
        
        # Check for common patterns that are not skills
        invalid_patterns = [
            r'^\d+$',  # Pure numbers
            r'^[a-z]{1,2}$',  # Too short
            r'.*\d{4}.*',  # Contains years
        ]
        
        for pattern in invalid_patterns:
            if re.match(pattern, skill_lower):
                return False
        
        # Check if it's in our master skills list
        if skill_lower in self.master_skills:
            return True
        
        # Check synonyms
        for main_skill, synonyms in self.skill_synonyms.items():
            if skill_lower in synonyms:
                return True
        
        return False
    
    def extract_skills_with_context(self, text: str) -> Dict[str, Any]:
        """Enhanced skill extraction with proper filtering"""
        if not text or not isinstance(text, str):
            return {"skills": [], "metadata": {"error": "Invalid text input"}}
        
        # Generate cache key
        text_hash = hashlib.md5(text.encode()).hexdigest()[:16]
        if text_hash in self.evidence_cache:
            return self.evidence_cache[text_hash]
        
        detected_skills = {}
        text_lower = text.lower()
        
        # Method 1: Direct pattern matching with master skills
        for skill in self.master_skills:
            if self._is_valid_skill(skill):
                pattern = r'\b' + re.escape(skill) + r'\b'
                matches = re.findall(pattern, text_lower)
                if matches:
                    confidence = min(0.9, 0.6 + len(matches) * 0.1)
                    detected_skills[skill] = {
                        "method": "pattern",
                        "confidence": confidence,
                        "frequency": len(matches)
                    }
        
        # Method 2: Synonym expansion
        for main_skill, synonyms in self.skill_synonyms.items():
            for synonym in synonyms:
                if synonym in text_lower and main_skill not in detected_skills:
                    detected_skills[main_skill] = {
                        "method": "synonym",
                        "confidence": 0.7,
                        "matched_synonym": synonym,
                        "frequency": text_lower.count(synonym)
                    }
        
        # Convert to final format with proficiency analysis
        skills_with_proficiency = []
        for skill, data in detected_skills.items():
            proficiency_info = self._analyze_skill_proficiency(skill, text, data)
            
            # Categorize skill
            category = "Other"
            for cat_name, cat_data in self.skill_categories.items():
                if skill.lower() in cat_data["keywords"]:
                    category = cat_name
                    break
            
            skills_with_proficiency.append({
                "skill": skill,
                "proficiency_level": proficiency_info["level"],
                "proficiency_score": proficiency_info["score"],
                "confidence": data["confidence"],
                "evidence": proficiency_info["evidence"],
                "extraction_method": data["method"],
                "category": category
            })
        
        # Sort by confidence and limit to reasonable number
        skills_with_proficiency.sort(key=lambda x: x["confidence"], reverse=True)
        skills_with_proficiency = skills_with_proficiency[:30]  # Limit to top 30
        
        result = {
            "skills": skills_with_proficiency,
            "metadata": {
                "total_skills_found": len(skills_with_proficiency),
                "text_length": len(text),
                "processing_time": datetime.now().isoformat()
            }
        }
        
        self.evidence_cache[text_hash] = result
        return result
    
    def _analyze_skill_proficiency(self, skill: str, text: str, skill_data: Dict) -> Dict[str, Any]:
        """Analyze skill proficiency level"""
        text_lower = text.lower()
        skill_lower = skill.lower()
        
        # Default values
        level = "Intermediate"
        score = 2.0
        evidence = []
        
        # Analyze based on keywords and context
        expert_keywords = ["expert", "expertise", "master", "advanced", "senior", "lead"]
        intermediate_keywords = ["proficient", "experienced", "skilled", "competent"]
        beginner_keywords = ["basic", "beginner", "familiar", "knowledge"]
        
        # Check for proficiency indicators
        for keyword in expert_keywords:
            if keyword in text_lower and skill_lower in text_lower:
                level = "Expert"
                score = 4.0
                break
        
        if level == "Intermediate":
            for keyword in intermediate_keywords:
                if keyword in text_lower and skill_lower in text_lower:
                    level = "Advanced"
                    score = 3.0
                    break
        
        if level == "Intermediate":
            for keyword in beginner_keywords:
                if keyword in text_lower and skill_lower in text_lower:
                    level = "Beginner"
                    score = 1.0
                    break
        
        # Boost based on frequency
        frequency = skill_data.get("frequency", 1)
        if frequency > 3 and score < 4.0:
            score = min(4.0, score + 0.5)
            if score >= 3.5:
                level = "Expert"
            elif score >= 2.5:
                level = "Advanced"
        
        return {
            "level": level,
            "score": score,
            "evidence": evidence,
            "context_quality": 0.8
        }
    
    def comprehensive_gap_analysis(self, resume_skills: List[Dict], job_role_id: str) -> Dict[str, Any]:
        """Perform gap analysis between resume skills and job requirements"""
        if job_role_id not in self.job_roles:
            return {"error": f"Job role '{job_role_id}' not found"}
        
        job_data = self.job_roles[job_role_id]
        required_skills = job_data.get("required_skills", [])
        
        # Create skill map for quick lookup
        resume_skill_map = {skill["skill"].lower(): skill for skill in resume_skills}
        
        gaps = {
            "missing_critical": [],
            "level_gaps": [],
            "strengths": [],
            "summary": {}
        }
        
        total_required = len(required_skills)
        critical_gaps = 0
        level_gaps = 0
        
        for req_skill in required_skills:
            skill_name = req_skill["skill"].lower()
            required_level = req_skill["level"]
            
            if skill_name not in resume_skill_map:
                # Missing skill
                gaps["missing_critical"].append({
                    "skill": req_skill["skill"],
                    "required_level": required_level,
                    "current_level": "Not Found",
                    "priority": req_skill["priority"]
                })
                critical_gaps += 1
            else:
                # Check level gap
                current_skill = resume_skill_map[skill_name]
                current_level_score = self.level_hierarchy.get(current_skill["proficiency_level"], 1)
                required_level_score = self.level_hierarchy.get(required_level, 1)
                
                if current_level_score < required_level_score:
                    gaps["level_gaps"].append({
                        "skill": req_skill["skill"],
                        "required_level": required_level,
                        "current_level": current_skill["proficiency_level"],
                        "priority": req_skill["priority"]
                    })
                    level_gaps += 1
                else:
                    # Strength
                    gaps["strengths"].append({
                        "skill": req_skill["skill"],
                        "your_level": current_skill["proficiency_level"],
                        "required_level": required_level
                    })
        
        # Calculate match score
        match_score = ((total_required - critical_gaps - level_gaps) / max(1, total_required)) * 100
        
        gaps["summary"] = {
            "overall_match_score": round(match_score, 1),
            "total_required_skills": total_required,
            "missing_critical_skills": critical_gaps,
            "level_gap_skills": level_gaps,
            "strength_skills": len(gaps["strengths"]),
            "recommendation": self._get_recommendation_level(match_score),
            "job_title": job_data["title"],
            "job_level": job_data["level"]
        }
        
        return gaps
    
    def _get_recommendation_level(self, match_score: float) -> str:
        """Get recommendation based on match score"""
        if match_score >= 80:
            return "Excellent match! You're well-qualified for this role."
        elif match_score >= 60:
            return "Good match! Focus on developing a few key skills."
        elif match_score >= 40:
            return "Moderate match. Consider targeted skill development."
        else:
            return "Significant skill gaps. Consider comprehensive learning path."
    
    def get_course_recommendations(self, gap_skills: List[str], max_courses: int = 10) -> pd.DataFrame:
        """Get personalized course recommendations based on skill gaps"""
        recommendations = []
        
        for skill in gap_skills:
            skill_lower = skill.lower()
            # Find courses that match the skill
            for _, course in self.courses_df.iterrows():
                course_skills = ' '.join(course.get('skills', [])).lower()
                if skill_lower in course_skills:
                    # Calculate relevance score
                    relevance = course_skills.count(skill_lower) * 10
                    course_copy = course.copy()
                    course_copy['relevance_score'] = relevance
                    course_copy['gap_skill'] = skill
                    recommendations.append(course_copy)
        
        # Remove duplicates and sort by relevance
        if recommendations:
            rec_df = pd.DataFrame(recommendations)
            rec_df = rec_df.drop_duplicates(subset=['title'])
            rec_df = rec_df.sort_values('relevance_score', ascending=False)
            return rec_df.head(max_courses)
        
        return pd.DataFrame()

# =============================================================================
# NEW: Enhanced UI Components
# =============================================================================
def create_advanced_analytics_dashboard(skills_data, analytics_engine):
    """Create advanced analytics dashboard"""
    st.subheader("📈 Advanced Analytics")
    
    # Salary Impact Analysis
    salary_impact = analytics_engine.get_salary_impact_analysis(skills_data)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Estimated Total Salary", f"${salary_impact['total_estimated_salary']:,.0f}")
    with col2:
        st.metric("Skill Premium Value", f"${salary_impact['skill_premium_value']:,.0f}")
    with col3:
        st.metric("Average Skill Value", f"${salary_impact['average_skill_value']:,.0f}")
    
    # Market Demand Analysis
    skill_names = [s["skill"] for s in skills_data]
    market_demand = analytics_engine.get_market_demand_scores(skill_names)
    
    # Create demand chart
    if PLOTLY_AVAILABLE:
        demand_data = []
        for skill, data in market_demand.items():
            demand_data.append({
                "Skill": skill,
                "Demand Score": data["demand_score"],
                "Trend": data["market_trend"]
            })
        
        if demand_data:
            df_demand = pd.DataFrame(demand_data)
            fig = px.bar(df_demand, x="Skill", y="Demand Score", 
                        title="Market Demand for Your Skills",
                        color="Demand Score")
            st.plotly_chart(fig, use_container_width=True)

def create_career_advisor_interface(advisor, skills_data):
    """Create AI Career Advisor interface"""
    st.subheader("🤖 AI Career Advisor")
    
    experience_level = st.selectbox(
        "Your Current Experience Level",
        ["Entry", "Mid", "Senior", "Expert"],
        key="career_exp"
    )
    
    if st.button("Get Career Recommendations", key="career_btn"):
        with st.spinner("Analyzing your career potential..."):
            recommendations = advisor.get_career_recommendations(skills_data, experience_level)
        
        st.success("Career analysis complete!")
        
        # Display recommended paths
        for path in recommendations["recommended_paths"]:
            with st.expander(f"🎯 {path['career_path']} (Match: {path['match_score']:.1f}%)"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Growth Potential:** {path['growth_potential']}")
                    st.write("**Next Steps:**")
                    for step in path['next_steps']:
                        st.write(f"- {step}")
                with col2:
                    st.metric("Match Score", f"{path['match_score']:.1f}%")

# =============================================================================
# PRESERVED: Original UI Functions (with enhancements)
# =============================================================================
def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file"""
    try:
        if uploaded_file.type == "text/plain":
            return uploaded_file.read().decode("utf-8"), {}
        elif uploaded_file.type == "application/pdf" and PDF_AVAILABLE:
            reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text, {"pages": len(reader.pages)}
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                                  "application/msword"] and DOCX_AVAILABLE:
            doc = docx.Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text, {}
        else:
            return None, {"error": f"Unsupported file type: {uploaded_file.type}"}
    except Exception as e:
        return None, {"error": str(e)}

def create_skill_radar_chart(skills_data):
    """Create a radar chart for skills visualization"""
    if not PLOTLY_AVAILABLE or not skills_data:
        return None
    
    try:
        # Group by category and calculate average proficiency
        categories = {}
        for skill in skills_data:
            category = skill.get('category', 'Other')
            if category not in categories:
                categories[category] = []
            categories[category].append(skill['proficiency_score'])
        
        # Calculate averages
        avg_scores = {}
        for category, scores in categories.items():
            avg_scores[category] = sum(scores) / len(scores)
        
        # Create radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=list(avg_scores.values()),
            theta=list(avg_scores.keys()),
            fill='toself',
            name='Skill Proficiency'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 4]
                )),
            showlegend=False,
            title="Skill Proficiency by Category"
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating chart: {e}")
        return None

def main():
    """Main Streamlit application - Enhanced with New Features"""
    st.title("🧠 AI Skill Gap Analyzer Pro")
    st.markdown("### Complete Career Analysis Platform with Advanced AI Features")
    
    # Initialize analyzer and new modules
    if 'analyzer' not in st.session_state:
        with st.spinner("🚀 Initializing AI analyzer with advanced features..."):
            st.session_state.analyzer = AdvancedSkillGapAnalyzer()
            # Initialize new modules
            st.session_state.analytics_engine = AnalyticsEngine(st.session_state.analyzer)
            st.session_state.report_generator = ReportGenerator(
                st.session_state.analyzer, 
                st.session_state.analytics_engine
            )
            st.session_state.learning_optimizer = LearningPathOptimizer(st.session_state.analyzer)
            st.session_state.career_advisor = AICareerAdvisor(st.session_state.analyzer)
    
    analyzer = st.session_state.analyzer
    analytics_engine = st.session_state.analytics_engine
    report_generator = st.session_state.report_generator
    
    # Enhanced sidebar with new features
    with st.sidebar:
        st.header("🔧 System Status")
        st.write(f"**NLP Engine:** {'✅ Available' if analyzer.nlp else '❌ Not available'}")
        st.write(f"**Skills Database:** {len(analyzer.master_skills)} skills")
        st.write(f"**Job Roles:** {len(analyzer.job_roles)} roles")
        st.write(f"**Courses:** {len(analyzer.courses_df)} courses")
        st.write(f"**Advanced Analytics:** ✅ Available")
        st.write(f"**AI Career Advisor:** ✅ Available")
        
        st.header("📊 Quick Stats")
        if 'skills_result' in st.session_state:
            skills_data = st.session_state.skills_result["skills"]
            st.metric("Your Skills", len(skills_data))
            expert_count = len([s for s in skills_data if s["proficiency_level"] == "Expert"])
            st.metric("Expert Skills", expert_count)
        
        if 'gaps_result' in st.session_state:
            gaps = st.session_state.gaps_result
            if "error" not in gaps:
                st.metric("Match Score", f"{gaps['summary']['overall_match_score']}%")
        
        # New: Quick Actions
        st.header("⚡ Quick Actions")
        if st.button("Generate Comprehensive Report"):
            if 'skills_result' in st.session_state:
                st.session_state.generate_report = True
    
    # Enhanced tabs with new features
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📄 Resume Analysis", 
        "📊 Skill Dashboard", 
        "📈 Advanced Analytics",
        "🎯 Gap Analysis", 
        "🎓 Learning Path",
        "🤖 Career Advisor"
    ])
    
    # Tab 1: Resume Analysis (Enhanced)
    with tab1:
        st.header("📄 Resume Skill Extraction")
        
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF, DOCX, or TXT)",
            type=["pdf", "docx", "txt"],
            help="Supported formats: PDF, Word documents, and text files"
        )
        
        if uploaded_file is not None:
            with st.spinner("Extracting text from your resume..."):
                text, metadata = extract_text_from_file(uploaded_file)
            
            if text is None:
                st.error(f"Error processing file: {metadata.get('error', 'Unknown error')}")
            elif len(text.strip()) < 100:
                st.warning("The extracted text seems too short. Please check if the file contains readable text.")
            else:
                # Show file info
                with st.expander("📄 File Information"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**File name:** {uploaded_file.name}")
                        st.write(f"**File size:** {uploaded_file.size} bytes")
                    with col2:
                        st.write(f"**Text length:** {len(text)} characters")
                        if metadata.get('pages'):
                            st.write(f"**Pages:** {metadata['pages']}")
                
                if st.button("🚀 Analyze Skills", type="primary", use_container_width=True):
                    with st.spinner("🤖 Analyzing skills with AI..."):
                        skills_result = analyzer.extract_skills_with_context(text)
                    
                    if skills_result["skills"]:
                        st.session_state.skills_result = skills_result
                        st.session_state.resume_text = text
                        st.success(f"✅ Found {len(skills_result['skills'])} skills!")
                        
                        # Auto-generate analytics
                        with st.spinner("📈 Generating advanced analytics..."):
                            st.session_state.analytics_data = analytics_engine.get_salary_impact_analysis(
                                skills_result["skills"]
                            )
                    else:
                        st.warning("No skills detected. This could be because:")
                        st.write("- The resume format is not supported")
                        st.write("- Skills are mentioned in unconventional ways")
    
    # Tab 2: Skill Dashboard (Enhanced)
    with tab2:
        st.header("📊 Skill Dashboard")
        
        if 'skills_result' not in st.session_state:
            st.info("👆 Please upload and analyze your resume first in the Resume Analysis tab")
        else:
            skills_data = st.session_state.skills_result["skills"]
            
            # Enhanced metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Total Skills", len(skills_data))
            with col2:
                expert_skills = len([s for s in skills_data if s["proficiency_level"] == "Expert"])
                st.metric("Expert Skills", expert_skills)
            with col3:
                avg_confidence = sum(s["confidence"] for s in skills_data) / len(skills_data)
                st.metric("Avg Confidence", f"{avg_confidence:.2f}")
            with col4:
                unique_categories = len(set(s.get('category', 'Other') for s in skills_data))
                st.metric("Skill Categories", unique_categories)
            with col5:
                if 'analytics_data' in st.session_state:
                    salary_impact = st.session_state.analytics_data['total_estimated_salary']
                    st.metric("Est. Salary Impact", f"${salary_impact:,.0f}")
            
            # Enhanced visualizations
            col_viz1, col_viz2 = st.columns(2)
            
            with col_viz1:
                # Skill distribution by category
                if skills_data:
                    category_counts = {}
                    for skill in skills_data:
                        category = skill.get('category', 'Other')
                        category_counts[category] = category_counts.get(category, 0) + 1
                    
                    if category_counts:
                        fig = px.pie(
                            values=list(category_counts.values()),
                            names=list(category_counts.keys()),
                            title="Skills by Category"
                        )
                        st.plotly_chart(fig, use_container_width=True)
            
            with col_viz2:
                # Proficiency distribution
                if skills_data:
                    level_counts = {}
                    for skill in skills_data:
                        level = skill["proficiency_level"]
                        level_counts[level] = level_counts.get(level, 0) + 1
                    
                    if level_counts:
                        fig = px.bar(
                            x=list(level_counts.keys()),
                            y=list(level_counts.values()),
                            title="Skills by Proficiency Level",
                            labels={'x': 'Proficiency Level', 'y': 'Count'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
            
            # Enhanced skills table with analytics
            st.subheader("🔍 Detailed Skills Breakdown with Market Insights")
            
            # Filter options
            col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)
            with col_filter1:
                min_confidence = st.slider("Minimum Confidence", 0.0, 1.0, 0.5, 0.1)
            with col_filter2:
                selected_category = st.selectbox("Filter by Category", 
                                               ["All"] + list(set(s.get('category', 'Other') for s in skills_data)))
            with col_filter3:
                selected_level = st.selectbox("Filter by Level", 
                                           ["All", "Beginner", "Intermediate", "Advanced", "Expert"])
            with col_filter4:
                show_analytics = st.checkbox("Show Market Insights", value=True)
            
            # Filter skills
            filtered_skills = skills_data
            if selected_category != "All":
                filtered_skills = [s for s in filtered_skills if s.get('category', 'Other') == selected_category]
            if selected_level != "All":
                filtered_skills = [s for s in filtered_skills if s["proficiency_level"] == selected_level]
            filtered_skills = [s for s in filtered_skills if s["confidence"] >= min_confidence]
            
            # Display filtered skills with enhanced insights
            for i, skill in enumerate(filtered_skills):
                with st.expander(f"{skill['skill'].title()} | {skill['proficiency_level']} | Confidence: {skill['confidence']:.2f}"):
                    col_s1, col_s2 = st.columns(2)
                    with col_s1:
                        st.write(f"**Category:** {skill.get('category', 'Other')}")
                        st.write(f"**Extraction Method:** {skill['extraction_method']}")
                        st.write(f"**Proficiency Score:** {skill['proficiency_score']:.1f}/4.0")
                    
                    with col_s2:
                        if show_analytics:
                            # Show market insights
                            market_data = analytics_engine.get_market_demand_scores([skill['skill']])
                            if skill['skill'] in market_data:
                                insight = market_data[skill['skill']]
                                st.write(f"**Market Demand:** {insight['demand_score']}/100")
                                st.write(f"**Trend:** {insight['market_trend']}")
                                st.write(f"**Recommendation:** {insight['recommendation']}")
    
    # NEW TAB: Advanced Analytics
    with tab3:
        st.header("📈 Advanced Analytics & Market Insights")
        
        if 'skills_result' not in st.session_state:
            st.info("👆 Please upload and analyze your resume first")
        else:
            skills_data = st.session_state.skills_result["skills"]
            
            # Salary Impact Analysis
            st.subheader("💰 Salary Impact Analysis")
            salary_impact = analytics_engine.get_salary_impact_analysis(skills_data)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Estimated Salary", f"${salary_impact['total_estimated_salary']:,.0f}")
            with col2:
                st.metric("Skill Premium Value", f"${salary_impact['skill_premium_value']:,.0f}")
            with col3:
                st.metric("Average Skill Value", f"${salary_impact['average_skill_value']:,.0f}")
            
            # Market Demand Analysis
            st.subheader("📊 Market Demand Analysis")
            skill_names = [s["skill"] for s in skills_data]
            market_demand = analytics_engine.get_market_demand_scores(skill_names)
            
            if PLOTLY_AVAILABLE and market_demand:
                demand_data = []
                for skill, data in market_demand.items():
                    demand_data.append({
                        "Skill": skill,
                        "Demand Score": data["demand_score"],
                        "Trend": data["market_trend"]
                    })
                
                df_demand = pd.DataFrame(demand_data)
                fig = px.bar(df_demand, x="Skill", y="Demand Score", 
                            title="Market Demand for Your Skills",
                            color="Demand Score")
                st.plotly_chart(fig, use_container_width=True)
            
            # Skill Trends Analysis
            st.subheader("📈 Skill Trends & Future Outlook")
            trend_analysis = analytics_engine.get_skill_trend_analysis(skill_names)
            
            for skill, trends in trend_analysis.items():
                with st.expander(f"📊 {skill} Trend Analysis"):
                    col_t1, col_t2 = st.columns(2)
                    with col_t1:
                        st.write("**Popularity Trend:**")
                        for year, score in trends["trends"].items():
                            st.write(f"{year}: {score}/100")
                        st.write(f"**Growth Rate:** {trends['growth_rate']:.1f}%")
                    with col_t2:
                        st.write("**Future Outlook:**")
                        st.info(trends["future_outlook"])
    
    # Tab 4: Gap Analysis (Enhanced)
    with tab4:
        st.header("🎯 Skill Gap Analysis")
        
        if 'skills_result' not in st.session_state:
            st.info("👆 Please upload and analyze your resume first")
        else:
            skills_data = st.session_state.skills_result["skills"]
            
            # Enhanced job role selection
            st.subheader("Select Target Job Role")
            
            col_job1, col_job2, col_job3 = st.columns(3)
            with col_job1:
                job_categories = list(set(role["category"] for role in analyzer.job_roles.values()))
                selected_category = st.selectbox("Job Category", ["All"] + job_categories)
            with col_job2:
                experience_levels = list(set(role["level"] for role in analyzer.job_roles.values()))
                selected_level = st.selectbox("Experience Level", ["All"] + experience_levels)
            with col_job3:
                # New: Salary expectation filter
                min_salary = st.number_input("Minimum Expected Salary ($)", 
                                           min_value=50000, max_value=300000, 
                                           value=80000, step=10000)
            
            # Filter job roles
            filtered_roles = {}
            for role_id, role_data in analyzer.job_roles.items():
                if selected_category != "All" and role_data["category"] != selected_category:
                    continue
                if selected_level != "All" and role_data["level"] != selected_level:
                    continue
                filtered_roles[role_id] = role_data
            
            if not filtered_roles:
                st.warning("No job roles match the selected filters.")
            else:
                selected_role = st.selectbox(
                    "Choose a job role:",
                    list(filtered_roles.keys()),
                    format_func=lambda x: f"{filtered_roles[x]['title']} ({filtered_roles[x]['level']})"
                )
                
                if st.button("🔍 Analyze Gaps", type="primary", use_container_width=True):
                    with st.spinner("Analyzing skill gaps with enhanced analytics..."):
                        gaps = analyzer.comprehensive_gap_analysis(skills_data, selected_role)
                    
                    st.session_state.gaps_result = gaps
                    st.session_state.selected_role = selected_role
            
            # Enhanced gap analysis results
            if 'gaps_result' in st.session_state:
                gaps = st.session_state.gaps_result
                selected_role_data = analyzer.job_roles[st.session_state.selected_role]
                
                if "error" in gaps:
                    st.error(f"Error: {gaps['error']}")
                else:
                    summary = gaps["summary"]
                    
                    # Enhanced overall match score display
                    st.subheader(f"📊 Analysis for {summary['job_title']} ({summary['job_level']})")
                    
                    col_score1, col_score2, col_score3 = st.columns([1, 2, 1])
                    with col_score2:
                        match_score = summary['overall_match_score']
                        st.metric("Overall Match Score", f"{match_score}%")
                        st.progress(match_score / 100)
                        
                        # New: Salary impact estimation
                        st.write(f"**Recommendation:** {summary['recommendation']}")
                        
                        # Estimate salary impact of closing gaps
                        if match_score < 80:
                            potential_increase = (100 - match_score) * 500  # $500 per percentage point
                            st.info(f"💡 Closing skill gaps could increase salary by ~${potential_increase:,.0f}")
                    
                    # Enhanced detailed analysis
                    col_gap1, col_gap2 = st.columns(2)
                    
                    with col_gap1:
                        st.subheader("🚨 Critical Gaps")
                        if gaps["missing_critical"]:
                            for gap in gaps["missing_critical"]:
                                with st.container():
                                    st.error(f"**{gap['skill']}** (Priority {gap['priority']})")
                                    st.write(f"❌ Required: {gap['required_level']} | Current: Not Found")
                                    
                                    # New: Market demand for missing skill
                                    market_data = analytics_engine.get_market_demand_scores([gap['skill']])
                                    if gap['skill'] in market_data:
                                        demand = market_data[gap['skill']]['demand_score']
                                        st.write(f"📈 Market Demand: {demand}/100")
                                    
                                    st.divider()
                        else:
                            st.success("🎉 No critical skills missing!")
                    
                    with col_gap2:
                        st.subheader("📈 Improvement Areas")
                        if gaps["level_gaps"]:
                            for gap in gaps["level_gaps"]:
                                with st.container():
                                    st.warning(f"**{gap['skill']}** (Priority {gap['priority']})")
                                    st.write(f"📊 Current: {gap['current_level']} → Required: {gap['required_level']}")
                                    
                                    # New: Learning time estimation
                                    level_diff = (analyzer.level_hierarchy[gap['required_level']] - 
                                                analyzer.level_hierarchy[gap['current_level']])
                                    estimated_hours = level_diff * 40  # 40 hours per level
                                    st.write(f"⏱️ Estimated learning time: {estimated_hours} hours")
                                    
                                    st.divider()
                        else:
                            st.success("🎉 All skills meet required levels!")
                    
                    # Enhanced strengths section with market value
                    if gaps["strengths"]:
                        st.subheader("💪 Your Strengths")
                        strength_cols = st.columns(3)
                        for i, strength in enumerate(gaps["strengths"][:6]):
                            with strength_cols[i % 3]:
                                st.success(f"**{strength['skill']}**")
                                st.caption(f"Your level: {strength['your_level']} (Required: {strength['required_level']})")
                                
                                # New: Market value display
                                market_data = analytics_engine.get_market_demand_scores([strength['skill']])
                                if strength['skill'] in market_data:
                                    demand = market_data[strength['skill']]['demand_score']
                                    st.caption(f"Market Demand: {demand}/100")
    
    # Tab 5: Learning Path (Enhanced)
    with tab5:
        st.header("🎓 Personalized Learning Path")
        
        if 'gaps_result' not in st.session_state:
            st.info("👆 Please complete gap analysis first to get personalized recommendations")
        else:
            gaps = st.session_state.gaps_result
            
            if "error" in gaps:
                st.error(f"Cannot generate recommendations: {gaps['error']}")
            else:
                # Get gap skills
                missing_skills = [gap["skill"] for gap in gaps["missing_critical"]]
                level_gap_skills = [gap["skill"] for gap in gaps["level_gaps"]]
                all_gap_skills = missing_skills + level_gap_skills
                
                if not all_gap_skills:
                    st.success("🎉 No skill gaps detected! You're well-prepared for this role.")
                    st.balloons()
                else:
                    st.subheader("💡 Skills Development Focus")
                    st.write(f"**Priority skills to learn:** {', '.join(all_gap_skills)}")
                    
                    # Enhanced learning path customization
                    st.subheader("🎯 Customize Your Learning Path")
                    
                    col_learn1, col_learn2 = st.columns(2)
                    with col_learn1:
                        learning_style = st.selectbox(
                            "Preferred Learning Style",
                            ["Self-paced", "Structured", "Video-based", "Project-based"]
                        )
                        max_budget = st.slider("Maximum Budget ($)", 0, 500, 100)
                        weekly_hours = st.slider("Weekly Study Hours", 1, 40, 10)
                    
                    with col_learn2:
                        time_commitment = st.selectbox(
                            "Preferred Timeline",
                            ["Accelerated (3-6 months)", "Standard (6-12 months)", "Extended (12+ months)"]
                        )
                        difficulty_pref = st.selectbox(
                            "Difficulty Preference",
                            ["Beginner", "Intermediate", "Advanced", "Mixed"]
                        )
                    
                    # New: AI-optimized learning path
                    if st.button("🤖 Generate AI-Optimized Learning Plan", type="primary"):
                        with st.spinner("Optimizing your learning path with AI..."):
                            constraints = {
                                "weekly_hours": weekly_hours,
                                "max_budget": max_budget,
                                "learning_style": learning_style
                            }
                            optimized_path = st.session_state.learning_optimizer.optimize_learning_path(
                                all_gap_skills, constraints
                            )
                        
                        st.session_state.optimized_path = optimized_path
                    
                    # Display optimized learning path
                    if 'optimized_path' in st.session_state:
                        path = st.session_state.optimized_path
                        
                        st.subheader("📅 AI-Optimized Learning Schedule")
                        
                        col_path1, col_path2 = st.columns(2)
                        with col_path1:
                            st.metric("Total Duration", f"{path['total_duration_hours']} hours")
                            st.metric("Estimated Completion", f"{path['estimated_completion_weeks']:.1f} weeks")
                        
                        with col_path2:
                            st.metric("Weekly Commitment", f"{path['weekly_commitment']} hours/week")
                            st.metric("Learning Efficiency", "AI-Optimized")
                        
                        # Display learning schedule
                        st.subheader("📚 Learning Modules Schedule")
                        for module in path['optimized_path']:
                            with st.expander(f"🗓️ Weeks {module['start_week']}-{module['end_week']}: {module['skill']} - {module['module']}"):
                                col_m1, col_m2 = st.columns(2)
                                with col_m1:
                                    st.write(f"**Duration:** {module['duration_hours']} hours")
                                    st.write(f"**Difficulty:** {module['difficulty']}")
                                with col_m2:
                                    st.write(f"**Timeline:** {module['duration_weeks']:.1f} weeks")
                                    if module.get('review_weeks'):
                                        st.write(f"**Reviews:** Weeks {module['review_weeks'][0]}, {module['review_weeks'][1]}")
                    
                    # Course recommendations (existing functionality)
                    if st.button("🔄 Generate Course Recommendations", type="primary"):
                        with st.spinner("Finding the best courses for you..."):
                            recommendations = analyzer.get_course_recommendations(all_gap_skills, max_courses=8)
                        
                        if not recommendations.empty:
                            st.subheader("📚 Recommended Courses")
                            
                            for category in recommendations['category'].unique():
                                category_courses = recommendations[recommendations['category'] == category]
                                
                                st.markdown(f"### {category}")
                                
                                for _, course in category_courses.iterrows():
                                    with st.expander(f"🎓 {course['title']} - {course['provider']} ⭐ {course['rating']}"):
                                        col_c1, col_c2 = st.columns([3, 1])
                                        with col_c1:
                                            st.write(f"**Difficulty:** {course['difficulty']}")
                                            st.write(f"**Duration:** {course['duration']} hours")
                                            st.write(f"**Skills:** {', '.join(course.get('skills', []))}")
                                            st.write(f"**Relevance Score:** {course.get('relevance_score', 0)}")
                                        with col_c2:
                                            st.write(f"**Price:** ${course['price']}")
                                            if course.get('url'):
                                                st.markdown(f"[🔗 Visit Course]({course['url']})")
                                
                                st.divider()
    
    # NEW TAB: Career Advisor
    with tab6:
        st.header("🤖 AI Career Advisor")
        
        if 'skills_result' not in st.session_state:
            st.info("👆 Please upload and analyze your resume first")
        else:
            skills_data = st.session_state.skills_result["skills"]
            
            # Career advisor interface
            st.subheader("🎯 Career Path Recommendations")
            
            col_adv1, col_adv2 = st.columns(2)
            with col_adv1:
                experience_level = st.selectbox(
                    "Your Current Experience Level",
                    ["Entry", "Mid", "Senior", "Expert"],
                    key="advisor_exp"
                )
                
                industry_preference = st.selectbox(
                    "Industry Preference",
                    ["Technology", "Finance", "Healthcare", "Education", "Any"]
                )
            
            with col_adv2:
                career_goals = st.selectbox(
                    "Primary Career Goal",
                    ["Technical Excellence", "Management", "Entrepreneurship", "Research", "Consulting"]
                )
                
                relocation_willingness = st.selectbox(
                    "Relocation Willingness",
                    ["Not willing", "Open to relocation", "Actively seeking relocation"]
                )
            
            if st.button("🎯 Get AI Career Advice", type="primary"):
                with st.spinner("🤖 Analyzing your career potential with AI..."):
                    recommendations = st.session_state.career_advisor.get_career_recommendations(
                        skills_data, experience_level
                    )
                
                st.session_state.career_recommendations = recommendations
                st.success("AI career analysis complete!")
            
            # Display career recommendations
            if 'career_recommendations' in st.session_state:
                recommendations = st.session_state.career_recommendations
                
                st.subheader("💡 Recommended Career Paths")
                
                for path in recommendations["recommended_paths"]:
                    with st.expander(f"🎯 {path['career_path']} - Match: {path['match_score']:.1f}%"):
                        col_p1, col_p2 = st.columns(2)
                        with col_p1:
                            st.write(f"**Growth Potential:** {path['growth_potential']}")
                            st.write("**Recommended Next Steps:**")
                            for step in path['next_steps']:
                                st.write(f"✅ {step}")
                        
                        with col_p2:
                            # Visual match score
                            st.metric("AI Match Score", f"{path['match_score']:.1f}%")
                            st.progress(path['match_score'] / 100)
                            
                            # Action buttons
                            if st.button(f"Explore {path['career_path']} Path", key=path['career_path']):
                                st.info(f"Detailed analysis for {path['career_path']} would be shown here")
                
                # Strengths alignment
                if recommendations.get("strengths_alignment"):
                    st.subheader("💪 Your Strengths Alignment")
                    
                    for path_name, alignment in recommendations["strengths_alignment"].items():
                        with st.expander(f"📊 {path_name} Alignment"):
                            st.write(f"**Expert Skills:** {alignment.get('expert_skills_count', 0)}")
                            st.write(f"**Alignment Score:** {alignment.get('alignment_score', 0):.1f}%")
                            if alignment.get('leverage_points'):
                                st.write("**Key Strengths to Leverage:**")
                                for strength in alignment['leverage_points']:
                                    st.write(f"▪️ {strength}")
                
                # Growth opportunities
                if recommendations.get("growth_opportunities"):
                    st.subheader("🚀 Growth Opportunities")
                    
                    for opportunity in recommendations["growth_opportunities"]:
                        st.write(f"🌟 {opportunity}")

# =============================================================================
# NEW: Report Generation Feature
# =============================================================================
def generate_comprehensive_report():
    """Generate and display comprehensive report"""
    if 'skills_result' not in st.session_state:
        st.warning("No skills data available for report generation")
        return
    
    skills_data = st.session_state.skills_result["skills"]
    gaps_data = st.session_state.gaps_result if 'gaps_result' in st.session_state else {"error": "No gap analysis"}
    
    with st.spinner("📊 Generating comprehensive report..."):
        report = st.session_state.report_generator.generate_comprehensive_report(skills_data, gaps_data)
    
    st.success("✅ Comprehensive report generated!")
    
    # Display report sections
    st.header("📋 Comprehensive Skills Analysis Report")
    
    # Executive Summary
    st.subheader("📈 Executive Summary")
    summary = report["executive_summary"]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Skills", summary["total_skills"])
    with col2:
        st.metric("Expert Skills", summary["expert_skills"])
    with col3:
        st.metric("Match Score", f"{summary['match_score']}%")
    with col4:
        st.metric("Critical Gaps", summary["critical_gaps"])
    
    st.write(f"**Overall Assessment:** {summary['overall_assessment']}")
    
    # Detailed sections
    with st.expander("🔍 Detailed Skill Analysis"):
        if report.get("skill_analysis"):
            st.write("Salary impact and market demand analysis would be displayed here")
    
    with st.expander("🎯 Gap Analysis Details"):
        if report.get("gap_analysis"):
            st.write("Detailed gap analysis would be displayed here")
    
    with st.expander("📈 Market Insights"):
        if report.get("market_insights"):
            st.write("Market trends and insights would be displayed here")
    
    with st.expander("💡 Recommendations"):
        if report.get("recommendations"):
            st.write("Personalized recommendations would be displayed here")
    
    # Export option
    if st.button("📤 Export Report as PDF"):
        st.info("PDF export functionality would be implemented here")

# Run the enhanced application
if __name__ == "__main__":
    main()