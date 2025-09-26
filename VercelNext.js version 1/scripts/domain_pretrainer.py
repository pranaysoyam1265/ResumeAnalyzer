"""
Step 2: Domain-Adaptive Pre-training of RoBERTa
Adapts a general pre-trained RoBERTa model to the HR/recruitment domain
"""

import os
import logging
from pathlib import Path
from datasets import Dataset, concatenate_datasets
from transformers import (
    RobertaTokenizer, 
    RobertaForMaskedLM,
    DataCollatorForLanguageModeling,
    TrainingArguments,
    Trainer
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_domain_corpus(directories):
    """
    Load all .txt files from specified directories into a single Dataset
    
    Args:
        directories (list): List of directory paths containing .txt files
    
    Returns:
        Dataset: Hugging Face Dataset with 'text' column
    """
    all_texts = []
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            logger.warning(f"Directory {directory} does not exist, skipping...")
            continue
            
        txt_files = list(dir_path.glob("*.txt"))
        logger.info(f"Found {len(txt_files)} .txt files in {directory}")
        
        for txt_file in txt_files:
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                    # Filter out excessively long or short documents
                    if 50 <= len(content) <= 10000:  # Character count limits
                        all_texts.append(content)
                    else:
                        logger.debug(f"Skipping {txt_file.name}: length {len(content)}")
                        
            except Exception as e:
                logger.error(f"Error reading {txt_file}: {e}")
                continue
    
    logger.info(f"Loaded {len(all_texts)} valid documents")
    
    # Create Dataset
    dataset = Dataset.from_dict({"text": all_texts})
    return dataset

def tokenize_function(examples, tokenizer, block_size=512):
    """
    Tokenize and chunk text for masked language modeling
    
    Args:
        examples: Batch of examples from dataset
        tokenizer: RoBERTa tokenizer
        block_size: Maximum sequence length
    
    Returns:
        dict: Tokenized and chunked examples
    """
    # Tokenize all texts
    tokenized = tokenizer(examples["text"], truncation=False, padding=False)
    
    # Concatenate all tokenized texts
    concatenated_examples = {k: sum(tokenized[k], []) for k in tokenized.keys()}
    total_length = len(concatenated_examples[list(concatenated_examples.keys())[0]])
    
    # Split into chunks of block_size
    result = {
        k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
        for k, t in concatenated_examples.items()
    }
    
    # Remove the last chunk if it's too short
    if len(result["input_ids"][-1]) < block_size:
        for k in result.keys():
            result[k] = result[k][:-1]
    
    return result

def main():
    """Main training function"""
    
    # Configuration
    model_name = "roberta-base"
    output_dir = "./domain_adapted_roberta"
    block_size = 512
    
    # Data directories
    data_directories = [
        'project_data/resumes/raw_text/',
        'project_data/job_descriptions/'
    ]
    
    logger.info("Starting domain-adaptive pre-training...")
    
    # Step 1: Load domain corpus
    logger.info("Loading domain corpus...")
    dataset = load_domain_corpus(data_directories)
    
    if len(dataset) == 0:
        logger.error("No data loaded! Check your data directories.")
        return
    
    # Step 2: Load tokenizer and model
    logger.info(f"Loading {model_name} tokenizer and model...")
    tokenizer = RobertaTokenizer.from_pretrained(model_name)
    model = RobertaForMaskedLM.from_pretrained(model_name)
    
    # Step 3: Tokenize dataset
    logger.info("Tokenizing dataset...")
    tokenized_dataset = dataset.map(
        lambda examples: tokenize_function(examples, tokenizer, block_size),
        batched=True,
        remove_columns=dataset.column_names,
        desc="Tokenizing"
    )
    
    logger.info(f"Tokenized dataset size: {len(tokenized_dataset)}")
    
    # Step 4: Set up data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=True,
        mlm_probability=0.15
    )
    
    # Step 5: Configure training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=1,
        per_device_train_batch_size=8,
        gradient_accumulation_steps=2,
        save_steps=10_000,
        save_total_limit=2,
        prediction_loss_only=True,
        logging_dir=f"{output_dir}/logs",
        logging_steps=500,
        warmup_steps=1000,
        learning_rate=5e-5,
        weight_decay=0.01,
        fp16=True,  # Enable mixed precision for faster training
        dataloader_num_workers=4,
        remove_unused_columns=False,
    )
    
    # Step 6: Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=tokenized_dataset,
    )
    
    # Step 7: Start training
    logger.info("Starting training...")
    trainer.train()
    
    # Step 8: Save the final model
    logger.info(f"Saving domain-adapted model to {output_dir}")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    logger.info("Domain-adaptive pre-training completed successfully!")

if __name__ == "__main__":
    main()
