import spacy
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SpacyPreprocessor:
    """
    A class for performing spaCy-based text preprocessing.
    Handles tokenization, lemmatization, POS tagging, and dependency parsing.
    """
    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Initializes the SpacyPreprocessor by loading the specified spaCy model.

        Args:
            model_name (str): The name of the spaCy model to load (e.g., "en_core_web_sm").
        """
        self.model_name = model_name
        self.nlp = None
        self._load_model()

    def _load_model(self):
        """
        Loads the spaCy model. If the model is not found, it attempts to download it.
        """
        try:
            self.nlp = spacy.load(self.model_name)
            logger.info(f"Loaded spaCy model: {self.model_name}")
        except OSError:
            logger.warning(f"spaCy model '{self.model_name}' not found. Attempting to download...")
            try:
                spacy.cli.download(self.model_name)
                self.nlp = spacy.load(self.model_name)
                logger.info(f"Successfully downloaded and loaded spaCy model: {self.model_name}")
            except Exception as e:
                logger.error(f"Could not download or load spaCy model '{self.model_name}': {e}")
                self.nlp = None # Ensure nlp is None if loading fails

    def preprocess_text(self, text: str) -> Dict[str, Any]:
        """
        Processes the input text using spaCy to extract tokens, lemmas, POS tags, and dependencies.

        Args:
            text (str): The input text to preprocess.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - 'tokens': List of tokens.
                - 'lemmas': List of lemmas.
                - 'pos_tags': List of Part-of-Speech tags.
                - 'dependencies': List of dependency relations.
                - 'doc': The full spaCy Doc object.
        """
        if not self.nlp:
            logger.error("spaCy model not loaded. Cannot preprocess text.")
            return {
                'tokens': text.split(),
                'lemmas': text.split(),
                'pos_tags': ['UNK'] * len(text.split()),
                'dependencies': ['UNK'] * len(text.split()),
                'doc': None
            }

        doc = self.nlp(text)
        tokens = [token.text for token in doc]
        lemmas = [token.lemma_ for token in doc]
        pos_tags = [token.pos_ for token in doc]
        dependencies = [token.dep_ for token in doc]

        return {
            'tokens': tokens,
            'lemmas': lemmas,
            'pos_tags': pos_tags,
            'dependencies': dependencies,
            'doc': doc
        }

if __name__ == "__main__":
    preprocessor = SpacyPreprocessor()
    sample_text = "I have experience with Python programming and machine learning using TensorFlow."
    processed_data = preprocessor.preprocess_text(sample_text)

    print("Tokens:", processed_data['tokens'])
    print("Lemmas:", processed_data['lemmas'])
    print("POS Tags:", processed_data['pos_tags'])
    print("Dependencies:", processed_data['dependencies'])

    sample_text_2 = "Proficient in SQL database management and data analysis with Excel."
    processed_data_2 = preprocessor.preprocess_text(sample_text_2)
    print("\nTokens 2:", processed_data_2['tokens'])
