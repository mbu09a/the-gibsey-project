// Symbol to color mapping for corpus characters
export const symbolColors: Record<string, string> = {
  // Main Characters
  'an-author': '#34FF78',           // Terminal green
  'london-fox': '#FF3B3B',          // Terminal red
  'glyph-marrow': '#00A2FF',        // Terminal blue
  'glyph-marrow-chapter-1': '#00A2FF', // Terminal blue
  'glyph-marrow-chapter-2': '#00A2FF', // Terminal blue  
  'glyph-marrow-chapter-3': '#00A2FF', // Terminal blue
  'phillip-bafflemint': '#FFB33B',  // Terminal orange
  'jacklyn-variance': '#B33BFF',    // Terminal purple
  'oren-progresso': '#3BB3FF',      // Terminal blue
  'old-natalie': '#FFFF3B',         // Terminal yellow
  'princhetta': '#FF3BFF',          // Terminal magenta
  'copy-e-right': '#3BFFFF',        // Terminal cyan
  'new-natalie': '#B3FF3B',         // Lime green
  'arieol-owlist': '#FF943B',       // Amber
  'jack-parlance': '#943BFF',       // Violet
  'manny-valentinas': '#3B94FF',    // Sky blue
  'shamrock-stillman': '#94FF3B',   // Bright green
  'todd-fishbone': '#FF3B94',       // Pink
  'the-author': '#FFFFFF',          // White
  
  // Default fallback
  default: '#34FF78'                // Terminal green
};

// Export corpusColors as an alias for symbolColors (used in StoryContext)
export const corpusColors = symbolColors;