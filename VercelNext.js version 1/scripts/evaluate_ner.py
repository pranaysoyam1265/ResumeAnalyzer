"""
NER Model Evaluation Script
Compares custom fine-tuned NER model against regex baseline
"""

import re
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from seqeval.metrics import classification_report, f1_score
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaselineNER:
    """Simple baseline NER using regex and keyword matching"""
    
    def __init__(self, skill_list_path: str = None):
        """Initialize with predefined skill list"""
        self.skills = self._load_skill_list(skill_list_path)
        
    def _load_skill_list(self, skill_list_path: str) -> List[str]:
        """Load skill list from file or use default"""
        if skill_list_path and Path(skill_list_path).exists():
            with open(skill_list_path, 'r') as f:
                return [line.strip().lower() for line in f.readlines()]
        
        # Default skill list for testing
        return [
            'python', 'java', 'javascript', 'sql', 'machine learning',
            'data analysis', 'project management', 'communication',
            'leadership', 'teamwork', 'problem solving', 'excel',
            'powerpoint', 'word', 'outlook', 'salesforce', 'tableau',
            'power bi', 'r programming', 'statistics', 'deep learning',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'matplotlib', 'seaborn', 'git', 'docker', 'kubernetes',
            'aws', 'azure', 'gcp', 'linux', 'windows', 'macos'
        ]
    
    def extract_skills(self, text: str) -> List[Tuple[str, int, int]]:
        """
        Extract skills using regex matching
        Returns: List of (skill, start_pos, end_pos) tuples
        """
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            matches = re.finditer(pattern, text_lower)
            
            for match in matches:
                found_skills.append((skill.upper(), match.start(), match.end()))
        
        return found_skills
    
    def baseline_ner(self, text: str, skill_list: List[str] = None) -> List[str]:
        """
        Main baseline NER function
        Returns BIO tags for the input text
        """
        if skill_list:
            self.skills = [s.lower() for s in skill_list]
        
        # Tokenize text (simple whitespace tokenization)
        tokens = text.split()
        bio_tags = ['O'] * len(tokens)
        
        # Find skills and tag tokens
        skills_found = self.extract_skills(text)
        
        for skill, start_pos, end_pos in skills_found:
            # Find which tokens correspond to this skill
            char_pos = 0
            for i, token in enumerate(tokens):
                token_start = char_pos
                token_end = char_pos + len(token)
                
                # Check if token overlaps with skill span
                if (token_start < end_pos and token_end > start_pos):
                    if bio_tags[i] == 'O':  # Only tag if not already tagged
                        if i > 0 and bio_tags[i-1].startswith('B-SKILL'):
                            bio_tags[i] = 'I-SKILL'
                        else:
                            bio_tags[i] = 'B-SKILL'
                
                char_pos = token_end + 1  # +1 for space
        
        return bio_tags

