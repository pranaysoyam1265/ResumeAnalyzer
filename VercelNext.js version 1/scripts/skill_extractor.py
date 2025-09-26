import spacy
import re
from neo4j import GraphDatabase
import logging
from pathlib import Path
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SkillExtractor:
    """
    Multi-layered Skill Extraction Pipeline for Resume Skill Gap Analyzer.
    
    This class integrates a custom NER model, rule-based extraction, and knowledge graph
    normalization to extract skills from text.
    """
    
    def __init__(self, 
                 ner_model_path: str = "models/ner_model/model-best",
                 neo4j_uri: str = "bolt://localhost:7687", 
                 neo4j_user: str = "neo4j", 
                 neo4j_password: str = "password"):
        """
        Initialize the SkillExtractor with paths to the NER model and Neo4j credentials.
        
        Args:
            ner_model_path: Path to the trained spaCy NER model.
            neo4j_uri: URI for the Neo4j database.
            neo4j_user: Username for Neo4j authentication.
            neo4j_password: Password for Neo4j authentication.
        """
        self.ner_model_path = Path(ner_model_path)
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        
        self.nlp = self._load_ner_model()
        self.neo4j_driver = self._connect_to_neo4j()
        
        # Define rule-based patterns (can be expanded)
        self.rule_based_patterns = [
            r'\b(python|java|javascript|c\+\+|c#|go|ruby|php|swift|kotlin)\b',
            r'\b(react|angular|vue|node\.js|django|flask|spring|rails)\b',
            r'\b(sql|mysql|postgresql|mongodb|redis|oracle)\b',
            r'\b(aws|azure|gcp|docker|kubernetes|terraform)\b',
            r'\b(machine learning|deep learning|data science|nlp|computer vision)\b',
            r'\b(git|jira|agile|scrum)\b'
        ]
        logger.info("SkillExtractor initialized.")

    def _load_ner_model(self):
        """Loads the custom spaCy NER model."""
        logger.info(f"Loading NER model from {self.ner_model_path}...")
        try:
            nlp = spacy.load(self.ner_model_path)
            logger.info("NER model loaded successfully.")
            return nlp
        except OSError:
            logger.error(f"NER model not found at {self.ner_model_path}. Please ensure it is trained and saved.")
            raise
        except Exception as e:
            logger.error(f"Error loading NER model: {e}")
            raise

    def _connect_to_neo4j(self):
        """Connects to the Neo4j database."""
        logger.info(f"Connecting to Neo4j at {self.neo4j_uri}...")
        try:
            driver = GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password))
            driver.verify_connectivity()
            logger.info("Successfully connected to Neo4j.")
            return driver
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    def close_neo4j_connection(self):
        """Closes the Neo4j database connection."""
        if self.neo4j_driver:
            self.neo4j_driver.close()
            logger.info("Neo4j connection closed.")

    def _extract_with_ner(self, text: str) -> List[str]:
        """Extracts skills using the custom NER model."""
        doc = self.nlp(text)
        ner_skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"] # Assuming "SKILL" is the label
        logger.debug(f"NER extracted skills: {ner_skills}")
        return ner_skills

    def _extract_with_rules(self, text: str) -> List[str]:
        """Extracts skills using rule-based patterns."""
        rule_skills = []
        text_lower = text.lower()
        for pattern in self.rule_based_patterns:
            matches = re.findall(pattern, text_lower)
            rule_skills.extend(matches)
        logger.debug(f"Rule-based extracted skills: {rule_skills}")
        return list(set(rule_skills)) # Remove duplicates

    def _normalize_and_expand_skills(self, skills: List[str]) -> List[str]:
        """
        Normalizes and expands extracted skills using the Neo4j knowledge graph.
        
        Args:
            skills: A list of raw extracted skill strings.
            
        Returns:
            A list of normalized and potentially expanded skill strings.
        """
        normalized_skills = set()
        with self.neo4j_driver.session() as session:
            for skill in skills:
                # Try to find exact match or similar skill in KG
                query = """
                MATCH (s:Skill)
                WHERE toLower(s.name) = toLower($skill_name) OR toLower($skill_name) CONTAINS toLower(s.name)
                RETURN s.name AS normalized_skill
                LIMIT 1
                """
                result = session.run(query, skill_name=skill).single()
                if result:
                    normalized_skills.add(result["normalized_skill"])
                else:
                    # If no direct match, add the original skill (or a cleaned version)
                    normalized_skills.add(skill.lower().strip())
                    
                # Optionally, expand with broader/narrower skills from KG
                # This can be added later based on specific requirements
                # For example:
                # query_expansion = """
                # MATCH (s:Skill)-[:IS_BROADER_THAN|IS_NARROWER_THAN*0..1]-(related:Skill)
                # WHERE toLower(s.name) = toLower($skill_name)
                # RETURN related.name AS expanded_skill
                # """
                # results_expansion = session.run(query_expansion, skill_name=skill)
                # for record in results_expansion:
                #     normalized_skills.add(record["expanded_skill"])
        
        logger.debug(f"Normalized and expanded skills: {list(normalized_skills)}")
        return list(normalized_skills)

    def extract_skills(self, text: str) -> List[str]:
        """
        Executes the multi-layered skill extraction pipeline.
        
        Args:
            text: The input text (e.g., resume or job description).
            
        Returns:
            A list of unique, normalized skills extracted from the text.
        """
        logger.info("Starting multi-layered skill extraction...")
        
        # Layer 1: Custom NER Model
        ner_extracted = self._extract_with_ner(text)
        
        # Layer 2: Rule-based Extraction
        rule_extracted = self._extract_with_rules(text)
        
        # Combine skills from both layers
        all_extracted_skills = list(set(ner_extracted + rule_extracted))
        logger.info(f"Combined raw extracted skills: {all_extracted_skills}")
        
        # Layer 3: Knowledge Graph Integration (Normalization and Expansion)
        final_skills = self._normalize_and_expand_skills(all_extracted_skills)
        
        logger.info(f"Final extracted and normalized skills: {final_skills}")
        return final_skills

