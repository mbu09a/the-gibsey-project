import React, { useState } from 'react';
import { Prompt } from '../types/story';
import { useStory } from '../context/StoryContext';

interface BranchNavigatorProps {
  onBranchCreated?: (branchId: string) => void;
}

const BranchNavigator: React.FC<BranchNavigatorProps> = ({ onBranchCreated }) => {
  const { 
    currentPage, 
    currentColor, 
    getCurrentPrompts, 
    createBranch, 
    rotateSymbol, 
    getBranchTree,
    navigateToBranch
  } = useStory();
  
  const [selectedPrompt, setSelectedPrompt] = useState<Prompt | null>(null);
  const [userInput, setUserInput] = useState('');
  const [isCreatingBranch, setIsCreatingBranch] = useState(false);
  const [showBranches, setShowBranches] = useState(false);

  const prompts = getCurrentPrompts();
  const branches = getBranchTree();

  const handlePromptSelect = (prompt: Prompt) => {
    setSelectedPrompt(prompt);
    if (prompt.targetRotation) {
      rotateSymbol(prompt.targetRotation);
    }
  };

  const handleCreateBranch = async () => {
    if (!selectedPrompt || !userInput.trim()) return;

    setIsCreatingBranch(true);
    
    try {
      // Create user branch
      createBranch(selectedPrompt, userInput, 'user');
      
      // Simulate AI response (in real implementation, this would call the AI service)
      setTimeout(() => {
        const aiResponse = generateAIResponse(selectedPrompt, userInput);
        const aiBranchId = createBranch(selectedPrompt, aiResponse, 'ai');
        
        setIsCreatingBranch(false);
        setUserInput('');
        setSelectedPrompt(null);
        
        if (onBranchCreated) {
          onBranchCreated(aiBranchId);
        }
      }, 2000);
      
    } catch (error) {
      console.error('Error creating branch:', error);
      setIsCreatingBranch(false);
    }
  };

  const generateAIResponse = (prompt: Prompt, userInput: string): string => {
    // PRD-compliant AI response generation based on prompt type
    const characterName = getCurrentCharacterName();
    
    const responses = {
      character_prompt: `${characterName} considers the suggestion "${userInput}" and takes decisive action. The narrative pivots as new possibilities unfold from this character-driven moment...`,
      user_prompt: `${characterName} responds to your query "${userInput}" with characteristic insight. The conversation reveals hidden depths of the character's perspective and motivations...`,
      character_response: `In response to "${userInput}", ${characterName} provides a detailed answer that deepens the narrative understanding and opens new avenues for exploration...`
    };
    
    return responses[prompt.type] || `${characterName} acknowledges your input: "${userInput}" and responds in unexpected ways...`;
  };

  const getCurrentCharacterName = (): string => {
    if (!currentPage) return 'The Character';
    const characterMap: Record<string, string> = {
      'an-author': 'The Author',
      'london-fox': 'London Fox',
      'glyph-marrow': 'Glyph Marrow',
      'phillip-bafflemint': 'Phillip Bafflemint',
      'jacklyn-variance': 'Jacklyn Variance',
      'oren-progresso': 'Oren Progresso',
      'natalie-weissman': 'Natalie Weissman',
      'princhetta': 'Princhetta',
      'copy-e-right': 'Copy-E-Right',
      'arieol-owlist': 'Arieol Owlist',
      'jack-parlance': 'Jack Parlance',
      'manny-valentinas': 'Manny Valentinas',
      'shamrock-stillman': 'Shamrock Stillman',
      'todd-fishbone': 'Todd Fishbone'
    };
    return characterMap[currentPage.symbolId] || 'The Character';
  };

  if (!currentPage) return null;

  return (
    <div className="branch-navigator mt-6">

      {/* Branch Tree Viewer */}
      {branches.length > 0 && (
        <div className="mb-6">
          <button
            onClick={() => setShowBranches(!showBranches)}
            className="text-sm font-crt mb-3 opacity-70 hover:opacity-100 transition-opacity"
            style={{ color: currentColor }}
          >
            {showBranches ? '↓' : '→'} {branches.length} narrative branch{branches.length !== 1 ? 'es' : ''}
          </button>
          
          {showBranches && (
            <div className="branch-tree pl-4 border-l-2 border-opacity-30" style={{ borderColor: currentColor }}>
              {branches.map((branch, index) => (
                <div 
                  key={branch.pageId}
                  className="branch-item mb-3 p-3 border rounded-sm cursor-pointer transition-all hover:scale-105"
                  style={{
                    borderColor: currentColor,
                    background: `${currentColor}08`
                  }}
                  onClick={() => navigateToBranch(branch.pageId)}
                >
                  <div className="text-xs font-crt opacity-70 mb-1" style={{ color: currentColor }}>
                    {branch.createdBy === 'user' ? '👤 User' : '🤖 AI'} • {branch.timestamp.toLocaleTimeString()}
                  </div>
                  <div className="text-sm font-crt" style={{ color: currentColor }}>
                    Branch {index + 1}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}


      {/* User Input for Branch Creation */}
      {selectedPrompt && (
        <div className="branch-creation mt-4 p-4 border rounded-sm" 
             style={{ 
               borderColor: currentColor,
               background: `${currentColor}08`,
               boxShadow: `0 0 15px ${currentColor}20`
             }}>
          <div className="text-sm font-crt mb-3" style={{ color: currentColor }}>
            Selected: {selectedPrompt.type.replace('_', ' ').toUpperCase()} → {selectedPrompt.targetRotation}°
          </div>
          <div className="text-xs font-crt mb-3 opacity-70" style={{ color: currentColor }}>
            {selectedPrompt.description}
          </div>
          
          <textarea
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Enter your narrative intervention..."
            disabled={isCreatingBranch}
            className="w-full h-24 p-3 bg-transparent border font-crt text-sm resize-none
                       focus:outline-none focus:ring-2 disabled:opacity-50"
            style={{
              borderColor: currentColor,
              color: currentColor,
              backgroundColor: `${currentColor}05`
            }}
          />
          
          <div className="flex justify-between items-center mt-3">
            <button
              onClick={() => setSelectedPrompt(null)}
              disabled={isCreatingBranch}
              className="px-4 py-2 border font-crt text-sm transition-all
                         disabled:opacity-50 hover:bg-opacity-20"
              style={{
                borderColor: currentColor,
                color: currentColor
              }}
            >
              Cancel
            </button>
            
            <button
              onClick={handleCreateBranch}
              disabled={isCreatingBranch || !userInput.trim()}
              className="px-4 py-2 border font-crt text-sm transition-all
                         disabled:opacity-50 disabled:cursor-not-allowed"
              style={{
                borderColor: currentColor,
                color: currentColor,
                backgroundColor: userInput.trim() ? `${currentColor}20` : 'transparent'
              }}
            >
              {isCreatingBranch ? 'Creating Branch...' : 'Create Branch'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default BranchNavigator;