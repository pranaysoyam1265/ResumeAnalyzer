"""
Step 3: Fine-Tuning for Named Entity Recognition (NER)
Fine-tunes the domain-adapted RoBERTa model for token classification
"""

import os
import logging
import pandas as pd
import numpy as np
from pathlib import Path
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    DataCollatorForTokenClassification,
    TrainingArguments,
    Trainer
)
from sklearn.metrics import classification_report
import seqeval.metrics as seqeval

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_annotated_data(csv_path):
    """
    Load annotated resume data and convert to NER format
    
    Args:
        csv_path (str): Path to annotated_resumes.csv
    
    Returns:
        Dataset: Hugging Face Dataset for token classification
    """
    df = pd.read_csv(csv_path)
    
    # Convert to token classification format
    examples = []
    
    for _, row in df.iterrows():
        # Parse the annotations (assuming format: "token1:LABEL1 token2:LABEL2 ...")
        tokens = []
        labels = []
        
        # Split text into tokens and extract labels from annotations
        text_tokens = row['text'].split()
        annotations = row['annotations'].split() if pd.notna(row['annotations']) else []
        
        # Create label mapping for tokens
        token_labels = {}
        for annotation in annotations:
            if ':' in annotation:
                token, label = annotation.split(':', 1)
                token_labels[token] = label
        
        # Assign labels to tokens
        for token in text_tokens:
            tokens.append(token)
            labels.append(token_labels.get(token, 'O'))  # 'O' for outside/no entity
        
        examples.append({
            'tokens': tokens,
            'ner_tags': labels
        })
    
    return Dataset.from_list(examples)

def create_label_mapping(dataset):
    """
    Create label to ID mapping from dataset
    
    Args:
        dataset: Dataset with ner_tags
    
    Returns:
        tuple: (label2id, id2label) dictionaries
    """
    all_labels = set()
    for example in dataset:
        all_labels.update(example['ner_tags'])
    
    # Sort labels to ensure consistent mapping
    sorted_labels = sorted(list(all_labels))
    
    label2id = {label: i for i, label in enumerate(sorted_labels)}
    id2label = {i: label for label, i in label2id.items()}
    
    logger.info(f"Found {len(sorted_labels)} unique labels: {sorted_labels}")
    
    return label2id, id2label

def augment_data(dataset, augmentation_factor=0.3):
    """
    Apply Label-wise Token Replacement (LwTR) data augmentation
    
    Args:
        dataset: Original dataset
        augmentation_factor: Fraction of data to augment
    
    Returns:
        Dataset: Augmented dataset
    """
    # Collect tokens by label
    label_tokens = {}
    for example in dataset:
        for token, label in zip(example['tokens'], example['ner_tags']):
            if label != 'O':  # Only augment named entities
                if label not in label_tokens:
                    label_tokens[label] = []
                label_tokens[label].append(token)
    
    # Remove duplicates
    for label in label_tokens:
        label_tokens[label] = list(set(label_tokens[label]))
    
    augmented_examples = []
    num_to_augment = int(len(dataset) * augmentation_factor)
    
    for i in range(num_to_augment):
        # Select random example
        original_idx = np.random.randint(0, len(dataset))
        original = dataset[original_idx]
        
        # Create augmented version
        new_tokens = original['tokens'].copy()
        new_labels = original['ner_tags'].copy()
        
        # Replace some entity tokens
        for j, (token, label) in enumerate(zip(new_tokens, new_labels)):
            if label != 'O' and label in label_tokens and len(label_tokens[label]) > 1:
                if np.random.random() < 0.3:  # 30% chance to replace
                    # Replace with random token of same label
                    replacement_options = [t for t in label_tokens[label] if t != token]
                    if replacement_options:
                        new_tokens[j] = np.random.choice(replacement_options)
        
        augmented_examples.append({
            'tokens': new_tokens,
            'ner_tags': new_labels
        })
    
    logger.info(f"Generated {len(augmented_examples)} augmented examples")
    
    # Combine original and augmented data
    all_examples = list(dataset) + augmented_examples
    return Dataset.from_list(all_examples)