class NEREvaluator:
    """Evaluates NER models against test dataset"""
    
    def __init__(self, model_path: str = "./ner_skill_extractor"):
        """Initialize with fine-tuned model path"""
        self.model_path = model_path
        self.baseline = BaselineNER()
        self.custom_model = None
        self._load_custom_model()
    
    def _load_custom_model(self):
        """Load the fine-tuned NER model"""
        try:
            self.custom_model = pipeline(
                "ner",
                model=self.model_path,
                tokenizer=self.model_path,
                aggregation_strategy="simple"
            )
            logger.info(f"Loaded custom NER model from {self.model_path}")
        except Exception as e:
            logger.warning(f"Could not load custom model: {e}")
            logger.info("Will use mock predictions for testing")
    
    def _custom_model_predict(self, text: str) -> List[str]:
        """Get predictions from custom model"""
        if not self.custom_model:
            # Mock predictions for testing
            tokens = text.split()
            return ['O'] * len(tokens)
        
        try:
            # Get NER predictions
            predictions = self.custom_model(text)
            
            # Convert to BIO format
            tokens = text.split()
            bio_tags = ['O'] * len(tokens)
            
            for pred in predictions:
                # Map character positions to token positions
                start_char = pred['start']
                end_char = pred['end']
                label = pred['entity_group']
                
                char_pos = 0
                for i, token in enumerate(tokens):
                    token_start = char_pos
                    token_end = char_pos + len(token)
                    
                    if token_start < end_char and token_end > start_char:
                        if bio_tags[i] == 'O':
                            if i > 0 and bio_tags[i-1].startswith(f'B-{label}'):
                                bio_tags[i] = f'I-{label}'
                            else:
                                bio_tags[i] = f'B-{label}'
                    
                    char_pos = token_end + 1
            
            return bio_tags
            
        except Exception as e:
            logger.error(f"Error in custom model prediction: {e}")
            tokens = text.split()
            return ['O'] * len(tokens)
    
    def load_test_dataset(self, test_path: str) -> List[Dict]:
        """Load test dataset from JSON file"""
        try:
            with open(test_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Test file {test_path} not found. Creating mock data.")
            return self._create_mock_test_data()
    
    def _create_mock_test_data(self) -> List[Dict]:
        """Create mock test data for demonstration"""
        return [
            {
                "text": "I have experience with Python programming and machine learning using TensorFlow.",
                "tokens": ["I", "have", "experience", "with", "Python", "programming", "and", "machine", "learning", "using", "TensorFlow."],
                "labels": ["O", "O", "O", "O", "B-SKILL", "I-SKILL", "O", "B-SKILL", "I-SKILL", "O", "B-SKILL"]
            },
            {
                "text": "Proficient in SQL database management and data analysis with Excel.",
                "tokens": ["Proficient", "in", "SQL", "database", "management", "and", "data", "analysis", "with", "Excel."],
                "labels": ["O", "O", "B-SKILL", "O", "O", "O", "B-SKILL", "I-SKILL", "O", "B-SKILL"]
            },
            {
                "text": "Strong communication skills and project management experience.",
                "tokens": ["Strong", "communication", "skills", "and", "project", "management", "experience."],
                "labels": ["O", "B-SKILL", "O", "O", "B-SKILL", "I-SKILL", "O"]
            }
        ]
    
    def run_ner_evaluation(self, test_dataset_path: str = None) -> Dict:
        """
        Main evaluation function
        Compares custom model vs baseline on test dataset
        """
        logger.info("Starting NER evaluation...")
        
        # Load test dataset
        if test_dataset_path:
            test_data = self.load_test_dataset(test_dataset_path)
        else:
            test_data = self._create_mock_test_data()
        
        # Collect predictions
        custom_predictions = []
        baseline_predictions = []
        ground_truth = []
        
        for item in test_data:
            text = item['text']
            true_labels = item['labels']
            
            # Get predictions from both models
            custom_pred = self._custom_model_predict(text)
            baseline_pred = self.baseline.baseline_ner(text)
            
            # Ensure all sequences have same length
            min_len = min(len(true_labels), len(custom_pred), len(baseline_pred))
            
            ground_truth.append(true_labels[:min_len])
            custom_predictions.append(custom_pred[:min_len])
            baseline_predictions.append(baseline_pred[:min_len])
        
        # Calculate metrics
        logger.info("Calculating evaluation metrics...")
        
        # Custom model metrics
        custom_f1 = f1_score(ground_truth, custom_predictions)
        custom_report = classification_report(ground_truth, custom_predictions, output_dict=True)
        
        # Baseline model metrics
        baseline_f1 = f1_score(ground_truth, baseline_predictions)
        baseline_report = classification_report(ground_truth, baseline_predictions, output_dict=True)
        
        # Calculate improvement
        improvement = ((custom_f1 - baseline_f1) / baseline_f1) * 100 if baseline_f1 > 0 else 0
        
        # Print results
        print("\n" + "="*60)
        print("NER MODEL EVALUATION RESULTS")
        print("="*60)
        
        print(f"\nCUSTOM MODEL F1-SCORE: {custom_f1:.4f}")
        print(f"BASELINE MODEL F1-SCORE: {baseline_f1:.4f}")
        print(f"IMPROVEMENT: {improvement:.2f}%")
        
        print(f"\n{'CUSTOM MODEL DETAILED REPORT':^60}")
        print("-"*60)
        print(classification_report(ground_truth, custom_predictions))
        
        print(f"\n{'BASELINE MODEL DETAILED REPORT':^60}")
        print("-"*60)
        print(classification_report(ground_truth, baseline_predictions))
        
        # Return results for further analysis
        return {
            'custom_f1': custom_f1,
            'baseline_f1': baseline_f1,
            'improvement_percent': improvement,
            'custom_report': custom_report,
            'baseline_report': baseline_report,
            'test_cases': len(test_data)
        }

def main():
    """Main execution function"""
    evaluator = NEREvaluator()
    
    # Run evaluation
    results = evaluator.run_ner_evaluation()
    
    # Save results
    results_path = Path("data/evaluation_results/ner_evaluation.json")
    results_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Evaluation results saved to {results_path}")
    
    return results

if __name__ == "__main__":
    main()
