# train_and_analyze.py

import json
import logging
import random
import re
from pathlib import Path
from datetime import datetime, timezone
import spacy
from spacy.training.example import Example
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from collections import Counter
from tqdm import tqdm

# --- CONFIGURATION ---

# 1. Directory Configuration
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
NER_MODEL_DIR = MODELS_DIR / "ner_model"

# JSON data paths
JOBS_JSON = DATA_DIR / "jobs" / "json" / "all_jobs.json"
COURSES_JSON = DATA_DIR / "courses" / "json" / "unified_courses.json"
RESUMES_JSON = DATA_DIR / "resumes" / "json" / "all_resumes.json"
SKILLS_JSON = DATA_DIR / "skills" / "json" / "unified_skills.json"

# 2. Logging Configuration
LOG_FILE = BASE_DIR / "analysis.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Predefined skill set for fallback extraction
SKILLS_DB = {
    "python", "java", "javascript", "c++", "c#", "php", "ruby", "swift", "kotlin", "go",
    "rust", "typescript", "sql", "bash", "powershell", "r", "matlab", "scala",
    "html", "css", "react", "angular", "vue.js", "node.js", "django", "flask", "asp.net",
    "ruby on rails", "redux", "webpack", "graphql", "rest api", "mysql", "postgresql",
    "mongodb", "sqlite", "microsoft sql server", "oracle", "redis", "cassandra", "dynamodb",
    "aws", "azure", "google cloud", "gcp", "heroku", "digitalocean", "s3", "ec2", "lambda",
    "cloudfront", "rds", "git", "docker", "kubernetes", "jenkins", "ansible", "terraform",
    "ci/cd", "jira", "confluence", "machine learning", "tensorflow", "pytorch", "pandas",
    "numpy", "scikit-learn", "keras", "tableau", "power bi", "hadoop", "spark", "data analysis",
    "leadership", "communication", "problem solving", "teamwork", "critical thinking",
    "agile", "scrum", "project management", "collaboration", "mentoring"
}


# --- UTILITY FUNCTIONS ---

def load_json_data(file_path):
    """Loads a JSON file, handling potential errors."""
    if not file_path.exists():
        logging.error(f"Data file not found: {file_path}")
        return None
    try:
        # Special handling for skills JSON which is a dictionary, not a list of records
        if "unified_skills.json" in str(file_path):
             with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                df = pd.DataFrame(data['skills'], columns=['skills'])
        else:
            df = pd.read_json(file_path)

        logging.info(f"Successfully loaded {len(df)} records from {file_path.name}")
        return df
    except Exception as e:
        logging.error(f"Error loading {file_path}: {e}")
        return None

def extract_skills_from_text(text):
    """Fallback skill extractor for any text block using the SKILLS_DB."""
    if not isinstance(text, str): return []
    text_lower = text.lower()
    found_skills = {skill for skill in SKILLS_DB if re.search(r'\b' + re.escape(skill) + r'\b', text_lower)}
    return sorted(list(found_skills))


# --- NLP & SKILL EXTRACTION LAYER ---

def create_spacy_training_data(texts, skills_list):
    """
    Creates training data for spaCy NER, intelligently handling overlapping entities.
    """
    # Sort skills by length (desc) to find longer matches first (e.g., "react js" before "react")
    sorted_skills = sorted(skills_list, key=len, reverse=True)
    
    training_data = []
    for text in tqdm(texts, desc="Creating NER training data"):
        if not isinstance(text, str): continue
        
        entities = []
        # Create a bitmask to track used character indices
        tagged_indices = [False] * len(text)
        
        for skill in sorted_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                start, end = match.span()
                # Check if any character in this span is already tagged
                if any(tagged_indices[start:end]):
                    continue
                
                # If not, add the entity and mark indices as tagged
                entities.append((start, end, "SKILL"))
                for i in range(start, end):
                    tagged_indices[i] = True
                    
        if entities:
            training_data.append((text, {"entities": entities}))
            
    return training_data

def train_ner_model(training_data, model_path, iterations=10):
    """Trains a custom spaCy NER model for skill extraction."""
    logging.info("Starting NER model training...")
    nlp = spacy.blank("en")
    
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    
    for _, annotations in training_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            random.shuffle(training_data)
            losses = {}
            for text, annotations in tqdm(training_data, desc=f"Iteration {itn+1}/{iterations}"):
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                nlp.update([example], drop=0.35, sgd=optimizer, losses=losses)
            logging.info(f"Iteration {itn+1} - Losses: {losses}")

    model_path.mkdir(parents=True, exist_ok=True)
    nlp.to_disk(model_path)
    logging.info(f"NER model trained and saved to {model_path}")


# --- SKILL TREND ANALYSIS LAYER ---

def analyze_job_market_trends(jobs_df, top_n=20):
    """Analyzes job data to find and display the most in-demand skills."""
    logging.info("Analyzing job market skill trends...")
    if 'extracted_skills' not in jobs_df.columns:
        logging.error("Jobs data does not contain 'extracted_skills' column.")
        return
        
    all_skills = [skill for sublist in jobs_df['extracted_skills'] for skill in sublist]
    skill_counts = Counter(all_skills)
    
    print("\n--- Top 20 Most In-Demand Skills ---")
    for i, (skill, count) in enumerate(skill_counts.most_common(top_n), 1):
        print(f"{i:2}. {skill:<20} | Mentions: {count}")
    print("-" * 40)


# --- RECOMMENDATION ENGINE ---

