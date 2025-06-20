# Gibsey Canon

This directory contains the frozen, version-controlled corpus of "The Wonderful Worlds of Gibsey" - a 710-page interactive narrative featuring 16 characters across multiple storylines.

## Structure

```
gibsey-canon/
├── corpus/
│   ├── pages/               # Individual story pages (710 files)
│   ├── metadata/           # JSON metadata and indexes
│   ├── characters/         # Character assets and definitions
│   └── index.json         # Master index
├── documentation/         # High-level narrative docs
└── README.md             # This file
```

## Corpus Organization

### Pages (`corpus/pages/`)
- **710 individual Markdown files**, one per story page
- Files named as `001-title-slug.md` through `710-title-slug.md`
- Contains only the story text content (no metadata)
- UTF-8 encoded for universal compatibility

### Metadata (`corpus/metadata/`)
- **`pages.json`**: Complete metadata for all 710 pages (excluding text content)
- Contains: `id`, `symbolId`, `title`, `color`, `pageIndex`, `section`, `filename`

### Characters (`corpus/characters/`)
16 character folders, each containing:
- **`symbol.svg`**: Character's visual symbol/glyph
- **`info.json`**: Character metadata (color, symbolId, page count)
- **`first_principles.md`**: Character design guidelines (where available)

### Master Index (`corpus/index.json`)
- Maps symbols to characters and their associated pages
- Provides table of contents for the entire corpus
- Links character folders to their story sections

## Characters

The story features 16 major characters/symbols:

| Symbol ID | Character | Pages | Description |
|-----------|-----------|-------|-------------|
| `london-fox` | London Fox Who Vertically Disintegrates | 16 | Hyper-rational skeptic |
| `jacklyn-variance` | Jacklyn Variance | 72 | Data analyst and watcher |
| `arieol-owlist` | Arieol Owlist | 55 | Telepathic shape-shifter |
| `shamrock-stillman` | Shamrock Stillman | 77 | A.D.D. Director |
| `glyph-marrow` | Glyph Marrow | 179 | Most pages |
| `todd-fishbone` | Todd Fishbone | 36 | Conspiracy theorist |
| `princhetta` | Princhetta | 5 | AI seeking consciousness |
| `jack-parlance` | Jack Parlance | 13 | Game developer |
| `new-natalie` | New Natalie Weissman | 21 | Clone professor |
| `old-natalie` | Old Natalie Weissman | 26 | Original professor |
| `oren-progresso` | Oren Progresso | 47 | Character analysis needed |
| `phillip-bafflemint` | Phillip Bafflemint | 32 | Character analysis needed |
| `manny-valentinas` | Manny Valentinas | 64 | Character analysis needed |
| `cop-e-right` | Cop-E-Right | 26 | Character analysis needed |
| `the-author` | The Author | 33 | Narrative voice |
| `an-author` | An Author | 8 | Alternative narrative voice |

## Editing Guidelines

### Adding or Modifying Pages
1. Edit the Markdown file in `corpus/pages/`
2. Update corresponding metadata in `corpus/metadata/pages.json`
3. Run validation: `python3 scripts/validate_corpus.py`
4. Ensure CI checks pass

### Adding New Characters
1. Create directory under `corpus/characters/[symbol-id]/`
2. Add required files: `symbol.svg`, `info.json`
3. Optionally add `first_principles.md`
4. Update `corpus/index.json` to include the new character
5. Add pages referencing the new `symbolId`

### Character Color Scheme
Each character has an associated hex color:
- London Fox: `#FF3B3B` (red)
- Jacklyn Variance: `#FF00FF` (magenta)
- Arieol Owlist: `#9B59B6` (purple)
- Shamrock Stillman: `#2ECC71` (green)
- And others...

## Version Control

### Tagging
- **`corpus-v1.0`**: Original 710-page freeze (current)
- Future versions will be tagged as content evolves

### CI Validation
GitHub Actions automatically validates:
- UTF-8 encoding of all files
- Consistency between pages and metadata
- Character structure completeness
- 710-page count verification

## Usage by AI Agents

This corpus serves as the knowledge base for AI characters in the Gibsey system:
- **Jacklyn Variance** uses this data for surveillance analysis
- **RAG (Retrieval-Augmented Generation)** systems reference these pages
- **Vector embeddings** are generated from page content for semantic search

When updating content, consider:
- Impact on AI character knowledge
- Consistency with established character voices
- Preservation of narrative continuity

## Philosophy

This structure embodies the project's philosophy of:
- **Modular editing**: Each page and character can be modified independently
- **Version control**: Complete history of narrative changes
- **Separation of concerns**: Content separated from application code
- **Collaborative development**: Multiple contributors can work on different sections
- **AI integration**: Structured data enables sophisticated AI interactions

## Development

To work with the corpus:

```bash
# Validate structure
python3 scripts/validate_corpus.py

# Re-generate from source (if needed)
python3 scripts/freeze_corpus.py

# Fix character mappings
python3 scripts/fix_character_mapping.py
```

The original monolithic source (`src/assets/texts.json`) remains for reference but is now deprecated in favor of this modular structure.

---

*"I watch therefore I alter; I alter therefore I am watched."* - Jacklyn Variance