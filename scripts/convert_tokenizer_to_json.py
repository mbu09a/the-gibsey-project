#!/usr/bin/env python3
"""
Convert the trained SentencePiece tokenizer to JSON format for JavaScript usage.

This script:
1. Loads the trained gibsey_bpe.model file
2. Extracts vocabulary and configuration 
3. Creates a JSON format that can be used in JavaScript/Bun
"""

import json
from pathlib import Path
import sentencepiece as spm

def create_vocab_export(model_path: str, output_path: str):
    """Create a vocabulary export that can be used to reconstruct the tokenizer in JS."""
    
    print(f"Loading SentencePiece model: {model_path}")
    
    # Load the SentencePiece model
    sp = spm.SentencePieceProcessor()
    sp.load(model_path)
    
    print(f"Model loaded successfully")
    print(f"  Vocab size: {sp.get_piece_size()}")
    print(f"  Model type: BPE")
    
    # Extract all pieces and their IDs
    pieces = []
    special_tokens = []
    
    for i in range(sp.get_piece_size()):
        piece = sp.id_to_piece(i)
        score = sp.get_score(i)
        is_control = sp.is_control(i)
        is_unknown = sp.is_unknown(i)
        is_unused = sp.is_unused(i)
        
        piece_info = {
            "id": i,
            "piece": piece,
            "score": score,
            "type": "normal"
        }
        
        # Categorize special tokens
        if is_control or piece in ["<unk>", "<s>", "</s>", "<pad>"]:
            piece_info["type"] = "control"
        elif piece in ["<X_READ>", "<Y_INDEX>", "<A_ASK>", "<Z_RECEIVE>"]:
            piece_info["type"] = "qdpi"
            special_tokens.append(piece)
        elif piece in ["an-author", "london-fox", "glyph-marrow", "phillip-bafflemint",
                      "jacklyn-variance", "oren-progresso", "old-natalie", "princhetta", 
                      "cop-e-right", "new-natalie", "arieol-owlist", "jack-parlance",
                      "manny-valentinas", "shamrock-stillman", "todd-fishbone", "the-author"]:
            piece_info["type"] = "character"
            special_tokens.append(piece)
        elif piece.startswith("<0x") and piece.endswith(">"):
            piece_info["type"] = "byte"
        
        pieces.append(piece_info)
    
    print(f"Extracted {len(pieces)} pieces")
    print(f"Found {len(special_tokens)} special tokens")
    
    # Create export format optimized for JavaScript usage
    export_data = {
        "version": "1.0",
        "type": "SentencePiece_BPE",
        "model_info": {
            "vocab_size": sp.get_piece_size(),
            "model_type": "BPE",
            "unk_id": sp.unk_id(),
            "bos_id": sp.bos_id(),
            "eos_id": sp.eos_id(),
            "pad_id": sp.pad_id() if hasattr(sp, 'pad_id') else -1
        },
        "special_tokens": {
            "unk_token": "<unk>",
            "bos_token": "<s>",
            "eos_token": "</s>",
            "pad_token": "<pad>",
            "qdpi_tokens": ["<X_READ>", "<Y_INDEX>", "<A_ASK>", "<Z_RECEIVE>"],
            "character_tokens": [
                "an-author", "london-fox", "glyph-marrow", "phillip-bafflemint",
                "jacklyn-variance", "oren-progresso", "old-natalie", "princhetta",
                "cop-e-right", "new-natalie", "arieol-owlist", "jack-parlance",
                "manny-valentinas", "shamrock-stillman", "todd-fishbone", "the-author"
            ]
        },
        "vocab": {piece["piece"]: piece["id"] for piece in pieces},
        "pieces": pieces
    }
    
    # Save the JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Vocabulary export saved to: {output_path}")
    
    # Create a simple usage example
    create_usage_example(output_path, sp)
    
    return export_data

