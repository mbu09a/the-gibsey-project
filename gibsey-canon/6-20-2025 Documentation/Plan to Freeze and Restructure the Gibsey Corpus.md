Great — I’ll prepare a plan for Claude Code that starts from the current repo state and reorganizes the corpus into a frozen, versioned structure with CI. I’ll include a new directory structure, extraction scripts, metadata flattening, and GitHub Actions-based CI to diff and lint corpus changes.

# Plan to Freeze and Restructure the Gibsey Corpus

**Objective:** Establish a version-controlled “gibsey-canon” directory containing the 710-page story corpus in a modular, maintainable format. This will split the monolithic JSON into individual page files with metadata and gather all character-specific assets (SVGs, colors, first principles) into one organized location for long-term editing and CI validation.

## 1. Export Pages to Markdown Files and Build Index

- **Script to split `texts.json`:** Create a Node.js or Python script that reads the entire corpus JSON (`src/assets/texts.json`, which currently holds all 710 pages) and writes each page’s text into its own UTF-8 encoded Markdown file. For example, output files under `gibsey-canon/corpus/pages/` named by page number and title (e.g. `001-Title.md`, `002-Next-Title.md`). The script should sanitize file names (use page index with zero-padding for ordering, and a slugified title after the number) to avoid special characters or spaces.
    
- **Preserve page content:** In each `.md` file, include **only the story text** for that page (no JSON syntax). Paragraph breaks in the original JSON should be retained as newlines or Markdown breaks so that the text reads naturally. We do not include frontmatter in these files (the metadata will be stored separately), keeping them as pure content for easy reading/editing.
    
- **Extract metadata:** For each page, collect all non-text fields (e.g. `id`, `symbolId`, `title`, `color`, `pageIndex`, `section`, and any other keys like `rotation`, `childIds`, `branches`, etc. if present) from the JSON. Write these entries to a JSON file `gibsey-canon/corpus/metadata/pages.json` as an array of page metadata objects. This `pages.json` will list every page with its attributes except the actual text (which now lives in the Markdown files). For example, an entry might look like:
    
    ```json
    {
      "pageIndex": 1,
      "id": "page_0",
      "title": "An Author’s Preface",
      "symbolId": "an-author",
      "section": "Preface",
      "color": "#34FF78"
    }
    ```
    
    (All fields from the original JSON except `text` should be preserved here for each page.)
    
- **Build master index:** Generate a top-level index file `gibsey-canon/corpus/index.json` that links pages to their symbols and character folders. This index helps navigate the corpus by character/chapter. One approach is to structure it by symbol (chapter): for each unique `symbolId` encountered, list the pages that belong to that symbol and the associated character info. For example:
    
    ```json
    {
      "symbols": {
        "london-fox": {
          "title": "London Fox Who Vertically Disintegrates",
          "color": "#FF3B3B",
          "characterDir": "characters/london-fox",
          "pages": [1, 2, 3, ...] 
        },
        "jacklyn-variance": {
          "title": "Jacklyn Variance…",
          "color": "#FF00FF",
          "characterDir": "characters/jacklyn-variance",
          "pages": [45, 46, ...]
        },
        "...": {}
      }
    }
    ```
    
    The index maps each `symbolId` to its human-readable title, color, folder, and list of page numbers (or file paths). This provides a quick lookup of which pages belong to each chapter/character. It essentially captures the table of contents: 16 symbols (chapters) in total, each with its set of page files.
    
- **Verify ordering and completeness:** After running the script, verify that 710 Markdown files were created (one per page) and that `pages.json` has 710 entries. The index should have 16 top-level symbols (matching the 16 chapters/characters mentioned in the README). This granular breakup will allow piecemeal updates to individual pages and easier diffs, instead of editing one giant JSON for all content.
    

## 2. Consolidate Character Symbols and Info

- **Gather SVG symbols:** Collect all 16 SVG files from `public/corpus-symbols/` (each glyph representing a chapter symbol) and copy them into the new `gibsey-canon/corpus/characters/` directory. Create one subfolder per character/symbol, named by the `symbolId` (e.g. `gibsey-canon/corpus/characters/london-fox/`, `.../jacklyn-variance/`, etc.). In each character’s folder, place the SVG file as `symbol.svg`. This ensures each “chapter” glyph is stored alongside that character’s other info. (The exact file names in `public/corpus-symbols` may have been arbitrary, so this step establishes a consistent naming convention and location for each symbol graphic.)
    