class SkillGapAnalyzer:
    def __init__(self, courses_df, jobs_df, ner_model_path=None):
        self.courses_df = courses_df
        self.jobs_df = jobs_df
        self.nlp = None
        
        if ner_model_path and ner_model_path.exists() and (ner_model_path / "meta.json").exists():
            try:
                self.nlp = spacy.load(ner_model_path)
                logging.info(f"Loaded custom NER model from {ner_model_path}")
            except Exception as e:
                logging.warning(f"Could not load NER model from {ner_model_path} due to error: {e}. Falling back to keyword matching.")
        else:
            logging.warning("Custom NER model not found or invalid. Skill extraction will rely on basic keyword matching.")

        # Prepare for course recommendation
        self.courses_df['recommend_text'] = self.courses_df['title'].fillna('') + ' ' + self.courses_df['skills'].apply(lambda x: ' '.join(x) if isinstance(x, list) else '')
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.course_tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.courses_df['recommend_text'])

    def extract_skills_from_resume(self, resume_text):
        """Extracts skills from text using the trained NER model or a fallback."""
        if self.nlp:
            doc = self.nlp(resume_text)
            skills = sorted(list(set([ent.text.lower() for ent in doc.ents if ent.label_ == "SKILL"])))
            return skills
        else:
            return extract_skills_from_text(resume_text)

    def find_skill_gap(self, resume_skills, job_skills):
        """Identifies skills in the job that are missing from the resume."""
        if not job_skills: return []
        missing_skills = list(set(job_skills) - set(resume_skills))
        return sorted(missing_skills)

    def recommend_courses(self, missing_skills, top_n=5):
        """Recommends top N courses based on a list of missing skills."""
        if not missing_skills: return []
        
        missing_skills_text = ' '.join(missing_skills)
        missing_skills_vector = self.tfidf_vectorizer.transform([missing_skills_text])
        cosine_similarities = cosine_similarity(missing_skills_vector, self.course_tfidf_matrix).flatten()
        top_course_indices = cosine_similarities.argsort()[-top_n:][::-1]
        
        recommendations = self.courses_df.iloc[top_course_indices]
        return recommendations[['title', 'provider', 'url', 'difficulty']].to_dict('records')

# --- MAIN EXECUTION SCRIPT ---

def main():
    logging.info("="*45)
    logging.info(" AI Skill Gap Analysis & Recommendation System ")
    logging.info("="*45)

    # --- 1. Train the NER model (if needed) ---
    is_model_valid = NER_MODEL_DIR.exists() and (NER_MODEL_DIR / "meta.json").exists()
    
    if not is_model_valid:
        logging.info("Custom NER model not found or is invalid. Training a new model.")
        jobs_df = load_json_data(JOBS_JSON)
        skills_df = load_json_data(SKILLS_JSON)

        if jobs_df is not None and skills_df is not None:
            job_descriptions = jobs_df['description'].dropna().tolist()
            # Correctly convert the DataFrame column to a list of skills
            master_skill_list = skills_df['skills'].tolist()
            
            training_data = create_spacy_training_data(job_descriptions[:500], master_skill_list)
            
            if training_data:
                train_ner_model(training_data, NER_MODEL_DIR)
            else:
                logging.error("Could not create training data. Aborting NER training.")
        else:
            logging.error("Required data files for training not found. Aborting NER training.")
            
    # --- 2. Run Job Market Trend Analysis ---
    jobs_df = load_json_data(JOBS_JSON)
    if jobs_df is not None:
        analyze_job_market_trends(jobs_df)

    # --- 3. Perform Skill Gap Analysis on a sample resume ---
    logging.info("\n--- Sample Skill Gap Analysis ---")
    courses_df = load_json_data(COURSES_JSON)
    resumes_df = load_json_data(RESUMES_JSON)

    if jobs_df is not None and courses_df is not None and resumes_df is not None:
        analyzer = SkillGapAnalyzer(courses_df, jobs_df, NER_MODEL_DIR)

        # Select samples for demonstration
        sample_resume_index = 0
        sample_job_index = 5 
        
        sample_resume = resumes_df.iloc[sample_resume_index]
        sample_job = jobs_df.iloc[sample_job_index]

        print("\n" + "="*50)
        print(f"ANALYZING RESUME: {sample_resume['metadata']['filename']}")
        print(f"TARGET JOB: '{sample_job['title']}' at {sample_job['company']}")
        print("="*50 + "\n")

        resume_skills = analyzer.extract_skills_from_resume(sample_resume['raw_text'])
        print(f"✅ Skills found in resume:\n   {', '.join(resume_skills) if resume_skills else 'None'}\n")

        job_skills = sample_job['extracted_skills']
        print(f"🎯 Skills required for job:\n   {', '.join(job_skills) if job_skills else 'None'}\n")
        
        missing_skills = analyzer.find_skill_gap(resume_skills, job_skills)
        
        if not missing_skills:
            print("🎉 Congratulations! No significant skill gap found.")
        else:
            print(f"❌ Skill Gap Identified (missing skills):\n   {', '.join(missing_skills)}\n")
            recommendations = analyzer.recommend_courses(missing_skills)
            
            if recommendations:
                print("--- 📚 Recommended Courses to Fill the Gap ---")
                for course in recommendations:
                    print(f"  - Title: {course['title']}")
                    print(f"    Provider: {course.get('provider', 'N/A')} ({course.get('difficulty', 'N/A')})")
                    print(f"    Link: {course['url']}")
            else:
                print("Could not find course recommendations for the missing skills.")
    else:
        logging.error("Could not load all necessary data files for analysis.")


if __name__ == "__main__":
    main()

