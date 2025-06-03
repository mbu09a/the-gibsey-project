import React from 'react';
import { useStory } from '../context/StoryContext';
import CorpusSymbol from './CorpusSymbol';

const SymbolIndex: React.FC = () => {
  const { getAllSymbols, navigateToSymbol, currentSymbol, currentColor, currentPage } = useStory();
  const symbols = getAllSymbols();

  return (
    <div className="symbol-index h-full flex flex-col">
      <h3 className="text-lg font-bold mb-4 font-crt"
          style={{ color: currentColor }}>
        TABLE OF CONTENTS
      </h3>
      <div className="symbol-index__list flex-1 overflow-y-auto pr-2 custom-scrollbar">
        <ul className="space-y-2">
          {symbols.map((symbolData) => {
            // Check if this TOC entry is active based on current page
            let isActive = false;
            if (symbolData.id.startsWith('glyph-marrow-chapter-')) {
              // For chapter entries, check if current page matches this chapter
              isActive = currentPage?.symbolId === 'glyph-marrow' && 
                         symbolData.id.includes((currentPage as any)?.chapter?.toLowerCase().replace(/\s+/g, '-') || '');
            } else {
              isActive = currentSymbol === symbolData.id;
            }
            
            return (
              <li key={symbolData.id}>
                <button
                  className="w-full text-left p-3 rounded transition-all font-crt text-sm"
                  onClick={() => navigateToSymbol(symbolData.id)}
                  style={{ 
                    color: symbolData.color, // Always use the symbol's original color
                    borderColor: isActive ? symbolData.color : 'transparent',
                    borderWidth: '1px',
                    borderStyle: 'solid',
                    boxShadow: isActive ? `0 0 20px ${symbolData.color}40` : 'none',
                    textShadow: isActive ? `0 0 5px ${symbolData.color}` : 'none',
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
                  <div className="flex items-center gap-3">
                    <div className="w-6 h-6 flex-shrink-0 flex items-center justify-center">
                      <CorpusSymbol 
                        symbolId={symbolData.id.startsWith('glyph-marrow-') ? 'glyph-marrow' : symbolData.id}
                        color={symbolData.color}
                        size="20px"
                      />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <span className="symbol-index__symbol">
                          [{symbolData.id}]
                        </span>
                        <span className="symbol-index__count text-xs opacity-50">
                          {symbolData.pageCount} {symbolData.pageCount === 1 ? 'page' : 'pages'}
                        </span>
                      </div>
                      <div className="symbol-index__name mt-1 text-xs opacity-75">
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
      <div className="mt-4 pt-4 border-t border-opacity-20"
           style={{ borderColor: currentColor }}>
        <p className="text-xs font-crt opacity-50 text-center"
           style={{ color: currentColor }}>
          Use ← → keys to navigate
        </p>
      </div>
    </div>
  );
};

export default SymbolIndex;