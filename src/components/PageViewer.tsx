import React, { useEffect, useState } from 'react';
import { useStory } from '../context/StoryContext';
import { useTypewriter } from '../hooks/useTypewriter';
import CorpusSymbol from './CorpusSymbol';

const PageViewer: React.FC = () => {
  const { currentPage, currentColor, nextPage, previousPage, currentPageIndex, pages } = useStory();
  const [key, setKey] = useState(0);

  // Reset animation when page changes
  useEffect(() => {
    setKey(prev => prev + 1);
  }, [currentPageIndex]);

  const { displayedText, isTyping } = useTypewriter(
    currentPage?.text || '',
    {
      speed: 20, // Adjust typing speed (lower = faster)
      delay: 500 // Initial delay before typing starts
    }
  );

  if (!currentPage) {
    return (
      <div className="page-viewer flex items-center justify-center h-full">
        <p className="text-phosphor-green opacity-50 animate-pulse">Loading...</p>
      </div>
    );
  }

  return (
    <div className="page-viewer h-full flex flex-col">
      {/* AI Assistant Header */}
      <div className="page-viewer__ai-header mb-4 pb-4 border-b border-opacity-30"
           style={{ borderColor: currentColor }}>
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full p-1 flex items-center justify-center"
               style={{ boxShadow: `0 0 20px ${currentColor}40` }}>
            <CorpusSymbol 
              symbolId={currentPage.symbolId}
              color={currentColor}
              size="32px"
            />
          </div>
          <div>
            <div className="text-sm font-crt" style={{ color: currentColor }}>
              {currentPage.symbolId === 'london-fox' ? 'Synchromy-S.S.S.T.E.R.Y' : 
               currentPage.symbolId === 'glyph-marrow' ? 'Glyph Marrow' :
               currentPage.title}
            </div>
            <div className="text-xs opacity-50 font-crt" style={{ color: currentColor }}>
              MCP: [{currentPage.symbolId}] • Page {currentPageIndex + 1} of {pages.length}
            </div>
          </div>
        </div>
      </div>
      
      {/* Content Area */}
      <div className="page-viewer__content flex-1 overflow-y-auto pr-4 custom-scrollbar">
        <div className="ai-message-bubble"
             style={{
               background: `${currentColor}0D`, // 5% opacity
               border: `1px solid ${currentColor}33`, // 20% opacity
               boxShadow: `inset 0 0 20px ${currentColor}1A, 0 0 30px ${currentColor}1A` // 10% opacity
             }}>
          <h3 className="text-lg font-crt mb-3" style={{ color: currentColor }}>
            {currentPage.title}
          </h3>
          <div className="relative">
            <p className="whitespace-pre-wrap font-crt leading-relaxed" key={key} style={{ color: currentColor }}>
              {displayedText}
              {isTyping && (
                <span className="inline-block w-2 h-4 ml-1 animate-pulse" 
                      style={{ 
                        backgroundColor: currentColor,
                        animation: 'blink 1s infinite',
                        verticalAlign: 'text-bottom'
                      }}>
                </span>
              )}
            </p>
          </div>
        </div>
      </div>
      
      {/* Navigation */}
      <div className="page-viewer__navigation mt-6 flex items-center justify-between">
        <button
          onClick={previousPage}
          disabled={currentPageIndex === 0 || isTyping}
          className="px-4 py-2 font-crt border transition-all
                     disabled:opacity-30 disabled:cursor-not-allowed"
          style={{
            color: currentColor,
            borderColor: currentColor,
            boxShadow: currentPageIndex > 0 && !isTyping ? `0 0 20px ${currentColor}80` : 'none'
          }}
          onMouseEnter={(e) => {
            if (!isTyping && currentPageIndex > 0) {
              e.currentTarget.style.backgroundColor = currentColor;
              e.currentTarget.style.color = '#0a0a0a';
            }
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'transparent';
            e.currentTarget.style.color = currentColor;
          }}
        >
          ← Previous
        </button>
        
        <div className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
          {isTyping ? 'Generating response...' : `Section ${currentPage.section || 1}`}
        </div>
        
        <button
          onClick={nextPage}
          disabled={currentPageIndex === pages.length - 1 || isTyping}
          className="px-4 py-2 font-crt border transition-all
                     disabled:opacity-30 disabled:cursor-not-allowed"
          style={{
            color: currentColor,
            borderColor: currentColor,
            boxShadow: currentPageIndex < pages.length - 1 && !isTyping ? `0 0 20px ${currentColor}80` : 'none'
          }}
          onMouseEnter={(e) => {
            if (!isTyping && currentPageIndex < pages.length - 1) {
              e.currentTarget.style.backgroundColor = currentColor;
              e.currentTarget.style.color = '#0a0a0a';
            }
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'transparent';
            e.currentTarget.style.color = currentColor;
          }}
        >
          Next →
        </button>
      </div>
    </div>
  );
};

export default PageViewer;