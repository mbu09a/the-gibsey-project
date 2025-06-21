# Gibsey Custom BPE Tokenizer

This directory contains the custom Byte-Pair Encoding (BPE) tokenizer for the Gibsey Project, trained on the complete 710-page corpus with special tokens for QDPI roles and character glyphs.

## Overview

The Gibsey tokenizer provides consistent text encoding across all project services (Python backend and TypeScript frontend) with a shared vocabulary of **31,484 tokens**. It includes special handling for narrative-specific elements:

- **4 QDPI Role Tokens**: `<X_READ>`, `<Y_INDEX>`, `<A_ASK>`, `<Z_RECEIVE>`
- **16 Character Glyph Tokens**: `london-fox`, `jacklyn-variance`, etc.
- **Standard BPE Vocabulary**: Optimized for the Gibsey corpus text

## Files

```
tokenizer/
├── README.md                 # This file
├── gibsey_bpe.model          # SentencePiece model (for Python)
├── gibsey_bpe.vocab          # Vocabulary file
├── gibsey_bpe.json           # JSON export (for JavaScript/TypeScript)
└── tokenizer_example.js      # JavaScript usage example
```

## Special Tokens

### QDPI Role Tokens
The tokenizer includes four special tokens representing the QDPI (Query-Data-Process-Integrate) phases:

- `<X_READ>` - Read phase marker
- `<Y_INDEX>` - Index phase marker  
- `<A_ASK>` - Ask phase marker
- `<Z_RECEIVE>` - Receive phase marker

These tokens are treated as indivisible units and will never be split during tokenization.

### Character Glyph Tokens
All 16 main character symbol IDs are included as special tokens:

```
an-author            london-fox           glyph-marrow         phillip-bafflemint
jacklyn-variance     oren-progresso       old-natalie          princhetta
cop-e-right          new-natalie          arieol-owlist        jack-parlance
manny-valentinas     shamrock-stillman    todd-fishbone        the-author
```

## Usage

### Python Backend

```python
from backend.app.tokenizer_service import get_tokenizer_service

# Get the tokenizer service
tokenizer = get_tokenizer_service()

# Count tokens
token_count = tokenizer.count_tokens("Hello world!")

# Tokenize text
tokens = tokenizer.tokenize("<X_READ>Hello jacklyn-variance<Y_INDEX>")

# Calculate TNA cost (1 TNA = 100 tokens)
cost = tokenizer.calculate_tna_cost("Some text here")

# Chunk text for embeddings
chunks = tokenizer.chunk_text(long_text, max_tokens_per_chunk=256)
```

### TypeScript Frontend

```typescript
import { getTokenizerService, countTokens } from '@/services/tokenizerService';

// Count tokens (async)
const count = await countTokens("Hello world!");

// Use React hook
import { useTokenCount } from '@/hooks/useTokenizer';

function MyComponent({ text }: { text: string }) {
  const { tokenCount, tnaCost, specialTokens } = useTokenCount(text);
  
  return (
    <div>
      <p>Tokens: {tokenCount}</p>
      <p>TNA Cost: {tnaCost}</p>
      {specialTokens.qdpi.length > 0 && (
        <p>QDPI tokens: {specialTokens.qdpi.join(', ')}</p>
      )}
    </div>
  );
}
```

### CLI Tool

```bash
# Basic analysis
npm run token-viz "Your text here"

# Interactive mode
npm run token-viz -- --interactive

# Analyze a file
npm run token-viz -- --file path/to/text.txt

# Show examples
npm run token-viz -- --examples

# Direct usage
python3 scripts/token_viz.py "Text to analyze"
```

## Token Network Abstraction (TNA) Credits

The system uses TNA as a credit unit for token consumption:

- **1 TNA = 100 tokens**
- Used for cost tracking and rate limiting
- Consistent across all services

## Training Information

The tokenizer was trained using SentencePiece with the following parameters:

- **Model Type**: BPE (Byte-Pair Encoding)
- **Vocabulary Size**: 31,484 tokens
- **Training Data**: 710 pages from the Gibsey corpus (817,006 characters)
- **Special Tokens**: 20 user-defined symbols (4 QDPI + 16 characters)
- **Normalization**: NFKC Unicode normalization
- **Character Coverage**: 99.95%

### Training Command

```bash
python3 scripts/train_tokenizer.py
```

