import pandas as pd
import spacy
from spacy.tokens import DocBin
import logging
from pathlib import Path
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NERTrainer:
    """
    NER Trainer for Resume Skill Gap Analyzer
    
    This class handles the preparation of training data, training of a custom spaCy NER model,
    and saving the trained model.
    """
    
    def __init__(self, data_path: str = "project_data/resumes/annotated_resumes.csv", 
                 output_dir: str = "models/ner_model", 
                 base_model: str = "en_core_web_lg"):
        """
        Initialize the NER Trainer.
        
        Args:
            data_path: Path to the annotated resumes CSV file.
            output_dir: Directory to save the trained NER model.
            base_model: Base spaCy model to use for training.
        """
        self.data_path = Path(data_path)
        self.output_dir = Path(output_dir)
        self.base_model = base_model
        self.nlp = None # To be loaded or created during training
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory created: {self.output_dir}")

    def _load_and_prepare_data(self) -> list:
        """
        Loads annotated data and converts it into spaCy training format.
        
        Returns:
            A list of (text, annotations) tuples for spaCy training.
        """
        logger.info(f"Loading annotated data from {self.data_path}...")
        if not self.data_path.exists():
            logger.error(f"Annotated data file not found: {self.data_path}")
            raise FileNotFoundError(f"Annotated data file not found: {self.data_path}")
        
        df = pd.read_csv(self.data_path)
        
        # Group annotations by resume_id
        grouped_annotations = df.groupby('resume_id').apply(lambda x: x.to_dict(orient='records'))
        
        training_data = []
        for resume_id, annotations in grouped_annotations.items():
            # Assuming 'content' is the raw text of the resume, which needs to be retrieved.
            # For now, we'll use a placeholder or assume it's available.
            # In a real scenario, you'd load the raw text from the corresponding .txt file.
            
            # For demonstration, let's assume we can reconstruct the text from annotations
            # or that the 'content' was stored somewhere.
            # Since data_collector.py saves raw text, we need to link it.
            # For now, I'll use the 'entity_text' to reconstruct a basic text for training.
            # This is a simplification and should be improved by loading actual raw resume text.
            
            # A better approach would be to load the raw text from project_data/resumes/raw_text/resume_id.txt
            # For now, let's use the first annotation's text as a proxy for the full resume text.
            
            raw_resume_text_path = Path("project_data/resumes/raw_text") / f"{resume_id}.txt"
            if not raw_resume_text_path.exists():
                logger.warning(f"Raw resume text not found for {resume_id}. Skipping.")
                continue
            
            with open(raw_resume_text_path, 'r', encoding='utf-8') as f:
                resume_text = f.read()

            entities = []
            for ann in annotations:
                start = ann['start_pos']
                end = ann['end_pos']
                label = ann['entity_label']
                
                # Ensure start and end positions are valid within the text
                if 0 <= start < len(resume_text) and 0 <= end <= len(resume_text) and start < end:
                    entities.append((start, end, label))
                else:
                    logger.warning(f"Invalid entity span for resume_id {resume_id}: ({start}, {end}, {label}) in text of length {len(resume_text)}")
            
            if entities: # Only add if there are valid entities
                training_data.append((resume_text, {"entities": entities}))
        
        logger.info(f"Prepared {len(training_data)} training examples.")
        return training_data

    def train_model(self, n_iter: int = 20, dropout: float = 0.5, eval_split: float = 0.2):
        """
        Trains a custom NER model using spaCy.
        
        Args:
            n_iter: Number of training iterations.
            dropout: Dropout rate for training.
            eval_split: Fraction of data to use for evaluation.
        """
        logger.info("Starting NER model training...")
        
        TRAIN_DATA = self._load_and_prepare_data()
        if not TRAIN_DATA:
            logger.error("No training data available. Aborting training.")
            return

        # Split data into training and evaluation sets
        random.shuffle(TRAIN_DATA)
        split_idx = int(len(TRAIN_DATA) * (1 - eval_split))
        train_set = TRAIN_DATA[:split_idx]
        dev_set = TRAIN_DATA[split_idx:]
        
        logger.info(f"Training with {len(train_set)} examples, evaluating with {len(dev_set)} examples.")

        # Initialize spaCy model
        try:
            self.nlp = spacy.load(self.base_model)
            logger.info(f"Loaded base model: {self.base_model}")
        except OSError:
            logger.warning(f"Base model '{self.base_model}' not found. Downloading and installing...")
            spacy.cli.download(self.base_model)
            self.nlp = spacy.load(self.base_model)
            logger.info(f"Downloaded and loaded base model: {self.base_model}")

        if "ner" not in self.nlp.pipe_names:
            ner = self.nlp.add_pipe("ner", last=True)
        else:
            ner = self.nlp.get_pipe("ner")

        # Add labels to the NER pipe
        for _, annotations in TRAIN_DATA:
            for ent in annotations.get("entities", []):
                ner.add_label(ent[2]) # ent[2] is the label

        # Prepare DocBin for efficient training
        train_docbin = DocBin(attrs=["ORTH", "SPACY", "TAG", "LEMMA", "POS", "DEP", "ENT_IOB", "ENT_TYPE"])
        for text, annotations in train_set:
            try:
                doc = self.nlp.make_doc(text)
                ents = []
                for start, end, label in annotations["entities"]:
                    span = doc.char_span(start, end, label=label)
                    if span is not None:
                        ents.append(span)
                    else:
                        logger.warning(f"Skipping entity: ({start}, {end}, {label}) for text: {text[:50]}...")
                doc.ents = ents
                train_docbin.add(doc)
            except Exception as e:
                logger.error(f"Error processing training example: {e} for text: {text[:50]}...")
        train_docbin.to_disk(self.output_dir / "train.spacy")

        dev_docbin = DocBin(attrs=["ORTH", "SPACY", "TAG", "LEMMA", "POS", "DEP", "ENT_IOB", "ENT_TYPE"])
        for text, annotations in dev_set:
            try:
                doc = self.nlp.make_doc(text)
                ents = []
                for start, end, label in annotations["entities"]:
                    span = doc.char_span(start, end, label=label)
                    if span is not None:
                        ents.append(span)
                    else:
                        logger.warning(f"Skipping entity: ({start}, {end}, {label}) for text: {text[:50]}...")
                doc.ents = ents
                dev_docbin.add(doc)
            except Exception as e:
                logger.error(f"Error processing dev example: {e} for text: {text[:50]}...")
        dev_docbin.to_disk(self.output_dir / "dev.spacy")

        # Train the model
        logger.info("Training spaCy NER model...")
        # This part typically involves running `spacy train` from the command line
        # For programmatic training, we'd use nlp.begin_training() and update()
        # However, for simplicity and to leverage spaCy's config system,
        # we'll generate a config file and instruct the user to run `spacy train`.
        
        config_content = f"""
[paths]
train = "{self.output_dir / "train.spacy"}"
dev = "{self.output_dir / "dev.spacy"}"
vectors = null
init_tok2vec = null

[system]
gpu_id = -1
seed = 0

[nlp]
lang = "en"
pipeline = ["tok2vec", "ner"]
batch_size = 1000

[components]

[components.tok2vec]
factory = "tok2vec"

[components.ner]
factory = "ner"
overwrite_ents = true

[components.ner.model]
@architectures = "spacy.TransitionBasedParser.v2"
state_type = "ner"
extra_annotation_attributes = ["LEMMA", "POS", "DEP"]
hidden_width = 64
maxout_pieces = 2
use_upper = true
n_iter = {n_iter}
dropout = {dropout}

[corpora]

[corpora.train]
@readers = "spacy.Corpus.v1"
path = ${paths.train}
gold_pretokenize = false

[corpora.dev]
@readers = "spacy.Corpus.v1"
path = ${paths.dev}
gold_pretokenize = false

[training]
logger = {{"@loggers":"spacy.ConsoleLogger.v1"}}
dropout = {dropout}
optimizer = {{"@optimizers":"Adam.v1"}}
max_epochs = {n_iter}
"""
        config_path = self.output_dir / "config.cfg"
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_content)
        
        logger.info(f"Generated spaCy config file at: {config_path}")
        logger.info(f"To train the model, run the following command in your terminal:")
        logger.info(f"  python -m spacy train {config_path} --output {self.output_dir} --paths.train {self.output_dir / 'train.spacy'} --paths.dev {self.output_dir / 'dev.spacy'}")
        logger.info(f"The trained model will be saved to: {self.output_dir}/model-best")

    def evaluate_model(self, model_path: str = None):
        """
        Evaluates the trained NER model.
        
        Args:
            model_path: Path to the trained model. If None, uses the model trained by this instance.
        """
        if model_path:
            nlp_eval = spacy.load(model_path)
        elif self.nlp:
            nlp_eval = self.nlp
        else:
            logger.error("No model to evaluate. Please train a model first or provide a model_path.")
            return

        logger.info("Evaluating NER model...")
        # This part would typically involve loading the dev.spacy and running nlp.evaluate()
        # For now, we'll provide instructions for command-line evaluation.
        logger.info(f"To evaluate the trained model, run the following command in your terminal:")
        logger.info(f"  python -m spacy evaluate {self.output_dir}/model-best {self.output_dir}/dev.spacy")

def main():
    """Main execution function."""
    print("=" * 60)
    print("RESUME SKILL GAP ANALYZER - NER MODEL TRAINING")
    print("=" * 60)
    
    try:
        trainer = NERTrainer()
        trainer.train_model()
        trainer.evaluate_model() # Instructions for evaluation
        
        print("\n" + "=" * 60)
        print("NER MODEL TRAINING SETUP COMPLETED. PLEASE RUN THE SPACY COMMANDS MANUALLY TO TRAIN AND EVALUATE.")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"NER model training failed: {e}")
        print(f"\n❌ Error: {e}")
        print("\nPlease ensure:")
        print("1. Annotated data is available at project_data/resumes/annotated_resumes.csv")
        print("2. Raw resume texts are available in project_data/resumes/raw_text/")
        print("3. All necessary Python packages are installed (check scripts/ner_trainer_requirements.txt)")

if __name__ == "__main__":
    main()
