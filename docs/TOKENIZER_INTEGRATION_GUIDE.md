# Gibsey Custom Tokenizer Integration Guide

This document provides a comprehensive guide to the custom BPE tokenizer implementation in the Gibsey Project, covering training, integration, usage, and maintenance across all system components.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Training Process](#training-process)
4. [Backend Integration](#backend-integration)
5. [Frontend Integration](#frontend-integration)
6. [CLI Tools](#cli-tools)
7. [API Reference](#api-reference)
8. [Maintenance Procedures](#maintenance-procedures)
9. [Performance Optimization](#performance-optimization)
10. [Troubleshooting](#troubleshooting)

## Overview

The Gibsey Project uses a custom Byte-Pair Encoding (BPE) tokenizer to ensure consistent text processing across all services. This tokenizer is specifically trained on the 710-page Gibsey corpus and includes special tokens for narrative elements.

### Key Features

- **Corpus-Specific Vocabulary**: 31,484 tokens optimized for Gibsey text
- **Special Token Support**: QDPI roles and character glyphs preserved as single tokens
- **Cross-Platform Consistency**: Same tokenization in Python backend and TypeScript frontend
- **TNA Credit System**: Token Network Abstraction for usage tracking
- **Real-Time Analysis**: CLI and UI tools for token visualization

### Special Tokens

#### QDPI Role Markers
```
<X_READ>    - Query/Read phase
<Y_INDEX>   - Data/Index phase  
<A_ASK>     - Process/Ask phase
<Z_RECEIVE> - Integrate/Receive phase
```

#### Character Glyph Tokens
```
an-author            london-fox           glyph-marrow         phillip-bafflemint
jacklyn-variance     oren-progresso       old-natalie          princhetta
cop-e-right          new-natalie          arieol-owlist        jack-parlance
manny-valentinas     shamrock-stillman    todd-fishbone        the-author
```

## Architecture

### System Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Training      │    │   Python        │    │   TypeScript    │
│   Pipeline      │───▶│   Backend       │    │   Frontend      │
│                 │    │                 │    │                 │
│ SentencePiece   │    │ tokenizer_      │    │ tokenizerService│
│ BPE Training    │    │ service.py      │    │ .ts             │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Tokenizer     │    │   RAG Service   │    │   Chat UI       │
│   Files         │    │   LLM Service   │    │   Token Counter │
│                 │    │   Context Mgmt  │    │   Debug Tools   │
│ .model .vocab   │    │                 │    │                 │
│ .json           │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow

1. **Training**: Corpus text → SentencePiece → BPE model + vocab
2. **Export**: BPE model → JSON format for JavaScript
3. **Backend**: Model loading → Token counting → Context management
4. **Frontend**: JSON loading → UI feedback → User guidance
5. **CLI**: Direct model access → Analysis → Visualization

## Training Process

### Prerequisites

```bash
pip install sentencepiece transformers tokenizers
```

### Training Script

The tokenizer is trained using `scripts/train_tokenizer.py`:

```python
# Key training parameters
trainer_spec = {
    'model_type': 'BPE',
    'vocab_size': 31484,  # Max allowed by SentencePiece
    'character_coverage': 0.9995,
    'normalization_rule_name': 'nfkc',
    'user_defined_symbols': special_tokens,
    'byte_fallback': True
}
```

### Training Data

- **Source**: `gibsey-canon/corpus/pages/*.md` (710 files)
- **Size**: 817,006 characters, 5,419 sentences
- **Processing**: Unicode normalization, whitespace handling
- **Quality**: 99.95% character coverage

### Execution

```bash
# Train the tokenizer
python3 scripts/train_tokenizer.py

# Convert to JSON for frontend
python3 scripts/convert_tokenizer_to_json.py

# Copy to public directory
cp tokenizer/gibsey_bpe.json public/tokenizer/
```

## Backend Integration

### Service Architecture

```python
# backend/app/tokenizer_service.py
class GibseyTokenizerService:
    def __init__(self, model_path: str = None)
    def count_tokens(self, text: str) -> int
    def tokenize(self, text: str) -> List[str]
    def chunk_text(self, text: str, max_tokens: int) -> List[str]
    def calculate_tna_cost(self, text: str) -> float
    def has_special_tokens(self, text: str) -> Dict[str, List[str]]
```

### LLM Service Integration

```python
# backend/app/llm_service.py
class LLMService:
    def __init__(self):
        # Prefers Gibsey tokenizer over tiktoken
        self.gibsey_tokenizer = get_tokenizer_service()
        self.use_gibsey_tokenizer = True
    
    def count_tokens(self, text: str) -> int:
        if self.use_gibsey_tokenizer:
            return self.gibsey_tokenizer.count_tokens(text)
        # Fallback to tiktoken
```

### RAG Service Integration

```python
# backend/app/rag_service.py  
class RAGService:
    def build_context(self, query: str, character_id: str):
        # Uses custom tokenizer for context limits
        total_tokens = self.llm_service.count_tokens(content)
        if total_tokens > self.max_context_tokens:
            # Token-aware truncation
            context = self.llm_service.truncate_to_tokens(
                context, available_tokens
            )
```

### Usage Examples

```python
from backend.app.tokenizer_service import get_tokenizer_service

tokenizer = get_tokenizer_service()

# Basic tokenization
text = "<X_READ>Hello jacklyn-variance<Y_INDEX>"
tokens = tokenizer.tokenize(text)
# Result: ['▁', '<X_READ>', 'Hello', '▁', 'jacklyn-variance', '<Y_INDEX>']

# Token counting
count = tokenizer.count_tokens(text)
# Result: 6

# TNA cost calculation  
cost = tokenizer.calculate_tna_cost(text)
# Result: 0.06 (6 tokens / 100 tokens per TNA)

# Text chunking for embeddings
chunks = tokenizer.chunk_text(long_text, max_tokens_per_chunk=256)

# Special token detection
special = tokenizer.has_special_tokens(text)
# Result: {'qdpi': ['<X_READ>', '<Y_INDEX>'], 'character': ['jacklyn-variance']}
```

## Frontend Integration

### Service Architecture

```typescript
// src/services/tokenizerService.ts
export class GibseyTokenizerService {
  private async loadTokenizer(): Promise<void>
  async countTokens(text: string): Promise<number>
  async detectSpecialTokens(text: string): Promise<SpecialTokens>
  async calculateTNACost(text: string): Promise<number>
  async wouldExceedLimit(text: string, maxTokens: number): Promise<boolean>
}
```

### React Integration

```typescript
// src/hooks/useTokenizer.ts
export function useTokenizer() {
  return {
    loading, loaded, info,
    countTokens, calculateTNACost, 
    detectSpecialTokens, wouldExceedLimit
  };
}

export function useTokenCount(text: string) {
  return { tokenCount, tnaCost, specialTokens, calculating };
}
```

### UI Components

```typescript
// src/components/TokenCounter.tsx
<TokenCounter 
  text={inputText}
  maxTokens={500}
  showDetails={true}
/>

<InlineTokenCount text={text} />

<TNACostBadge text={text} />
```

### Chat Interface Integration

```typescript
// src/components/ChatInterface.tsx
{inputValue.trim() && (
  <div className="mt-2 opacity-70">
    <TokenCounter 
      text={inputValue}
      maxTokens={500}
      showDetails={true}
      className="text-xs"
    />
  </div>
)}
```

### Debug Interface

Access via `http://localhost:5174/?debug` to test:
- Tokenizer loading status
- Token counting accuracy
- Special token detection
- Performance characteristics

## CLI Tools

### Token Visualization Tool

```bash
# Basic analysis
npm run token-viz "Your text here"

# Interactive mode
npm run token-viz -- --interactive

# File analysis
npm run token-viz -- --file corpus/pages/001-an-authors-preface.md

# Examples and help
npm run token-viz -- --examples
npm run token-viz -- --help
```

### Features

- **Colored Output**: QDPI tokens (purple), character tokens (blue)
- **Detailed Breakdown**: Token-by-token visualization
- **Special Token Detection**: Automatic identification
- **TNA Cost Calculation**: Real-time cost estimation
- **Interactive Mode**: Continuous analysis loop

### Example Output

```
============================================================
GIBSEY TOKEN ANALYSIS
============================================================

INPUT TEXT:
"<X_READ>Hello jacklyn-variance, what do you see?<Y_INDEX>"

BASIC METRICS:
  Characters: 57
  Tokens:     12
  TNA Cost:   0.1200
  Ratio:      4.75 chars/token

SPECIAL TOKENS DETECTED:
  QDPI:       <X_READ>, <Y_INDEX>
  Characters: jacklyn-variance

TOKEN BREAKDOWN:
    1- 10: ▁ <X_READ> Hello ▁ jacklyn-variance , ▁what ▁do ▁you ▁see
   11- 12: ? <Y_INDEX>
```

## API Reference

### Python Backend API

#### GibseyTokenizerService

```python
class GibseyTokenizerService:
    def count_tokens(self, text: str) -> int:
        """Count tokens using custom tokenizer."""
        
    def encode(self, text: str) -> List[int]:
        """Encode text to token IDs."""
        
    def decode(self, token_ids: List[int]) -> str:
        """Decode token IDs back to text."""
        
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into string pieces."""
        
    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to maximum tokens."""
        
    def chunk_text(self, text: str, max_tokens_per_chunk: int, 
                   overlap_tokens: int = 0) -> List[str]:
        """Split text into token-based chunks."""
        
    def calculate_tna_cost(self, text: str) -> float:
        """Calculate TNA cost (tokens / 100)."""
        
    def has_special_tokens(self, text: str) -> Dict[str, List[str]]:
        """Detect QDPI and character tokens."""
        
    def get_tokenizer_info(self) -> Dict[str, Any]:
        """Get tokenizer metadata."""
```

#### Convenience Functions

```python
from backend.app.tokenizer_service import (
    count_tokens, truncate_to_tokens, 
    chunk_text, calculate_tna_cost
)

# Direct usage without service instance
tokens = count_tokens("Hello world")
truncated = truncate_to_tokens(long_text, 100)
chunks = chunk_text(text, 256, overlap_tokens=20)
cost = calculate_tna_cost(text)
```

### TypeScript Frontend API

#### Service Methods

```typescript
interface GibseyTokenizerService {
  countTokens(text: string): Promise<number>;
  detectSpecialTokens(text: string): Promise<SpecialTokens>;
  calculateTNACost(text: string): Promise<number>;
  wouldExceedLimit(text: string, maxTokens: number): Promise<boolean>;
  truncateToApproxTokens(text: string, maxTokens: number): Promise<string>;
  getInfo(): Promise<TokenizerInfo>;
}
```

#### React Hooks

```typescript
// Basic tokenizer access
const { loading, loaded, info, countTokens } = useTokenizer();

// Real-time token counting
const { tokenCount, tnaCost, specialTokens, calculating } = useTokenCount(text);
```

#### Component Props

```typescript
interface TokenCounterProps {
  text: string;
  maxTokens?: number;
  showDetails?: boolean;
  className?: string;
}
```

## Maintenance Procedures

### Regular Maintenance

#### Monthly Checks
1. Verify tokenizer loading in all environments
2. Run CLI examples to test functionality
3. Check token count accuracy against known samples
4. Monitor performance metrics

#### Quarterly Reviews
1. Analyze corpus changes since last training
2. Evaluate tokenizer performance on new content
3. Review special token usage patterns
4. Consider vocabulary optimization

### Updating the Corpus

When the corpus changes significantly:

1. **Assess Impact**:
   ```bash
   # Compare token counts before/after
   npm run token-viz -- --file old_page.md
   npm run token-viz -- --file new_page.md
   ```

2. **Retrain if Needed**:
   - >10% of pages changed significantly
   - New character symbols added
   - Major vocabulary shifts detected

3. **Training Process**:
   ```bash
   python3 scripts/train_tokenizer.py
   python3 scripts/convert_tokenizer_to_json.py
   cp tokenizer/gibsey_bpe.json public/tokenizer/
   ```

4. **Validation**:
   ```bash
   npm run token-viz -- --examples
   # Test in development environment
   npm run dev
   ```

5. **Deployment**:
   ```bash
   git add tokenizer/
   git commit -m "Update tokenizer for corpus v1.1"
   git tag tokenizer-v1.1
   git push origin main --tags
   ```

### Adding New Special Tokens

For new characters or QDPI extensions:

1. **Update Token Lists**:
   ```python
   # scripts/train_tokenizer.py
   character_tokens = [
       # ... existing tokens ...
       "new-character-symbol"
   ]
   ```

2. **Update Services**:
   ```python
   # backend/app/tokenizer_service.py
   self.character_tokens = [
       # ... add new token ...
   ]
   ```
   
   ```typescript
   // src/services/tokenizerService.ts
   character_tokens: [
       // ... add new token ...
   ]
   ```

3. **Retrain and Deploy** (see above)

### Performance Optimization

#### Backend Optimization
- Cache tokenizer instances
- Use lazy loading for large files
- Implement token count caching for repeated texts
- Monitor memory usage with large vocabularies

#### Frontend Optimization
- Debounce real-time token counting (300ms)
- Cache tokenization results for common phrases
- Use Web Workers for heavy tokenization tasks
- Implement progressive loading for large texts

#### Example Caching Implementation

```python
# Backend caching
from functools import lru_cache

class GibseyTokenizerService:
    @lru_cache(maxsize=1000)
    def count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))
```

```typescript
// Frontend caching
const tokenCountCache = new Map<string, number>();

async countTokens(text: string): Promise<number> {
  if (tokenCountCache.has(text)) {
    return tokenCountCache.get(text)!;
  }
  const count = await this.actualCountTokens(text);
  tokenCountCache.set(text, count);
  return count;
}
```

## Performance Optimization

### Benchmarks

| Operation | Backend (Python) | Frontend (TypeScript) |
|-----------|------------------|----------------------|
| Load tokenizer | 100ms | 200ms |
| Count tokens (100 chars) | 0.1ms | 1ms |
| Tokenize (100 chars) | 0.5ms | 2ms |
| Chunk text (10KB) | 5ms | 15ms |

### Optimization Strategies

#### Backend
```python
# Pre-compile regex patterns
class GibseyTokenizerService:
    def __init__(self):
        self._special_token_pattern = re.compile(
            r'(' + '|'.join(re.escape(t) for t in all_special_tokens) + r')'
        )
```

#### Frontend
```typescript
// Use Web Workers for heavy operations
const worker = new Worker(new URL('./tokenizer.worker.ts', import.meta.url));

async countTokensHeavy(text: string): Promise<number> {
  return new Promise((resolve) => {
    worker.postMessage({ text });
    worker.onmessage = (e) => resolve(e.data.count);
  });
}
```

## Troubleshooting

### Common Issues

#### 1. Tokenizer Not Loading

**Symptoms**: Service fails to initialize, fallback to character estimation

**Python Backend**:
```bash
# Check file existence
ls -la tokenizer/gibsey_bpe.model

# Test direct loading
python3 -c "import sentencepiece as smp; sp = smp.SentencePieceProcessor(); sp.load('tokenizer/gibsey_bpe.model'); print('OK')"
```

**TypeScript Frontend**:
```bash
# Check public file access
curl http://localhost:5174/tokenizer/gibsey_bpe.json

# Test in browser console
fetch('/tokenizer/gibsey_bpe.json').then(r => r.json()).then(console.log)
```

#### 2. Token Count Mismatch

**Symptoms**: Different counts between Python and TypeScript

**Debugging**:
```bash
# Compare outputs
npm run token-viz "Test string"
# vs frontend debug interface
```

**Common Causes**:
- Different preprocessing (whitespace handling)
- Version mismatch between model files
- Character encoding issues

#### 3. Special Tokens Split

**Symptoms**: QDPI or character tokens appear as multiple tokens

**Check Training**:
```python
# Verify special tokens in vocabulary
sp = smp.SentencePieceProcessor()
sp.load('tokenizer/gibsey_bpe.model')
print(sp.piece_to_id('<X_READ>'))  # Should return valid ID
print(sp.piece_to_id('jacklyn-variance'))  # Should return valid ID
```

**Resolution**: Retrain tokenizer with correct special token list

#### 4. Performance Issues

**Symptoms**: Slow tokenization, UI lag

**Profile Performance**:
```python
# Backend profiling
import time
start = time.time()
tokenizer.count_tokens(large_text)
print(f"Time: {time.time() - start:.3f}s")
```

**Optimizations**:
- Implement caching for repeated texts
- Use debouncing for real-time UI updates
- Consider chunking very large inputs

### Debug Tools

#### CLI Debugging
```bash
# Test specific functionality
npm run token-viz -- --interactive

# Compare with reference
echo "Test text" | npm run token-viz

# File analysis
npm run token-viz -- --file problematic_file.txt
```

#### Debug Interface
```url
http://localhost:5174/?debug
```

Features:
- Tokenizer loading status
- Live token counting
- Special token highlighting
- Performance metrics
- Test case validation

#### Backend Testing
```python
# Test service directly
from backend.app.tokenizer_service import get_tokenizer_service

service = get_tokenizer_service()
info = service.get_tokenizer_info()
print(json.dumps(info, indent=2))

# Test with known inputs
test_cases = [
    "Hello world",
    "<X_READ>Test<Y_INDEX>", 
    "jacklyn-variance london-fox"
]

for test in test_cases:
    tokens = service.tokenize(test)
    print(f"{test} -> {tokens}")
```

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `SentencePiece model not found` | Missing model file | Check file path, re-run training |
| `Failed to load tokenizer` | Corrupted model | Re-download or retrain |
| `Special token not found` | Missing from vocabulary | Retrain with updated special tokens |
| `Token count mismatch` | Version differences | Ensure same model in all services |
| `JSON parse error` | Corrupted JSON export | Re-run conversion script |

---

This integration guide provides comprehensive coverage of the Gibsey custom tokenizer implementation. For additional support, refer to the CLI tool examples and debug interface for hands-on testing and validation.