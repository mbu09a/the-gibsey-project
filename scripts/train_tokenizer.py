#!/usr/bin/env python3
"""
Train a custom BPE tokenizer for the Gibsey Project.

This script:
1. Loads all 710 pages from the corpus
2. Extracts 16 character symbol IDs from the corpus index
3. Trains a SentencePiece BPE tokenizer with ~32k vocab
4. Includes special tokens for glyphs and QDPI roles
5. Outputs tokenizer files to tokenizer/ directory
"""

import json
import os
import re
from pathlib import Path
from typing import List, Dict, Any
import sentencepiece as spm

def load_corpus_pages(corpus_dir: Path) -> str:
    """Load all page content from the corpus into a single training text."""
    pages_dir = corpus_dir / 'pages'
    all_text = []
    
    print(f"Loading pages from {pages_dir}")
    
    # Get all markdown files
    md_files = sorted(pages_dir.glob('*.md'))
    print(f"Found {len(md_files)} markdown files")
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:  # Only add non-empty content
                    all_text.append(content)
        except Exception as e:
            print(f"Warning: Could not read {md_file}: {e}")
    
    # Join with double newlines to separate pages
    combined_text = '\n\n'.join(all_text)
    print(f"Total text length: {len(combined_text):,} characters")
    print(f"Total pages loaded: {len(all_text)}")
    
    return combined_text

def extract_character_symbols(corpus_dir: Path) -> List[str]:
    """Extract character symbol IDs from the corpus index."""
    index_path = corpus_dir / 'index.json'
    
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        
        # Extract symbol IDs from the index
        symbols = list(index_data.get('symbols', {}).keys())
        print(f"Found {len(symbols)} character symbols: {symbols}")
        return symbols
        
    except Exception as e:
        print(f"Warning: Could not load index.json: {e}")
        # Fallback: extract from character directory names
        chars_dir = corpus_dir / 'characters'
        if chars_dir.exists():
            symbols = [d.name for d in chars_dir.iterdir() if d.is_dir()]
            print(f"Fallback: Found {len(symbols)} character folders: {symbols}")
            return symbols
        else:
            print("No character symbols found")
            return []

def prepare_special_tokens(character_symbols: List[str]) -> List[str]:
    """Prepare the list of special tokens for training."""
    # QDPI role tokens
    qdpi_tokens = ["<X_READ>", "<Y_INDEX>", "<A_ASK>", "<Z_RECEIVE>"]
    
    # Character glyph tokens (symbol IDs)
    special_tokens = qdpi_tokens + character_symbols
    
    print(f"Special tokens ({len(special_tokens)} total):")
    print(f"  QDPI tokens: {qdpi_tokens}")
    print(f"  Character tokens: {character_symbols}")
    
    return special_tokens

def train_tokenizer(training_text: str, special_tokens: List[str], output_prefix: str):
    """Train the SentencePiece BPE tokenizer."""
    
    # Write training text to temporary file
    temp_file = f"{output_prefix}_training.txt"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(training_text)
    
    # Use the maximum allowed vocab size as reported by SentencePiece
    # The error shows max allowed is 31484, so we'll use that directly
    max_allowed_vocab = 31484
    effective_vocab_size = max_allowed_vocab
    
    print(f"Training SentencePiece tokenizer...")
    print(f"  Max allowed vocab size: {max_allowed_vocab}")
    print(f"  Special tokens: {len(special_tokens)}")
    print(f"  Training file: {temp_file}")
    
    # Train the tokenizer
    try:
        spm.SentencePieceTrainer.train(
            input=temp_file,
            model_prefix=output_prefix,
            vocab_size=effective_vocab_size,
            model_type='bpe',
            user_defined_symbols=special_tokens,
            normalization_rule_name='nfkc',  # Unicode normalization
            remove_extra_whitespaces=True,
            max_sentence_length=4192,  # Handle long sentences
            shuffle_input_sentence=True,
            character_coverage=0.9995,  # High coverage for custom text
            split_by_unicode_script=True,
            split_by_whitespace=True,
            split_by_number=True,
            split_digits=True,
            treat_whitespace_as_suffix=False,
            byte_fallback=True  # Handle unknown characters
        )
        
        print(f"✓ Training completed successfully")
        print(f"  Model: {output_prefix}.model")
        print(f"  Vocab: {output_prefix}.vocab")
        
        # Clean up temporary file
        os.remove(temp_file)
        
        # Test the tokenizer
        test_tokenizer(output_prefix, special_tokens)
        
    except Exception as e:
        print(f"Error during training: {e}")
        raise

def test_tokenizer(model_prefix: str, special_tokens: List[str]):
    """Test the trained tokenizer with some sample inputs."""
    
    print(f"\nTesting tokenizer...")
    
    # Load the trained tokenizer
    sp = spm.SentencePieceProcessor()
    sp.load(f"{model_prefix}.model")
    
    # Test cases
    test_cases = [
        "Hello, world!",
        "<X_READ>This is a test with QDPI tokens<Y_INDEX>",
        "The london-fox character appears in the story.",
        "jacklyn-variance is watching and analyzing.",
        "<A_ASK>What does the corpus contain?<Z_RECEIVE>",
        "Special characters: é, ñ, 中文, 🙂"
    ]
    
    print(f"Vocab size: {sp.get_piece_size()}")
    
    for test_text in test_cases:
        tokens = sp.encode(test_text, out_type=str)
        token_ids = sp.encode(test_text)
        
        print(f"\nInput: {test_text}")
        print(f"Tokens: {tokens}")
        print(f"Count: {len(tokens)}")
        
        # Check if special tokens are preserved
        for special_token in special_tokens:
            if special_token in test_text and special_token not in tokens:
                print(f"⚠️  Warning: Special token '{special_token}' was split!")
    
    print(f"\n✓ Tokenizer test completed")

def main():
    """Main execution function."""
    
    # Setup paths
    project_root = Path('/Users/ghostradongus/the-gibsey-project')
    corpus_dir = project_root / 'gibsey-canon' / 'corpus'
    tokenizer_dir = project_root / 'tokenizer'
    
    # Ensure tokenizer directory exists
    tokenizer_dir.mkdir(exist_ok=True)
    
    print("=== Training Gibsey Custom BPE Tokenizer ===")
    print(f"Project root: {project_root}")
    print(f"Corpus directory: {corpus_dir}")
    print(f"Output directory: {tokenizer_dir}")
    
    # Step 1: Load corpus text
    print(f"\n1. Loading corpus pages...")
    training_text = load_corpus_pages(corpus_dir)
    
    if not training_text.strip():
        raise ValueError("No training text found! Check corpus directory.")
    
    # Step 2: Extract character symbols
    print(f"\n2. Extracting character symbols...")
    character_symbols = extract_character_symbols(corpus_dir)
    
    # Step 3: Prepare special tokens
    print(f"\n3. Preparing special tokens...")
    special_tokens = prepare_special_tokens(character_symbols)
    
    # Step 4: Train tokenizer
    print(f"\n4. Training tokenizer...")
    output_prefix = str(tokenizer_dir / 'gibsey_bpe')
    train_tokenizer(training_text, special_tokens, output_prefix)
    
    print(f"\n=== Training Complete ===")
    print(f"Tokenizer files created:")
    print(f"  {output_prefix}.model")
    print(f"  {output_prefix}.vocab")
    print(f"\nNext steps:")
    print(f"  1. Convert to JSON for JavaScript usage")
    print(f"  2. Integrate into backend services")
    print(f"  3. Create CLI visualization tool")

if __name__ == '__main__':
    main()