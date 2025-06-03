import React from 'react';
import { useStory } from '../context/StoryContext';

const SymbolTag: React.FC = () => {
  const { currentSymbol, currentColor, currentPage } = useStory();

  if (!currentSymbol || !currentPage) {
    return null;
  }

  return (
    <div className="symbol-tag-container flex items-center justify-center mb-6">
      <div 
        className="symbol-tag inline-flex items-center px-6 py-3 rounded-md font-crt text-lg
                   transition-all animate-pulse"
        style={{ 
          backgroundColor: `${currentColor}15`,
          borderColor: currentColor,
          borderWidth: '2px',
          borderStyle: 'solid',
          color: currentColor,
          boxShadow: `0 0 30px ${currentColor}40, inset 0 0 20px ${currentColor}20`,
          textShadow: `0 0 10px ${currentColor}`
        }}
      >
        <span className="symbol-tag__label text-sm opacity-75 mr-3">CORPUS:</span>
        <span className="symbol-tag__bracket">[</span>
        <span className="symbol-tag__text mx-2 font-bold">{currentSymbol.toUpperCase()}</span>
        <span className="symbol-tag__bracket">]</span>
      </div>
    </div>
  );
};

export default SymbolTag;