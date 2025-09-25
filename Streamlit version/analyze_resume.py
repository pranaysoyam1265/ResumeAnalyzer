# analyze_resume.py (Robust Version 2.0)

import json
import logging
import re
from pathlib import Path
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import docx
import PyPDF2

# --- CONFIGURATION ---

# 1. Directory Configuration
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
NER_MODEL_DIR = MODELS_DIR / "ner_model"

# JSON data paths
COURSES_JSON = DATA_DIR / "courses" / "json" / "unified_courses.json"
RESUME_RAW_DIR = DATA_DIR / "resumes" / "raw"
SKILLS_JSON = DATA_DIR / "skills" / "json" / "unified_skills.json"


# 2. Logging (set to a higher level for cleaner output during analysis)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')


# --- UTILITY FUNCTIONS ---

def load_json_data(file_path, is_skills_dict=False):
    """Loads a JSON file, handling both lists of records and skill dictionaries."""
    if not file_path.exists():
        print(f"❌ Error: Data file not found: {file_path}")
        return None
    try:
        if is_skills_dict:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Return the list of skills directly
                skills_list = data.get('skills', [])
                print(f"✅ Successfully loaded {len(skills_list)} skills from {file_path.name}")
                return skills_list
        else:
            df = pd.read_json(file_path)
            print(f"✅ Successfully loaded {len(df)} records from {file_path.name}")
            return df
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None

def extract_text_from_file(file_path):
    """Extracts text from PDF, DOCX, or TXT files."""
    text = ""
    try:
        file_type = file_path.suffix.lower()
        if file_type == '.pdf':
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages: text += page.extract_text() or ""
        elif file_type == '.docx':
            doc = docx.Document(file_path)
            for para in doc.paragraphs: text += para.text + "\n"
        elif file_type == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f: text = f.read()
        return text
    except Exception as e:
        logging.error(f"Error extracting text from {file_path.name}: {e}")
        return ""


# --- CORE ANALYSIS ENGINE ---

class SkillGapAnalyzer:
    def __init__(self, courses_df, master_skills_list, ner_model_path):
        self.courses_df = courses_df
        self.master_skills = set(master_skills_list) # Use a set for faster lookups
        self.nlp = None
        
        # Load the pre-trained custom NER model
        if not ner_model_path.exists() or not (ner_model_path / "meta.json").exists():
            print(f"❌ FATAL ERROR: Trained NER model not found at {ner_model_path}.")
            print("Please run the `train_and_analyze.py` script first to train and save the model.")
            exit()
            
        try:
            self.nlp = spacy.load(ner_model_path)
            print(f"✅ Custom skill extraction model loaded successfully.")
        except Exception as e:
            print(f"❌ FATAL ERROR: Could not load the NER model. Error: {e}")
            exit()

        # Prepare for course recommendation
        self.courses_df['recommend_text'] = self.courses_df['title'].fillna('') + ' ' + self.courses_df['skills'].apply(lambda x: ' '.join(x) if isinstance(x, list) else '')
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.course_tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.courses_df['recommend_text'])

    def extract_and_clean_skills(self, text):
        """
        Extracts skills using the NER model and then rigorously cleans the results.
        """
        if not text or not isinstance(text, str):
            return []
        
        # 1. Extract candidate skills with NER model
        doc = self.nlp(text)
        candidate_skills = {ent.text.lower().strip() for ent in doc.ents if ent.label_ == "SKILL"}
        
        # 2. Add skills from master list found in text (case-insensitive)
        text_lower = text.lower()
        for skill in self.master_skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                candidate_skills.add(skill)

        # 3. Rigorous Cleaning Phase
        cleaned_skills = set()
        for skill in candidate_skills:
            # Rule 1: Remove short, likely irrelevant terms
            if len(skill) <= 2: continue
            # Rule 2: Remove purely numeric skills
            if skill.isdigit(): continue
            # Rule 3: Remove skills that are just common english words (case-insensitive)
            if skill in ['and', 'the', 'for', 'with', 'not', 'are', 'was', 'were', 'from', 'our', 'new', 'all', 'use', 'has', 'had', 'been', 'will', 'also']: continue
            # Rule 4: Check if the skill is in our master list of valid skills
            if skill in self.master_skills:
                 cleaned_skills.add(skill)

        return sorted(list(cleaned_skills))

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

# --- MAIN INTERACTIVE SCRIPT ---

def main():
    print("="*50)
    print("      AI Skill Gap Analysis Tool")
    print("="*50)

    # --- Load necessary data and the trained model ---
    courses_df = load_json_data(COURSES_JSON)
    master_skills_list = load_json_data(SKILLS_JSON, is_skills_dict=True)
    if courses_df is None or master_skills_list is None: return
    
    analyzer = SkillGapAnalyzer(courses_df, master_skills_list, NER_MODEL_DIR)

    while True:
        # --- 1. Get User Resume ---
        resume_filename = input("\n▶️ Enter the filename of your resume (e.g., my_resume.pdf): ")
        resume_path = RESUME_RAW_DIR / resume_filename
        
        if not resume_path.exists():
            print(f"❌ Error: File '{resume_filename}' not found in '{RESUME_RAW_DIR}'. Please try again.")
            continue
            
        resume_text = extract_text_from_file(resume_path)
        if not resume_text:
            print("❌ Error: Could not extract any text from the resume file.")
            continue

        # --- 2. Get Target Job Description ---
        print("\n▶️ Paste the job description below. When you're done, type 'DONE' on a new line and press Enter:")
        job_desc_lines = []
        while True:
            line = input()
            if line.strip().upper() == 'DONE':
                break
            job_desc_lines.append(line)
        job_desc_text = "\n".join(job_desc_lines)

        if not job_desc_text.strip():
            print("❌ Error: Job description cannot be empty.")
            continue
            
        # --- 3. Perform Analysis ---
        print("\n" + "="*22 + " ANALYSIS REPORT " + "="*22)

        resume_skills = analyzer.extract_and_clean_skills(resume_text)
        print(f"\n✅ Skills Found in Your Resume ({len(resume_skills)}):\n   {', '.join(resume_skills) if resume_skills else 'None identified'}\n")

        job_skills = analyzer.extract_and_clean_skills(job_desc_text)
        print(f"🎯 Skills Required for the Job ({len(job_skills)}):\n   {', '.join(job_skills) if job_skills else 'None identified'}\n")
        
        missing_skills = analyzer.find_skill_gap(resume_skills, job_skills)
        
        if not missing_skills:
            print("🎉 Congratulations! No significant skill gap was found for this job.")
        else:
            print(f"❌ Skill Gap Identified ({len(missing_skills)} missing skills):\n   {', '.join(missing_skills)}\n")
            recommendations = analyzer.recommend_courses(missing_skills)
            
            if recommendations:
                print("--- 📚 Recommended Courses to Fill the Gap ---")
                for course in recommendations:
                    print(f"  - Title:      {course['title']}")
                    print(f"    Provider:   {course.get('provider', 'N/A')} ({course.get('difficulty', 'N/A')})")
                    print(f"    Link:       {course['url']}\n")
            else:
                print("Could not find specific course recommendations for the missing skills.")
        
        print("="*61)
        
        # --- 4. Ask to continue ---
        another = input("\nWould you like to analyze another resume? (y/n): ").lower()
        if another != 'y':
            break

    print("\nThank you for using the Skill Gap Analysis Tool!")


if __name__ == "__main__":
    main()

