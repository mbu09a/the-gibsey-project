#!/usr/bin/env python3
"""
Gibsey Token Visualization CLI Tool

A command-line tool for visualizing token breakdown and calculating TNA costs
using the custom Gibsey BPE tokenizer.

Usage:
    python scripts/token_viz.py "Your text here"
    python scripts/token_viz.py --interactive
    python scripts/token_viz.py --file path/to/text.txt
    python scripts/token_viz.py --help
"""

import sys
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import sentencepiece as spm

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from backend.app.tokenizer_service import get_tokenizer_service
    TOKENIZER_SERVICE_AVAILABLE = True
except ImportError:
    TOKENIZER_SERVICE_AVAILABLE = False
    print("⚠️ Warning: Could not import backend tokenizer service")

class TokenVizCLI:
    """CLI tool for token visualization and analysis."""
    
    def __init__(self):
        """Initialize the CLI tool."""
        self.tokenizer = None
        self.tokenizer_service = None
        
        # Configuration
        self.tokens_per_tna = 100
        
        # Color codes for terminal output
        self.colors = {
            'header': '\033[95m',
            'blue': '\033[94m',
            'cyan': '\033[96m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'purple': '\033[35m',
            'bold': '\033[1m',
            'underline': '\033[4m',
            'end': '\033[0m'
        }
        
        # Try to load tokenizer after colors are initialized
        self.load_tokenizer()
    
    def load_tokenizer(self):
        """Load the SentencePiece tokenizer."""
        # First try using the tokenizer service
        if TOKENIZER_SERVICE_AVAILABLE:
            try:
                self.tokenizer_service = get_tokenizer_service()
                if self.tokenizer_service.tokenizer:
                    print(f"{self.colors['green']}✓ Loaded tokenizer service{self.colors['end']}")
                    return
            except Exception as e:
                print(f"{self.colors['yellow']}⚠️ Tokenizer service failed: {e}{self.colors['end']}")
        
        # Fallback: load tokenizer directly
        project_root = Path(__file__).parent.parent
        model_path = project_root / "tokenizer" / "gibsey_bpe.model"
        
        if model_path.exists():
            try:
                self.tokenizer = spm.SentencePieceProcessor()
                self.tokenizer.load(str(model_path))
                print(f"{self.colors['green']}✓ Loaded tokenizer directly{self.colors['end']}")
            except Exception as e:
                print(f"{self.colors['red']}✗ Failed to load tokenizer: {e}{self.colors['end']}")
        else:
            print(f"{self.colors['red']}✗ Tokenizer model not found at {model_path}{self.colors['end']}")
    
    def colorize(self, text: str, color: str) -> str:
        """Add color to text."""
        return f"{self.colors.get(color, '')}{text}{self.colors['end']}"
    
    def tokenize_text(self, text: str) -> List[str]:
        """Tokenize text into string pieces."""
        if self.tokenizer_service and self.tokenizer_service.tokenizer:
            return self.tokenizer_service.tokenize(text)
        elif self.tokenizer:
            return self.tokenizer.encode(text, out_type=str)
        else:
            # Fallback: simple split
            return text.split()
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        if self.tokenizer_service:
            return self.tokenizer_service.count_tokens(text)
        elif self.tokenizer:
            return len(self.tokenizer.encode(text))
        else:
            # Fallback estimate
            return len(text) // 3
    
    def calculate_tna_cost(self, text: str) -> float:
        """Calculate TNA cost."""
        token_count = self.count_tokens(text)
        return token_count / self.tokens_per_tna
    
    def detect_special_tokens(self, text: str) -> Dict[str, List[str]]:
        """Detect special tokens in text."""
        if self.tokenizer_service:
            return self.tokenizer_service.has_special_tokens(text)
        
        # Fallback: manual detection
        qdpi_tokens = ["<X_READ>", "<Y_INDEX>", "<A_ASK>", "<Z_RECEIVE>"]
        character_tokens = [
            "an-author", "london-fox", "glyph-marrow", "phillip-bafflemint",
            "jacklyn-variance", "oren-progresso", "old-natalie", "princhetta",
            "cop-e-right", "new-natalie", "arieol-owlist", "jack-parlance",
            "manny-valentinas", "shamrock-stillman", "todd-fishbone", "the-author"
        ]
        
        found_qdpi = [token for token in qdpi_tokens if token in text]
        found_chars = [token for token in character_tokens if token in text]
        
        return {"qdpi": found_qdpi, "character": found_chars}
    
    def format_tokens_for_display(self, tokens: List[str]) -> str:
        """Format tokens for visual display with colors."""
        formatted_tokens = []
        
        for token in tokens:
            # Color code different token types
            if token in ["<X_READ>", "<Y_INDEX>", "<A_ASK>", "<Z_RECEIVE>"]:
                # QDPI tokens in purple
                formatted_tokens.append(self.colorize(token, 'purple'))
            elif token.startswith('<') and token.endswith('>'):
                # Other special tokens in cyan
                formatted_tokens.append(self.colorize(token, 'cyan'))
            elif token in ["an-author", "london-fox", "glyph-marrow", "phillip-bafflemint",
                          "jacklyn-variance", "oren-progresso", "old-natalie", "princhetta",
                          "cop-e-right", "new-natalie", "arieol-owlist", "jack-parlance",
                          "manny-valentinas", "shamrock-stillman", "todd-fishbone", "the-author"]:
                # Character tokens in blue
                formatted_tokens.append(self.colorize(token, 'blue'))
            else:
                # Regular tokens
                formatted_tokens.append(token)
        
        return ' '.join(formatted_tokens)
    
    def analyze_text(self, text: str, show_detailed: bool = True) -> None:
        """Perform comprehensive text analysis."""
        print(f"\n{self.colorize('=' * 60, 'header')}")
        print(f"{self.colorize('GIBSEY TOKEN ANALYSIS', 'header')}")
        print(f"{self.colorize('=' * 60, 'header')}\n")
        
        # Basic stats
        char_count = len(text)
        token_count = self.count_tokens(text)
        tna_cost = self.calculate_tna_cost(text)
        
        print(f"{self.colorize('INPUT TEXT:', 'bold')}")
        print(f'"{text[:200]}{"..." if len(text) > 200 else ""}"\n')
        
        print(f"{self.colorize('BASIC METRICS:', 'bold')}")
        print(f"  Characters: {self.colorize(str(char_count), 'cyan')}")
        print(f"  Tokens:     {self.colorize(str(token_count), 'green')}")
        print(f"  TNA Cost:   {self.colorize(f'{tna_cost:.4f}', 'yellow')}")
        print(f"  Ratio:      {self.colorize(f'{char_count/token_count:.2f}', 'blue')} chars/token\n")
        
        # Special tokens
        special_tokens = self.detect_special_tokens(text)
        if special_tokens['qdpi'] or special_tokens['character']:
            print(f"{self.colorize('SPECIAL TOKENS DETECTED:', 'bold')}")
            if special_tokens['qdpi']:
                print(f"  QDPI:       {self.colorize(', '.join(special_tokens['qdpi']), 'purple')}")
            if special_tokens['character']:
                print(f"  Characters: {self.colorize(', '.join(special_tokens['character']), 'blue')}")
            print()
        
        # Detailed tokenization
        if show_detailed:
            tokens = self.tokenize_text(text)
            print(f"{self.colorize('TOKEN BREAKDOWN:', 'bold')}")
            
            # Show tokens in groups of 10 for readability
            for i in range(0, len(tokens), 10):
                chunk = tokens[i:i+10]
                formatted_chunk = self.format_tokens_for_display(chunk)
                print(f"  {i+1:3d}-{min(i+10, len(tokens)):3d}: {formatted_chunk}")
            
            print(f"\n{self.colorize('LEGEND:', 'bold')}")
            print(f"  {self.colorize('QDPI tokens', 'purple')}   {self.colorize('Character tokens', 'blue')}   {self.colorize('Special tokens', 'cyan')}   Regular tokens")
    
    def interactive_mode(self):
        """Run interactive mode for continuous text analysis."""
        print(f"\n{self.colorize('GIBSEY TOKEN ANALYZER - INTERACTIVE MODE', 'header')}")
        print(f"Enter text to analyze, or type 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input(f"{self.colorize('> ', 'green')}").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                self.analyze_text(user_input, show_detailed=True)
                print()
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break
    
    def analyze_file(self, file_path: str):
        """Analyze text from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            print(f"Analyzing file: {file_path}")
            self.analyze_text(text, show_detailed=False)
            
            # Additional file-specific stats
            lines = text.split('\n')
            words = text.split()
            
            print(f"{self.colorize('FILE METRICS:', 'bold')}")
            print(f"  Lines:      {self.colorize(str(len(lines)), 'cyan')}")
            print(f"  Words:      {self.colorize(str(len(words)), 'cyan')}")
            print(f"  Avg tokens/line: {self.colorize(f'{self.count_tokens(text)/len(lines):.2f}', 'blue')}")
            
        except FileNotFoundError:
            print(f"{self.colorize('Error: File not found:', 'red')} {file_path}")
        except Exception as e:
            print(f"{self.colorize('Error reading file:', 'red')} {e}")
    
    def show_examples(self):
        """Show example usage with different types of text."""
        examples = [
            ("Simple greeting", "Hello, world!"),
            ("QDPI sequence", "<X_READ>This is a test<Y_INDEX>"),
            ("Character mentions", "The london-fox character meets jacklyn-variance in the story"),
            ("Mixed content", "<A_ASK>What does jacklyn-variance think about glyph-marrow?<Z_RECEIVE>"),
            ("Complex narrative", "In the underground tunnels beneath the theme park, jacklyn-variance monitors data streams while glyph-marrow navigates the recursive mysteries of the corpus.")
        ]
        
        print(f"\n{self.colorize('EXAMPLE ANALYSES', 'header')}")
        print(f"{self.colorize('=' * 50, 'header')}\n")
        
        for title, text in examples:
            print(f"{self.colorize(f'Example: {title}', 'bold')}")
            print(f"Text: \"{text}\"")
            
            token_count = self.count_tokens(text)
            tna_cost = self.calculate_tna_cost(text)
            special = self.detect_special_tokens(text)
            
            print(f"Tokens: {self.colorize(str(token_count), 'green')} | TNA: {self.colorize(f'{tna_cost:.3f}', 'yellow')}", end="")
            
            if special['qdpi'] or special['character']:
                special_list = special['qdpi'] + special['character']
                print(f" | Special: {self.colorize(', '.join(special_list[:3]), 'purple')}")
                if len(special_list) > 3:
                    print(f"   (+{len(special_list)-3} more)")
            else:
                print()
            
            print()

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Gibsey Token Visualization CLI Tool",
        epilog="Examples:\n"
               "  token_viz.py \"Hello world\"\n"
               "  token_viz.py --interactive\n"
               "  token_viz.py --file story.txt\n"
               "  token_viz.py --examples",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('text', nargs='?', help='Text to analyze')
    parser.add_argument('-i', '--interactive', action='store_true', 
                       help='Run in interactive mode')
    parser.add_argument('-f', '--file', help='Analyze text from file')
    parser.add_argument('-e', '--examples', action='store_true',
                       help='Show example analyses')
    parser.add_argument('--detailed', action='store_true',
                       help='Show detailed token breakdown')
    
    args = parser.parse_args()
    
    cli = TokenVizCLI()
    
    if args.examples:
        cli.show_examples()
    elif args.interactive:
        cli.interactive_mode()
    elif args.file:
        cli.analyze_file(args.file)
    elif args.text:
        cli.analyze_text(args.text, show_detailed=args.detailed or True)
    else:
        # No arguments provided, show help and examples
        parser.print_help()
        print()
        cli.show_examples()

if __name__ == '__main__':
    main()