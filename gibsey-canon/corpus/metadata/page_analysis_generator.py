#!/usr/bin/env python3
"""
Page Analysis Generator for The Entrance Way: Into the Wonderful Worlds of Gibsey
Systematically analyzes all 710 pages and generates comprehensive metadata
"""

import json
import os
import re
from typing import Dict, List, Set, Tuple
from pathlib import Path

class PageAnalyzer:
    def __init__(self, pages_dir: str, output_file: str):
        self.pages_dir = Path(pages_dir)
        self.output_file = Path(output_file)
        self.analysis_data = None
        self.character_first_principles = {}
        self.load_character_first_principles()
        self.load_existing_analysis()
        
    def load_character_first_principles(self):
        """Load character first principles from character directories"""
        characters_dir = Path("gibsey-canon/corpus/characters")
        
        for char_dir in characters_dir.glob("*"):
            if char_dir.is_dir():
                first_principles_file = char_dir / "first_principles.md"
                if first_principles_file.exists():
                    with open(first_principles_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract key principles and character information
                    self.character_first_principles[char_dir.name] = {
                        "content": content,
                        "principles": self.extract_principles(content),
                        "character_traits": self.extract_character_traits(content),
                        "thematic_elements": self.extract_thematic_elements(content)
                    }
    
    def extract_principles(self, content: str) -> List[str]:
        """Extract key principles from first principles content"""
        principles = []
        lines = content.split('\n')
        
        for line in lines:
            # Look for numbered principles or key statements
            if re.match(r'^\d+\.', line.strip()) or line.strip().startswith('**Principle:'):
                principles.append(line.strip())
            elif line.strip().startswith('###') or line.strip().startswith('GM-'):
                principles.append(line.strip())
        
        return principles[:10]  # Limit to top 10 principles
    
    def extract_character_traits(self, content: str) -> List[str]:
        """Extract character traits from first principles"""
        traits = []
        content_lower = content.lower()
        
        # Common character trait indicators
        trait_keywords = ['skeptic', 'rational', 'obsessive', 'panic', 'control', 'creator', 
                         'investigator', 'confusion', 'perception', 'consciousness', 'mystical']
        
        for keyword in trait_keywords:
            if keyword in content_lower:
                traits.append(keyword)
        
        return traits
    
    def extract_thematic_elements(self, content: str) -> List[str]:
        """Extract thematic elements from first principles"""
        themes = []
        content_lower = content.lower()
        
        # Thematic keywords specific to characters
        theme_keywords = ['control', 'reality', 'fiction', 'consciousness', 'ai', 'surveillance',
                         'extraction', 'transformation', 'recursion', 'mysticism', 'identity']
        
        for keyword in theme_keywords:
            if keyword in content_lower:
                themes.append(keyword)
        
        return themes

    def load_existing_analysis(self):
        """Load existing analysis structure or create new one"""
        if self.output_file.exists():
            with open(self.output_file, 'r', encoding='utf-8') as f:
                self.analysis_data = json.load(f)
        else:
            self.analysis_data = self.create_base_structure()
    
    def create_base_structure(self):
        """Create the base analysis structure"""
        return {
            "metadata": {
                "title": "The Entrance Way: Into the Wonderful Worlds of Gibsey - Page Analysis",
                "description": "Granular page-by-page metadata analysis of all 710 pages",
                "version": "1.0",
                "created": "2025-07-05",
                "analyst": "Page Analysis Engine",
                "methodology": "Comprehensive content analysis focusing on literary, philosophical, and thematic elements",
                "total_pages": 710
            },
            "classification_schema": {
                "content_types": {
                    "meta_commentary": "Author's prefaces, meta-textual commentary, fourth wall breaks",
                    "narrative_prose": "Traditional narrative storytelling with character development",
                    "dialogue": "Character conversations and interactions",
                    "mystical_exposition": "Philosophical and mystical texts, symbolic language",
                    "corporate_reports": "Surveillance reports, business documents, bureaucratic text",
                    "stream_of_consciousness": "Internal monologue, fragmented thoughts",
                    "legal_documents": "Contracts, petitions, formal legal language",
                    "technical_exposition": "AI/technology descriptions, system documentation"
                },
                "emotional_tones": {
                    "contemplative": "Reflective, thoughtful, meditative",
                    "anxious": "Worried, uncertain, paranoid",
                    "mysterious": "Enigmatic, puzzling, hidden meanings",
                    "bureaucratic": "Formal, official, impersonal",
                    "philosophical": "Abstract, theoretical, existential",
                    "nostalgic": "Longing, reminiscent, melancholic",
                    "tense": "Suspenseful, dramatic, urgent",
                    "humorous": "Playful, ironic, satirical",
                    "introspective": "Self-examining, psychological, internal"
                },
                "themes": {
                    "reality_vs_fiction": "Blurred lines between real and imagined",
                    "surveillance_watching": "Observation, monitoring, being watched",
                    "corporate_control": "Business dominance, theme park metaphors",
                    "consciousness": "Awareness, thought, mental states",
                    "identity": "Self-knowledge, character development, authenticity",
                    "authorship": "Creation, writing, artistic control",
                    "ai_technology": "Artificial intelligence, automation, digital existence",
                    "mysticism": "Spiritual elements, symbolic language, transcendence",
                    "transformation": "Change, evolution, metamorphosis",
                    "alienation": "Isolation, disconnection, loneliness"
                },
                "narrative_devices": {
                    "meta_textual": "Self-referential, breaking fourth wall",
                    "nested_stories": "Stories within stories, layered narratives",
                    "unreliable_narrator": "Questionable or biased narration",
                    "genre_shifts": "Movement between different literary styles",
                    "fragmented_structure": "Non-linear, broken narrative flow",
                    "direct_address": "Speaking directly to reader",
                    "document_within_document": "Embedded reports, letters, files"
                },
                "mystical_elements": {
                    "corpus_references": "References to The Corpus, mystical texts",
                    "gibsey_world": "Theme park as metaphor for reality",
                    "symbolic_language": "Metaphorical, allegorical content",
                    "transformation_imagery": "Metamorphosis, change, evolution",
                    "consciousness_themes": "Awareness, thought, mental states",
                    "magical_realism": "Fantastical elements in realistic settings"
                },
                "technical_metaphors": {
                    "ai_chatbots": "Artificial intelligence, automated systems",
                    "surveillance_systems": "Monitoring, observation, control",
                    "corporate_structures": "Business hierarchies, organizational control",
                    "theme_parks": "Constructed realities, entertainment complexes",
                    "screens_cameras": "Visual media, observation devices",
                    "data_processing": "Information systems, digital analysis"
                }
            },
            "pages": {},
            "character_first_principles": {}
        }
    
    def analyze_page_content(self, content: str, page_num: int, filename: str) -> Dict:
        """Analyze individual page content"""
        analysis = {
            "title": self.extract_title(content, filename),
            "section": self.determine_section(page_num),
            "content_type": self.determine_content_type(content),
            "emotional_tone": self.determine_emotional_tone(content),
            "word_count": len(content.split()),
            "themes": self.identify_themes(content),
            "character_interactions": self.identify_characters(content),
            "narrative_devices": self.identify_narrative_devices(content),
            "mystical_elements": self.identify_mystical_elements(content),
            "connection_points": self.identify_connections(content),
            "technical_metaphors": self.identify_technical_metaphors(content),
            "key_phrases": self.extract_key_phrases(content),
            "literary_references": self.identify_literary_references(content),
            "recurring_motifs": self.identify_motifs(content),
            "analysis_notes": self.generate_analysis_notes(content, page_num)
        }
        return analysis
    
    def extract_title(self, content: str, filename: str) -> str:
        """Extract title from content or filename"""
        lines = content.strip().split('\n')
        first_line = lines[0] if lines else ""
        
        # Check for markdown header
        if first_line.startswith('#'):
            return first_line.lstrip('#').strip()
        
        # Check for bold title
        if first_line.startswith('**') and first_line.endswith('**'):
            return first_line[2:-2].strip()
        
        # Extract from filename
        title_part = filename.split('-', 1)[1] if '-' in filename else filename
        return title_part.replace('-', ' ').replace('.md', '').title()
    
    def determine_section(self, page_num: int) -> str:
        """Determine which section the page belongs to"""
        if 1 <= page_num <= 8:
            return "author_preface_1"
        elif 9 <= page_num <= 24:
            return "london_fox"
        elif 25 <= page_num <= 203:
            return "glyph_marrow_1_6"
        elif 204 <= page_num <= 235:
            return "phillip_bafflemint_1_3"
        elif 236 <= page_num <= 307:
            return "jacklyn_variance"
        elif 308 <= page_num <= 354:
            return "last_auteur"
        elif 355 <= page_num <= 380:
            return "gibseyan_mysticism"
        elif 381 <= page_num <= 385:
            return "princhetta"
        elif 386 <= page_num <= 411:
            return "petition_bankruptcy"
        elif 412 <= page_num <= 432:
            return "tempestuous_storm"
        elif 433 <= page_num <= 487:
            return "arieol_owlist"
        elif 488 <= page_num <= 500:
            return "biggest_shit"
        elif 501 <= page_num <= 564:
            return "phillip_bafflemint_4_6"
        elif 565 <= page_num <= 641:
            return "glyph_marrow_7_11"
        elif 642 <= page_num <= 677:
            return "todd_fishbone"
        elif 678 <= page_num <= 710:
            return "author_preface_2"
        else:
            return "unknown"
    
    def determine_content_type(self, content: str) -> str:
        """Determine the content type based on content analysis"""
        content_lower = content.lower()
        
        # Check for meta-commentary indicators
        if any(phrase in content_lower for phrase in ['author', 'preface', 'this is not', 'reader', 'writing']):
            return "meta_commentary"
        
        # Check for corporate/legal documents
        if any(phrase in content_lower for phrase in ['petition', 'bankruptcy', 'report', 'analysis', 'document']):
            return "corporate_reports"
        
        # Check for stream of consciousness
        if content.count('.') < content.count(',') and len(content.split()) > 100:
            return "stream_of_consciousness"
        
        # Check for dialogue
        if content.count('"') > 4 or content.count("'") > 4:
            return "dialogue"
        
        # Check for mystical exposition
        if any(phrase in content_lower for phrase in ['mysticism', 'consciousness', 'spiritual', 'transcend']):
            return "mystical_exposition"
        
        # Default to narrative prose
        return "narrative_prose"
    
    def determine_emotional_tone(self, content: str) -> str:
        """Determine emotional tone based on content analysis"""
        content_lower = content.lower()
        
        # Anxiety indicators
        if any(phrase in content_lower for phrase in ['anxiety', 'worried', 'panic', 'fear', 'nervous']):
            return "anxious"
        
        # Bureaucratic indicators
        if any(phrase in content_lower for phrase in ['petition', 'report', 'document', 'analysis', 'official']):
            return "bureaucratic"
        
        # Mysterious indicators
        if any(phrase in content_lower for phrase in ['mystery', 'unknown', 'hidden', 'secret', 'enigma']):
            return "mysterious"
        
        # Philosophical indicators
        if any(phrase in content_lower for phrase in ['consciousness', 'existence', 'reality', 'meaning', 'truth']):
            return "philosophical"
        
        # Nostalgic indicators
        if any(phrase in content_lower for phrase in ['remember', 'past', 'nostalgia', 'longing', 'memory']):
            return "nostalgic"
        
        # Default to contemplative
        return "contemplative"
    
    def identify_themes(self, content: str) -> List[str]:
        """Identify themes present in the content"""
        themes = []
        content_lower = content.lower()
        
        # Reality vs fiction
        if any(phrase in content_lower for phrase in ['fiction', 'reality', 'real', 'imagined', 'true', 'false']):
            themes.append("reality_vs_fiction")
        
        # Surveillance/watching
        if any(phrase in content_lower for phrase in ['watch', 'observe', 'surveillance', 'monitor', 'see', 'look']):
            themes.append("surveillance_watching")
        
        # Corporate control
        if any(phrase in content_lower for phrase in ['corporate', 'company', 'business', 'ceo', 'control']):
            themes.append("corporate_control")
        
        # Consciousness
        if any(phrase in content_lower for phrase in ['consciousness', 'aware', 'thought', 'mind', 'thinking']):
            themes.append("consciousness")
        
        # Identity
        if any(phrase in content_lower for phrase in ['identity', 'self', 'who am i', 'myself', 'person']):
            themes.append("identity")
        
        # Authorship
        if any(phrase in content_lower for phrase in ['author', 'write', 'writing', 'create', 'creation']):
            themes.append("authorship")
        
        # AI/Technology
        if any(phrase in content_lower for phrase in ['ai', 'artificial', 'intelligence', 'technology', 'digital', 'computer']):
            themes.append("ai_technology")
        
        # Mysticism
        if any(phrase in content_lower for phrase in ['mystical', 'spiritual', 'transcend', 'mysticism', 'sacred']):
            themes.append("mysticism")
        
        return themes
    
    def identify_characters(self, content: str) -> Dict:
        """Identify character interactions in the content using first principles"""
        characters = {
            "primary": "",
            "secondary": [],
            "mentioned": [],
            "first_principles_traits": [],
            "character_alignment": {}
        }
        
        # Enhanced character mapping with first principles
        character_mapping = {
            "London Fox": "london-fox",
            "Glyph Marrow": "glyph-marrow", 
            "Phillip Bafflemint": "phillip-bafflemint",
            "Jacklyn Variance": "jacklyn-variance",
            "Oren Progresso": "oren-progresso",
            "Natalie": "old-natalie",
            "Princhetta": "princhetta",
            "Arieol Owlist": "arieol-owlist",
            "Jack Parlance": "jack-parlance",
            "Todd Fishbone": "todd-fishbone",
            "The Author": "the-author",
            "An Author": "an-author",
            "Shamrock Stillman": "shamrock-stillman",
            "Cop E. Right": "cop-e-right"
        }
        
        content_lower = content.lower()
        
        for display_name, char_key in character_mapping.items():
            if display_name.lower() in content_lower:
                if not characters["primary"]:
                    characters["primary"] = display_name
                    
                    # Add first principles traits if available
                    if char_key in self.character_first_principles:
                        fp_data = self.character_first_principles[char_key]
                        characters["first_principles_traits"] = fp_data["character_traits"]
                        characters["character_alignment"] = {
                            "thematic_elements": fp_data["thematic_elements"],
                            "key_principles": fp_data["principles"][:3]  # Top 3 principles
                        }
                else:
                    characters["mentioned"].append(display_name)
        
        return characters
    
    def identify_narrative_devices(self, content: str) -> List[str]:
        """Identify narrative devices used in the content"""
        devices = []
        content_lower = content.lower()
        
        # Meta-textual
        if any(phrase in content_lower for phrase in ['reader', 'this is not', 'writing', 'text', 'story']):
            devices.append("meta_textual")
        
        # Direct address
        if 'you' in content_lower:
            devices.append("direct_address")
        
        # Document within document
        if any(phrase in content_lower for phrase in ['report', 'document', 'petition', 'analysis']):
            devices.append("document_within_document")
        
        # Fragmented structure
        if content.count('\n\n') > 5:
            devices.append("fragmented_structure")
        
        return devices
    
    def identify_mystical_elements(self, content: str) -> List[str]:
        """Identify mystical elements in the content"""
        elements = []
        content_lower = content.lower()
        
        # Gibsey World references
        if 'gibsey' in content_lower:
            elements.append("gibsey_world")
        
        # Consciousness themes
        if any(phrase in content_lower for phrase in ['consciousness', 'awareness', 'mind', 'thought']):
            elements.append("consciousness_themes")
        
        # Transformation imagery
        if any(phrase in content_lower for phrase in ['transform', 'change', 'metamorphosis', 'evolution']):
            elements.append("transformation_imagery")
        
        return elements
    
    def identify_connections(self, content: str) -> List[str]:
        """Identify connection points to other parts of the work"""
        connections = []
        content_lower = content.lower()
        
        # Common connection patterns
        if 'screen' in content_lower:
            connections.append("screen_imagery")
        
        if 'mirror' in content_lower:
            connections.append("mirror_metaphor")
        
        if 'theme park' in content_lower:
            connections.append("theme_park_metaphor")
        
        return connections
    
    def identify_technical_metaphors(self, content: str) -> List[str]:
        """Identify technical metaphors in the content"""
        metaphors = []
        content_lower = content.lower()
        
        # AI/Technology metaphors
        if any(phrase in content_lower for phrase in ['ai', 'artificial', 'intelligence', 'chatbot', 'digital']):
            metaphors.append("ai_technology")
        
        # Surveillance metaphors
        if any(phrase in content_lower for phrase in ['surveillance', 'monitor', 'watch', 'observe']):
            metaphors.append("surveillance_systems")
        
        # Corporate metaphors
        if any(phrase in content_lower for phrase in ['corporate', 'company', 'business', 'ceo']):
            metaphors.append("corporate_structures")
        
        # Screen/camera metaphors
        if any(phrase in content_lower for phrase in ['screen', 'camera', 'monitor', 'display']):
            metaphors.append("screens_cameras")
        
        return metaphors
    
    def extract_key_phrases(self, content: str) -> List[str]:
        """Extract key phrases from the content"""
        # Simple extraction of quoted phrases and significant sentences
        phrases = []
        
        # Extract quoted text
        quotes = re.findall(r'"([^"]*)"', content)
        phrases.extend(quotes[:3])  # Limit to 3 quotes
        
        # Extract sentences with significant words
        sentences = content.split('.')
        for sentence in sentences[:10]:  # Limit to first 10 sentences
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 100:
                if any(word in sentence.lower() for word in ['consciousness', 'reality', 'mystery', 'author', 'watch', 'think']):
                    phrases.append(sentence)
                    if len(phrases) >= 5:
                        break
        
        return phrases[:5]  # Return max 5 phrases
    
    def identify_literary_references(self, content: str) -> List[str]:
        """Identify literary references in the content"""
        references = []
        content_lower = content.lower()
        
        # Common literary references
        if 'raymond chandler' in content_lower:
            references.append("Raymond Chandler")
        
        if 'beckett' in content_lower:
            references.append("Samuel Beckett")
        
        if 'giallo' in content_lower:
            references.append("Giallo films")
        
        return references
    
    def identify_motifs(self, content: str) -> List[str]:
        """Identify recurring motifs in the content"""
        motifs = []
        content_lower = content.lower()
        
        # Common motifs
        if 'screen' in content_lower:
            motifs.append("screens")
        
        if 'watch' in content_lower:
            motifs.append("watching")
        
        if 'mirror' in content_lower:
            motifs.append("mirrors")
        
        if 'mystery' in content_lower:
            motifs.append("mystery")
        
        if 'author' in content_lower:
            motifs.append("authorship")
        
        return motifs
    
    def generate_analysis_notes(self, content: str, page_num: int) -> str:
        """Generate analysis notes for the page"""
        notes = []
        
        # Add section-specific notes
        section = self.determine_section(page_num)
        if section == "author_preface_1":
            notes.append("Part of the opening meta-fictional framework.")
        elif section == "jacklyn_variance":
            notes.append("Corporate surveillance narrative analyzing the text itself.")
        elif section == "gibseyan_mysticism":
            notes.append("Philosophical exploration of consciousness and reality.")
        
        # Add content-specific notes
        if "screen" in content.lower():
            notes.append("Contains significant screen/mirror imagery.")
        
        if "author" in content.lower():
            notes.append("Addresses questions of authorship and creation.")
        
        if len(notes) == 0:
            notes.append("Standard narrative content within the broader work.")
        
        return " ".join(notes)
    
    def analyze_all_pages(self, force_reanalyze=False):
        """Analyze all pages in the directory"""
        page_files = sorted([f for f in os.listdir(self.pages_dir) if f.endswith('.md')])
        updated_count = 0
        
        for filename in page_files:
            # Extract page number from filename
            page_num = int(filename[:3])
            page_key = f"{page_num:03d}"
            
            # Skip if already analyzed and not forcing re-analysis
            if page_key in self.analysis_data["pages"] and not force_reanalyze:
                continue
            
            # Read and analyze page
            with open(self.pages_dir / filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = self.analyze_page_content(content, page_num, filename)
            self.analysis_data["pages"][page_key] = analysis
            updated_count += 1
            
            print(f"Analyzed page {page_num}: {analysis['title']}")
            
        print(f"Total pages updated: {updated_count}")
    
    def save_analysis(self):
        """Save the analysis to JSON file"""
        # Include character first principles in the analysis data
        self.analysis_data["character_first_principles"] = self.character_first_principles
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_data, f, indent=2, ensure_ascii=False)
        print(f"Analysis saved to {self.output_file}")
        print(f"Character first principles included: {len(self.character_first_principles)} characters")

def main():
    """Main function to run the analysis"""
    pages_dir = "/Users/ghostradongus/the-gibsey-project/gibsey-canon/corpus/pages"
    output_file = "/Users/ghostradongus/the-gibsey-project/gibsey-canon/corpus/metadata/page_analysis.json"
    
    analyzer = PageAnalyzer(pages_dir, output_file)
    
    # Force re-analysis to incorporate character first principles
    print("Re-analyzing all pages to incorporate character first principles...")
    analyzer.analyze_all_pages(force_reanalyze=True)
    analyzer.save_analysis()

if __name__ == "__main__":
    main()