def tokenize_and_align_labels(examples, tokenizer, label2id, label_all_tokens=False):
    """
    Tokenize and align labels for subword tokens
    
    Args:
        examples: Batch of examples
        tokenizer: Tokenizer
        label2id: Label to ID mapping
        label_all_tokens: Whether to label all subword tokens
    
    Returns:
        dict: Tokenized examples with aligned labels
    """
    tokenized_inputs = tokenizer(
        examples["tokens"],
        truncation=True,
        is_split_into_words=True,
        padding=False
    )
    
    labels = []
    for i, label in enumerate(examples["ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        
        for word_idx in word_ids:
            if word_idx is None:
                # Special tokens get -100
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                # First subword of a word gets the label
                label_ids.append(label2id[label[word_idx]])
            else:
                # Subsequent subwords get -100 or the same label
                label_ids.append(label2id[label[word_idx]] if label_all_tokens else -100)
            previous_word_idx = word_idx
        
        labels.append(label_ids)
    
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

def compute_metrics(eval_pred, id2label):
    """
    Compute entity-level metrics using seqeval
    
    Args:
        eval_pred: Predictions and labels
        id2label: ID to label mapping
    
    Returns:
        dict: Metrics dictionary
    """
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=2)
    
    # Remove ignored index (special tokens)
    true_predictions = [
        [id2label[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [id2label[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    
    results = {
        "precision": seqeval.precision_score(true_labels, true_predictions),
        "recall": seqeval.recall_score(true_labels, true_predictions),
        "f1": seqeval.f1_score(true_labels, true_predictions),
        "accuracy": seqeval.accuracy_score(true_labels, true_predictions),
    }
    
    return results

def main():
    """Main fine-tuning function"""
    
    # Configuration
    domain_adapted_model_path = "./domain_adapted_roberta"
    annotated_data_path = "project_data/annotated_resumes.csv"
    output_dir = "./ner_skill_extractor"
    
    logger.info("Starting NER fine-tuning...")
    
    # Step 1: Load annotated data
    logger.info("Loading annotated data...")
    if not os.path.exists(annotated_data_path):
        logger.error(f"Annotated data file not found: {annotated_data_path}")
        return
    
    dataset = load_annotated_data(annotated_data_path)
    logger.info(f"Loaded {len(dataset)} annotated examples")
    
    # Step 2: Create label mapping
    label2id, id2label = create_label_mapping(dataset)
    num_labels = len(label2id)
    
    # Step 3: Apply data augmentation
    logger.info("Applying data augmentation...")
    augmented_dataset = augment_data(dataset)
    logger.info(f"Total dataset size after augmentation: {len(augmented_dataset)}")
    
    # Step 4: Split dataset
    train_test_split = augmented_dataset.train_test_split(test_size=0.2, seed=42)
    train_dataset = train_test_split['train']
    eval_dataset = train_test_split['test']
    
    # Step 5: Load model and tokenizer
    logger.info(f"Loading domain-adapted model from {domain_adapted_model_path}")
    tokenizer = AutoTokenizer.from_pretrained(domain_adapted_model_path)
    model = AutoModelForTokenClassification.from_pretrained(
        domain_adapted_model_path,
        num_labels=num_labels,
        id2label=id2label,
        label2id=label2id
    )
    
    # Step 6: Tokenize datasets
    logger.info("Tokenizing datasets...")
    train_tokenized = train_dataset.map(
        lambda examples: tokenize_and_align_labels(examples, tokenizer, label2id),
        batched=True,
        remove_columns=train_dataset.column_names
    )
    
    eval_tokenized = eval_dataset.map(
        lambda examples: tokenize_and_align_labels(examples, tokenizer, label2id),
        batched=True,
        remove_columns=eval_dataset.column_names
    )
    
    # Step 7: Set up data collator
    data_collator = DataCollatorForTokenClassification(tokenizer)
    
    # Step 8: Configure training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        logging_dir=f"{output_dir}/logs",
        logging_steps=100,
        warmup_steps=500,
        fp16=True,
        dataloader_num_workers=4,
    )
    
    # Step 9: Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_tokenized,
        eval_dataset=eval_tokenized,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=lambda eval_pred: compute_metrics(eval_pred, id2label),
    )
    
    # Step 10: Start training
    logger.info("Starting fine-tuning...")
    trainer.train()
    
    # Step 11: Final evaluation
    logger.info("Running final evaluation...")
    eval_results = trainer.evaluate()
    logger.info(f"Final evaluation results: {eval_results}")
    
    # Step 12: Save the final model
    logger.info(f"Saving fine-tuned NER model to {output_dir}")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    logger.info("NER fine-tuning completed successfully!")

if __name__ == "__main__":
    main()
