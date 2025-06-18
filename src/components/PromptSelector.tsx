import React, { useEffect, useState } from 'react';
import { Prompt, PromptType, SymbolRotation } from '../types/story';
import { useStory } from '../context/StoryContext';
import { generatePrompts, GeneratedPrompt } from '../utils/promptExtractor';
import CorpusSymbol from './CorpusSymbol';

interface PromptSelectorProps {
  prompts?: Prompt[]; // Made optional since we'll generate our own
  onPromptSelect: (prompt: Prompt) => void;
  disabled?: boolean;
}

const PromptSelector: React.FC<PromptSelectorProps> = ({ 
  onPromptSelect, 
  disabled = false 
}) => {
  const { currentColor, currentPage } = useStory();
  const [contextPrompts, setContextPrompts] = useState<GeneratedPrompt[]>([]);

  // Generate context-aware prompts when page changes
  useEffect(() => {
    if (currentPage) {
      const generated = generatePrompts(currentPage.text);
      setContextPrompts(generated);
    }
  }, [currentPage]);

  // Convert GeneratedPrompt to Prompt for compatibility
  const convertToPrompt = (generated: GeneratedPrompt): Prompt => ({
    id: generated.id,
    type: 'user_prompt' as PromptType, // All context prompts are user queries
    text: generated.question,
    targetRotation: 90 as SymbolRotation, // Character response rotation
    description: `Ask ${generated.characterId} about ${generated.concept}`
  });

  // Removed unused helper functions - using direct character assignment now

  return (
    <div className="prompt-selector mt-3">
      <div className="text-xs font-crt opacity-70 mb-2" style={{ color: currentColor }}>
        Ask about this page:
      </div>
      
      <div className="space-y-2">
        {contextPrompts.map((generated) => {
          const prompt = convertToPrompt(generated);
          return (
            <button
              key={generated.id}
              onClick={() => onPromptSelect(prompt)}
              disabled={disabled}
              className="prompt-option p-2 border rounded-sm transition-all duration-200 
                         disabled:opacity-30 disabled:cursor-not-allowed
                         hover:scale-102 active:scale-98 text-left group w-full flex items-center gap-2"
              style={{
                borderColor: generated.color,
                background: `${generated.color}08`,
                boxShadow: `0 0 5px ${generated.color}20`
              }}
              onMouseEnter={(e) => {
                if (!disabled) {
                  e.currentTarget.style.backgroundColor = `${generated.color}15`;
                  e.currentTarget.style.boxShadow = `0 0 10px ${generated.color}40`;
                }
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = `${generated.color}08`;
                e.currentTarget.style.boxShadow = `0 0 5px ${generated.color}20`;
              }}
            >
              {/* Character Symbol (90° rotated) */}
              <div
                className="transition-transform duration-300 flex-shrink-0"
                style={{ transform: 'rotate(90deg)' }}
              >
                <CorpusSymbol 
                  symbolId={generated.symbolId} 
                  color={generated.color} 
                  size="16px"
                />
              </div>
              
              {/* Question Text */}
              <div className="flex-1 min-w-0">
                <div className="text-sm font-crt" style={{ color: generated.color }}>
                  {generated.question}
                </div>
                <div className="text-xs font-crt opacity-60 mt-1" style={{ color: generated.color }}>
                  Ask {generated.characterId.replace('-', ' ')}
                </div>
              </div>
            </button>
          );
        })}
      </div>
      
      {contextPrompts.length === 0 && (
        <div className="text-center py-4 opacity-50">
          <div className="text-sm font-crt" style={{ color: currentColor }}>
            No questions generated for this page
          </div>
        </div>
      )}
    </div>
  );
};

export default PromptSelector;