- **Integrate color codes:** Take the color hex codes from `src/assets/colors.ts` (the `symbolColors` map) and include them in the character data. For each character folder, we can create a simple JSON or include it in the index. For instance, add a file `info.json` inside `characters/{symbolId}/` containing the color (and possibly the full character name if needed). Alternatively, as shown above, the `index.json` can directly map each symbol to its color code. The key point is to externalize the color mapping out of the code and into the canon data. (Currently `colors.ts` is the single source of truth for symbol colors. After restructuring, the color for each symbol should live in the canon directory so that the app or any tool can read it from there.)
    
- **Extract “First Principles” docs:** Incorporate the character backstory and design notes (“first principles”) for each character into the corresponding folder. These were previously in separate markdown files under `docs/characters/*.md`. For example, copy **London Fox – First Principles** from `docs/characters/london_fox_first_principles.md` into `gibsey-canon/corpus/characters/london-fox/first_principles.md`. Do this for all characters to collate their narrative design guidelines with the rest of their data. Each of these files contains the foundational traits or rules governing the character (as shown in the London Fox example). Having them alongside the story content means editors and AI agents can easily reference a character’s defining principles when working with the corpus.
    
- **Map symbols to character identities:** Ensure the folder structure cleanly reflects the mapping of symbol IDs (used in the story pages) to character names. In most cases the `symbolId` is the character’s identifier (e.g. `london-fox`, `cop-e-right`, `shamrock-stillman`). A few might need clarification (e.g. `old-natalie` vs `new-natalie` for two versions of Natalie Weissman). We should use the same `symbolId` strings from the pages and color map as the folder names to avoid confusion. Inside each folder, the `first_principles.md` file can have a header with the full character name if needed, but the directory name itself will match the symbol ID used in code and data.
    
- **Include other related info:** If there are additional narrative files (for example, any “Agent blueprint” or similar design notes such as Jacklyn’s agent blueprint), those could also be moved into the respective character folder or into the `documentation` area. The goal is to **flatten all character-specific definitions** (symbol SVG, color, principles, etc.) into one place. This makes each character’s folder a self-contained reference for that character’s visual and narrative metadata.
    
- **Consolidate global docs:** Move any high-level narrative documentation into the `gibsey-canon/documentation/` directory. For instance, the **architecture notes** currently in `docs/architecture.md` (which likely describe the story’s structural or thematic architecture) should be copied to `gibsey-canon/documentation/architecture.md` for posterity. Similarly, if there are general “Gibsey first principles” or other overarching world documents (such as `docs/gibsey_first_principles.md`), bring them into this documentation folder. By doing this, all canon-related text (both the story content and the supporting narrative design docs) live under `gibsey-canon/`, separate from the application code. This separation clearly delineates **content** vs. **code**, enabling future agents or editors to work with the story canon without digging through source code.
    

## 3. Set Up Continuous Integration Checks

With the corpus frozen and structured, add a GitHub Actions workflow to validate any changes to it:

- **UTF-8 encoding check:** The CI job should scan all files under `gibsey-canon/corpus/pages/` to ensure they are valid UTF-8 text. This guards against any binary or encoding corruption in the page files. A simple script can attempt to open each `.md` with UTF-8 decoding and fail if an error is encountered. This ensures that all page content remains textually editable and does not accidentally include non-text data.
    
- **Sync consistency check:** The workflow should verify that the **metadata and index stay in sync with the page files**. For example:
    
    - Compare the list of Markdown filenames in `corpus/pages/` with the entries in `metadata/pages.json`. The count should match 1:1 (710 entries). Every page file should have a corresponding metadata entry and vice versa.
        
    - For each entry in `pages.json`, confirm the `title`, `symbolId`, and other fields match the corresponding page file’s content or file naming. (We can enforce a convention that the first line of the `.md` might be the page title as a Markdown heading, and check that against the metadata title field. If not using frontmatter, at least ensure the file name’s title slug aligns with the metadata title.)
        
    - Verify that every `symbolId` in pages.json has a matching character folder in `corpus/characters/`, and that each character folder has a `symbol.svg` and `first_principles.md`. This catches any broken links between the pages and the character definitions.
        
- **Diff monitoring:** Add a step that runs the page-splitting script in a dry-run mode (or a small utility) to re-generate `pages.json` and perhaps a sorted list of page files, then diff them against the repository’s current versions. If the diff finds discrepancies, it means someone manually edited the pages or metadata without the two staying consistent. The CI can then flag this. In practice, after the initial freeze, we may require that any page text edits are accompanied by any required metadata updates (like if a title changed). By doing an automated diff, the CI can fail if, say, the title in a page’s metadata doesn’t match the actual title in the text.
    
