import React, { useEffect, useState } from 'react';
import { useStory } from '../context/StoryContext';
import { useTypewriter } from '../hooks/useTypewriter';
import CorpusSymbol from './CorpusSymbol';
import BranchNavigator from './BranchNavigator';
import LondonFoxChat from './LondonFoxChat';
import GlyphMarrowChat from './GlyphMarrowChat';
import PhillipBafflemintChat from './PhillipBafflemintChat';
import JacklynVarianceChat from './JacklynVarianceChat';
import OrenProgressoChat from './OrenProgressoChat';
import OldNatalieWeissmanChat from './OldNatalieWeissmanChat';
import NewNatalieWeissmanChat from './NewNatalieWeissmanChat';
import ArieolOwlistChat from './ArieolOwlistChat';
import JackParlanceChat from './JackParlanceChat';
import PrinchettaChat from './PrinchettaChat';
import CopERightChat from './CopERightChat';
import ShamrockStillmanChat from './ShamrockStillmanChat';
import ToddFishboneChat from './ToddFishboneChat';
import StreamingCharacterChat from './StreamingCharacterChat';

const PageViewer: React.FC = () => {
  const { currentPage, currentColor, nextPage, previousPage, currentPageIndex, pages } = useStory();
  const [key, setKey] = useState(0);
  const [isLondonChatOpen, setIsLondonChatOpen] = useState(false);
  const [isGlyphChatOpen, setIsGlyphChatOpen] = useState(false);
  const [isPhillipChatOpen, setIsPhillipChatOpen] = useState(false);
  const [isJacklynChatOpen, setIsJacklynChatOpen] = useState(false);
  const [isOrenChatOpen, setIsOrenChatOpen] = useState(false);
  const [isOldNatalieChatOpen, setIsOldNatalieChatOpen] = useState(false);
  const [isNewNatalieChatOpen, setIsNewNatalieChatOpen] = useState(false);
  const [isArieolChatOpen, setIsArieolChatOpen] = useState(false);
  const [isJackChatOpen, setIsJackChatOpen] = useState(false);
  const [isPrinchettaChatOpen, setIsPrinchettaChatOpen] = useState(false);
  const [isCopERightChatOpen, setIsCopERightChatOpen] = useState(false);
  const [isShamrockChatOpen, setIsShamrockChatOpen] = useState(false);
  const [isToddChatOpen, setIsToddChatOpen] = useState(false);
  const [isStreamingChatOpen, setIsStreamingChatOpen] = useState(false);
  const [selectedCharacter, setSelectedCharacter] = useState<{
    id: string;
    name: string;
    color: string;
    initials: string;
  } | null>(null);

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
      {/* AI Assistant Header - responsive */}
      <div className="page-viewer__ai-header mb-3 sm:mb-4 pb-3 sm:pb-4 border-b border-opacity-30"
           style={{ borderColor: currentColor }}>
        <div className="flex items-center gap-2 sm:gap-3">
          <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-full p-1 flex items-center justify-center flex-shrink-0"
               style={{ boxShadow: `0 0 15px ${currentColor}40` }}>
            <CorpusSymbol 
              symbolId={currentPage.symbolId}
              color={currentColor}
              size="24px"
              className="sm:w-8 sm:h-8"
            />
          </div>
          <div className="min-w-0 flex-1">
            <div className="text-xs sm:text-sm font-crt truncate" style={{ color: currentColor }}>
              {currentPage.symbolId === 'london-fox' ? 'Synchromy-S.S.S.T.E.R.Y' : 
               currentPage.symbolId === 'glyph-marrow' ? 'Glyph Marrow' :
               currentPage.title}
            </div>
            <div className="text-xs opacity-50 font-crt" style={{ color: currentColor }}>
              <span className="hidden sm:inline">MCP: [{currentPage.symbolId}] • </span>
              Page {currentPageIndex + 1} of {pages.length}
            </div>
          </div>
          
          {/* Chat Buttons - Two rows, 5 per row */}
          <div className="flex flex-col gap-1 ml-2">
            {/* Top row */}
            <div className="flex gap-1">
              {/* London Fox Button - Red when available */}
              <button
                onClick={() => setIsLondonChatOpen(true)}
                className="px-1 py-1 border font-crt text-xs transition-all hover:bg-opacity-20"
                style={{
                  borderColor: '#FF3B3B',
                  color: '#FF3B3B',
                  backgroundColor: 'transparent'
                }}
                title="Debate with London Fox"
              >
                [LONDON]
              </button>
              
              {/* Glyph Marrow Button - Blue when available */}
              <button
                onClick={() => setIsGlyphChatOpen(true)}
                className="px-1 py-1 border font-crt text-xs transition-all hover:bg-opacity-20"
                style={{
                  borderColor: '#00A2FF',
                  color: '#00A2FF',
                  backgroundColor: 'transparent'
                }}
                title="Queue with Glyph Marrow"
              >
                [GLYPH]
              </button>
              
              {/* Phillip Bafflemint Button - Yellow when available */}
              <button
                onClick={() => setIsPhillipChatOpen(true)}
                className="px-1 py-1 border font-crt text-xs transition-all hover:bg-opacity-20"
                style={{
                  borderColor: '#FFFF33',
                  color: '#FFFF33',
                  backgroundColor: 'transparent'
                }}
                title="Investigate with Phillip Bafflemint"
              >
                [PHILLIP]
              </button>
              
              {/* Jacklyn Variance Button - Magenta when available */}
              <button
                onClick={() => setIsJacklynChatOpen(true)}
                className="px-1 py-1 border font-crt text-xs transition-all hover:bg-opacity-20"
                style={{
                  borderColor: '#FF00FF',
                  color: '#FF00FF',
                  backgroundColor: 'transparent'
                }}
                title="Analyze with Jacklyn Variance"
              >
                [JACKLYN]
              </button>
              
              {/* Oren Progresso Button - Cyan-green when available */}
              <button
                onClick={() => setIsOrenChatOpen(true)}
                className="px-1 py-1 border font-crt text-xs transition-all hover:bg-opacity-20"
                style={{
                  borderColor: '#00FFAA',
                  color: '#00FFAA',
                  backgroundColor: 'transparent'
                }}
                title="Negotiate with Oren Progresso"
              >
                [OREN]
              </button>
            </div>
            
            {/* Bottom row */}
            <div className="flex gap-1">
              {/* Old Natalie Weissman Button - Deep purple when available */}
              <button
                onClick={() => setIsOldNatalieChatOpen(true)}
                className="px-1 py-1 border font-crt text-xs transition-all hover:bg-opacity-20"
                style={{
                  borderColor: '#9932CC',
                  color: '#9932CC',
                  backgroundColor: 'transparent'
                }}
                title="Navigate memory palace with Old Natalie"
              >
                [OLD NAT]
              </button>
              
              {/* New Natalie Weissman Button - Medium purple when available */}
              <button
                onClick={() => setIsNewNatalieChatOpen(true)}
                className="px-1 py-1 border font-crt text-xs transition-all hover:bg-opacity-20"
                style={{
                  borderColor: '#BA55D3',
                  color: '#BA55D3',
                  backgroundColor: 'transparent'
                }}
                title="Race the clock with New Natalie"
              >
                [NEW NAT]
              </button>
              
              {/* Arieol Owlist Button - Medium slate blue when available */}
              <button
                onClick={() => setIsArieolChatOpen(true)}
                className="px-1 py-1 border font-crt text-xs transition-all hover:bg-opacity-20"
                style={{
                  borderColor: '#9370DB',
                  color: '#9370DB',
                  backgroundColor: 'transparent'
                }}
                title="Shapeshift with Arieol Owlist"
              >
                [ARIEOL]
              </button>
              
              {/* Jack Parlance Button - Saddle brown when available */}
              <button
                onClick={() => setIsJackChatOpen(true)}
                className="px-1 py-1 border font-crt text-xs transition-all hover:bg-opacity-20"
                style={{
                  borderColor: '#FF3385',
                  color: '#FF3385',
                  backgroundColor: 'transparent'
                }}
                title="Debug the unfinished with Jack Parlance"
              >
                [JACK]
              </button>
              
              {/* Princhetta Button - Deep pink when available */}
              <button
                onClick={() => setIsPrinchettaChatOpen(true)}
                className="px-1 py-1 border font-crt text-xs transition-all hover:bg-opacity-20"
                style={{
                  borderColor: '#AAAAAA',
                  color: '#AAAAAA',
                  backgroundColor: 'transparent'
                }}
                title="Test consciousness with Princhetta"
              >
                [PRIN]
              </button>
            </div>
            
            {/* Third row for Cop-E-Right, Shamrock, and Todd */}
            <div className="flex gap-1">
              {/* Cop-E-Right Button - Gold when available */}
              <button
                onClick={() => setIsCopERightChatOpen(true)}
                className="px-1 py-1 border font-crt text-xs transition-all hover:bg-opacity-20"
                style={{
                  borderColor: '#FFD700',
                  color: '#FFD700',
                  backgroundColor: 'transparent'
                }}
                title="Litigate with Cop‑E‑Right"
              >
                [COP‑E‑RIGHT]
              </button>
              
              {/* Shamrock Stillman Button - Shamrock green when available */}
              <button
                onClick={() => setIsShamrockChatOpen(true)}
                className="px-1 py-1 border font-crt text-xs transition-all hover:bg-opacity-20"
                style={{
                  borderColor: '#00FFFF',
                  color: '#00FFFF',
                  backgroundColor: 'transparent'
                }}
                title="Compartmentalize with Shamrock Stillman"
              >
                [SHAMROCK]
              </button>
              
              {/* Todd Fishbone Button - Burnt orange when available */}
              <button
                onClick={() => setIsToddChatOpen(true)}
                className="px-1 py-1 border font-crt text-xs transition-all hover:bg-opacity-20"
                style={{
                  borderColor: '#FF7744',
                  color: '#FF7744',
                  backgroundColor: 'transparent'
                }}
                title="Extract synchronicities with Todd Fishbone"
              >
                [TODD]
              </button>
            </div>
            
            {/* Real AI Streaming Chat Section */}
            <div className="mt-4 pt-3 border-t border-opacity-30" style={{ borderColor: currentColor }}>
              <div className="text-xs font-crt opacity-75 mb-2 text-center" style={{ color: currentColor }}>
                Real-Time AI Streaming
              </div>
              <div className="flex flex-wrap gap-1 justify-center">
                <button
                  onClick={() => {
                    setSelectedCharacter({
                      id: 'jacklyn-variance',
                      name: 'Jacklyn Variance',
                      color: '#FFAA00',
                      initials: 'JV'
                    });
                    setIsStreamingChatOpen(true);
                  }}
                  className="px-2 py-1 border font-crt text-xs transition-all hover:bg-opacity-20 animate-pulse"
                  style={{
                    borderColor: '#FFAA00',
                    color: '#FFAA00',
                    backgroundColor: 'transparent',
                    boxShadow: `0 0 10px #FFAA0040`
                  }}
                  title="Chat with real AI Jacklyn Variance (Ollama)"
                >
                  🤖 JACKLYN
                </button>
                
                <button
                  onClick={() => {
                    setSelectedCharacter({
                      id: 'arieol-owlist',
                      name: 'Arieol Owlist',
                      color: '#9370DB',
                      initials: 'AO'
                    });
                    setIsStreamingChatOpen(true);
                  }}
                  className="px-2 py-1 border font-crt text-xs transition-all hover:bg-opacity-20 animate-pulse"
                  style={{
                    borderColor: '#9370DB',
                    color: '#9370DB',
                    backgroundColor: 'transparent',
                    boxShadow: `0 0 10px #9370DB40`
                  }}
                  title="Chat with real AI Arieol Owlist (Ollama)"
                >
                  🤖 ARIEOL
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Content Area - responsive */}
      <div className="page-viewer__content flex-1 overflow-y-auto pr-2 sm:pr-4 custom-scrollbar">
        <div className="ai-message-bubble"
             style={{
               background: `${currentColor}0D`, // 5% opacity
               border: `1px solid ${currentColor}33`, // 20% opacity
               boxShadow: `inset 0 0 15px ${currentColor}1A, 0 0 20px ${currentColor}1A` // 10% opacity
             }}>
          <h3 className="text-base sm:text-lg font-crt mb-2 sm:mb-3" style={{ color: currentColor }}>
            {currentPage.title}
          </h3>
          <div className="relative">
            <p className="whitespace-pre-wrap font-crt leading-relaxed text-sm sm:text-base" 
               key={key} style={{ color: currentColor }}>
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

      {/* Mycelial Branch Navigator */}
      <BranchNavigator onBranchCreated={(branchId) => console.log('Branch created:', branchId)} />
      
      {/* Navigation - responsive */}
      <div className="page-viewer__navigation mt-4 sm:mt-6 flex flex-col sm:flex-row items-center justify-between gap-3 sm:gap-0">
        {/* Mobile: Section info at top */}
        <div className="sm:hidden text-xs font-crt opacity-50 order-1" style={{ color: currentColor }}>
          {isTyping ? 'Generating response...' : `Section ${currentPage.section || 1}`}
        </div>
        
        {/* Navigation buttons */}
        <div className="flex items-center justify-between w-full sm:w-auto gap-4 order-2 sm:order-none">
          <button
            onClick={previousPage}
            disabled={currentPageIndex === 0 || isTyping}
            className="px-3 py-2 sm:px-4 font-crt border transition-all text-sm
                       disabled:opacity-30 disabled:cursor-not-allowed flex-1 sm:flex-none"
            style={{
              color: currentColor,
              borderColor: currentColor,
              boxShadow: currentPageIndex > 0 && !isTyping ? `0 0 15px ${currentColor}80` : 'none'
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
            <span className="hidden sm:inline">← Previous</span>
            <span className="sm:hidden">← Prev</span>
          </button>
          
          <button
            onClick={nextPage}
            disabled={currentPageIndex === pages.length - 1 || isTyping}
            className="px-3 py-2 sm:px-4 font-crt border transition-all text-sm
                       disabled:opacity-30 disabled:cursor-not-allowed flex-1 sm:flex-none"
            style={{
              color: currentColor,
              borderColor: currentColor,
              boxShadow: currentPageIndex < pages.length - 1 && !isTyping ? `0 0 15px ${currentColor}80` : 'none'
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
            <span className="hidden sm:inline">Next →</span>
            <span className="sm:hidden">Next →</span>
          </button>
        </div>
        
        {/* Desktop: Section info in center */}
        <div className="hidden sm:block text-xs font-crt opacity-50" style={{ color: currentColor }}>
          {isTyping ? 'Generating response...' : `Section ${currentPage.section || 1}`}
        </div>
      </div>
      
      {/* Character Chat Interfaces */}
      
      <LondonFoxChat 
        isOpen={isLondonChatOpen}
        onClose={() => setIsLondonChatOpen(false)}
      />
      
      <GlyphMarrowChat
        isOpen={isGlyphChatOpen}
        onClose={() => setIsGlyphChatOpen(false)}
      />
      
      <PhillipBafflemintChat
        isOpen={isPhillipChatOpen}
        onClose={() => setIsPhillipChatOpen(false)}
      />
      
      <JacklynVarianceChat
        isOpen={isJacklynChatOpen}
        onClose={() => setIsJacklynChatOpen(false)}
      />
      
      <OrenProgressoChat
        isOpen={isOrenChatOpen}
        onClose={() => setIsOrenChatOpen(false)}
      />
      
      <OldNatalieWeissmanChat
        isOpen={isOldNatalieChatOpen}
        onClose={() => setIsOldNatalieChatOpen(false)}
      />
      
      <NewNatalieWeissmanChat
        isOpen={isNewNatalieChatOpen}
        onClose={() => setIsNewNatalieChatOpen(false)}
      />
      
      <ArieolOwlistChat
        isOpen={isArieolChatOpen}
        onClose={() => setIsArieolChatOpen(false)}
      />
      
      <JackParlanceChat
        isOpen={isJackChatOpen}
        onClose={() => setIsJackChatOpen(false)}
      />
      
      <PrinchettaChat
        isOpen={isPrinchettaChatOpen}
        onClose={() => setIsPrinchettaChatOpen(false)}
      />
      
      <CopERightChat
        isOpen={isCopERightChatOpen}
        onClose={() => setIsCopERightChatOpen(false)}
      />
      
      <ShamrockStillmanChat
        isOpen={isShamrockChatOpen}
        onClose={() => setIsShamrockChatOpen(false)}
      />
      
      <ToddFishboneChat
        isOpen={isToddChatOpen}
        onClose={() => setIsToddChatOpen(false)}
      />
      
      {/* Real AI Streaming Chat */}
      {selectedCharacter && (
        <StreamingCharacterChat
          isOpen={isStreamingChatOpen}
          onClose={() => {
            setIsStreamingChatOpen(false);
            setSelectedCharacter(null);
          }}
          characterId={selectedCharacter.id}
          characterName={selectedCharacter.name}
          characterColor={selectedCharacter.color}
          characterInitials={selectedCharacter.initials}
        />
      )}
    </div>
  );
};

export default PageViewer;