// Symbol to color mapping for corpus characters
export const symbolColors: Record<string, string> = {
  // Main Characters
  'an-author': '#34FF78',           // Terminal green
  'london-fox': '#FF3B3B',          // Terminal red
  'glyph-marrow': '#00A2FF',        // Terminal blue
  'glyph-marrow-chapter-1': '#00A2FF', // Terminal blue
  'glyph-marrow-chapter-2': '#00A2FF', // Terminal blue  
  'glyph-marrow-chapter-3': '#00A2FF', // Terminal blue
  'phillip-bafflemint': '#FFFF33',  // Terminal yellow
  'jacklyn-variance': '#FF00FF',    // Terminal magenta
  'oren-progresso': '#00FFAA',      // Terminal cyan-green
  'old-natalie': '#7A3CFF',         // Terminal purple
  'princhetta': '#AAAAAA',          // Gray
  'cop-e-right': '#FFFFFF',         // White
  'new-natalie': '#CC66FF',         // Pinkish purple
  'arieol-owlist': '#99CCFF',       // Light blue
  'jack-parlance': '#FF3385',       // Pink/Magenta
  'manny-valentinas': '#FFB000',    // Orange/Gold
  'shamrock-stillman': '#00FFFF',   // Cyan
  'todd-fishbone': '#FF7744',       // Orange
  'the-author': '#BFFF00',          // Bright lime
  
  // Default fallback
  default: '#34FF78'                // Terminal green
};

// Export corpusColors as an alias for symbolColors (used in StoryContext)
export const corpusColors = symbolColors;