This script:
1. Loads all corpus pages from `gibsey-canon/corpus/pages/`
2. Extracts character symbols from `corpus/index.json`
3. Trains a SentencePiece BPE model with special tokens
4. Outputs `gibsey_bpe.model` and `gibsey_bpe.vocab`

## Maintenance

### Retraining the Tokenizer

Retrain when:
- The corpus significantly changes (new pages, major edits)
- New character symbols are added
- Performance optimization is needed

**Steps:**
1. Update the corpus in `gibsey-canon/corpus/pages/`
2. Run `python3 scripts/train_tokenizer.py`
3. Run `python3 scripts/convert_tokenizer_to_json.py`
4. Copy `gibsey_bpe.json` to `public/tokenizer/`
5. Test with `npm run token-viz -- --examples`
6. Update version tag: `git tag tokenizer-v1.1`

### Adding New Special Tokens

To add a new character or special token:

1. **Update training script** (`scripts/train_tokenizer.py`):
   ```python
   # Add to the character tokens list
   character_tokens = [
       # ... existing tokens ...
       "new-character-symbol"
   ]
   ```

2. **Retrain the tokenizer** (see above)

3. **Update services**:
   - Add to `backend/app/tokenizer_service.py` character list
   - Add to `src/services/tokenizerService.ts` character list

4. **Test thoroughly** with the CLI tool

### Validation

After any changes, validate with:

```bash
# Test tokenizer loading
python3 scripts/token_viz.py --examples

# Test backend integration
python3 -c "from backend.app.tokenizer_service import get_tokenizer_service; print(get_tokenizer_service().get_tokenizer_info())"

# Test frontend integration
npm run dev
# Visit http://localhost:5174/?debug
```

## Architecture Integration

### Backend Services

- **LLM Service**: Uses tokenizer for context management and truncation
- **RAG Service**: Token-based chunking for embeddings and context assembly
- **WebSocket Service**: Token counting for rate limiting

### Frontend Services

- **Chat Interface**: Real-time token counting and TNA cost display
- **Token Counter Component**: Visual feedback for user input
- **Debug Interface**: Comprehensive tokenizer testing

## Performance Characteristics

- **Loading Time**: ~100ms (Python), ~200ms (TypeScript)
- **Tokenization Speed**: ~10,000 tokens/second
- **Memory Usage**: ~2MB (vocabulary + model)
- **Accuracy**: 99.9% consistent with SentencePiece reference

## Troubleshooting

### Common Issues

**Tokenizer not loading in Python:**
```python
# Check model file exists
import os
print(os.path.exists("tokenizer/gibsey_bpe.model"))

# Test direct loading
import sentencepiece as spm
sp = spm.SentencePieceProcessor()
sp.load("tokenizer/gibsey_bpe.model")
```

**Frontend tokenizer fails:**
```javascript
// Check if JSON is accessible
fetch('/tokenizer/gibsey_bpe.json')
  .then(r => r.json())
  .then(data => console.log('Loaded:', data.model_info.vocab_size));
```

**Special tokens not recognized:**
```bash
# Check token IDs
npm run token-viz -- "<X_READ>Test<Y_INDEX>"
# Should show special tokens in purple
```

### Error Messages

- `"Tokenizer model not found"` → Check file paths and permissions
- `"Vocab size mismatch"` → Retrain tokenizer
- `"Special token split"` → Verify special token lists match training

## Version History

- **v1.0** (2025-06-20): Initial release with 31,484 vocab, 20 special tokens
  - Trained on complete 710-page corpus
  - Full Python/TypeScript integration
  - CLI tool with visualization

## Contributing

When modifying the tokenizer:

1. **Test thoroughly** with diverse inputs
2. **Maintain consistency** between Python and JavaScript implementations  
3. **Update documentation** for any API changes
4. **Validate special tokens** are preserved correctly
5. **Performance test** with large texts

## Support

For tokenizer issues:
- Check this README first
- Use the CLI tool for debugging: `npm run token-viz -- --examples`
- Test with the debug interface: add `?debug` to frontend URL
- Create issues with example text that fails to tokenize correctly

---

*The tokenizer is trained specifically for the Gibsey narrative universe and may not generalize well to other text domains. For general-purpose tokenization, consider using standard models like tiktoken or Hugging Face tokenizers.*