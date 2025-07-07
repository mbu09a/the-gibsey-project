import React from 'react';
import { useStory } from '../context/StoryContext';
import CorpusSymbol from './CorpusSymbol';

const SymbolIndex: React.FC = () => {
  const { getAllSymbols, navigateToSymbol, currentSymbol, currentColor, currentPage } = useStory();
  const symbols = getAllSymbols();

  return (
    <div className="symbol-index h-full flex flex-col">
      <h3 className="text-base sm:text-lg font-bold mb-3 sm:mb-4 font-crt"
          style={{ color: currentColor }}>
        TABLE OF CONTENTS
      </h3>
      <div className="symbol-index__list flex-1 overflow-y-auto pr-1 sm:pr-2 custom-scrollbar">
        <ul className="space-y-1 sm:space-y-2">
          {symbols.map((symbolData) => {
            // Check if this TOC entry is active based on current page
            let isActive = false;
            if (symbolData.id.startsWith('glyph-marrow-chapter-') || symbolData.id.startsWith('phillip-bafflemint-chapter-') || symbolData.id.startsWith('jacklyn-variance-part-') || symbolData.id.startsWith('arieol-owlist-part-') || symbolData.id.startsWith('manny-valentinas-chapter-') || symbolData.id.startsWith('shamrock-stillman-chapter-')) {
              // For chapter/part entries, check if current page matches this chapter/part
              const symbolId = symbolData.id.startsWith('glyph-marrow-chapter-') ? 'glyph-marrow' : 
                               symbolData.id.startsWith('phillip-bafflemint-chapter-') ? 'phillip-bafflemint' : 
                               symbolData.id.startsWith('jacklyn-variance-part-') ? 'jacklyn-variance' : 
                               symbolData.id.startsWith('arieol-owlist-part-') ? 'arieol-owlist' : 
                               symbolData.id.startsWith('manny-valentinas-chapter-') ? 'manny-valentinas' : 'shamrock-stillman';
              isActive = currentPage?.symbolId === symbolId && 
                         symbolData.id.includes((currentPage as any)?.chapter?.toLowerCase().replace(/\s+/g, '-') || '');
            } else {
              isActive = currentSymbol === symbolData.id;
            }
            
            return (
              <li key={symbolData.id}>
                <button
                  className="w-full text-left p-2 sm:p-3 rounded transition-all font-crt text-xs sm:text-sm touch-manipulation"
                  onClick={() => navigateToSymbol(symbolData.id)}
                  style={{ 
                    color: symbolData.color, // Always use the symbol's original color
                    borderColor: isActive ? symbolData.color : 'transparent',
                    borderWidth: '1px',
                    borderStyle: 'solid',
                    boxShadow: isActive ? `0 0 15px ${symbolData.color}40` : 'none',
                    textShadow: isActive ? `0 0 3px ${symbolData.color}` : 'none',
                    backgroundColor: isActive ? `${symbolData.color}20` : 'transparent'
                  }}
                  onMouseEnter={(e) => {
                    if (!isActive) {
                      e.currentTarget.style.backgroundColor = `${currentColor}10`;
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (!isActive) {
                      e.currentTarget.style.backgroundColor = 'transparent';
                    }
                  }}
                >
                  <div className="flex items-center gap-2 sm:gap-3">
                    <div className="w-5 h-5 sm:w-6 sm:h-6 flex-shrink-0 flex items-center justify-center">
                      <CorpusSymbol 
                        symbolId={
                          symbolData.id.startsWith('glyph-marrow-') ? 'glyph-marrow' :
                          symbolData.id.startsWith('phillip-bafflemint-') ? 'phillip-bafflemint' :
                          symbolData.id.startsWith('jacklyn-variance-') ? 'jacklyn-variance' :
                          symbolData.id.startsWith('arieol-owlist-') ? 'arieol-owlist' :
                          symbolData.id.startsWith('manny-valentinas-') ? 'manny-valentinas' :
                          symbolData.id.startsWith('shamrock-stillman-') ? 'shamrock-stillman' :
                          symbolData.id
                        }
                        color={symbolData.color}
                        size="16px"
                        className="sm:w-5 sm:h-5"
                        enableQDPI={true}
                        onClick={() => {}} // Prevent double navigation
                      />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-2">
                        <span className="symbol-index__symbol truncate">
                          <span className="hidden sm:inline">[</span>{symbolData.id}<span className="hidden sm:inline">]</span>
                        </span>
                        <span className="symbol-index__count text-xs opacity-50 flex-shrink-0">
                          {symbolData.pageCount}<span className="hidden sm:inline"> {symbolData.pageCount === 1 ? 'page' : 'pages'}</span>
                        </span>
                      </div>
                      <div className="symbol-index__name mt-1 text-xs opacity-75 truncate">
                        {symbolData.name}
                      </div>
                    </div>
                  </div>
                </button>
              </li>
            );
          })}
        </ul>
      </div>
      <div className="mt-3 sm:mt-4 pt-3 sm:pt-4 border-t border-opacity-20"
           style={{ borderColor: currentColor }}>
        <p className="text-xs font-crt opacity-50 text-center"
           style={{ color: currentColor }}>
          <span className="hidden sm:inline">Use ← → keys to navigate</span>
          <span className="sm:hidden">Tap to navigate</span>
        </p>
      </div>
    </div>
  );
};

export default SymbolIndex;