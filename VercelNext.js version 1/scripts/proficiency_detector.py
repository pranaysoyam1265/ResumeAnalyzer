import re
import logging
from typing import List, Dict, Any
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProficiencyDetector:
    """
    Detects proficiency levels for extracted skills based on contextual cues and frequency.
    """
    
    def __init__(self):
        """
        Initializes the ProficiencyDetector.
        """
        # Define keywords and their associated proficiency levels
        # These can be expanded and refined
        self.proficiency_keywords = {
            "expert": ["expert in", "mastery of", "deep understanding of", "highly proficient in", "advanced knowledge of"],
            "proficient": ["proficient in", "skilled in", "experienced with", "strong background in", "familiar with"],
            "basic": ["basic knowledge of", "familiarity with", "exposure to", "understanding of"]
        }
        
        # Reverse map for easier lookup
        self.keyword_to_level = {}
        for level, keywords in self.proficiency_keywords.items():
            for keyword in keywords:
                self.keyword_to_level[keyword] = level
        
        logger.info("ProficiencyDetector initialized.")

    def _analyze_contextual_cues(self, text: str, skill: str) -> str:
        """
        Analyzes the text around a skill for contextual cues indicating proficiency.
        
        Args:
            text: The full text (e.g., resume or job description).
            skill: The skill to analyze.
            
        Returns:
            A string representing the detected proficiency level ("expert", "proficient", "basic", or "unknown").
        """
        text_lower = text.lower()
        skill_lower = skill.lower()
        
        # Search for proficiency keywords around the skill
        for keyword, level in self.keyword_to_level.items():
            # Look for keyword before the skill
            if re.search(r'\b' + re.escape(keyword) + r'\s+(?:of\s+)?' + re.escape(skill_lower) + r'\b', text_lower):
                return level
            # Look for keyword after the skill (e.g., "Python expert")
            if re.search(r'\b' + re.escape(skill_lower) + r'\s+' + re.escape(keyword.replace(" in", "").replace(" of", "")) + r'\b', text_lower):
                return level
        
        return "unknown"

    def _analyze_frequency(self, text: str, skill: str) -> int:
        """
        Counts the occurrences of a skill in the text.
        
        Args:
            text: The full text.
            skill: The skill to count.
            
        Returns:
            The frequency count of the skill.
        """
        return text.lower().count(skill.lower())

    def detect_proficiency(self, text: str, extracted_skills: List[str]) -> Dict[str, Any]:
        """
        Detects proficiency levels for a list of extracted skills.
        
        Args:
            text: The original text (resume or job description).
            extracted_skills: A list of skills extracted from the text.
            
        Returns:
            A dictionary where keys are skills and values are dictionaries containing
            'proficiency_level' and 'frequency'.
        """
        logger.info("Starting proficiency detection...")
        
        skill_proficiencies = {}
        for skill in extracted_skills:
            proficiency_level = self._analyze_contextual_cues(text, skill)
            frequency = self._analyze_frequency(text, skill)
            
            skill_proficiencies[skill] = {
                "proficiency_level": proficiency_level,
                "frequency": frequency
            }
            logger.debug(f"Skill: {skill}, Level: {proficiency_level}, Frequency: {frequency}")
            
        logger.info("Proficiency detection completed.")
        return skill_proficiencies

def main():
    """Main execution function for testing the proficiency detector."""
    print("=" * 60)
    print("RESUME SKILL GAP ANALYZER - PROFICIENCY DETECTION")
    print("=" * 60)
    
    detector = ProficiencyDetector()
    
    # Example 1: Resume text
    sample_resume_text = """
    I am an expert in Python and have a deep understanding of Machine Learning algorithms.
    I am proficient in SQL and have strong background in data analysis.
    I have basic knowledge of AWS and some exposure to Docker.
    Experienced with Flask and Django. Python is my primary language.
    """
    extracted_skills_resume = ["Python", "Machine Learning", "SQL", "Data Analysis", "AWS", "Docker", "Flask", "Django"]
    
    print("\n--- Detecting proficiency in sample resume ---")
    resume_proficiencies = detector.detect_proficiency(sample_resume_text, extracted_skills_resume)
    for skill, data in resume_proficiencies.items():
        print(f"- {skill}: Level={data['proficiency_level']}, Frequency={data['frequency']}")

    # Example 2: Job description text
    sample_job_desc_text = """
    Seeking a candidate with advanced knowledge of Java and proficient in Spring Boot.
    Familiarity with PostgreSQL is a plus. Experience with Agile methodologies required.
    """
    extracted_skills_job_desc = ["Java", "Spring Boot", "PostgreSQL", "Agile"]
    
    print("\n--- Detecting proficiency in sample job description ---")
    job_desc_proficiencies = detector.detect_proficiency(sample_job_desc_text, extracted_skills_job_desc)
    for skill, data in job_desc_proficiencies.items():
        print(f"- {skill}: Level={data['proficiency_level']}, Frequency={data['frequency']}")
        
    print("\n" + "=" * 60)
    print("PROFICIENCY DETECTION TEST COMPLETED.")
    print("=" * 60)

if __name__ == "__main__":
    main()
