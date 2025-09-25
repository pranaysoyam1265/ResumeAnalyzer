import logging
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Any, Optional
from pathlib import Path
import json
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from neo4j import GraphDatabase
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import re
from scripts.spacy_preprocessing import SpacyPreprocessor  # Import SpacyPreprocessor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RecommenderEngine:
    """
    Resume Skill Gap Analyzer and Course Recommender
    
    This class integrates the custom NER model with the Knowledge Graph to provide
    skill gap analysis and course recommendations for career development.
    """
    
    def __init__(self, 
                 neo4j_uri: str = "bolt://localhost:7687",
                 neo4j_user: str = "neo4j", 
                 neo4j_password: str = "password",
                 ner_model_path: str = "./ner_skill_extractor",
                 embedding_model: str = "all-MiniLM-L6-v2",
                 similarity_threshold: float = 0.8,
                 spacy_model_name: str = "en_core_web_sm"):  # Added spacy_model_name parameter
        """
        Initialize the Recommender Engine
        
        Args:
            neo4j_uri: Neo4j database URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
            ner_model_path: Path to the fine-tuned NER model
            embedding_model: Sentence transformer model for embeddings
            similarity_threshold: Minimum similarity score for entity linking
            spacy_model_name: Name of the spaCy model to use for preprocessing
        """
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        self.ner_model_path = ner_model_path
        self.similarity_threshold = similarity_threshold
        self.spacy_model_name = spacy_model_name  # Stored spacy_model_name
        
        # Initialize components
        self.driver = None
        self.ner_pipeline = None
        self.embedding_model = None
        self.kg_skill_embeddings = None
        self.kg_skills_cache = None
        self.spacy_preprocessor = None  # Added spacy_preprocessor attribute
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all components (Neo4j, NER model, embedding model, spaCy preprocessor)"""  # Updated docstring
        try:
            # Initialize Neo4j connection
            self.driver = GraphDatabase.driver(
                self.neo4j_uri, 
                auth=(self.neo4j_user, self.neo4j_password)
            )
            logger.info("Connected to Neo4j database")
            
            # Initialize NER model
            self._load_ner_model()
            
            # Initialize embedding model
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Loaded sentence transformer model")
            
            # Cache KG skills and their embeddings
            self._cache_kg_skills()
            
            # Initialize spaCy preprocessor  # Initialized SpacyPreprocessor
            self.spacy_preprocessor = SpacyPreprocessor(model_name=self.spacy_model_name)
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            raise
    
    def _load_ner_model(self):
        """Load the fine-tuned NER model"""
        try:
            if Path(self.ner_model_path).exists():
                # Load the fine-tuned model
                self.ner_pipeline = pipeline(
                    "ner",
                    model=self.ner_model_path,
                    tokenizer=self.ner_model_path,
                    aggregation_strategy="simple"
                )
                logger.info(f"Loaded fine-tuned NER model from {self.ner_model_path}")
            else:
                # Fallback to a general NER model
                logger.warning(f"Fine-tuned model not found at {self.ner_model_path}")
                logger.info("Using fallback NER model: dbmdz/bert-large-cased-finetuned-conll03-english")
                self.ner_pipeline = pipeline(
                    "ner",
                    model="dbmdz/bert-large-cased-finetuned-conll03-english",
                    aggregation_strategy="simple"
                )
        except Exception as e:
            logger.error(f"Error loading NER model: {e}")
            # Create a mock pipeline for testing
            self.ner_pipeline = self._create_mock_ner_pipeline()
    
    def _create_mock_ner_pipeline(self):
        """Create a mock NER pipeline for testing when model is not available"""
        def mock_pipeline(text):
            # Simple keyword-based skill extraction for testing
            common_skills = [
                'python', 'java', 'javascript', 'sql', 'machine learning',
                'data analysis', 'deep learning', 'tensorflow', 'pytorch',
                'pandas', 'numpy', 'scikit-learn', 'git', 'docker',
                'kubernetes', 'aws', 'azure', 'react', 'node.js'
            ]
            
            entities = []
            text_lower = text.lower()
            
            for skill in common_skills:
                if skill in text_lower:
                    start_idx = text_lower.find(skill)
                    entities.append({
                        'entity_group': 'SKILL',
                        'score': 0.9,
                        'word': skill.title(),
                        'start': start_idx,
                        'end': start_idx + len(skill)
                    })
            
            return entities
        
        logger.info("Created mock NER pipeline for testing")
        return mock_pipeline
    
    def _cache_kg_skills(self):
        """Cache all skills from the knowledge graph with their embeddings, including synonyms.""" # Updated docstring
        try:
            with self.driver.session() as session:
                # Fetch all skills from the KG, including any 'synonym' properties
                result = session.run("""
                    MATCH (s:Skill)
                    OPTIONAL MATCH (s)-[:HAS_SYNONYM]->(syn:SkillSynonym)
                    RETURN s.uri as uri, s.name as name, s.description as description, 
                           COLLECT(syn.name) as synonyms
                """)
                
                skills_data = []
                for record in result:
                    skills_data.append({
                        'uri': record['uri'],
                        'name': record['name'] or '',
                        'description': record['description'] or '',
                        'synonyms': record['synonyms'] or [] # Added synonyms to cached data
                    })
                
                if not skills_data:
                    logger.warning("No skills found in knowledge graph, creating sample skills")
                    self._create_sample_skills()
                    return self._cache_kg_skills()
                
                # Create embeddings for all skills and their synonyms
                skill_texts = []
                for skill in skills_data:
                    # Combine name, description, and synonyms for better embeddings
                    text = f"{skill['name']} {skill['description']}"
                    if skill['synonyms']:
                        text += " " + " ".join(skill['synonyms']) # Added synonyms to text for embedding
                    skill_texts.append(text.strip())
                
                # Generate embeddings
                embeddings = self.embedding_model.encode(skill_texts)
                
                # Cache the results
                self.kg_skills_cache = skills_data
                self.kg_skill_embeddings = embeddings
                
                logger.info(f"Cached {len(skills_data)} skills with embeddings")
                
        except Exception as e:
            logger.error(f"Error caching KG skills: {e}")
            # Create fallback cache
            self._create_fallback_skills_cache()
    
    def _create_sample_skills(self):
        """Create sample skills in the knowledge graph for testing"""
        sample_skills = [
            {'name': 'Python', 'description': 'Programming language for data science and web development', 'synonyms': ['Python3', 'Py']}, # Added synonyms
            {'name': 'Machine Learning', 'description': 'Algorithms and techniques for predictive modeling', 'synonyms': ['ML', 'AI/ML']}, # Added synonyms
            {'name': 'Data Analysis', 'description': 'Analyzing and interpreting complex datasets', 'synonyms': ['Data Analytics']}, # Added synonyms
            {'name': 'SQL', 'description': 'Database query language for data manipulation', 'synonyms': ['Structured Query Language']}, # Added synonyms
            {'name': 'Deep Learning', 'description': 'Neural networks and artificial intelligence', 'synonyms': ['DL']}, # Added synonyms
            {'name': 'JavaScript', 'description': 'Programming language for web development', 'synonyms': ['JS', 'ECMAScript']}, # Added synonyms
            {'name': 'React', 'description': 'JavaScript library for building user interfaces', 'synonyms': ['React.js', 'ReactJS']}, # Added synonyms
            {'name': 'Docker', 'description': 'Containerization platform for application deployment'},
            {'name': 'AWS', 'description': 'Amazon Web Services cloud computing platform'},
            {'name': 'Git', 'description': 'Version control system for code management'}
        ]
        
        with self.driver.session() as session:
            for i, skill in enumerate(sample_skills):
                session.run("""
                    MERGE (s:Skill {uri: $uri})
                    SET s.name = $name, s.description = $description
                """, {
                    'uri': f"skill_{i}",
                    'name': skill['name'],
                    'description': skill['description']
                })
                if 'synonyms' in skill and skill['synonyms']:
                    for synonym in skill['synonyms']:
                        session.run("""
                            MATCH (s:Skill {uri: $uri})
                            MERGE (syn:SkillSynonym {name: $synonym_name})
                            MERGE (s)-[:HAS_SYNONYM]->(syn)
                        """, {
                            'uri': f"skill_{i}",
                            'synonym_name': synonym
                        })
        
        logger.info("Created sample skills in knowledge graph")
    
    def _create_fallback_skills_cache(self):
        """Create fallback skills cache when KG is not available"""
        fallback_skills = [
            {'uri': 'skill_0', 'name': 'Python', 'description': 'Programming language', 'synonyms': ['Python3', 'Py']}, # Added synonyms
            {'uri': 'skill_1', 'name': 'Machine Learning', 'description': 'AI and ML techniques', 'synonyms': ['ML', 'AI/ML']}, # Added synonyms
            {'uri': 'skill_2', 'name': 'Data Analysis', 'description': 'Data interpretation', 'synonyms': ['Data Analytics']}, # Added synonyms
            {'uri': 'skill_3', 'name': 'SQL', 'description': 'Database queries', 'synonyms': ['Structured Query Language']}, # Added synonyms
            {'uri': 'skill_4', 'name': 'JavaScript', 'description': 'Web programming', 'synonyms': ['JS', 'ECMAScript']} # Added synonyms
        ]
        
        skill_texts = []
        for s in fallback_skills:
            text = f"{s['name']} {s['description']}"
            if s['synonyms']:
                text += " " + " ".join(s['synonyms']) # Added synonyms to text for embedding
            skill_texts.append(text.strip())

        embeddings = self.embedding_model.encode(skill_texts)
        
        self.kg_skills_cache = fallback_skills
        self.kg_skill_embeddings = embeddings
        
        logger.info("Created fallback skills cache")

    def _detect_proficiency_level(self, skill_text: str, original_context: List[str], doc: Any) -> str: # New helper method
        """
        Detects the proficiency level of a skill based on contextual clues.
        
        Args:
            skill_text: The extracted skill string.
            original_context: A list of context snippets where the skill was found.
            doc: The spaCy Doc object for the entire resume text.
            
        Returns:
            str: The detected proficiency level (e.g., "Beginner", "Intermediate", "Advanced", "Expert").
        """
        context_lower = " ".join(original_context).lower()
        
        # Keywords for different proficiency levels
        expert_keywords = ["expert in", "mastery of", "deep expertise", "pioneered", "led development", "architected", "senior", "principal"]
        advanced_keywords = ["proficient in", "strong command of", "extensive experience", "developed advanced", "implemented complex", "lead", "managed"]
        intermediate_keywords = ["experience with", "familiar with", "worked with", "used", "applied", "contributed to"]
        beginner_keywords = ["basic knowledge of", "exposure to", "learning", "studied", "introductory"]

        # Check for years of experience
        years_of_experience_match = re.search(r'(\d+)\+?\s*(year|yr)s?\s*of\s*experience', context_lower)
        if years_of_experience_match:
            years = int(years_of_experience_match.group(1))
            if years >= 5:
                return "Expert"
            elif years >= 3:
                return "Advanced"
            elif years >= 1:
                return "Intermediate"

        # Check for specific keywords
        for keyword in expert_keywords:
            if keyword in context_lower:
                return "Expert"
        for keyword in advanced_keywords:
            if keyword in context_lower:
                return "Advanced"
        for keyword in intermediate_keywords:
            if keyword in context_lower:
                return "Intermediate"
        for keyword in beginner_keywords:
            if keyword in context_lower:
                return "Beginner"
        
        # Fallback to a default if no specific indicators are found
        return "Intermediate"
    
    def extract_skills_from_resume(self, resume_text: str) -> Tuple[List[Dict], Dict[str, Any]]: # Changed return type to include processed_data
        """
        Extract skills from resume text using the fine-tuned NER model and spaCy for context.
        
        Args:
            resume_text: Raw resume text
            
        Returns:
            Tuple[List[Dict], Dict[str, Any]]: A tuple containing:
                - List of dictionaries with extracted skill information (skill, confidence, original_context, proficiency_level)
                - Dictionary with spaCy processed data (tokens, lemmas, pos_tags, dependencies, doc)
        """
        try:
            extracted_skill_data = [] # New list to store dictionaries of skill data

            # Preprocess text with spaCy
            processed_data = None
            if self.spacy_preprocessor:
                processed_data = self.spacy_preprocessor.preprocess_text(resume_text)
                logger.debug("Text preprocessed with spaCy.")
            else:
                logger.warning("spaCy preprocessor not initialized. Proceeding without spaCy preprocessing.")

            # Run NER inference
            entities = self.ner_pipeline(resume_text)
            
            # Extract skill entities and apply context-aware filtering
            for entity in entities:
                if entity.get('entity_group') in ['SKILL', 'B-SKILL', 'I-SKILL'] or \
                   entity.get('entity') in ['B-SKILL', 'I-SKILL']:
                    skill_text = entity['word'].strip()
                    # Clean up the skill text
                    skill_text = re.sub(r'^##', '', skill_text)  # Remove BERT subword markers
                    skill_text = skill_text.replace(' ##', '')   # Remove internal markers
                    
                    if len(skill_text) > 2:
                        is_valid_skill = True
                        if processed_data and processed_data['doc']:
                            # Find the span in the spaCy doc corresponding to the extracted skill
                            # This is a simplified approach; a more robust solution would map char offsets
                            for token in processed_data['doc']:
                                if skill_text.lower() in token.text.lower() and \
                                   token.pos_ not in ["NOUN", "PROPN", "ADJ"]: # Skills are typically nouns, proper nouns, or adjectives
                                    # Example: "managing" might be a verb, but "project management" is a skill
                                    # This simple check helps filter out some false positives
                                    is_valid_skill = False
                                    break
                        
                        if is_valid_skill:
                            confidence = entity.get('score', 0.5) * 100 # Convert to percentage
                            
                            # Extract original context snippet
                            original_context = []
                            if entity.get('start') is not None and entity.get('end') is not None:
                                start_char = max(0, entity['start'] - 50) # 50 chars before
                                end_char = min(len(resume_text), entity['end'] + 50) # 50 chars after
                                context_snippet = resume_text[start_char:end_char].strip()
                                original_context.append(context_snippet)

                            proficiency_level = self._detect_proficiency_level(
                                skill_text, original_context, processed_data['doc'] if processed_data else None
                            )

                            extracted_skill_data.append({
                                'name': skill_text,
                                'confidence': confidence,
                                'original_context': original_context,
                                'proficiency_level': proficiency_level # Add proficiency level
                            })
            
            unique_skills_map = {}
            for skill_data in extracted_skill_data:
                skill_name_lower = skill_data['name'].lower()
                if skill_name_lower not in unique_skills_map or \
                   skill_data['confidence'] > unique_skills_map[skill_name_lower]['confidence']:
                    unique_skills_map[skill_name_lower] = skill_data
            
            unique_skills = list(unique_skills_map.values())

            logger.info(f"Extracted {len(unique_skills)} unique skills from resume with confidence and context")
            return unique_skills, processed_data # Return processed_data
            
        except Exception as e:
            logger.error(f"Error extracting skills from resume: {e}")
            return [], {}
    
    def link_entities_to_kg(self, skill_data_list: List[Dict], processed_data: Dict[str, Any]) -> List[Dict]: # Added processed_data parameter
        """
        Link extracted skill strings to Knowledge Graph entities using semantic similarity and spaCy lemmas for normalization. # Updated docstring
        
        Args:
            skill_data_list: List of dictionaries with extracted skill information
            processed_data: Dictionary with spaCy processed data (tokens, lemmas, pos_tags, dependencies, doc)
            
        Returns:
            List of dictionaries with linked skill information
        """
        try:
            if not skill_data_list:
                return []
            
            normalized_input_skills = []
            for skill_data in skill_data_list:
                skill_name = skill_data['name']
                if processed_data and processed_data['doc']:
                    # Find the lemma for the skill name in the spaCy doc
                    # This is a simplified approach, a more robust solution would map char offsets
                    lemma_found = False
                    for token in processed_data['doc']:
                        if skill_name.lower() == token.text.lower():
                            normalized_input_skills.append(token.lemma_)
                            lemma_found = True
                            break
                    if not lemma_found:
                        normalized_input_skills.append(skill_name) # Fallback to original if lemma not found
                else:
                    normalized_input_skills.append(skill_name)
            
            # Generate embeddings for normalized input skills
            input_embeddings = self.embedding_model.encode(normalized_input_skills) # Use normalized_input_skills
            
            # Calculate similarities with KG skills
            similarities = cosine_similarity(input_embeddings, self.kg_skill_embeddings)
            
            linked_skills = []
            for i, skill_data in enumerate(skill_data_list):
                skill_string = skill_data['name']
                # Find best matching KG skill
                best_match_idx = np.argmax(similarities[i])
                best_similarity = similarities[i][best_match_idx]
                
                if best_similarity >= self.similarity_threshold:
                    kg_skill = self.kg_skills_cache[best_match_idx]
                    linked_skills.append({
                        'input_skill': skill_string,
                        'kg_skill_uri': kg_skill['uri'],
                        'kg_skill_name': kg_skill['name'],
                        'similarity_score': float(best_similarity),
                        'confidence': skill_data['confidence'],
                        'original_context': skill_data['original_context'],
                        'normalized_skill': normalized_input_skills[i], # Add normalized skill
                        'synonyms': kg_skill.get('synonyms', []), # Add synonyms from KG
                        'proficiency_level': skill_data['proficiency_level'] # Add proficiency level
                    })
                    logger.debug(f"Linked '{skill_string}' to '{kg_skill['name']}' (score: {best_similarity:.3f})")
                else:
                    logger.debug(f"No good match found for '{skill_string}' (best score: {best_similarity:.3f})\n")
            
            logger.info(f"Successfully linked {len(linked_skills)} out of {len(skill_data_list)} skills")
            return linked_skills
            
        except Exception as e:
            logger.error(f"Error linking entities to KG: {e}")
            return []
    
    def get_recommendations(self, user_skills: List[Dict], target_job_role: str) -> Dict:
        """
        Generate skill gap analysis and course recommendations, incorporating weighted skill importance and proficiency. # Updated docstring
        
        Args:
            user_skills: List of linked skill dictionaries
            target_job_role: Target job role name
            
        Returns:
            Dictionary with skill gaps and course recommendations
        """
        try:
            proficiency_map = {
                "Beginner": 1,
                "Intermediate": 2,
                "Advanced": 3,
                "Expert": 4
            }
            default_required_proficiency_level = "Advanced"
            default_required_proficiency_score = proficiency_map[default_required_proficiency_level]

            with self.driver.session() as session:
                # Find the target job role
                job_result = session.run("""
                    MATCH (j:JobRole)
                    WHERE toLower(j.title) CONTAINS toLower($job_title)
                       OR toLower(j.title) = toLower($job_title)
                    RETURN j.id as job_id, j.title as job_title
                    LIMIT 1
                """, {'job_title': target_job_role})
                
                job_record = job_result.single()
                if not job_record:
                    logger.warning(f"Job role '{target_job_role}' not found in KG")
                    return self._create_fallback_recommendations(user_skills, target_job_role)
                
                job_id = job_record['job_id']
                job_title = job_record['job_title']
                
                # Get required skills for the job
                required_skills_result = session.run("""
                    MATCH (j:JobRole {id: $job_id})-[r:REQUIRES]->(s:Skill)
                    RETURN s.uri as skill_uri, s.name as skill_name, 
                           s.description as skill_description, r.importance as importance
                    ORDER BY r.importance DESC
                """, {'job_id': job_id})
                
                required_skills = []
                for record in required_skills_result:
                    required_skills.append({
                        'uri': record['skill_uri'],
                        'name': record['skill_name'],
                        'description': record['skill_description'],
                        'importance': record['importance'] or 0.5, # Default importance
                        'required_proficiency': default_required_proficiency_level # Add default required proficiency
                    })
                
                total_required_importance = sum(skill['importance'] for skill in required_skills)
                total_matched_importance = 0
                missing_skills_list = []
                proficiency_gaps_list = []
                
                user_skill_map = {skill['kg_skill_uri']: skill for skill in user_skills}

                for required_skill in required_skills:
                    if required_skill['uri'] in user_skill_map:
                        user_skill = user_skill_map[required_skill['uri']]
                        user_proficiency_score = proficiency_map.get(user_skill['proficiency_level'], 1)
                        required_proficiency_score = proficiency_map.get(required_skill['required_proficiency'], default_required_proficiency_score)

                        if user_proficiency_score >= required_proficiency_score:
                            total_matched_importance += required_skill['importance']
                        else:
                            proficiency_gaps_list.append({
                                'skill_info': required_skill,
                                'user_proficiency': user_skill['proficiency_level'],
                                'required_proficiency': required_skill['required_proficiency'],
                                'gap_type': 'Proficiency Gap'
                            })
                            total_matched_importance += required_skill['importance'] * (user_proficiency_score / required_proficiency_score)
                    else:
                        missing_skills_list.append({
                            'skill_info': required_skill,
                            'gap_type': 'Missing Skill'
                        })
                
                weighted_skill_gap_count = len(missing_skills_list) + len(proficiency_gaps_list)
                weighted_skill_match_percentage = (total_matched_importance / total_required_importance) * 100 if total_required_importance > 0 else 0

                # Get course recommendations for missing and proficiency-gapped skills
                recommendations = {}
                for gap_item in missing_skills_list + proficiency_gaps_list:
                    missing_skill = gap_item['skill_info']
                    courses_result = session.run("""
                        MATCH (c:Course)-[r:TEACHES]->(s:Skill {uri: $skill_uri})
                        RETURN c.id as course_id, c.title as course_title,
                               c.description as course_description, c.platform as platform,
                               c.url as url, c.rating as rating, c.duration as duration
                        ORDER BY c.rating DESC
                        LIMIT 5
                    """, {'skill_uri': missing_skill['uri']})
                    
                    courses = []
                    for course_record in courses_result:
                        courses.append({
                            'id': course_record['course_id'],
                            'title': course_record['course_title'],
                            'description': course_record['course_description'],
                            'platform': course_record['platform'],
                            'url': course_record['url'],
                            'rating': course_record['rating'],
                            'duration': course_record['duration']
                        })
                    
                    recommendations[missing_skill['name']] = {
                        'skill_info': missing_skill,
                        'courses': courses,
                        'gap_type': gap_item['gap_type'] # Add gap type to recommendations
                    }
                
                return {
                    'target_job': {
                        'id': job_id,
                        'title': job_title
                    },
                    'user_skills': user_skills,
                    'required_skills': required_skills,
                    'missing_skills': missing_skills_list, # Updated to missing_skills_list
                    'proficiency_gaps': proficiency_gaps_list, # Added proficiency gaps
                    'skill_gap_count': weighted_skill_gap_count, # Use weighted count
                    'skill_match_percentage': weighted_skill_match_percentage, # Use weighted percentage
                    'recommendations': recommendations
                }
                
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return self._create_fallback_recommendations(user_skills, target_job_role)
    
    def _create_fallback_recommendations(self, user_skills: List[Dict], target_job_role: str) -> Dict:
        """Create fallback recommendations when KG query fails"""
        # Sample missing skills based on common job requirements
        common_job_skills = {
            'data scientist': ['Python', 'Machine Learning', 'SQL', 'Statistics', 'Data Visualization'],
            'software engineer': ['Python', 'JavaScript', 'Git', 'Algorithms', 'System Design'],
            'machine learning engineer': ['Python', 'Machine Learning', 'Deep Learning', 'MLOps', 'Docker']
        }
        
        job_lower = target_job_role.lower()
        required_skills = []
        for job_type, skills in common_job_skills.items():
            if job_type in job_lower:
                required_skills = skills
                break
        
        if not required_skills:
            required_skills = ['Python', 'Machine Learning', 'Data Analysis']
        
        user_skill_names = {skill['kg_skill_name'].lower() for skill in user_skills}
        missing_skills = [skill for skill in required_skills if skill.lower() not in user_skill_names]
        
        recommendations = {}
        for skill in missing_skills:
            recommendations[skill] = {
                'skill_info': {'name': skill, 'description': f'Important skill for {target_job_role}'},
                'courses': [{
                    'title': f'Learn {skill}',
                    'description': f'Comprehensive course on {skill}',
                    'platform': 'Online Learning',
                    'rating': 4.5
                }],
                'gap_type': 'Missing Skill' # Add gap type to fallback
            }
        
        return {
            'target_job': {'title': target_job_role},
            'user_skills': user_skills,
            'missing_skills': [{'skill_info': {'name': s}, 'gap_type': 'Missing Skill'} for s in missing_skills], # Format for consistency
            'proficiency_gaps': [], # Add empty proficiency gaps
            'skill_gap_count': len(missing_skills),
            'recommendations': recommendations
        }
    
    def format_recommendations(self, recommendations: Dict) -> str:
        """Format recommendations for user-friendly display"""
        output = []
        output.append("=" * 60)
        output.append("RESUME SKILL GAP ANALYSIS & RECOMMENDATIONS")
        output.append("=" * 60)
        
        # Job information
        target_job = recommendations.get('target_job', {})
        output.append(f"\nTarget Job Role: {target_job.get('title', 'Unknown')}")
        
        # User skills
        user_skills = recommendations.get('user_skills', [])
        output.append(f"\nYour Current Skills ({len(user_skills)}):\n")
        for skill in user_skills:
            output.append(f"  ✓ {skill['kg_skill_name']} (confidence: {skill['confidence']:.2f}%, proficiency: {skill['proficiency_level']})") # Display proficiency level
            if skill.get('normalized_skill') and skill['normalized_skill'].lower() != skill['input_skill'].lower(): # Display normalized skill if different
                output.append(f"    (Normalized: {skill['normalized_skill']})")
            if skill.get('synonyms'): # Display synonyms
                output.append(f"    (Synonyms: {', '.join(skill['synonyms'])})")
            if skill.get('original_context'): # Display original context
                output.append(f"    (Context: \"{skill['original_context'][0][:70]}...\")") # Show first 70 chars of first context snippet
        
        # Skill gap analysis
        skill_gap_count = recommendations.get('skill_gap_count', 0)
        skill_match_percentage = recommendations.get('skill_match_percentage', 0)
        
        output.append(f"\nSkill Gap Analysis:")
        output.append(f"  • Total Gaps (Weighted): {skill_gap_count}") # Updated label
        output.append(f"  • Skills Match (Weighted): {skill_match_percentage:.1f}%") # Updated label
        
        missing_skills_list = recommendations.get('missing_skills', [])
        proficiency_gaps_list = recommendations.get('proficiency_gaps', [])

        if missing_skills_list:
            output.append("\nCritical Gaps (Missing Skills):")
            for gap in missing_skills_list:
                output.append(f"  - {gap['skill_info']['name']} (Importance: {gap['skill_info']['importance']:.1f})")
        
        if proficiency_gaps_list:
            output.append("\nDevelopment Areas (Proficiency Gaps):")
            for gap in proficiency_gaps_list:
                output.append(f"  - {gap['skill_info']['name']} (Your Proficiency: {gap['user_proficiency']}, Required: {gap['required_proficiency']}, Importance: {gap['skill_info']['importance']:.1f})")

        # Recommendations
        recs = recommendations.get('recommendations', {})
        if recs:
            output.append(f"\nRecommended Courses to Bridge Skill Gaps:")
            output.append("-" * 50)
            
            for skill_name, skill_data in recs.items():
                output.append(f"\n📚 {skill_data.get('gap_type', 'Missing Skill')}: {skill_name}") # Display gap type
                courses = skill_data.get('courses', [])
                
                if courses:
                    output.append("   Recommended Courses:")
                    for i, course in enumerate(courses[:3], 1):  # Show top 3 courses
                        rating = course.get('rating', 'N/A')
                        platform = course.get('platform', 'Unknown')
                        output.append(f"   {i}. {course.get('title', 'Untitled Course')}")
                        output.append(f"      Platform: {platform} | Rating: {rating}")
                        if course.get('description'):
                            output.append(f"      Description: {course['description'][:100]}...")
                else:
                    output.append("   No specific courses found. Consider searching online learning platforms.")
        else:
            output.append("\n🎉 Congratulations! You have all the required skills for this role!")
        
        output.append("\n" + "=" * 60)
        return "\n".join(output)
    
    def close(self):
        """Close database connection"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")