- **Markdown linting (optional):** We can include a Markdown linter to enforce basic consistency in the page files. For example, ensure each page file starts with a top-level heading of the page title or has no stray HTML. If we decide to add YAML frontmatter to pages in the future (for metadata right in the file), the linter could check that all pages include the required fields. Since frontmatter is not currently used (we keep metadata separate), this is optional. At minimum, we might use a tool to ensure there are no malformed Markdown syntaxes.
    
- **Configuration:** Create a workflow file (e.g. `.github/workflows/corpus-validation.yml`) that runs on each pull request or push to main. Use a lightweight CI environment (Node or Python image) to run the above checks. This automated test will protect the canon from structural errors as it evolves. (Currently no CI is in place in the repo, so this will be the first one added.)
    

## 4. Version Control and Tagging for the Canon

- **Introduce `gibsey-canon/` in the repository:** Add the new directory (with subfolders `corpus/` and `documentation/`) at the root of the repo. This will be a major commit effectively “freezing” the corpus content in its new form. It’s wise to do this in a dedicated feature branch and merge it into main via PR for traceability (given the large number of files).
    
- **Retire the old JSON:** Once the split is in place, the original `src/assets/texts.json` can be considered frozen or deprecated. We might keep it for reference, but ideally the app should start using the new structure (this may involve updating loaders in the code to read from `gibsey-canon/corpus/index.json` and page files instead of the old JSON). In the short term, freezing means we will not manually edit `texts.json` anymore. We should document this in the project README or the new canon README.
    
- **Git tag the release:** After merging the changes, create a git tag **`corpus-v1.0`** on that commit. This tag marks the canonical version 1.0 of the story corpus. It signifies that the content as of this commit is a stable reference that the AI agents and other systems can rely on. In the future, if the story content is updated (say new pages or edits for a second edition), we can tag those as `corpus-v1.1` or `v2.0` accordingly. The tag is effectively a “freeze point” for the exact 710-page dataset as originally published. This will be invaluable for downstream ML processing or reverting content changes – one can always fetch the repository at `corpus-v1.0` to get the exact data the AI was trained on.
    
- **Ensure branch protection:** It’s a good idea to protect the main branch from direct edits to the canon files except through review. The CI checks from step 3 will run on PRs to catch issues, and the tag ensures an easy rollback point if something goes wrong.
    

## 5. Add a README for `gibsey-canon/` (Optional)

Include a `README.md` in the `gibsey-canon` directory explaining the structure and purpose of this folder. This file will be helpful for new contributors or tools interacting with the corpus:

- **Describe subfolders:** Explain that `corpus/pages/` contains one Markdown per page (with just the story text), `corpus/metadata/` holds JSON indexes (page metadata and master index), and `corpus/characters/` contains each character’s symbol SVG and design notes. Also mention the `documentation/` folder for higher-level narrative documents (like the architecture overview and any world-building notes).
    
- **Editing guidelines:** Note how to add or edit a page (e.g. “edit the Markdown and update the title in pages.json”), how to add a new chapter or character (create a new folder under characters, add a color, etc.), and point out that changes should pass the CI checks.
    
- **Purpose:** Emphasize that this separation is to allow **modular editing and version control** of the story. Each chapter (symbol) and even each page can be worked on independently without risk of merge conflicts in one giant file. The README can quote the project’s philosophy that the book can be “expanded or tweaked piecemeal without touching the code”. Now that is achieved by this structure – the narrative content is decoupled from the application logic, fulfilling the original design of one file per story/symbol (and in fact going further to one file per page for maximum granularity).
    
- **Usage by AI/agents:** (If relevant) note that the AI agents (like Jacklyn Variance) use this canon as their knowledge base, and thus maintaining consistency here is critical. The tag `corpus-v1.0` corresponds to the state the AI has “read”. Future updates should be tagged accordingly so AI models can be kept in sync with the text.
    

By following this plan, **Claude Code** can implement the refactoring in stages: first generating the new files and data structures, then integrating them into the repo, and finally setting up CI and documentation. The result will be a well-organized `gibsey-canon` directory that locks in the story’s text and all associated lore, with proper versioning for future-proofing. This creates a single source of truth for the narrative content that’s easy to maintain and review over time, independent of the application codebase.

**Sources:**

- Project README – on corpus structure and design
    
- Ingestion script – confirms all 710 pages are in one JSON file
    
- Color map – list of symbol IDs and colors (the 16 characters)
    
- Character design docs – example first principles for London Fox