def create_usage_example(json_path: str, sp):
    """Create a simple example showing how to use the exported vocab in JavaScript."""
    
    example_js = '''
// Example usage of Gibsey BPE tokenizer in JavaScript/Bun
// Load the exported vocabulary
import fs from 'fs';
import { Tokenizer } from '@huggingface/tokenizers';

// For now, we'll use the SentencePiece model directly
// This example shows the expected interface

class GibseyTokenizer {
    constructor(vocabPath) {
        const vocabData = JSON.parse(fs.readFileSync(vocabPath, 'utf-8'));
        this.vocab = vocabData.vocab;
        this.pieces = vocabData.pieces;
        this.specialTokens = vocabData.special_tokens;
        this.modelInfo = vocabData.model_info;
    }
    
    // Basic tokenization (simplified - real implementation would need SentencePiece logic)
    tokenize(text) {
        // This is a placeholder - real BPE tokenization is complex
        // For production, use the SentencePiece model file with a WASM wrapper
        console.log(`Tokenizing: "${text}"`);
        console.log(`Vocab size: ${Object.keys(this.vocab).length}`);
        console.log(`Special tokens: ${this.specialTokens.qdpi_tokens.join(', ')}`);
        return text.split(' '); // Placeholder
    }
    
    countTokens(text) {
        return this.tokenize(text).length;
    }
    
    getTNACost(text, tokensPerTNA = 100) {
        const tokenCount = this.countTokens(text);
        return tokenCount / tokensPerTNA;
    }
}

// Usage
const tokenizer = new GibseyTokenizer('./gibsey_bpe.json');
console.log(tokenizer.tokenize('<X_READ>Hello jacklyn-variance<Y_INDEX>'));
console.log('TNA cost:', tokenizer.getTNACost('Some sample text'));
'''
    
    example_path = Path(json_path).parent / 'tokenizer_example.js'
    with open(example_path, 'w', encoding='utf-8') as f:
        f.write(example_js)
    
    print(f"✓ Usage example saved to: {example_path}")

def test_export(json_path: str, original_sp):
    """Test that the exported data is correct."""
    
    print(f"\nTesting exported data...")
    
    # Load the exported JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        export_data = json.load(f)
    
    # Verify vocab completeness
    expected_vocab_size = original_sp.get_piece_size()
    actual_vocab_size = len(export_data['vocab'])
    
    print(f"Vocab size check: {actual_vocab_size}/{expected_vocab_size} {'✓' if actual_vocab_size == expected_vocab_size else '✗'}")
    
    # Test special tokens are present
    special_checks = []
    for token_type, tokens in export_data['special_tokens'].items():
        if isinstance(tokens, list):
            for token in tokens:
                if token in export_data['vocab']:
                    special_checks.append(f"✓ {token}")
                else:
                    special_checks.append(f"✗ {token} MISSING")
        elif tokens in export_data['vocab']:
            special_checks.append(f"✓ {tokens}")
        else:
            special_checks.append(f"✗ {tokens} MISSING")
    
    print(f"Special tokens check:")
    for check in special_checks[:10]:  # Show first 10
        print(f"  {check}")
    if len(special_checks) > 10:
        print(f"  ... and {len(special_checks) - 10} more")
    
    # Test a few token encodings
    test_cases = [
        "Hello",
        "<X_READ>",
        "london-fox",
        "jacklyn-variance"
    ]
    
    print(f"\nToken ID verification:")
    for test_token in test_cases:
        original_ids = original_sp.piece_to_id(test_token)
        exported_id = export_data['vocab'].get(test_token, None)
        
        if exported_id == original_ids:
            print(f"  ✓ {test_token}: {exported_id}")
        else:
            print(f"  ✗ {test_token}: expected {original_ids}, got {exported_id}")
    
    print(f"\n✓ Export validation complete")

def main():
    """Main execution function."""
    
    # Setup paths
    project_root = Path('/Users/ghostradongus/the-gibsey-project')
    tokenizer_dir = project_root / 'tokenizer'
    model_path = tokenizer_dir / 'gibsey_bpe.model'
    json_path = tokenizer_dir / 'gibsey_bpe.json'
    
    print("=== Converting SentencePiece to JSON ===")
    print(f"Input model: {model_path}")
    print(f"Output JSON: {json_path}")
    
    if not model_path.exists():
        raise FileNotFoundError(f"SentencePiece model not found: {model_path}")
    
    # Load the original model for testing
    sp = spm.SentencePieceProcessor()
    sp.load(str(model_path))
    
    # Create the vocabulary export
    export_data = create_vocab_export(str(model_path), str(json_path))
    
    # Test the export
    test_export(str(json_path), sp)
    
    print(f"\n=== Conversion Complete ===")
    print(f"The tokenizer is now available in both formats:")
    print(f"  Python (SentencePiece): {model_path}")
    print(f"  JavaScript (JSON): {json_path}")
    print(f"\nNext steps:")
    print(f"  1. Install @huggingface/tokenizers or sentencepiece-wasm in Bun project")
    print(f"  2. Integrate JSON vocab into TypeScript frontend")
    print(f"  3. Create CLI visualization tool")
    print(f"\nNote: For full BPE functionality in JavaScript, consider using:")
    print(f"  - @huggingface/tokenizers with the original .model file")
    print(f"  - sentencepiece-wasm package")
    print(f"  - The JSON export provides vocab lookup and special token detection")

if __name__ == '__main__':
    main()