def main():
    """Main application flow demonstrating the end-to-end process"""
    logger.info("Starting Resume Skill Gap Analyzer...")
    
    # Sample resume text for testing
    sample_resume = """
    John Doe
    Data Analyst
    
    Experience:
    - 3 years of experience in data analysis using Python and SQL
    - Proficient in pandas, numpy, and matplotlib for data manipulation and visualization
    - Experience with machine learning algorithms using scikit-learn
    - Worked with databases including MySQL and PostgreSQL
    - Created dashboards using Tableau and Power BI
    
    Skills:
    - Programming: Python, SQL, R
    - Data Analysis: pandas, numpy, matplotlib, seaborn
    - Machine Learning: scikit-learn, basic neural networks
    - Databases: MySQL, PostgreSQL
    - Visualization: Tableau, Power BI, matplotlib
    - Tools: Git, Jupyter Notebooks, Excel
    
    Education:
    - Bachelor's in Computer Science
    - Coursera Machine Learning Certificate
    """
    
    # Target job role
    target_job = "Data Scientist"
    
    # Initialize the recommender engine
    try:
        recommender = RecommenderEngine()
        
        # Step 1: Extract skills from resume
        logger.info("Step 1: Extracting skills from resume...")
        extracted_skills, processed_data = recommender.extract_skills_from_resume(sample_resume) # Capture processed_data
        logger.info(f"Extracted skills: {extracted_skills}")
        
        # Step 2: Link entities to knowledge graph
        logger.info("Step 2: Linking skills to knowledge graph...")
        linked_skills = recommender.link_entities_to_kg(extracted_skills, processed_data) # Pass processed_data
        logger.info(f"Successfully linked {len(linked_skills)} skills")
        
        # Step 3: Generate recommendations
        logger.info("Step 3: Generating skill gap analysis and recommendations...")
        recommendations = recommender.get_recommendations(linked_skills, target_job)
        
        # Step 4: Display results
        logger.info("Step 4: Displaying results...")
        formatted_output = recommender.format_recommendations(recommendations)
        print(formatted_output)
        
        # Save results to file
        output_file = "skill_gap_analysis.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(formatted_output)
        logger.info(f"Results saved to {output_file}")
        
    except Exception as e:
        logger.error(f"Error in main application flow: {e}")
        raise
    finally:
        if 'recommender' in locals():
            recommender.close()

if __name__ == "__main__":
    main()
