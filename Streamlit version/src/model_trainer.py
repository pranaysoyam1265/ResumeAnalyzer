import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
import json
import random
from pathlib import Path
from typing import List, Dict, Any, Tuple
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle
import numpy as np

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeDatasetCreator:
    """Create training datasets from resume data in /data folder"""
    
    def __init__(self, config: Config):
        self.config = config
        self.resumes_dir = config.RESUMES_DIR / "processed"
        self.annotations_dir = config.RESUMES_DIR / "annotations"
    
    def create_skill_extraction_dataset(self) -> List[Dict[str, Any]]:
        """Create dataset for skill extraction training"""
        dataset = []
        
        # Load processed resumes
        for resume_file in self.resumes_dir.glob("*.txt"):
            with open(resume_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Check for corresponding annotation file
            annotation_file = self.annotations_dir / f"{resume_file.stem}_skills.json"
            if annotation_file.exists():
                with open(annotation_file, 'r', encoding='utf-8') as f:
                    annotations = json.load(f)
                
                # Convert to spaCy training format
                entities = []
                for skill in annotations.get('skills', []):
                    entities.append((skill['start'], skill['end'], 'SKILL'))
                
                dataset.append({
                    "text": text,
                    "entities": entities,
                    "filename": resume_file.name
                })
            else:
                # Auto-generate annotations using existing system
                logger.info(f"Auto-generating annotations for {resume_file.name}")
                auto_annotations = self._auto_generate_skill_annotations(text)
                dataset.append({
                    "text": text,
                    "entities": auto_annotations,
                    "filename": resume_file.name,
                    "auto_generated": True
                })
        
        logger.info(f"Created dataset with {len(dataset)} resume examples")
        return dataset
    
    def _auto_generate_skill_annotations(self, text: str) -> List[Tuple[int, int, str]]:
        """Auto-generate skill annotations using existing extraction logic"""
        from skill_extractor import SkillExtractor
        
        extractor = SkillExtractor(self.config)
        skills = extractor.extract_skills_phase1(text)
        
        entities = []
        for skill in skills:
            for evidence in skill.get('evidence', []):
                start = evidence.get('start', 0)
                end = evidence.get('end', 0)
                if start < end:  # Valid span
                    entities.append((start, end, 'SKILL'))
        
        return entities
    
    def create_course_relevance_dataset(self) -> Tuple[List[str], List[str], List[int]]:
        """Create dataset for course relevance scoring"""
        texts = []
        skills = []
        relevance_scores = []
        
        # Load course data
        for course_file in self.config.COURSES_DIR.glob("*.json"):
            with open(course_file, 'r', encoding='utf-8') as f:
                courses = json.load(f)
            
            for course in courses:
                course_text = f"{course.get('title', '')} {course.get('description', '')}"
                course_skills = course.get('skills', [])
                
                for skill in course_skills:
                    texts.append(course_text)
                    skills.append(skill)
                    # Use rating as relevance score (normalized 0-10)
                    relevance_scores.append(int(course.get('rating', 3) * 2))
        
        logger.info(f"Created course relevance dataset with {len(texts)} examples")
        return texts, skills, relevance_scores

class NERModelTrainer:
    """Train custom NER model for skill extraction"""
    
    def __init__(self, config: Config):
        self.config = config
        self.model_path = config.NER_MODEL_PATH
    
    def train_skill_ner_model(self, training_data: List[Dict[str, Any]], 
                            n_iterations: int = 30) -> None:
        """Train custom NER model for skill extraction"""
        
        # Create blank spaCy model or load existing
        try:
            nlp = spacy.load("en_core_web_sm")
            logger.info("Loaded existing spaCy model")
        except:
            nlp = spacy.blank("en")
            logger.info("Created blank spaCy model")
        
        # Add NER component if not present
        if "ner" not in nlp.pipe_names:
            ner = nlp.add_pipe("ner")
        else:
            ner = nlp.get_pipe("ner")
        
        # Add labels
        ner.add_label("SKILL")
        
        # Convert training data to spaCy format
        examples = []
        for item in training_data:
            doc = nlp.make_doc(item["text"])
            entities = item["entities"]
            example = Example.from_dict(doc, {"entities": entities})
            examples.append(example)
        
        # Training
        logger.info(f"Training NER model with {len(examples)} examples...")
        
        # Disable other pipes during training
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
        with nlp.disable_pipes(*other_pipes):
            
            # Initialize the model
            nlp.initialize(lambda: examples)
            
            # Training loop
            for iteration in range(n_iterations):
                random.shuffle(examples)
                losses = {}
                
                # Batch training
                batches = minibatch(examples, size=compounding(4.0, 32.0, 1.001))
                for batch in batches:
                    nlp.update(batch, losses=losses, drop=0.5)
                
                if iteration % 10 == 0:
                    logger.info(f"Iteration {iteration}, Losses: {losses}")
        
        # Save model
        self.model_path.mkdir(parents=True, exist_ok=True)
        nlp.to_disk(self.model_path)
        logger.info(f"Model saved to {self.model_path}")
    
    def evaluate_model(self, test_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Evaluate trained NER model"""
        try:
            nlp = spacy.load(self.model_path)
        except:
            logger.error("No trained model found")
            return {}
        
        correct_entities = 0
        total_entities = 0
        
        for item in test_data:
            doc = nlp(item["text"])
            predicted_entities = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
            true_entities = item["entities"]
            
            # Simple evaluation - count exact matches
            for true_ent in true_entities:
                total_entities += 1
                if true_ent in predicted_entities:
                    correct_entities += 1
        
        precision = correct_entities / max(total_entities, 1)
        
        logger.info(f"Model evaluation - Precision: {precision:.3f}")
        return {"precision": precision, "correct": correct_entities, "total": total_entities}

class SkillClassificationTrainer:
    """Train skill category classification model"""
    
    def __init__(self, config: Config):
        self.config = config
        self.model_path = config.SKILL_CLASSIFIER_PATH
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def prepare_training_data(self) -> Tuple[List[str], List[str]]:
        """Prepare training data for skill classification"""
        texts = []
        labels = []
        
        # Load skill taxonomy
        taxonomy_path = self.config.get_skill_taxonomy_path()
        with open(taxonomy_path, 'r', encoding='utf-8') as f:
            taxonomy = json.load(f)
        
        # Create training examples from taxonomy
        for category, subcategories in taxonomy.items():
            for subcategory, skills in subcategories.items():
                label = f"{category}.{subcategory}"
                for skill in skills:
                    # Create synthetic training examples
                    texts.extend([
                        f"experienced in {skill}",
                        f"proficient with {skill}",
                        f"skilled in {skill}",
                        f"expert at {skill}",
                        f"working with {skill}",
                        skill.lower()
                    ])
                    labels.extend([label] * 6)
        
        # Add examples from resume data
        processed_dir = self.config.RESUMES_DIR / "processed"
        for resume_file in processed_dir.glob("*.txt"):
            with open(resume_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Extract skill contexts from resumes
            skill_contexts = self._extract_skill_contexts(text)
            for context, skill_category in skill_contexts:
                texts.append(context)
                labels.append(skill_category)
        
        logger.info(f"Prepared {len(texts)} training examples for skill classification")
        return texts, labels
    
    def _extract_skill_contexts(self, text: str) -> List[Tuple[str, str]]:
        """Extract skill contexts from resume text"""
        # This is a simplified implementation
        # In practice, you'd want more sophisticated context extraction
        contexts = []
        
        # Find sentences containing known skills
        sentences = text.split('.')
        for sentence in sentences:
            sentence = sentence.strip().lower()
            if len(sentence) < 10:
                continue
                
            # Check if sentence contains skills (simplified)
            for category in ['programming', 'web_development', 'databases']:
                if any(word in sentence for word in ['python', 'java', 'javascript', 'react', 'sql']):
                    contexts.append((sentence, f"technical_skills.{category}"))
                    break
        
        return contexts
    
    def train_classifier(self) -> None:
        """Train skill classification model"""
        texts, labels = self.prepare_training_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        # Vectorize text
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        # Train classifier
        logger.info("Training skill classification model...")
        self.classifier.fit(X_train_vec, y_train)
        
        # Evaluate
        y_pred = self.classifier.predict(X_test_vec)
        accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"Skill classifier accuracy: {accuracy:.3f}")
        logger.info("\nClassification Report:")
        logger.info(classification_report(y_test, y_pred))
        
        # Save model
        self.model_path.mkdir(parents=True, exist_ok=True)
        
        model_data = {
            'vectorizer': self.vectorizer,
            'classifier': self.classifier,
            'accuracy': accuracy
        }
        
        with open(self.model_path / 'skill_classifier.pkl', 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"Model saved to {self.model_path}")
    
    def load_trained_model(self) -> bool:
        """Load trained classification model"""
        model_file = self.model_path / 'skill_classifier.pkl'
        if model_file.exists():
            with open(model_file, 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data['vectorizer']
            self.classifier = model_data['classifier']
            logger.info(f"Loaded trained model with accuracy: {model_data['accuracy']:.3f}")
            return True
        
        return False
    
    def predict_skill_category(self, skill_text: str) -> Tuple[str, float]:
        """Predict skill category for given text"""
        if not hasattr(self.classifier, 'predict'):
            if not self.load_trained_model():
                return "unknown", 0.0
        
        text_vec = self.vectorizer.transform([skill_text])
        prediction = self.classifier.predict(text_vec)[0]
        probability = max(self.classifier.predict_proba(text_vec)[0])
        
        return prediction, probability

class ModelTrainingPipeline:
    """Complete training pipeline for resume analyzer models"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.dataset_creator = ResumeDatasetCreator(self.config)
        self.ner_trainer = NERModelTrainer(self.config)
        self.skill_classifier = SkillClassificationTrainer(self.config)
    
    def run_complete_training(self) -> Dict[str, Any]:
        """Run complete model training pipeline"""
        logger.info("Starting complete model training pipeline...")
        
        results = {}
        
        try:
            # 1. Create datasets
            logger.info("Step 1: Creating training datasets...")
            skill_dataset = self.dataset_creator.create_skill_extraction_dataset()
            
            if len(skill_dataset) < 5:
                logger.warning("Insufficient training data. Need at least 5 annotated resumes.")
                return {"error": "Insufficient training data"}
            
            # 2. Split dataset
            train_size = int(0.8 * len(skill_dataset))
            train_data = skill_dataset[:train_size]
            test_data = skill_dataset[train_size:]
            
            # 3. Train NER model
            logger.info("Step 2: Training NER model for skill extraction...")
            self.ner_trainer.train_skill_ner_model(train_data, n_iterations=50)
            
            # 4. Evaluate NER model
            logger.info("Step 3: Evaluating NER model...")
            ner_results = self.ner_trainer.evaluate_model(test_data)
            results['ner_evaluation'] = ner_results
            
            # 5. Train skill classifier
            logger.info("Step 4: Training skill classification model...")
            self.skill_classifier.train_classifier()
            results['skill_classifier'] = {"status": "trained"}
            
            # 6. Training summary
            results['training_summary'] = {
                "total_resumes": len(skill_dataset),
                "training_resumes": len(train_data),
                "test_resumes": len(test_data),
                "ner_precision": ner_results.get('precision', 0),
                "models_saved": True
            }
            
            logger.info("Model training completed successfully!")
            return results
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            return {"error": str(e)}
    
    def retrain_with_new_data(self) -> Dict[str, Any]:
        """Retrain models with newly added data"""
        logger.info("Retraining models with new data...")
        return self.run_complete_training()

# Main training function
def train_models_from_data(config: Optional[Config] = None) -> Dict[str, Any]:
    """Train models using data from /data folder"""
    pipeline = ModelTrainingPipeline(config)
    return pipeline.run_complete_training()

if __name__ == "__main__":
    # Create directories
    Config.create_directories()
    
    # Run training
    results = train_models_from_data()
    print("=== TRAINING RESULTS ===")
    print(json.dumps(results, indent=2))
