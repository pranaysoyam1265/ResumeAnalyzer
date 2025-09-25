import spacy
import json
import re
import logging
from typing import List, Dict, Any, Tuple, Optional, Set
from pathlib import Path
from collections import defaultdict, Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkillTaxonomy:
    """Manage skill taxonomy and synonyms"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.taxonomy = self.load_skill_taxonomy()
        self.synonyms = self.load_skill_synonyms()
        self.all_skills = self._build_skill_index()
    
    def load_skill_taxonomy(self) -> Dict[str, Any]:
        """Load comprehensive skill taxonomy"""
        taxonomy_path = self.config.get_skill_taxonomy_path()
        
        if taxonomy_path.exists():
            with open(taxonomy_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Create comprehensive default taxonomy
        default_taxonomy = {
            "technical_skills": {
                "programming": [
                    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "C", "Ruby", 
                    "Go", "Rust", "Swift", "Kotlin", "PHP", "R", "Scala", "Perl", "Dart",
                    "Shell", "Bash", "PowerShell", "VBA", "MATLAB", "SAS", "Julia"
                ],
                "web_development": [
                    "HTML", "CSS", "SCSS", "SASS", "Less", "React", "Angular", "Vue.js", 
                    "Svelte", "Node.js", "Express.js", "Next.js", "Nuxt.js", "Django", 
                    "Flask", "FastAPI", "Spring Boot", "Laravel", "Ruby on Rails", "ASP.NET",
                    "jQuery", "Bootstrap", "Tailwind CSS", "Material-UI", "Chakra UI"
                ],
                "mobile_development": [
                    "React Native", "Flutter", "Ionic", "Xamarin", "Cordova", "PhoneGap",
                    "iOS Development", "Android Development", "Swift", "Objective-C", "Kotlin"
                ],
                "databases": [
                    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "Oracle", 
                    "SQL Server", "SQLite", "Cassandra", "DynamoDB", "Neo4j", "CouchDB",
                    "InfluxDB", "MariaDB", "Firebase", "Supabase", "PlanetScale"
                ],
                "cloud_platforms": [
                    "AWS", "Microsoft Azure", "Google Cloud Platform", "IBM Cloud", 
                    "Oracle Cloud", "DigitalOcean", "Linode", "Vultr", "Heroku", "Vercel",
                    "Netlify", "Railway", "Render"
                ],
                "devops_tools": [
                    "Docker", "Kubernetes", "Terraform", "Ansible", "Puppet", "Chef",
                    "Jenkins", "GitLab CI", "GitHub Actions", "CircleCI", "Travis CI",
                    "Azure DevOps", "Bamboo", "TeamCity"
                ],
                "data_science": [
                    "Machine Learning", "Deep Learning", "Data Analysis", "Data Mining",
                    "Statistics", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch",
                    "Keras", "XGBoost", "LightGBM", "NLTK", "spaCy", "OpenCV", "Matplotlib",
                    "Seaborn", "Plotly", "Jupyter", "Apache Spark", "Hadoop", "Kafka"
                ],
                "tools_ides": [
                    "Git", "GitHub", "GitLab", "Bitbucket", "SVN", "Visual Studio Code",
                    "IntelliJ IDEA", "Eclipse", "Sublime Text", "Atom", "Vim", "Emacs",
                    "PyCharm", "WebStorm", "Android Studio", "Xcode"
                ],
                "testing": [
                    "Unit Testing", "Integration Testing", "End-to-End Testing", "Jest",
                    "Mocha", "Chai", "Cypress", "Selenium", "TestNG", "JUnit", "pytest",
                    "Postman", "Insomnia", "SoapUI"
                ]
            },
            "soft_skills": {
                "communication": [
                    "Communication", "Public Speaking", "Presentation", "Writing", 
                    "Documentation", "Technical Writing", "Verbal Communication",
                    "Cross-cultural Communication", "Client Communication"
                ],
                "leadership": [
                    "Leadership", "Team Management", "Project Management", "People Management",
                    "Mentoring", "Coaching", "Decision Making", "Delegation", "Conflict Resolution",
                    "Change Management", "Strategic Planning"
                ],
                "analytical": [
                    "Problem Solving", "Critical Thinking", "Analytical Thinking", 
                    "Data Analysis", "Research", "Attention to Detail", "Pattern Recognition",
                    "Root Cause Analysis", "Systems Thinking"
                ],
                "collaboration": [
                    "Teamwork", "Collaboration", "Cross-functional Collaboration",
                    "Stakeholder Management", "Customer Service", "Negotiation",
                    "Interpersonal Skills", "Networking"
                ],
                "adaptability": [
                    "Adaptability", "Flexibility", "Learning Agility", "Innovation",
                    "Creativity", "Open-mindedness", "Resilience", "Stress Management"
                ]
            },
            "certifications": {
                "cloud": [
                    "AWS Certified Solutions Architect", "AWS Certified Developer", 
                    "Azure Fundamentals", "Azure Solutions Architect", "Google Cloud Professional",
                    "Certified Kubernetes Administrator", "Docker Certified Associate"
                ],
                "project_management": [
                    "PMP", "PRINCE2", "Scrum Master", "Product Owner", "Agile Certified",
                    "SAFe", "Kanban", "Six Sigma", "ITIL"
                ],
                "security": [
                    "CISSP", "CISM", "CISA", "CompTIA Security+", "Ethical Hacker",
                    "CISSP", "GCIH", "OSCP"
                ],
                "data": [
                    "Certified Data Scientist", "Tableau Certified", "Power BI Certified",
                    "Google Analytics Certified", "Hadoop Certified", "Spark Certified"
                ]
            },
            "methodologies": {
                "development": [
                    "Agile", "Scrum", "Kanban", "Waterfall", "DevOps", "CI/CD", 
                    "Test-Driven Development", "Behavior-Driven Development",
                    "Domain-Driven Design", "Microservices", "RESTful APIs", "GraphQL"
                ],
                "design": [
                    "UX Design", "UI Design", "User Research", "Wireframing", "Prototyping",
                    "Design Thinking", "Human-Computer Interaction", "Information Architecture",
                    "Usability Testing", "Accessibility"
                ]
            }
        }
        
        # Save default taxonomy
        taxonomy_path.parent.mkdir(parents=True, exist_ok=True)
        with open(taxonomy_path, 'w', encoding='utf-8') as f:
            json.dump(default_taxonomy, f, indent=2)
        
        return default_taxonomy
    
    def load_skill_synonyms(self) -> Dict[str, List[str]]:
        """Load skill synonyms for normalization"""
        synonyms_path = self.config.get_skill_synonyms_path()
        
        if synonyms_path.exists():
            with open(synonyms_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Create comprehensive synonyms
        default_synonyms = {
            "JavaScript": ["JS", "Javascript", "ECMAScript", "ES6", "ES2015"],
            "Python": ["Python3", "Python 3", "Py"],
            "Machine Learning": ["ML", "Machine-Learning", "MachineLearning"],
            "Artificial Intelligence": ["AI", "A.I.", "Artificial-Intelligence"],
            "Natural Language Processing": ["NLP", "Natural-Language-Processing"],
            "React": ["ReactJS", "React.js"],
            "Node.js": ["NodeJS", "Node"],
            "PostgreSQL": ["Postgres", "PostgresQL"],
            "MongoDB": ["Mongo", "Mongo DB"],
            "Amazon Web Services": ["AWS", "Amazon AWS"],
            "Microsoft Azure": ["Azure", "MS Azure"],
            "Google Cloud Platform": ["GCP", "Google Cloud"],
            "Kubernetes": ["K8s", "k8s"],
            "Docker": ["Docker Container", "Containerization"],
            "Visual Studio Code": ["VS Code", "VSCode"],
            "GitHub": ["Github"],
            "DevOps": ["Dev Ops"],
            "CI/CD": ["Continuous Integration", "Continuous Deployment", "CI CD"],
            "REST": ["RESTful", "REST API", "RESTful API"],
            "JSON": ["JavaScript Object Notation"],
            "XML": ["Extensible Markup Language"],
            "SQL": ["Structured Query Language"],
            "NoSQL": ["No SQL"],
            "TensorFlow": ["Tensor Flow"],
            "scikit-learn": ["sklearn", "sci-kit learn"],
            "jQuery": ["JQuery"]
        }
        
        synonyms_path.parent.mkdir(parents=True, exist_ok=True)
        with open(synonyms_path, 'w', encoding='utf-8') as f:
            json.dump(default_synonyms, f, indent=2)
        
        return default_synonyms
    
    def _build_skill_index(self) -> Dict[str, Dict[str, str]]:
        """Build a searchable index of all skills"""
        skill_index = {}
        
        for category, subcategories in self.taxonomy.items():
            for subcategory, skills in subcategories.items():
                for skill in skills:
                    skill_key = skill.lower()
                    skill_index[skill_key] = {
                        "canonical": skill,
                        "category": f"{category}.{subcategory}"
                    }
                    
                    # Add synonyms
                    if skill in self.synonyms:
                        for synonym in self.synonyms[skill]:
                            skill_index[synonym.lower()] = {
                                "canonical": skill,
                                "category": f"{category}.{subcategory}"
                            }
        
        return skill_index
    
    def normalize_skill(self, skill: str) -> Optional[Dict[str, str]]:
        """Normalize a skill name to canonical form"""
        skill_lower = skill.lower().strip()
        return self.all_skills.get(skill_lower)

class SkillExtractor:
    """Advanced skill extraction with multiple methods"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.taxonomy = SkillTaxonomy(config)
        
        # Load spaCy model
        try:
            self.nlp = spacy.load(self.config.SPACY_MODEL)
        except OSError:
            logger.warning(f"spaCy model {self.config.SPACY_MODEL} not found. Using blank model.")
            self.nlp = spacy.blank("en")
        
        # Skill extraction patterns
        self.skill_patterns = [
            r'(?:experienced|proficient|skilled|expert|specialist)\s+(?:in|with|at)\s+([^,.]{2,40})',
            r'(?:knowledge|experience|expertise)\s+(?:of|in|with|using)\s+([^,.]{2,40})',
            r'(?:using|worked with|utilized|implemented|developed with)\s+([^,.]{2,40})',
            r'(?:technologies|tools|frameworks|languages)[\s:]+([^.]{10,100})',
            r'(?:skills|competencies)[\s:]+([^.]{10,150})'
        ]
        
        # Context patterns for skill validation
        self.positive_contexts = [
            r'develop\w*', r'build\w*', r'creat\w*', r'implement\w*', r'design\w*',
            r'manag\w*', r'lead\w*', r'architect\w*', r'optimi[sz]\w*', r'deploy\w*',
            r'maintain\w*', r'troubleshoot\w*', r'configur\w*', r'program\w*'
        ]
        
        # Initialize TF-IDF for skill similarity
        self.tfidf = TfidfVectorizer(max_features=1000, stop_words='english', ngram_range=(1, 2))
    
    def extract_skills_phase1(self, resume_text: str) -> List[Dict[str, Any]]:
        """Phase 1: Comprehensive skill extraction"""
        if not resume_text or len(resume_text.strip()) < 50:
            return []
        
        # Process text with spaCy
        doc = self.nlp(resume_text)
        
        # Extract skills using multiple methods
        all_skills = []
        
        # Method 1: Taxonomy-based extraction
        taxonomy_skills = self._extract_taxonomy_skills(resume_text, doc)
        all_skills.extend(taxonomy_skills)
        
        # Method 2: Pattern-based extraction
        pattern_skills = self._extract_pattern_skills(resume_text)
        all_skills.extend(pattern_skills)
        
        # Method 3: NER-based extraction
        ner_skills = self._extract_ner_skills(doc)
        all_skills.extend(ner_skills)
        
        # Method 4: Section-based extraction
        section_skills = self._extract_section_skills(resume_text)
        all_skills.extend(section_skills)
        
        # Normalize and deduplicate
        normalized_skills = self._normalize_and_merge_skills(all_skills)
        
        # Score skills
        scored_skills = self._score_skills(normalized_skills, resume_text, doc)
        
        # Filter and rank
        final_skills = self._filter_and_rank_skills(scored_skills)
        
        return final_skills[:self.config.MAX_SKILLS_PER_RESUME]
    
    def _extract_taxonomy_skills(self, text: str, doc) -> List[Dict[str, Any]]:
        """Extract skills by matching against taxonomy"""
        skills = []
        text_lower = text.lower()
        
        for skill_key, skill_info in self.taxonomy.all_skills.items():
            if self._find_skill_in_text(skill_key, text_lower):
                evidence = self._find_evidence(skill_info['canonical'], text, doc)
                if evidence:  # Only add if we found evidence
                    skills.append({
                        'name': skill_info['canonical'],
                        'category': skill_info['category'],
                        'evidence': evidence,
                        'extraction_method': 'taxonomy',
                        'matched_term': skill_key
                    })
        
        return skills
    
    def _extract_pattern_skills(self, text: str) -> List[Dict[str, Any]]:
        """Extract skills using regex patterns"""
        skills = []
        
        for pattern in self.skill_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                potential_skills = match.group(1).strip()
                
                # Split by common delimiters
                skill_candidates = re.split(r'[,;|&\n]', potential_skills)
                
                for candidate in skill_candidates:
                    candidate = candidate.strip()
                    if self._is_valid_skill_candidate(candidate):
                        # Try to normalize
                        normalized = self.taxonomy.normalize_skill(candidate)
                        if normalized:
                            skills.append({
                                'name': normalized['canonical'],
                                'category': normalized['category'],
                                'evidence': [{
                                    'text': match.group(0),
                                    'start': match.start(),
                                    'end': match.end()
                                }],
                                'extraction_method': 'pattern',
                                'matched_term': candidate
                            })
                        else:
                            # Add as unknown skill if it looks valid
                            skills.append({
                                'name': candidate.title(),
                                'category': 'unknown.pattern',
                                'evidence': [{
                                    'text': match.group(0),
                                    'start': match.start(),
                                    'end': match.end()
                                }],
                                'extraction_method': 'pattern',
                                'matched_term': candidate
                            })
        
        return skills
    
    def _extract_ner_skills(self, doc) -> List[Dict[str, Any]]:
        """Extract skills using Named Entity Recognition"""
        skills = []
        
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'LANGUAGE', 'PERSON']:
                # Filter for technology-related entities
                if self._is_technology_entity(ent.text):
                    normalized = self.taxonomy.normalize_skill(ent.text)
                    if normalized:
                        skills.append({
                            'name': normalized['canonical'],
                            'category': normalized['category'],
                            'evidence': [{
                                'text': ent.sent.text,
                                'start': ent.start_char,
                                'end': ent.end_char
                            }],
                            'extraction_method': 'ner',
                            'matched_term': ent.text,
                            'ner_label': ent.label_
                        })
        
        return skills
    
    def _extract_section_skills(self, text: str) -> List[Dict[str, Any]]:
        """Extract skills from dedicated sections"""
        skills = []
        
        # Find skills section
        sections = self._identify_sections(text)
        skills_section = sections.get('skills', '')
        
        if skills_section:
            # Extract from bullet points and lists
            lines = skills_section.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.lower().startswith('skill'):
                    # Remove bullet points and numbering
                    cleaned_line = re.sub(r'^[-•*\d\.)]\s*', '', line)
                    
                    # Split by common delimiters
                    skill_candidates = re.split(r'[,;|&]', cleaned_line)
                    
                    for candidate in skill_candidates:
                        candidate = candidate.strip()
                        if self._is_valid_skill_candidate(candidate):
                            normalized = self.taxonomy.normalize_skill(candidate)
                            if normalized:
                                skills.append({
                                    'name': normalized['canonical'],
                                    'category': normalized['category'],
                                    'evidence': [{
                                        'text': line,
                                        'start': text.find(line),
                                        'end': text.find(line) + len(line)
                                    }],
                                    'extraction_method': 'section',
                                    'matched_term': candidate
                                })
        
        return skills
    
    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identify different sections in resume"""
        sections = {}
        
        section_patterns = {
            'skills': r'(?i)(technical\s+skills?|skills?|competenc\w+|proficienc\w+)[\s:]*\n(.*?)(?=\n\s*[A-Z][A-Za-z\s]{3,}:|\Z)',
            'experience': r'(?i)(work\s+experience|experience|employment)[\s:]*\n(.*?)(?=\n\s*[A-Z][A-Za-z\s]{3,}:|\Z)',
            'education': r'(?i)(education|academic|qualification)[\s:]*\n(.*?)(?=\n\s*[A-Z][A-Za-z\s]{3,}:|\Z)',
            'projects': r'(?i)(projects?|portfolio)[\s:]*\n(.*?)(?=\n\s*[A-Z][A-Za-z\s]{3,}:|\Z)'
        }
        
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
            if match:
                sections[section_name] = match.group(2).strip()
        
        return sections
    
    def _find_skill_in_text(self, skill: str, text: str) -> bool:
        """Find skill in text with word boundaries"""
        # Create pattern with word boundaries
        pattern = r'\b' + re.escape(skill) + r'\b'
        return bool(re.search(pattern, text, re.IGNORECASE))
    
    def _find_evidence(self, skill: str, text: str, doc) -> List[Dict[str, Any]]:
        """Find evidence sentences for a skill"""
        evidence = []
        skill_lower = skill.lower()
        
        # Use spaCy sentences for better evidence
        for sent in doc.sents:
            sent_text = sent.text.strip()
            if skill_lower in sent_text.lower() and len(sent_text) > 10:
                # Find the exact position in original text
                start_pos = text.find(sent_text)
                if start_pos != -1:
                    evidence.append({
                        'text': sent_text,
                        'start': start_pos,
                        'end': start_pos + len(sent_text)
                    })
                
                if len(evidence) >= 3:  # Limit evidence
                    break
        
        return evidence
    
    def _is_valid_skill_candidate(self, candidate: str) -> bool:
        """Validate if text could be a skill"""
        if not candidate or len(candidate.strip()) < self.config.MIN_SKILL_LENGTH:
            return False
        
        if len(candidate) > self.config.MAX_SKILL_LENGTH:
            return False
        
        # Filter out common non-skills
        invalid_patterns = [
            r'^\d+$',  # Pure numbers
            r'^[a-z]{1,2}$',  # Single/double letters
            r'\b(the|and|or|in|on|at|to|for|with|by|of|a|an)\b',  # Common words
            r'\b(years?|months?|days?)\b',  # Time words
            r'^(including|such as|like|etc)$'  # Connective words
        ]
        
        candidate_lower = candidate.lower()
        for pattern in invalid_patterns:
            if re.search(pattern, candidate_lower):
                return False
        
        return True
    
    def _is_technology_entity(self, text: str) -> bool:
        """Check if entity could be a technology skill"""
        tech_indicators = [
            'software', 'framework', 'library', 'database', 'tool', 'platform',
            'language', 'api', 'cloud', 'server', 'system'
        ]
        
        text_lower = text.lower()
        
        # Check if it's a known skill
        if self.taxonomy.normalize_skill(text):
            return True
        
        # Check for tech indicators in context (this is simplified)
        return len(text) <= 30 and not text.isdigit()
    
    def _normalize_and_merge_skills(self, skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize skill names and merge duplicates"""
        skill_map = {}
        
        for skill in skills:
            canonical_name = skill['name']
            
            if canonical_name not in skill_map:
                skill_map[canonical_name] = skill
            else:
                # Merge evidence and update extraction methods
                existing = skill_map[canonical_name]
                existing['evidence'].extend(skill['evidence'])
                existing['evidence'] = existing['evidence'][:5]  # Limit evidence
                
                # Track multiple extraction methods
                if 'extraction_methods' not in existing:
                    existing['extraction_methods'] = [existing['extraction_method']]
                existing['extraction_methods'].append(skill['extraction_method'])
                existing['extraction_methods'] = list(set(existing['extraction_methods']))
        
        return list(skill_map.values())
    
    def _score_skills(self, skills: List[Dict[str, Any]], text: str, doc) -> List[Dict[str, Any]]:
        """Score skills based on multiple factors"""
        text_lower = text.lower()
        
        for skill in skills:
            skill_name = skill['name']
            skill_lower = skill_name.lower()
            
            # Base score from extraction method
            method_scores = {
                'taxonomy': 0.8,
                'pattern': 0.7,
                'ner': 0.6,
                'section': 0.9
            }
            
            base_score = method_scores.get(skill['extraction_method'], 0.5)
            
            # Multiple extraction methods boost
            if 'extraction_methods' in skill:
                method_boost = len(skill['extraction_methods']) * 0.1
                base_score = min(base_score + method_boost, 1.0)
            
            # Frequency boost
            frequency = text_lower.count(skill_lower)
            frequency_boost = min(frequency * 0.05, 0.2)
            
            # Evidence quality boost
            evidence_boost = min(len(skill['evidence']) * 0.03, 0.15)
            
            # Context boost
            context_boost = self._calculate_context_boost(skill, text, doc)
            
            # Category boost (technical skills slightly higher)
            category_boost = 0.1 if skill['category'].startswith('technical') else 0.05
            
            # Calculate final score
            final_score = min(
                base_score + frequency_boost + evidence_boost + context_boost + category_boost,
                1.0
            )
            
            skill.update({
                'score': int(final_score * 100),
                'confidence': final_score,
                'level': self._determine_skill_level(skill, text),
                'frequency': frequency
            })
        
        return skills
    
    def _calculate_context_boost(self, skill: Dict[str, Any], text: str, doc) -> float:
        """Calculate boost based on context quality"""
        boost = 0.0
        skill_name = skill['name'].lower()
        
        # Check for positive action verbs near skill mentions
        for evidence in skill['evidence']:
            context_window = 100  # Characters around skill mention
            start = max(0, evidence['start'] - context_window)
            end = min(len(text), evidence['end'] + context_window)
            context = text[start:end].lower()
            
            for pattern in self.positive_contexts:
                if re.search(pattern, context):
                    boost += 0.05
                    break
        
        return min(boost, 0.2)
    
    def _determine_skill_level(self, skill: Dict[str, Any], text: str) -> str:
        """Determine skill proficiency level"""
        text_lower = text.lower()
        skill_lower = skill['name'].lower()
        
        # Look for explicit level indicators
        level_patterns = {
            'Expert': ['expert', 'advanced', 'senior', 'lead', 'architect', 'principal'],
            'Advanced': ['experienced', 'proficient', 'skilled', 'strong'],
            'Intermediate': ['intermediate', 'working knowledge', 'familiar'],
            'Beginner': ['basic', 'beginner', 'learning', 'introduced to']
        }
        
        # Check context around skill mentions
        for evidence in skill['evidence']:
            context_window = 50
            start = max(0, evidence['start'] - context_window)
            end = min(len(text), evidence['end'] + context_window)
            context = text_lower[start:end]
            
            for level, indicators in level_patterns.items():
                if any(indicator in context for indicator in indicators):
                    return level
        
        # Default based on evidence quantity and quality
        evidence_count = len(skill['evidence'])
        frequency = skill.get('frequency', 0)
        
        if evidence_count >= 3 or frequency >= 3:
            return 'Advanced'
        elif evidence_count >= 2 or frequency >= 2:
            return 'Intermediate'
        else:
            return 'Beginner'
    
    def _filter_and_rank_skills(self, skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter skills by confidence and rank them"""
        # Filter by minimum confidence
        filtered_skills = [
            skill for skill in skills 
            if skill['confidence'] >= self.config.MIN_SKILL_CONFIDENCE
        ]
        
        # Sort by score (descending)
        filtered_skills.sort(key=lambda x: x['score'], reverse=True)
        
        return filtered_skills

# Main function for Phase 1
def analyze_resume_phase1(resume_text: str) -> Dict[str, Any]:
    """Phase 1 implementation: Extract skills only"""
    try:
        extractor = SkillExtractor()
        skills = extractor.extract_skills_phase1(resume_text)
        
        # Format skills for API response
        formatted_skills = []
        for i, skill in enumerate(skills):
            formatted_skills.append({
                "id": f"skill_{i}",
                "name": skill['name'],
                "category": skill['category'],
                "score": skill['score'],
                "level": skill['level'],
                "confidence": skill['confidence'],
                "evidence": skill['evidence'][:3]  # Limit evidence for API
            })
        
        return {
            "version": Config.API_VERSION,
            "skills": formatted_skills
        }
    
    except Exception as e:
        logger.error(f"Error in analyze_resume_phase1: {e}")
        return {
            "version": Config.API_VERSION,
            "skills": [],
            "error": str(e)
        }

if __name__ == "__main__":
    # Test the skill extractor
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
    
    Developed an e-commerce platform with 10,000+ users using React and Node.js
    Built a recommendation system using Python and machine learning algorithms
    """
    
    result = analyze_resume_phase1(sample_resume)
    print("=== SKILL EXTRACTION TEST ===")
    print(json.dumps(result, indent=2))
    print(f"\nTotal skills extracted: {len(result['skills'])}")
# Add this to your existing skill_extractor.py

class MLEnhancedSkillExtractor(SkillExtractor):
    """Enhanced skill extractor using trained ML models"""
    
    def __init__(self, config: Optional[Config] = None):
        super().__init__(config)
        self.trained_ner = None
        self.skill_classifier = None
        self._load_trained_models()
    
    def _load_trained_models(self):
        """Load trained ML models if available"""
        try:
            # Load trained NER model
            if (self.config.NER_MODEL_PATH / "meta.json").exists():
                self.trained_ner = spacy.load(self.config.NER_MODEL_PATH)
                logger.info("Loaded trained NER model")
            
            # Load skill classifier
            from model_trainer import SkillClassificationTrainer
            self.skill_classifier = SkillClassificationTrainer(self.config)
            if self.skill_classifier.load_trained_model():
                logger.info("Loaded trained skill classifier")
            
        except Exception as e:
            logger.warning(f"Could not load trained models: {e}")
    
    def extract_skills_phase1(self, resume_text: str) -> List[Dict[str, Any]]:
        """Enhanced skill extraction using trained models"""
        # Get base extraction results
        base_skills = super().extract_skills_phase1(resume_text)
        
        # Enhance with trained models if available
        if self.trained_ner:
            ml_skills = self._extract_with_trained_ner(resume_text)
            base_skills.extend(ml_skills)
        
        # Enhance categories with trained classifier
        if self.skill_classifier:
            base_skills = self._enhance_categories(base_skills)
        
        return self._deduplicate_and_rank(base_skills)
    
    def _extract_with_trained_ner(self, text: str) -> List[Dict[str, Any]]:
        """Extract skills using trained NER model"""
        doc = self.trained_ner(text)
        skills = []
        
        for ent in doc.ents:
            if ent.label_ == "SKILL":
                skills.append({
                    'name': ent.text.strip(),
                    'category': 'ml_extracted',
                    'evidence': [{
                        'text': ent.sent.text,
                        'start': ent.start_char,
                        'end': ent.end_char
                    }],
                    'extraction_method': 'trained_ner',
                    'confidence': 0.8  # NER confidence
                })
        
        return skills
    
    def _enhance_categories(self, skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhance skill categories using trained classifier"""
        for skill in skills:
            if skill['category'] in ['ml_extracted', 'unknown.pattern']:
                predicted_category, confidence = self.skill_classifier.predict_skill_category(skill['name'])
                if confidence > 0.6:  # High confidence threshold
                    skill['category'] = predicted_category
                    skill['category_confidence'] = confidence
        
        return skills