def main():
    """Main execution function for testing the skill extractor."""
    print("=" * 60)
    print("RESUME SKILL GAP ANALYZER - SKILL EXTRACTION PIPELINE")
    print("=" * 60)
    
    # Example usage
    sample_text_resume = """
    Experienced Software Engineer with a strong background in Python, Java, and Machine Learning.
    Proficient in developing RESTful APIs with Flask and Django. Skilled in SQL and PostgreSQL
    for database management. Familiar with AWS cloud services and Docker for deployment.
    Completed a Deep Learning specialization on Coursera. Agile methodology experience.
    """
    
    sample_text_job_desc = """
    We are looking for a Data Scientist with expertise in Python, R, and statistical modeling.
    Experience with big data technologies like Spark and Hadoop is a plus.
    Knowledge of SQL and data visualization tools (e.g., Tableau) is required.
    Familiarity with Machine Learning algorithms and cloud platforms (Azure, GCP) is essential.
    """
    
    extractor = None
    try:
        extractor = SkillExtractor()
        
        print("\n--- Extracting skills from sample resume ---")
        resume_skills = extractor.extract_skills(sample_text_resume)
        print(f"\nExtracted skills from resume: {resume_skills}")
        
        print("\n--- Extracting skills from sample job description ---")
        job_desc_skills = extractor.extract_skills(sample_text_job_desc)
        print(f"\nExtracted skills from job description: {job_desc_skills}")
        
        print("\n" + "=" * 60)
        print("SKILL EXTRACTION PIPELINE TEST COMPLETED.")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"Skill extraction pipeline failed: {e}")
        print(f"\n❌ Error: {e}")
        print("\nPlease ensure:")
        print("1. The custom NER model is trained and saved at 'models/ner_model/model-best'.")
        print("2. Neo4j database is running and accessible with correct credentials.")
        print("3. All necessary Python packages are installed (check scripts/skill_extractor_requirements.txt).")
    finally:
        if extractor:
            extractor.close_neo4j_connection()

if __name__ == "__main__":
    main()
