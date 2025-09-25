import os
import requests
import zipfile
import pandas as pd
import json
from pathlib import Path
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import time
import logging
import re # Added for text cleaning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self, base_dir="project_data"):
        self.base_dir = Path(base_dir)
        self.setup_directories()
        self.setup_kaggle_api()
    
    def setup_directories(self):
        """Create the main directory structure for the project."""
        directories = [
            self.base_dir / "resumes" / "raw_text",
            self.base_dir / "resumes" / "processed", # Added processed directory for resumes
            self.base_dir / "job_descriptions" / "processed", # Added processed directory for job descriptions
            self.base_dir / "job_descriptions",
            self.base_dir / "courses"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
    
    def setup_kaggle_api(self):
        """Initialize Kaggle API with authentication."""
        try:
            self.api = KaggleApi()
            self.api.authenticate()
            logger.info("Kaggle API authenticated successfully")
        except Exception as e:
            logger.error(f"Failed to authenticate Kaggle API: {e}")
            logger.info("Please ensure kaggle.json is in ~/.kaggle/ directory")
            raise
    
    def download_with_retry(self, download_func, max_retries=3, delay=5):
        """Download with retry mechanism for handling network issues."""
        for attempt in range(max_retries):
            try:
                download_func()
                return True
            except Exception as e:
                logger.warning(f"Download attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error("All download attempts failed")
                    return False
        return False
    
    def fetch_resume_datasets(self):
        """Download and process resume datasets from Kaggle."""
        logger.info("Starting resume data collection...")
        
        # Dataset 1: Resume Dataset by snehaanbhawal
        def download_resume_dataset():
            logger.info("Downloading snehaanbhawal/resume-dataset...")
            self.api.dataset_download_files(
                'snehaanbhawal/resume-dataset',
                path=str(self.base_dir / "temp"),
                unzip=True
            )
        
        if self.download_with_retry(download_resume_dataset):
            try:
                # Process the resume dataset
                csv_files = list((self.base_dir / "temp").glob("*.csv"))
                if csv_files:
                    df = pd.read_csv(csv_files[0])
                    if 'Resume_str' in df.columns:
                        for idx, resume_text in enumerate(df['Resume_str'].dropna()):
                            filename = f"resume_sneha_{idx:05d}.txt"
                            filepath = self.base_dir / "resumes" / "raw_text" / filename
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(str(resume_text))
                        logger.info(f"Processed {len(df['Resume_str'].dropna())} resumes from snehaanbhawal dataset")
                    else:
                        logger.warning("Resume_str column not found in dataset")
            except Exception as e:
                logger.error(f"Error processing snehaanbhawal resume dataset: {e}")
        
        # Dataset 2: Dataturks Resume Entities
        def download_dataturks_dataset():
            logger.info("Downloading dataturks/resume-entities-for-ner...")
            self.api.dataset_download_files(
                'dataturks/resume-entities-for-ner',
                path=str(self.base_dir / "temp2"),
                unzip=True
            )
        
        if self.download_with_retry(download_dataturks_dataset):
            try:
                # Process the dataturks dataset
                json_files = list((self.base_dir / "temp2").glob("*.json"))
                annotations_data = []
                
                for json_file in json_files:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        for line_idx, line in enumerate(f):
                            try:
                                data = json.loads(line.strip())
                                resume_id = f"dataturks_{json_file.stem}_{line_idx:05d}"
                                
                                # Extract raw text
                                if 'content' in data:
                                    filename = f"{resume_id}.txt"
                                    filepath = self.base_dir / "resumes" / "raw_text" / filename
                                    with open(filepath, 'w', encoding='utf-8') as f:
                                        f.write(data['content'])
                                
                                # Extract annotations
                                if 'annotation' in data:
                                    for annotation in data['annotation']:
                                        for entity in annotation.get('entities', []):
                                            annotations_data.append({
                                                'resume_id': resume_id,
                                                'entity_text': entity.get('value', ''),
                                                'entity_label': entity.get('label', ''),
                                                'start_pos': entity.get('start', 0),
                                                'end_pos': entity.get('end', 0)
                                            })
                            except json.JSONDecodeError as e:
                                logger.warning(f"Skipping invalid JSON line in {json_file}: {e}")
                
                # Save annotations
                if annotations_data:
                    annotations_df = pd.DataFrame(annotations_data)
                    annotations_df.to_csv(
                        self.base_dir / "resumes" / "annotated_resumes.csv",
                        index=False
                    )
                    logger.info(f"Processed {len(annotations_data)} annotations from dataturks dataset")
                
            except Exception as e:
                logger.error(f"Error processing dataturks dataset: {e}")
        
        # Cleanup temp directories
        self._cleanup_temp_dirs()
        logger.info("Resume data collection completed")
    
    def fetch_job_description_datasets(self):
        """Download and process job description datasets from Kaggle."""
        logger.info("Starting job description data collection...")
        
        def download_job_dataset():
            logger.info("Downloading kshitizregmi/jobs-and-job-description...")
            self.api.dataset_download_files(
                'kshitizregmi/jobs-and-job-description',
                path=str(self.base_dir / "temp_jobs"),
                unzip=True
            )
        
        if self.download_with_retry(download_job_dataset):
            try:
                csv_files = list((self.base_dir / "temp_jobs").glob("*.csv"))
                if csv_files:
                    df = pd.read_csv(csv_files[0])
                    
                    # Look for job description column (case insensitive)
                    job_desc_col = None
                    for col in df.columns:
                        if 'job' in col.lower() and 'description' in col.lower():
                            job_desc_col = col
                            break
                    
                    if job_desc_col:
                        for idx, job_desc in enumerate(df[job_desc_col].dropna()):
                            filename = f"job_desc_{idx:05d}.txt"
                            filepath = self.base_dir / "job_descriptions" / filename
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(str(job_desc))
                        logger.info(f"Processed {len(df[job_desc_col].dropna())} job descriptions")
                    else:
                        logger.warning("Job Description column not found in dataset")
                        logger.info(f"Available columns: {list(df.columns)}")
            except Exception as e:
                logger.error(f"Error processing job description dataset: {e}")
        
        self._cleanup_temp_dirs()
        logger.info("Job description data collection completed")
    
    def fetch_course_datasets(self):
        """Download and process course catalog datasets from Kaggle."""
        logger.info("Starting course data collection...")
        
        course_dataframes = []
        
        # Dataset 1: Online Courses by khaledatef1
        def download_courses_1():
            logger.info("Downloading khaledatef1/online-courses...")
            self.api.dataset_download_files(
                'khaledatef1/online-courses',
                path=str(self.base_dir / "temp_courses1"),
                unzip=True
            )
        
        if self.download_with_retry(download_courses_1):
            try:
                csv_files = list((self.base_dir / "temp_courses1").glob("*.csv"))
                if csv_files:
                    df1 = pd.read_csv(csv_files[0])
                    course_dataframes.append(('khaledatef1', df1))
                    logger.info(f"Loaded {len(df1)} courses from khaledatef1 dataset")
            except Exception as e:
                logger.error(f"Error processing khaledatef1 course dataset: {e}")
        
        # Dataset 2: Multi-platform Online Courses by everydaycodings
        def download_courses_2():
            logger.info("Downloading everydaycodings/multi-platform-online-courses-dataset...")
            self.api.dataset_download_files(
                'everydaycodings/multi-platform-online-courses-dataset',
                path=str(self.base_dir / "temp_courses2"),
                unzip=True
            )
        
        if self.download_with_retry(download_courses_2):
            try:
                csv_files = list((self.base_dir / "temp_courses2").glob("*.csv"))
                if csv_files:
                    df2 = pd.read_csv(csv_files[0])
                    course_dataframes.append(('everydaycodings', df2))
                    logger.info(f"Loaded {len(df2)} courses from everydaycodings dataset")
            except Exception as e:
                logger.error(f"Error processing everydaycodings course dataset: {e}")
        
        # Merge and clean course datasets
        if course_dataframes:
            self._clean_and_merge_courses(course_dataframes)
        
        self._cleanup_temp_dirs()
        logger.info("Course data collection completed")
    
    def _clean_and_merge_courses(self, course_dataframes):
        """Clean and merge course datasets into a standardized format."""
        logger.info("Cleaning and merging course datasets...")
        
        standardized_courses = []
        
        for source, df in course_dataframes:
            logger.info(f"Processing {source} dataset with columns: {list(df.columns)}")
            
            # Standardize column mapping based on common patterns
            column_mapping = self._create_column_mapping(df.columns)
            
            for _, row in df.iterrows():
                course_record = {
                    'course_title': self._extract_value(row, column_mapping.get('title', [])),
                    'course_description': self._extract_value(row, column_mapping.get('description', [])),
                    'skills_taught': self._extract_value(row, column_mapping.get('skills', [])),
                    'platform': self._extract_value(row, column_mapping.get('platform', [])),
                    'duration': self._extract_value(row, column_mapping.get('duration', [])),
                    'level': self._extract_value(row, column_mapping.get('level', [])),
                    'rating': self._extract_value(row, column_mapping.get('rating', [])),
                    'price': self._extract_value(row, column_mapping.get('price', []))
                }
                standardized_courses.append(course_record)
        
        # Create final DataFrame and save
        final_df = pd.DataFrame(standardized_courses)
        
        # Handle missing values
        final_df = final_df.fillna('')
        
        # Remove completely empty rows
        final_df = final_df[final_df['course_title'].str.strip() != '']
        
        # Save the cleaned catalog
        output_path = self.base_dir / "courses" / "course_catalog.csv"
        final_df.to_csv(output_path, index=False)
        
        logger.info(f"Saved {len(final_df)} cleaned course records to {output_path}")
    
    def _create_column_mapping(self, columns):
        """Create mapping from standardized names to actual column names."""
        mapping = {
            'title': [],
            'description': [],
            'skills': [],
            'platform': [],
            'duration': [],
            'level': [],
            'rating': [],
            'price': []
        }
        
        for col in columns:
            col_lower = col.lower()
            if any(word in col_lower for word in ['title', 'name', 'course']):
                mapping['title'].append(col)
            elif any(word in col_lower for word in ['description', 'summary', 'overview']):
                mapping['description'].append(col)
            elif any(word in col_lower for word in ['skill', 'tag', 'subject', 'category']):
                mapping['skills'].append(col)
            elif any(word in col_lower for word in ['platform', 'provider', 'site', 'source']):
                mapping['platform'].append(col)
            elif any(word in col_lower for word in ['duration', 'length', 'time']):
                mapping['duration'].append(col)
            elif any(word in col_lower for word in ['level', 'difficulty']):
                mapping['level'].append(col)
            elif any(word in col_lower for word in ['rating', 'score', 'review']):
                mapping['rating'].append(col)
            elif any(word in col_lower for word in ['price', 'cost', 'fee']):
                mapping['price'].append(col)
        
        return mapping
    
    def _extract_value(self, row, column_candidates):
        """Extract value from the first available column candidate."""
        for col in column_candidates:
            if col in row and pd.notna(row[col]):
                return str(row[col])
        return ''
    
    def _clean_text(self, text: str) -> str: # Added text cleaning method
        """Performs basic text cleaning: lowercase, remove special characters, strip extra spaces."""
        text = str(text).lower()
        text = re.sub(r'[^a-z0-9\s]', '', text) # Remove non-alphanumeric characters
        text = re.sub(r'\s+', ' ', text).strip() # Replace multiple spaces with single space
        return text

    def process_raw_data(self): # Added method to process raw data
        """Cleans raw resume and job description texts and saves them to processed directories."""
        logger.info("Starting raw data processing (cleaning and initial feature engineering)...")

        # Process resumes
        raw_resume_dir = self.base_dir / "resumes" / "raw_text"
        processed_resume_dir = self.base_dir / "resumes" / "processed"
        for raw_file in raw_resume_dir.glob("*.txt"):
            with open(raw_file, 'r', encoding='utf-8') as f:
                content = f.read()
            cleaned_content = self._clean_text(content)
            processed_file = processed_resume_dir / raw_file.name
            with open(processed_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            logger.debug(f"Processed resume: {raw_file.name}")
        logger.info(f"Processed {len(list(raw_resume_dir.glob('*.txt')))} raw resumes.")

        # Process job descriptions
        raw_job_dir = self.base_dir / "job_descriptions"
        processed_job_dir = self.base_dir / "job_descriptions" / "processed"
        for raw_file in raw_job_dir.glob("*.txt"):
            with open(raw_file, 'r', encoding='utf-8') as f:
                content = f.read()
            cleaned_content = self._clean_text(content)
            processed_file = processed_job_dir / raw_file.name
            with open(processed_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            logger.debug(f"Processed job description: {raw_file.name}")
        logger.info(f"Processed {len(list(raw_job_dir.glob('*.txt')))} raw job descriptions.")
        logger.info("Raw data processing completed.")
    
    def _cleanup_temp_dirs(self):
        """Clean up temporary directories."""
        import shutil
        temp_dirs = [
            self.base_dir / "temp",
            self.base_dir / "temp2",
            self.base_dir / "temp_jobs",
            self.base_dir / "temp_courses1",
            self.base_dir / "temp_courses2"
        ]
        
        for temp_dir in temp_dirs:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
                logger.info(f"Cleaned up temporary directory: {temp_dir}")

def main():
    """Main execution function."""
    print("=" * 60)
    print("RESUME SKILL GAP ANALYZER - DATA COLLECTION AND PREPROCESSING") # Updated title
    print("=" * 60)
    
    try:
        collector = DataCollector()
        
        print("\n1. Setting up project directories...")
        print("✓ Directory structure created")
        
        print("\n2. Collecting resume datasets...")
        collector.fetch_resume_datasets()
        print("✓ Resume data collection completed")
        
        print("\n3. Collecting job description datasets...")
        collector.fetch_job_description_datasets()
        print("✓ Job description data collection completed")
        
        print("\n4. Collecting course catalog datasets...")
        collector.fetch_course_datasets()
        print("✓ Course data collection completed")

        print("\n5. Processing raw data (cleaning and initial feature engineering)...")
        collector.process_raw_data()
        print("✓ Raw data processing completed")
        
        print("\n" + "=" * 60)
        print("DATA COLLECTION AND PREPROCESSING COMPLETED SUCCESSFULLY!") # Updated success message
        print("=" * 60)
        
        # Print summary
        base_dir = Path("project_data")
        resume_raw_count = len(list((base_dir / "resumes" / "raw_text").glob("*.txt"))) # Added raw count
        resume_processed_count = len(list((base_dir / "resumes" / "processed").glob("*.txt"))) # Added processed count
        job_raw_count = len(list((base_dir / "job_descriptions").glob("*.txt"))) # Added raw count
        job_processed_count = len(list((base_dir / "job_descriptions" / "processed").glob("*.txt"))) # Added processed count
        
        print(f"\nSUMMARY:")
        print(f"- Raw resumes collected: {resume_raw_count}") # Updated summary
        print(f"- Processed resumes: {resume_processed_count}") # Updated summary
        print(f"- Raw job descriptions collected: {job_raw_count}") # Updated summary
        print(f"- Processed job descriptions: {job_processed_count}") # Updated summary
        print(f"- Course catalog: {'✓' if (base_dir / 'courses' / 'course_catalog.csv').exists() else '✗'}\n") # Added newline for spacing
        
    except Exception as e:
        logger.error(f"Data collection and preprocessing failed: {e}") # Updated error message
        print(f"\n❌ Error: {e}")
        print("\nPlease ensure:")
        print("1. Kaggle API is properly configured (~/.kaggle/kaggle.json)")
        print("2. You have internet connection")
        print("3. You have sufficient disk space")
        print("4. All necessary Python packages are installed (check scripts/requirements.txt)") # Added package installation reminder

if __name__ == "__main__":
    main()
